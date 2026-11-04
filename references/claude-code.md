# Claude Code para DOF Castorena

Complemento operativo de [SKILL.md](../SKILL.md). No cambia el método, los controles ni el calendario.

## Frenos activos (hooks)
Configurados en `.claude/` de este repositorio:
1. Bloquean cualquier correo o borrador de Gmail con destinatario distinto de emilianogarciamilla@gmail.com, o con CC/CCO. Nunca al Licenciado.
2. Antes de un `git commit` que toque `src/`, `tests/`, `schemas/`, `config/` o `templates/`, corren `python3 -m pytest -q` (si falta pytest, preguntan).
3. Antes de cada commit, buscan secretos y datos personales (CURP, tarjetas) en el diff; el repositorio es público.
4. Preguntan antes de `git push` y bloquean `git push --force`.
5. Si el commit cambia SKILL.md, comprueban su compatibilidad con claude.ai.

Solo actúan en Claude Code dentro de este repositorio, no en claude.ai ni en otras IA, y no sustituyen las reglas de la skill: el destinatario único, la lectura íntegra y el bloqueo PARCIAL se cumplen igual.

Las mismas reglas valen fuera de Claude Code: están en `ia/REGLAS.md` (generadas de `ia/politica.json`). Con terminal, `sh ia/instalar.sh` las activa como hooks de git para cualquier IA o persona, y GitHub revisa cada push con `registro-ia.yml`. En chat sin frenos (claude.ai, ChatGPT, Gemini), la IA las cumple por sí misma y entrega el registro pendiente. Además, todo commit sin entrada de registro con `Agente:` queda bloqueado.

## Plan y entrevista
Modo plan con Shift+Tab: investiga y propone sin tocar nada; antes de aprobarlo, se corrige respondiendo con los cambios. Las ejecuciones programadas de martes, jueves y viernes no llevan entrevista. Pedirla solo cuando Emi solicite una entrega extraordinaria, un cambio de formato o de alcance:

> Antes de armar el plan, entrevístame. Hazme una pregunta a la vez sobre lo que quiero, para qué es y qué no puede fallar, hasta que no te quede ninguna duda. Después muéstrame el plan.

## Reparto en paralelo
- Primero, un inventario único de ediciones y publicaciones del periodo (matutina, vespertina, extraordinaria) desde el índice oficial DOF/SIDOF.
- Un subagente por edición o por tramo de páginas. Los rangos se asignan sin huecos ni solapamientos y cada uno devuelve páginas leídas, notas por publicación, anexos y estado (INTEGRO, PARCIAL, PENDIENTE, INACCESIBLE).
- Viernes SJF: un subagente por tipo (jurisprudencia, tesis aisladas, votos), con las relaciones entre tesis, sentencias y votos conservadas en el mismo inventario.
- Quien consolida concilia contra el inventario, ejecuta el QUALITY_GATE y es el único que declara cobertura y prepara el correo. Ningún subagente envía, publica ni declara cobertura final.

## /goal
```
/goal Entrega DOF del [fecha]: docs/QUALITY_GATE.md cumplido, inventario sin huecos, cuatro archivos renderizados y revisados, enlaces comprobados y correo a Emi verificado en Enviados; si algo falta, bloqueo PARCIAL explícito con faltantes exactos.
```
```
/goal SJF del viernes [fecha]: inventario conciliado, cada documento INTEGRO con rangos y notas, `sjf_weekly audit` sin discrepancias y control persistido en privado/; sin correo.
```

## /loop
```
/loop 2h Revisa en el índice oficial DOF/SIDOF si hoy hay edición vespertina, extraordinaria o fe de erratas no inventariada; si la hay, agrégala al inventario y avísame. Registra la hora real de la consulta. Detente después de las 23:00.
```
`/loop` dura mientras la sesión esté abierta (hasta 7 días). No envía nada; solo vigila e inventaría.

## Ejecución programada
[scripts/headless.sh](../scripts/headless.sh) trae ejemplos de `claude -p` para martes, jueves y viernes con `--permission-mode dontAsk` y herramientas mínimas. **No se activa al instalar**: hay que programarlo (tarea programada de Claude Code, cron con `CRON_TZ=America/Mexico_City` o el programador del sistema). El workflow `.github/workflows/tests.yml` solo corre pruebas; no conviene usarlo para el DOF porque exigiría credenciales de Gmail y material privado en un repositorio público. El prompt programado nunca escribe a terceros: solo a Emi, y el hook lo vigila.

## Navegador
- Claude in Chrome (tu Chrome, con tus sesiones): para dof.gob.mx, SIDOF y el SJF cuando la descarga automática falla, hay 403 o el portal responde «navegador desactualizado». Aplicar antes el [protocolo de desbloqueo](desbloqueo.md) y solo después pedir archivos a Emi.
- Playwright (navegador aparte): para renderizar y revisar el PDF y el HTML del correo antes de enviar.
- Nunca para eludir accesos, captchas ni restricciones del portal.

## En la sesión
- `/context`: ver cuánto ocupa la sesión antes de una lectura larga.
- `/compact <foco>`: resumir conservando inventario, rangos y pendientes (ej. `/compact inventario y pendientes del martes`).
- `/clear`: empezar una entrega nueva sin arrastrar la anterior.
- `/rewind` (o Esc Esc): volver a un punto previo si un cambio salió mal.
- `/btw`: preguntar algo sin meterlo en la conversación principal.
- `!comando`: correr en la terminal, por ejemplo `!python3 -m src.dof_monitor.sjf_weekly audit --control ...`.
- `/remote-control`: seguir desde el teléfono una ejecución larga.
