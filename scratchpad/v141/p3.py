import io,re
S=io.open('app.html',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:80]); S=S.replace(old,new)

# ══ 1 · lot-E2 (script) est RETIRÉ : remplacé par le guide (lot-V141-GUIDE) ══
i=S.index('<script id="lot-E2">'); j=S.index('</script>',i)+len('</script>')
assert S.count('<script id="lot-E2">')==1
GUIDE=io.open('scratchpad/v141/guide.html',encoding='utf-8').read()
S=S[:i]+GUIDE+S[j:]

# ══ 2 · l'onboarding d'origine : « Plus tard » à chaque étape, la main sur le trait, le guide à la fin ══
rep("""      '<input class="onbv-a onbv-in" id="onbIn" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="done">';
    ov.appendChild(v);""",
"""      '<input class="onbv-a onbv-in" id="onbIn" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="done">'+
      /* ⚑ v141 (Tom, 10 oct. 2026, C-075) — gardé de v140 : « un “Plus tard” à chaque étape, mais sans soulignement, et deux fois plus petit ».
         En haut à droite, à la hauteur du mot-marque : il ne recouvre ni le trait ni le message de fin. */
      '<div class="onbv-a onbv-tard" id="onbTard" data-onb="plus-tard" data-eng="plus-tard" role="button" tabindex="0">Plus tard</div>';
    ov.appendChild(v);
    v.querySelector('#onbTard').addEventListener('click', function(e){ e.stopPropagation(); e.preventDefault(); plusTard(); });""")
rep("""  function focus(){ var i=document.getElementById('onbIn'); if(!i) return;
    i.value = etape==='prenom' ? prenom : parole;""",
"""  /* « Plus tard » : un toucher, et l'on est sur sa Toile — rien n'est redemandé, le guide de fin ne se joue pas (v141) */
  function plusTard(){ sansGuide=true; LS.s('ob_fini','1'); try{ if(!rejeu) LS.s('promi_guide','1'); }catch(_){ }
    try{ if(window.GesteFantome) window.GesteFantome.arrete(); }catch(_){ }
    if(rejeu && !fini){ ov.classList.add('gone'); return; }   /* au rejeu, avant le trait : fermé « par un autre », l'observateur rend toutes les dalles */
    terminer(); }
  function focus(){ var i=document.getElementById('onbIn'); if(!i) return;
    i.value = etape==='prenom' ? prenom : parole;""")
rep("  var O=null, etape=null, rejeu=false, prenom='', parole='', fini=false, prog=0, actif=false, minuteurs=[], voisines=false;",
    "  var O=null, etape=null, rejeu=false, prenom='', parole='', fini=false, prog=0, actif=false, minuteurs=[], voisines=false, sansGuide=false, mainN=0, mainT=0;")
rep("      function suiteFin(e){ if(parti) return; parti=true; if(e){ e.preventDefault(); e.stopPropagation(); }",
    "      function suiteFin(e){ if(parti) return; if(e && e.target && e.target.closest && e.target.closest('#onbTard')) return;   /* v141 : « Plus tard » garde son toucher */ parti=true; if(e){ e.preventDefault(); e.stopPropagation(); }")
rep("""    var fin=document.getElementById('onbFin'); if(fin) fin.style.opacity='0';
    var p=document.createElement('div'); p.className='onbv-compte';""",
"""    var fin=document.getElementById('onbFin'); if(fin) fin.style.opacity='0';
    var _ot=document.getElementById('onbTard'); if(_ot) _ot.style.display='none';   /* v141 : le panneau du compte porte SON « Plus tard » */
    var p=document.createElement('div'); p.className='onbv-compte';""")
rep("""    try{ if(window.Toile&&Toile.redraw) setTimeout(Toile.redraw,60); }catch(_){}
    rejeu=false;
  }""",
"""    try{ if(window.Toile&&Toile.redraw) setTimeout(Toile.redraw,60); }catch(_){}
    /* ⚑ v141 (Tom, C-094) — à la fin d'un parcours COMPLET (la parole est plantée), le guide : le Studio, puis le + (`lot-V141-GUIDE`).
       Une seule fois ; « Revoir la présentation » le rejoue. Pas après « Plus tard ». */
    var _gd=fini && !sansGuide, _rj=rejeu;
    rejeu=false;
    if(_gd){ try{ if(window._guide) window._guide.attend(_rj); }catch(_){ } }
  }""")
