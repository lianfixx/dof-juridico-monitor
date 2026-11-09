// Uso: node email.js DIR_CONTENIDO DIR_SALIDA  → Correo_revision_<DOF|DOF_SJF>_<sufijo>.html
const P=require("path"),DIR=P.resolve(process.argv[2]),OUT=process.argv[3];
const C=require(P.join(DIR,"content.js")),G=require(P.join(DIR,"guia.js"));const SJF=Array.isArray(C.sjf)&&C.sjf.length>0;
const esc=s=>s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const mk=arr=>arr.map(f=>`<tr><td style="padding:10px 0;border-bottom:1px solid #e5e5e5;vertical-align:top"><div style="font-weight:600;color:#111">${esc(f.asunto)}</div><div style="margin-top:4px;color:#333">${esc(f.efecto)}</div><div style="margin-top:4px;color:#666;font-size:13px">${esc(f.vigencia)}</div></td></tr>`).join("");
const rows=mk(C.filas), rowsS=SJF?mk(C.sjf):"";
const correo=C.correoLic.parrafos.map(x=>`<p style="margin:0 0 10px">${esc(x)}</p>`).join("");
const pend=G.pendientes.map(x=>`<li style="margin-bottom:6px">${esc(x)}</li>`).join("");
const h=`<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(C.titulo)}</title></head>
<body style="margin:0;background:#f4f4f4;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;color:#111">
<div style="max-width:640px;margin:0 auto;padding:16px"><div style="background:#fff;border:1px solid #e5e5e5;padding:28px 24px">
<div style="font-size:20px;font-weight:600">${esc(C.titulo)}</div>
<div style="color:#666;font-size:13px;margin-top:4px">Para tu revisión antes de enviar al Lic. Castorena</div>
<hr style="border:0;border-top:1px solid #e5e5e5;margin:20px 0">
<div style="font-size:12px;letter-spacing:.08em;color:#666;font-weight:600">PARA EL LIC. CASTORENA</div>
<div style="margin-top:10px">${C.relevante.map(x=>`<p style="margin:0 0 10px">${esc(x)}</p>`).join("")}</div>
<div style="margin-top:6px;font-weight:600">Diario Oficial de la Federación</div><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:14px">${rows}</table>${SJF?`<div style="margin-top:16px;font-weight:600">${esc(C.sjfTitulo)}</div><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:14px">${rowsS}</table>`:""}
<div style="margin-top:22px;font-size:13px;color:#666">Asunto: ${esc(C.correoLic.asunto)}</div>
<div style="margin-top:8px;padding:14px 16px;border-left:2px solid #111;background:#fafafa">${correo}</div>
<hr style="border:0;border-top:1px solid #e5e5e5;margin:24px 0">
<div style="font-size:12px;letter-spacing:.08em;color:#666;font-weight:600">SOLO PARA TI</div>
<p style="margin:12px 0 6px;font-weight:600">Comentario sugerido</p><p style="margin:0;font-style:italic;color:#333">${esc(C.comentario)}</p>
<p style="margin:18px 0 6px;font-weight:600">Qué estudiar primero</p><p style="margin:0">${G.estudiar.map(s=>esc(s.tema)).join("<br>")}</p>
<p style="margin:18px 0 6px;font-weight:600">Nota de control</p><p style="margin:0 0 8px">${esc(G.estado)}</p><ul style="margin:0;padding-left:18px;color:#333;font-size:14px">${pend}</ul><p style="margin:18px 0 6px;font-weight:600">Avisos de interés</p><ul style="margin:0;padding-left:18px;color:#333;font-size:14px">${G.avisos.map(x=>`<li style="margin-bottom:6px">${esc(x)}</li>`).join("")}</ul>
</div></div></body></html>`;
require("fs").writeFileSync(P.join(OUT,`Correo_revision_${SJF?"DOF_SJF":"DOF"}_${C.sufijo}.html`),h);
