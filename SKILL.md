---
name: dof-castorena
description: Revisa el DOF de martes y jueves para Castorena; verifica fuentes oficiales y genera reporte ejecutivo minimalista, guía personal, comentario y correo de revisión.
version: 1.1.0
---

# DOF Castorena · Skill 1.1.0

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

## Módulo semanal SJF — obligatorio
El módulo SJF aprobado el 15/10/2026 se rige por [docs/sjf/METODO.md](docs/sjf/METODO.md) y sus plantillas, incorporadas desde el PR #1. Es independiente del parche 1.2.0. La revisión corresponde al viernes de publicación efectiva; el martes se integra su síntesis al reporte DOF y el jueves únicamente novedades o correcciones posteriores verificadas, sin modificar el horario DOF.

Antes de declarar integración, recuperar en Library los cinco controles/entregables SJF_AAAA-MM-DD_Reporte.pdf/.docx, SJF_AAAA-MM-DD_Guia.pdf/.docx y SJF_AAAA-MM-DD_Control.json, o reconstruir evidencia de lectura íntegra y auditoría. Si falta evidencia, marcar SJF PENDIENTE y bloquear el cierre final DOF+SJF. Conservar por separado fechas, fuentes, cobertura y estados DOF/SJF.

Leer íntegramente publicaciones, sentencias, tesis, votos y anexos del SJF sin selección previa; verificar fuente oficial, razones, votación, ámbito, fecha y fundamento de obligatoriedad, efectos y temporalidad. Distinguir jurisprudencia obligatoria, tesis aislada y votos. Cada ficha debe explicar hechos, resolución, relevancia, aplicación y límites; en la guía de Emi añadir estudio, ejemplos hipotéticos, preguntas y opinión/contraargumento separados.

Integrar SJF en los mismos cuatro archivos DOF, sin adjuntos duplicados. Mantener PDF ejecutivo del Licenciado sin metodología interna, DOCX editable y guía personal PDF/DOCX, comentario sugerido 40–70 palabras y correo BLUF 80–130 palabras con «Comentario personal: [Espacio para mi opinión antes del envío]». Antes de cualquier envío comprobar duplicados, tentativa, versiones, renderizado y adjuntos; si el resultado de envío es ambiguo, bloquear reenvío. Destinatario exclusivo: emilianogarciamilla@gmail.com; nunca el Licenciado.

Las instrucciones prioritarias de lectura exhaustiva y bloqueo ante evidencia incompleta prevalecen sobre cualquier simplificación documental del módulo.

## Operación SJF asistida y recuperación de documentos
Aplicar [docs/sjf/OPERACION.md](docs/sjf/OPERACION.md). Cuando una fuente SJF no sea accesible automáticamente, facilitar el enlace al portal oficial y solicitar al usuario los PDF concretos faltantes. Usar `sjf_intake` para registrar hashes, páginas y pendientes sin afirmar lectura automática. El viernes puede mantenerse un paquete SJF parcial; el martes no se integrará como final sin recuperar el control íntegro y auditarlo. No subir material personal a GitHub. El módulo no genera ni envía automáticamente los cuatro archivos: esa ejecución requiere herramientas externas y verificación individual.

## Distribución semanal definitiva — aprobada 20/10/2026

**Martes, 06:00 America/Mexico_City: DOF + SJF.** Integrar el DOF del periodo y la síntesis de la edición SJF del último viernes efectivamente publicado, conservando la fecha original del viernes. El correo personal contiene **exactamente cuatro archivos conjuntos**: reporte ejecutivo PDF, reporte editable DOCX, guía de estudio/control PDF y guía editable DOCX. Secciones y controles DOF/SJF diferenciados dentro de esos mismos archivos; jamás ocho adjuntos duplicados.

**Jueves, 06:00 America/Mexico_City: exclusivamente DOF.** Revisar miércoles, jueves y pendientes/correcciones DOF desde el corte anterior. Los **cuatro adjuntos son exclusivamente DOF**. No insertar tesis, sentencias, votos, jurisprudencia, sección SJF ni correcciones SJF en el correo del jueves. Registrar novedades judiciales sobrevenidas en el control SJF para el siguiente martes o una revisión extraordinaria expresamente solicitada. No ocultar pendientes ni falsificar que se hayan resuelto.

**Viernes, 15:00 (ventana flexible): revisión SJF interna.** Inventariar y leer todo lo publicado; investigar y persistir control y paquete SJF si la auditoría lo permite. La tarea del viernes prepara la integración del martes, **no crea un envío semanal adicional por defecto**. Si se solicita una entrega extraordinaria, aplicar los mismos controles y deduplicación.

**Independencia de cierre:** si el SJF sigue PARCIAL el martes, bloquear únicamente la presentación como final del paquete **conjunto DOF+SJF**; informar exactamente qué falta y conservar DOF y SJF separados. El jueves puede cerrarse como **DOF solamente** si su propia lectura y auditoría son completas, sin depender del SJF. El martes no enviar un paquete conjunto rotulado final si cualquiera de los dos módulos está pendiente.

Las cuatro piezas siguen sujetas a generación, renderizado, revisión de enlaces, hashes y controles de duplicados. El correo se dirige únicamente a emilianogarciamilla@gmail.com, nunca al Licenciado. El cambio de distribución no relaja la lectura exhaustiva, ni autoriza enviar un paquete parcial como final.

Esta sección prevalece sobre toda referencia anterior que incorpore novedades SJF el jueves o que presuponga un correo separado los viernes. El calendario DOF y sus horas no cambian.
