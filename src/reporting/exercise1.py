"""Presentación del caso seccional, sin introducir cargas ni luz ficticias."""
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

FIELDS=[('area_m2','Área','m²',1),('inertia_m4','Inercia','m⁴',1),
 ('section_modulus_m3','Módulo resistente','m³',1),('eccentricity_m','Excentricidad','m',1),
 ('force_lower_n','Límite inferior abierto P','kN',1000),('force_upper_n','Límite superior abierto P','kN',1000),
 ('adopted_force_n','Fuerza efectiva adoptada','kN',1000),('steel_area_m2','Área activa teórica','mm²',1e-6),
 ('top_stress_pa','Tensión superior','MPa',1e6),('bottom_stress_pa','Tensión inferior','MPa',1e6),
 ('moment_demand_n_m','Momento requerido','kN m',1000),('fps_pa','Tensión última acero','MPa',1e6),
 ('compression_block_m','Bloque comprimido a','mm',.001),('nominal_moment_n_m','Momento nominal','kN m',1000),
 ('capacity_n_m','Resistencia phi Mn','kN m',1000)]

def exercise_report(result):
    return {**result,'tables':{'Resultados':[{'Magnitud':label,'Valor':result['values'][key]/scale,'Unidad':unit}
        for key,label,unit,scale in FIELDS if key in result['values']]}}

def exercise_pdf(report):
    out=BytesIO();styles=getSampleStyleSheet()
    def p(s):return Paragraph(escape(str(s)),styles['Normal'])
    story=[Paragraph('Ejercicio 1: comparación manual y software',styles['Title']),p(report['source']),Spacer(1,12),
        p(report['adoption']),p(report['normative_status']),p(report['manual_status']),Spacer(1,12),
        Paragraph('Datos de entrada en SI',styles['Heading2'])]
    for key,value in report['input_si'].items():story.append(p(f'{key}: {value}'))
    story.append(Paragraph('Resultados calculados',styles['Heading2']))
    rows=[[p(x) for x in ['Magnitud','Valor','Unidad']]]
    rows += [[p(r['Magnitud']),p(f"{r['Valor']:.9g}"),p(r['Unidad'])] for r in report['tables']['Resultados']]
    table=Table(rows,colWidths=[260,120,80],repeatRows=1)
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(table)
    for c in report['checks']:story += [Spacer(1,8),p(c['name']+': '+c['status']),p(c['reference'])]
    for text in report['not_applicable']:story.append(p(text))
    SimpleDocTemplate(out,title='Ejercicio 1 del set',leftMargin=40,rightMargin=40).build(story)
    return out.getvalue()
