/* ════════════════════════════════════════════════════════════════════════════
   L'ORBITE — LE PAVAGE HABILLE.  Le moteur.
   Technique acquise : des tampons pre-rendus, verses dans un tampon de pixels,
   un putImageData. Aucun drawImage par grain (hors budget d'un facteur trois).
   ⚑ NOUVEAU ICI : le tampon ne porte plus que L'ALPHA. La couleur se compose au
   versement, par un OR. Sans ca, 4 couleurs x 6 marches x 3 tailles x 8
   orientations x 6 niveaux faisaient 3 456 tampons ; il y en a 144.
   ════════════════════════════════════════════════════════════════════════════ */
var D=2, TAU=6.283185307179586;

function fabTampon(dat,src,x1,y1,w,h,ox,oy,mul){
  var off=[], alp=[];
  for(var y=0;y<h;y++)for(var x=0;x<w;x++){
    var al=(dat[((y1+y)*src+(x1+x))*4+3]*mul)|0;
    if(al>4){ off.push([y-oy,x-ox]); alp.push(al>255?255:al); }
  }
  return {rel:off, al:alp};
}
/* ⚑ L'ATLAS SE MET A PLAT — et c'est LA que part le temps par poil.
   Mesure : reduire un poil de 13,9 a 9,7 pixels ne gagne que 2,5 %. Ce ne sont
   donc pas les pixels ecrits qui coutent, c'est le TRAVAIL PAR POIL. Or chaque
   poil faisait `A[idx]` sur un tableau d'OBJETS puis lisait trois proprietes
   (`off`, `alp`, `n`) — trois dereferencements et deux en-tetes de tableau
   typé a ramener en cache, pour quatorze pixels a ecrire.
   On concatene tout dans DEUX grands tableaux typés, avec un depart et un
   compte par tampon. La boucle ne touche plus que de la memoire contigue. */
function lieTampons(A,W){
  if(A.__W===W) return A;
  var i,j,tot=0;
  for(i=0;i<A.length;i++) tot+=A[i].rel.length;
  var FOFF=new Int32Array(tot), FALP=new Uint32Array(tot);
  var FSTA=new Int32Array(A.length+1);
  var p=0;
  for(i=0;i<A.length;i++){
    FSTA[i]=p;
    var t=A[i], n=t.rel.length;
    for(j=0;j<n;j++){ FOFF[p]=t.rel[j][0]*W+t.rel[j][1]; FALP[p]=(t.al[j]&255)<<24; p++; }
    t.n=n;
  }
  FSTA[A.length]=p;
  A.__off=FOFF; A.__alp=FALP; A.__sta=FSTA; A.__W=W;
  return A;
}
/* LE GRAIN : le fil. C'est le seul grain retenu — on le garde. */
/* ⚑ LE POIL — la matiere est duveteuse, et elle flotte.
   Le brin part de la RACINE (le centre du tampon) et s'en va : il est donc
   oriente sur 360 degres, pas sur 180 comme un fil symetrique. Il s'affine et
   s'eteint vers la pointe — c'est ce qui fait doux plutot que herisse — et il
   s'incurve un peu, comme un poil dans un liquide. */
/* ⚑ UNE TOUFFE, PAS UN POIL — et c'est ce qui permet d'en avoir deux fois plus.
   Mesure : un poil coute 0,108 microseconde, dont seulement 0,042 de pixels
   ecrits. Les deux tiers sont le passage dans la BOUCLE — lectures, rotation,
   eclairage, rangement. Or quatre poils qui partent de la meme racine ne
   coutent qu'UN passage de boucle et quatre fois les pixels : chaque poil
   supplementaire revient a 0,042 au lieu de 0,108, deux fois et demie moins
   cher. Et une fourrure pousse en touffes, pas en brins isoles. */
function unPoil(g,L,ep,cby,N){
  var cbx=L*0.62;
  for(var i=0;i<N;i++){
    var t0=i/N, t1=(i+1)/N, mt0=1-t0, mt1=1-t1;
    var ax=2*mt0*t0*cbx+t0*t0*L, ay=2*mt0*t0*cby*0.35+t0*t0*cby;
    var bx=2*mt1*t1*cbx+t1*t1*L, by=2*mt1*t1*cby*0.35+t1*t1*cby;
    g.globalAlpha=(1-t0*0.86);                /* la pointe s'eteint */
    g.lineWidth=ep*(1-t0*0.78);               /* et elle s'affine */
    g.beginPath(); g.moveTo(ax,ay); g.lineTo(bx,by); g.stroke();
  }
}
var TOUFFE=[[[0,1.00,0.52],[0.30,0.86,0.20],[-0.26,0.78,0.80],[0.13,0.62,-0.22]],
            [[0,0.94,0.34],[-0.33,0.88,0.70],[0.28,0.72,-0.10],[0.06,0.58,0.92]],
            [[0,1.04,0.66],[0.22,0.80,-0.28],[-0.19,0.90,0.28],[0.36,0.60,0.58]]];
