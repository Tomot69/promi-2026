/* ════════════════════════════════════════════════════════════════════════════
   LE DUVET — LA DALLE RESTE NETTE, LA MATIERE SE MET AUTOUR

   ⚑ CE QUE TOM A REJETE, ET QUI NE REVIENDRA PAS.
     « pas des photos detourees degueulasses, abandonne et plus jamais ca »
   Trois gestes de la version precedente FABRIQUAIENT ce detourage :
     1 · L'EFFILOCHAGE. Il prelevait la couleur a une position deplacee. Le
         contour du moteur — net, calcule, exact — etait donc RONGE : des bords
         mordus, irreguliers, sales. C'est litteralement l'aspect d'un mauvais
         detourage. Supprime.
     2 · L'OMBRE PORTEE. Une copie sombre decalee sous la matiere fait un
         AUTOCOLLANT pose sur le fond, jamais une matiere. Supprimee.
     3 · LE RELIEF A FORTE AMPLITUDE. Une pente a 0,78 pose un liseré clair
         d'un cote et sombre de l'autre : encore un contour sale. Ramene a un
         galbe doux qui ne se lit plus comme un bord mais comme une rondeur.
   ⚠ LA REGLE QUI EN SORT : ON NE DEPLACE JAMAIS UN PIXEL DE LA DALLE. Le
   moteur a calcule ce contour, il est la verite. Tout ce qu'on ajoute se met
   AUTOUR, ou module la CLARTE — jamais la forme.

   ⚑ CE QUE TOM DEMANDE, ET COMMENT CHAQUE MOT EST TRAITE.
     « les vraies dalles »        Toile.dalleTrame peint ; on ne redessine rien
                                  et on ne deplace rien.
     « fluffy mais pas trop,      un duvet AUTOUR : deux halos flous, plus
       que ca reste lisible »     clairs, poses SOUS la dalle nette. Le dessin
                                  n'est jamais touche, donc jamais moins lisible.
     « belle lumiere generale »   une seule lumiere douce sur toute la dalle,
                                  plus un galbe par marque. Aucun effet local.
     « belles couleurs »          le plafond porte sur le CANAL LE PLUS HAUT :
                                  aucun ecretage, teinte et saturation exactes ;
                                  et le duvet s'eclaircit sans virer au blanc.
     « donne envie de toucher »   la rondeur et le halo, pas le poil.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var DPR=Math.min(2,window.devicePixelRatio||1);

/* ── un bruit de valeur, deterministe et lisse ────────────────────────────── */
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
/* ⚠ acquis, et il a coute un lot : la plus fine octave est celle du PIXEL, et
   toutes les autres sont PLUS BASSES. Une octave sous l'echantillonnage ne
   disparait pas, elle SE REPLIE — en treillis gaufre en travers de la dalle. */
function grain(u,v){
  return 0.46*bruit(u,v)
       + 0.32*bruit(u*0.47+7.1, v*0.43-3.7)
       + 0.22*bruit(u*0.21-19.3, v*0.19+5.9);
}

/* ── LE SENS DU POIL ──────────────────────────────────────────────────────
   Un biais constant plus long que le gradient supprime tout point critique :
   sans lui le champ s'enroule, la matiere s'evente, et le fond se voit. */
function peigne(x,y){
  var w=0.233, d=2.2;
  function f(a,b){return Math.sin(a*w+0.7)*Math.cos(b*w*0.86+1.9)
                       +0.62*Math.sin(b*w*1.66-1.1)*Math.cos(a*w*1.41+0.5);}
  var gx=f(x+d,y)-f(x-d,y),gy=f(x,y+d)-f(x,y-d);
  var m=Math.hypot(gx,gy)||1;
  return Math.atan2(gy/m+0.44, gx/m+1.28);
}

