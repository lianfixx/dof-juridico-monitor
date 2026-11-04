# Changelog

Formato inspirado en Keep a Changelog. Versionado SemVer.

## [Unreleased]
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
