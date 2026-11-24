# Changelog

Formato inspirado en Keep a Changelog. Versionado SemVer.

## [Unreleased]
### 2026-11-23 · corrección: la tarea lanzadora no existe todavía
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, 20:53, en chat: «Audita de fondo y arregla por favor».
- Cambios: la entrada anterior daba por creada la tarea «DOF · lanzar el lector por API». No lo está: al crearla, el control de permisos de la sesión lo negó. `references/api.md`, `references/box.md` y `references/guardia.md` ahora dicen lo que es cierto: el texto está listo en `prompts/api/lanzador-api.md`, la tarea queda pendiente de que Emi la pida, y mientras tanto el lector nocturno lanza el workflow cuando falta. También quedó igualado en el box `sjf_fuentes.mjs` con el del repositorio (difería desde el cambio del proxy configurable; mismos valores por defecto), para que ninguna tarea tenga que reescribirlo a mano.
- Archivos: `references/api.md`, `references/box.md`, `references/guardia.md`, este registro.
- Verificación: `python3 -m pytest -q` 116 aprobadas; los diez scripts de `/workspace/dof/bin` del box tienen el mismo SHA-256 que `scripts/box/`.
- Pendiente: decisión de Emi sobre la lanzadora o la edición del `cron` desde su cuenta.

### 2026-11-23 · auditoría del relevo y de la redacción: cinco correcciones
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, 20:53, en chat: «Audita de fondo y arregla por favor».
- Hallazgos y correcciones: (1) GitHub no disparó ninguna corrida programada el 23/11/2026 en `dof-trabajo`, `Cerebro-Castorena-` ni `INDEP` (cero corridas de tipo `schedule` en los tres; en `MATRIZ`, cuya programación no subió una sesión de Claude, sí corren); causa probable, que GitHub asocia la programación con quien firmó el commit. Corrección que no depende de GitHub: tarea de Claude «DOF · lanzar el lector por API» (lunes y miércoles 19:17, Haiku 5.5; `prompts/api/lanzador-api.md`); el lector nocturno ya la lanzaba si faltaba. (2) La lista del box pasa a la sesión copiada por un modelo: un carácter mal copiado en un SHA-256 habría mandado ese documento a la suscripción sin motivo. Ahora la lista lleva una `huella` y `relevo.py` responde `LISTA_MAL_COPIADA` (código 5) si no coincide. (3) «sin `anulado`» en el texto de los cierres era ambiguo, porque el lector nocturno escribe `anulado: false`; `references/api.md` lo define (solo `true` anula). (4) `templates/operator-study.md`, `templates/report.md` y `docs/sjf/METODO.md` contradecían la redacción nueva; ya remiten a `references/redaccion.md`. (5) `estilo.js` daba un error ilegible si faltaba `content.js`.
- Archivos: `scripts/api/relevo.py`, `scripts/box/relevo_lista.py`, `scripts/paquete/estilo.js`, `tests/test_relevo.py`, `tests/test_sincronia.py`, `prompts/api/lanzador-api.md`, `references/api.md`, `references/box.md`, `references/guardia.md`, `templates/operator-study.md`, `templates/report.md`, `docs/sjf/METODO.md`, este registro.
- Verificación: `python3 -m pytest -q` 116 aprobadas (2 nuevas); `relevo_lista.py` actualizado en el box con el mismo SHA-256 del repositorio; comprobación con los datos reales de la entrega 2026-11-24.
- Pendiente: que Emi confirme la causa de la programación (editar una línea `cron` desde su cuenta) y decida si la lanzadora se queda.

### Skill 1.4.0 — 2026-11-23: redacción del reporte y de la guía, relevo en operación y regla de sincronía
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, 20:20, en chat: «la redacción del reporte debe ser muy natural, humana, fluida y completa […] debe parecer escrito realmente por mí […] que no dé hueva leer, súper fácil de entender, técnico también, argumentado, fundado»; «la guía debe ser muy concisa, completa y de los puntos relevantes, debo entenderlo desde cero, teórico, conceptual, fundado, argumentado, no repetitivo»; «cualquier mejora o cambio debe estar tanto en la API como en la suscripción».
- Diagnóstico (entregas del 10 al 19 de noviembre leídas en el box): celdas de veinte renglones con varias reglas encadenadas con punto y coma; cada cifra entre comillas angulares (la auditoría literal metida en la prosa); títulos de fila que eran inventarios; guía que abría con el control de páginas y cuyos temas eran etiquetas con fragmentos que daban por sabido el concepto.
- Cambios: `references/redaccion.md` nueva y obligatoria (núcleo de nueve reglas; reporte con una fila por asunto y medidas por columna; guía que enseña desde cero con siete apartados fijos; correo y comentario con la voz de Emi; antes y después con una fila real; revisión antes de armar). `scripts/paquete/estilo.js` revisa la forma de `content.js` y `guia.js` (medidas, comillas, dos puntos, punto y coma, muletillas, apartados) y no deja armar con errores. El redactor del lector por API carga el mismo núcleo desde ese archivo. Textos de los cierres con la redacción nueva y el revisor. `tests/test_sincronia.py` vigila que la vía de API y la de suscripción no se separen (núcleo, relevo, scripts del box, apartados). SKILL.md 1.4.0: «Lector por API (en relevo)» y regla de sincronía. `docs/QUALITY_GATE.md`, `references/box.md` y `scripts/paquete/` al día. `references/guardia.md` nueva: procedimiento de la tarea de guardia (corridas, reparación, evaluación en real en lugar de la sombra y comparación del texto de las tareas programadas con `prompts/tareas/`); el texto de esa tarea ahora solo remite al archivo.
- Archivos: `references/redaccion.md`, `scripts/paquete/estilo.js`, `scripts/paquete/README.md`, `scripts/paquete/content.ejemplo.js`, `scripts/api/lector_api.py`, `tests/test_sincronia.py`, `prompts/tareas/cierre-martes.md`, `prompts/tareas/cierre-jueves.md`, `SKILL.md`, `README.md`, `docs/QUALITY_GATE.md`, `references/box.md`, este registro.
- Verificación: `python3 -m pytest -q` 114 aprobadas (6 nuevas); `node scripts/paquete/estilo.js` sobre una fila buena (0 errores) y una mala (6 errores).
- Pendiente: actualizar el texto de las tareas de cierre en Claude; primer paquete con la redacción nueva (martes 24); que Emi lo lea y marque lo que aún no suene a él.

