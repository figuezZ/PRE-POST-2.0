"""Evaluación académica acotada. CIRSOC 201-2005, no certificación ni adopción USS.
Solo sección rectangular bruta, hormigón normal, un tendón adherente inferior,
sin armadura pasiva longitudinal, torsión ni cargas concentradas.
"""
from math import sqrt, pi
from dataclasses import asdict
from src.analysis.pipeline import stresses

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


def shear_capacity(fc,b,h,dp,vu,mu,pe,ap,fpu,fy,av,spacing,transfer_length,area):
    """11.4.2, 11.4.4 y 11.5. SI; conversion MPa explícita.
    Se usa mínimo de 11-13 (conservador frente a alternativa menor 11-14).
    Cap Vcw cerca del extremo adopta fpc reducido a h/2.
    """
    if pe < .4*ap*fpu:
        raise ValueError('Corte simplificado exige Pe >= 0.40 Ap fpu.')
    d=max(dp,.8*h)
    root=sqrt(fc/1e6)
    ratio=min(1,abs(vu)*dp/abs(mu)) if abs(mu)>1e-12 else 1.
    raw=(root/20+5*ratio)*1e6*b*d
    vc=min(.4*root*1e6*b*d,max(root/6*1e6*b*d,raw))
    reduction=min(1.,(h/2)/transfer_length)
    if reduction<1:
        vc=min(vc,(.3*root*1e6+pe/area*reduction)*b*dp)
    vs=av*fy*d/spacing
    vsmax=2/3*root*1e6*b*d
    amin=max(root/16,.33)*1e6*b/fy if abs(vu)>.5*.75*vc else 0.
    required=max(amin,max(0,abs(vu)/.75-vc)/(fy*d))
    smax=min(.75*h,.4)
    if vs>root/3*1e6*b*d:
        smax/=2
    return dict(d_m=d,vc_n=vc,vs_n=vs,vs_limit_n=vsmax,capacity_n=.75*(vc+min(vs,vsmax)),
                av_s_required_m=required,av_s_provided_m=av/spacing,spacing_limit_m=smax,
                transfer_reduction=reduction)


def elastic_deflections(w,p,e,length,ec,inertia):
    """Integración EI v''=M; centro de luz; desplazamiento positivo abajo."""
    gravity=5*w*length**4/(384*ec*inertia)
    prestress=p*e*length**2/(8*ec*inertia)
    return dict(gravity_m=gravity,prestress_m=prestress,total_m=gravity+prestress)


