#!/usr/bin/env python3
"""Manifiesto de una entrega: todo lo que hay en fuentes/<entrega>/ con tamaño y SHA-256,
más el resumen del inventario DOF y del control SJF. Es lo primero que lee la sesión."""
import glob, hashlib, json, os, sys, time

dest = sys.argv[1].rstrip("/")
files = []
for f in sorted(glob.glob(os.path.join(dest, "**", "*"), recursive=True)):
    if os.path.isfile(f) and not f.endswith("manifiesto.json"):
        h = hashlib.sha256(open(f, "rb").read()).hexdigest()
        files.append({"ruta": os.path.relpath(f, dest), "bytes": os.path.getsize(f), "sha256": h})
man = {"entrega": os.path.basename(dest), "generado": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "archivos": files}
inv = os.path.join(dest, "dof", "inventario.json")
if os.path.exists(inv):
    i = json.load(open(inv))
    man["dof"] = {"ediciones": [{"fecha": e["fecha"], "edicion": e["edicion"], "numero": e["numero"], "pdf": e["pdf"], "paginas": e["paginas_reales"],
                                  "ok_paginas": e["ok_paginas"], "notas": len(e["notas"]), "imagen": len(e["paginas_sin_texto"]), "ocr": e.get("ocr", []),
                                  "anexos": [{"archivo": a.get("archivo"), "paginas": a.get("paginas"), "ocr": a.get("ocr", []), "error": a.get("error")} for a in e["anexos"]]}
                                 for e in i["ediciones"]],
                  "sin_edicion": i["sin_edicion"], "consultas": i["consultas"]}
    nums = sorted(int(e["numero"].split("/")[0]) for e in i["ediciones"] if e["numero"])
    man["dof"]["numeros_consecutivos"] = all(b - a == 1 for a, b in zip(nums, nums[1:])) if len(nums) > 1 else None
ctl = os.path.join(dest, "sjf", "control.json")
if os.path.exists(ctl):
    c = json.load(open(ctl))
    man["sjf"] = {"fecha": c["fecha"], "hora_publicacion": c["hora_publicacion"], "resumen": c["resumen"]}
json.dump(man, open(os.path.join(dest, "manifiesto.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in man.items() if k != "archivos"}, ensure_ascii=False)[:1500])
print("archivos:", len(files))
