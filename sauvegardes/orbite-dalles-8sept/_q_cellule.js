/* ════════════════════════════════════════════════════════════════════════════
   L'ORBITE — LE MOTEUR DESSINE LUI-MEME CHAQUE CELLULE.

   ⚑ POURQUOI ON REPART DE ZERO ICI.
   L'ancienne chaine etait : raster d'une dalle -> nuage de points -> tampon de
   poil. Trois approximations empilees, et une contradiction insoluble : un poil
   fait 6 px, un motif du moteur a un pas de 5 a 11 px. Poil plus petit que le
   motif, il l'ecrase ; motif agrandi pour le sauver, une cellule n'en montre
   plus qu'un ou deux et LE MOTIF CESSE D'ETRE UN MOTIF. A l'echelle d'une dalle
   de 67 px il n'y a pas de place pour un grain de fourrure entre les deux.

   Ici : on calcule le VRAI POLYGONE de chaque cellule sur la sphere, on le
   projette, on decoupe dessus, et on laisse `Toile.dalleTrame` peindre dedans
   A L'ECHELLE 1. Contour vectoriel net, vrai motif, vrai pas, vraies couleurs,
   vraies strates — parce que c'est le moteur qui peint, pas moi qui le
   reechantillonne.
   ════════════════════════════════════════════════════════════════════════════ */
var TAU=6.283185307179586;
function hh(i){var x=(i*2654435761)>>>0; x^=x>>>15; x=(x*2246822519)>>>0;
  x^=x>>>13; x=(x*3266489917)>>>0; x^=x>>>16; return (x>>>8)/16777216;}
function nrm(v){var m=Math.hypot(v[0],v[1],v[2])||1;return [v[0]/m,v[1]/m,v[2]/m];}

/* ── LE SEMIS DES SITES — la densite fait la taille des dalles ────────────
   (acquis du lot precedent : c'est la DENSITE qui donne des grandes et des
   petites dalles, jamais le poids — un site a poids faible est avale, pas
   retreci.) */
function densite(x,y,z,K){
  var v=0.5+0.5*Math.sin(K[0]*x+K[3])*Math.cos(K[1]*y+K[4])*Math.sin(K[2]*z+K[5]);
  var w=0.5+0.5*Math.sin(K[6]*z+K[9])*Math.cos(K[7]*x+K[10])*Math.sin(K[8]*y+K[11]);
  return 0.10+0.90*Math.pow(0.60*v+0.40*w, 2.0);
}
function sites(M,K){
  var CAND=M*24, i, dn=new Float64Array(CAND), som=0, GOLD=2.399963229728653;
  for(i=0;i<CAND;i++){
    var y=1-2*(i+0.5)/CAND, r=Math.sqrt(Math.max(0,1-y*y)), a=i*GOLD;
    dn[i]=densite(Math.cos(a)*r,y,Math.sin(a)*r,K); som+=dn[i];
  }
  var taux=M/som, S=[];
  for(i=0;i<CAND;i++){
    if(hh(i*7+3)>=dn[i]*taux) continue;
    var y2=1-2*(i+0.5)/CAND, r2=Math.sqrt(Math.max(0,1-y2*y2)), a2=i*GOLD;
    var jx=(hh(i*11+1)-0.5)*0.06, jy=(hh(i*13+5)-0.5)*0.06, jz=(hh(i*17+9)-0.5)*0.06;
    S.push(nrm([Math.cos(a2)*r2+jx, y2+jy, Math.sin(a2)*r2+jz]));
  }
  return S;
}

/* ── LE POLYGONE D'UNE CELLULE — Sutherland-Hodgman sur la sphere ─────────
   La cellule d'un site est l'intersection des demi-espaces { p . (Si-Sj) >= d }.
   On part d'une calotte large et on la RABOTE par chaque bissectrice. Le
   resultat est le contour EXACT, en sommets — pas une frontiere devinee point
   par point. `inset` recule chaque plan : c'est le filet entre deux dalles. */
