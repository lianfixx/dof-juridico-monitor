#!/usr/bin/env python3
"""Fuentes del DOF para la skill dof-castorena (corre en el box).

Uso: dof_fuentes.py DESTINO [--corte AAAA-MM-DD] FECHA [FECHA ...]   (fechas AAAA-MM-DD)

Para cada fecha consulta el índice oficial (https://dof.gob.mx/index.php?year&month&day),
detecta todas las ediciones (matutina, vespertina, extraordinaria) por los enlaces
`edicion=` que el propio índice ofrece, lista las notas de cada edición con su título,
descarga el PDF completo por la ruta oficial (nota_to_pdf.php -> abrirPDF.php), lo
verifica (cabecera PDF, páginas declaradas vs. reales), extrae el texto con pdftotext,
marca las páginas que requieren OCR y localiza anexos publicados aparte
(enlaces a PDF dentro de dof.gob.mx/AAAA/...). Escribe DESTINO/inventario.json.

Páginas que requieren OCR (`paginas_ocr`): las que casi no tienen texto
(`paginas_sin_texto`) y las que llevan una imagen grande (`paginas_con_imagen`), porque
un formato o una tabla escaneada puede ir en imagen debajo de un párrafo con texto.

--corte FECHA: día del cierre anterior. En esa fecha, lo que ya cubrió el cierre anterior
se descarga solo para comprobar la continuidad de números y se marca `ya_reportada`
(no se lee ni se reporta otra vez): lo que esté en el inventario de una entrega anterior
del box y, si esa entrega no está en el box, la matutina de ese día. Las vespertinas y
extraordinarias de ese día que no estén en una entrega anterior son nuevas.

Ediciones no entregadas: fuentes/no_entregadas.json (lista de {fecha, edicion, numero,
nota_correo, decidido}) registra lo que ya se había dado por reportado pero no llegó al
Licenciado. Esas ediciones nunca se marcan `ya_reportada`: su fecha entra al periodo de la
entrega y quedan con `no_entregada_antes` para leerse e incorporarse al reporte. Si una
corrida anterior ya las había marcado `ya_reportada`, se vuelven a procesar.

Un fallo en una fecha o edición no detiene las demás: queda en `errores` del inventario
y el script termina con código 1. El inventario se guarda tras cada edición.
Solo biblioteca estándar + poppler-utils (pdftotext, pdfinfo, pdfimages). No adivina URLs.
"""
import glob, hashlib, html, json, os, re, subprocess, sys, time, urllib.request, urllib.parse

BASE = "https://dof.gob.mx"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0 Safari/537.36"
LABEL2CODE = {"Matutina": "MAT", "Vespertina": "VES", "Extraordinaria": "EXT"}
# Imagen «grande»: ancho y alto mínimos en píxeles. Deja fuera viñetas e iconos (12x12, 33x30).
IMG_MIN_W, IMG_MIN_H = 300, 100


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


# Esperas entre intentos cuando el portal responde algo inesperado (página de error o de
# saturación en lugar de la redirección o del PDF). Comprobado el 9/11/2026: la ruta del
# 05/11/2026 falló una vez y respondió bien minutos después.
ESPERAS = (10, 30, 60, 120)


def pdf_url(fecha_ddmmaaaa, code):
    """Ruta oficial: nota_to_pdf.php devuelve un script con la redirección a abrirPDF.php."""
    for i, espera in enumerate((0,) + ESPERAS):
        if espera:
            log(f"nota_to_pdf {fecha_ddmmaaaa} {code}: sin redirección, reintento {i} en {espera} s")
            time.sleep(espera)
        page = get(f"{BASE}/nota_to_pdf.php?fecha={fecha_ddmmaaaa}&edicion={code}")
        m = re.search(r"self\.location=\('([^']+)'\)", page)
        if m:
            return urllib.parse.urljoin(BASE + "/", html.unescape(m.group(1)))
    raise RuntimeError(f"nota_to_pdf sin redirección para {fecha_ddmmaaaa} {code} tras {len(ESPERAS) + 1} intentos")


