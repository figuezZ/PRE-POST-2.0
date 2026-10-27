import json
from pathlib import Path
import pytest
from streamlit.testing.v1 import AppTest
from src.analysis.pipeline import analyze
from src.exercises.exercise1 import compare_values
from src.models.exercise1 import Exercise1Input
from src.reporting.tables import report_tables
from src.reporting.exports import json_bytes,pdf_bytes

# Referencias independientes: sustitución manual en A=bh, I=bh³/12,
# sigma=-P/A +/- Pe/W +/- Ms/W; Ap=P/fpe; bloque 0.85 fc b a.
EXPECTED={'area_m2':.36,'inertia_m4':.0243,'section_modulus_m3':.054,
 'eccentricity_m':-.35,'force_lower_n':1408459.637894,'force_upper_n':1585921.746526,
 'adopted_force_n':1410000,'steel_area_m2':.001226086956522,
 'top_stress_pa':-13296296.296296,'bottom_stress_pa':5462962.962963,
 'moment_demand_n_m':1600000,'fps_pa':1714449053.70844,
 'compression_block_m':.2060846688601,'nominal_moment_n_m':1465049.355129,
 'capacity_n_m':1318544.419616}

def test_reference_and_equilibrium():
    r=analyze(Exercise1Input());v=r['values']
    for k,x in EXPECTED.items():assert v[k]==pytest.approx(x,rel=1e-9)
    assert v['tension_u_pa']<v['bottom_stress_pa']<v['tension_c_pa']
    assert .85*30e6*.4*v['compression_block_m']==pytest.approx(v['tensile_force_n'])
    assert r['checks'][1]['status']=='NO CUMPLE'
    assert 1e6/.054-1403e3*(1/.36+.35/.054)>v['tension_c_pa']

def test_comparison_and_exports():
    r=analyze(Exercise1Input());report=report_tables(r)
    assert compare_values(r,{'adopted_force_n':1410000})[0]['absolute_error']==0
    assert compare_values(r,{'adopted_force_n':0})[0]['relative_error_percent'] is None
    with pytest.raises(ValueError):compare_values(r,{'area_m2':float('nan')})
    assert json.loads(json_bytes(r,report))['input_si']==r['input_si']
    assert pdf_bytes(report).startswith(b'%PDF')

@pytest.mark.parametrize('change',[{'steel_depth_m':.9},{'fc_pa':float('nan')},{'force_rounding_n':2e6}])
def test_invalid_inputs(change):
    with pytest.raises(ValueError):analyze({**Exercise1Input().model_dump(),**change})

def test_sensitivity():
    a=analyze(Exercise1Input());b=analyze({**Exercise1Input().model_dump(),'service_moment_n_m':1.1e6})
    assert b['values']['adopted_force_n']>a['values']['adopted_force_n']
    assert b['values']['moment_demand_n_m']==1760000

def test_default_app_and_invalidation():
    at=AppTest.from_file(str(Path(__file__).parents[1]/'app/main.py'),default_timeout=30).run()
    assert not at.exception
    assert not at.selectbox
    assert len(list((Path(__file__).parents[1]/'examples').glob('*.json')))==1
    next(b for b in at.button if b.label=='Calcular ejercicio 1').click().run()
    assert not at.exception
    assert 'exercise_result' in at.session_state
    at.number_input(key='ex1_service_moment_n_m').set_value(1100).run()
    assert 'exercise_result' not in at.session_state


def test_rejects_retired_beam_case():
    with pytest.raises(ValueError):
        analyze({'span_m':10,'initial_force_n':1000000,'loss_ratio':.15})
