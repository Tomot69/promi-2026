# v119 §1 + §2 — la Pelote : l'écho retiré ; la lumière du velours appliquée APRÈS le rendu ; le mini halo tramé ; l'ombre et la flaque
import io, re
S=io.open('app.html',encoding='utf-8').read()
def rep(old,new,n=1):
    global S
    assert S.count(old)==n,(S.count(old),old[:80]); S=S.replace(old,new)
def coupe(debut, fin, remplace=''):
    global S
    assert S.count(debut)==1,('début',S.count(debut),debut[:60]); i=S.find(debut); j=S.find(fin,i+len(debut)); assert j>i,('fin',fin[:60])
    S=S[:i]+remplace+S[j:]
# ── l'écho : retiré entièrement
coupe("/* ⚑ v118 (Tom, Q368 → A) — L'ÉCHO DÉCALÉ : un disque PLAT", "</style>\n<script id=\"lot-V118-PELOTE\">", "")
coupe("<script id=\"lot-V118-PELOTE\">", "<style id=\"lot-V116-GENS-css\">", "@@V119@@\n\n")
i=S.find("</style>\n@@V119@@"); assert i>0
coupe("    /* ⚑ v118 (Tom, Q368 → A) : L'ÉCHO DÉCALÉ — une copie PLATE", "    OMBRE=el('div','au-ombre');", "")
coupe("  /* le ton de l'écho : le ton dominant + 2 (la planche v117)", "  function place(){", "")
rep("    if(!CAD) return;\n    echoTeinte();\n", "    if(!CAD) return;\n")
rep("FIN, HALO, OMBRE, ECHO;", "FIN, HALO, OMBRE, FLAQUE;")
# ── l'ombre : en sombre, plus de crème — une flaque de lumière, et l'ombre est ce que la lumière n'atteint pas
coupe("/* ⚑ v117 (Tom) : « en sombre elle est invisible : inverse sa couleur plutôt que de la supprimer » — la crème, au même 0,10 */", "#auraScreen.au2 .au-bo{z-index:1}",
"""/* ⚑ v119 (Tom) : EN SOMBRE, AUCUNE OMBRE CRÈME. Le halo dépose sous la Pelote une flaque de lumière à peine perceptible, et l'ombre
   est la zone que cette lumière n'atteint pas : `#auPeloteFlaque`, peinte et tramée par `window._flaquePelote` (lot-V119-PELOTE). */
#device:not(.light) #auraScreen.au2 .au-ombre{display:none!important}
#auraScreen.au2 .au-flaque{position:absolute!important;left:55px!important;top:437.347px!important;width:280px!important;height:48px!important;margin:0!important;pointer-events:none;z-index:0;display:none}
#device:not(.light) #auraScreen.au2 .au-flaque{display:block}
""")
rep("    OMBRE=el('div','au-ombre'); OMBRE.id='auPeloteOmbre'; CAD.appendChild(OMBRE);",
    "    OMBRE=el('div','au-ombre'); OMBRE.id='auPeloteOmbre'; CAD.appendChild(OMBRE);\n    FLAQUE=el('canvas','au-flaque'); FLAQUE.id='auPeloteFlaque'; CAD.appendChild(FLAQUE);   /* v119 : la flaque de lumière du sombre */")
# ── §2 : la lumière n'est plus calculée par poil
rep("            velours:souffle(), contre:0, duvet:0, grade:0, velours2:1, dresse:0,",
    "            velours:0, contre:0, duvet:0, grade:0, velours2:1, dresse:0,   /* v119 : la lumière du velours s'applique APRÈS le rendu (voir `lumiere`) */")
