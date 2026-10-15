// inventaire.js — ce que portent les données engendrées : glyphes absents, variantes manquantes (node inventaire.js [gilbert|promilate])
global.window = global; const cle = process.argv[2] || 'gilbert';
require('../../../variantes/trace-chemins-' + cle + '.js'); const D = Object.values(TraceLettresChemins)[0], g = D.g;
const voulu = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZéèêëàâçùûôîï0123456789.,'’!?«»…:+";
console.log('glyphes', Object.keys(g).length);
console.log('absents :', [...voulu].filter(c => !g[c]).join(' '));
console.log('sans h :', [...voulu].filter(c => g[c] && !g[c].h).join(' '));
console.log('sans b :', [...voulu].filter(c => g[c] && !g[c].b).join(' '));
if (process.argv[3]) for (const c of process.argv[3]) console.log(c, JSON.stringify(g[c]));
