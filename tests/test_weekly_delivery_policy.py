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