rep("""  window._peloteSouffle={valeur:souffle, regle:SOUFFLE, t:function(){ return PEL.souffleT; }};""",
"""  window._peloteSouffle={valeur:souffle, regle:SOUFFLE, t:function(){ return PEL.souffleT; }};
  /* ⚑ v119 (Tom, Q371) — LA LUMIÈRE S'APPLIQUE APRÈS LE RENDU, SUR L'IMAGE ENTIÈRE, EN UN SEUL RÉGLAGE. Les poils sont peints au
     repos ; la lumière du velours est une CARTE (ce que le maximum ajoute au repos, lissée, bornée à la silhouette) ajoutée par
     composition (`lighter`) avec une seule opacité — la valeur du souffle. Le halo suit le même réglage.
     La carte se CALIBRE sur le peintre lui-même (une image au maximum, une au repos, hors affichage) : à l'ouverture, puis quand
     la couleur du sol, le thème, le palier ou la taille changent — jamais sous le doigt. Mesuré : le champ de lumière tient à la
     VUE (il bouge de ± 0,03 de gain d'un angle à l'autre), il se réemploie donc quand la Pelote tourne. */
  var LUM={carte:null, halo:null, cle:'', t1:null, t2:null};
  function fondPage(){ if(clair()) return [CREME[0],CREME[1],CREME[2]];
    var mm=/(\\d+)[, ]+(\\d+)[, ]+(\\d+)/.exec(getComputedStyle(SC).backgroundColor); return mm?[+mm[1],+mm[2],+mm[3]]:[5,3,2]; }
  function tonLumiere(){ var R=M.rampeVelours(PEL.solR||solEffectif()), b=R[0], lb=-1;
    for(var i=0;i<R.length;i++){ var l=0.2126*R[i][0]+0.7152*R[i][1]+0.0722*R[i][2]; if(l>lb){ lb=l; b=R[i]; } } return [Math.round(b[0]),Math.round(b[1]),Math.round(b[2])]; }
  function lumCle(){ var s=PEL.solR||solEffectif(), f=fondPage(); return [s[0]|0,s[1]|0,s[2]|0,f[0],f[1],f[2],PEL.palier,CV.width,PEL.sansIles?1:0,window._haloSansTrame?1:0].join(','); }
  function lumCalme(){ return !DG.on && !EMP && !V.vlac && !V.vtan; }
  function lumCalibre(){
    var W=CV.width, g=CV.getContext('2d'), n=Math.max(24, Math.round(W/16));
    function toile(k,w){ var c=LUM[k]; if(!c){ c=LUM[k]=document.createElement('canvas'); } if(c.width!==w){ c.width=w; c.height=w; } return c; }
    var T1=toile('t1',W), g1=T1.getContext('2d'), C=toile('t2',n), gc=C.getContext('2d', {willReadFrequently:true}), o;
    o=opts(); o.velours=SOUFFLE.MAX; M.peint(CV,o);                       /* le maximum… */
    g1.setTransform(1,0,0,1,0,0); g1.globalCompositeOperation='copy'; g1.drawImage(CV,0,0);
    M.peint(CV,opts());                                                  /* …puis le repos, qui reste à l'écran */
    g1.globalCompositeOperation='difference'; g1.drawImage(CV,0,0);      /* ce que la lumière ajoute */
    gc.setTransform(1,0,0,1,0,0); gc.globalCompositeOperation='copy'; gc.imageSmoothingEnabled=true; gc.drawImage(T1,0,0,n,n);
    /* la carte, en petit (la lumière est lisse) : la couleur à pleine valeur, l'opacité au plus juste — pour que l'ajout ne
       change PAS l'opacité de la Pelote à son bord ; et rien hors de la silhouette (le bord est rogné de 4 %) */
    var im=gc.getImageData(0,0,n,n), d=im.data, c0=(n-1)/2, rr=K.R*n*0.96;
    for(var y=0;y<n;y++) for(var x=0;x<n;x++){ var q=(y*n+x)*4, m=Math.max(d[q],d[q+1],d[q+2]), r=Math.hypot(x-c0,y-c0);
      var bord=r<=rr-1 ? 1 : (r>=rr ? 0 : rr-r);
      if(m<1 || !bord){ d[q]=d[q+1]=d[q+2]=d[q+3]=0; continue; }
      d[q]=Math.round(d[q]*255/m); d[q+1]=Math.round(d[q+1]*255/m); d[q+2]=Math.round(d[q+2]*255/m); d[q+3]=Math.round(m*bord); }
    gc.putImageData(im,0,0); LUM.carte=C;
    /* le mini halo et, en sombre, la flaque : le ton le plus clair de la rampe, dosés sur le fond de la page */
    try{ var ton=tonLumiere(), fd=fondPage();
      LUM.halo=window._haloPelote(W, K.R*W, W*(K.bo.d*K.R+5)/K.bo.d, W*(K.bo.d*K.R*2*0.08)/K.bo.d, ton, fd, !!window._haloSansTrame);
      if(FLAQUE) window._flaquePelote(FLAQUE, 280, 48, 52.2145, 8.1225, ton, fd, Math.min(3, window.devicePixelRatio||1), !!window._haloSansTrame); }catch(_){ LUM.halo=null; }
    LUM.cle=lumCle(); PEL.lumCal=(PEL.lumCal||0)+1;
  }
  /* la valeur du souffle, de 0 à 1 */
  function souffleU(){ return Math.max(0, Math.min(1, souffle()/SOUFFLE.MAX)); }
  function lumiere(){
    if(!LUM.carte) return;
    var W=CV.width, g=CV.getContext('2d'), u=souffleU();
    g.save(); g.setTransform(1,0,0,1,0,0); g.imageSmoothingEnabled=true;
    if(u>0){ g.globalCompositeOperation='lighter'; g.globalAlpha=u; g.drawImage(LUM.carte,0,0,W,W); }
    if(LUM.halo){ g.globalCompositeOperation='destination-over'; g.globalAlpha=(0.8+0.4*u)/1.2; g.drawImage(LUM.halo,0,0); }   /* ± 20 %, même cycle, même phase */
    g.restore();
  }
  window._peloteLumiere={etat:function(){ return {cle:LUM.cle, calibrages:PEL.lumCal||0, u:souffleU(), halo:!!LUM.halo, ton:(function(){ try{ return tonLumiere(); }catch(_){ return null; } })()}; },
                         recalibre:function(){ LUM.cle=''; }};""")
