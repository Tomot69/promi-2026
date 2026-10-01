
var CREME='#F4EEE1', ENCRE='#16171B';
function cc(){return [200,180,255];}
function render(){}
var state={structure:'encre'};

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
        var q=(n+0.5)/NIV, mul=a0+(a1-a0)*q*q;
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
  o.aC=E.a*Math.pow(E.p,1/3);
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
  if(s<=1) return {s:s,w:-E.d,gl:0,plat:1,dx:0,dy:0,dz:0};
  var u=s-1, ub=E.ub||0.30, rho=E.rho||0.10;
  var bosse=(u/ub)*Math.exp(1-u/ub);
  var w=-E.d*Math.exp(-u/rho) + (E.B||0.55)*E.d*bosse;
  /* la direction du glissement : radiale, dans le plan tangent */
  var ex=du*E.ax[0]+wx, ey=du*E.ax[1]+wy, ez=du*E.ax[2]+wz;
  var m=Math.hypot(ex,ey,ez)||1;
  return {s:s,w:w,gl:(E.U||0.9)*E.d*bosse,plat:0,dx:ex/m,dy:ey/m,dz:ez/m};
}

/* ════════════════════════════════════════════════════════════════════════════
   LES TROIS SEMIS — ce sont TROIS PARTIS PRIS, pas trois rendus.
   Un point ne peut pas etre a la fois un grain libre, un maillon de fil, et
   une cellule d'un pavage. Chacun porte SA loi de contact.
   ════════════════════════════════════════════════════════════════════════════ */
function fr(v){return v-Math.floor(v);}
var GOLD=2.399963229728653;

/* ── A · LA POUSSIERE ─────────────────────────────────────────────────────
   N grains independants. Ce qu'on lit : une DENSITE. */
function semisPoussiere(N){
  var P=new Float64Array(N*3);
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, r=Math.sqrt(Math.max(0,1-y*y)), a=i*GOLD;
    P[i*3]=Math.cos(a)*r; P[i*3+1]=y; P[i*3+2]=Math.sin(a)*r;
  }
  return {P:P, n:N, brins:null};
}

/* ── B · LE FIL ───────────────────────────────────────────────────────────
   K brins CONTINUS enroules autour de la boule. Ce qu'on lit : un BOBINAGE.
   Le chemin d'un brin n'est pas un grand cercle : sa colatitude ONDULE
   (l'onde de Promi, portee sur la sphere) — nu tours entiers, donc le brin
   se referme sur lui-meme. C'est ce qui fait les noeuds et les moires. */
function semisFil(K,M,amp){
  var P=new Float64Array(K*M*3), brins=[], NU=[2,3,3,5,5,7,4,6];
  for(var k=0;k<K;k++){
    /* l'axe du brin : reparti sur la sphere par deux irrationnels */
    var t=fr(k*0.6180339887), u2=fr(k*0.7548776662);
    var cz=1-2*(t+0.5/K), sr=Math.sqrt(Math.max(0,1-cz*cz)), az=u2*TAU;
    var ax=[sr*Math.cos(az), cz, sr*Math.sin(az)];
    /* deux vecteurs du plan du brin */
    var h=Math.abs(ax[1])<0.9?[0,1,0]:[1,0,0];
    var e1=[ax[1]*h[2]-ax[2]*h[1], ax[2]*h[0]-ax[0]*h[2], ax[0]*h[1]-ax[1]*h[0]];
    var m1=Math.hypot(e1[0],e1[1],e1[2]); e1=[e1[0]/m1,e1[1]/m1,e1[2]/m1];
    var e2=[ax[1]*e1[2]-ax[2]*e1[1], ax[2]*e1[0]-ax[0]*e1[2], ax[0]*e1[1]-ax[1]*e1[0]];
    var nu=NU[k%NU.length], ph=fr(k*0.4142135624)*TAU, am=amp*(0.55+0.9*fr(k*0.3819660113));
    brins.push([k*M, M]);
    for(var i=0;i<M;i++){
      var th=i/M*TAU;
      var co=am*Math.sin(nu*th+ph);          /* L'ONDE : la colatitude respire */
      var sc=Math.cos(co), sa=Math.sin(co);
      var cx=Math.cos(th+ph*0.13), sx=Math.sin(th+ph*0.13);
      var j=(k*M+i)*3;
      P[j]  = sc*(e1[0]*cx+e2[0]*sx) + sa*ax[0];
      P[j+1]= sc*(e1[1]*cx+e2[1]*sx) + sa*ax[1];
      P[j+2]= sc*(e1[2]*cx+e2[2]*sx) + sa*ax[2];
    }
  }
  return {P:P, n:K*M, brins:brins};
}

