#!/usr/bin/env bash
# Avance de una corrida lanzada con bin/lanzar.sh.
#   estado.sh ENTREGA [N]   -> estado.json, si sigue viva y las últimas N líneas del log (15)
# Termina con 0 si la corrida acabó (OK o CON_FALLOS), 3 si sigue en curso.
set -uo pipefail
cd /workspace/dof
ENT="${1:?entrega}"; N="${2:-15}"
D="fuentes/$ENT"
cat "$D/estado.json" 2>/dev/null || echo '{"estado":"SIN_ESTADO"}'
vivo=no
[ -f "$D/fuentes.pid" ] && kill -0 "$(cat "$D/fuentes.pid")" 2>/dev/null && vivo=si
echo "proceso vivo: $vivo"
echo "--- últimas $N líneas de $D/fuentes.log"
tail -n "$N" "$D/fuentes.log" 2>/dev/null
[ "$vivo" = si ] && exit 3
exit 0
