# Lector por API (créditos de Claude)

Complemento de [SKILL.md](../SKILL.md) y de [Fuentes con el box](box.md), en operación desde el 23 de noviembre de 2026 (primero en prueba y, desde esa misma noche, en relevo con la suscripción). No cambia el método jurídico, la lectura íntegra, las compuertas, el destinatario único ni los cierres: agrega un **lector previo** que corre con los créditos de API de Emi, sin gastar los límites de su suscripción, y deja notas para que la sesión que cierra las verifique.

## Qué es y qué no es

| | Lector por API | Sesión de Claude (suscripción) |
|---|---|---|
| Dónde corre | Servidor de GitHub, en el repositorio privado `lianfixx/dof-trabajo` | Nube de Claude, con el box |
| Qué hace | Baja el DOF, lo parte en bloques, anota cada publicación y redacta un preliminar | Comprueba el relevo, lee lo que la API no dejó perfecto y la edición del día, hace la doble lectura, aplica el criterio jurídico, audita, arma el paquete y envía a Emi |
| Semanario | No lo baja ni lo lee | Sí (tarea del viernes, con el box) |
| Correo | Nunca | Solo a Emi |
| Quién declara la cobertura | Nadie: su estado es `INTEGRO` o `PARCIAL` técnico | La sesión que cierra, con las compuertas de siempre |

El material (fuentes, notas, preliminar) vive en el repositorio **privado**; en este repositorio público solo está el código.

## Piezas

- `scripts/api/fuentes_api.sh`: mismo periodo que `fuentes.sh` del box, con `dof_fuentes.py`, `paginas.py` y `ocr.py`. Comprobado el 23/11/2026: un servidor de GitHub bajó el periodo del 3 de noviembre (ediciones 297 a 300, 544 páginas, 4 anexos) con SHA-256 idénticos a los del box.
- `scripts/api/lector_api.py`: el lector. Pruebas en `tests/test_lector_api.py`.
- Workflow `lector-api.yml` del repositorio privado: corre lunes y miércoles por la tarde (hora del centro de México) y a mano. Lo lanza la tarea programada de Claude «DOF · lanzar el lector por API» a las 19:17, con reintento a las 20:17; si falta, el lector nocturno a las 21:41. El reloj de GitHub (líneas `cron` de 19:17 y 20:37) queda solo como tercera red, porque dispara con horas de retraso o no dispara; si su corrida llega fuera de lunes o miércoles, el trabajo «reloj» del workflow la termina sin leer, sin gastar y sin abrir aviso. Una corrida repetida no vuelve a pagar lo ya leído. Si una corrida no queda íntegra abre el issue «Lector del DOF por API: la corrida no quedó íntegra», que se cierra solo cuando otra sale bien.
- Tarea programada de Claude «DOF · guardia del lector por API» (martes y jueves 11:23, Opus 5.5): revisa las corridas de la víspera; si hubo una falla del código la repara de fondo (prueba que falla, corrección, pull request; para reparar usa un subagente con Fable y, si no está disponible, Opus), y durante la sombra compara la entrega con la lectura de la suscripción en `sombra/` del repositorio privado. No toca tareas programadas ni el box, y no envía correos.

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

El modelo de síntesis solo redacta **«Candidatas a la tabla del reporte»** y **«Avisos secundarios para la guía»**, y solo recibe las notas de relevancia alta o media (completas) y baja (abreviadas), una unidad por publicación con todos sus trozos. Redacta por grupos pequeños (45 000 caracteres de notas por llamada) y el programa une los resultados en esas dos secciones; si una respuesta se corta, ese grupo se redacta de nuevo en dos mitades. Como cada grupo ve solo una parte de las notas, el redactor tiene prohibido escribir que algo «no hay» o «no viene», y el programa descarta al unir las afirmaciones de ausencia que aun así aparezcan («Ninguna nota de la edición…», «las notas no incluyen…»): serían falsas para la entrega completa. Lo que una ficha dice de su nota («no consta») se conserva, y una sección que queda vacía no se imprime. Si las notas no cambiaron desde la corrida anterior, se conserva la síntesis de entonces (`notas/SINTESIS_API.md`) y no se paga otra.

## Modelos y costo