function cellule(S, i, inset){
  var Si=S[i], k;
  /* la calotte de depart, largement au-dela de la plus grande cellule */
  var h=Math.abs(Si[1])<0.9?[0,1,0]:[1,0,0];
  var e1=nrm([Si[1]*h[2]-Si[2]*h[1], Si[2]*h[0]-Si[0]*h[2], Si[0]*h[1]-Si[1]*h[0]]);
  var e2=[Si[1]*e1[2]-Si[2]*e1[1], Si[2]*e1[0]-Si[0]*e1[2], Si[0]*e1[1]-Si[1]*e1[0]];
  var P=[], N0=12, ray=1.15;
  for(k=0;k<N0;k++){
    var a=k/N0*TAU, ca=Math.cos(ray), sa=Math.sin(ray);
    P.push(nrm([Si[0]*ca+(e1[0]*Math.cos(a)+e2[0]*Math.sin(a))*sa,
                Si[1]*ca+(e1[1]*Math.cos(a)+e2[1]*Math.sin(a))*sa,
                Si[2]*ca+(e1[2]*Math.cos(a)+e2[2]*Math.sin(a))*sa]));
  }
  for(var j=0;j<S.length && P.length>2;j++){
    if(j===i) continue;
    var Sj=S[j];
    var n=[Si[0]-Sj[0], Si[1]-Sj[1], Si[2]-Sj[2]];
    var nm=Math.hypot(n[0],n[1],n[2]); if(nm<1e-9) continue;
    n=[n[0]/nm,n[1]/nm,n[2]/nm];
    /* on ne garde que si la bissectrice peut couper : demi-angle de la cellule */
    var dec=inset;                       /* le plan recule : le JOINT entre dalles */
    var Q=[], m=P.length;
    for(k=0;k<m;k++){
      var a1=P[k], b1=P[(k+1)%m];
      var da=a1[0]*n[0]+a1[1]*n[1]+a1[2]*n[2]-dec;
      var db=b1[0]*n[0]+b1[1]*n[1]+b1[2]*n[2]-dec;
      if(da>=0) Q.push(a1);
      if((da>=0)!==(db>=0)){
        var t=da/(da-db);
        Q.push(nrm([a1[0]+(b1[0]-a1[0])*t, a1[1]+(b1[1]-a1[1])*t, a1[2]+(b1[2]-a1[2])*t]));
      }
    }
    P=Q;
  }
  return P;
}

/* ── LES FIBRES — le coton par-dessus ────────────────────────────────────
   ⚑ CE QUI A ETE COMPRIS TROP TARD : la fourrure ne doit pas PORTER le dessin,
   elle doit le RECOUVRIR. Tant que chaque poil devait dire « ici il y a de la
   matiere du motif », il fallait qu'il soit aussi petit que le motif — et il
   l'ecrasait. Ici, le moteur a deja peint la dalle : la fibre n'a plus qu'a
   prendre LA COULEUR DE CE QU'IL Y A DESSOUS et la duveter. Elle peut donc
   etre fine, dense, et deborder — c'est ce debord qui fait le coton. */
