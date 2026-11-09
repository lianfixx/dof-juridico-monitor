#!/usr/bin/env bash
# Orquestador de fuentes para dof-castorena (corre en el box).
#   fuentes.sh martes  [FECHA]   DOF viernes..martes + SJF del viernes anterior
#   fuentes.sh jueves  [FECHA]   DOF miércoles y jueves
#   fuentes.sh viernes [FECHA]   SJF del viernes
#   fuentes.sh noche   [FECHA]   lo ya publicado del periodo que cierra mañana (lunes o miércoles)
#   fuentes.sh dof FECHA...      fechas sueltas (vespertinas tardías, correcciones)
# FECHA = día de la entrega (AAAA-MM-DD); por defecto hoy en America/Mexico_City.
# Deja todo en /workspace/dof/fuentes/<entrega>/ (dof/, sjf/, manifiesto.json) y nunca borra nada.
set -euo pipefail
cd /workspace/dof
export TZ=America/Mexico_City
MODO="${1:?modo}"; shift || true
HOY="${1:-$(date +%F)}"
d() { date -d "$HOY $1" +%F; }
dow=$(date -d "$HOY" +%u)   # 1=lunes ... 7=domingo
case "$MODO" in
  martes)  DIAS="$(d '-4 days') $(d '-3 days') $(d '-2 days') $(d '-1 day') $HOY"; SJF="$(d '-4 days')"; ENT="$HOY" ;;
  jueves)  DIAS="$(d '-1 day') $HOY"; SJF=""; ENT="$HOY" ;;
  viernes) DIAS=""; SJF="$HOY"; ENT="sjf-$HOY" ;;
  noche)   # lunes 21:30 -> periodo del martes; miércoles 21:30 -> periodo del jueves
           if [ "$dow" = 1 ]; then DIAS="$(d '-3 days') $(d '-2 days') $(d '-1 day') $HOY"; SJF="$(d '-3 days')"; ENT="$(d '+1 day')";
           else DIAS="$HOY"; SJF=""; ENT="$(d '+1 day')"; fi ;;
  dof)     DIAS="$HOY $*"; SJF=""; ENT="$HOY" ;;
  *) echo "modo desconocido: $MODO" >&2; exit 2 ;;
esac
DEST="fuentes/$ENT"; mkdir -p "$DEST"
echo "== $MODO entrega $ENT | DOF: ${DIAS:-ninguno} | SJF: ${SJF:-ninguno}"
bash bin/arranque.sh
if [ -n "$DIAS" ]; then
  python3 bin/dof_fuentes.py "$DEST/dof" $DIAS
  python3 bin/paginas.py "$DEST/dof"
  python3 bin/ocr.py "$DEST/dof"
fi
if [ -n "$SJF" ]; then
  node bin/sjf_fuentes.mjs "$DEST/sjf" "$SJF"
fi
python3 bin/manifiesto.py "$DEST"
echo "== listo: $DEST"
