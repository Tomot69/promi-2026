import io
S=io.open('app.html',encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:80]); S=S.replace(a,b)
# ═══ 1 · LE BORD : celui du peintre d'avant v114 — les pointes telles que le peintre les pose, sans resserrement ni recoloration ═══
rep("""    '  float t=clamp(uR0-r+0.5,0.0,1.0);',""",
"""    /* ⚑ v141 (Tom, 10 oct. 2026, C-083 — RÉCIDIVE) — LE BORD EST CELUI DU PEINTRE D'AVANT v114, EXACTEMENT. « Compare l'algorithme de bord de
       l'ancien peintre avec celui de la carte graphique, et reproduis l'ancien exactement : n'en invente pas un. »
       CE QUE LA COMPARAISON MONTRE : les poils sont posés de la même façon par les deux peintres (un tampon par poil, le plus opaque gagne :
       ΔE 0,3 entre eux). L'ancien bord, c'est ce versement LAISSÉ TEL QUEL : les pointes qui dépassent gardent l'opacité et la couleur que
       leur tampon leur donne — une frange douce. Tout ce qui a été ajouté depuis à la composition est retiré : le repli de couleur (v137),
       la limite franche (v139), le resserrement de l'opacité et la recoloration des pointes (v140). Reste, de v120 (« la Pelote est
       pleine »), le corps opaque sous les poils, qui finit comme la peau d'alors : plein jusqu'à 0,972 R, fondu jusqu'à 1,012 R.
       Le corps est d'une autre teinte que le poil depuis v123 : sur les derniers 12 % du rayon il rejoint la couleur du poil qui le couvre
       (la peau d'avant v114 ÉTAIT de la couleur du poil) — sans quoi il ferait un anneau entre les pointes. */
    '  float t=1.0-smoothstep(uR0, uR1, r);',""")
rep("""    '  float mc=step(0.5,uA), tb=t*mc; float a2=mix(f.a, smoothstep(0.30,0.62,f.a), mc); float al=a2+tb*(1.0-a2);',
    '  vec3 c=f.rgb*f.a+uCorps*mc*(1.0-f.a); float ac=mix(f.a,1.0,mc);',
    '  o=vec4(c*(al/max(ac,0.0001)), al); }'].join('\\n');""",
"""    '  float mc=step(0.5,uA), tb=t*mc; float al=f.a+tb*(1.0-f.a);',
    '  vec3 corps=mix(uCorps, f.rgb, step(0.004,f.a)*smoothstep(0.88*uR0/0.972, uR0, r));',
    '  o=vec4(f.rgb*f.a+corps*tb*(1.0-f.a), al); }'].join('\\n');""")
rep("gl.uniform1f(u2.uR0,E.R*(window._peloteBord||1.0)); gl.uniform1f(u2.uR1,E.R*1.012);",
    "gl.uniform1f(u2.uR0,E.R*(window._peloteBord||0.972)); gl.uniform1f(u2.uR1,E.R*1.012);   /* v141 : 0,972 → 1,012 R, la fin de la peau d'avant v114 */")
# le peintre de secours : le masque du plein revient à 0,972 R, la couronne de v140 est retirée
rep("_r0=R*1.0 /* v138 : plein jusqu'au rayon de la boule, comme la carte graphique (0,972 avant) */, _r1=R*1.012;",
    "_r0=R*0.972 /* v141 : la fin de la peau d'avant v114 (0,972 → 1,012 R), comme la carte graphique */, _r1=R*1.012;")
i=S.index("    try{\n      if(!cv.__cr || cv.__crW!==W){ var _L=[], _ra=R+0.5, _rb=R*1.09;"); j=S.index("    }catch(_){}\n",i)+len("    }catch(_){}\n")
S=S[:i]+"    /* ⚑ v141 (Tom, C-083 — récidive) : RIEN. Le bord est celui du peintre d'avant v114 — les pointes telles qu'il les pose. La couronne de v140\n       (opacité resserrée, pointes recolorées) est retirée, comme sur la carte graphique. */\n"+S[j:]
# ═══ 2 · LES POILS DU BORD SE COUCHENT DANS LE SENS OÙ LA PELOTE TOURNE ═══
rep("'uniform float uCl,uSl,uCt,uSt,uR,uFOC,uC,uW,uVel,uDoux,uPousse,uNCOL,uNT,uILE,uETAGE,uM,uCell,uGrid,uORI,uNVAR;','uniform vec2 uAtlas;',",
    "'uniform float uCl,uSl,uCt,uSt,uR,uFOC,uC,uW,uVel,uDoux,uPousse,uNCOL,uNT,uILE,uETAGE,uM,uCell,uGrid,uORI,uNVAR;','uniform vec2 uAtlas;','uniform vec2 uTour;',")
