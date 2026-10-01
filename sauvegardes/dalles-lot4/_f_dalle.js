/* ════════════════════════════════════════════════════════════════════════════
   LA VRAIE DALLE — CELLE QUE LE MOTEUR A PEINTE SUR LA TOILE

   ⚑ CE QUI ETAIT FAUX, ET LA MESURE QUI LE PROUVE (scratchpad/verite.html).
   J'ai compare, monde par monde, la dalle rendue par `Toile.dalleTrame` a LA
   MEME DALLE prelevee sur la Toile peinte. Verdict :
     encre, touffe        elles coincident.
     les six autres       elles ne coincident pas, et toujours de la meme facon.
   `dalleTrame` refait l'attribution PIXEL PAR PIXEL et efface l'alpha des
   pixels qui ne tombent pas dans la cellule. Il DECOUPE DONC LES MARQUES EN
   DEUX : des demi-points de braille, des demi-carreaux de mosaique, des
   hachures tranchees net. Et sur pixel, l'escalier de 5 px — la signature du
   monde — disparait au profit d'un polygone lisse.
   Sur la vraie Toile c'est l'inverse : chaque marque appartient a UNE graine
   et se peint ENTIERE. Le bord d'une dalle est donc quantifie par la trame,
   jamais lisse.
   C'est exactement ce que Tom a vu : « des screenshots de dalles dans un
   cadre ». Le cadre, c'etait ce polygone.

   ⚑ CE QU'ON FAIT A LA PLACE — ON N'EXTRAIT PLUS PAR LA FORME, MAIS PAR LA
   COULEUR.
   Le moteur peint la Toile entiere, correctement. On y preleve la dalle par
   son APPARTENANCE : le moteur garantit qu'une dalle coloree n'a jamais la
   couleur d'une voisine (`cc()` ecarte les couleurs des voisines, `tones()`
   ecarte leurs marches de clarte). Sa teinte exacte est donc UNIQUE dans son
   voisinage. On garde les pixels de cette teinte, dans la cellule elargie
   d'une demi-periode de trame — et les marques restent ENTIERES, coupees
   exactement la ou le moteur les a coupees.
     · aucun redimensionnement   · aucun deplacement   · aucun redessin
     · a l'echelle 1, pixel pour pixel
   ⚠ Ce n'est pas le rejet capital de l'audit §2 : celui-la vise le fait de
   prendre l'IMAGE d'une dalle pour DECOUPER UNE AUTRE FORME. Ici on ne
   decoupe rien : on garde ce que le moteur a peint, tel qu'il l'a peint.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){

/* ── la cellule est convexe (Voronoi) : la distance signee au polygone est le
      max des distances signees aux droites de ses cotes. « Elargir » revient
      donc a comparer ce max a une marge — exact, et en quelques lignes. ─── */
function distPoly(P,x,y){
  var n=P.length, cx=0, cy=0, i;
  for(i=0;i<n;i++){cx+=P[i][0];cy+=P[i][1];}
  cx/=n; cy/=n;
  var mx=-1e9;
  for(i=0;i<n;i++){
    var a=P[i], b=P[(i+1)%n];
    var ex=b[0]-a[0], ey=b[1]-a[1], L=Math.hypot(ex,ey);
    if(L<1e-9)continue;
    var nx=ey/L, ny=-ex/L;                       /* normale au cote */
    if((cx-a[0])*nx+(cy-a[1])*ny>0){nx=-nx;ny=-ny;}   /* orientee vers l'exterieur */
    var d=(x-a[0])*nx+(y-a[1])*ny;
    if(d>mx)mx=d;
  }
  return mx;                                     /* <=0 : dedans */
}

/* la demi-periode de la trame : de combien une marque peut deborder du
   polygone tout en appartenant a la cellule. Ce sont les pas du moteur. */
var PER={braille:9, mosaique:11, pixel:5, sillons:6, gravure:8};

