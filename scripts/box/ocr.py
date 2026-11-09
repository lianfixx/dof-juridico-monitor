#!/usr/bin/env python3
"""OCR en español de las páginas que lo requieren (box).

Uso: ocr.py DESTINO [--dpi 200] [--hilos 2]
  DESTINO = fuentes/<entrega>/dof  (lee inventario.json)
         o fuentes/<entrega>/sjf   (lee control.json; anexos PDF del Semanario)

DOF: para cada edición nueva (no `ya_reportada`) pasa por Tesseract 'spa' las páginas de
`paginas_ocr` (sin texto o con imagen grande; si el inventario es anterior a ese campo, las
de `paginas_sin_texto`). En los anexos aparte, todas las páginas si `necesita_ocr`; si no,
las de `paginas_ocr`.
SJF: en cada anexo PDF, las páginas sin texto o con imagen grande.

Escribe <archivo>.ocr.txt con separadores "=== PAGINA n (OCR) ===" (reanudable: no repite
páginas ya reconocidas) y anota en el inventario o control qué páginas se reconocieron
(`ocr`) y cuáles faltan (`ocr_pendiente`). El texto OCR nunca sustituye al oficial: se
guarda aparte y se marca como OCR. Usa `--hilos` procesos de Tesseract en paralelo, cada
uno con un solo hilo (el box tiene 2 vCPU).
"""
import json, os, re, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor

dest = sys.argv[1].rstrip("/")
dpi = sys.argv[sys.argv.index("--dpi") + 1] if "--dpi" in sys.argv else "200"
hilos = int(sys.argv[sys.argv.index("--hilos") + 1]) if "--hilos" in sys.argv else 2
ENV = dict(os.environ, OMP_THREAD_LIMIT="1")
IMG_MIN_W, IMG_MIN_H = 300, 100


def one_page(pdf, n):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", dpi, "-f", str(n), "-l", str(n), "-png", pdf, f"{td}/p"], check=True)
        png = [f for f in os.listdir(td) if f.endswith(".png")][0]
        subprocess.run(["tesseract", f"{td}/{png}", f"{td}/o", "-l", "spa", "--psm", "4"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, env=ENV)
        return open(f"{td}/o.txt", encoding="utf-8", errors="replace").read()


def ocr_pages(pdf, pages, out):
    """Devuelve (reconocidas, pendientes)."""
    done = {}
    if os.path.exists(out):
        cur = open(out, encoding="utf-8").read()
        for blk in cur.split("=== PAGINA ")[1:]:
            n = int(blk.split(" ", 1)[0]); done[n] = blk
    todo = [n for n in pages if n not in done]
    fallos = []

    def run(n):
        t0 = time.time()
        try:
            txt = one_page(pdf, n)
        except Exception as e:  # noqa
            return n, None, str(e)[:200]
        print(time.strftime("%H:%M:%S"), os.path.basename(pdf), "p", n, f"{time.time()-t0:.0f}s", flush=True)
        return n, txt, None

    with ThreadPoolExecutor(max_workers=max(1, hilos)) as ex:
        for k, (n, txt, err) in enumerate(ex.map(run, todo), 1):
            if err:
                fallos.append(n); print("ERROR OCR", os.path.basename(pdf), "p", n, err, flush=True); continue
            done[n] = f"{n} (OCR) ===\n{txt}\n"
            if k % 5 == 0 or k == len(todo):  # guardar avance (reanudable)
                write(out, done)
    write(out, done)
    ok = sorted(n for n in pages if n in done)
    return ok, sorted(set(pages) - set(ok))


def write(out, done):
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for k in sorted(done):
            f.write("=== PAGINA " + done[k])
    os.replace(tmp, out)


def pages_needing_ocr(pdf, txt):
    """Para PDFs sin inventario previo (anexos del SJF): sin texto o con imagen grande."""
    if not os.path.exists(txt):
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=False)
    pages = open(txt, encoding="utf-8", errors="replace").read().split("\f") if os.path.exists(txt) else []
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    low = {i + 1 for i, p in enumerate(pages) if len(re.sub(r"\s+", "", p)) < 80}
    out = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    for line in out:
        f = line.split()
        try:
            if int(f[3]) >= IMG_MIN_W and int(f[4]) >= IMG_MIN_H:
                low.add(int(f[0]))
        except (IndexError, ValueError):
            continue
    return sorted(low)


pendiente_total = 0
if os.path.exists(os.path.join(dest, "inventario.json")):
    inv_path = os.path.join(dest, "inventario.json")
    inv = json.load(open(inv_path))
    for e in inv["ediciones"]:
        if e.get("ya_reportada"):
            continue
        pdf = os.path.join(dest, "raw", e["pdf"])
        pags = e.get("paginas_ocr", e.get("paginas_sin_texto", []))
        if pags:
            e["ocr"], e["ocr_pendiente"] = ocr_pages(pdf, pags, pdf[:-4] + ".ocr.txt")
            pendiente_total += len(e["ocr_pendiente"])
        for a in e["anexos"]:
            if not a.get("archivo"):
                continue
            apdf = os.path.join(dest, "anexos", a["archivo"])
            pags = list(range(1, (a.get("paginas") or 0) + 1)) if a.get("necesita_ocr") else a.get("paginas_ocr", [])
            if pags:
                a["ocr"], a["ocr_pendiente"] = ocr_pages(apdf, pags, apdf[:-4] + ".ocr.txt")
                pendiente_total += len(a["ocr_pendiente"])
        tmp = inv_path + ".tmp"; json.dump(inv, open(tmp, "w"), ensure_ascii=False, indent=1); os.replace(tmp, inv_path)
elif os.path.exists(os.path.join(dest, "control.json")):
    ctl_path = os.path.join(dest, "control.json")
    ctl = json.load(open(ctl_path))
    if ctl.get("estado") == "EN_CURSO":
        print("control del SJF EN_CURSO (corrida interrumpida): no hay anexos que reconocer"); sys.exit(1)
    ctl["anexos_ocr"] = ctl.get("anexos_ocr", {})
    for name in sorted(ctl.get("anexos", {})):
        apdf = os.path.join(dest, "pdf", name)
        if not os.path.exists(apdf):
            continue
        txt = os.path.join(dest, "txt", "ANX_" + re.sub(r"\.pdf$", "", name, flags=re.I) + ".txt")
        pags = pages_needing_ocr(apdf, txt)
        if not pags:
            continue
        out = txt[:-4] + ".ocr.txt"
        ok, pend = ocr_pages(apdf, pags, out)
        ctl["anexos_ocr"][name] = {"paginas_ocr": pags, "ocr": ok, "ocr_pendiente": pend, "archivo_ocr": os.path.basename(out)}
        pendiente_total += len(pend)
    tmp = ctl_path + ".tmp"; json.dump(ctl, open(tmp, "w"), ensure_ascii=False, indent=1); os.replace(tmp, ctl_path)
else:
    print("sin inventario.json ni control.json en", dest); sys.exit(2)
print("OCR terminado", "· pendientes:", pendiente_total)
sys.exit(1 if pendiente_total else 0)
