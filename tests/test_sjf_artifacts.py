import pytest
from src.dof_monitor.sjf_artifacts import validate_editorial, build, OPINION_SLOT

def sample():
    return {
        "summary":"La publicación exige revisar los límites de obligatoriedad antes de aplicar el criterio.",
        "items":[{
            "title":"Criterio hipotético",
            "effect":"Ejemplo no real para probar el generador.",
            "status":"Tesis aislada; no obligatoria",
            "importance":"Verificar hechos y régimen temporal",
            "study":"Explicación, fundamentos, límites, ejemplo hipotético y contraargumento, redactados sólo como prueba.",
            "source_url":"https://sjfsemanal.scjn.gob.mx/detalle/tesis/2031846"
        }],
        "suggested_comment":"El criterio plantea una distinción jurídica relevante que conviene examinar con cautela. Antes de trasladarlo a un expediente concreto debemos comprobar los hechos, el órgano emisor, el fundamento y la temporalidad aplicable. También resulta indispensable contrastar los posibles argumentos contrarios y evitar atribuir efectos generales a una resolución particular sin respaldo suficiente.",
        "draft_email":"Licenciado, buen día. Le comparto la actualización del Semanario Judicial de la Federación correspondiente al periodo revisado. El reporte presenta un criterio de ejemplo, utilizado únicamente para verificar el funcionamiento técnico del generador, sin afirmar que se trate de una publicación real del periodo. Antes de aplicar cualquier razonamiento a un asunto del despacho conviene revisar su fuente primaria, los hechos relevantes y la fuerza jurídica del criterio. La guía adjunta desarrolla los límites y los puntos que requerirían una comprobación adicional. " + OPINION_SLOT + " Saludos, Emiliano García Milla"
    }

def test_valid_editorial():
    assert validate_editorial(sample()) == []

def test_missing_source_blocks():
    x=sample()
    x["items"][0]["source_url"]="https://example.org"
    assert any("non-official" in e for e in validate_editorial(x))

def test_missing_opinion_slot_blocks():
    x=sample()
    x["draft_email"]=x["draft_email"].replace(OPINION_SLOT,"")
    assert validate_editorial(x)

def test_incomplete_control_blocks_generation(tmp_path):
    from src.dof_monitor.sjf_intake import initialize
    import json
    control=initialize("2026-10-16",tmp_path)
    editorial=tmp_path/"editorial.json"
    editorial.write_text(json.dumps(sample()),encoding="utf-8")
    with pytest.raises(ValueError,match="NO FINAL"):
        build(control,editorial,tmp_path/"output")
    assert not (tmp_path/"output").exists()
