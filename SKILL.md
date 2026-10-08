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
3. Aplicar filtro de relevancia antes de lectura jurídica profunda. Leer íntegramente cada publicación seleccionada y los anexos aplicables; revisar artículos, transitorios, vigencia, sujetos, excepciones y efectos.
4. Confirmar cada enlace directo de nota oficial y cada fundamento. Separar anuncio, iniciativa, dictamen, aprobación, publicación y vigencia. Nunca presentar sentencia aislada como jurisprudencia.
5. La revisión profesional proporcional al encargo NO equivale a certificación de lectura íntegra de todas las publicaciones secundarias. Solo usar «COBERTURA COMPLETA AL CORTE» si se cumplen los criterios estrictos de docs/QUALITY_GATE.md; de lo contrario explicar el alcance real sin afirmar exhaustividad.
6. No extrapolar efectos a expedientes concretos sin documentación autorizada y suficiente. Corregir cualquier error en todos los entregables antes de cerrar.

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
Solo enviar UN correo a emilianogarciamilla@gmail.com, sin CC/CCO, si Gmail está disponible y autorizado. Antes buscar duplicados en Enviados; adjuntar cuatro archivos reales (PDF del Licenciado, DOCX editable, guía PDF y DOCX), confirmar respuesta de Gmail y releer metadatos y adjuntos. No enviar al Licenciado. Si el usuario solo pide actualización de repositorio, no enviar correos.

## Referencias
Consultar AGENTS.md, docs/SPECIFICATION.md, docs/WORKFLOW.md, docs/QUALITY_GATE.md, prompts/master.md y config/default.yaml. Ante conflicto, no debilitar verificación jurídica ni declarar cobertura completa sin prueba. Este SKILL.md define la presentación final aprobada para Castorena.
