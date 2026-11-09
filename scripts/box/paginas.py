#!/usr/bin/env python3
"""Índice de páginas para que los lectores lean del box por tramos exactos.

Uso: paginas.py DESTINO_DOF
Para cada .txt de raw/ y anexos/ escribe <archivo>.paginas.json: por página, la primera
y la última línea (1-based) del .txt, el número de caracteres sin espacios y si es imagen.
Así un lector pide con read_file(path, offset=linea_ini, limit=linea_fin-linea_ini+1)
exactamente su rango de páginas. Las páginas se separan por el salto de página (\\f)
que pdftotext escribe al final de cada una.
"""
import glob, json, os, re, sys

dest = sys.argv[1]
for txt in sorted(glob.glob(os.path.join(dest, "raw", "*.txt")) + glob.glob(os.path.join(dest, "anexos", "*.txt"))):
    if txt.endswith(".ocr.txt"):
        continue
    text = open(txt, encoding="utf-8", errors="replace").read()
    total_lines = text.count("\n") + 1
    pages = text.split("\f")
    if pages and pages[-1] == "":
        pages = pages[:-1]  # el último \f cierra la última página real
    idx, line = [], 1
    for n, pg in enumerate(pages, 1):
        nl = pg.count("\n")
        chars = len(re.sub(r"\s+", "", pg))
        idx.append({"pagina": n, "linea_ini": line, "linea_fin": line + nl, "chars": chars, "imagen": chars < 80})
        line += nl
    json.dump({"archivo": os.path.basename(txt), "paginas": len(idx), "lineas": total_lines, "indice": idx},
              open(txt[:-4] + ".paginas.json", "w"), ensure_ascii=False)
    print(os.path.basename(txt), "páginas", len(idx), "líneas", total_lines, "imagen", sum(p["imagen"] for p in idx))
