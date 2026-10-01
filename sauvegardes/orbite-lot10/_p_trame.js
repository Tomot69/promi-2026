/* ════════════════════════════════════════════════════════════════════════════
   LA TRAME — LA SPHERE EST LA TOILE, PAS UNE IMITATION.
   Une cellule de l'Orbite n'est pas « de la couleur de la Toile » : c'est UNE
   VRAIE DALLE DU MOTEUR, rendue par Toile.dalleTrame a l'echelle 1, avec sa
   forme, sa matiere et ses couleurs. Changer de monde ou de palette au Studio
   change la Toile ET l'Orbite, du meme geste.
   ⚠ Regle 1 du §4 de CLAUDE.md : toujours la vraie dalle du moteur, jamais un
   polygone, jamais une approximation.
   ════════════════════════════════════════════════════════════════════════════ */

/* ⚠ PIEGE PAYE ICI, ET IL A COUTE UNE DEMI-HEURE.
   `Toile_resize()` lit le PARENT du canevas hote, pas le canevas :
      var st=host.parentNode; var w=st.clientWidth, h=st.clientHeight;
      if(!w||!h) return;
   Mon hote etait dans un <div style="height:0;overflow:hidden"> : la Toile
   restait a 0x0, seedGray() ne posait rien, plantOne() rendait null, et
   dalleTrame sortait des canevas VIDES — sans une seule erreur, parce qu'elle
   avale la sienne dans un try/catch. Le parent doit avoir une vraie taille. */

/* ⚑ DE GRANDES DALLES, SINON LES MOTIFS NE RESSEMBLENT A RIEN.
   Les trames sont ancrees sur des coordonnees ABSOLUES de Toile, avec des pas
   fixes : pois tous les 9, tesselles tous les 11, carres tous les 5, sillons
   tous les 6. Si on ETIRE une dalle pour la faire tenir dans une cellule, ce
   pas devient quelconque — et le motif ne ressemble plus au design. Il faut
   donc des dalles ASSEZ GRANDES pour qu'on n'ait jamais a les etirer.
   La taille d'une dalle vaut racine(W x H / nombre de cellules). Or seedGray()
   ne repeuple QUE si la Toile est vide : on l'amorce petite (46 cellules),
   puis on AGRANDIT le canevas et relax() etale ces memes 46 cellules sur toute
   la surface. Les dalles passent de 72 a plus de 200 px, au pas absolu
   inchange. C'est la vraie trame, en grand. */
