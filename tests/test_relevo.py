"""Pruebas del relevo entre el lector por API y la suscripción (scripts/api/relevo.py y scripts/box/relevo_lista.py)."""
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


relevo = cargar("relevo", "scripts/api/relevo.py")
lista_box = cargar("relevo_lista", "scripts/box/relevo_lista.py")

INVENTARIO = {"ediciones": [
    {"fecha": "2026-01-01", "edicion": "MAT", "numero": "1/2026", "pdf": "01012026-MAT.pdf", "sha256": "a" * 64, "paginas_reales": 90, "ya_reportada": True},
    {"fecha": "2026-01-02", "edicion": "MAT", "numero": "2/2026", "pdf": "02012026-MAT.pdf", "sha256": "b" * 64, "paginas_reales": 120, "ok_paginas": True,
     "anexos": [{"archivo": "anexo1.pdf", "sha256": "c" * 64, "paginas": 30}, {"url": "https://dof.gob.mx/x.pdf", "error": "HTTP 500"}]},
    {"fecha": "2026-01-05", "edicion": "MAT", "numero": "3/2026", "pdf": "05012026-MAT.pdf", "sha256": "d" * 64, "paginas_reales": 64, "anexos": []}],
    "errores": []}


def doc(id_, sha, paginas, integro=True, tipo="edicion"):
    return {"id": id_, "tipo": tipo, "sha256_pdf": sha, "paginas": paginas, "bloques": 4, "integro": integro}


def estado(docs, **cambios):
    e = {"formato": "dof-lector-api-v2", "entrega": "2026-01-06", "estado": "INTEGRO", "sintesis": "ok", "run_id": "77",
         "fin_utc": "2026-01-06T01:40:00Z", "documentos_leidos": docs}
    e.update(cambios)
    return e


TODOS = [doc("02012026-MAT", "b" * 64, 120), doc("anexo_anexo1", "c" * 64, 30, tipo="anexo"), doc("05012026-MAT", "d" * 64, 64)]


def test_lista_del_box_solo_lo_nuevo_y_lo_que_no_bajo_aparte():
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    assert [(d["id"], d["tipo"], d["paginas"]) for d in l["documentos"]] == \
        [("02012026-MAT", "edicion", 120), ("anexo_anexo1", "anexo", 30), ("05012026-MAT", "edicion", 64)]
    assert len(l["sin_descargar"]) == 1 and l["sin_descargar"][0]["que"] == "anexo"


def test_relevo_total_cuando_todo_coincide():
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    v = relevo.comprobar(estado(TODOS), l)
    assert v["relevo"] == "TOTAL" and len(v["por_api"]) == 3 and v["por_suscripcion"] == [] and v["sintesis_ok"]
    assert any("no pudo descargar" in m for m in v["motivos"])   # el anexo que el box no bajó se avisa aparte


def test_documento_nuevo_o_con_otro_sha_lo_lee_la_suscripcion():
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    v = relevo.comprobar(estado(TODOS[:2]), l)                                   # la API no vio la edición del día 5
    assert v["relevo"] == "PARCIAL" and [d["id"] for d in v["por_suscripcion"]] == ["05012026-MAT"]
    otro = [TODOS[0], TODOS[1], doc("05012026-MAT", "e" * 64, 64)]                 # mismo nombre, otro PDF
    v = relevo.comprobar(estado(otro), l)
    assert v["relevo"] == "PARCIAL" and "SHA-256 distinto" in v["por_suscripcion"][0]["motivo"] and v["solo_en_api"] == ["05012026-MAT"]


def test_documento_no_integro_o_con_paginas_distintas_no_se_releva():
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    v = relevo.comprobar(estado([doc("02012026-MAT", "b" * 64, 120, integro=False), TODOS[1], doc("05012026-MAT", "d" * 64, 60)], estado="PARCIAL"), l)
    assert v["relevo"] == "PARCIAL" and [d["id"] for d in v["por_api"]] == ["anexo_anexo1"]
    assert [d["motivo"][:28] for d in v["por_suscripcion"]] == ["el lector por API no lo dejó", "páginas distintas: box 64, A"]