function GRAIN_POIL(g,e,v){
  var T=TOUFFE[(v||0)%TOUFFE.length], ep=Math.max(0.80,e*0.20);
  g.lineCap='round';
  for(var k=0;k<T.length;k++){
    g.save(); g.rotate(T[k][0]);
    unPoil(g, e*1.75*T[k][1], ep*(0.72+0.5*T[k][1]), e*T[k][2], 6);
    g.restore();
  }
  g.globalAlpha=1;
}
function GRAIN_FIL(g,e){
  /* ⚑ LE GRAIN DOIT COUVRIR. Trop maigre, une dalle n'est plus un aplat : elle
     devient une hachure clairsemee, et la mosaique se lit comme du bruit. Le
     fil est donc plus epais et plus long — a l'espacement du semis (0,0165 rad,
     soit 4,4 px sur le grand cadre), il faut environ 11 px carres par grain
     pour que la dalle fasse surface. */
  g.lineWidth=Math.max(1.0,e*0.27);
  g.beginPath(); g.moveTo(-e*1.10,0); g.lineTo(e*1.10,0); g.stroke();
}
function atlasAlpha(dessin, tailles, ORI, NIV, a0, a1, tour, NV){
  NV=NV||1;
  /* `tour` : le poil est oriente sur 2 pi (il a une racine et une pointe),
     un fil symetrique sur pi seulement. */
  var PL=tour?TAU:Math.PI;
  var S=80, cv=document.createElement('canvas'); cv.width=S; cv.height=S;
  var g=cv.getContext('2d'), A=[];
  for(var s=0;s<tailles.length;s++) for(var r=0;r<ORI*NV;r++){
    g.clearRect(0,0,S,S);
    g.save(); g.translate(S/2,S/2); g.rotate(((r/NV)|0)*PL/ORI);
    g.fillStyle='#fff'; g.strokeStyle='#fff'; g.lineCap='round';
    dessin(g, tailles[s], r%NV); g.restore();
    var d=g.getImageData(0,0,S,S).data;
    var x1=S,y1=S,x2=-1,y2=-1;
    for(var y=0;y<S;y++)for(var x=0;x<S;x++) if(d[(y*S+x)*4+3]>3){
      if(x<x1)x1=x; if(x>x2)x2=x; if(y<y1)y1=y; if(y>y2)y2=y; }
    if(x2<0){x1=y1=S/2;x2=y2=S/2;}
    var w=x2-x1+1, h=y2-y1+1, ox=S/2-x1, oy=S/2-y1;
    for(var n=0;n<NIV;n++){
      var q=(n+0.5)/NIV;
      A.push(fabTampon(d,S,x1,y1,w,h,ox,oy,a0+(a1-a0)*Math.pow(q,1.40)));
    }
  }
  return A;
}

/* ── LA COULEUR — CELLE DU STUDIO, ET LA RAMPE DE LA TOILE ────────────────
   Une dalle d'Aura est une dalle de Toile : elle prend UNE couleur de la
   palette choisie au Studio, et UNE marche de ton. Le moteur en a cinq
   (TON = 1 · 0,76 · 1,24 · 0,88 · 1,12) ; on les reprend telles quelles.
   ⚑ ET LA LUMIERE NE FAIT PAS UN DEGRADE : elle fait MONTER la dalle d'une
   marche dans sa propre rampe. Un aplat franc, jamais un fondu — c'est la
   regle de la Toile, et c'est aussi ce qui evite les rayures paralleles pour
   lesquelles l'iridescence a ete refusee deux fois. */
function r2h(c){var r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),
  h,s,l=(mx+mn)/2,d=mx-mn;
  if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);
    h=mx===r?((g-b)/d+(g<b?6:0)):mx===g?((b-r)/d+2):((r-g)/d+4);h/=6;}
  return [h,s,l];}
function h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;
    if(t<1/6)return p+(q-p)*6*t; if(t<1/2)return q;
    if(t<2/3)return p+(q-p)*(2/3-t)*6; return p;}
  if(s===0){var v=l*255;return [v,v,v];}
  var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;
  return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
/* la clarte bouge, LA TEINTE ET LA SATURATION NE BOUGENT JAMAIS : c'est ce qui
   fait qu'une palette reste elle-meme sur un volume. */