def get_pdf(url):
    """Descarga un PDF; si el portal devuelve otra cosa, reintenta con espera."""
    data = b""
    for i, espera in enumerate((0,) + ESPERAS):
        if espera:
            log(f"{url}: no devolvió PDF ({len(data)} bytes), reintento {i} en {espera} s")
            time.sleep(espera)
        data = get(url, binary=True)
        if data.startswith(b"%PDF"):
            return data
    raise RuntimeError(f"{url}: no devolvió PDF ({len(data)} bytes) tras {len(ESPERAS) + 1} intentos")


def pdf_pages(path):
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def image_pages(path):
    """Páginas con al menos una imagen grande (pdfimages -list)."""
    out = subprocess.run(["pdfimages", "-list", path], capture_output=True, text=True).stdout.splitlines()[2:]
    pages = set()
    for line in out:
        f = line.split()
        try:
            if int(f[3]) >= IMG_MIN_W and int(f[4]) >= IMG_MIN_H:
                pages.add(int(f[0]))
        except (IndexError, ValueError):
            continue
    return sorted(pages)


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
    first = pages_text[0] if pages_text else ""
    # Preferir «No. de publicación: N/AAAA»; si no aparece, el primer N/AAAA de la portada.
    n = re.search(r"publicaci[oó]n:?\s*(\d{1,4}/20\d\d)", first, re.I)
    num = n.group(1) if n else None
    if not num:
        n = re.search(r"(?<![\d/])(\d{1,3})/(20\d\d)\b", first)
        num = n.group(0) if n else None
    return (int(m.group(1)) if m else None), num


def annex_links(pages_text):
    """Anexos publicados aparte: enlaces a PDF dentro de dof.gob.mx mencionados en el texto.
    Admite enlaces partidos en dos renglones por el formato del PDF."""
    joined = "\n".join(pages_text)
    links = set()
    for m in re.finditer(r"(?:https?://)?(?:www\.)?dof\.gob\.mx/(20\d\d/(?:[^\s\)\]]|\n[ \t]*){1,300}?\.pdf)", joined, re.I):
        rel = re.sub(r"\s+", "", m.group(1))
        links.add(f"{BASE}/{rel}")  # sin www: el certificado del www no coincide
    return sorted(links)


