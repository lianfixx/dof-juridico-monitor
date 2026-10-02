# AGENTS.md

Este repositorio es la fuente de verdad del DOF Jurídico Monitor. Un agente nuevo debe poder ejecutar el sistema sin contexto externo.

## Orden
README → SPECIFICATION → WORKFLOW → QUALITY_GATE → master prompt → config → schemas → templates.

## No negociable
- Nunca afirmar lectura, cobertura, vigencia o envío no verificado.
- Nunca usar Top notas/snippets/buscadores generales como universo oficial.
- Nunca fabricar URLs o códigos DOF.
- Cobertura completa requiere universo cerrado y lectura íntegra.
- Si PDF real no es accesible, usar vía B y declarar huecos.
- Distinguir hecho, análisis y sugerencia.
- Iniciativa ≠ norma; sentencia ≠ jurisprudencia; caso ≠ regla general.
- Memoria del agente no prueba expedientes.
- Corregir errores y propagarlos.
- No enviar al destinatario final sin aprobación humana.

## Estilo
Español de México. Natural, claro, jurídico, profesional, minimalista; sin grandilocuencia, arcaísmos, redundancia, emojis ni relleno.

Todo cambio material actualiza CHANGELOG. Cambios arquitectónicos requieren ADR.
