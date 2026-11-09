#!/usr/bin/env python3
"""Fuentes del DOF para la skill dof-castorena (corre en el box).

Uso: dof_fuentes.py DESTINO FECHA [FECHA ...]      (fechas AAAA-MM-DD)

Para cada fecha consulta el índice oficial (https://dof.gob.mx/index.php?year&month&day),
detecta todas las ediciones (matutina, vespertina, extraordinaria) por los enlaces
`edicion=` que el propio índice ofrece, lista las notas de cada edición con su título,
descarga el PDF completo por la ruta oficial (nota_to_pdf.php -> abrirPDF.php), lo
verifica (cabecera PDF, páginas declaradas vs. reales), extrae el texto con pdftotext,
marca las páginas sin texto (imagen) y localiza anexos publicados aparte
(enlaces a PDF dentro de dof.gob.mx/AAAA/...). Escribe DESTINO/inventario.json.

Solo biblioteca estándar + pdftotext/pdfinfo (poppler-utils). No adivina URLs.
"""
import hashlib, html, json, os, re, subprocess, sys, time, urllib.request, urllib.parse

BASE = "https://dof.gob.mx"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0 Safari/537.36"
LABEL2CODE = {"Matutina": "MAT", "Vespertina": "VES", "Extraordinaria": "EXT"}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def get(url, binary=False, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-MX,es;q=0.9"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                return data if binary else data.decode("utf-8", "replace")
        except Exception as e:  # noqa
            last = e
            time.sleep(3 * (i + 1))
    raise RuntimeError(f"GET {url}: {last}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean(t):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()


def parse_index(page):
    """Devuelve (label_edicion_actual, codigos_de_otras_ediciones, notas, sin_datos)."""
    sin_datos = "No hay datos para la fecha seleccionada" in page
    m = re.search(r"Fecha:\s*(\d\d/\d\d/\d{4})\s*-\s*Edici(?:&oacute;|ó)n\s+([A-Za-z]+)", page)
    label = m.group(2) if m else None
    otras = sorted(set(re.findall(r"index\.php\?year=\d+&(?:amp;)?month=\d+&(?:amp;)?day=\d+&(?:amp;)?edicion=([A-Z]+)", page)))
    notas = []
    for mm in re.finditer(r'<a href="/nota_detalle\.php\?codigo=(\d+)&amp;fecha=([\d/]+)"\s+class="enlaces">(.*?)</a>', page, re.S):
        notas.append({"codigo": mm.group(1), "fecha": mm.group(2), "titulo": clean(mm.group(3)),
                      "url": f"{BASE}/nota_detalle.php?codigo={mm.group(1)}&fecha={mm.group(2)}"})
    # Organismo emisor: el encabezado en negritas más cercano antes de cada nota.
    heads = [(h.start(), clean(h.group(1))) for h in re.finditer(r'<td[^>]*class="subtitle_azul"[^>]*>(.*?)</td>', page, re.S)]
    if heads:
        for n in notas:
            pos = page.find(f'codigo={n["codigo"]}&amp;')
            prev = [t for p, t in heads if p < pos]
            n["organismo"] = prev[-1] if prev else None
    return label, otras, notas, sin_datos


def pdf_url(fecha_ddmmaaaa, code):
    """Ruta oficial: nota_to_pdf.php devuelve un script con la redirección a abrirPDF.php."""
    page = get(f"{BASE}/nota_to_pdf.php?fecha={fecha_ddmmaaaa}&edicion={code}")
    m = re.search(r"self\.location=\('([^']+)'\)", page)
    if not m:
        raise RuntimeError(f"nota_to_pdf sin redirección para {fecha_ddmmaaaa} {code}")
    return urllib.parse.urljoin(BASE + "/", html.unescape(m.group(1)))


def pdf_pages(path):
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def extract_text(pdf, txt):
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    pages = open(txt, encoding="utf-8", errors="replace").read().split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    low = [i + 1 for i, p in enumerate(pages) if len(re.sub(r"\s+", "", p)) < 80]
    return pages, low


def declared(pages_text):
    joined = "\n".join(pages_text)
    m = re.search(r"Esta edici[oó]n consta de\s+(\d+)\s+p[aá]ginas", joined)
    n = re.search(r"\b(\d{1,3})/(20\d\d)\b", pages_text[0]) if pages_text else None
    return (int(m.group(1)) if m else None), (n.group(0) if n else None)


def annex_links(pages_text):
    """Anexos publicados aparte: enlaces a PDF dentro de dof.gob.mx mencionados en el texto."""
    joined = "\n".join(pages_text)
    links = set()
    for m in re.finditer(r"(?:https?://)?(?:www\.)?dof\.gob\.mx/(20\d\d/[^\s\)\]]+?\.pdf)", joined, re.I):
        links.add(f"{BASE}/{m.group(1)}")  # sin www: el certificado del www no coincide
    return sorted(links)


def fetch_annex(url, destdir):
    name = os.path.basename(urllib.parse.urlparse(url).path)
    path = os.path.join(destdir, name)
    if not os.path.exists(path):
        data = get(url, binary=True)
        if not data.startswith(b"%PDF"):
            return {"url": url, "error": "no es PDF", "bytes": len(data)}
        open(path, "wb").write(data)
    txt = path[:-4] + ".txt"
    pages, low = extract_text(path, txt)
    return {"url": url, "archivo": name, "sha256": sha256(path), "paginas": pdf_pages(path),
            "paginas_sin_texto": low, "necesita_ocr": len(low) > max(1, len(pages) // 2)}


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    dest = sys.argv[1]
    fechas = sys.argv[2:]
    os.makedirs(os.path.join(dest, "raw"), exist_ok=True)
    os.makedirs(os.path.join(dest, "anexos"), exist_ok=True)
    inv_path = os.path.join(dest, "inventario.json")
    inv = json.load(open(inv_path)) if os.path.exists(inv_path) else {"ediciones": [], "sin_edicion": [], "consultas": []}
    done = {(e["fecha"], e["edicion"]) for e in inv["ediciones"]}
    for f in fechas:
        y, m, d = f.split("-")
        ddmmaaaa = f"{d}/{m}/{y}"
        url0 = f"{BASE}/index.php?year={int(y)}&month={int(m)}&day={int(d)}"
        page = get(url0)
        label, otras, notas, sin = parse_index(page)
        inv["consultas"].append({"fecha": f, "hora": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "url": url0,
                                 "edicion_mostrada": label, "otras": otras, "sin_datos": sin})
        if sin and not notas:
            log(f, "sin edición"); inv["sin_edicion"].append(f)
            if f in inv["sin_edicion"]: inv["sin_edicion"] = sorted(set(inv["sin_edicion"]))
            continue
        ediciones = {}
        if label:
            ediciones[LABEL2CODE.get(label, label.upper()[:3])] = (label, notas)
        for code in otras:
            if code in ediciones:
                continue
            p2 = get(url0 + f"&edicion={code}")
            l2, _, n2, s2 = parse_index(p2)
            if s2 or not n2:
                log(f, code, "sin datos (enlace de navegación vacío)"); continue
            ediciones[code] = (l2 or code, n2)
        for code, (lab, ns) in sorted(ediciones.items()):
            if (f, code) in done:
                log(f, code, "ya inventariada"); continue
            log(f, code, lab, len(ns), "notas")
            url = pdf_url(ddmmaaaa, code)
            name = os.path.basename(urllib.parse.urlparse(url).query.split("archivo=")[1].split("&")[0])
            pdf = os.path.join(dest, "raw", name)
            if not os.path.exists(pdf):
                data = get(url, binary=True)
                if not data.startswith(b"%PDF"):
                    raise RuntimeError(f"{url}: no devolvió PDF ({len(data)} bytes)")
                open(pdf, "wb").write(data)
            txt = pdf[:-4] + ".txt"
            pages, low = extract_text(pdf, txt)
            real = pdf_pages(pdf)
            decl, num = declared(pages)
            anexos = [fetch_annex(u, os.path.join(dest, "anexos")) for u in annex_links(pages)]
            e = {"fecha": f, "edicion": code, "etiqueta": lab, "numero": num, "pdf": name, "pdf_url": url,
                 "sha256": sha256(pdf), "paginas_reales": real, "paginas_declaradas": decl,
                 "paginas_sin_texto": low, "notas": ns, "anexos": anexos,
                 "ok_paginas": (decl == real) if decl else None}
            inv["ediciones"].append(e)
            log(f, code, f"pág. reales {real} declaradas {decl} núm. {num} imagen {len(low)} anexos {len(anexos)}")
    inv["ediciones"].sort(key=lambda e: (e["fecha"], e["edicion"]))
    json.dump(inv, open(inv_path, "w"), ensure_ascii=False, indent=1)
    # Resumen
    nums = [e["numero"] for e in inv["ediciones"] if e["numero"]]
    print(json.dumps({"ediciones": [(e["fecha"], e["edicion"], e["numero"], e["paginas_reales"], e["ok_paginas"]) for e in inv["ediciones"]],
                      "sin_edicion": inv["sin_edicion"], "numeros": nums}, ensure_ascii=False))


if __name__ == "__main__":
    main()
