import io,re
S=io.open('app.html',encoding='utf-8').read()
a=S.index('<style id="lot-V139-CREME-css">'); b=S.index('</style>',a)+len('</style>')
S=S[:a]+"""<style id="lot-V139-CREME-css">
/* ⚑ v141 (Tom, 11 oct. 2026, C-084 — RETOUR EN ARRIÈRE) : « Le crème #EAD9B9 est trop beige sur téléphone. Le corps et les encarts des fiches
   reprennent le ton clair le plus clair de l'app, comme avant v139. Aucun troisième ton clair : il y en a deux dans l'app, pas plus. Les cartes
   du fil d'un Cercle reprennent leur valeur d'avant v139. » Les règles de v139 sont RETIRÉES : le corps et l'encart retrouvent #F7F0DE, les
   cartes #E9D8B7. Ce bloc reste, vide, pour l'histoire. */
</style>"""+S[b:]
o="""background:(e.light?'#F7F0DE' /* v139 (C-084) : le corps de la fiche prend #EAD9B9 — la carte passe à la crème claire, comme sur la page du Fil (#E9D8B7 avant) */:CARTE[e.nat])"""
assert S.count(o)==1
S=S.replace(o,"""background:(e.light?'#E9D8B7' /* v141 (C-084) : retour à la valeur d'avant v139 */:CARTE[e.nat])""")
io.open('app.html','w',encoding='utf-8').write(S)
