import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:70]); S=S.replace(o,n)
# 1 · la pose : le chemin du doigt commence
rep("""        DG.tr0=versObjet(v); DG.trN=DG.tr0;
      } else { DG.tr0=null; DG.trN=null; }
      e.preventDefault();""",
"""        DG.tr0=versObjet(v); DG.trN=DG.tr0;
      } else { DG.tr0=null; DG.trN=null; }
      DG.chem=[{x:e.clientX, y:e.clientY, a:(EMP&&v)?EMP.a:0}];   /* v140 (C-083) : le chemin réel du doigt, à l'écran, avec la largeur de son contact */
      e.preventDefault();""")
# 2 · le mouvement : on ne pose plus un arc tous les 20 px au point touché (c'était toujours le même point de l'objet : un tampon)
rep("""      if(v){ DG.pas=(DG.pas||0);
        var _dx=e.clientX-(DG.px==null?e.clientX:DG.px), _dy=e.clientY-(DG.py==null?e.clientY:DG.py);
        DG.pas+=Math.sqrt(_dx*_dx+_dy*_dy)/s;
        if(DG.pas>=20){ var _m=Math.sqrt(_dx*_dx+_dy*_dy)||1, _R=24*s;
          var _v2=surBoule(e.clientX+_dx/_m*_R, e.clientY+_dy/_m*_R);
          if(_v2){ var _g=arc(versObjet(v), versObjet(_v2)); _g.L=Math.max(_g.L, G.W); DG.arcs.push(_g); }
          DG.pas=0; }
        DG.px=e.clientX; DG.py=e.clientY; }
      if(v){
        if(EMP && EMP.tr===0){ EMP.c=v; empSuit(e, v); }
        var o=versObjet(v);
        if(!DG.tr0) DG.tr0=o;
        else if(angle(DG.tr0, o)>=0.6){ DG.arcs.push(arc(DG.tr0, o)); DG.tr0=o; }
        DG.trN=o;
      }""",
"""      /* ⚑ v140 (Tom, 10 oct. 2026, C-083) — L'EMPREINTE SUIT LE VRAI GESTE. « Quand le doigt glisse, les poils se couchent dans le sens et
         sur le trajet réels du doigt, avec la largeur de son contact. Plus de tampon identique à chaque fois. » Avant (v21) : un arc de
         24 pt posé tous les 20 pt AU POINT TOUCHÉ — or la boule suit la main, ce point est toujours le même point de l'objet : dix arcs
         empilés au même endroit, la même marque quel que soit le geste. On RELÈVE maintenant le chemin du doigt à l'écran (un point tous
         les 8 pt, avec la largeur du contact lue à cet instant) ; la trace est posée au lâcher, le long de ce chemin (voir `lacher`). */
      if(DG.chem){ var _cl=DG.chem[DG.chem.length-1], _cd=Math.hypot(e.clientX-_cl.x, e.clientY-_cl.y)/s;
        if(_cd>=8 && DG.chem.length<400) DG.chem.push({x:e.clientX, y:e.clientY, a:(EMP&&EMP.tr===0)?EMP.a:_cl.a}); }
      if(v){
        if(EMP && EMP.tr===0){ EMP.c=v; empSuit(e, v); }
        var o=versObjet(v);
        if(!DG.tr0) DG.tr0=o;
        DG.trN=o;
      }""")
