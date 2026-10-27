"""Orquestación única en SI. Estática y superposición elástica: docs/formulas.md."""
from dataclasses import asdict, dataclass
from math import isfinite
from typing import Literal
from src.models.project import ProjectInput
from src.sections.composite import CompositeProperties, component_properties, contains_concrete, template
from src.sections.rectangular import calculate_rectangular_properties
from src.analysis.elastic import ElasticStresses, calculate_elastic_stresses, uniform_load_effects, generate_beam_diagram


@dataclass(frozen=True)
class Stage:
    force_n: float
    steel_stress_pa: float
    uniform_load_n_m: float
    reaction_n: float
    max_shear_n: float
    midspan_moment_n_m: float
    stress: ElasticStresses


@dataclass(frozen=True)
class AnalysisResult:
    input: ProjectInput
    section: CompositeProperties
    transfer: Stage
    service: Stage
    losses: object | None = None
    engineering: dict | None = None


@dataclass(frozen=True)
class PositionResult:
    x: float
    force: float
    w: float
    reaction: float
    shear: float
    moment: float
    stress: ElasticStresses
    slope: float
    zero: float | None
    zero_inside: bool


def stresses(section, force, eccentricity, moment) -> ElasticStresses:
    # El archivo literal del documento usa h/2. Es correcto para el rectángulo.
    if abs(section.centroid_from_bottom_m-section.height_m/2) < 1e-14:
        return calculate_elastic_stresses(section, force, eccentricity, moment)
    mp = force*eccentricity
    mr = mp+moment
    axial = -force/section.area_m2
    return ElasticStresses(axial-mr*(section.height_m-section.centroid_from_bottom_m)/section.inertia_m4,
        axial+mr*section.centroid_from_bottom_m/section.inertia_m4, axial, mp, moment, mr)


def effective_force(initial_force: float, loss_ratio: float) -> float:
    """Pe=(1-r)Pi; r es un dato declarado, no una predicción de pérdidas."""
    return initial_force*(1-loss_ratio)


def analyze(data: ProjectInput | dict) -> AnalysisResult:
    beam = ProjectInput.model_validate(data)
    parts = beam.components or template('Rectangular', beam.width_m, beam.height_m)
    section = component_properties(parts, beam.unit_weight_n_m3)
    if not beam.components:
        # Usa las funciones exactas solicitadas para el alcance rectangular base.
        base = calculate_rectangular_properties(beam)
        for key, value in asdict(base).items():
            setattr(section, key, value)
    if not contains_concrete(parts, 0, section.centroid_from_bottom_m+beam.eccentricity_m):
        raise ValueError('El centro del tendón debe estar dentro del hormigón y fuera de vacíos.')
    def stage(force, load):
        effects = uniform_load_effects(load, beam.span_m)
        stress = stresses(section, force, beam.eccentricity_m, effects.midspan_moment_n_m)
        values = [force/beam.steel_area_m2, *asdict(effects).values(), *asdict(stress).values()]
        if not all(isfinite(v) for v in values):
            raise ValueError('Resultados fuera del rango numérico. Revise las unidades.')
        return Stage(force, force/beam.steel_area_m2, load, effects.reaction_n,
            effects.max_shear_n, effects.midspan_moment_n_m, stress)
    from dataclasses import replace
    from src.prestress.losses import calculate_losses
    from src.checks.engineering import evaluate
    losses = calculate_losses(beam, section, beam.design) if beam.design else None
    transfer_force = losses.transfer_force_n if losses else beam.initial_force_n
    service_force = losses.effective_force_n if losses else effective_force(beam.initial_force_n, beam.loss_ratio)
    result = AnalysisResult(beam, section,
        stage(transfer_force, section.self_weight_n_m),
        stage(service_force, section.self_weight_n_m+beam.dead_load_n_m+beam.live_load_n_m),losses)
    return replace(result, engineering=evaluate(result,beam.design)) if beam.design else result


