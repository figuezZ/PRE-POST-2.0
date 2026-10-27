"""Memoria reproducible de 19 pasos; solo consume el núcleo en SI."""
from src.analysis.pipeline import stage_at, fiber_at

REFERENCE = 'Áreas compuestas; ejes paralelos; equilibrio; elasticidad (Clase 3 USS 2026). e positivo hacia arriba.'


def calculation_memory(result, stage, x):
    p, i, s = result.section, result.input, stage_at(result, stage, x)
    cy = p.centroid_from_bottom_m
    n = lambda value: f'{value:.7e}'
    steps = [
        ('Área de hormigón', 'A = sum(s b h)', ' + '.join(n(r.area) for r in p.rows), p.area_m2, 'm2'),
        ('Centroide', 'Yc = sum(Ai Yi)/A', ' + '.join(f'({n(r.area)} x {n(r.centroid)})' for r in p.rows)+'; dividir por '+n(p.area_m2), cy, 'm'),
        ('Inercia centroidal', 'I = sum(s b h^3/12 + Ai di^2)', ' + '.join(f'({n(r.own)} + {n(r.parallel)})' for r in p.rows), p.inertia_m4, 'm4'),
        ('Distancia superior', 'cs = h - Yc', n(p.height_m)+' - '+n(cy), p.height_m-cy, 'm'),
        ('Distancia inferior', 'ci = Yc', n(cy), cy, 'm'),
        ('Módulo superior', 'Ws = I/cs', n(p.inertia_m4)+' / '+n(p.height_m-cy), p.section_modulus_top_m3, 'm3'),
        ('Módulo inferior', 'Wi = I/ci', n(p.inertia_m4)+' / '+n(cy), p.section_modulus_bottom_m3, 'm3'),
        ('Peso propio', 'wpp = gamma A', n(i.unit_weight_n_m3)+' x '+n(p.area_m2), p.self_weight_n_m, 'N/m'),
        ('Fuerza de etapa', 'Pe = (1 - r) Pi' if stage == 'service' else 'P = Pi',
         f'(1 - {n(i.loss_ratio)}) x {n(i.initial_force_n)}' if stage == 'service' else n(i.initial_force_n), s.force, 'N'),
        ('Tensión del acero', 'fp = P/Ap', n(s.force)+' / '+n(i.steel_area_m2), s.force/i.steel_area_m2, 'Pa'),
        ('Carga de etapa', 'w = wpp + g + q' if stage == 'service' else 'w = wpp',
         ' + '.join(map(n, [p.self_weight_n_m, i.dead_load_n_m, i.live_load_n_m])) if stage == 'service' else n(p.self_weight_n_m), s.w, 'N/m'),
        ('Reacción', 'R = w L/2', n(s.w)+' x '+n(i.span_m)+' / 2', s.reaction, 'N'),
        ('Corte en x', 'V = R - wx', n(s.reaction)+' - '+n(s.w)+' x '+n(x), s.shear, 'N'),
        ('Momento en x', 'M = Rx - wx^2/2', n(s.reaction)+' x '+n(x)+' - '+n(s.w)+' x '+n(x)+'^2 / 2', s.moment, 'N m'),
        ('Momento del pretensado', 'Mp = P e', n(s.force)+' x '+n(i.eccentricity_m), s.stress.prestress_moment_n_m, 'N m'),
        ('Momento resultante', 'Mr = Mp + M', n(s.stress.prestress_moment_n_m)+' + '+n(s.moment), s.stress.resultant_moment_n_m, 'N m'),
        ('Compresión uniforme', 'sigmaN = -P/A', '-'+n(s.force)+' / '+n(p.area_m2), s.stress.axial_component_pa, 'Pa'),
    ]
    for label, y in [('superior', p.height_m-cy), ('inferior', -cy)]:
        f = fiber_at(result, stage, x, y)
        steps.append(('Tensión '+label, 'sigma(y) = -P/A - (P e + M)y/I',
            f'y={n(y)} m; -{n(s.force)}/{n(p.area_m2)} - ({n(s.force)} x {n(i.eccentricity_m)} + {n(s.moment)}) x {n(y)}/{n(p.inertia_m4)} = {n(f["axial"])} + {n(f["prestress"])} + {n(f["external"])}', f['stress'], 'Pa'))
    if result.losses and result.losses.method != 'declarada':
        loss = result.losses
        steps[8] = ('Fuerza de etapa', 'Pt=P0-Ap*ES; Pe=Pt-Ap*(SH+CR+RE)',
            f'P0={i.initial_force_n:.9g} N; Ap={i.steel_area_m2:.9g} m2; ES={loss.elastic_pa:.9g} Pa; SH={loss.shrinkage_pa:.9g} Pa; CR={loss.creep_pa:.9g} Pa; RE={loss.relaxation_pa:.9g} Pa',s.force,'N')
    return [dict(label=a, formula=b, substitution=c, value=d, unit=e, reference=REFERENCE) for a,b,c,d,e in steps]
