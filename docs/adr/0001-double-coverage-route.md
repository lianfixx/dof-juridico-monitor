# ADR 0001 — Doble vía de cobertura

Estado: Accepted · 2026-10-02

## Contexto
El enlace visual al PDF del DOF puede no exponer el archivo real a todas las herramientas. Depender solo de PDF o solo de búsquedas genera falsos positivos.

## Decisión
Vía A: PDF completo real cuando pueda abrirse y recorrerse.
Vía B: índice + cada publicación + colecciones secundarias y paginación oficial.

## Consecuencia
Cobertura completa solo si una vía cierra el universo sin huecos. Nunca se afirma lectura de un PDF no abierto.
