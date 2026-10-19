global.window = global; global.document = undefined;
require('../../variantes/trace-chemins-atkinson.js'); require('../../variantes/trace-chemins-gilbert.js'); require('../../variantes/trace-lettres.js');
const [pol, car] = process.argv.slice(2);
for (const v of ['h','b']) { const p = TraceLettres.parcours(pol, car, v); if (!p || p.variante !== v) continue;
  console.log(v, 'ordre', JSON.stringify(p.ordre), 'mi', p.mi);
  p.traits.forEach((t,i)=>console.log(' trait', i, 'R', t.R.toFixed(1), 'L', t.L.toFixed(0), 'b0', t.b0, 'b1', t.b1, 'de', t.pts[0].map(Math.round), 'à', t.pts[t.pts.length-1].map(Math.round), 'n', t.pts.length));
  console.log(' repassages', p.repassages.map(r=>r.length), 'sauts', p.sauts.length); }
