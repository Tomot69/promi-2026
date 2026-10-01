
/* ════════════════════════════════════════════════════════════════════════════
   lot-AURA-PELOTE-MOTEUR — le moteur de la Pelote (velours), porte tel quel.
   Source : sauvegardes/pelote-velours/ — les cinq fichiers, dans l'ordre de la
   planche : _m_base.js, _v_moteur.js, _v_iles.js, _v_semis.js, _v_peint.js.
   ⚑ ENFERME DANS UNE FONCTION. Ces fichiers definissent des noms generiques
   (D, TAU, mix, hh, fr, peint, verse...) : poses tels quels a la racine d'app.html
   ils ecraseraient des globales de l'app. Rien ne sort, sauf window.PeloteMoteur.
   ⚑ UNE SEULE RETOUCHE, dans batIles : la source de dalle (voir le commentaire
   « PORTAGE DANS L'APP »). Le moteur de la Toile n'est PAS touche (§9).
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
/* ──────── _m_base.js  (md5 source 51280ead7c67d921d9e3231b8ba03385) ──────── */
/* ════════════════════════════════════════════════════════════════════════════
   LA MÉMOIRE DE LA MAIN — les fondations communes aux trois planches.

   ⚑ CE QUI EST NOUVEAU, ET QUI VIENT DE DEUX ETUDES INDEPENDANTES :
   un objet numerique QUI SE SOUVIENT DES GESTES DE SON PROPRIETAIRE. La patine
   est l'organe, pas l'ornement. Avec trois conditions posees par Tom :
     1 · LA FORME RESTE BELLE. Une empreinte ne rend jamais l'objet difforme :
         on doit pouvoir tracer un cercle parfait autour, quelle que soit
         l'histoire des gestes.
     2 · LA MATIERE RESISTE. Ni mou, ni slime, ni caoutchouc — quelque chose
         entre la ceramique crue, la cire minerale et la pierre tendre. Une
         matiere qui n'existe pas.
     3 · CA REVIENT. La deformation est reelle sur le moment, puis la forme
         spherique revient — lentement. CE QUI RESTE N'EST PAS UN CREUX :
         c'est une trace DANS la matiere — un lustre, un grain, une chroma qui
         a monte.

   ⚠ TROIS INTERDITS QUI FONT LE « MEGA CHEAP », ET ON NE LES TOUCHE PAS :
     aucun degrade · aucune ombre portee · aucune tache speculaire.
   Toute la lumiere passe donc par LE GRAIN : chaque marque est un aplat franc,
   et c'est le NOMBRE de marques et leur marche de ton qui font le volume.
   ════════════════════════════════════════════════════════════════════════════ */

/* ── LA PALETTE, PILOTEE EN LUMINANCE PERCUE ──────────────────────────────
   Acquis paye au lot precedent : le bleu ne pese que 11 % dans la luminance
   (0,299 R + 0,587 V + 0,114 B). Regler une CLARTE HSL sur une teinte
   bleu-violet ne veut rien dire a l'oeil. On resout en luminance. */
function m_r2h(c){var r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),
  h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);
  h=mx===r?((g-b)/d+(g<b?6:0)):mx===g?((b-r)/d+2):((r-g)/d+4);h/=6;}return [h,s,l];}
function m_h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;
  if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}
  if(s===0){var v=l*255;return [v,v,v];}
  var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;
  return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
function m_lum(c){return 0.299*c[0]+0.587*c[1]+0.114*c[2];}
function m_versLum(h,s,cible){
  var sat=s,c;
  for(var e=0;e<7;e++){
    var lo=0.02,hi=0.985;
    for(var i=0;i<22;i++){var m=(lo+hi)/2;c=m_h2r(h,sat,m);
      if(m_lum(c)<cible)lo=m;else hi=m;}
    c=m_h2r(h,sat,(lo+hi)/2);
    if(Math.abs(m_lum(c)-cible)<3)return c;
    sat*=0.80;
  }
  return c;
}

/* ── LE SEMIS D'UNE SPHERE — reseau de Fibonacci, perturbe ───────────────── */
function m_h(i){var x=(i*2654435761)>>>0;x^=x>>>15;x=(x*2246822519)>>>0;
  x^=x>>>13;x=(x*3266489917)>>>0;x^=x>>>16;return (x>>>8)/16777216;}
function m_semis(N){
  var P=new Float32Array(N*3), GOLD=2.399963229728653;
  var pas=Math.sqrt(12.566370614/N);
  for(var i=0;i<N;i++){
    var y=1-2*(i+0.5)/N, r=Math.sqrt(Math.max(0,1-y*y)), a=i*GOLD;
    var x=Math.cos(a)*r, z=Math.sin(a)*r;
    x+=(m_h(i*3+1)-0.5)*pas*0.96; y+=(m_h(i*5+2)-0.5)*pas*0.96;
    z+=(m_h(i*7+4)-0.5)*pas*0.96;
    var m=Math.hypot(x,y,z)||1;
    P[i*3]=x/m; P[i*3+1]=y/m; P[i*3+2]=z/m;
  }
  return P;
}

/* ── LA VEINE DE LA MATIERE — le lit mineral, pas un peignage ────────────
   Une pierre tendre a un LIT : des plans de depot, tres basse frequence. Ce
   n'est pas une fourrure peignee ; c'est ce qui donne a la matiere son sens
   sans qu'elle ait l'air d'un pelage. */
function m_veine(x,y,z){
  var e=0.04;
  function f(a,b,c){return Math.sin(1.7*a+0.4)*Math.cos(1.3*b-0.9)
                        +0.55*Math.sin(2.1*c+1.7)*Math.cos(1.9*a+0.2);}
  var gx=f(x+e,y,z)-f(x-e,y,z), gy=f(x,y+e,z)-f(x,y-e,z), gz=f(x,y,z+e)-f(x,y,z-e);
  var d=gx*x+gy*y+gz*z; gx-=d*x; gy-=d*y; gz-=d*z;
  var m=Math.hypot(gx,gy,gz)||1;
  return [gx/m,gy/m,gz/m];
}

/* ════════════════════════════════════════════════════════════════════════════
   LES GESTES — ce que la main a laissé.
   Un geste est un ARC sur la sphere : un depart, une direction, une longueur.
   Il n'y a AUCUN creux : le geste ne deforme pas, il POLIT. On garde donc, par
   point, une part de « poli » entre 0 et 1 — et c'est elle qui fera monter la
   chroma, affiner le grain et coucher la marque.
   ⚠ Determinisme : meme Pelote, memes gestes. Rien n'est tire au hasard.
   ════════════════════════════════════════════════════════════════════════════ */
function m_gestes(n,graine){
  var G=[], k;
  for(k=0;k<n;k++){
    var s=graine+k*97;
    /* un depart quelconque sur la sphere */
    var u=m_h(s*3+1)*2-1, ph=m_h(s*5+2)*6.283185, r=Math.sqrt(Math.max(0,1-u*u));
    var a=[Math.cos(ph)*r, u, Math.sin(ph)*r];
    /* une direction tangente */
    var hx=0,hy=1,hz=0; if(Math.abs(a[1])>0.9){hx=1;hy=0;}
    var e1=[a[1]*hz-a[2]*hy, a[2]*hx-a[0]*hz, a[0]*hy-a[1]*hx];
    var m1=Math.hypot(e1[0],e1[1],e1[2])||1; e1=[e1[0]/m1,e1[1]/m1,e1[2]/m1];
    var e2=[a[1]*e1[2]-a[2]*e1[1], a[2]*e1[0]-a[0]*e1[2], a[0]*e1[1]-a[1]*e1[0]];
    var an=m_h(s*7+3)*6.283185, ca=Math.cos(an), sa=Math.sin(an);
    var d=[e1[0]*ca+e2[0]*sa, e1[1]*ca+e2[1]*sa, e1[2]*ca+e2[2]*sa];
    G.push({a:a, d:d,
            L:0.45+m_h(s*11+5)*1.05,          /* la longueur de la caresse */
            w:0.055+m_h(s*13+7)*0.075,        /* sa largeur */
            f:0.45+m_h(s*17+9)*0.55});        /* combien elle a poli */
  }
  return G;
}
/* la part de poli en un point : distance a l'arc le plus proche */
function m_poli(G,x,y,z){
  var best=0;
  for(var k=0;k<G.length;k++){
    var g=G[k];
    /* projection sur le grand cercle porte par (a,d) */
    var t=Math.atan2(x*g.d[0]+y*g.d[1]+z*g.d[2], x*g.a[0]+y*g.a[1]+z*g.a[2]);
    if(t<0) t=0; else if(t>g.L) t=g.L;       /* borne : c'est un ARC, pas un cercle */
    var ct=Math.cos(t), st=Math.sin(t);
    var px=g.a[0]*ct+g.d[0]*st, py=g.a[1]*ct+g.d[1]*st, pz=g.a[2]*ct+g.d[2]*st;
    var dp=x*px+y*py+z*pz; if(dp>1)dp=1; else if(dp<-1)dp=-1;
    var an=Math.acos(dp);
    if(an<g.w){
      var v=1-an/g.w; v=v*v*(3-2*v);          /* un bord doux, pas un ruban */
      v*=g.f;
      if(v>best) best=v;
    }
  }
  return best;
}

/* ──────── _v_moteur.js  (md5 source 48acf6ea7a0b532d4f180f30cd4fc120) ──────── */
/* ════════════════════════════════════════════════════════════════════════════
   L'PELOTE — LE PAVAGE HABILLE.  Le moteur.
   Technique acquise : des tampons pre-rendus, verses dans un tampon de pixels,
   un putImageData. Aucun drawImage par grain (hors budget d'un facteur trois).
   ⚑ NOUVEAU ICI : le tampon ne porte plus que L'ALPHA. La couleur se compose au
   versement, par un OR. Sans ca, 4 couleurs x 6 marches x 3 tailles x 8
   orientations x 6 niveaux faisaient 3 456 tampons ; il y en a 144.
   ════════════════════════════════════════════════════════════════════════════ */
var D=2, TAU=6.283185307179586;

/* ⚑ 22 SEPTEMBRE 2026 — POURQUOI ON VOYAIT LA PEAU ENTRE LES POILS. C'EST ICI.
   `atlasAlpha` dessine le poil UNE FOIS en blanc plein, puis en tire NIV tampons, un par
   NIVEAU D'ÉCLAIREMENT, chacun multiplié par `mul = a0 + (a1−a0)·q^1,40` — de 0,15 (le poil
   à l'ombre) à 0,78 (le poil en pleine lumière).
   LE SEUIL ÉTAIT APPLIQUÉ APRÈS LA MULTIPLICATION : `al = (source × mul)|0 ; if(al>4)`.
   Conséquence, et c'est tout le défaut : à mul 0,15, TOUT PIXEL SOURCE SOUS ALPHA 27 EST
   JETÉ. Or ce sont exactement les bords anticrénelés du brin. **Un poil à l'ombre perdait
   donc sa silhouette** — il ne restait qu'un noyau dur et maigre, et la peau passait entre.
   Les poils en lumière, eux, gardaient tout : d'où des « écarts blancs » qui suivaient
   l'éclairement, et qu'aucun réglage de nombre ou d'épaisseur ne pouvait combler (mesuré :
   les trois l'aggravaient, 27,9 % → 29,3 · 30,8 · 53,2 %).
   LA CORRECTION : le seuil se juge sur LA SOURCE, pas sur le produit. Un poil a donc LA MÊME
   SILHOUETTE à tous les niveaux ; seule son opacité change. C'est ce que le mot « niveau
   d'éclairement » voulait dire depuis le début. */
function fabTampon(dat,src,x1,y1,w,h,ox,oy,mul){
  var off=[], alp=[];
  for(var y=0;y<h;y++)for(var x=0;x<w;x++){
    var a=dat[((y1+y)*src+(x1+x))*4+3];
    if(a<=4) continue;                      /* le seuil porte sur LA SOURCE */
    var al=(a*mul)|0; if(al<1) al=1;        /* jamais zéro : le bord existe, même sombre */
    off.push([y-oy,x-ox]); alp.push(al>255?255:al);
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
    /* ⚑ PLUS NET. A 0,86 d'extinction, la pointe disparaissait avant d'arriver
       et le pelage sortait BRUMEUX — on lisait un voile, pas des poils. Un poil
       de chat ou de lapin garde sa matiere presque jusqu'au bout : il s'affine
       beaucoup, il ne s'efface pas. On inverse le partage — peu d'alpha, plus
       d'affinement. */
    /* ⚑ POURQUOI LA BOULE RESTE SOMBRE, ET CE N'EST NI LA RAMPE NI LA DENSITE.
       Mesure : la couverture est de 100 %, mais un pixel couvert rend 44 a 77
       la ou sa couleur vaut 132 a 190. La difference est L'ALPHA : chaque brin
       est semi-transparent et le fond est NOIR, donc chaque pixel rend
       couleur x alpha. On remonte donc l'alpha du brin — c'est le seul levier
       qui reste apres la rampe et la densite. */
    g.globalAlpha=(1-t0*0.30);                /* la pointe reste presente */
    g.lineWidth=ep*(1-t0*0.88);               /* et c'est elle qui s'affine */
    g.beginPath(); g.moveTo(ax,ay); g.lineTo(bx,by); g.stroke();
  }
}
/* ⚑ SIX BRINS, PLUS FINS — « ça ne paraît pas assez doux ».
   La douceur d'une fourrure ne vient pas de sa longueur, elle vient de la
   FINESSE et du NOMBRE : c'est le recouvrement de brins qu'on ne distingue
   plus qui fait le soyeux. A quatre brins epais on lit encore chaque trait.
   Le cout est faible : le banc dit qu'un poil coute 0,108 microseconde dont
   seulement 0,042 de pixels, et deux brins de plus sur la MEME racine ne
   paient que leurs pixels — et ils en paient moins, puisqu'ils sont plus fins. */
/* ⚑ ET PLUS SOYEUX : LES BRINS SE SERRENT.
   Une fourrure de chat ou de lapin est FINE, DENSE et PARALLELE — c'est
   l'alignement qui fait le soyeux. A ±0,44 d'ecart les brins partaient en
   etoile : ca fait une brosse, pas un pelage. On resserre a ±0,20, on allonge,
   et on garde des longueurs proches les unes des autres. */
var TOUFFE=[[[0,1.00,0.34],[0.17,0.96,0.14],[-0.15,0.94,0.48],[0.08,0.90,-0.14],
             [-0.08,0.98,0.04],[0.21,0.92,0.30]],
            [[0,0.98,0.22],[-0.19,0.94,0.44],[0.16,0.92,-0.06],[0.04,0.90,0.56],
             [0.10,1.00,0.10],[-0.22,0.90,0.26]],
            [[0,1.02,0.42],[0.13,0.94,-0.18],[-0.11,0.96,0.18],[0.20,0.90,0.36],
             [-0.05,1.00,0.52],[0.24,0.92,0.02]]];
function GRAIN_POIL(g,e,v){
  /* ⚑ UNE MECHE SE COURBE, UN BRIN RESTE DROIT. 1,75 de long et une courbure
     modeste donnaient un duvet plante ; on allonge a 2,05 et on force la
     courbure d'un quart : les pointes se rabattent, se croisent, et c'est ce
     croisement-la qui fait « mou » a l'oeil. */
  /* ⚑ UN BRIN D'UN DEMI-PIXEL N'EST PAS FIN, IL EST CRENELE.
     A 0,50 px d'epaisseur et a pleine opacite, chaque meche tombe entre deux
     pixels : elle sort en marches, et la matiere se lit en GRAINS durs — c'est
     la delicatesse perdue. La finesse d'un velours ne vient pas de brins plus
     maigres, elle vient de brins QUI SE FONDENT : un peu plus larges, un peu
     moins opaques, et qui se recouvrent. On elargit d'un demi-pixel et on
     baisse l'opacite du tampon (voir `atlasPour`) : meme densite, meme sens,
     mais un fondu au lieu d'un crenelage. */
  /* ⚑ 21 SEPTEMBRE 2026 — « LA SPHÈRE N'EST PAS ASSEZ VELUE, ON VOIT DES TROUS » (Tom).
     LE DÉFAUT EST MESURÉ, ET IL EST RÉEL : à la loupe, vue figée, sans les îles, **27,9 % de
     la surface du cœur est encore à la couleur de la PEAU** (peau L* 46,1, poil L* 64,1).
     ⚠ MAIS LES TROIS LEVIERS ÉVIDENTS LE RENDENT PIRE, ET C'EST MESURÉ AUSSI :
         épaisseur 0,118 → 0,150   peau découverte 27,9 % → 30,8 %
         épaisseur 0,118 → 0,178                          → 32,3 %
         nombre   110 000 → 125 000                       → 29,3 %   (et +1,3 ms)
         opacité  0,15-0,78 → 0,32-0,86                   → 53,2 %   (L* moyen 55,1 → 48,9)
     Le peintre NORMALISE : élargir un brin baisse l'opacité de son tampon (c'est écrit plus
     haut, et c'est ce qui évite le crénelage) ; en ajouter répartit la même lumière sur plus
     de brins ; monter l'opacité du bas de rampe assombrit toute la matière.
     RIEN N'EST TOUCHÉ. Le défaut reste ouvert : il demande de comprendre la normalisation de
     `atlasAlpha`, pas d'essayer un quatrième réglage au jugé (§7). */
  var T=TOUFFE[(v||0)%TOUFFE.length], ep=Math.max(0.82,e*0.118);
  g.lineCap='round';
  for(var k=0;k<T.length;k++){
    g.save(); g.rotate(T[k][0]);
    unPoil(g, e*2.05*T[k][1], ep*(0.72+0.5*T[k][1]), e*T[k][2]*1.26, 6);
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
var CREME=[247,240,222];
/* ⚑ VINGT MARCHES, PLUS SEPT — et c'est ce qui enleve les bandes.
   « Un aplat franc, jamais un degrade » est la regle de LA COULEUR D'UNE DALLE.
   Je l'appliquais aussi a L'OMBRAGE DU VOLUME : la lumiere tombait sur sept
   marches, et la sphere se terrassait en BANDES DIAGONALES — un defaut de
   quantification, pas un parti pris. Une dalle garde sa teinte ; c'est son
   eclairement qui doit etre continu. Vingt marches, l'oeil ne les separe plus. */
var MARCHES=20;
/* ⚑ LE GRADING — ce qui separe un RENDU d'une PHOTOGRAPHIE.
   Aucun objet reel n'est eclaire par une lumiere neutre : la cle est chaude,
   l'ombre est ouverte par un ciel froid. L'oeil lit ce couple comme « vrai »
   avant meme de nommer la forme. On le cuit donc dans la rampe — cout nul au
   rendu, puisque la rampe est une table.
   ⚠ La teinte de la palette ne se perd pas : on decale la BALANCE, pas la
   couleur. Marche basse -> +bleu/-rouge de `f`; marche haute -> l'inverse. */
function rampeGradee(base,f){
  var out=rampeCouleur(base), n=out.length;
  for(var k=0;k<n;k++){
    var t=k/(n-1)*2-1;                       /* -1 l'ombre, +1 la lumiere */
    var c=out[k];
    var r=c[0]+f*t*22, g=c[1]+f*t*4, b=c[2]-f*t*26;
    out[k]=[r<0?0:r>255?255:r, g<0?0:g>255?255:g, b<0?0:b>255?255:b];
  }
  return out;
}
/* ⚑ UNE RAMPE POUR UNE MATIERE ECLAIREE, PAS POUR UNE DALLE.
   `rampeCouleur` ne joue que sur la CLARTE HSL. Sur un violet sature, baisser
   la clarte ne donne pas un violet profond : ca donne un BLEU ELECTRIQUE — le
   bleu garde toute sa saturation en descendant, et c'est lui qu'on voit. Le
   bas-droite de la boule sortait donc en bleu vif la ou il fallait de l'ombre.
   Une matiere dans l'ombre, elle, va vers LA COULEUR DU LIEU : ici l'encre du
   fond. On melange donc vers l'encre en descendant, et on monte en clarte sans
   jamais atteindre la creme (deux marches de reflet en moins : il n'y a pas de
   reflet sur un velours). */
var ENCRE_F=[32,25,8];
function rampeVelours(base){
  var out=[], k, n=MARCHES;
  for(k=0;k<n;k++){
    var t=k/(n-1);                       /* 0 = l'ombre, 1 = la lumiere */
    if(t<0.5){
      var u=1-t/0.5;                     /* 1 tout en bas */
      /* ⚠ ET LE BAS DE LA RAMPE NE DOIT PAS REJOINDRE L'ENCRE. A 0,62 vers le
         fond, le cote sombre de la boule DESCENDAIT SOUS LE SEUIL DE LECTURE
         de sa propre silhouette : les 360 rayons s'arretaient vingt pixels
         trop tot en bas a droite (rayon min 254 pour une moyenne de 274).
         Une boule dont le bord se dissout dans le fond n'a plus de contour, et
         le contour est ce qui la fait exister. On garde le glissement vers
         l'encre — c'est lui qui evite le bleu electrique — mais on s'arrete
         avant de la toucher. */
      out.push(mix(marche(base,-0.10*u), ENCRE_F, 0.44*u*u));
    } else {
      /* ⚑ EN HAUT, LA CHROMA MONTE PLUS QUE LA CLARTE.
         A +0,30 de clarte HSL, le violet montait vers le BLANC : le haut de la
         boule sortait gris-lilas, delave, pendant qu'on demandait un violet
         clair. Monter la clarte desature mecaniquement — c'est le meme mur de
         colorimetrie que le bas de la rampe, pris par l'autre bout. On monte
         donc la clarte de moitie moins, et on RESSATURE : le haut reste
         violet, il est simplement plus lumineux. */
      var v=(t-0.5)/0.5, _t=r2h(base);
      out.push(h2r(_t[0], Math.min(0.98, _t[1]*(1+0.34*v)),
                   Math.max(0.045, Math.min(0.965, _t[2]+0.225*v))));
    }
  }
  return out;
}
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
/* ⚑ UN PRODUIT DE SINUS EST UN RESEAU — c'etait ca, « l'eclairage en croisillon ».
   `sin(fx·x)·sin(fy·y)·cos(fz·z)` est SEPARABLE : ses zeros sont des plans
   x = cte, y = cte, z = cte. La surface porte donc une GRILLE, et des qu'on
   l'eclaire on voit un croisillon en travers de la boule. Ce n'etait ni la
   lumiere ni le grain : c'etait la forme meme du relief.
   ⚑ LA PARADE : UNE SOMME D'ONDES PLANES, dans des directions quelconques.
   Aucune n'est alignee sur un axe, aucune periode n'est commune : le relief
   devient ISOTROPE et il ne se repete pas. Et la regle de l'audit — « toutes
   les frequences >= 8 SUR LES TROIS AXES », qui evitait une enveloppe basse
   frequence sur un seul axe, donc une courge — reste tenue : chaque onde a un
   vecteur d'onde de norme >= 9 dans une direction oblique. */
function phi(x,y,z,R){
  var s=0;
  for(var i=0;i<R.length;i++){var h=R[i];
    s+=h[0]*Math.sin(h[1]*x+h[2]*y+h[3]*z+h[4]);}
  return s;
}
/* l'enveloppe module l'AMPLITUDE : elle aussi doit etre une somme, sinon elle
   repose son propre reseau, plus grossier, par-dessus le premier. */
function enveloppe(x,y,z,E){
  var v=0.5+0.5*(0.62*Math.sin(E[2]*x+E[3]*y+E[4]*z+E[5])
                +0.38*Math.sin(E[6]*x+E[7]*y+E[8]*z+E[9]));
  return E[0]+E[1]*v;
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

/* ──────── _v_iles.js  (md5 source 6ee03456e9fe74fd39624f76303565c7) ──────── */
/* ════════════════════════════════════════════════════════════════════════════
   LES ÎLES — le renversement du 9 septembre 2026.

   ⚑ CE QUI CHANGE, ET POURQUOI ÇA RÈGLE QUINZE SÉRIES.
   On enroulait la Toile sur la sphere. Or UN PAVAGE PARTITIONNE : sa beaute
   est une fonction de sa densite. A une dalle c'est une sphere unie, a trois
   un quartier d'orange ; il ne devient beau que vers vingt ou trente. Une
   Pelote neuve doit etre belle DES LE PREMIER JOUR — elle est partageable et
   vendable des le premier jour.
   La bonne geometrie est l'inverse : UNE FOURRURE DENSE PAR DEFAUT, ET DES
   ILES DEDANS. L'etat de repos n'est pas le vide, c'est le PEIGNE. Chaque
   Promi est une ile. La densite croit par ACCRETION, jamais par subdivision.

   ⚑ ET CA REGLE LA MOITIE DU PROBLEME DE LUMINANCE : on n'eclairait pas un
   objet trop sombre, ON ECLAIRAIT UNE SURFACE PLATE. Une fourrure a un relief
   qui accroche la lumiere rasante ; une masse unie n'a rien a eclairer.
   ════════════════════════════════════════════════════════════════════════════ */

/* ── LA PALETTE DE L'PELOTE — elle vient du Studio ─────────────────────────
   Le sol n'est pas un gris : c'est la FAMILLE de la palette, profonde et
   saturee. Les iles sont les couleurs de la palette, pleines. C'est ce qui
   lie la Pelote au reste de l'app — et ca ne pose plus le probleme du
   terracotta, puisque c'est une palette et non des couleurs d'etat. */
function _o_r2h(c){var r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),
  h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);
  h=mx===r?((g-b)/d+(g<b?6:0)):mx===g?((b-r)/d+2):((r-g)/d+4);h/=6;}return [h,s,l];}
