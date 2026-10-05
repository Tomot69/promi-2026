import io
S=io.open('app.html',encoding='utf-8').read()
old="""#device:not(.light) #murPhrase.sur-tropical{color:var(--c-encre09);-webkit-text-fill-color:var(--c-encre09);--orange-maparole:var(--c-orange-maparole)}"""
new="""#device:not(.light) #murPhrase.sur-tropical{color:var(--c-encre09);-webkit-text-fill-color:var(--c-encre09)}"""
assert S.count(old)==1; S=S.replace(old,new)
old="""    try{ p.classList.toggle('sur-corps', !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet'))); }catch(_){}
    try{ p.classList.toggle('sur-tropical', !!(mur && mur.closest && mur.closest('#detailPoster.corps-tropical, #createSheet.corps-tropical'))); }catch(_){} var D="""
new="""    /* v130 : sur le corps Tropical Breeze d'un Promi (clair), ce n'est plus un « corps sombre » — l'orange des fonds clairs, la phrase à l'encre */
    try{ var _trop=!!(mur && mur.closest && mur.closest('#detailPoster.corps-tropical, #createSheet.corps-tropical'));
      p.classList.toggle('sur-tropical', _trop);
      p.classList.toggle('sur-corps', !_trop && !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet'))); }catch(_){} var D="""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