rep("""    '  float fx2=fX*aE1.y-fY*aE1.z; fY=fX*aE1.z+fY*aE1.y; fX=fx2;',""",
"""    '  float fx2=fX*aE1.y-fY*aE1.z; fY=fX*aE1.z+fY*aE1.y; fX=fx2;',
    /* ⚑ v141 (Tom, C-083) : « les poils du bord suivent la rotation : ils se couchent dans le sens où la Pelote tourne ». `uTour` est le sens
       (à l'écran) où la face visible se déplace, dosé par la vitesse ; il s'ajoute à la direction du poil, du milieu du rayon (rien) au bord (tout). */
    '  { float wb=smoothstep(0.50,0.96,length(vec2(X2,Y2))); fX+=uTour.x*wb; fY+=uTour.y*wb; }',""")
rep("G.u1={}; ['uCl','uSl','uCt','uSt','uR','uFOC','uC','uW','uVel','uDoux','uPousse',", "G.u1={}; ['uTour','uCl','uSl','uCt','uSt','uR','uFOC','uC','uW','uVel','uDoux','uPousse',")
rep("gl.uniform1f(u.uVel,o.velours||0); gl.uniform1f(u.uDoux,o.doux?1:0); gl.uniform1f(u.uPousse,E.POUSSE);",
    "gl.uniform1f(u.uVel,o.velours||0); gl.uniform1f(u.uDoux,o.doux?1:0); gl.uniform1f(u.uPousse,E.POUSSE); gl.uniform2f(u.uTour,(o.tour&&o.tour[0])||0,(o.tour&&o.tour[1])||0);")
rep("    var _fx2=fX*_jc-fY*_js; fY=fX*_js+fY*_jc; fX=_fx2;\n",
    "    var _fx2=fX*_jc-fY*_js; fY=fX*_js+fY*_jc; fX=_fx2;\n    /* v141 (C-083) : les poils du bord se couchent dans le sens où la Pelote tourne — la même loi que la carte graphique (`uTour`) */\n    if(o.tour && (o.tour[0] || o.tour[1])){ var _rb=Math.sqrt(X2*X2+Y2*Y2), _wb=(_rb-0.50)/0.46; _wb=_wb<0?0:(_wb>1?1:_wb); _wb=_wb*_wb*(3-2*_wb); fX+=o.tour[0]*_wb; fY+=o.tour[1]*_wb; }\n")
rep("emp:(EMP && EMP.p>=G.EMP_FIN) ? empPour(EMP) : null, peauVers:peauVers(), corps:corps()};",
    "emp:(EMP && EMP.p>=G.EMP_FIN) ? empPour(EMP) : null, peauVers:peauVers(), corps:corps(), tour:tour()};")
rep("  function relisse(){ var av=TRACES;",
"""  /* ⚑ v141 (Tom, C-083) — le sens où la face visible se déplace, à l'écran, dosé par la vitesse : la rotation de repos (un tour en 100 s) couche à
     peine les poils du bord (0,18), un lancer les couche franchement (jusqu'à 0,9). Vue figée : rien. */
  function tour(){ if(PEL.fige) return null; var wl=(DG.on?0:G.AUTO)+V.vlac, wt=V.vtan, w=Math.sqrt(wl*wl+wt*wt); if(w<1e-4) return null;
    var s=Math.min(1, w/1.2), A=0.18+0.72*s; return [A*wl/w, -A*wt/w]; }
  function relisse(){ var av=TRACES;""")
