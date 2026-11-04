import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_delivery_config_is_explicit_and_consistent():
    config = (ROOT / "config/default.yaml").read_text(encoding="utf-8")
    assert "modules: [dof, sjf]" in config
    assert "modules: [dof]" in config
    assert "include_sjf: false" in config
    assert config.count("attachment_count: 4") == 2
    assert "auto_email: false" in config

def test_skill_explicitly_excludes_sjf_thursday():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "exclusivamente DOF" in skill
    assert "cuatro archivos conjuntos" in skill
    assert "no crea un envío semanal adicional por defecto" in skill

def test_quality_gate_separates_day_audits():
    gate = (ROOT / "docs/QUALITY_GATE.md").read_text(encoding="utf-8")
    assert "Un SJF parcial bloquea el cierre conjunto del martes" in gate
    assert "no" in gate and "DOF autónomo del jueves" in gate

def test_moved_skill_sections_keep_full_text_in_references():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    sjf = (ROOT / "references/sjf-y-distribucion.md").read_text(encoding="utf-8")
    unlock = (ROOT / "references/desbloqueo.md").read_text(encoding="utf-8")
    assert "references/sjf-y-distribucion.md" in skill
    assert "references/desbloqueo.md" in skill
    for heading in ("## Módulo semanal SJF — obligatorio",
                    "## Operación SJF asistida y recuperación de documentos",
                    "## Distribución semanal definitiva — aprobada 20/10/2026"):
        assert heading in sjf and heading not in skill
    assert "exclusivamente DOF" in sjf
    assert "cuatro archivos conjuntos" in sjf
    assert "no crea un envío semanal adicional por defecto" in sjf
    assert "Esta sección prevalece sobre toda referencia anterior" in sjf
    assert "## Protocolo obligatorio de desbloqueo con intervención de Emi — 20/10/2026" in unlock
    assert "Portales oficiales de recuperación" in unlock
    for name in ("sjf-y-distribucion.md", "desbloqueo.md", "claude-code.md"):
        text = (ROOT / "references" / name).read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#\s]+)", text):
            if not re.match(r"^[a-z]+:", target):
                assert (ROOT / "references" / target).exists(), (name, target)
