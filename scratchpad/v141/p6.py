import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""      pose(nfAdd, {visibility:'visible', display:'flex', position:'absolute', left:'24px', top:(PAGE+46+gensH)+'px',""",
"""      /* ⚑ v141 (Tom, 10 oct. 2026, C-096) : « Dans Peaufiner, l'encart “+ Planter dans le Cercle” prend le même + que dans la fiche, et se place
         juste sous Commentaires ; le reste remonte. » COMMENTAIRES finit à 656 : le bouton est à 672 (16 d'écart, comme entre les cartes),
         342 × 62 au trait de 2, son + dans son rond, à gauche — le bouton de la fiche. (Avant : en page 2, à 806, 348 × 68, sans le rond.) */
      pose(nfAdd, {visibility:'visible', display:'flex', position:'absolute', left:'24px', top:(672+gensH)+'px',""")
rep("""                   width:'348px', height:'68px', margin:'0', padding:'0',
                   'align-items':'center', 'justify-content':'center',
                   background:MAUVE, border:'3px solid '+MAUVE, 'border-radius':'31px',
                   'font-family':'var(--f-libelle)', 'font-weight':'700',
                   'font-size':'19px', color:CREME, '-webkit-text-fill-color':CREME});""",
"""                   width:'342px', height:'62px', margin:'0', padding:'0 12px', gap:'14px', 'box-sizing':'border-box',
                   'align-items':'center', 'justify-content':'flex-start',
                   background:MAUVE, 'border-width':'2px', 'border-style':'solid', 'border-radius':'31px',
                   'font-family':'var(--f-libelle)', 'font-weight':'700',
                   'font-size':'18px', color:CREME, '-webkit-text-fill-color':CREME});""")
rep("    if(nfAdd && nfAdd.getAttribute('data-np-pris') === '1') pose(nfAdd, {top:(PAGE+46+gensH)+'px'});",
    "    if(nfAdd && nfAdd.getAttribute('data-np-pris') === '1') pose(nfAdd, {top:(672+gensH)+'px'});")
rep("  var PAGE=760, TOP=PAGE+130, ECART=104, BLOC=384;",
    "  var PAGE=760, TOP=672+62+16, ECART=104, BLOC=384;   /* v141 (C-096) : « le reste remonte » — le bloc suit le bouton, posé sous COMMENTAIRES (672 + 62 + 16 = 750 ; 890 avant) */")
rep('<style id="lot-V141-MUR-LU-css">','''<style id="lot-V141-CERCLE-css">
/* ⚑ v141 (Tom, 10 oct. 2026, C-096) — LA FICHE D'UN CERCLE.
   « Le bandeau Peaufiner reste tout en bas. L'encart “+ Planter dans le Cercle” remonte juste ce qu'il faut, avec un petit écart au-dessus du
   bandeau. Le fil passe sous l'encart sans jamais le recouvrir. » Le bouton reste la DERNIÈRE LIGNE du fil (Q213) ; tant que cette place est
   sous l'écran, il se tient à 12 pt au-dessus du bandeau (84) : `position:sticky`, le fil défile dessous. */
#detailPoster.dp-nuee:not(.s2-ouv) #dpNueeFil .nf-tete, #detailPoster.dp-mode-nuee:not(.s2-ouv) #dpNueeFil .nf-tete{position:-webkit-sticky!important;position:sticky!important;bottom:96px!important;z-index:6!important}
/* dans Peaufiner : le + dans son rond, comme sur la fiche */
#detailPoster #dpdCorps > #nfAdd .nf-plus{display:grid!important;place-items:center!important;width:40px!important;height:40px!important;flex:none!important;border-radius:50%!important;background:var(--c-creme95)!important;margin:0!important}
#detailPoster #dpdCorps > #nfAdd .nf-plus svg{width:22px!important;height:22px!important;display:block!important}
/* « Dissoudre le Cercle » perd son encart, comme « Supprimer ce Promi » : le mot seul, centré */
#detailPoster #npDiss.np-carte{border-color:transparent!important;background:transparent!important;box-shadow:none!important}
#detailPoster #npDiss .np-lab{position:absolute!important;left:0!important;right:0!important;width:auto!important;text-align:center!important}
#detailPoster #npDiss .np-val{display:none!important}
</style>
<style id="lot-V141-MUR-LU-css">''')
io.open('app.html','w',encoding='utf-8').write(S)