function marche(c,dl){var t=r2h(c);
  return h2r(t[0], t[1], Math.max(0.045,Math.min(0.965,t[2]+dl)));}
function mix(a,b,t){return [a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t];}
var CREME=[244,238,225];
/* ⚑ VINGT MARCHES, PLUS SEPT — et c'est ce qui enleve les bandes.
   « Un aplat franc, jamais un degrade » est la regle de LA COULEUR D'UNE DALLE.
   Je l'appliquais aussi a L'OMBRAGE DU VOLUME : la lumiere tombait sur sept
   marches, et la sphere se terrassait en BANDES DIAGONALES — un defaut de
   quantification, pas un parti pris. Une dalle garde sa teinte ; c'est son
   eclairement qui doit etre continu. Vingt marches, l'oeil ne les separe plus. */
var MARCHES=20;
function rampeCouleur(base){
  var out=[], k;
  for(k=0;k<MARCHES-2;k++) out.push(marche(base, -0.30+0.60*k/(MARCHES-3)));
  out.push(mix(marche(base,0.32),CREME,0.34));
  out.push(mix(marche(base,0.36),CREME,0.62));            /* le reflet */
  return out;
}
function pack(c){return (((c[2]|0)&255)<<16 | ((c[1]|0)&255)<<8 | ((c[0]|0)&255))>>>0;}

/* ── LE RELIEF — DE SURFACE, ET D'AMPLITUDE VARIABLE ──────────────────────
   Deux acquis, et le second est plus fort que le premier :
   1 · toutes les frequences >= 8 SUR LES TROIS AXES. « Haute frequence » sur
       un seul axe, c'est une enveloppe a l'echelle de la boule : des lobes
       verticaux, une courge. C'etait le defaut des cinq series ratees.
   2 · le deplacement radial est AMORTI AU LIMBE (face^0,6, nul la ou la
       normale est perpendiculaire au regard). La silhouette est alors un
       CERCLE EXACT quelle que soit l'amplitude.
   ⚑ ET L'AMPLITUDE VARIE : des zones lisses, des zones froissees. L'enveloppe
   est BASSE frequence — et elle ne deforme pas le contour pour autant, parce
   qu'elle multiplie un terme HAUTE frequence de moyenne nulle. C'est le
   produit qui compte, pas les facteurs. */
function phi(x,y,z,R){
  var s=0;
  for(var i=0;i<R.length;i++){var h=R[i];
    s+=h[0]*Math.sin(h[1]*x+h[4])*Math.sin(h[2]*y+h[5])*Math.cos(h[3]*z+h[6]);}
  return s;
}
function enveloppe(x,y,z,E){
  var v=0.5+0.5*Math.sin(E[2]*x+E[5])*Math.cos(E[3]*y+E[6])*Math.sin(E[4]*z+E[7]);
  return E[0]+E[1]*Math.pow(v,E[8]||1.5);
}

/* ── L'EMPREINTE — LA PULPE, PROUVEE EN PIXELS LE 6 SEPTEMBRE ─────────────
   Ce n'est plus une cloche. Une pulpe ADHERE et s'aplatit :
     s <= 1  LE PLATEAU. La surface epouse le doigt, elle devient PLANE, et
             RIEN N'Y GLISSE. Mesure : le coeur reste intact a +2 a +4 % de
             l'amplitude, la cloche y perdait 76 a 80 %.
     s  > 1  LA PAROI (raide) puis LE BOURRELET, la matiere chassee. Et c'est
             LA, et seulement la, que ca glisse vers l'exterieur.
   ET LE CONTACT GRANDIT AVEC LA PRESSION — Hertz : a = amax p^(1/3),
   d = dmax p^(2/3). Mesure : 5,0 -> 11,0 -> 14,0 px, x2,80. La cloche : zero
   a toutes les pressions, elle n'a pas de zone de contact.
   ⚠ Deux bugs payes : l'axe du doigt doit etre TANGENT (sinon la tache est un
   cylindre qui traverse la boule et ressort de l'autre cote), et le plan du
   plateau est perpendiculaire A LA NORMALE, jamais a l'axe. */