function agrandit(w,h,pids){
  var host=document.getElementById('toileCv'), par=host.parentNode;
  var _w=par.style.width, _h=par.style.height;
  try{
    par.style.width=w+'px'; par.style.height=h+'px';
    host.style.width=w+'px'; host.style.height=h+'px';
    window.Toile_resize();
    window.Toile.sync(pids);
  }catch(e){}
  return function(){
    try{ par.style.width=_w; par.style.height=_h;
         host.style.width=_w; host.style.height=_h;
         window.Toile_resize(); window.Toile.sync(pids); }catch(e){}
  };
}
function bat_trames(pids){
  /* ⚠ ET ON APPELLE VRAIMENT agrandit(). Je l'avais ecrite et jamais appelee :
     les dalles restaient a 70-150 px, il fallait donc replier au miroir pour
     couvrir une cellule — d'ou des CHEVRONS sur la gravure, tres visibles.
     Avec des dalles de 200 a 380 px, plus rien ne se replie. */
  /* ⚑ ON NE PASSE PLUS PAR `dalleTrame` — ELLE COUPE LES MARQUES EN DEUX.
     Mesure (scratchpad/verite.html), monde par monde, contre la meme dalle
     prelevee sur la Toile peinte : encre, touffe et terrazzo coincident ; les
     cinq TRAMES non, et toujours pareil. `dalleTrame` refait l'attribution
     PIXEL PAR PIXEL et efface l'alpha hors cellule : demi-points de braille,
     demi-carreaux de mosaique, hachures tranchees — et sur pixel, l'escalier
     de 5 px, la signature du monde, remplace par un polygone lisse.
     Sur la vraie Toile, une marque appartient a UNE graine et se peint
     ENTIERE : le bord d'une dalle y est quantifie par la trame, jamais lisse.
     `DallesDeMonde` rend les vraies dalles, marques entieres, bord net, et
     SANS ATTENDRE (Toile.preview peint en ligne — voir _f_dalle.js).
     ⚠ `agrandit()` ci-dessus n'est plus appelee : on ne touche plus a la
     taille de la Toile de l'app. Elle est conservee, son piege documente. */
  /* ⚑ ON NE PRELEVE PLUS RIEN — LE MOTEUR GENERE CHAQUE DALLE.
     Tout ce qu'on avait avant DECOUPAIT dans une Toile deja peinte :
       · `dalleTrame` coupe les marques en deux (demi-pois, demi-carreaux, et
         l'escalier de `pixel` remplace par un polygone lisse) ;
       · l'extraction par la couleur rendait des marques entieres, mais restait
         un tri dans une image de Toile — « des photos de la Toile detourees
         encadrees », et c'est refuse.
     `Toile.dalleGeneree` fait l'inverse : on lui donne UNE CELLULE, il la
     PEINT avec son propre code, au pas absolu, echelle 1. La cellule se
     fabrique en posant une graine voisine EN MIROIR de chaque cote — la
     bissectrice EST alors ce cote — et c'est le moteur qui decide, avec sa
     regle, quelle marque appartient a qui. Une marque reste donc entiere.
     Puis la dalle se separe de son fond par DIFFERENCE DE DEUX RENDUS : le
     meme jeu de graines, au meme instant, la graine cible plantee puis grise.
     Ce qui differe lui appartient — son lisere d'encre et son coeur orange
     compris. Rien n'est devine, rien n'est detoure, rien ne se superpose.

     Verifie, part de matiere dans LA MEME cellule, Toile / generee :
        encre -4,5 · mosaique +0,7 · touffe -3,8 · braille -2,6
        pixel -2,1 · terrazzo +3,7 · gravure +1,4 · sillons -0,2
     (scratchpad/probe_gen2.py, critere identique des deux cotes) */
  var mo=Toile.getTheme(), pa=Toile.getPalette(), BRUT=[];
  for(var q=0;q<pids.length;q++){
    var ab=null; try{ ab=Toile.dalleAbs(pids[q]); }catch(e){}
    if(!ab||!ab.poly||ab.poly.length<3) continue;
    var c=document.createElement('canvas'), ok=false;
    try{ ok=Toile.dalleGeneree(c,{monde:mo, palette:pa, poly:ab.poly,
           ci:q%4, lit:(q*3)%5, ang:((q*47)%180)*Math.PI/180,
           tone:[1.0,0.76,1.24,0.88,1.12][q%5], pad:22}); }catch(e){}
    if(!ok||!c.width) continue;
    var g=c.getContext('2d');
    /* ⚑ ON GARDE LA CELLULE, PAS SEULEMENT LE DESSIN.
       Une dalle de `touffe` a des tiges qui descendent d'une demi-cellule et
       des fleurs qui debordent : la BOITE DE SON DESSIN vaut deux fois sa
       cellule. Caler cette boite sur la cellule de la sphere rapetissait donc
       les fleurs de moitie — mesure a l'ecran, elles sortaient en mouchetis.
       Sur la Toile, une fleur est dimensionnee par rapport a SA CELLULE. On
       transporte donc le polygone et la graine, et c'est eux qui donnent
       l'echelle. */
    var pl=c.__poly, si=c.__site, dpr=c.width/Math.max(1,c.__box[2]);
    var ax=1e9,ay=1e9,bx=-1e9,by=-1e9;
    for(var z=0;z<pl.length;z++){
      if(pl[z][0]<ax)ax=pl[z][0]; if(pl[z][0]>bx)bx=pl[z][0];
      if(pl[z][1]<ay)ay=pl[z][1]; if(pl[z][1]>by)by=pl[z][1]; }
    BRUT.push({w:c.width, h:c.height, d:g.getImageData(0,0,c.width,c.height).data,
               cw:(bx-ax)*dpr, ch:(by-ay)*dpr, sx:si[0]*dpr, sy:si[1]*dpr});
  }
  return bat_depuis(BRUT);
}

/* ════════════════════════════════════════════════════════════════════════════
   ⚑ UNE DALLE PAR CELLULE — et c'est le dernier « a peu pres » qui saute.
   Avec vingt dalles pour soixante-dix-sept cellules, chaque forme revenait
   quatre fois, et AUCUNE n'etait la cellule qu'elle occupait : on posait une
   dalle etrangere, mise a l'echelle, dans un contour qui n'etait pas le sien.
   Ici on demande au moteur de peindre, pour CHAQUE cellule, une dalle dans le
   contour EXACT de cette cellule-la. Plus de repetition, plus de mise a
   l'echelle par cellule, plus de contour d'emprunt.

   ⚠ LA CELLULE NE SE DEVINE PAS, ELLE SE MESURE. L'attribution du semis est
   `acos(p.s) - w` : ce n'est pas un Voronoi ordinaire, et un polygone
   reconstruit sans les poids rate le bord de 12 % du rayon. On lance donc des
   rayons depuis la graine, dans 24 directions, et on cherche par dichotomie
   l'angle ou l'attribution BASCULE. C'est la vraie frontiere, celle que la
   fourrure utilisera.
   ════════════════════════════════════════════════════════════════════════════ */
