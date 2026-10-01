
/* ⚑ L'ENCRE D'UNE NATURE SUR LE CORPS CLAIR — décision Tom, 17 septembre 2026.
   « Pose le compagnon sombre par nature, mode clair seulement. C'est le motif de ma planche
   pour la Nuée, étendu aux trois. Le pastel reste le texte du mode sombre. »

   LA DÉRIVATION EST CELLE DE LA PLANCHE, pas un choix d'œil : sa paire lilas → violet
   (#C9A8F5 L*74,2 C43,2 h308,3 → #291547 L*12,4 C35,8 h309,4) donne ΔL −61,8, un rapport de
   chroma de 0,83 et une teinte tenue. On l'applique telle quelle au bleu et au rose.

     Promi   #82AEF8 → #022140     Δlum sur la crème 82,5   (il était à 24,2)
     Chiche  #FFB8D2 → #3D0F23     Δlum sur la crème 82,6   (il était à 12,9)
     Nuée    #C9A8F5 → #291547     Δlum sur la crème 82,5   (il était à 20,7)   ← la valeur de la planche

   Les trois restent trois : ΔE 20,6 · 26,2 · 30,5 entre eux, et 27 à 44 de l'encre #201908 —
   ils ne se confondent ni entre eux ni avec le texte ordinaire.
   ⚠ MODE CLAIR SEULEMENT : sur le corps SOMBRE ils tombent à Δlum 4,5–5,2. Le pastel y reste. */
window._NATTXT = {promi:'#022140', chiche:'#3D0F23', nuee:'#43291C'};
/* La pastille de nature d'une carte est sur la CRÈME dans LES DEUX thèmes : son encre est
   toujours le compagnon, jamais le pastel. ⚠ GLOBALE, et pas enfermée dans une IIFE : les deux
   peintres de carte vivent dans un autre bloc, et un ReferenceError y est avalé par le
   try/catch du moteur d'Index — la liste sortait VIDE, sans une erreur en console. */
window._nt = function(c){ var T=window._NATTXT||{}, M={'#82AEF8':T.promi,'#FFB8D2':T.chiche,'#C9A8F5':T.nuee};
  return M[String(c).toUpperCase()] || c; };
