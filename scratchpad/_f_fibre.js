/* ════════════════════════════════════════════════════════════════════════════
   L'ORBITE — LA FIBRE EST LE TRAIT DU MONDE

   ⚑ LE PARTI PRIS, EN UNE PHRASE
   On ne pose pas de fourrure SUR un dessin : on DESSINE AVEC la fourrure.
   Chaque monde du Studio ne donne plus une image a recouvrir, il donne une
   LOI D'IMPLANTATION — ou une touffe pousse, dans quel sens elle est peignee,
   quelle longueur elle a, quelle marche de clarte elle porte.

   ⚑ POURQUOI CA DEBLOQUE LA CONTRADICTION DES DIX DERNIERS TOURS
   Le mur etait une COLLISION D'ECHELLES : un poil fait 6 px, un motif du
   moteur a un pas de 5 a 11 px. Tant que le poil devait RECOUVRIR le motif,
   il l'ecrasait ; tant qu'il devait le PORTER pixel par pixel, il fallait
   qu'il soit plus petit que lui. Ici il n'y a plus deux grains : le poil EST
   la marque du monde. Une hachure de gravure n'est plus une ligne qu'on
   duvette, c'est une RANGEE DE FIBRES COUCHEES — du velours cotele.

   ⚑ LA PREUVE QUE LE PRODUIT LE PENSAIT DEJA
   Un des huit mondes s'appelle TOUFFE. Ses fleurs sont deja des rosettes de
   fibres. Ce lot ne fait qu'etendre aux sept autres ce que celui-la savait.

   Les pas et les constantes viennent des peintres du moteur, a la lettre
   (toile-extrait.js : Rpix STEP 5, Rbra DOT 9, Rsil SP 6 AMP 4,5 WL 0,018,
   Rgra HS 8, Rmos T 11, Renc 9 ellipses rayon 0,6·sp, Rterr 7 tessons,
   Rtouf 3-5 fleurs). Rien n'est invente : la loi est celle du moteur, seule
   la MARQUE change — un poil au lieu d'un trait.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var TAU=6.283185307179586;

/* ⚑ LES TROIS CONSTANTES DE LA MATIERE — c'est elles qui font soie ou herisson.
   Premier rendu : pas 2,4 · longueur 6,5 · epaisseur 1,30. Un poil couvrait
   trois pas : chaque brin se lisait tout seul, et la cellule sortait en
   BOGUE DE CHATAIGNE. Une fourrure ne se lit jamais brin par brin — elle se
   lit comme un TAPIS, et un tapis demande que les brins se recouvrent SANS
   qu'aucun ne se detache. On resserre le pas de moitie, on raccourcit le poil
   de moitie, on l'affine : un brin couvre alors ~2,4 pas et se noie dans ses
   voisins. */
var PAS=1.05, LON=3.00, EPA=0.62;

/* ⚑ POURQUOI CINQ BRINS ET PAS TROIS. Une fourrure ne se lit jamais brin par
   brin. A trois brins ecartes de 0,30 rad, les pointes finissent a 3 px l'une
   de l'autre et le trou se VOIT : ca fait une patte d'oiseau. Cinq brins
   serres a 0,20, plus fins, se recouvrent — et c'est le recouvrement qui fait
   le soyeux, pas la longueur.
   Le cout est tenable : a 390 px, une trentaine de cellules sont visibles de
   face (audit §5) ; a ce pas, ~4 070 touffes par cellule -> ~122 000 visibles,
   exactement le plafond mesure des 60 images par seconde. Le dos n'est pas
   visite (culling par plaques, deja acquis). */

/* ── le hasard, deterministe ─────────────────────────────────────────────── */
function hh(i){var x=(i*2654435761)>>>0;x^=x>>>15;x=(x*2246822519)>>>0;
  x^=x>>>13;x=(x*3266489917)>>>0;x^=x>>>16;return (x>>>8)/16777216;}
function graine(n){var s=(n*2654435761)>>>0;return function(){
  s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};}

/* ── LES STRATES : la loi du moteur, a la lettre ──────────────────────────
   PALL() du moteur : LITS=[0,0.10,0.04,0.14,0.07], un lift de CLARTE en HSL,
   teinte et saturation strictement preservees. LITS[0]=0 -> le code couleur
   exact de la palette est toujours present. Une dalle a UNE couleur et des
   STRATES dedans — jamais une autre couleur. */
