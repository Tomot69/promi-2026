/**
 * « DE » OU « D’ » (Tom, 22 sept. ; v210 §6 ; v212, C-312 : une place vide porte la liaison de SON EXEMPLE) — la règle du prototype
 * (`_promiElide`, la même que liaison_regle.py, le juge) : le premier mot, en minuscules, sans accents ; « d’ » devant une voyelle, un h muet,
 * « y » et « en » ; « de » devant un h aspiré (la liste), un y consonne, « onze », « onzième », « oui », un chiffre.
 */
const H_ASPIRE = new Set(
  'hurler hair hausser heurter hisser hater harceler hacher hanter heler honte haine hasard hasarder haleter happer harasser hennir herisser hocher huer hululer hurle hais hait hate haut hors huit heros hockey harponner heurte'.split(
    ' ',
  ),
);

function norme(s: string): string {
  return s.toLowerCase().replace(/æ/g, 'ae').replace(/œ/g, 'oe').normalize('NFD').replace(/[̀-ͯ]/g, '');
}

export function elision(texte: string): 'de' | 'd’' {
  const m = /^[^\s’'"“«(]+/.exec(texte.trim());
  if (!m) return 'de';
  const w = norme(m[0]).replace(/[^a-z0-9]/g, '');
  if (!w) return 'de';
  const c = w.charAt(0);
  if (/[0-9]/.test(c) || w === 'onze' || w === 'onzieme' || w === 'oui') return 'de';
  if (w === 'y' || w === 'en') return 'd’';
  if (c === 'y') return 'de';
  if (c === 'h') return H_ASPIRE.has(w) ? 'de' : 'd’';
  return 'aeiou'.includes(c) ? 'd’' : 'de';
}
