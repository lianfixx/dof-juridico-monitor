"""Pruebas de los scripts del box (scripts/box/) y de las tareas programadas (prompts/tareas/).

No tocan la red ni el box: prueban la lógica que decide qué se lee, qué se marca como ya
reportado y cuándo la compuerta de fuentes puede declararse lista. Cubren los fallos
encontrados en la auditoría del 9/11/2026."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "scripts" / "box"


def load_dof_fuentes():
    spec = importlib.util.spec_from_file_location("dof_fuentes", BOX / "dof_fuentes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_numero_de_publicacion_prefiere_la_etiqueta_oficial():
    m = load_dof_fuentes()
    portada = "DIARIO OFICIAL DE LA FEDERACION 06/11/2026\nNo. de publicación: 304/2026\nCiudad de México, viernes 6 de noviembre de 2026"
    decl, num = m.declared([portada, "Esta edición consta de 358 páginas"])
    assert num == "304/2026"
    assert decl == 358


def test_numero_no_confunde_la_fecha_de_la_portada():
    m = load_dof_fuentes()
    # Sin etiqueta, el respaldo no debe tomar «11/2026» de la fecha 06/11/2026.
    _, num = m.declared(["DOF: 06/11/2026 edición 304/2026"])
    assert num == "304/2026"


def test_anexos_aparte_admite_enlace_partido_y_quita_www():
    m = load_dof_fuentes()
    texto = ["Consultable en www.dof.gob.mx/2026/SHCP/Anexo_largo_\n   de_la_resolucion.pdf y en https://dof.gob.mx/2026/SE/otro.pdf)"]
    links = m.annex_links(texto)
    assert "https://dof.gob.mx/2026/SHCP/Anexo_largo_de_la_resolucion.pdf" in links
    assert "https://dof.gob.mx/2026/SE/otro.pdf" in links
    assert all("www." not in u for u in links)


def test_entregas_anteriores_solo_toma_entregas_reales_previas(tmp_path):
    m = load_dof_fuentes()
    fuentes = tmp_path / "fuentes"
    def inv(nombre, eds):
        d = fuentes / nombre / "dof"; d.mkdir(parents=True)
        (d / "inventario.json").write_text(json.dumps({"ediciones": eds}), encoding="utf-8")
    inv("2026-11-05", [{"fecha": "2026-11-05", "edicion": "MAT", "numero": "303/2026"},
                       {"fecha": "2026-11-03", "edicion": "MAT", "numero": "300/2026", "ya_reportada": True}])
    inv("prueba-2026-11-06", [{"fecha": "2026-11-06", "edicion": "MAT", "numero": "304/2026"}])
    inv("2026-11-12", [{"fecha": "2026-11-12", "edicion": "MAT", "numero": "310/2026"}])
    previas = m.entregas_anteriores(str(fuentes / "2026-11-10" / "dof"))
    assert ("2026-11-05", "MAT") in previas            # entrega anterior real
    assert ("2026-11-03", "MAT") not in previas        # ya_reportada allá: no cuenta como reportada ahí
    assert ("2026-11-06", "MAT") not in previas        # carpeta de prueba
    assert ("2026-11-12", "MAT") not in previas        # entrega posterior


def test_paginas_con_imagen_grande(tmp_path, monkeypatch):
    m = load_dof_fuentes()
    salida = (
        "page   num  type   width height color comp bpc  enc interp  object ID x-ppi y-ppi size ratio\n"
        "--------------------------------------------------------------------------------------------\n"
        "   1     0 image    2275  1866  rgb     3   8  jpeg   no        12  0   400   400  200K 1.6%\n"
        "  10     1 image    1693   542  rgb     3   8  jpeg   no        30  0   282   282  100K 3.0%\n"
        " 130     2 image      12    12  rgb     3   8  image  no        90  0    99    99   10B 2.0%\n"
    )
    class R:  # noqa
        stdout = salida
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: R())
    assert m.image_pages("x.pdf") == [1, 10]  # la viñeta de 12x12 no cuenta


def _manifiesto(tmp_path, inventario=None, control=None):
    ent = tmp_path / "2026-11-10"
    if inventario is not None:
        (ent / "dof").mkdir(parents=True)
        (ent / "dof" / "inventario.json").write_text(json.dumps(inventario), encoding="utf-8")
    if control is not None:
        (ent / "sjf").mkdir(parents=True, exist_ok=True)
        (ent / "sjf" / "control.json").write_text(json.dumps(control), encoding="utf-8")
    subprocess.run([sys.executable, str(BOX / "manifiesto.py"), str(ent)], check=True, capture_output=True)
    return json.loads((ent / "manifiesto.json").read_text(encoding="utf-8"))


def _ed(fecha, edicion, numero, **kw):
    e = {"fecha": fecha, "edicion": edicion, "numero": numero, "pdf": f"{fecha}-{edicion}.pdf",
         "paginas_reales": 10, "paginas_declaradas": 10, "ok_paginas": True, "notas": [],
         "paginas_sin_texto": [], "paginas_ocr": [], "anexos": []}
    e.update(kw)
    return e


def test_compuerta_lista_con_continuidad_desde_lo_ya_reportado(tmp_path):
    inv = {"corte_anterior": "2026-11-05", "sin_edicion": [], "consultas": [], "errores": [],
           "ediciones": [_ed("2026-11-05", "MAT", "303/2026", ya_reportada=True),
                         _ed("2026-11-06", "MAT", "304/2026", paginas_ocr=[10], ocr=[10], ocr_pendiente=[]),
                         _ed("2026-11-09", "MAT", "305/2026")]}
    man = _manifiesto(tmp_path, inv)
    assert man["compuerta_fuentes"] == {"listo": True, "faltantes": []}


def test_compuerta_detecta_hueco_ocr_pendiente_y_error(tmp_path):
    inv = {"corte_anterior": "2026-11-05", "sin_edicion": [], "consultas": [],
           "errores": [{"fecha": "2026-11-09", "edicion": "VES", "paso": "pdf", "error": "sin redirección"}],
           "ediciones": [_ed("2026-11-05", "MAT", "303/2026", ya_reportada=True),
                         _ed("2026-11-06", "MAT", "305/2026", paginas_ocr=[10, 11], ocr=[10], ocr_pendiente=[11])]}
    man = _manifiesto(tmp_path, inv)
    f = " | ".join(man["compuerta_fuentes"]["faltantes"])
    assert man["compuerta_fuentes"]["listo"] is False
    assert "304..304/2026" in f and "OCR pendiente" in f and "sin redirección" in f


def test_compuerta_exige_referencia_del_corte(tmp_path):
    inv = {"corte_anterior": "2026-11-05", "sin_edicion": [], "consultas": [], "errores": [],
           "ediciones": [_ed("2026-11-06", "MAT", "304/2026")]}
    man = _manifiesto(tmp_path, inv)
    assert any("corte anterior" in x for x in man["compuerta_fuentes"]["faltantes"])


def test_compuerta_no_acepta_sjf_interrumpido(tmp_path):
    man = _manifiesto(tmp_path, control={"fecha": "2026-11-06", "estado": "EN_CURSO", "resumen": {}, "hora_publicacion": None})
    assert man["compuerta_fuentes"]["listo"] is False
    assert any("incompleto" in x for x in man["compuerta_fuentes"]["faltantes"])


def test_scripts_del_box_y_arranque_coinciden():
    arranque = (BOX / "arranque.sh").read_text(encoding="utf-8")
    for s in ["fuentes.sh", "lanzar.sh", "estado.sh", "dof_fuentes.py", "paginas.py", "ocr.py", "manifiesto.py", "sjf_fuentes.mjs"]:
        assert (BOX / s).exists(), s
        assert s in arranque, f"arranque.sh no comprueba {s}"


def test_periodos_desde_el_corte_anterior():
    f = (BOX / "fuentes.sh").read_text(encoding="utf-8")
    assert 'martes)  CORTE="$(d \'-5 days\')"' in f   # jueves anterior
    assert 'jueves)  CORTE="$(d \'-2 days\')"' in f   # martes
    assert "--corte" in f


def test_tareas_programadas_usan_lanzador_y_reglas():
    tareas = ROOT / "prompts" / "tareas"
    textos = {p.name: p.read_text(encoding="utf-8") for p in tareas.glob("*.md")}
    assert set(textos) == {"cierre-martes.md", "cierre-jueves.md", "lector-nocturno.md", "sjf-viernes.md"}
    for nombre, t in textos.items():
        assert "bin/lanzar.sh" in t and "bin/estado.sh" in t, nombre
        assert "600 s" in t, nombre
        assert "Nunca escribas al Licenciado" in t, nombre
        assert "fuentes.sh dof" not in t, nombre  # las tardías ya entran por el corte
    for nombre in ("cierre-martes.md", "cierre-jueves.md"):
        t = textos[nombre]
        assert "emilianogarciamilla@gmail.com, sin CC/CCO" in t
        assert "sha256:<hash" in t
        assert "compuerta_fuentes" in t
    assert "Sin sección, hallazgo ni corrección SJF" in textos["cierre-jueves.md"]
    for nombre in ("lector-nocturno.md", "sjf-viernes.md"):
        assert "no envía correos" in textos[nombre]
