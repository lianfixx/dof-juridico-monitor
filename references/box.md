# Fuentes con el box y ejecución automática

Complemento operativo de [SKILL.md](../SKILL.md), vigente desde la skill 1.2.0 (8 de noviembre de 2026). No cambia el método jurídico, la lectura íntegra, las compuertas ni el destinatario único: cambia **de dónde salen las fuentes** y **quién hace cada parte**. Probado el 8 de noviembre de 2026 contra el periodo del 3 de noviembre: mismas 544 páginas del DOF (ediciones 297 a 300), los mismos 4 anexos aparte y el mismo Semanario del 30 de octubre (31 tesis, 16 ejecutorias, 4 votos, 26 anexos con SHA-256 idéntico al paquete entregado a mano).

## Reparto de papeles

| Pieza | Hace | No hace |
|---|---|---|
| **Box «main» de Simular** (Ubuntu 24.04, 2 vCPU, siempre despierta en 1 s; conector `box` en Claude) | Inventario oficial del DOF, descarga de PDFs y anexos, API del SJF con Chrome real, OCR en español, almacén persistente de fuentes, notas y entregas (`/workspace/dof`) | Leer ni razonar (no tiene modelo). Su disco de sistema se reinicia: `arranque.sh` reinstala lo que falte |
| **Sesión de Claude en la nube** | Orquesta, lee íntegro con lectores en paralelo que leen **directo del box**, redacta, audita, arma DOCX/PDF/HTML, envía el correo a Emi | Abrir dof.gob.mx ni sjf2.scjn.gob.mx (bloqueados por su lista de salida) |
| **TinyFish** | Cotejo de títulos de notas en paralelo (`fetch_content`, hasta 10 URLs); vigilancia de vespertinas y extraordinarias (`create_monitor`); navegador de reserva para el SJF | PDFs escaneados ni archivos binarios |
| **Mac de Emi** (chat vinculado) | Copia de los entregables en `~/Downloads/DOF Castorena/AAAA-MM-DD/`; último recurso para SJF y OCR (panel del navegador) | Nada de la ejecución normal: no se depende de que esté encendida |
| **GitHub `lianfixx/dof-juridico-monitor`** (público) | Skill, scripts (`scripts/box/`), registro de cambios | Fuentes, notas ni entregas: material de trabajo, nunca en un repositorio público |
| **Gmail / Drive de Emi** | Un correo a `emilianogarciamilla@gmail.com` con los cuatro adjuntos; copia de respaldo en Drive | Nunca al Licenciado ni a terceros |

## El box: carpeta `/workspace/dof`

```
bin/arranque.sh      comprueba que estén los scripts e instala si faltan poppler, qpdf, tesseract-ocr-spa, netcat, puppeteer-core, docx (idempotente, < 1 min)
bin/lanzar.sh        lanza fuentes.sh en segundo plano y regresa de inmediato (cada llamada al shell del box tiene tope de 600 s)
bin/estado.sh        avance de la corrida: estado.json, proceso vivo y final del log (código 3 = sigue en curso)
bin/fuentes.sh       orquestador por día: martes | jueves | viernes | noche | dof FECHA...; no se detiene en el primer fallo
bin/dof_fuentes.py   índice oficial por fecha → ediciones → PDF completo → verificación → texto → páginas que requieren OCR → anexos aparte
bin/paginas.py       índice de líneas por página (<archivo>.paginas.json) para leer por tramos exactos
bin/ocr.py           Tesseract 'spa' (2 procesos) de las páginas de `paginas_ocr` y de los anexos en imagen del DOF y del SJF (<archivo>.ocr.txt, reanudable)
bin/manifiesto.py    manifiesto.json con SHA-256 de todo, resumen DOF y SJF y `compuerta_fuentes` (listo / faltantes)
bin/sjf_fuentes.mjs  Semanario del viernes: tesis, ejecutorias, votos, acuerdos, detalle, anexos PDF, control.json (con `errores`)
fuentes/<entrega>/   dof/raw, dof/anexos, dof/inventario.json, sjf/raw, sjf/txt, sjf/pdf, sjf/control.json, manifiesto.json, estado.json, fuentes.log, notas/
entregas/<fecha>/    los cuatro archivos, el correo HTML, la bitácora y el control SJF de cada entrega
```

El paquete (cuatro archivos y correo HTML) se arma en la sesión con [scripts/paquete/](../scripts/paquete/README.md) a partir de `content.js` y `guia.js`. Las copias canónicas de los scripts del box están en [scripts/box/](../scripts/box/) de este repositorio; si el box las pierde, se vuelven a escribir desde ahí con `write_file`.

