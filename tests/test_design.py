"""Controles independientes, invariantes físicos y límites del alcance nuevo."""
import json, math
from dataclasses import replace
from pathlib import Path
import pytest
from pydantic import ValidationError
from streamlit.testing.v1 import AppTest
from src.models.project import DEFAULT_INPUT,ProjectInput
from src.models.design import DesignOptions
from src.analysis.pipeline import analyze,stage_at
from src.prestress.losses import calculate_losses
from src.checks.engineering import rectangular_flexure,shear_capacity,elastic_deflections
from src.reporting.tables import report_tables
from src.reporting.exports import json_bytes,pdf_bytes,excel_bytes
from src.validation_avance2 import run_references


def new_case(**kw): return analyze(dict(DEFAULT_INPUT,design={},**kw))

def test_loss_equilibrium_and_no_double_counting():
    r=new_case();l=r.losses;b=r.input;o=b.design;s=r.section
    # Compatibilidad independiente: ES/Ep = sigma_hormigon/Eci.
    sigma=l.transfer_force_n/s.area_m2+(l.transfer_force_n*b.eccentricity_m+r.transfer.midspan_moment_n_m)*b.eccentricity_m/s.inertia_m4
    assert l.elastic_pa/o.ep_pa == pytest.approx(sigma/o.eci_pa)
    assert b.initial_force_n-l.effective_force_n == pytest.approx(b.steel_area_m2*(l.elastic_pa+l.shrinkage_pa+l.creep_pa+l.relaxation_pa))
    r2=new_case(loss_ratio=.6)
    assert r2.service.force_n == r.service.force_n
    assert r.transfer.force_n< b.initial_force_n
    assert r.service.force_n<r.transfer.force_n


def test_centered_tendon_closed_form():
    # A=.32, e=0, n=6.5: ES=(6.5*1e6/.32)/(1+6.5*.0007/.32)
    r=new_case(eccentricity_m=0)
    assert r.losses.elastic_pa == pytest.approx(20027730.70405176)


def test_humidity_sensitivity():
    dry=analyze(dict(DEFAULT_INPUT,design={'humidity_percent':40}))
    wet=analyze(dict(DEFAULT_INPUT,design={'humidity_percent':80}))
    assert dry.losses.shrinkage_pa>wet.losses.shrinkage_pa
    assert dry.service.force_n<wet.service.force_n


def test_source_shear_control():
    sh=shear_capacity(30e6,.4,.9,.8,360192,305356.8,1403e3,.00122,1860e6,420e6,2*math.pi*.008**2/4,.25,.635,.36)
    assert sh['vc_n'] == pytest.approx(701084.873606613)
    assert sh['av_s_required_m'] == pytest.approx(.0003260253321233287)
    assert sh['av_s_provided_m']>sh['av_s_required_m']


def test_flexure_independent_equilibrium():
    f=rectangular_flexure(.4,.9,.8,.00122,30e6,1860e6,1700e6,1150e6)
    assert .85*30e6*.4*f['a_m'] == pytest.approx(.00122*f['fps_pa'])
    assert f['nominal_n_m'] == pytest.approx(.85*30e6*.4*f['a_m']*(.8-f['a_m']/2))
    assert f['c_m']*f['beta1'] == pytest.approx(f['a_m'])
    assert f['capacity_n_m']<1600000


def test_deflection_independent_curvature_integral():
    # Unidad de carga virtual central: m=x/2 en [0,L/2], simetría.
    L=10;EI=34e9*.4*.8**3/12;w=13000;p=850000;e=-.2
    N=20000;dx=L/2/N
    integral=sum(2*(w*x*(L-x)/2+p*e)*(x/2)/EI*dx for x in ((j+.5)*dx for j in range(N)))
    d=elastic_deflections(w,p,e,L,34e9,.4*.8**3/12)
    assert d['total_m']==pytest.approx(integral,abs=1e-10)

@pytest.mark.parametrize('options',[{'system':'postensado'},{'ep_pa':float('nan')},{'humidity_percent':101},{'stirrup_spacing_m':0},{'fpy_pa':2e9}])
def test_new_invalid_inputs(options):
    with pytest.raises(ValidationError):analyze(dict(DEFAULT_INPUT,design=options))


def test_no_global_pass_and_real_noncompliance():
    r=new_case();states={c['name']:c['status'] for c in r.engineering['checks']}
    assert states['Acero después de transferencia']=='NO CUMPLE'
    assert states['Flecha diferida']=='PENDIENTE'
    overload=new_case(live_load_n_m=90000)
    assert any(c['status']=='NO CUMPLE' for c in overload.engineering['checks'])


def test_limits_not_silently_accepted():
    with pytest.raises(ValueError):rectangular_flexure(.4,.9,.8,.00122,30e6,1860e6,1700e6,500e6)
    with pytest.raises(ValueError):shear_capacity(30e6,.4,.9,.8,360192,305356,1000,.00122,1860e6,420e6,.0001,.25,.635,.36)


def test_reports_use_real_losses_and_states():
    r=new_case();rep=report_tables(r)
    assert rep['memory'][8]['value']==r.service.force_n
    assert 'ES' in rep['memory'][8]['formula']
    assert len(rep['design_memory'])>=8
    assert rep['checks']
    assert json.loads(json_bytes(r,rep))['report']['engineering']['values']['mu_n_m']==220000
    assert pdf_bytes(rep).startswith(b'%PDF')
    assert excel_bytes(rep).startswith(b'PK')


def test_references(): assert run_references()['status']=='PASS'


def test_new_interface_and_invalidation():
    app=Path(__file__).resolve().parents[1]/'app/main.py'
    at=AppTest.from_file(str(app),default_timeout=40).run()
    at.checkbox(key='design_enabled').check().run()
    next(b for b in at.button if b.label=='Calcular etapas').click().run()
    assert not at.exception
    assert at.session_state['result'].engineering
    before=at.session_state['result'].service.force_n
    at.radio(key='unit_system').set_value('USCS').run()
    assert at.session_state['result'].service.force_n==before
    at.number_input(key='design_humidity_percent').set_value(60).run()
    assert not at.tabs
    next(b for b in at.button if b.label=='Calcular etapas').click().run()
    assert not at.exception
    assert at.session_state['result'].service.force_n<before


def test_transformed_concentrated_steel():
    from src.sections.transformed import transformed_rectangular
    p=transformed_rectangular(.4,.8,.0007,.2,195e9,34e9)
    assert p['net']['area_m2']==pytest.approx(.3193)
    assert p['net']['centroid_m']==pytest.approx((.32*.4-.0007*.2)/.3193)
    # Primer momento total de sección transformada calculado desde neta + n Ap.
    tr=p['transformed'];n=195/34
    assert tr['area_m2']*tr['centroid_m']==pytest.approx(.3193*p['net']['centroid_m']+n*.0007*.2)
    assert tr['inertia_m4']>.4*.8**3/12


def test_loss_scope_is_explicit():
    from src.sections.composite import template
    with pytest.raises(ValueError,match='rectángulo simple'):
        new_case(components=template('T',.4,.8))