function _o_h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;
  if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}
  if(s===0){var v=l*255;return [v,v,v];}
  var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;
  return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}

/* ⚑ ON PILOTE LA LUMINANCE PERCUE, PAS LA CLARTE HSL.
   Mesure : le sol sortait a [77, 9, 225] — clarte HSL 0,46, et luminance
   PERCUE 54. Le bleu ne pese que 11 % dans la luminance (0,299 R + 0,587 V +
   0,114 B) : regler une clarte sur une teinte bleu-violet ne veut rien dire a
   l'oeil. C'est pour ca que la boule restait a 36 de moyenne alors que je
   croyais l'avoir montee. On resout donc en luminance, par dichotomie ; si la
   teinte ne peut pas y arriver a saturation pleine, on desature juste ce qu'il
   faut — jamais l'inverse. */
function _o_lum(c){return 0.299*c[0]+0.587*c[1]+0.114*c[2];}
function _o_versLum(h,s,cible){
  var sat=s, c;
  for(var essai=0;essai<7;essai++){
    var lo=0.02, hi=0.985;
    for(var i=0;i<22;i++){
      var m=(lo+hi)/2; c=_o_h2r(h,sat,m);
      if(_o_lum(c)<cible) lo=m; else hi=m;
    }
    c=_o_h2r(h,sat,(lo+hi)/2);
    if(Math.abs(_o_lum(c)-cible)<3) return c;
    sat*=0.80;                       /* la teinte ne peut pas monter si haut */
  }
  return c;
}

function palPelote(pal,opt){
  opt=opt||{};
  var chr=opt.chroma!=null?opt.chroma:1.55;
  var cols=[];
  /* LE SOL : la teinte moyenne de la palette, a la luminance VOULUE. */
  var hs=0, hc=0, ss=0, i;
  for(i=0;i<pal.length;i++){
    var h=_o_r2h(pal[i]);
    hs+=Math.sin(h[0]*6.283185); hc+=Math.cos(h[0]*6.283185); ss+=h[1];
  }
  var hm=Math.atan2(hs,hc)/6.283185; if(hm<0)hm+=1;
  var sm=Math.min(0.92,(ss/pal.length)*chr*0.86);
  var solL=opt.solLum!=null?opt.solLum:96;
  cols.push(_o_versLum(hm, sm, solL));

  /* ⚑ LES DALLES S'ECHELONNENT EN LUMINANCE, ET AUCUNE NE FRISE LE SOL.
     « on reconnait peu les dalles, faut les preciser ou contraster » : deux
     couleurs peuvent avoir des teintes tres differentes et la MEME luminance —
     l'oeil les separe alors mal, surtout sous une fourrure qui moyenne tout.
     On impose donc des luminances etagees, toutes ecartees d'au moins 34 du
     sol. La teinte dit LAQUELLE ; la luminance garantit qu'on la VOIT. */
  var CIB=opt.ileLum||[solL-42, solL+52, solL+88, solL-26];
  for(i=0;i<pal.length;i++){
    var q=_o_r2h(pal[i]);
    var t=Math.max(18,Math.min(232,CIB[i%CIB.length]));
    if(Math.abs(t-solL)<34) t = (t>solL)?solL+34:solL-34;
    cols.push(_o_versLum(q[0], Math.min(0.97,Math.max(0.55,q[1]*chr)), t));
  }
  return cols;
}

/* ── LE SEMIS DES ÎLES — par ACCRÉTION ────────────────────────────────────
   Une ile nouvelle se pose CONTRE les precedentes, comme `plantOne` cherche
   une cellule degagee pres des autres sur la Toile. La grappe grandit ; elle
   ne se subdivise pas. Deterministe : meme Pelote, meme semis. */
function _o_h(i){var x=(i*2654435761)>>>0;x^=x>>>15;x=(x*2246822519)>>>0;
  x^=x>>>13;x=(x*3266489917)>>>0;x^=x>>>16;return (x>>>8)/16777216;}
function _o_nrm(v){var m=Math.hypot(v[0],v[1],v[2])||1;return [v[0]/m,v[1]/m,v[2]/m];}

function semisIles(n,opt){
  opt=opt||{};
  var R=opt.r||0.215;                       /* le rayon angulaire d'une ile */
  /* ⚑ LE MEME PIEGE QUE L'EMPREINTE ET QUE LE FOYER DU SEMIS — TROISIEME FOIS.
     Ecrire « face a nous » en coordonnees d'OBJET ne veut rien dire : la vue
     est tournee de 2,9 radians et inclinee de 0,32. La grappe tombait donc
     DERRIERE la boule, et les etats a une et cinq iles paraissaient identiques
     a l'etat vide. On ecrit la direction dans le repere de la VUE, puis on la
     ramene dans celui de l'objet — exactement comme `semisPavage` le fait pour
     son foyer, et comme l'audit §4 le prescrit. */
  var _cl=Math.cos(2.9), _sl=Math.sin(2.9), _ct=Math.cos(0.32), _st=Math.sin(0.32);
  var _v=opt.centre||[-0.10,-0.14,0.985];
  var _zp=-_v[1]*_st+_v[2]*_ct, _y=_v[1]*_ct+_v[2]*_st;
  var C=[_v[0]*_cl-_zp*_sl, _y, _v[0]*_sl+_zp*_cl];
  var IL=[], k, t;
  /* ⚠ ZERO ILE VEUT DIRE ZERO. La premiere etait posee AVANT la boucle : a
     n = 0 la sphere en portait donc une, et l'etat « vide » etait identique a
     l'etat « une » — mesure, meme luminance a la decimale. */
  if(n<=0) return IL;
  IL.push({c:_o_nrm(C), r:R*(0.92+_o_h(3)*0.22), ci:0, ph:1});
  for(k=1;k<n;k++){
    /* ⚑ LA DALLE QU'ON VIENT DE PLANTER SE POSE FACE A TOI.
       MESURE, et c'est ce qui condamnait le critere 4 : entre cinq et six
       Promi, 0,09 % des pixels bougeaient. Aucune variable globale continue ne
       peut rendre un +1 visible — un trente-quatrieme de quoi que ce soit est
       invisible, c'est de l'arithmetique. Ce qui rend un +1 visible, c'est LA
       DALLE ELLE-MEME ; et une chance sur deux qu'elle tombe sur la face
       cachee, puisque la grappe pousse par accretion vers l'exterieur.
       ⚠ ET ON NE FAIT PAS TOURNER LA BOULE POUR AUTANT. Essaye, mesure,
       regarde : en tournant tout l'objet pour presenter la derniere dalle, les
       cinq precedentes partaient sur le dos — a six Promi on en voyait MOINS
       qu'a cinq. « Rien ne recule jamais » interdit ca.
       La loi de croissance ne bouge pas (l'accretion fait la forme) : parmi
       les positions valides, on garde simplement CELLE QUI REGARDE LE PLUS
       VERS NOUS. Les anciennes ne bougent pas d'un pouce, la nouvelle est
       devant. */
    var pose=null, meil=-2;
    for(t=0;t<220;t++){
      var a=IL[(_o_h(k*17+t*7+1)*IL.length)|0];
      /* une direction tangente au hasard, a un peu plus de deux rayons */
      var hx=0,hy=1,hz=0; if(Math.abs(a.c[1])>0.9){hx=1;hy=0;}
      var e1=_o_nrm([a.c[1]*hz-a.c[2]*hy, a.c[2]*hx-a.c[0]*hz, a.c[0]*hy-a.c[1]*hx]);
      var e2=[a.c[1]*e1[2]-a.c[2]*e1[1], a.c[2]*e1[0]-a.c[0]*e1[2], a.c[0]*e1[1]-a.c[1]*e1[0]];
      var an=_o_h(k*53+t*11+5)*6.283185307;
      var dd=R*(2.02+_o_h(k*29+t*13+2)*0.42);
      var cd=Math.cos(dd), sd=Math.sin(dd), ca=Math.cos(an), sa=Math.sin(an);
      var p=_o_nrm([a.c[0]*cd+(e1[0]*ca+e2[0]*sa)*sd,
                    a.c[1]*cd+(e1[1]*ca+e2[1]*sa)*sd,
                    a.c[2]*cd+(e1[2]*ca+e2[2]*sa)*sd]);
      var ok=true;
      for(var j=0;j<IL.length;j++){
        var dp=p[0]*IL[j].c[0]+p[1]*IL[j].c[1]+p[2]*IL[j].c[2];
        if(dp>1)dp=1; else if(dp<-1)dp=-1;
        if(Math.acos(dp) < R*1.80){ok=false;break;}
      }
      if(ok){
        var face=p[0]*C[0]+p[1]*C[1]+p[2]*C[2];
        if(face>meil){ meil=face; pose=p; }
      }
    }
    if(!pose) break;
    IL.push({c:pose, r:R*(0.88+_o_h(k*97+11)*0.30),
             ci:(_o_h(k*31+7)*4)|0, ph:1+k});
  }
  return IL;
}

/* ── L'APPARTENANCE — un bord ORGANIQUE, jamais un cercle ─────────────────
   Le rayon d'une ile est module par un bruit basse frequence pris dans la
   direction du point : le contour ondule comme une tache de pelage. */
function _o_ondule(px,py,pz,ph){
  return Math.sin(px*7.3+ph*1.7)*Math.cos(py*6.1-ph*0.9)
       + 0.62*Math.sin(pz*9.7+ph*2.3)*Math.cos(px*8.3+ph*0.4);
}

/* le champ qui repartit les trois tons du sol : basse frequence, doux */
function _o_robe(x,y,z){
  return 0.5+0.5*(0.70*Math.sin(x*2.1+0.7)*Math.cos(y*1.8-1.1)
                 +0.30*Math.sin(z*2.7+2.2)*Math.cos(x*2.3+0.5));
}
/* ── LE POLYGONE D'UNE DALLE — une vraie cellule, pas un rond ─────────────
   Un rond « ne correspond a rien » : une dalle a le contour de SA cellule de
   Voronoi. On en fabrique une par ile, avec sa propre graine, en rabotant un
   grand carre par les bissectrices de voisines jitterees. */
function _o_cellule(g,graine){
  var S=[], rnd=(function(s){s=(s*2654435761)>>>0;return function(){
    s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};})(graine);
  var i,j,k,q;
  for(j=-2;j<=2;j++)for(i=-2;i<=2;i++)
    S.push([i*g+(rnd()-.5)*g*0.46, j*g+(rnd()-.5)*g*0.46]);
  var bi=0,bd=1e9;
  for(q=0;q<S.length;q++){var d=Math.hypot(S[q][0],S[q][1]);if(d<bd){bd=d;bi=q;}}
  var Si=S[bi], R=g*6, P=[[Si[0]-R,Si[1]-R],[Si[0]+R,Si[1]-R],[Si[0]+R,Si[1]+R],[Si[0]-R,Si[1]+R]];
  for(j=0;j<S.length&&P.length>2;j++){
    if(j===bi)continue;
    var Sj=S[j], nx=Si[0]-Sj[0], ny=Si[1]-Sj[1], nm=Math.hypot(nx,ny);
    if(nm<1e-9)continue; nx/=nm; ny/=nm;
    var dec=((Si[0]+Sj[0])/2)*nx+((Si[1]+Sj[1])/2)*ny;
    var Q=[], m=P.length;
    for(k=0;k<m;k++){
      var a=P[k], b=P[(k+1)%m];
      var da=a[0]*nx+a[1]*ny-dec, db=b[0]*nx+b[1]*ny-dec;
      if(da>=0)Q.push(a);
      if((da>=0)!==(db>=0)){var t=da/(da-db);
        Q.push([a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t]);}
    }
    P=Q;
  }
  var O=[]; for(k=0;k<P.length;k++)O.push([P[k][0]-Si[0],P[k][1]-Si[1]]);
  return O;
}

/* ════════════════════════════════════════════════════════════════════════════
   ⚑ UNE ÎLE EST UNE VRAIE DALLE, DANS LE MONDE DE SA PLANTATION.
   « c'est des pois ronds qui correspondent a rien qui s'ajoutent » — juste.
   Une ile n'est pas une tache de couleur : c'est LE PROMI, avec le design et la
   couleur qu'il avait le jour ou on l'a plante. Ca s'ancre et ca ne rechange
   plus (CLAUDE.md §4 : « une dalle est figee a sa plantation »). D'ou une
   DIVERSITE DE DESIGNS a la surface de la meme sphere — encre a cote de braille
   a cote de gravure — puisque chaque Promi garde son monde.
   Le moteur les peint lui-meme, une par une, dans une vraie cellule.
   ⚠ La trame se lit AGRANDIE (mag 2,2) : un poil fait 6 a 10 px, un carreau de
   mosaique 11. A l'echelle naturelle le poil l'ecrase — c'est la collision
   d'echelles payee tout au long de ce chantier.
   ════════════════════════════════════════════════════════════════════════════ */
var MONDES_O=['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons'];

function batIles(n,pal,opt){
  opt=opt||{};
  var cols=palPelote(pal,opt);          /* [0] = le sol, uniforme */
  var IL=semisIles(n,opt);
  var PXR=opt.pxr||293, MAG=opt.mag||2.2;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  var cnt={}, BRUT=[], k, q, j;

  for(k=0;k<IL.length;k++){
    var I=IL[k];
    I.monde=opt.monde||MONDES_O[(_o_h(k*13+5)*MONDES_O.length)|0];
    var g=I.r*2*PXR/MAG*0.72;
    var P=_o_cellule(g, k*7919+31);
    var cv=document.createElement('canvas'), ok=false, _kk=PXR/MAG*dpr, _sx=null, _sy=null;
    /* ⚑ PORTAGE DANS L'APP — 10 septembre 2026. `Toile.dalleGeneree` n'existe que dans
       la COPIE du moteur (scratchpad/toile-extrait.js) : l'ajouter a app.html, ce serait
       toucher le code de la Toile (§9). Dans l'app, une ile EST un Promi reel, qui a deja
       sa vraie dalle : l'appelant la fournit (`opt.dalle`), rendue par
       `Toile.dalleTrame(cv, id, 1, monde)` — la regle 1 du §4, dans le monde de SA
       plantation. Sans `opt.dalle`, le chemin de la planche reste tel quel. */
    if(opt.dalle){
      var _rd=null; try{ _rd=opt.dalle(k,I,g); }catch(e){}
      if(_rd&&_rd.cv&&_rd.cv.width){ cv=_rd.cv; ok=true; _sx=_rd.sx; _sy=_rd.sy;
        if(_rd.kk) _kk=_rd.kk; if(_rd.monde) I.monde=_rd.monde; }
    } else {
    try{ ok=Toile.dalleGeneree(cv,{monde:I.monde, palette:opt.palette||Toile.getPalette(),
          poly:P, site:[0,0], sp:g*1.05, ci:(_o_h(k*29+3)*4)|0,
          lit:(k*3)%5, ang:_o_h(k*47+9)*Math.PI,
          tone:[1.0,0.76,1.24,0.88,1.12][k%5], pad:10}); }catch(e){}
    }
    if(!ok||!cv.width){ BRUT.push(null); continue; }
    /* ⚑ v29 — dans l'app, le moteur a rendu SES pixels avec la dalle (`__dalleDonnees`) ; la planche seule relit */
    var d=cv.__dalleDonnees || cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    for(q=0;q<d.length;q+=4){
      if(d[q+3]<24) continue;
      var q5=((d[q]>>3)<<10)|((d[q+1]>>3)<<5)|(d[q+2]>>3);
      cnt[q5]=(cnt[q5]||0)+1;
    }
    BRUT.push({w:cv.width, h:cv.height, d:d,
               sx:(_sx!=null?_sx:cv.__site[0]*dpr), sy:(_sy!=null?_sy:cv.__site[1]*dpr),
               k:_kk});
  }

  var cles=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a];}).slice(0,230);
  var IDX={};
  for(k=0;k<cles.length;k++){
    var v=+cles[k];
    IDX[v]=cols.length;
    cols.push([((v>>10)&31)*8+4, ((v>>5)&31)*8+4, (v&31)*8+4]);
  }
  function proche(v){
    if(IDX[v]!==undefined) return IDX[v];
    var r=((v>>10)&31)*8+4, gg=((v>>5)&31)*8+4, b=(v&31)*8+4, best=1, bd=1e9;
    for(var z=1;z<cols.length;z++){
      var dr=cols[z][0]-r, dg=cols[z][1]-gg, db=cols[z][2]-b, dd=dr*dr+dg*dg+db*db;
      if(dd<bd){bd=dd;best=z;}
    }
    return (IDX[v]=best);
  }
  for(k=0;k<BRUT.length;k++){
    var B=BRUT[k]; if(!B){ IL[k].m=null; continue; }
    var m=new Uint8Array(B.w*B.h), pp=0;
    for(j=0;j<B.d.length;j+=4,pp++){
      if(B.d[j+3]<24) continue;
      m[pp]=proche(((B.d[j]>>3)<<10)|((B.d[j+1]>>3)<<5)|(B.d[j+2]>>3));
    }
    IL[k].m=m; IL[k].mw=B.w; IL[k].mh=B.h;
    IL[k].sx=B.sx; IL[k].sy=B.sy; IL[k].kk=B.k;
  }
  for(k=0;k<IL.length;k++){
    var c=IL[k].c;
    var hx=0,hy=1,hz=0; if(Math.abs(c[1])>0.9){hx=1;hy=0;}
    var ax=c[1]*hz-c[2]*hy, ay=c[2]*hx-c[0]*hz, az=c[0]*hy-c[1]*hx;
    var am=Math.hypot(ax,ay,az)||1; ax/=am; ay/=am; az/=am;
    IL[k].e1=[ax,ay,az];
    IL[k].e2=[c[1]*az-c[2]*ay, c[2]*ax-c[0]*az, c[0]*ay-c[1]*ax];
  }
  /* la derniere plantee : c'est elle que la Pelote vient presenter */
  return {iles:IL, derniere:IL.length?IL[IL.length-1].c:null,
          col:cols, dl:new Int8Array(cols.length),
          nsol:1, plein:1, cle:'iles'+n+'/'+(opt.palette||''), dalles:[]};
}


/* ──────── _v_semis.js  (md5 source 32a8757cca1ad7ee23a96b399fc0c708) ──────── */
/* ════════════════════════════════════════════════════════════════════════════
   LE PAVAGE — un Voronoi PONDERE spherique. La Toile fermee sur elle-meme.
   ════════════════════════════════════════════════════════════════════════════ */
function fr(v){return v-Math.floor(v);}
var GOLD=2.399963229728653;
/* ⚠ UN HACHAGE, PAS UNE SUITE A FAIBLE DISCREPANCE.
   J'utilisais fr(i x 0,7548...) pour decider quels sites garder. Cette suite
   est REGULIERE par construction, et le reseau de Fibonacci sur lequel elle
   s'applique l'est aussi : les deux se sont accordes et la sphere est sortie
   EN BANDES MERIDIENNES. Un hachage entier casse la correlation. */
