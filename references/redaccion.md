# Redacción del reporte, la guía y el correo

Obligatoria desde la skill 1.4.0 (23 de noviembre de 2026). La pidió Emi después de leer cuatro entregas: «debe parecer escrito realmente por mí», «claro, completo y no redundante», «que no dé flojera leerlo», «técnico, argumentado y fundado». Aplica igual a las dos vías: la sesión de la suscripción que redacta el paquete y el lector por API que redacta el preliminar (su instrucción carga el núcleo de este archivo; `tests/test_sincronia.py` lo comprueba).

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

**«Lo relevante».** De dos a cuatro párrafos de una o dos frases. Cada párrafo, un tema: qué cambió, para quién y desde cuándo. Primero lo que más pesa para el despacho. Es lo que el Licenciado debe saber si solo lee eso; no es el índice de lo publicado.

**La tabla.** Una fila por asunto, no por publicación. Una ley con cinco cambios que importan son cinco filas, cada una con su título. Orden por importancia para el despacho (fiscal, prevención de lavado, administrativo, amparo), no por fecha. Lo secundario no entra a la tabla: va a los avisos de la guía.

| Columna | Qué lleva | Medida |
|---|---|---|
| Asunto | El cambio, nombrado como lo diría un abogado. Sin dos puntos. | Hasta 12 palabras |
| Qué ocurrió / efecto | Qué cambia, dicho en llano. A quién aplica. Cómo opera, con la cifra o la condición clave. Fundamento entre paréntesis. | 2 a 4 frases, 35 a 80 palabras, tres cifras como máximo |
| Vigencia / estado | Cuándo entra en vigor y, si existe, la excepción o el plazo que corre. | Una frase, hasta 25 palabras |
| Por qué importa / qué revisar | A qué clientes o asuntos del despacho les pega y qué conviene hacer. Si se ve venir una discusión jurídica, en una frase. | 1 a 3 frases, 20 a 60 palabras |

Si una celda necesita más de tres cifras, la fila se parte en dos o el detalle baja a la guía. En el Semanario, la fila dice el criterio en una frase, si es jurisprudencia o tesis aislada y desde cuándo obliga, y para qué sirve en un asunto.

**Antes y después** (fila real de la entrega del 17 de noviembre de 2026):

> Antes. *Asunto:* «Reforma a la Ley del ISR: deducciones de grandes personas morales, pérdidas y…». *Qué ocurrió:* «Personas morales con ingresos «superiores a 50 millones de pesos» que determinen utilidad fiscal: sus deducciones se limitan con los factores «0.9667» y «0.9900» (artículos 78-A a 78-E) y el excedente…».

> Después. *Asunto:* Límite a las deducciones de personas morales grandes. *Qué ocurrió:* Las personas morales con ingresos acumulables superiores a 50 millones de pesos ya no podrán deducir todo en el ejercicio. Sus deducciones se topan con un factor de 0.9667 sobre los ingresos o de 0.9900 sobre las propias deducciones, según el caso, y lo que no se deduzca se recupera en los veinte ejercicios siguientes (artículos 78-A a 78-E de la Ley del ISR). *Vigencia:* En vigor el 1 de enero de 2027. *Por qué importa:* Pega a clientes medianos y grandes con márgenes bajos, que pagarán ISR aun con poca utilidad. Conviene proyectar su ISR de 2027 con ambos supuestos y revisar si alguno cae en las exclusiones del artículo 78-E.

Las pérdidas fiscales, los intereses y los grupos de sociedades, que iban en esa misma celda, son otras filas.

## El correo al Licenciado y el comentario

El correo conserva sus fórmulas fijas (apertura «Licenciado, buen día. Le comparto la actualización…», «Comentario personal: [Espacio para mi opinión antes del envío].», cierre y firma «Emiliano García Milla») y sus 80 a 130 palabras. El cuerpo dice lo más importante en dos o tres frases, con la voz de Emi: directa, segura, con postura y sin adornos. No resume la tabla ni enumera todo.

El comentario sugerido (40 a 70 palabras) es una opinión jurídica en primera persona: qué le parece lo más delicado del periodo y por qué. Tiene postura; no es un resumen. Si la skill `estilo-emi` está disponible, el correo y el comentario se redactan con ella.

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
2. Leer en voz alta «Lo relevante» y dos filas. Si suenan a acta, se reescriben.
3. Cada fila contesta qué cambió, a quién, desde cuándo y qué hacer.
4. Ningún dato repetido entre «Lo relevante», la tabla y el correo. Ninguna fila de la tabla copiada en la guía.
5. Cada sigla desarrollada la primera vez.
