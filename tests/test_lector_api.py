import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "api"))
import lector_api as la  # noqa: E402

# Texto ficticio: ninguna publicación real.
PAGS = [f"Página {n} del diario de prueba.\nACUERDO de prueba número {n} por el que se dispone algo.\n"
        f"El plazo vence el día {n} del mes.\nÚltima línea de la página {n}." for n in range(1, 8)]
USO = {"modelo": "prueba", "entrada": 1000, "salida": 200, "costo_usd": 0.004}


def montar(tmp: Path, paginas=PAGS, ocr=None, sin_texto=(), paginas_ocr=(), ya=False, anexo=False) -> Path:
    dest = tmp / "fuentes" / "2026-01-06"
    (dest / "dof" / "raw").mkdir(parents=True)
    (dest / "dof" / "raw" / "05012026-MAT.txt").write_text("\f".join(paginas) + "\f", encoding="utf-8")
    if ocr:
        (dest / "dof" / "raw" / "05012026-MAT.ocr.txt").write_text(
            "".join(f"=== PAGINA {n} (OCR) ===\n{t}\n" for n, t in ocr.items()), encoding="utf-8")
    anexos = []
    if anexo:
        (dest / "dof" / "anexos").mkdir()
        (dest / "dof" / "anexos" / "anexo1.txt").write_text("Anexo de prueba, única página.\nFin del anexo.\f", encoding="utf-8")
        anexos = [{"url": "https://dof.gob.mx/2026/X/anexo1.pdf", "archivo": "anexo1.pdf", "sha256": "b" * 64, "paginas": 1,
                   "paginas_sin_texto": [], "paginas_ocr": [], "necesita_ocr": False}]
    inv = {"ediciones": [{"fecha": "2026-01-05", "edicion": "MAT", "numero": "3/2026", "pdf": "05012026-MAT.pdf",
                          "sha256": "a" * 64, "paginas_reales": len(paginas), "paginas_declaradas": len(paginas),
                          "ok_paginas": True, "paginas_sin_texto": list(sin_texto), "paginas_ocr": list(paginas_ocr),
                          "ya_reportada": ya, "anexos": anexos,
                          "notas": [{"codigo": "5700001", "titulo": "ACUERDO de prueba uno", "organismo": "SECRETARIA DE PRUEBA",
                                     "url": "https://dof.gob.mx/nota_detalle.php?codigo=5700001&fecha=05/01/2026"},
                                    {"codigo": "5700002", "titulo": "AVISO de prueba dos", "organismo": "BANCO DE PRUEBA",
                                     "url": "https://dof.gob.mx/nota_detalle.php?codigo=5700002&fecha=05/01/2026"}]}],
           "errores": []}
    (dest / "dof" / "inventario.json").write_text(json.dumps(inv), encoding="utf-8")
    return dest


def pub(codigo, ini, fin, citas):
    return {"codigo": codigo, "titulo": "ACUERDO de prueba", "organismo": "SECRETARIA DE PRUEBA", "pagina_inicio": ini,
            "pagina_fin": fin, "completa_en_bloque": True, "tipo": "acuerdo", "resumen": "Dispone algo.",
            "sujetos_obligados": "no consta", "plazos": "día del mes", "vigencia": "no consta", "transitorios": "no consta",
            "efectos": "no consta", "materias": ["fiscal"], "relevancia": "media", "citas": citas}