/* hh() vit dans _p_moteur.js */

/* ⚑ CE QUI TUE L'EFFET REPTILE : LA DENSITE DES SEMENCES, PAS LEUR POIDS.
   Ma premiere version faisait varier le POIDS des sites (diagramme de
   puissance). Ca ne marche pas : au-dela d'un ecart de l'ordre de
   l'espacement, un site a poids faible n'est pas une PETITE cellule — il est
   AVALE, il disparait. Les survivantes se retrouvent donc toutes de la meme
   taille. C'est exactement ce qu'on voyait : une peau de reptile.
   La bonne variable est la DENSITE DU SEMIS. Une cellule occupe 1/densite :
   la ou les semences se serrent, les dalles sont petites ; la ou elles
   s'espacent, elles sont grandes — et AUCUNE ne disparait. C'est aussi ce que
   fait une vraie Toile : des grappes serrees et des clairieres.
   Le poids reste, mais faible : il sert a casser la regularite locale. */
function densite(x,y,z,K){
  /* les frequences valent 4 a 7 : une grappe fait cinq ou six dalles. Plus bas,
     la densite varie a l'echelle de la boule et on retombe sur des bandes. */
  var v=0.5+0.5*Math.sin(K[0]*x+K[3])*Math.cos(K[1]*y+K[4])*Math.sin(K[2]*z+K[5]);
  var w=0.5+0.5*Math.sin(K[6]*z+K[9])*Math.cos(K[7]*x+K[10])*Math.sin(K[8]*y+K[11]);
  return 0.08+0.92*Math.pow(0.60*v+0.40*w, 2.4);
}
function semisSites(M, K){
  /* ⚑ LE BUG QUI FAISAIT DES COINS NOIRS, ET IL ETAIT ENORME.
     Ma boucle de rejet s'arretait des qu'elle avait M semences :
        while(i<CAND && garde<M) ...
     Or l'indice i d'un reseau de Fibonacci parcourt la sphere DU POLE NORD AU
     POLE SUD. En s'arretant a la 240e acceptee, on ne sortait jamais du
     PREMIER QUART du reseau : les 240 semences etaient toutes dans la calotte
     nord. Partout ailleurs, les deux plus proches sites etaient loin ET a
     egale distance — donc d2-d1 tombait sous le joint sur des regions
     entieres, et le pavage effacait des quartiers complets de la boule.
     Le diagnostic l'a montre d'un coup : avec une densite UNIFORME, les memes
     coins noirs. Ce n'etait donc pas la densite.
     LA PARADE : on balaie TOUT le reseau, et on regle le taux d'acceptation
     pour tomber sur M en moyenne. Deux passes, l'une pour la somme. */
  var CAND=M*26, i, x,y,z,r,a, som=0, dn=new Float64Array(CAND);
  for(i=0;i<CAND;i++){
    y=1-2*(i+0.5)/CAND; r=Math.sqrt(Math.max(0,1-y*y)); a=i*GOLD;
    dn[i]=densite(Math.cos(a)*r,y,Math.sin(a)*r,K); som+=dn[i];
  }
  var taux=M/som, S=[];
  for(i=0;i<CAND;i++){
    if(hh(i*7+3) >= dn[i]*taux) continue;
    y=1-2*(i+0.5)/CAND; r=Math.sqrt(Math.max(0,1-y*y)); a=i*GOLD;
    x=Math.cos(a)*r; z=Math.sin(a)*r;
    /* un peu de desordre : un reseau garde sa trame si on n'y touche pas */
    var jx=(hh(i*11+1)-0.5)*0.060, jy=(hh(i*13+5)-0.5)*0.060,
        jz=(hh(i*17+9)-0.5)*0.060;
    var m=Math.hypot(x+jx,y+jy,z+jz)||1;
    S.push([(x+jx)/m,(y+jy)/m,(z+jz)/m]);
  }
  return S;
}
var ARR=0.011;                 /* le rayon d'arrondi des coins, en radians */
function semisPavage(NC, M, joint, K, nbCoul, tourne, GRIL){
  GRIL=GRIL||0;
  var S=semisSites(M,K), Mn=S.length;
  var SX=new Float64Array(Mn), SY=new Float64Array(Mn), SZ=new Float64Array(Mn),
      Wt=new Float64Array(Mn), CI=new Int32Array(Mn), TI=new Int32Array(Mn),
      PLANT=new Uint8Array(Mn);
  /* ⚑ LE FOYER DE LA GRAPPE, ET LE MEME PIEGE QUE L'EMPREINTE.
     Je l'avais donne en coordonnees d'OBJET en le voulant face a nous : avec
     une vue tournee de 2,9 radians il tombait DERRIERE la sphere, et l'ecran
     sortait tout noir. Ici il est ecrit dans le repere de la vue de reference
     puis ramene dans celui de l'objet, une fois pour toutes. */
  var _cl=Math.cos(2.9), _sl=Math.sin(2.9), _ct=Math.cos(0.32), _st=Math.sin(0.32);
  var _v=[-0.10,-0.14,0.985];                    /* face a nous, un peu haut-gauche */
  var _zp=-_v[1]*_st+_v[2]*_ct, _y=_v[1]*_ct+_v[2]*_st;
  var PLX=_v[0]*_cl-_zp*_sl, PLY=_y, PLZ=_v[0]*_sl+_zp*_cl;
  var _pm=Math.hypot(PLX,PLY,PLZ); PLX/=_pm; PLY/=_pm; PLZ/=_pm;
  /* les cinq marches de ton de la Toile : TON = 1 · 0,76 · 1,24 · 0,88 · 1,12.
     Une dalle porte UNE couleur de la palette et UNE marche. Rien d'autre. */
  for(var k=0;k<Mn;k++){
    SX[k]=S[k][0]; SY[k]=S[k][1]; SZ[k]=S[k][2];
    Wt[k]=(hh(k*23+7)-0.5)*0.055;                /* faible : il casse, il n'avale pas */
    CI[k]=(hh(k*29+11)*nbCoul)|0;
    TI[k]=(hh(k*31+13)*5)|0;
    /* ⚑ LA PLUPART DES CELLULES SONT VIDES — c'est ca, une Toile.
       Sur l'ecran de l'app, une poignee de dalles colorees vit au milieu d'un
       champ de cellules vides, presque noires. Je peignais TOUTES les cellules
       en couleur : ca faisait une mosaique de vitrail, pas une Toile.
       Les Promi se GROUPENT, comme sur la Toile ou plantOne cherche une
       cellule degagee proche des autres. */
    var dc=SX[k]*PLX+SY[k]*PLY+SZ[k]*PLZ;        /* proximite du foyer */
    /* relevee : la vraie Toile montre a peu pres quatre dixiemes de dalles
       plantees dans sa grappe, pas une sur dix. */
    var pr=0.30+0.70*Math.pow(Math.max(0,(dc+0.70)/1.70), 1.4);
    PLANT[k]= hh(k*41+17)<pr ? 1 : 0;
  }
  var P=new Float64Array(NC*3), CEL=new Int32Array(NC), BORD=new Uint8Array(NC), n=0;
  /* ⚑ LE SEMIS DE REMPLISSAGE SE PERTURBE, SINON SA SPIRALE SE VOIT.
     Un reseau de Fibonacci non perturbe a une structure en spirale ; a la
     taille de grain qu'on emploie, elle bat avec le grain et sort en bras
     spirales sur toute la boule. On decale chaque point d'une fraction de
     l'espacement moyen, tire au hachage. */
  var pasM=Math.sqrt(12.566370614/NC);
  for(var i=0;i<NC;i++){
    var cy=1-2*(i+0.5)/NC, cr=Math.sqrt(Math.max(0,1-cy*cy)), ca=i*GOLD;
    var px=Math.cos(ca)*cr, py=cy, pz=Math.sin(ca)*cr;
    px+=(hh(i*3+1)-0.5)*pasM*0.95; py+=(hh(i*5+2)-0.5)*pasM*0.95;
    pz+=(hh(i*7+4)-0.5)*pasM*0.95;
    var mn=Math.hypot(px,py,pz)||1; px/=mn; py/=mn; pz/=mn;
    /* ⚑ PIXEL : SON DESSIN EST DANS LE CONTOUR, PAS DANS L'INTERIEUR.
       Une dalle « pixel » est PLEINE (73 % de remplissage) : ce qui la rend
       reconnaissable, c'est que son bord est cale sur une grille de cinq
       pixels. Je cherchais son motif a l'interieur — il n'y en a pas, et elle
       sortait en polygone lisse, illisible. On quantifie donc la POSITION qui
       sert a decider de la cellule : le bord devient escalier. */
    var qx=px, qy=py, qz=pz;
    if(GRIL>0){
      qx=Math.round(px/GRIL)*GRIL; qy=Math.round(py/GRIL)*GRIL; qz=Math.round(pz/GRIL)*GRIL;
      var qm=Math.hypot(qx,qy,qz)||1; qx/=qm; qy/=qm; qz/=qm;
    }
    var d1=9,d2=9,d3=9,k1=-1;
    for(var q=0;q<Mn;q++){
      var dp=qx*SX[q]+qy*SY[q]+qz*SZ[q];
      if(dp>1)dp=1; if(dp<-1)dp=-1;
      var dd=Math.acos(dp)-Wt[q];
      if(dd<d1){d3=d2;d2=d1;d1=dd;k1=q;}
      else if(dd<d2){d3=d2;d2=dd;}
      else if(dd<d3){d3=dd;}
    }
    /* ⚑ LE CONTOUR D'UNE DALLE, C'EST SA CELLULE — pas une image mise a l'echelle.
       Je decoupais chaque cellule avec le SILHOUETTE d'une image de dalle
       redimensionnee : les contours sortaient etires, ils ne se raccordaient pas
       d'une cellule a l'autre, et le pavage etait faux. Or j'ai deja la vraie
       chose : une cellule de Voronoi PONDERE sur la sphere, c'est-a-dire
       exactement ce qu'est une dalle de Toile.
       Le bord se lit dans l'ecart au deuxieme site (d2-d1). Et LES COINS SE
       ARRONDISSENT comme le fait le moteur : pres d'un coin on est proche de
       DEUX voisins a la fois, donc la somme des deux exponentielles franchit le
       seuil plus tot et le coin se trouve rogne. Une intersection molle de
       demi-espaces — c'est la definition meme d'un arrondi. */
    var e=d2-d1;
    if(joint>0){
      var t3=Math.exp(-(d2-d1)/ARR)+Math.exp(-(d3-d1)/ARR);
      if(t3>Math.exp(-joint/ARR)) continue;
    }
    P[n*3]=px; P[n*3+1]=py; P[n*3+2]=pz; CEL[n]=k1;
    /* ⚑ LA DISTANCE AU BORD, GARDEE. C'est elle qui rend le contour NET : un
       poil pousse a la taille de la cellule deborde de son bord et le rend
       flou — une dalle a un contour franc. Pres du bord, le poil raccourcit. */
    var eb=e/(joint>0?joint*3:0.05); if(eb>1)eb=1;
    BORD[n]=(eb*255)|0;
    n++;
  }
  /* ── LE REPERE LOCAL DE CHAQUE CELLULE ────────────────────────────────
     Une cellule doit porter UNE VRAIE DALLE du moteur. Il lui faut donc un
     plan tangent (deux axes), un rayon (pour choisir une dalle de la bonne
     taille et l'y poser), et une rotation propre — sinon toutes les dalles de
     la sphere seraient alignees sur le meme repere, ce qui ne se voit sur
     aucune Toile. */
  var E1=new Float64Array(Mn*3), E2=new Float64Array(Mn*3), RAY=new Float64Array(Mn);
  for(var k3=0;k3<Mn;k3++){
    var sx=SX[k3], sy=SY[k3], sz=SZ[k3];
    var hx=0,hy=1,hz=0; if(Math.abs(sy)>0.9){hx=1;hy=0;}
    var ax=sy*hz-sz*hy, ay=sz*hx-sx*hz, az=sx*hy-sy*hx;
    var am=Math.hypot(ax,ay,az)||1; ax/=am; ay/=am; az/=am;
    var bx=sy*az-sz*ay, by=sz*ax-sx*az, bz=sx*ay-sy*ax;
    /* ⚑ TOURNER PAR CELLULE OU NON : LE MOTEUR TRANCHE, PAS MOI.
       Sur la vraie Toile, braille, mosaique, pixel et sillons sont ANCRES sur
       des coordonnees absolues (pois tous les 9, tesselles tous les 11, carres
       tous les 5, sillons tous les 6) : leur motif est CONTINU d'une dalle a
       la suivante. Encre, touffe, terrazzo et gravure, eux, portent l'angle
       propre de leur graine (`s.ang` dans le moteur) : chaque dalle a SA
       direction, et c'est ce qui fait la gravure.
       Je tournais TOUTES les cellules au hasard : la grille du braille partait
       dans tous les sens. Puis AUCUNE : la gravure devenait un peigne uniforme.
       Les deux etaient faux — c'est par monde. */
    if(tourne){
      var th=hh(k3*37+19)*Math.PI, ct=Math.cos(th), st=Math.sin(th);
      E1[k3*3]=ax*ct+bx*st; E1[k3*3+1]=ay*ct+by*st; E1[k3*3+2]=az*ct+bz*st;
      E2[k3*3]=-ax*st+bx*ct; E2[k3*3+1]=-ay*st+by*ct; E2[k3*3+2]=-az*st+bz*ct;
    } else {
      E1[k3*3]=ax; E1[k3*3+1]=ay; E1[k3*3+2]=az;
      E2[k3*3]=bx; E2[k3*3+1]=by; E2[k3*3+2]=bz;
    }
  }
  /* ⚑ LA BOITE DE LA CELLULE, DANS SON PROPRE PLAN TANGENT.
     Caler la dalle sur le CERCLE maximal de la cellule la faisait rentrer trop
     petit : les cellules allongees restaient aux trois quarts vides et la
     sphere sortait trouee. On mesure les quatre bornes en u et en v, et la
     dalle se pose sur cette boite-la. */
  var U0=new Float64Array(Mn), U1=new Float64Array(Mn),
      V0=new Float64Array(Mn), V1=new Float64Array(Mn);
  for(var z=0;z<Mn;z++){ U0[z]=V0[z]=1e9; U1[z]=V1[z]=-1e9; }
  for(var i3=0;i3<n;i3++){
    var c3=CEL[i3];
    var dp3=P[i3*3]*SX[c3]+P[i3*3+1]*SY[c3]+P[i3*3+2]*SZ[c3];
    if(dp3>1)dp3=1; var an=Math.acos(dp3);
    if(an>RAY[c3]) RAY[c3]=an;
    var wx3=P[i3*3]-SX[c3], wy3=P[i3*3+1]-SY[c3], wz3=P[i3*3+2]-SZ[c3];
    var uu3=wx3*E1[c3*3]+wy3*E1[c3*3+1]+wz3*E1[c3*3+2];
    var vv3=wx3*E2[c3*3]+wy3*E2[c3*3+1]+wz3*E2[c3*3+2];
    if(uu3<U0[c3])U0[c3]=uu3; if(uu3>U1[c3])U1[c3]=uu3;
    if(vv3<V0[c3])V0[c3]=vv3; if(vv3>V1[c3])V1[c3]=vv3;
  }
  return {P:P.subarray(0,n*3), n:n, cel:CEL.subarray(0,n), bord:BORD.subarray(0,n),
          ci:CI, ti:TI, plant:PLANT, sites:Mn,
          /* ⚑ LES POIDS SORTENT AVEC LE RESTE. La cellule d'une graine n'est
             pas un Voronoi ordinaire : l'attribution est `acos(p.s) - w`.
             Sans les poids, un polygone reconstruit rate le bord de 12 % du
             rayon — assez pour que la dalle et sa cellule ne coincident plus. */
          wt:Wt,
          sx:SX, sy:SY, sz:SZ, e1:E1, e2:E2, ray:RAY,
          u0:U0, u1:U1, v0:V0, v1:V1};
}

/* ──────── _v_peint.js  (md5 source 7ca230169d13768cbc5d863905872ef3) ──────── */
/* ════════════════════════════════════════════════════════════════════════════
   LE PEINTRE — tout allume : relief a amplitude variable, palette du Studio,
   dalles de tailles variees, et le doigt qui s'enfonce pour de bon.
   ════════════════════════════════════════════════════════════════════════════ */
var ORI=24, NIVA=6, NVAR=3;
/* ════════════════════════════════════════════════════════════════════════════
   ⚑ LE CHAMP DE POIL — ET C'EST LUI, MAINTENANT, QUI PORTE TOUT LE PRODUIT.
   Trois choses ecrivent le sens du poil, et AUCUNE n'ajoute quoi que ce soit a
   la matiere : elles SONT la matiere.

     1 · LA COURONNE — le Noyau. Tout pelage a un point d'ou il part. Le sien
         est au centre de la face qu'on regarde : c'est « toi », et ca ne coute
         pas un pixel d'interface. Ancien Noyau : un disque creme de 8 % du
         rayon, qui se lisait comme UN TROU CLAIR perce dans le velours.
     2 · LES EPIS — les six. Une personne a qui on a donne sa parole est un
         EPI : le poil converge vers elle en spirale. L'intensite du peignage
         dit le CUMUL des paroles tenues avec elle, et un epi ne se defait pas.
         Anciens six : six pastilles sombres a anneau, a intervalle egal, qui
         n'encodaient plus rien depuis qu'on avait libere la geometrie — six
         trous perces dans le velours, et la regle du §3 les condamnait.
     3 · LES CARESSES — la memoire de la main. Une main qui passe COUCHE le
         poil dans son sens. Ce n'est ni un creux ni une rayure : c'est un
         lustre, parce que quelques milliers de poils y regardent tous dans la
         meme direction. Et c'est la seule chose que personne d'autre n'a.

   ⚠ POURQUOI LES TRACES REVIENNENT AU REPOS, APRES AVOIR ETE RETIREES.
   Elles avaient ete retirees le matin meme, et a raison : c'etaient des
   GRAVURES posees au hasard sur un objet neuf, qui cassaient l'uniformite.
   Ce n'est plus la meme chose. Une caresse ne creuse plus rien — elle change
   LE SENS DU POIL. L'objet au repos doit porter ses traces : on doit voir,
   sans toucher, que quelqu'un s'en est occupe.
   ════════════════════════════════════════════════════════════════════════════ */
function nrmT(vx,vy,vz,x,y,z){          /* projette sur le plan tangent, normalise */
  var d=vx*x+vy*y+vz*z; vx-=d*x; vy-=d*y; vz-=d*z;
  var m=Math.sqrt(vx*vx+vy*vy+vz*vz);
  return m>1e-7?[vx/m,vy/m,vz/m]:null;
}
function bruitPoil(x,y,z,t){
  var e=0.03, f=function(a,b,c){
    return Math.sin(2.1*a+0.7+t)*Math.cos(1.7*b+1.9)*Math.sin(1.9*c+0.4)
         + 0.55*Math.sin(3.3*c-1.1+t*0.6)*Math.cos(2.9*a+0.5);};
  return nrmT(f(x+e,y,z)-f(x-e,y,z), f(x,y+e,z)-f(x,y-e,z), f(x,y,z+e)-f(x,y,z-e), x,y,z);
}
/* ════════════════════════════════════════════════════════════════════════════
   ⚑ LE CHAMP DE POIL — ET IL NE PORTE PLUS QUE LA MAIN.

   ⚠ CE QU'ON A ESSAYE, ET POURQUOI ON L'ABANDONNE POUR DE BON.
   On a demande a la matiere d'encoder QUI EST QUI : par la position, par la
   saturation, par la densite, puis par un EPI — un tourbillon de poil par
   personne. Verdict de Tom sur le dernier : « ca fait des signes BMW, ni beau
   ni comprehensible ». Et il ajoute la vraie raison, qui n'est pas une
   question d'execution : UNE MATIERE NE SAIT PAS DIRE UN NOM. Un epi ne peut
   pas etre « Rachel ». Une saturation non plus, une densite non plus. C'est
   structurel — c'est pour ca que vingt series ont echoue au meme endroit.

   Donc on arrete de le lui demander. La sphere est belle ; elle n'a pas a etre
   informative. Elle ne porte plus que trois choses :
     le velours · ses dalles dans leur monde d'origine · LA MEMOIRE DE LA MAIN.
   Elle dit « voila ce que j'ai tenu, et j'y ai passe du temps ». Les six et le
   Noyau vivent maintenant SOUS elle, en anneaux lisibles avec un prenom (§2.9).
   Bonus, et il est gros : l'image reste indechiffrable pour un inconnu, donc
   elle se partage.

   Le champ a donc deux termes, et un seul dessine :
     1 · LE PEIGNE — une direction unique, ses deux zeros au limbe. Uniforme :
         c'est le fond sur lequel la main se lit.
     2 · LES CARESSES — le poil couche dans le sens du geste. Comme tout le
         reste est uniforme, c'est LA SEULE STRUCTURE de la surface, donc la
         plus visible. C'est exactement ce qu'on veut.
   ════════════════════════════════════════════════════════════════════════════ */
