# Control técnico DOF + SJF (propuesta de auditoría)

El módulo SJF y el parche independiente 1.2.0 no son equivalentes. Este cambio introduce validaciones conservadoras en `quality.py`, sin modificar el calendario ni enviar correos.

## Alcance y límites

`evidence_gaps` exige manifiestos separados DOF y SJF, inventario cerrado, registros íntegros, URL, páginas/rangos, notas de lectura y verificación explícita de anexos. `can_release_package` añade aprobación de auditoría y cuatro archivos renderizados con identificador SHA-256. `can_attempt_send` exige destinatario personal, revisión de duplicados y estado NOT_SENT.

**Importante:** estas funciones no prueban que las páginas realmente hayan sido leídas; sólo revisan la estructura y los campos declarados. El control jurídico de obligatoriedad, fechas, votos, fuentes primarias y régimen temporal sigue siendo obligatorio y requiere revisión humana. La verificación criptográfica de archivos y la inspección visual deben realizarse externamente; el campo sha256 por sí solo no verifica el contenido.

Las funciones son controles de apoyo y no se conectan automáticamente al envío Gmail ni al motor de producción. No afirmar automatización integral hasta integrar la ruta de ejecución, pruebas de integración y evidencia real.

## Pendientes antes de producción

- Especificar y validar esquema JSON versionado del manifiesto y cobertura real de páginas sin huecos.
- Probar referencias cruzadas, jurisprudencia/tesis aislada, votos, obligatoriedad y transitorios.
- Integrar el bloqueo al proceso real de generación/envío y auditar idempotencia ante respuestas ambiguas.
- Verificar seguridad y protección de main desde un acceso con permisos suficientes.
- Auditar la documentación histórica sin reescribir registros fechados.
- Mantener el parche 1.2.0 separado hasta su aplicación expresamente autorizada.

No usar el resultado de CI como certificación jurídica de lectura exhaustiva.
