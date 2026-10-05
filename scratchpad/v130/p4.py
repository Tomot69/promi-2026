import io
S=io.open('app.html',encoding='utf-8').read()
a="""    if(!cv.__glc){
      cv.__glc=G.cv; G.cv.id='auBouleGL'; G.cv.setAttribute('aria-hidden','true'); G.cv.style.pointerEvents='none';
      if(cv.parentNode) cv.parentNode.insertBefore(G.cv, cv.nextSibling);
      var _gc=cv.getContext;"""
assert S.count(a)==1
S=S.replace(a,"""    /* ⚑ v130 (Tom, C-002 — RÉCIDIVE) — « LA DOUBLE ZONE » REVENAIT PAR UN CANEVAS MORT. Quand le navigateur retire son contexte graphique à la
       Pelote (le Studio en ouvre d'autres pour ses aperçus : à la deuxième ouverture, l'iPhone reprend le plus ancien) ou quand son côté
       change, `_glInit` fabrique un canevas NEUF — mais l'ancien (`cv.__glc`) restait dans la page, PAR-DESSUS, figé sur sa dernière image :
       la Pelote d'avant, d'une autre teinte, derrière la nouvelle. Mesuré : trois canevas dans `.au-bo` (auBoule, le neuf sans nom, l'ancien
       `#auBouleGL`). L'ancien est RETIRÉ dès qu'un neuf le remplace ; il n'y a jamais qu'UN canevas de la carte. Juge : redteam_zone C. */
    if(cv.__glc!==G.cv){
      var _anc=cv.__glc; if(_anc && _anc.parentNode) _anc.parentNode.removeChild(_anc);
      try{ [].forEach.call((cv.parentNode||document).querySelectorAll('canvas#auBouleGL'), function(x){ if(x!==G.cv && x.parentNode) x.parentNode.removeChild(x); }); }catch(_){}
      cv.__glc=G.cv; G.cv.id='auBouleGL'; G.cv.setAttribute('aria-hidden','true'); G.cv.style.pointerEvents='none';
      if(cv.parentNode) cv.parentNode.insertBefore(G.cv, cv.nextSibling);
    }
    if(!cv.__ctx2d){
      var _gc=cv.getContext;""")
io.open('app.html','w',encoding='utf-8').write(S)
