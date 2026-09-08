import streamlit as st
import pandas as st_pandas
import plotly.graph_objects as go
import io
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.inputs import BeamInput
from src.sections.rectangular import calculate_rectangular_properties
from src.analysis.elastic import uniform_load_effects, calculate_elastic_stresses, generate_beam_diagram

st.set_page_config(page_title="PRE-POST | Viga Pretensada", layout="wide")
st.title("PRE-POST | Viga pretensada")
st.info("Uso académico: herramienta en desarrollo. Versión local estructurada.")

system = st.radio("Sistema de unidades", ["SI", "USCS"], horizontal=True)
fact_l = 1.0 if system == "SI" else 3.28084 

col1, col2, col3 = st.columns(3)
with col1:
    span = st.number_input(f"Luz [{'m' if system=='SI' else 'ft'}]", value=10.0 * fact_l) / fact_l
    width = st.number_input(f"Ancho b [{'m' if system=='SI' else 'ft'}]", value=0.4 * fact_l) / fact_l
    height = st.number_input(f"Alto h [{'m' if system=='SI' else 'ft'}]", value=0.8 * fact_l) / fact_l
with col2:
    w_weight = st.number_input("Peso específico [N/m³]", value=25000.0)
    live_load = st.number_input("Carga viva [N/m]", value=5000.0)
    fci = st.number_input("f'ci [Pa]", value=35000000.0)
    fc = st.number_input("f'c [Pa]", value=45000000.0)
with col3:
    force = st.number_input("Fuerza inicial Pi [N]", value=1000000.0)
    ecc = st.number_input(f"Excentricidad e [{'m' if system=='SI' else 'ft'}]", value=-0.2 * fact_l) / fact_l
    area_s = st.number_input("Área de acero Ap [m²]", value=0.0007, format="%.5f")
    loss = st.number_input("Pérdida [%]", value=15.0)

if st.button("Calcular etapas"):
    try:
        beam = BeamInput(span_m=span, width_m=width, height_m=height, unit_weight_n_m3=w_weight, fci_pa=fci, fc_pa=fc, live_load_n_m=live_load, initial_force_n=force, eccentricity_m=ecc, steel_area_m2=area_s, loss_ratio=loss/100)
        props = calculate_rectangular_properties(beam)
        
        trans_eff = uniform_load_effects(props.self_weight_n_m, beam.span_m)
        trans_stress = calculate_elastic_stresses(props, beam.initial_force_n, beam.eccentricity_m, trans_eff.midspan_moment_n_m)
        
        eff_force = beam.initial_force_n * (1 - beam.loss_ratio)
        serv_eff = uniform_load_effects(props.self_weight_n_m + beam.live_load_n_m, beam.span_m)
        serv_stress = calculate_elastic_stresses(props, eff_force, beam.eccentricity_m, serv_eff.midspan_moment_n_m)

        tab1, tab2, tab3 = st.tabs(["Métricas", "Gráficos", "Exportar Informe"])
        
        with tab1:
            st.subheader("Resultados - Transferencia")
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Área Bruta", f"{props.area_m2:.3f} m²")
            mc2.metric("Momento Centro", f"{trans_eff.midspan_moment_n_m:,.0f} N·m")
            mc3.metric("Tensión Inf.", f"{trans_stress.bottom_pa:,.0f} Pa")
            
            st.subheader("Resultados - Servicio")
            mc4, mc5, mc6 = st.columns(3)
            mc4.metric("Fuerza Efectiva", f"{eff_force:,.0f} N")
            mc5.metric("Momento Centro", f"{serv_eff.midspan_moment_n_m:,.0f} N·m")
            mc6.metric("Tensión Inf.", f"{serv_stress.bottom_pa:,.0f} Pa")

        with tab2:
            st.markdown("### Diagramas Comparativos")
            trans_diag = generate_beam_diagram(props.self_weight_n_m, beam.span_m)
            serv_diag = generate_beam_diagram(props.self_weight_n_m + beam.live_load_n_m, beam.span_m)
            
            x_vals = [d["x"] for d in trans_diag]
            
            fig_shear = go.Figure()
            fig_shear.add_trace(go.Scatter(x=x_vals, y=[d["shear"] for d in trans_diag], name="Transferencia", line=dict(color='#2563eb')))
            fig_shear.add_trace(go.Scatter(x=x_vals, y=[d["shear"] for d in serv_diag], name="Servicio", line=dict(color='#f59e0b')))
            fig_shear.update_layout(title="Corte V(x)")
            st.plotly_chart(fig_shear, use_container_width=True)

            fig_mom = go.Figure()
            fig_mom.add_trace(go.Scatter(x=x_vals, y=[d["moment"] for d in trans_diag], name="Transferencia", line=dict(color='#2563eb')))
            fig_mom.add_trace(go.Scatter(x=x_vals, y=[d["moment"] for d in serv_diag], name="Servicio", line=dict(color='#f59e0b')))
            fig_mom.update_layout(title="Momento M(x)")
            st.plotly_chart(fig_mom, use_container_width=True)

        with tab3:
            df = st_pandas.DataFrame({
                "Propiedad": ["Luz (m)", "Área (m2)", "Inercia (m4)", "P. Propio (N/m)", "Fuerza Efectiva (N)"],
                "Valor": [beam.span_m, props.area_m2, props.inertia_m4, props.self_weight_n_m, eff_force]
            })
            st.dataframe(df, hide_index=True)
            
            buffer = io.BytesIO()
            with st_pandas.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Reporte PRE-POST')
            st.download_button(label="Descargar Reporte Excel", data=buffer.getvalue(), file_name="Reporte_PRE_POST.xlsx", mime="application/vnd.ms-excel")

    except Exception as e:
        st.error(f"Error en validación o cálculo: {e}")