def fetch_annex(url, destdir):
    name = os.path.basename(urllib.parse.urlparse(url).path)
    path = os.path.join(destdir, name)
    try:
        if not os.path.exists(path):
            open(path, "wb").write(get_pdf(url))
        txt = path[:-4] + ".txt"
        pages, low = extract_text(path, txt)
        imgs = image_pages(path)
        return {"url": url, "archivo": name, "sha256": sha256(path), "paginas": pdf_pages(path),
                "paginas_sin_texto": low, "paginas_con_imagen": imgs,
                "paginas_ocr": sorted(set(low) | set(imgs)),
                "necesita_ocr": len(low) > max(1, len(pages) // 2)}
    except Exception as e:  # noqa
        return {"url": url, "error": str(e)[:300]}


def entregas_anteriores(dest):
    """Inventarios de entregas anteriores del box: fuentes/AAAA-MM-DD/dof/inventario.json
    con fecha menor que la entrega actual (DESTINO = fuentes/<entrega>/dof)."""
    ent_dir = os.path.dirname(os.path.abspath(dest))
    actual = os.path.basename(ent_dir)
    raiz = os.path.dirname(ent_dir)
    vistos = {}
    for inv in sorted(glob.glob(os.path.join(raiz, "*", "dof", "inventario.json"))):
        ent = os.path.basename(os.path.dirname(os.path.dirname(inv)))
        if not re.fullmatch(r"\d{4}-\d\d-\d\d", ent) or not re.fullmatch(r"\d{4}-\d\d-\d\d", actual) or ent >= actual:
            continue
        try:
            for e in json.load(open(inv)).get("ediciones", []):
                if not e.get("ya_reportada"):
                    vistos[(e["fecha"], e["edicion"])] = {"entrega": ent, "numero": e.get("numero")}
        except Exception:  # noqa
            continue
    return vistos


def no_entregadas(dest):
    """fuentes/no_entregadas.json → {(fecha, edicion): registro}. Decisión de Emi, no del script."""
    ent_dir = os.path.dirname(os.path.abspath(dest))
    ruta = os.path.join(os.path.dirname(ent_dir), "no_entregadas.json")
    if not os.path.exists(ruta):
        return {}
    actual = os.path.basename(ent_dir)
    ya_en = entregas_anteriores(dest)  # una entrega anterior del box ya la tiene como nueva → ya se reportó ahí
    out = {}
    for r in json.load(open(ruta)):
        if (r["fecha"], r["edicion"]) in ya_en:
            continue
        # Solo para entregas posteriores a la fecha de la edición y que no la hayan reportado ya.
        if r.get("reportada_en") and r["reportada_en"] != actual:
            continue
        if re.fullmatch(r"\d{4}-\d\d-\d\d", actual) and r["fecha"] < actual:
            out[(r["fecha"], r["edicion"])] = r
    return out


def save(inv, inv_path):
    inv["ediciones"].sort(key=lambda e: (e["fecha"], e["edicion"]))
    tmp = inv_path + ".tmp"
    json.dump(inv, open(tmp, "w"), ensure_ascii=False, indent=1)
    os.replace(tmp, inv_path)


def main():
    args = sys.argv[1:]
    corte = None
    if "--corte" in args:
        i = args.index("--corte"); corte = args[i + 1]; del args[i:i + 2]
    if len(args) < 2:
        print(__doc__); sys.exit(2)
    dest, fechas = args[0], args[1:]
    for f in fechas + ([corte] if corte else []):
        if not re.fullmatch(r"\d{4}-\d\d-\d\d", f):
            print(f"fecha inválida: {f}", file=sys.stderr); sys.exit(2)
    if corte and corte not in fechas:
        fechas = [corte] + fechas
    pendientes = no_entregadas(dest)
    periodo = set(fechas)
    fechas = sorted(dict.fromkeys(fechas + [k[0] for k in pendientes]))
    os.makedirs(os.path.join(dest, "raw"), exist_ok=True)
    os.makedirs(os.path.join(dest, "anexos"), exist_ok=True)
    inv_path = os.path.join(dest, "inventario.json")
    inv = json.load(open(inv_path)) if os.path.exists(inv_path) else {}
    for k, v in (("ediciones", []), ("sin_edicion", []), ("consultas", []), ("errores", [])):
        inv.setdefault(k, v)
    if corte:
        inv["corte_anterior"] = corte
    previas = entregas_anteriores(dest) if corte else {}
    # Una edición que quedó `ya_reportada` en una corrida anterior pero que Emi registró como no
    # entregada se vuelve a procesar como nueva (el PDF ya está en disco: solo rehace OCR y anexos).
    inv["ediciones"] = [e for e in inv["ediciones"]
                        if not (e.get("ya_reportada") and (e["fecha"], e["edicion"]) in pendientes)]
    done = {(e["fecha"], e["edicion"]) for e in inv["ediciones"]}
    errores_run = []
    for f in fechas:
        y, m, d = f.split("-")
        ddmmaaaa = f"{d}/{m}/{y}"
        url0 = f"{BASE}/index.php?year={int(y)}&month={int(m)}&day={int(d)}"
        try:
            page = get(url0)
            label, otras, notas, sin = parse_index(page)
        except Exception as e:  # noqa
            errores_run.append({"fecha": f, "paso": "indice", "error": str(e)[:300], "hora": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
            log(f, "ERROR índice:", e); continue
        inv["consultas"].append({"fecha": f, "hora": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "url": url0,
                                 "edicion_mostrada": label, "otras": otras, "sin_datos": sin})
        if sin and not notas:
            log(f, "sin edición")
            inv["sin_edicion"] = sorted(set(inv["sin_edicion"]) | {f})
            continue
        inv["sin_edicion"] = [x for x in inv["sin_edicion"] if x != f]  # ya hay edición (reintento)
        ediciones = {}
        if label:
            ediciones[LABEL2CODE.get(label, label.upper()[:3])] = (label, notas)
        for code in otras:
            if code in ediciones:
                continue
            try:
                p2 = get(url0 + f"&edicion={code}")
            except Exception as e:  # noqa
                errores_run.append({"fecha": f, "edicion": code, "paso": "indice", "error": str(e)[:300]})
                log(f, code, "ERROR índice:", e); continue
            l2, _, n2, s2 = parse_index(p2)
            if s2 or not n2:
                log(f, code, "sin datos (enlace de navegación vacío)"); continue
            ediciones[code] = (l2 or code, n2)
        for code, (lab, ns) in sorted(ediciones.items()):
            if (f, code) in done:
                log(f, code, "ya inventariada"); continue
            ya = None
            pend = pendientes.get((f, code))
            if pend:
                pass  # no entregada antes: se lee y se reporta
            elif f not in periodo:
                ya = "fecha fuera del periodo, incluida solo por una edición no entregada"
            elif corte and f == corte:
                if (f, code) in previas:
                    ya = f"en la entrega {previas[(f, code)]['entrega']}"
                elif code == "MAT" and not any(k[0] == f for k in previas):
                    ya = "matutina del día del corte: la cubre el cierre anterior (entrega fuera del box)"
            log(f, code, lab, len(ns), "notas", f"(ya reportada: {ya})" if ya else "")
            try:
                url = pdf_url(ddmmaaaa, code)
                name = os.path.basename(urllib.parse.urlparse(url).query.split("archivo=")[1].split("&")[0])
                pdf = os.path.join(dest, "raw", name)
                if not os.path.exists(pdf):
                    open(pdf, "wb").write(get_pdf(url))
                txt = pdf[:-4] + ".txt"
                pages, low = extract_text(pdf, txt)
                real = pdf_pages(pdf)
                decl, num = declared(pages)
                imgs = image_pages(pdf)
                anexos = [] if ya else [fetch_annex(u, os.path.join(dest, "anexos")) for u in annex_links(pages)]
            except Exception as e:  # noqa
                errores_run.append({"fecha": f, "edicion": code, "paso": "pdf", "error": str(e)[:300],
                                    "hora": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
                log(f, code, "ERROR PDF:", e); continue
            e = {"fecha": f, "edicion": code, "etiqueta": lab, "numero": num, "pdf": name, "pdf_url": url,
                 "sha256": sha256(pdf), "paginas_reales": real, "paginas_declaradas": decl,
                 "paginas_sin_texto": low, "paginas_con_imagen": imgs,
                 "paginas_ocr": [] if ya else sorted(set(low) | set(imgs)),
                 "notas": ns, "anexos": anexos,
                 "ok_paginas": (decl == real) if decl else None}
            if ya:
                e["ya_reportada"] = True; e["ya_reportada_motivo"] = ya
            if pend:
                e["no_entregada_antes"] = {k: pend.get(k) for k in ("numero", "nota_correo", "decidido")}
                if pend.get("numero") and num and pend["numero"] != num:
                    errores_run.append({"fecha": f, "edicion": code, "paso": "no_entregadas",
                                        "error": f"no_entregadas.json dice {pend['numero']} y el PDF dice {num}"})
            for a in anexos:
                if a.get("error"):
                    errores_run.append({"fecha": f, "edicion": code, "paso": "anexo", "url": a["url"], "error": a["error"]})
            inv["ediciones"].append(e); done.add((f, code))
            save(inv, inv_path)
            log(f, code, f"pág. reales {real} declaradas {decl} núm. {num} sin texto {len(low)} con imagen {len(imgs)} anexos {len(anexos)}")
    inv["errores"] = errores_run  # errores de esta corrida (las anteriores quedan en el log)
    save(inv, inv_path)
    nums = [e["numero"] for e in inv["ediciones"] if e["numero"]]
    print(json.dumps({"ediciones": [(e["fecha"], e["edicion"], e["numero"], e["paginas_reales"], e["ok_paginas"],
                                     "ya_reportada" if e.get("ya_reportada") else "nueva") for e in inv["ediciones"]],
                      "sin_edicion": inv["sin_edicion"], "numeros": nums, "errores": errores_run}, ensure_ascii=False))
    sys.exit(1 if errores_run else 0)


if __name__ == "__main__":
    main()
