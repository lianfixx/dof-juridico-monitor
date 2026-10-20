# SJF semanal: flujo operable con archivos del usuario

## Qué puede hacer el sistema ahora

Este repositorio ofrece un flujo **asistido y auditable**, no un lector automático capaz de certificar lectura jurídica. El agente debe verificar el índice oficial completo y cada documento antes de valorar relevancia. Si la fuente oficial no permite descargar un archivo, pedir al usuario que lo descargue y adjunte; no sustituirlo por snippets.

**Fuentes oficiales para localizar y descargar:** [Buscador SJF](https://sjf2.scjn.gob.mx/) y [Gaceta SCJN](https://www.scjn.gob.mx/coordinacion/gaceta). Son portales de acceso, **no enlaces inventados a un PDF específico**. Elegir en el sitio la publicación real del viernes y guardar todos los documentos, anexos, votos, sentencias y paginaciones que correspondan. Para el 16-10-2026 no afirmar que la edición esté completa sin cotejar su índice real.

## Operación paso a paso

1. El viernes, identificar fecha efectiva, secciones y total de documentos mediante fuentes oficiales. Registrar fecha de publicación y corte.
2. Descargar los PDF oficiales, o pedir al usuario que adjunte los faltantes; mantener lista exacta de documentos/rangos pendientes. No guardar PDFs con datos sensibles en este repositorio público.
3. Crear un control privado local: `python -m src.dof_monitor.sjf_intake init --date 2026-10-16 --out ./privado/SJF_2026-10-16`.
4. Por cada PDF descargado, ejecutar `python -m src.dof_monitor.sjf_intake add --control ./privado/SJF_2026-10-16/SJF_2026-10-16_Control.json --file /ruta/archivo.pdf --url https://URL-OFICIAL-DEL-DOCUMENTO`. La URL debe ser la dirección oficial real, no el ejemplo. El sistema calcula SHA-256 e intenta contar páginas; el registro permanece PENDIENTE.
5. Leer visualmente todas las páginas y anexos. Tras revisar cada documento, completar manualmente en el JSON `read_ranges`, `reading_notes`, `annexes`, `annexes_verified`, `legal_checks` y `status`. No marcar verdadero un control que no se verificó. Identificar cada documento y vincular tesis, sentencias y votos.
6. Sólo después de conciliar índice, totales y paginaciones, establecer `edition_verified`, `inventory_reconciled` y `universe_closed` según evidencia. Realizar investigación y revisión crítica de obligatoriedad, votaciones, ámbito, excepciones y efectos, contrastando fuentes primarias. Aprobar auditoría sólo con evidencia real.
7. Ejecutar `python -m src.dof_monitor.sjf_intake check --control ./privado/SJF_2026-10-16/SJF_2026-10-16_Control.json`. Si informa PARCIAL, no generar ni enviar un paquete rotulado final.
8. Tras cierre real, crear `SJF_AAAA-MM-DD_Reporte.pdf`, `.docx`, `SJF_AAAA-MM-DD_Guia.pdf` y `.docx`; renderizar, revisar, registrar hashes reales, persistir con `SJF_AAAA-MM-DD_Control.json` en almacenamiento privado accesible al martes.
9. Martes: recuperar los cinco archivos, cotejar identidad/hashes, fecha del viernes, correcciones y auditoría; integrar DOF y SJF en los mismos cuatro adjuntos. Jueves: sólo novedades posteriores verificadas. No presumir que los archivos de otro hilo están accesibles.
10. Antes del único correo a la cuenta personal autorizada: revisar duplicados, intentos previos, archivos y destinatario. Ante respuesta ambigua, bloquear reenvío. No enviar al Licenciado.

## Alcance honesto

El comando comprueba consistencia estructural y hashes de PDF registrados, pero no demuestra que el documento sea oficial, que el universo esté completo, que la lectura se haya realizado o que la interpretación jurídica sea correcta. Los indicadores de revisión son declaraciones que exigen respaldo independiente. Los cuatro archivos y Gmail **no se generan ni envían mediante este comando**. Si el entorno no permite persistencia, entregar los archivos de control al usuario para que los adjunte en la siguiente ejecución.

## Seguridad

La carpeta `privado/` debe mantenerse fuera de Git. No subir a GitHub expedientes, notas confidenciales, PDF de clientes, direcciones de correo adicionales ni credenciales. Los documentos del SJF pueden ser públicos, pero los análisis y controles personales deben permanecer privados.

## Inventario semanal conciliado (mejora de octubre de 2026)

El acceso preferente es el [SJF semanal](https://sjfsemanal.scjn.gob.mx/) y sus secciones de tesis, ejecutorias, votos, acuerdos y demás publicaciones. Consultar también la [Gaceta de la SCJN](https://www.scjn.gob.mx/coordinacion/gaceta): los tomos semanales pueden incluir varios volúmenes y posteriormente formar un libro mensual. El libro mensual es una vía de contraste, no motivo para confundir la fecha de publicación del viernes.

Tras comprobar **todas las páginas y secciones del índice de la edición**, crear un CSV UTF-8 con encabezado exacto `id,section,type,official_url,related_ids`. Cada fila corresponde a una entrada real y su URL oficial exacta. Los identificadores deben ser únicos; `related_ids` permite referencias separadas por punto y coma, siempre que estén respaldadas por la fuente. No copiar sólo los criterios relevantes: el CSV incluye incluso acuerdos, votos, sentencias y documentos secundarios.

Ejemplo **de estructura, no inventario de una edición real**:

```csv
id,section,type,official_url,related_ids
2031846,Pleno jurisprudencia,tesis,https://sjfsemanal.scjn.gob.mx/detalle/tesis/2031846,
```

Importar: `python -m src.dof_monitor.sjf_weekly inventory --control privado/SJF_2026-10-16/SJF_2026-10-16_Control.json --csv inventario_oficial.csv --index-url https://sjfsemanal.scjn.gob.mx/ --evidence "Revisadas todas las secciones y paginaciones del viernes; conservar evidencia en carpeta privada"`.

Obtener enlaces exactos pendientes: `python -m src.dof_monitor.sjf_weekly missing --control privado/SJF_2026-10-16/SJF_2026-10-16_Control.json`. Con ellos, solicitar a Emi únicamente los PDF faltantes. Cuando un documento esté disponible, usar `sjf_intake add --id IDENTIFICADOR --url URL_OFICIAL` con su PDF original. No inventar rutas de descarga ni convertir HTML en PDF oficial.

Revisar consistencia: `python -m src.dof_monitor.sjf_weekly audit --control privado/SJF_2026-10-16/SJF_2026-10-16_Control.json`. Este control combina inventario y evidencias por documento, pero **no demuestra que el índice se haya transcrito completo ni que los campos declarados sean ciertos**. La conciliación humana con el índice oficial sigue siendo indispensable. No cerrar ni enviar con cualquier discrepancia.

La tarea del viernes debe guardar el CSV, PDF originales y JSON en un destino privado persistente; la del martes debe recuperar esos mismos bytes, cotejar hashes y verificar correcciones. Si no existe acceso a archivos entre tareas, pedir al usuario los archivos de control y originales y mantener SJF PENDIENTE hasta recuperarlos. Nunca almacenar este paquete en el repositorio público.

### Limitación comprobada del portal y alternativa

En una prueba de acceso automatizado del 20-10-2026, la portada del SJF semanal y su búsqueda de tesis devolvieron únicamente el aviso «Su navegador esta desactualizado para este sitio». Eso **no demuestra que el Semanario no tenga publicaciones**; demuestra que esa vía de extracción no permite cerrar el inventario. No fabricar resultados ni marcar el viernes como vacío. Usar un navegador compatible, otra ruta oficial efectivamente comprobada o los PDF oficiales adjuntos por Emi; verificar manualmente el índice completo antes de marcar `inventory_reconciled`.

Para contar páginas en la CLI local instalar la dependencia opcional: `pip install '.[pdf]'`. Sin `pypdf` el conteo permanece `null` y bloquea el cierre hasta verificación posterior. Nunca modificar manualmente el conteo sin cotejo del PDF real.

### Ruta oficial alternativa comprobada: Gaceta de octubre de 2026

La página de [Gaceta SCJN](https://www.scjn.gob.mx/coordinacion/gaceta) muestra «Octubre libro 14» y enlaza a [PDF completo oficial de octubre de 2026](https://www.scjn.gob.mx/coordinacion/sites/default/files/gaceta/documents/2026/14_oct_completo.pdf). En consulta automatizada el enlace se identificó, pero la lectura directa excedió el límite de tamaño de la herramienta (aproximadamente 13.6 MB). Esto no autoriza declarar el libro leído ni permite inferir que el contenido de un viernes particular está completo. El operador puede descargarlo desde el navegador, adjuntarlo y cotejar sus tomos, volúmenes y fechas con el índice semanal. Registrar por separado el rango realmente leído de cada viernes.

## Generación controlada de los cuatro archivos

Instalar `pip install '.[pdf,artifacts]'`. Sólo cuando el índice, las lecturas, anexos, investigación jurídica y auditoría hayan sido efectivamente comprobados, preparar un JSON editorial privado. Debe contener `summary`, `items` (cada elemento con `title`, `effect`, `status`, `importance`, `study`, `source_url` oficial), `suggested_comment` (40–70 palabras) y `draft_email` (80–130 palabras, incluyendo el espacio literal de opinión personal). Nunca usar los datos de pruebas como hallazgos reales.

Ejecutar `python -m src.dof_monitor.sjf_artifacts --control privado/SJF_2026-10-16/SJF_2026-10-16_Control.json --editorial editorial_verificado.json --out privado/SJF_2026-10-16/salida`. El generador bloquea cualquier control incompleto, produce PDF/DOCX del reporte y PDF/DOCX de la guía, calcula hashes y deja `render_checked: false` y estado `READY_FOR_VISUAL_REVIEW`. **No equivale a un paquete final ni envía Gmail.** La revisión humana debe renderizar e inspeccionar los cuatro archivos, cotejar enlaces y contenido y registrar aprobación expresa. La guía requiere contenido sustantivo redactado en `study` para cada tema; el programa no inventa análisis ni fuentes.

En la integración del martes no enviar ocho archivos: preparar el único conjunto DOF+SJF, preservando las fechas originales y la cobertura independiente. El generador SJF sirve para el viernes y como fuente editable de integración, no sustituye el generador DOF. Si falta evidencia o persiste bloqueo, conservar PARCIAL y no enviar.
