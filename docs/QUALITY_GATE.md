# Quality Gate

## Cobertura
- [ ] Fechas correctas.
- [ ] Todas las ediciones.
- [ ] Vía documentada.
- [ ] Universo cerrado o pendiente exacto.
- [ ] Lectura íntegra si se declara completa.
- [ ] Anexos revisados.

## Jurídico
- [ ] Fuente oficial.
- [ ] Fecha/autoridad.
- [ ] Vigencia/transitorios.
- [ ] Sujetos/excepciones/cifras.
- [ ] Antes/después solo si comparado.
- [ ] Iniciativa ≠ norma.
- [ ] Sentencia ≠ jurisprudencia.
- [ ] Caso ≠ regla general.

## Editorial
- [ ] Solo contenido útil.
- [ ] Sin repetición.
- [ ] Lenguaje natural/profesional.
- [ ] Enlaces abiertos.
- [ ] Despacho separado de material interno.

## Archivos/acciones
- [ ] Archivos existen y abren.
- [ ] PDF legible/seleccionable.
- [ ] DOCX editable.
- [ ] Enlaces funcionales.
- [ ] No prometer adjuntos inexistentes.
- [ ] No enviar a tercero sin aprobación.


## Control DOF + SJF integrado (adición 2026-10-20)
- [ ] Inventarios DOF y SJF separados, conciliados con índices oficiales y paginaciones sin huecos.
- [ ] Cada documento y anexo con evidencia de lectura completa, notas específicas y fuente primaria verificable; el validador sólo comprueba campos declarados, nunca lectura real.
- [ ] Tesis aislada, sentencia, voto y jurisprudencia identificados correctamente; obligatoriedad, fecha, votación, ámbito y efectos cotejados con fuente y régimen temporal.
- [ ] Manifiesto conforme a `schemas/evidence-manifest.schema.json` y control de rangos contiguos sin solapamientos.
- [ ] Cuatro archivos reales renderizados, inspeccionados y sus SHA-256 calculados externamente y cotejados.
- [ ] Gmail: destinatario personal único, duplicados y tentativas revisados, estado inequívoco; ante `ENVIO_INCIERTO` no reenviar.
- [ ] Ejecución de controles en la ruta real de generación/envío, no únicamente en pruebas unitarias; de lo contrario marcar integración pendiente.

## Matriz de auditoría por día — 20/10/2026
- [ ] Martes: se acreditan **por separado** DOF y SJF; exactamente cuatro archivos conjuntos, sin duplicación y fecha SJF original del viernes.
- [ ] Jueves: universo y contenido exclusivamente DOF; ningún hallazgo, sección o corrección SJF. Cuatro archivos DOF.
- [ ] Viernes: preparación SJF interna sin correo de rutina; preservar inventario y control recuperable.
- [ ] Un SJF parcial bloquea el cierre conjunto del martes, pero **no** el DOF autónomo del jueves.
- [ ] Comprobar destinatario, duplicados, versión de archivos y estado de envío por día y tipo de paquete.
