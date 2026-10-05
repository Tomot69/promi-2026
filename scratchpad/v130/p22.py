import io
S=io.open('app.html',encoding='utf-8').read()
old="""--c-tropical78:#8ACBE8;--c-encre-attente:rgba(32,25,8,.72);"""
new="""--c-tropical78:#8ACBE8;--c-encre-attente:rgba(32,25,8,.72);--c-encre09:#201908;"""
assert S.count(old)==1; S=S.replace(old,new)
old="""#murPhrase .mp{color:var(--orange-maparole);-webkit-text-fill-color:var(--orange-maparole)}"""
new="""/* v130 (C-050) : posée sur le corps Tropical Breeze d'un Promi (sombre), la phrase suit ce qui est peint sous elle (§3) — l'encre, et
   l'orange des fonds clairs. `--c-encre09` ne bascule pas en sombre (`--c-brun09` y devient la seiche). */
#device:not(.light) #murPhrase.sur-tropical{color:var(--c-encre09);-webkit-text-fill-color:var(--c-encre09);--orange-maparole:var(--c-orange-maparole)}
#murPhrase .mp{color:var(--orange-maparole);-webkit-text-fill-color:var(--orange-maparole)}"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    try{ p.classList.toggle('sur-corps', !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet'))); }catch(_){} var D="""
new="""    try{ p.classList.toggle('sur-corps', !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet'))); }catch(_){}
    try{ p.classList.toggle('sur-tropical', !!(mur && mur.closest && mur.closest('#detailPoster.corps-tropical, #createSheet.corps-tropical'))); }catch(_){} var D="""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('PROMI-TOKENS.json',encoding='utf-8').read()
old='''    "--c-encre-attente": "rgba(32,25,8,.72)",'''
assert J.count(old)==1; J=J.replace(old, old+'''\n    "--c-encre09": "#201908",''')
io.open('PROMI-TOKENS.json','w',encoding='utf-8').write(J)