### 2026-11-23 · relevo entre el lector por API y la suscripción (fin de la sombra)
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, 20:20, en chat: «implementa desde esta corrida que viene o la próxima, que si la API no lo hace de manera perfecta, ya entre mi suscripción de Claude (para no hacer lo mismo dos veces), ya ejecutemos todo a la realidad y evaluemos»; «cualquier mejora o cambio debe estar tanto en la API como en la suscripción, ambas deben estar sincronizadas».
- Cambios: `scripts/api/relevo.py` (veredicto determinista TOTAL, PARCIAL o NINGUNO, documento por documento: mismo SHA-256, mismas páginas e íntegro) y `scripts/box/relevo_lista.py` (lista compacta del inventario del box; `arranque.sh` ya lo exige). `lector_api.py` anota en `ESTADO_API.json`, por documento, tipo, páginas, bloques e `integro`. Textos de las tareas: «lector nocturno» con el paso B2 (comprobar, lanzar el lector por API si GitHub no lo corrió, esperar hasta 50 minutos, muestra de control, `RELEVO_API.json` en el box, leer solo lo que quede por suscripción); cierres de martes y jueves con el paso B (notas de la API desde el repositorio privado) y la evaluación en la doble lectura (`lectura_api.diferencias` en la bitácora). `references/api.md` (sección «Relevo con la suscripción» y regla de sincronía), `references/box.md` y ADR 0007. Hallazgo de auditoría: el 23/11/2026 GitHub no disparó la corrida programada de las 19:17; por eso el lector nocturno lanza el workflow cuando falta.
- Archivos: `scripts/api/relevo.py`, `scripts/api/lector_api.py`, `scripts/box/relevo_lista.py`, `scripts/box/arranque.sh`, `tests/test_relevo.py`, `prompts/tareas/lector-nocturno.md`, `prompts/tareas/cierre-martes.md`, `prompts/tareas/cierre-jueves.md`, `references/api.md`, `references/box.md`, `docs/adr/0007-relevo-api-suscripcion.md`, este registro.
- Verificación: `python3 -m pytest -q` 108 aprobadas (9 nuevas).
- Pendiente: actualizar el texto de las tres tareas programadas en Claude con estos archivos; primera noche con relevo y primer cierre con notas de la API.

### Skill 1.3.2 — 2026-11-23: horario 19:17 con reintento, aviso por issue, guardia y comprobación real de las tablas
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: «revisa que esté bien sincronizado, ajustado y programado por si un día falla, entres para arreglar de fondo con Fable alto o medio o con Opus alto dependiendo que esté disponible y si no se puede continúe en mi suscripción»; hacer la comparación de la sombra en automático.
- Cambios: SKILL.md 1.3.2 (sección «Lector por API (en sombra)») y `references/api.md` con el horario nuevo del workflow privado (19:17 y reintento 20:37, en vez de 20:00 en punto), el issue de aviso que se cierra solo y la tarea programada «DOF · guardia del lector por API» (martes y jueves 11:23, Opus 5.5; repara con subagente Fable u Opus; compara la sombra). Comprobación real de las tablas numéricas (corrida 45286205364 del repositorio privado, `releer_tablas=2`): dos bloques de tabla leídos por lote con Haiku 5.5, `INTEGRO`, 0.0056 USD en total, ninguna relectura, síntesis reutilizada.
- Archivos: `SKILL.md`, `README.md`, `references/api.md`, este registro.
- Verificación: `python3 -m pytest -q` 99 aprobadas; corrida citada.
- Pendiente: cuatro comparaciones en sombra; guardar la skill 1.3.2 en Claude (tarjeta enviada a Emi).

### 2026-11-23 · lector por API: `--releer-tablas N` para comprobar el modelo barato sin tocar notas a mano
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: auditar de fondo y dejar todo verificado.
- Cambios: `lector_api.py` acepta `--releer-tablas N`: vuelve a leer N bloques de tabla numérica aunque ya tengan nota. Permite comprobar en real el camino del modelo barato (por lote y con salida estructurada) sin editar a mano `fuentes/` del repositorio privado, que solo escribe el workflow.
- Archivos: `scripts/api/lector_api.py`, `tests/test_lector_api.py`, este registro.
- Verificación: `python3 -m pytest -q` 99 aprobadas (1 nueva).
- Pendiente: corrida de comprobación con dos bloques en el repositorio privado.

