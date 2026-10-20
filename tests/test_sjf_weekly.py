import csv
import pytest
from src.dof_monitor.sjf_intake import initialize, add_document, _load
from src.dof_monitor.sjf_weekly import (
    load_inventory, import_inventory, reconcile, pending_links, audit,
)

URL = "https://sjfsemanal.scjn.gob.mx/detalle/tesis/2031846"
def inventory_csv(tmp_path, rows):
    path = tmp_path / "official.csv"
    with path.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=["id","section","type","official_url","related_ids"])
        writer.writeheader()
        writer.writerows(rows)
    return path

def item(identifier="2031846", related=""):
    return {"id":identifier,"section":"Pleno - jurisprudencia","type":"tesis",
            "official_url":URL,"related_ids":related}

def test_missing_inventory_blocks(tmp_path):
    control=initialize("2026-10-16",tmp_path)
    assert "No official inventory" in reconcile(_load(control))[0]

def test_import_requires_real_official_url(tmp_path):
    control=initialize("2026-10-16",tmp_path)
    csvfile=inventory_csv(tmp_path,[item()])
    with pytest.raises(ValueError):
        import_inventory(control,csvfile,"https://example.com","Checked all pages")

def test_import_never_marks_complete(tmp_path):
    control=initialize("2026-10-16",tmp_path)
    csvfile=inventory_csv(tmp_path,[item()])
    assert import_inventory(control,csvfile,URL,"Index sections and pagination checked") == 1
    data=_load(control)
    assert data["universe_closed"] is False
    assert pending_links(data)[0]["state"]=="NOT_DOWNLOADED"
    assert "MISSING" in reconcile(data)[0]
    assert audit(control)

def test_reject_duplicate_identifiers(tmp_path):
    csvfile=inventory_csv(tmp_path,[item(),item()])
    with pytest.raises(ValueError,match="duplicate"):
        load_inventory(csvfile)

def test_reject_unofficial_document_url(tmp_path):
    row=item()
    row["official_url"]="https://example.com/false"
    with pytest.raises(ValueError,match="non-SCJN"):
        load_inventory(inventory_csv(tmp_path,[row]))

def test_detect_mismatch_and_missing_related(tmp_path):
    control=initialize("2026-10-16",tmp_path)
    csvfile=inventory_csv(tmp_path,[item(related="sentencia-1")])
    import_inventory(control,csvfile,URL,"Reviewed weekly index")
    pdf=tmp_path/"source.pdf"
    pdf.write_bytes(b"%PDF-1.4\nplaceholder")
    add_document(control,pdf,"https://sjf2.scjn.gob.mx/")
    problems=reconcile(_load(control))
    assert any("MISSING" in p for p in problems)
    assert any("RELATED DOCUMENT" in p for p in problems) is False
