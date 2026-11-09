#!/usr/bin/env bash
# Orquestador de fuentes para dof-castorena (corre en el box).
#   fuentes.sh martes  [FECHA]   DOF desde el corte del jueves anterior hasta el martes + SJF del viernes
#   fuentes.sh jueves  [FECHA]   DOF desde el corte del martes hasta el jueves
#   fuentes.sh viernes [FECHA]   SJF del viernes
#   fuentes.sh noche   [FECHA]   lo ya publicado del periodo que cierra mañana (lunes o miércoles)
#   fuentes.sh dof FECHA...      fechas sueltas en la entrega FECHA (la primera)
# FECHA = día de la entrega (AAAA-MM-DD); por defecto hoy en America/Mexico_City.
#
# Periodo «desde el corte anterior»: incluye el día del cierre anterior (jueves para el
# martes, martes para el jueves) para recoger sus vespertinas y extraordinarias tardías;
# lo que ese cierre ya cubrió se descarga solo para la continuidad de números y queda
# marcado `ya_reportada` en el inventario (no se lee ni se reporta otra vez).
#
# Deja todo en /workspace/dof/fuentes/<entrega>/ (dof/, sjf/, manifiesto.json), nunca
# borra nada y no se detiene en el primer fallo: corre todos los pasos, los anota en
# fuentes/<entrega>/estado.json y termina con código 1 si alguno falló.
# Para corridas largas (más de 10 min) usar bin/lanzar.sh, que lo deja en segundo plano.
set -uo pipefail
cd /workspace/dof
export TZ=America/Mexico_City
MODO="${1:?modo}"; shift || true
HOY="${1:-$(date +%F)}"
d() { date -d "$HOY $1" +%F; }
dow=$(date -d "$HOY" +%u)   # 1=lunes ... 7=domingo
CORTE=""
case "$MODO" in
  martes)  CORTE="$(d '-5 days')"; DIAS="$(d '-4 days') $(d '-3 days') $(d '-2 days') $(d '-1 day') $HOY"; SJF="$(d '-4 days')"; ENT="$HOY" ;;
  jueves)  CORTE="$(d '-2 days')"; DIAS="$(d '-1 day') $HOY"; SJF=""; ENT="$HOY" ;;
  viernes) DIAS=""; SJF="$HOY"; ENT="sjf-$HOY" ;;
  noche)   # lunes 21:30 -> periodo del martes; miércoles 21:30 -> periodo del jueves
           if [ "$dow" = 1 ]; then CORTE="$(d '-4 days')"; DIAS="$(d '-3 days') $(d '-2 days') $(d '-1 day') $HOY"; SJF="$(d '-3 days')"; ENT="$(d '+1 day')";
           elif [ "$dow" = 3 ]; then CORTE="$(d '-1 day')"; DIAS="$HOY"; SJF=""; ENT="$(d '+1 day')";
           else echo "noche solo corre lunes o miércoles (hoy $HOY es día $dow)" >&2; exit 2; fi ;;
  dof)     DIAS="$HOY $*"; SJF=""; ENT="$HOY" ;;
  *) echo "modo desconocido: $MODO" >&2; exit 2 ;;
esac
DEST="fuentes/$ENT"; mkdir -p "$DEST"
EST="$DEST/estado.json"
PASOS=()
paso() {  # paso NOMBRE comando...
  local n="$1"; shift
  local t0; t0=$(date +%s)
  "$@"; local rc=$?
  PASOS+=("{\"paso\":\"$n\",\"rc\":$rc,\"segundos\":$(( $(date +%s) - t0 ))}")
  [ $rc -eq 0 ] || echo "== FALLÓ $n (código $rc)" >&2
  return 0
}
escribe_estado() {  # escribe_estado ESTADO
  local p; p=$(IFS=,; echo "${PASOS[*]:-}")
  printf '{"entrega":"%s","modo":"%s","estado":"%s","actualizado":"%s","corte_anterior":"%s","dias":"%s","sjf":"%s","pasos":[%s]}\n' \
    "$ENT" "$MODO" "$1" "$(date +%FT%T%z)" "$CORTE" "$DIAS" "$SJF" "$p" > "$EST.tmp" && mv "$EST.tmp" "$EST"
}
echo "== $MODO entrega $ENT | corte anterior: ${CORTE:-n/a} | DOF: ${DIAS:-ninguno} | SJF: ${SJF:-ninguno} | $(date +%FT%T%z)"
escribe_estado EN_CURSO
paso arranque bash bin/arranque.sh
if [ -n "$DIAS" ]; then
  if [ -n "$CORTE" ]; then paso dof python3 bin/dof_fuentes.py "$DEST/dof" --corte "$CORTE" $DIAS
  else paso dof python3 bin/dof_fuentes.py "$DEST/dof" $DIAS; fi
  escribe_estado EN_CURSO
  paso paginas python3 bin/paginas.py "$DEST/dof"
  paso ocr_dof python3 bin/ocr.py "$DEST/dof"
fi
if [ -n "$SJF" ]; then
  paso sjf node bin/sjf_fuentes.mjs "$DEST/sjf" "$SJF"
  [ -f "$DEST/sjf/control.json" ] && paso ocr_sjf python3 bin/ocr.py "$DEST/sjf"
fi
paso manifiesto python3 bin/manifiesto.py "$DEST"
if printf '%s\n' "${PASOS[@]}" | grep -q '"rc":[1-9]'; then
  escribe_estado CON_FALLOS; echo "== terminado CON FALLOS: $DEST (ver $EST)"; exit 1
fi
escribe_estado OK
echo "== listo: $DEST | $(date +%FT%T%z)"
