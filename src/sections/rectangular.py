from dataclasses import dataclass
from src.models.inputs import BeamInput

@dataclass
class SectionProperties:
    area_m2: float
    centroid_from_bottom_m: float
    inertia_m4: float
    section_modulus_top_m3: float
    section_modulus_bottom_m3: float
    self_weight_n_m: float
    height_m: float

def calculate_rectangular_properties(beam: BeamInput) -> SectionProperties:
    area = beam.width_m * beam.height_m
    centroid = beam.height_m / 2.0
    inertia = (beam.width_m * beam.height_m ** 3) / 12.0
    return SectionProperties(
        area_m2=area, centroid_from_bottom_m=centroid, inertia_m4=inertia,
        section_modulus_top_m3=inertia/centroid, section_modulus_bottom_m3=inertia/centroid,
        self_weight_n_m=area * beam.unit_weight_n_m3, height_m=beam.height_m
    )
