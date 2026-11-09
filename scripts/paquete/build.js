const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  BorderStyle, ExternalHyperlink, AlignmentType, ShadingType, LevelFormat, Footer, PageNumber,
} = require("docx");
// Uso: NODE_PATH=<node_modules> node build.js DIR_CONTENIDO DIR_SALIDA
// DIR_CONTENIDO tiene content.js y guia.js (ver content.ejemplo.js). Si C.sjf está vacío o
// no existe (jueves), el reporte no lleva sección del Semanario.
const path0 = require("path");
const DIR = path0.resolve(process.argv[2]);
const C = require(path0.join(DIR, "content.js"));
const G = require(path0.join(DIR, "guia.js"));
const OUT = process.argv[3];
const SJF = Array.isArray(C.sjf) && C.sjf.length > 0;

const FONT = "Arial";
const INK = "111111", GRAY = "6B6B6B", RULE = "BFBFBF";
const page = { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } };
const W = 12240 - 2160; // 10080

const t = (text, o = {}) => new TextRun({ text, font: FONT, size: o.size || 19, bold: o.bold, color: o.color || INK, italics: o.italics });
const p = (runs, o = {}) => new Paragraph({ pageBreakBefore: o.pageBreakBefore, keepNext: o.keepNext, children: Array.isArray(runs) ? runs : [runs], spacing: { after: o.after ?? 120, before: o.before ?? 0, line: o.line || 276 }, alignment: o.align, border: o.border, numbering: o.numbering });
const link = (label, url, size = 15) => new ExternalHyperlink({ link: url, children: [new TextRun({ text: label, font: FONT, size, color: "333333", underline: {} })] });
const rule = () => p([t("")], { after: 160, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 1 } } });

const footer = (label) => new Footer({ children: [p([t(label + "  ·  ", { size: 15, color: GRAY }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 15, color: GRAY })], { align: AlignmentType.RIGHT, after: 0 })] });

const noB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const cellBorders = { top: noB, left: noB, right: noB, bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE } };

function table(filas, h3) {
  const widths = [1900, 3700, 1800, 2680];
  const head = new TableRow({ tableHeader: true, children: ["Asunto", "Qué ocurrió / efecto", h3, "Por qué importa / qué revisar"].map((h, i) =>
    new TableCell({ width: { size: widths[i], type: WidthType.DXA }, borders: { ...cellBorders, bottom: { style: BorderStyle.SINGLE, size: 8, color: INK } }, margins: { top: 60, bottom: 80, left: 80, right: 80 },
      children: [p(t(h, { bold: true, size: 16, color: INK }), { after: 0 })] })) });
  const rows = filas.map((f) => new TableRow({ cantSplit: true, children: [
    [p(t(f.asunto, { bold: true, size: 18 }), { after: 40, line: 252 }), p(t(f.emisor, { size: 15, color: GRAY }), { after: 0 })],
    [p(t(f.efecto, { size: 17 }), { after: 0, line: 252 })],
    [p(t(f.vigencia, { size: 17 }), { after: 0, line: 252 })],
    [p(t(f.importa, { size: 17 }), { after: 60, line: 252 }),
     ...f.fuente.map(([l, u]) => p([t("Fuente: ", { size: 15, color: GRAY }), link(l, u)], { after: 0, line: 240 }))],
  ].map((ch, i) => new TableCell({ width: { size: widths[i], type: WidthType.DXA }, borders: cellBorders, margins: { top: 100, bottom: 100, left: 80, right: 80 }, children: ch })) }));
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: [head, ...rows] });
}

function reportDoc() {
  return new Document({
    creator: "Emiliano García Milla", title: C.titulo,
    sections: [{ properties: { page }, footers: { default: footer(C.titulo) }, children: [
      p(t(C.titulo, { bold: true, size: 28 }), { after: 60 }),
      rule(),
      p(t("Lo relevante", { bold: true, size: 21 }), { after: 100 }),
      ...C.relevante.map((x) => p(t(x, { size: 19 }), { after: 120, line: 288 })),
      p(t(C.dofTitulo, { bold: true, size: 21 }), { before: 160, after: 120 }),
      table(C.filas, "Vigencia / estado"),
      ...(SJF ? [
        p(t(C.sjfTitulo, { bold: true, size: 21 }), { before: 320, after: 120, pageBreakBefore: true }),
        table(C.sjf, "Tipo, obligatoriedad y fecha"),
      ] : []),
    ] }],
  });
}

function guideDoc() {
  const kids = [
    p(t(G.titulo, { bold: true, size: 28 }), { after: 40 }),
    p(t("Material interno. No forma parte del envío al Licenciado.", { size: 16, color: GRAY }), { after: 60 }),
    rule(),
    p(t("Estado", { bold: true, size: 21 }), { after: 80 }),
    p(t(G.estado, { size: 19 }), { after: 200 }),
    p(t("Qué conviene estudiar primero", { bold: true, size: 21 }), { after: 120 }),
  ];
  G.estudiar.forEach((s) => {
    kids.push(p(t(s.tema, { bold: true, size: 19 }), { before: 120, after: 80 }));
    s.puntos.forEach(([k, v]) => kids.push(p([t(k + ". ", { bold: true, size: 18, color: "333333" }), t(v, { size: 18 })], { after: 70, line: 264 })));
  });
  kids.push(p(t("Control de cobertura", { bold: true, size: 21 }), { before: 280, after: 120 }));
  const widths = [2400, 7680];
  kids.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: G.cobertura.map(([a, b]) => new TableRow({ children: [
    new TableCell({ width: { size: widths[0], type: WidthType.DXA }, borders: cellBorders, margins: { top: 80, bottom: 80, left: 80, right: 80 }, children: [p(t(a, { bold: true, size: 17 }), { after: 0 })] }),
    new TableCell({ width: { size: widths[1], type: WidthType.DXA }, borders: cellBorders, margins: { top: 80, bottom: 80, left: 80, right: 80 }, children: [p(t(b, { size: 17 }), { after: 0 })] }),
  ] })) }));
  kids.push(p(t("Avisos que podrían interesar al despacho", { bold: true, size: 21 }), { before: 280, after: 120, keepNext: true }));
  G.avisos.forEach((x) => kids.push(p(t(x, { size: 18 }), { after: 80, line: 264, numbering: { reference: "b", level: 0 } })));
  kids.push(p(t("Pendientes concretos (desbloqueo)", { bold: true, size: 21 }), { before: 280, after: 120 }));
  G.pendientes.forEach((x) => kids.push(p(t(x, { size: 18 }), { after: 80, line: 264, numbering: { reference: "b", level: 0 } })));
  kids.push(p(t("Comentario sugerido", { bold: true, size: 21 }), { before: 280, after: 100 }));
  kids.push(p(t(C.comentario, { size: 18, italics: true }), { after: 80, line: 276 }));
  return new Document({
    creator: "Emiliano García Milla", title: G.titulo,
    numbering: { config: [{ reference: "b", levels: [{ level: 0, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] }] },
    sections: [{ properties: { page }, footers: { default: footer("Guía interna · " + C.fecha) }, children: kids }],
  });
}

(async () => {
  const tag = SJF ? "DOF_SJF" : "DOF";
  fs.writeFileSync(path.join(OUT, `Actualizacion_${tag}_${C.sufijo}.docx`), await Packer.toBuffer(reportDoc()));
  fs.writeFileSync(path.join(OUT, `Guia_estudio_${tag}_${C.sufijo}.docx`), await Packer.toBuffer(guideDoc()));
  console.log("ok");
})();
