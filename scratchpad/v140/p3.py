import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:70]); S=S.replace(o,n)
# 1 · le gros pinceau
rep("    TAILLES: [2, 6, 14],             /* fin, moyen, gros — la pointe jamais sous 1 pt */",
    "    TAILLES: [2, 6, 22],             /* fin, moyen, gros — la pointe jamais sous 1 pt ; v140 (Tom, C-086) : « le gros pinceau : 22 pt au lieu de 14 » */\n    POINT_PLUS: 3,         /* v140 : les points du choix de taille « grossissent un peu » — le diamètre du trait + 3 pt */\n    CIBLE: 44,             /* v140 : « une cible tactile de 44 pt chacun » */")
# 2 · les trois points : une cible de 44 pt chacun, des points un peu plus gros
rep("""      p.style.left=(x0+(o==='gomme'?pas:0))+'px'; p.style.top=(yD-44)+'px';
      var _xt=8; (o==='gomme'?P.TAILLES_GOMME:P.TAILLES).forEach(function(dd,i){ var e=document.createElement('button'); e.type='button'; e.className=(M.taille[o]===i?'on':''); var bw=Math.max(26, dd+6); e.style.left=_xt+'px'; e.style.width=bw+'px'; e.style.height=bw+'px'; e.style.top=((44-bw)/2)+'px'; e.style.borderRadius=(bw/2)+'px'; _xt+=bw+8; p.style.width=_xt+'px';
        e.innerHTML='<i style="width:'+dd+'px;height:'+dd+'px"></i>';   /* v139 : le point à l'échelle du trait (1 pt pour 1 pt) */""",
"""      /* ⚑ v140 (Tom, 10 oct. 2026, C-086) — « Les trois points de taille : plus grands, avec une cible tactile de 44 pt chacun ; les points
         eux-mêmes grossissent un peu. » Chaque bouton fait 44 × 44 ; son point fait le diamètre du trait + 3 pt (au plus 40). */
      var _hc=P.CIBLE+8; p.style.left=Math.max(P.MARGE_COTE-8, Math.min(W-P.MARGE_COTE+8-(8+3*P.CIBLE+2*4+8), x0+(o==='gomme'?pas:0)))+'px'; p.style.top=(yD-_hc)+'px'; p.style.height=_hc+'px'; p.style.borderRadius=(_hc/2)+'px';
      var _xt=8; (o==='gomme'?P.TAILLES_GOMME:P.TAILLES).forEach(function(dd0,i){ var dd=Math.min(40, dd0+P.POINT_PLUS); var e=document.createElement('button'); e.type='button'; e.className=(M.taille[o]===i?'on':''); var bw=P.CIBLE; e.style.left=_xt+'px'; e.style.width=bw+'px'; e.style.height=bw+'px'; e.style.top=((_hc-bw)/2)+'px'; e.style.borderRadius=(bw/2)+'px'; _xt+=bw+(i<2?4:8); p.style.width=_xt+'px';
        e.innerHTML='<i style="width:'+dd+'px;height:'+dd+'px"></i>';""")
# 3 · remplacer : POSER un dessin retire la photo de la bande
rep("""    if(poser){ if(d.traits.length){ d.poses=JSON.parse(JSON.stringify(d.traits)); d.pose=true; d.masque=false; ecrit(c, d); } else { ecrit(c, null); } }""",
"""    /* ⚑ v140 (Tom, 10 oct. 2026, C-086, C-085) — REMPLACER. « On doit pouvoir passer d'un dessin à une photo et inversement, par le menu du
       bouton. […] La photo remplace entièrement ce qui était dans la bande, sans aucun reste. » La bande montre UNE chose (v128) : poser un
       dessin retire la photo de la bande ; importer une photo retire le dessin posé (`_photoImportee`, plus bas). */
    if(poser){ if(d.traits.length){ d.poses=JSON.parse(JSON.stringify(d.traits)); d.pose=true; d.masque=false; ecrit(c, d); retirePhoto(c); } else { ecrit(c, null); } }""")
rep("""  function retire(c){ c=c||cibleFiche()||ciblePlus(); if(!c) return; ecrit(c, null); MEMO={}; bandes();""",
"""  function porteur(c){ return !c ? null : (c.type==='promi' ? c.p : (c.type==='brouillon' ? (window._phrase=window._phrase||{}) : null)); }
  function retirePhoto(c){ var q=porteur(c); if(q && q.photo){ q.photo=null; delete q.photoCadre; try{ if(c.type==='promi' && typeof saveState==='function') saveState(); }catch(_){ } } }
  /* une photo vient d'être importée par le bouton (fiche ou page +) : elle REMPLACE le dessin de la bande — il n'en reste rien.
     ⚠ LA CAUSE DE LA « BANDE PARASITE » (v139) : le dessin posé et la photo vivaient ensemble ; la couche du dessin recouvrait la photo, mais
     elle s'arrête 7 pt au-dessus de l'axe du trait (`BANDE_RETRAIT`) — dans cette lisière, et partout où le fond du dessin laissait la
     boîte de la photo dépasser, on voyait la photo sous le dessin. */
  window._photoImportee=function(q){ try{ var c=cibleFiche(); if(!(c && c.type==='promi' && c.p===q)){ c=ciblePlus(); if(!(c && porteur(c)===q)) c=null; }
      if(c && lit(c)){ ecrit(c, null); MEMO={}; var h=c.hote, x=h && h.querySelector(':scope > canvas.dz-bande'), o=h && h.querySelector(':scope > button.dz-oeil'); if(x) x.remove(); if(o) o.remove(); bandes(); try{ if(window._entier && window._entier.annonce) setTimeout(window._entier.annonce, 60); }catch(_){ } } }catch(_){ } };
  function retire(c){ c=c||cibleFiche()||ciblePlus(); if(!c) return; ecrit(c, null); MEMO={}; bandes();""")
rep("""        rd.onload=function(){ try{ var q=b._p; if(q){ q.photo=rd.result; }
          _cache[rd.result]=null; rejoue && rejoue(); }catch(_){} };""",
"""        rd.onload=function(){ try{ var q=b._p; if(q){ q.photo=rd.result; delete q.photoCadre; try{ if(window._photoImportee) window._photoImportee(q); }catch(_){} }   /* v140 : la photo remplace le dessin de la bande */
          _cache[rd.result]=null; (b._rejoue||rejoue) && (b._rejoue||rejoue)(); }catch(_){} };""")
io.open('app.html','w',encoding='utf-8').write(S)
