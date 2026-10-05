import io
S=io.open('app.html',encoding='utf-8').read()
old="""    if(!light && n==='promi' && !tenu){ e.colTexte=ENCRE; e.corpsPastel=true; }"""
new="""    /* ⚠ ce résolveur sert AUSSI aux cartes de l'Index et du Fil, dont le corps reste sombre : il ne fait que DÉCLARER le corps pastel ;
       c'est le poseur de la fiche qui en tire l'encre (une première écriture posait l'encre ici : les cartes la prenaient). */
    if(!light && n==='promi' && !tenu){ e.corpsPastel=true; }"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    var encre = (e.light || e.corpsPastel) ? ENCRE : CREME;   /* v130 : sur Tropical Breeze, l'encre */"""
new="""    var encre = (e.light || e.corpsPastel) ? ENCRE : CREME;   /* v130 : sur Tropical Breeze, l'encre */
    if(e.corpsPastel) e.colTexte = ENCRE;"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
