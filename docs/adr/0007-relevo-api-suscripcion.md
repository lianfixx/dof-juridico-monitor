# ADR 0007 · Relevo entre el lector por API y la suscripción

Fecha: 23 de noviembre de 2026. Estado: aceptado (decisión de Emi en chat: «si la API no lo hace de manera perfecta, ya entre mi suscripción, para no hacer lo mismo dos veces; ya ejecutemos todo a la realidad y evaluemos»).

## Contexto
El ADR 0006 dejó el lector por API en sombra durante cuatro entregas: las dos vías leían lo mismo. Emi decidió pasar a operación real el mismo día de la primera corrida íntegra.

## Decisión
1. El relevo lo decide un programa determinista (`scripts/api/relevo.py`), documento por documento, por SHA-256 del PDF, páginas e integridad registrada en `ESTADO_API.json`. Ningún modelo decide si una lectura «está bien».
2. La tarea «lector nocturno» de la suscripción sigue corriendo siempre: baja fuentes, comprueba, lanza el lector por API si GitHub no lo corrió, revisa una muestra y lee solo lo que no quedó `por_api`.
3. Los cierres toman las notas de la API del repositorio privado (no se copian al box) y siguen con todas las compuertas. La doble lectura sirve además de evaluación continua; las diferencias quedan en la bitácora.
4. Regla de sincronía: un cambio de método se hace a la vez en la vía de API y en la de suscripción, con una prueba que lo vigila.

## Alternativas descartadas
- Seguir en sombra cuatro entregas: más evidencia, pero doble trabajo y doble gasto; Emi prefirió evaluar en real con la suscripción como red.
- Copiar las notas de la API al box: unos 80 archivos por entrega escritos por un modelo, lento y caro; el cierre las lee directo del repositorio privado.
- Que el lector nocturno decida «a criterio»: no es reproducible.

## Consecuencias
- Una noche con relevo total, la suscripción ya no lee cientos de páginas: comprueba, muestrea y termina.
- Si GitHub, la API, el crédito o el código fallan, el veredicto es `NINGUNO` o `PARCIAL` y la suscripción lee como antes: la entrega no depende de la API.
- La calidad del lector por API se mide con las diferencias que encuentre la doble lectura; si omite algo relevante, se cambia el modelo lector o se vuelve a la lectura por suscripción.
