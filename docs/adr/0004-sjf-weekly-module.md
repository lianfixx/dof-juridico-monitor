# ADR 0004 · Incorporar el Semanario al seguimiento jurídico

Fecha: 2026-10-15. Estado: método aprobado por el usuario; incorporación a main sujeta al pull request correspondiente.

## Necesidad

El seguimiento del DOF necesita complementarse con criterios judiciales y material de estudio personal. El usuario exige rigor exhaustivo y una explicación humana, clara y amena.

## Decisión

Añadir un módulo SJF documentado y plantillas compatibles con los cuatro entregables existentes. Usar viernes por la tarde para iniciar su revisión y martes para integrar una síntesis útil al DOF, conforme a la recomendación aceptada por el usuario. La hora de inicio no garantiza una hora de cierre.

Mantener separados inventario oficial, lectura comprobada, selección, estudio y opinión. Separar fechas de resolución, publicación, obligatoriedad y efectos. TFJA/TEPJF conservan cobertura propia. Documentar el perfil general; mantener datos de clientes y continuidad de correos en destinos privados.

## Consecuencias

- La lectura íntegra precede a la selección, aunque el reporte ejecutivo sea breve.
- La tarea del martes necesita el control persistente del viernes y revalidación al nuevo corte.
- El repositorio conserva instrucciones; el programador y Gmail acreditan respectivamente activación y envío.
- El módulo es una extensión documental sin cambios al código o schemas actuales. Su integración no acredita capacidad automática de descargar ni leer íntegramente el SJF.
- Se publica en una rama independiente del parche DOF 1.2.0. No se aplica ese parche ni se afirma que sus 16 pruebas hayan corrido.

## Alternativa descartada

Seleccionar sólo por rubros o buscadores y llamar completo al resultado incumpliría las reglas expresas del usuario. Los resúmenes externos pueden orientar búsquedas, pero no sustituyen el universo ni las fuentes oficiales.
