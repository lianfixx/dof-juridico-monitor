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

1. **La cobertura la arma el código.** Cada edición nueva y cada anexo se parte en bloques de páginas consecutivas (30 por defecto, menos si el texto es muy denso), sin huecos ni solapamientos. Toda página viaja en exactamente un bloque; el modelo no decide qué leer. Al final se comprueba que las notas cubran todas las páginas: lo que falte queda como `SIN_NOTA`.
2. **Líneas finales.** Cada respuesta copia la última línea del bloque y el código la busca entre las ocho últimas líneas con contenido (un número de página debe ser idéntico; una línea larga puede ser parte de una o casi igual, por el OCR). Si no está, repite una vez; si vuelve a fallar, el bloque queda con problema y la entrega en `PARCIAL`.
3. **Respuesta cortada.** Si la respuesta se corta por longitud (páginas con muchas publicaciones pequeñas), el bloque se parte en dos mitades por páginas completas y cada una se lee aparte, hasta tres veces. El bloque original queda como `DIVIDIDO`, con sus partes.
4. **Bloque con texto y sin publicaciones.** No pasa: se repite.
5. **Citas literales.** Cada cita que sustenta una nota se busca en el texto del bloque. La que no aparece se quita y se cuenta.
6. **Códigos de nota.** Solo valen los del índice oficial de la edición. Un código que no está ahí se borra; las URL salen del índice, nunca del modelo.
7. **Cruce con el índice.** Los títulos del índice oficial que ninguna nota recogió quedan listados en el preliminar para leerse en el cierre.
8. **OCR.** A las páginas marcadas para OCR se les agrega su texto reconocido. Una página sin texto que no pasó por OCR deja la entrega en `PARCIAL`.
9. **Nada tumba la corrida.** Un error en un bloque queda en su nota; `ESTADO_API.json` se escribe siempre, también ante un error inesperado (`ERROR_INTERNO`).

`INTEGRO` significa que todos los bloques pasaron esas comprobaciones. No significa «COBERTURA COMPLETA AL CORTE»: eso lo declara solo la sesión que cierra, con `docs/QUALITY_GATE.md`.

## Qué arma el código y qué redacta el modelo

El preliminar tiene cuatro partes. Tres las arma el programa, sin modelo: el control de cobertura, **«Por verificar en el cierre»** (bloques con problema, páginas sin texto ni OCR, títulos del índice sin nota, citas no localizadas, notas sin código, páginas sin publicación anotada) y el **«Inventario por edición»** (todas las publicaciones anotadas; los trozos de una misma nota partida entre bloques se unen). Un bloque de pura continuación no trae título: su trozo toma el código de la publicación que venía abierta del bloque anterior, se cuenta en `codigos_heredados` y se avisa para confirmarlo; el archivo de la nota conserva lo que respondió el lector.

El modelo de síntesis solo redacta **«Candidatas a la tabla del reporte»** y **«Avisos secundarios para la guía»**, y solo recibe las notas de relevancia alta o media (completas) y baja (abreviadas). Si las notas no cambiaron desde la corrida anterior, se conserva la síntesis de entonces (`notas/SINTESIS_API.md`) y no se paga otra.

## Modelos y costo

