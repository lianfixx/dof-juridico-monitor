# Paquete de entrega

Genera los cuatro archivos y el correo HTML a partir de `content.js` y `guia.js` (esquema en `content.ejemplo.js`).

```
NODE_PATH=/ruta/node_modules node scripts/paquete/build.js DIR_CONTENIDO DIR_SALIDA   # DOCX del reporte y de la guía
node scripts/paquete/email.js DIR_CONTENIDO DIR_SALIDA                                 # Correo_revision_*.html
soffice --headless --convert-to pdf DIR_SALIDA/*.docx --outdir DIR_SALIDA             # PDF
python3 scripts/paquete/audit.py DIR_CONTENIDO/evidencias.json                          # auditoría literal (100 % o no sale)
```

Requiere `docx` (npm) y LibreOffice. Los nombres salen `Actualizacion_DOF_SJF_<sufijo>` los martes y `Actualizacion_DOF_<sufijo>` los jueves (sin sección SJF cuando `C.sjf` está vacío). Comprobar siempre: comentario 40–70 palabras, correo al Licenciado 80–130, sin leyendas visibles, y revisar el PDF renderizado.