var LITS=[0,0.10,0.04,0.14,0.07];
function r2h(c){var r=c[0]/255,g=c[1]/255,b=c[2]/255,mx=Math.max(r,g,b),mn=Math.min(r,g,b),
  h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);
  h=mx===r?((g-b)/d+(g<b?6:0)):mx===g?((b-r)/d+2):((r-g)/d+4);h/=6;}return [h,s,l];}
function h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;
  if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}
  if(s===0){var v=l*255;return [v,v,v];}
  var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;
  return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
function strates(col){var hs=r2h(col),out=[];
  for(var k=0;k<LITS.length;k++)
    out.push(LITS[k]===0?[col[0],col[1],col[2]]
      :h2r(hs[0],hs[1],Math.min(0.965,hs[2]+LITS[k]*(1-hs[2]))));
  return out;}

/* ── LE POLYGONE D'UNE CELLULE, dans le plan ──────────────────────────────
   Meme principe que _q_cellule.js sur la sphere : on part d'un grand carre
   et on le RABOTE par la bissectrice de chaque voisin. `inset` recule chaque
   plan — c'est le JOINT, le vide entre deux dalles. */
function cellulePlane(S,i,inset){
  var Si=S[i],R=900,P=[[Si[0]-R,Si[1]-R],[Si[0]+R,Si[1]-R],[Si[0]+R,Si[1]+R],[Si[0]-R,Si[1]+R]];
  for(var j=0;j<S.length&&P.length>2;j++){
    if(j===i)continue;
    var Sj=S[j],nx=Si[0]-Sj[0],ny=Si[1]-Sj[1],nm=Math.hypot(nx,ny);
    if(nm<1e-9)continue; nx/=nm; ny/=nm;
    var mx=(Si[0]+Sj[0])/2,my=(Si[1]+Sj[1])/2,dec=mx*nx+my*ny+inset;
    var Q=[],m=P.length;
    for(var k=0;k<m;k++){
      var a=P[k],b=P[(k+1)%m];
      var da=a[0]*nx+a[1]*ny-dec,db=b[0]*nx+b[1]*ny-dec;
      if(da>=0)Q.push(a);
      if((da>=0)!==(db>=0)){var t=da/(da-db);
        Q.push([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]);}
    }
    P=Q;
  }
  return P;
}
function dedans(P,x,y){var n=P.length,c=false;
  for(var i=0,j=n-1;i<n;j=i++){
    var xi=P[i][0],yi=P[i][1],xj=P[j][0],yj=P[j][1];
    if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c;}
  return c;}
function boite(P){var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  for(var i=0;i<P.length;i++){var p=P[i];
    if(p[0]<x0)x0=p[0];if(p[0]>x1)x1=p[0];if(p[1]<y0)y0=p[1];if(p[1]>y1)y1=p[1];}
  return [x0,y0,x1,y1];}

/* ── LE CHAMP DE PEIGNAGE — un champ lisse, jamais un hachage ─────────────
   Acquis de _q_cellule.js : un hachage donne un herisson, un champ donne un
   pelage. */
/* ⚠ LA LONGUEUR D'ONDE SE COMPTE EN CELLULES, PAS EN PIXELS. Reglee a
   l'echelle de l'ecran, le champ ne tourne pas dans une cellule de 67 px :
   tous les poils partent dans le meme sens, le lustre devient constant, et
   un monde dense (encre, pixel) sort en DALLE PLATE ET PALE — mesure au
   rendu precedent. Il faut ~2,5 tourbillons en travers d'une cellule : c'est
   ce moire-la qui fait le velours froisse. */
function peigne(x,y,k){
  var kk=k||1, w=0.233/kk, d=2.2*kk;
  function f(a,b){return Math.sin(a*w+0.7)*Math.cos(b*w*0.86+1.9)
                       +0.62*Math.sin(b*w*1.66-1.1)*Math.cos(a*w*1.41+0.5);}
  var gx=f(x+d,y)-f(x-d,y),gy=f(x,y+d)-f(x,y-d);
  /* ⚑ LES ARAIGNEES NOIRES. Un champ de gradient a des POINTS CRITIQUES : la
     ou il s'annule, la direction fait un tour complet, les touffes s'eventent
     en rosette, et le FOND se voit entre elles — une petite etoile noire au
     milieu de la peluche. Ce n'etait ni un poil noir ni une ombre : c'etait
     un trou. On ne peut pas les rattraper un par un ; on empeche le champ
     d'en avoir. Un biais CONSTANT plus long que le gradient (1,35 > 1) enferme
     la direction dans un cone de ±47° : plus aucun enroulement possible, et
     le pelage garde un sens dominant — ce qu'une fourrure peignee a de toute
     facon. */
  var m=Math.hypot(gx,gy)||1;
  return Math.atan2(gy/m+0.44, gx/m+1.28);
}

