---
paths:
  - "src/**"
  - "tests/**"
  - "schemas/**"
---

Los controles son fail-closed: ante evidencia incompleta, bloquear. No debilitar una prueba para que pase. Todo cambio material actualiza CHANGELOG; los arquitectónicos requieren ADR en docs/adr/. Correr `python3 -m pytest -q` (el freno lo exige antes del commit).