### 2026-11-23 · lector por API: las tablas de pura cifra las lee el modelo barato
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: «si de manera segura y sólida observas que no afecta en lo absoluto la mejora que propones, implementa».
- Cambios: `lector_api.py` manda a `--modelo-tablas` (Haiku 5.5) los bloques que el código reconoce como tabla numérica: todas sus páginas con al menos 90 % de dígitos, sin palabras normativas y sin títulos del índice oficial. Auditoría previa con las 1 128 páginas reales de la entrega 2026-11-24: la regla marca los 24 bloques de precios promedio del INPC (0.99 en todas sus páginas) y ninguno más (el siguiente más alto, 0.53; y trae palabras normativas). Doble seguro: una nota con más de dos trozos, con relevancia alta o media, o una falla del modelo barato, hacen que el bloque lo relea el modelo lector. Estimado de lectura de esa entrega, por lote: de 4.34 a 2.99 USD. `ESTADO_API.json` anota `bloques_tabla_numerica` y `tablas_releidas_con_el_lector`.
- Archivos: `scripts/api/lector_api.py`, `tests/test_lector_api.py`, `references/api.md`, `docs/adr/0006-lector-por-api.md`, este registro.
- Verificación: `python3 -m pytest -q` 98 aprobadas (4 nuevas; 5 mutaciones de la regla detectadas).
- Pendiente: comprobación real con dos bloques de tabla en el repositorio privado.

### 2026-11-23 · lector por API: corrida real completa, en sombra desde hoy
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: que la API funcione para el DOF, medir y cuidar los costos.
- Cambios: solo este registro y la medición en `references/api.md`. Corrida 45279097570 del repositorio privado (entrega 2026-11-24): `INTEGRO`, 78 de 78 bloques íntegros y ya leídos (0 USD de lectura), síntesis completa en 5 grupos (18 candidatas, 37 avisos secundarios, 31 enlaces del índice oficial), 0.96 USD. Gasto total del día en el espacio `castorena-dof`: 12.10 USD (9.07 de la primera corrida con llamadas directas, 2.07 y 0.96 de las dos siguientes). Estimado de una entrega de lunes como esta, ya por lote: 4.3 USD de lectura más cerca de 1 USD de síntesis. Se eliminó en Claude Console la llave `dof-github-actions`; el secreto de este repositorio público quedó con una llave muerta y lo borra Emi (GitHub pide su passkey).
- Archivos: `references/api.md`, este registro.
- Verificación: `ESTADO_API.json`, `bitacora/2026-11.md` y `notas/PRELIMINAR_API.md` del repositorio privado.
- Pendiente: cuatro entregas en sombra (24 y 26 de noviembre, 1 y 3 de diciembre) comparadas con la lectura de la suscripción; después, decisión de Emi sobre el relevo. La tarea «lector nocturno» no cambió.

### 2026-11-23 · lector por API: síntesis por grupos y nota mínima para edictos (tras la corrida real de la versión 2)
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: auditar de fondo cada paso y arreglar; cuidar los costos.
- Cambios: la corrida real de la versión 2 (45276910098 del repositorio privado, entrega 2026-11-24) quedó `INTEGRO`: 78 bloques íntegros (69 reutilizados sin costo, 4 por lote, 5 directos tras 3 divisiones), lote terminado en 142 s, 0 títulos del índice sin nota, 2.07 USD. Dejó dos ajustes: (1) la síntesis se cortó por longitud con 138 000 caracteres de notas; ahora el redactor recibe una unidad por publicación, en grupos de 45 000 caracteres, el programa une los resultados en «Candidatas» y «Avisos secundarios» y un grupo cortado se rehace en mitades; (2) las páginas de edictos y convocatorias producían respuestas de hasta 14 000 tokens por seis páginas y cortes; ahora llevan nota mínima cuando su relevancia es baja o ninguna.
- Archivos: `scripts/api/lector_api.py`, `tests/test_lector_api.py`, `references/api.md`, este registro.
- Verificación: `python3 -m pytest -q` 94 aprobadas (3 nuevas). Repetición sobre las notas reales, sin llamar a la API: 5 grupos para el redactor, 78 bloques reutilizados.
- Pendiente: corrida real para confirmar la síntesis completa; cuatro entregas en sombra.

### Skill 1.3.1 — 2026-11-23: lector por API, versión 2 (lo que enseñó la primera corrida real)
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: «cada paso que hagas audita de fondo y arregla sí o sí»; cuidar los costos; que la API funcione perfecto para el DOF.
- Cambios: la primera corrida real (periodo del 20 al 23 de noviembre: 9 documentos, 1 128 páginas, 75 bloques) leyó 71 bloques, costó 9.07 USD y se cayó antes de escribir `ESTADO_API.json` por una nota sin lectura; terminó en rojo, como debe, y la suscripción trabajó normal. `lector_api.py` versión 2: (1) ningún bloque tumba la corrida y el estado se escribe siempre; (2) una respuesta cortada parte el bloque en mitades en vez de repetirse igual, y todo lo cobrado cuenta en el tope; (3) la «última línea» se busca entre las líneas finales (número de página, OCR) y las notas anteriores se revalidan sin nueva llamada; (4) lectura por lote a mitad de precio con plazo de 35 minutos, cancelación y relevo por llamadas directas, sin repetir cuando no se sabe si el lote cobró; (5) el inventario y «por verificar» los arma el código, la síntesis solo redacta candidatas y secundarios y se reutiliza si las notas no cambiaron; (6) los trozos de continuación sin título heredan el código de la publicación abierta; (7) comprobación de que las notas cubren todas las páginas y de bloques con texto sin publicaciones; (8) cada nota guarda su uso y su costo.
- Archivos: `scripts/api/lector_api.py`, `tests/test_lector_api.py`, `references/api.md`, `docs/adr/0006-lector-por-api.md`, `SKILL.md`, `README.md`, este registro.
- Verificación: `python3 -m pytest -q` 91 aprobadas (19 nuevas; siete mutaciones del código detectadas por las pruebas). Repetición sobre los datos reales de la corrida, sin llamar a la API: 69 de 75 bloques íntegros (65 más 4 revalidados), 0 títulos del índice sin nota, 29 códigos heredados, estimado en lote 4.33 USD.
- Pendiente: corrida real de la versión 2; cuatro entregas en sombra; guardar la skill 1.3.1 en Claude.

