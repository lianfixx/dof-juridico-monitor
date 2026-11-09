// Esquema del contenido de una entrega (copiar como content.js y llenar). Todo texto en español
// de México, natural y sobrio; cada dato debe estar en evidencias.json y en la fuente oficial.
const N = (c, f) => `https://dof.gob.mx/nota_detalle.php?codigo=${c}&fecha=${f}`; // f = DD/MM/AAAA
const T = (r) => `https://sjf2.scjn.gob.mx/detalle/tesis/${r}`;
module.exports = {
  sufijo: "DD-MM_DD-MM-AAAA",                      // va en los nombres de archivo
  fecha: "30 de octubre al 3 de noviembre de 2026", // pie de la guía
  titulo: "Actualización DOF y Semanario Judicial | 30 de octubre al 3 de noviembre de 2026", // jueves: «Actualización DOF | …»
  dofTitulo: "Diario Oficial de la Federación · 30 de octubre, 2 y 3 de noviembre de 2026",
  relevante: ["2–4 líneas sustantivas.", "…"],
  filas: [{ asunto: "", emisor: "", efecto: "", vigencia: "", importa: "", fuente: [["DOF 30/10/2026", N(5802597, "30/10/2026")]] }],
  sjfTitulo: "Semanario Judicial de la Federación · publicación del viernes 30 de octubre de 2026", // martes
  sjf: [{ asunto: "", emisor: "Pleno de la Suprema Corte · P./J. 216/2026 (12a.)", efecto: "", vigencia: "", importa: "", fuente: [["Registro 2032862", T(2032862)]] }], // jueves: []
  correoLic: { asunto: "", parrafos: ["Licenciado, buen día. Le comparto la actualización del DOF correspondiente a …", "…", "Comentario personal: [Espacio para mi opinión antes del envío].", "Adjunto el reporte. Quedo atento a sus comentarios.", "Emiliano García Milla"] }, // 80–130 palabras
  comentario: "40–70 palabras.",
};
// guia.js: { titulo, estado, estudiar: [{tema, puntos: [[clave, texto]]}], cobertura: [[a, b]], avisos: [], pendientes: [] }