/* ════════════════════════════════════════════════════════════════════════════
   LES HUIT LOIS D'IMPLANTATION
   Chacune rend une liste de touffes {x,y,a,l,s} :
     x,y  la racine        a  l'angle de peignage
     l    la longueur      s  la marche de clarte (indice dans strates())
   `k` est l'echelle : k = taille de la cellule / 67 px. A k=1 les pas sont
   EXACTEMENT ceux du moteur.
   ════════════════════════════════════════════════════════════════════════════ */

/* PIXEL — Rpix : STEP 5, des carres pleins jointifs.
   La fibre : dense partout, peignee d'un seul mouvement, mais la racine n'est
   admise que si le CENTRE de son bloc de 5 est dans la cellule -> le contour
   sort en escalier, la signature du monde. */
function loiPixel(P,k,rnd){
  var T=[],B=boite(P),pas=5*k,pi=PAS*k,ang=rnd()*TAU;
  for(var y=B[1];y<B[3];y+=pi)for(var x=B[0];x<B[2];x+=pi){
    var jx=x+(rnd()-.5)*pi*.9,jy=y+(rnd()-.5)*pi*.9;
    var bx=Math.floor((jx-B[0])/pas)*pas+B[0]+pas/2,
        by=Math.floor((jy-B[1])/pas)*pas+B[1]+pas/2;
    if(!dedans(P,bx,by))continue;
    var s=(((bx/pas)|0)+((by/pas)|0))%7===0?2:0;
    /* ⚠ 0,13 de champ ne suffit pas : la direction constante l'ecrase, le
       lustre devient uniforme et la cellule sort en DALLE PLATE ET PALE
       (mesure deux fois). Il faut que le champ MENE — le sens propre a la
       dalle ne fait plus qu'incliner l'ensemble. */
    var ap=peigne(jx,jy,k);
    var a=Math.atan2(0.72*Math.sin(ap)+0.28*Math.sin(ang),
                     0.72*Math.cos(ap)+0.28*Math.cos(ang));
    T.push({x:jx,y:jy,a:a+(rnd()-.5)*0.22,l:LON*k*(0.72+rnd()*0.36),s:s});
  }
  return T;
}

/* BRAILLE — Rbra : DOT 9, un disque de rayon 2,9 par noeud de grille.
   La fibre : une ROSETTE serree par noeud, rien entre. Un tapis a points. */
function loiBraille(P,k,rnd){
  var T=[],B=boite(P),DOT=9*k;
  var x0=Math.floor(B[0]/DOT)*DOT+DOT*.5,y0=Math.floor(B[1]/DOT)*DOT+DOT*.5;
  for(var y=y0;y<B[3];y+=DOT)for(var x=x0;x<B[2];x+=DOT){
    if(!dedans(P,x,y))continue;
    var s=hh((x*7+y*13)|0)<0.22?3:0,n=22;
    for(var q=0;q<n;q++){
      var a=q/n*TAU+hh((x*3+y*5+q)|0)*0.7,r=2.9*k*Math.sqrt(hh((x+y*7+q*11)|0))*0.72;
      T.push({x:x+Math.cos(a)*r,y:y+Math.sin(a)*r,a:a,l:LON*k*(0.7+rnd()*0.4),s:s});
    }
  }
  return T;
}

/* SILLONS — Rsil : SP 6, AMP 4,5, WL 0,018 — des lignes ondulees.
   La fibre : les poils COUCHES le long de l'onde, rangee par rangee. De la
   soie moiree. Le sens de peignage est la TANGENTE de l'onde. */