### Skill 1.3.0 — 2026-11-23: lector previo por la API de Claude (en sombra)
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: «tratemos de utilizar la API para el DOF y que funcione todo perfecto»; que corra antes y que, si un día falla, su suscripción lo haga de manera normal. Autorizó workflows, fusión y el repositorio privado `lianfixx/dof-trabajo`, que él mismo creó.
- Cambios: `scripts/api/lector_api.py` (lector por bloques con comprobación de última línea, citas literales, códigos del índice y cruce con el índice oficial; tope de gasto; reanudable) y `scripts/api/fuentes_api.sh` (mismo periodo del box, sin Semanario). `references/api.md` y ADR 0006. SKILL.md 1.3.0 con la sección «Lector por API (en prueba)». Resultado de la prueba del Semanario desde GitHub: el portal dejó colgada la conexión los 15 minutos del tope y la Corte no ofrece vía oficial para programas; el Semanario sigue en el box. Las tareas programadas, sus textos y el box no cambian.
- Archivos: `scripts/api/lector_api.py`, `scripts/api/fuentes_api.sh`, `tests/test_lector_api.py`, `references/api.md`, `docs/adr/0006-lector-por-api.md`, `SKILL.md`, este registro.
- Verificación: `python3 -m pytest -q` 72 aprobadas (12 nuevas, sin llamadas reales). Primera corrida real, en el repositorio privado.
- Pendiente: cuatro entregas en sombra y decisión de Emi sobre el relevo; guardar la skill 1.3.0 en Claude.

### 2026-11-23 · sjf_fuentes.mjs: el proxy del box pasa a ser configurable
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: llevar el lector nocturno a la API; prueba de factibilidad.
- Cambios: `sjf_fuentes.mjs` tenía fijo el proxy local del box (`127.0.0.1:3128`), que no existe en un servidor de GitHub. Ahora lo toma de `SJF_PROXY` (vacío = salida directa) y Chrome de `SJF_CHROME`; sin esas variables se comporta exactamente igual que antes en el box. La prueba de fuentes corre el Semanario con `SJF_PROXY` vacío y muestra el final del registro.
- Archivos: `scripts/box/sjf_fuentes.mjs`, `.github/workflows/prueba-fuentes.yml`, este registro.
- Verificación: `python3 -m pytest -q` aprobadas; corrida de la prueba después de fusionar.
- Pendiente: el box toma la copia nueva del script en su siguiente arranque (el del repositorio manda).

### 2026-11-23 · prueba de fuentes desde GitHub: el DOF coincide byte por byte; se agrega el Semanario
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: llevar el lector nocturno a la API; prueba de factibilidad.
- Cambios: resultado de la primera corrida: un servidor de GitHub bajó en 50 s el periodo del 3 de noviembre (ediciones 297 a 300, 544 páginas, 4 anexos aparte, 0 errores) y los SHA-256 de los cuatro PDF y de los cuatro anexos son idénticos a los del inventario del box (`fuentes/2026-11-03`). Se agrega al mismo workflow la prueba del Semanario con `sjf_fuentes.mjs` y Chrome.
- Archivos: `.github/workflows/prueba-fuentes.yml`, este registro.
- Verificación: aprobado para el DOF (corrida 23/11/2026); Semanario, en la corrida siguiente.
- Pendiente: repositorio privado para las notas del lector por API (lo crea Emi).

### 2026-11-23 · prueba de fuentes desde un servidor de GitHub
- Agente: claude.ai (sesión en la nube, claude-fable-5-2)
- Solicitud: Emi, 23/11/2026, en chat: llevar el lector nocturno a la API con créditos de Claude; autorizó crear workflows. Primer paso: prueba de factibilidad.
- Cambios: workflow manual `prueba-fuentes.yml`: corre `scripts/box/dof_fuentes.py` y `paginas.py` en un servidor de GitHub sobre las fechas que se le den y deja en el registro solo edición, número, páginas y SHA-256, para cotejar con el manifiesto del box. No guarda nada, no usa llaves, no lee ni redacta. No cambia la skill, las tareas programadas ni el box.
- Archivos: `.github/workflows/prueba-fuentes.yml`, este registro.
- Verificación: corrida manual después de fusionar; resultado en la entrada que siga.
- Pendiente: según el resultado, decidir si las fuentes del lector por API salen de GitHub.

### 2026-11-09 · 301/2026 y 302/2026 también al paquete del martes 10/11
- Agente: Claude Code (sesión en la nube, claude-opus-5-5), a petición de Muse con instrucción de Emi (11:16): tampoco consta la entrega de la matutina 301/2026 y la vespertina 302/2026 del miércoles 4/11; darlas por no entregadas e incluirlas con la 303/2026; una sola nota en el correo al Licenciado para las tres; no enviar nada.
- Cambios: `no_entregadas.json` del box con 301, 302 y 303 y una nota común; `dof_fuentes.py` toma siempre la nota y la decisión vigentes del registro, también para ediciones ya inventariadas; los cierres incluyen cada `nota_correo` distinta una sola vez (tareas programadas actualizadas).
- Archivos: `scripts/box/dof_fuentes.py`, `prompts/tareas/cierre-martes.md`, `prompts/tareas/cierre-jueves.md`, este registro.
- Verificación: `python3 -m pytest -q` 60 aprobadas; entrega 2026-11-10 en el box: 301, 302 y 303 nuevas con `no_entregada_antes` (OCR 11/11, 2/2 y 46/46), 304–306 sin cambios, números 301–306 consecutivos, una sola nota, `compuerta_fuentes.listo` = true → aprobado.
- Pendiente: ninguno para este punto.