# 3 · le toucher sans glisser : une étoile autour du point
rep("""          try{ var _s=echelle(), _v=surBoule(DG.x, DG.y), _w=surBoule(DG.x, DG.y+24*_s);
            /* inscrite AU LÂCHER (pas au repos) : au repos, le lustre paraissait d'un coup au moment où le creux
               finissait de se refermer — un saut. Un toucher n'a pas d'élan à saccader, et la retouche est locale. */
            if(_v && _w){ var _a=arc(versObjet(_v), versObjet(_w)); _a.L=Math.max(_a.L, G.W);
              var _av=TRACES; TRACES=TRACES.concat([_a]).slice(-G.TRACES); TVER++; retouche(_av, TRACES); } }catch(_){}""",
"""          /* ⚑ v140 (C-083) — « Un appui sans glisser couche les poils en étoile autour du point. » Huit branches qui partent du point
             touché vers l'extérieur ; leur longueur suit la taille du contact ET la profondeur atteinte (un appui bref marque peu, un
             appui long marque large) : jamais deux fois le même tampon. Avant : un seul arc de 24 pt, toujours vers le bas. */
          try{ var _s=echelle(), _v=surBoule(DG.x, DG.y);
            /* inscrite AU LÂCHER (pas au repos) : au repos, le lustre paraissait d'un coup au moment où le creux
               finissait de se refermer — un saut. Un toucher n'a pas d'élan à saccader, et la retouche est locale. */
            if(_v){ var _ae=(EMP&&EMP.a)||(PULPE.pouce[0]/K.Rpt), _qe=(EMP&&(EMP.qRel||EMP.q))||0, _re=_ae*(0.55+0.75*_qe)*K.Rpt*_s, _L8=[], _o0=versObjet(_v);
              for(var _b=0;_b<8;_b++){ var _an=_b*Math.PI/4+0.39, _p1=surBoule(DG.x+Math.cos(_an)*_re*0.22, DG.y+Math.sin(_an)*_re*0.22), _p2=surBoule(DG.x+Math.cos(_an)*_re, DG.y+Math.sin(_an)*_re);
                if(_p1 && _p2){ var _a=arc(versObjet(_p1), versObjet(_p2)); _a.w=Math.max(0.07, _ae*(0.30+0.25*_qe)); _a.et=1; _L8.push(_a); } }
              if(_L8.length){ var _av=TRACES; TRACES=TRACES.concat(_L8).slice(-G.TRACES); TVER++; retouche(_av, TRACES); } } }catch(_){}""")
# 4 · le glissement : la trace le long du chemin, à l'orientation du lâcher
rep("""      if(DG.tr0 && DG.trN && angle(DG.tr0, DG.trN)>=0.08) DG.arcs.push(arc(DG.tr0, DG.trN));""",
"""      /* ⚑ v140 (C-083) — la trace est le chemin du doigt TEL QU'IL L'A TRACÉ À L'ÉCRAN, rapporté à la boule telle qu'elle est au lâcher :
         des arcs bout à bout (seize au plus), chacun dans le sens du geste, large comme le contact lu à cet endroit (0,27 rad pour un
         pouce, moins pour un index). Deux trajets différents laissent deux traces différentes. */
      try{ var _C=DG.chem||[], _n=_C.length;
        if(_n>=2){ var _pas=Math.max(1, Math.ceil((_n-1)/16)), _a0=PULPE.pouce[0]/K.Rpt, _pv=null, _po=null;
          for(var _i=0;_i<_n;_i+=_pas){ var _c=_C[Math.min(_n-1,_i)], _vv=surBoule(_c.x,_c.y), _oo=_vv?versObjet(_vv):null;
            if(_oo && _po && angle(_po,_oo)>=0.03){ var _g=arc(_po,_oo); _g.w=Math.max(0.12, Math.min(0.42, G.W*((_c.a||_a0)/_a0))); DG.arcs.push(_g); }
            if(_oo){ _po=_oo; } if(_i<_n-1 && _i+_pas>_n-1) _i=_n-1-_pas; } } }catch(_){}
      DG.chem=null;""")
# 5 · pour le juge : la géométrie des traces, vue à l'écran
rep("""    relisse:relisse, K:K, G:G, PALIERS:PALIERS, MOTS:MOTS,""",
"""    relisse:relisse, K:K, G:G, PALIERS:PALIERS, MOTS:MOTS,
    /* v140 : pour les juges — les traces (posées et en attente), chacune avec sa largeur et ses deux bouts dans l'objet */
    tracesGeo:function(){ return TRACES.concat(ATTENTE).map(function(t){ var c=Math.cos(t.L), s=Math.sin(t.L); return {a:t.a, b:[t.a[0]*c+t.d[0]*s, t.a[1]*c+t.d[1]*s, t.a[2]*c+t.d[2]*s], L:t.L, w:t.w, et:t.et?1:0}; }); },""")
io.open('app.html','w',encoding='utf-8').write(S)
