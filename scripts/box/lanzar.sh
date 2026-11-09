#!/usr/bin/env bash
# Lanza fuentes.sh en segundo plano dentro del box y regresa de inmediato.
# Cada llamada al shell del box tiene un tope de 600 s y, si se rebasa, la sesión se
# reinicia; un martes con OCR puede tardar más. Un proceso lanzado con setsid sobrevive a
# ese reinicio (comprobado el 9/11/2026).
#
#   lanzar.sh MODO [FECHA] [más argumentos de fuentes.sh]   -> imprime la entrega y el log
#   bin/estado.sh ENTREGA                                    -> consulta el avance
#
# Si ya hay una corrida de la misma entrega en curso, no lanza otra.
set -euo pipefail
cd /workspace/dof
export TZ=America/Mexico_City
MODO="${1:?modo}"
HOY="${2:-$(date +%F)}"
case "$MODO" in
  viernes) ENT="sjf-$HOY" ;;
  noche)   ENT="$(date -d "$HOY +1 day" +%F)" ;;
  *)       ENT="$HOY" ;;
esac
mkdir -p "fuentes/$ENT"
LOG="fuentes/$ENT/fuentes.log"
PIDF="fuentes/$ENT/fuentes.pid"
if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then
  echo "ya en curso: entrega $ENT (pid $(cat "$PIDF")); consulta con: bash bin/estado.sh $ENT"; exit 0
fi
shift || true
[ $# -gt 0 ] && shift || true
setsid nohup bash bin/fuentes.sh "$MODO" "$HOY" "$@" >>"$LOG" 2>&1 < /dev/null &
echo $! > "$PIDF"
echo "lanzado: modo $MODO, entrega $ENT, pid $(cat "$PIDF"), log $LOG"
echo "consulta con: bash bin/estado.sh $ENT"