def lector_bueno(codigos=("5700001", "5700002")):
    def f(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is None:
            return "## Inventario por edición\n\n- 5700001 ACUERDO de prueba.", USO
        cuerpo = usuario.split("Bloque:\n", 1)[1]
        nums = [int(x) for x in __import__("re").findall(r"<<<PÁGINA (\d+)>>>", cuerpo)]
        return {"ultima_linea": la.ultima_linea_real(cuerpo),
                "publicaciones": [pub(c, nums[0], nums[-1], [f"El plazo vence el día {nums[0]} del mes."]) for c in codigos]}, USO
    return f


def test_bloques_cubren_todo_sin_huecos(tmp_path):
    dest = montar(tmp_path)
    docs, problemas = la.universo(dest)
    bloques, sin = la.bloques_de(docs[0], 3)
    assert [(b["ini"], b["fin"]) for b in bloques] == [(1, 3), (4, 6), (7, 7)]
    assert not sin and not problemas
    assert all(f"<<<PÁGINA {n}>>>" in "".join(b["texto"] for b in bloques) for n in range(1, 8))


def test_ya_reportada_no_se_lee(tmp_path):
    docs, _ = la.universo(montar(tmp_path, ya=True))
    assert docs == []


def test_ocr_se_agrega_y_pagina_sin_ocr_queda_pendiente(tmp_path):
    pags = PAGS[:2] + ["  "] + [" "]
    dest = montar(tmp_path, paginas=pags, ocr={3: "Texto reconocido de la página tres por OCR."}, sin_texto=[3, 4], paginas_ocr=[3, 4])
    docs, _ = la.universo(dest)
    bloques, sin = la.bloques_de(docs[0], 10)
    assert "Texto reconocido de la página tres" in bloques[0]["texto"]
    assert sin == [4]


def test_pagina_en_blanco_con_ocr_vacio_cuenta_como_leida(tmp_path):
    dest = montar(tmp_path, paginas=PAGS[:2] + [" "], ocr={3: ""}, sin_texto=[3], paginas_ocr=[3])
    docs, _ = la.universo(dest)
    assert la.bloques_de(docs[0], 10)[1] == []


def test_corrida_integra(tmp_path, monkeypatch):
    dest = montar(tmp_path, anexo=True)
    monkeypatch.setattr(la, "llamar", lector_bueno())
    est = la.correr(dest, False, 8, 3, 2, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "INTEGRO" and est["bloques"] == 4 and est["paginas"] == 8
    assert est["titulos_del_indice_sin_nota"] == 0
    pre = (dest / "notas" / "PRELIMINAR_API.md").read_text()
    assert "Estado: INTEGRO" in pre and "codigo=5700001" in pre
    assert len(list((dest / "notas").glob("*_p*.json"))) == 4
    assert json.loads((dest / "ESTADO_API.json").read_text())["costo_usd"] > 0


def test_ultima_linea_falsa_deja_parcial(tmp_path, monkeypatch):
    dest = montar(tmp_path)

    def malo(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is None:
            return "texto", USO
        return {"ultima_linea": "Esta línea no existe en el bloque de ninguna manera.", "publicaciones": []}, USO
    monkeypatch.setattr(la, "llamar", malo)
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "PARCIAL" and "ULTIMA_LINEA_NO_COINCIDE" in est["bloques_con_problema"][0]
    assert est["llamadas"] == 3  # dos intentos de lectura y la síntesis
    assert "Estado: PARCIAL" in (dest / "notas" / "PRELIMINAR_API.md").read_text()


def test_citas_y_codigos_inventados_se_quitan(tmp_path):
    dest = montar(tmp_path)
    docs, _ = la.universo(dest)
    blq = la.bloques_de(docs[0], 10)[0][0]
    resp = {"ultima_linea": la.ultima_linea_real(blq["texto"]),
            "publicaciones": [pub("9999999", 1, 99, ["El plazo vence el día 1 del mes.", "Frase que el modelo inventó y no está."])]}
    nota = la.comprobar(docs[0], blq, resp)
    p = nota["publicaciones"][0]
    assert p["codigo"] == "" and p["citas"] == ["El plazo vence el día 1 del mes."] and p["citas_no_localizadas"] == 1
    assert (p["pagina_inicio"], p["pagina_fin"]) == (1, 7) and len(nota["avisos"]) == 3 and nota["estado"] == "INTEGRO"


def test_indice_sin_nota_se_reporta(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    monkeypatch.setattr(la, "llamar", lector_bueno(codigos=("5700001",)))
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["titulos_del_indice_sin_nota"] == 1
    assert "5700002 · AVISO de prueba dos" in (dest / "notas" / "PRELIMINAR_API.md").read_text()


def test_tope_de_gasto_detiene_y_deja_parcial(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    monkeypatch.setattr(la, "llamar", lector_bueno())
    est = la.correr(dest, False, 0.0001, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "PARCIAL" and est["llamadas"] == 0 and "tope" in est["sintesis"]


def test_reanudar_no_vuelve_a_pagar(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    monkeypatch.setattr(la, "llamar", lector_bueno())
    la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["bloques_reutilizados"] == 3 and est["llamadas"] == 1  # solo la síntesis


def test_seco_no_llama(tmp_path, monkeypatch):
    dest = montar(tmp_path)

    def nunca(*a, **k):
        raise AssertionError("no debe llamar")
    monkeypatch.setattr(la, "llamar", nunca)
    est = la.correr(dest, True, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "SECO" and est["bloques"] == 3 and not (dest / "ESTADO_API.json").exists()


def test_error_de_fuentes_impide_integro(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    inv = json.loads((dest / "dof" / "inventario.json").read_text())
    inv["errores"] = [{"fecha": "2026-01-05", "edicion": "VES", "paso": "pdf", "error": "no bajó"}]
    (dest / "dof" / "inventario.json").write_text(json.dumps(inv))
    monkeypatch.setattr(la, "llamar", lector_bueno())
    assert la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")["estado"] == "PARCIAL"
