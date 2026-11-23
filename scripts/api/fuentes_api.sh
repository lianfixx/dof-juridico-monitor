#!/usr/bin/env bash
# Fuentes del DOF para el lector por API, fuera del box (por ejemplo, un servidor de GitHub).
#   fuentes_api.sh RAIZ noche [FECHA]     lo ya publicado del periodo que cierra mañana (lunes o miércoles)
#   fuentes_api.sh RAIZ dof FECHA...      fechas sueltas, en la entrega FECHA (la primera)
# RAIZ = carpeta de trabajo privada; deja todo en RAIZ/fuentes/<entrega>/dof. FECHA = AAAA-MM-DD.
#
# Usa los mismos scripts del box (scripts/box/dof_fuentes.py, paginas.py y ocr.py) con el mismo
# periodo «desde el corte anterior» de fuentes.sh. Diferencias con el box, a propósito:
#   - No baja el Semanario: su portal no responde a servidores de centros de datos (comprobado el
#     23/11/2026) y no hay vía oficial para programas. El Semanario sigue en el box.
#   - No conoce `no_entregadas.json` del box ni las entregas de los cierres: el inventario que manda
#     es el del box. Este solo alimenta al lector por API, cuyo trabajo verifica la sesión que cierra.
# Imprime la carpeta de la entrega en la última línea. Termina con 1 si dof_fuentes.py tuvo errores.
set -uo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/../box" && pwd)"
RAIZ="${1:?raíz de trabajo}"; MODO="${2:?modo}"; shift 2
export TZ=America/Mexico_City
HOY="${1:-$(date +%F)}"
d() { date -d "$HOY $1" +%F; }
dow=$(date -d "$HOY" +%u)
CORTE=""
case "$MODO" in
  noche) if [ "$dow" = 1 ]; then CORTE="$(d '-4 days')"; DIAS="$(d '-3 days') $(d '-2 days') $(d '-1 day') $HOY"; ENT="$(d '+1 day')";
         elif [ "$dow" = 3 ]; then CORTE="$(d '-1 day')"; DIAS="$HOY"; ENT="$(d '+1 day')";
         else echo "noche solo corre lunes o miércoles (hoy $HOY es día $dow)" >&2; exit 2; fi ;;
  dof)   DIAS="$*"; ENT="$HOY" ;;
  *) echo "modo desconocido: $MODO" >&2; exit 2 ;;
esac
DEST="$RAIZ/fuentes/$ENT"; mkdir -p "$DEST/dof"
echo "== $MODO entrega $ENT | corte anterior: ${CORTE:-n/a} | DOF: $DIAS | $(date +%FT%T%z)" >&2
rc=0
if [ -n "$CORTE" ]; then python3 "$AQUI/dof_fuentes.py" "$DEST/dof" --corte "$CORTE" $DIAS >&2 || rc=1
else python3 "$AQUI/dof_fuentes.py" "$DEST/dof" $DIAS >&2 || rc=1; fi
python3 "$AQUI/paginas.py" "$DEST/dof" > /dev/null || rc=1
python3 "$AQUI/ocr.py" "$DEST/dof" >&2 || rc=1
echo "$DEST"
exit $rc
