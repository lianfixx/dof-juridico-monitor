# ADR 0006 · Lector previo por la API de Claude

Fecha: 2026-11-23. Estado: en prueba (sombra), a petición de Emi («sacar tareas pesadas de los límites de la suscripción con los créditos de API; el DOF es prioridad»).

## Necesidad

El lector nocturno es la tarea más pesada de la suscripción y falló por límite de uso el 9 y el 11 de noviembre de 2026. Emi tiene 100 USD mensuales de créditos de API que no se pueden gastar dentro de Claude.

## Decisión

Un lector previo determinista (`scripts/api/lector_api.py`) corre en un servidor de GitHub, en un repositorio privado, antes que la tarea de la suscripción. El código, no el modelo, reparte las páginas; cada respuesta se comprueba (última línea, citas literales, códigos del índice) y lo que no se comprueba se descarta. La sesión de la suscripción conserva el criterio, la auditoría, las compuertas y el envío, y nunca se apaga.

## Alternativas descartadas

- **Correr la skill entera con `claude -p` en GitHub.** Depende de conectores (box, Gmail) que solo existen dentro de Claude, su costo es menos predecible y la cobertura dependería de que el agente decida leer todo.
- **La Action oficial `claude-code-action`.** Anthropic la cuenta como uso de Claude Code: no gasta créditos de API.
- **Guardar las notas en este repositorio.** Es público; el material de trabajo nunca va aquí.
- **Bajar el Semanario desde GitHub.** El portal no responde a servidores de centros de datos y no hay vía oficial para programas; rodear su muro anti-bots no es aceptable. El Semanario sigue en el box.

## Actualización del 23/11/2026: lote y síntesis acotada

La primera corrida real costó 9.07 USD por 71 de 75 bloques con llamadas directas: dos entregas por semana a ese precio agotan el espacio de trabajo (60 USD al mes). Se decide leer por lote (Message Batches, 50 % de descuento) con un plazo: si el lote no termina en 35 minutos se cancela y lo que falte se lee con llamadas directas, de modo que el lector siempre termina antes que la tarea de la suscripción. Ante la duda de si un lote cobró, no se repite. El inventario y los pendientes pasan a armarse con código; el modelo de síntesis solo redacta candidatas y secundarios.

Descartado por ahora: mandar las tablas numéricas densas a un modelo más barato. Ahorraría cerca de 1 USD en las entregas que traen el INPC, a cambio de una regla más que puede clasificar mal una página; se revisa con los datos de la sombra.

## Consecuencias

- Redundancia real entre proveedores de cómputo: si la API falla o se acaba el crédito, la suscripción hace el trabajo; si la suscripción llega a su límite, las notas del lector ya existen.
- Un repositorio privado más (`lianfixx/dof-trabajo`) y una llave de API como secreto de ese repositorio.
- El relevo (que la tarea de las 21:41 parta de las notas) se decide con datos, después de cuatro entregas en sombra.
