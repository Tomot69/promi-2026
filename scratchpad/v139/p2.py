import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:60]); S=S.replace(a,b)
# 1 · peintre de secours : la même limite franche
a=S.index("    var _B=cv.__bd;\n"); b=S.index("    g.putImageData(_bi,_B.x,_B.y);\n")+len("    g.putImageData(_bi,_B.x,_B.y);\n")
S=S[:a]+"""    /* ⚑ v139 (Tom, 9 oct. 2026, C-083) — LA LIMITE FRANCHE, comme sur la carte graphique : rien au-delà du rayon de la boule. Le repli de
       couleur de v138 (table `cv.__bd`) est retiré avec la frange qu'il corrigeait. */
    g.save(); g.setTransform(1,0,0,1,0,0); g.globalCompositeOperation='destination-in'; g.beginPath(); g.arc(CX,CY,R*(window._peloteBord||1.0),0,6.283185307); g.fill(); g.restore();
"""+S[b:]
# 2 · l'ombre revient
rep("    BO=el('div','au-bo'); CV=el('canvas'); CV.id='auBoule'; BO.appendChild(CV);",
"""    /* ⚑ v139 (Tom, 9 oct. 2026, C-083) — « L'ombre revient, sous la Pelote, dans les deux thèmes (géométrie de v121). Rien d'autre autour :
       ni halo, ni liseré. » Un seul nœud, posé SOUS la boule. */
    var _om139=el('div','au-ombre'); _om139.id='auPeloteOmbre'; CAD.appendChild(_om139);
    BO=el('div','au-bo'); CV=el('canvas'); CV.id='auBoule'; BO.appendChild(CV);""")
rep("""/* ⚑ v137 (Tom, 8 oct. 2026, C-071) — « Code mort : retire le peintre du halo""","""/*VOIR lot-V139-OMBRE-css*/
/* ⚑ v137 (Tom, 8 oct. 2026, C-071) — « Code mort : retire le peintre du halo""")
i=S.index("/*VOIR lot-V139-OMBRE-css*/"); j=S.index("</style>",i)+len("</style>")
S=S[:j]+"""
<style id="lot-V139-OMBRE-css">
/* ⚑ v139 (Tom, 9 oct. 2026, C-083) — L'OMBRE DE LA PELOTE REVIENT, DANS LES DEUX THÈMES. Géométrie de v121 : une ellipse de 0,45 D × 0,07 D
   (104,429 × 16,245), l'encre du mode à 0,10 en clair, la crème à 0,105 en sombre (v123). Sa place : celle de la composition B (391,224),
   remontée de 5 pt avec le bas de la silhouette (la limite franche est au rayon de la boule, 116 pt ; la frange allait à 121) — le même
   écart qu'avant entre la Pelote et son ombre. C'est la SEULE exception de la liste blanche de `redteam_volume`. */
#auraScreen.au2 .au-ombre{position:absolute!important;left:142.786px!important;top:386.224px!important;width:104.429px!important;height:16.245px!important;
  margin:0!important;pointer-events:none;z-index:0;background:radial-gradient(closest-side,rgba(var(--c-brun09-rgb),.10),rgba(var(--c-brun09-rgb),0))}
#device:not(.light) #auraScreen.au2 .au-ombre{background:radial-gradient(closest-side,rgba(var(--c-creme95-rgb),.105),rgba(var(--c-creme95-rgb),0))!important}
</style>"""+S[j:]
rep("/*VOIR lot-V139-OMBRE-css*/\n","")
io.open(f,'w',encoding='utf-8').write(S)
