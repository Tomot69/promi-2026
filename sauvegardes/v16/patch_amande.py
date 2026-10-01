# Lot v16 — décision 3 et « l'amande sort partout où elle n'est pas la célébration ».
# Trois propriétaires peignaient l'amande sur le sombre : lot-V10-SOMBRE (la passe + « TENUE »),
# lot-V13-js (la lisibilité des corps), et une règle CSS de la fiche tenue. Ils gardent leur
# mécanique (une marque suit ce qui est peint SOUS elle) ; seule la valeur change : CRÈME.
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
def rep(a,b,n=1):
    global S; c=S.count(a); assert c==n,(c,a[:80]); S=S.replace(a,b)
rep("  var TENU='#00341A', AMANDE='#8FE08F', CRETE='#0B4A2A';\n  function rgbDe(c)",
    "  /* ⚑ v16 (Tom) : un texte d'état sur fond sombre passe CRÈME — l'amande ne peint que la célébration.\n     Le nom reste (trois lectures le partagent) ; la valeur est la crème. */\n  var TENU='#00341A', AMANDE='#F7F0DE', CRETE='#0B4A2A';\n  function rgbDe(c)")
rep("  function marqueTenue(racine){\n    var n = racine || document.getElementById('device'); if(!n) return;",
    "  function marqueTenue(racine){\n    /* ⚑ v16 (Tom) : « TENUE » ne se marque plus en amande — l'amande n'est que la célébration. */\n    return;\n    var n = racine || document.getElementById('device'); if(!n) return;")
rep("      var v = estTenu(el,f) ? AMANDE : (lum(f)<128 ? CREME : '#201908');",
    "      var v = (lum(f)<128 ? CREME : '#201908');   /* ⚑ v16 : crème sur le sombre, tenu compris */", 2)
rep("""/* les marques d'état : l'amande, dans les deux thèmes, parce que le corps est sombre */""",
    """/* les marques d'état : ⚑ v16 — CRÈME, dans les deux thèmes (l'amande n'est que la célébration) */""")
rep("""#device #detailPoster#detailPoster.f-tenue #dpTete .dpt-qui b,.frame #detailPoster#detailPoster.f-tenue #dpTete .dpt-qui b{
  color:var(--c-menthe82)!important;-webkit-text-fill-color:var(--c-menthe82)!important}""",
    """#device #detailPoster#detailPoster.f-tenue #dpTete .dpt-qui b,.frame #detailPoster#detailPoster.f-tenue #dpTete .dpt-qui b{
  color:var(--c-creme95)!important;-webkit-text-fill-color:var(--c-creme95)!important}""")
io.open(F,'w',encoding='utf-8').write(S); print('ok')
