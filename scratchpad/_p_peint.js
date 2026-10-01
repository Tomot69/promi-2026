/* ════════════════════════════════════════════════════════════════════════════
   LE PEINTRE — tout allume : relief a amplitude variable, palette du Studio,
   dalles de tailles variees, et le doigt qui s'enfonce pour de bon.
   ════════════════════════════════════════════════════════════════════════════ */
var ORI=24, NIVA=6, NVAR=3;
/* ⚑ LE CHAMP DE FLUX — les poils sont PEIGNES, pas plantes au hasard.
   Un hachage par point donne un herisson ; un champ lisse donne une fourrure,
   et c'est lui qui fait « immerge dans un liquide ». On prend le gradient
   tangent d'un scalaire basse frequence : les poils tournent en volutes
   lentes, jamais en bandes. */
function flux(x,y,z,t){
  var e=0.03, f=function(a,b,c){
    return Math.sin(2.1*a+0.7+t)*Math.cos(1.7*b+1.9)*Math.sin(1.9*c+0.4)
         + 0.55*Math.sin(3.3*c-1.1+t*0.6)*Math.cos(2.9*a+0.5);};
  var gx=(f(x+e,y,z)-f(x-e,y,z)), gy=(f(x,y+e,z)-f(x,y-e,z)), gz=(f(x,y,z+e)-f(x,y,z-e));
  var d=gx*x+gy*y+gz*z;
  return [gx-d*x, gy-d*y, gz-d*z];
}
var SIX=[[0.34,0.30],[1.42,0.58],[2.31,0.86],[3.55,0.44],[4.48,0.72],[5.63,0.94]];

