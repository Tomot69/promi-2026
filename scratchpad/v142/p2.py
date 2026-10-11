import io
f='app.html'; S=io.open(f,encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n, ('motif absent ou multiple', S.count(old), old[:80]); S=S.replace(old,new)
# 1 · les constantes : plus de multiplicateur, plus de bornes pouce / index
rep("""ENF_TAU:0.60, RETOUR_TAU:0.60, COMBLE_K:0.08, DOIGT_K:2.2, A_MIN:0.16, A_MAX:0.46,
            TRACES:48, W:0.27,""",
"""ENF_TAU:0.60, RETOUR_TAU:0.60, COMBLE_K:0.08, DOIGT_K:1, A_MIN:0.035, A_MAX:0.60,   /* ⚑ v142 (Tom, C-083) : « la largeur de contact lue, sans multiplicateur (le 2,2 disparaît) » — l'empreinte et la trace ont la taille du contact ; les bornes ne servent plus qu'à écarter une lecture absurde (4 pt, 70 pt) */
            TRACES:260, W:0.27,""")
# 2 · la bande continue, à chaque mouvement
i0=S.index("      if(v && EMP && EMP.tr===0 && DG.chem){ DG.dernEv={x:e.clientX, y:e.clientY}; var _cl=DG.chem[0]")
i1=S.index("      if(v){\n        if(EMP && EMP.tr===0){ EMP.c=v; empSuit(e, v); }", i0)
neuf = """      /* ⚑ v142 (Tom, 11 oct. 2026, C-083 — RÉCIDIVE : « ça apparaît en grand alors qu'on a à peine touché, et inversement ; on ne croit pas que
         la trace est notre empreinte ») — LA TRACE EST UNE BANDE CONTINUE QUI SUIT LE DOIGT, MOUVEMENT PAR MOUVEMENT, À LA LARGEUR DU CONTACT LU.
         POURQUOI C'EST REVENU : v141 posait UN arc par « zone », au plus un toutes les 360 ms, long comme l'empreinte et large de
         0,12 à 0,42 rad selon un rapport au pouce (× 2,2) — ni sa longueur ni sa largeur n'étaient celles du geste : un effleurement
         posait un arc entier, un long trajet rapide n'en posait qu'un ou deux. Le juge de v141 vérifiait qu'une trace PARAISSAIT et
         suivait le sens du geste, pas sa taille.
         Ici, à CHAQUE mouvement : le point de la boule sous le doigt (dans le repère de l'objet) est relié au précédent par un segment,
         large du contact lu à cet instant (son rayon EN TRAVERS du geste, `radiusX` / `radiusY`, sans multiplicateur ni borne), inscrit
         aussitôt. Le chemin RÉEL du doigt sur la fourrure : court si le geste est court, fin si le doigt effleure. */
      if(v && EMP && EMP.tr===0 && DG.chem){ var _oc=versObjet(v);
        if(!DG.oPrec){ DG.oPrec=_oc; DG.ePrec={x:e.clientX, y:e.clientY}; }
        else { var _an=angle(DG.oPrec,_oc);
          if(_an>=0.02){ var _g=arc(DG.oPrec,_oc); _g.w=contactTravers(e.clientX-DG.ePrec.x, e.clientY-DG.ePrec.y); _g.vif=DG.geste; _g.m=nrm([DG.oPrec[0]+_oc[0], DG.oPrec[1]+_oc[1], DG.oPrec[2]+_oc[2]]);
            var _av=TRACES; TRACES=TRACES.concat([_g]).slice(-G.TRACES); TVER++; retouche(_av, TRACES); DG.vifs=(DG.vifs||0)+1; DG.oPrec=_oc; DG.ePrec={x:e.clientX, y:e.clientY}; } } }
"""
S=S[:i0]+neuf+S[i1:]
# 3 · la largeur du contact en travers du geste ; la forme du contact d'un appui immobile
rep("""  function empSuit(e, v){
    if(!EMP || EMP.tr!==0 || !v) return;""",
"""  /* v142 — le rayon du contact EN TRAVERS d'un geste (dx, dy à l'écran), en radians sur la boule : la demi-largeur de l'ellipse de contact
     (rx ≥ ry, grand axe à `rot`) vue perpendiculairement au geste. Sans capteur (souris) : la pulpe du pouce. Jamais moins d'un point. */
  function contactRayons(){ var rx=EMP&&EMP.rx, ry=EMP&&EMP.ry; if(!(rx>0&&ry>0)){ rx=PULPE.pouce[0]/2.2; ry=rx*PULPE.pouce[1]; }   /* sans capteur : un pouce (21 × 15 pt — la pulpe de la planche, sans son ancien multiplicateur) */ return [rx, ry, (EMP&&EMP.rot)||0]; }
  function contactTravers(dx, dy){ var c=contactRayons(), m=Math.sqrt(dx*dx+dy*dy)||1, nx=-dy/m, ny=dx/m, ca=Math.cos(c[2]), sa=Math.sin(c[2]);
    var u=nx*ca+ny*sa, w=-nx*sa+ny*ca; return Math.max(1, Math.sqrt(c[0]*c[0]*u*u+c[1]*c[1]*w*w))/K.Rpt; }
  /* v142 — « Un appui immobile laisse la forme du contact, à sa taille réelle » : un segment le long du grand axe du contact, long de la
     différence de ses deux rayons, large de son petit rayon — l'ellipse du contact, sans motif ; un contact rond : un disque. */
  function poseContact(){ try{ if(!EMP || !EMP.c) return false; var c=contactRayons(), s=echelle(), cxE=null;
    var bb=PRISE.getBoundingClientRect(), o0=versObjet(EMP.c), demi=Math.max(0.5,(c[0]-c[1]))/K.Rpt;
    var ax=EMP.ax||[1,0,0], t=nrm([ax[0], ax[1], 0]); if(!(c[0]>c[1]*1.05)) t=[1,0,0];
    /* deux points de la boule de part et d'autre du centre du contact, le long du grand axe (à l'écran) */
    var p1=nrm([EMP.c[0]-t[0]*demi, EMP.c[1]-t[1]*demi, EMP.c[2]]), p2=nrm([EMP.c[0]+t[0]*demi, EMP.c[1]+t[1]*demi, EMP.c[2]]);
    var g=arc(versObjet(p1), versObjet(p2)); g.w=Math.max(1,c[1])/K.Rpt; g.vif=DG.geste; g.m=o0; g.appui=1;
    var av=TRACES; TRACES=TRACES.concat([g]).slice(-G.TRACES); TVER++; retouche(av, TRACES); return true; }catch(_){ return false; } }
  function empSuit(e, v){
    if(!EMP || EMP.tr!==0 || !v) return;""")
rep("""    if(f.capteur){ EMP.a+=(f.a-EMP.a)*k; EMP.el0+=(f.el-EMP.el0)*k; EMP.dmax=G.PROF*EMP.a; EMP.rx=f.rx; EMP.ry=f.ry; }""",
"""    if(f.capteur){ EMP.a+=(f.a-EMP.a)*k; EMP.el0+=(f.el-EMP.el0)*k; EMP.dmax=G.PROF*EMP.a; EMP.rx=f.rx; EMP.ry=f.ry; EMP.rot=f.rot||0; }""")
rep("""    return {a:a, el:elp, dmax:G.PROF*a, ax:ax, capteur:cap, rx:rx, ry:ry};""","""    mesContact();
    return {a:a, el:elp, dmax:G.PROF*a, ax:ax, capteur:cap, rx:rx, ry:ry, rot:rot||0};""")
rep("""  var TCH={rx:0, ry:0, rot:0, t:0};""","""  var TCH={rx:0, ry:0, rot:0, t:0};
  /* v142 — avec `?mesure=1`, la ligne « contact lu » EN DIRECT, à chaque lecture (elle n'était réécrite qu'avec le relevé, une fois par seconde) */
  function mesContact(){ if(!MES) return; try{ var n=document.getElementById('auMesContact'); if(!n){ n=document.createElement('div'); n.id='auMesContact';
        n.style.cssText='position:absolute;left:12px;top:104px;z-index:60;margin:0;padding:4px 8px;max-width:366px;pointer-events:none;font:500 12px/1.3 Atkinson,system-ui;background:#201908;color:#F7F0DE;-webkit-text-fill-color:#F7F0DE;border-radius:8px';
        (document.getElementById('device')||document.body).appendChild(n); }
      n.textContent='contact lu : '+(window._peloteContact||'—'); n.style.display=document.getElementById('auraScreen').classList.contains('show')?'block':'none'; }catch(_){ } }""")
# 4 · le lâcher d'un appui immobile, et la remise à zéro du chemin
rep("""        else { DG.tap=now;
          /* ⚑ v21 — et LÀ OÙ ON LA TOUCHE, LE POIL SE COUCHE ET RESTE COUCHÉ (un arc au diamètre du doigt) */""",
"""        else { DG.tap=now; if(!DG.vifs) poseContact();   /* v142 : la forme du contact, à sa taille réelle */
          /* ⚑ v21 — et LÀ OÙ ON LA TOUCHE, LE POIL SE COUCHE ET RESTE COUCHÉ (un arc au diamètre du doigt) */""")
rep("""DG.chem=[{x:e.clientX, y:e.clientY}]; DG.geste=(DG.geste||0)+1; DG.vifs=0; DG.tPose=0; DG.dernEv=null;""",
"""DG.chem=[{x:e.clientX, y:e.clientY}]; DG.geste=(DG.geste||0)+1; DG.vifs=0; DG.tPose=0; DG.dernEv=null; DG.oPrec=null; DG.ePrec=null;""")
rep("""    var a=PULPE.pouce[0]/K.Rpt, elp=PULPE.pouce[1], ax=[0.62,-0.72,0], cap=false, s=echelle(), rx=0, ry=0, rot=null;""",
"""    var a=PULPE.pouce[0]/2.2/K.Rpt, elp=PULPE.pouce[1], ax=[0.62,-0.72,0], cap=false, s=echelle(), rx=0, ry=0, rot=null;   /* v142 : sans capteur, un pouce à sa taille (21 pt), plus 2,2 fois */""")
io.open(f,'w',encoding='utf-8').write(S); print('ok')