/* ── LE REGLAGE, en unites de CELLULE (1 = un pixel d'une cellule de 67) ──── */
var DEF={
  h1   : 1.00,   /* le duvet serre : son rayon de flou */
  a1   : 0.86,   /* et son opacite. ⚠ un halo peu opaque se compose vers le
                    fond sombre : il GRISE le bord. Serre et dense, il garde
                    la couleur de la dalle. */
  h2   : 2.60,   /* le duvet lache, celui qui fait le halo de coton */
  a2   : 0.30,
  lift : 0.000,   /* ⚠ zero : la moindre montee vers le blanc fait un halo
                    clair sur fond sombre, et un halo clair EST un neon. */  /* ⚠ de combien le duvet est plus clair. A 0,15 il faisait un
                    NEON — un flou gaussien eclairci sur fond sombre, c'est
                    l'outer glow, et c'est cheap. Il reste presque a la
                    couleur de la dalle : c'est sa DECOUPE qui dit la fibre,
                    pas sa clarte. */
  fib  : 1.05,   /* la periode du bruit EN TRAVERS du poil, dans le halo */
  fil  : 4.00,   /* et DANS LE SENS du poil : c'est ce rapport qui fait une
                    meche plutot qu'une tache */
  troue: 2.10,   /* l'exposant qui troue le halo. Un flou plein est un nuage ;
                    troue, il devient un bord de fourrure. */
  galbe: 0.26,   /* la rondeur d'une marque. ⚠ a 0,78 c'etait un liseré sale. */
  flou : 2.30,   /* sur quel rayon on arrondit la marque avant d'en lire la pente */
  grn  : 0.055,  /* le grain couche — un tact, pas une texture */
  trav : 1.15,   /* sa periode en travers du poil (2,3 px reels : le plancher) */
  long : 5.20,   /* et dans le sens du poil */
  hmax : 246,    /* le plafond, EN NIVEAU DE CANAL : aucune derive de teinte */
  lux  : -2.15   /* d'ou vient la lumiere */
};

/* un calque de la dalle, eclairci sur place — il sert aux deux halos */
function calque(cv,W,H,M,lift){
  var t=document.createElement('canvas'); t.width=W; t.height=H;
  var g=t.getContext('2d');
  g.drawImage(cv,M,M);
  if(lift>0){
    g.globalCompositeOperation='source-atop';
    g.fillStyle='rgba(255,255,255,'+lift+')';
    g.fillRect(0,0,W,H);
  }
  return t;
}

/* ⚑ LE DUVET SE GRIGNOTE, SINON C'EST UN NEON.
   Un flou gaussien est UNIFORME : sur fond sombre il ne peut donner qu'une
   aureole — l'outer glow, la signature du toc. Une fourrure fait l'inverse :
   chaque meche atteint une distance differente, et il reste du VIDE entre.
   On troue donc l'alpha du halo par un bruit etire dans le sens du poil.
   ⚠ On ne touche que le HALO. La dalle, dessus, reste au pixel pres celle
   que le moteur a calculee. */
function grignote(t,W,H,s,o){
  var g=t.getContext('2d'), im=g.getImageData(0,0,W,H), D=im.data;
  for(var y=0;y<H;y++){
    var cy=y/s;
    for(var x=0;x<W;x++){
      var i=(y*W+x)*4; if(!D[i+3])continue;
      var cx=x/s, a=peigne(cx,cy), ca=Math.cos(a), sa=Math.sin(a);
      var u=( cx*ca+cy*sa)/o.fil, v=(-cx*sa+cy*ca)/o.fib;
      var n=bruit(u+3.7,v-8.1);
      n=Math.pow(n,o.troue)*2.05; if(n>1)n=1;
      D[i+3]*=n;
    }
  }
  g.putImageData(im,0,0);
  return t;
}

/* ════════════════════════════════════════════════════════════════════════════
   `cv` porte la dalle peinte par le moteur, fond transparent. Rend un NOUVEAU
   canevas, marge comprise. `k` : l'echelle de la cellule (1 = 67 px).
   ════════════════════════════════════════════════════════════════════════════ */
