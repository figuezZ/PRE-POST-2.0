"""Evaluación académica acotada. CIRSOC 201-2005, no certificación ni adopción USS.
Solo sección rectangular bruta, hormigón normal, un tendón adherente inferior,
sin armadura pasiva longitudinal, torsión ni cargas concentradas.
"""

REF = 'CIRSOC 201-2005'


def check(name, demand, capacity, unit, reference, function, note=''):
    return dict(name=name,demand=demand,capacity=capacity,unit=unit,
                ratio=demand/capacity if capacity>0 else None,
                status='CUMPLE CRITERIO' if demand<=capacity else 'NO CUMPLE',
                reference=reference,function=function,note=note,
                normative_status='PRELIMINAR: adopción académica pendiente')


def pending(name, reason, reference='', function=''):
    return dict(name=name,demand=None,capacity=None,unit='',ratio=None,status='PENDIENTE',
                reference=reference,function=function,note=reason,normative_status='NO VERIFICADO')


def rectangular_flexure(b,h,dp,ap,fc,fpu,fpy,fpe):
    """CIRSOC 18.7.2(a); sin acero pasivo. No supone fps=fpy."""
    if not 0<dp<h or fpe < .5*fpu:
        raise ValueError('Flexión aproximada exige 0<dp<h y fpe >= 0.50 fpu.')
    beta = max(.65,.85-.05*max(0,fc/1e6-30)/7)
    ratio = fpy/fpu
    gamma = .28 if ratio>=.9-1e-12 else .4 if ratio>=.85 else .55
    rho = ap/(b*dp)
    fps = fpu*(1-gamma/beta*rho*fpu/fc)
    a = ap*fps/(.85*fc*b)
    c = a/beta
    if fps<=0 or not 0<c<dp:
        raise ValueError('Sección fuera del campo de la aproximación a flexión.')
    eps = .003*(dp-c)/c
    if eps<.005:
        raise ValueError('La sección no es controlada por tracción; requiere compatibilidad y otro factor phi.')
    mn = ap*fps*(dp-a/2)
    return dict(fps_pa=fps,beta1=beta,gamma_p=gamma,a_m=a,c_m=c,net_strain=eps,
                nominal_n_m=mn,phi=.9,capacity_n_m=.9*mn)