/* ── C · LE PAVAGE ────────────────────────────────────────────────────────
   Les COUTURES d'un Voronoi PONDERE spherique. Ce qu'on lit : une PARTITION.
   C'est la Toile — meme loi, meme diagramme de puissance — fermee sur
   elle-meme. Les poids varient, donc les cellules aussi : des grandes et des
   petites, comme sur une vraie Toile, jamais une grille.
   ⚠ On ne calcule ce nuage QU'UNE FOIS : la partition ne bouge pas, seule la
   vue tourne. Le cout par image redevient celui de la poussiere. */
function semisPavage(NC,M,eps){
  var S=new Float64Array(M*3), Wt=new Float64Array(M);
  for(var k=0;k<M;k++){
    var y=1-2*(k+0.5)/M, r=Math.sqrt(Math.max(0,1-y*y)), a=k*GOLD;
    /* un peu de desordre : un semis parfait donne des cellules toutes pareilles */
    var jx=(fr(k*0.7548776662)-0.5)*0.16, jy=(fr(k*0.3819660113)-0.5)*0.16;
    var x=Math.cos(a)*r+jx, yy=y+jy, z=Math.sin(a)*r+jx*0.6;
    var m=Math.hypot(x,yy,z)||1;
    S[k*3]=x/m; S[k*3+1]=yy/m; S[k*3+2]=z/m;
    Wt[k]=(fr(k*0.2360679775)-0.5)*0.115;      /* LE POIDS : c'est lui qui fait la Toile */
  }
  var out=[], brins=null;
  for(var i=0;i<NC;i++){
    var cy=1-2*(i+0.5)/NC, cr=Math.sqrt(Math.max(0,1-cy*cy)), ca=i*GOLD;
    var px=Math.cos(ca)*cr, py=cy, pz=Math.sin(ca)*cr;
    var d1=9, d2=9;
    for(var k2=0;k2<M;k2++){
      var dp=px*S[k2*3]+py*S[k2*3+1]+pz*S[k2*3+2];
      if(dp>1)dp=1; if(dp<-1)dp=-1;
      var dd=Math.acos(dp)-Wt[k2];
      if(dd<d1){ d2=d1; d1=dd; } else if(dd<d2){ d2=dd; }
    }
    if(d2-d1<eps) out.push(px,py,pz);
  }
  var P=new Float64Array(out.length);
  for(var q=0;q<out.length;q++) P[q]=out[q];
  return {P:P, n:out.length/3, brins:null, pavage:1};
}

/* ════════════════════════════════════════════════════════════════════════════
   LE PEINTRE — et LES TROIS LOIS DE CONTACT.
   ════════════════════════════════════════════════════════════════════════════ */
var ORI=12;
function lisse(a,b,v){ var t=(v-a)/(b-a); if(t<0)t=0; if(t>1)t=1; return t*t*(3-2*t); }

/* LES SIX + LE NOYAU — identiques dans les neuf cadres : ce n'est pas la
   variable qu'on teste, c'est le decor qui rend la composition lisible.
   Le rayon dit la date de la derniere parole tenue (acquis, on n'y touche pas). */
var SIX=[[0.34,0.30],[1.42,0.58],[2.31,0.86],[3.55,0.44],[4.48,0.72],[5.63,0.94]];

function decor(g,CX,CY,R,CSS){
  var d=D;
  g.save();
  for(var i=0;i<SIX.length;i++){
    var th=SIX[i][0], rho=SIX[i][1];
    var x=CX+Math.cos(th)*rho*R, y=CY+Math.sin(th)*rho*R*0.46;
    var r=11.5*d;
    g.beginPath(); g.arc(x,y,r+3.2*d,0,TAU);
    g.fillStyle='rgba(22,23,27,.86)'; g.fill();          /* la matiere s'ecarte */
    g.beginPath(); g.arc(x,y,r,0,TAU);
    g.fillStyle='rgba(22,23,27,1)'; g.fill();
    g.lineWidth=1.9*d; g.strokeStyle='rgba(244,238,225,.90)'; g.stroke();
  }
  g.restore();
}
function noyau(g,CX,CY){
  var d=D, r=27*d;
  g.beginPath(); g.arc(CX,CY,r+7*d,0,TAU); g.fillStyle='rgba(22,23,27,.90)'; g.fill();
  g.beginPath(); g.arc(CX,CY,r,0,TAU); g.fillStyle='#F4EEE1'; g.fill();
}