function prepEmp(E, cl,sl,ct,st){
  var inv=function(v){var zp=-v[1]*st+v[2]*ct, y=v[1]*ct+v[2]*st;
    return [v[0]*cl-zp*sl, y, v[0]*sl+zp*cl];};
  var n=function(v){var m=Math.hypot(v[0],v[1],v[2])||1;return [v[0]/m,v[1]/m,v[2]/m];};
  var o={}; for(var k in E) o[k]=E[k];
  o.c=n(inv(E.c));
  var a0=n(inv(E.ax)), dp=a0[0]*o.c[0]+a0[1]*o.c[1]+a0[2]*o.c[2];
  o.ax=n([a0[0]-dp*o.c[0], a0[1]-dp*o.c[1], a0[2]-dp*o.c[2]]);
  /* la lumiere, ramenee dans le repere de l'objet : elle sert a ombrer
     l'interieur du creux — sans ombre portee, un trou reste un disque */
  /* ⚠ SEULE LA PART TANGENTE DE LA LUMIERE CREUSE UNE OMBRE PORTEE, et il
     faut la NORMALISER. Au point touche, la lumiere etait radiale a 88 % : sa
     part tangente valait 0,47, l'ombre ne separait le fond qu'entre 0,46 et
     0,81, et le creux ne se lisait pas comme un creux. Ramenee a une
     direction unitaire, elle donne le contraste entier ou que le doigt se
     pose — c'est une ombre portee, pas une loi d'eclairage. */
  var Lo=inv(E.Lv||[-0.40,-0.62,0.675]);
  var lr=Lo[0]*o.c[0]+Lo[1]*o.c[1]+Lo[2]*o.c[2];
  o.L=n([Lo[0]-lr*o.c[0], Lo[1]-lr*o.c[1], Lo[2]-lr*o.c[2]]);
  o.aC=E.cloche? E.a : E.a*Math.pow(E.p,1/3);   /* la cloche ne grandit pas */
  o.bC=o.aC*(E.el||0.62);
  o.d =E.dmax*Math.pow(E.p,2/3);
  return o;
}
function contact(E,x,y,z){
  var vx=x-E.c[0], vy=y-E.c[1], vz=z-E.c[2];
  var vr=vx*E.c[0]+vy*E.c[1]+vz*E.c[2];
  if(vr<-0.55) return null;
  vx-=vr*E.c[0]; vy-=vr*E.c[1]; vz-=vr*E.c[2];
  var du=vx*E.ax[0]+vy*E.ax[1]+vz*E.ax[2];
  var wx=vx-du*E.ax[0], wy=vy-du*E.ax[1], wz=vz-du*E.ax[2];
  var dv=Math.sqrt(wx*wx+wy*wy+wz*wz);
  du-=(E.biais||0)*E.aC;
  var s=Math.sqrt((du/E.aC)*(du/E.aC)+(dv/E.bC)*(dv/E.bC));
  /* ⚑ LA PERTURBATION DOIT S'ANNULER POUR DE BON, ET LA QUEUE DU BOURRELET
     NE S'ANNULAIT JAMAIS. (u/ub)exp(1-u/ub) vaut encore 18 % de son pic a
     u = 1,4 ; avec un rayon de contact de 0,36 rad, ca portait jusqu'a
     SOIXANTE DEGRES du doigt. Resultat mesure a l'ecran : la boule entiere se
     soulevait de 3 % et glissait de 7 % — l'image sous le pouce ne ressemblait
     plus du tout a l'image au repos, et ce n'etait pas l'empreinte, c'etait
     un effet global. On borne, et la borne est FRANCHE. */
  if(s>3.0) return null;
  var ex=du*E.ax[0]+wx, ey=du*E.ax[1]+wy, ez=du*E.ax[2]+wz;
  var m=Math.hypot(ex,ey,ez)||1; ex/=m; ey/=m; ez/=m;
  /* LE TEMOIN : l'ANCIENNE loi, une cloche gaussienne. Il ne sert qu'a la
     mesure — c'est contre lui que le plateau se prouve. Ni fond plat, ni bord
     franc, ni croissance du contact avec la pression. */
  if(E.cloche){
    var e2=s*s, gu=(1-1.9*e2)*Math.exp(-1.6*e2);
    return {s:s,w:-E.d*gu,gl:(E.U||0.5)*E.d*Math.max(0,gu)*0.7,plat:0,
            dx:ex,dy:ey,dz:ez,ombre:0};
  }
  if(s<=1){
    /* L'OMBRE DANS LE CREUX : le bord du cote de la lumiere porte son ombre
       sur le fond. Sans elle, le plateau est un disque pose, pas un trou. */
    var lp=ex*E.L[0]+ey*E.L[1]+ez*E.L[2];
    return {s:s,w:-E.d,gl:0,plat:1,dx:ex,dy:ey,dz:ez,ombre:lp};
  }
  /* ⚑ LE MUR N'EST PAS UN COUTEAU : C'EST UNE CUVETTE LARGE.
     Je faisais remonter la surface en exp(-u/0,085) : le creux tombait a zero
     en un cinquantieme de radian, et l'empreinte se reduisait a un petit
     disque terne. La carte des zones l'a montre — 1 435 points de plateau,
     545 de paroi, et une queue de bourrelet plus grande que tout le reste.
     La solution exacte d'un POINCON PLAT sur un solide mou est connue :
     hors du contact, l'enfoncement vaut (2/pi) asin(a/r). Elle vaut 1 au bord
     — la continuite est assuree —, 0,46 a une fois et demie le rayon, 0,33 a
     deux fois. C'est une CUVETTE, et c'est elle qui fait « la matiere cede ».
     Le bord garde sa cassure de pente : la derivee y est infinie. Le fond
     reste plat, donc la preuve en pixels du 6 septembre tient toujours. */
  var u=s-1, ub=E.ub||0.35;
  var cuv=0.6366197724*Math.asin(1/s);
  var fin=1-(s-1)/2.0; if(fin<0)fin=0; fin*=fin;   /* la fenetre qui ferme */
  var bosse=(u/ub)*Math.exp(1-u/ub)*fin;
  var w=-E.d*cuv*fin + (E.B||0.30)*E.d*bosse;
  return {s:s,w:w,gl:(E.U||1.6)*E.d*bosse,plat:0,dx:ex,dy:ey,dz:ez,ombre:0};
}
/* le repli au MIROIR : ce qui deborde du rectangle inscrit revient dedans
   sans couture franche (un simple modulo laisserait un saut de motif). */