function celluleDe(S,k,NDIR,PXR){
  var sx=S.sx[k], sy=S.sy[k], sz=S.sz[k], NS=S.sites, P=[];
  var e1x=S.e1[k*3], e1y=S.e1[k*3+1], e1z=S.e1[k*3+2];
  var e2x=S.e2[k*3], e2y=S.e2[k*3+1], e2z=S.e2[k*3+2];
  function aQui(px,py,pz){
    var bq=0, bd=1e9;
    for(var q=0;q<NS;q++){
      var dp=px*S.sx[q]+py*S.sy[q]+pz*S.sz[q];
      if(dp>1)dp=1; else if(dp<-1)dp=-1;
      var d=Math.acos(dp)-(S.wt?S.wt[q]:0);
      if(d<bd){bd=d;bq=q;}
    }
    return bq;
  }
  var TMAX=Math.min(1.1, (S.ray&&S.ray[k]?S.ray[k]*1.7:0.7));
  for(var i=0;i<NDIR;i++){
    var a=i/NDIR*6.283185307179586, ca=Math.cos(a), sa=Math.sin(a);
    var dx=e1x*ca+e2x*sa, dy=e1y*ca+e2y*sa, dz=e1z*ca+e2z*sa;
    var lo=0, hi=TMAX;
    for(var it=0;it<16;it++){
      var t=(lo+hi)*0.5, ct=Math.cos(t), st=Math.sin(t);
      if(aQui(sx*ct+dx*st, sy*ct+dy*st, sz*ct+dz*st)===k) lo=t; else hi=t;
    }
    var r=Math.sin(lo)*PXR;
    P.push([r*ca, r*sa]);
  }
  return P;
}

function bat_cellules(S,PXR,pids){
  var mo=Toile.getTheme(), pa=Toile.getPalette(), BRUT=[];
  for(var k=0;k<S.sites;k++){
    var P=celluleDe(S,k,24,PXR);
    /* ⚑ L'ESPACEMENT SE PREND SUR CETTE CELLULE-CI, PAS SUR LA TOILE DE L'APP.
       `Renc`, `Rterr` et `Rtouf` dimensionnent leur marque sur `sp`. En lui
       laissant la valeur de la Toile (59 px) alors qu'une cellule de sphere en
       fait 45, les lobes debordaient si loin que les voisines les recouvraient :
       la difference des deux rendus ne trouvait presque rien, et les trois
       mondes libres tombaient de 146 000 touffes peintes a 8 800. Mesure. */
    var rm=0; for(var z2=0;z2<P.length;z2++) rm+=Math.hypot(P[z2][0],P[z2][1]);
    rm=rm/Math.max(1,P.length);
    /* ⚑ LA PHASE GLOBALE DE CETTE CELLULE.
       Le repere tangent est deja commun aux mondes ancres (est / nord, pose
       par `semisPavage` quand `tourne` est faux). Il manquait l'ORIGINE : on
       la prend dans une parametrisation de la sphere dont le gradient suit ce
       repere — longitude x cos(latitude) vers l'est, latitude vers le nord.
       ⚠ Aucune parametrisation ne peut etre exacte partout (c'est Gauss : la
       sphere n'est pas developpable). Elle l'est AU PREMIER ORDRE entre deux
       cellules voisines, et c'est tout ce qu'il faut pour que le raccord ne se
       voie pas. */
    var la=Math.asin(Math.max(-1,Math.min(1,S.sy[k])));
    var lo=Math.atan2(S.sz[k],S.sx[k]);
    var PH=[lo*Math.cos(la)*PXR, la*PXR];
    var c=document.createElement('canvas'), ok=false;
    try{ ok=Toile.dalleGeneree(c,{monde:mo, palette:pa, poly:P, site:[0,0], sp:2*rm, phase:PH,
           ci:S.ci[k], lit:(k*3)%5, ang:((k*47)%180)*Math.PI/180,
           tone:[1.0,0.76,1.24,0.88,1.12][S.ti?S.ti[k]%5:k%5], pad:18}); }catch(e){}
    if(!ok||!c.width){ BRUT.push(null); continue; }
    var g=c.getContext('2d'), si=c.__site, dpr=c.width/Math.max(1,c.__box[2]);
    BRUT.push({w:c.width, h:c.height, d:g.getImageData(0,0,c.width,c.height).data,
               cw:c.width, ch:c.height, sx:si[0]*dpr, sy:si[1]*dpr});
  }
  var T=bat_depuis(BRUT.filter(function(x){return x;}), BRUT);
  if(T){
    T.parCell=true; T.pxr=PXR;
    /* ⚠ LE MASQUE EST EN PIXELS REELS, PAS EN PIXELS CSS. `dalleGeneree` rend
       un canevas de `dw x DPR` : un radian y vaut donc PXR x DPR pixels, pas
       PXR. Sans ce facteur l'echantillon tombe deux fois trop loin, hors de la
       dalle — mesure : la sphere passait de 100 000 touffes peintes a 9 500. */
    T.pxrpx=PXR*Math.min(2,window.devicePixelRatio||1);
  }
  return T;
}

