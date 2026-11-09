#!/usr/bin/env python3
"""Manifiesto de una entrega: todo lo que hay en fuentes/<entrega>/ con tamaño y SHA-256,
más el resumen del inventario DOF y del control SJF. Es lo primero que lee la sesión.

`compuerta_fuentes` resume lo que la compuerta 1 (universo cerrado) necesita ver:
números consecutivos desde la última edición ya reportada, páginas reales = declaradas,
errores de descarga, OCR pendiente y errores del SJF. `listo` es true solo si todo cuadra;
si no, `faltantes` dice qué falta. Las ediciones `ya_reportada` cuentan para la
continuidad de números, no para la lectura."""
import glob, hashlib, json, os, sys, time

dest = sys.argv[1].rstrip("/")
files = []
for f in sorted(glob.glob(os.path.join(dest, "**", "*"), recursive=True)):
    if os.path.isfile(f) and not f.endswith(("manifiesto.json", ".tmp", "fuentes.pid")):
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        files.append({"ruta": os.path.relpath(f, dest), "bytes": os.path.getsize(f), "sha256": h.hexdigest()})
man = {"entrega": os.path.basename(dest), "generado": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "archivos": files}
faltantes = []
inv = os.path.join(dest, "dof", "inventario.json")
if os.path.exists(inv):
    i = json.load(open(inv))
    eds = i["ediciones"]
    man["dof"] = {"corte_anterior": i.get("corte_anterior"),
                  "ediciones": [{"fecha": e["fecha"], "edicion": e["edicion"], "numero": e["numero"], "pdf": e["pdf"],
                                 "paginas": e["paginas_reales"], "ok_paginas": e["ok_paginas"], "notas": len(e["notas"]),
                                 "ya_reportada": bool(e.get("ya_reportada")), "motivo": e.get("ya_reportada_motivo"),
                                 "paginas_ocr": len(e.get("paginas_ocr", e.get("paginas_sin_texto", []))),
                                 "ocr": len(e.get("ocr", [])), "ocr_pendiente": e.get("ocr_pendiente", []),
                                 "anexos": [{"archivo": a.get("archivo"), "paginas": a.get("paginas"), "ocr": len(a.get("ocr", [])),
                                             "ocr_pendiente": a.get("ocr_pendiente", []), "error": a.get("error")} for a in e["anexos"]]}
                                for e in eds],
                  "sin_edicion": i["sin_edicion"], "consultas": i["consultas"], "errores": i.get("errores", [])}
    nums = []
    for e in eds:
        try:
            n, y = e["numero"].split("/"); nums.append((int(y), int(n)))
        except Exception:  # noqa
            faltantes.append(f"sin número de publicación: {e['fecha']} {e['edicion']}")
    nums.sort()
    huecos = [f"{a[1]+1}..{b[1]-1}/{a[0]}" for a, b in zip(nums, nums[1:]) if a[0] == b[0] and b[1] - a[1] != 1]
    man["dof"]["numeros"] = [f"{n}/{y}" for y, n in nums]
    man["dof"]["numeros_consecutivos"] = (not huecos) if len(nums) > 1 else None
    man["dof"]["huecos"] = huecos
    if huecos:
        faltantes.append("números no consecutivos: " + ", ".join(huecos))
    if i.get("corte_anterior") and not any(e.get("ya_reportada") for e in eds):
        faltantes.append(f"sin edición de referencia del corte anterior ({i['corte_anterior']}): no se puede probar la continuidad")
    for e in eds:
        if e["ok_paginas"] is False:
            faltantes.append(f"páginas reales ≠ declaradas: {e['fecha']} {e['edicion']} ({e['paginas_reales']} vs {e['paginas_declaradas']})")
        if e["ok_paginas"] is None:
            faltantes.append(f"sin pie de páginas declaradas: {e['fecha']} {e['edicion']}")
        if e.get("ya_reportada"):
            continue
        pend = e.get("ocr_pendiente")
        if pend is None and e.get("paginas_ocr", e.get("paginas_sin_texto")):
            pend = e.get("paginas_ocr", e.get("paginas_sin_texto"))
        if pend:
            faltantes.append(f"OCR pendiente {e['fecha']} {e['edicion']}: {len(pend)} páginas")
        for a in e["anexos"]:
            if a.get("error"):
                faltantes.append(f"anexo no descargado: {a.get('url')} ({a['error']})")
            elif a.get("ocr_pendiente"):
                faltantes.append(f"OCR pendiente anexo {a['archivo']}: {len(a['ocr_pendiente'])} páginas")
    for err in i.get("errores", []):
        faltantes.append(f"error DOF {err.get('fecha')} {err.get('edicion', '')} {err.get('paso')}: {err.get('error')}")
ctl = os.path.join(dest, "sjf", "control.json")
if os.path.exists(ctl):
    c = json.load(open(ctl))
    man["sjf"] = {"fecha": c["fecha"], "estado": c.get("estado", "COMPLETO"), "hora_publicacion": c.get("hora_publicacion"), "resumen": c.get("resumen", {}),
                  "errores": c.get("errores", []), "anexos_ocr": c.get("anexos_ocr", {})}
    if c.get("estado") == "EN_CURSO":
        faltantes.append(f"SJF del {c['fecha']} incompleto: la última corrida no terminó (ver fuentes.log)")
    for err in c.get("errores", []):
        faltantes.append(f"error SJF {err.get('tipo')} {err.get('ius')} {err.get('paso')}: {err.get('error')}")
    for name, a in c.get("anexos_ocr", {}).items():
        if a.get("ocr_pendiente"):
            faltantes.append(f"OCR pendiente anexo SJF {name}: {len(a['ocr_pendiente'])} páginas")
    if c.get("estado") != "EN_CURSO" and not c.get("resumen", {}).get("tesis") and not c.get("resumen", {}).get("ejecutorias"):
        faltantes.append(f"SJF del {c['fecha']} sin tesis ni ejecutorias: confirmar si no hubo publicación")
man["compuerta_fuentes"] = {"listo": not faltantes, "faltantes": faltantes}
tmp = os.path.join(dest, "manifiesto.json.tmp")
json.dump(man, open(tmp, "w"), ensure_ascii=False, indent=1)
os.replace(tmp, os.path.join(dest, "manifiesto.json"))
print(json.dumps({k: v for k, v in man.items() if k not in ("archivos",)}, ensure_ascii=False)[:3000])
print("archivos:", len(files))
