# ADR 0008 · Quién lanza el lector por API

Fecha: 23 de noviembre de 2026. Estado: aceptado (autorización de Emi en chat: «soluciona, tienes expreso mi sí de todo»).

## Contexto
El lector por API es un workflow de GitHub Actions en el repositorio privado `lianfixx/dof-trabajo`. Debe terminar antes de las 21:41 de lunes y miércoles, cuando empieza el lector nocturno de la suscripción. Se programó con el reloj de GitHub (`schedule`) y la primera noche no disparó. Medición del 23/11/2026: en `lianfixx/MATRIZ`, una programación de cada 15 minutos produjo 39 corridas en 12 días, de unas 1,100 esperadas, con huecos de 5 a 9 horas. GitHub documenta que las corridas programadas pueden retrasarse o descartarse. La primera hipótesis (que GitHub atara la programación a quien firmó el commit) quedó descartada: las corridas programadas de MATRIZ salen a nombre de `lianfixx`.

## Decisión
1. Lo lanza una tarea programada de Claude, «DOF · lanzar el lector por API» (Haiku 5.5), lunes y miércoles a las 19:17 y a las 20:17. Lanza el workflow solo si no hay una corrida válida en los últimos 90 minutos; la segunda hora hace de reintento. Su texto vive en `prompts/api/lanzador-api.md`.
2. El lector nocturno (21:41) sigue lanzándolo si falta, y espera hasta 50 minutos.
3. El reloj de GitHub se conserva como tercera red, porque es la única que no depende de la suscripción. Un trabajo previo del workflow («reloj») termina en verde, sin leer ni gastar, la corrida programada que GitHub dispare fuera de lunes o miércoles.
4. Nada con hora límite depende del reloj de GitHub, en este proyecto ni en los demás de Emi.

## Alternativas descartadas
- Dejar solo el reloj de GitHub: no dispara a tiempo.
- Que Emi edite el `cron` desde su cuenta: no cambia nada, porque la corrida ya sale a su nombre.
- Dejar solo al lector nocturno: funciona, pero su sesión espera hasta 50 minutos y gasta suscripción en esperar.
- Un servicio externo de reloj: otra cuenta y otra llave que cuidar, sin necesidad.

## Consecuencias
Dos tareas de la suscripción pueden lanzar el workflow; una corrida repetida no vuelve a pagar lo ya leído. Si la suscripción no pudiera correr sus tareas, queda el reloj de GitHub, tarde o nunca: en ese caso el lector por API se lanza a mano (`workflow_dispatch`).