function mir(v,n){ var p=2*n; v=((v%p)+p)%p; return v<n?v:p-1-v; }
function hh(i){var x=(i*2654435761)>>>0; x^=x>>>15; x=(x*2246822519)>>>0;
  x^=x>>>13; x=(x*3266489917)>>>0; x^=x>>>16; return (x>>>8)/16777216;}
/* ⚑ TROIS TABLES, ET ELLES VALENT DES MILLISECONDES.
   Le banc a fini par montrer ou part le temps : sur 27,4 ms a 90 000 poils, le
   VERSEMENT n'en coute que 3,3 et la boucle de projection 0,7. Les 23,4 autres
   sont dans la boucle de deformation — qui appelait `Math.pow` et `Math.hypot`
   PAR POINT. `Math.hypot` fait une mise a l'echelle pour eviter les
   debordements : on n'en a aucun besoin sur des coordonnees entre -1 et 1, et
   `Math.sqrt` va cinq a dix fois plus vite. `Math.pow(x,0,6)` se tabule. */
function nrm3(x,y,z){ return Math.sqrt(x*x+y*y+z*z); }
/* ⚑ L'ANGLE D'UN POIL SANS Math.atan2.
   Il y en avait UN PAR POIL, et atan2 coute cinquante a cent nanosecondes —
   plus que tout le reste de la boucle reunie. On n'a besoin que d'un secteur
   sur vingt-quatre : le rapport du petit cote sur le grand donne l'angle dans
   le premier huitieme, une table de 256 entrees le convertit, et l'octant se
   rattrape par des comparaisons de signe. Aucune division par une racine. */
var _ATN=new Float32Array(257);
(function(){ for(var i=0;i<=256;i++) _ATN[i]=Math.atan(i/256); })();
var TAU_=6.283185307179586;
function secteur(x,y,n){
  var ax=x<0?-x:x, ay=y<0?-y:y, a;
  if(ax>=ay) a=_ATN[(ay/(ax||1e-9)*256)|0];
  else       a=1.5707963268-_ATN[(ax/(ay||1e-9)*256)|0];
  if(x<0) a=3.1415926536-a;
  if(y<0) a=TAU_-a;
  var s=(a/TAU_*n)|0; return s>=n?n-1:(s<0?0:s);
}
var _P06=new Float32Array(1025), _P074=new Float32Array(1025), _P34=new Float32Array(1025);
(function(){ for(var i=0;i<=1024;i++){ var t=i/1024;
  _P06[i]=Math.pow(t,0.60); _P074[i]=Math.pow(t,0.74); _P34[i]=Math.pow(t,3.40); } })();
function p06(t){ return t<=0?0:(t>=1?1:_P06[(t*1024)|0]); }
function p074(t){ return t<=0?0:(t>=1?1:_P074[(t*1024)|0]); }
function p34(t){ return t<=0?0:(t>=1?1:_P34[(t*1024)|0]); }
function lisse(a,b,v){var t=(v-a)/(b-a); if(t<0)t=0; if(t>1)t=1; return t*t*(3-2*t);}
