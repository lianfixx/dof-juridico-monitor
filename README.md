# DOF Jurídico Monitor

Sistema autónomo, auditable y agnóstico de proveedor para revisar el Diario Oficial de la Federación (DOF), verificar cobertura, detectar novedades jurídicas relevantes y producir entregables ejecutivos y de estudio.

No depende de ChatGPT, de una conversación previa ni de servidores privados de un proveedor de IA. Cualquier agente con acceso web/PDF puede implementar el flujo siguiendo este repositorio.

## Principios
1. Cobertura antes que selección.
2. Fuentes oficiales primero.
3. Lo no comprobado se marca; no se infiere.
4. Doble vía: PDF completo real o índice + publicaciones + colecciones secundarias.
5. Cobertura completa exige lectura íntegra del universo.
6. Separación despacho / operador.
7. Corrección inmediata y propagación.
8. Neutralidad política.
9. Profundidad en investigación; concisión en entregables.
10. Diseño limpio, natural y profesional.

## Calendario
- Martes: viernes anterior + lunes + martes.
- Jueves: miércoles + jueves.
- Complemento: fines de semana, publicaciones posteriores al corte, fes de erratas/correcciones/republicaciones.
- Zona: America/Mexico_City.

## Entregables
**Despacho:** reporte PDF + correo BLUF para revisión humana.
**Operador:** editable DOCX + guía PDF/DOCX + comentario + bitácora.

## Semanario Judicial semanal

El [módulo SJF](docs/sjf/METODO.md) añade criterios judiciales, estudio y opinión al seguimiento. Explica primero qué resolvió el tribunal, por qué importa y qué revisar; conserva después todo el fundamento y sus límites. Mantiene la lectura íntegra antes de seleccionar y los cuatro entregables aprobados.

- [Cómo estudiar los criterios](docs/sjf/GUIA.md).
- [Prompt de ejecución](prompts/sjf.md) y plantillas de [reporte](templates/sjf-report.md), [guía](templates/sjf-study.md) y [correo](templates/sjf-email.md).
- [Auditoría del método](docs/sjf/AUDITORIA_2026-10-15.md).

La extensión se documentó el 15-10-2026; su primer corte previsto es el 16-10-2026. La programación efectiva y el primer reporte requieren comprobación propia. Esta documentación no aplica el parche DOF 1.2.0 ni declara una nueva versión del código.

## Skill portable y estilo Castorena

- [SKILL.md](SKILL.md): instrucciones operativas y formato final aprobado, compatible con agentes que admitan skills de Markdown.
- Reporte blanco/negro/grises, fuentes directas dentro de cada fila, sin leyendas operativas, con «Lo relevante» y tabla ejecutiva.
- Paquete completo para Emi: PDF del Licenciado, editable DOCX, guía PDF/DOCX, comentario sugerido separado y correo HTML BLUF.
- Revisión profesional proporcional al encargo: distinguirla expresamente de la certificación exhaustiva de cobertura. Los requisitos estrictos de cobertura completa no cambian.

## Inicio
1. SKILL.md
2. AGENTS.md
3. docs/SPECIFICATION.md
4. docs/WORKFLOW.md
5. docs/QUALITY_GATE.md
6. prompts/master.md
7. config/default.yaml

Versión: **1.1.0**.


## Estado de implementación y límites (2026-10-20)
El módulo SJF está documentado en `main`. Los controles de evidencia estructurada propuestos en el PR #2 requieren integración adicional con el motor de generación, persistencia y Gmail; no se debe interpretar una ejecución exitosa de `pytest` como prueba de lectura jurídica completa. La versión de la skill (1.1.0) y la versión del paquete Python (1.0.0) son independientes. El parche 1.2.0 no se ha aplicado.

### Flujo práctico SJF con PDF adjuntos
Ver [operación asistida y enlaces oficiales](docs/sjf/OPERACION.md). El comando local `python -m src.dof_monitor.sjf_intake` crea un control privado, incorpora PDF adjuntos con hash y bloquea el cierre cuando falta lectura o investigación. No equivale a un servicio autónomo de publicación, generación de cuatro documentos o envío Gmail.

## Calendario de entrega definitivo (20-10-2026)

| Día | Trabajo | Correo a Emi | Archivos |
|---|---|---|---|
| Viernes 15:00 | Investigación y control SJF interno | No, salvo solicitud extraordinaria | Control y fuentes persistentes; paquete interno si procede |
| Martes 06:00 | DOF + SJF del viernes publicado | Uno, únicamente tras auditoría completa | Cuatro archivos conjuntos: reporte PDF/DOCX y guía PDF/DOCX |
| Jueves 06:00 | DOF exclusivamente | Uno, únicamente tras auditoría DOF completa | Cuatro archivos DOF: reporte PDF/DOCX y guía PDF/DOCX |

El jueves nunca incluye una sección SJF. Las novedades judiciales sobrevenidas quedan para el martes siguiente; el jueves puede cerrarse aunque SJF tenga pendientes. El martes no se declara completo si DOF o SJF carecen de lectura íntegra. Las tareas programadas deben mantener sus horas actuales; el repositorio documenta la política y no demuestra ejecución automática ni envíos.
