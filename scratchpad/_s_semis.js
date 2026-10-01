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