window.Velours=function(cv,k,opt){
  var o={},q; for(q in DEF)o[q]=DEF[q]; if(opt)for(q in opt)o[q]=opt[q];
  k=k||1;
  var s=DPR*k;
  var W0=cv.width,H0=cv.height; if(!W0||!H0)return cv;
  var M=Math.ceil(o.h2*s*2.2)+2, W=W0+2*M, H=H0+2*M;

  var out=document.createElement('canvas'); out.width=W; out.height=H;
  var og=out.getContext('2d');

  /* ── 1 · LE DUVET, AUTOUR ────────────────────────────────────────────────
     Deux halos concentriques de la dalle elle-meme, flous et plus clairs,
     poses DESSOUS. Ils debordent du contour : c'est ce debord qui fait le
     coton. Et comme ils sont dessous, le dessin reste intact au-dessus —
     « fluffy, mais que ca reste lisible ». */
  function couche(r,al,lift){
    var t=document.createElement('canvas'); t.width=W; t.height=H;
    var tg2=t.getContext('2d');
    tg2.filter='blur('+(r*s)+'px)';
    tg2.drawImage(calque(cv,W,H,M,lift),0,0);
    tg2.filter='none';
    grignote(t,W,H,s,o);
    og.globalAlpha=al; og.drawImage(t,0,0); og.globalAlpha=1;
  }
  couche(o.h2,o.a2,o.lift*1.5);
  couche(o.h1,o.a1,o.lift);

  /* ── 2 · LA DALLE, NETTE, PAR-DESSUS — pas un pixel deplace ────────────── */
  og.drawImage(cv,M,M);

  /* ── 3 · LA LUMIERE ──────────────────────────────────────────────────────
     Une lumiere GENERALE sur toute la dalle, plus un galbe doux par marque et
     un grain fin. On ne touche qu'a la clarte : aucun bord n'est deplace. */
  var img=og.getImageData(0,0,W,H), D=img.data;

  /* ⚠ la pente se lit sur un alpha FLOUTE. Sur l'alpha brut elle vaut 255 sur
     deux pixels : le bord sort en liseré blanc et la couleur se lave. Floutee,
     la marque devient un bourrelet et la lumiere la parcourt en entier. */
  var NP=W*H, A=new Float32Array(NP), B=new Float32Array(NP);
  for(var q0=0;q0<NP;q0++) A[q0]=D[q0*4+3];
  var rr=Math.max(1,Math.round(o.flou*s)), den=2*rr+1, xx, yy;
  for(yy=0;yy<H;yy++){ var so=0,ro=yy*W;
    for(xx=-rr;xx<=rr;xx++) so+=A[ro+Math.min(W-1,Math.max(0,xx))];
    for(xx=0;xx<W;xx++){ B[ro+xx]=so/den;
      so+=A[ro+Math.min(W-1,xx+rr+1)]-A[ro+Math.min(W-1,Math.max(0,xx-rr))]; } }
  for(xx=0;xx<W;xx++){ var s2=0;
    for(yy=-rr;yy<=rr;yy++) s2+=B[Math.min(H-1,Math.max(0,yy))*W+xx];
    for(yy=0;yy<H;yy++){ A[yy*W+xx]=s2/den;
      s2+=B[Math.min(H-1,yy+rr+1)*W+xx]-B[Math.min(H-1,Math.max(0,yy-rr))*W+xx]; } }

  var cl=Math.cos(o.lux), sl=Math.sin(o.lux);
  var dd=Math.max(1,Math.round(1.7*s));

  for(yy=0;yy<H;yy++){
    var cy=yy/s;
    for(xx=0;xx<W;xx++){
      var i=(yy*W+xx)*4;
      if(D[i+3]===0)continue;
      var cx=xx/s;

      /* LE GALBE — la rondeur de la marque, jamais son bord. */
      var aE=A[yy*W+(xx+dd<W?xx+dd:W-1)], aO=A[yy*W+(xx-dd>=0?xx-dd:0)];
      var aS=A[(yy+dd<H?yy+dd:H-1)*W+xx], aN=A[(yy-dd>=0?yy-dd:0)*W+xx];
      var galbe=1-o.galbe*(((aE-aO)*cl+(aS-aN)*sl)/255);
      if(galbe<0.76)galbe=0.76;

      /* LE GRAIN COUCHE — un tact, pas une texture. */
      var a=peigne(cx,cy), ca=Math.cos(a), sa=Math.sin(a);
      var u=( cx*ca+cy*sa)/o.long, v=(-cx*sa+cy*ca)/o.trav;
      var grn=1+o.grn*(grain(u,v)*2-1);

      var f=galbe*grn;
      var c0=D[i],c1=D[i+1],c2=D[i+2];
      var mx=c0>c1?(c0>c2?c0:c2):(c1>c2?c1:c2);
      if(mx*f>o.hmax) f=o.hmax/(mx||1);   /* aucun ecretage : la teinte tient */
      D[i]=c0*f; D[i+1]=c1*f; D[i+2]=c2*f;
    }
  }
  og.putImageData(img,0,0);
  out.__marge=M;
  return out;
};
/* ════════════════════════════════════════════════════════════════════════════
   LA LUMIERE GENERALE — elle appartient a la SCENE, pas a la dalle.
   ⚑ Posee par dalle, elle se repete a l'identique sur chacune : chaque dalle
   a son propre haut clair et son propre bas sombre, et rien ne se tient
   ensemble. Une seule lumiere doit traverser TOUTE la composition — c'est
   exactement ce qu'elle fera sur la sphere. On l'applique donc apres montage.
   La saturation monte du meme geste : « belles couleurs ». Elle n'entame ni la
   teinte ni le plafond de canal.
   ════════════════════════════════════════════════════════════════════════════ */
