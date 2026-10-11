import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n, ('motif', S.count(old), old[:70]); S=S.replace(old,new)
rep("""  function solPalette(){
    try{ var c=window.Toile.cols();
      if(c && c.length){ var t=c[Math.max(0,Math.min(SOL_IDX, c.length-1))] || c[0];""",
"""  /* ⚑ v142 (Tom, 11 oct. 2026, C-083) — LA PELOTE SOUS LA PALETTE PAR DÉFAUT. « Sous Ingénu, les couleurs de la Pelote sont ternes. Sous Ingénu
     seulement, les poils et le corps se tirent parmi les couleurs des trois natures (#82AEF8, #FFB8D2, #C9A8F5) et leurs teintes voisines,
     jamais parmi les crèmes. Le corps reste d'une autre teinte que les poils. »
     POURQUOI C'ÉTAIT TERNE, mesuré : ① le quatrième ton d'Ingénu est le crème dalle (#EFE3C7) : une ouverture sur quatre il faisait les poils,
     et il était le corps de presque toutes les autres ; ② en clair le poil est le ton × 0,38 (la clarté de Q210) : un bleu marine sourd
     (#1B436F) là où la nature est #82AEF8. Sous Ingénu : les poils et le corps sont tirés parmi les TROIS NATURES ; en clair le poil garde
     la teinte de sa nature, plus dense qu'elle (clarté OKLCH ≤ 0,60, chroma × 1,5 — une « teinte voisine »), puis le garde-fou de la page. */
  function ingenu(){ try{ return window.Toile.mondeCourant().p==='signal'; }catch(_){ return false; } }
  function solPalette(){
    try{ var c=window.Toile.cols();
      if(c && c.length){ var t=c[Math.max(0,Math.min((ingenu()&&SOL_IDX>2)?(SOL_IDX%3):SOL_IDX, c.length-1))] || c[0];""")
rep("""    var L=[], i, j, t; for(i=0;i<n;i++) if(i!==SOL_IDX) L.push(i);
    for(i=L.length-1;i>0;i--){ j=(Math.random()*(i+1))|0; t=L[i]; L[i]=L[j]; L[j]=t; }
    CORPS_ORDRE=L; CORPS_MEMO.cle='';""",
"""    var L=[], i, j, t, ing=ingenu(), sI=(ing&&SOL_IDX>2)?(SOL_IDX%3):SOL_IDX; for(i=0;i<n;i++) if(i!==sI && !(ing && i>2)) L.push(i);   /* v142 : sous Ingénu, jamais le crème (le quatrième ton) */
    for(i=L.length-1;i>0;i--){ j=(Math.random()*(i+1))|0; t=L[i]; L[i]=L[j]; L[j]=t; }
    CORPS_ORDRE=L; CORPS_MEMO.cle='';""")
rep("""    if(!CORPS_ORDRE.length || CORPS_ORDRE.some(function(i){ return i>=P.length || i===SOL_IDX; })) nouveauCorps();""",
"""    var _ing=ingenu(); if(!CORPS_ORDRE.length || CORPS_ORDRE.some(function(i){ return i>=P.length || i===SOL_IDX || (_ing && i>2); })) nouveauCorps();""")
rep("""    var poil=PEL.solR||solEffectif(), cle=[poil[0]|0,poil[1]|0,poil[2]|0,SOL_IDX,CORPS_ORDRE.join('.'),""","""    var poil=PEL.solR||solEffectif(), cle=[poil[0]|0,poil[1]|0,poil[2]|0,SOL_IDX,_ing?1:0,CORPS_ORDRE.join('.'),""")
rep("""    if(!c){ c=corpsTient([CREME[0],CREME[1],CREME[2]], poil) ? [CREME[0],CREME[1],CREME[2]] : [5,3,2]; idx=-1; }
    CORPS_MEMO={cle:cle, c:c, idx:idx};""",
"""    if(!c && _ing && CORPS_ORDRE.length){ q=P[CORPS_ORDRE[0]]; s=versNoir(q, 0.45); c=[Math.round(s[0]),Math.round(s[1]),Math.round(s[2])]; idx=CORPS_ORDRE[0]; }   /* v142 : sous Ingénu le dernier recours reste une teinte d'une nature, jamais la crème */
    if(!c){ c=corpsTient([CREME[0],CREME[1],CREME[2]], poil) ? [CREME[0],CREME[1],CREME[2]] : [5,3,2]; idx=-1; }
    CORPS_MEMO={cle:cle, c:c, idx:idx};""")
rep("""      SOL_IDX=(Math.random()*n)|0;
      try{ nouveauCorps(); }catch(_){}""","""      SOL_IDX=(Math.random()*(ingenu()?Math.min(3,n):n))|0;   /* v142 : sous Ingénu, l'une des trois natures */
      try{ nouveauCorps(); }catch(_){}""")
rep("""    var p=solPalette(), s=p;
    if(clair()){
      s=[Math.round(p[0]*SOL_CLAIR), Math.round(p[1]*SOL_CLAIR), Math.round(p[2]*SOL_CLAIR)];""",
"""    var p=solPalette(), s=p;
    if(clair() && ingenu() && window._teinte){ var _o=window._teinte.okl(p); return ecarteDeLaPage(window._teinte.deOkl(Math.min(_o[0], ING_L), _o[1]*ING_C, _o[2])); }   /* v142 : la teinte de la nature, plus dense */
    if(clair()){
      s=[Math.round(p[0]*SOL_CLAIR), Math.round(p[1]*SOL_CLAIR), Math.round(p[2]*SOL_CLAIR)];""")
rep("""  var SOL_CREME=0.39;""","""  var SOL_CREME=0.39, ING_L=0.60, ING_C=1.5;""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
