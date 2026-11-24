#!/usr/bin/env node
// Revisión de forma de content.js y guia.js contra references/redaccion.md. No juzga el fondo: mide.
// Uso: node scripts/paquete/estilo.js DIR_CONTENIDO     (sale con 1 si hay errores; los avisos no detienen)
const path = require("path");

const APARTADOS = ["De qué se trata", "Qué cambió", "Fundamento", "Cómo opera", "Por qué importa", "Dónde está la discusión", "Para dominarlo"];
const OPCIONALES = new Set(["Dónde está la discusión"]);
const MULETILLAS = ["cabe señalar", "cabe mencionar", "cabe destacar", "es importante mencionar", "es importante señalar", "en este sentido",
  "derivado de lo anterior", "a efecto de", "se hace de su conocimiento", "en términos de lo dispuesto", "agradezco de antemano",
  "no omito mencionar", "por medio del presente", "en virtud de lo anterior"];
const palabras = (t) => String(t || "").trim().split(/\s+/).filter(Boolean).length;
const cuenta = (t, re) => (String(t || "").match(re) || []).length;

function revisar(C, G) {
  const errores = [], avisos = [];
  const prosa = (donde, t, { min, max, tope }) => {
    const n = palabras(t);
    if (!n) return errores.push(`${donde}: vacío`);
    if (tope && n > tope) errores.push(`${donde}: ${n} palabras (tope ${tope}); parte la fila o baja el detalle a la guía`);
    else if ((max && n > max) || (min && n < min)) avisos.push(`${donde}: ${n} palabras (medida ${min || 1} a ${max})`);
    if (cuenta(t, /«/g) > 1) errores.push(`${donde}: ${cuenta(t, /«/g)} citas entre comillas (una como máximo); di la cifra con naturalidad`);
    if (cuenta(t, /;/g) > 1) errores.push(`${donde}: cadena de punto y coma; sepáralo en frases`);
    if (cuenta(t, /:(?!\d)/g) > 0) errores.push(`${donde}: dos puntos dentro del texto; redáctalo como frase`);
    const baja = String(t).toLowerCase();
    MULETILLAS.filter((m) => baja.includes(m)).forEach((m) => errores.push(`${donde}: muletilla «${m}»`));
    const largas = String(t).split(/(?<=[.!?])\s+/).filter((f) => palabras(f) > 45).length;
    if (largas) avisos.push(`${donde}: ${largas} frase(s) de más de 45 palabras`);
  };

  // Versión final de Emi del 24/11/2026: «Lo relevante» es el título de una sola tabla, sin párrafos de resumen
  // (el resumen es el correo), y la tabla lleva pocas filas.
  if ((C.relevante || []).some((x) => palabras(x))) errores.push("«Lo relevante»: ya no lleva párrafos; el resumen va en el correo al Licenciado");
  const total = (C.filas || []).length + (C.sjf || []).length;
  if (!total) errores.push("Tabla: sin filas");
  if (total > 12) avisos.push(`Tabla: ${total} filas; revisa que cada una valga la lectura del Licenciado y que lo secundario esté en la guía`);
  const nPar = (x) => String(x || "").split(/\n\s*\n/).filter((s) => s.trim()).length;
  [["DOF", C.filas || []], ["SJF", C.sjf || []]].forEach(([nombre, filas]) => filas.forEach((f, i) => {
    const d = `${nombre}, fila ${i + 1} («${String(f.asunto || "").slice(0, 40)}»)`;
    const na = palabras(f.asunto);
    if (!na) errores.push(`${d}: sin asunto`);
    if (na > 16) errores.push(`${d}: asunto de ${na} palabras (hasta 12)`);
    else if (na > 12) avisos.push(`${d}: asunto de ${na} palabras (hasta 12)`);
    if (/:(?!\d)/.test(String(f.asunto || ""))) errores.push(`${d}: dos puntos en el asunto`);
    prosa(`${d}, qué ocurrió`, f.efecto, { min: 30, max: 90, tope: 110 });
    if (nPar(f.efecto) > 2) errores.push(`${d}: «qué ocurrió» en ${nPar(f.efecto)} párrafos (dos como máximo, separados por una línea en blanco)`);
    prosa(`${d}, vigencia`, f.vigencia, { max: 25, tope: 40 });
    prosa(`${d}, por qué importa`, f.importa, { min: 8, max: 45, tope: 70 });   // siempre lleva frase (Emi, 24/11/2026)
    if (/\bconviene\b/i.test(String(f.importa || ""))) avisos.push(`${d}: «conviene» en «por qué importa»; Emi quitó esos consejos el 24/11. Di para qué sirve`);
    if (nombre === "SJF" && !/P\.\/J\.|J\/|\(\d+a\.\)/.test(String(f.emisor || ""))) avisos.push(`${d}: el emisor no trae la clave de la tesis (por ejemplo, «Pleno de la Suprema Corte · P./J. 10/2027 (12a.)»)`);
    if (!(f.fuente || []).length) errores.push(`${d}: sin fuente en la fila`);
    if (cuenta(f.efecto, /\d[\d.,]*\s?(%|por ciento|millones|pesos|días|meses|años)/g) > 4) avisos.push(`${d}: más de cuatro cifras en «qué ocurrió»; valora partir la fila`);
  }));
  if (C.comentario !== undefined) {
    const n = palabras(C.comentario);
    if (n < 40 || n > 70) errores.push(`Comentario sugerido: ${n} palabras (de 40 a 70)`);
  }
  if (C.correoLic && Array.isArray(C.correoLic.parrafos)) {
    const texto = C.correoLic.parrafos.join(" ");
    const n = palabras(texto);
    if (n < 120 || n > 230) errores.push(`Correo al Licenciado: ${n} palabras (de 120 a 230)`);
    const bluf = C.correoLic.parrafos[1];
    if (palabras(bluf) > 35) avisos.push(`Correo al Licenciado: el segundo párrafo (lo principal) tiene ${palabras(bluf)} palabras; debe decirse en una frase`);
    if (/:(?!\d)/.test(texto)) errores.push("Correo al Licenciado: dos puntos dentro del texto");
    if (/\[Espacio para mi opinión|Comentario personal/i.test(texto)) errores.push("Correo al Licenciado: la opinión de Emi va ya escrita, sin el espacio «Comentario personal» (decisión de Emi del 24/11/2026)");
    if (!/\b(a mi juicio|considero|me parece|en mi opinión|desde mi punto de vista|estimo)\b/i.test(texto)) avisos.push("Correo al Licenciado: no se ve la opinión de Emi en primera persona (por ejemplo, «a mi juicio…»)");
    (C.sjf || []).forEach((f) => {
      const clave = (String(f.emisor || "").match(/P\.\/J\.\s*\d+\/\d{4}/) || [])[0];
      if (clave && !texto.includes(clave)) avisos.push(`Correo al Licenciado: no menciona la ${clave}; cada jurisprudencia de la tabla va con su clave y su criterio`);
    });
    MULETILLAS.filter((m) => texto.toLowerCase().includes(m)).forEach((m) => errores.push(`Correo al Licenciado: muletilla «${m}»`));
  }

  if (G) {
    if (palabras(G.estado) > 70) errores.push(`Guía, estado: ${palabras(G.estado)} palabras (dos frases; el control va en «Control de cobertura»)`);
    const temas = G.estudiar || [];
    if (temas.length < 1 || temas.length > 5) errores.push(`Guía: ${temas.length} temas (de 1 a 5)`);
    let total = 0;
    temas.forEach((s, i) => {
      const d = `Guía, tema ${i + 1} («${String(s.tema || "").slice(0, 40)}»)`;
      const claves = (s.puntos || []).map(([k]) => String(k).replace(/[.:]\s*$/, ""));
      const ajenas = claves.filter((k) => !APARTADOS.includes(k));
      if (ajenas.length) errores.push(`${d}: apartados fuera de la lista (${ajenas.join(", ")})`);
      const faltan = APARTADOS.filter((k) => !OPCIONALES.has(k) && !claves.includes(k));
      if (faltan.length) errores.push(`${d}: faltan apartados (${faltan.join(", ")})`);
      const orden = claves.filter((k) => APARTADOS.includes(k)).map((k) => APARTADOS.indexOf(k));
      if (orden.some((x, j) => j && x <= orden[j - 1])) errores.push(`${d}: apartados repetidos o fuera de orden`);
      (s.puntos || []).forEach(([k, v]) => { total += palabras(v); prosa(`${d}, ${k}`, v, { min: 30, max: 90, tope: 120 }); });
    });
    if (temas.length && (total < 150 * temas.length || total > 1100)) avisos.push(`Guía: ${total} palabras en los temas (de 600 a 1,100 con tres o más temas)`);
    (G.avisos || []).forEach((t, i) => { if (palabras(t) > 45) avisos.push(`Guía, aviso ${i + 1}: ${palabras(t)} palabras (una línea)`); });
  }
  return { errores, avisos };
}

module.exports = { revisar, APARTADOS };

if (require.main === module) {
  const dir = path.resolve(process.argv[2] || ".");
  let C;
  try { C = require(path.join(dir, "content.js")); } catch (e) { console.log(`ERROR: no se pudo cargar content.js de ${dir} (${e.message.split("\n")[0]})`); process.exit(1); }
  let G = null;
  try { G = require(path.join(dir, "guia.js")); } catch (e) { console.log("AVISO: no hay guia.js en la carpeta"); }
  const { errores, avisos } = revisar(C, G);
  avisos.forEach((x) => console.log("AVISO: " + x));
  errores.forEach((x) => console.log("ERROR: " + x));
  console.log(`Estilo: ${errores.length} errores, ${avisos.length} avisos`);
  process.exit(errores.length ? 1 : 0);
}
