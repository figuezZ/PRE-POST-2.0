"""Validación exclusiva del ejercicio 1; salida reproducible y estados explícitos."""
import subprocess,sys,json,datetime,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.analysis.pipeline import analyze
out=Path('outputs');out.mkdir(exist_ok=True)
r=subprocess.run([sys.executable,'-m','pytest','-q','--junitxml=outputs/pytest_results.xml'],capture_output=True,text=True)
(out/'test_run.txt').write_text(r.stdout+r.stderr)
counts={}
if (out/'pytest_results.xml').exists():
    for s in ET.parse(out/'pytest_results.xml').getroot().iter('testsuite'):
        for k in ('tests','failures','errors','skipped'):counts[k]=counts.get(k,0)+int(s.get(k,0))
case=json.loads(Path('examples/set_ejercicio_1.json').read_text())
result=analyze(case)
summary=dict(case='Ejercicio 1 del set',executed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    status='PASS' if r.returncode==0 else 'FAIL',tests=dict(returncode=r.returncode,**counts),
    checks=result['checks'],manual_validation='PENDIENTE de manuscrito y revisión humana',
    note='PASS se refiere a las pruebas del software, no al cumplimiento resistente.')
(out/'validation_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
print(r.stdout);print('Validación:',summary['status']);sys.exit(r.returncode)