### Hechos comprobados sobre los portales (8/11/2026)
- `https://dof.gob.mx/index.php?year=A&month=M&day=D` muestra **la última edición del día** (si hubo vespertina, muestra la vespertina) y ofrece enlaces `edicion=MAT|VES|EXT` a las demás; un enlace vacío responde «No hay datos para la fecha seleccionada». Un día sin publicación responde lo mismo en la página principal.
- El PDF completo se pide por `nota_to_pdf.php?fecha=DD/MM/AAAA&edicion=XXX`, que redirige al nombre oficial (`abrirPDF.php?archivo=DDMMAAAA-XXX.pdf&anio=AAAA&repo=`). Nunca se construye el nombre a mano.
- La primera página del PDF trae «No. de publicación: N/AAAA» y el pie «Esta edición consta de N páginas»; ambos se verifican contra `pdfinfo`.
- Anexos publicados aparte: el texto del DOF los cita como `www.dof.gob.mx/AAAA/...pdf`; se descargan de `dof.gob.mx` **sin `www`** (el certificado del `www` no coincide con el nombre).
- `sjf2.scjn.gob.mx` rechaza clientes sin navegador (Incapsula). Con Chrome headless del box, la API pública que usa la propia aplicación responde: listas por tipo (Duodécima Época), detalle `.../{tipo}/{ius}?isSemanal=true`, anexos `.../file/{ius}?isSemanal=1` y PDF `/api/pdf?path=SJFSem/anexos/{archivo}`. Las listas incluyen semanas anteriores: se filtra por `fechaPublicacion`.
- Tiempos medidos: periodo completo de un martes (4 ediciones, 544 pp., 4 anexos) en 23–70 s; Semanario de una semana en ~60 s; OCR 7–10 s por página densa (1–2 s las casi vacías), dos páginas a la vez.
- `nota_to_pdf.php` puede responder sin la redirección y acertar minutos después (05/11/2026 MAT, 9/11/2026): `dof_fuentes.py` reintenta con esperas de 10, 30, 60 y 120 s antes de anotar el error.
- Hay páginas con texto que llevan además una imagen grande con contenido propio: en la matutina del 06/11/2026, 30 páginas de formatos del SAT tenían de 126 a 331 caracteres de texto y el formato completo en imagen (la página 10: 9 renglones de texto, 45 en la imagen). Por eso el OCR cubre `paginas_ocr` = páginas sin texto ∪ páginas con una imagen de al menos 300×100 px (`pdfimages -list`), no solo las páginas sin texto.

### Periodo y corte anterior
Cada entrega empieza en el día del cierre anterior para recoger sus vespertinas y extraordinarias tardías: martes = jueves anterior (solo tardías) a martes; jueves = martes (solo tardías) a jueves; el lector nocturno usa el mismo corte. En ese día, lo que el cierre anterior ya cubrió se descarga solo para probar la continuidad de números y queda `ya_reportada: true` en el inventario: lo que esté en el inventario de una entrega anterior del box y, si esa entrega no está en el box, la matutina de ese día. Las ediciones `ya_reportada` no se leen, no pasan por OCR ni se reportan. Así la compuerta 1 comprueba números consecutivos desde la última edición ya reportada sin depender de la memoria de la sesión. Si un cierre termina PARCIAL, su bitácora debe decir qué edición no entró al paquete: la entrega siguiente la tomará por reportada. Para corregirlo, o cuando no consta que un cierre se haya entregado, Emi registra esas ediciones en `/workspace/dof/fuentes/no_entregadas.json` (`fecha`, `edicion`, `numero`, `nota_correo`, `decidido`; al reportarlas, `reportada_en`): nunca se marcan `ya_reportada`, su fecha entra al periodo, el manifiesto las lista en `dof.no_entregadas_incluidas` y el cierre pone su `nota_correo` en el correo al Licenciado (ver [ADR 0005](../docs/adr/0005-corte-anterior-y-fuentes-en-segundo-plano.md)).

### Correr en segundo plano
Cada llamada a `mcp__box__shell` tiene un tope de 600 s; si se rebasa, la sesión del box se reinicia (los procesos lanzados con `setsid` sobreviven: comprobado el 9/11/2026). Un martes con un anexo grande en imagen rebasa ese tope solo en OCR. Por eso las tareas usan `bash bin/lanzar.sh <modo>` y consultan `bash bin/estado.sh <entrega>` con llamadas cortas. Un segundo `lanzar.sh` de la misma entrega mientras la primera corre no lanza otra. Todo es reanudable: volver a lanzar solo baja y reconoce lo que falta.

### `compuerta_fuentes` del manifiesto
`listo: true` solo si no hay huecos de numeración, las páginas reales coinciden con las declaradas, no hay errores de descarga (DOF, anexos, SJF), no queda OCR pendiente y hay una edición de referencia del corte anterior; si no, `faltantes` dice exactamente qué falta. Es la primera prueba de la compuerta 1; no la sustituye (la lectura completa y la doble lectura siguen siendo de la sesión).

## Tareas programadas (America/Mexico_City)

