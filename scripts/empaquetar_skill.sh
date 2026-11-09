#!/usr/bin/env sh
# Genera el ZIP de la skill dof-castorena para subirlo a claude.ai (Ajustes → Skills).
# claude.ai exige exactamente un SKILL.md en el ZIP; el repositorio trae además los puentes
# .claude/skills/ y .agents/skills/ (para Claude Code y Codex), que lo hacían rechazar
# («Zip must contain exactly one SKILL.md file. Currently there are 3.», 9/11/2026).
#
# Uso: sh scripts/empaquetar_skill.sh [SALIDA.zip]
# Por defecto escribe dist/dof-castorena-<versión>.zip. Deja fuera .git, .github, .claude,
# .agents, dist y cachés; comprueba que haya un solo SKILL.md y que la versión cuadre.
set -eu
cd "$(dirname "$0")/.."
VER=$(sed -n 's/^  version: "\(.*\)"/\1/p' SKILL.md | head -1)
[ -n "$VER" ] || { echo "no encontré la versión en SKILL.md" >&2; exit 1; }
OUT="${1:-dist/dof-castorena-$VER.zip}"
mkdir -p "$(dirname "$OUT")"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/dof-castorena"
git ls-files | grep -v -E '^(\.git|\.github|\.claude|\.agents|dist)/' | while IFS= read -r f; do
  mkdir -p "$TMP/dof-castorena/$(dirname "$f")"
  cp "$f" "$TMP/dof-castorena/$f"
done
N=$(find "$TMP/dof-castorena" -name SKILL.md | wc -l | tr -d ' ')
[ "$N" = 1 ] || { echo "el ZIP tendría $N SKILL.md; debe tener 1" >&2; exit 1; }
rm -f "$OUT"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
(cd "$TMP" && zip -qr "$OUT_ABS" dof-castorena)
echo "listo: $OUT (skill $VER, $(unzip -l "$OUT" | tail -1 | awk '{print $2}') archivos, un solo SKILL.md)"