function peint(cv,o){
  var CSS=o.css||400, W=CSS*D;
  cv.width=W; cv.height=W;
  var g=cv.getContext('2d');
  g.fillStyle='#16171B'; g.fillRect(0,0,W,W);
  var NIV=o.niv||10, TAI=o.tailles;
  var A=lieTampons(o.atlas,W);
  var R=CSS*(o.R||0.405)*D, FOC=R*5.4, CX=W/2, CY=W/2;
  var lac=o.lac, tan=o.tan;
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var E=o.emp?prepEmp(o.emp,cl,sl,ct,st):null;
  var S=o.semis, P=S.P, N=S.n, REL=o.relief;
  var LX=-0.40, LY=-0.62, LZ=0.675;                    /* la lumiere, haut-gauche-avant */
  var t0=performance.now();

  /* ── position deformee + normale, point par point ───────────────────── */
  var QX=new Float64Array(N), QY=new Float64Array(N), QZ=new Float64Array(N);
  var NX=new Float64Array(N), NY=new Float64Array(N), NZ=new Float64Array(N);
  var PLAT=new Uint8Array(N);
  var e=0.014, i, j;
  for(i=0;i<N;i++){
    var x=P[i*3], y=P[i*3+1], z=P[i*3+2];
    var ph0=REL?phi(x,y,z,REL):0;
    var nx=x, ny=y, nz=z;
    if(REL){
      var gx=(phi(x+e,y,z,REL)-phi(x-e,y,z,REL))/(2*e);
      var gy=(phi(x,y+e,z,REL)-phi(x,y-e,z,REL))/(2*e);
      var gz=(phi(x,y,z+e,REL)-phi(x,y,z-e,REL))/(2*e);
      var dot=gx*x+gy*y+gz*z;                          /* on ne garde que la part TANGENTE */
      nx=x+(gx-dot*x)*1.15; ny=y+(gy-dot*y)*1.15; nz=z+(gz-dot*z)*1.15;
      var m0=Math.hypot(nx,ny,nz)||1; nx/=m0; ny/=m0; nz/=m0;
    }
    var rr=1+ph0, X=x, Y=y, Z=z;
    /* ⚑ L'AMORTI AU LIMBE : le relief radial s'annule la ou la normale est
       perpendiculaire au regard. La silhouette est donc un CERCLE EXACT.
       On a besoin de la profondeur de vue AVANT de deformer : on la prend sur
       la position non deformee, ce qui suffit a 3 % d'amplitude. */
    var zv0=(-x*sl+z*cl); zv0=y*st+(zv0)*ct;
    var face=zv0>0?zv0:0;
    rr=1+ph0*Math.pow(face,0.6);
    /* L'EMPREINTE */
    var pl=0;
    if(E){
      var c1=contact(E,x,y,z);
      if(c1){
        if(c1.plat){
          /* LE PLATEAU : la surface epouse le doigt — elle devient PLANE.
             On projette le point sur le plan perpendiculaire a l'axe du doigt.
             Consequence directe : la normale y est CONSTANTE, donc le contact
             se lit comme un mereau uniformement eclaire, jamais comme un puits. */
          /* ⚑ LE PLAN DE CONTACT EST PERPENDICULAIRE A LA NORMALE, jamais a
             l'axe du doigt (qui est TANGENT). Perpendiculaire a l'axe, le
             « plateau » etait un plan qui TRANCHE la boule : on voyait une
             morsure, pas une pulpe. */
          var h=(1-E.d);
          var pa=x*E.c[0]+y*E.c[1]+z*E.c[2];
          X=x+E.c[0]*(h-pa); Y=y+E.c[1]*(h-pa); Z=z+E.c[2]*(h-pa);
          nx=E.c[0]; ny=E.c[1]; nz=E.c[2];
          pl=1; rr=1;
        } else {
          var h2=0.022;
          var c2=contact(E,x+c1.dx*h2,y+c1.dy*h2,z+c1.dz*h2);
          var pente=((c2?c2.w:0)-c1.w)/h2;
          rr+=c1.w;
          /* LE GLISSEMENT : il n'existe QU'A L'EXTERIEUR du plateau.
             Un vrai doigt ADHERE : rien ne glisse sous la pulpe. */
          X=x+c1.dx*c1.gl; Y=y+c1.dy*c1.gl; Z=z+c1.dz*c1.gl;
          var mm=Math.hypot(X,Y,Z)||1; X/=mm; Y/=mm; Z/=mm;
          nx-=c1.dx*pente; ny-=c1.dy*pente; nz-=c1.dz*pente;
          var m2=Math.hypot(nx,ny,nz)||1; nx/=m2; ny/=m2; nz/=m2;
        }
      }
    }
    if(!pl){ X*=rr; Y*=rr; Z*=rr; }
    /* la matiere encaisse, elle ne gicle pas : rien ne franchit l'enveloppe */
    var mr=Math.hypot(X,Y,Z);
    if(mr>1.035){ var f2=1.035/mr; X*=f2; Y*=f2; Z*=f2; }
    QX[i]=X; QY[i]=Y; QZ[i]=Z; NX[i]=nx; NY[i]=ny; NZ[i]=nz; PLAT[i]=pl;
  }

  /* ── LA LOI DE CONTACT DU FIL : il n'entre pas dans le creux, il l'ENJAMBE.
     Un brin est tendu. Sous le doigt, il quitte la surface et tire une corde
     droite d'un bord a l'autre du plateau — et il se serre juste a cote.
     C'est ce qu'aucune poussiere ne peut faire : il faut un ORDRE le long du
     fil pour savoir ou la corde commence et ou elle finit. ─────────────── */
  if(E && o.loi==='fil' && S.brins){
    for(var b=0;b<S.brins.length;b++){
      var i0=S.brins[b][0], M=S.brins[b][1];
      var dedans=new Uint8Array(M), any=0;
      for(j=0;j<M;j++){
        var cq=contact(E,P[(i0+j)*3],P[(i0+j)*3+1],P[(i0+j)*3+2]);
        if(cq && cq.s<=1){ dedans[j]=1; any=1; }
      }
      if(!any) continue;
      j=0;
      while(j<M){
        if(!dedans[j]){ j++; continue; }
        var a=j; while(dedans[(a-1+M)%M] && ((a-1+M)%M)!==j) a=(a-1+M)%M;
        var bb=j; while(dedans[(bb+1)%M] && ((bb+1)%M)!==a) bb=(bb+1)%M;
        var ia=(a-1+M)%M, ib=(bb+1)%M;
        var Ax=QX[i0+ia],Ay=QY[i0+ia],Az=QZ[i0+ia];
        var Bx=QX[i0+ib],By=QY[i0+ib],Bz=QZ[i0+ib];
        var len=(bb>=a? bb-a : bb+M-a)+2, k2=0, jj=a;
        while(true){
          var t=(k2+1)/len, TEN=o.tension===undefined?0.88:o.tension;
          var cx=Ax*(1-t)+Bx*t, cy=Ay*(1-t)+By*t, cz=Az*(1-t)+Bz*t;
          QX[i0+jj]=QX[i0+jj]*(1-TEN)+cx*TEN;
          QY[i0+jj]=QY[i0+jj]*(1-TEN)+cy*TEN;
          QZ[i0+jj]=QZ[i0+jj]*(1-TEN)+cz*TEN;
          NX[i0+jj]=E.ax[0]; NY[i0+jj]=E.ax[1]; NZ[i0+jj]=E.ax[2];
          PLAT[i0+jj]=2;                                /* le fil TENDU, pas le mereau */
          dedans[jj]=0;
          if(jj===bb) break;
          jj=(jj+1)%M; k2++;
          if(k2>M) break;
        }
        j=0; var reste=0; for(var q=0;q<M;q++) if(dedans[q]){reste=1;break;}
        if(!reste) break;
        while(!dedans[j]) j++;
      }
    }
  }

  /* ── projection, tri en deux tranches, versement ─────────────────────── */
  var avA=[], apA=[];
  var TN=TAI.length;
  for(i=0;i<N;i++){
    var X1=QX[i], Y1=QY[i], Z1=QZ[i];
    var X2=X1*cl+Z1*sl, Zt=-X1*sl+Z1*cl, Y2=Y1*ct-Zt*st; var Z2=Y1*st+Zt*ct;
    var nX=NX[i]*cl+NZ[i]*sl, nZt=-NX[i]*sl+NZ[i]*cl, nY=NY[i]*ct-nZt*st; var nZ2=NY[i]*st+nZt*ct;
    var k=FOC/(FOC-Z2*R);
    var px=(CX+X2*R*k)|0, py=(CY+Y2*R*k)|0;
    if(px<10||py<10||px>W-10||py>W-10) continue;
    /* LA LUMIERE : c'est elle qui fait le volume, pas la profondeur seule */
    var dl=nX*LX+nY*LY+nZ2*LZ; if(dl<0)dl=0;
    var lum=0.30+0.70*Math.pow(dl,0.85);
    if(Z2<0) lum*=0.46;                                 /* le dos, en retrait */
    /* LA RAREFACTION AU CENTRE : la place du Noyau, elle ne se negocie pas */
    var rho=Math.hypot(X2,Y2);
    lum*=0.16+0.84*lisse(0.06,0.56,rho);
    if(PLAT[i]===1) lum=Math.min(1,lum*1.34);           /* le mereau prend la lumiere a plat */
    if(PLAT[i]===2) lum=Math.min(1,lum*1.18);
    var niv=(lum*NIV)|0; if(niv>=NIV)niv=NIV-1; if(niv<0)niv=0;
    var zz=(Z2+1)*0.5, tai=(zz*TN)|0; if(tai>=TN)tai=TN-1; if(tai<0)tai=0;
    var ori;
    if(o.loi==='fil') ori=oriDe(QX,QY,QZ,i,N,cl,sl,ct,st);
    else              ori=(((i*2654435761)>>>0)%ORI);
    if(ori<0)ori+=ORI;
    var idx=(tai*ORI+ori)*NIV+niv;
    (Z2<0?avA:apA).push(py*W+px, idx);
  }
  var off=document.createElement('canvas'); off.width=W; off.height=W;
  var og=off.getContext('2d');
  verse(og,A,avA,W);  g.drawImage(off,0,0);
  decor(g,CX,CY,R,CSS);
  og.clearRect(0,0,W,W);
  verse(og,A,apA,W);  g.drawImage(off,0,0);
  noyau(g,CX,CY);
  return {n:(avA.length+apA.length)/2, ms:+(performance.now()-t0).toFixed(1)};
}
/* l'orientation du grain d'un FIL suit la tangente du brin, a l'ecran */
function oriDe(QX,QY,QZ,i,N,cl,sl,ct,st){
  var i2=(i+1<N)?i+1:i-1;
  var dx=QX[i2]-QX[i], dy=QY[i2]-QY[i], dz=QZ[i2]-QZ[i];
  var X2=dx*cl+dz*sl, Zt=-dx*sl+dz*cl, Y2=dy*ct-Zt*st;
  var a=Math.atan2(Y2,X2); if(a<0)a+=Math.PI; if(a>=Math.PI)a-=Math.PI;
  var o=((a/Math.PI)*ORI)|0; if(o>=ORI)o=ORI-1; return o;
}
function verse(og,A,L,W){
  var im=og.createImageData(W,W), B=new Uint32Array(im.data.buffer);
  for(var i=0;i<L.length;i+=2){
    var sp=A[L[i+1]]; if(!sp) continue;
    var bas=L[i], of=sp.off, va=sp.val;
    for(var j=0;j<sp.n;j++){
      var oo=bas+of[j], vv=va[j];
      if(oo>=0 && oo<B.length && (vv>>>24)>(B[oo]>>>24)) B[oo]=vv;
    }
  }
  og.putImageData(im,0,0);
}

