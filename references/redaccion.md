# Redacción del reporte, la guía y el correo

Obligatoria desde la skill 1.4.0 (23 de noviembre de 2026); la forma del reporte y del correo se ajustó en la 1.5.0 (24 de noviembre de 2026) con la versión final que Emi envió ese día. La pidió Emi después de leer cuatro entregas: «debe parecer escrito realmente por mí», «claro, completo y no redundante», «que no dé flojera leerlo», «técnico, argumentado y fundado». Aplica igual a las dos vías: la sesión de la suscripción que redacta el paquete y el lector por API que redacta el preliminar (su instrucción carga el núcleo de este archivo; `tests/test_sincronia.py` lo comprueba).

## Qué estaba mal (entregas del 10 al 19 de noviembre de 2026)

- Las celdas de la tabla eran notas, no prosa: veinte renglones con siete reglas distintas encadenadas con punto y coma.
- Cada cifra iba entre comillas angulares («1.38 por ciento mensual», «el 50 por ciento de la multa»). Era la huella de la auditoría literal metida en el texto: nadie escribe así.
- Los títulos de fila eran inventarios («Ley de Ingresos 2027: tasas, multas y retenciones»).
- La guía abría con el control de ediciones y páginas, y sus temas eran etiquetas con fragmentos («Quiénes.», «Mecánica.», «Otras piezas.»). Daba por sabido el concepto y repetía las cifras del reporte.

## Núcleo (vale para todo lo que se escriba)

<!-- nucleo:inicio -->
1. Escribe como Emi le explicaría el tema al Licenciado de viva voz. Frases completas, con sujeto y verbo, una idea por frase. Ni telegrama ni acta.
2. Primero el cambio y su efecto; después, el fundamento. El fundamento va entre paréntesis (artículo, fracción, transitorio) y no como sujeto de la frase.
3. Cifras, fechas y plazos exactos, escritos de forma natural (1.38% mensual, 31 de octubre de 2027). Sin comillas angulares alrededor de cifras o frases de la norma. Las comillas se reservan para la expresión cuya redacción exacta sea el punto en discusión, una por apartado como máximo.
4. Sin dos puntos dentro de una frase, sin cadenas de punto y coma y sin paréntesis encadenados. Si hacen falta, son dos frases.
5. Cada sigla se desarrolla la primera vez. Cada término que no sea de uso diario en el despacho se explica en media línea.
6. Nada se repite. Un dato aparece una sola vez en cada documento.
7. Sin muletillas ni burocratismos (cabe señalar, es importante mencionar, en este sentido, derivado de lo anterior, a efecto de, se hace de su conocimiento, en términos de lo dispuesto), sin adjetivos de relleno (importante, relevante, significativo) y nunca «agradezco de antemano».
8. Se distingue siempre publicación, entrada en vigor y plazo. Una iniciativa no es norma, una tesis aislada no es jurisprudencia y una sentencia no es regla general. Si la fuente no lo dice, se escribe «no consta».
9. Preciso y fluido a la vez. La prueba es leerlo en voz alta: si se tropieza, se reescribe.
<!-- nucleo:fin -->

La exactitud no cambia: cada dato sigue en `evidencias.json` con su texto literal y `audit.py` al 100 %. La cita literal vive en las evidencias; el reporte la dice con naturalidad.

## El reporte (para el Licenciado)

**Lo que Emi cambió en su versión final del 24 de noviembre de 2026** (comparación del reporte enviado con el que él mandó al Licenciado; el detalle, con la entrega real, está en el repositorio privado `lianfixx/dof-trabajo`, carpeta `ejemplos/2026-11-24/`):

- Quitó los párrafos de «Lo relevante» y el subtítulo del DOF. «Lo relevante» quedó como título de la tabla.
- Dejó 5 de las 14 filas (decisión de esa semana, no regla; Emi lo aclaró el mismo día). Conservó los días inhábiles de fin de año de dos autoridades, una declaratoria de amparo en línea y las jurisprudencias del Pleno. Quitó los avisos y listados rutinarios del SAT, las reglas operativas de comercio exterior, la jurisprudencia de un tribunal colegiado y las tesis aisladas.
- Partió «Qué ocurrió» en dos párrafos (la regla y, aparte, el dato que la completa: precedente, votación o detalle operativo).
- En «Por qué importa» dejó solo para qué sirve («Sirve para…», «Permite…») y borró los consejos («conviene…») y los datos laterales. En dos filas dejó solo la fuente (también decisión de ese reporte: la columna siempre lleva frase).
- Después pidió juntar las dos tablas en una y un correo más claro y más apegado a las jurisprudencias, con su opinión ya escrita por el cierre.