function peint(cv,o){
  var CSS=o.css||520, W=CSS*D;
  cv.width=W; cv.height=W;
  var g=cv.getContext('2d');
  g.fillStyle=o.fond||'#131319'; g.fillRect(0,0,W,W);
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
  var LX=-0.42, LY=-0.58, LZ=0.700, DOS=o.dos||1;
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
  var DILUE=((o.trame&&o.trame.plein)||1)>0.34;
  /* l'indice de la teinte grise dans la rampe : la boucle de versement s'en
     sert pour raccourcir le grain du sol. */
  var TCOL=(TR.col&&TR.col.length)?TR.col:(o.pal||[[143,160,255]]);
  var NCOL=TCOL.length;
  for(var c=0;c<NCOL;c++){ var RP=rampeCouleur(TCOL[c]);
    for(var m4=0;m4<MARCHES;m4++) COL.push(pack(RP[m4])); }
  var RPG=rampeCouleur(GRIS);
  for(var m5=0;m5<MARCHES;m5++) COL.push(pack(RPG[m5]));   /* la cellule vide */
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
  if(!ENR && S.__dalCle!==TR.cle){
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
  var CD=ENR?null:S.__dal, CK=ENR?null:S.__ech, CU=ENR?null:S.__cu, CV=ENR?null:S.__cv;

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

  var CLE=(TR.cle||'')+'|'+(o.kn||2.5)+'|'+(o.tflux||0)+'|'+PXR.toFixed(1)+'|'+LIBRE;
  if(S.__stCle!==CLE){
    var _PH=new Float32Array(N), _GX=new Float32Array(N), _GY=new Float32Array(N),
        _GZ=new Float32Array(N), _FX=new Float32Array(N), _FY=new Float32Array(N),
        _FZ=new Float32Array(N), _CI=new Int16Array(N);
    var e=0.013;
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
      var fl0=flux(x0,y0,z0,o.tflux||0), fm0=nrm3(fl0[0],fl0[1],fl0[2])||1;
      _FX[i]=fl0[0]/fm0; _FY[i]=fl0[1]/fm0; _FZ[i]=fl0[2]/fm0;
      /* ⚑ LA LECTURE DE LA TOILE ENROULEE.
         Lambert azimutale equivalente : k = racine(2/(1+z)), u = k x, v = k y.
         Le disque a pour rayon 2, on l'echelle en pixels par PXR. Aucun
         montage, aucun choix de dalle : le poil lit la Toile a l'endroit ou il
         se trouve, et c'est tout. */
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
    var Q=new Float32Array(NG*10), CIX=new Int16Array(NG), BRD=new Uint8Array(NG);
    var pos=new Int32Array(NP);
    pos.set(CNT.subarray(0,NP));
    for(var gj=0;gj<NG;gj++){
      i=GARDE[gj];
      var d2=pos[PID[gj]]++, o2=d2*10;
      Q[o2]=P[i*3]; Q[o2+1]=P[i*3+1]; Q[o2+2]=P[i*3+2];
      Q[o2+3]=_GX[i]; Q[o2+4]=_GY[i]; Q[o2+5]=_GZ[i];
      Q[o2+6]=_PH[i];
      Q[o2+7]=_FX[i]; Q[o2+8]=_FY[i]; Q[o2+9]=_FZ[i];
      CIX[d2]=_CI[i]; BRD[d2]=S.bord[i];
    }
    S.__st={Q:Q, ci:CIX, bd:BRD, pd:PD, pst:PST, np:NP, n:NG};
    S.__stCle=CLE;
  }
  var ST=S.__st, Q=ST.Q, CIX=ST.ci, BRD=ST.bd, PD=ST.pd, PST=ST.pst, NP=ST.np;
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
        nx=ccx; ny=ccy; nz=ccz; pl=1; rr=1; omb=c1.ombre;
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
    var dl=nX*LX+nY*LY+nZ2*LZ; if(dl<0)dl=0;
    /* UN AMBIANT : sans lui la moitie de la boule est noire et la palette
       ne se voit nulle part. Le volume vient du contraste, pas du noir. */
    var fi=nX*FX2+nY*FY2+nZ2*FZ2; if(fi<0)fi=0;
    var lum=0.34+0.52*p074(dl)+0.26*fi*fi;
    /* LE LISERE DU LIMBE : un vrai volume se signe par son bord. C'est aussi
       lui qui affirme le cercle exact — le contour se voit au lieu de se
       deviner. Terme de Fresnel : il ne depend que de l'angle de vue. */
    lum+=0.30*p34(1-(nZ2<0?-nZ2:nZ2));
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
    if(dedans) lum*=0.20+0.62*lisse(-0.55,0.62,-dOM[i]);
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
    var mar=(lum*11.0+1.6+strate)|0;
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
    var pres=(0.07+0.93*lisse(0.0081,0.0841,rho2q))
             *(dedans?1:(0.62+0.38*lum));   /* le cote a l'ombre ne s'efface plus */
    var niv=(pres*NIVA)|0; if(niv>=NIVA)niv=NIVA-1; if(niv<0)niv=0;
    var zz=(Z2+1)*0.5, tai=(zz*TAI.length)|0;
    if(tai>=TAI.length)tai=TAI.length-1; if(tai<0)tai=0;
    /* le sol gris porte le grain le plus court : il fait le volume, pas le motif */
    if(ci>=NCOL && tai>0) tai--;
    /* couches, donc plus courts a l'ecran : un poil rabattu se raccourcit */
    if(mo && tai>0) tai--;
    /* ⚑ LE POIL NE RACCOURCIT PLUS AU BORD — ET C'EST LE COEUR DU FLUFFY.
       Il raccourcissait deux fois pres du filet, « pour que le contour reste
       net ». Mais un bord net, c'est justement ce qui fait une decoupe : la
       ou une fourrure se lit le plus, c'est AU BORD, quand les meches passent
       par-dessus le vide. Tom : « une boule qu'on a envie d'ecraser ».
       On garde donc la pleine longueur jusqu'au filet, et on ne raccourcit
       plus qu'au tout dernier rang — juste assez pour que deux dalles voisines
       ne se rejoignent pas et que le vide reste lisible (exigence 4). */
    var bo=BRD[i];
    if(bo<18 && tai>0) tai--;
    /* L'ORIENTATION DU POIL : la direction du flux, projetee a l'ecran.
       Sur 24 secteurs et 2 pi — un poil a une racine et une pointe. */
    var fu,fv,fw;
    if(mo){ fu=dFX[i]; fv=dFY[i]; fw=dFZ[i]; }
    else  { fu=Q[qb+7]; fv=Q[qb+8]; fw=Q[qb+9]; }
    var fX=fu*cl+fw*sl, fZt=-fu*sl+fw*cl, fY=fv*ct-fZt*st;
    var ori=secteur(fX,fY,ORI)*NVAR + (i%NVAR);
    if(o.sansBoucle){ nap+=3; continue; }
    if(Z2<0){ av[nav]=py*W+px; av[nav+1]=(tai*ORI*NVAR+ori)*NIVA+niv; av[nav+2]=ci*MARCHES+mar; nav+=3; }
    else    { ap[nap]=py*W+px; ap[nap+1]=(tai*ORI*NVAR+ori)*NIVA+niv; ap[nap+2]=ci*MARCHES+mar; nap+=3; }
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
  if(!o.nu) disques(B,W,CX,CY,R,o.pal);
  og.putImageData(cv.__im,0,0);
  g.drawImage(cv.__off,0,0);
  if(!o.nu) noyau(g,CX,CY,R);       /* rien ne passe devant ton Noyau */
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
function verse(A,COL,L,n,B,W){
  var OF=A.__off, AL=A.__alp, ST=A.__sta;
  for(var i=0;i<n;i+=3){
    var t=L[i+1], a=ST[t], b2=ST[t+1], bas=L[i], col=COL[L[i+2]];
    for(var j=a;j<b2;j++) B[bas+OF[j]]=(AL[j]|col)>>>0;
  }
}
/* les six, trames DANS le tampon pour qu'ils restent dedans */
function disques(B,W,CX,CY,R,PAL){
  for(var i=0;i<SIX.length;i++){
    var th=SIX[i][0], rho=SIX[i][1];
    var x0=CX+Math.cos(th)*rho*R, y0=CY+Math.sin(th)*rho*R*0.46;
    var r=0.047*R, halo=r+0.013*R, ep=Math.max(1.4,0.0105*R);
    var c=PAL[i%PAL.length], col=pack(c), enc=pack([19,19,25]);
    var r2=r*r, h2=halo*halo, ri=(r-ep)*(r-ep);
    for(var y=Math.max(1,(y0-halo)|0); y<Math.min(W-1,(y0+halo+1)|0); y++){
      var dy=y-y0, base=y*W;
      for(var x=Math.max(1,(x0-halo)|0); x<Math.min(W-1,(x0+halo+1)|0); x++){
        var dx=x-x0, d2=dx*dx+dy*dy;
        if(d2>h2) continue;
        B[base+x] = d2>r2 ? (0xE0000000|enc)>>>0
                  : (d2>ri ? (0xF0000000|col)>>>0 : (0xF0000000|enc)>>>0);
      }
    }
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
    g.fillStyle='rgba(19,19,25,.88)'; g.fill();
    g.beginPath(); g.arc(x,y,r,0,TAU);
    g.fillStyle='rgba(19,19,25,1)'; g.fill();
    g.lineWidth=Math.max(1.4,0.0105*R); g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')'; g.stroke();
  }
}
function noyau(g,CX,CY,R){
  /* plus petit, et cercle d'encre autour : au diametre precedent il perçait un
     trou dans la composition au lieu d'y tenir sa place. */
  var r=0.080*R;
  g.beginPath(); g.arc(CX,CY,r+0.034*R,0,TAU); g.fillStyle='rgba(19,19,25,.94)'; g.fill();
  g.beginPath(); g.arc(CX,CY,r,0,TAU); g.fillStyle='#F4EEE1'; g.fill();
}