function loiSillons(P,k,rnd){
  var T=[],B=boite(P),SP=6*k,AMP=4.5*k,WL=0.018/k,pas=PAS*k*0.86;
  function wv(x,ln){return AMP*Math.sin(x*WL+ln*.55)+AMP*.62*Math.sin(x*WL*2.4-ln*.42+1.2);}
  var li=Math.floor(B[1]/SP);
  for(var bY=li*SP+SP*.5;bY<B[3];bY+=SP,li++){
    var s=(li%3===0)?2:(li%5===0?1:0);
    for(var x=B[0];x<B[2];x+=pas){
      var y=bY+wv(x,li);
      if(!dedans(P,x,y))continue;
      var dy=(wv(x+2,li)-wv(x-2,li))/4;
      var a=Math.atan2(dy,1)+(li%2?0:Math.PI);
      T.push({x:x,y:y+(rnd()-.5)*SP*0.34,a:a+(rnd()-.5)*0.14,l:LON*k*(0.85+rnd()*0.45),s:s});
    }
  }
  return T;
}

/* GRAVURE — Rgra : HS 8, des hachures paralleles a l'angle PROPRE de la dalle.
   La fibre : une rangee de poils couches, un sens sur deux inverse. C'est
   exactement du VELOURS COTELE — et le cotele est ce qui se voit le mieux
   quand la lumiere tourne, donc sur une sphere qui tourne. */
function loiGravure(P,k,rnd,ang){
  var T=[],B=boite(P),HS=8*k,pas=PAS*k*0.86;
  var dx=Math.cos(ang),dy=Math.sin(ang),px=-dy,py=dx;
  var cx=(B[0]+B[2])/2,cy=(B[1]+B[3])/2,R=Math.hypot(B[2]-B[0],B[3]-B[1])/2+HS;
  var ri=0;
  for(var off=-R;off<=R;off+=HS,ri++){
    var ox=cx+px*off,oy=cy+py*off,s=(ri%2)?0:(ri%4===1?3:2);
    for(var t=-R;t<=R;t+=pas){
      var x=ox+dx*t,y=oy+dy*t;
      if(!dedans(P,x,y))continue;
      T.push({x:x+px*(rnd()-.5)*HS*0.36,y:y+py*(rnd()-.5)*HS*0.36,
              a:ang+(ri%2?0:Math.PI)+(rnd()-.5)*0.13,
              l:LON*k*(0.9+rnd()*0.4),s:s});
    }
  }
  return T;
}

/* MOSAIQUE — Rmos : T 11, des carreaux jointifs a 2 px de gouttiere.
   La fibre : un carreau de poils peignes, la gouttiere reste NUE, et le sens
   alterne en damier. Une tapisserie. */
function loiMosaique(P,k,rnd){
  var T=[],B=boite(P),Tt=11*k,g=2*k,pas=PAS*k*0.9;
  var x0=Math.floor(B[0]/Tt)*Tt,y0=Math.floor(B[1]/Tt)*Tt;
  for(var cy=y0;cy<B[3];cy+=Tt)for(var cx=x0;cx<B[2];cx+=Tt){
    var ic=(cx/Tt)|0,jc=(cy/Tt)|0,a=((ic+jc)%2)?0.42:1.99;
    var s=hh((ic*31+jc*17)|0)<0.30?(hh((ic*7+jc*3)|0)<0.5?2:3):0;
    for(var y=cy+g;y<cy+Tt-g;y+=pas)for(var x=cx+g;x<cx+Tt-g;x+=pas){
      var jx=x+(rnd()-.5)*pas*.7,jy=y+(rnd()-.5)*pas*.7;
      if(!dedans(P,jx,jy))continue;
      T.push({x:jx,y:jy,a:a+(rnd()-.5)*0.20,l:LON*k*(0.82+rnd()*0.4),s:s});
    }
  }
  return T;
}

/* ENCRE — Renc : 9 ellipses par graine, rayon 0,6·sp, alpha .9 -> les
   recouvrements font les strates visibles sur la vraie Toile.
   La fibre : dense DANS les lobes, peignee en RADIAL depuis le centre de son
   lobe, et la marche de clarte compte les recouvrements. La silhouette lobee
   est la signature du monde. */
