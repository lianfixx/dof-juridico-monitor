"""Official-index reconciliation for weekly SJF intake (stdlib only).

Inventory CSV columns: id,section,type,official_url,related_ids
Each row must be transcribed from the actual official weekly index, including
secondary sections. Never use search snippets to manufacture a weekly universe.
"""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlsplit
from .sjf_intake import _load, _save, gaps

COLUMNS = ("id", "section", "type", "official_url", "related_ids")
PORTALS = (
    "https://sjfsemanal.scjn.gob.mx/",
    "https://sjf2.scjn.gob.mx/",
    "https://www.scjn.gob.mx/coordinacion/gaceta",
)
def _official(url):
    if not isinstance(url, str):
        return False
    p = urlsplit(url)
    return p.scheme == "https" and p.hostname in {
        "sjfsemanal.scjn.gob.mx", "sjf2.scjn.gob.mx", "www.scjn.gob.mx",
        "scjn.gob.mx", "www2.scjn.gob.mx",
    }

def load_inventory(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(COLUMNS).issubset(reader.fieldnames):
            raise ValueError("Inventory CSV must include " + ", ".join(COLUMNS))
        rows = []
        ids = set()
        for line, row in enumerate(reader, 2):
            item = {k: (row.get(k) or "").strip() for k in COLUMNS}
            if not item["id"] or item["id"] in ids:
                raise ValueError(f"Missing/duplicate ID on CSV line {line}")
            if not item["section"] or not item["type"]:
                raise ValueError(f"Missing section/type on CSV line {line}")
            if not _official(item["official_url"]):
                raise ValueError(f"Missing/non-SCJN official URL on CSV line {line}")
            ids.add(item["id"])
            rows.append(item)
    if not rows:
        raise ValueError("Official inventory is empty")
    return rows

def import_inventory(control_path, csv_path, index_url, evidence):
    if not _official(index_url):
        raise ValueError("Official SCJN weekly index URL required")
    if not evidence.strip():
        raise ValueError("Record how the weekly index and pagination were inspected")
    data = _load(control_path)
    if data.get("official_inventory"):
        raise ValueError("Inventory already imported; review explicitly before replacing")
    rows = load_inventory(csv_path)
    data["official_inventory"] = rows
    data["official_index_url"] = index_url
    data["inventory_evidence"] = evidence.strip()
    # Import never certifies completeness; independent reconciliation is required.
    data["inventory_reconciled"] = False
    data["universe_closed"] = False
    data["status"] = "PARCIAL"
    _save(control_path, data)
    return len(rows)

def reconcile(data):
    problems = []
    expected = data.get("official_inventory")
    if not isinstance(expected, list) or not expected:
        return ["No official inventory CSV imported"]
    if not data.get("inventory_evidence"):
        problems.append("Official index/pagination evidence missing")
    ids = [x.get("id") for x in expected]
    if len(set(ids)) != len(ids):
        problems.append("Official inventory contains duplicate identifiers")
    by_id = {x.get("id"): x for x in data.get("documents", [])}
    if len(by_id) != len(data.get("documents", [])):
        problems.append("Document records contain duplicate identifiers")
    expected_ids = set(ids)
    for item in expected:
        key = item["id"]
        doc = by_id.get(key)
        if not doc:
            problems.append(f"MISSING {key} | {item['section']} | {item['official_url']}")
            continue
        if doc.get("source_url") != item["official_url"]:
            problems.append(f"URL MISMATCH {key}: official {item['official_url']}")
        if doc.get("status") != "INTEGRO":
            problems.append(f"UNREAD {key}: {doc.get('status', 'PENDIENTE')}")
        for related in filter(None, (x.strip() for x in item.get("related_ids", "").split(";"))):
            if related not in expected_ids and related not in by_id:
                problems.append(f"RELATED DOCUMENT NOT RESOLVED {key} -> {related}")
    for key in by_id.keys() - expected_ids:
        problems.append(f"EXTRA {key}: verify whether supplementary source, not weekly item")
    return problems

def pending_links(data):
    expected = data.get("official_inventory") or []
    by_id = {x.get("id"): x for x in data.get("documents", [])}
    return [
        {"id": x["id"], "section": x["section"], "type": x["type"],
         "official_url": x["official_url"], "state": (
             "NOT_DOWNLOADED" if x["id"] not in by_id else
             by_id[x["id"]].get("status", "PENDIENTE")
         )}
        for x in expected if x["id"] not in by_id or
        by_id[x["id"]].get("status") != "INTEGRO"
    ]

def audit(control_path):
    data = _load(control_path)
    problems = reconcile(data)
    problems.extend(gaps(data))
    if problems:
        # A manually checked flag cannot override inventory mismatches.
        return list(dict.fromkeys(problems))
    return []

def main():
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest="command", required=True)
    a = subs.add_parser("inventory")
    a.add_argument("--control", required=True)
    a.add_argument("--csv", required=True)
    a.add_argument("--index-url", required=True)
    a.add_argument("--evidence", required=True)
    a = subs.add_parser("missing")
    a.add_argument("--control", required=True)
    a = subs.add_parser("audit")
    a.add_argument("--control", required=True)
    args = p.parse_args()
    if args.command == "inventory":
        print(f"Imported {import_inventory(args.control, args.csv, args.index_url, args.evidence)} official entries; coverage remains PARCIAL")
    elif args.command == "missing":
        data = _load(args.control)
        if not data.get("official_inventory"):
            print(json.dumps({"status":"INVENTORY_REQUIRED","official_portals":PORTALS}, indent=2))
            raise SystemExit(2)
        print(json.dumps(pending_links(data), ensure_ascii=False, indent=2))
    else:
        problems = audit(args.control)
        if problems:
            print("NO FINAL: " + str(len(problems)) + " blockers\n" + "\n".join(problems))
            raise SystemExit(2)
        print("Structural audit passed; verify real reading and legal accuracy independently.")

if __name__ == "__main__":
    main()
