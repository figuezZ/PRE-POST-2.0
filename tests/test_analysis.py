from dataclasses import asdict
import json
from pathlib import Path
import shutil
import subprocess
import pytest
from src.models.project import DEFAULT_INPUT, ProjectInput
from src.sections.composite import template, component_properties, tendon_eccentricity, append_component
from src.analysis.pipeline import (analyze, stage_at, fiber_at, diagrams, selected_coordinates,
    stress_profile, stress_field, stress_scale)
from src.analysis.memory import calculation_memory
from src.validation import validate_all


def data_for(shape):
    if shape == 'Rectangular':
        return dict(DEFAULT_INPUT)
    parts = template(shape,.4,.8)
    sec = component_properties(parts,25000)
    return {**DEFAULT_INPUT,'components':[p.model_dump() for p in parts],
            'eccentricity_m':tendon_eccentricity(sec)}


def test_manual_validation():
    assert validate_all()['status'] == 'PASS'


def test_editor_shortcuts():
    parts = template('Rectangular',.4,.8)
    solid = append_component(parts,'solid',25000)
    assert solid[-1].y == .8
    assert solid[-1].h == pytest.approx(.12)
    hole = append_component(parts,'hole',25000)
    assert hole[-1].sign == -1
    assert component_properties(hole,25000).area_m2 == pytest.approx(.32-.12*.24)
    with pytest.raises(ValueError,match='superponerse'):
        append_component(hole,'hole',25000)


@pytest.mark.parametrize('shape',['Rectangular','T','I','Hueca'])
@pytest.mark.parametrize('stage',['transfer','service'])
def test_equilibrium(shape,stage):
    r = analyze(data_for(shape))
    sec = r.section
    # Integrales independientes desde la base: A, integral(y), integral(y²).
    a = sum(p.sign*p.b*p.h for p in sec.components)
    first = sum(p.sign*p.b*((p.y+p.h)**2-p.y**2)/2 for p in sec.components)
    second = sum(p.sign*p.b*((p.y+p.h)**3-p.y**3)/3 for p in sec.components)
    cy = first/a
    inertia = second-first*first/a
    assert sec.inertia_m4 == pytest.approx(inertia,rel=1e-12)
    for x in (0,2.5,5,10):
        s = stage_at(r,stage,x)
        assert s.stress.axial_component_pa*a+s.slope*(first-cy*a) == pytest.approx(-s.force)
        assert s.stress.axial_component_pa*(first-cy*a)+s.slope*inertia == pytest.approx(-s.stress.resultant_moment_n_m)
        profile = stress_profile(r,stage,x)
        assert profile[0]['stress'] == pytest.approx(s.stress.bottom_pa)
        assert profile[-1]['stress'] == pytest.approx(s.stress.top_pa)
        mem = calculation_memory(r,stage,x)
        assert len(mem) == 19
        assert mem[-2]['value'] == pytest.approx(s.stress.top_pa)
        assert mem[-1]['value'] == pytest.approx(s.stress.bottom_pa)
        f = fiber_at(r,stage,x,0)
        assert f['stress'] == pytest.approx(f['axial']+f['prestress']+f['external'])
        if s.zero_inside:
            assert fiber_at(r,stage,x,s.zero)['stress'] == pytest.approx(0,abs=1e-8)


@pytest.mark.parametrize('field,value',[
    ('span_m',0),('width_m',-1),('height_m',0),('unit_weight_n_m3',float('inf')),
    ('eccentricity_m',float('nan')),('eccentricity_m',.4),('fc_pa',34e6),
    ('initial_force_n',2e6),('steel_area_m2',0),('loss_ratio',1),('loss_ratio',-.1),
    ('live_load_n_m',-1),('dead_load_n_m',-1)])
def test_invalid_input(field,value):
    with pytest.raises(ValueError):
        analyze({**DEFAULT_INPUT,field:value})