function loiEncre(P,k,rnd){
  var T=[],B=boite(P),cx=(B[0]+B[2])/2,cy=(B[1]+B[3])/2;
  var sp=Math.min(B[2]-B[0],B[3]-B[1]),rad=sp*0.60,E=[];
  for(var b=0;b<9;b++){
    E.push({x:cx+(rnd()-.5)*rad*1.2,y:cy+(rnd()-.5)*rad,
            rx:rad*(.32+rnd()*.42),ry:rad*(.16+rnd()*.32),a:rnd()*3.14});
  }
  var pas=PAS*k;
  for(var y=B[1];y<B[3];y+=pas)for(var x=B[0];x<B[2];x+=pas){
    var jx=x+(rnd()-.5)*pas*.9,jy=y+(rnd()-.5)*pas*.9;
    if(!dedans(P,jx,jy))continue;
    var n=0,ox=0,oy=0;
    for(var e=0;e<9;e++){var el=E[e];
      var ca=Math.cos(-el.a),sa=Math.sin(-el.a);
      var ux=(jx-el.x)*ca-(jy-el.y)*sa,uy=(jx-el.x)*sa+(jy-el.y)*ca;
      if(ux*ux/(el.rx*el.rx)+uy*uy/(el.ry*el.ry)<=1){n++;if(n===1){ox=el.x;oy=el.y;}}
    }
    if(!n)continue;
    /* ⚠ PAS DE PEIGNAGE RADIAL. Un depart radial depuis le centre d'un lobe
       fait tourner l'angle a l'infini pres du centre : la cellule sort en
       BOGUE DE CHATAIGNE. Le lobe donne la SILHOUETTE et la STRATE ; le sens,
       c'est le champ lisse, et lui seul. */
    var a=peigne(jx,jy,k);
    T.push({x:jx,y:jy,a:a+(rnd()-.5)*0.22,
            l:LON*k*(0.82+rnd()*0.45),s:n>=3?3:(n===2?2:0)});
  }
  return T;
}

/* TERRAZZO — Rterr : 7 tessons polygonaux par graine.
   La fibre : chaque tesson est une PLAQUE de poil a son propre peignage. Les
   plaques se lisent parce que la lumiere y tombe autrement — comme sur un
   velours froisse. */
function loiTerrazzo(P,k,rnd){
  var T=[],B=boite(P),cx=(B[0]+B[2])/2,cy=(B[1]+B[3])/2;
  var sp=Math.min(B[2]-B[0],B[3]-B[1]),SH=[];
  for(var e=0;e<7;e++){
    var a=rnd()*TAU,rd=rnd()*sp*0.46;
    var ex=cx+Math.cos(a)*rd,ey=cy+Math.sin(a)*rd;
    var w2=sp*(0.11+rnd()*0.19),h2=sp*(0.08+rnd()*0.15),rot=rnd()*3.1416;
    var sides=4+((rnd()*3)|0),Q=[];
    for(var s2=0;s2<sides;s2++){
      var an=s2/sides*TAU,px=Math.cos(an)*w2*(0.7+rnd()*0.5),py=Math.sin(an)*h2*(0.7+rnd()*0.5);
      Q.push([ex+px*Math.cos(rot)-py*Math.sin(rot), ey+px*Math.sin(rot)+py*Math.cos(rot)]);
    }
    /* on RETRECIT le tesson vers son centre : c'est la gouttiere qui fait
       lire les plaques une par une. Sans elle les sept tessons fondent en un
       seul pate — mesure au rendu precedent. */
    var gx=0,gy=0;
    for(var w=0;w<Q.length;w++){gx+=Q[w][0];gy+=Q[w][1];}
    gx/=Q.length; gy/=Q.length;
    for(w=0;w<Q.length;w++){Q[w][0]=gx+(Q[w][0]-gx)*0.86; Q[w][1]=gy+(Q[w][1]-gy)*0.86;}
    SH.push({P:Q,a:e/7*TAU+rnd()*0.5,s:rnd()<0.34?(rnd()<0.5?2:3):0});
  }
  var pas=PAS*k;
  for(var i=0;i<SH.length;i++){
    var sh=SH[i],b2=boite(sh.P);
    for(var y=b2[1];y<b2[3];y+=pas)for(var x=b2[0];x<b2[2];x+=pas){
      var jx=x+(rnd()-.5)*pas*.8,jy=y+(rnd()-.5)*pas*.8;
      if(!dedans(sh.P,jx,jy)||!dedans(P,jx,jy))continue;
      T.push({x:jx,y:jy,a:sh.a+(rnd()-.5)*0.22,l:LON*k*(0.82+rnd()*0.4),s:sh.s});
    }
  }
  return T;
}

/* TOUFFE — Rtouf : 3 a 5 fleurs, 6 a 8 petales, un coeur orange, une tige.
   C'est LE monde ou la fibre et le motif etaient deja la meme chose. Chaque
   petale devient un FAISCEAU de fibres partant du coeur ; le coeur reste
   orange (heart du moteur) ; la tige est une trainee de fibres. */
