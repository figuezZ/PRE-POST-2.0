from pathlib import Path
import ast
import json
import pytest
from streamlit.testing.v1 import AppTest
from streamlit.proto.WidgetStates_pb2 import WidgetState
from src.models.project import DEFAULT_INPUT
from src.units import Quantity as Q, from_si

APP = Path(__file__).resolve().parents[1]/'app/main.py'


def click_calculate(at):
    next(b for b in at.button if b.label=='Calcular etapas').click().run()
    assert not at.exception


def test_rectangular_flow_units_preserved_and_stale_results():
    at = AppTest.from_file(str(APP),default_timeout=30).run()
    assert not at.exception
    click_calculate(at)
    assert len(at.tabs) == 5
    assert len(at.get('download_button')) == 3
    before = at.session_state['result']
    at.radio(key='unit_system').set_value('USCS').run()
    assert not at.exception
    assert at.number_input(key='initial_force_n').value == pytest.approx(from_si(1e6,Q.FORCE,'USCS'))
    assert at.session_state['result'].input == before.input
    click_calculate(at)
    assert at.session_state['result'].service.stress.top_pa == pytest.approx(before.service.stress.top_pa)
    at.slider(key='x_ratio').set_value(.25).run()
    assert not at.exception
    assert len(at.get('download_button')) == 3
    at.number_input(key='live_load_n_m').set_value(1.0).run()
    assert not at.exception
    assert not at.tabs
    click_calculate(at)
    at.radio(key='unit_system').set_value('SI').run()
    assert not at.exception
    assert at.number_input(key='width_m').value == pytest.approx(.4)


@pytest.mark.parametrize('shape',['T','I','Hueca'])
def test_composite_templates_and_units(shape):
    at = AppTest.from_file(str(APP),default_timeout=30).run()
    at.checkbox(key='custom_section').check().run()
    at.selectbox(key='shape').set_value(shape).run()
    next(b for b in at.button if b.label.startswith('Aplicar plantilla')).click().run()
    assert not at.exception
    click_calculate(at)
    r = at.session_state['result']
    assert len(r.section.components) >= 2
    assert r.input.eccentricity_m == pytest.approx(.08-r.section.centroid_from_bottom_m)
    at.radio(key='unit_system').set_value('USCS').run()
    assert not at.exception
    click_calculate(at)
    assert at.session_state['result'].section.inertia_m4 == pytest.approx(r.section.inertia_m4)
    at.radio(key='explorer_stage').set_value('Servicio').run()
    at.slider(key='x_ratio').set_value(0.0).run()
    assert not at.exception


def test_bad_inputs_are_explained():
    at = AppTest.from_file(str(APP),default_timeout=30).run()
    at.number_input(key='height_m').set_value(-1.0).run()
    assert not at.exception
    assert at.error
    assert next(b for b in at.button if b.label=='Calcular etapas').disabled
    at.checkbox(key='custom_section').check().run()
    next(b for b in at.button if b.label.startswith('Aplicar plantilla')).click().run()
    assert not at.exception
    assert at.error


def test_editor_edit_delete_and_reset():
    at = AppTest.from_file(str(APP),default_timeout=30).run()
    at.checkbox(key='custom_section').check().run()
    def edit(payload,calculate=False):
        # AppTest no expone edición de Dataframe. Se envía el mismo estado JSON
        # que serializa el frontend (DataEditorSerde), incluyendo otros controles.
        if calculate:
            next(b for b in at.button if b.label=='Calcular etapas').click()
        states = at._tree.get_widget_states()
        editor = next(d for d in at.dataframe if d.key and d.key.startswith('components_'))
        states.widgets.append(WidgetState(id=editor.proto.id,string_value=json.dumps(payload)))
        at._run(states)
        assert not at.exception
    change = {'edited_rows':{0:{'b':.6}},'added_rows':[],'deleted_rows':[]}
    edit(change)
    edit(change,calculate=True)
    assert at.session_state['result'].section.area_m2 == pytest.approx(.48)
    edit(change,calculate=True)
    assert at.session_state['result'].section.area_m2 == pytest.approx(.48)
    deletion = {'edited_rows':{},'added_rows':[],'deleted_rows':[0]}
    edit(deletion)
    assert at.error
    at.radio(key='unit_system').set_value('USCS')
    edit(deletion)
    assert at.error
    next(b for b in at.button if b.label=='Restablecer valores').click().run()
    assert not at.exception
    assert not at.checkbox(key='custom_section').value
    click_calculate(at)
    assert at.session_state['result'].section.area_m2 == pytest.approx(.32)


def test_core_does_not_import_interface_or_execute_js():
    root = APP.parents[1]
    for path in (root/'src').rglob('*.py'):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node,ast.ImportFrom):
                names = [node.module or '']
            else:
                continue
            assert not any(n.split('.')[0] in ('app','streamlit','subprocess') for n in names),path
