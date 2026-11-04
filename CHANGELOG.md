# Changelog

Formato inspirado en Keep a Changelog. Versionado SemVer.

## [Unreleased]
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
