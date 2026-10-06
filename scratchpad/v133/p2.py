import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b):
    global S
    assert S.count(a)==1,(S.count(a),a[:70]); S=S.replace(a,b)
rep("""  Object.keys(pals).forEach(function(kk){var cols=pals[kk].cols,pos=[[0,0],[1,0],[0,1],[1,1]],q='';""",
    """  /* v133 (Tom, C-057) : « Primesautier passe en premier dans la liste des palettes (clin d'œil au créateur). L'ordre des autres est inchangé. » */
  var _ordreP=Object.keys(pals); if(_ordreP.indexOf('primesautier')>0){ _ordreP.splice(_ordreP.indexOf('primesautier'),1); _ordreP.unshift('primesautier'); }
  _ordreP.forEach(function(kk){var cols=pals[kk].cols,pos=[[0,0],[1,0],[0,1],[1,1]],q='';""")
rep("""    var pnom=document.getElementById('st3pn');
    if(pnom && pnom.parentNode!==pl) pl.appendChild(pnom);
    if(pnom && spec && spec.parentNode===pl) pl.insertBefore(pnom, spec);
    if(spec && spec.parentNode!==pl) pl.appendChild(spec);""",
    """    /* ⚑ v133 (Tom, C-057) — LE MENU DES PALETTES CASSÉ À LA DEUXIÈME OUVERTURE DU STUDIO. Cause : `buildStudio()` rebâtit aussi le NOM
       (`#st3pn`), mais on ne retirait que l'ancienne rangée et l'ancienne jauge, jamais l'ancien nom. `getElementById('st3pn')` rendait
       donc le VIEUX nom, déjà dans le panneau : il y restait, la rangée neuve était rangée APRÈS lui — le nom au-dessus de la grille, la
       grille 25 pt plus bas, et deux `#st3pn` dans le document. On prend le nom NEUF (celui de `#studioBody`), on retire l'ancien, et
       l'ordre est posé explicitement : la grille, le nom, la jauge. */
    var pnomNeuf=$('#studioBody #st3pn');
    if(pnomNeuf){ [].slice.call(pl.querySelectorAll('.st3-pn')).forEach(function(v){ if(v!==pnomNeuf){ try{ v.parentNode.removeChild(v); }catch(_){ } } }); }
    var pnom=pnomNeuf||pl.querySelector('.st3-pn')||document.getElementById('st3pn');
    var specIci=(spec && spec.parentNode!==pl) ? spec : pl.querySelector('.st3-spec');
    var palsIci=pl.querySelector('.st3-pals');
    if(palsIci) pl.appendChild(palsIci);
    if(pnom) pl.appendChild(pnom);
    if(specIci) pl.appendChild(specIci);""")
io.open('app.html','w',encoding='utf-8').write(S)
