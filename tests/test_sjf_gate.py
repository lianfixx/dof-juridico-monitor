from src.dof_monitor.quality import evidence_gaps, can_release_package, can_attempt_send, validate_direct_links

def valid_manifest():
    rec = {"status":"INTEGRO","url":"https://sjf2.scjn.gob.mx/x","total_pages":1,"read_ranges":[[1,1]],"annexes_verified":True,"reading_notes":"Revisado"}
    return {"dof":{"universe_closed":True,"records":[dict(rec)]},
            "sjf":{"universe_closed":True,"records":[dict(rec)]},
            "audit_approved":True,
            "files":{k:{"sha256":"abc","render_checked":True} for k in ("report_pdf","report_docx","study_pdf","study_docx")},
            "recipient":"emilianogarciamilla@gmail.com","duplicates_checked":True,"send_state":"NOT_SENT"}

def test_no_manifest_fails_closed():
    assert evidence_gaps(None)
    assert not can_release_package(None)

def test_missing_sjf_blocks():
    m=valid_manifest();del m["sjf"]
    assert not can_release_package(m)

def test_incomplete_document_blocks():
    m=valid_manifest();m["dof"]["records"][0]["status"]="PARCIAL"
    assert not can_release_package(m)

def test_missing_read_ranges_blocks():
    m=valid_manifest();m["sjf"]["records"][0]["read_ranges"]=[]
    assert not can_release_package(m)

def test_missing_annex_verification_blocks():
    m=valid_manifest();m["sjf"]["records"][0]["annexes_verified"]=False
    assert not can_release_package(m)

def test_missing_audit_blocks():
    m=valid_manifest();m["audit_approved"]=False
    assert not can_release_package(m)

def test_missing_render_blocks():
    m=valid_manifest();m["files"]["study_pdf"]["render_checked"]=False
    assert not can_release_package(m)

def test_uncertain_send_blocks():
    m=valid_manifest();m["send_state"]="ENVIO_INCIERTO"
    assert not can_attempt_send(m)

def test_no_dedup_blocks():
    m=valid_manifest();m["duplicates_checked"]=False
    assert not can_attempt_send(m)

def test_wrong_recipient_blocks():
    m=valid_manifest();m["recipient"]="other@example.com"
    assert not can_attempt_send(m)

def test_valid_evidence_structure():
    m=valid_manifest()
    assert not evidence_gaps(m)
    assert can_release_package(m)
    assert can_attempt_send(m)

def test_malformed_links():
    assert len(validate_direct_links([{"source_url":"https://"},{"source_url":"https://valid.example/path"}])) == 1
