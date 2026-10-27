"""Entrada Streamlit: no contiene ecuaciones estructurales ni un núcleo JS."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st
from src.models.project import ProjectInput, DEFAULT_INPUT
from src.models.design import DesignOptions
from src.sections.composite import template, component_properties, tendon_eccentricity, append_component
from src.analysis.pipeline import analyze, selected_coordinates, fiber_at
from src.reporting.tables import INPUT_FIELDS, CONVENTIONS, report_tables
from src.reporting.exports import excel_bytes, pdf_bytes, json_bytes
from src.units import Quantity as Q, display_unit, from_si, to_si
from app.plots import beam_plots, profile_plot, section_plot, LABELS


def invalidate():
    st.session_state.pop('result', None)


def initialize():
    ss = st.session_state
    if 'units_previous' not in ss:
        ss['units_previous'] = ss['unit_system'] = 'SI'
        ss['editor_revision'] = 0
        ss['components_si'] = []
        ss['editor_base_si'] = None
        for field, _, q in INPUT_FIELDS:
            ss[field] = from_si(DEFAULT_INPUT[field],q,'SI')
        ss['loss_percent'] = DEFAULT_INPUT['loss_ratio']*100


def change_units():
    ss = st.session_state
    old, new = ss['units_previous'], ss['unit_system']
    for field, _, q in INPUT_FIELDS:
        ss[field] = from_si(to_si(ss[field],q,old),q,new)
    ss['units_previous'] = new
    ss['editor_revision'] += 1
    if ss['editor_base_si'] is not None:
        ss['editor_base_si'] = ss['components_si']


def apply_template():
    ss = st.session_state
    invalidate()
    try:
        b = to_si(ss['width_m'],Q.SECTION_LENGTH,ss['unit_system'])
        h = to_si(ss['height_m'],Q.SECTION_LENGTH,ss['unit_system'])
        parts = template(ss['shape'],b,h)
        sec = component_properties(parts, to_si(ss['unit_weight_n_m3'],Q.UNIT_WEIGHT,ss['unit_system']))
        ss['components_si'] = [p.model_dump() for p in parts]
        ss['editor_base_si'] = ss['components_si']
        ss['eccentricity_m'] = from_si(tendon_eccentricity(sec),Q.SECTION_LENGTH,ss['unit_system'])
        ss['editor_revision'] += 1
    except (ValueError,OverflowError,ZeroDivisionError) as exc:
        ss['template_error'] = str(exc)


def read_input(system, components):
    data = {field:to_si(st.session_state[field],q,system) for field,_,q in INPUT_FIELDS}
    return ProjectInput(**data,loss_ratio=st.session_state['loss_percent']/100,
        project=st.session_state['project'],author=st.session_state['author'],components=components,
        design=st.session_state.get('design_options') if st.session_state.get('design_enabled') else None)


def add_component(kind):
    ss = st.session_state
    invalidate()
    try:
        parts = append_component(ss['components_si'],kind,
            to_si(ss['unit_weight_n_m3'],Q.UNIT_WEIGHT,ss['unit_system']))
        ss['components_si'] = ss['editor_base_si'] = [p.model_dump() for p in parts]
        ss['editor_revision'] += 1
    except (ValueError,OverflowError,ZeroDivisionError) as exc:
        ss['template_error'] = str(exc)


def reset_values():
    ss = st.session_state
    invalidate()
    for field,_,q in INPUT_FIELDS:
        ss[field] = from_si(DEFAULT_INPUT[field],q,ss['unit_system'])
    ss['loss_percent'] = 15.0
    ss['custom_section'] = False
    ss['design_enabled'] = False
    ss['components_si'] = []
    ss['editor_base_si'] = None
    ss['editor_revision'] += 1
    ss['x_ratio'],ss['y_ratio'] = .5,1.0



def main():
    st.set_page_config(page_title='PRE-POST 2.0 | Viga pretensada',layout='wide')
    initialize()
    st.title('PRE-POST 2.0 | Viga pretensada')
    st.caption('ICIV 1042 · Transferencia y servicio · Núcleo modular en Python')
    st.info('Uso académico. Viga simplemente apoyada, carga uniforme y un tendón equivalente. Modo histórico o extensión preliminar de pérdidas y verificaciones.')
    system = st.radio('Sistema de unidades',['SI','USCS'],horizontal=True,key='unit_system',on_change=change_units)
    st.button('Restablecer valores',on_click=reset_values)
    c1,c2 = st.columns(2)
    c1.text_input('Proyecto',value='PRE-POST',key='project',on_change=invalidate)
    c2.text_input('Autor / equipo',key='author',on_change=invalidate)
    st.subheader('1. Ingreso de datos')
    cols = st.columns(3)
    for index,(field,label,q) in enumerate(INPUT_FIELDS):
        with cols[index%3]:
            st.number_input(f'{label} [{display_unit(system,q).symbol}]',key=field,format='%.8f',on_change=invalidate)
    cols[2].number_input('Pérdida declarada [%]',key='loss_percent',on_change=invalidate)
    st.caption('e positivo hacia arriba; un tendón inferior usa e negativo. Carga muerta adicional excluye el peso propio.')
    st.checkbox('Activar pérdidas y verificaciones del Avance 2',key='design_enabled',on_change=invalidate)
    if st.session_state['design_enabled']:
        with st.expander('Materiales y criterios del Avance 2 — entradas SI explícitas',expanded=True):
            st.warning('PRELIMINAR. Solo pretesado recto adherente rectangular. CIRSOC 201-2005 como referencia; adopción USS pendiente. Flecha diferida y extremos sin verificar.')
            method = st.selectbox('Método de pérdidas',['fhwa_2003','declarada'],key='new_loss_method',on_change=invalidate)
            defaults=DesignOptions().model_dump()
            fields=[('ep_pa','Ep [Pa]'),('eci_pa','Eci [Pa]'),('ec_pa','Ec [Pa]'),
                ('humidity_percent','Humedad relativa [%]'),('fpu_pa','fpu [Pa]'),('fpy_pa','fpy [Pa]'),
                ('stirrup_fy_pa','fy estribos [Pa]'),('stirrup_diameter_m','Diámetro estribo [m]'),
                ('stirrup_spacing_m','Separación estribos [m]'),('strand_diameter_m','Diámetro cordón [m]'),
                ('live_deflection_divisor','Divisor límite flecha viva L/n')]
            options={'loss_method':method}
            newcols=st.columns(2)
            for j,(field,label) in enumerate(fields):
                options[field]=newcols[j%2].number_input(label,value=float(defaults[field]),key='design_'+field,on_change=invalidate,format='%.6g')
            options['stirrup_legs']=st.number_input('Ramas de estribos',value=2,min_value=2,max_value=8,key='design_legs',on_change=invalidate)
            st.session_state['design_options']=options
            st.caption('El modo FHWA usa P0 antes de transferencia y descarta el porcentaje global. Baja relajación; método histórico de estimación. Los valores precargados son supuestos ilustrativos, no datos confirmados del equipo.')
    st.subheader('Editor de sección (opcional)')
    st.checkbox('Usar sección compuesta',key='custom_section',on_change=invalidate)
    components = []
    geometry_error = None
    if st.session_state['custom_section']:
        st.selectbox('Plantilla',['Rectangular','T','I','Hueca'],key='shape')
        st.button('Aplicar plantilla (reemplaza componentes)',on_click=apply_template)
        buttons = st.columns(2)
        buttons[0].button('Agregar sólido arriba',on_click=add_component,args=('solid',))
        buttons[1].button('Agregar vacío centrado',on_click=add_component,args=('hole',))
        if 'template_error' in st.session_state:
            st.error(st.session_state.pop('template_error'))
        st.caption('Ancho y alto de plantilla se aplican con el botón. Este también sitúa el tendón al 10 % del alto desde la base. '
            'Edite filas para agregar o eliminar sólidos (+1) y vacíos (-1). Todos están centrados horizontalmente; '
            'los sólidos se apilan sin separación y cada vacío pertenece a un sólido.')
        if st.session_state['editor_base_si'] is None:
            st.session_state['editor_base_si'] = [p.model_dump() for p in template('Rectangular',DEFAULT_INPUT['width_m'],DEFAULT_INPUT['height_m'])]
        rows = [{**p,**{k:from_si(p[k],Q.SECTION_LENGTH,system) for k in ('b','h','y')}} for p in st.session_state['editor_base_si']]
        symbol = display_unit(system,Q.SECTION_LENGTH).symbol
        edited = st.data_editor(pd.DataFrame(rows,columns=['name','sign','b','h','y']),num_rows='dynamic',hide_index=True,
            key=f"components_{st.session_state['editor_revision']}",on_change=invalidate,
            column_config={'name':'Nombre','sign':st.column_config.SelectboxColumn('Signo',options=[1,-1],required=True),
                **{k:st.column_config.NumberColumn(f'{label} [{symbol}]',format='%.8f',required=True)
                    for k,label in [('b','Ancho'),('h','Alto'),('y','Y inferior desde base')]}})
        try:
            components = [{**p,**{k:to_si(p[k],Q.SECTION_LENGTH,system) for k in ('b','h','y')}} for p in edited.to_dict('records')]
            st.session_state['components_si'] = components
        except (ValueError,TypeError) as exc:
            geometry_error = str(exc)
    try:
        if geometry_error:
            raise ValueError(geometry_error)
        beam = read_input(system,components)
        if st.session_state['custom_section'] and not components:
            raise ValueError('Agregue al menos un componente.')
        preview = component_properties(beam.components or template('Rectangular',beam.width_m,beam.height_m),beam.unit_weight_n_m3)
        with st.expander('Vista de la sección, centroide y tendón',expanded=True):
            st.plotly_chart(section_plot(preview,beam.eccentricity_m,system),use_container_width=True,key='preview')
    except (ValueError,TypeError,OverflowError,ZeroDivisionError) as exc:
        beam = None
        invalidate()
        st.error(f'Revise las entradas: {exc}')
    st.subheader('2. Cálculo')
    if st.button('Calcular etapas',type='primary',disabled=beam is None):
        try:
            st.session_state['result'] = analyze(beam)
        except (ValueError,OverflowError,ZeroDivisionError) as exc:
            invalidate()
            st.error(f'Error en validación o cálculo: {exc}')
    result = st.session_state.get('result')
    if result is None:
        return
    st.success('Cálculo actualizado. Los resultados siguientes corresponden a las entradas calculadas.')
    panels = st.tabs(['3. Resultados','4. Validación y reportes'])
    with panels[0]:
        tabs = [st.container(),st.expander('Diagramas esenciales'),st.expander('Explorar tensiones')]
    with panels[1]:
        tabs += [st.expander('Desarrollo del cálculo'),st.container()]
    if result.engineering:
        with panels[0]:
            st.warning(result.engineering['warning'])
            st.dataframe(pd.DataFrame(result.engineering['checks'])[['name','demand','capacity','unit','ratio','status']],hide_index=True)
            st.caption('Estados parciales; CUMPLE CRITERIO no significa cumplimiento global. Validación manual del grupo pendiente.')
    with tabs[2]:
        label = st.radio('Etapa a explorar',list(LABELS.values()),horizontal=True,key='explorer_stage')
        stage = next(k for k,v in LABELS.items() if v == label)
        xr = st.slider('Posición x/L',0.0,1.0,.5,.005,key='x_ratio')
        yr = st.slider('Fibra Y/h desde la base',0.0,1.0,1.0,.005,key='y_ratio')
        x,y = selected_coordinates(result,xr,yr)
        st.plotly_chart(section_plot(result.section,result.input.eccentricity_m,system,result,stage,x,y),
            use_container_width=True,key='stress_map')
        st.caption('Azul: compresión. Rojo: tracción. Escala fija común a ambas etapas y toda la luz. '
            'El centroide y la línea de tensión cero son distintos. Los colores no representan límites admisibles.')
        if not fiber_at(result,stage,x,y)['concrete']:
            st.info('La fibra sobre el eje central está en un vacío o borde: se muestra la prolongación del campo elástico.')
    report = report_tables(result,system,stage,x,y)
    with tabs[0]:
        for name in ('Sección','Transferencia','Servicio','Pérdidas','Verificaciones numéricas','Sección auxiliar'):
            if name not in report['tables']: continue
            st.subheader(name)
            st.dataframe(pd.DataFrame(report['tables'][name]),hide_index=True,use_container_width=True)
        st.caption('Transferencia y servicio se resumen en el centro de luz. El explorador y la memoria usan la posición elegida.')
    with tabs[1]:
        for j,fig in enumerate(beam_plots(result,system)):
            st.plotly_chart(fig,use_container_width=True,key=f'beam_{j}')
        st.plotly_chart(profile_plot(result,system,x),use_container_width=True,key='profile')
    with tabs[2]:
        st.dataframe(pd.DataFrame(report['tables']['Explorador']),hide_index=True,use_container_width=True)
    with tabs[3]:
        st.caption(f'Memoria en SI base (m, N, Pa). Etapa: {label}; x = {x:.6g} m.')
        st.dataframe(pd.DataFrame(report['components']),hide_index=True,use_container_width=True)
        st.caption('Componentes: b, h, y, centroid y d en m; area en m²; own y parallel en m⁴. Los vacíos llevan signo negativo.')
        for j,step in enumerate(report['memory']+report.get('design_memory',[]),1):
            with st.expander(f"{j}. {step['label']} = {step['value']:.7g} {step['unit']}"):
                st.code(step['formula'],language=None)
                st.text(step['substitution'])
                st.caption(step['reference'])
    with tabs[4]:
        if st.button('Ejecutar casos de referencia',key='run_references'):
            from src.validation_avance2 import run_references
            summary=run_references()
            st.json(summary)
        st.caption('Respaldo con papel y lápiz pendiente. Consulte docs/fichas_manuales.md y la matriz de cobertura.')
        st.write('Entradas, propiedades, ambas etapas, fibra elegida y memoria de 19 pasos. Las descargas conservan valores numéricos y unidades.')
        st.caption('Excel y PDF son instantáneas tabuladas; JSON conserva las entradas en SI. Los gráficos interactivos se consultan en la plataforma.')
        st.download_button('Descargar Excel',excel_bytes(report),'PRE_POST_2_0.xlsx',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',key='download_excel')
        st.download_button('Descargar PDF',pdf_bytes(report),'PRE_POST_2_0.pdf','application/pdf',key='download_pdf')
        st.download_button('Descargar datos JSON',json_bytes(result,report),'PRE_POST_2_0.json','application/json',key='download_json')
    st.caption(CONVENTIONS)


if __name__ == '__main__':
    main()