- Lectores: Sonnet 5.5. Síntesis del preliminar: Opus 5.5. Se cambian con `--modelo-lector` y `--modelo-sintesis`.
- **Tablas numéricas: Haiku 5.5** (`--modelo-tablas`; con el mismo modelo que el lector se apaga). Solo para bloques que cumplen tres condiciones a la vez, decididas por el código: todas sus páginas tienen al menos 90 % de dígitos entre dígitos y letras, no aparece ninguna palabra normativa (artículo, transitorio, acuerdo, decreto, aviso, vigencia y similares) y no aparece ningún título del índice oficial. Medido en las 1 128 páginas reales del 23/11/2026: los 24 bloques de precios promedio del INPC dan 0.99 en todas sus páginas y ninguno más pasa (el siguiente más alto da 0.53). Doble seguro: si la nota del modelo barato trae más de dos trozos, algo de relevancia alta o media, o falla, el bloque lo relee el modelo lector. Baja la lectura de una entrega como esa de 4.34 a 2.99 USD estimados.
- **Lote a mitad de precio.** Los bloques pendientes viajan juntos en un lote (Message Batches de la API: 50 % de descuento en todos los tokens; la mayoría termina en menos de una hora). Se espera hasta `--espera-lote` minutos (35 por defecto); si no terminó, se cancela, se aprovecha lo que sí alcanzó a responder y el resto se lee con llamadas directas, a precio normal. Lo que el lote devolvió con error, cortado o sin pasar la comprobación también se repite con llamada directa. Si no se puede saber si el lote existe o cobró (sin respuesta al crearlo o al consultarlo), **no** se repite con llamadas directas, para no pagar dos veces: la entrega queda `PARCIAL` (`LOTE_SIN_TERMINAR`) y la suscripción hace el trabajo. `--sin-lote` lee todo con llamadas directas.
- Tope por corrida: `--max-usd` (8 por defecto). Si se alcanza, deja de llamar y la entrega queda `PARCIAL`. Todo lo que la API cobra cuenta, también las respuestas cortadas o fallidas.
- Medición real del 23/11/2026 (periodo del viernes 20 al lunes 23: 9 documentos, 1 128 páginas, 75 bloques, con llamadas directas): 9.07 USD por 71 bloques, de los cuales cerca de 1.50 fueron repeticiones que la segunda versión ya no hace. Estimado del mismo periodo en lote: 4.33 USD de lectura. Las tablas numéricas densas (por ejemplo, los precios promedio del INPC) pesan: 24 bloques de cinco páginas.
- Mismo día, versión 2: releer solo lo pendiente (6 bloques, lote terminado en 142 s) costó 2.07 USD; la síntesis completa, 0.96 USD (Opus, 5 grupos). Repetir una entrega ya leída y sin cambios cuesta 0.
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

## Relevo con la suscripción (vigente desde la noche del 23/11/2026)

Decisión de Emi del 23/11/2026: se acabó la sombra. Lo que el lector por API deja perfecto no se vuelve a leer con la suscripción; lo que no, lo lee la suscripción como siempre. Nada se hace dos veces y la suscripción nunca se apaga.

**Quién decide.** Un programa, no un modelo: `scripts/api/relevo.py comprobar`. Compara, documento por documento (cada edición nueva y cada anexo aparte), lo que el box bajó (`python3 bin/relevo_lista.py <entrega>`) con `ESTADO_API.json`. Un documento queda `por_api` solo si es el mismo PDF (mismo SHA-256), tiene las mismas páginas y el lector lo dejó íntegro (todos sus bloques comprobados, sin huecos, sin páginas sin texto ni OCR). Cualquier otra cosa queda `por_suscripcion` con su motivo. Veredicto: `TOTAL`, `PARCIAL` o `NINGUNO`.

**Lanzador (lunes y miércoles 19:17 y 20:17).** El reloj de GitHub no sirve para nada que tenga hora límite. Medido el 23/11/2026: en `lianfixx/MATRIZ`, de una programación de cada 15 minutos, GitHub disparó 39 corridas en 12 días (de unas 1,100), con huecos de 5 a 9 horas; en `dof-trabajo`, `Cerebro-Castorena-` e `INDEP`, las programaciones nuevas no habían disparado ninguna. La causa no es quién firmó el commit (hipótesis descartada el mismo día): las corridas programadas de MATRIZ salen a nombre de `lianfixx` aunque el `cron` lo subió una sesión de Claude. GitHub lo documenta: las corridas programadas pueden retrasarse y, con carga alta, descartarse. Por eso el workflow lo lanza la tarea programada de Claude «DOF · lanzar el lector por API» (Haiku 5.5, creada el 23/11/2026 con autorización expresa de Emi; texto en `prompts/api/lanzador-api.md`): a las 19:17 lo lanza si no hay una corrida válida (en curso o terminada con éxito) en los últimos 90 minutos, y a las 20:17 repite la comprobación, que hace de reintento si la primera falló. El reloj de GitHub se conserva porque es la única red que no depende de la suscripción de Claude.