**«Lo relevante».** Es el título de la única tabla del reporte. No lleva párrafos de resumen: el resumen es el correo al Licenciado.

**La tabla.** Una sola, con el DOF primero y el Semanario después. Una fila por asunto, no por publicación. Orden por importancia para el despacho (fiscal, prevención de lavado, administrativo, amparo), no por fecha. Lo político, social y de Presidencia que la [escala de relevancia](relevancia.md) califica alto también entra (Emi, 26/11/2026). Lo secundario no entra: va a los avisos de la guía. El número de filas lo marca la semana; no hay tope fijo, pero cada fila tiene que valer la lectura del Licenciado. El preliminar del lector por API propone candidatas con criterio amplio y la selección es del cierre.

| Columna | Qué lleva | Medida |
|---|---|---|
| Asunto | El cambio, nombrado como lo diría un abogado. Sin dos puntos. Debajo, en gris, quién lo emite y su clave (en el Semanario, «Pleno de la Suprema Corte · P./J. 10/2027 (12a.)») | Hasta 12 palabras |
| Qué ocurrió / efecto | Primer párrafo, la regla o el criterio, dicho en llano y con su fundamento entre paréntesis. Segundo párrafo, si hace falta, el dato que lo completa (precedente y votación, horario, excepción) | 30 a 90 palabras, dos párrafos como máximo |
| Vigencia / obligatoriedad | En el DOF, cuándo entra en vigor y el plazo que corre. En el Semanario, si es jurisprudencia o tesis aislada y desde cuándo obliga | Una frase, hasta 25 palabras |
| Por qué importa / qué revisar | Siempre lleva frase. Para qué sirve en un asunto, en una o dos frases. Sin consejos genéricos ni datos que no estén en la fuente | 8 a 45 palabras |

Si una celda necesita más de tres cifras, la fila se parte en dos o el detalle baja a la guía.

**Antes y después** (fila real de la entrega del 17 de noviembre de 2026):

> Antes. *Asunto:* «Reforma a la Ley del ISR: deducciones de grandes personas morales, pérdidas y…». *Qué ocurrió:* «Personas morales con ingresos «superiores a 50 millones de pesos» que determinen utilidad fiscal: sus deducciones se limitan con los factores «0.9667» y «0.9900» (artículos 78-A a 78-E) y el excedente…».

> Después. *Asunto:* Límite a las deducciones de personas morales grandes. *Qué ocurrió:* Las personas morales con ingresos acumulables superiores a 50 millones de pesos ya no podrán deducir todo en el ejercicio. Sus deducciones se topan con un factor de 0.9667 sobre los ingresos o de 0.9900 sobre las propias deducciones, según el caso, y lo que no se deduzca se recupera en los veinte ejercicios siguientes (artículos 78-A a 78-E de la Ley del ISR). *Vigencia:* En vigor el 1 de enero de 2027. *Por qué importa:* Pega a clientes medianos y grandes con márgenes bajos, que pagarán ISR aun con poca utilidad. Sirve para proyectar su ISR de 2027 con ambos supuestos.

Las pérdidas fiscales, los intereses y los grupos de sociedades, que iban en esa misma celda, son otras filas.

## El correo al Licenciado y el comentario

El correo es el resumen del reporte y se escribe como si Emi lo hubiera redactado después de estudiar cada criterio. Va en orden BLUF (lo principal primero):

1. Apertura fija. «Licenciado, buen día. Le comparto la actualización del DOF y del Semanario Judicial de la Federación del …» (los jueves, solo «del DOF»).
2. Lo principal, en una frase de hasta 35 palabras. Por ejemplo, «Lo principal son tres jurisprudencias del Pleno de la Corte, obligatorias desde el 23 de noviembre.»
3. Un párrafo corto por cada asunto de la tabla, en su orden. Cada jurisprudencia con su clave, su criterio en una frase con las palabras de la tesis y para qué sirve. Lo del DOF puede ir junto en un solo párrafo.
4. La opinión de Emi, ya escrita por el cierre (decisión de Emi del 24 de noviembre de 2026, que sustituye al espacio «Comentario personal»). Una o dos frases en primera persona, naturales y claras, sobre lo que más le sirve al despacho de lo reportado y por qué, apoyadas solo en la tabla. Puede ir dentro del párrafo del asunto que comenta. Nada de opinión de relleno ni de afirmaciones sobre expedientes concretos.
5. Cierre y firma fijos. «Adjunto el reporte. Quedo atento a sus comentarios.» y «Emiliano García Milla».

