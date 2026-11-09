#!/usr/bin/env bash
# Deja el box listo para dof-castorena. Idempotente: solo instala lo que falte.
# El disco de sistema del box se reinicia; /workspace y $HOME persisten en las instantáneas.
set -euo pipefail
cd /workspace/dof
need_apt=()
command -v pdftotext >/dev/null || need_apt+=(poppler-utils)
command -v qpdf >/dev/null || need_apt+=(qpdf)
command -v nc >/dev/null || need_apt+=(netcat-openbsd)
tesseract --list-langs 2>/dev/null | grep -qx spa || need_apt+=(tesseract-ocr-spa)
if ((${#need_apt[@]})); then
  echo "instalando: ${need_apt[*]}"
  sudo -n apt-get install -y -qq "${need_apt[@]}" >/tmp/arranque-apt.log 2>&1 || { tail -5 /tmp/arranque-apt.log; exit 1; }
fi
[ -d node_modules/puppeteer-core ] && [ -d node_modules/docx ] || { [ -f package.json ] || npm init -y >/dev/null; npm install --silent puppeteer-core@24 docx@9 >/tmp/arranque-npm.log 2>&1; }
mkdir -p fuentes entregas
echo "box listo: $(tesseract --version 2>&1 | head -1) | $(pdftotext -v 2>&1 | head -1) | node $(node -v) | chrome $(google-chrome --version 2>/dev/null)"
