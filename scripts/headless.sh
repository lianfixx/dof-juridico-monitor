#!/usr/bin/env bash
# Ejecución sin interfaz de la skill dof-castorena con `claude -p`.
#
# Uso:   scripts/headless.sh martes|jueves|viernes
#        DRY_RUN=1 scripts/headless.sh martes   # muestra el comando sin ejecutarlo
#
# NO SE ACTIVA AL INSTALAR. Este archivo solo documenta y ejecuta una corrida cuando
# alguien lo llama. Para programarlo (zona America/Mexico_City):
#   - Tarea programada de Claude Code que llame a este script con el día.
#   - cron, por ejemplo:
#       CRON_TZ=America/Mexico_City
#       0 6 * * 2  /ruta/al/repo/scripts/headless.sh martes
#       0 6 * * 4  /ruta/al/repo/scripts/headless.sh jueves
#       0 15 * * 5 /ruta/al/repo/scripts/headless.sh viernes
#   - El workflow .github/workflows/tests.yml solo corre pytest; no usarlo para esta
#     tarea: requeriría credenciales de Gmail y material privado en un repo público.
#
# El prompt sigue SKILL.md. El único destinatario permitido es la cuenta de Emi;
# el hook del repositorio bloquea cualquier otro destinatario y la propia skill
# lo prohíbe. El viernes no tiene herramientas de Gmail.
#
# Los nombres de las herramientas de Gmail dependen de cómo esté conectado el
# conector; ajustar GMAIL_TOOLS a lo que muestre /mcp en tu instalación.
set -euo pipefail

DIA="${1:-}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

FECHA="$(TZ=America/Mexico_City date +%F)"
LOG_DIR="outputs/headless"   # outputs/ está en .gitignore

# Herramientas mínimas. dontAsk rechaza todo lo que no esté en esta lista
# (sin git, sin curl, sin borrar archivos). python3 se necesita para los
# controles de src/dof_monitor y para generar/renderizar PDF y DOCX.
BASE_TOOLS="Read,Glob,Grep,Write,Edit,WebFetch,Bash(python3:*)"
GMAIL_TOOLS="${GMAIL_TOOLS:-mcp__Gmail__search_threads,mcp__Gmail__get_message,mcp__Gmail__send_message}"

COMUN="Sigue SKILL.md de este repositorio y la referencia que indique para el día. Es una ejecución programada: no hagas entrevista inicial. Cumple docs/QUALITY_GATE.md. Registra la hora real de última consulta. Nunca escribas al Licenciado ni a terceros. Si cualquier tramo queda sin lectura íntegra, deja bloqueo PARCIAL explícito con los faltantes exactos y no presentes ni envíes nada como final."

case "$DIA" in
  martes)
    TOOLS="$BASE_TOOLS,$GMAIL_TOOLS"
    PROMPT="Entrega del martes $FECHA: DOF del viernes anterior, lunes y martes, más la síntesis SJF del último viernes efectivamente publicado. Lee íntegra references/sjf-y-distribucion.md. $COMUN Solo con DOF y SJF auditados por separado, envía un único correo a emilianogarciamilla@gmail.com, sin CC/CCO, con exactamente cuatro archivos conjuntos, tras buscar duplicados en Enviados; después verifica el estado del envío."
    ;;
  jueves)
    TOOLS="$BASE_TOOLS,$GMAIL_TOOLS"
    PROMPT="Entrega del jueves $FECHA: exclusivamente DOF (miércoles, jueves y pendientes o correcciones DOF desde el corte anterior), sin ninguna sección ni corrección SJF. Lee íntegra references/sjf-y-distribucion.md. $COMUN Solo con auditoría DOF completa, envía un único correo a emilianogarciamilla@gmail.com, sin CC/CCO, con los cuatro archivos DOF, tras buscar duplicados en Enviados; después verifica el estado del envío."
    ;;
  viernes)
    TOOLS="$BASE_TOOLS"
    PROMPT="Revisión SJF interna del viernes $FECHA. Lee íntegra references/sjf-y-distribucion.md. $COMUN Inventaría y lee todo lo publicado, distingue jurisprudencia, tesis aisladas y votos, y persiste control y paquete en privado/ para el martes. No envíes correo."
    ;;
  *)
    echo "Uso: $0 martes|jueves|viernes" >&2
    exit 2
    ;;
esac

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  printf 'claude -p "%s" --permission-mode dontAsk --allowedTools "%s"\n' "$PROMPT" "$TOOLS"
  exit 0
fi

command -v claude >/dev/null || { echo "No se encontró el comando claude" >&2; exit 127; }
mkdir -p "$LOG_DIR"

claude -p "$PROMPT" \
  --permission-mode dontAsk \
  --allowedTools "$TOOLS" \
  > "$LOG_DIR/${FECHA}_${DIA}.log" 2>&1
