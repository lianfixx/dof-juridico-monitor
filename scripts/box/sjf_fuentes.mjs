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
await p.goto('https://sjf2.scjn.gob.mx/busqueda-principal-tesis', { waitUntil: 'networkidle2', timeout: 90000 });
const retry = async (fn, n = 4) => { let e; for (let i = 0; i < n; i++) { try { return await fn(); } catch (x) { e = x; if (/^404 /.test(String(x.message))) throw x; await new Promise(r => setTimeout(r, 2000 * (i + 1))); } } throw e; };
const post = (url, body) => retry(() => p.evaluate(async (url, body) => { const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }); if (!r.ok) throw new Error(r.status + ' ' + url); return r.json(); }, url, body));
const getJ = (url) => retry(() => p.evaluate(async (url) => { const r = await fetch(url); if (!r.ok) throw new Error(r.status + ' ' + url); return r.json(); }, url));
const getB64 = (url) => retry(() => p.evaluate(async (url) => { const r = await fetch(url); if (!r.ok) throw new Error(r.status + ' ' + url); const buf = new Uint8Array(await r.arrayBuffer()); let s = ''; for (let i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000)); return btoa(s); }, url));

const control = { fecha, consulta: new Date().toISOString(), tipos: {}, anexos: {}, hora_publicacion: null };
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
    const files = await getJ(`/services/${T.svc}/api/public/file/${d.ius}?isSemanal=1`).catch(() => []);
    const anexos = [];
    for (const f of (Array.isArray(files) ? files : [])) {
      const name = f.archivo; const dst = path.join(dest, 'pdf', name);
      if (!fs.existsSync(dst)) {
        const b64 = await getB64(`/api/pdf?path=SJFSem/anexos/${name}`);
        const buf = Buffer.from(b64, 'base64');
        if (buf.subarray(0, 4).toString() !== '%PDF') { anexos.push({ archivo: name, error: 'no es PDF', bytes: buf.length }); continue; }
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
fs.writeFileSync(path.join(dest, 'control.json'), JSON.stringify(control, null, 1));
log('resumen', JSON.stringify(control.resumen), 'hora', control.hora_publicacion);
await b.close();
