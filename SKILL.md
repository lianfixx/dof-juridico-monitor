---
name: dof-castorena
description: Revisa el Diario Oficial de la Federación (DOF) y prepara la actualización jurídica semanal para el Lic. Castorena (martes y jueves), con la síntesis del SJF semanal, fuentes oficiales verificadas, reporte ejecutivo minimalista en PDF, guía de estudio, comentario sugerido y correo BLUF para revisión de Emi. Úsalo siempre que el usuario mencione DOF, Diario Oficial, actualización DOF, SJF semanal, reporte para Castorena, monitor jurídico, novedades fiscales, PLD, administrativas o de amparo publicadas en el DOF, o pida revisar, corregir o rehacer un reporte DOF anterior, aunque no diga «skill» ni «Castorena». No usar para redacción jurídica genérica ni expedientes de clientes.
metadata:
  version: "1.1.2"
  release_date: "2026-11-04"
  language: "es-MX"
  jurisdiction: "MX"
---

# DOF Castorena · Skill 1.1.2

## Propósito
Preparar para Emiliano García Milla una actualización jurídica del DOF que pueda revisar antes de decidir si la envía al Lic. Guillermo Castorena Álvarez. Priorizar Fiscal, Compliance/PLD-FT, Administrativo y Amparo. Añadir reformas nacionales significativas solo cuando tengan consecuencias jurídicas prácticas. No enviar al Licenciado ni crear borradores a terceros.

## Periodicidad
Martes: viernes anterior, lunes y martes. Jueves: miércoles y jueves. Zona America/Mexico_City; objetivo 06:00 para revisión antes de 09:00, sin prometer cumplimiento cuando existan bloqueos. Complementar con correcciones, fes de erratas, ediciones tardías y fines de semana desde el corte anterior. Registrar hora real de última consulta.

## Investigación y control
1. Identificar las ediciones de cada fecha mediante calendario/índice oficial DOF/SIDOF, incluyendo matutina, vespertina y extraordinaria. No inventar ediciones.
2. Intentar abrir el PDF completo real, no su icono. Si existe, utilizarlo para comprobar estructura, secciones y potenciales omisiones. Si no puede abrirse, emplear índice oficial y notas individuales; señalar limitaciones.
3. OBLIGATORIO: leer íntegramente, palabra por palabra, TODAS las publicaciones de todas las ediciones y colecciones, incluyendo contenido secundario, artículos, resolutivos, transitorios, tablas, notas al pie y anexos. No filtrar por relevancia antes de completar la lectura. Solo después seleccionar los hallazgos que aparecerán en el reporte ejecutivo. Registrar rangos/páginas y estados sin huecos.
4. Confirmar cada enlace directo de nota oficial y cada fundamento. Separar anuncio, iniciativa, dictamen, aprobación, publicación y vigencia. Nunca presentar sentencia aislada como jurisprudencia.
5. Prohibido sustituir la lectura íntegra por revisión selectiva o proporcional. Solo declarar «COBERTURA COMPLETA AL CORTE» cuando todas las ediciones, publicaciones y anexos hayan sido leídos íntegramente y se cumplan docs/QUALITY_GATE.md. Si existe un solo tramo sin cerrar, marcar PARCIAL y no presentar ni enviar una versión como final.
6. No extrapolar efectos a expedientes concretos sin documentación autorizada y suficiente. Corregir cualquier error en todos los entregables antes de cerrar.

## Condición previa de cierre y envío
No generar ni enviar un paquete presentado como final antes de terminar la lectura exhaustiva y una investigación jurídica profunda, razonada, crítica, argumentada y verificada. Si hay fuentes inaccesibles, explicar con precisión el bloqueo, sin inventar contenido ni declarar final. La concisión del reporte no reduce el alcance de la investigación. Estas reglas prevalecen sobre cualquier referencia histórica a revisión selectiva.

## Entregables
**Para el Lic. Castorena:** PDF «Actualización DOF | [fecha]» y texto de correo BLUF para revisión de Emi. Reporte sin controles operativos, metodología, guía ni portada vacía.
**Solo para Emi:** DOCX editable del reporte, guía de estudio/control PDF y DOCX, comentario sugerido separado (40–70 palabras), correo completo (80–130 palabras) y bitácora interna. El comentario sugerido NO sustituye automáticamente «Comentario personal: [Espacio para mi opinión antes del envío]».

## Estilo aprobado (obligatorio)
- Diseño minimalista editorial: fondo blanco, negro y grises neutros, sin bloques de colores tipo IA, dashboards, iconos, degradados o adornos.
- Mantener «Lo relevante» en 2–4 líneas sustantivas y una tabla de cuatro columnas: «Asunto | Qué ocurrió/efecto | Vigencia/estado | Por qué importa/qué revisar».
- Cada hallazgo lleva su fuente oficial DIRECTAMENTE EN SU FILA, con nombre identificable y enlace comprobado. Cuando haya varias fuentes (IMPI, PRODECON, TFJA), separarlas claramente dentro de la misma fila.
- No incluir la leyenda «Periodo revisado: ... · Ediciones oficiales ... · Revisión cerrada para el encargo del despacho», ni frases internas equivalentes.
- Redacción natural, humana, fluida, precisa, profesional, sobria; conservar contenido sustantivo aprobado al hacer solo cambios visuales.
- Correo personal a Emi: HTML responsive con fondo gris muy claro, contenedor blanco (~640 px), líneas finas, tipografía sistema, secciones «PARA EL LIC. CASTORENA» y «SOLO PARA TI», hallazgos, texto íntegro del correo al Licenciado, comentario sugerido separado, qué estudiar primero y nota breve de control. Sin logos inventados.
- Correo al Licenciado inicia «Licenciado, buen día. Le comparto la actualización del DOF correspondiente a ...»; firma «Emiliano García Milla». BLUF, directo y sin burocratismos.

## Envío y verificación
Solo tras superar el control exhaustivo y verificar los cuatro archivos, enviar UN correo a emilianogarciamilla@gmail.com, sin CC/CCO, si Gmail está disponible y autorizado. Antes buscar duplicados en Enviados; adjuntar cuatro archivos reales (PDF del Licenciado, DOCX editable, guía PDF y DOCX), confirmar respuesta de Gmail y releer metadatos y adjuntos. No enviar al Licenciado. Si el usuario solo pide actualización de repositorio, no enviar correos.

## Referencias
Consultar AGENTS.md, docs/SPECIFICATION.md, docs/WORKFLOW.md, docs/QUALITY_GATE.md, prompts/master.md y config/default.yaml. Ante conflicto, no debilitar verificación jurídica ni declarar cobertura completa sin prueba. Este SKILL.md define la presentación final aprobada para Castorena.

## Calendario, SJF y desbloqueo
- Martes, 06:00 America/Mexico_City: DOF + SJF del último viernes efectivamente publicado, en un solo correo cuyos adjuntos son exactamente cuatro archivos conjuntos (reporte PDF/DOCX y guía PDF/DOCX).
- Jueves, 06:00: exclusivamente DOF; sin sección, hallazgo ni corrección SJF.
- Viernes, 15:00 (ventana flexible): revisión SJF interna; no crea un envío semanal adicional por defecto.
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