### 2026-11-09 · ediciones no entregadas (303/2026 al paquete del martes 10/11)
- Agente: Claude Code (sesión en la nube, claude-opus-5-5), a petición de Muse con instrucción de Emi (11:06): no consta la entrega del cierre del jueves 5/11 (ni en el box ni en Gmail); darlo por no entregado e incluir la matutina 303/2026 en el paquete del martes 10/11; no enviar nada.
- Cambios: registro `/workspace/dof/fuentes/no_entregadas.json` (fuera del repositorio) que `dof_fuentes.py` respeta: esas ediciones nunca se marcan `ya_reportada`, su fecha entra al periodo, se vuelven a procesar si una corrida anterior las había marcado, y dejan de incluirse en cuanto una entrega anterior del box las tiene como nuevas o llevan `reportada_en`. Las demás ediciones de una fecha añadida solo por ellas quedan `ya_reportada`. `manifiesto.py` las lista en `dof.no_entregadas_incluidas` y las acepta como referencia de continuidad. Los cierres de martes y jueves ponen su `nota_correo`, tal cual, en el correo al Licenciado y después anotan `reportada_en`; tareas programadas actualizadas. Documentado en `references/box.md`; 3 pruebas nuevas.
- Archivos: `scripts/box/dof_fuentes.py`, `scripts/box/manifiesto.py`, `prompts/tareas/cierre-martes.md`, `prompts/tareas/cierre-jueves.md`, `references/box.md`, `tests/test_box_scripts.py`, este registro.
- Verificación: `python3 -m pytest -q` 60 aprobadas; en el box, entrega 2026-11-10 relanzada: 303/2026 nueva con `no_entregada_antes`, 46/46 páginas con OCR; 304, 305 y 306 sin cambios; `compuerta_fuentes.listo` = true → aprobado.
- Pendiente: resuelto en la entrada siguiente (301 y 302 incluidas).

### Skill 1.2.1 — 2026-11-09: auditoría del sistema automático (box, tareas, vigía)
- Agente: Claude Code (sesión en la nube, modelo claude-opus-5-5), a petición de Muse (asistente de Emi) con instrucción de Emi: «audita, mejora y deja todo perfecto»; condición: no actualizar la imagen del box a v14 antes del SJF del viernes.
- Solicitud: auditar y corregir la skill 1.2.0 instalada, los scripts del box «main», las cuatro tareas programadas, la vigía de TinyFish y la prueba del DOF del 06/11/2026; documentar todo aquí.
- Auditado: skill instalada en claude.ai idéntica al commit 11a8cb1 (sin diferencias salvo .gitignore); scripts del box idénticos al repositorio (SHA-256); cuatro tareas programadas (horario, modelo, conectores, texto); vigía; prueba del 06/11; conector de Gmail (adjuntos).
- Hallazgos y correcciones:
  - Huecos entre cortes: las vespertinas y extraordinarias del martes y del jueves (posteriores al cierre de las 05:50/06:05) no entraban en ningún periodo. Ahora cada entrega empieza en el día del cierre anterior (`--corte`); lo ya cubierto se marca `ya_reportada` y solo prueba la continuidad de números (ADR 0005).
  - OCR incompleto: solo se reconocían páginas con menos de 80 caracteres. El 06/11/2026, 30 páginas de formatos del SAT tenían el formato completo en imagen bajo un poco de texto (p. 10: 9 renglones de texto, 45 en la imagen). Ahora `paginas_ocr` incluye las páginas con imagen de 300×100 px o más; OCR en dos procesos, reanudable, también para anexos del SJF.
  - Tope de 600 s por llamada al shell del box: nuevos `bin/lanzar.sh` (segundo plano con setsid, comprobado que sobrevive al reinicio) y `bin/estado.sh`.
  - Fallos que lo detenían todo o pasaban en silencio: `dof_fuentes.py` registra errores por edición sin abortar, guarda el inventario tras cada edición y reintenta con esperas cuando `nota_to_pdf.php` no redirige (falla real del 05/11/2026 MAT, resuelta al reintentar); `sjf_fuentes.mjs` registra errores de detalle y anexos, trata el 404 de la lista de anexos como «sin anexos», recarga la página ante el muro anti-bots (ocurrió en la prueba) y marca su control EN_CURSO hasta terminar; `fuentes.sh` corre todos los pasos y deja `estado.json` (OK / CON_FALLOS); `manifiesto.py` publica `compuerta_fuentes` (listo / faltantes).
  - `sin_edicion` no se limpiaba al reintentar una fecha que ya tenía edición; el número de publicación podía confundirse con la fecha de la portada; los enlaces de anexos partidos en dos renglones no se detectaban; `arranque.sh` no comprobaba que estuvieran los scripts ni reintentaba apt tras reiniciarse el disco de sistema. Corregidos.
  - Tareas programadas: usaban `fuentes.sh` en primer plano (rebasa 600 s) y `fuentes.sh dof <fecha>` hacia la carpeta equivocada; no decían cómo adjuntar en Gmail. Texto nuevo en `prompts/tareas/` y aplicado a las cuatro tareas (mismo horario y modelo): lanzador, `compuerta_fuentes`, páginas de `paginas_ocr`, ediciones `ya_reportada`, consulta de la vigía y adjuntos como referencia `sha256:<hash>:<ruta>`.
  - README desactualizado (decía skill 1.1.2 y «parche 1.2.0 no aplicado»; horas viejas): corregido. Nuevo `scripts/empaquetar_skill.sh` para el ZIP de claude.ai con un solo SKILL.md.
