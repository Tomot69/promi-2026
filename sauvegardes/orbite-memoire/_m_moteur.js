/* ════════════════════════════════════════════════════════════════════════════
   LE MOTEUR — celui qui est ACQUIS : des tampons pre-rendus, verses dans un
   tampon de pixels, un putImageData. Aucun drawImage par grain (hors budget
   d'un facteur trois, mesure au lot du 5 septembre). Tout ce qui suit tient
   donc a 60 images par seconde.
   ════════════════════════════════════════════════════════════════════════════ */
var D=2;                          /* pixels d'appareil par pixel CSS */
var TAU=6.283185307179586;

/* ── LES TAMPONS ──────────────────────────────────────────────────────────── */
function fabTampon(dat,src,x1,y1,w,h,ox,oy,mul,rgb){
  var offs=[], vals=[];
  for(var y=0;y<h;y++)for(var x=0;x<w;x++){
    var al=(dat[((y1+y)*src+(x1+x))*4+3]*mul)|0;
    if(al>3){ offs.push([y-oy,x-ox]); vals.push(al); }
  }
  return {rel:offs, al:vals, rgb:rgb};
}
function lieTampons(A,W){
  for(var i=0;i<A.length;i++){
    var t=A[i]; if(t.off && t.W===W) continue;
    var n=t.rel.length, off=new Int32Array(n), val=new Uint32Array(n);
    for(var j=0;j<n;j++){
      off[j]=t.rel[j][0]*W+t.rel[j][1];
      val[j]=(((t.al[j]&255)<<24)|((t.rgb[2]&255)<<16)|((t.rgb[1]&255)<<8)|(t.rgb[0]&255))>>>0;
    }
    t.off=off; t.val=val; t.n=n; t.W=W;
  }
  return A;
}
/* un atlas : 1 teinte x T tailles x O orientations x NIV niveaux */
function atlasForme(dessin, rgb, tailles, ORI, NIV, a0, a1){
  var S=52, cv=document.createElement('canvas'); cv.width=S; cv.height=S;
  var g=cv.getContext('2d'), A=[];
  for(var s=0;s<tailles.length;s++){
    for(var r=0;r<ORI;r++){
      g.clearRect(0,0,S,S);
      g.save(); g.translate(S/2,S/2); g.rotate(r*Math.PI/ORI);
      g.fillStyle='#fff'; g.strokeStyle='#fff'; g.lineCap='round';
      dessin(g, tailles[s]); g.restore();
      var d=g.getImageData(0,0,S,S).data;
      var x1=S,y1=S,x2=-1,y2=-1;
      for(var y=0;y<S;y++)for(var x=0;x<S;x++) if(d[(y*S+x)*4+3]>3){
        if(x<x1)x1=x; if(x>x2)x2=x; if(y<y1)y1=y; if(y>y2)y2=y; }
      if(x2<0){x1=y1=S/2;x2=y2=S/2;}
      var w=x2-x1+1, h=y2-y1+1, ox=S/2-x1, oy=S/2-y1;
      for(var n=0;n<NIV;n++){
        /* la rampe d'opacite : q^1,45 et non q^2. Au carre, les niveaux du
           milieu tombaient a un tiers et toute la matiere sortait sourde. */
        var q=(n+0.5)/NIV, mul=a0+(a1-a0)*Math.pow(q,1.45);
        A.push(fabTampon(d,S,x1,y1,w,h,ox,oy,mul,rgb));
      }
    }
  }
  return A;
}
/* LE GRAIN RETENU : le fil. Un brin long, legerement renfle au milieu. */
function GRAIN_FIL(g,e){
  g.lineWidth=Math.max(0.85,e*0.19);
  g.beginPath(); g.moveTo(-e*1.15,0); g.lineTo(e*1.15,0); g.stroke();
}
/* le meme, avec le fil de trame en travers : la vraie toile tissee */
function GRAIN_TRAME(g,e){
  g.lineWidth=Math.max(0.85,e*0.19);
  g.beginPath(); g.moveTo(-e*1.10,0); g.lineTo(e*1.10,0); g.stroke();
  g.lineWidth=Math.max(0.7,e*0.15);
  g.beginPath(); g.moveTo(0,-e*0.36); g.lineTo(0,e*0.36); g.stroke();
}