/* le traitement commun : table de couleurs, strates, cartes d'indices */
function bat_depuis(BRUT,ORDRE){
  if(!BRUT.length) return null;
  /* LA TABLE DE COULEURS : on collecte les teintes reellement peintes, on les
     quantifie sur 5 bits par canal, et on garde les 96 plus frequentes. Touffe
     en sort 119 distinctes ; encre, six. Une table par monde, donc. */
  var cnt={}, k;
  for(k=0;k<BRUT.length;k++){
    var d=BRUT[k].d;
    for(var i=0;i<d.length;i+=4){
      if(d[i+3]<10) continue;
      var q5=((d[i]>>3)<<10)|((d[i+1]>>3)<<5)|(d[i+2]>>3);
      cnt[q5]=(cnt[q5]||0)+1;
    }
  }
  var cles=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a];}).slice(0,96);
  var COL=[], q5v=[];
  for(k=0;k<cles.length;k++){
    var v=+cles[k];
    COL.push([((v>>10)&31)*8+4, ((v>>5)&31)*8+4, (v&31)*8+4]);
    q5v.push(v);
  }
  /* le rapprochement se fait A LA DEMANDE, pas sur les 32 768 cases : une
     dalle ne porte jamais plus de cent cinquante teintes distinctes, et un
     balayage complet du cube coutait deux millions de distances PAR MONDE. */
  var MEM={};
  function proche(v){
    if(MEM[v]!==undefined) return MEM[v];
    var r=((v>>10)&31)*8+4, gg=((v>>5)&31)*8+4, b=(v&31)*8+4, best=0, bd=1e9;
    for(var k=0;k<COL.length;k++){
      var dr=COL[k][0]-r, dg=COL[k][1]-gg, db=COL[k][2]-b, dd=dr*dr+dg*dg+db*db;
      if(dd<bd){bd=dd;best=k;}
    }
    return (MEM[v]=best);
  }
  /* chaque dalle devient une carte d'indices : 0 = le vide, n = la teinte n-1 */
  var DAL=[];
  for(k=0;k<BRUT.length;k++){
    var B=BRUT[k], m=new Uint8Array(B.w*B.h);
    for(var j=0,pp=0;j<B.d.length;j+=4,pp++){
      if(B.d[j+3]<10) continue;
      m[pp]=1+proche(((B.d[j]>>3)<<10)|((B.d[j+1]>>3)<<5)|(B.d[j+2]>>3));
    }
    var R=inscrit(m,B.w,B.h);
    if(!R) continue;
    /* ⚑ L'ETENDUE REELLEMENT PEINTE, pas la taille du canevas.
       dalleTrame rend la dalle dans un canevas plus grand qu'elle : il ajoute
       une marge `pad` qui vaut 0,85 fois l'espacement pour encre, terrazzo et
       touffe (ces trois-la DEBORDENT de leur cellule sur la Toile). En calant
       le CANEVAS sur la cellule, la dalle s'y retrouvait deux fois trop petite
       et noyee dans du fond — c'est pour ca que touffe ne se voyait pas. */
    var bx=B.w, by=B.h, bX=-1, bY=-1;
    for(var yb=0;yb<B.h;yb++) for(var xb=0;xb<B.w;xb++) if(m[yb*B.w+xb]){
      if(xb<bx)bx=xb; if(xb>bX)bX=xb; if(yb<by)by=yb; if(yb>bY)bY=yb; }
    if(bX<0) continue;
    /* LE REMPLISSAGE DU RECTANGLE INSCRIT : c'est lui qui dit combien de poils
       ce monde peindra. Encre en couvre plus de neuf dixiemes, gravure un
       quart — sans compensation, l'Orbite en gravure sort deux fois moins
       fournie que la meme en encre, alors que ce n'est pas ce qu'on veut voir. */
    var pl=0, tot=0;
    for(var yy=R.y;yy<R.y+R.h;yy++) for(var xx=R.x;xx<R.x+R.w;xx++){
      if(yy<0||xx<0||yy>=B.h||xx>=B.w) continue;
      tot++; if(m[yy*B.w+xx]) pl++;
    }
    /* ⚑ LA SILHOUETTE FERMEE — et c'est elle qui reconcilie le contour et la
       masse.
       En ne faisant pousser la fourrure que sur les MARQUES, on obtient bien
       le vrai contour... et une sphere squelettique : une trame est vide a 60
       ou 80 % (gravure 25 % de matiere, braille 27 %, sillons 27 %). Mesure a
       l'ecran : touffe passait d'une boule fournie a des lambeaux.
       Or les deux ne sont pas la meme chose. Le CONTOUR d'une dalle, c'est
       l'enveloppe de ses marques — l'escalier de pixel, le bord quantifie de
       mosaique, le pourtour d'un bouquet de touffe. Les TROUS de la trame, eux,
       sont de la matiere absente A L'INTERIEUR : sur la Toile ils laissent voir
       le fond, ils ne decoupent pas la dalle.
       On ferme donc la silhouette par balayage en lignes ET en colonnes — la
       meme fermeture que `inscrit` — et la fourrure pousse dans TOUTE la
       silhouette. La trame n'y dit plus la presence : elle y dit LA CLARTE.
       Contour reel + masse pleine, sans avoir a choisir. */
    var sil=new Uint8Array(B.w*B.h);
    (function(){
      var mnx=new Int32Array(B.h), mxx=new Int32Array(B.h),
          mny=new Int32Array(B.w), mxy=new Int32Array(B.w), xa, ya;
      for(ya=0;ya<B.h;ya++){mnx[ya]=B.w;mxx[ya]=-1;}
      for(xa=0;xa<B.w;xa++){mny[xa]=B.h;mxy[xa]=-1;}
      for(ya=0;ya<B.h;ya++)for(xa=0;xa<B.w;xa++) if(m[ya*B.w+xa]){
        if(xa<mnx[ya])mnx[ya]=xa; if(xa>mxx[ya])mxx[ya]=xa;
        if(ya<mny[xa])mny[xa]=ya; if(ya>mxy[xa])mxy[xa]=ya; }
      for(ya=0;ya<B.h;ya++)for(xa=0;xa<B.w;xa++)
        if(xa>=mnx[ya]&&xa<=mxx[ya]&&ya>=mny[xa]&&ya<=mxy[xa]) sil[ya*B.w+xa]=1;
    })();
    DAL.push({w:B.w, h:B.h, m:m, sil:sil, diag:Math.hypot(B.w,B.h),
              rx:R.x, ry:R.y, rw:R.w, rh:R.h, plein:tot?pl/tot:1,
              bx:bx, by:by, bw:bX-bx+1, bh:bY-by+1,
              /* la CELLULE et la GRAINE — c'est d'elles que vient l'echelle */
              cw:B.cw||(bX-bx+1), ch:B.ch||(bY-by+1),
              sx:(B.sx!=null?B.sx:(bx+bX)*0.5), sy:(B.sy!=null?B.sy:(by+bY)*0.5),
              cx:(bx+bX)*0.5, cy:(by+bY)*0.5});
  }
  /* quand on batit une dalle PAR CELLULE, l'ordre doit etre conserve : la
     cellule k lit DAL[k]. On reinsere donc les trous (cellules ratees) en
     recopiant la premiere dalle valide — jamais en decalant l'index. */
  if(ORDRE){
    var PARC=[], vu=0, secours=DAL[0];
    for(var z=0;z<ORDRE.length;z++){
      if(ORDRE[z] && DAL[vu]) PARC.push(DAL[vu++]);
      else PARC.push(secours);
    }
    DAL=PARC;
  }
  var moy=0; for(k=0;k<DAL.length;k++) moy+=DAL[k].plein;
  moy=DAL.length?moy/DAL.length:1;
  /* ⚑ LE CLAIR-OBSCUR DES STRATES D'UNE MEME DALLE.
     Le moteur ne peint pas une dalle d'un seul aplat : il en module le ton
     (TON, LITS) — c'est ce qui donne les strates d'une encre ou d'un terrazzo.
     En ne gardant que « matiere ou vide » je les perdais, et les dalles
     sortaient en PATES. On mesure donc, pour chaque teinte relevee, son ecart
     de clarte a la mediane du monde : c'est ce decalage-la qu'on reportera sur
     la couleur de la cellule, en marches. */
  var Ls=[]; for(k=0;k<COL.length;k++) Ls.push(r2h(COL[k])[2]);
  var tri=Ls.slice().sort(function(a,b){return a-b;});
  var med=tri[tri.length>>1]||0.5;
  var DL=new Int8Array(COL.length);
  for(k=0;k<COL.length;k++){
    /* ⚠ DISCRET. A 26 marches par unite de clarte, une strate claire sautait
       de sept marches d'un coup — droit dans la partie qui deteint vers la
       creme — et TOUTE la sphere se lavait de blanc. Les strates nuancent une
       dalle, elles ne la repeignent pas. */
    var d=Math.round((Ls[k]-med)*9);
    DL[k]=d<-3?-3:(d>3?3:d);
  }
  return {dalles:DAL, col:COL, dl:DL, cle:'', plein:moy};
}

