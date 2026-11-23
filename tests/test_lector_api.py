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
            return "## Candidatas a la tabla del reporte\n\n### 5700001 · ACUERDO de prueba.", USO
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
        return {"ultima_linea": "Esta línea no existe en el bloque de ninguna manera.",
                "publicaciones": [pub("5700001", 1, 7, ["El plazo vence el día 1 del mes."])]}, USO
    monkeypatch.setattr(la, "llamar", malo)
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "PARCIAL" and "ULTIMA_LINEA_NO_COINCIDE" in est["bloques_con_problema"][0]
    assert est["llamadas"] == 3  # dos intentos de lectura y la síntesis
    assert est["costo_lectura_usd"] == 0.008  # los dos intentos se cobran
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
    assert est["estado"] == "PARCIAL" and est["llamadas"] == 0 and est["costo_usd"] == 0
    assert all("SIN_LEER_TOPE_DE_GASTO" in m for m in est["bloques_con_problema"])


def test_reanudar_no_vuelve_a_pagar(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    monkeypatch.setattr(la, "llamar", lector_bueno())
    la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["bloques_reutilizados"] == 3 and est["llamadas"] == 0 and est["costo_usd"] == 0  # ni lectura ni síntesis
    assert est["sintesis"].startswith("ok (la de la corrida anterior") and est["estado"] == "INTEGRO"
    assert "## Inventario por edición" in (dest / "notas" / "PRELIMINAR_API.md").read_text()


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


# ---------------------------------------------------------------- segunda versión: lo que enseñó la primera corrida real

def test_lineas_finales_toleran_numero_de_pagina_y_ocr():
    texto = "<<<PÁGINA 17>>>\nARTÍCULO 9. Texto final del lineamiento de prueba.\nLic. Nombre Ficticio Maza\n17\n"
    assert la.coincide_final("17", texto)                                   # el número de página es la última línea
    assert la.coincide_final("Lic. Nombre Ficticio Maza", texto)            # la última línea «con letras»
    assert la.coincide_final("ARTICULO 9. Texto final del lineamiento de prueba", texto)   # OCR corregido al copiar
    assert not la.coincide_final("18", texto)                               # una línea corta debe ser idéntica
    assert not la.coincide_final("7", texto)                                # «7» está dentro de «17», pero no es la línea
    assert not la.coincide_final("Una línea que no está en el final del bloque.", texto)
    assert not la.coincide_final("", texto) and la.coincide_final("", "<<<PÁGINA 1>>>\n")


def test_un_bloque_con_error_no_tumba_la_corrida(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    bueno = lector_bueno()

    def a_veces(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is not None and "Páginas 4 a 6" in usuario:
            raise la.ErrorAPI("HTTP 500 api_error", uso=None)
        return bueno(modelo, sistema, usuario, esquema, max_tokens)
    monkeypatch.setattr(la, "llamar", a_veces)
    est = la.correr(dest, False, 8, 3, 2, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "PARCIAL" and est["bloques_con_problema"] == ["05012026-MAT p. 4-6: ERROR_API"]
    assert json.loads((dest / "ESTADO_API.json").read_text())["bloques_integros"] == 2
    assert "ERROR_API" in (dest / "notas" / "05012026-MAT_p0004-0006.md").read_text()
    assert "Bloque con problema: 05012026-MAT p. 4-6" in (dest / "notas" / "PRELIMINAR_API.md").read_text()


def test_respuesta_cortada_parte_el_bloque_y_cobra(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    bueno, vistos = lector_bueno(), []

    def corta(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is not None:
            vistos.append(usuario.split("Páginas ", 1)[1].split(" de ", 1)[0])
            if "Páginas 1 a 7" in usuario:
                raise la.ErrorAPI("respuesta cortada por max_tokens", uso=dict(USO), corte=True)
        return bueno(modelo, sistema, usuario, esquema, max_tokens)
    monkeypatch.setattr(la, "llamar", corta)
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "INTEGRO" and est["bloques"] == 1 and est["bloques_leidos"] == 2 and est["bloques_divididos"] == 1
    assert vistos == ["1 a 7", "1 a 3", "4 a 7"]
    assert est["costo_lectura_usd"] == 0.012  # la respuesta cortada también se cobró
    assert json.loads((dest / "notas" / "05012026-MAT_p0001-0007.json").read_text())["estado"] == "DIVIDIDO"
    # Al reanudar no se vuelve a pagar ni el bloque cortado ni sus mitades.
    vistos.clear()
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert vistos == [] and est["bloques_reutilizados"] == 2 and est["estado"] == "INTEGRO"


def test_bloque_de_una_pagina_cortado_queda_con_problema(tmp_path, monkeypatch):
    dest = montar(tmp_path, paginas=PAGS[:1])

    def corta(modelo, sistema, usuario, esquema, max_tokens):
        raise la.ErrorAPI("respuesta cortada por max_tokens", uso=dict(USO), corte=True)
    monkeypatch.setattr(la, "llamar", corta)
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "PARCIAL" and "ERROR_API" in est["bloques_con_problema"][0]


def test_revalida_nota_anterior_sin_volver_a_llamar(tmp_path, monkeypatch):
    dest = montar(tmp_path, paginas=PAGS[:2] + ["Página 3.\nACUERDO de prueba número 3.\nLic. Nombre Ficticio\n3"])
    docs, _ = la.universo(dest)
    blq = la.bloques_de(docs[0], 10)[0][0]
    vieja = la.comprobar(docs[0], blq, {"ultima_linea": "3", "publicaciones": [pub("5700001", 1, 3, []), pub("5700002", 1, 3, [])]})
    assert vieja["estado"] == "INTEGRO"
    vieja.update({"estado": "ULTIMA_LINEA_NO_COINCIDE", "ultima_linea_ok": False})  # como la dejó la primera versión
    (dest / "notas").mkdir()
    (dest / "notas" / "05012026-MAT_p0001-0003.json").write_text(json.dumps(vieja))
    llamadas = []

    def solo_sintesis(modelo, sistema, usuario, esquema, max_tokens):
        llamadas.append(esquema is None)
        assert esquema is None, "no debe releer el bloque"
        return "## Candidatas a la tabla del reporte", USO
    monkeypatch.setattr(la, "llamar", solo_sintesis)
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "INTEGRO" and est["bloques_reutilizados"] == 1 and llamadas == [True]


def test_bloque_con_texto_y_sin_publicaciones_no_es_integro(tmp_path):
    dest = montar(tmp_path, paginas=["Texto largo de prueba con un acuerdo. " * 20 + "\nÚltima línea real del bloque."])
    docs, _ = la.universo(dest)
    blq = la.bloques_de(docs[0], 10)[0][0]
    nota = la.comprobar(docs[0], blq, {"ultima_linea": "Última línea real del bloque.", "publicaciones": []})
    assert nota["estado"] == "SIN_PUBLICACIONES" and nota["paginas_sin_nota"] == [1]


def test_inventario_y_pendientes_los_arma_el_codigo(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    recibido = []

    def lector(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is None:
            recibido.append(usuario)
            return "## Candidatas a la tabla del reporte\n\n- 5700001: algo.", USO
        cuerpo = usuario.split("Bloque:\n", 1)[1]
        nums = [int(x) for x in __import__("re").findall(r"<<<PÁGINA (\d+)>>>", cuerpo)]
        nada = dict(pub("5700002", nums[-1], nums[-1], []), relevancia="ninguna", titulo="AVISO sin importancia")
        return {"ultima_linea": la.ultima_linea_real(cuerpo), "publicaciones": [pub("5700001", nums[0], nums[-1], []), nada]}, USO
    monkeypatch.setattr(la, "llamar", lector)
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    pre = (dest / "notas" / "PRELIMINAR_API.md").read_text()
    assert est["estado"] == "INTEGRO" and len(recibido) == 1
    assert "AVISO sin importancia" not in recibido[0] and "5700001" in recibido[0]   # lo «ninguna» no viaja al redactor
    assert "- 5700001 · SECRETARIA DE PRUEBA · ACUERDO de prueba · p. 1-7 · media (fiscal)" in pre   # una nota partida en 3 bloques, unida
    assert "- 5700002 · SECRETARIA DE PRUEBA · AVISO sin importancia · p. 3-7 · ninguna" in pre
    assert pre.index("## Por verificar en el cierre") < pre.index("## Candidatas") < pre.index("## Inventario por edición")


def lote_falso(responder, estado="terminado"):
    """Sustituto de leer_por_lote: `responder(custom_id, params)` devuelve el resultado de cada petición (o None)."""
    def f(peticiones, espera_s):
        res = {}
        for q in peticiones:
            r = responder(q["custom_id"], q["params"])
            if r is not None:
                res[q["custom_id"]] = r
        return res, {"id": "msgbatch_prueba", "estado": estado, "pedidos": len(peticiones), "segundos": 1}
    return f


def mensaje_de(params, **cambios):
    usuario = params["messages"][0]["content"]
    obj, _ = lector_bueno()("m", "", usuario, {"x": 1}, 1)
    obj.update(cambios)
    return {"type": "succeeded", "message": {"model": "claude-sonnet-5-5", "stop_reason": "end_turn",
                                             "content": [{"type": "text", "text": json.dumps(obj)}],
                                             "usage": {"input_tokens": 1000, "output_tokens": 200}}}


def solo_sintesis_directa(contador):
    def f(modelo, sistema, usuario, esquema, max_tokens):
        contador.append("síntesis" if esquema is None else usuario.split("Páginas ", 1)[1].split(" de ", 1)[0])
        return lector_bueno()(modelo, sistema, usuario, esquema, max_tokens)
    return f


def test_lote_lee_todo_a_mitad_de_precio(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    directas = []
    monkeypatch.setattr(la, "leer_por_lote", lote_falso(lambda cid, params: mensaje_de(params)))
    monkeypatch.setattr(la, "llamar", solo_sintesis_directa(directas))
    est = la.correr(dest, False, 8, 3, 2, "claude-sonnet-5-5", "claude-opus-5-5", lote=True)
    assert est["estado"] == "INTEGRO" and est["bloques_por_lote"] == 3 and est["bloques_directos"] == 0
    assert directas == ["síntesis"] and est["lote"]["estado"] == "terminado"
    # 1 000 de entrada y 200 de salida con Sonnet (2 y 10 USD por millón) = 0.004; en lote, la mitad.
    assert est["costo_lectura_usd"] == round(3 * 0.002, 4)
    assert json.loads((dest / "notas" / "05012026-MAT_p0001-0003.json").read_text())["uso"]["via"] == "lote"


def test_lote_lo_que_falla_se_repite_con_llamada_directa(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    directas = []

    def responder(cid, params):
        usuario = params["messages"][0]["content"]
        if "Páginas 1 a 3" in usuario:
            return {"type": "errored", "error": {"type": "api_error"}}
        if "Páginas 4 a 6" in usuario:
            return mensaje_de(params, ultima_linea="Una línea que no está en el bloque para nada.")
        return None  # cancelada: no vino en los resultados
    monkeypatch.setattr(la, "leer_por_lote", lote_falso(responder, "cancelado_por_tiempo"))
    monkeypatch.setattr(la, "llamar", solo_sintesis_directa(directas))
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5", lote=True)
    assert est["estado"] == "INTEGRO" and sorted(directas) == ["1 a 3", "4 a 6", "7 a 7", "síntesis"]
    assert est["bloques_directos"] == 3 and est["bloques_por_lote"] == 1
    assert json.loads((dest / "notas" / "05012026-MAT_p0004-0006.json").read_text())["uso"]["via"] == "lote y directo"


def test_lote_respuesta_cortada_se_parte(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    directas = []

    def responder(cid, params):
        if "Páginas 1 a 3" in params["messages"][0]["content"]:
            return {"type": "succeeded", "message": {"stop_reason": "max_tokens", "content": [{"type": "text", "text": "{"}],
                                                     "usage": {"input_tokens": 1000, "output_tokens": 16000}}}
        return mensaje_de(params)
    monkeypatch.setattr(la, "leer_por_lote", lote_falso(responder))
    monkeypatch.setattr(la, "llamar", solo_sintesis_directa(directas))
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5", lote=True)
    assert est["estado"] == "INTEGRO" and sorted(directas) == ["1 a 1", "2 a 3", "síntesis"]
    assert est["bloques_leidos"] == 4 and est["bloques_divididos"] == 1


def test_lote_incierto_no_se_paga_dos_veces(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    directas = []
    monkeypatch.setattr(la, "leer_por_lote", lote_falso(lambda cid, params: None, "sin_terminar"))
    monkeypatch.setattr(la, "llamar", solo_sintesis_directa(directas))
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5", lote=True)
    assert est["estado"] == "PARCIAL" and directas == [] and est["costo_usd"] == 0
    assert all("LOTE_SIN_TERMINAR" in m for m in est["bloques_con_problema"])


def test_lote_no_creado_cae_a_llamadas_directas(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    directas = []
    monkeypatch.setattr(la, "leer_por_lote", lote_falso(lambda cid, params: None, "no_creado: HTTP 400"))
    monkeypatch.setattr(la, "llamar", solo_sintesis_directa(directas))
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5", lote=True)
    assert est["estado"] == "INTEGRO" and len(directas) == 4 and est["bloques_directos"] == 3


class RedFalsa:
    """Sustituto de _http para probar leer_por_lote sin red."""

    def __init__(self, estados, crear=None, resultados=""):
        self.estados, self.crear, self.resultados, self.pedidos = list(estados), crear, resultados, []

    def __call__(self, metodo, url, cuerpo=None, esperas=(0,), reintentar_red=True):
        self.pedidos.append((metodo, url.replace(la.API_LOTES, "")))
        if metodo == "POST" and url == la.API_LOTES:
            if isinstance(self.crear, Exception):
                raise self.crear
            return json.dumps({"id": "msgbatch_1", "processing_status": "in_progress"}).encode()
        if url.endswith("/cancel"):
            return b"{}"
        if url.endswith("/results"):
            return self.resultados.encode()
        if "?limit=" in url:
            return json.dumps({"data": []}).encode()
        est = self.estados.pop(0) if len(self.estados) > 1 else self.estados[0]
        return json.dumps({"id": "msgbatch_1", "processing_status": est}).encode()


def test_leer_por_lote_espera_y_trae_resultados(monkeypatch):
    red = RedFalsa(["in_progress", "ended"], resultados='{"custom_id":"a-0000","result":{"type":"succeeded","message":{}}}\nbasura\n')
    monkeypatch.setattr(la, "_http", red)
    monkeypatch.setattr(la, "PAUSA_LOTE", 0)
    res, info = la.leer_por_lote([{"custom_id": "a-0000", "params": {}}], 60)
    assert info["estado"] == "terminado" and info["id"] == "msgbatch_1" and res["a-0000"]["type"] == "succeeded"
    assert ("POST", "/msgbatch_1/cancel") not in red.pedidos


def test_leer_por_lote_cancela_al_vencer_el_plazo(monkeypatch):
    red = RedFalsa(["in_progress", "canceling", "ended"], resultados='{"custom_id":"a-0000","result":{"type":"canceled"}}')
    monkeypatch.setattr(la, "_http", red)
    monkeypatch.setattr(la, "PAUSA_LOTE", 0)
    res, info = la.leer_por_lote([{"custom_id": "a-0000", "params": {}}], 0)
    assert info["estado"] == "cancelado_por_tiempo" and ("POST", "/msgbatch_1/cancel") in red.pedidos
    assert res["a-0000"]["type"] == "canceled"


def test_leer_por_lote_rechazo_claro_es_no_creado_y_fallo_ambiguo_no(monkeypatch):
    monkeypatch.setattr(la, "PAUSA_LOTE", 0)
    monkeypatch.setattr(la, "_http", RedFalsa(["ended"], crear=la.ErrorAPI("HTTP 400 invalid_request_error", codigo=400)))
    assert la.leer_por_lote([{"custom_id": "a", "params": {}}], 60)[1]["estado"].startswith("no_creado")
    # Sin respuesta al crear y sin lote reciente en la lista: tampoco existe.
    monkeypatch.setattr(la, "_http", RedFalsa(["ended"], crear=la.ErrorAPI("sin respuesta: TimeoutError", codigo=-1)))
    assert la.leer_por_lote([{"custom_id": "a", "params": {}}], 60)[1]["estado"].startswith("no_creado")

    def sin_red(metodo, url, cuerpo=None, esperas=(0,), reintentar_red=True):
        raise la.ErrorAPI("sin respuesta: TimeoutError", codigo=-1)
    monkeypatch.setattr(la, "_http", sin_red)
    assert la.leer_por_lote([{"custom_id": "a", "params": {}}], 60)[1]["estado"].startswith("incierto")


def test_interpretar_cobra_aunque_falle():
    msg = {"stop_reason": "max_tokens", "content": [{"type": "text", "text": "{"}], "usage": {"input_tokens": 1_000_000, "output_tokens": 0}}
    try:
        la.interpretar(msg, "claude-sonnet-5-5", {"x": 1}, la.DESCUENTO_LOTE)
        raise AssertionError("debió fallar")
    except la.ErrorAPI as e:
        assert e.corte and e.uso["costo_usd"] == 1.0  # 2 USD por millón, a mitad de precio


def test_error_inesperado_deja_estado_y_no_revienta(tmp_path, monkeypatch, capsys):
    dest = montar(tmp_path)

    def roto(*a, **k):
        raise RuntimeError("detalle interno que no debe imprimirse")
    monkeypatch.setattr(la, "universo", roto)
    assert la.main(["lector_api.py", str(dest), "--sin-lote"]) == 1
    assert json.loads((dest / "ESTADO_API.json").read_text())["estado"] == "ERROR_INTERNO"
    assert "detalle interno" not in capsys.readouterr().out


def test_paginas_que_ninguna_nota_cubre_impiden_integro(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    partir_real = la.partir

    def corta(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is not None and "Páginas 1 a 7" in usuario:
            raise la.ErrorAPI("respuesta cortada por max_tokens", uso=dict(USO), corte=True)
        return lector_bueno()(modelo, sistema, usuario, esquema, max_tokens)
    monkeypatch.setattr(la, "llamar", corta)
    monkeypatch.setattr(la, "partir", lambda b: partir_real(b)[:1])  # defecto simulado: se pierde la segunda mitad
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert est["estado"] == "PARCIAL" and est["bloques_con_problema"] == ["05012026-MAT p. 4-7: SIN_NOTA"]


def test_trozo_de_continuacion_hereda_el_codigo_del_bloque_anterior():
    def nota(ini, fin, pubs):
        return {"doc": "05012026-MAT", "ini": ini, "fin": fin, "estado": "INTEGRO", "publicaciones": pubs}
    abierta = dict(pub("5700001", 1, 3, []), completa_en_bloque=False)
    sigue = dict(pub("", 4, 6, []), completa_en_bloque=False, titulo="No consta: continuación de una tabla")
    edicto = dict(pub("", 7, 7, []), titulo="Edicto de prueba")                      # completo y sin código: no hereda
    originales = [nota(1, 3, [abierta]), nota(4, 6, [sigue]), nota(7, 7, [edicto])]
    nuevas, cuantos = la.heredar_codigos(originales)
    assert cuantos == 1 and [p["codigo"] for n in nuevas for p in n["publicaciones"]] == ["5700001", "5700001", ""]
    assert nuevas[1]["publicaciones"][0]["codigo_heredado"] and sigue["codigo"] == ""   # la nota original no se toca
    assert [(g["codigo"], g["ini"], g["fin"], g["titulo"]) for g in la.agrupar(nuevas)] == \
        [("5700001", 1, 6, "ACUERDO de prueba"), ("", 7, 7, "Edicto de prueba")]
    # Si el bloque anterior cerró su última publicación, o hay un hueco de páginas, nadie hereda.
    assert la.heredar_codigos([nota(1, 3, [pub("5700001", 1, 3, [])]), nota(4, 6, [sigue])])[1] == 0
    assert la.heredar_codigos([nota(1, 3, [abierta]), nota(5, 6, [dict(sigue, pagina_inicio=5)])])[1] == 0


def test_sintesis_por_grupos_se_une_en_dos_secciones():
    partes = ["## Candidatas a la tabla del reporte\n\n### 5700001 · Uno\nTexto uno.\n\n## Avisos secundarios para la guía\n- 5700002: tipo de cambio.",
              "## Candidatas a la tabla del reporte\n\n### 5700003 · Tres\nTexto tres.",
              "## Avisos secundarios para la guía\n- 5700004: tasas."]
    texto = la.unir_sintesis(partes)
    assert texto.count("## Candidatas a la tabla del reporte") == 1 and texto.count("## Avisos secundarios para la guía") == 1
    assert texto.index("### 5700001") < texto.index("### 5700003") < texto.index("## Avisos secundarios") < texto.index("5700002") < texto.index("5700004")
    assert la.unir_sintesis([]) == ""


def test_material_va_por_publicacion_y_en_grupos_pequenos():
    def nota(ini, fin, pubs):
        return {"doc": "05012026-MAT", "ini": ini, "fin": fin, "estado": "INTEGRO", "publicaciones": pubs}
    doc = {"id": "05012026-MAT", "tipo": "edicion", "fecha": "2026-01-05", "edicion": "MAT", "numero": "3/2026"}
    notas = [nota(1, 3, [dict(pub("5700001", 1, 3, ["cita uno"]), completa_en_bloque=False)]),
             nota(4, 6, [pub("5700001", 4, 5, []), dict(pub("5700002", 6, 6, []), relevancia="baja"),
                         dict(pub("", 6, 6, []), relevancia="ninguna")])]
    unidades = la.material_sintesis([doc], {"05012026-MAT": notas})
    assert [(u["codigo"], len(u["trozos"])) for u in unidades] == [("5700001", 2), ("5700002", 1)]   # los trozos de una nota viajan juntos
    assert "citas" in unidades[0]["trozos"][0] and "citas" not in unidades[1]["trozos"][0]             # lo «baja» va abreviado
    assert [len(g) for g in la.en_grupos(unidades, maximo=10)] == [1, 1] and len(la.en_grupos(unidades)) == 1


def test_sintesis_cortada_se_redacta_en_mitades(tmp_path, monkeypatch):
    dest = montar(tmp_path)
    bueno, tamanos = lector_bueno(), []

    def redactor(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is not None:
            return bueno(modelo, sistema, usuario, esquema, max_tokens)
        n = len(json.loads(usuario.split("\n", 1)[1]))
        tamanos.append(n)
        if n > 1:
            raise la.ErrorAPI("respuesta cortada por max_tokens", uso=dict(USO), corte=True, parcial="## Candidatas a la tabla del reporte\n\nA medias")
        return "## Candidatas a la tabla del reporte\n\n### 570000%d · completa" % len(tamanos), USO
    monkeypatch.setattr(la, "llamar", redactor)
    est = la.correr(dest, False, 8, 10, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    pre = (dest / "notas" / "PRELIMINAR_API.md").read_text()
    assert tamanos == [2, 1, 1] and est["sintesis"] == "ok" and "A medias" not in pre and pre.count("· completa") == 2
    assert est["costo_sintesis_usd"] == 0.012  # la respuesta cortada también se cobró


# ---------------------------------------------------------------- tablas numéricas con el modelo barato

CIFRAS = "001 002 003 4,512.75 98.10 1,204.33 77.00 5.25\n" * 80   # una página de pura tabla (más de 2 000 cifras)


def lector_de_tablas(vistos, relevancia="ninguna"):
    def f(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is None:
            return "## Candidatas a la tabla del reporte\n\n### sin código · tabla", USO
        cuerpo = usuario.split("Bloque:\n", 1)[1]
        nums = [int(x) for x in __import__("re").findall(r"<<<PÁGINA (\d+)>>>", cuerpo)]
        vistos.append((modelo, nums[0], nums[-1]))
        rel = relevancia if modelo == "claude-haiku-5-5" else "media"
        trozo = dict(pub("", nums[0], nums[-1], []), completa_en_bloque=False, relevancia=rel, titulo="No consta: continuación de tabla")
        return {"ultima_linea": la.ultima_linea_real(cuerpo), "publicaciones": [trozo]}, USO
    return f


def test_tabla_numerica_exige_cifras_sin_palabras_normativas_ni_titulos(tmp_path):
    dest = montar(tmp_path, paginas=[CIFRAS, CIFRAS, PAGS[0], CIFRAS + "ARTÍCULO 5. Texto.", CIFRAS[:1500], CIFRAS + "ACUERDO de prueba uno y lo que sigue"])
    doc = la.universo(dest)[0][0]
    bloques = la.bloques_de(doc, 1)[0]
    assert [la.es_tabla_numerica(doc, b) for b in bloques] == [True, True, False, False, False, False]
    assert not la.es_tabla_numerica(doc, la.bloques_de(doc, 3)[0][0])   # basta una página de texto en el bloque
    # Un título del índice oficial dentro del bloque (aunque no traiga palabras normativas) también lo descarta.
    titulo = "TIPO de cambio para solventar obligaciones denominadas en moneda extranjera"
    con_indice = dict(doc, indice=[{"codigo": "5700009", "organismo": "BANCO DE PRUEBA", "titulo": titulo, "url": ""}])
    blq = la._bloque(doc["id"], 1, [CIFRAS * 40 + titulo + " pagaderas en la República"])
    assert la.es_tabla_numerica(doc, blq) and not la.es_tabla_numerica(con_indice, blq)


def test_tablas_van_al_modelo_barato_y_el_texto_al_lector(tmp_path, monkeypatch):
    dest = montar(tmp_path, paginas=[PAGS[0], CIFRAS, CIFRAS])
    vistos = []
    monkeypatch.setattr(la, "llamar", lector_de_tablas(vistos))
    est = la.correr(dest, False, 8, 1, 1, "claude-sonnet-5-5", "claude-opus-5-5", m_tablas="claude-haiku-5-5")
    assert vistos == [("claude-sonnet-5-5", 1, 1), ("claude-haiku-5-5", 2, 2), ("claude-haiku-5-5", 3, 3)]
    assert est["estado"] == "INTEGRO" and est["bloques_tabla_numerica"] == 2 and est["tablas_releidas_con_el_lector"] == 0
    assert json.loads((dest / "notas" / "05012026-MAT_p0002-0002.json").read_text())["uso"]["modelo"] == "prueba"
    # Sin modelo de tablas (o igual al lector), todo lo lee el lector.
    vistos.clear()
    dest2 = montar(tmp_path / "otra", paginas=[PAGS[0], CIFRAS])
    la.correr(dest2, False, 8, 1, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    assert {m for m, _, _ in vistos} == {"claude-sonnet-5-5"}


def test_tabla_cuya_nota_trae_algo_mas_la_relee_el_lector(tmp_path, monkeypatch):
    dest = montar(tmp_path, paginas=[CIFRAS])
    vistos = []
    monkeypatch.setattr(la, "llamar", lector_de_tablas(vistos, relevancia="media"))   # el modelo barato ve algo relevante
    est = la.correr(dest, False, 8, 1, 1, "claude-sonnet-5-5", "claude-opus-5-5", m_tablas="claude-haiku-5-5")
    assert vistos == [("claude-haiku-5-5", 1, 1), ("claude-sonnet-5-5", 1, 1)] and est["tablas_releidas_con_el_lector"] == 1
    assert est["estado"] == "INTEGRO" and est["costo_lectura_usd"] == 0.008   # las dos lecturas se cobran


def test_tabla_en_lote_usa_el_modelo_barato_y_se_repite_si_falla(tmp_path, monkeypatch):
    dest = montar(tmp_path, paginas=[PAGS[0], CIFRAS, CIFRAS])
    modelos, vistos = {}, []

    def responder(cid, params):
        usuario = params["messages"][0]["content"]
        modelos[usuario.split("Páginas ", 1)[1].split(" de ", 1)[0]] = params["model"]
        if "Páginas 3 a 3" in usuario:
            return {"type": "errored", "error": {"type": "api_error"}}
        r = mensaje_de(params)
        if params["model"] == "claude-haiku-5-5":
            obj = json.loads(r["message"]["content"][0]["text"])
            obj["publicaciones"] = [dict(obj["publicaciones"][0], relevancia="baja")]
            r["message"]["content"][0]["text"] = json.dumps(obj)
        return r
    monkeypatch.setattr(la, "leer_por_lote", lote_falso(responder))
    monkeypatch.setattr(la, "llamar", lector_de_tablas(vistos))
    est = la.correr(dest, False, 8, 1, 1, "claude-sonnet-5-5", "claude-opus-5-5", lote=True, m_tablas="claude-haiku-5-5")
    assert modelos == {"1 a 1": "claude-sonnet-5-5", "2 a 2": "claude-haiku-5-5", "3 a 3": "claude-haiku-5-5"}
    assert vistos == [("claude-haiku-5-5", 3, 3)] and est["estado"] == "INTEGRO"   # un error de la API se repite con el mismo modelo
    # 1 000 de entrada y 200 de salida en lote: Sonnet 0.002 y Haiku 0.0001; más la relectura directa de prueba (0.004)
    assert est["costo_lectura_usd"] == round(0.002 + 0.0001 + 0.004, 4)


def test_releer_tablas_vuelve_a_leer_solo_las_pedidas(tmp_path, monkeypatch):
    dest = montar(tmp_path, paginas=[PAGS[0], CIFRAS, CIFRAS])
    vistos = []
    monkeypatch.setattr(la, "llamar", lector_de_tablas(vistos))
    la.correr(dest, False, 8, 1, 1, "claude-sonnet-5-5", "claude-opus-5-5", m_tablas="claude-haiku-5-5")
    vistos.clear()
    est = la.correr(dest, False, 8, 1, 1, "claude-sonnet-5-5", "claude-opus-5-5", m_tablas="claude-haiku-5-5", releer_tablas=1)
    assert vistos == [("claude-haiku-5-5", 2, 2)] and est["bloques_reutilizados"] == 2 and est["estado"] == "INTEGRO"
    assert est["sintesis"].startswith("ok (la de la corrida anterior")   # las notas no cambiaron de estado: no se paga otra síntesis
