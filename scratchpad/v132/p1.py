import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
# la liste de l'Aura : la plus récente en premier
rep("""    var L=D.T.slice();   /* v131 : toutes, dans l'ordre où elles ont été tenues */""","""    var L=D.T.slice().reverse();   /* v131 : toutes · v132 (Tom) : la plus récente EN PREMIER — « la parole qu'on vient de tenir doit se voir sans défiler » */""")
rep("""      moisson:D.T.map(function(p){ return p.id; }),""","""      moisson:D.T.slice().reverse().map(function(p){ return p.id; }),""")
# jetons
rep("--c-cobalt50:#273CEB;","--c-cobalt50:#273CEB;--c-lilas85:#DAC3FF;")
lot=r'''<style id="lot-V132-COBALT-css">
/* ⚑ v132 (Tom, 5 oct. 2026) — DEUX TEXTES SOUS 4,5:1 SUR LE COBALT.
   C-054 · « La phrase lilas de la page + garde sa teinte, éclaircie jusqu'à 4,5:1 » : #C4A2F5 (3,35:1) → #DAC3FF (OKLCH h −58°, la même teinte ;
   4,51:1 sur #273CEB). Sur la page + d'un Promi, en sombre, et là seulement : le jeton du lilas y est remplacé, aucune règle n'est touchée.
   C-053 · « SUPPRIMER CE PROMI passe en crème : le #DD4D23 est une couleur d'état et ne sert à rien d'autre » — le libellé et sa corbeille,
   dans le Peaufiner d'une fiche : crème en sombre, encre en clair (jamais l'orange d'état). */
#device.device:not(.light) #createSheet:not([data-kind="chiche"]):not([data-kind="nuee"]){--c-mauve75:var(--c-lilas85)}
#device#device #detailPoster#detailPoster .s2-reg.v16-danger.v16-danger .s2-lab{color:var(--c-creme95)!important;-webkit-text-fill-color:var(--c-creme95)!important}
#device#device #detailPoster#detailPoster .s2-reg.v16-danger.v16-danger::before{background:var(--c-creme95)!important}
#device#device.light #detailPoster#detailPoster .s2-reg.v16-danger.v16-danger .s2-lab{color:var(--c-brun09)!important;-webkit-text-fill-color:var(--c-brun09)!important}
#device#device.light #detailPoster#detailPoster .s2-reg.v16-danger.v16-danger::before{background:var(--c-brun09)!important}
</style>
</body>'''
assert S.count("</script>\n</body>")==1; S=S.replace("</script>\n</body>","</script>\n"+lot)
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('PROMI-TOKENS.json',encoding='utf-8').read()
a='''    "--c-cobalt50": "#273CEB",'''; assert J.count(a)==1; J=J.replace(a,a+'''\n    "--c-lilas85": "#DAC3FF",''')
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(J)
