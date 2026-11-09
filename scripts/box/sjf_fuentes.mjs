// Fuentes del Semanario Judicial de la Federación (publicación semanal) para dof-castorena.
// Uso: node sjf_fuentes.mjs DESTINO AAAA-MM-DD   (fecha del viernes de publicación)
// Usa Chrome headless del box (pasa el muro anti-bots de sjf2.scjn.gob.mx) y la API pública
// que la propia aplicación del SJF consume. Guarda JSON crudo, texto plano por documento,
// anexos PDF (con SHA-256 y texto) y DESTINO/control.json.
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const [dest, fecha] = process.argv.slice(2);
if (!dest || !/^\d{4}-\d\d-\d\d$/.test(fecha || '')) { console.error('Uso: sjf_fuentes.mjs DESTINO AAAA-MM-DD'); process.exit(2); }
for (const d of ['raw', 'txt', 'pdf']) fs.mkdirSync(path.join(dest, d), { recursive: true });
const log = (...a) => console.log(new Date().toISOString().slice(11, 19), ...a);
// Se marca EN_CURSO al empezar: si la corrida se interrumpe, nadie toma por bueno un control viejo.
const ctlPath = path.join(dest, 'control.json');
if (fs.existsSync(ctlPath)) fs.renameSync(ctlPath, path.join(dest, `control.anterior.json`));
fs.writeFileSync(ctlPath, JSON.stringify({ fecha, consulta: new Date().toISOString(), estado: 'EN_CURSO', resumen: {}, hora_publicacion: null }, null, 1));

const TIPOS = {
  tesis:       { svc: 'sjftesismicroservice',      list: 'tesis',       cls: [{ name: 'numInstancia', value: ['6','60','7','70','80','1','2','50'] }, { name: 'tipoDocumento', value: ['1'] }], pref: 'T' },
  ejecutorias: { svc: 'sjfejecutoriamicroservice', list: 'ejecutorias', cls: [{ name: 'idTipoEjecutoria', value: ['1','2','3'] }], pref: 'E' },
  votos:       { svc: 'sjfvotosmicroservice',      list: 'votos',       cls: [{ name: '-parteT', value: ['99'] }], pref: 'V' },
  acuerdos:    { svc: 'sjfacuerdosmicroservice',   list: 'acuerdos',    cls: [{ name: 'idTipoAcuerdo', value: ['1','2','3','4','5'] }], pref: 'A' },
};
const base = { searchTerms: [], bFacet: false, ius: [], idApp: 'SJFAPP2020', lbSearch: [], filterExpression: '' };
const strip = (s) => (s == null ? '' : String(s)).replace(/<br\s*\/?>/gi, '\n').replace(/<\/p>/gi, '\n').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/\r/g, '').trim();
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');

const b = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--proxy-server=http://127.0.0.1:3128'] });
const p = await b.newPage();
const HOME = 'https://sjf2.scjn.gob.mx/busqueda-principal-tesis';
await p.goto(HOME, { waitUntil: 'networkidle2', timeout: 90000 });
// El muro anti-bots (Incapsula) puede responder con una página HTML en lugar de JSON tras
// varias consultas seguidas (9/11/2026). Ante eso se recarga la página principal para volver
// a pasar el muro y se reintenta con esperas más largas.
const bloqueo = (m) => /BLOQUEO|Unexpected token '<'|is not valid JSON/.test(m);
const retry = async (fn, n = 6) => { let e; for (let i = 0; i < n; i++) { try { return await fn(); } catch (x) { e = x; const m = String(x.message); if (/^404 /.test(m)) throw x; if (bloqueo(m)) { log('muro anti-bots: recargo y reintento', i + 1); await p.goto(HOME, { waitUntil: 'networkidle2', timeout: 90000 }).catch(() => {}); await new Promise(r => setTimeout(r, 15000 * (i + 1))); } else await new Promise(r => setTimeout(r, 2000 * (i + 1))); } } throw e; };
const post = (url, body) => retry(() => p.evaluate(async (url, body) => { const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }); if (!r.ok) throw new Error(r.status + ' ' + url); const t = await r.text(); if (/^\s*</.test(t)) throw new Error('BLOQUEO html en ' + url); return JSON.parse(t); }, url, body));
const getJ = (url) => retry(() => p.evaluate(async (url) => { const r = await fetch(url); if (!r.ok) throw new Error(r.status + ' ' + url); const t = await r.text(); if (/^\s*</.test(t)) throw new Error('BLOQUEO html en ' + url); return JSON.parse(t); }, url));
const getB64 = (url) => retry(() => p.evaluate(async (url) => { const r = await fetch(url); if (!r.ok) throw new Error(r.status + ' ' + url); const buf = new Uint8Array(await r.arrayBuffer()); let s = ''; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000)); return btoa(s); }, url));