- Lectores: Sonnet 5.5. Síntesis del preliminar: Opus 5.5. Se cambian con `--modelo-lector` y `--modelo-sintesis`.
- **Lote a mitad de precio.** Los bloques pendientes viajan juntos en un lote (Message Batches de la API: 50 % de descuento en todos los tokens; la mayoría termina en menos de una hora). Se espera hasta `--espera-lote` minutos (35 por defecto); si no terminó, se cancela, se aprovecha lo que sí alcanzó a responder y el resto se lee con llamadas directas, a precio normal. Lo que el lote devolvió con error, cortado o sin pasar la comprobación también se repite con llamada directa. Si no se puede saber si el lote existe o cobró (sin respuesta al crearlo o al consultarlo), **no** se repite con llamadas directas, para no pagar dos veces: la entrega queda `PARCIAL` (`LOTE_SIN_TERMINAR`) y la suscripción hace el trabajo. `--sin-lote` lee todo con llamadas directas.
- Tope por corrida: `--max-usd` (8 por defecto). Si se alcanza, deja de llamar y la entrega queda `PARCIAL`. Todo lo que la API cobra cuenta, también las respuestas cortadas o fallidas.
- Medición real del 23/11/2026 (periodo del viernes 20 al lunes 23: 9 documentos, 1 128 páginas, 75 bloques, con llamadas directas): 9.07 USD por 71 bloques, de los cuales cerca de 1.50 fueron repeticiones que la segunda versión ya no hace. Estimado del mismo periodo en lote: 4.33 USD de lectura. Las tablas numéricas densas (por ejemplo, los precios promedio del INPC) pesan: 24 bloques de cinco páginas.
- Tope mensual: el espacio de trabajo `castorena-dof` de Claude Console (60 USD, aviso a los 30). Sin recarga automática: si el crédito se acaba, el lector se detiene y la sesión de la suscripción hace el trabajo completo.
- El costo real de cada corrida queda en `ESTADO_API.json`.

## Qué deja, en `fuentes/<entrega>/` del repositorio privado

```
dof/inventario.json, dof/raw/*.txt, *.paginas.json, *.ocr.txt, dof/anexos/*.txt   fuentes (los PDF no se guardan: se vuelven a bajar y su SHA-256 queda en el inventario)
notas/<documento>_pNNNN-NNNN.json y .md   una nota por bloque, con sus comprobaciones y su uso (tokens, costo, lote o directo)
notas/PRELIMINAR_API.md                   control de cobertura, por verificar, candidatas, secundarios e inventario
notas/SINTESIS_API.md                     lo que redactó el modelo de síntesis (se reutiliza si las notas no cambian)
ESTADO_API.json                           estado, páginas, bloques, lote, tokens, costo de lectura y de síntesis, modelos y SHA-256 de cada PDF leído
```

## Relevo con la sesión de la suscripción

Fase de sombra (vigente): el lector por API corre a las 20:00 y la tarea «lector nocturno» de la suscripción corre a las 21:41 **sin cambios**, como si el lector por API no existiera. Se comparan las dos lecturas en al menos cuatro entregas.

Después de la sombra, y solo con aprobación de Emi, la tarea de las 21:41 empezará por leer `ESTADO_API.json` y el preliminar: con `INTEGRO` y los mismos SHA-256 que el inventario del box, verifica por muestreo, lee los títulos «por verificar» y continúa; con `PARCIAL`, sin archivo o con SHA-256 distintos, hace la lectura completa como hoy. La tarea de la suscripción nunca se apaga.

## Primera corrida real y lo que cambió (23/11/2026)

La primera corrida real leyó 71 de 75 bloques y se cayó antes de escribir el estado. La falla quedó donde debía (corrida en rojo, la suscripción hizo el trabajo esa noche), y dejó cinco hallazgos que la versión 2 del lector corrige, cada uno con su prueba:

| Hallazgo | Corrección |
|---|---|
| Dos respuestas cortadas por longitud dejaron una nota sin lectura y el programa se cayó al escribirla | Ningún bloque tumba la corrida; el estado se escribe siempre |
| Esas respuestas cortadas se repetían igual y se pagaban sin contarse | Se parte el bloque en mitades; todo lo cobrado cuenta |
| Cuatro bloques de anexos fallaron la «última línea» porque la última línea era el número de página o texto de OCR | Comprobación contra las líneas finales; las notas anteriores se revalidan sin nueva llamada |
| Costo cercano al tope (9 USD) | Lote a mitad de precio; el inventario y los pendientes los arma el código; la síntesis se reutiliza |
| 44 notas sin código: bloques de pura continuación, sin título | El trozo hereda el código de la publicación que venía abierta, con aviso |

## Lo que este lector nunca hace

Enviar correos, escribir en este repositorio público material de trabajo, inventar URL o códigos, declarar cobertura completa, leer el Semanario, tocar el box o cambiar tareas programadas.
