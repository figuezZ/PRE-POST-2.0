"""Trazabilidad de la extensión: misma instantánea para pantalla y exportaciones."""
from dataclasses import asdict
from src.units import Quantity as Q, from_si, display_unit

def extend_report(report,result,system):
    if not result.input.design:
        return report
    if result.losses.method != 'declarada':
        report['conventions'] = report['conventions'].replace('Pérdida global declarada.', 'Pérdidas ES/SH/CR/RE calculadas; porcentaje ingresado no aplicado.')
    report['conventions'] += ' Extensión: pretesado recto; criterios preliminares. '+result.engineering['warning']
    report['design_input_si']=result.input.design.model_dump()
    report['engineering']=result.engineering
    report['checks']=result.engineering['checks']
    def row(label,value,q):
        return {'Propiedad':label,'Valor':from_si(value,q,system),'Unidad':display_unit(system,q).symbol}
    loss=result.losses
    report['tables']['Pérdidas']=[row(label,getattr(loss,field),q) for label,field,q in [
        ('Acortamiento elástico ES','elastic_pa',Q.STRESS),('Retracción SH','shrinkage_pa',Q.STRESS),
        ('Fluencia CR','creep_pa',Q.STRESS),('Relajación RE','relaxation_pa',Q.STRESS),
        ('Fuerza después de ES','transfer_force_n',Q.FORCE),('Fuerza efectiva','effective_force_n',Q.FORCE)]]
    report['tables']['Pérdidas'].append(dict(Propiedad='Pérdida total',Valor=loss.total_ratio*100,Unidad='%'))
    report['tables']['Parámetros nuevos SI']=[dict(Propiedad=k,Valor=v,Unidad=('Pa' if k.endswith('_pa') else 'm' if k.endswith('_m') else '%' if k=='humidity_percent' else '1')) for k,v in result.input.design.model_dump().items() if isinstance(v,(float,int))]
    v=result.engineering['values']; rows=[]
    for key,label,q in [('mu_n_m','Demanda flexión Mu',Q.MOMENT),('vu_n','Demanda corte Vu',Q.FORCE),('shear_x_m','Sección de corte x',Q.SPAN),('live_deflection_m','Flecha viva elástica',Q.SECTION_LENGTH),('cracking_moment_n_m','Momento fisuración Mcr',Q.MOMENT)]:
        if key in v: rows.append(row(label,v[key],q))
    if 'flexure' in v:
        rows += [row('Momento nominal Mn',v['flexure']['nominal_n_m'],Q.MOMENT),row('Capacidad phi Mn',v['flexure']['capacity_n_m'],Q.MOMENT)]
    if 'shear' in v:
        rows += [row('Vc',v['shear']['vc_n'],Q.FORCE),row('Vs',v['shear']['vs_n'],Q.FORCE),row('Capacidad phi Vn',v['shear']['capacity_n'],Q.FORCE)]
    report['tables']['Verificaciones numéricas']=rows
    if 'section_auxiliary' in v:
        aux=v['section_auxiliary']; ar=[]
        for name in ('net','transformed'):
            for key,label,q in [('area_m2','Área',Q.SECTION_AREA),('centroid_m','Centroide',Q.SECTION_LENGTH),('inertia_m4','Inercia',Q.INERTIA)]:
                ar.append(row(name+' '+label,aux[name][key],q))
        report['tables']['Sección auxiliar']=ar
    for k,c in enumerate(report['checks']):
        c=dict(c); c['manual_status']='PENDIENTE DE HOJA MANUSCRITA'; report['checks'][k]=c
    report['design_memory']=design_memory(result)
    return report


def design_memory(result):
    b=result.input; o=b.design; s=result.section; l=result.losses; v=result.engineering['values']
    records=[]
    def add(name,formula,sub,value,unit,ref):
        records.append(dict(label=name,formula=formula,substitution=sub,value=value,unit=unit,reference=ref))
    if l.method!='declarada':
        add('ES','ES=n[P0(1/A+e²/I)+Mg e/I]/[1+n Ap(1/A+e²/I)]',
            f'n={o.ep_pa/o.eci_pa:.9g}; P0={b.initial_force_n}; A={s.area_m2}; e={b.eccentricity_m}; I={s.inertia_m4}; Mg={s.self_weight_n_m*b.span_m**2/8}; Ap={b.steel_area_m2}',l.elastic_pa,'Pa',l.reference)
        add('SH','SH=(17-0.15 H)*6894757.293168',f'H={o.humidity_percent} %',l.shrinkage_pa,'Pa',l.reference)
        add('CR','CR=max(0,12 fcgp-7 fcdp)',f'fcgp={l.concrete_at_steel_pa}; fcdp={-b.dead_load_n_m*b.span_m**2/8*b.eccentricity_m/s.inertia_m4}',l.creep_pa,'Pa',l.reference)
        add('RE','RE=max(0,0.3[20 ksi-0.4 ES-0.2(SH+CR)])',f'ES={l.elastic_pa}; SH={l.shrinkage_pa}; CR={l.creep_pa}',l.relaxation_pa,'Pa',l.reference)
    if 'flexure' in v:
        f=v['flexure']; dp=b.height_m/2-b.eccentricity_m
        add('Tensión resistente fps','fps=fpu[1-(gamma/beta1)(Ap/(b dp)) fpu/fc]',f'fpu={o.fpu_pa}; gamma={f["gamma_p"]}; beta1={f["beta1"]}; Ap={b.steel_area_m2}; b={b.width_m}; dp={dp}; fc={b.fc_pa}',f['fps_pa'],'Pa','CIRSOC 201-2005 18.7.2(a)')
        add('Bloque comprimido','a=Ap fps/(0.85 fc b)',f'Ap={b.steel_area_m2}; fps={f["fps_pa"]}; fc={b.fc_pa}; b={b.width_m}',f['a_m'],'m','CIRSOC 201-2005 10.2.7')
        add('Momento nominal','Mn=Ap fps(dp-a/2)',f'Ap={b.steel_area_m2}; fps={f["fps_pa"]}; dp={dp}; a={f["a_m"]}',f['nominal_n_m'],'N m','CIRSOC 201-2005 18.7.2')
    if 'shear' in v:
        sh=v['shear']
        add('Corte Vc','Vc=limitar[(sqrt(fc_MPa)/20+5 min(Vu dp/Mu,1))*1e6*b*d]; cap Vcw en extremos',f'fc={b.fc_pa/1e6} MPa; b={b.width_m}; d={sh["d_m"]}; Vu={v["vu_n"]}; M(x)={v["shear_moment_n_m"]}; reducción transferencia={sh["transfer_reduction"]}',sh['vc_n'],'N','CIRSOC 201-2005 11.4.2 y 11.4.4')
        add('Estribos Vs','Vs=(Av/s) fy d',f'Av/s={sh["av_s_provided_m"]} m2/m; fy={o.stirrup_fy_pa}; d={sh["d_m"]}',sh['vs_n'],'N','CIRSOC 201-2005 11.5.7.2')
    if 'deflection_service' in v:
        add('Flecha elástica servicio','delta=5 w L^4/(384 Ec I)+Pe e L²/(8 Ec I)',f'w={result.service.uniform_load_n_m}; L={b.span_m}; Ec={o.ec_pa}; I={s.inertia_m4}; Pe={l.effective_force_n}; e={b.eccentricity_m}',v['deflection_service']['total_m'],'m','Integración de curvatura EI; solo sección no fisurada, instante elástico.')
    return records