rep("    rejeu=!!estRejeu; fini=false; prog=0; actif=false; parole='';",
    "    rejeu=!!estRejeu; fini=false; prog=0; actif=false; parole=''; sansGuide=false; mainN=0; mainT=performance.now();")
# la main fantôme sur le trait de l'onboarding
rep("""  window._onbTerminer=function(){ if(dev.classList.contains('onb-actif')) terminer(); };""",
"""  /* ⚑ v141 (Tom, C-075) — gardé de v140 : « la main fantôme sur les traits ». Sur le trait de l'onboarding, elle paraît après 0,7 s sans toucher
     (clavier fermé), trace du rond de gauche jusqu'au milieu — là où la parole se plante —, et part au premier toucher ; deux fois au plus. */
  ['pointerdown','keydown'].forEach(function(n){ document.addEventListener(n, function(){ mainT=performance.now(); }, true); });
  setInterval(function(){ try{ if(!dev.classList.contains('onb-actif') || fini || actif || etape==='prenom' || etape===null || !parole.trim() || aFocus() || mainN>=2 || !window.GesteFantome) return;
      var cv=document.getElementById('onbTrait'); if(!cv || cv.style.display==='none' || !window._onde) return;
      if(performance.now()-mainT<700 || window.GesteFantome.etat()) return;
      var r=cv.getBoundingClientRect(), kk=r.width/W, y=yOnde(), P=[]; if(!r.width) return;
      for(var x=CX; x<=MID+0.1; x+=(MID-CX)/14) P.push({x:r.left+x*kk, y:r.top+y(x)*kk});
      mainN++; window.GesteFantome.montrer('onb-trait', cv, P, {de:0, ep:8}); }catch(_){ } }, 250);
  window._onbTerminer=function(){ if(dev.classList.contains('onb-actif')) terminer(); };""")
# ══ 3 · « Toi, c'est ? » sans dalle derrière le texte ══
rep("""        var r=e.getBoundingClientRect(); if(!r.width||!r.height) return; rects.push({x:Math.round((r.left-cr.left)*sx), y:Math.round((r.top-cr.top)*sy), w:Math.round(r.width*sx), h:Math.round(r.height*sy)}); }); }""",
"""        var r=e.getBoundingClientRect(); if(!r.width||!r.height) return; var q={x:Math.round((r.left-cr.left)*sx), y:Math.round((r.top-cr.top)*sy), w:Math.round(r.width*sx), h:Math.round(r.height*sy)};
        /* ⚑ v141 (Tom, C-075) : « “Toi, c'est ?” reste, mais sans dalle derrière le texte. » L'écart ne replie que les cellules dont la GRAINE
           tombe près du texte : une cellule voisine, plus large, pouvait encore passer derrière lui. À l'étape du prénom, la zone dégagée de la
           phrase prend toute la largeur et 40 pt de plus en haut et en bas. */
        try{ if(e.id==='onbPh' && window._onbV20 && window._onbV20.etape()==='prenom'){ q.x=0; q.w=cv.clientWidth; q.y-=40; q.h+=80; } }catch(_){ }
        rects.push(q); }); }""")
# le geste « aura-apparait » redevient recensé, non branché (E2bis est remplacé)
rep("geste:'la main désigne l’Aura : un appui sur son entrée', branche:true, quand:function(){ try{ return (window._devoile && window._devoile.auraQuand) ? window._devoile.auraQuand() : null; }catch(_){ return null; } }},   /* E2bis (v140, C-076) */",
    "geste:'la main désigne l’Aura : un appui sur son entrée', branche:false, raison:'E2bis (le dévoilement de la barre) est remplacé par le guide de fin de parcours (v141, C-094) : la barre est complète dès le départ'},")
io.open('app.html','w',encoding='utf-8').write(S)
