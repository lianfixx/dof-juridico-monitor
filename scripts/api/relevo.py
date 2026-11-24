#!/usr/bin/env python3
"""Relevo entre el lector por API y la suscripción: ¿qué documentos ya están leídos y cuáles faltan?

Uso (en la sesión de Claude, con el repositorio privado clonado):
  relevo.py comprobar <dof-trabajo>/fuentes/<entrega>/ESTADO_API.json <lista del box>.json

La lista del box sale de `python3 bin/relevo_lista.py <entrega>` (scripts/box/relevo_lista.py). Compara, documento
por documento, lo que el box bajó con lo que el lector por API dejó íntegro. Un documento queda «por API» solo
si es el mismo PDF (mismo SHA-256), tiene las mismas páginas y el lector lo dejó íntegro: todos sus bloques
comprobados, sin huecos y sin páginas sin texto ni OCR. Cualquier otra cosa queda «por suscripción», con su
motivo. No usa modelo ni red: mismas entradas, mismo veredicto.

Veredicto y código de salida: TOTAL (0), todo por API; PARCIAL (3), una parte; NINGUNO (4), nada.
La suscripción lee íntegro lo que quede «por suscripción»; lo que quedó «por API» no se vuelve a leer desde cero
(sí pasa por la doble lectura y la auditoría del cierre, como cualquier nota).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def comprobar(estado: dict | None, lista: dict) -> dict:
    entrega = lista.get("entrega")
    docs_box = lista.get("documentos") or []
    v = {"formato": "dof-relevo-v1", "entrega": entrega, "relevo": "NINGUNO", "por_api": [], "por_suscripcion": [],
         "motivos": [], "sintesis_ok": False, "estado_api": None, "corrida_api": None, "fin_api_utc": None,
         "solo_en_api": [], "sin_descargar_en_box": lista.get("sin_descargar") or []}

    def nada(motivo: str) -> dict:
        v["motivos"].append(motivo)
        v["por_suscripcion"] = [{"id": d.get("id"), "motivo": motivo} for d in docs_box]
        return v

    if lista.get("error"):
        return nada(f"el box no tiene inventario de la entrega ({lista['error']})")
    if not docs_box:
        v["relevo"] = "SIN_DOCUMENTOS"
        v["motivos"].append("el box no tiene ediciones nuevas en esta entrega")
        return v
    if not isinstance(estado, dict):
        return nada("no hay ESTADO_API.json de esta entrega: el lector por API no corrió o no terminó")
    v.update({"estado_api": estado.get("estado"), "corrida_api": estado.get("run_id"), "fin_api_utc": estado.get("fin_utc"),
              "sintesis_ok": str(estado.get("sintesis", "")).startswith("ok")})
    if estado.get("formato") != "dof-lector-api-v2":
        return nada(f"formato de estado desconocido: {estado.get('formato')}")
    if estado.get("entrega") != entrega:
        return nada(f"el estado es de otra entrega ({estado.get('entrega')})")
    if estado.get("estado") not in ("INTEGRO", "PARCIAL"):
        return nada(f"el lector por API terminó en {estado.get('estado')}")
    por_sha = {d.get("sha256_pdf"): d for d in estado.get("documentos_leidos") or [] if d.get("sha256_pdf")}
    vistos = set()
    for d in docs_box:
        api = por_sha.get(d.get("sha256"))
        if api is None:
            motivo = "el lector por API no leyó este PDF (documento nuevo o SHA-256 distinto)"
        elif not api.get("integro"):
            motivo = "el lector por API no lo dejó íntegro"
        elif d.get("paginas") and api.get("paginas") != d.get("paginas"):
            motivo = f"páginas distintas: box {d.get('paginas')}, API {api.get('paginas')}"
        elif d.get("paginas_ok") is False:
            motivo = "en el box las páginas reales no coinciden con las declaradas"
        else:
            motivo = ""
        if api is not None:
            vistos.add(api.get("sha256_pdf"))
        if motivo:
            v["por_suscripcion"].append({"id": d.get("id"), "motivo": motivo})
        else:
            v["por_api"].append({"id": d.get("id"), "id_api": api.get("id"), "paginas": api.get("paginas"), "bloques": api.get("bloques")})
    v["solo_en_api"] = [d.get("id") for sha, d in por_sha.items() if sha not in vistos]
    v["relevo"] = "TOTAL" if not v["por_suscripcion"] else ("PARCIAL" if v["por_api"] else "NINGUNO")
    if v["sin_descargar_en_box"]:
        v["motivos"].append("el box no pudo descargar algo: resolverlo con las vías B o C antes de cerrar")
    if not v["sintesis_ok"] and v["por_api"]:
        v["motivos"].append("la síntesis del preliminar no quedó completa: usar las notas y el inventario, no las candidatas")
    return v


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] != "comprobar":
        print(__doc__)
        return 2
    try:
        lista = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(json.dumps({"formato": "dof-relevo-v1", "relevo": "NINGUNO", "motivos": [f"lista del box ilegible: {type(e).__name__}"]}))
        return 4
    try:
        estado = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        estado = None
    v = comprobar(estado, lista)
    print(json.dumps(v, ensure_ascii=False, indent=1))
    return {"TOTAL": 0, "PARCIAL": 3}.get(v["relevo"], 4)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
