import json
import pytest
from src.dof_monitor.sjf_intake import initialize, add_document, gaps, _load

def test_initialize_fail_closed(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    data = _load(control)
    assert data["status"] == "PENDIENTE"
    assert gaps(data, verify_files=False)
    with pytest.raises(FileExistsError):
        initialize("2026-10-16", tmp_path)

def test_add_document_registers_without_claiming_reading(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "official.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    record = add_document(control, pdf, "https://sjf2.scjn.gob.mx/")
    assert record["status"] == "PENDIENTE"
    assert record["read_ranges"] == []
    assert record["annexes_verified"] is False
    assert any("not read in full" in x for x in gaps(_load(control)))

def test_add_rejects_duplicate_pdf(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "official.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    add_document(control, pdf, "https://sjf2.scjn.gob.mx/")
    with pytest.raises(ValueError, match="already registered"):
        add_document(control, pdf, "https://sjf2.scjn.gob.mx/")

def test_add_rejects_untrusted_url_and_bad_pdf(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "bad.pdf"
    pdf.write_bytes(b"not a pdf")
    with pytest.raises(ValueError):
        add_document(control, pdf, "https://sjf2.scjn.gob.mx/")
    with pytest.raises(ValueError):
        add_document(control, pdf, "http://example.com/")

def test_full_record_requires_all_legal_checks(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "official.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    add_document(control, pdf, "https://sjf2.scjn.gob.mx/")
    data = _load(control)
    data.update(edition_verified=True, inventory_reconciled=True, universe_closed=True,
                legal_review_approved=True, audit_approved=True)
    doc = data["documents"][0]
    doc.update(pages=2, read_ranges=[[1, 2]], status="INTEGRO",
               reading_notes="Specific verified analysis", annexes_verified=True)
    assert any("legal check" in x for x in gaps(data, verify_files=False))
    doc["legal_checks"] = {k: True for k in doc["legal_checks"]}
    assert gaps(data, verify_files=False) == []

def test_gap_detection(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "official.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    add_document(control, pdf, "https://sjf2.scjn.gob.mx/")
    data = _load(control)
    data["documents"][0].update(pages=3,read_ranges=[[1,1],[3,3]])
    assert any("page gaps" in x for x in gaps(data, verify_files=False))

def test_add_rejects_non_scjn_https_domain(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "official.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    with pytest.raises(ValueError):
        add_document(control, pdf, "https://scjn.gob.mx.evil.example/tesis")

def test_malformed_page_ranges_fail_closed(tmp_path):
    control = initialize("2026-10-16", tmp_path)
    pdf = tmp_path / "official.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    add_document(control, pdf, "https://sjf2.scjn.gob.mx/")
    data = _load(control)
    data["documents"][0].update(pages=2, read_ranges=[{"bad": 1}])
    assert any("page gaps" in x for x in gaps(data, verify_files=False))