function nrmT(vx,vy,vz,x,y,z){
  var d=vx*x+vy*y+vz*z; vx-=d*x; vy-=d*y; vz-=d*z;
  var m=Math.sqrt(vx*vx+vy*vy+vz*vz);
  return m>1e-7?[vx/m,vy/m,vz/m]:null;
}
function bruitPoil(x,y,z,t){
  var e=0.03, f=function(a,b,c){
    return Math.sin(2.1*a+0.7+t)*Math.cos(1.7*b+1.9)*Math.sin(1.9*c+0.4)
         + 0.55*Math.sin(3.3*c-1.1+t*0.6)*Math.cos(2.9*a+0.5);};
  return nrmT(f(x+e,y,z)-f(x-e,y,z), f(x,y+e,z)-f(x,y-e,z), f(x,y,z+e)-f(x,y,z-e), x,y,z);
}
var _EPW=0;                     /* le poids de caresse au dernier point calcule */
function champPoil(x,y,z,t,B,TR){
  _EPW=0;
  /* 1 · LE PEIGNE. B est la direction qui sort horizontale a l'ecran : ses
     deux seuls zeros tombent au limbe gauche et au limbe droit, vus de profil,
     ou personne ne les lit (theoreme de la boule chevelue — un champ tangent
     sur une sphere a forcement deux zeros, on choisit OU). */
  /* ⚑ PORTAGE DANS L'APP — 10 septembre 2026. Sur la planche, B est la direction
     horizontale de L'ÉCRAN, prise à la vue du moment où le cache se remplit : ses deux
     zéros tombent aux limbes gauche et droit. Mais dans l'app la Pelote TOURNE TOUJOURS :
     un quart de tour plus tard (~41 s), un zéro — un épi, la « couronne » refusée —
     arrive au centre de la face ; et chaque caresse, qui refait le cache, recuisait le
     peigne à la vue du moment : toute la fourrure changeait d'orientation au lâcher.
     Sans B, le peigne est AZIMUTAL autour de l'axe de rotation (u = y × p). Au centre
     de la face il vaut exactement le B de la planche, même sens ; il ne dépend plus de
     la vue ; ses deux zéros sont aux pôles de l'axe, que la rotation lente ne ramène
     jamais de face (théorème de la boule chevelue : on choisit OÙ). */
  var u=B?nrmT(B[0],B[1],B[2],x,y,z):nrmT(z,0,-x,x,y,z);
  if(!u) u=[1,0,0];
  var vx=u[0], vy=u[1], vz=u[2];
  var g=bruitPoil(x,y,z,t);
  if(g){ vx+=0.26*g[0]; vy+=0.26*g[1]; vz+=0.26*g[2]; }
  /* 2 · LES CARESSES. Le poil se couche DANS LE SENS du geste : tangente de
     l'arc au point le plus proche. C'est ce parallelisme-la qu'on lit comme un
     lustre — pas un creux, pas une rayure. */
  if(TR) for(var j=0;j<TR.length;j++){
    var G=TR[j];
    var th=Math.atan2(x*G.d[0]+y*G.d[1]+z*G.d[2], x*G.a[0]+y*G.a[1]+z*G.a[2]);
    if(th<0) th=0; else if(th>G.L) th=G.L;
    var ct=Math.cos(th), st=Math.sin(th);
    var px=G.a[0]*ct+G.d[0]*st, py=G.a[1]*ct+G.d[1]*st, pz=G.a[2]*ct+G.d[2]*st;
    var dd=x*px+y*py+z*pz; if(dd>1)dd=1; else if(dd<-1)dd=-1;
    var an=Math.acos(dd); if(an>=G.w) continue;
    var wg=1-an/G.w; wg=wg*wg*(3-2*wg); wg*=G.f;
    if(wg>_EPW)_EPW=wg;
    var qx=-G.a[0]*st+G.d[0]*ct, qy=-G.a[1]*st+G.d[1]*ct, qz=-G.a[2]*st+G.d[2]*ct;
    var qq=nrmT(qx,qy,qz,x,y,z); if(!qq) continue;
    var w2=0.96*wg, r2=3.4*w2;
    vx=vx*(1-w2)+r2*qq[0]; vy=vy*(1-w2)+r2*qq[1]; vz=vz*(1-w2)+r2*qq[2];
  }
  return [vx,vy,vz];
}
var SIX=[[0.34,0.30],[1.42,0.58],[2.31,0.86],[3.55,0.44],[4.48,0.72],[5.63,0.94]];