- Vigía: monitor TinyFish «DOF Castorena · vigía» (id 3adb2cba-2cba-4f1e-90ee-2a24c6060c2d), portada `https://dof.gob.mx/index.php`, lunes a jueves cada hora de 13:00 a 20:00, creado el 09/11/2026 con aprobación de Emi; sin webhook, por eso los cierres lo consultan con `get_monitor`.
- Archivos: `SKILL.md` (1.2.1), `README.md`, `references/box.md`, `docs/adr/0005-corte-anterior-y-fuentes-en-segundo-plano.md`, `scripts/box/` (arranque.sh, fuentes.sh, lanzar.sh, estado.sh, dof_fuentes.py, ocr.py, manifiesto.py, sjf_fuentes.mjs), `scripts/empaquetar_skill.sh`, `prompts/tareas/` (4), `tests/test_box_scripts.py`, `.gitignore`, este registro.
- Verificación: en el box, prueba del cierre del jueves 05/11 (corte 03/11 en el box: 300 ya reportada → 301, 302, 303, consecutivos; falla real de `nota_to_pdf` registrada y resuelta al relanzar) → aprobado; entrega real del martes 10/11 bajada hoy con el modo noche (303 ya reportada → 304, 305, 306; 119 + 2 + 2 páginas y 13 de anexos con OCR, 0 pendientes; SJF del 06/11: 28 tesis, 11 J y 17 aisladas, 16 ejecutorias, 14 votos, 1 acuerdo, 25 anexos, 0 errores; `compuerta_fuentes.listo` = true) → aprobado; scripts del box = repositorio (SHA-256) → aprobado; `python3 -m pytest -q` 57 aprobadas; `ia/check_skill.py` e `ia/test_guard.py`: ver resultado del commit.
- Estado del box: `/workspace/dof/fuentes/2026-11-10/` ya tiene fuentes y OCR del periodo del martes (el lector de esta noche solo bajará lo nuevo, como la vespertina del lunes); carpetas de prueba `prueba-2026-11-05-jueves` y `prueba-2026-11-06` (esta última con el formato anterior); respaldo de los scripts previos en `bin.respaldo-2026-11-09/`.
- Pendiente: (1) subir el ZIP 1.2.1 a claude.ai (`sh scripts/empaquetar_skill.sh`) para que la skill instalada coincida; las tareas programadas ya leen el repositorio; (2) actualizar la imagen del box a v14 después del SJF del viernes 13/11 y correr `bash bin/arranque.sh`; (3) confirmar con Emi si el cierre del jueves 05/11 se entregó: no está en el box ni en Gmail; el martes 10/11 toma su matutina (303/2026) como ya reportada; (4) primera semana en modo vigilado.

### 2026-11-09 · instalación de la skill 1.2.0 en claude.ai
- Agente: Muse (asistente de Emi). Registro preparado por Claude (chat) como «registro pendiente para el repositorio» y aplicado en este commit.
- Cambios: se instaló la skill dof-castorena 1.2.0 (commit 11a8cb1) en claude.ai en lugar de la 1.1.2. El primer ZIP fue rechazado («Zip must contain exactly one SKILL.md file. Currently there are 3.») porque los puentes de `.agents/` y `.claude/` cuentan como SKILL.md; se reempaquetó con solo el SKILL.md canónico. Se creó la vigía de TinyFish y se probó el box con el DOF del 06/11/2026.
- Verificación: aparece una sola vez en la lista; SKILL.md dice 1.2.0 y trae la sección «Fuentes con el box y ejecución automática»; prueba de chat aprobada; prueba del box: matutina 304/2026 de 358 páginas y vespertina 305/2026 de 8 páginas, páginas reales = declaradas, números consecutivos, OCR en español funcionando → aprobado.
- Pendiente: actualizar la imagen del box a v14 después del SJF del viernes.
### 2026-11-08 · paquete de entrega reutilizable
- Agente: Claude (sesión en la nube, claude-fable-5-1).
- Cambios: `scripts/paquete/` (build.js, email.js, audit.py, content.ejemplo.js, README) generan los cuatro archivos y el correo HTML desde `content.js` y `guia.js`; `references/box.md` lo enlaza.
- Verificación: DOCX idéntico al paquete del 3/11/2026 salvo los ids internos de hipervínculo; `python3 -m pytest -q` 45 aprobadas.

