import io
S=io.open('app.html',encoding='utf-8').read()
def rep(o,n,c=1):
    global S
    assert S.count(o)==c,(S.count(o),o[:70]); S=S.replace(o,n)
rep("""    if(st && (st.classList.contains('stp-verrou')||st.classList.contains('world-locked')) && !st.classList.contains('st-entre')) ['#stpTons','#stpVue','#stpDots','#stpLab'].forEach(function(s){ var e=st.querySelector(s); if(e&&vu(e)) L.push(e); });""",
"""    /* ⚑ v140 (Tom, 10 oct. 2026, C-092) — le panneau des palettes ouvert sur un monde de Ma Parole ! : c'est LUI le mur (il recouvre les
       quatre zones, qui restaient pourtant les murs : la phrase se posait sur des pastilles nettes). Il est flouté comme elles. */
    if(st && (st.classList.contains('stp-verrou')||st.classList.contains('world-locked')) && !st.classList.contains('st-entre')){
      if(st.classList.contains('stp-pals')){ var _pp=st.querySelector('#stpPals'); if(_pp&&vu(_pp)) L.push(_pp); }
      else ['#stpTons','#stpVue','#stpDots','#stpLab'].forEach(function(s){ var e=st.querySelector(s); if(e&&vu(e)) L.push(e); }); }""")
rep("""    var r=mur?mur.getBoundingClientRect():D; var x0=Math.max(r.left,D.left), x1=Math.min(r.right,D.right), y0=Math.max(r.top,D.top), y1=Math.min(r.bottom,D.bottom);""",
"""    var r=mur?mur.getBoundingClientRect():D;
    /* ⚑ v140 (Tom, 10 oct. 2026, C-092) — AU STUDIO, LA PHRASE PARAÎT SUR LE FLOU TOUCHÉ. La cause : le panneau flouté du Studio est fait de
       quatre murs en bandes (les tons 54 pt, les libellés 19, les disques 44, les barrettes 4). La phrase se centrait dans LA BANDE touchée ;
       une bande de moins de 40 pt n'étant pas « assez grande », elle retombait sur l'appareil entier — au milieu de l'écran, sur le nom du
       monde, net. Au Studio le mur est donc LE PANNEAU : la réunion de ses bandes floutées. */
    if(mur && mur.closest && mur.closest('#studioScreen')){ var _LS=murs().filter(function(e){ return e.closest && e.closest('#studioScreen'); });
      if(_LS.length){ var _u={left:1e9, top:1e9, right:-1e9, bottom:-1e9}; _LS.forEach(function(e){ var q=e.getBoundingClientRect(); if(q.width<2) return; _u.left=Math.min(_u.left,q.left); _u.top=Math.min(_u.top,q.top); _u.right=Math.max(_u.right,q.right); _u.bottom=Math.max(_u.bottom,q.bottom); });
        if(_u.right>_u.left) r=_u; } }
    var x0=Math.max(r.left,D.left), x1=Math.min(r.right,D.right), y0=Math.max(r.top,D.top), y1=Math.min(r.bottom,D.bottom);""")
rep("""#studioScreen.st-plat.stp-verrou #stpDots{filter:blur(2.4px)!important;pointer-events:none!important}""",
"""#studioScreen.st-plat.stp-verrou #stpDots{filter:blur(2.4px)!important;pointer-events:none!important}
/* v140 (C-092) : le panneau des palettes, ouvert sur un monde de Ma Parole !, est un mur comme les quatre zones qu'il recouvre */
#studioScreen.st-plat.stp-verrou.stp-pals #stpPals{filter:blur(2.4px)!important;pointer-events:none!important}""")
io.open('app.html','w',encoding='utf-8').write(S)