function loiTouffe(P,k,rnd){
  var T=[],B=boite(P),cx=(B[0]+B[2])/2,cy=(B[1]+B[3])/2;
  var sp=Math.min(B[2]-B[0],B[3]-B[1]);
  var n=3+((rnd()*3)|0);
  for(var f=0;f<n;f++){
    var ox=cx+(rnd()-.5)*sp*0.86,oy=cy+(rnd()-.5)*sp*0.80;
    var R=sp*(0.13+rnd()*0.20),rot=rnd()*TAU,np=6+((rnd()*3)|0);
    /* la tige */
    var nt=Math.max(8,(sp*0.5/(PAS*k))|0);
    for(var t=0;t<nt;t++){
      var ty=oy+sp*0.5*(t/nt),tx=ox+(rnd()-.5)*4*k*(1-t/nt);
      if(dedans(P,tx,ty))T.push({x:tx,y:ty,a:Math.PI/2+(rnd()-.5)*0.26,
        l:LON*k*(0.7+rnd()*0.4),s:2});
    }
    /* les petales : un faisceau serre par petale, et son LISERE D'ENCRE au
       bord — c'est le _tfStroke(ink) du moteur, rendu en fibres creme. */
    for(var q=0;q<np;q++){
      var pa=rot+q/np*TAU+(rnd()-.5)*0.34;
      var len=R*(0.85+rnd()*0.6),wid=R*(0.26+rnd()*0.16);
      var nb=Math.max(5,(len/(PAS*k*0.9))|0), nv=Math.max(3,(wid/(PAS*k*0.9))|0);
      for(var u=0;u<nb;u++){
        var rr=len*(u+0.5)/nb, ev=wid*(1-Math.abs(rr/len-0.45)*1.1);
        for(var v=-nv;v<=nv;v++){
          var sw=ev*(v/nv);
          var px2=ox+Math.cos(pa)*rr-Math.sin(pa)*sw,
              py2=oy+Math.sin(pa)*rr+Math.cos(pa)*sw;
          if(!dedans(P,px2,py2))continue;
          var bord=(Math.abs(v)===nv)||(u===nb-1);
          T.push({x:px2,y:py2,a:pa+(rnd()-.5)*0.18,
                  l:LON*k*(0.72+rnd()*0.4),s:bord?-2:((u>nb*0.72)?1:0)});
        }
      }
    }
    /* le coeur — orange, comme dans le moteur */
    var nc=Math.max(20,((R*0.30/(PAS*k*0.8))*(R*0.30/(PAS*k*0.8))*3.14)|0);
    for(var c2=0;c2<nc;c2++){
      var ca=rnd()*TAU,cr=R*0.30*Math.sqrt(rnd());
      var hx=ox+Math.cos(ca)*cr,hy=oy+Math.sin(ca)*cr;
      if(dedans(P,hx,hy))T.push({x:hx,y:hy,a:ca,l:LON*k*0.8,s:-1});
    }
  }
  return T;
}

var LOIS={pixel:loiPixel,braille:loiBraille,sillons:loiSillons,gravure:loiGravure,
          mosaique:loiMosaique,encre:loiEncre,terrazzo:loiTerrazzo,touffe:loiTouffe};

function implante(monde,P,k,gr,ang){
  var rnd=graine(gr||7);
  var f=LOIS[monde]||loiEncre;
  return (monde==='gravure')?f(P,k,rnd,ang==null?0.62:ang):f(P,k,rnd);
}

/* ════════════════════════════════════════════════════════════════════════════
   LE PEINTRE D'UNE TOUFFE
   Trois brins d'une meme racine, effiles, la pointe LEGEREMENT plus claire.
   ⚠ acquis de l'audit : eclaircir la pointe vers le blanc lave toute la
   palette en beige. Le lift reste faible (0,05 a 0,20) — c'est le liseré du
   limbe qui donnera la lumiere, jamais le blanchiment de chaque fibre.
   ⚠ acquis : AUCUNE tache speculaire. Le velours est retro-reflectif.
   ════════════════════════════════════════════════════════════════════════════ */
var BRINS=[[0,1.00,0.22],[0.20,0.86,-0.12],[-0.19,0.88,0.34],
           [0.09,0.94,0.40],[-0.10,0.92,-0.30]];
