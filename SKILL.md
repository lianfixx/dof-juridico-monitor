---
name: dof-castorena
description: Revisa el Diario Oficial de la Federación (DOF) y prepara la actualización jurídica semanal para el Lic. Castorena (martes y jueves), con la síntesis del SJF semanal, fuentes oficiales verificadas, reporte ejecutivo minimalista en PDF, guía de estudio, comentario sugerido y correo BLUF para revisión de Emi. Úsalo siempre que el usuario mencione DOF, Diario Oficial, actualización DOF, SJF semanal, reporte para Castorena, monitor jurídico, novedades fiscales, PLD, administrativas o de amparo publicadas en el DOF, o pida revisar, corregir o rehacer un reporte DOF anterior, aunque no diga «skill» ni «Castorena». No usar para redacción jurídica genérica ni expedientes de clientes.
metadata:
  version: "1.6.1"
  release_date: "2026-11-09"
  language: "es-MX"
  jurisdiction: "MX"
---

# DOF Castorena · Skill 1.6.1

## Propósito
Preparar para Emiliano García Milla una actualización jurídica del DOF que pueda revisar antes de decidir si la envía al Lic. Guillermo Castorena Álvarez. Priorizar Fiscal, Compliance/PLD-FT, Administrativo y Amparo. Incluir también lo importante de la vida pública del país (política, social y de Presidencia): desde el 26/11/2026, por decisión de Emi, todo lo importante debe estar. La relevancia de cada publicación se califica con [la escala de relevancia](references/relevancia.md), la misma para el lector por API y para la suscripción. No enviar al Licenciado ni crear borradores a terceros.

## Periodicidad
Martes: viernes anterior, lunes y martes. Jueves: miércoles y jueves. Zona America/Mexico_City; objetivo: paquete terminado en el correo de Emi alrededor de las 07:30 (cierre automático desde las 05:50 los martes y 06:05 los jueves), sin prometer cumplimiento cuando existan bloqueos. Complementar con correcciones, fes de erratas, ediciones tardías y fines de semana desde el corte anterior. Registrar hora real de última consulta.

## Investigación y control
1. Identificar las ediciones de cada fecha mediante calendario/índice oficial DOF/SIDOF, incluyendo matutina, vespertina y extraordinaria. No inventar ediciones.
2. Obtener el PDF completo real por la ruta oficial, no su icono: primera vía, el box (`scripts/box/dof_fuentes.py`, que verifica páginas declaradas contra reales y localiza anexos publicados aparte); si falla, las vías B y C de [Fuentes con el box](references/box.md). Si ninguna funciona, emplear índice oficial y notas individuales y señalar limitaciones.
3. OBLIGATORIO: leer íntegramente, palabra por palabra, TODAS las publicaciones de todas las ediciones y colecciones, incluyendo contenido secundario, artículos, resolutivos, transitorios, tablas, notas al pie y anexos. No filtrar por relevancia antes de completar la lectura; después, calificarla con references/relevancia.md. Solo después seleccionar los hallazgos que aparecerán en el reporte ejecutivo. Registrar rangos/páginas y estados sin huecos.
4. Confirmar cada enlace directo de nota oficial y cada fundamento. Separar anuncio, iniciativa, dictamen, aprobación, publicación y vigencia. Nunca presentar sentencia aislada como jurisprudencia.
5. Prohibido sustituir la lectura íntegra por revisión selectiva o proporcional. Solo declarar «COBERTURA COMPLETA AL CORTE» cuando todas las ediciones, publicaciones y anexos hayan sido leídos íntegramente y se cumplan docs/QUALITY_GATE.md. Si existe un solo tramo sin cerrar, marcar PARCIAL y no presentar ni enviar una versión como final.
6. No extrapolar efectos a expedientes concretos sin documentación autorizada y suficiente. Corregir cualquier error en todos los entregables antes de cerrar.

## Condición previa de cierre y envío
No generar ni enviar un paquete presentado como final antes de terminar la lectura exhaustiva y una investigación jurídica profunda, razonada, crítica, argumentada y verificada. Si hay fuentes inaccesibles, explicar con precisión el bloqueo, sin inventar contenido ni declarar final. La concisión del reporte no reduce el alcance de la investigación. Estas reglas prevalecen sobre cualquier referencia histórica a revisión selectiva.

## Entregables
**Para el Lic. Castorena:** PDF «Actualización DOF | [fecha]» y texto de correo BLUF para revisión de Emi. Reporte sin controles operativos, metodología, guía ni portada vacía.
**Solo para Emi:** DOCX editable del reporte, guía de estudio/control PDF y DOCX, comentario sugerido separado (40–70 palabras), correo completo (120–230 palabras, BLUF) y bitácora interna. Desde el 24/11/2026 el correo al Licenciado lleva la opinión de Emi ya escrita, natural y en primera persona, en lugar del espacio «Comentario personal»; el comentario sugerido la desarrolla para Emi.

