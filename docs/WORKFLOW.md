# Workflow

1. Resolver fechas exactas.
2. Identificar todas las ediciones.
3. Intentar vía A.
4. Si falla, ejecutar vía B.
5. Construir inventario antes de filtrar.
6. Leer íntegramente si se pretende cobertura completa.
7. Registrar bitácora.
8. Filtrar relevancia.
9. Re-verificar cada dato decisivo.
10. Comprobar agenda legislativa/iniciativas en fuentes oficiales.
11. Redactar solo al cerrar investigación o pendientes.
12. Generar reporte y guía.
13. Ejecutar Quality Gate.
14. Generar/verificar archivos y enlaces.
15. Preparar correo.
16. Enviar solo al operador configurado; destinatario final requiere aprobación.
17. Registrar cambios.

## Bitácora
fecha, edición, vía, colección, emisor, título, identificador, URL, páginas/rangos, anexos, estado, incluido/excluido, motivo.

Estados: INTEGRO, PARCIAL, PENDIENTE, INACCESIBLE.


## Integración semanal SJF (adición 2026-10-20)
Leer `docs/sjf/METODO.md` y `SKILL.md`. Viernes: inventario oficial SJF, lectura íntegra y control independiente. Martes: recuperar control y cuatro archivos SJF persistidos, comprobar corte y novedades, integrar en los cuatro archivos DOF sin duplicarlos. Jueves: sólo correcciones posteriores comprobadas. Mantener fechas y coberturas distintas.

Antes de cualquier cierre o envío, verificar manualmente evidencia primaria y usar el manifiesto de `schemas/evidence-manifest.schema.json`; `evidence_gaps`, `can_release_package` y `can_attempt_send` son controles auxiliares no conectados todavía al motor de ejecución. Nunca asumir que CI acredita lectura real, obligatoriedad o aceptación de Gmail.
