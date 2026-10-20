import pytest
from src.dof_monitor.sjf_artifacts import validate_editorial, build, OPINION_SLOT

def sample():
    return {
        "summary":"La publicación exige revisar los límites de obligatoriedad antes de aplicar el criterio.",
        "items":[{
            "title":"Criterio hipotético",
            "effect":"Ejemplo no real para probar el generador.",
            "status":"Tesis aislada; no obligatoria",
            "importance":"Verificar hechos y régimen temporal",
            "study":"Explicación, fundamentos, límites, ejemplo hipotético y contraargumento, redactados sólo como prueba.",
            "source_url":"https://sjfsemanal.scjn.gob.mx/detalle/tesis/2031846"
        }],
        "suggested_comment":"El criterio plantea una distinción jurídica relevante que conviene examinar con cautela. Antes de trasladarlo a un expediente concreto debemos comprobar los hechos, el órgano emisor, el fundamento y la temporalidad aplicable. También resulta indispensable contrastar los posibles argumentos contrarios y evitar atribuir efectos generales a una resolución particular sin respaldo suficiente.",
        "draft_email":"Licenciado, buen día. Le comparto la actualización del Semanario Judicial de la Federación correspondiente al periodo revisado. El reporte presenta un criterio de ejemplo, utilizado únicamente para verificar el funcionamiento técnico del generador, sin afirmar que se trate de una publicación real del periodo. Antes de aplicar cualquier razonamiento a un asunto del despacho conviene revisar su fuente primaria, los hechos relevantes y la fuerza jurídica del criterio. La guía adjunta desarrolla los límites y los puntos que requerirían una comprobación adicional. " + OPINION_SLOT + " Saludos, Emiliano García Milla"
    }

def test_valid_editorial():
    assert validate_editorial(sample()) == []

def test_missing_source_blocks():
    x=sample()
    x["items"][0]["source_url"]="https://example.org"
    assert any("non-official" in e for e in validate_editorial(x))

def test_missing_opinion_slot_blocks():
    x=sample()
    x["draft_email"]=x["draft_email"].replace(OPINION_SLOT,"")
    assert validate_editorial(x)

def test_incomplete_control_blocks_generation(tmp_path):
    from src.dof_monitor.sjf_intake import initialize
    import json
    control=initialize("2026-10-16",tmp_path)
    editorial=tmp_path/"editorial.json"
    editorial.write_text(json.dumps(sample()),encoding="utf-8")
    with pytest.raises(ValueError,match="NO FINAL"):
        build(control,editorial,tmp_path/"output")
    assert not (tmp_path/"output").exists()

def test_four_real_files_generated_but_not_final(tmp_path):
    import json
    from reportlab.pdfgen import canvas
    from pypdf import PdfReader
    from docx import Document
    from src.dof_monitor.sjf_intake import initialize, add_document, _load, _save
    from src.dof_monitor.sjf_weekly import import_inventory
    import csv

    control = initialize("2026-10-16", tmp_path)
    source = tmp_path / "source.pdf"
    pdf = canvas.Canvas(str(source))
    pdf.drawString(40, 750, "Synthetic test only")
    pdf.save()
    url = "https://sjfsemanal.scjn.gob.mx/detalle/tesis/2031846"
    csvpath = tmp_path / "index.csv"
    with csvpath.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id","section","type","official_url","related_ids"])
        writer.writeheader()
        writer.writerow({"id":"2031846","section":"Pleno","type":"tesis","official_url":url,"related_ids":""})
    import_inventory(control, csvpath, url, "Synthetic index for integration test")
    add_document(control, source, url, "2031846")
    data = _load(control)
    data.update(edition_verified=True, inventory_reconciled=True, universe_closed=True,
                legal_review_approved=True, audit_approved=True)
    document = data["documents"][0]
    document.update(status="INTEGRO", pages=1, read_ranges=[[1,1]],
                    reading_notes="Synthetic test", annexes_verified=True)
    document["legal_checks"] = {key:True for key in document["legal_checks"]}
    _save(control, data)
    editorial = tmp_path / "editorial.json"
    editorial.write_text(json.dumps(sample()), encoding="utf-8")
    output = tmp_path / "out"
    files = build(control, editorial, output)
    assert len(files) == 4
    assert all(not x["render_checked"] for x in files.values())
    assert len(list(output.glob("*.pdf"))) == 2
    assert len(list(output.glob("*.docx"))) == 2
    assert all(len(PdfReader(str(p)).pages) >= 1 for p in output.glob("*.pdf"))
    assert all(Document(str(p)).paragraphs for p in output.glob("*.docx"))
    assert _load(control)["status"] == "READY_FOR_VISUAL_REVIEW"
