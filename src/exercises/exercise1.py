"""Resolución auditada del set p.1-3. No afirma identidad con sus errores impresos."""
from math import sqrt,floor
from src.models.exercise1 import Exercise1Input
from src.sections.rectangular import SectionProperties
from src.analysis.elastic import calculate_elastic_stresses

SOURCE='SET DE EJERCICIOS PARA AVANCE 2.pdf, ejercicio 1, pp.1-3 (UNaM, Dávalos y Fraticelli)'
SOURCE_SHA256='dd620e184eb43082242f6dc8e155ccfab8c35c13846982553f89652b1aff016c'

def solve_exercise1(data):
    from src.checks.engineering import rectangular_flexure,check,pending
    b=Exercise1Input.model_validate(data)
    area=b.width_m*b.height_m
    inertia=b.width_m*b.height_m**3/12
    w=inertia/(b.height_m/2)
    # Contenedor solo para reutilizar tensiones. No se calcula ni informa peso propio.
    section=SectionProperties(area,b.height_m/2,inertia,w,w,0,b.height_m)
    e=b.height_m/2-b.steel_depth_m
    ft_c=sqrt(b.fc_pa/1e6)*1e6
    ft_u=.7*ft_c
    denominator=1/area-e/w
    lower=(b.service_moment_n_m/w-ft_c)/denominator
    upper=(b.service_moment_n_m/w-ft_u)/denominator
    if lower<=0:
        raise ValueError('Este caso de dimensionamiento requiere P límite positivo; revise momento y sección.')
    # Clase T es intervalo ABIERTO. No etiquetar la igualdad sqrt(fc) como T.
    adopted=(floor(lower/b.force_rounding_n)+1)*b.force_rounding_n
    if not lower<adopted<upper:
        raise ValueError('El redondeo elegido sale del intervalo de clase T. Reduzca el incremento de fuerza.')
    ap=adopted/b.effective_steel_stress_pa
    if ap>=area:
        raise ValueError('Área activa incompatible con el área de sección.')
    s=calculate_elastic_stresses(section,adopted,e,b.service_moment_n_m)
    values=dict(area_m2=area,inertia_m4=inertia,section_modulus_m3=w,eccentricity_m=e,
        tension_u_pa=ft_u,tension_c_pa=ft_c,force_lower_n=lower,force_upper_n=upper,
        adopted_force_n=adopted,steel_area_m2=ap,top_stress_pa=s.top_pa,bottom_stress_pa=s.bottom_pa,
        moment_demand_n_m=b.moment_factor*b.service_moment_n_m,service_class='T')
    checks=[dict(name='Clase T en fibra inferior',status='CUMPLE CRITERIO',demand=s.bottom_pa,
        capacity=ft_c,unit='Pa',note='Intervalo estricto 0.7 sqrt(fc) < sigma_inf < sqrt(fc); fuerza adoptada por exceso.',
        reference=SOURCE,function='solve_exercise1',normative_status='PRELIMINAR; referencia de la fuente, no adopción docente confirmada')]
    try:
        f=rectangular_flexure(b.width_m,b.height_m,b.steel_depth_m,ap,b.fc_pa,b.fpu_pa,b.fpy_pa,b.effective_steel_stress_pa)
        values.update(fps_pa=f['fps_pa'],compression_block_m=f['a_m'],neutral_axis_m=f['c_m'],
            beta1=f['beta1'],gamma_p=f['gamma_p'],net_strain=f['net_strain'],
            nominal_moment_n_m=f['nominal_n_m'],capacity_n_m=f['capacity_n_m'],
            tensile_force_n=ap*f['fps_pa'],lever_arm_m=b.steel_depth_m-f['a_m']/2)
        checks.append(check('Flexión: phi Mn frente a 1.6 Ms',values['moment_demand_n_m'],f['capacity_n_m'],'N m',
            'CIRSOC 201-2005 18.7.2(a), 9.3.2.1; método revisado distinto al simplificado de la fuente','rectangular_flexure'))
    except ValueError as exc:
        checks.append(pending('Flexión',str(exc),'CIRSOC 201-2005 18.7.2(a)','rectangular_flexure'))
    return dict(case_type=b.case_type,input_si=b.model_dump(),values=values,checks=checks,
        source=SOURCE,source_sha256=SOURCE_SHA256,
        adoption='P se redondea por exceso al incremento indicado (10 kN por defecto); es una decisión explícita de la resolución, no dato de la fuente.',
        manual_status='PENDIENTE: la referencia recalculada no es evidencia manuscrita del equipo',
        not_applicable=['Pérdidas: fpe es dato efectivo; no se inventa P0','Transferencia: falta estado inicial',
            'Corte y flecha: el ejercicio 1 no da luz ni distribución de cargas'],
        normative_status='PRELIMINAR: CIRSOC 201-2005; material docente ACI requiere ratificación y unificación')


def compare_values(result,manual_values):
    """Compara números aportados por usuario; no acredita autoría ni revisión."""
    rows=[]
    for key,reference in manual_values.items():
        if key not in result['values']:raise ValueError('Magnitud desconocida: '+key)
        from math import isfinite
        if not isinstance(reference,(int,float)) or not isfinite(reference):
            raise ValueError('Valor manual debe ser numérico y finito.')
        app=result['values'][key]
        if not isinstance(app,(int,float)):raise ValueError('Magnitud no numérica: '+key)
        delta=abs(app-reference)
        rows.append(dict(quantity=key,manual=reference,software=app,absolute_error=delta,
            relative_error_percent=100*delta/abs(reference) if reference else None))
    return rows
