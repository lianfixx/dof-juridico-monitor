"""Local SJF intake. Never treats downloading or extraction as proof of reading.

Run with: python -m src.dof_monitor.sjf_intake init --date YYYY-MM-DD --out DIR
           python -m src.dof_monitor.sjf_intake add --control DIR/SJF_DATE_Control.json --file PATH --url URL
           python -m src.dof_monitor.sjf_intake check --control DIR/SJF_DATE_Control.json
Files stay local/private; this tool never sends email or writes to GitHub.
"""
import argparse
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

def _save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)

def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def initialize(edition, directory):
    date.fromisoformat(edition)
    folder = Path(directory)
    folder.mkdir(parents=True, exist_ok=True)
    control = folder / f"SJF_{edition}_Control.json"
    if control.exists():
        raise FileExistsError(f"Refusing to overwrite existing control: {control}")
    data = {
        "schema_version": "sjf-intake-1",
        "edition_date": edition,
        "edition_verified": False,
        "official_index_url": "https://sjf2.scjn.gob.mx/",
        "inventory_reconciled": False,
        "universe_closed": False,
        "documents": [],
        "legal_review_approved": False,
        "audit_approved": False,
        "status": "PENDIENTE",
        "deliverables": {},
        "email": {"state": "NOT_SENT", "duplicate_check": "PENDIENTE"},
        "last_checked_utc": datetime.now(timezone.utc).isoformat()
    }
    _save(control, data)
    return control

def add_document(control, file_path, source_url, identifier=None):
    control = Path(control)
    data = _load(control)
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    parsed = urlsplit(source_url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("An official HTTPS source URL is required")
    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF source files are accepted")
    with path.open("rb") as stream:\n        signature = stream.read(5)\n    if signature != b"%PDF-":
        raise ValueError("File does not have a PDF signature")
    digest = _hash(path)
    if any(x["sha256"] == digest for x in data["documents"]):
        raise ValueError("Identical PDF already registered")
    # Count only when pypdf is installed. Unknown count is a blocker.
    pages = None
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(str(path)).pages)
    except Exception:
        pages = None
    record = {
        "id": identifier or path.stem,
        "source_url": source_url,
        "local_path": str(path),
        "sha256": digest,
        "pages": pages,
        "read_ranges": [],
        "reading_notes": "",
        "annexes": [],
        "annexes_verified": False,
        "legal_checks": {
            "identity": False, "type": False, "reasons": False,
            "vote": False, "binding_force": False, "temporal_scope": False,
            "effects": False, "official_sources": False
        },
        "status": "PENDIENTE"
    }
    data["documents"].append(record)
    data["status"] = "PARCIAL"
    data["last_checked_utc"] = datetime.now(timezone.utc).isoformat()
    _save(control, data)
    return record

def gaps(data, verify_files=True):
    errors = []
    if not data.get("edition_verified"):
        errors.append("Official publication date not verified")
    if not data.get("inventory_reconciled") or not data.get("universe_closed"):
        errors.append("Official universe and pagination not reconciled")
    docs = data.get("documents")
    if not isinstance(docs, list) or not docs:
        errors.append("No documents in inventory")
        return errors
    seen = set()
    for i, doc in enumerate(docs, 1):
        name = f"document {i}"
        identifier = doc.get("id")
        if not identifier or identifier in seen:
            errors.append(f"{name}: missing or duplicate ID")
        seen.add(identifier)
        if doc.get("status") != "INTEGRO":
            errors.append(f"{name}: not read in full")
        n = doc.get("pages")
        ranges = doc.get("read_ranges")
        if type(n) is not int or n < 1 or not isinstance(ranges, list):
            errors.append(f"{name}: page count/ranges absent")
        else:
            cursor = 1
            valid = True
            for pair in sorted(ranges):
                if not isinstance(pair, list) or len(pair) != 2 or any(type(v) is not int for v in pair) or pair[0] != cursor or pair[1] < pair[0] or pair[1] > n:
                    valid = False
                    break
                cursor = pair[1] + 1
            if not valid or cursor != n + 1:
                errors.append(f"{name}: page gaps, overlaps or invalid ranges")
        if not str(doc.get("reading_notes", "")).strip():
            errors.append(f"{name}: reading notes missing")
        if doc.get("annexes_verified") is not True:
            errors.append(f"{name}: annexes not verified")
        for field, passed in doc.get("legal_checks", {}).items():
            if passed is not True:
                errors.append(f"{name}: legal check {field} pending")
        if not doc.get("legal_checks"):
            errors.append(f"{name}: legal checks missing")
        if verify_files:
            path = Path(doc.get("local_path", ""))
            if not path.is_file() or _hash(path) != doc.get("sha256"):
                errors.append(f"{name}: source PDF missing or changed")
    if data.get("legal_review_approved") is not True:
        errors.append("Legal review pending")
    if data.get("audit_approved") is not True:
        errors.append("Final audit pending")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("init")
    a.add_argument("--date", required=True)
    a.add_argument("--out", required=True)
    a = sub.add_parser("add")
    a.add_argument("--control", required=True)
    a.add_argument("--file", required=True)
    a.add_argument("--url", required=True)
    a.add_argument("--id")
    a = sub.add_parser("check")
    a.add_argument("--control", required=True)
    args = parser.parse_args()
    if args.command == "init":
        print(initialize(args.date, args.out))
    elif args.command == "add":
        print(json.dumps(add_document(args.control, args.file, args.url, args.id), ensure_ascii=False, indent=2))
    else:
        errors = gaps(_load(args.control))
        if errors:
            print("PARCIAL / NO FINAL\n" + "\n".join("- " + e for e in errors))
            raise SystemExit(2)
        print("Evidence fields complete; independently verify actual reading, legal analysis and attachments.")

if __name__ == "__main__":
    main()