# ═══ 3 · LA TRACE : LA SURFACE RÉELLEMENT TOUCHÉE, FORMÉE SOUS LE DOIGT ═══
rep("""      if(DG.chem){ var _cl=DG.chem[DG.chem.length-1], _cd=Math.hypot(e.clientX-_cl.x, e.clientY-_cl.y)/s;
        if(_cd>=8 && DG.chem.length<400) DG.chem.push({x:e.clientX, y:e.clientY, a:(EMP&&EMP.tr===0)?EMP.a:_cl.a}); }
      if(v){""",
"""      /* ⚑ v141 (Tom, 10 oct. 2026, C-083 — RÉCIDIVE) — LA TRACE EST LA SURFACE RÉELLEMENT TOUCHÉE, ET ELLE SE FORME SOUS LE DOIGT. « L'union des
         zones de contact lues à chaque image le long du chemin, les poils couchés dans le sens du mouvement. Elle se forme sous le doigt, en
         direct, pas au lâcher. » POURQUOI C'EST REVENU : v140 relevait le chemin à l'ÉCRAN et posait la trace AU LÂCHER, rapportée à la boule
         telle qu'elle était alors — une forme dessinée après coup, pas ce que le doigt avait touché (et un appui posait une étoile).
         Ici, tous les 10 pt de geste : la zone de contact DU MOMENT (le point de l'objet sous le doigt, la largeur du contact lue à cet
         instant) reçoit un arc de sa longueur, couché dans le sens où le doigt va, et il est inscrit AUSSITÔT (retouche locale). Quand la
         boule suit la main, c'est la même zone de l'objet qui est touchée : son arc est remplacé, pas empilé. */
      if(v && EMP && EMP.tr===0 && DG.chem){ var _cl=DG.chem[0], _cd=Math.hypot(e.clientX-_cl.x, e.clientY-_cl.y)/s;
        if(_cd>=10){ var _ux=(e.clientX-_cl.x)/(_cd*s), _uy=(e.clientY-_cl.y)/(_cd*s), _dm=Math.max(9, EMP.a*K.Rpt*0.9)*s;
          var _p1=surBoule(e.clientX-_ux*_dm, e.clientY-_uy*_dm)||v, _p2=surBoule(e.clientX+_ux*_dm, e.clientY+_uy*_dm);
          if(_p2){ var _o1=versObjet(_p1), _o2=versObjet(_p2); if(angle(_o1,_o2)>=0.02){ var _g=arc(_o1,_o2), _a0=PULPE.pouce[0]/K.Rpt; _g.w=Math.max(0.12, Math.min(0.42, G.W*(EMP.a/_a0))); _g.vif=1;
              var _av=TRACES, _der=TRACES[TRACES.length-1], _nv=TRACES;
              if(_der && _der.vif===DG.geste && angle(_der.a,_g.a)<EMP.a*0.5) _nv=TRACES.slice(0,-1);
              _g.vif=DG.geste; TRACES=_nv.concat([_g]).slice(-G.TRACES); TVER++; retouche(_av, TRACES); DG.vifs=(DG.vifs||0)+1; } }
          DG.chem[0]={x:e.clientX, y:e.clientY}; } }
      if(v){""")
rep("      DG.chem=[{x:e.clientX, y:e.clientY, a:(EMP&&v)?EMP.a:0}];   /* v140 (C-083) : le chemin réel du doigt, à l'écran, avec la largeur de son contact */",
    "      DG.chem=[{x:e.clientX, y:e.clientY}]; DG.geste=(DG.geste||0)+1; DG.vifs=0;   /* v141 : le dernier point où la trace a été posée, et le numéro du geste */")
# l'étoile d'un appui : retirée
i=S.index("          try{ var _s=echelle(), _v=surBoule(DG.x, DG.y);\n            /* inscrite AU LÂCHER"); j=S.index("}catch(_){}\n",i)+len("}catch(_){}\n")
assert "_L8" in S[i:j]
S=S[:i]+"          /* ⚑ v141 (Tom, C-083 — récidive) : « Retire l'étoile à huit branches et tout dessin géométrique. Un appui immobile creuse la forme du\n             contact, sans motif. » Un appui ne pose plus RIEN : l'empreinte (le creux, à la forme du contact) fait seule le travail, puis revient. */\n"+S[j:]
# la trace posée au lâcher : retirée
i=S.index("      try{ var _C=DG.chem||[], _n=_C.length;\n        if(_n>=2){ var _pas="); j=S.index("} } }catch(_){}\n",i)+len("} } }catch(_){}\n")
S=S[:i]+"      /* v141 : plus rien n'est posé au lâcher — la trace s'est formée sous le doigt (voir `pointermove`) */\n"+S[j:]
io.open('app.html','w',encoding='utf-8').write(S)
