import io
S=io.open('app.html',encoding='utf-8').read()
old="""      if(!estTrop(fond(r)) && !r.querySelector('[data-trop],[data-tropb]') && id==='detailPoster') return;"""
new="""      if(!estTrop(fond(r)) && !r.querySelector('[data-trop],[data-tropb]')) return;   /* un autre corps (terre, Chiche, Cercle) : rien à lire */"""
assert S.count(old)==1; S=S.replace(old,new)
old="""      try{ new MutationObserver(demande).observe(n, id"""
new="""      /* l'observateur passe DANS la micro-tâche de la mutation, donc avant que l'image soit peinte (une passe remise à l'image suivante
         laissait voir une image à l'ancienne couleur) ; pendant l'animation de « tenir » (v124) elle attend l'image suivante. La passe
         n'écrit que ce qui diffère : son propre réveil ne trouve plus rien à écrire. */
      try{ new MutationObserver(function(){ if(window._tenirAnime){ demande(); return; } try{ passe(); }catch(e){} }).observe(n, id"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
