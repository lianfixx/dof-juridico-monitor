#!/usr/bin/env python3
"""Lista compacta de lo que el box bajó para una entrega, para decidir el relevo con el lector por API.

Uso (en el box):  python3 bin/relevo_lista.py <entrega>      (por ejemplo 2026-11-24)

Imprime un JSON pequeño: cada edición nueva (no `ya_reportada`) y cada anexo publicado aparte, con su
SHA-256 y sus páginas, tal como quedaron en fuentes/<entrega>/dof/inventario.json. Lo ya reportado y lo que
no se pudo descargar van aparte. La `huella` permite a scripts/api/relevo.py detectar si la lista se copió con
un error al pasarla del box a la sesión. No lee ni decide nada: la decisión es de scripts/api/relevo.py.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def lista(inventario: dict, entrega: str) -> dict:
    documentos, sin_descargar = [], []
    for e in inventario.get("ediciones", []):
        if e.get("ya_reportada"):
            continue
        base = {"fecha": e.get("fecha"), "edicion": e.get("edicion"), "numero": e.get("numero")}
        if not e.get("pdf") or not e.get("sha256"):
            sin_descargar.append({**base, "que": "edición"})
            continue
        documentos.append({**base, "id": e["pdf"][:-4], "tipo": "edicion", "sha256": e["sha256"],
                           "paginas": e.get("paginas_reales"), "paginas_ok": e.get("ok_paginas") is not False})
        for a in e.get("anexos", []):
            if a.get("error") or not a.get("archivo") or not a.get("sha256"):
                sin_descargar.append({**base, "que": "anexo", "url": str(a.get("url", ""))[:120]})
                continue
            documentos.append({**base, "id": "anexo_" + a["archivo"][:-4], "tipo": "anexo", "sha256": a["sha256"],
                               "paginas": a.get("paginas"), "paginas_ok": True})
    return {"formato": "dof-relevo-lista-v1", "entrega": entrega, "documentos": documentos, "sin_descargar": sin_descargar,
            "errores_de_fuentes": len(inventario.get("errores", [])), "huella": huella(documentos)}


def huella(documentos: list) -> str:
    """SHA-256 de los identificadores, hashes y páginas, en orden: prueba de que la lista se copió sin errores."""
    return hashlib.sha256("|".join(f"{d.get('id')}:{d.get('sha256')}:{d.get('paginas')}" for d in documentos).encode()).hexdigest()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    ruta = RAIZ / "fuentes" / argv[1] / "dof" / "inventario.json"
    try:
        inventario = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(json.dumps({"formato": "dof-relevo-lista-v1", "entrega": argv[1], "error": f"sin inventario: {type(e).__name__}"}))
        return 1
    print(json.dumps(lista(inventario, argv[1]), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
