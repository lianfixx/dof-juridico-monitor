VALID_STATES = {"INTEGRO", "PARCIAL", "PENDIENTE", "INACCESIBLE"}

def can_claim_complete(records, universe_closed: bool) -> bool:
    """True only when universe is closed and every record is INTEGRO."""
    if not universe_closed or not records:
        return False
    return all(r.get("status") == "INTEGRO" for r in records)

def coverage_label(records, universe_closed: bool) -> str:
    return "COBERTURA COMPLETA AL CORTE" if can_claim_complete(records, universe_closed) else "REPORTE PARCIAL AL CORTE"

def validate_direct_links(items):
    """Return items without an http(s) source URL."""
    return [i for i in items if not str(i.get("source_url", "")).startswith(("https://", "http://"))]
