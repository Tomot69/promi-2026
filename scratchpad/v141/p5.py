import io
S=io.open('app.html',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:70]); S=S.replace(old,new)
# 1 · les points à tracer : centrés sur le trajet
rep("      for(var x=x0;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x)-(rp-rr),rp,0,6.2832); g.fill(); } }",
    "      for(var x=x0;x<W-rr;x+=esp){ g.beginPath(); g.arc(x,y(x),rp,0,6.2832); g.fill(); } }   /* v141 (C-095) : « les points sont placés exactement sur ce trajet » — leur centre est SUR l'onde (v140 les remontait de 1,5) */")
rep("        for(var x=cx+esp*1.3; x<W-rr; x+=esp){ g.beginPath(); g.arc(x,y(x)-(rp-rr),rp,0,6.2832); g.fill(); }",
    "        for(var x=cx+esp*1.3; x<W-rr; x+=esp){ g.beginPath(); g.arc(x,y(x),rp,0,6.2832); g.fill(); }   /* v141 : centrés sur l'onde */")
# 2 · le geste de tenir part aussi du MILIEU
rep("    if(p.x > B.a.x + 130) return;\n    actif = true; arrive = false; lent = false; lentMs = 0;",
    """    /* ⚑ v141 (Tom, 10 oct. 2026, C-095) : « la main part du milieu, là où s'arrête la moitié plantée, et suit les points jusqu'au bout ».
       Le geste part donc AUSSI du milieu (avant : du tiers gauche seulement — tracer la seconde moitié seule ne tenait pas, mesuré). */
    if(p.x > W/2 + 44) return;
    x0Geste = p.x;
    actif = true; arrive = false; lent = false; lentMs = 0;""")
rep("  var t0 = 0, dernierT = 0, dernierP = null, lentMs = 0;\n\n  function taille(){",
    "  var t0 = 0, dernierT = 0, dernierP = null, lentMs = 0, x0Geste = 0;\n\n  function taille(){")
rep("    if(!arrive && p.x > B.a.x + (B.b.x - B.a.x) * 0.66){",
    "    if(!arrive && p.x > Math.max(B.a.x + (B.b.x - B.a.x) * 0.66, Math.min(x0Geste + W*0.30, W-52))){   /* v141 : parti du milieu, il faut aller presque au bout (30 % de la largeur au moins) */")
# 3 · la main : un peu plus petite, contour deux fois plus épais vers l'intérieur
rep("var INACTIF=600, PAUSE=900, TOURS=3, GRAND=1.5, TRAJET=1600, PRE='geste_vu_';",
    "var INACTIF=600, PAUSE=900, TOURS=3, GRAND=1.3, TRAJET=1600, PRE='geste_vu_';   /* v141 (Tom, C-095) : « un peu plus petite » — 1,5 → 1,3 */")
rep("  var A=null;   /* le geste en cours : {id, pts, couche, main, t0, tours, raf} */",
    """  var A=null;   /* le geste en cours : {id, pts, couche, main, t0, tours, raf} */
  /* ⚑ v141 (Tom, 10 oct. 2026, C-095) : « son contour deux fois plus épais, vers l'intérieur ». Le bord extérieur ne bouge pas : au contour d'avant
     (centré, largeur w) s'ajoute un second trait de largeur 3 w, découpé à l'intérieur de la main — 0,5 w dehors, 1,5 w dedans : 2 w. */
  function mainNoeud(s, enc, fond, w){ var d=svg('defs',{}), cp=svg('clipPath',{id:'gfMainInt'}); cp.appendChild(svg('path',{d:MAIN})); d.appendChild(cp); s.appendChild(d);
    var q=svg('g',{'data-main-g':'1'}); q.appendChild(svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':w, 'stroke-linejoin':'round', 'data-main':'1'}));
    q.appendChild(svg('path',{d:MAIN, fill:'none', stroke:enc, 'stroke-width':w*3, 'stroke-linejoin':'round', 'clip-path':'url(#gfMainInt)', 'data-main-int':'1'})); s.appendChild(q); return q; }""")
rep("      var m0=svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':2.6, 'stroke-linejoin':'round', 'data-main':'1'}); s.appendChild(m0); place(m0, P[0].x, P[0].y, true);",
    "      var m0=mainNoeud(s, enc, fond, 2.6/1.5); place(m0, P[0].x, P[0].y, true);")
rep("    var m=svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':2.6/GRAND*1.25, 'stroke-linejoin':'round', 'data-main':'1'}); s.appendChild(m); place(m, P[0].x, P[0].y, false);",
    "    var m=mainNoeud(s, enc, fond, 2.6/1.5*1.25); place(m, P[0].x, P[0].y, false);")
# 4 · sur une fiche, la main part du milieu et suit les points
rep("    var P=onde(cv, +t[0], +t[1], 30, 360); if(!P) return null; var de=0, kk=cv.getBoundingClientRect().width/390, x195=cv.getBoundingClientRect().left+195*kk; if(t[3]==='moitie'){ while(de<P.length-2 && P[de].x<x195) de++; }\n    return {cible:$('tenirZone'), chemin:P, trace:{de:de, col:/^#[0-9A-Fa-f]{6}$/.test(t[2])?t[2]:null, ep:8}}; }",
    "    /* ⚑ v141 (Tom, C-095) : la main PART DU MILIEU, là où s'arrête la moitié plantée, et suit les points jusqu'au bout (avant : de 30 à 360, le tracé\n       ne commençant qu'au milieu). Une parole dont le trait n'est pas en « moitié » garde le trajet entier. */\n    var moit=(t[3]==='moitie'), P=onde(cv, +t[0], +t[1], moit?195:30, 360); if(!P) return null;\n    return {cible:$('tenirZone'), chemin:P, trace:{de:0, col:/^#[0-9A-Fa-f]{6}$/.test(t[2])?t[2]:null, ep:8}}; }")
io.open('app.html','w',encoding='utf-8').write(S)