function peint(cv,o){
  var CSS=o.css||520, W=CSS*D;
  cv.width=W; cv.height=W;
  var g=cv.getContext('2d');
  g.fillStyle=o.fond||'#1D1501'; g.fillRect(0,0,W,W);
  var A=lieTampons(o.atlas,W), TAI=o.tailles;
  var R=CSS*(o.R||0.425)*D, FOC=R*5.4, CX=W/2, CY=W/2;
  var lac=o.lac, tan=o.tan;
  var cl=Math.cos(lac), sl=Math.sin(lac), ct=Math.cos(tan), st=Math.sin(tan);
  var E=o.emp?prepEmp(o.emp,cl,sl,ct,st):null;
  var S=o.semis, P=S.P, N=S.n, REL=o.relief, ENV=o.env;
  /* ⚑ UN VRAI ECLAIRAGE, A TROIS TERMES — pas une seule lampe.
     Une seule directionnelle laissait la moitie de la boule dans le noir : on
     ne lisait ni le pavage ni le pelage. On pose donc ce que pose n'importe
     quel eclairage de studio, et pour les memes raisons :
       LA CLE     en haut a gauche, devant — elle sculpte le volume.
       LE REMPLISSAGE en bas a droite, plus faible et plus large — il OUVRE
                  l'ombre au lieu de la boucher, sans effacer la forme.
       LE LISERE  au limbe (Fresnel) — il detache la silhouette du fond et
                  affirme le cercle exact.
     Plus un ambiant franc : la matiere doit se lire PARTOUT. */
  /* ⚑ LA LUMIERE VIENT DU TITRE « AURA », EN HAUT A GAUCHE DE LA SPHERE.
     Elle est SUGGEREE, pas figuree : aucune source, aucun reflet, aucun halo.
     La direction est donc franchement haut-gauche, mais l'amplitude est
     minuscule — voir `lum` plus bas. */
  /* ⚠ ET LE SIGNE SE VERIFIE A L'ECRAN, PAS AU RAISONNEMENT. J'avais deduit
     que -X, -Y pointait en haut a gauche ; rendu, le clair etait en BAS A
     DROITE. La normale de vue ne porte pas la convention que je croyais. On
     retourne, et on regarde. */
  /* ⚑ LA LUMIERE VIENT DU TITRE « AURA », EN HAUT A GAUCHE.
     ⚠ Le signe se verifie AU CHIFFRE, pas au raisonnement : j'ai deduit deux
     fois de suite la mauvaise convention pour la normale de vue. Le controle
     tient en trois lignes — on releve la couleur moyenne dans le coin haut
     gauche et dans le coin bas droit, et on regarde laquelle est la plus
     claire. Vise : clair en haut a gauche, violet profond en bas a droite. */
  var LX=-0.58, LY=-0.72, LZ=0.380, DOS=o.dos||1;
  var FX2=0.52, FY2=0.40, FZ2=0.756;                 /* le remplissage */
  /* ⚑ LA TABLE DE COULEURS VIENT DE LA TRAME ELLE-MEME.
     Ce ne sont plus « les quatre couleurs de la palette » reconstruites de mon
     cote : ce sont les teintes REELLEMENT PEINTES par le moteur dans les
     dalles du monde courant. La sphere ne ressemble donc pas a la Toile —
     elle EST la Toile. Chaque teinte porte ses sept marches ; la lumiere fait
     monter la dalle d'une marche, elle ne fait jamais un degrade. */
  /* ⚑ DEUX TABLES : la dalle PLANTEE, et la cellule VIDE.
     Sur la vraie Toile une cellule vide n'est pas absente — elle porte la meme
     trame, dans un gris tres sombre. C'est ce fond-la qui fait ressortir la
     grappe de Promi. On derive le gris de la teinte elle-meme (desaturee,
     clarte ramenee a 0,11) : la trame reste la meme, seule la couleur tombe. */
  /* ⚑ L'ENTRE-DALLES RESTE VIDE.
     J'avais rempli toute la sphere pour supprimer les trous noirs. Mais avec
     les six disques et le Noyau par-dessus, ca surcharge : on ne lit plus rien.
     On ne peint donc QUE la matiere des dalles plantees — le reste est du vide,
     et c'est ce vide qui laisse la place au Noyau et aux six. */
  /* ⚑ SUR UNE TRAME, LA COULEUR VIENT DE LA DALLE, PAS DU MOTIF.
     Le moteur peint la trame d'une dalle DANS LA COULEUR DE CETTE DALLE : le
     motif ne dit que « matiere ou vide ». En prenant la couleur dans l'image du
     motif, j'etais oblige de choisir la dalle-source pour sa taille, donc de
     tomber toujours sur les deux ou trois memes — et la sphere sortait
     presque monochrome. Separer les deux rend la variete de la palette ET
     libere le choix du motif. */
  /* ⚑ UNE DALLE A UNE COULEUR, ET DES STRATES DEDANS.
     C'est ainsi que le moteur peint : `PALL()` donne UNE couleur de palette
     declinee en cinq eclats. La trame ne dit donc pas la couleur — elle dit la
     MATIERE et, pour chaque pixel, DE COMBIEN il est plus clair ou plus sombre
     que la mediane de son monde. On reporte ce clair-obscur en marches sur la
     couleur de la cellule : les strates d'une encre ou d'un terrazzo
     reviennent, sans que la palette du Studio se disperse. */
  var TR=o.trame, TDL=TR.dl, COL=[];
  /* ⚑ UNE CELLULE VIDE N'EST PAS UN TROU : SUR LA TOILE ELLE EST GRISE, ET
     ELLE PORTE LA MEME TRAME.
     Les cellules non plantees ne peignaient RIEN : la sphere sortait en
     plaques qui flottent dans du noir, et les grands vides ne sont pas le
     joint (0,017 rad, soit 4,5 px a l'ecran) mais ces cellules-la. Or l'audit
     §2 rejette deja « une majorite de cellules vides : la silhouette se creuse,
     ce n'est plus une boule ». Et la vraie Toile ne fait pas ca : ses cellules
     sans Promi sont sombres, presque noires, mais PLEINES de matiere.
     On ajoute donc une teinte de plus a la rampe — le gris de la Toile — et
     les cellules vides la portent. La boule redevient continue et fournie,
     les dalles colorees ressortent, et le joint reste le seul vide. */
  /* ⚑ LA RAMPE PORTE LES VRAIES COULEURS DE LA DALLE — pas quatre teintes de
     palette avec une marche de clarte.
     C'est LA perte qui faisait dire a Tom « c'est 10 % du vrai design ». Le
     peintre jetait la couleur peinte par le moteur et n'en gardait qu'un
     ecart de clarte reporte sur la couleur de la CELLULE. Tout ce que le
     dessin a de propre disparaissait : le lisere creme et le coeur orange
     d'une fleur de touffe, les recouvrements de lobes d'une encre, les eclats
     plus clairs d'un terrazzo, le liant d'une mosaique.
     `bat_trames` releve deja les teintes REELLEMENT peintes du monde (jusqu'a
     96) et rend, pour chaque pixel de dalle, l'indice de la sienne. On batit
     donc la rampe sur CES teintes-la : chaque poil porte exactement la couleur
     que le moteur a posee sous sa racine.
     ⚠ Ce que l'ancien commentaire redoutait — « la sphere sortait presque
     monochrome » — venait d'ailleurs : pour les trames, TOUTES les cellules
     prenaient la MEME dalle-source (celle au plus grand rectangle inscrit).
     La variete revient en rendant a chaque cellule son propre tirage. */
  var GRIS=o.gris||[52,56,66];
  var POUSSE=o.pousse===undefined?0:(o.pousse<0?0:(o.pousse>1?1:o.pousse));
  var DILUE=((o.trame&&o.trame.plein)||1)>0.34;
  /* l'indice de la teinte grise dans la rampe : la boucle de versement s'en
     sert pour raccourcir le grain du sol. */
  var TCOL=(TR.col&&TR.col.length)?TR.col:(o.pal||[[41,21,71]]);
  /* ⚑ LA COULEUR DU SOL DIT L'ETAT MAJORITAIRE.
     Le sol (indice 0) couvre toute la sphere : c'est LUI la couleur de
     la Pelote. On le force donc a la couleur d'etat qui domine — menthe si le
     plus gros des paroles est TENU, terracotta si c'est A TENIR, mauve si
     c'est EN COURS. Les dalles gardent, elles, le monde de leur plantation :
     la regle du §4 (« la dalle porte le monde ») n'est pas entamee, parce que
     le sol n'est pas une dalle. */
  if(o.sol){ TCOL=TCOL.slice(); TCOL[0]=o.sol; }
  var NCOL=TCOL.length;
  for(var c=0;c<NCOL;c++){ var RP=o.velours2?rampeVelours(TCOL[c]):(o.grade?rampeGradee(TCOL[c],o.grade):rampeCouleur(TCOL[c]));
    for(var m4=0;m4<MARCHES;m4++) COL.push(pack(RP[m4])); }
  /* ⚑ QUELLES TEINTES SONT DES PROMI, ET LESQUELLES SONT LE FOND.
     Sur la Toile, une cellule sans Promi est GRISE — saturation quasi nulle —
     et une dalle plantee porte une couleur de palette. On n'a donc besoin
     d'aucune information de cellule : la SATURATION suffit a les distinguer,
     teinte par teinte, une fois pour toutes. */
  var SAT=new Uint8Array(NCOL+1);
  for(var cs=0;cs<NCOL;cs++){
    var _c=TCOL[cs], _mx=Math.max(_c[0],_c[1],_c[2]), _mn=Math.min(_c[0],_c[1],_c[2]);
    SAT[cs]=(_mx>=48 && _mx-_mn>=28)?1:0;
  }
  var RPG=o.velours2?rampeVelours(GRIS):rampeCouleur(GRIS);
  for(var m5=0;m5<MARCHES;m5++) COL.push(pack(RPG[m5]));   /* la cellule vide */
  /* ⚑ LA MATIERE TRAVAILLEE — LE SECOND ETAGE DE LA TABLE.
     « Une personne proche est une matiere PLUS SATUREE, plus travaillee, ou
     qu'elle soit sur la sphere. » Je l'avais cable sur la MARCHE : le poli
     ajoutait deux marches de clarte, et les six sortaient en POIS RONDS PALES
     — precisement ce que Tom avait refuse. Une marche de clarte est de la
     lumiere, et la lumiere de cette boule vient du titre, d'un seul cote : on
     ne peut pas s'en servir pour dire autre chose.
     On double donc la table : les memes teintes, les memes vingt marches,
     mais RESSATUREES. Le poli ne deplace plus la marche, il change d'etage —
     la matiere devient plus dense en couleur, jamais plus claire. */
  var ETAGE=COL.length;
  for(var c2=0;c2<NCOL;c2++){
    var _b=r2h(TCOL[c2]), _sv=[0,0,0];
    _sv=h2r(_b[0], Math.min(0.99,_b[1]*1.11+0.03), _b[2]);
    var RP2=o.velours2?rampeVelours(_sv):(o.grade?rampeGradee(_sv,o.grade):rampeCouleur(_sv));
    for(var m6=0;m6<MARCHES;m6++) COL.push(pack(RP2[m6]));
  }
  for(var m7=0;m7<MARCHES;m7++) COL.push(pack(RPG[m7]));   /* le gris ne se sature pas */
  var t0=performance.now(), i;
  /* ── QUELLE DALLE DANS QUELLE CELLULE ────────────────────────────────────
     On choisit celle dont la boite est la plus proche de la taille de la
     cellule, puis on l'y pose exactement : le grain de la trame reste donc a
     peu pres a sa taille naturelle d'une cellule a l'autre — comme sur une
     vraie Toile, ou les pois du braille ont le meme pas dans une grande dalle
     et dans une petite. */
  /* combien de pixels de trame pour un radian, et le monde deborde-t-il de sa
     cellule — les deux servent des le choix de la dalle. */
  /* ⚑ LA TRAME SE LIT AGRANDIE — sinon le poil la detruit.
     Les motifs du moteur ont des pas de 5 a 11 pixels (carres tous les 5, pois
     tous les 9, tesselles tous les 11). Un poil en fait 5 a 8 : a l'echelle
     naturelle, LE POIL EST AUSSI GROS QUE LE DETAIL QU'IL DOIT DESSINER, et il
     l'ecrase. Pixel sortait illisible, encre et terrazzo en pates. On lit donc
     la trame agrandie : ses details passent a 15-30 px, franchement plus gros
     que le grain qui les peint, et une cellule montre trois a cinq periodes —
     comme une dalle de Toile qu'on regarde de pres. */
  var MAG=o.mag||2.7;
  var PXR=(o.pxr||1.0)*R/D/MAG, LIBRE=!!o.libre;
  var DA=TR.dalles, NS=S.sites;
  var ENR=!!TR.toile;                  /* la Toile enroulee : plus rien a choisir */
  var ILE=TR.iles||null;               /* la fourrure d'abord, les iles dedans */
  var NIL=ILE?ILE.length:0;
  /* en mode ILES il n'y a plus de dalle a choisir : on saute tout le bloc */
  if(!ENR && !ILE && S.__dalCle!==TR.cle){
    var CD=new Int32Array(NS), CK=new Float64Array(NS);
    /* KREF : combien de pixels de trame pour un radian de sphere. On choisit
       la dalle dont la boite est la plus proche de la cellule a cette echelle,
       PUIS on l'y ajuste exactement — le reste d'ecart est faible, donc le
       grain de la trame garde a peu pres sa taille naturelle d'une cellule a
       l'autre, comme sur une vraie Toile. */
    var CU=new Float64Array(NS), CV=new Float64Array(NS);
    for(var k=0;k<NS;k++){
      var du=Math.max(1e-4,S.u1[k]-S.u0[k]), dv=Math.max(1e-4,S.v1[k]-S.v0[k]);
      /* on choisit la dalle dont la BOITE ressemble le plus a celle de la
         cellule — meme allongement, meme taille. Moins on gaspille, plus la
         dalle remplit sa cellule. */
      /* ⚑ UNE CELLULE MONTRE UNE DALLE ENTIERE, pas un morceau de son interieur.
         En n'echantillonnant que le rectangle inscrit et en repliant au miroir,
         je decoupais les motifs : les fleurs de touffe devenaient du moucheté,
         la gravure des losanges. On pose LA DALLE COMPLETE dans la cellule —
         sa silhouette, sa matiere, ses couleurs — et le motif redevient lisible.
         Le tirage reste au hachage (la variete des couleurs en depend), mais on
         prefere, a egalite, une dalle dont l'ALLONGEMENT ressemble a celui de
         la cellule : moins de marge perdue autour. */
      /* ⚑ UNE DALLE PAR CELLULE : la cellule k lit DA[k]. Plus de tirage,
         plus de preference d'allongement, plus de mise a l'echelle par
         cellule — la dalle A ETE PEINTE dans ce contour-la. */
      if(TR.parCell){
        CD[k]=k<DA.length?k:(k%DA.length);
        CK[k]=PXR/(TR.pxr||PXR);       /* une seule echelle, celle du cadre */
        CU[k]=0; CV[k]=0;
        continue;
      }
      var lf=Math.log(du/dv), best=(hh(k*53+29)*DA.length)|0, bd=1e9;
      /* ⚑ CHAQUE CELLULE TIRE SA PROPRE DALLE, EN TRAME COMME EN LIBRE.
         Les trames prenaient TOUTES la meme dalle-source — celle au plus grand
         rectangle inscrit — parce que la couleur venait de la cellule et que
         seule la taille comptait. Maintenant que la couleur vient de la DALLE,
         ce choix unique rendrait la sphere monochrome. Le tirage au hachage
         revient, avec la preference d'allongement. */
      if(true){
        for(var q=0;q<DA.length;q++){
          var qq=(best+q)%DA.length;
          var dd=Math.abs(Math.log(DA[qq].bw/DA[qq].bh)-lf)+0.045*q;
          if(dd<bd){bd=dd;best=qq;} }
      } else {
        /* ⚑ POUR UNE TRAME, IL FAUT QUE L'INTERIEUR SOIT ASSEZ GRAND.
           On lit la matiere au PAS NATUREL dans le rectangle inscrit de la
           dalle. Si la cellule est plus large que ce rectangle, je rabattais
           l'echantillon sur son bord — et ca faisait des TRAINEES radiales au
           bord des cellules. On part du tirage au hachage (la variete des
           couleurs en depend) et on avance jusqu'a une dalle assez grande. */
        /* la couleur ne vient plus du motif : on peut donc prendre pour source
           la dalle au plus grand interieur, celle qui ne rabattra jamais. */
        var bb=0, bs=-1;
        for(var q4=0;q4<DA.length;q4++){ var ar=Math.min(DA[q4].rw,DA[q4].rh);
          if(ar>bs){bs=ar;bb=q4;} }
        best=bb;
      }
      CD[k]=best;
      /* ⚑ L'ECHELLE DE LA TRAME EST FIXE, ELLE NE SUIT PAS LA CELLULE.
         Les trames sont ancrees sur des pas ABSOLUS — pois tous les 9,
         tesselles tous les 11, carres tous les 5, sillons tous les 6. En
         etirant chaque dalle pour la faire tenir dans sa cellule, ce pas
         devenait quelconque : c'est pour ca que les motifs ne ressemblaient
         pas au design. Ici, un radian vaut toujours le meme nombre de pixels
         de trame, quelle que soit la cellule. Ce qui deborde se replie au
         MIROIR sur le rectangle inscrit. */
      /* la dalle entiere tient dans la cellule, un peu debordante pour ne pas
         laisser de couronne vide autour */
      /* ⚑ L'ECHELLE VIENT DE LA CELLULE DE LA DALLE, PAS DE LA BOITE DE SON
         DESSIN. Sur la Toile, une marque est dimensionnee par rapport a sa
         cellule ; une dalle de `touffe` deborde largement de la sienne (tiges,
         fleurs excentrees), et sa boite de dessin vaut le double. Caler cette
         boite-la sur la cellule de la sphere divisait ses fleurs par deux :
         elles sortaient en mouchetis. */
      CK[k]=Math.min(DA[best].cw/du, DA[best].ch/dv)*(o.remp||1.02);
      CU[k]=(S.u0[k]+S.u1[k])*0.5; CV[k]=(S.v0[k]+S.v1[k])*0.5;
    }
    S.__dal=CD; S.__ech=CK; S.__cu=CU; S.__cv=CV; S.__dalCle=TR.cle;
  }
  var _sk=(ENR||ILE);
  var CD=_sk?null:S.__dal, CK=_sk?null:S.__ech, CU=_sk?null:S.__cu, CV=_sk?null:S.__cv;

  /* ⚑ EN FLOTTANTS SIMPLES. La boucle de rendu lit huit tableaux par point ;
     en double precision c'est deux fois plus d'octets a faire passer, et le
     banc montre que c'est la BOUCLE qui domine, pas le versement. La precision
     simple suffit largement a des coordonnees comprises entre -1 et 1. */
  /* ⚑ CE QUI NE DEPEND PAS DE LA VUE SE CALCULE UNE FOIS.
     Le relief coute SIX evaluations de phi par point (une trentaine d'appels
     trigonometriques), le flux six de plus, et la lecture de la trame un tour
     de repere complet. Tout cela vit dans le repere de l'OBJET : la rotation
     n'y change rien. On le met en cache, et l'image ne paie plus que la
     projection, la lumiere et le versement — c'est ce que mesure le banc. */
  /* combien de pixels de trame pour un radian : la meme valeur partout */

  /* ⚠ LA CLE DU CACHE DOIT PORTER LES TRACES ET LES SIX, sinon deux cadres
     qui ne different QUE par la memoire des gestes se partagent le meme cache
     et sortent identiques — le piege exact de la livraison ou huit cadres
     etaient pixel pour pixel les memes. */
  var CLE=(TR.cle||'')+'|'+(o.kn||2.5)+'|'+(o.tflux||0)+'|'+PXR.toFixed(1)+'|'+LIBRE
          +'|t'+(o.tracesIncr?'i':(o.traces?o.traces.length+':'+(o.traces[0]?o.traces[0].L.toFixed(3):'0'):'0'))
          +'|s'+(o.six?o.six.map(function(z){return z.k.toFixed(2);}).join(','):'0')
          +'|p'+POUSSE.toFixed(3);
  if(S.__stCle!==CLE){
    var _PH=new Float32Array(N), _GX=new Float32Array(N), _GY=new Float32Array(N),
        _GZ=new Float32Array(N), _FX=new Float32Array(N), _FY=new Float32Array(N),
        _FZ=new Float32Array(N), _CI=new Int16Array(N), _PO=new Uint8Array(N),
        _EW=new Uint8Array(N);
    var e=0.013;
    /* le peigne : la direction qui sort HORIZONTALE a l'ecran, ramenee dans le
       repere de l'objet. Ses deux zeros tombent donc aux limbes. */
    var _CRN=[cl, 0, sl];
    for(i=0;i<N;i++){
      var x0=P[i*3], y0=P[i*3+1], z0=P[i*3+2];
      var am=ENV?enveloppe(x0,y0,z0,ENV):1;
      _PH[i]=am*phi(x0,y0,z0,REL);
      var gx=(phi(x0+e,y0,z0,REL)-phi(x0-e,y0,z0,REL))/(2*e)*am;
      var gy=(phi(x0,y0+e,z0,REL)-phi(x0,y0-e,z0,REL))/(2*e)*am;
      var gz=(phi(x0,y0,z0+e,REL)-phi(x0,y0,z0-e,REL))/(2*e)*am;
      var dt=gx*x0+gy*y0+gz*z0, kn=o.kn||2.5;
      var ax=x0+(gx-dt*x0)*kn, ay=y0+(gy-dt*y0)*kn, az=z0+(gz-dt*z0)*kn;
      var mm0=nrm3(ax,ay,az)||1;
      _GX[i]=ax/mm0; _GY[i]=ay/mm0; _GZ[i]=az/mm0;
      var fl0=champPoil(x0,y0,z0,o.tflux||0,o.peigneAxial?null:_CRN,o.traces), fm0=nrm3(fl0[0],fl0[1],fl0[2])||1;
      _FX[i]=fl0[0]/fm0; _FY[i]=fl0[1]/fm0; _FZ[i]=fl0[2]/fm0;
      _EW[i]=(_EPW*255)|0;
      /* ⚑ LA LECTURE DE LA TOILE ENROULEE.
         Lambert azimutale equivalente : k = racine(2/(1+z)), u = k x, v = k y.
         Le disque a pour rayon 2, on l'echelle en pixels par PXR. Aucun
         montage, aucun choix de dalle : le poil lit la Toile a l'endroit ou il
         se trouve, et c'est tout. */
      /* ⚑ LA FOURRURE D'ABORD, LES ILES DEDANS.
         Le sol (indice 0) couvre TOUTE la sphere : l'etat de repos est le
         peigne, pas le vide. Une ile est une tache de pelage d'une autre
         couleur — son bord ondule (bruit basse frequence) et il INTERPENETRE
         (une gigue a l'echelle de la fibre), sinon on lit de la peinture et
         non de la fourrure. */
      /* ⚑ LE SOL, ET LES DALLES DEDANS.
         Le sol (indice 0) couvre TOUTE la sphere : l'etat de repos est le
         peigne. Une ile est UNE VRAIE DALLE peinte par le moteur dans le monde
         de sa plantation : on projette le point dans le plan tangent de l'ile
         et on lit ce que le moteur y a peint. Hors matiere, c'est le sol.
         ⚠ La dalle ne se DEFORME pas avec la sphere : elle est posee a plat
         dans son plan tangent, comme un ecusson. Au-dela de ~0,3 rad la
         projection s'etirerait — une ile fait 0,215, on reste dedans. */
      if(ILE){
        var qi=0, _il9=null;
        for(var z9=0;z9<NIL;z9++){
          var I9=ILE[z9]; if(!I9.m) continue;
          var dp9=x0*I9.c[0]+y0*I9.c[1]+z0*I9.c[2];
          if(dp9 < 0.93) continue;                 /* trop loin : on saute vite */
          var u9=x0*I9.e1[0]+y0*I9.e1[1]+z0*I9.e1[2];
          var v9=x0*I9.e2[0]+y0*I9.e2[1]+z0*I9.e2[2];
          var tx9=(u9*I9.kk+I9.sx)|0, ty9=(v9*I9.kk+I9.sy)|0;
          if(tx9<0||ty9<0||tx9>=I9.mw||ty9>=I9.mh) continue;
          var mm9=I9.m[ty9*I9.mw+tx9];
          if(mm9){ qi=mm9; _il9=I9; break; }
        }
        /* ⚑ LA MEMOIRE DU GESTE — ce qui reste quand la forme est revenue.
         La deformation, elle, est reelle sur le moment et disparait : la
         silhouette n'est JAMAIS abimee. Ce qui reste, c'est le poil couche —
         un lustre, une chroma qui a monte, un grain oriente. Acquis du lot
         precedent : une trace n'est pas un creux, c'est une marque qui COUVRE
         PLUS. On la traite donc en montant de marche, jamais en creusant. */
      var _po=(o.traces&&o.traces.length)?m_poli(o.traces,x0,y0,z0):0;
      if(_po>0.12){
        var _gg=null,_bd=9;
        for(var _q=0;_q<o.traces.length;_q++){
          var _G=o.traces[_q];
          var _t=Math.atan2(x0*_G.d[0]+y0*_G.d[1]+z0*_G.d[2],
                            x0*_G.a[0]+y0*_G.a[1]+z0*_G.a[2]);
          if(_t<0)_t=0; else if(_t>_G.L)_t=_G.L;
          var _ct=Math.cos(_t),_st=Math.sin(_t);
          var _qx=_G.a[0]*_ct+_G.d[0]*_st,_qy=_G.a[1]*_ct+_G.d[1]*_st,_qz=_G.a[2]*_ct+_G.d[2]*_st;
          var _dp=x0*_qx+y0*_qy+z0*_qz; if(_dp>1)_dp=1;
          var _an=Math.acos(_dp);
          if(_an<_bd){_bd=_an;_gg=_G;}
        }
        if(_gg){
          var _pd=_gg.d[0]*x0+_gg.d[1]*y0+_gg.d[2]*z0;
          var _tx=_gg.d[0]-_pd*x0,_ty=_gg.d[1]-_pd*y0,_tz=_gg.d[2]-_pd*z0;
          var _tm=Math.hypot(_tx,_ty,_tz)||1;
          _FX[i]=_tx/_tm; _FY[i]=_ty/_tm; _FZ[i]=_tz/_tm;
        }
      }
      _PO[i]=(_po*255)|0;

      /* ⚠ LES SIX NE PASSENT PLUS PAR LE POLI. Ils l'ont fait un temps : une
         personne proche = une matiere plus saturee, en calotte. Ca sortait en
         taches, et surtout ca melangeait deux choses dans la meme variable —
         la main et les gens. Depuis, les six sont des EPIS : ils ecrivent le
         SENS du poil (voir `champPoil`), pas son ton. `_PO` ne porte donc plus
         qu'une seule chose : LA MEMOIRE DE LA MAIN. */

      /* ⚑ CHAQUE ILE A SON EPI : sur un vrai pelage, deux plages se
           distinguent par LE SENS DU POIL autant que par la couleur. */
        if(qi && _il9){
          var cc9=_il9.c;
          var pr9=x0*cc9[0]+y0*cc9[1]+z0*cc9[2];
          var rx9=x0-cc9[0]*pr9, ry9=y0-cc9[1]*pr9, rz9=z0-cc9[2]*pr9;
          var rm9=Math.sqrt(rx9*rx9+ry9*ry9+rz9*rz9);
          if(rm9>1e-4){
            rx9/=rm9; ry9/=rm9; rz9/=rm9;
            var tX=y0*rz9-z0*ry9, tY=z0*rx9-x0*rz9, tZ=x0*ry9-y0*rx9;
            var A9=0.74, B9=0.62;
            var wx=A9*rx9+B9*tX, wy=A9*ry9+B9*tY, wz=A9*rz9+B9*tZ;
            var wm=Math.sqrt(wx*wx+wy*wy+wz*wz)||1;
            _FX[i]=wx/wm; _FY[i]=wy/wm; _FZ[i]=wz/wm;
          }
        }
        _CI[i]=qi;
        continue;
      }
      if(ENR){
        /* on ramene le point dans le repere de la Toile enroulee : son centre
           regarde la vue, donc l'antipode (le seul defaut de Lambert) est
           derriere, la ou rien n'est peint. */
        var _zc=x0*TR.cx+y0*TR.cy+z0*TR.cz;
        var _xc=x0*TR.ax+y0*TR.ay+z0*TR.az;
        var _yc=x0*TR.bx+y0*TR.by+z0*TR.bz;
        var _kk=Math.sqrt(2/Math.max(1e-4,1+_zc));
        var _tu=(TR.sz*0.5+TR.pxr*_kk*_xc)*TR.dpr;
        var _tv=(TR.sz*0.5+TR.pxr*_kk*_yc)*TR.dpr;
        var _ix=_tu|0, _iy=_tv|0;
        _CI[i]=(_ix<0||_iy<0||_ix>=TR.iw||_iy>=TR.ih) ? -1 : TR.map[_iy*TR.iw+_ix];
        continue;
      }
      /* LA LECTURE DE LA TRAME — statique elle aussi */
      var cel0=S.cel[i];
      var wx0=x0-S.sx[cel0], wy0=y0-S.sy[cel0], wz0=z0-S.sz[cel0];
      var d0=DA[CD[cel0]], k0=CK[cel0];
      var tx0, ty0;
      if(true){
        /* ⚑ LE CONTOUR EST CELUI DE LA DALLE, POUR LES HUIT MONDES.
           Ce chemin etait reserve a encre, terrazzo et touffe. Les cinq trames
           lisaient leur RECTANGLE INSCRIT en rabattant l'echantillon sur son
           bord : la silhouette venait du pavage et le motif n'etait qu'un bout
           d'interieur recadre. D'ou « des formes a peu pres ressemblantes ».
           ⚠ Ce correctif avait deja ete tente, et RETIRE, parce qu'il vidait
           la sphere : la fourrure ne poussait plus que sur la matiere, et une
           trame est vide a 60-80 %. Il est tenable MAINTENANT, et seulement
           maintenant, parce que les cellules non plantees portent desormais le
           gris de la Toile : la boule reste pleine et ronde pendant que chaque
           dalle retrouve son propre bord. */
        var k0=CK[cel0];
        var u0=(wx0*S.e1[cel0*3]+wy0*S.e1[cel0*3+1]+wz0*S.e1[cel0*3+2]-CU[cel0])*k0;
        var v0=(wx0*S.e2[cel0*3]+wy0*S.e2[cel0*3+1]+wz0*S.e2[cel0*3+2]-CV[cel0])*k0;
        if(TR.parCell){ u0*=(TR.pxrpx||TR.pxr||1); v0*=(TR.pxrpx||TR.pxr||1); }
        /* et le centre est LA GRAINE de la dalle, pas le milieu de son dessin :
           une cellule est centree sur sa graine, pas sur ce qu'elle deborde. */
        tx0=(u0+d0.sx)|0; ty0=(v0+d0.sy)|0;
      } else {
        /* ⚑ MOSAIQUE, BRAILLE, PIXEL, SILLONS, GRAVURE : leur trame est DECOUPEE
           sur la cellule. Le contour vient donc du pavage (deja pose, arrondi
           aux coins) et l'image ne fournit que LA MATIERE — prise dans son
           interieur, au pas naturel, sans redimensionnement ni repli. */
        var u1=(wx0*S.e1[cel0*3]+wy0*S.e1[cel0*3+1]+wz0*S.e1[cel0*3+2])*PXR;
        var v1=(wx0*S.e2[cel0*3]+wy0*S.e2[cel0*3+1]+wz0*S.e2[cel0*3+2])*PXR;
        tx0=(d0.rx+d0.rw*0.5+u1)|0; ty0=(d0.ry+d0.rh*0.5+v1)|0;
        if(tx0<d0.rx)tx0=d0.rx; if(ty0<d0.ry)ty0=d0.ry;
        if(tx0>=d0.rx+d0.rw)tx0=d0.rx+d0.rw-1;
        if(ty0>=d0.ry+d0.rh)ty0=d0.ry+d0.rh-1;
      }
      var q0=(tx0<0||ty0<0||tx0>=d0.w||ty0>=d0.h) ? 0 : d0.m[ty0*d0.w+tx0];
      /* ⚑ SUR LA TOILE IL N'Y A AUCUN TROU : le canevas est ENTIEREMENT pave.
         Ce que je prenais pour des « ecarts noirs entre les dalles », ce sont
         des CELLULES SOMBRES qui portent la meme trame. Je sautais ces points :
         la sphere se trouait de noir, ce qui ne ressemble a rien de la Toile.
         Ici tout point peint quelque chose — la couleur de la dalle la ou il y
         a matiere, le ton sombre de la cellule partout ailleurs. */
      /* trame : le motif dit la matiere, la CELLULE dit la couleur.
         libre : la forme porte ses propres couleurs (petales, coeurs, eclats). */
      /* on range ensemble la couleur de la cellule et l'ecart de strate :
         seize valeurs de decalage suffisent (-8 a +7). */
      /* ⚠ LE SOL GRIS SE PAIE — MAIS PAS SUR UN MONDE CREUX.
         Remplir les cellules vides avait fait passer l'image de 22,8 a 36,7 ms :
         on l'avait donc dilue de moitie. Depuis, le poil a raccourci et le
         budget est revenu a 23,1 ms — et sur un monde ou la trame elle-meme
         est presque vide (touffe couvre 11 % de sa cellule, terrazzo 13 %),
         cette dilution acheve la boule : elle sort en lambeaux.
         On ne dilue donc QUE les mondes pleins. Le seuil est le remplissage
         releve par `bat_trames`, pas une devinette. */
      /* l'indice EST celui de la teinte reellement peinte sous la racine.
         Plus de paquetage couleur+strate : la couleur porte deja sa strate. */
      /* ⚑ UNE CELLULE VIDE PORTE LE MEME DESSIN, EN SOMBRE.
         Je la peignais en gris UNI : sur `touffe`, ses fleurs perdaient leur
         lisere creme et leur coeur, et les trois quarts de la boule n'avaient
         plus aucun dessin. Ce n'est pas ce que fait la Toile : une cellule sans
         Promi y porte exactement la meme trame, seulement sombre.
         On garde donc l'indice de la teinte reelle, decale de NCOL pour dire
         « celle-ci est vide » ; le versement la peindra sur la rampe grise, a
         la marche que dit son propre clair-obscur. */
      _CI[i]= q0
                ? ( S.plant[cel0] ? (q0-1)
                                  : ((DILUE && (i&1)) ? -1 : (NCOL+q0-1)) )
                : -1;
    }
    /* ⚑ ON RANGE LES POINTS PAR PLAQUES, ET ON ENTRELACE.
       Deux gains, et ce sont les derniers gros.
       1 · LE DOS NE SE VISITE MEME PLUS. Le tester point par point coute quatre
           produits par point, sur la moitie du semis. On decoupe la sphere en
           96 plaques, on trie les points dedans, et par image on ne teste que
           96 directions : les plaques tournees vers l'arriere ne sont jamais
           parcourues. Culling par plaque, pas par point.
       2 · TOUT CE QU'UN POINT PORTE TIENT DANS UNE SEULE BANDE DE MEMOIRE.
           La boucle lisait huit tableaux separes ; elle en lit un seul, de dix
           flottants par point, contigu. */
    /* ⚑ ON COMPACTE : un point qui ne peint rien ne doit meme pas exister.
       Depuis que l'entre-dalles reste vide, la plupart des candidats sont
       ecartes — et les visiter couterait le passage de boucle pour rien. On les
       supprime ICI, une fois, avant le tri par plaques. Le semis de depart peut
       donc etre tres dense sans que l'image le paie. */
    var GARDE=new Int32Array(N), NG=0;
    for(i=0;i<N;i++) if(_CI[i]>=0) GARDE[NG++]=i;
    var NP=96, PD=new Float32Array(NP*3), PID=new Int32Array(NG);
    for(var q2=0;q2<NP;q2++){
      var yq=1-2*(q2+0.5)/NP, rq=Math.sqrt(Math.max(0,1-yq*yq)), aq=q2*2.399963229728653;
      PD[q2*3]=Math.cos(aq)*rq; PD[q2*3+1]=yq; PD[q2*3+2]=Math.sin(aq)*rq;
    }
    /* la plaque la plus proche se lit dans une table (hauteur x azimut) :
       une recherche exhaustive coutait 96 produits PAR POINT, soit quarante
       millions a la construction. La table en coute huit cent mille, une fois.
       Une erreur de plaque au bord d'une case est sans effet : la marge de
       culling la couvre. */
    var GH=64, GA=128, LUT=new Int16Array(GH*GA);
    for(var gh=0;gh<GH;gh++){
      var zg=1-2*(gh+0.5)/GH, rg=Math.sqrt(Math.max(0,1-zg*zg));
      for(var ga=0;ga<GA;ga++){
        var ag=(ga+0.5)/GA*6.283185307179586;
        var xg=Math.cos(ag)*rg, yg=zg, zg2=Math.sin(ag)*rg, bq=0, bv=-9;
        for(q2=0;q2<NP;q2++){
          var dq=xg*PD[q2*3]+yg*PD[q2*3+1]+zg2*PD[q2*3+2];
          if(dq>bv){bv=dq;bq=q2;}
        }
        LUT[gh*GA+ga]=bq;
      }
    }
    var CNT=new Int32Array(NP+1);
    for(var gi=0;gi<NG;gi++){
      i=GARDE[gi];
      var xq=P[i*3], yq2=P[i*3+1], zq=P[i*3+2];
      var gh2=((1-yq2)*0.5*GH)|0; if(gh2<0)gh2=0; if(gh2>=GH)gh2=GH-1;
      var ang2=Math.atan2(zq,xq); if(ang2<0)ang2+=6.283185307179586;
      var ga2=(ang2/6.283185307179586*GA)|0; if(ga2>=GA)ga2=GA-1;
      var bq2=LUT[gh2*GA+ga2];
      PID[gi]=bq2; CNT[bq2+1]++;
    }
    for(q2=1;q2<=NP;q2++) CNT[q2]+=CNT[q2-1];
    var PST=new Int32Array(NP+1); PST.set(CNT);
    var Q=new Float32Array(NG*10), CIX=new Int16Array(NG), BRD=new Uint8Array(NG),
        POL=new Uint8Array(NG), EPW=new Uint8Array(NG);
    var pos=new Int32Array(NP);
    pos.set(CNT.subarray(0,NP));
    for(var gj=0;gj<NG;gj++){
      i=GARDE[gj];
      var d2=pos[PID[gj]]++, o2=d2*10;
      Q[o2]=P[i*3]; Q[o2+1]=P[i*3+1]; Q[o2+2]=P[i*3+2];
      Q[o2+3]=_GX[i]; Q[o2+4]=_GY[i]; Q[o2+5]=_GZ[i];
      Q[o2+6]=_PH[i];
      Q[o2+7]=_FX[i]; Q[o2+8]=_FY[i]; Q[o2+9]=_FZ[i];
      CIX[d2]=_CI[i]; BRD[d2]=S.bord[i]; POL[d2]=_PO[i]; EPW[d2]=_EW[i];
    }
    S.__st={Q:Q, ci:CIX, bd:BRD, pd:PD, pst:PST, np:NP, n:NG, po:POL, ew:EPW};
    S.__stCle=CLE;
  }
  var ST=S.__st, Q=ST.Q, CIX=ST.ci, BRD=ST.bd, PD=ST.pd, PST=ST.pst, NP=ST.np;
  var POL=ST.po, EPWA=ST.ew;
  N=ST.n;                                    /* le semis compacte */

  /* ⚑ SEUL LE DOIGT BOUGE — le reste ne se recalcule plus a chaque image.
     Le banc a fini par le dire : sur 27,4 ms a 90 000 poils, le versement en
     coute 3,3 et la projection 0,7. LES 23,4 AUTRES etaient dans la boucle de
     deformation, qui repassait sur TOUS les points a chaque image.
     Or elle est STATIQUE : positions, normales et champ de flux vivent dans le
     repere de l'objet. Elle ne dependait de la vue que par l'amorti au limbe —
     et celui-la se calcule a la PROJECTION, ou la profondeur est deja connue.
     Il ne reste donc, par image, que la calotte du contact : un produit
     scalaire par point pour la trouver, et la vraie geometrie pour les quelques
     milliers qui y tombent. On note ceux qu'on touche, et on les rend a l'image
     suivante. */
  if(!cv.__mod || cv.__mod.length<N){
    cv.__mod=new Uint8Array(N); cv.__tch=new Int32Array(N); cv.__ntch=0;
    cv.__dX=new Float32Array(N); cv.__dY=new Float32Array(N); cv.__dZ=new Float32Array(N);
    cv.__nX=new Float32Array(N); cv.__nY=new Float32Array(N); cv.__nZ=new Float32Array(N);
    cv.__pl=new Uint8Array(N);   cv.__om=new Float32Array(N);
    cv.__fX=new Float32Array(N); cv.__fY=new Float32Array(N); cv.__fZ=new Float32Array(N);
  }
  var MOD=cv.__mod, TCH=cv.__tch;
  var dX=cv.__dX, dY=cv.__dY, dZ=cv.__dZ, dNX=cv.__nX, dNY=cv.__nY, dNZ=cv.__nZ;
  var dPL=cv.__pl, dOM=cv.__om, dFX=cv.__fX, dFY=cv.__fY, dFZ=cv.__fZ;
  for(i=0;i<cv.__ntch;i++) MOD[TCH[i]]=0;
  cv.__ntch=0;
  /* ⚑ PORTAGE — la part d'effet du contact suit sa PROFONDEUR (voir fabrique.py) */
  var FE=E?Math.min(1,(E.d/(E.dmax||1))/0.3):0;
  if(E){
    var ccx=E.c[0], ccy=E.c[1], ccz=E.c[2], ntch=0;
    /* la calotte qui contient tout le contact : 3 fois le rayon, plus une marge */
    var ang=Math.min(1.50, 3.2*Math.max(E.aC,E.bC)+0.20), seuil=Math.cos(ang);
    for(i=0;i<N;i++){
      var qb=i*10, x=Q[qb], y=Q[qb+1], z=Q[qb+2];
      if(x*ccx+y*ccy+z*ccz < seuil) continue;
      var c1=contact(E,x,y,z);
      if(!c1) continue;
      var ph0=Q[qb+6];
      var nx=Q[qb+3], ny=Q[qb+4], nz=Q[qb+5];
      var X=x, Y=y, Z=z, pl=0, omb=0, rr=1+ph0, pei=0, pdx=0, pdy=0, pdz=0;
      if(c1.plat){
        var h=(1-E.d), pa=x*ccx+y*ccy+z*ccz;
        X=x+ccx*(h-pa); Y=y+ccy*(h-pa); Z=z+ccz*(h-pa);
        /* le fond plat, sa normale : ils rejoignent la matière naturelle avec FE */
        if(FE<1){ var q1=(1+ph0)*(1-FE); X=X*FE+x*q1; Y=Y*FE+y*q1; Z=Z*FE+z*q1; }
        nx=nx*(1-FE)+ccx*FE; ny=ny*(1-FE)+ccy*FE; nz=nz*(1-FE)+ccz*FE;
        var mF=nrm3(nx,ny,nz)||1; nx/=mF; ny/=mF; nz/=mF; pl=1; rr=1; omb=c1.ombre;
        pei=1; pdx=c1.dx; pdy=c1.dy; pdz=c1.dz;
      } else {
        var h2=0.020;
        var c2=contact(E,x+c1.dx*h2,y+c1.dy*h2,z+c1.dz*h2);
        var pente=((c2?c2.w:0)-c1.w)/h2;
        rr+=c1.w;
        X=x+c1.dx*c1.gl; Y=y+c1.dy*c1.gl; Z=z+c1.dz*c1.gl;
        var mm=nrm3(X,Y,Z)||1; X/=mm; Y/=mm; Z/=mm;
        nx-=c1.dx*pente; ny-=c1.dy*pente; nz-=c1.dz*pente;
        var m2=nrm3(nx,ny,nz)||1; nx/=m2; ny/=m2; nz/=m2;
        pei=1-lisse(1.05,2.40,c1.s); pdx=c1.dx; pdy=c1.dy; pdz=c1.dz;
      }
      pei*=FE;                         /* le poil peigné s'éteint avec le creux */
      if(!pl){ X*=rr; Y*=rr; Z*=rr; }
      var mr=nrm3(X,Y,Z);
      if(mr>1.05){ var f2=1.05/mr; X*=f2; Y*=f2; Z*=f2; }
      /* LE DOIGT PEIGNE LA FOURRURE : sous un pelage, un creux ne se lit pas a
         son ombre — les poils se rabattent en rosette, et c'est ca qu'on voit. */
      var fx0=Q[qb+7], fy0=Q[qb+8], fz0=Q[qb+9];
      if(pei>0){
        fx0=fx0*(1-pei)+pdx*pei; fy0=fy0*(1-pei)+pdy*pei; fz0=fz0*(1-pei)+pdz*pei;
        var fn2=nrm3(fx0,fy0,fz0)||1; fx0/=fn2; fy0/=fn2; fz0/=fn2;
      }
      dX[i]=X; dY[i]=Y; dZ[i]=Z; dNX[i]=nx; dNY[i]=ny; dNZ[i]=nz;
      dPL[i]=pl; dOM[i]=omb; dFX[i]=fx0; dFY[i]=fy0; dFZ[i]=fz0;
      MOD[i]=1; TCH[ntch++]=i;
    }
    cv.__ntch=ntch;
  }

  /* ⚑ DES TABLEAUX TYPES PREALLOUES, PAS DES push().
     Un `av.push(a,b,c)` sur un tableau JS ordinaire realloue, boxe et suit un
     type dynamique. Le banc donnait 0,34 microseconde par poil — dix fois le
     cout de la vingtaine de pixels qu'il ecrit. C'etait la. */
  if(!cv.__av || cv.__av.length<N*3){
    cv.__av=new Int32Array(N*3); cv.__ap=new Int32Array(N*3);
  }
  var av=cv.__av, ap=cv.__ap, nav=0, nap=0;
  /* ⚑ QUELLES PLAQUES SONT TOURNEES VERS NOUS ?
     Quatre-vingt-seize produits scalaires par image, et le dos n'est plus
     VISITE du tout — pas seulement rejete. Le tester point par point coutait
     quatre produits sur la MOITIE du semis ; ici on teste 96 directions, une
     fois. La marge de 0,26 couvre le rayon d'une plaque : aucun point du bord
     ne se perd. */
  var VU=cv.__vu||(cv.__vu=new Uint8Array(256));
  for(var pq=0;pq<NP;pq++){
    var px3=PD[pq*3], py3=PD[pq*3+1], pz3=PD[pq*3+2];
    var pzt=-px3*sl+pz3*cl;
    /* ⚠ J'AI ACCUSE LE CULLING A TORT, ET LA MESURE M'A REPRIS.
       Je lisais des facettes sur le bord et j'ai elargi ce seuil pour « rendre
       la frontiere aux points ». Mesure faite ensuite — 360 rayons tires du
       centre, on note ou la matiere s'arrete : rayon 296,3, ECART-TYPE 1,65,
       soit 0,56 %. La silhouette etait DEJA un cercle. Ce que je prenais pour
       des facettes, ce sont les grands plateaux clairs de la MATIERE, pas le
       contour. Seuil remis a sa valeur, et le surcout avec.
       (`scratchpad/mesure_rond.py` garde ce controle.) */
    VU[pq]= (py3*st+pzt*ct) > -0.26 ? 1 : 0;
  }
  for(var pq2=0;pq2<NP;pq2++){
   if(!VU[pq2]) continue;
   var iFin=PST[pq2+1];
   for(i=PST[pq2];i<iFin;i++){
    /* ⚑ ON SORT LE PLUS TOT POSSIBLE, avant la normale : le banc donne le
       cout d'un candidat a 0,73 fois celui d'un tampon peint, donc la BOUCLE
       compte autant que le versement.
       ⚠ ET ECLAIRCIR LE DOS EST UNE PERTE NETTE — mesure, contre mon intuition.
       Un point du dos garde son cout de boucle ; on n'economise que son
       tampon. Resultat : 35 956 poils a 18,40 ms avec un dos au tiers, contre
       36 453 a 16,40 ms avec le dos PLEIN et moins de candidats. On garde donc
       le dos entier (o.dos = 1) — il n'est la que pour le banc.
       Ancien commentaire, faux, garde pour memoire :
       Le banc donne le cout d'un candidat a 0,73 fois celui d'un tampon peint :
       la BOUCLE domine, pas le versement. Jeter un point apres avoir tourne sa
       position ET sa normale ne fait donc presque rien gagner. On calcule
       d'abord la seule profondeur (quatre produits), on decide, et on ne paie
       le reste que pour ce qui sera peint.
       Le dos ne garde qu'un point sur trois : il est a moitie transparent, on
       ne l'y lit pas, et ce budget rendu au devant fait la fourrure. */
    var mo=MOD[i], qb=i*10, X1,Y1,Z1,bnx,bny,bnz;
    if(mo){ X1=dX[i]; Y1=dY[i]; Z1=dZ[i]; bnx=dNX[i]; bny=dNY[i]; bnz=dNZ[i]; }
    else  { X1=Q[qb]; Y1=Q[qb+1]; Z1=Q[qb+2];
            bnx=Q[qb+3]; bny=Q[qb+4]; bnz=Q[qb+5]; }
    var Zt=-X1*sl+Z1*cl, Z2=Y1*st+Zt*ct;
    if(Z2<0) continue;                      /* le dos ne se peint plus */
    var ci=CIX[i];
    if(ci<0) continue;
    var strate=0;                      /* la strate vit dans la couleur, pas a cote */
    /* une cellule vide : meme trame, rampe grise, et son propre clair-obscur */
    if(ci>=NCOL){ strate=TDL[ci-NCOL]; ci=NCOL; }
    var X2=X1*cl+Z1*sl, Y2=Y1*ct-Zt*st;
    /* ⚑ L'AMORTI AU LIMBE SE FAIT ICI, plus dans la deformation : la
       profondeur est deja calculee, le relief ne coute donc rien de plus, et la
       boucle de deformation redevient entierement statique. La silhouette reste
       un cercle exact — c'est la meme loi, appliquee au meme endroit. */
    if(!mo){ var rrp=1+Q[qb+6]*p06(Z2>0?Z2:0);
             X2*=rrp; Y2*=rrp; Z2*=rrp; }
    var nX=bnx*cl+bnz*sl, nZt=-bnx*sl+bnz*cl, nY=bny*ct-nZt*st;
    var nZ2=bny*st+nZt*ct;
    var k=FOC/(FOC-Z2*R);
    var px=(CX+X2*R*k)|0, py=(CY+Y2*R*k)|0;
    /* ⚠ LA MARGE DE REJET APLATIT LA SILHOUETTE SI LA BOULE TOUCHE LE BORD.
       Un poil dont le tampon sortirait du tampon de pixels ecrirait sur la
       ligne suivante : on le rejette. Mais a R = 0,472 la boule laissait moins
       de marge que ca — le rejet lui coupait donc quatre MEPLATS, en haut, en
       bas, a gauche et a droite, et on lisait un polygone la ou la geometrie
       etait un cercle exact (rayon min 269 pour une moyenne de 295). Le rayon
       de la boule tient compte de la marge : voir `R` dans la planche. */
    if(px<26||py<26||px>W-26||py>W-26) continue;
    if(o.nuLum){
      /* ⚑ LE MODE DE MESURE — ECLAIRAGE PLAT. La luminance ne dit PAS la
         geometrie : sur une surface courbe vue de biais, une lumiere
         directionnelle fabrique un dipole clair/sombre qui noie le profil.
         Ici tout grain vaut pareil : l'image devient LA DENSITE PROJETEE du
         semis, c'est-a-dire la geometrie et rien d'autre. */
      if(Z2<0) continue;
      var spN=A[(1*ORI+(((i*2654435761)>>>0)%ORI))*NIVA+(NIVA-1)];
      ap.push(py*W+px, (1*ORI+(((i*2654435761)>>>0)%ORI))*NIVA+(NIVA-1), 3);
      continue;
    }
    /* ⚑ LA FIBRE REMONTE AVANT L'ECLAIRAGE — c'est tout le sujet.
       Un velours ne se lit pas a sa couleur : il se lit a son ANISOTROPIE.
       Sa clarte depend de l'angle entre LE POIL et la lumiere, pas seulement
       de la normale. C'est pour ca qu'un velours change quand on le tourne,
       et c'est ce qui le rend hypnotique. On avait la direction du poil sous
       la main — elle servait a orienter le tampon, dix lignes plus bas. */
    var fu,fv,fw;
    if(mo){ fu=dFX[i]; fv=dFY[i]; fw=dFZ[i]; }
    else  { fu=Q[qb+7]; fv=Q[qb+8]; fw=Q[qb+9]; }
    var fX=fu*cl+fw*sl, fZt=-fu*sl+fw*cl;
    var fY=fv*ct-fZt*st, fZv=fv*st+fZt*ct;      /* le poil, dans le repere de la VUE */
    /* ⚑ LE PEIGNE A UN SENS, MAIS PAS UN SEUL ANGLE.
       Depuis que la direction porte un biais, tous les poils d'une zone
       tombent dans LE MEME secteur sur vingt-quatre : le meme tampon, au meme
       angle, sur un semis quasi-regulier — et ca TISSE. C'est le
       « croisillon » : une moire entre le pas du semis et un motif unique.
       Sur un vrai pelage les poils suivent le peigne A PEU PRES, et c'est ce
       « a peu pres » qui fait le soyeux. On disperse donc l'angle de chaque
       poil autour du peigne, de facon deterministe.
       ⚠ ET LA DISPERSION SE POSE ICI, PAS AU MOMENT DU TAMPON. Posee juste
       avant `secteur`, elle ne tournait que le DESSIN ; le lustre, lui,
       continuait de lire le peigne moyen, donc tous les poils sortaient a la
       meme marche et la fourrure etait invisible sur sa peau. La fibre doit
       etre tournee UNE FOIS, et tout ce qui suit lit la fibre tournee. */
    var _ja=(((i*2246822519)>>>0)%2048/2048-0.5)*0.74;
    var _jc=Math.cos(_ja), _js=Math.sin(_ja);
    var _fx2=fX*_jc-fY*_js; fY=fX*_js+fY*_jc; fX=_fx2;

    var dl=nX*LX+nY*LY+nZ2*LZ; if(dl<0)dl=0;
    /* UN AMBIANT : sans lui la moitie de la boule est noire et la palette
       ne se voit nulle part. Le volume vient du contraste, pas du noir. */
    var fi=nX*FX2+nY*FY2+nZ2*FZ2; if(fi<0)fi=0;
    /* ⚑ ON OUVRE L'OMBRE. A 0,34 d'ambiant contre 0,52 de cle, la moitie de la
       boule tombait dans le noir : on ne pouvait ni lire ses dalles ni avoir
       envie d'y toucher. C'est ce que fait n'importe quel eclairage de studio
       — un remplissage qui OUVRE l'ombre au lieu de la boucher, sans effacer
       le volume, puisque c'est le CONTRASTE qui sculpte, pas le noir. */
    /* ⚑ ET L'ECLAIRAGE AUSSI. A 0,50 d'ambiant contre 0,40 de cle, un tiers de
       la boule restait trop sombre pour qu'on y lise une dalle : une dalle
       posee dans l'ombre etait simplement invisible, et « on ne se rend pas
       compte des ajouts ».
       Le volume ne vient pas du NOIR : il vient du lisere au limbe, du lustre
       de fibre et du relief du pelage — trois choses qu'on a deja. On peut
       donc ouvrir tres largement sans aplatir la sphere. */
    /* ⚑ MESURE, MOITIE PAR MOITIE : couverture 100 % des deux cotes, mais
       luminance 44 d'un cote et 77 de l'autre. Ce n'etait donc ni la densite
       de la fourrure ni un trou : c'etait LA CLE, encore trop forte. Une dalle
       posee du cote sombre etait simplement invisible — « on ne se rend pas
       compte des ajouts ». On aplatit franchement : le volume tient par le
       lisere au limbe et par le relief du pelage, pas par le noir. */
    /* ⚑ ET ON REND SON VOLUME A LA BOULE. J'avais aplati la cle a 0,12 pour
       compenser le degrade directionnel — qui ne venait pas de la lumiere mais
       du versement. Le defaut corrige, un eclairage plat n'a plus de raison
       d'etre : il donnait un aplat lilas sans relief. On remet une vraie cle. */
    /* ⚑ UN SEUL DEGRADE, DU HAUT-GAUCHE VERS LE BAS-DROITE.
       J'avais aplati la lumiere a 0,16 d'amplitude pour tuer les halos — et
       j'ai tue le volume avec : la boule sortait uniformement claire, sans
       aucun modele. Ce n'etait pas ce qu'il fallait faire. Ce qui creait les
       halos, c'etaient les termes qui posent un MOTIF (le lustre de fibre en
       bandes, le contre-jour en anneau, le lisere au limbe) — pas la cle.
       On rend donc toute son amplitude a LA CLE, et rien qu'a elle : la boule
       est claire du cote du titre « Aura », en haut a gauche, et elle descend
       en violet profond vers l'angle oppose. Aucun autre terme, donc aucun
       motif possible. */
    var lum=0.30+0.70*p074(dl);
    /* LE LISERE DU LIMBE : un vrai volume se signe par son bord. C'est aussi
       lui qui affirme le cercle exact — le contour se voit au lieu de se
       deviner. Terme de Fresnel : il ne depend que de l'angle de vue. */
    /* le lisere reste, mais discret : a 0,30 il creait a lui seul un ecart de
       trente points entre le centre et le bord. */
    /* ⚠ AUCUN TERME AU LIMBE, NI CLAIR NI SOMBRE. Un bord traite a part est un
       anneau, donc un halo. Le contour se lit tout seul : la matiere s'y voit
       de biais et le degrade y arrive a son terme. */

    /* ⚑ LE LUSTRE DE FIBRE (Kajiya-Kay). Un poil est un cylindre : il ne
       renvoie pas dans une direction mais sur un CONE. Le reflet n'est donc
       pas une tache, c'est une BANDE perpendiculaire au sens du peignage — et
       elle glisse quand la boule tourne. Aucune tache speculaire n'apparait :
       la regle du §6 de l'audit tient, parce que le terme ne depend que du
       SENS du poil. */
    if(o.velours){
      var tl=fX*LX+fY*LY+fZv*LZ;               /* poil . lumiere */
      var tv=fZv;                              /* poil . vue, la vue est (0,0,1) */
      var s1=1-tl*tl; s1=s1>0?Math.sqrt(s1):0;
      var s2=1-tv*tv; s2=s2>0?Math.sqrt(s2):0;
      var kk=s1*s2-tl*tv; if(kk<0)kk=0;
      var k2=kk*kk, k4=k2*k2;                  /* exposant 8, une bande large */
      lum+=o.velours*(0.26*s1*dl + 0.62*k4*k2);
    }

    /* ⚑ LE CONTRE-JOUR — la photo qui fait vendre.
       Un poil est TRANSLUCIDE : eclaire par derriere, sa pointe s'allume. Sur
       toute photographie de fourrure, c'est ce liseré-la qu'on regarde en
       premier. On l'allume la ou la normale s'eloigne de nous ET ou la fibre
       est de profil : le limbe s'ourle de lumiere sans que le centre bouge. */
    if(o.contre){
      var re=1-(nZ2<0?-nZ2:nZ2);
      var rr=re*re; rr*=rr;                    /* serré sur le limbe */
      var bl=-(nX*LX+nY*LY+nZ2*LZ); if(bl<0)bl=0;
      lum+=o.contre*(0.85*rr*(0.35+0.65*bl));
    }
    /* et ce qui se dresse prend un peu plus de jour : un relief accroche la
       lumiere, sinon il ne se voit pas. */
    if(o.dresse && ci>0 && ci<NCOL && (ILE?1:SAT[ci])) lum+=0.10*o.dresse;
    if(lum>1)lum=1;
    /* L'OMBRE PORTEE DANS LE CREUX : sans elle, le plateau est un disque pose */
    /* L'OMBRE PORTEE : le bord du cote de la lumiere jette son ombre sur le
       fond ; le fond d'en face reste eclaire. Sans elle, le plateau est un
       disque pose, pas un trou. */
    var dedans=(mo && dPL[i]===1);
    /* ⚠ ET LE FOND D'UN CREUX EST OCCULTE PAR SON PROPRE BORD.
       Sans ce facteur, le plateau ressortait PLUS CLAIR que le reste de la
       boule : sa normale regarde le doigt, donc la lumiere, et Lambert le
       recompensait — il montait jusqu'a la marche du reflet et l'empreinte
       sortait en cicatrice blanche. Un trou est sombre, meme quand sa surface
       est bien orientee. Ici : de 0,20 (le bord de la lumiere jette son ombre)
       a 0,82 (le fond d'en face, encore atteint). */
    if(dedans) lum*=1-FE*(1-(0.20+0.62*lisse(-0.55,0.62,-dOM[i])));   /* l'ombre du fond aussi */
    /* ⚑ ON LIT LA COULEUR DANS LA VRAIE DALLE, au pixel.
       Le point est ramene dans le plan tangent de sa cellule, mis a l'echelle
       de la dalle choisie, et on va chercher ce que le moteur a peint la. Hors
       de la dalle, c'est du vide : c'est ce vide qui fait le joint d'encre
       entre les dalles, et c'est la VRAIE FORME de la dalle qui le decoupe —
       jamais un polygone reconstruit (regle 1 du §4). */
    /* LA MARCHE : la lumiere fait monter la teinte d'une marche dans sa propre
       rampe. Un aplat franc, jamais un fondu — c'est la regle de la Toile. */
    /* ⚠ la rampe montait trop haut : la moitie des poils atteignait la marche
       du reflet et toute la sphere virait a la creme — la palette du Studio
       disparaissait sous son propre eclairage. */
    /* ⚠ une dalle de Toile est un APLAT. Trop de marches et la lumiere mange
       la couleur : les dalles se fondaient les unes dans les autres. */
    /* ⚠ plus contraste : le pixel et la mosaique ne se lisaient pas, leurs
       aplats tombaient tous dans deux marches voisines. */
    /* LA MARCHE : vingt marches, donc un eclairement CONTINU. La couleur de la
       dalle reste son aplat ; c'est la lumiere qui glisse dessus. */
    /* ⚠ et il faut que la MOYENNE tombe dans la partie COLOREE de la rampe.
       A lum x 19 le gros des poils atterrissait sur les trois dernieres marches
       — celles qui deteignent vers la creme — et la palette du Studio
       disparaissait sous son propre eclairage. Les hautes marches sont
       reservees aux vrais reflets. */
    /* ⚑ LA BOULE NE DOIT PAS ETRE PLUS SOMBRE QUE LA TOILE QU'ELLE ENROULE.
       La rampe part a -30 % de la couleur et monte a +60 % : avec le decalage
       precedent, le gros des poils atterrissait dans sa MOITIE BASSE, et la
       sphere sortait nettement plus eteinte que la Toile source — la comparer
       a l'image qu'on lui donne le montre d'un coup d'oeil. On recentre : la
       marche neutre (la couleur exacte du moteur) tombe a l'eclairement moyen. */
    /* ⚠ ET LA MARCHE MOYENNE DOIT TOMBER SUR LA COULEUR. La rampe part a
       -30 % : avec un decalage trop bas, le gros des poils atterrissait dans
       sa moitie sombre et la boule sortait eteinte quelle que soit sa teinte. */
    /* ⚠ ET IL NE FAUT PAS DEBORDER SUR LES MARCHES CREME. `rampeCouleur` finit
       par deux marches melangees a la creme (34 % puis 62 %) : ce sont des
       REFLETS, pas des tons. A +4,2 le gros des poils y atterrissait et la
       palette sortait kaki — mesure : la saturation moyenne tombait de 0,39 a
       0,25 quand les iles se multipliaient, alors qu'elle devrait MONTER.
       On monte l'exposition par la COULEUR (le sol part de 0,46 de clarte) et
       on garde la marche moyenne dans la partie coloree de la rampe. */
    /* ⚑ ET IL FAUT ENCORE DECALER LA RAMPE. Le sol atteint 96 de luminance
       une fois resolu, mais la boule rendait 47 : l'eclairage la divise par
       deux (l'ambiant vaut 0,34, la moyenne de `lum` tourne autour de 0,4).
       La marche moyenne tombait donc a 4 ou 5 sur vingt — dans le tiers
       sombre. On decale pour que l'eclairement moyen tombe sur la couleur. */
    /* ⚠ ET ON NE PEUT PAS MONTER PLUS SANS PERDRE LA COULEUR.
       A +5,6 la boule passe de 47 a 59 de luminance... et sa saturation tombe
       de 0,38 a 0,23. Ce n'est pas un reglage rate, c'est de la colorimetrie :
       monter la clarte d'une teinte la rapproche du blanc, et une teinte
       BLEU-VIOLET ne peut pas etre a la fois claire et saturee — le bleu ne
       pese que 11 % dans la luminance percue. On s'arrete donc au point ou la
       couleur tient encore, et le contraste se fait AILLEURS : entre le sol et
       les dalles, par des luminances etagees. */
    /* ⚑ LA TRACE DU GESTE : elle monte la chroma d'un ton et affine le grain.
       C'est tout ce qui reste quand la forme est revenue — jamais un creux. */
    var _po=POL?POL[i]/255:0, _ew=EPWA?EPWA[i]/255:0;
    /* ⚑ ET LA RAMPE S'ETALE POUR PORTER LE DEGRADE. A `lum x 12 + 3,6`, une
       lumiere allant de 0,30 a 1,00 ne parcourait que les marches 7 a 15 : le
       bas-droite ne descendait jamais dans le violet profond. On etale sur
       4 a 16 — le sombre existe vraiment, et les deux dernieres marches
       (celles qui deteignent vers la creme) restent hors d'atteinte. */
    /* ⚑ ET C'EST LE POIL QUI DOIT PORTER LE GRAIN, PAS LE TROU.
       Avant la peau, tout le dessin de la fourrure venait des pixels que
       personne ne couvrait : le fond d'encre transparaissait, et ces trous
       NOIRS faisaient le grain. C'est pour ca qu'elle sortait en gravier, et
       c'est pour ca qu'aucun degrade ne se voyait dessous.
       Sur un vrai velours le grain vient de l'ANGLE DE CHAQUE FIBRE : un poil
       en travers de la lumiere s'allume, un poil dans son axe s'eteint. C'est
       exactement le terme de Kajiya-Kay, mais applique a LA MARCHE d'un poil
       entier, pas en tache speculaire — il n'y a donc aucun reflet, seulement
       des poils un peu plus clairs et un peu plus sombres que leur voisinage.
       La dispersion d'angle posee plus bas (le « a peu pres » du peigne) suffit
       a le faire varier d'un poil a l'autre. */
    var _tl=fX*LX+fY*LY+fZv*LZ, _sn=1-_tl*_tl; _sn=_sn>0?Math.sqrt(_sn):0;
    /* ⚠ ET LA RAMPE NE DOIT PAS SATURER, SINON LE GRAIN DISPARAIT DANS LE
       CLAIR. A `lum x 19,4`, le cote eclaire tombait deja sur la derniere
       marche : la variation de fibre y etait ECRETEE, et la fourrure sortait
       lisse en haut a gauche et grenue en bas a droite — sans qu'on comprenne
       pourquoi. On laisse donc, aux deux bouts, la place du lustre. */
    /* ⚑ ET ON REMONTE LE NIVEAU GENERAL D'UNE MARCHE ET DEMIE. La boule
       sortait « legerement trop sombre » : le pied de la rampe partait a 2,2,
       donc le cote a l'ombre tombait presque dans l'encre. On releve le pied,
       on resserre un peu la course pour ne pas saturer le clair, et le lustre
       de fibre garde sa place aux deux bouts. */
    /* ⚑ ET ON REMONTE ENCORE LE PIED DE LA RAMPE. « Un peu trop sombre » :
       le cote a l'ombre partait trop bas, et sur une boule dont la moitie est
       dans l'ombre c'est la moyenne entiere qui descend. On releve le pied,
       on resserre la course pour ne pas ecreter le clair, et le lustre de
       fibre garde sa place aux deux bouts. */
    /* ⚠ ET LE LUSTRE PEUT ALLUMER UN POIL, PAS ETEINDRE UNE REGION. La ou le
       peigne pointe vers la lumiere, TOUS les poils du coin s'eteignent en
       meme temps : ca ne fait pas du grain, ca fait une TACHE SOMBRE — une
       salissure en haut a droite de la boule, au meme endroit sur les trois
       teintes. On borne donc le lustre par le bas : il eclaire librement, il
       n'assombrit que d'une marche. */
    /* ⚑ ET DANS UN EPI, LE POIL SE VOIT DEUX FOIS PLUS.
       Un epi ne se lit que si on SUIT LES BRINS qui tournent. Au contraste de
       la surface plate ils se fondaient dans leur peau, et on ne lisait qu'une
       ombre vague : Tom n'a ni vu ni compris le principe. On double donc
       l'amplitude du lustre a l'interieur de l'epi — le brin se detache de la
       peau, et c'est le TOUR qu'on lit, pas une tache. Et on allonge d'un cran
       (plus bas) : un poil que le peigne redresse est plus long a l'ecran. */
    /* ⚑ ET LA MAIN DOIT ETRE LA CHOSE LA PLUS VISIBLE AU REPOS.
       C'est la seule chose que personne d'autre n'a, et elle etait la moins
       lisible de l'ecran. Dans une caresse, le brin double de contraste (il se
       detache de sa peau, donc on SUIT le sens du geste) et la bande monte en
       ton et en chroma. Le reste de la boule est uniforme : c'est ce contraste
       entre l'uniforme et le peigne qui fait qu'on voit, SANS TOUCHER, que
       quelqu'un s'en occupe. */
    var _lu=(_sn-0.78)*(11.5+16.0*_ew); if(_lu<-1.0-1.4*_ew) _lu=-1.0-1.4*_ew;
    /* ⚑ LE LUSTRE DE LA MAIN. Une caresse couche quelques milliers de poils
       dans le meme sens : ce parallelisme RENVOIE mieux la lumiere, et c'est
       ca qu'on appelle un lustre. Sans ce terme, une bande peignee ne se
       distingue que par l'orientation de ses brins — et comme ils s'eteignent
       tous ensemble, elle sortait SOMBRE : une salissure, pas une caresse.
       Le poli monte donc le ton, et il monte aussi la chroma (l'etage de la
       table). C'est la seule chose que `_po` porte encore. */
    /* et le pelage qui pousse s'epaissit aussi EN COULEUR : plus dense, il
       laisse moins voir sa peau, donc il monte d'une marche. */
    var mar=((lum-0.30)*16.4+5.4+strate+_lu+_po*2.6+POUSSE*1.4)|0;
    if(mar>MARCHES-3)mar=MARCHES-3;      /* les deux dernieres restent des reflets */
    if(mar<0)mar=0; if(mar>MARCHES-1)mar=MARCHES-1;
    /* la profondeur et la place du Noyau decident de la PRESENCE, pas du ton */
    /* LA PLACE DU NOYAU — une CLAIRIERE, pas un evidement general.
       ⚠ A 0,52 de rayon, la rarefaction mangeait tout le milieu et la boule
       sortait en anneau : elle ne se lisait plus comme un volume. La regle est
       « la matiere se rarefie au centre pour leur laisser la place » — la
       place du Noyau, pas la moitie de la sphere. */
    var rho2q=X2*X2+Y2*Y2;
    /* ⚑ L'OMBRE SE PORTE AUSSI PAR L'OPACITE, PAS SEULEMENT PAR LA COULEUR.
       L'audit du 5 septembre l'avait annonce : « la palette d'un monde n'a pas
       l'ecart de luminosite de la creme sur l'encre — c'est cet ecart qui
       faisait le volume ; avec des dalles colorees, la sphere s'aplatit ». Et
       elle s'aplatissait : un disque a lisere, pas une boule. On rend cet
       ecart a la matiere en laissant le cote a l'ombre S'ETEINDRE VERS
       L'ENCRE. La palette reste exacte ; c'est sa PRESENCE qui baisse. */
    /* ⚠ MAIS LA MATIERE NE DISPARAIT PAS SOUS LE DOIGT : ELLE S'ASSOMBRIT.
       En laissant la presence suivre la lumiere DANS le creux, les dalles du
       contact devenaient si pales qu'on ne voyait plus la mosaique — un trou
       noir, pas un enfoncement. Dans le creux, la presence reste pleine ; c'est
       la MARCHE DE COULEUR qui descend. */
    /* la clairiere du Noyau, mesuree au carre : une racine de moins par poil */
    /* ⚠ LA CLAIRIERE DU NOYAU N'EST PAS UN TROU. A 0,07 de presence residuelle,
       le centre sortait en anneau noir franc — on lisait un trou perce, pas une
       matiere qui s'ecarte. On laisse du poil dessous. */
    /* ⚑ LA FOURRURE DOIT ETRE UNIFORME, SINON ON NE VOIT PLUS LES AJOUTS.
       Trois choses la faisaient varier, et aucune n'a plus lieu d'etre :
       1 · LE COTE A L'OMBRE ETAIT PLUS CLAIRSEME (x 0,62 + 0,38 lum). C'etait
           une economie de calcul deguisee en effet : la densite du pelage se
           mettait a dependre de L'ECLAIRAGE. Une fourrure ne se depeuple pas
           du cote de l'ombre. Supprime.
       2 · LA CLAIRIERE DU NOYAU creusait de 0,34 a 1 : un grand disque
           degarni au milieu, qui se lisait comme une calvitie. Elle reste —
           le Noyau a besoin de sa place — mais tres adoucie (0,80 a 1).
       3 · reste la profondeur, qui raccourcit les poils vers le limbe : celle-
           la est juste, c'est du raccourci geometrique, pas une variation de
           matiere.
       Sans uniformite, on ne peut pas voir qu'une dalle s'ajoute : le fond
       bouge autant qu'elle. */
    /* ⚠ PLUS DE CLAIRIERE DU TOUT. Meme adoucie a 0,80, elle sortait en
       grand disque sombre autour du Noyau — exactement le « halo bizarre »
       refuse. Le Noyau est creme sur un velours violet : il se detache tout
       seul, il n'a besoin d'aucune place qu'on lui degage. La fourrure est
       donc UNIFORME jusque sous lui. */
    var pres=1;
    var niv=(pres*NIVA)|0; if(niv>=NIVA)niv=NIVA-1; if(niv<0)niv=0;
    /* ⚑ LE SOL EST LONG, LA DALLE EST RASEE. */
    var zz=(Z2+1)*0.5, tai;
    if(ILE && ci>0 && TAI.length>1){
      tai=0;                                   /* la tonte */
    } else {
      /* ⚑ LE POIL POUSSE AVEC CE QU'ON A TENU — c'est ca, « la croissance se
         voit ». Une dalle de plus, ce n'est pas seulement une tache de plus :
         c'est un pelage un peu plus fourni, sur TOUTE la boule. Le critere 4
         du brief demande qu'on voie l'ajout d'un coup d'oeil ; une tache
         plantee sur la face cachee ne se voit pas, le pelage entier si.
         `pousse` va de 0 a 1 et ne redescend jamais. */
      var base0=(ILE&&TAI.length>1)?1:0;        /* le pelage : les longueurs hautes */
      var _zz=zz*(1-0.72*POUSSE)+0.72*POUSSE;   /* la pousse releve le plancher */
      tai=base0+((_zz*(TAI.length-base0))|0);
      if(tai>=TAI.length)tai=TAI.length-1; if(tai<base0)tai=base0;
    }
    /* le sol gris porte le grain le plus court : il fait le volume, pas le motif */
    if(ci>=NCOL && tai>0) tai--;
    /* couches, donc plus courts a l'ecran : un poil rabattu se raccourcit */
    if(mo && tai>0 && (((i*2654435761)>>>0)%1024)/1024 < FE) tai--;   /* le poil raccourci, TRAMÉ */
    /* ⚑ LE POIL NE RACCOURCIT PLUS AU BORD — ET C'EST LE COEUR DU FLUFFY.
       Il raccourcissait deux fois pres du filet, « pour que le contour reste
       net ». Mais un bord net, c'est justement ce qui fait une decoupe : la
       ou une fourrure se lit le plus, c'est AU BORD, quand les meches passent
       par-dessus le vide. Tom : « une boule qu'on a envie d'ecraser ».
       On garde donc la pleine longueur jusqu'au filet, et on ne raccourcit
       plus qu'au tout dernier rang — juste assez pour que deux dalles voisines
       ne se rejoignent pas et que le vide reste lisible (exigence 4). */
    var bo=BRD[i];
    /* ⚠ AUCUN FILET DE CELLULE DANS UNE FOURRURE. Le raccourcissement au bord
       d'une cellule dessinait le PAVAGE dans le pelage — or le pavage sort
       comme structure d'ensemble. On ne le garde que hors mode « iles ». */
    if(!ILE && bo<18 && tai>0) tai--;
    /* ⚑ LE LIMBE NE DOIT PAS ETRE UN CERCLE NET. La premiere chose que l'oeil
       lit d'une boule, c'est son contour : net, il dit « calcul » ; effiloche,
       il dit « fourrure ». Au limbe, le poil est vu de PROFIL — il est donc
       plus long a l'ecran, et il deborde. On lui rend cette longueur. */
    if(o.duvet){
      var lb=1-(nZ2<0?-nZ2:nZ2);
      if(lb>0.86 && tai<TAI.length-1) tai++;
    }
    /* ⚑ LES PROMI TENUS SE DRESSENT — et c'est la proposition la plus forte.
       Sur la Toile, 58 % des cellules sont grises : enroulees telles quelles,
       elles donnent « un globe gris avec des confettis ». Le sujet disparait.
       Ici le pelage d'une dalle PLANTEE est plus long : elle se tient PLUS HAUT
       que le fond, la lumiere rasante l'accroche, et sa silhouette deborde sur
       le gris. On ne change ni sa couleur ni son dessin — on lui donne du
       RELIEF. Ce qu'on a tenu est litteralement ce qu'on touche.
       Cout : nul. C'est un cran de taille de tampon. */
    if(o.dresse && ci>0 && ci<NCOL && (ILE?1:SAT[ci]) && tai<TAI.length-1) tai++;
    /* le poil couche est plus court a l'ecran : un velours peigne se tasse */
    if(_po>0.34 && tai>0) tai--;
    if(_ew>0.30 && tai<TAI.length-1) tai++;   /* le poil couche est plus long a l'ecran */
    var ori=secteur(fX,fY,ORI)*NVAR + (i%NVAR);
    if(o.sansBoucle){ nap+=3; continue; }
    /* ── SONDE : on releve ce qu'on DEPOSE, moitie par moitie de l'ecran ── */
    if(o.sonde){
      var hh2=(px<CX?0:1)+(py<CY?0:2);
      var SD=o.sonde;
      SD.n[hh2]++; SD.lum[hh2]+=lum; SD.mar[hh2]+=mar;
      SD.tai[hh2]+=tai; SD.niv[hh2]+=niv; SD.ci[hh2]+=ci;
    }
    /* le second etage de la table : la meme teinte, ressaturee */
    /* ⚠ ET LE SEUIL DOIT ETRE TIRE AU POIL, PAS FIXE. Un seuil franc sur une
       calotte donne un DISQUE a bord net : les six ressortaient en taches
       rondes saturees, la version chroma du defaut « des pois ronds qui ne
       correspondent a rien ». On tire le seuil par poil : la bascule d'etage
       devient un fondu granuleux, a l'echelle de la fibre — la seule maniere
       dont deux plages de pelage se rejoignent vraiment. */
    var _et=(_po>0.10+0.62*(((i*2654435761)>>>0)%1024/1024) && ci<NCOL)?ETAGE:0;
    if(Z2<0){ av[nav]=py*W+px; av[nav+1]=(tai*ORI*NVAR+ori)*NIVA+niv; av[nav+2]=_et+ci*MARCHES+mar; nav+=3; }
    else    { ap[nap]=py*W+px; ap[nap+1]=(tai*ORI*NVAR+ori)*NIVA+niv; ap[nap+2]=_et+ci*MARCHES+mar; nap+=3; }
   }
  }
  /* le tampon hors-ecran et son ImageData se GARDENT : les reallouer a chaque
     image coute plus cher que tout le versement. */
  if(!cv.__off || cv.__off.width!==W){
    cv.__off=document.createElement('canvas'); cv.__off.width=W; cv.__off.height=W;
    cv.__og=cv.__off.getContext('2d');
    cv.__im=cv.__og.createImageData(W,W);
    cv.__B=new Uint32Array(cv.__im.data.buffer);
  }
  var og=cv.__og, B=cv.__B;
  /* ⚑ UNE SEULE PASSE DE TAMPON, PLUS DEUX.
     Le banc donne 4,3 ms de cout FIXE — un quart du budget d'une image — et il
     part dans DEUX vidages de 608 000 mots, DEUX putImageData de 2,4 Mo et DEUX
     drawImage. Les six restent DEDANS (regle acquise) : on les trame dans le
     tampon lui-meme, entre le dos et le devant, au lieu de les dessiner sur le
     canevas entre deux versements. */
  /* ⚠ LES SIX ETAIENT PEINTS ENTRE LE DOS ET LE DEVANT — c'etait la regle
     « les six DEDANS et pas dessus ». Depuis que le dos n'est plus peint, la
     passe de dos est vide : les disques se retrouvaient sous toute la fourrure
     et ils ont DISPARU. On les pose donc apres la matiere, dans une clairiere
     d'encre qui les fait quand meme lire comme poses DANS le pelage. */
  B.fill(0);
  if(!o.sansVerse) verse(A,COL,av,nav,B,W);
  if(!o.sansVerse) verse(A,COL,ap,nap,B,W);
  if(!o.sansVerse && !o.sansPeau){
    if(!cv.__cb || cv.__cb.length!==W*W) cv.__cb=new Uint32Array(W*W);
    comble(B,W,cv.__cb);
  }
  /* les six passent au contexte, apres le versement : voir `disques` */
  /* la peau d'abord, la fourrure par-dessus */
  if(!o.sansVerse && !o.sansPeau){
    var PB=o.bloc||26, PK=peau(B,W,PB,o.omb,o.peauVers);
    if(!cv.__pk || cv.__pk.width!==PK.w){
      cv.__pk=document.createElement('canvas'); cv.__pk.width=PK.w; cv.__pk.height=PK.w;
      cv.__pg=cv.__pk.getContext('2d');
      cv.__pi=cv.__pg.createImageData(PK.w,PK.w);
      cv.__pb=new Uint32Array(cv.__pi.data.buffer);
    }
    cv.__pb.set(PK.d); cv.__pg.putImageData(cv.__pi,0,0);
    /* ⚠ ET LE BLOC DOIT ETRE GRAND DEVANT LE POIL. A sept pixels — la taille
       d'un poil — la peau est la fourrure elle-meme : elle annule son propre
       contraste et la boule sort en aplats lisses, sans un poil (essaye,
       regarde). Le bloc vaut donc trois a quatre poils : la peau devient une
       surface EOMBREE lente, et le grain du pelage se lit encore dessus.
       ⚠ Et on la DECOUPE AU CERCLE : un bloc a cheval sur le limbe deborderait
       de la silhouette, et un debord de peau autour d'une boule est un halo. */
    g.save();
    g.beginPath(); g.arc(CX,CY,R*1.012,0,TAU); g.clip();
    g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high';
    g.drawImage(cv.__pk, -PB*0.5, -PB*0.5, PK.w*PB, PK.w*PB);
    g.restore();
  }
  og.putImageData(cv.__im,0,0);
  g.drawImage(cv.__off,0,0);
  /* ⚠ PLUS AUCUNE PASTILLE. Les six et le Noyau sont maintenant DANS la
     matiere : une couronne et six epis (voir `champPoil`). Un disque pose
     par-dessus le velours, meme joli, est un trou perce dedans — et depuis
     que la proximite ne se lit plus dans la POSITION, il n'encodait plus rien.
     Le §3 est clair : un element colore qui ne porte ni sens ni action degage.
     `disques` et `noyau` restent dans le fichier, non appeles, le temps que
     Tom tranche. */
  if(o.pastilles){ disques(g,CX,CY,R,o.pal,o.six); noyau(g,CX,CY,R); }
  /* ⚑ LE PRENOM NE S'ECRIT QU'AU TOUCHER. Rien n'est lisible sur la Pelote
     pour un inconnu : on effleure un epi, le prenom parait, puis disparait. */
  if(o.effleure){
    var _E=o.six&&o.six[o.effleure.i||0];
    if(_E){
      var _kx=FOC/(FOC-_E.v[2]*R);
      var _px=CX+_E.v[0]*R*_kx, _py=CY+_E.v[1]*R*_kx;
      g.save();
      g.font='600 '+(0.070*R|0)+'px Gilbert,system-ui,sans-serif';
      g.textAlign='center'; g.textBaseline='middle';
      g.fillStyle='rgba(247,240,222,'+(o.effleure.a===undefined?0.94:o.effleure.a)+')';
      g.fillText(o.effleure.nom||'', _px, _py-0.115*R);
      g.restore();
    }
  }
  /* ⚑ LA PULPE, DESSINEE PAR-DESSUS, A L'ECHELLE. Ce n'est pas un element du
     produit : c'est un CALQUE DE MESURE, pour qu'on voie de ses yeux quelle
     part de la Pelote un vrai doigt couvre. Il ne s'affiche que si on le
     demande (`o.pulpe`).
     ⚠ Le trace est le contact VU DE FACE ; pose de biais sur la sphere il est
     un peu raccourci a l'ecran — l'ellipse dit la taille du doigt, pas la
     projection exacte de la zone touchee. */
  if(o.pulpe && o.emp){
    var Ep=o.emp, aC9=Ep.a*Math.pow(Ep.p===undefined?1:Ep.p,1/3), bi9=(Ep.biais||0)*aC9;
    /* le contact est decale de `biais` le long de son axe : le calque suit */
    var c0=Ep.c[0]+bi9*Ep.ax[0], c1=Ep.c[1]+bi9*Ep.ax[1], c2=Ep.c[2]+bi9*Ep.ax[2];
    var kk=FOC/(FOC-c2*R);
    var pxc=CX+c0*R*kk, pyc=CY+c1*R*kk;
    var aa=aC9*R, bb=aa*(Ep.el||0.62);
    g.save();
    g.beginPath(); g.ellipse(pxc,pyc,aa,bb,Math.atan2(Ep.ax[1],Ep.ax[0]),0,TAU);
    g.lineWidth=Math.max(1.4,0.0055*R); g.strokeStyle='rgba(247,240,222,.90)';
    g.setLineDash([Math.max(3,0.016*R), Math.max(3,0.016*R)]); g.stroke();
    g.restore();
  }
  if(E) cv.__emp=1;
  return {n:(nav+nap)/3, sites:S.sites, ms:+(performance.now()-t0).toFixed(1)};
}
/* ⚑ LE VERSEMENT — ecriture SEULE, sans relecture ni bornes.
   Mesure : 13,9 pixels par poil, 24 nanosecondes le pixel. Ce n'est pas le
   calcul, c'est l'ACCES DISPERSE dans un tampon de 2,4 Mo. La comparaison
   `a > (B[oo]>>>24)` ajoutait une LECTURE a chaque pixel — donc un defaut de
   cache de plus, et une dependance. On ecrit sans relire : le dernier pose
   gagne. C'est acceptable pour une fourrure (un poil en recouvre un autre,
   c'est ce que fait un pelage) et ca ne l'etait pas pour des grains isoles.
   Les bornes sautent aussi : les points sont deja bornes a 24 px du cadre et
   aucun tampon ne depasse cette taille. */
