import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(a,b,n=1):
    global S
    assert S.count(a)==n,(S.count(a),a[:70]); S=S.replace(a,b)
rep("            EMP_FIN:0.0004, DOUBLE:350,",
"""            EMP_FIN:0.0004, DOUBLE:350,
            /* ⚑ v139 (Tom, 9 oct. 2026, C-083) — LE TOUCHER, REFAIT. « Plus on appuie longtemps, plus ça s'enfonce : vite au début, puis de
               plus en plus lentement, jusqu'à une butée, comme une matière qui durcit ; jamais de saut ; au relâcher, la fourrure revient
               lentement à sa forme. » La PROFONDEUR (part q de la butée) suit q(t) = 1 − 1/(1 + t/ENF_TAU)² : sa vitesse ne fait que
               décroître dès la première image (2/ENF_TAU par seconde au départ, soit 5,6 % de la butée par image à 60 i/s — l'ancienne
               loi en prenait 32 % à la première image), et elle tend vers la butée sans l'atteindre. Au relâcher q décroît en
               RETOUR_TAU (0,15 s avant). CEDE, CEDE_TAU, RESISTE_TAU et REPOUSSE_TAU ne servent plus qu'à l'histoire.
               LA FORME DU CONTACT : le demi-axe de l'empreinte vaut DOIGT_K × le rayon du contact lu sur le toucher, borné à
               [A_MIN, A_MAX] (en rayons de boule) ; avant, il était borné entre l'index et le pouce (0,26–0,40) et un vrai contact
               (≈ 0,10–0,17) tombait toujours sur la borne basse : deux doigts différents donnaient la même empreinte. */
            ENF_TAU:0.60, RETOUR_TAU:0.60, DOIGT_K:2.2, A_MIN:0.16, A_MAX:0.46,""")
rep("""    if(EMP.tr===0){ var tt=(now-EMP.t0)/1000;
      EMP.p=Math.min(1, 1-G.CEDE*Math.exp(-tt/G.CEDE_TAU)-(1-G.CEDE)*Math.exp(-tt/G.RESISTE_TAU)); return; }""",
"""    if(EMP.tr===0){ var tt=Math.max(0,(now-EMP.t0)/1000), _u=1+tt/G.ENF_TAU;
      EMP.q=1-1/(_u*_u); EMP.p=Math.pow(EMP.q,1.5);   /* v139 : d = dmax × p^(2/3) = dmax × q — c'est la profondeur qui suit la loi */ return; }""")
rep("""    var p=EMP.pRel*Math.exp(-(now-EMP.tr)/1000/G.REPOUSSE_TAU);""",
"""    var _q=(EMP.qRel||0)*Math.exp(-Math.max(0,now-EMP.tr)/1000/G.RETOUR_TAU); EMP.q=_q;
    var p=Math.pow(_q,1.5);   /* v139 : le retour lent, sur la profondeur */""")