function semisFibres(N){
  var P=new Float32Array(N*3), F=new Float32Array(N*3), GOLD=2.399963229728653;
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, r=Math.sqrt(Math.max(0,1-y*y)), a=i*GOLD;
    var x=Math.cos(a)*r, z=Math.sin(a)*r;
    /* un peu de desordre : un reseau de Fibonacci laisse voir sa spirale */
    var pas=Math.sqrt(12.566370614/N);
    x+=(hh(i*3+1)-0.5)*pas; y+=(hh(i*5+2)-0.5)*pas; z+=(hh(i*7+4)-0.5)*pas;
    var m=Math.hypot(x,y,z)||1; x/=m; y/=m; z/=m;
    P[i*3]=x; P[i*3+1]=y; P[i*3+2]=z;
    /* LE PEIGNAGE : un champ lisse, pas un hachage. Un hachage donne un
       herisson ; un champ donne un pelage. */
    var e=0.03;
    var f=function(a2,b2,c2){
      return Math.sin(2.3*a2+0.7)*Math.cos(1.9*b2+1.9)*Math.sin(2.1*c2+0.4)
           + 0.6*Math.sin(3.7*c2-1.1)*Math.cos(3.1*a2+0.5);};
    var gx=f(x+e,y,z)-f(x-e,y,z), gy=f(x,y+e,z)-f(x,y-e,z), gz=f(x,y,z+e)-f(x,y,z-e);
    var d=gx*x+gy*y+gz*z;
    gx-=d*x; gy-=d*y; gz-=d*z;
    var gm=Math.hypot(gx,gy,gz)||1;
    F[i*3]=gx/gm; F[i*3+1]=gy/gm; F[i*3+2]=gz/gm;
  }
  return {P:P, F:F, n:N};
}
/* le tampon d'une TOUFFE de fibres : trois brins d'une meme racine, effiles */
function atlasFibres(tailles, ORI){
  var S=48, cv=document.createElement('canvas'); cv.width=S; cv.height=S;
  var g=cv.getContext('2d'), A=[];
  var T=[[0,1.00,0.30],[0.34,0.80,-0.16],[-0.30,0.86,0.44]];
  for(var s=0;s<tailles.length;s++) for(var r=0;r<ORI;r++){
    g.clearRect(0,0,S,S);
    g.save(); g.translate(S/2,S/2); g.rotate(r*TAU/ORI);
    g.strokeStyle='#fff'; g.lineCap='round';
    var e=tailles[s];
    for(var k=0;k<T.length;k++){
      g.save(); g.rotate(T[k][0]);
      var L=e*T[k][1], cby=e*T[k][2], NP=5;
      for(var q=0;q<NP;q++){
        var t0=q/NP, t1=(q+1)/NP, m0=1-t0, m1=1-t1;
        var ax=2*m0*t0*L*0.6+t0*t0*L, ay=2*m0*t0*cby*0.35+t0*t0*cby;
        var bx=2*m1*t1*L*0.6+t1*t1*L, by=2*m1*t1*cby*0.35+t1*t1*cby;
        g.globalAlpha=1-t0*0.80;
        g.lineWidth=Math.max(0.7,e*0.17)*(1-t0*0.72);
        g.beginPath(); g.moveTo(ax,ay); g.lineTo(bx,by); g.stroke();
      }
      g.restore();
    }
    g.globalAlpha=1; g.restore();
    var d=g.getImageData(0,0,S,S).data;
    var x1=S,y1=S,x2=-1,y2=-1;
    for(var y=0;y<S;y++)for(var x=0;x<S;x++) if(d[(y*S+x)*4+3]>4){
      if(x<x1)x1=x; if(x>x2)x2=x; if(y<y1)y1=y; if(y>y2)y2=y; }
    if(x2<0){x1=y1=S/2;x2=y2=S/2;}
    var off=[], al=[];
    for(y=y1;y<=y2;y++)for(x=x1;x<=x2;x++){
      var a=d[(y*S+x)*4+3];
      if(a>4){ off.push([y-S/2, x-S/2]); al.push(a); }
    }
    A.push({rel:off, al:al});
  }
  return A;
}
function lieFib(A,W){
  if(A.__W===W) return A;
  var i,j,tot=0;
  for(i=0;i<A.length;i++) tot+=A[i].rel.length;
  var OF=new Int32Array(tot), AL=new Uint8Array(tot), ST=new Int32Array(A.length+1), p=0;
  for(i=0;i<A.length;i++){
    ST[i]=p;
    for(j=0;j<A[i].rel.length;j++){ OF[p]=A[i].rel[j][0]*W+A[i].rel[j][1]; AL[p]=A[i].al[j]; p++; }
  }
  ST[A.length]=p;
  A.__off=OF; A.__al=AL; A.__st=ST; A.__W=W;
  return A;
}