@pytest.mark.parametrize('parts',[
    [], [{'b':.4,'h':.8,'y':.1}],
    [{'b':.4,'h':.4,'y':0},{'b':.4,'h':.4,'y':.3}],
    [{'b':.4,'h':.4,'y':0},{'b':.4,'h':.4,'y':.5}],
    [{'b':.4,'h':.8,'y':0},{'b':.4,'h':.2,'y':.2,'sign':-1}],
    [{'b':.4,'h':.8,'y':0},{'b':.2,'h':.8,'y':0,'sign':-1}],
    [{'b':.4,'h':.8,'y':0},{'b':.2,'h':.3,'y':.2,'sign':-1},{'b':.1,'h':.3,'y':.3,'sign':-1}],
])
def test_invalid_components(parts):
    with pytest.raises(ValueError):
        component_properties(parts,25000)


def test_void_and_loads_and_selection():
    data = data_for('Hueca')
    with pytest.raises(ValueError,match='vacíos'):
        analyze({**data,'eccentricity_m':0})
    r = analyze({**DEFAULT_INPUT,'dead_load_n_m':2000})
    assert r.service.uniform_load_n_m == pytest.approx(15000)
    assert r.service.stress.top_pa == pytest.approx(-3066406.25)
    assert selected_coordinates(r,.5,1) == pytest.approx((5,.4))
    points = diagrams(r,'service')
    assert points[0]['moment'] == points[-1]['moment'] == 0
    assert points[50]['shear'] == pytest.approx(0)
    assert points[50]['moment'] == pytest.approx(r.service.midspan_moment_n_m)
    hollow = analyze(data)
    xs,ys,z = stress_field(hollow,'service',5)
    assert any(v is None for row in z for v in row)
    assert all(v is None or abs(v) <= stress_scale(hollow) for row in z for v in row)
    for call in [lambda: stage_at(r,'other',0),lambda: stage_at(r,'service',11),
                 lambda: fiber_at(r,'transfer',0,.5),lambda: diagrams(r,'service',1),
                 lambda: stress_profile(r,'transfer',0,1),lambda: selected_coordinates(r,2,0),
                 lambda: stress_field(r,'service',0,1,1)]:
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize('shape',['Rectangular','T','I','Hueca'])
def test_migration_against_original_javascript(shape):
    node = shutil.which('node')
    if node is None:
        pytest.skip('Node solo se requiere para la prueba de migración; CI lo instala.')
    data = data_for(shape)
    reference = Path(__file__).parent/'reference/prepost_v0_7_core.js'
    code = reference.read_text()+'''\nconst data=JSON.parse(require('fs').readFileSync(0,'utf8'));
const r=PrePostCore.analyze(data);
const positions=['transfer','service'].flatMap(s=>[0,2.5,5,10].map(x=>({stage:s,x,
  at:PrePostCore.stageAt(r,s,x),memory:PrePostCore.memory(r,s,x),fiber:PrePostCore.fiberAt(r,s,x,0)})));
process.stdout.write(JSON.stringify({r,positions}));'''
    old = json.loads(subprocess.run([node,'-e',code],input=json.dumps(data),text=True,capture_output=True,check=True).stdout)
    r = analyze(data)
    for field in ('area_m2','gross_area_m2','centroid_from_bottom_m','inertia_m4','gross_inertia_m4',
                  'section_modulus_top_m3','section_modulus_bottom_m3','self_weight_n_m'):
        assert getattr(r.section,field) == pytest.approx(old['r']['section'][field],rel=1e-12)
    for item in old['positions']:
        s,x = item['stage'],item['x']
        new = stage_at(r,s,x)
        for field in ('force','w','reaction','shear','moment','slope'):
            assert getattr(new,field) == pytest.approx(item['at'][field],rel=1e-12,abs=1e-8)
        assert asdict(new.stress) == pytest.approx(item['at']['stress'],rel=1e-12,abs=1e-8)
        assert [m['value'] for m in calculation_memory(r,s,x)] == pytest.approx([m['value'] for m in item['memory']],rel=1e-12,abs=1e-8)
        for field in ('stress','axial','prestress','external'):
            assert fiber_at(r,s,x,0)[field] == pytest.approx(item['fiber'][field],rel=1e-12,abs=1e-8)
