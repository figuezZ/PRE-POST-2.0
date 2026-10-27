"""Ejecuta un JSON en SI. Un cálculo válido no implica cumplimiento."""
import argparse,json
from pathlib import Path
from src.analysis.pipeline import analyze
from src.reporting.tables import report_tables
from src.reporting.exports import json_bytes,pdf_bytes

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--output',default='outputs/caso');a=p.parse_args()
    try:
        result=analyze(json.loads(Path(a.input).read_text(encoding='utf-8')))
        report=report_tables(result)
    except (ValueError,TypeError,KeyError) as exc:
        p.exit(2,'ENTRADA RECHAZADA: '+str(exc)+'\n')
    dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.with_suffix('.json').write_bytes(json_bytes(result,report));dest.with_suffix('.pdf').write_bytes(pdf_bytes(report))
    print('Cálculo ejecutado; revisar estados y pendientes:',dest)
    for c in report.get('checks',[]):print(c['status'],c['name'])
if __name__=='__main__':main()
