/* ════════════════════════════════════════════════════════════════════════════
   LE VELOURS — LA MATIERE EST UN TRAITEMENT DE SURFACE, PAS UN DESSIN

   ⚑ CE QUE LE LOT PRECEDENT A PROUVE, ET CE QU'IL A RATE.
   Prouve : chaque monde peut donner une loi d'implantation, et la collision
   d'echelles disparait. Rate, et Tom l'a dit en deux phrases :
     « les poils donnent pas envie de caresser, ca fait cheap visuellement »
     « ca doit etre les VRAIES dalles »
   Les deux reproches n'en font qu'un. En redessinant chaque monde en fibres
   j'ai produit HUIT APPROXIMATIONS — braille en etoiles au lieu de points,
   mosaique en briques decalees au lieu d'une grille, gravure en fougeres au
   lieu de hachures, pixel sans son escalier. Et pour que le motif survive, il
   fallait des brins assez gros pour se voir un par un : c'est exactement ce
   qui fait cheap. A cette echelle, une vraie soie NE MONTRE AUCUN POIL.

   ⚑ LE RENVERSEMENT.
   Le moteur sait deja peindre la vraie dalle : `Toile.dalleTrame(cv,pid,1)`
   la rend dans sa vraie cellule ponderee, a l'echelle 1, avec sa vraie trame,
   son vrai pas, sa vraie couleur et ses vraies strates. Aucune approximation
   n'est possible : c'est LE moteur. On ne la redessine plus.
   La matiere devient alors ce qu'elle est dans un vrai textile : un
   TRAITEMENT DE SURFACE. Pas un poil dessine, mais
     · un effilochage de chaque bord, plus fin que l'oeil ne resout,
     · un grain anisotrope couche dans le sens du peignage,
     · un lustre qui suit ce peignage,
     · un duvet retro-reflectif la ou la matiere s'arrete.
   Aucun brin n'est jamais trace. On ne peut donc plus en distinguer un.

   ⚠ CE N'EST PAS LE REJET CAPITAL DE L'AUDIT §2. Ce qui est abandonne a tout
   jamais, c'est de prendre l'IMAGE d'une dalle pour DECOUPER une autre forme
   — des fausses dalles detourees. Ici la dalle n'est ni redimensionnee ni
   detouree ni deplacee : le moteur la peint dans SA cellule, et on ne touche
   qu'a la surface. Le contour reste celui que le moteur a calcule.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var DPR=Math.min(2,window.devicePixelRatio||1);

/* ── un bruit de valeur, deterministe et lisse ─────────────────────────────
   (deterministe : meme Orbite, meme grain — exigence du semis, audit §4) */
function hh2(ix,iy){
  var x=(ix*374761393+iy*668265263)>>>0;
  x=((x^(x>>>13))*1274126177)>>>0;
  return ((x^(x>>>16))>>>8)/16777216;
}
function bruit(x,y){
  var ix=Math.floor(x),iy=Math.floor(y),fx=x-ix,fy=y-iy;
  fx=fx*fx*(3-2*fx); fy=fy*fy*(3-2*fy);
  var a=hh2(ix,iy),b=hh2(ix+1,iy),c=hh2(ix,iy+1),d=hh2(ix+1,iy+1);
  return a+(b-a)*fx+(c-a)*fy+(a-b-c+d)*fx*fy;
}
/* ⚑ LE TREILLIS GAUFRE ETAIT UN REPLIEMENT DE SPECTRE, PAS UNE GRILLE.
   J'avais ajoute deux octaves PLUS HAUTES pour casser le reseau du bruit de
   valeur. A x4,41 en travers, leur periode tombait a 0,26 px de cellule —
   soit 0,5 px reel, tres en dessous de l'echantillonnage. Une frequence qu'on
   ne peut pas representer ne disparait pas : elle SE REPLIE, en moire large.
   D'ou un gaufrage de 8 px en travers d'une dalle, alors que je croyais
   ajouter du grain fin.
   La regle : la plus fine octave est celle du pixel, et toutes les autres
   sont PLUS BASSES. On casse le reseau par le bas, jamais par le haut. */
