# DOF Jurídico Monitor

Sistema autónomo, auditable y agnóstico de proveedor para revisar el Diario Oficial de la Federación (DOF), verificar cobertura, detectar novedades jurídicas relevantes y producir entregables ejecutivos y de estudio.

No depende de ChatGPT, de una conversación previa ni de servidores privados de un proveedor de IA. Cualquier agente con acceso web/PDF puede implementar el flujo siguiendo este repositorio.

## Principios
1. Cobertura antes que selección.
2. Fuentes oficiales primero.
3. Lo no comprobado se marca; no se infiere.
4. Doble vía: PDF completo real o índice + publicaciones + colecciones secundarias.
5. Cobertura completa exige lectura íntegra del universo.
6. Separación despacho / operador.
7. Corrección inmediata y propagación.
8. Neutralidad política.
9. Profundidad en investigación; concisión en entregables.
10. Diseño limpio, natural y profesional.

## Calendario
- Martes: viernes anterior + lunes + martes.
- Jueves: miércoles + jueves.
- Complemento: fines de semana, publicaciones posteriores al corte, fes de erratas/correcciones/republicaciones.
- Zona: America/Mexico_City.

## Entregables
**Despacho:** reporte PDF + correo BLUF para revisión humana.
**Operador:** editable DOCX + guía PDF/DOCX + comentario + bitácora.

## Inicio
1. AGENTS.md
2. docs/SPECIFICATION.md
3. docs/WORKFLOW.md
4. docs/QUALITY_GATE.md
5. prompts/master.md
6. config/default.yaml

Versión: **1.0.0**.
