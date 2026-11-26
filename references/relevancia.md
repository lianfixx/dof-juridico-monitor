# Escala de relevancia

Decisión de Emi del 26/11/2026: «temas de relevancia social, de política, cosas de presidencia, todo lo IMPORTANTE debe estar». Esta escala la usan por igual el lector por API (`scripts/api/lector_api.py` la carga tal cual en su instrucción) y los lectores de la suscripción (lector nocturno y cierres). Si se cambia aquí, cambia en las dos vías; `tests/test_sincronia.py` lo comprueba.

La relevancia no decide qué se lee: todo se lee íntegro antes. Decide qué se propone. Lo alto y lo medio son candidatas a la tabla del reporte; lo bajo va a los avisos de la guía; lo que no tiene relevancia solo queda en el inventario. La selección final de filas es del cierre.

<!-- escala:inicio -->
Califica cada publicación con esta escala, pensando en un despacho que sigue Fiscal, Compliance y PLD-FT, Administrativo y Amparo, y en lo que su titular debe saber de la vida pública del país (política, social y de Presidencia).
- alta: cambia reglas que obligan a empresas o personas o que se discuten en juicio. Leyes y reformas constitucionales o legales; reglamentos; decretos y acuerdos del Presidente o de la Presidenta de la República; reglas, resoluciones y criterios del SAT, la SHCP, la UIF, la CNBV y demás autoridades fiscales o financieras (Miscelánea, RGCE, estímulos y cuotas, listas del 69-B); nuevas obligaciones, plazos, montos o sanciones de alcance general; creación, fusión o extinción de dependencias y organismos; declaratorias de emergencia o de desastre de alcance nacional; programas sociales nacionales nuevos o sus cambios de fondo; reformas electorales y en materia de seguridad, salud, educación o derechos humanos de alcance nacional.
- media: afecta a un sector, a una entidad o a un grupo, o es un dato que el despacho usa. Normas oficiales mexicanas; lineamientos y acuerdos de órganos autónomos (INE, Banco de México, CNDH y demás); acuerdos de la SCJN y del órgano de administración judicial; días inhábiles y calendarios de autoridades; revocaciones, concesiones, sanciones e inhabilitaciones; convenios federales con efectos para particulares; reglas de operación de programas sociales; nombramientos y cambios de estructura en Presidencia y secretarías; acuerdos electorales (topes de gasto, registros, lineamientos); indicadores mensuales que se usan en cálculos (INPC, recargos, actualización).
- baja: rutina sin efecto nuevo. Indicadores diarios (tipo de cambio, TIIE, UDI, CPP y similares); convenios de coordinación ordinarios con estados o municipios; avisos de asociaciones religiosas; tarifas y avisos de particulares; convocatorias y licitaciones; edictos ordinarios.
- ninguna: efemérides, avisos internos del propio Diario Oficial y estados financieros de particulares.
Si dudas entre dos niveles, elige el más alto. Una publicación de la Presidencia de la República, de una secretaría de Estado o de una autoridad fiscal, financiera o jurisdiccional no se califica baja o ninguna salvo que sea claramente rutina (por ejemplo, el tipo de cambio diario).
<!-- escala:fin -->

## Semanario Judicial de la Federación

El Semanario no pasa por el lector por API; lo lee la suscripción el viernes. Vale el mismo principio: todo se lee íntegro y después se ordena. Se proponen para la tabla del martes las jurisprudencias y tesis de las materias del despacho (fiscal, prevención de lavado, administrativo y amparo) y, además, las de trascendencia nacional aunque sean de otra materia: las que declaran inconstitucional una norma general, las de derechos humanos, laboral y seguridad social, electoral y las de relevancia social o política (`docs/sjf/METODO.md`, «Prioridad inicial»). En la duda entre proponer o no, se propone; la selección final es del cierre.

## Revisión del cierre

El cierre vuelve a mirar, en el inventario, lo que quedó con relevancia baja o ninguna de estas autoridades, y si alguna debió ser candidata la lee en el box y la registra como diferencia (`lectura_api.diferencias`):

Presidencia de la República; secretarías de Estado (en especial Gobernación, Hacienda, Economía, Trabajo y Bienestar); SAT, UIF, CNBV, CNSF, CONSAR, Banco de México y PRODECON; IMSS e INFONAVIT; CONAMER; Congreso de la Unión; SCJN, TFJA, tribunales federales y órgano de administración judicial; INE y demás órganos autónomos; y cualquier ley, reforma o decreto de alcance nacional.
