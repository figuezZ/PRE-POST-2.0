"""Referencias independientes; nunca recalcula valores esperados con producción."""
import json, math, argparse
from pathlib import Path
from src.analysis.pipeline import analyze
from src.models.project import DEFAULT_INPUT
from src.checks.engineering import shear_capacity


def run_references():
    root=Path(__file__).resolve().parents[1]
    cases=json.loads((root/'examples/reference_expected.json').read_text())
    rows=[]
    for case in cases:
        result=analyze(case['input'])
        for c in case['controls']:
            obj=result
            for key in c['path'].split('.'):
                obj=obj[key] if isinstance(obj,dict) else getattr(obj,key)
            error=abs(obj-c['expected'])
            tolerance=max(c.get('atol',0),c['rtol']*abs(c['expected']))
            rows.append(dict(case=case['name'],quantity=c['path'],obtained=obj,expected=c['expected'],
                absolute_error=error,relative_error=error/abs(c['expected']) if c['expected'] else None,
                tolerance=tolerance,passed=error<=tolerance,source=c['source']))
    sh=shear_capacity(30e6,.4,.9,.8,360192,305356.8,1403e3,.00122,1860e6,420e6,2*math.pi*.008**2/4,.25,.635,.36)
    expected=701084.873606613
    rows.append(dict(case='B2 Corte de guía, cálculo local',quantity='Vc N',obtained=sh['vc_n'],expected=expected,
        absolute_error=abs(sh['vc_n']-expected),relative_error=abs(sh['vc_n']-expected)/expected,
        tolerance=.01,passed=abs(sh['vc_n']-expected)<=.01,source='Guía p.4: cap 400 sqrt(30)*0.4*0.8 kN; independiente de producción. Publicado 701.10 kN.'))
    return dict(version='2.1.0-rc1',status='PASS' if all(r['passed'] for r in rows) else 'FAIL',comparisons=rows,
        source_discrepancies=[c['published_discrepancy'] for c in cases if 'published_discrepancy' in c],
        manual_validation='PENDIENTE: no hay manuscritos del equipo incorporados',
        normative_validation='PRELIMINAR: no ratificada por docente',
        pending=['Flecha diferida','Zonas locales y desarrollo','Sección transformada integrada','Contribuciones humanas'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='outputs/validation_summary.json')
    args=parser.parse_args();summary=run_references()
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(summary,indent=2,ensure_ascii=False))
    print(summary['status'],len(summary['comparisons']),'comparaciones; validación manual pendiente')
    raise SystemExit(0 if summary['status']=='PASS' else 1)
