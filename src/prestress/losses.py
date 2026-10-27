"""FHWA-NHI-04-043 (2003), Design Step 5.4. Método histórico, no norma chilena.
Solo pretesado recto, una etapa, baja relajación; fuerza antes de transferencia.
SH/CR/RE estimadas a largo plazo. No combina un porcentaje global adicional.
"""
from dataclasses import dataclass

KSI_PA = 6894757.293168
REFERENCE = 'FHWA-NHI-04-043, Design Step 5.4, S5.9.5.2.3a y S5.9.5.4.2-4 (método histórico).'

@dataclass(frozen=True)
class LossResult:
    method: str
    elastic_pa: float
    shrinkage_pa: float
    creep_pa: float
    relaxation_pa: float
    transfer_force_n: float
    effective_force_n: float
    total_ratio: float
    concrete_at_steel_pa: float
    reference: str


def calculate_losses(beam, section, options):
    p0, ap = beam.initial_force_n, beam.steel_area_m2
    if options.loss_method == 'declarada':
        return LossResult('declarada',0,0,0,0,p0,p0*(1-beam.loss_ratio),beam.loss_ratio,0,
                          'Modo histórico: porcentaje ingresado; sin desglose físico.')
    if beam.components or beam.eccentricity_m > 0:
        raise ValueError('Pérdidas FHWA de esta extensión: rectángulo simple y tendón inferior o centrado; use modo declarado para el taller.')
    a,i,e = section.area_m2, section.inertia_m4, beam.eccentricity_m
    mg = section.self_weight_n_m*beam.span_m**2/8
    n = options.ep_pa/options.eci_pa
    k = 1/a + e*e/i
    # ES = n[(P0-Ap ES) k + Mg e/I]. Compresión positiva aquí.
    es = n*(p0*k + mg*e/i)/(1+n*ap*k)
    if es < 0:
        raise ValueError('El modelo de acortamiento exige compresión en el tendón al transferir.')
    pt = p0-ap*es
    fcgp = pt*k + mg*e/i
    sh = (17-.15*options.humidity_percent)*KSI_PA
    # Alivio de compresión causado por carga permanente posterior.
    fcdp = -(beam.dead_load_n_m*beam.span_m**2/8)*e/i
    cr = max(0.,12*fcgp-7*fcdp)
    re = max(0.,.3*(20*KSI_PA-.4*es-.2*(sh+cr)))
    pe = pt-ap*(sh+cr+re)
    if not 0 < pe <= pt <= p0:
        raise ValueError('Pérdidas incompatibles: la fuerza efectiva debe ser positiva y no superar la inicial.')
    return LossResult('fhwa_2003',es,sh,cr,re,pt,pe,1-pe/p0,fcgp,REFERENCE)