/* ⚑ LE VERSEMENT — ecriture SEULE, sans relecture ni bornes.
   Mesure : 13,9 pixels par poil, 24 nanosecondes le pixel. Ce n'est pas le
   calcul, c'est l'ACCES DISPERSE dans un tampon de 2,4 Mo. La comparaison
   `a > (B[oo]>>>24)` ajoutait une LECTURE a chaque pixel — donc un defaut de
   cache de plus, et une dependance. On ecrit sans relire : le dernier pose
   gagne. C'est acceptable pour une fourrure (un poil en recouvre un autre,
   c'est ce que fait un pelage) et ca ne l'etait pas pour des grains isoles.
   ⚠ Ranger d'abord les poils par bande d'ecran pour grouper les ecritures a
   ete essaye et MESURE : aucun gain (17,7 ms contre 17,3). Le comptage coute
   ce que le cache economise. Ne pas y revenir. */
/* ⚑ « LE DERNIER POSE GAGNE » FABRIQUAIT UN DEGRADE DIRECTIONNEL.
   C'etait une optimisation mesuree (-18 % par poil : on ecrit sans relire), et
   le commentaire disait « acceptable pour une fourrure, un poil en recouvre un
   autre ». Ce n'est PAS acceptable, et voici pourquoi.
   L'alpha d'un brin est FORT A LA RACINE et FAIBLE A LA POINTE. Le peignage a
   une direction dominante : du cote ou les poils pointent, ce sont donc les
   POINTES qui ecrasent les racines de leurs voisins ; du cote oppose, ce sont
   les RACINES. Resultat : une moitie de boule a 49 de luminance et l'autre a
   83 — a couverture egale (100 % des deux cotes) et a eclairage egal (la sonde
   donne lum 1,00 et 0,95 dans les quatre quarts, et le quart le PLUS clair en
   lum est le plus SOMBRE a l'ecran).
   Trois hypotheses ont ete essayees et mesurees avant de trouver : aplatir la
   cle (aucun effet), supprimer les variations de densite (aucun effet),
   densifier de 2,3 fois (ca EMPIRE : dispersion 44 -> 52 %).
   ⚑ La parade tient en un test : ON GARDE LE PLUS OPAQUE. L'alpha etant dans
   l'octet de poids fort, comparer les entiers compare les alphas — c'est donc
   un « max » a une comparaison, et non un vrai melange. */
