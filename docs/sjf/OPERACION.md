# SJF semanal: flujo operable con archivos del usuario

## Qué puede hacer el sistema ahora

Este repositorio ofrece un flujo **asistido y auditable**, no un lector automático capaz de certificar lectura jurídica. El agente debe verificar el índice oficial completo y cada documento antes de valorar relevancia. Si la fuente oficial no permite descargar un archivo, pedir al usuario que lo descargue y adjunte; no sustituirlo por snippets.

**Fuentes oficiales para localizar y descargar:** [Buscador SJF](https://sjf2.scjn.gob.mx/) y [Gaceta SCJN](https://www.scjn.gob.mx/coordinacion/gaceta). Son portales de acceso, **no enlaces inventados a un PDF específico**. Elegir en el sitio la publicación real del viernes y guardar todos los documentos, anexos, votos, sentencias y paginaciones que correspondan. Para el 16-10-2026 no afirmar que la edición esté completa sin cotejar su índice real.

## Operación paso a paso

1. El viernes, identificar fecha efectiva, secciones y total de documentos mediante fuentes oficiales. Registrar fecha de publicación y corte.
2. Descargar los PDF oficiales, o pedir al usuario que adjunte los faltantes; mantener lista exacta de documentos/rangos pendientes. No guardar PDFs con datos sensibles en este repositorio público.
3. Crear un control privado local: `python -m src.dof_monitor.sjf_intake init --date 2026-10-16 --out ./privado/SJF_2026-10-16`.
4. Por cada PDF descargado, ejecutar `python -m src.dof_monitor.sjf_intake add --control ./privado/SJF_2026-10-16/SJF_2026-10-16_Control.json --file /ruta/archivo.pdf --url https://URL-OFICIAL-DEL-DOCUMENTO`. La URL debe ser la dirección oficial real, no el ejemplo. El sistema calcula SHA-256 e intenta contar páginas; el registro permanece PENDIENTE.
5. Leer visualmente todas las páginas y anexos. Tras revisar cada documento, completar manualmente en el JSON `read_ranges`, `reading_notes`, `annexes`, `annexes_verified`, `legal_checks` y `status`. No marcar verdadero un control que no se verificó. Identificar cada documento y vincular tesis, sentencias y votos.
6. Sólo después de conciliar índice, totales y paginaciones, establecer `edition_verified`, `inventory_reconciled` y `universe_closed` según evidencia. Realizar investigación y revisión crítica de obligatoriedad, votaciones, ámbito, excepciones y efectos, contrastando fuentes primarias. Aprobar auditoría sólo con evidencia real.
7. Ejecutar `python -m src.dof_monitor.sjf_intake check --control ./privado/SJF_2026-10-16/SJF_2026-10-16_Control.json`. Si informa PARCIAL, no generar ni enviar un paquete rotulado final.
8. Tras cierre real, crear `SJF_AAAA-MM-DD_Reporte.pdf`, `.docx`, `SJF_AAAA-MM-DD_Guia.pdf` y `.docx`; renderizar, revisar, registrar hashes reales, persistir con `SJF_AAAA-MM-DD_Control.json` en almacenamiento privado accesible al martes.
9. Martes: recuperar los cinco archivos, cotejar identidad/hashes, fecha del viernes, correcciones y auditoría; integrar DOF y SJF en los mismos cuatro adjuntos. Jueves: sólo novedades posteriores verificadas. No presumir que los archivos de otro hilo están accesibles.
10. Antes del único correo a la cuenta personal autorizada: revisar duplicados, intentos previos, archivos y destinatario. Ante respuesta ambigua, bloquear reenvío. No enviar al Licenciado.

## Alcance honesto

El comando comprueba consistencia estructural y hashes de PDF registrados, pero no demuestra que el documento sea oficial, que el universo esté completo, que la lectura se haya realizado o que la interpretación jurídica sea correcta. Los indicadores de revisión son declaraciones que exigen respaldo independiente. Los cuatro archivos y Gmail **no se generan ni envían mediante este comando**. Si el entorno no permite persistencia, entregar los archivos de control al usuario para que los adjunte en la siguiente ejecución.

## Seguridad

La carpeta `privado/` debe mantenerse fuera de Git. No subir a GitHub expedientes, notas confidenciales, PDF de clientes, direcciones de correo adicionales ni credenciales. Los documentos del SJF pueden ser públicos, pero los análisis y controles personales deben permanecer privados.