def stage_at(result: AnalysisResult, stage: Literal['transfer', 'service'], x: float) -> PositionResult:
    if stage not in ('transfer', 'service'):
        raise ValueError('Etapa inválida.')
    if not isfinite(x) or not 0 <= x <= result.input.span_m:
        raise ValueError('Posición fuera de la luz.')
    s = getattr(result, stage)
    moment = s.reaction_n*x-s.uniform_load_n_m*x*x/2
    stress = stresses(result.section, s.force_n, result.input.eccentricity_m, moment)
    slope = -stress.resultant_moment_n_m/result.section.inertia_m4
    zero = None if abs(slope) < 1e-12 else -stress.axial_component_pa/slope
    cy = result.section.centroid_from_bottom_m
    return PositionResult(x, s.force_n, s.uniform_load_n_m, s.reaction_n,
        s.reaction_n-s.uniform_load_n_m*x, moment, stress, slope, zero,
        zero is not None and -cy <= zero <= result.section.height_m-cy)


def fiber_at(result, stage, x, y) -> dict:
    cy = result.section.centroid_from_bottom_m
    if not isfinite(y) or not -cy-1e-10 <= y <= result.section.height_m-cy+1e-10:
        raise ValueError('Fibra fuera de la altura de la sección.')
    s = stage_at(result, stage, x)
    return dict(stress=s.stress.axial_component_pa+s.slope*y, axial=s.stress.axial_component_pa,
        prestress=-s.stress.prestress_moment_n_m*y/result.section.inertia_m4,
        external=-s.moment*y/result.section.inertia_m4,
        concrete=contains_concrete(result.section.components, 0, y+cy))


def selected_coordinates(result, x_ratio: float, y_ratio: float) -> tuple[float, float]:
    if not all(isfinite(v) and 0 <= v <= 1 for v in (x_ratio, y_ratio)):
        raise ValueError('Las posiciones relativas deben estar entre 0 y 1.')
    return x_ratio*result.input.span_m, y_ratio*result.section.height_m-result.section.centroid_from_bottom_m


def diagrams(result, stage, count=101):
    if stage not in ('transfer', 'service') or not isinstance(count, int) or not 2 <= count <= 10001:
        raise ValueError('Etapa o cantidad de puntos inválida.')
    return generate_beam_diagram(getattr(result, stage).uniform_load_n_m, result.input.span_m, count)


def stress_profile(result, stage, x, count=51):
    if not isinstance(count, int) or not 2 <= count <= 10001:
        raise ValueError('Cantidad de puntos inválida.')
    cy, h = result.section.centroid_from_bottom_m, result.section.height_m
    s = stage_at(result, stage, x)
    return [dict(y=-cy+h*i/(count-1), stress=s.stress.bottom_pa+
        (s.stress.top_pa-s.stress.bottom_pa)*i/(count-1)) for i in range(count)]


def stress_scale(result):
    """Escala común a ambas etapas y todas las posiciones bajo carga uniforme."""
    return max(1.0, *(abs(v) for stage in ('transfer', 'service')
        for x in (0, result.input.span_m/2)
        for v in (stage_at(result, stage, x).stress.top_pa, stage_at(result, stage, x).stress.bottom_pa)))


def stress_field(result, stage, x, columns=41, rows=61):
    """Campo elástico en hormigón; los vacíos se representan con None."""
    if not all(isinstance(v, int) and 2 <= v <= 201 for v in (columns, rows)):
        raise ValueError('Resolución del mapa inválida.')
    sec = result.section
    xs = [-sec.width_m/2+sec.width_m*(i+.5)/columns for i in range(columns)]
    ys = [-sec.centroid_from_bottom_m+sec.height_m*(j+.5)/rows for j in range(rows)]
    s = stage_at(result, stage, x)
    z = [[s.stress.axial_component_pa+s.slope*y if contains_concrete(sec.components, a,
        y+sec.centroid_from_bottom_m) else None for a in xs] for y in ys]
    return xs, ys, z