/* ════════════════════════════════════════════════════════════════════════════
   LES NEUF CADRES — trois partis pris x trois pressions.
   Le grain est LE MEME partout (le fil, seul retenu) et la couleur aussi
   (creme sur encre). On ne fait varier que DE QUOI la matiere est faite et
   CE QU'ELLE FAIT quand on appuie. Une variable a la fois.
   ════════════════════════════════════════════════════════════════════════════ */
var EMP_BASE={ c:[-0.40,-0.26,0.88], ax:[0.62,-0.72,0.00],
               a:0.34, el:0.64, dmax:0.105, biais:0.14,
               rho:0.10, ub:0.30, B:0.55, U:1.10 };
function emp(p){ var o={}; for(var k in EMP_BASE)o[k]=EMP_BASE[k]; o.p=p; return o; }

var RANGS=[
 {id:'poussiere', h:'A · La poussiere',
  d:'Des grains independants. Ce qu\'on lit, c\'est une <b>densite</b>. Sous le doigt, chaque grain suit la surface et se fait chasser vers l\'exterieur — chacun pour soi.',
  loi:'poussiere', relief:P_PEAU, tailles:[5.0,7.0,9.5],
  legs:['Au repos.','Effleuree — le plateau fait deja un mereau net, petit.','Appuyee — le meme mereau, deux fois plus large, et son bourrelet.']},
 {id:'fil', h:'B · Le fil',
  d:'Deux cents brins <b>continus</b> enroules, dont la colatitude ondule. Ce qu\'on lit, c\'est un <b>bobinage</b> et une <b>tension</b>. Sous le doigt, un brin tendu n\'entre pas dans le creux : <b>il l\'enjambe</b>.',
  loi:'fil', relief:P_TRAME, tailles:[4.0,5.2,6.8],
  legs:['Au repos.','Effleuree — les cordes commencent a se tendre au-dessus du creux.','Appuyee — une toile tendue par-dessus le vide, et les brins se serrent au bord.']},
 {id:'pavage', h:'C · Le pavage',
  d:'Les <b>coutures</b> d\'un Voronoi pondere spherique — la Toile, meme loi, fermee sur elle-meme. Ce qu\'on lit, c\'est une <b>partition</b>. Sous le doigt, rien ne se disperse : la partition se <b>cisaille</b> et laisse un <b>sceau</b>.',
  loi:'pavage', relief:P_GLACE, tailles:[3.0,4.0,5.2],
  legs:['Au repos.','Effleuree — les cellules du contact s\'aplatissent d\'un bloc.','Appuyee — un sceau appose dans la matiere, cellules serrees tout autour.']}
];

