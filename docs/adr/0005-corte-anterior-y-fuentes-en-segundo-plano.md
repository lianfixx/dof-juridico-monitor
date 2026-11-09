# ADR 0005 · Periodo desde el corte anterior y fuentes del box en segundo plano

Fecha: 2026-11-09. Estado: aplicado (skill 1.2.1), a petición de Emi («audita, mejora y deja todo perfecto»).

## Necesidad

La auditoría del 9/11/2026 sobre la skill 1.2.0 encontró cuatro riesgos en las fuentes del box:

1. **Huecos entre cortes.** Los periodos eran «viernes a martes» y «miércoles a jueves», pero el martes cierra a las 05:50 y el jueves a las 06:05: sus vespertinas y extraordinarias se publican después de cerrar y no entraban en ningún periodo. Las tareas las bajaban con `fuentes.sh dof <fecha>` a la carpeta de la entrega anterior, fuera del paquete siguiente, y la comprobación de números consecutivos (solo dentro de la entrega) no lo detectaba.
2. **OCR incompleto.** Solo pasaban por OCR las páginas con menos de 80 caracteres de texto. En la matutina del 06/11/2026, 30 páginas de formatos del SAT tenían texto (126 a 331 caracteres) y el formato completo en imagen; la página 10 tenía 9 renglones de texto y 45 en la imagen.
3. **Tope de 600 s del shell del box.** Un periodo con muchas páginas en imagen rebasa ese tope solo en OCR; al rebasarlo, la sesión del box se reinicia.
4. **Fallos silenciosos o que lo detienen todo.** Un fallo transitorio de `nota_to_pdf.php` (05/11/2026) abortaba la corrida sin guardar el inventario; el SJF ocultaba errores de detalle y anexos, y tras el muro anti-bots dejaba el control de una corrida anterior como si fuera el vigente.

## Decisión

- El periodo de cada entrega empieza en el día del cierre anterior (`--corte`). Lo que ese cierre ya cubrió se descarga solo para probar la continuidad de números y queda `ya_reportada` en el inventario (no se lee ni se reporta): lo que esté en el inventario de una entrega anterior del box y, si no la hay, la matutina de ese día. Así la compuerta 1 compara números desde la última edición ya reportada.
- `paginas_ocr` = páginas sin texto ∪ páginas con una imagen de al menos 300×100 px (`pdfimages -list`). El OCR corre dos páginas a la vez y es reanudable.
- Las tareas lanzan las fuentes con `bin/lanzar.sh` (proceso con `setsid`, que sobrevive al reinicio de la sesión) y consultan `bin/estado.sh` con llamadas cortas.
- Ningún paso detiene a los demás: los errores quedan en el inventario o el control, `estado.json` dice OK o CON_FALLOS, y el manifiesto publica `compuerta_fuentes` (`listo`, `faltantes`). El portal se reintenta con esperas ante respuestas inesperadas; el SJF recarga la página ante el muro anti-bots, marca su control EN_CURSO hasta terminar y trata el 404 de la lista de anexos como «sin anexos».
- El texto íntegro de las tareas programadas se versiona en `prompts/tareas/`.

## Consecuencias

- El inventario de una entrega es también el registro de lo reportado: si un cierre termina PARCIAL, la bitácora de esa entrega debe decir qué edición no entró, porque la siguiente la tomará por reportada. Lo resuelve la lectura de la bitácora en el cierre siguiente, no el script.
- Más páginas pasan por OCR (119 en lugar de 89 el 06/11/2026), con tiempo aceptable en segundo plano.
- `compuerta_fuentes.listo` es condición necesaria, no suficiente: la lectura completa, la doble lectura y la auditoría siguen siendo de la sesión.
