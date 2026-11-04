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

## Trabajo entre IA (obligatorio para cualquier IA o persona)

Este repositorio sigue el protocolo común de `ia/PROTOCOLO.md`; las reglas concretas están en `ia/REGLAS.md`.
- Al empezar, ejecuta `python3 ia/verificar.py inicio`: resume rama, último commit y su IA, reglas, registro y hooks (en Claude Code corre solo).
- Fuente de verdad: el repositorio remoto y su estado vigente (la bitácora y los controles de la última entrega, según `docs/WORKFLOW.md`), no la memoria de una conversación.
- Todo cambio se registra en el mismo commit, con la línea `Agente:` (protocolo, sección 3). Sin escritura, entrega un «Registro pendiente para el repositorio».
- Lo prohibido y lo que requiere confirmación de Emi vale en Claude, ChatGPT, Codex, Gemini y cualquier otra IA. Con terminal, ejecuta `sh ia/instalar.sh` una vez por copia. GitHub revisa cada push con `registro-ia.yml`.
- Para pasar trabajo a otra IA: `ia/plantillas/PETICION.md` y `ia/plantillas/ENTREGA.md`.