rep("      if(EMP && EMP.tr===0){ EMP.pRel=EMP.p; EMP.tr=now; }","      if(EMP && EMP.tr===0){ EMP.pRel=EMP.p; EMP.qRel=EMP.q||0; EMP.tr=performance.now(); }")
# la forme du contact
rep("""  function doigt(e){
    var lo=PULPE.index[0]/K.Rpt, hi=PULPE.pouce[0]/K.Rpt, a=hi, elp=PULPE.pouce[1];
    if(e && e.pointerType==='touch' && e.width>4 && e.height>4){
      var s=echelle(), rx=Math.max(e.width,e.height)/2/s, ry=Math.min(e.width,e.height)/2/s;
      a=rx/K.Rpt; elp=Math.max(0.5, Math.min(1, ry/rx));
    }
    a=Math.max(lo, Math.min(hi, a));
    return {a:a, el:elp, dmax:G.PROF*a, ax:[0.62,-0.72,0], capteur:!!(e && e.pointerType==='touch' && e.width>4 && e.height>4)};
  }""",
"""  /* ⚑ v139 (C-083) — LA FORME RÉELLE DU CONTACT. Safari donne, sur l'événement de toucher, `radiusX`, `radiusY` et `rotationAngle` ;
     l'événement de pointeur donne `width` et `height`. On prend le toucher quand il est là (TCH, tenu à jour par `touchstart` /
     `touchmove`), sinon le pointeur, sinon le pouce. Le grand axe du contact oriente l'empreinte tant que le doigt ne glisse pas. */
  var TCH={rx:0, ry:0, rot:0, t:0};
  function lisTouche(ev){ var t=ev.touches&&ev.touches[0]; if(!t) return;
    var rx=+(t.radiusX||t.webkitRadiusX||0), ry=+(t.radiusY||t.webkitRadiusY||0); if(!(rx>1 && ry>1)){ TCH.t=0; return; }
    TCH.rx=rx; TCH.ry=ry; TCH.rot=+(t.rotationAngle||t.webkitRotationAngle||0)||0; TCH.t=performance.now(); }
  function doigt(e){
    var a=PULPE.pouce[0]/K.Rpt, elp=PULPE.pouce[1], ax=[0.62,-0.72,0], cap=false, s=echelle(), rx=0, ry=0, rot=null;
    if(TCH.t && performance.now()-TCH.t<400){ rx=TCH.rx/s; ry=TCH.ry/s; rot=TCH.rot*Math.PI/180; if(ry>rx){ var _t=rx; rx=ry; ry=_t; rot+=Math.PI/2; } cap=true; }
    else if(e && e.pointerType==='touch' && e.width>4 && e.height>4){ rx=Math.max(e.width,e.height)/2/s; ry=Math.min(e.width,e.height)/2/s; if(e.height>e.width*1.08) rot=Math.PI/2; else if(e.width>e.height*1.08) rot=0; cap=true; }
    if(cap){ a=Math.max(G.A_MIN, Math.min(G.A_MAX, G.DOIGT_K*rx/K.Rpt)); elp=Math.max(0.5, Math.min(1, ry/rx));
      if(rot!=null && elp<0.93) ax=[Math.cos(rot), Math.sin(rot), 0]; }
    return {a:a, el:elp, dmax:G.PROF*a, ax:ax, capteur:cap, rx:rx, ry:ry};
  }""")
rep("""    if(f.capteur){ EMP.a+=(f.a-EMP.a)*k; EMP.el0+=(f.el-EMP.el0)*k; EMP.dmax=G.PROF*EMP.a; }""",
"""    if(f.capteur){ EMP.a+=(f.a-EMP.a)*k; EMP.el0+=(f.el-EMP.el0)*k; EMP.dmax=G.PROF*EMP.a; EMP.rx=f.rx; EMP.ry=f.ry; }""")
rep("""    PRISE.addEventListener('pointerdown', function(e){""",
"""    PRISE.addEventListener('touchstart', lisTouche, {passive:true}); PRISE.addEventListener('touchmove', lisTouche, {passive:true});
    PRISE.addEventListener('pointerdown', function(e){""")
# reprise au même endroit : on repart de la profondeur en cours, jamais de zéro
rep("""        EMP={c:v, ax:f.ax, a:f.a, el:f.el, el0:f.el, dmax:f.dmax, p:0, t0:performance.now(), tr:0, pRel:0, comble:0, lx:e.clientX, ly:e.clientY, gl:0};""",
"""        var _q0=0; if(EMP && EMP.q>0 && EMP.comble<1e-6){ var _c0=EMP.c, _dd=Math.hypot(v[0]-_c0[0], v[1]-_c0[1], v[2]-_c0[2]); if(_dd<EMP.a*0.6) _q0=Math.min(0.98, EMP.q); }   /* v139 : on rappuie au même endroit — on repart de la profondeur en cours, sans saut */
        EMP={c:v, ax:f.ax, a:f.a, el:f.el, el0:f.el, dmax:f.dmax, p:Math.pow(_q0,1.5), q:_q0, t0:performance.now()-1000*G.ENF_TAU*(1/Math.sqrt(1-_q0)-1), tr:0, pRel:0, qRel:0, comble:0, lx:e.clientX, ly:e.clientY, gl:0, rx:f.rx, ry:f.ry};""")
rep("""      prise:DG.on, emp:EMP?{p:EMP.p, relache:EMP.tr>0, c:EMP.c, a:EMP.a}:null,""",
"""      prise:DG.on, emp:EMP?{p:EMP.p, q:EMP.q||0, relache:EMP.tr>0, c:EMP.c, a:EMP.a, el:EMP.el, ax:EMP.ax, dmax:EMP.dmax, rx:EMP.rx||0, ry:EMP.ry||0}:null,""")
io.open(f,'w',encoding='utf-8').write(S)