def test_sin_estado_otra_entrega_o_error_interno_es_ninguno():
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    for e in (None, estado(TODOS, entrega="2026-01-08"), estado(TODOS, estado="ERROR_INTERNO"), estado(TODOS, formato="otro"), {"x": 1}):
        v = relevo.comprobar(e, l)
        assert v["relevo"] == "NINGUNO" and len(v["por_suscripcion"]) == 3 and v["por_api"] == []
    assert relevo.comprobar(estado([doc("x", "f" * 64, 9)]), l)["relevo"] == "NINGUNO"


def test_sintesis_incompleta_no_impide_el_relevo_pero_se_avisa():
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    v = relevo.comprobar(estado(TODOS, sintesis="cortada por longitud (x)"), l)
    assert v["relevo"] == "TOTAL" and not v["sintesis_ok"] and any("síntesis" in m for m in v["motivos"])


def test_box_sin_ediciones_nuevas_o_sin_inventario():
    assert relevo.comprobar(estado(TODOS), lista_box.lista({"ediciones": []}, "2026-01-06"))["relevo"] == "SIN_DOCUMENTOS"
    assert relevo.comprobar(estado(TODOS), {"entrega": "2026-01-06", "error": "sin inventario"})["relevo"] == "NINGUNO"


def test_linea_de_comandos_y_codigos_de_salida(tmp_path):
    l = tmp_path / "lista.json"
    l.write_text(json.dumps(lista_box.lista(INVENTARIO, "2026-01-06")))
    e = tmp_path / "ESTADO_API.json"
    e.write_text(json.dumps(estado(TODOS)))
    assert relevo.main(["relevo.py", "comprobar", str(e), str(l)]) == 0
    e.write_text(json.dumps(estado(TODOS[:1])))
    assert relevo.main(["relevo.py", "comprobar", str(e), str(l)]) == 3
    assert relevo.main(["relevo.py", "comprobar", str(tmp_path / "no-existe.json"), str(l)]) == 4


def test_el_lector_deja_integro_por_documento(tmp_path, monkeypatch):
    la = cargar("lector_api_r", "scripts/api/lector_api.py")
    prueba = cargar("prueba_lector", "tests/test_lector_api.py")
    dest = prueba.montar(tmp_path)
    monkeypatch.setattr(la, "llamar", prueba.lector_bueno())
    est = la.correr(dest, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")
    d = est["documentos_leidos"][0]
    assert (d["id"], d["tipo"], d["paginas"], d["bloques"], d["integro"]) == ("05012026-MAT", "edicion", 7, 3, True)

    def falla(modelo, sistema, usuario, esquema, max_tokens):
        if esquema is not None and "Páginas 4 a 6" in usuario:
            raise la.ErrorAPI("HTTP 500")
        return prueba.lector_bueno()(modelo, sistema, usuario, esquema, max_tokens)
    dest2 = prueba.montar(tmp_path / "b")
    monkeypatch.setattr(la, "llamar", falla)
    assert la.correr(dest2, False, 8, 3, 1, "claude-sonnet-5-5", "claude-opus-5-5")["documentos_leidos"][0]["integro"] is False


def test_lista_copiada_con_un_error_se_detecta_por_su_huella(tmp_path):
    l = lista_box.lista(INVENTARIO, "2026-01-06")
    assert len(l["huella"]) == 64 and relevo.comprobar(estado(TODOS), l)["relevo"] == "TOTAL"
    mala = json.loads(json.dumps(l))
    mala["documentos"][0]["sha256"] = "b" * 63 + "c"            # un carácter cambiado al copiar
    v = relevo.comprobar(estado(TODOS), mala)
    assert v["relevo"] == "LISTA_MAL_COPIADA" and v["por_api"] == [] and "huella" in v["motivos"][0]
    sin = {k: x for k, x in l.items() if k != "huella"}          # una lista sin huella tampoco vale
    assert relevo.comprobar(estado(TODOS), sin)["relevo"] == "LISTA_MAL_COPIADA"
    f = tmp_path / "l.json"
    f.write_text(json.dumps(mala))
    e = tmp_path / "e.json"
    e.write_text(json.dumps(estado(TODOS)))
    assert relevo.main(["relevo.py", "comprobar", str(e), str(f)]) == 5