/* ⚑ LA PEAU SOUS LA FOURRURE — CE QUI FAISAIT LE « GRAVIER ».
   Mesure : 6,9 % du disque restait a l'ENCRE, parce qu'aucun poil n'y tombait.
   Le fond du canevas se voyait donc entre les poils, en tirets noirs — et on
   ne lisait plus un velours, on lisait du gravier. Pire : ces trous sont un
   BRUIT A HAUTE FREQUENCE reparti uniformement, donc ils ecrasent le degrade,
   qui est une variation lente. Tant qu'ils sont la, aucun eclairage ne se voit.
   Un vrai pelage a une PEAU dessous : entre deux poils on ne voit pas le vide,
   on voit la bete. On comble donc les trous avec ce que leurs voisins ont
   depose — la vraie couleur du lieu, dalle comprise.
   ⚠ ET SEULEMENT LES TROUS ENTOURES. On exige au moins DEUX voisins peints sur
   quatre : un pixel du dehors n'en a pas, donc la silhouette ne bave pas d'un
   pixel. C'est ce qui distingue un comblement d'une dilatation.
   Cout : une lecture lineaire du tampon, et un travail reel sur 7 % des pixels. */
/* ⚠ ET LE COMBLEMENT SE LIT SUR UNE COPIE, JAMAIS SUR LUI-MEME.
   Ecrit en place, un balayage en lignes utilise comme voisin CE QU'IL VIENT DE
   COMBLER : le remplissage se propage vers le bas et vers la droite, et la
   boule sortait avec UN ESCALIER DE RECTANGLES qui bavait hors du limbe, en
   bas a droite seulement — la direction du balayage. C'est l'asymetrie qui
   trahit ce bug : un defaut de geometrie serait symetrique. */