def evaluate(result,options):
    beam,sec=result.input,result.section
    if beam.components:
        return dict(checks=[pending('Extensión resistente','Disponible solo para rectángulo simple; taller geométrico conservado.')],
                    values={},warning='No se verifican secciones T/I/huecas en el módulo nuevo.')
    if beam.eccentricity_m>0:
        return dict(checks=[pending('Extensión resistente','Se requiere tendón centrado o inferior para flexión positiva.')],values={},warning='Fuera de alcance.')
    b,h,L=beam.width_m,beam.height_m,beam.span_m
    e=beam.eccentricity_m; dp=h/2-e; fc=beam.fc_pa; fci=beam.fci_pa
    pe,pt=result.service.force_n,result.transfer.force_n
    from src.sections.transformed import transformed_rectangular
    checks=[]; values={}
    values['section_auxiliary']=transformed_rectangular(b,h,beam.steel_area_m2,h/2+e,options.ep_pa,options.ec_pa)
    lt=50*options.strand_diameter_m
    if lt>=L/2:
        return dict(checks=[pending('Transferencia','Longitud de transferencia >= L/2: fuera de alcance.')],values={},warning='Fuera de alcance.')
    # Envolvente de sección desarrollada: lt, L/2, L-lt; extremos se explicitan como pendientes.
    for name,force,load,limit,ref in [
        ('Transferencia',pt,sec.self_weight_n_m,.6*fci,'18.4.1'),
        ('Servicio total',pe,result.service.uniform_load_n_m,.6*fc,'18.4.2'),
        ('Servicio permanente',pe,sec.self_weight_n_m+beam.dead_load_n_m,.45*fc,'18.4.2')]:
        ss=[]
        for x in (lt,L/2,L-lt):
            s=stresses(sec,force,e,load*x*(L-x)/2)
            ss.extend([s.top_pa,s.bottom_pa])
        compression=max(0,-min(ss)); tension=max(0,max(ss))
        checks.append(check(name+' compresión',compression,limit,'Pa',REF+' '+ref,'evaluate'))
        if name=='Transferencia':
            checks.append(check(name+' tracción',tension,.25*sqrt(fci/1e6)*1e6,'Pa',REF+' 18.4.1(b)','evaluate','Límite general conservador; sin excepción de extremos.'))
        elif name=='Servicio total':
            values['service_class']='U' if tension<=.7*sqrt(fc/1e6)*1e6 else 'T' if tension<=sqrt(fc/1e6)*1e6 else 'C'
            checks.append(check('Servicio clase U',tension,.7*sqrt(fc/1e6)*1e6,'Pa',REF+' 18.3.3','evaluate','Objetivo de esta extensión: clase U.'))
            values['service_tension_pa']=tension
        values[name+' extrema_pa']=[min(ss),max(ss)]
    checks.append(check('Acero después de transferencia',pt/beam.steel_area_m2,min(.74*options.fpu_pa,.82*options.fpy_pa),'Pa',REF+' 18.5.1(b)','evaluate'))
    checks.append(pending('Límite del gato','P0 corresponde a antes de transferencia; falta historial de tesado y límite del fabricante.',REF+' 18.5.1(a)'))
    values['decompression_moment_n_m']=pe*(sec.section_modulus_bottom_m3/sec.area_m2-e)
    mcr=values['decompression_moment_n_m']+.7*sqrt(fc/1e6)*1e6*sec.section_modulus_bottom_m3
    values['cracking_moment_n_m']=mcr
    dload=sec.self_weight_n_m+beam.dead_load_n_m
    cases={'1.4D':1.4*dload,'1.2D+1.6L':1.2*dload+1.6*beam.live_load_n_m}
    combo,wu=max(cases.items(),key=lambda a:a[1])
    mu=wu*L**2/8
    values.update(ultimate_combination=combo,ultimate_load_n_m=wu,mu_n_m=mu,transfer_length_m=lt)
    try:
        flex=rectangular_flexure(b,h,dp,beam.steel_area_m2,fc,options.fpu_pa,options.fpy_pa,pe/beam.steel_area_m2)
        values['flexure']=flex
        checks.append(check('Flexión',mu,flex['capacity_n_m'],'N m',REF+' 18.7.2(a), 9.3.2.1','rectangular_flexure'))
        checks.append(check('Resistencia mínima a flexión',1.2*mcr,flex['capacity_n_m'],'N m',REF+' 18.8.2','rectangular_flexure','Se comprueba 1.2 Mcr; no se aplica exención.'))
    except ValueError as exc:
        checks.append(pending('Flexión',str(exc),REF+' 18.7.2','rectangular_flexure'))
    d=max(dp,.8*h)
    if d<L/2:
        vu=wu*(L/2-d); mx=wu*d*(L-d)/2
        values.update(shear_x_m=d,vu_n=vu,shear_moment_n_m=mx)
        try:
            av=options.stirrup_legs*pi*options.stirrup_diameter_m**2/4
            sh=shear_capacity(fc,b,h,dp,vu,mx,pe,beam.steel_area_m2,options.fpu_pa,options.stirrup_fy_pa,av,options.stirrup_spacing_m,lt,sec.area_m2)
            values['shear']=sh
            checks.extend([
                check('Corte en sección d',vu,sh['capacity_n'],'N',REF+' 11.4.2, 11.4.4, 11.5.7','shear_capacity'),
                check('Estribos requeridos',sh['av_s_required_m'],sh['av_s_provided_m'],'m2/m',REF+' 11.5.6.3 y 11.5.7.2','shear_capacity'),
                check('Separación de estribos',options.stirrup_spacing_m,sh['spacing_limit_m'],'m',REF+' 11.5.5','shear_capacity'),
                check('Límite de Vs',sh['vs_n'],sh['vs_limit_n'],'N',REF+' 11.5.7.9','shear_capacity')])
        except ValueError as exc:
            checks.append(pending('Corte',str(exc),REF+' 11.4.2','shear_capacity'))
    else:
        checks.append(pending('Corte','Viga corta: d >= L/2; requiere otro modelo.'))
    values['deflection_transfer']=elastic_deflections(sec.self_weight_n_m,pt,e,L,options.eci_pa,sec.inertia_m4)
    values['deflection_service']=elastic_deflections(result.service.uniform_load_n_m,pe,e,L,options.ec_pa,sec.inertia_m4)
    live=elastic_deflections(beam.live_load_n_m,0,e,L,options.ec_pa,sec.inertia_m4)['total_m']
    values['live_deflection_m']=live
    if values['service_class']=='U':
        checks.append(check('Flecha instantánea por carga viva',live,L/options.live_deflection_divisor,'m','Criterio de proyecto L/divisor; confirmar uso y tabla 9.5(b)','elastic_deflections'))
    else:
        checks.append(pending('Flecha de servicio','Clase T/C: la inercia bruta no basta; falta modelo fisurado.',REF+' 9.5.4.2','elastic_deflections'))
    checks.append(pending('Flecha diferida','Falta historia temporal de cargas, rigidez y contraflecha; pérdidas no equivalen a deformación diferida.',REF+' 9.5.4'))
    checks.append(pending('Extremos y desarrollo','Falta diseño local de transferencia, anclaje y longitud de desarrollo. No usar mapas de fuerza constante en esta zona.',REF+' 11.4.4, 18.13'))
    return dict(checks=checks,values=values,warning=options.criterion_note+' Resultados parciales; no certifican la viga.')
