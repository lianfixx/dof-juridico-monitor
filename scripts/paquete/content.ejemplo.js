// Esquema del contenido de una entrega (copiar como content.js y llenar). Todo texto en español
// de México, natural y sobrio; cada dato debe estar en evidencias.json y en la fuente oficial.
const N = (c, f) => `https://dof.gob.mx/nota_detalle.php?codigo=${c}&fecha=${f}`; // f = DD/MM/AAAA
const T = (r) => `https://sjf2.scjn.gob.mx/detalle/tesis/${r}`;
module.exports = {
  sufijo: "DD-MM_DD-MM-AAAA",                      // va en los nombres de archivo
  fecha: "30 de octubre al 3 de noviembre de 2026", // pie de la guía
  titulo: "Actualización DOF y Semanario Judicial | 30 de octubre al 3 de noviembre de 2026", // jueves: «Actualización DOF | …»
  // Una sola tabla bajo «Lo relevante», sin párrafos de resumen: primero `filas` (DOF), después `sjf` (Semanario).
  // `efecto` e `importa` admiten dos párrafos separados por una línea en blanco ("\n\n"). `importa` siempre lleva frase.
  filas: [{ asunto: "", emisor: "Autoridad que publica", efecto: "La regla.\n\nEl dato que la completa.", vigencia: "", importa: "Para qué sirve.", fuente: [["DOF 30/10/2026", N(5802597, "30/10/2026")]] }],
  sjf: [{ asunto: "", emisor: "Pleno de la Suprema Corte · P./J. 216/2026 (12a.)", efecto: "El criterio.\n\nPrecedente y votación.", vigencia: "Jurisprudencia del Pleno, obligatoria desde …", importa: "Para qué sirve.", fuente: [["Registro 2032862", T(2032862)]] }], // jueves: []
  correoLic: { asunto: "", parrafos: ["Licenciado, buen día. Le comparto la actualización del DOF y del Semanario Judicial de la Federación del …", "Lo principal, en una frase.", "Una frase o dos por cada asunto de la tabla; cada jurisprudencia con su clave, su criterio y para qué sirve.", "La opinión de Emi en una o dos frases («A mi juicio…»), si no va ya dentro de un párrafo anterior.", "Adjunto el reporte. Quedo atento a sus comentarios.", "Emiliano García Milla"] }, // 120–230 palabras
  comentario: "40–70 palabras.",
};
// guia.js: { titulo, estado (dos frases), estudiar: [{tema, puntos: [[clave, texto]]}] (1 a 5 temas), cobertura: [[a, b]], avisos: [], pendientes: [] }
// claves de `puntos`, en este orden: "De qué se trata", "Qué cambió", "Fundamento", "Cómo opera", "Por qué importa", "Dónde está la discusión" (opcional), "Para dominarlo"