function comble(B,W,C){
  var n=W*W, w=W;
  C.set(B);
  for(var o2=w+1;o2<n-w-1;o2++){
    if(C[o2]!==0) continue;
    var a=C[o2-1], b=C[o2+1], c=C[o2-w], d=C[o2+w], k=0, mx=0;
    if(a){k++; if(a>mx)mx=a;}
    if(b){k++; if(b>mx)mx=b;}
    if(c){k++; if(c>mx)mx=c;}
    if(d){k++; if(d>mx)mx=d;}
    if(k>=2) B[o2]=mx;
  }
  /* ⚠ ET NON, ON NE REND PAS LA FOURRURE OPAQUE. Essai fait et regarde :
     forcer alpha a 255 sur tout l'interieur EFFACE LE PELAGE. Toute la forme
     d'un poil vit dans son ALPHA — la couleur, elle, est un aplat de marche.
     Opacifier, c'est donc remplacer la fourrure par des aplats : la boule est
     sortie en bandes lisses, sans un poil. Le bord doux du tampon n'est pas un
     defaut a corriger, c'est le dessin lui-meme. Ce qu'il faut, c'est lui
     donner autre chose que du NOIR dessous — voir `peau`. */
}
/* ⚑ LA PEAU — CE SUR QUOI LE POIL SE COMPOSE.
   Le bord d'un tampon de poil est doux : sur le pourtour son alpha tombe a 60
   ou 100. Comme le versement ne garde que le plus opaque, une foule de pixels
   restent a mi-alpha — et ils se composent avec L'ENCRE DU FOND. Resultat :
   des tirets noirs partout, un gravier a haute frequence, uniformement
   reparti, qui ECRASE le degrade (une variation lente ne se voit pas sous un
   bruit fort). Mesure : 6,9 % du disque sous 40 de luminance.
   ⚠ Et on ne corrige pas ca en opacifiant la fourrure : toute la forme d'un
   poil vit dans son alpha, l'opacifier la remplace par des aplats (essaye,
   regarde, revenu).
   Un pelage a UNE PEAU. On la fabrique a partir du depot lui-meme : on reduit
   le tampon par blocs, chaque bloc prend la couleur de son pixel le plus
   opaque, et on redilate en lissage bilineaire. C'est donc, par construction,
   LA COULEUR DU LIEU — dalles comprises, sans un calcul de plus. Le poil se
   fond alors dans ses voisins au lieu de se fondre dans le vide.
   L'alpha d'un bloc suit sa part peinte : au limbe la peau s'eteint avec la
   fourrure, et rien ne deborde de la silhouette. */
function peau(B,W,BLOC,OMB,VERS){
  OMB=OMB===undefined?0.64:OMB;
  var SW=Math.ceil(W/BLOC), out=new Uint32Array(SW*SW), frc=new Float32Array(SW*SW);
  for(var by=0;by<SW;by++){
    var y0=by*BLOC, y1=Math.min(W,y0+BLOC);
    for(var bx=0;bx<SW;bx++){
      var x0=bx*BLOC, x1=Math.min(W,x0+BLOC), sr=0, sg=0, sb=0, sw=0, np=0, tot=0;
      for(var y=y0;y<y1;y++){
        var b=y*W;
        for(var x=x0;x<x1;x++){
          var v=B[b+x]; tot++;
          if(v!==0){ np++;
            var al=(v>>>24)/255;
            sr+=(v&255)*al; sg+=((v>>>8)&255)*al; sb+=((v>>>16)&255)*al; sw+=al; }
        }
      }
      if(!np||!sw){ out[by*SW+bx]=0; frc[by*SW+bx]=0; continue; }
      frc[by*SW+bx]=np/tot;
      /* ⚑ ET LA PEAU EST PLUS SOMBRE QUE LE POIL — C'EST LA TOUTE LA DENTELLE.
         Peau et poil de la MEME couleur, le pelage devient invisible : il ne
         reste qu'un daim un peu bruite, et toute la delicatesse du poil est
         perdue (mesure a l'oeil, cadre par cadre). Sur une vraie fourrure, le
         FOND entre les fibres est a l'ombre — c'est de l'occlusion, pas un
         trou : chaque poil se detache alors comme un trait clair sur un fond
         legerement plus sombre, et c'est ce contraste-la qui fait la dentelle.
         On assombrit donc la peau d'un facteur, sans toucher a sa teinte. Le
         gravier ne revient pas : le fond reste LA COULEUR DU LIEU, jamais
         l'encre. */
      var rr, gg, bb;
      if(VERS){ var tv=VERS[3]; rr=(sr/sw*(1-tv)+VERS[0]*tv)|0; gg=(sg/sw*(1-tv)+VERS[1]*tv)|0; bb=(sb/sw*(1-tv)+VERS[2]*tv)|0; }
      else { rr=(sr/sw*OMB)|0; gg=(sg/sw*OMB)|0; bb=(sb/sw*OMB)|0; }   /* ⚑ PORTAGE — la peau claire (fabrique.py) */
      out[by*SW+bx]=((bb<<16)|(gg<<8)|rr)>>>0;
    }
  }
  /* ⚠ ET LA PEAU S'ARRETE AVANT LE LIMBE, PAS APRES.
     Un bloc a cheval sur le bord est a moitie peint : lui donner un alpha
     proportionnel laissait sortir DES CARRES DE COULEUR autour de la boule —
     un debord rectangulaire, donc pire qu'un halo. Un decoupage au cercle ne
     suffit pas non plus : le rayon de la silhouette n'est pas exactement celui
     du modele, et il reste soit un anneau de peau, soit un anneau d'encre.
     On EROSE : un bloc n'est opaque que si LUI ET SES QUATRE VOISINS sont
     pleins. La peau se termine donc un bloc AVANT le bord, et c'est la
     fourrure — qui, elle, est antialiasee — qui dessine seule la silhouette. */
  var out2=new Uint32Array(SW*SW);
  for(var j=0;j<SW;j++){
    for(var k2=0;k2<SW;k2++){
      var id=j*SW+k2;
      if(!out[id]) continue;
      var f0=frc[id];
      if(k2>0) f0=Math.min(f0,frc[id-1]);   else f0=0;
      if(k2<SW-1) f0=Math.min(f0,frc[id+1]); else f0=0;
      if(j>0) f0=Math.min(f0,frc[id-SW]);   else f0=0;
      if(j<SW-1) f0=Math.min(f0,frc[id+SW]); else f0=0;
      var a2=(255*(f0-0.72)/0.26)|0; if(a2<0)a2=0; if(a2>255)a2=255;
      if(a2) out2[id]=(((a2<<24)>>>0)|(out[id]&0x00FFFFFF))>>>0;
    }
  }
  return {w:SW, d:out2};
}
function verse(A,COL,L,n,B,W){
  var OF=A.__off, AL=A.__alp, ST=A.__sta;
  for(var i=0;i<n;i+=3){
    var t=L[i+1], a=ST[t], b2=ST[t+1], bas=L[i], col=COL[L[i+2]];
    for(var j=a;j<b2;j++){
      var o2=bas+OF[j], v=(AL[j]|col)>>>0;
      if(v>B[o2]) B[o2]=v;
    }
  }
}
/* les six, trames DANS le tampon pour qu'ils restent dedans */
/* ⚑ « ON VOIT LES HALOS AU PIXEL » — et c'etait exactement ca.
   Les six se dessinaient DANS LE TAMPON DE PIXELS, cercle par cercle, avec un
   test `d2 > r2` : aucun antialiasing possible, donc un bord en escalier. Et
   ils portaient un HALO D'ENCRE de treize millemes du rayon, c'est-a-dire une
   ombre portee deguisee — l'un des trois interdits qui font le « cheap ».
   On les redessine au CONTEXTE 2D, apres le versement : les arcs y sont
   antialiases par le navigateur, et le halo saute. Un anneau de leur propre
   couleur suffit a les detacher du velours.
   ⚠ Et leur POSITION n'encode plus rien : la proximite se lit dans la MATIERE
   (voir `o.six` dans le peintre). On les pose donc a intervalle egal. */
function disques(g,CX,CY,R,PAL,SX){
  var n=SIX.length;
  for(var i=0;i<n;i++){
    var th=i/n*TAU+0.4, rho=0.62;
    var x0=CX+Math.cos(th)*rho*R, y0=CY+Math.sin(th)*rho*R*0.46;
    var r=0.045*R, ep=Math.max(1.6,0.0115*R);
    var c=PAL[i%PAL.length];
    g.beginPath(); g.arc(x0,y0,r,0,TAU);
    g.fillStyle='rgba(29,21,1,.86)'; g.fill();
    g.beginPath(); g.arc(x0,y0,r-ep*0.5,0,TAU);
    g.lineWidth=ep; g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';
    g.stroke();
  }
}
/* LES SIX ET LE NOYAU — la couleur d'un disque dit la Nuee (acquis).
   Rien ne passe devant ton Noyau : il est peint en dernier. */
/* ⚠ LES COTES DU DECOR SE PRENNENT SUR LA BOULE, PAS EN PIXELS ABSOLUS.
   En dur (21 px, 12,5 px), le Noyau et les six restaient de la meme taille
   quand le cadre passait de 620 a 200 px : sur les petits formats ils
   mangeaient la moitie de la sphere. */
function decor(g,CX,CY,R,PAL){
  for(var i=0;i<SIX.length;i++){
    var th=SIX[i][0], rho=SIX[i][1];
    var x=CX+Math.cos(th)*rho*R, y=CY+Math.sin(th)*rho*R*0.46, r=0.047*R;
    var c=PAL[i%PAL.length];
    g.beginPath(); g.arc(x,y,r+0.013*R,0,TAU);
    g.fillStyle='rgba(29,21,1,.88)'; g.fill();
    g.beginPath(); g.arc(x,y,r,0,TAU);
    g.fillStyle='rgba(29,21,1,1)'; g.fill();
    g.lineWidth=Math.max(1.4,0.0105*R); g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')'; g.stroke();
  }
}
function noyau(g,CX,CY,R){
  /* plus petit, et cercle d'encre autour : au diametre precedent il perçait un
     trou dans la composition au lieu d'y tenir sa place. */
  /* ⚠ PLUS DE HALO D'ENCRE. Un disque sombre de trois centiemes du rayon
     AUTOUR du Noyau, c'est une ombre portee — un des trois interdits. Le Noyau
     est creme sur un velours violet : il se detache tout seul. On garde un
     filet mince, de la couleur du fond, pour qu'il ne bave pas dans la
     matiere — un filet n'est pas un halo. */
  var r=0.080*R;
  g.beginPath(); g.arc(CX,CY,r+Math.max(1.2,0.006*R),0,TAU);
  g.fillStyle='rgba(29,21,1,.80)'; g.fill();
  g.beginPath(); g.arc(CX,CY,r,0,TAU); g.fillStyle='#F7F0DE'; g.fill();
}

/* ════════════════════════════════════════════════════════════════════════════
   ⚑ PORTAGE DANS L'APP — 10 septembre 2026. LA SEULE ADDITION AU MOTEUR.
   Mesuré au profileur : inscrire UNE caresse refaisait tout le cache statique des
   110 000 poils — le relief `phi` compris, qui ne dépend pas des caresses — soit 240 à
   340 ms d'image figée. `retoucheTraces` ne recalcule QUE les points proches des arcs
   qui entrent ou qui sortent, et l'écrit dans le cache compacté (`S.__st`), avec EXACTEMENT
   la logique de la passe statique : champ du poil (peigne azimutal + caresses), lustre de
   la main, sens de l'arc le plus proche au-delà de 0,12 de poli — et une île garde son épi.
   ════════════════════════════════════════════════════════════════════════════ */
function retoucheTraces(ST, anciennes, nouvelles){
  if(!ST) return 0;
  anciennes=anciennes||[]; nouvelles=nouvelles||[];
  var Q=ST.Q, CIX=ST.ci, POL=ST.po, EPW=ST.ew, N=ST.n, ch=[], k, i;
  function dans(L,g){ for(var z=0;z<L.length;z++) if(L[z]===g) return true; return false; }
  for(k=0;k<anciennes.length;k++) if(!dans(nouvelles,anciennes[k])) ch.push(anciennes[k]);
  for(k=0;k<nouvelles.length;k++) if(!dans(anciennes,nouvelles[k])) ch.push(nouvelles[k]);
  if(!ch.length) return 0;
  var CM=[], CR=[];
  for(k=0;k<ch.length;k++){ var g=ch[k], h=g.L/2, c=Math.cos(h), s=Math.sin(h);
    CM.push([g.a[0]*c+g.d[0]*s, g.a[1]*c+g.d[1]*s, g.a[2]*c+g.d[2]*s]);
    CR.push(Math.cos(Math.min(Math.PI, h+g.w+0.05))); }
  var n=0, T=nouvelles;
  for(i=0;i<N;i++){
    var qb=i*10, x0=Q[qb], y0=Q[qb+1], z0=Q[qb+2], pris=false;
    for(k=0;k<CM.length;k++) if(x0*CM[k][0]+y0*CM[k][1]+z0*CM[k][2]>=CR[k]){ pris=true; break; }
    if(!pris) continue;
    n++;
    var fl0=champPoil(x0,y0,z0,0,null,T), fm0=nrm3(fl0[0],fl0[1],fl0[2])||1;
    var fx=fl0[0]/fm0, fy=fl0[1]/fm0, fz=fl0[2]/fm0;
    EPW[i]=(_EPW*255)|0;
    var _po=T.length?m_poli(T,x0,y0,z0):0;
    if(_po>0.12){
      var _gg=null,_bd=9;
      for(var _q=0;_q<T.length;_q++){
        var _G=T[_q];
        var _t=Math.atan2(x0*_G.d[0]+y0*_G.d[1]+z0*_G.d[2], x0*_G.a[0]+y0*_G.a[1]+z0*_G.a[2]);
        if(_t<0)_t=0; else if(_t>_G.L)_t=_G.L;
        var _ct=Math.cos(_t),_st=Math.sin(_t);
        var _qx=_G.a[0]*_ct+_G.d[0]*_st,_qy=_G.a[1]*_ct+_G.d[1]*_st,_qz=_G.a[2]*_ct+_G.d[2]*_st;
        var _dp=x0*_qx+y0*_qy+z0*_qz; if(_dp>1)_dp=1;
        var _an=Math.acos(_dp);
        if(_an<_bd){_bd=_an;_gg=_G;}
      }
      if(_gg){
        var _pd=_gg.d[0]*x0+_gg.d[1]*y0+_gg.d[2]*z0;
        var _tx=_gg.d[0]-_pd*x0,_ty=_gg.d[1]-_pd*y0,_tz=_gg.d[2]-_pd*z0;
        var _tm=Math.hypot(_tx,_ty,_tz)||1;
        fx=_tx/_tm; fy=_ty/_tm; fz=_tz/_tm;
      }
    }
    POL[i]=(_po*255)|0;
    if(CIX[i]===0){ Q[qb+7]=fx; Q[qb+8]=fy; Q[qb+9]=fz; }   /* une île garde son épi */
  }
  return n;
}

try{ window.PeloteMoteur={atlasAlpha:atlasAlpha, GRAIN_POIL:GRAIN_POIL, ORI:ORI, NIVA:NIVA,
  NVAR:NVAR, semisPavage:semisPavage, batIles:batIles, peint:peint, m_gestes:m_gestes,
  retoucheTraces:retoucheTraces}; }catch(e){}
})();
