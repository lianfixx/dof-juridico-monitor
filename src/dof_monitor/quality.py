"""Conservative, evidence-based checks for DOF/SJF publication packages.

These checks validate structured evidence, not whether a human actually read a page.
"""
from urllib.parse import urlparse

VALID_STATES = {"INTEGRO", "PARCIAL", "PENDIENTE", "INACCESIBLE"}
REQUIRED_FILES = ("report_pdf", "report_docx", "study_pdf", "study_docx")

def can_claim_complete(records, universe_closed: bool) -> bool:
    if not universe_closed or not records:
        return False
    return all(r.get("status") == "INTEGRO" for r in records)

def coverage_label(records, universe_closed: bool) -> str:
    return "COBERTURA COMPLETA AL CORTE" if can_claim_complete(records, universe_closed) else "REPORTE PARCIAL AL CORTE"

def validate_direct_links(items):
    """Return items lacking a valid HTTP(S) source with a hostname."""
    return [i for i in items if not _valid_url(i.get("source_url"))]

def _valid_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("https", "http") and bool(parsed.hostname)
    except ValueError:
        return False

def evidence_gaps(manifest):
    """Identify missing proof. A passing result is not proof of actual reading."""
    gaps = []
    if not isinstance(manifest, dict):
        return ["manifest missing"]
    for module in ("dof", "sjf"):
        block = manifest.get(module)
        if not isinstance(block, dict):
            gaps.append(f"{module}: missing coverage")
            continue
        if not block.get("universe_closed"):
            gaps.append(f"{module}: universe not closed")
        records = block.get("records")
        if not isinstance(records, list) or not records:
            gaps.append(f"{module}: no document records")
            continue
        for index, record in enumerate(records):
            prefix = f"{module}: document {index + 1}"
            if not isinstance(record, dict):
                gaps.append(f"{prefix}: invalid record")
                continue
            if record.get("status") != "INTEGRO":
                gaps.append(f"{prefix}: not integral")
            if not _valid_url(record.get("url")):
                gaps.append(f"{prefix}: invalid source URL")
            total = record.get("total_pages")
            ranges = record.get("read_ranges")
            if type(total) is not int or total < 1 or not isinstance(ranges, list):
                gaps.append(f"{prefix}: missing or invalid page evidence")
            else:
                valid = all(isinstance(pair, list) and len(pair) == 2
                            and all(type(n) is int for n in pair)
                            and 1 <= pair[0] <= pair[1] <= total for pair in ranges)
                if not valid:
                    gaps.append(f"{prefix}: invalid page ranges")
                else:
                    ordered = sorted(ranges)
                    cursor = 1
                    for start, end in ordered:
                        if start != cursor:
                            gaps.append(f"{prefix}: page gap or overlap at {cursor}")
                            break
                        cursor = end + 1
                    else:
                        if cursor != total + 1:
                            gaps.append(f"{prefix}: unread final pages")
            if record.get("annexes_verified") is not True:
                gaps.append(f"{prefix}: annex verification missing")
            if not record.get("reading_notes"):
                gaps.append(f"{prefix}: reading notes missing")
    return gaps

def can_release_package(manifest):
    """Fail closed for final generation and sending; requires explicit human audit."""
    if evidence_gaps(manifest):
        return False
    if manifest.get("audit_approved") is not True:
        return False
    files = manifest.get("files")
    if not isinstance(files, dict):
        return False
    return all(isinstance(files.get(k), dict) and
               files[k].get("render_checked") is True and
               bool(files[k].get("sha256")) for k in REQUIRED_FILES)

def can_attempt_send(manifest):
    """Sending requires explicit deduplication and an unambiguous prior state."""
    return (can_release_package(manifest)
            and manifest.get("recipient") == "emilianogarciamilla@gmail.com"
            and manifest.get("duplicates_checked") is True
            and manifest.get("send_state") == "NOT_SENT")