function grain(u,v){
  return 0.46*bruit(u,v)
       + 0.32*bruit(u*0.47+7.1, v*0.43-3.7)
       + 0.22*bruit(u*0.21-19.3, v*0.19+5.9);
}
/* ── LA NAPPE : le champ qui donne les PLAGES claires et sombres ───────────
   Un velours froisse doit ses grandes taches au poil couche dans un sens ou
   dans l'autre. On ne peut pas le tirer de l'angle de peignage : celui-ci est
   enferme dans un cone de ±47° (sinon le champ s'enroule et le fond se voit),
   et un cone si etroit ne donne aucune variation. On prend donc un champ
   SCALAIRE a part, a grande longueur d'onde. */
function nappe(x,y){
  var w=0.052;
  return 0.5+0.5*(0.62*Math.sin(x*w+1.3)*Math.cos(y*w*0.81-0.4)
                 +0.38*Math.sin(y*w*1.53+2.2)*Math.cos(x*w*1.31+0.9));
}

/* ── LE REGLAGE, en unites de CELLULE (1 = un pixel d'une cellule de 67) ──── */
var DEF={
  lon : 3.40,   /* la fibre : 3 px pour un motif au pas de 5 a 11 — SOUS l'echelle
                   du motif, c'est la condition pour ne jamais le detruire */
  trav: 1.15,   /* le grain, EN TRAVERS du peignage. ⚠ a 0,80 il tombait a 1,6 px
                   reels : sous Nyquist, donc du moire, pas du grain. */
  long: 5.20,   /* le grain, LE LONG du peignage — c'est ce rapport qui couche
                   la matiere et fait lire « du tissu » */
  nap : 0.130,  /* l'amplitude du grain */
  rel : 0.78,   /* LE RELIEF de chaque marque — le bord tourne vers la lumiere
                   s'allume, l'oppose s'eteint. C'est lui qui souleve le poil. */
  flou: 1.90,   /* sur quel rayon on arrondit la marque avant d'en lire la pente */
  hmax: 242,    /* ⚠ LE PLAFOND, EN NIVEAU DE CANAL — pas en facteur.
                   Un plafond en facteur traite le lilas (208,176,255) comme
                   l'encre : x1,26 sur une couleur deja claire la pousse au
                   blanc, et le terrazzo sortait lave. En bornant le CANAL LE
                   PLUS HAUT on borne l'ecretage lui-meme : la teinte et la
                   saturation ne bougent pas d'un point, quelle que soit la
                   couleur de la palette. */
  omb : 0.30,   /* l'ombre portee sous la matiere */
  lus : 0.230,  /* les plages claires et sombres du velours froisse */
  duv : 0.170,  /* le duvet retro-reflectif. ⚠ a 0,40 le facteur montait a 1,88
                   au bord : la dalle se lavait en blanc. */
  lux : -2.15   /* d'ou vient la lumiere, en radians */
};

/* ── LE CHAMP DE PEIGNAGE ─────────────────────────────────────────────────
   Repris du lot precedent, avec son acquis : un biais constant plus long que
   le gradient supprime tout point critique. Sans lui le champ s'enroule, les
   fibres s'eventent, et le fond se voit — les araignees noires. */
function peigne(x,y){
  var w=0.233, d=2.2;
  function f(a,b){return Math.sin(a*w+0.7)*Math.cos(b*w*0.86+1.9)
                       +0.62*Math.sin(b*w*1.66-1.1)*Math.cos(a*w*1.41+0.5);}
  var gx=f(x+d,y)-f(x-d,y),gy=f(x,y+d)-f(x,y-d);
  var m=Math.hypot(gx,gy)||1;
  return Math.atan2(gy/m+0.44, gx/m+1.28);
}

/* ════════════════════════════════════════════════════════════════════════════
   LA PASSE. `cv` porte la dalle peinte par le moteur, fond transparent.
   Rend un NOUVEAU canevas, marge comprise (le duvet deborde du contour).
   `k` : l'echelle de la cellule (1 = 67 px, celle d'une cellule d'Orbite).
   ════════════════════════════════════════════════════════════════════════════ */
