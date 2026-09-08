from io import BytesIO
import json
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import pytest
from pypdf import PdfReader
from src.units import Quantity as Q, UnitSystem, to_si, from_si, display_unit
from src.analysis.pipeline import analyze
from src.models.project import DEFAULT_INPUT
from src.reporting.tables import INPUT_FIELDS, report_tables
from src.reporting.exports import excel_bytes, pdf_bytes, json_bytes
from app.plots import beam_plots, profile_plot, section_plot


@pytest.mark.parametrize('q',list(Q))
@pytest.mark.parametrize('system',list(UnitSystem))
def test_conversion_roundtrip(q,system):
    for v in (-.007,0,1234.56789):
        assert to_si(from_si(v,q,system),q,system) == pytest.approx(v,rel=1e-14)


def test_units_known_and_bad_inputs():
    assert to_si(1,Q.SPAN,'USCS') == .3048
    assert to_si(1,Q.SECTION_LENGTH,'USCS') == .0254
    assert to_si(1,Q.FORCE,'USCS') == pytest.approx(4448.2216152605)
    assert to_si(1,Q.STRESS,'USCS') == pytest.approx(6894.757293168)
    for value in (True,float('inf'),float('nan'),'1'):
        with pytest.raises(ValueError):
            from_si(value,Q.FORCE,'SI')


@pytest.mark.parametrize('system',['SI','USCS'])
def test_exports_numeric_and_readable(system):
    r = analyze({**DEFAULT_INPUT,'project':'=1+2 <proyecto> & prueba','author':'Equipo USS'})
    report = report_tables(r,system,'service',2.5,0)
    out = excel_bytes(report)
    ns = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with ZipFile(BytesIO(out)) as book:
        workbook = ET.fromstring(book.read('xl/workbook.xml'))
        assert len(workbook.find('m:sheets',ns)) == 8
        for path in book.namelist():
            if path.startswith('xl/worksheets/sheet'):
                sheet = ET.fromstring(book.read(path))
                assert not sheet.findall('.//m:f',ns)  # User text is never an Excel formula.
        section = ET.fromstring(book.read('xl/worksheets/sheet3.xml'))
        area = section.find('.//m:c[@r="B2"]/m:v',ns)
        assert float(area.text) == pytest.approx(from_si(.32,Q.SECTION_AREA,system))
        assert section.find('.//m:c[@r="B2"]',ns).get('t') != 's'
    pdf = PdfReader(BytesIO(pdf_bytes(report)))
    text = '\n'.join(p.extract_text() for p in pdf.pages)
    for word in ('Transferencia','Servicio','Explorador','Memoria','Tensión inferior','Equipo USS'):
        assert word in text
    assert 4 <= len(pdf.pages) <= 10
    assert all(len(page.extract_text()) > 120 for page in pdf.pages)
    data = json.loads(json_bytes(r,report))
    assert data['input_si']['initial_force_n'] == 1e6
    assert analyze(data['input_si']).service.stress == r.service.stress
    assert data['report']['x_m'] == 2.5
    assert data['report']['memory'][-1]['value'] == report['memory'][-1]['value']


@pytest.mark.parametrize('system',['SI','USCS'])
def test_plot_values_and_labels(system):
    r = analyze(DEFAULT_INPUT)
    shear,moment = beam_plots(r,system)
    assert shear.data[0].y[0] == pytest.approx(from_si(r.transfer.reaction_n,Q.FORCE,system))
    assert moment.data[1].y[50] == pytest.approx(from_si(r.service.midspan_moment_n_m,Q.MOMENT,system))
    assert display_unit(system,Q.MOMENT).symbol in moment.layout.yaxis.title.text
    profile = profile_plot(r,system,5)
    assert profile.data[0].x[-1] == pytest.approx(from_si(r.transfer.stress.top_pa,Q.STRESS,system))
    fig = section_plot(r.section,r.input.eccentricity_m,system,r,'service',5,.2)
    assert fig.data[0].type == 'heatmap'
    assert fig.data[0].zmin == -fig.data[0].zmax
    assert len(fig.layout.shapes) >= 3