/* ── LE RELIEF — DE SURFACE, JAMAIS DE FORME ──────────────────────────────
   ⚠ LE DEFAUT DES CINQ DERNIERES SERIES ETAIT ICI, ET IL SE LIT DANS LES
   NOMBRES. P_PLIS valait 0,060 x sin(16,2x) x sin(0,7y) x cos(0,6z) : la
   frequence n'etait haute QUE SUR X. En y et en z, 0,7 et 0,6, c'est-a-dire
   une enveloppe a l'echelle de la boule entiere — donc des lobes verticaux,
   donc une courge. La regle « haute frequence » etait ecrite, elle n'etait
   appliquee que sur un axe.
   ICI : toutes les frequences sont >= 8 SUR LES TROIS AXES, l'amplitude
   totale ne depasse pas 3,6 %, ET le deplacement radial est AMORTI AU LIMBE
   (facteur face^0,6, nul la ou la normale est perpendiculaire au regard).
   Consequence : la silhouette est un CERCLE EXACT, quelle que soit
   l'amplitude. Le relief vit dans le disque, jamais sur son bord. */
function phi(x,y,z,R){
  var s=0;
  for(var i=0;i<R.length;i++){
    var h=R[i];
    s+=h[0]*Math.sin(h[1]*x+h[4])*Math.sin(h[2]*y+h[5])*Math.cos(h[3]*z+h[6]);
  }
  return s;
}
var P_PEAU =[[0.024, 9.3,10.7, 8.9,0.4,1.1,2.2],[0.012,19.7,17.3,18.1,1.9,0.3,1.4]];
var P_TRAME=[[0.021,13.1,12.7,11.9,0.7,2.4,1.0],[0.011,25.3,23.9,24.7,2.7,1.8,0.4]];
var P_GLACE=[[0.018,10.9,11.7,12.3,1.3,0.5,1.9],[0.010,22.1,20.7,21.3,0.8,2.1,0.6]];

/* ── L'EMPREINTE — UNE PULPE, PAS UNE CLOCHE ──────────────────────────────
   L'ancien modele etait (1 - k e2) exp(-lam e2) : une gaussienne. Une pulpe
   molle ne fait pas ca. Elle s'APLATIT contre la surface :

     s <= 1   LE PLATEAU. Enfoncement CONSTANT, egal partout. La surface
              epouse le doigt : elle est PLANE, donc elle prend un seul
              niveau de lumiere — un mereau plat, pas un puits.
              Et le contact ADHERE : rien ne glisse a l'interieur.
     s  = 1   LE BORD FRANC. La pente saute ; ce n'est pas une decroissance.
     s  > 1   LA PAROI (exp(-u/rho), rho = 0,10 : elle remonte en un rien)
              puis LE BOURRELET (pic a u = ub), la matiere chassee.
              Et c'est LA, et seulement la, que ca glisse vers l'exterieur.

   ET ELLE GRANDIT AVEC LA PRESSION. Contact de Hertz : le rayon de contact
   va comme la racine cubique de la force, l'enfoncement comme sa puissance
   2/3. Donc a = amax p^(1/3), d = dmax p^(2/3). A pression 1/8, le rayon
   vaut la moitie. C'est ca qui fait doigt. */
