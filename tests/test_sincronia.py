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
    buena = """{ asunto: "Límite a las deducciones de personas morales grandes", efecto: "Las personas morales con ingresos acumulables superiores a 50 millones de pesos ya no podrán deducir todo en el ejercicio. Sus deducciones se topan con un factor de 0.9667 sobre los ingresos o de 0.9900 sobre las propias deducciones, según el caso, y lo que no se deduzca se recupera en los veinte ejercicios siguientes (artículos 78-A a 78-E de la Ley del ISR).", vigencia: "En vigor el 1 de enero de 2027.", importa: "Pega a clientes medianos y grandes con márgenes bajos, que pagarán ISR aun con poca utilidad. Conviene proyectar su ISR de 2027 con ambos supuestos y revisar si alguno cae en las exclusiones del artículo 78-E.", fuente: [["DOF", "https://dof.gob.mx/x"]] }"""
    mala = """{ asunto: "Ley de Ingresos 2027: tasas", efecto: "Recargos «1.38 por ciento»; multas «50 por ciento»; retención «0.68 por ciento»; cabe señalar que aplica: todo.", vigencia: "En vigor.", importa: "Revisar.", fuente: [["DOF", "https://dof.gob.mx/x"]] }"""
    rel = '["La reforma al ISR limita desde 2027 las deducciones de las personas morales con ingresos superiores a 50 millones de pesos.", "La Ley de Ingresos condona multas y recargos de adeudos de 2025 o anteriores a quien pague durante 2027."]'

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