## Estilo aprobado (obligatorio)
- Diseño minimalista editorial: fondo blanco, negro y grises neutros, sin bloques de colores tipo IA, dashboards, iconos, degradados o adornos.
- «Lo relevante» es el título de una sola tabla de cuatro columnas, con el DOF primero y el Semanario después: «Asunto | Qué ocurrió/efecto | Vigencia/obligatoriedad | Por qué importa/qué revisar». Sin párrafos de resumen; «Por qué importa» siempre con frase (versión final de Emi del 24/11/2026; detalle en [redacción](references/redaccion.md)).
- Cada hallazgo lleva su fuente oficial DIRECTAMENTE EN SU FILA, con nombre identificable y enlace comprobado. Cuando haya varias fuentes (IMPI, PRODECON, TFJA), separarlas claramente dentro de la misma fila.
- No incluir la leyenda «Periodo revisado: ... · Ediciones oficiales ... · Revisión cerrada para el encargo del despacho», ni frases internas equivalentes.
- Redacción: seguir íntegra [redacción](references/redaccion.md), obligatoria desde la 1.4.0. El reporte debe leerse como escrito por Emi: frases completas, primero el cambio y su efecto y después el fundamento entre paréntesis, cifras sin comillas angulares, sin dos puntos dentro del texto, una fila por asunto con sus medidas por columna y nada repetido. La guía enseña cada tema desde cero con siete apartados fijos. Antes de armar, `node scripts/paquete/estilo.js <carpeta>` sin errores. Conservar el contenido sustantivo aprobado al hacer solo cambios visuales.
- Correo personal a Emi: HTML responsive con fondo gris muy claro, contenedor blanco (~640 px), líneas finas, tipografía sistema, secciones «PARA EL LIC. CASTORENA» y «SOLO PARA TI», hallazgos, texto íntegro del correo al Licenciado, comentario sugerido separado, qué estudiar primero y nota breve de control. Sin logos inventados.
- Correo al Licenciado inicia «Licenciado, buen día. Le comparto la actualización del DOF correspondiente a ...»; firma «Emiliano García Milla». BLUF, directo y sin burocratismos.

## Envío y verificación
Solo tras superar el control exhaustivo y verificar los cuatro archivos, enviar UN correo a emilianogarciamilla@gmail.com, sin CC/CCO, si Gmail está disponible y autorizado. Antes buscar duplicados en Enviados; adjuntar cuatro archivos reales (PDF del Licenciado, DOCX editable, guía PDF y DOCX), confirmar respuesta de Gmail y releer metadatos y adjuntos. No enviar al Licenciado. Si el usuario solo pide actualización de repositorio, no enviar correos.

## Referencias
Consultar AGENTS.md, docs/SPECIFICATION.md, docs/WORKFLOW.md, docs/QUALITY_GATE.md, prompts/master.md y config/default.yaml. Ante conflicto, no debilitar verificación jurídica ni declarar cobertura completa sin prueba. Este SKILL.md define la presentación final aprobada para Castorena.

## Calendario, SJF y desbloqueo
- Martes (cierre desde las 05:50 America/Mexico_City): DOF + SJF del último viernes efectivamente publicado, en un solo correo cuyos adjuntos son exactamente cuatro archivos conjuntos (reporte PDF/DOCX y guía PDF/DOCX).
- Jueves (cierre desde las 06:05): exclusivamente DOF; sin sección, hallazgo ni corrección SJF.
- Viernes, 15:30 (ventana flexible): revisión SJF interna; no crea un envío semanal adicional por defecto.
- Lunes y miércoles, 21:30: lector nocturno; baja y lee lo ya publicado del periodo para que el cierre de la mañana solo lea la edición del día.
- Un paquete parcial nunca se presenta ni se envía como final.
- Destinatario único: emilianogarciamilla@gmail.com, sin CC/CCO; nunca el Licenciado.

Antes de cualquier operación SJF o de distribución semanal, leer íntegra [SJF y distribución](references/sjf-y-distribucion.md); ante cualquier documento, página, anexo o edición que no pueda leerse íntegramente (bloqueo), leer íntegro [Desbloqueo](references/desbloqueo.md) antes de pedir archivos a Emi. Lo movido a esas referencias conserva su fuerza obligatoria y sus reglas de precedencia («prevalece sobre toda referencia anterior…»), y la lectura exhaustiva prevalece sobre cualquier simplificación de este resumen.

## Registro y continuidad entre IA