function prepEmp(E, cl,sl,ct,st){
  /* ⚑ LE BUG PAYE QUATRE SERIES : l'empreinte donnee dans le repere de
     l'OBJET tombait derriere la sphere. On la donne FACE A NOUS et on
     applique la rotation INVERSE. */
  var inv=function(v){
    var zp=-v[1]*st+v[2]*ct, y=v[1]*ct+v[2]*st;
    return [v[0]*cl-zp*sl, y, v[0]*sl+zp*cl];
  };
  var n=function(v){var m=Math.hypot(v[0],v[1],v[2])||1;return [v[0]/m,v[1]/m,v[2]/m];};
  var o={};
  for(var k in E) o[k]=E[k];
  o.c=n(inv(E.c));
  /* ⚑ BUG TROUVE ICI, ET IL EST DE LA MEME FAMILLE QUE CELUI DE L'AUDIT.
     L'axe du doigt n'etait pas TANGENT au point de contact : il gardait une
     part radiale. « du » melangeait donc du tangentiel et du radial, et la
     zone s<1 n'etait plus une tache sur la surface mais un CYLINDRE qui
     traverse la boule — il ressortait de l'autre cote, et on voyait une
     seconde empreinte detachee, hors silhouette. On orthogonalise. */
  var a0=n(inv(E.ax)), dp=a0[0]*o.c[0]+a0[1]*o.c[1]+a0[2]*o.c[2];
  o.ax=n([a0[0]-dp*o.c[0], a0[1]-dp*o.c[1], a0[2]-dp*o.c[2]]);
  o.aC=E.cloche? E.a : E.a*Math.pow(E.p,1/3);   /* la cloche ne grandit pas */
  o.bC=o.aC*(E.el||0.62);
  o.d =E.dmax*Math.pow(E.p,2/3);
  return o;
}
/* rend {s, w, gl} : s la distance normalisee (1 = le bord du plateau),
   w le deplacement radial, gl le glissement vers l'exterieur */
function contact(E,x,y,z){
  /* ⚠ la tache de contact se mesure DANS LE PLAN TANGENT au point touche.
     Mesuree dans l'espace, elle devient un cylindre qui traverse la boule. */
  var vx=x-E.c[0], vy=y-E.c[1], vz=z-E.c[2];
  var vr=vx*E.c[0]+vy*E.c[1]+vz*E.c[2];
  vx-=vr*E.c[0]; vy-=vr*E.c[1]; vz-=vr*E.c[2];
  var du=vx*E.ax[0]+vy*E.ax[1]+vz*E.ax[2];
  var wx=vx-du*E.ax[0], wy=vy-du*E.ax[1], wz=vz-du*E.ax[2];
  var dv=Math.sqrt(wx*wx+wy*wy+wz*wz);
  if(vr<-0.55) return null;                  /* jamais la face opposee */
  du-=(E.biais||0)*E.aC;                       /* la pulpe appuie plus que le bout */
  var s=Math.sqrt((du/E.aC)*(du/E.aC)+(dv/E.bC)*(dv/E.bC));
  if(s>3.4) return null;
  /* ⚑ LE TEMOIN : l'ANCIENNE loi, une cloche gaussienne. Il ne sert qu'a la
     mesure — c'est contre lui qu'on prouve que le plateau existe vraiment.
     (1 - k e2) exp(-lam e2) : ni fond plat, ni bord franc, ni croissance. */
  var _ex=du*E.ax[0]+wx, _ey=du*E.ax[1]+wy, _ez=du*E.ax[2]+wz;
  var _m=Math.hypot(_ex,_ey,_ez)||1;
  if(E.cloche){
    var e2=s*s, gu=(1-1.9*e2)*Math.exp(-1.6*e2);
    return {s:s,w:-E.d*gu,gl:(E.U||0.9)*E.d*Math.max(0,gu)*0.7,plat:0,
            dx:_ex/_m,dy:_ey/_m,dz:_ez/_m,__c:1};
  }
  if(s<=1) return {s:s,w:-E.d,gl:0,plat:1,dx:0,dy:0,dz:0};
  var u=s-1, ub=E.ub||0.30, rho=E.rho||0.10;
  var bosse=(u/ub)*Math.exp(1-u/ub);
  var w=-E.d*Math.exp(-u/rho) + (E.B||0.55)*E.d*bosse;
  /* la direction du glissement : radiale, dans le plan tangent */
  return {s:s,w:w,gl:(E.U||0.9)*E.d*bosse,plat:0,dx:_ex/_m,dy:_ey/_m,dz:_ez/_m};
}

