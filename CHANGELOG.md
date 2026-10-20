# Changelog

Formato inspirado en Keep a Changelog. Versionado SemVer.

## [Unreleased]

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