const control = { fecha, consulta: new Date().toISOString(), estado: 'EN_CURSO', tipos: {}, anexos: {}, hora_publicacion: null, errores: [] };
for (const [tipo, T] of Object.entries(TIPOS)) {
  const docs = [];
  for (let page = 0; page < 50; page++) {
    const r = await post(`/services/${T.svc}/api/public/${T.list}?page=${page}&size=100`, { ...base, classifiers: [{ name: 'idEpoca', value: ['210'] }, ...T.cls] });
    const ds = r.documents || [];
    for (const d of ds) if ((d.fechaPublicacion || '').slice(0, 10) === fecha) docs.push(d);
    const minDate = ds.length ? ds.map(d => (d.fechaPublicacion || '').slice(0, 10)).sort()[0] : '';
    if (!ds.length || minDate < fecha) break;
  }
  log(tipo, docs.length);
  const items = [];
  for (const d of docs) {
    const det = await getJ(`/services/${T.svc}/api/public/${T.list}/${d.ius}?isSemanal=true`).catch(e => ({ _error: String(e) }));
    if (det._error) control.errores.push({ tipo, ius: d.ius, paso: 'detalle', error: det._error });
    const full = { ...d, ...det };
    fs.writeFileSync(path.join(dest, 'raw', `${T.pref}${d.ius}.json`), JSON.stringify(full, null, 1));
    const m = /a las (\d\d:\d\d)/.exec(d.textoPublicacion || ''); if (m && !control.hora_publicacion) control.hora_publicacion = m[1];
    let out = `# ${tipo} ${d.ius}\n`;
    for (const [k, v] of Object.entries(full)) {
      if (v == null || v === '' || typeof v === 'object' && !Array.isArray(v)) continue;
      if (Array.isArray(v)) { if (v.length && typeof v[0] !== 'object') out += `## ${k}\n${v.join(', ')}\n\n`; continue; }
      out += `## ${k}\n${strip(v)}\n\n`;
    }
    fs.writeFileSync(path.join(dest, 'txt', `${T.pref}${d.ius}.txt`), out);
    // 404 en la lista de anexos = el registro no tiene anexos (comprobado el 9/11/2026 en 28 tesis del 06/11/2026); otro error sí se registra.
    const files = await getJ(`/services/${T.svc}/api/public/file/${d.ius}?isSemanal=1`).catch(e => { if (!/^(Error: )?404 /.test(String(e))) control.errores.push({ tipo, ius: d.ius, paso: 'lista de anexos', error: String(e) }); return []; });
    const anexos = [];
    for (const f of (Array.isArray(files) ? files : [])) {
      const name = f.archivo; const dst = path.join(dest, 'pdf', name);
      if (!fs.existsSync(dst)) {
        let b64; try { b64 = await getB64(`/api/pdf?path=SJFSem/anexos/${name}`); } catch (e) { anexos.push({ archivo: name, error: String(e) }); control.errores.push({ tipo, ius: d.ius, paso: 'anexo', archivo: name, error: String(e) }); continue; }
        const buf = Buffer.from(b64, 'base64');
        if (buf.subarray(0, 4).toString() !== '%PDF') { anexos.push({ archivo: name, error: 'no es PDF', bytes: buf.length }); control.errores.push({ tipo, ius: d.ius, paso: 'anexo', archivo: name, error: 'no es PDF' }); continue; }
        fs.writeFileSync(dst, buf);
      }
      const txt = path.join(dest, 'txt', `ANX_${name.replace(/\.pdf$/i, '')}.txt`);
      try { execFileSync('pdftotext', ['-layout', dst, txt]); } catch { }
      const pages = (execFileSync('pdfinfo', [dst]).toString().match(/Pages:\s+(\d+)/) || [])[1];
      const a = { archivo: name, frase: f.frase, sha256: sha(dst), paginas: Number(pages), texto_chars: fs.existsSync(txt) ? fs.statSync(txt).size : 0 };
      anexos.push(a); control.anexos[name] = a.sha256;
    }
    items.push({ ius: d.ius, clave: d.claveTesis || null, ta_tj: d.ta_tj ?? null, rubro: strip(d.rubro).slice(0, 200), tipoAsuntoE: d.tipoAsuntoE || null, anexos });
  }
  control.tipos[tipo] = { total: items.length, items };
}
control.resumen = Object.fromEntries(Object.entries(control.tipos).map(([k, v]) => [k, v.total]));
control.resumen.jurisprudencias = (control.tipos.tesis?.items || []).filter(i => String(i.ta_tj) === '1').length;
control.resumen.aisladas = (control.tipos.tesis?.items || []).filter(i => String(i.ta_tj) !== '1').length;
control.resumen.anexos = Object.keys(control.anexos).length;
control.resumen.errores = control.errores.length;
control.estado = 'COMPLETO';
fs.writeFileSync(ctlPath + '.tmp', JSON.stringify(control, null, 1)); fs.renameSync(ctlPath + '.tmp', ctlPath);
log('resumen', JSON.stringify(control.resumen), 'hora', control.hora_publicacion);
await b.close();
if (control.errores.length) { console.error('ERRORES SJF:', JSON.stringify(control.errores)); process.exit(1); }
