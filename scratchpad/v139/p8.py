import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("  var INACTIF=600, PAUSE=900, TOURS=2, PRE='geste_vu_';",
"""  /* ⚑ v139 (Tom, 9 oct. 2026, C-074, Q429) — LA MAIN, PLUS PARLANTE. « On ne comprend pas ce qu'elle montre. » ① elle TRACE : la seconde moitié
     du trait se dessine sous son doigt — les pointillés deviennent pleins à mesure — puis s'efface quand elle part ; ② plus grande (× 1,5) ;
     ③ plus lente (1,6 s pour le trajet d'un trait) ; ④ trois passages au plus. Toujours opaque, sans fondu (A2).
     ⚠ En E1 la main s'arrêtait au milieu du trait (30 → 195) : au vrai doigt ce tracé-là ne tient PAS la parole (mesuré : il faut aller
     jusqu'à la moitié de droite). Elle va maintenant jusqu'au bout. */
  var INACTIF=600, PAUSE=900, TOURS=3, GRAND=1.5, TRAJET=1600, PRE='geste_vu_';""")
rep("  function place(m, x, y, pose){ m.setAttribute('transform','translate('+(x-17).toFixed(1)+' '+(y-2+(pose?0:-7)).toFixed(1)+')'); }",
    "  function place(m, x, y, pose){ m.setAttribute('transform','translate('+(x-17*GRAND).toFixed(1)+' '+(y-2*GRAND+(pose?0:-9)).toFixed(1)+') scale('+GRAND+')'); }")
rep("  function montrer(id, cible, chemin){","  function montrer(id, cible, chemin, trace){")
rep("""    var m=svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':2.6, 'stroke-linejoin':'round', 'data-main':'1'}); s.appendChild(m); place(m, P[0].x, P[0].y, false);
    var AVANT=260, D=tot>6 ? Math.max(700, Math.min(1500, tot*5)) : 0, APRES=260, UN=AVANT+appui+D+APRES;""",
"""    /* le tracé : des pointillés posés d'avance (quand l'écran ne les porte pas déjà), et le plein qui grandit sous le doigt */
    var TR=null; if(trace && tot>6){ var de=Math.max(0, Math.min(P.length-2, trace.de|0)), col=trace.col||enc, ep=trace.ep||6;
      if(trace.pointille) s.appendChild(svg('path',{d:'M'+P.slice(de).map(function(p){ return p.x.toFixed(1)+' '+p.y.toFixed(1); }).join(' L'), fill:'none', stroke:col, 'stroke-width':ep*0.75, 'stroke-linecap':'round', 'stroke-dasharray':'0.1 '+(ep*2.2).toFixed(1), 'data-pointille':'1'}));
      TR={de:de, el:svg('path',{d:'', fill:'none', stroke:col, 'stroke-width':ep, 'stroke-linecap':'round', 'stroke-linejoin':'round', 'data-trace':'1', visibility:'hidden'})}; s.appendChild(TR.el); }
    function traceJusqua(d){ if(!TR) return; if(d<=L[TR.de]){ TR.el.setAttribute('visibility','hidden'); return; } var q=pos(d/tot), dd='M'+P[TR.de].x.toFixed(1)+' '+P[TR.de].y.toFixed(1);
      for(var i=TR.de+1;i<P.length && L[i]<d;i++) dd+=' L'+P[i].x.toFixed(1)+' '+P[i].y.toFixed(1); dd+=' L'+q.x.toFixed(1)+' '+q.y.toFixed(1); TR.el.setAttribute('d',dd); TR.el.setAttribute('visibility','visible'); }
    var m=svg('path',{d:MAIN, fill:fond, stroke:enc, 'stroke-width':2.6/GRAND*1.25, 'stroke-linejoin':'round', 'data-main':'1'}); s.appendChild(m); place(m, P[0].x, P[0].y, false);
    var AVANT=320, D=tot>6 ? (TR ? TRAJET : Math.max(900, Math.min(TRAJET, tot*8))) : 0, APRES=420, UN=AVANT+appui+D+APRES;""")
rep("""        m.setAttribute('visibility','hidden'); A.tm=setTimeout(""","""        m.setAttribute('visibility','hidden'); if(TR) TR.el.setAttribute('visibility','hidden');   /* le tracé s'efface quand elle part */ A.tm=setTimeout(""")
rep("""      else if(t<AVANT+appui+D){ var u=(t-AVANT-appui)/D; u=u*u*(3-2*u); var q=pos(u); place(m, q.x, q.y, true); }
      else { var e=P[P.length-1]; place(m, e.x, e.y, t<AVANT+appui+D+APRES*0.5); }""",
"""      else if(t<AVANT+appui+D){ var u=(t-AVANT-appui)/D; u=u*u*(3-2*u); var q=pos(u); place(m, q.x, q.y, true); traceJusqua(u*tot); }
      else { var e=P[P.length-1]; place(m, e.x, e.y, t<AVANT+appui+D+APRES*0.5); traceJusqua(tot); }""")
rep("""    var P=onde(cv, +t[0], +t[1], 30, t[3]==='moitie' ? 195 : 360); return P ? {cible:$('tenirZone'), chemin:P} : null; }""",
"""    var P=onde(cv, +t[0], +t[1], 30, 360); if(!P) return null; var de=0, kk=cv.getBoundingClientRect().width/390, x195=cv.getBoundingClientRect().left+195*kk; if(t[3]==='moitie'){ while(de<P.length-2 && P[de].x<x195) de++; }
    return {cible:$('tenirZone'), chemin:P, trace:{de:de, col:/^#[0-9A-Fa-f]{6}$/.test(t[2])?t[2]:null, ep:6}}; }""")
rep("""      var P=onde(cv, e.base, e.amp, 30, e.nat==='nuee' ? 360 : 195); return P ? {cible:cs, chemin:P} : null; }},""",
"""      var P=onde(cv, e.base, e.amp, 30, e.nat==='nuee' ? 360 : 195); return P ? {cible:cs, chemin:P, trace:{de:0, pointille:true, ep:6}} : null; }},""")
rep("""P.push({x:r.left+r.width*(0.28+0.44*u), y:r.top+r.height*(0.42+0.07*Math.sin(u*Math.PI*2))}); } return {cible:s, chemin:P}; }},""",
    """P.push({x:r.left+r.width*(0.28+0.44*u), y:r.top+r.height*(0.42+0.07*Math.sin(u*Math.PI*2))}); } return {cible:s, chemin:P, trace:{de:0, ep:4.5}}; }},""")
rep("cand=null; montrer(trouve.g.id, trouve.q.cible, trouve.q.chemin); } }","cand=null; montrer(trouve.g.id, trouve.q.cible, trouve.q.chemin, trouve.q.trace); } }")
rep("geste:'tracer le trait, du rond de gauche vers le milieu', branche:true","geste:'tracer le trait, du rond de gauche jusqu’au bout : la moitié en pointillés devient pleine', branche:true")
rep("geste:'tracer sa moitié du trait', branche:true","geste:'tracer le trait jusqu’au bout : sa moitié en pointillés devient pleine', branche:true")
rep("regle:{INACTIF:INACTIF, PAUSE:PAUSE, TOURS:TOURS}","regle:{INACTIF:INACTIF, PAUSE:PAUSE, TOURS:TOURS, GRAND:GRAND, TRAJET:TRAJET}")
io.open(f,'w',encoding='utf-8').write(S)
