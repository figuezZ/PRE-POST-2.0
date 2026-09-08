"""Una instantánea común para pantalla, Excel y PDF."""
from dataclasses import asdict
from src.units import Quantity as Q, display_unit, from_si
from src.analysis.memory import calculation_memory
from src.analysis.pipeline import stage_at, fiber_at

INPUT_FIELDS = [
    ('span_m', 'Luz', Q.SPAN), ('width_m', 'Ancho de plantilla', Q.SECTION_LENGTH),
    ('height_m', 'Alto de plantilla', Q.SECTION_LENGTH), ('unit_weight_n_m3', 'Peso específico', Q.UNIT_WEIGHT),
    ('fci_pa', "f'ci", Q.STRESS), ('fc_pa', "f'c", Q.STRESS),
    ('dead_load_n_m', 'Carga muerta adicional', Q.LINE_LOAD), ('live_load_n_m', 'Carga viva', Q.LINE_LOAD),
    ('initial_force_n', 'Fuerza inicial Pi', Q.FORCE), ('eccentricity_m', 'Excentricidad e', Q.SECTION_LENGTH),
    ('steel_area_m2', 'Área de acero Ap', Q.STEEL_AREA),
]
CONVENTIONS = ('Compresión negativa; tracción positiva. y y e positivos hacia arriba desde el centroide. '
    'Momento externo sagante positivo. Pérdida global declarada. Modelo elástico no fisurado. '
    'Los colores indican el signo de la tensión, no cumplimiento normativo. '
    '1860 MPa es el control de entrada heredado, no una verificación ACI. Uso académico.')


def report_tables(result, system='SI', stage='service', x=None, y=None):
    x = result.input.span_m/2 if x is None else x
    y = result.section.height_m-result.section.centroid_from_bottom_m if y is None else y
    pos, fiber = stage_at(result, stage, x), fiber_at(result, stage, x, y)
    def row(label, value, quantity):
        return {'Propiedad': label, 'Valor': from_si(value, quantity, system),
                'Unidad': display_unit(system, quantity).symbol}
    inputs = [row(label, getattr(result.input, field), q) for field, label, q in INPUT_FIELDS]
    inputs.append({'Propiedad': 'Pérdida declarada', 'Valor': result.input.loss_ratio*100, 'Unidad': '%'})
    sec = result.section
    section = [row(label, getattr(sec, field), q) for field, label, q in [
        ('gross_area_m2', 'Área bruta (antes de vacíos)', Q.SECTION_AREA),
        ('gross_inertia_m4', 'Inercia bruta', Q.INERTIA), ('gross_centroid_m', 'Centroide bruto desde base', Q.SECTION_LENGTH),
        ('area_m2', 'Área de hormigón (descontando vacíos)', Q.SECTION_AREA),
        ('centroid_from_bottom_m', 'Centroide de hormigón desde base', Q.SECTION_LENGTH),
        ('inertia_m4', 'Inercia de hormigón', Q.INERTIA),
        ('section_modulus_top_m3', 'Módulo superior', Q.SECTION_MODULUS),
        ('section_modulus_bottom_m3', 'Módulo inferior', Q.SECTION_MODULUS),
        ('self_weight_n_m', 'Peso propio', Q.LINE_LOAD), ('width_m', 'Ancho real', Q.SECTION_LENGTH),
        ('height_m', 'Alto real', Q.SECTION_LENGTH)]]
    tables = {'Entradas': inputs, 'Sección': section}
    for name, s in [('Transferencia', result.transfer), ('Servicio', result.service)]:
        tables[name] = [row(label, value, q) for label, value, q in [
            ('Fuerza de etapa', s.force_n, Q.FORCE), ('Tensión del acero', s.steel_stress_pa, Q.STRESS),
            ('Carga uniforme total', s.uniform_load_n_m, Q.LINE_LOAD), ('Reacción por apoyo', s.reaction_n, Q.FORCE),
            ('Corte máximo absoluto', s.max_shear_n, Q.FORCE), ('Momento en centro de luz', s.midspan_moment_n_m, Q.MOMENT),
            ('Tensión superior en centro', s.stress.top_pa, Q.STRESS), ('Tensión inferior en centro', s.stress.bottom_pa, Q.STRESS),
            ('Compresión uniforme', s.stress.axial_component_pa, Q.STRESS),
            ('Momento del pretensado', s.stress.prestress_moment_n_m, Q.MOMENT),
            ('Momento resultante en centro', s.stress.resultant_moment_n_m, Q.MOMENT)]]
    tables['Explorador'] = [row(label, value, q) for label, value, q in [
        ('Posición x', x, Q.SPAN), ('Fibra y desde centroide', y, Q.SECTION_LENGTH),
        ('Cortante en x', pos.shear, Q.FORCE), ('Momento en x', pos.moment, Q.MOMENT),
        ('Tensión superior en x', pos.stress.top_pa, Q.STRESS), ('Tensión inferior en x', pos.stress.bottom_pa, Q.STRESS),
        ('Tensión en fibra', fiber['stress'], Q.STRESS), ('Aporte axial', fiber['axial'], Q.STRESS),
        ('Aporte del pretensado', fiber['prestress'], Q.STRESS), ('Aporte del momento externo', fiber['external'], Q.STRESS)]]
    return dict(system=system, project=result.input.project, author=result.input.author,
        stage=stage, x_m=x, y_m=y, concrete=fiber['concrete'], tables=tables,
        components=[asdict(r) for r in sec.rows], memory=calculation_memory(result, stage, x), conventions=CONVENTIONS)
