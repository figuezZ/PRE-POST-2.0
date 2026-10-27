"""Ejecutar desde raíz. Conserva evidencia incluso ante fallos."""
import subprocess,sys,json,datetime,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.validation import validate_all
from src.validation_avance2 import run_references
out=Path('outputs');out.mkdir(exist_ok=True)
r=subprocess.run([sys.executable,'-m','pytest','-q','--junitxml=outputs/pytest_results.xml'],capture_output=True,text=True)
(out/'test_run.txt').write_text(r.stdout+r.stderr)
legacy=validate_all();current=run_references()
(out/'validation_legacy.json').write_text(json.dumps(legacy,indent=2,ensure_ascii=False))
counts={}
if (out/'pytest_results.xml').exists():
    suites=ET.parse(out/'pytest_results.xml').getroot().iter('testsuite')
    for s in suites:
        for k in ('tests','failures','errors','skipped'):counts[k]=counts.get(k,0)+int(s.get(k,0))
current.update(executed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline_commit='d59181bcd2a3e111d2d0692dd53a2572aad2169e',
    tests=dict(returncode=r.returncode,**counts),legacy=legacy)
current['status']='PASS' if r.returncode==0 and legacy['status']=='PASS' and current['status']=='PASS' else 'FAIL'
(out/'validation_summary.json').write_text(json.dumps(current,indent=2,ensure_ascii=False))
print(r.stdout);print('Verificación conjunta:',current['status']);sys.exit(0 if current['status']=='PASS' else 1)
