# Paquete de entrega

Genera los cuatro archivos y el correo HTML a partir de `content.js` y `guia.js` (esquema en `content.ejemplo.js`).

```
NODE_PATH=/ruta/node_modules node scripts/paquete/build.js DIR_CONTENIDO DIR_SALIDA   # DOCX del reporte y de la guía
node scripts/paquete/email.js DIR_CONTENIDO DIR_SALIDA                                 # Correo_revision_*.html
soffice --headless --convert-to pdf DIR_SALIDA/*.docx --outdir DIR_SALIDA             # PDF
python3 scripts/paquete/audit.py DIR_CONTENIDO/evidencias.json                          # auditoría literal (100 % o no sale)
node scripts/paquete/estilo.js DIR_CONTENIDO                                           # forma: medidas, comillas, dos puntos, muletillas, apartados de la guía (sin errores o no sale)
```

Requiere `docx` (npm) y LibreOffice. Los nombres salen `Actualizacion_DOF_SJF_<sufijo>` los martes y `Actualizacion_DOF_<sufijo>` los jueves (sin filas del Semanario cuando `C.sjf` está vacío). El reporte lleva una sola tabla bajo «Lo relevante», sin párrafos de resumen (versión final de Emi del 24/11/2026). Comprobar siempre: comentario 40–70 palabras, correo al Licenciado 120–230, sin leyendas visibles, y revisar el PDF renderizado.