| Tarea | Cuándo | Qué hace | Correo |
|---|---|---|---|
| **SJF viernes** | viernes 15:37 | `fuentes.sh viernes`; lectura íntegra de tesis, ejecutorias, votos, acuerdos y anexos; notas y control en el box | No |
| **Lector nocturno** | lunes y miércoles 21:41 | `lanzar.sh noche`: ediciones ya publicadas del periodo que cierra al día siguiente desde el corte anterior, anexos, vespertinas y OCR; lectura íntegra por bloques; notas en `fuentes/<entrega>/notas/` | No |
| **Cierre martes** | martes 05:50 | `lanzar.sh martes` (baja la matutina del día; se relanza cada 15 min hasta las 08:00 si aún no está; recoge vespertinas o extraordinarias tardías desde el corte del jueves); lee lo nuevo; consolida con las notas de la noche y el SJF; compuertas; cuatro archivos; entrega | Sí, a Emi |
| **Cierre jueves** | jueves 06:05 | igual, solo DOF desde el corte del martes (tardías del martes, miércoles y jueves), sin sección SJF | Sí, a Emi |
| **Vigía** | monitor TinyFish «DOF Castorena · vigía», lunes a jueves, cada hora de 13:00 a 20:00 (portada `https://dof.gob.mx/index.php`) | registra si aparece vespertina, extraordinaria o fe de erratas; los cierres lo consultan con `get_monitor` como confirmación (el inventario del box manda) | No |

El texto íntegro de cada tarea programada está en [`prompts/tareas/`](../prompts/tareas/); si se cambia una tarea, se cambia también ese archivo en el mismo commit.

Objetivo: paquete terminado en el correo de Emi alrededor de las 07:30; él revisa y lo reenvía al Licenciado a las 12:00. Un paquete PARCIAL sale a la misma hora con el asunto marcado y los faltantes exactos; nunca se presenta como final.

## Plan A, B y C por paso

| Paso | A | B | C |
|---|---|---|---|
| Inventario de ediciones | Box: índice oficial por fecha y numeración consecutiva | TinyFish `fetch_content` del mismo índice | Panel del navegador de la Mac |
| PDF completo del DOF | Box: `nota_to_pdf.php` → verificación de páginas | TinyFish por notas (texto sin páginas ni imágenes: se marca «sin PDF original») | Mac; si no, [desbloqueo](desbloqueo.md) con enlaces directos |
| Anexos aparte | Box (`dof.gob.mx`, sin `www`) | TinyFish si tienen texto | Mac |
| SJF | Box, Chrome headless | TinyFish `run_web_automation` | Mac (panel), probado el 3/11/2026 |
| OCR | Box, Tesseract `spa` en serie | Contenedor con `spa.traineddata` | tesseract.js en el panel de la Mac |
| Lectura | Lectores en paralelo que leen del box con `read_file` por rangos de `paginas.json` | Bloque sin última línea confirmada: se repite con otro lector | El consolidador lo lee |
| DOCX/PDF | Node `docx` + LibreOffice en la sesión | LibreOffice del box | DOCX y HTML, PDF marcado pendiente |
| Entrega | Archivos en el chat + correo a Emi (adjuntos como referencia `sha256:<hash>:<ruta absoluta>`, sin base64 a mano) + copia en `entregas/` del box | Si Gmail falla: Drive + aviso push | Archivos en el chat + aviso push |
| Copia local | Mac vinculada: `~/Downloads/DOF Castorena/AAAA-MM-DD/` | Drive | — |

Regla: ningún paso se detiene en un aviso. Se agotan A, B y C, la bitácora registra cuál se usó y por qué, y solo entonces se declara PARCIAL con faltantes exactos.

## Compuertas (nada sale si falla una)
1. **Universo cerrado:** números de edición consecutivos desde la última edición ya reportada del corte anterior; cada fecha consultada; páginas reales = declaradas; SHA-256 de cada PDF y anexo en `manifiesto.json`; `compuerta_fuentes.listo` en true o cada faltante resuelto o declarado.
2. **Lectura completa:** cada bloque cita su última línea; publicaciones partidas entre bloques cotejadas de punta a punta; cada página de `paginas_ocr` (sin texto o con imagen grande) revisada también por su OCR, y por la vista de la imagen cuando el OCR dude.
3. **Doble lectura:** cada publicación que entra en la tabla la lee un segundo lector que no vio las notas del primero; se concilian las diferencias por escrito.
4. **Auditoría literal:** cada dato del reporte y la guía (plazos, montos, reglas, votaciones, registros) se encuentra textualmente en la fuente (`tools/audit.py` del paquete, 100 %).
5. **Auditor independiente:** un agente que no vio la redacción la contrasta con la fuente; cada hallazgo se corrige o se refuta por escrito.
6. **Enlaces:** cada nota del DOF se abre y su título coincide (TinyFish en paralelo); cada registro del SJF se abre.
7. **Forma:** comentario 40–70 palabras; correo 80–130; sin leyendas visibles; PDF renderizado y revisado; exactamente cuatro archivos.
8. **Envío:** solo `emilianogarciamilla@gmail.com`, sin CC/CCO; duplicados buscados en Enviados; confirmación de Gmail releída.

## Primer mes
Modo vigilado: Emi revisa cada paquete y anota correcciones; al cierre del mes se ajusta la skill con lo aprendido, con registro en `CHANGELOG.md`.