### Skill 1.2.0 — 2026-11-08: fuentes con el box y ejecución automática
- Agente: Claude (sesión en la nube, modelo claude-fable-5-1) — ejecución programada no; solicitud directa de Emi.
- Solicitud: Emi, 8/11/2026: combinar TinyFish, el box de Simular, la nube de Claude y su Mac con planes A, B y C por paso; velocidad, precisión y cero errores; reportes de martes y jueves automáticos, listos a las 07:30; todo en este repositorio, que sigue público.
- Cambios: `scripts/paquete/` (build.js, email.js, audit.py, content.ejemplo.js, README: generan los cuatro archivos y el correo HTML desde content.js y guia.js; probado: DOCX idéntico al paquete del 3/11/2026), `scripts/box/` (arranque.sh, fuentes.sh, dof_fuentes.py, paginas.py, ocr.py, manifiesto.py, sjf_fuentes.mjs), nueva `references/box.md` (reparto de papeles, hechos comprobados de los portales, calendario de tareas, planes A/B/C, compuertas), SKILL.md 1.2.0 (sección «Fuentes con el box y ejecución automática», horas de cierre 05:50/06:05 y lector nocturno, vía A del PDF por el box), `references/desbloqueo.md` (el box antes de pedir archivos a Emi), `references/claude-code.md` (programación con tareas de Claude).
- Verificación: regresión contra el periodo del 3/11/2026 en el box: DOF 30/10 MAT 144 pp. (297/2026), 30/10 VES 12 pp. (298), 02/11 156 pp. (299), 03/11 232 pp. (300), 4 anexos aparte localizados (2 en imagen, OCR en español); SJF del 30/10: 31 tesis (17 J, 14 aisladas), 16 ejecutorias, 4 votos, 0 acuerdos, 26 anexos con SHA-256 idénticos al paquete entregado a mano → aprobado. Lector subagente leyendo del box con `read_file` → aprobado. `python3 -m pytest -q`, `ia/check_skill.py` e `ia/test_guard.py`: ver resultado en el commit.
- Pendiente: crear las cuatro tareas programadas y el monitor; primera semana en modo vigilado; medir créditos del box por corrida.

### 2026-11-04 · corrección: puentes de skill con YAML válido

- Agente: Claude Code (sesión en la nube)
- Solicitud: autocorrección de Claude Code al revisar la skill matriz-castorena (4/11/2026).
- Cambios: los puentes `.claude/skills/` y `.agents/skills/` copiaban la descripción sin comillas; si contenía «: » el YAML quedaba inválido (afectaba a tareas-maestria y meta-ads-client-onboarding). Ahora va entre comillas, `ia/check_skill.py` rechaza valores que rompan el YAML y el control previo al commit revisa también los puentes.
- Archivos: `ia/check_skill.py`, `ia/politica.json`, `ia/REGLAS.md`, puentes de skill (si existen) y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

### 2026-11-04 · corrección: flag de push mal formado

- Agente: Claude Code (sesión en la nube)
- Solicitud: autocorrección de Claude Code al revisar su propio comando (4/11/2026).
- Cambios: la regla que prohíbe forzar el push no atrapaba flags cortos mal formados que contienen `f` o `d` (por ejemplo `-f-never`); el patrón ahora es `-(?!-)\S*[fd]\S*`. Se añadió el caso a las pruebas. Ese push concreto (rama de mes.) fue de avance lineal y no borró historial.
- Archivos: `ia/politica.json`, `ia/REGLAS.md`, `ia/INSTRUCCIONES_PROYECTO.md` y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

### 2026-11-04 · frenos de git también para Codex, ChatGPT y Gemini

- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 4/11/2026: que los frenos de git funcionen también con Codex y ChatGPT, no solo con Claude.
- Cambios: `python3 ia/verificar.py inicio`, que `AGENTS.md` pide ejecutar a cualquier IA al empezar, ahora también activa los hooks de git si faltan (antes solo lo hacía el hook de Claude Code). Así Codex, ChatGPT con terminal y Gemini CLI quedan con los mismos frenos de commit y push. `AGENTS.md` e `ia/INSTRUCCIONES_PROYECTO.md` lo indican.
- Archivos: `ia/verificar.py`, `ia/test_guard.py`, `ia/INSTRUCCIONES_PROYECTO.md`, `AGENTS.md` y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

### 2026-11-04 · arranque común entre IA (protocolo 1.1.0)

- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 4/11/2026: «haz lo que tengas que hacer para que entiendas» las reglas al trabajar.
- Cambios: `python3 ia/verificar.py inicio` resume al empezar rama, último commit y su IA, reglas, registro vigente y hooks de git; en Claude Code corre solo con un hook `SessionStart` y activa los hooks de git si faltan. `ia/PROTOCOLO.md` pasa a 1.1.0; `AGENTS.md`, `GEMINI.md` e `ia/INSTRUCCIONES_PROYECTO.md` indican el comando a las demás IA.
- Archivos: `.claude/settings.json`, `ia/verificar.py`, `ia/test_guard.py`, `ia/PROTOCOLO.md`, `ia/INSTRUCCIONES_PROYECTO.md`, `AGENTS.md`, `GEMINI.md` y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

