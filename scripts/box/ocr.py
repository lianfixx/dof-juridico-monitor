#!/usr/bin/env python3
"""OCR en español de las páginas sin texto del inventario (box).

Uso: ocr.py DESTINO [--dpi 200]
Lee DESTINO/inventario.json; para cada edición con páginas sin texto y cada anexo con
necesita_ocr, rasteriza esas páginas (pdftoppm) y las pasa por Tesseract 'spa'.
Escribe <archivo>.ocr.txt con separadores "=== PAGINA n (OCR) ===" y anota en el
inventario qué páginas se reconocieron. El texto OCR nunca sustituye al oficial: se
guarda aparte y se marca como OCR.
"""
import json, os, subprocess, sys, tempfile, time

dest = sys.argv[1]
dpi = "200"
if "--dpi" in sys.argv:
    dpi = sys.argv[sys.argv.index("--dpi") + 1]
inv_path = os.path.join(dest, "inventario.json")
inv = json.load(open(inv_path))


def ocr_pages(pdf, pages, out):
    done = {}
    if os.path.exists(out):
        cur = open(out, encoding="utf-8").read()
        for blk in cur.split("=== PAGINA ")[1:]:
            n = int(blk.split(" ", 1)[0]); done[n] = blk
    with tempfile.TemporaryDirectory() as td:
        for n in pages:
            if n in done:
                continue
            t0 = time.time()
            subprocess.run(["pdftoppm", "-r", dpi, "-f", str(n), "-l", str(n), "-png", pdf, f"{td}/p"], check=True)
            png = [f for f in os.listdir(td) if f.endswith(".png")][0]
            subprocess.run(["tesseract", f"{td}/{png}", f"{td}/o", "-l", "spa", "--psm", "4"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            txt = open(f"{td}/o.txt", encoding="utf-8", errors="replace").read()
            os.remove(f"{td}/{png}"); os.remove(f"{td}/o.txt")
            done[n] = f"{n} (OCR) ===\n{txt}\n"
            with open(out, "w", encoding="utf-8") as f:
                for k in sorted(done):
                    f.write("=== PAGINA " + done[k])
            print(time.strftime("%H:%M:%S"), os.path.basename(pdf), "p", n, f"{time.time()-t0:.0f}s", flush=True)
    return sorted(done)


for e in inv["ediciones"]:
    pdf = os.path.join(dest, "raw", e["pdf"])
    if e["paginas_sin_texto"]:
        e["ocr"] = ocr_pages(pdf, e["paginas_sin_texto"], pdf[:-4] + ".ocr.txt")
    for a in e["anexos"]:
        if a.get("archivo") and a.get("necesita_ocr"):
            apdf = os.path.join(dest, "anexos", a["archivo"])
            a["ocr"] = ocr_pages(apdf, list(range(1, a["paginas"] + 1)), apdf[:-4] + ".ocr.txt")
    json.dump(inv, open(inv_path, "w"), ensure_ascii=False, indent=1)
print("OCR terminado")
