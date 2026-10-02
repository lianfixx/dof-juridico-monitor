from src.dof_monitor.quality import can_claim_complete, coverage_label, validate_direct_links

def test_complete_requires_closed_universe():
    assert not can_claim_complete([{"status":"INTEGRO"}], False)

def test_complete_rejects_partial():
    assert not can_claim_complete([{"status":"INTEGRO"},{"status":"PARCIAL"}], True)

def test_complete_accepts_integral_records():
    assert can_claim_complete([{"status":"INTEGRO"},{"status":"INTEGRO"}], True)

def test_label():
    assert coverage_label([{"status":"PENDIENTE"}], True) == "REPORTE PARCIAL AL CORTE"

def test_links():
    assert validate_direct_links([{"source_url":"https://dof.gob.mx/x"}]) == []
