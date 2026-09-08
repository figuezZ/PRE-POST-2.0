import pytest
from src.models.inputs import BeamInput
from src.sections.rectangular import calculate_rectangular_properties

def test_rectangular_properties():
    beam = BeamInput(span_m=10.0, width_m=0.4, height_m=0.8, unit_weight_n_m3=25000.0, fci_pa=35e6, fc_pa=45e6, initial_force_n=1e6, eccentricity_m=-0.2, steel_area_m2=0.0007, loss_ratio=0.15)
    props = calculate_rectangular_properties(beam)
    assert props.area_m2 == pytest.approx(0.32)
    assert props.inertia_m4 == pytest.approx(0.0170666, rel=1e-3)