window.DalleVraie=function(pid,opt){
  opt=opt||{};
  var hote=document.getElementById('toileCv'); if(!hote)return null;
  var v, D;
  try{ v=Toile.vue(); D=Toile.dalleAbs(pid); }catch(e){ return null; }
  if(!D||!D.w||!D.poly||D.poly.length<3) return null;
  var monde=opt.monde||Toile.getTheme();
  var dil=opt.dil!=null?opt.dil:((PER[monde]||10)*0.62+2);

  /* on preleve un carre plus large que la cellule : une marque deborde */
  var mar=dil+6;
  var X0=(D.minx-mar)*v.s+v.ox, Y0=(D.miny-mar)*v.s+v.oy;
  var LW=(D.w+2*mar)*v.s, LH=(D.h+2*mar)*v.s;
  var sx=Math.round(X0*v.dpr), sy=Math.round(Y0*v.dpr);
  var sw=Math.round(LW*v.dpr), sh=Math.round(LH*v.dpr);
  if(sw<4||sh<4) return null;

  var C=document.createElement('canvas'); C.width=sw; C.height=sh;
  var g=C.getContext('2d');
  g.drawImage(hote,sx,sy,sw,sh,0,0,sw,sh);
  var im=g.getImageData(0,0,sw,sh), S=im.data;

  /* ── LA COULEUR DE LA DALLE : le mode des pixels COLORES dans la cellule.
        (un centroide peut tomber dans un creux de trame et rendre le fond) ── */
  var hist={}, best=null, bn=0, xx, yy;
  for(yy=0;yy<sh;yy++){
    var ty=(sy+yy+0.5)/v.dpr;
    var ly=((ty-v.oy)/v.s);
    for(xx=0;xx<sw;xx++){
      var tx=(sx+xx+0.5)/v.dpr, lx=((tx-v.ox)/v.s);
      if(distPoly(D.poly,lx,ly)>0) continue;
      var o=(yy*sw+xx)*4, r=S[o], gg=S[o+1], b=S[o+2];
      var mxc=Math.max(r,gg,b), mnc=Math.min(r,gg,b);
      if(mxc<40) continue;                       /* le fond */
      if(mxc-mnc < 26) continue;                 /* une cellule grise */
      var k=(r>>2)+','+(gg>>2)+','+(b>>2);
      var c2=(hist[k]=(hist[k]||0)+1);
      if(c2>bn){bn=c2;best=[r,gg,b];}
    }
  }
  if(!best) return null;

  /* ── ON GARDE LES MARQUES DE CETTE COULEUR, ENTIERES ───────────────────── */
  var tol=opt.tol!=null?opt.tol:34, tol2=tol*2.2;
  var x1=sw,y1=sh,x2=-1,y2=-1;
  for(yy=0;yy<sh;yy++){
    var ty2=(sy+yy+0.5)/v.dpr, ly2=((ty2-v.oy)/v.s);
    for(xx=0;xx<sw;xx++){
      var o2=(yy*sw+xx)*4;
      var tx2=(sx+xx+0.5)/v.dpr, lx2=((tx2-v.ox)/v.s);
      if(distPoly(D.poly,lx2,ly2)>dil){ S[o2+3]=0; continue; }
      var dr=S[o2]-best[0], dg=S[o2+1]-best[1], db=S[o2+2]-best[2];
      var d=Math.sqrt(dr*dr+dg*dg+db*db);
      if(d<=tol){ S[o2+3]=255; }
      else if(d<=tol2){ S[o2+3]=Math.round(255*(1-(d-tol)/(tol2-tol))); }
      else { S[o2+3]=0; continue; }
      if(xx<x1)x1=xx; if(xx>x2)x2=xx; if(yy<y1)y1=yy; if(yy>y2)y2=yy;
    }
  }
  g.putImageData(im,0,0);
  if(x2<x1||y2<y1) return null;

  /* recadre au plus juste, sans redimensionner : 1:1, pixel pour pixel */
  var tw=x2-x1+1, th=y2-y1+1;
  var O=document.createElement('canvas'); O.width=tw; O.height=th;
  O.getContext('2d').drawImage(C,x1,y1,tw,th,0,0,tw,th);
  O.__col=best; O.__dpr=v.dpr;
  return O;
};

/* ════════════════════════════════════════════════════════════════════════════
   L'ENTREE UNIQUE — et elle reprend la distinction que LE MOTEUR fait deja.

   ⚑ POURQUOI DEUX CHEMINS, ET PAS UN SEUL.
   L'extraction par la couleur ne sait garder qu'UNE couleur. Or une marque de
   `touffe` en porte TROIS : le petale a la couleur de la dalle, le liseré est
   a l'encre, le coeur est orange. Prelevee par la couleur, la fleur perd son
   contour et son coeur — mesure : petales nus, ou coeurs orange sans petales.
   Il se trouve que ce sont exactement les mondes que le moteur appelle LIBRE
   (`dalleTrame` : encre, terrazzo, touffe) : ceux dont la marque DEBORDE de sa
   cellule et a donc sa forme propre. Pour eux `dalleTrame` est deja juste —
   c'est mesure, ils coincident avec la Toile.
   Les cinq autres sont des TRAMES : leur marque n'a pas de forme propre, elle
   n'existe que comme un morceau du motif continu. C'est la, et la seulement,
   que le decoupage polygonal coupait les marques en deux.
   ════════════════════════════════════════════════════════════════════════════ */
var LIBRE={encre:1,terrazzo:1,touffe:1};
window.DalleReelle=function(pid,monde,opt){
  monde=monde||Toile.getTheme();
  if(LIBRE[monde]){
    var cv=document.createElement('canvas');
    try{ Toile.dalleTrame(cv,pid,1,{m:monde,p:Toile.getPalette(),h:0}); }catch(e){ return null; }
    return cv.width?cv:null;
  }
  return window.DalleVraie(pid,{monde:monde});
};
window.DalleReelle.LIBRE=LIBRE;
window.DalleVraie.distPoly=distPoly;
window.DalleVraie.PER=PER;
})();
