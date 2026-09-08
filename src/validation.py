"""Control analítico reproducible, ejecutable sin Streamlit."""
import argparse
import json
from math import isclose
from pathlib import Path
from src.models.project import DEFAULT_INPUT
from src.analysis.pipeline import analyze
from src.sections.composite import template, component_properties


def validate_all():
    r = analyze(DEFAULT_INPUT)
    t = component_properties(template('T',.4,.8),25000)
    checks = [
        ('A rectangular',r.section.area_m2,.32), ('I rectangular',r.section.inertia_m4,.017066666666666667),
        ('Peso propio',r.section.self_weight_n_m,8000), ('Reacción transferencia',r.transfer.reaction_n,40000),
        ('Momento transferencia',r.transfer.midspan_moment_n_m,100000),
        ('Superior transferencia',r.transfer.stress.top_pa,-781250),
        ('Inferior transferencia',r.transfer.stress.bottom_pa,-5468750),
        ('Pe servicio',r.service.force_n,850000), ('Carga servicio',r.service.uniform_load_n_m,13000),
        ('Momento servicio',r.service.midspan_moment_n_m,162500),
        ('Superior servicio',r.service.stress.top_pa,-2480468.75),
        ('Inferior servicio',r.service.stress.bottom_pa,-2832031.25),
        ('A sección T',t.area_m2,.1408), ('Centroide T',t.centroid_from_bottom_m,.5018181818181818),
        ('I sección T',t.inertia_m4,.008343427878787879),
    ]
    rows = [dict(name=name,calculated=actual,expected=expected,relative_tolerance=1e-10,
        passed=isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-12)) for name,actual,expected in checks]
    return dict(version='2.0.0',status='PASS' if all(r['passed'] for r in rows) else 'FAIL',comparisons=rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all',action='store_true',help='Ejecutar todos los controles disponibles')
    parser.add_argument('--output',default='outputs/validation_summary.json')
    args = parser.parse_args()
    report = validate_all()
    path = Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f"Autovalidación: {report['status']} ({sum(r['passed'] for r in report['comparisons'])}/{len(report['comparisons'])})")
    raise SystemExit(0 if report['status']=='PASS' else 1)


if __name__ == '__main__':
    main()
