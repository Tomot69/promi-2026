import io
S=io.open('app.html',encoding='utf-8').read()
old="""    if(!(h===cv || h===dp || (dp.contains(h) && !h.closest('#dpMain')))) return false;"""
new="""    /* `#dpMain` (la colonne de la fiche) couvre la bande : c'est LUI qu'on touche, pas le canevas. Lui-même oui ; ce qu'il porte
       (un texte, un disque, la carte du mot) non. */
    if(!(h===cv || h===dp || h.id==='dpMain')) return false;"""
assert S.count(old)==1; S=S.replace(old,new)
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('redteam_entier.py',encoding='utf-8').read()
old="""const s=dp.className+'|'+(dp.getAttribute('style')||'')+'|'+L.join('\\n');"""
new="""/* `gsN` : le grain de l'écran, que l'app retire au sort à chaque toucher — ce n'est pas l'état de la fiche */
  const s=dp.className.replace(/\\bgs\\d+\\b/g,'')+'|'+(dp.getAttribute('style')||'')+'|'+L.join('\\n');"""
assert J.count(old)==1; J=J.replace(old,new)
io.open('redteam_entier.py','w',encoding='utf-8').write(J)