De 120 a 230 palabras. Sin dos puntos dentro del texto, sin listas y sin datos que no estén en la tabla. `estilo.js` avisa si falta la clave de una jurisprudencia de la tabla.

**Ejemplo** (ficticio, con la estructura del correo que Emi aprobó el 24 de noviembre de 2026, opinión incluida; el real está en `ejemplos/2026-11-24/` del repositorio privado):

> Licenciado, buen día. Le comparto la actualización del DOF y del Semanario Judicial de la Federación del 1 al 3 de marzo de 2027.
>
> Lo principal son dos jurisprudencias del Pleno de la Corte, obligatorias desde el 1 de marzo.
>
> La P./J. 10/2027 resuelve que la notificación por estrados solo procede cuando el domicilio no puede localizarse después de dos visitas. Sirve para impugnar notificaciones hechas sin agotar esas visitas.
>
> La P./J. 11/2027 precisa que el plazo para ampliar la demanda de nulidad corre desde que se conoce la resolución complementaria. Permite ampliar en asuntos que el tribunal daba por extemporáneos, y a mi juicio es la de uso más inmediato.
>
> En el DOF, el Tribunal Federal de Justicia Administrativa publicó sus días inhábiles de Semana Santa.
>
> Adjunto el reporte. Quedo atento a sus comentarios.
>
> Emiliano García Milla

## La guía (para Emi)

Sirve para que Emi entienda cada tema desde cero y pueda explicarlo. El reporte informa; la guía enseña. Por eso no copia la tabla.

- `estado`: dos frases como máximo. Qué cubre la entrega y si quedó íntegra. Ediciones, páginas y controles van en «Control de cobertura».
- `estudiar`: de uno a cinco temas, solo los que conviene dominar, del más importante al menos. Entre todos, de 600 a 1,100 palabras.
- Cada tema lleva estos apartados, con estos nombres y en este orden. Cada uno, de dos a cuatro frases completas (30 a 90 palabras):

| Apartado | Qué contesta |
|---|---|
| De qué se trata | El concepto desde cero: qué es la figura y para qué existe, con sus términos explicados |
| Qué cambió | Cómo era y cómo queda, en una comparación directa |
| Fundamento | Norma, artículos y transitorios, fecha del DOF y entrada en vigor |
| Cómo opera | La mecánica, paso a paso. Un ejemplo con números sencillos cuando hay fórmula; los plazos contados cuando hay plazos |
| Por qué importa | El efecto práctico, a quién le pega y el argumento que lo sostiene |
| Dónde está la discusión | El argumento contrario o el punto dudoso y la vía probable (amparo, nulidad, consulta). Si no la hay, se omite |
| Para dominarlo | Una pregunta que Emi debe poder contestar sin ver la guía |

- `avisos`: una línea cada uno, lo secundario que conviene tener ubicado. `pendientes`: lo que falta, con el dato exacto.

**Ejemplo de apartado** (mismo tema): *De qué se trata.* Una deducción es un gasto que la ley permite restar de los ingresos antes de calcular el impuesto. Hasta 2026, una empresa restaba todas sus deducciones autorizadas en el mismo ejercicio. La reforma pone un tope a las empresas grandes: una parte de lo que gastaron no baja el impuesto de ese año, sino de los siguientes.

## Revisión antes de armar

1. `node scripts/paquete/estilo.js <carpeta con content.js y guia.js>` sin errores. Revisa medidas, comillas, dos puntos, punto y coma, muletillas y los apartados de la guía. Sus avisos se leen y se atienden o se justifican en la bitácora.
2. Leer en voz alta el correo y dos filas. Si suenan a acta, se reescriben.
3. Cada fila contesta qué cambió, a quién, desde cuándo y qué hacer.
4. El correo resume la tabla sin agregar datos. Ninguna fila de la tabla copiada en la guía.
5. Cada sigla desarrollada la primera vez.
