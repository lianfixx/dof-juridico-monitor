# Lector por API (créditos de Claude)

Complemento de [SKILL.md](../SKILL.md) y de [Fuentes con el box](box.md), en prueba desde el 23 de noviembre de 2026. No cambia el método jurídico, la lectura íntegra, las compuertas, el destinatario único ni los cierres: agrega un **lector previo** que corre con los créditos de API de Emi, sin gastar los límites de su suscripción, y deja notas para que la sesión que cierra las verifique.

## Qué es y qué no es

| | Lector por API | Sesión de Claude (suscripción) |
|---|---|---|
| Dónde corre | Servidor de GitHub, en el repositorio privado `lianfixx/dof-trabajo` | Nube de Claude, con el box |
| Qué hace | Baja el DOF, lo parte en bloques, anota cada publicación y redacta un preliminar | Verifica, lee lo que falte, aplica el criterio jurídico, audita, arma el paquete y envía a Emi |
| Semanario | No lo baja ni lo lee | Sí (tarea del viernes, con el box) |
| Correo | Nunca | Solo a Emi |
| Quién declara la cobertura | Nadie: su estado es `INTEGRO` o `PARCIAL` técnico | La sesión que cierra, con las compuertas de siempre |

El material (fuentes, notas, preliminar) vive en el repositorio **privado**; en este repositorio público solo está el código.

## Piezas

- `scripts/api/fuentes_api.sh`: mismo periodo que `fuentes.sh` del box, con `dof_fuentes.py`, `paginas.py` y `ocr.py`. Comprobado el 23/11/2026: un servidor de GitHub bajó el periodo del 3 de noviembre (ediciones 297 a 300, 544 páginas, 4 anexos) con SHA-256 idénticos a los del box.
- `scripts/api/lector_api.py`: el lector. Pruebas en `tests/test_lector_api.py`.
- Workflow `lector-api.yml` del repositorio privado: lunes y miércoles a las 20:00 (hora del centro de México) y a mano.

## Cómo garantiza la lectura

1. **La cobertura la arma el código.** Cada edición nueva y cada anexo se parte en bloques de páginas consecutivas (30 por defecto), sin huecos ni solapamientos. Toda página viaja en exactamente un bloque; el modelo no decide qué leer.
2. **Última línea.** Cada respuesta copia la última línea del bloque y el código la compara con la real. Si no coincide, repite una vez; si vuelve a fallar, el bloque queda con problema y la entrega en `PARCIAL`.
3. **Citas literales.** Cada cita que sustenta una nota se busca en el texto del bloque. La que no aparece se quita y se cuenta.
4. **Códigos de nota.** Solo valen los del índice oficial de la edición. Un código que no está ahí se borra; las URL salen del índice, nunca del modelo.
5. **Cruce con el índice.** Los títulos del índice oficial que ninguna nota recogió quedan listados en el preliminar para leerse en el cierre.
6. **OCR.** A las páginas marcadas para OCR se les agrega su texto reconocido. Una página sin texto que no pasó por OCR deja la entrega en `PARCIAL`.

`INTEGRO` significa que todos los bloques pasaron esas comprobaciones. No significa «COBERTURA COMPLETA AL CORTE»: eso lo declara solo la sesión que cierra, con `docs/QUALITY_GATE.md`.

## Modelos y costo

- Lectores: Sonnet 5.5. Síntesis del preliminar: Opus 5.5. Se cambian con `--modelo-lector` y `--modelo-sintesis`.
- Tope por corrida: `--max-usd` (8 por defecto). Si se alcanza, deja de llamar y la entrega queda `PARCIAL`.
- Tope mensual: el espacio de trabajo `castorena-dof` de Claude Console (60 USD, aviso a los 30). Sin recarga automática: si el crédito se acaba, el lector se detiene y la sesión de la suscripción hace el trabajo completo.
- El costo real de cada corrida queda en `ESTADO_API.json`.

## Qué deja, en `fuentes/<entrega>/` del repositorio privado

```
dof/inventario.json, dof/raw/*.txt, *.paginas.json, *.ocr.txt, dof/anexos/*.txt   fuentes (los PDF no se guardan: se vuelven a bajar y su SHA-256 queda en el inventario)
notas/<documento>_pNNNN-NNNN.json y .md   una nota por bloque, con sus comprobaciones
notas/PRELIMINAR_API.md                   control de cobertura, pendientes y preliminar
ESTADO_API.json                           estado, páginas, bloques, tokens, costo, modelos y SHA-256 de cada PDF leído
```

## Relevo con la sesión de la suscripción

Fase de sombra (vigente): el lector por API corre a las 20:00 y la tarea «lector nocturno» de la suscripción corre a las 21:41 **sin cambios**, como si el lector por API no existiera. Se comparan las dos lecturas en al menos cuatro entregas.

Después de la sombra, y solo con aprobación de Emi, la tarea de las 21:41 empezará por leer `ESTADO_API.json` y el preliminar: con `INTEGRO` y los mismos SHA-256 que el inventario del box, verifica por muestreo, lee los títulos «por verificar» y continúa; con `PARCIAL`, sin archivo o con SHA-256 distintos, hace la lectura completa como hoy. La tarea de la suscripción nunca se apaga.

## Lo que este lector nunca hace

Enviar correos, escribir en este repositorio público material de trabajo, inventar URL o códigos, declarar cobertura completa, leer el Semanario, tocar el box o cambiar tareas programadas.
