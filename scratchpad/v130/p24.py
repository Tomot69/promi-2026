import io
S=io.open('app.html',encoding='utf-8').read()
old="""      /* l'observateur passe DANS la micro-tâche de la mutation, donc avant que l'image soit peinte (une passe remise à l'image suivante
         laissait voir une image à l'ancienne couleur) ; pendant l'animation de « tenir » (v124) elle attend l'image suivante. La passe
         n'écrit que ce qui diffère : son propre réveil ne trouve plus rien à écrire. */
      try{ new MutationObserver(function(){ if(window._tenirAnime){ demande(); return; } try{ passe(); }catch(e){} }).observe(n, id"""
new="""      /* ⚠ UNE PASSE PAR IMAGE, DANS `requestAnimationFrame` — donc AVANT que l'image soit peinte, sans rien lire entre deux. Une première
         écriture passait dans la micro-tâche de chaque mutation : chaque passe forçait le recalcul des styles de tout le document
         (mesuré : la première image d'une fiche à 600 ms au lieu de 450, les suivantes deux à trois fois plus lentes). La passe n'écrit
         que ce qui diffère : son propre réveil ne trouve plus rien à écrire. */
      try{ new MutationObserver(demande).observe(n, id"""
assert S.count(old)==1; S=S.replace(old,new)
old="""var g=function(){ var r=f.apply(this,arguments); try{ passe(); }catch(e){} return r; }; g.__trop=true;"""
new="""var g=function(){ var r=f.apply(this,arguments); demande(); return r; }; g.__trop=true;"""
assert S.count(old)==1; S=S.replace(old,new)
old="""  /* derrière les poseurs (on ENVELOPPE, §8) : dans la même tâche que la pose, donc avant que l'image soit peinte */"""
new="""  /* derrière les poseurs (on ENVELOPPE, §8) : la passe est demandée pour l'image qui vient, avant sa peinture */"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