window.Velours=function(cv,k,opt){
  var o={},q; for(q in DEF)o[q]=DEF[q]; if(opt)for(q in opt)o[q]=opt[q];
  k=k||1;
  var s=DPR*k;                                   /* 1 unite de cellule -> px reels */
  var LON=o.lon*s, M=Math.ceil(LON)+2;
  var W0=cv.width,H0=cv.height; if(!W0||!H0)return cv;
  var W=W0+2*M,H=H0+2*M;

  var tmp=document.createElement('canvas'); tmp.width=W; tmp.height=H;
  var tg=tmp.getContext('2d'); tg.drawImage(cv,M,M);
  var src=tg.getImageData(0,0,W,H), S=src.data;
  var dst=tg.createImageData(W,H), D=dst.data;

  /* ⚑ LA PENTE SE LIT SUR UN ALPHA FLOUTE, JAMAIS SUR L'ALPHA BRUT.
     Un contour franc a une pente de 255 sur deux pixels : l'eclairage sort en
     LISERE BLANC et la couleur se lave. Floute d'abord, la marque devient un
     BOURRELET — une touffe de poil arrondie — et la lumiere la parcourt en
     entier au lieu de mordre son bord. Deux passes de boite separables. */
  var NP=W*H, A=new Float32Array(NP), B=new Float32Array(NP);
  for(var q0=0;q0<NP;q0++) A[q0]=S[q0*4+3];
  var rr=Math.max(1,Math.round(o.flou*s)), den=2*rr+1;
  for(var yy=0;yy<H;yy++){ var so=0,ro=yy*W;
    for(var xx=-rr;xx<=rr;xx++) so+=A[ro+Math.min(W-1,Math.max(0,xx))];
    for(xx=0;xx<W;xx++){ B[ro+xx]=so/den;
      so+=A[ro+Math.min(W-1,xx+rr+1)]-A[ro+Math.min(W-1,Math.max(0,xx-rr))]; } }
  for(var xx2=0;xx2<W;xx2++){ var s2=0;
    for(var yy2=-rr;yy2<=rr;yy2++) s2+=B[Math.min(H-1,Math.max(0,yy2))*W+xx2];
    for(yy2=0;yy2<H;yy2++){ A[yy2*W+xx2]=s2/den;
      s2+=B[Math.min(H-1,yy2+rr+1)*W+xx2]-B[Math.min(H-1,Math.max(0,yy2-rr))*W+xx2]; } }

  /* les prelevements le long du peigne : t=0 c'est la racine (la matiere
     elle-meme), t=1 la pointe. Le premier qui trouve de la matiere gagne. */
  var TS=[0,0.20,0.40,0.62,0.84,1.0], NT=TS.length;
  var cl=Math.cos(o.lux),sl=Math.sin(o.lux);

  for(var y=0;y<H;y++){
    var cy=y/s;
    for(var x=0;x<W;x++){
      var cx=x/s, i=(y*W+x)*4;

      var a=peigne(cx,cy), ca=Math.cos(a), sa=Math.sin(a);

      /* ⚑ L'EFFILOCHAGE EST ANISOTROPE, SINON IL FAIT DES PAQUETS.
         Un bruit isotrope au pas de 1,8 px donne des touffes de 1,8 px de
         large : on lit des paquets de matiere, pas des fibres. Une fibre est
         FINE EN TRAVERS et LONGUE DANS SON SENS. On prend donc le bruit dans
         le repere du peignage : 1,1 px de cellule en travers — soit 2,2 px
         reels, la plus fine periode representable, la lecon du repliement —
         et 3,5 px dans le sens. Chaque « poil » du contour est alors le plus
         fin que l'ecran puisse porter, et aucun ne se distingue. */
      var fu=( cx*ca+cy*sa)/3.5, fv=(-cx*sa+cy*ca)/1.1;
      var amp=LON*(0.14+1.10*bruit(fu+11.3, fv-4.7));

      /* ⚑ LE RELIEF. Sans lui la dalle reste UN FILTRE POSE SUR UNE FORME
         PLATE : le grain est la, mais rien ne se souleve, et on n'a pas envie
         d'y toucher. On lit la pente de la matiere (le gradient de l'alpha) :
         le bord tourne vers la lumiere s'allume, l'oppose s'eteint. Chaque
         point de braille, chaque hachure, chaque carreau devient alors une
         touffe posee SUR la surface, et non un trou decoupe dedans. */
      var rel=1;
      if(o.rel){
        var dd=Math.max(1,Math.round(1.6*s));
        var aE=A[y*W+(x+dd<W?x+dd:W-1)], aO=A[y*W+(x-dd>=0?x-dd:0)];
        var aS2=A[(y+dd<H?y+dd:H-1)*W+x], aN=A[(y-dd>=0?y-dd:0)*W+x];
        rel=1-o.rel*(((aE-aO)*cl+(aS2-aN)*sl)/255);
        if(rel<0.52)rel=0.52;
      }

      var got=-1,si=0;
      for(var t=0;t<NT;t++){
        var ox=Math.round(x-ca*amp*TS[t]), oy=Math.round(y-sa*amp*TS[t]);
        if(ox<0||oy<0||ox>=W||oy>=H)continue;
        var j=(oy*W+ox)*4;
        if(S[j+3]>10){got=t;si=j;break;}
      }
      if(got<0){D[i+3]=0;continue;}
      var tt=TS[got];

      /* LE GRAIN COUCHE. Un bruit etire dans le sens du peignage : long de
         4,4 px, large de 0,8. Sous l'echelle du motif, donc il ne peut pas le
         detruire — et c'est lui qu'on lit comme « du tissu ». */
      var u=( cx*ca+cy*sa)/o.long, v=(-cx*sa+cy*ca)/o.trav;
      var nap=1+o.nap*(grain(u,v)*2-1);

      /* LES PLAGES DU VELOURS. ⚠ Le premier reglage les tirait du produit
         scalaire entre la fibre et la lumiere. Le cone du peignage etant
         centre sur 0,33 rad et la lumiere sur -2,15, ce produit valait -0,79
         PARTOUT : le facteur tombait a 0,83 et TOUTE la dalle s'assombrissait
         de 17 %, sans la moindre variation. C'est la nappe qui porte les
         plages, et elle est centree sur 1.
         ⚠ Aucune tache speculaire : la nappe ne depend pas du regard. */
      var lus=1+o.lus*(nappe(cx,cy)*2-1);

      /* LE DUVET. La ou la matiere s'arrete, les fibres se voient de profil et
         renvoient plus de lumiere — velours et coton sont retro-reflectifs. */
      /* le duvet culmine au DEBUT du bord, pas a la pointe : a la pointe il
         ne reste presque plus de matiere, l'eclaircir n'ajoute que du blanc. */
      var duv=1+o.duv*Math.sin(tt*3.1416);
      var f=nap*lus*duv*rel;
      /* on borne le canal le plus haut : aucun ecretage, donc aucune derive
         de teinte ni de saturation — la couleur de la palette reste exacte. */
      var c0=S[si],c1=S[si+1],c2=S[si+2];
      var mx=c0>c1?(c0>c2?c0:c2):(c1>c2?c1:c2);
      if(mx*f>o.hmax) f=o.hmax/(mx||1);

      D[i]  =c0*f;
      D[i+1]=c1*f;
      D[i+2]=c2*f;
      /* la pointe est translucide : c'est le halo duveteux du contour */
      /* la lisiere commence des le premier prelevement : sans cette rampe le
         contour reste FRANC et le duvet a l'air colle a cote. */
      D[i+3]=S[si+3]*Math.pow(1-tt*0.94,1.55);
    }
  }
  /* ⚑ L'OMBRE PORTEE. Une matiere qui ne projette rien reste collee au fond :
     l'oeil la lit comme un aplat decoupe, jamais comme quelque chose de pose.
     Une copie sombre, decalee dans le sens de la lumiere et floutee, suffit —
     et elle ne coute qu'un drawImage. */
  var fin=document.createElement('canvas'); fin.width=W; fin.height=H;
  var fg=fin.getContext('2d');
  if(o.omb){
    var sh=document.createElement('canvas'); sh.width=W; sh.height=H;
    var sg=sh.getContext('2d');
    sg.drawImage(cv,M,M);
    sg.globalCompositeOperation='source-in';
    sg.fillStyle='rgba(0,0,0,'+o.omb+')'; sg.fillRect(0,0,W,H);
    fg.save();
    fg.filter='blur('+(1.15*s)+'px)';
    fg.drawImage(sh,-cl*1.5*s,-sl*1.5*s);
    fg.restore();
  }
  tg.putImageData(dst,0,0);
  fg.drawImage(tmp,0,0);
  fin.__marge=M;
  return fin;
};
window.Velours.reglage=DEF;
window.Velours.peigne=peigne;
})();
