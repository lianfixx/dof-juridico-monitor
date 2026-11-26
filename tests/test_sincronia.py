"""La vía de API y la de suscripción no se pueden separar: mismas reglas de redacción, mismo relevo, mismos scripts."""
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def texto(ruta):
    return (RAIZ / ruta).read_text(encoding="utf-8")


def lector():
    spec = importlib.util.spec_from_file_location("lector_api_s", RAIZ / "scripts/api/lector_api.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lector_api_s"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_el_redactor_por_api_carga_el_nucleo_de_redaccion():
    la = lector()
    nucleo = la.nucleo_redaccion()
    assert len(nucleo) > 800 and nucleo.startswith("1. ") and "9. " in nucleo
    assert nucleo in la.S_SINTESIS
    assert "comillas angulares" in nucleo and "dos puntos" in nucleo and "agradezco de antemano" in nucleo


def test_los_cierres_leen_y_aplican_la_misma_redaccion_y_el_mismo_relevo():
    for tarea in ("prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md"):
        t = texto(tarea)
        for pieza in ("references/redaccion.md", "references/api.md", "scripts/paquete/estilo.js", "scripts/api/relevo.py",
                      "bin/relevo_lista.py", "RELEVO_API.json", "lectura_api.diferencias", "De qué se trata", "Para dominarlo"):
            assert pieza in t, (tarea, pieza)
    noche = texto("prompts/tareas/lector-nocturno.md")
    for pieza in ("references/api.md", "scripts/api/relevo.py", "bin/relevo_lista.py", "RELEVO_API.json", "lector-api.yml/dispatches"):
        assert pieza in noche, pieza


def test_la_skill_y_las_compuertas_remiten_a_las_dos_referencias():
    skill = texto("SKILL.md")
    assert "references/redaccion.md" in skill and "references/api.md" in skill and "scripts/api/relevo.py" in skill
    assert "redaccion.md" in texto("references/box.md") and "estilo.js" in texto("docs/QUALITY_GATE.md")
    assert "Relevo con la suscripción" in texto("references/api.md") and "Regla de sincronía" in texto("references/api.md")


def test_el_box_exige_todos_los_scripts_del_repositorio():
    lista = re.search(r"for s in ([^;]+); do", texto("scripts/box/arranque.sh")).group(1).split()
    en_repo = sorted(p.name for p in (RAIZ / "scripts/box").iterdir() if p.is_file())
    assert sorted(lista) == en_repo


def test_los_apartados_de_la_guia_son_los_mismos_en_la_referencia_y_en_el_revisor():
    js = texto("scripts/paquete/estilo.js")
    apartados = re.findall(r'"([^"]+)"', re.search(r"const APARTADOS = \[(.*?)\];", js).group(1))
    assert len(apartados) == 7
    ref = texto("references/redaccion.md")
    for a in apartados:
        assert f"| {a} |" in ref, a
        assert a in texto("scripts/paquete/content.ejemplo.js"), a


def test_el_revisor_de_estilo_distingue_una_fila_buena_de_una_mala(tmp_path):
    if not shutil.which("node"):
        return
    buena = """{ asunto: "Límite a las deducciones de personas morales grandes", efecto: "Las personas morales con ingresos acumulables superiores a 50 millones de pesos ya no podrán deducir todo en el ejercicio. Sus deducciones se topan con un factor de 0.9667 sobre los ingresos o de 0.9900 sobre las propias deducciones, según el caso, y lo que no se deduzca se recupera en los veinte ejercicios siguientes (artículos 78-A a 78-E de la Ley del ISR).", vigencia: "En vigor el 1 de enero de 2027.", importa: "Pega a clientes medianos y grandes con márgenes bajos, que pagarán ISR aun con poca utilidad. Sirve para proyectar su ISR de 2027 con ambos supuestos.", fuente: [["DOF", "https://dof.gob.mx/x"]] }"""
    mala = """{ asunto: "Ley de Ingresos 2027: tasas", efecto: "Recargos «1.38 por ciento»; multas «50 por ciento»; retención «0.68 por ciento»; cabe señalar que aplica: todo.", vigencia: "En vigor.", importa: "Revisar.", fuente: [["DOF", "https://dof.gob.mx/x"]] }"""
    rel = "[]"   # desde el 24/11/2026 «Lo relevante» no lleva párrafos

    def correr(fila):
        d = tmp_path / str(abs(hash(fila)))
        d.mkdir()
        (d / "content.js").write_text(f"module.exports = {{ relevante: {rel}, filas: [{fila}], sjf: [] }};", encoding="utf-8")
        return subprocess.run(["node", str(RAIZ / "scripts/paquete/estilo.js"), str(d)], capture_output=True, text=True)
    ok, no = correr(buena), correr(mala)
    assert ok.returncode == 0 and "0 errores" in ok.stdout, ok.stdout
    assert no.returncode == 1
    for pista in ("dos puntos en el asunto", "citas entre comillas", "cadena de punto y coma", "muletilla «cabe señalar»"):
        assert pista in no.stdout, pista


def test_lanzador_y_plantillas_siguen_al_metodo():
    lanzador = texto("prompts/api/lanzador-api.md")
    assert "lector-api.yml/dispatches" in lanzador and "no lances otra" in lanzador
    assert "lanzador-api.md" in texto("references/api.md") and "Lanzador del lector por API" in texto("references/box.md")
    assert "19:17 y a las 20:17" in lanzador and "now-5400" in lanzador
    assert "lanzador-api.md" in texto("references/guardia.md") and "19:17 y 20:17" in texto("references/box.md")
    assert "firmó el commit (hipótesis descartada" in texto("references/api.md") and "20:37, en el repositorio" not in texto("SKILL.md")
    assert "De qué se trata" in texto("templates/operator-study.md") and "redaccion.md" in texto("templates/report.md")
    assert "anulado" in texto("references/api.md") and "LISTA_MAL_COPIADA" in texto("references/api.md")


def test_tareas_clonan_el_privado_sin_add_repo():
    # 23 y 24/11/2026: en las ejecuciones programadas add_repo no existe; el acceso viene de los repositorios de la tarea.
    for f in ("prompts/tareas/lector-nocturno.md", "prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md"):
        assert "git clone --depth 1 https://github.com/lianfixx/dof-trabajo" in texto(f), f
        assert "select:mcp__claude-code-remote__add_repo" not in texto(f), f
    assert "No adjuntes nada" in texto("prompts/api/lanzador-api.md")
    assert "Acceso de las tareas al repositorio privado" in texto("references/api.md")


def test_la_forma_aprobada_el_24_11_pasa_el_estilo_y_sale_en_una_sola_tabla(tmp_path):
    # Forma de la versión final de Emi del 24/11/2026, con contenido ficticio: una sola tabla y correo BLUF.
    if not shutil.which("node"):
        return
    d = RAIZ / "tests/fixtures/entrega_ficticia"
    r = subprocess.run(["node", str(RAIZ / "scripts/paquete/estilo.js"), str(d)], capture_output=True, text=True)
    assert r.returncode == 0 and "0 errores" in r.stdout, r.stdout
    assert "no menciona la P./J." not in r.stdout
    (tmp_path / "guia.js").write_text('module.exports = { titulo: "g", estado: "e", estudiar: [], cobertura: [], avisos: [], pendientes: [] };', encoding="utf-8")
    (tmp_path / "content.js").write_text((d / "content.js").read_text(encoding="utf-8").replace("module.exports = {", 'module.exports = { comentario: "c",', 1), encoding="utf-8")
    b = subprocess.run(["node", str(RAIZ / "scripts/paquete/build.js"), str(tmp_path), str(tmp_path)], capture_output=True, text=True)
    if "Cannot find module 'docx'" in b.stderr:
        return
    assert b.returncode == 0, b.stderr
    import zipfile
    xml = zipfile.ZipFile(tmp_path / "Actualizacion_DOF_SJF_01-03_03-03-2027.docx").read("word/document.xml").decode("utf-8")
    assert xml.count("<w:tbl>") == 1 and "Vigencia / obligatoriedad" in xml and "Semanario Judicial de la Federación ·" not in xml
    e = subprocess.run(["node", str(RAIZ / "scripts/paquete/email.js"), str(tmp_path), str(tmp_path)], capture_output=True, text=True)
    assert e.returncode == 0, e.stderr
    html = (tmp_path / "Correo_revision_DOF_SJF_01-03_03-03-2027.html").read_text(encoding="utf-8")
    assert html.count("<table") == 1 and "P./J. 11/2027" in html


def test_reglas_de_la_tabla_unica_en_todo_el_metodo():
    for f in ("prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md"):
        assert "título de una sola tabla" in texto(f) and "120–230" in texto(f) and "80–130" not in texto(f), f
    assert "Lo que Emi cambió en su versión final del 24 de noviembre de 2026" in texto("references/redaccion.md")
    assert "Vigencia/obligatoriedad" in texto("SKILL.md") and "80–130" not in texto("SKILL.md")


def test_respuestas_de_emi_del_24_11():
    # 1) el recorte de filas fue de esa semana; 2) el cierre escribe la opinión de Emi; 3) «por qué importa» siempre con frase.
    for f in ("prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md", "references/redaccion.md", "SKILL.md"):
        assert "[Espacio para mi opinión" not in texto(f), f
    for f in ("prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md"):
        assert "la opinión de Emi ya escrita" in texto(f) and "siempre con frase" in texto(f), f
    assert "Pocas filas" not in texto("references/redaccion.md") and "Siempre lleva frase" in texto("references/redaccion.md")


def test_escala_de_relevancia_igual_en_las_dos_vias():
    # Emi, 26/11/2026: «temas de relevancia social, de política, cosas de presidencia, todo lo IMPORTANTE debe estar».
    la = lector()
    escala = la.escala_relevancia()
    assert escala.startswith("Califica cada publicación") and escala in la.S_LECTOR
    for nivel in ("- alta:", "- media:", "- baja:", "- ninguna:", "elige el más alto"):
        assert nivel in escala, nivel
    for tema in ("Presidente o de la Presidenta de la República", "programas sociales", "reformas electorales", "INE"):
        assert tema in escala, tema
    assert "politica" in la.MATERIAS and "social" in la.MATERIAS
    assert "de cualquier materia" in la.S_SINTESIS and "en fiscal, PLD, administrativo o amparo" not in la.S_SINTESIS
    for f in ("prompts/tareas/lector-nocturno.md", "prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md"):
        t = texto(f)
        assert "references/relevancia.md" in t and "relevancia fiscal/PLD/administrativa/amparo" not in t, f
    for f in ("prompts/tareas/cierre-martes.md", "prompts/tareas/cierre-jueves.md"):
        t = texto(f)
        assert "Presidencia de la República, secretarías de Estado" in t and "IMSS, INFONAVIT" in t, f
        assert "(SHCP, SAT, CNBV, Banco de México, UIF, TFJA, SCJN, CJF y equivalentes)" not in t, f
    ref = texto("references/relevancia.md")
    assert "## Revisión del cierre" in ref and "Presidencia de la República; secretarías de Estado" in ref
    assert "references/relevancia.md" in texto("SKILL.md") and "relevancia.md" in texto("references/api.md")
    assert "relevancia.md" in texto("references/redaccion.md")