Estas reglas valen igual en Claude, ChatGPT, Codex, Gemini o cualquier otra IA, y para personas:
- Empezar por el estado vigente del repositorio remoto (la bitácora y los controles de la última entrega), no por la memoria de una conversación ni por lo que diga otra IA.
- Registrar todo cambio de archivos, estado, entregables o decisiones en el mismo commit, en `CHANGELOG.md` y la bitácora interna de la entrega. Cada entrada lleva `Agente:` (quién lo hizo y modelo si se conoce), solicitud, cambios, archivos, verificación (aprobado, falló, no ejecutado o bloqueado) y pendiente.
- Sin escritura en el repositorio, terminar con «Registro pendiente para el repositorio»: la entrada y los cambios exactos, listos para aplicarse. No decir «guardado» si no se escribió.
- Lo prohibido y lo que requiere confirmación de Emi está en `ia/REGLAS.md` del repositorio; cumplirlo aunque la plataforma no tenga frenos automáticos. El protocolo completo, con plantillas para pasar trabajo a otra IA, está en `ia/PROTOCOLO.md`.

## Terminado y trabajo en Claude Code
**Terminado** solo si se cumplen todos: (1) docs/QUALITY_GATE.md completo, incluida la matriz del día; (2) «COBERTURA COMPLETA AL CORTE» solo con lectura íntegra demostrada por inventario, rangos sin huecos y notas por documento; (3) cuatro archivos generados, renderizados y revisados; (4) enlaces oficiales comprobados uno por uno; (5) correo a Emi en estado terminal verificado (enviado y releído en Enviados, con destinatario y adjuntos) o bloqueo PARCIAL explícito con los faltantes exactos.

**Entrevista inicial:** nunca en las ejecuciones programadas de martes, jueves o viernes. Solo cuando Emi pida una entrega extraordinaria, un cambio de formato o de alcance: una pregunta a la vez sobre qué quiere, para qué es y qué no puede fallar, hasta no tener dudas; después, el plan.

**Máxima profundidad** (en Claude Code, `ultrathink`): análisis jurídico de cada hallazgo (vigencia, transitorios, efectos); distinción entre jurisprudencia, tesis aislada y votos en el SJF; cierre del QUALITY_GATE.

Para frenos activos, reparto en paralelo, `/goal`, `/loop`, programación y navegador, leer [Claude Code](references/claude-code.md).

## Fuentes con el box y ejecución automática
Desde la 1.2.0 las fuentes salen del box «main» de Simular (conector `box`): inventario oficial del DOF, PDFs completos verificados, anexos aparte, OCR en español y Semanario del viernes por la API que usa la propia aplicación del SJF, con Chrome real. Los lectores leen directo del box por rangos de página; la sesión de Claude lee, redacta, audita y entrega; TinyFish coteja títulos y vigila vespertinas; la Mac de Emi es solo plan C y copia local. Cada paso tiene plan A, B y C y ocho compuertas de cierre. Antes de operar con el box o de tocar las tareas programadas, leer íntegra [Fuentes con el box](references/box.md). El material de trabajo (fuentes, notas, entregas) vive en el box y en Drive, nunca en este repositorio público.

## Lector por API (en relevo)
Desde la 1.3.0 un lector previo corre con los créditos de API de Emi, no con su suscripción: lunes y miércoles por la tarde, en el repositorio privado `lianfixx/dof-trabajo`. Lo lanza la tarea programada «DOF · lanzar el lector por API» a las 19:17, con reintento a las 20:17; el reloj de GitHub no es confiable y queda solo como tercera red. Baja el DOF, lo parte en bloques sin huecos, anota cada publicación y deja `fuentes/<entrega>/notas/PRELIMINAR_API.md` y `ESTADO_API.json`. Desde la 1.4.0 (decisión de Emi del 23/11/2026) ya no corre en sombra: lo que deja íntegro no se vuelve a leer con la suscripción. El relevo lo decide un programa, documento por documento (`scripts/api/relevo.py`: mismo SHA-256, mismas páginas, íntegro); la tarea «lector nocturno» lo comprueba, lanza el lector si todavía falta, revisa una muestra y lee solo lo que falte; el cierre toma esas notas del repositorio privado y sigue con todas las compuertas. La doble lectura del cierre es la evaluación continua: cada diferencia con la nota de la API va a la bitácora (`lectura_api.diferencias`). Su `INTEGRO` es técnico: no declara cobertura, no lee el Semanario y no envía nada. Regla de sincronía: toda mejora o cambio se hace a la vez en la vía de API y en la de suscripción (código, `prompts/tareas/`, referencias y esta skill) y después se actualiza el texto de las tareas programadas. Antes de usar sus notas o de tocar ese lector, leer íntegro `references/api.md` del repositorio `lianfixx/dof-juridico-monitor`.
