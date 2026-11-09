#!/usr/bin/env python3
"""Auditoría literal: cada dato del reporte y la guía debe aparecer, carácter por carácter
(ignorando espacios y mayúsculas), en el texto oficial de su fuente.

Uso: audit.py evidencias.json
evidencias.json: {"fuentes": {"F": ["ruta/30102026-MAT.txt", ...], "S": ["ruta/sjf/txt/*.txt"]},
                  "evidencias": [["F", "90% sobre el importe de la multa"], ["S", "P./J. 216/2026 (12a.)"], ...]}
Las rutas admiten comodines. Sale con código 1 si falta una sola evidencia.
"""
import glob, json, re, sys

def n(s): return re.sub(r"\s+", "", s).lower()
spec = json.load(open(sys.argv[1], encoding="utf-8"))
S = {}
for k, pats in spec["fuentes"].items():
    files = [f for pat in pats for f in sorted(glob.glob(pat))]
    S[k] = n(" ".join(open(f, encoding="utf-8", errors="replace").read() for f in files))
    print(f"fuente {k}: {len(files)} archivos, {len(S[k])} caracteres")
bad = [(k, x) for k, x in spec["evidencias"] if n(x) not in S.get(k, "")]
for k, x in bad: print("NO:", k, x)
print(f"Evidencias verificadas: {len(spec['evidencias']) - len(bad)}/{len(spec['evidencias'])}")
sys.exit(1 if bad else 0)
