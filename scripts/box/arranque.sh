#!/usr/bin/env bash
# Deja el box listo para dof-castorena. Idempotente: solo instala lo que falte.
# El disco de sistema del box se reinicia; /workspace y $HOME persisten en las instantáneas.
set -euo pipefail
cd /workspace/dof
# Scripts que deben estar en bin/ (copias canónicas en scripts/box/ del repositorio).
faltan=()
for s in arranque.sh fuentes.sh lanzar.sh estado.sh dof_fuentes.py paginas.py ocr.py manifiesto.py sjf_fuentes.mjs; do
  [ -f "bin/$s" ] || faltan+=("$s")
done
if ((${#faltan[@]})); then
  echo "FALTAN en /workspace/dof/bin: ${faltan[*]} — escríbelos desde scripts/box/ del repositorio" >&2; exit 1
fi
need_apt=()
command -v pdftotext >/dev/null || need_apt+=(poppler-utils)
command -v pdfimages >/dev/null || need_apt+=(poppler-utils)
command -v qpdf >/dev/null || need_apt+=(qpdf)
command -v nc >/dev/null || need_apt+=(netcat-openbsd)
tesseract --list-langs 2>/dev/null | grep -qx spa || need_apt+=(tesseract-ocr-spa)
if ((${#need_apt[@]})); then
  mapfile -t need_apt < <(printf '%s\n' "${need_apt[@]}" | sort -u)
  echo "instalando: ${need_apt[*]}"
  if ! sudo -n apt-get install -y -qq "${need_apt[@]}" >/tmp/arranque-apt.log 2>&1; then
    # Tras un reinicio del disco de sistema la lista de paquetes puede venir vacía.
    sudo -n apt-get update -qq >>/tmp/arranque-apt.log 2>&1 || true
    sudo -n apt-get install -y -qq "${need_apt[@]}" >>/tmp/arranque-apt.log 2>&1 || { tail -5 /tmp/arranque-apt.log; exit 1; }
  fi
fi
[ -d node_modules/puppeteer-core ] && [ -d node_modules/docx ] || { [ -f package.json ] || npm init -y >/dev/null; npm install --silent puppeteer-core@24 docx@9 >/tmp/arranque-npm.log 2>&1; }
[ -x /usr/bin/google-chrome ] || echo "AVISO: no está /usr/bin/google-chrome; el SJF por el box no funcionará (usa la vía B o C)" >&2
mkdir -p fuentes entregas
echo "box listo: $(tesseract --version 2>&1 | head -1) | $(pdftotext -v 2>&1 | head -1) | node $(node -v) | chrome $(google-chrome --version 2>/dev/null)"