window.Velours.jour=function(cv,opt){
  var o={amp:0.20, lux:DEF.lux, sat:1.12, hmax:DEF.hmax, amb:0.06};
  if(opt)for(var q in opt)o[q]=opt[q];
  var g=cv.getContext('2d'), W=cv.width, H=cv.height;
  var im=g.getImageData(0,0,W,H), D=im.data;
  var cl=Math.cos(o.lux), sl=Math.sin(o.lux);
  var cx=W/2, cy=H/2, R=Math.max(W,H)/2;
  for(var y=0;y<H;y++){
    var py=(y-cy)/R;
    for(var x=0;x<W;x++){
      var i=(y*W+x)*4; if(!D[i+3])continue;
      var px=(x-cx)/R;
      /* une lumiere douce, orientee, plus un ambiant qui empeche le bas de
         tomber dans le noir — sans elle une scene sombre perd ses couleurs */
      var f=1-o.amp*(px*cl+py*sl)+o.amb;
      var c0=D[i],c1=D[i+1],c2=D[i+2];
      /* la saturation : on s'ecarte du gris propre au pixel. La teinte ne
         bouge pas d'un degre. */
      var lm=0.299*c0+0.587*c1+0.114*c2;
      c0=lm+(c0-lm)*o.sat; c1=lm+(c1-lm)*o.sat; c2=lm+(c2-lm)*o.sat;
      if(c0<0)c0=0; if(c1<0)c1=0; if(c2<0)c2=0;
      var mx=c0>c1?(c0>c2?c0:c2):(c1>c2?c1:c2);
      if(mx*f>o.hmax) f=o.hmax/(mx||1);
      D[i]=c0*f; D[i+1]=c1*f; D[i+2]=c2*f;
    }
  }
  g.putImageData(im,0,0);
  return cv;
};
window.Velours.reglage=DEF;
})();
