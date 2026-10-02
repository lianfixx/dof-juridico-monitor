# Versionado y mantenimiento

Se usa SemVer: MAJOR.MINOR.PATCH.

- MAJOR: cambia reglas fundamentales, schemas incompatibles o definición de cobertura.
- MINOR: nueva capacidad compatible (nuevo adaptador, nuevo entregable, fuente adicional).
- PATCH: corrección de prompt, redacción, bug o validación sin romper compatibilidad.

Cada cambio:
1. modificar archivos;
2. actualizar/crear tests;
3. actualizar CHANGELOG;
4. crear ADR si cambia arquitectura;
5. commit descriptivo;
6. opcionalmente tag/release.

GitHub es la fuente de verdad. Las conversaciones con cualquier IA son transitorias.