/* ⚑ LE LUSTRE — c'est LUI qui fait la soie, pas le blanchiment de la pointe.
   Un velours ne se lit pas a sa couleur mais a son ANISOTROPIE : deux plages
   de la meme teinte, peignees differemment, ne renvoient pas la meme lumiere.
   C'est exactement ce qui rend un cotele lisible quand la sphere tourne.
   ⚠ Ce degrade-la est un OMBRAGE DE VOLUME, pas la couleur d'une dalle :
   l'audit §6 l'autorise expressement, et l'interdit d'aplat ne le vise pas.
   ⚠ Aucun point chaud : le facteur ne depend que du SENS de la fibre, jamais
   de sa position — une tache speculaire est la signature d'une bille de verre. */
var LUX=[-0.55,-0.835];
function peintTouffe(g,t,cols,heart,ep,ink){
  var c=(t.s===-1)?heart:(t.s===-2)?ink:cols[t.s|0];
  var ca=Math.cos(t.a),sa=Math.sin(t.a);
  var lu=0.70+0.52*(0.5+0.5*(ca*LUX[0]+sa*LUX[1]));
  for(var b=0;b<BRINS.length;b++){
    var da=BRINS[b][0],L=t.l*BRINS[b][1],cb=t.l*BRINS[b][2];
    var a2=t.a+da,c2=Math.cos(a2),s2=Math.sin(a2);
    var nx=-s2,ny=c2, NP=3;
    for(var q=0;q<NP;q++){
      var t0=q/NP,t1=(q+1)/NP,m0=1-t0,m1=1-t1;
      var r0=2*m0*t0*L*0.62+t0*t0*L, o0=2*m0*t0*cb*0.35+t0*t0*cb;
      var r1=2*m1*t1*L*0.62+t1*t1*L, o1=2*m1*t1*cb*0.35+t1*t1*cb;
      /* ⚑ LE CONTRASTE VIENT DE LA PROFONDEUR DU PELAGE, PAS DU BLANC.
         Sous une fourrure dense, la racine est dans l'ombre de ses voisines
         et seule la pointe voit le jour. Sans ce degrade, quatre mille
         touffes qui se recouvrent moyennent vers la pointe et la dalle sort
         lavee. C'est un OMBRAGE DE VOLUME — l'audit §6 l'autorise. */
      var sh=(0.78+0.22*t0)*lu;
      var f=0.02+0.10*t0;
      var r=Math.min(255,(c[0]+(255-c[0])*f)*sh),
          v=Math.min(255,(c[1]+(255-c[1])*f)*sh),
          u=Math.min(255,(c[2]+(255-c[2])*f)*sh);
      g.strokeStyle='rgb('+(r|0)+','+(v|0)+','+(u|0)+')';
      g.lineWidth=Math.max(0.45,ep*(1-t0*0.62));
      g.beginPath();
      g.moveTo(t.x+c2*r0+nx*o0, t.y+s2*r0+ny*o0);
      g.lineTo(t.x+c2*r1+nx*o1, t.y+s2*r1+ny*o1);
      g.stroke();
    }
  }
}

/* peint une cellule entiere. `col` est la couleur de palette de la dalle. */
function peintCellule(g,monde,P,k,col,gr,ang){
  var T=implante(monde,P,k,gr,ang);
  var cols=strates(col), heart=[240,122,46], ink=[246,241,231];
  /* L'ORDRE DE POSE FAIT LE PELAGE : on pose de l'arriere vers l'avant, sinon
     les brins se croisent au hasard et ca fait du feutre, pas de la fourrure.
     Ici la lumiere vient du haut a gauche : on descend. */
  /* le lisere d'encre (-2) et le coeur (-1) passent PAR-DESSUS : c'est le
     _tfStroke(ink) du moteur, et c'est lui qui separe les petales. Sans ce
     biais, les petales fondent et la fleur sort en feuille d'erable. */
  T.sort(function(a,b){
    return (a.y+(a.s===-2?1e6:a.s===-1?2e6:0))-(b.y+(b.s===-2?1e6:b.s===-1?2e6:0));});
  g.save(); g.lineCap='round';
  for(var i=0;i<T.length;i++) peintTouffe(g,T[i],cols,heart,Math.max(0.5,EPA*k),ink);
  g.restore();
  return T.length;
}

window.Fibre={cellulePlane:cellulePlane,dedans:dedans,boite:boite,
  strates:strates,implante:implante,peintCellule:peintCellule,
  peintTouffe:peintTouffe,peigne:peigne,hh:hh,graine:graine,
  mondes:['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons']};
})();