### Skill 1.1.2 — 2026-11-04: registro obligatorio y trabajo entre IA
- Agente: Claude Code (sesión en la nube; modelo según la sesión)
- Solicitud: Emi, 4/11/2026: auditar y documentar las mejoras, hacerlas funcionar igual con ChatGPT, Gemini u otra IA, y documentar siempre todo cambio, use la IA que use, bajo las mismas reglas.
- Cambios: capa común `ia/` (protocolo común 1.0.0 basado en el de Mes, `REGLAS.md` generadas de `politica.json`, frenos para Claude Code, hooks de git para cualquier IA, workflow `registro-ia.yml`, `INSTRUCCIONES_PROYECTO.md` para ChatGPT y Gemini, plantillas de petición y entrega); `GEMINI.md`; sección «Trabajo entre IA» en `AGENTS.md`; `.claude/settings.json` apunta a `ia/guard.py` (se retira `.claude/hooks/`); auditoría en `ia/AUDITORIA_2026-11-04.md`. Skill 1.1.2: sección «Registro y continuidad entre IA» y nota de portabilidad en `references/claude-code.md`; el método no cambia.
- Archivos: ver `ia/AUDITORIA_2026-11-04.md`, sección «Archivos cambiados».
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py reglas --check` → aprobado; `python3 -m pytest -q` → aprobado (45).
- Revisión independiente: 17 hallazgos sobre el código común; corregidos los reproducidos, con pruebas de regresión (detalle en `ia/AUDITORIA_2026-11-04.md`).
- Pendiente: activar los hooks de git en cada copia (`sh ia/instalar.sh`); opcionalmente exigir el check `registro-ia` con protección de rama en GitHub.

### Skill 1.1.1 — 2026-11-04
- SKILL.md más ligero: «Módulo semanal SJF — obligatorio», «Operación SJF asistida y recuperación de documentos» y «Distribución semanal definitiva — aprobada 20/10/2026» pasan literalmente a `references/sjf-y-distribucion.md`; el «Protocolo obligatorio de desbloqueo con intervención de Emi — 20/10/2026» y sus portales oficiales, a `references/desbloqueo.md`. Solo se ajustaron rutas relativas de enlaces. Conservan su fuerza y sus reglas de precedencia.
- SKILL.md conserva un resumen de invariantes de calendario y destinatario, con la orden de leer íntegra la referencia antes de operar SJF, distribución o bloqueos.
- Nueva sección «Terminado y trabajo en Claude Code»: criterio de terminado verificable, entrevista solo en entregas extraordinarias o cambios de formato/alcance (nunca en las ejecuciones programadas) y pasos de máxima profundidad.
- Nuevos `references/claude-code.md` (hooks, reparto en paralelo, `/goal`, `/loop`, programación, navegador) y `scripts/headless.sh` (ejemplos de `claude -p`; no se activa al instalar).
- Descripción fusionada con la instalada en claude.ai para mejorar el disparo, sin perder el SJF semanal ni la exclusión.
- Prueba nueva que comprueba que el texto movido está completo en `references/` y que sus enlaces existen.
- El método jurídico, las reglas de verificación, privacidad y envío, el estilo aprobado y el calendario no cambian. Esta versión no es el parche independiente 1.2.0, que sigue sin aplicarse; el paquete Python sigue en 1.0.0.

### Maintenance — 2026-11-03
- Se modernizó el frontmatter de la skill para Codex sin cambiar la versión 1.1.0 ni el método jurídico.
- La descripción distingue el encargo DOF/SJF de la redacción jurídica genérica.
- Se añadió un extra reproducible de pruebas y el comando local correspondiente.

### Changed — 2026-10-20: calendario definitivo de entregas
- Viernes: preparación SJF interna sin correo ordinario separado.
- Martes: un único paquete DOF + SJF de cuatro adjuntos.
- Jueves: exclusivamente DOF, cuatro adjuntos, sin correcciones SJF.
- Independencia de auditoría DOF jueves y bloqueo de cierre conjunto martes cuando falte DOF o SJF.
- Se conservan horarios y reglas de lectura íntegra; el parche 1.2.0 continúa independiente.



### Audit follow-up (2026-10-20)
- Propuesta PR #2: controles fail-closed de evidencia DOF/SJF, rangos sin huecos, hashes declarados y estados de envío; pruebas unitarias y esquema de manifiesto.
- Documentación del Quality Gate y flujo SJF alineada. No implica integración automática con Gmail, lectura efectivamente realizada ni aplicación del parche independiente 1.2.0.

### Added
- Módulo documental SJF con lectura integral, estudio, opinión, continuidad y síntesis en el DOF del martes.
- Guía didáctica y plantillas de reporte, estudio y correo con lenguaje claro y fuentes verificables.
- Auditoría jurídica/editorial y ADR 0004 para distinguir publicación, obligatoriedad, efectos y cobertura.
### Scope
- Sin cambios al código, schemas, calendario DOF existente ni versión publicada. El módulo no aplica el parche 1.2.0 ni acredita una edición semanal leída.

## [1.1.0] - 2026-10-07
### Added
- Skill portable `SKILL.md` para reportes DOF Castorena.
- Formato minimalista blanco/negro/grises, enlaces oficiales identificados dentro de cada fila.
- UX de correo personal con cuatro adjuntos, comentario sugerido independiente y correo BLUF íntegro.
### Clarified
- Revisión profesional proporcional al encargo distinta de certificación exhaustiva de cobertura.
- Prohibición de afirmar «cobertura completa» sin cerrar todas las ediciones, publicaciones y anexos.

## [1.0.0] - 2026-10-02
### Added
- Especificación autónoma del monitor DOF.
- Doble vía de cobertura.
- Quality Gate jurídico/editorial.
- Prompt Maestro neutral.
- Adaptadores ChatGPT, Claude, Gemini y Grok.
- Schemas de cobertura/reporte.
- Plantillas de reporte, guía y correo.
- Librería Python mínima y pruebas.
- ADRs para decisiones de cobertura y separación de entregables.

### Changed
- Consolidación de las iteraciones desarrolladas durante septiembre-octubre de 2026 en una fuente de verdad independiente.

### Operación SJF asistida (2026-10-20)
- Nuevo registro local de PDF, hashes, páginas y controles jurídicos por edición con estado inicial PENDIENTE.
- Procedimiento de recuperación manual desde fuentes oficiales, sin sustituir lectura por índices.
- Pruebas para rechazar documentos faltantes, duplicados y cierres sin evidencia. Sin automatización de Gmail ni generación documental implícita.