/* ⚑ LE PLUS GRAND RECTANGLE INSCRIT DANS LA DALLE — et c'est ce qui rend les
   ecarts coherents.
   Je decoupais la cellule avec LA SILHOUETTE de la dalle : une dalle dont les
   proportions ne collaient pas a sa cellule y laissait une grosse marge, et
   celle d'a cote presque rien. D'ou des joints tantot enormes tantot nuls —
   rien a voir avec une Toile, ou le filet entre deux dalles est toujours le
   meme. On ne prend donc que L'INTERIEUR de la dalle, et le joint devient une
   valeur ANGULAIRE CONSTANTE, posee par le pavage.
   ⚠ Les trous de la TRAME, eux, restent : les pois du braille, les sillons,
   les stries de la gravure sont de la matiere absente, pas un bord de dalle. */
function inscrit(m,w,h){
  /* le plein : on ferme la silhouette par balayage en lignes ET en colonnes,
     sinon les mondes creux (gravure, 22 % de pixels) n'ont pas d'interieur */
  var minx=new Int32Array(h), maxx=new Int32Array(h),
      miny=new Int32Array(w), maxy=new Int32Array(w), x,y;
  for(y=0;y<h;y++){minx[y]=w;maxx[y]=-1;}
  for(x=0;x<w;x++){miny[x]=h;maxy[x]=-1;}
  var cx=0, cy=0, n=0;
  for(y=0;y<h;y++)for(x=0;x<w;x++) if(m[y*w+x]){
    if(x<minx[y])minx[y]=x; if(x>maxx[y])maxx[y]=x;
    if(y<miny[x])miny[x]=y; if(y>maxy[x])maxy[x]=y;
    cx+=x; cy+=y; n++;
  }
  if(!n) return null;
  cx/=n; cy/=n;
  function dedans(X,Y){
    X|=0; Y|=0;
    if(X<0||Y<0||X>=w||Y>=h) return false;
    return X>=minx[Y] && X<=maxx[Y] && Y>=miny[X] && Y<=maxy[X];
  }
  for(var s=1.0;s>0.18;s-=0.02){
    var a=w*0.5*s, b=h*0.5*s, ok=0, tot=0;
    for(var t=0;t<=40;t++){
      var f=t/40;
      var pts=[[cx-a+2*a*f,cy-b],[cx-a+2*a*f,cy+b],[cx-a,cy-b+2*b*f],[cx+a,cy-b+2*b*f]];
      for(var q=0;q<4;q++){ tot++; if(dedans(pts[q][0],pts[q][1])) ok++; }
    }
    if(ok/tot>=0.95)
      return {x:Math.round(cx-a), y:Math.round(cy-b),
              w:Math.max(4,Math.round(2*a)), h:Math.max(4,Math.round(2*b))};
  }
  return {x:Math.round(cx-w*0.09), y:Math.round(cy-h*0.09),
          w:Math.max(4,Math.round(w*0.18)), h:Math.max(4,Math.round(h*0.18))};
}