**Noche (lector nocturno, 21:41).** Baja las fuentes al box como siempre y corre la comprobación. Si no es `TOTAL` porque el lector por API no corrió (GitHub puede retrasar u omitir una corrida programada: pasó el 23/11/2026), no terminó o no vio un documento nuevo, lo lanza una vez y lo espera hasta 50 minutos. De lo que quede `por_api` revisa una muestra de control (dos candidatas leídas en el box contra su nota); si un dato es falso, anula el relevo. Lee íntegro lo que quede `por_suscripcion`. Deja en el box `fuentes/<entrega>/notas/RELEVO_API.json` con el veredicto, la muestra de control y `anulado`: `true` significa que la muestra falló y no hay relevo; `false` o ausente, que el relevo vale (en el texto de las tareas, «sin `anulado`» quiere decir que `anulado` no es `true`). La lista del box lleva una `huella`: si al pasarla a la sesión se copia con un error, `relevo.py` responde `LISTA_MAL_COPIADA` y hay que volver a copiarla; nunca puede salir un relevo falso por un error de copia.

**Cierre (martes 05:50, jueves 06:05).** Si hay `RELEVO_API.json`, vuelve a comprobar y toma del repositorio privado las notas y el preliminar de los documentos `por_api`; valen como las del lector nocturno. La edición del día y lo que no tenga nota se leen íntegros. Todo lo demás no cambia: compuertas, doble lectura, auditoría literal, auditor independiente, enlaces y envío solo a Emi.

**Evaluación en real.** La doble lectura del cierre (un lector que no ve la nota) es la prueba del lector por API: cada diferencia se registra en la bitácora de la entrega (`lectura_api.diferencias`). El cierre revisa además lo que la API dejó con relevancia baja o ninguna de autoridades fiscales, financieras, de prevención de lavado y jurisdiccionales. La tarea «DOF · guardia del lector por API» (martes y jueves 11:23; procedimiento en [guardia.md](guardia.md)) reúne esas diferencias en `sombra/` del repositorio privado y, si el lector omitió algo relevante, propone el ajuste (por ejemplo, lectores Opus).

**Regla de sincronía (Emi, 23/11/2026).** Toda mejora o cambio del método vale para las dos vías: el lector por API y las tareas de la suscripción. Un cambio se hace en el mismo commit en `scripts/api/`, `prompts/tareas/`, `references/` y `SKILL.md`, y después se actualiza el texto de las tareas programadas. `tests/test_sincronia.py` falla si se separan.

## Primera corrida real y lo que cambió (23/11/2026)

La primera corrida real leyó 71 de 75 bloques y se cayó antes de escribir el estado. La falla quedó donde debía (corrida en rojo, la suscripción hizo el trabajo esa noche), y dejó cinco hallazgos que la versión 2 del lector corrige, cada uno con su prueba:

| Hallazgo | Corrección |
|---|---|
| Dos respuestas cortadas por longitud dejaron una nota sin lectura y el programa se cayó al escribirla | Ningún bloque tumba la corrida; el estado se escribe siempre |
| Esas respuestas cortadas se repetían igual y se pagaban sin contarse | Se parte el bloque en mitades; todo lo cobrado cuenta |
| Cuatro bloques de anexos fallaron la «última línea» porque la última línea era el número de página o texto de OCR | Comprobación contra las líneas finales; las notas anteriores se revalidan sin nueva llamada |
| Costo cercano al tope (9 USD) | Lote a mitad de precio; el inventario y los pendientes los arma el código; la síntesis se reutiliza |
| 44 notas sin código: bloques de pura continuación, sin título | El trozo hereda el código de la publicación que venía abierta, con aviso |
| Segunda corrida (versión 2, `INTEGRO`, 2.07 USD): la síntesis se cortó por longitud con 138 000 caracteres de notas | Síntesis por grupos pequeños, unida por el programa; entradas más breves |
| Las páginas de edictos y convocatorias producían notas enormes (hasta 14 000 tokens por seis páginas) y cortes | Nota mínima para edictos, convocatorias y avisos de particulares de relevancia baja o ninguna |
| 24 de 75 bloques eran tablas de pura cifra leídas con el modelo lector | Las lee el modelo barato, con relectura por el lector ante cualquier duda |

## Lo que este lector nunca hace

Enviar correos, escribir en este repositorio público material de trabajo, inventar URL o códigos, declarar cobertura completa, leer el Semanario, tocar el box o cambiar tareas programadas.