rep("""    try{ var _o=opts(); if(window._peloteMod){ try{ window._peloteMod(_o); }catch(_){} }   /* v116 : un crochet pour les PLANCHES de la respiration — sans effet s'il n'est pas posé */
      M.peint(CV, _o); }catch(e){ window._auraErreur=String(e&&e.stack||e); PEL.pret=false; return; }
    var ms=performance.now()-t0;""",
"""    try{ var _o=opts(); if(window._peloteMod){ try{ window._peloteMod(_o); }catch(_){} }   /* v116 : un crochet pour les PLANCHES de la respiration — sans effet s'il n'est pas posé */
      /* v119 : la carte de lumière se (re)calibre ici, au calme — sa propre image est comptée à part, elle ne trompe pas le régulateur */
      var _cal=(LUM.cle!==lumCle()) && lumCalme() && !window._peloteMod;
      if(_cal) lumCalibre(); else M.peint(CV, _o);
      if(!window._peloteMod) lumiere(); }catch(e){ window._auraErreur=String(e&&e.stack||e); PEL.pret=false; return; }
    var ms=performance.now()-t0; if(_cal){ PEL.skip=4; }""")
V119 = r"""<script id="lot-V119-PELOTE">
/* ⚑ v119 (Tom, 2 oct. 2026) — LA PELOTE : UN MINI HALO QUI PROLONGE SA LUMIÈRE, ET UNE OMBRE PORTÉE, DANS LES DEUX MODES.
   Écho, couronne de fibres et halo flou sont REFUSÉS. Le halo n'est pas un flou posé autour : c'est la lumière du velours qui
   déborde à peine de la silhouette.
   · couleur : le ton LE PLUS CLAIR de la rampe de la Pelote (pas une moyenne) ;
   · forme : serré, décroissance EXPONENTIELLE — dosé au calcul (ΔE00 face au fond) : 7 au ras de la silhouette, 2,9 à 0,04 D,
     nul à 0,08 D, rien au-delà ;
   · direction : plein du côté éclairé (la lumière de la Pelote vient d'en haut à gauche), 20 % à l'opposé ; presque nul sur
     le quart inférieur, pour laisser l'ombre se lire ;
   · rendu : TRAMÉ avec le grain de l'app (`_noiseCanvas`) — aucune marche de quantification ;
   · il respire avec la lumière du velours (± 20 %, même cycle, même phase) : c'est l'appelant qui règle son opacité.
   Liste blanche NOMINATIVE de la Pelote : `window._haloPelote` et `window._flaquePelote` ne s'appellent que depuis l'Aura. */
(function(){
  function lin(c){ c/=255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4); }
  function lab(c){ var r=lin(c[0]), g=lin(c[1]), b=lin(c[2]);
    var x=(0.4124564*r+0.3575761*g+0.1804375*b)/0.95047, y=0.2126729*r+0.7151522*g+0.0721750*b, z=(0.0193339*r+0.1191920*g+0.9503041*b)/1.08883;
    function f(t){ return t>0.008856?Math.cbrt(t):7.787*t+16/116; } return [116*f(y)-16, 500*(f(x)-f(y)), 200*(f(y)-f(z))]; }
  function dE00(c1,c2){ var A=lab(c1), B=lab(c2), R=Math.PI/180, L1=A[0],a1=A[1],b1=A[2],L2=B[0],a2=B[1],b2=B[2];
    var C1=Math.hypot(a1,b1), C2=Math.hypot(a2,b2), Cb=(C1+C2)/2, G=0.5*(1-Math.sqrt(Math.pow(Cb,7)/(Math.pow(Cb,7)+Math.pow(25,7))));
    var ap1=(1+G)*a1, ap2=(1+G)*a2, Cp1=Math.hypot(ap1,b1), Cp2=Math.hypot(ap2,b2);
    var h1=(Math.atan2(b1,ap1)/R+360)%360, h2=(Math.atan2(b2,ap2)/R+360)%360;
    var dL=L2-L1, dC=Cp2-Cp1, dh=h2-h1; if(Cp1*Cp2===0) dh=0; else if(dh>180) dh-=360; else if(dh<-180) dh+=360;
    var dH=2*Math.sqrt(Cp1*Cp2)*Math.sin(dh/2*R), Lb=(L1+L2)/2, Cpb=(Cp1+Cp2)/2, hb=h1+h2;
    if(Cp1*Cp2!==0){ if(Math.abs(h1-h2)>180) hb+= (hb<360?360:-360); hb/=2; }
    var T=1-0.17*Math.cos((hb-30)*R)+0.24*Math.cos(2*hb*R)+0.32*Math.cos((3*hb+6)*R)-0.20*Math.cos((4*hb-63)*R);
    var Sl=1+0.015*(Lb-50)*(Lb-50)/Math.sqrt(20+(Lb-50)*(Lb-50)), Sc=1+0.045*Cpb, Sh=1+0.015*Cpb*T;
    var Rt=-2*Math.sqrt(Math.pow(Cpb,7)/(Math.pow(Cpb,7)+Math.pow(25,7)))*Math.sin(60*Math.exp(-Math.pow((hb-275)/25,2))*R);
    return Math.sqrt(Math.pow(dL/Sl,2)+Math.pow(dC/Sc,2)+Math.pow(dH/Sh,2)+Rt*(dC/Sc)*(dH/Sh)); }
  window._dE00=dE00;
  /* l'opacité qui donne l'écart voulu entre le fond et (fond + ton × opacité) — par dichotomie */
  function dose(ton, fond, cible){ var mel=function(a){ return [fond[0]+(ton[0]-fond[0])*a, fond[1]+(ton[1]-fond[1])*a, fond[2]+(ton[2]-fond[2])*a]; };
    if(cible<=0) return 0; if(dE00(mel(1),fond)<=cible) return 1;
    var lo=0, hi=1; for(var i=0;i<22;i++){ var m=(lo+hi)/2; if(dE00(mel(m),fond)<cible) lo=m; else hi=m; } return (lo+hi)/2; }
  var GRAIN=null;
  function grain(){ if(GRAIN) return GRAIN; var n=96, d=null;
    try{ if(typeof _noiseCanvas!=='undefined' && _noiseCanvas && _noiseCanvas.width){ n=_noiseCanvas.width; d=_noiseCanvas.getContext('2d').getImageData(0,0,n,n).data; } }catch(_){ d=null; }
    var G=new Float32Array(n*n), vide=true, i;
    if(d){ for(i=0;i<n*n;i++){ G[i]=d[i*4+3]>0 ? ((d[i*4]+d[i*4+3]*7)%256)/256 : 0; if(G[i]) vide=false; } }
    if(!d || vide){ for(i=0;i<n*n;i++){ var x=(i*2654435761)>>>0; x^=x>>>15; x=(x*2246822519)>>>0; x^=x>>>13; G[i]=(x>>>8)/16777216; } }
    /* on égalise : la trame doit être sans biais (chaque seuil autant de fois) */
    var ord=[]; for(i=0;i<n*n;i++) ord.push(i); ord.sort(function(a,b){ return G[a]-G[b]||a-b; }); for(i=0;i<n*n;i++) G[ord[i]]=(i+0.5)/(n*n);
    return (GRAIN={n:n, g:G}); }
  var CIBLE={ras:7, mi:2.9, fin:0.08, mi_d:0.04, oppose:0.20, bas:0.06, crete:1.2};
  /* W : le côté du canevas ; R : le rayon de la boule ; RS : celui de la silhouette (boule + poil) ; P : 0,08 D, en pixels */
  window._haloPelote=function(W, R, RS, P, ton, fond, sansTrame){
    var cv=document.createElement('canvas'); cv.width=W; cv.height=W;
    var g=cv.getContext('2d'), im=g.createImageData(W,W), d=im.data, c=(W-1)/2, GR=grain(), LX=-0.58, LY=-0.72, nL=Math.hypot(LX,LY);
    /* la décroissance : exponentielle, ramenée à zéro en P ; son pas est réglé pour que le mi-chemin tombe sur sa cible */
    var q=CIBLE.mi/CIBLE.ras, e=q/(1-q), lam=-(P/2)/Math.log(e), e2=Math.exp(-P/lam);
    function f(dd){ return dd<=0 ? 1 : (dd>=P ? 0 : (Math.exp(-dd/lam)-e2)/(1-e2)); }
    /* la table de l'opacité au ras, dosée au calcul ; la crête (+20 %) est dans l'image, l'appelant la module */
    var N=64, T=new Float32Array(N+1); for(var k=0;k<=N;k++) T[k]=dose(ton, fond, CIBLE.ras*CIBLE.crete*k/N);
    function op(v){ v=Math.max(0,Math.min(1,v))*N; var i=Math.floor(v), t=v-i; return i>=N?T[N]:T[i]+(T[i+1]-T[i])*t; }
    for(var y=0;y<W;y++) for(var x=0;x<W;x++){
      var dx=x-c, dy=y-c, r=Math.hypot(dx,dy); if(r<R*0.9 || r>RS+P) continue;
      var co=(dx*LX+dy*LY)/(r*nL), w=CIBLE.oppose+(1-CIBLE.oppose)*(1+co)/2;
      var bas=dy/r, qb=bas<=0.5736 ? 1 : (bas>=0.7071 ? CIBLE.bas : 1-(1-CIBLE.bas)*((bas-0.5736)/(0.7071-0.5736)));   /* le quart inférieur (± 45° du bas), fondu sur 10° */
      var a=op(f(r-RS)*w*qb)*255, n=sansTrame ? 0.5 : GR.g[(y%GR.n)*GR.n+(x%GR.n)], v=Math.floor(a+n);
      if(v<=0) continue; var i4=(y*W+x)*4; d[i4]=ton[0]; d[i4+1]=ton[1]; d[i4+2]=ton[2]; d[i4+3]=v>255?255:v; }
    g.putImageData(im,0,0); return cv;
  };
  /* la flaque du sombre : la lumière du halo, posée au sol autour de l'ombre — l'ombre (demi-axes a × b) est le creux qu'elle n'atteint pas */
  window._flaquePelote=function(cv, lw, lh, a, b, ton, fond, dpr, sansTrame){
    var W=Math.round(lw*dpr), H=Math.round(lh*dpr); if(cv.width!==W) cv.width=W; if(cv.height!==H) cv.height=H;
    var g=cv.getContext('2d'), im=g.createImageData(W,H), d=im.data, GR=grain(), a0=dose(ton, fond, 3.2), cx=(W-1)/2, cy=(H-1)/2;
    for(var y=0;y<H;y++) for(var x=0;x<W;x++){
      var rho=Math.hypot((x-cx)/(a*dpr), (y-cy)/(b*dpr)), t;
      if(rho<0.82) continue;
      if(rho<1.04) t=(rho-0.82)/0.22; else if(rho<2.55) t=Math.exp(-(rho-1.04)/0.62)*(1-Math.pow((rho-1.04)/1.51,3)); else continue;
      var al=a0*t*255, n=sansTrame ? 0.5 : GR.g[(y%GR.n)*GR.n+(x%GR.n)], v=Math.floor(al+n);
      if(v<=0) continue; var i4=(y*W+x)*4; d[i4]=ton[0]; d[i4+1]=ton[1]; d[i4+2]=ton[2]; d[i4+3]=v>255?255:v; }
    g.putImageData(im,0,0);
  };
})();
</script>"""
rep("@@V119@@", V119)
io.open('app.html','w',encoding='utf-8').write(S); print('ok')
for n in ['au-echo','_echoPelote','ECHO','echoTeinte']: print(n, len(re.findall(n,S)))
