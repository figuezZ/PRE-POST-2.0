"""Interfaz del ejercicio del set: entradas, instantánea y cotejo manuscrito."""
import json
import pandas as pd
import streamlit as st
from src.models.exercise1 import Exercise1Input
from src.analysis.pipeline import analyze
from src.exercises.exercise1 import compare_values
from src.reporting.exercise1 import FIELDS
from src.reporting.tables import report_tables
from src.reporting.exports import json_bytes,pdf_bytes

INPUTS=[('width_m','Ancho b (m)',1),('height_m','Altura h (m)',1),('steel_depth_m','Profundidad dp (m)',1),
 ('fc_pa',"Resistencia fc (MPa)",1e6),('service_moment_n_m','Momento de servicio (kN m)',1000),
 ('effective_steel_stress_pa','Tensión efectiva fpe (MPa)',1e6),('fpy_pa','fpy (MPa)',1e6),
 ('fpu_pa','fpu adoptado para grado 270 (MPa)',1e6),('moment_factor','Factor Mu / Ms',1),
 ('force_rounding_n','Incremento para adoptar P por exceso (kN)',1000)]

def invalidate():
    st.session_state.pop('exercise_result',None)
    st.session_state.pop('manual_comparison',None)

def reset():
    invalidate()
    for key,label,scale in INPUTS:st.session_state['ex1_'+key]=Exercise1Input().model_dump()[key]/scale
    st.session_state['ex1_revision']=st.session_state.get('ex1_revision',0)+1

def render_exercise1():
    st.title('Ejercicio 1 del set · manual y software')
    st.caption('Fuente: SET DE EJERCICIOS PARA AVANCE 2, pp. 1–3. Flexión simple de sección rectangular.')
    st.info('Usamos el momento de servicio del enunciado: 1000 kN m. No se necesitan luz, carga distribuida ni un porcentaje supuesto de pérdidas.')
    st.button('Restablecer ejercicio del set',on_click=reset)
    defaults=Exercise1Input().model_dump(); data={'case_type':'set_ejercicio_1'}
    cols=st.columns(2)
    for i,(key,label,scale) in enumerate(INPUTS):
        with cols[i%2]:
            data[key]=st.number_input(label,value=float(defaults[key]/scale),format='%.6f',key='ex1_'+key,on_change=invalidate)*scale
    st.caption('Adopciones explícitas: incremento de 10 kN y fpu = 1860 MPa. Área activa teórica; no constituye selección de cantidad de torones.')
    if st.button('Calcular ejercicio 1',type='primary'):
        invalidate()
        try:st.session_state['exercise_result']=analyze(data)
        except (ValueError,TypeError) as exc:st.error(str(exc))
    result=st.session_state.get('exercise_result')
    if result is None:return
    report=report_tables(result)
    st.dataframe(pd.DataFrame(report['tables']['Resultados']),hide_index=True)
    for c in result['checks']:
        (st.warning if c['status']=='NO CUMPLE' else st.info)(c['name']+': '+c['status'])
    st.caption(result['normative_status'])
    with st.expander('Diferencias respecto a los resultados impresos del set'):
        st.write('La guía publica P = 1403 kN y Ap = 1220 mm². Con sus datos, P = 1403 kN produce 5.527778 MPa en la fibra inferior, por encima de sqrt(30) = 5.477226 MPa. La resolución revisada adopta P = 1410 kN y recalcula Ap. Esta observación corresponde a los datos originales, no a entradas modificadas.')
        st.write('La resistencia revisada usa el procedimiento CIRSOC ya implementado, diferente de la simplificación de la guía; la norma para la entrega aún requiere ratificación docente.')
    st.subheader('Comparar con tu desarrollo manuscrito')
    st.write('Ingresa tus resultados en las unidades indicadas. Los campos vacíos no se comparan. No se rellenan automáticamente como si fueran un cálculo manual.')
    available=[f for f in FIELDS if f[0] in result['values']]
    frame=pd.DataFrame([{'Magnitud':label,'Unidad':unit,'Manual':None} for _,label,unit,_ in available])
    edited=st.data_editor(frame,hide_index=True,disabled=['Magnitud','Unidad'],key='manual_ex1_'+str(st.session_state.get('ex1_revision',0)),
        column_config={'Manual':st.column_config.NumberColumn('Manual',format='%.9f')})
    if st.button('Comparar resultados'):
        manual={key:float(edited.iloc[i]['Manual'])*scale for i,(key,_,_,scale) in enumerate(available) if pd.notna(edited.iloc[i]['Manual'])}
        rows=compare_values(result,manual)
        shown=[]
        for row in rows:
            _,label,unit,scale=next(f for f in available if f[0]==row['quantity'])
            shown.append({'Magnitud':label,'Unidad':unit,'Manual':row['manual']/scale,'Software':row['software']/scale,'Diferencia absoluta':row['absolute_error']/scale,'Error relativo (%)':row['relative_error_percent']})
        if shown:
            st.dataframe(pd.DataFrame(shown),hide_index=True)
            payload={'input_si':result['input_si'],'comparison':rows,'note':'Valores ingresados por usuario; autoría y revisión no acreditadas automáticamente.'}
            st.download_button('Descargar comparación JSON',json.dumps(payload,ensure_ascii=False,indent=2).encode(),'comparacion_ejercicio1.json','application/json')
        else:st.info('Ingresa al menos un resultado manual para comparar.')
    st.download_button('Descargar resultados JSON',json_bytes(result,report),'ejercicio1.json','application/json')
    st.download_button('Descargar memoria PDF',pdf_bytes(report),'ejercicio1.pdf','application/pdf')
    for item in result['not_applicable']:st.caption(item)
