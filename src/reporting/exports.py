"""Exportaciones sin ecuaciones: consumen la instantánea de reporting.tables."""
from io import BytesIO
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
import json
from math import ceil
import pandas as pd
import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether


def excel_bytes(report) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter', engine_kwargs={'options': {
        'strings_to_formulas': False, 'strings_to_urls': False}}) as writer:
        meta = [{'Dato': k, 'Valor': report[k]} for k in ('project','author','system','stage','x_m','y_m','concrete','conventions')]
        meta.append({'Dato': 'Fecha UTC', 'Valor': datetime.now(timezone.utc).isoformat()})
        sheets = {'Identificación': meta, **report['tables'], 'Componentes SI': report['components'], 'Memoria SI': report['memory']}
        for name, rows in sheets.items():
            frame = pd.DataFrame(rows)
            frame.to_excel(writer, sheet_name=name, index=False)
            sheet = writer.sheets[name]
            sheet.freeze_panes(1, 0)
            sheet.autofilter(0, 0, len(frame), len(frame.columns)-1)
            wrap = writer.book.add_format({'text_wrap': True, 'valign': 'top'})
            number = writer.book.add_format({'num_format': '0.00000000', 'valign': 'top'})
            for j, column in enumerate(frame.columns):
                numeric = pd.api.types.is_numeric_dtype(frame[column])
                sheet.set_column(j, j, 23 if numeric else 42, number if numeric else wrap)
            sheet.set_default_row(32)
            for index, record in enumerate(frame.to_dict('records'),1):
                lines = max(ceil(len(str(v))/40) for v in record.values())
                sheet.set_row(index,min(409,max(32,15*lines)))
    return output.getvalue()


def json_bytes(result, report) -> bytes:
    return json.dumps({'schema_version': '2.0.0', 'input_si': result.input.model_dump(mode='json'),
        'report': report}, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8')


def pdf_bytes(report) -> bytes:
    font_dir = Path(reportlab.__file__).parent/'fonts'
    if 'PrePost' not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont('PrePost', str(font_dir/'Vera.ttf')))
        pdfmetrics.registerFont(TTFont('PrePostBold', str(font_dir/'VeraBd.ttf')))
    styles = getSampleStyleSheet()
    for style in styles.byName.values():
        style.fontName = 'PrePost'
    styles['Normal'].fontSize = 8
    styles['Normal'].leading = 11
    styles['Heading1'].fontName = styles['Heading2'].fontName = 'PrePostBold'
    styles['Heading2'].fontSize = 12
    styles['Heading2'].leading = 15
    styles['Heading2'].spaceBefore = 10
    styles['Heading2'].spaceAfter = 5
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=38, leftMargin=38,
                            topMargin=38, bottomMargin=38, title='PRE-POST 2.0 - Memoria de cálculo')
    def p(value, style='Normal'):
        return Paragraph(escape(str(value)), styles[style])
    def table(rows, widths):
        t = Table([[p(c) for c in row] for row in rows], colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce8f6')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6fa')]),
            ('VALIGN',(0,0),(-1,-1),'TOP'), ('LEFTPADDING',(0,0),(-1,-1),7),
            ('RIGHTPADDING',(0,0),(-1,-1),7), ('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ]))
        return t
    story = [p('PRE-POST 2.0', 'Title'), p(report['project'], 'Heading1'),
        p('Autor: '+report['author']), p('Sistema: '+report['system']),
        p('Emisión UTC: '+datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')),
        Spacer(1, 10), p(report['conventions']), Spacer(1, 12)]
    for name, rows in report['tables'].items():
        if name in ('Transferencia', 'Explorador'):
            story.append(PageBreak())
        story.append(p(name, 'Heading2'))
        if name == 'Explorador':
            story += [p('Etapa: '+('Servicio' if report['stage']=='service' else 'Transferencia')), p('Fibra en hormigón: '+('Sí' if report['concrete'] else 'No')+
                '. En vacíos o bordes se informa la prolongación del campo elástico.'), Spacer(1, 8)]
        story += [table([['Propiedad','Valor','Unidad']]+[[r['Propiedad'], f"{r['Valor']:.8g}",r['Unidad']] for r in rows],
            [287, 145, 87])]
    story += [PageBreak(), p('Componentes y ejes paralelos', 'Heading1'),
        p('Todas las magnitudes de esta tabla están en SI. Ai y las inercias llevan signo; los vacíos restan.'), Spacer(1, 10),
        table([['Componente','Ai (m2)','Yi (m)','di (m)','I propio (m4)','Ai di2 (m4)']]+
            [[r['name']]+[f'{r[k]:.6g}' for k in ('area','centroid','d','own','parallel')] for r in report['components']],
            [129,78,78,78,78,78]), Spacer(1, 14), p('Memoria de cálculo - SI', 'Heading1'),
        p('Etapa: '+report['stage']+f"; x={report['x_m']:.8g} m. "+report['memory'][0]['reference'])]
    for j, step in enumerate(report['memory'], 1):
        story.append(KeepTogether([p(f"{j}. {step['label']}", 'Heading2'), p(step['formula']), p(step['substitution']),
            p(f"Resultado: {step['value']:.9g} {step['unit']}"), Spacer(1, 5)]))
    def footer(canvas, doc):
        canvas.setFont('PrePost', 8)
        canvas.drawString(38, 22, 'PRE-POST 2.0 | Instantánea de cálculo académico')
        canvas.drawRightString(A4[0]-38, 22, str(doc.page))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue()
