from dataclasses import dataclass
from src.sections.rectangular import SectionProperties

@dataclass
class LoadEffects:
    reaction_n: float
    max_shear_n: float
    midspan_moment_n_m: float

@dataclass
class ElasticStresses:
    top_pa: float
    bottom_pa: float
    axial_component_pa: float
    prestress_moment_n_m: float
    external_moment_n_m: float
    resultant_moment_n_m: float

def uniform_load_effects(w_n_m: float, span_m: float) -> LoadEffects:
    reaction = w_n_m * span_m / 2
    return LoadEffects(reaction_n=reaction, max_shear_n=reaction, midspan_moment_n_m=w_n_m * span_m**2 / 8)

def calculate_elastic_stresses(section: SectionProperties, force_n: float, eccentricity_m: float, ext_moment_n_m: float) -> ElasticStresses:
    prestress_moment = force_n * eccentricity_m
    resultant_moment = prestress_moment + ext_moment_n_m
    axial = -force_n / section.area_m2
    top_y = section.height_m / 2
    return ElasticStresses(
        top_pa=axial - resultant_moment * top_y / section.inertia_m4,
        bottom_pa=axial + resultant_moment * top_y / section.inertia_m4,
        axial_component_pa=axial, prestress_moment_n_m=prestress_moment,
        external_moment_n_m=ext_moment_n_m, resultant_moment_n_m=resultant_moment
    )

def generate_beam_diagram(w_n_m: float, span_m: float, count: int = 101):
    reaction = w_n_m * span_m / 2
    return [{"x": span_m * i / (count - 1), 
             "shear": reaction - w_n_m * (span_m * i / (count - 1)), 
             "moment": reaction * (span_m * i / (count - 1)) - w_n_m * (span_m * i / (count - 1))**2 / 2} 
            for i in range(count)]