window.addEventListener('load',function(){
  try{ window.Toile_resize&&window.Toile_resize(); window.Toile&&Toile.sync([1,2,3,4,5,6,7,8,9]); }catch(e){}
  setTimeout(function(){
    /* ⚠ la copie du moteur vieillit en silence : on VERIFIE ce qu'elle sait faire */
    window.__moteur = !!(window.Toile && window.Toile.mondeCourant);
    var CR=[244,238,225];
    var SEM={};
    SEM.poussiere = semisPoussiere(30000);
    SEM.fil       = semisFil(200,170,0.20);
    SEM.pavage    = semisPavage(220000,300,0.0090);
    var ATL={};
    RANGS.forEach(function(r){
      ATL[r.id]=atlasForme(GRAIN_FIL, CR, r.tailles, ORI, 10, 0.05, 1.00);
    });
    var G=document.getElementById('g'), infos=[];
    RANGS.forEach(function(r){
      var sec=document.createElement('div'); sec.className='rang';
      sec.innerHTML='<h2>'+r.h+'</h2><p>'+r.d+'</p>';
      var gr=document.createElement('div'); gr.className='grille'; sec.appendChild(gr);
      G.appendChild(sec);
      [0,0.14,1.0].forEach(function(p,ci){
        var fg=document.createElement('figure');
        var box=document.createElement('div'); box.className='cadre';
        var cv=document.createElement('canvas'); cv.setAttribute('data-cad',r.id+'-'+ci);
        box.appendChild(cv); fg.appendChild(box);
        var fc=document.createElement('figcaption'); fc.innerHTML=r.legs[ci];
        fg.appendChild(fc); gr.appendChild(fg);
        var o={css:392, R:0.405, niv:10, tailles:r.tailles, atlas:ATL[r.id],
               semis:SEM[r.id], relief:r.relief, loi:r.loi, lac:2.9, tan:0.32,
               emp: p>0?emp(p):null, tension:0.88};
        infos.push(peint(cv,o));
      });
    });
    window.__infos=infos; window.__pret=true;
  },700);
});

