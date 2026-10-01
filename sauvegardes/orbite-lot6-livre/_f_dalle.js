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

  /* ── ON GARDE LES MARQUES DE CETTE COULEUR, ENTIERES ─────────────────────
     ⚑ LE BORD SE LIT PAR PROJECTION, PAS PAR UNE BANDE DE TOLERANCE.
     Une bande gardait, a alpha partiel, les pixels d'antialiasing du VOISIN :
     d'ou le liseré mauve sale le long de l'escalier de pixel — reproche de Tom,
     « tu prends pas des vrais contours de dalles, pourtant ils sont bien
     contrastes ». Il a raison : justement parce qu'ils sont contrastes, la
     bonne lecture est exacte. Un pixel de bord est un MELANGE entre la couleur
     de la dalle et le fond. On projette sur le segment [fond -> dalle] : la
     part donne l'alpha, et le RESTE dit avec quoi le melange se faisait. Un
     pixel melange a une AUTRE dalle a un reste eleve : rejete, net. */
  var fond=[255,255,255], fl=1e9, _i;
  for(_i=0;_i<S.length;_i+=4*23){
    var _L=0.299*S[_i]+0.587*S[_i+1]+0.114*S[_i+2];
    if(_L<fl){fl=_L;fond=[S[_i],S[_i+1],S[_i+2]];}
  }
  var vr=best[0]-fond[0], vg=best[1]-fond[1], vb=best[2]-fond[2];
  var vv=vr*vr+vg*vg+vb*vb; if(vv<200) return null;
  var res=opt.res!=null?opt.res:22;
  var x1=sw,y1=sh,x2=-1,y2=-1;
  for(yy=0;yy<sh;yy++){
    var ty2=(sy+yy+0.5)/v.dpr, ly2=((ty2-v.oy)/v.s);
    for(xx=0;xx<sw;xx++){
      var o2=(yy*sw+xx)*4;
      var tx2=(sx+xx+0.5)/v.dpr, lx2=((tx2-v.ox)/v.s);
      if(distPoly(D.poly,lx2,ly2)>dil){ S[o2+3]=0; continue; }
      var pr2=S[o2]-fond[0], pg2=S[o2+1]-fond[1], pb2=S[o2+2]-fond[2];
      var a=(pr2*vr+pg2*vg+pb2*vb)/vv;
      if(a<=0.06){ S[o2+3]=0; continue; }
      if(a>1)a=1;
      var er=pr2-a*vr, eg=pg2-a*vg, eb=pb2-a*vb;
      if(Math.sqrt(er*er+eg*eg+eb*eb)>res){ S[o2+3]=0; continue; }
      S[o2]=best[0]; S[o2+1]=best[1]; S[o2+2]=best[2];
      S[o2+3]=Math.round(a*255);
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

/* ════════════════════════════════════════════════════════════════════════════
   LES DALLES D'UN MONDE, EN UN SEUL APPEL ET SANS ATTENDRE

   ⚑ POURQUOI PAS `dalleTrame`, ET POURQUOI PAS LA TOILE VIVANTE.
   `dalleTrame` coupe les marques en deux (mesure : scratchpad/verite.html) —
   demi-points, demi-carreaux, et l'escalier de pixel qui disparait.
   Prelever sur la Toile vivante corrige ca, mais il faut ATTENDRE qu'elle soit
   repeinte : le canevas ne se peint qu'a la frame suivante, et `bat_trames`
   est synchrone. Lire tout de suite, c'est lire l'ANCIEN monde — le piege du
   §8 (« un canevas est vide : peintMinis appele avant que le canevas soit
   dispose »), en pire, parce qu'il ne rend pas une erreur mais un mauvais
   dessin.
   `Toile.preview(cv, monde, w, h)` peint SYNCHRONIQUEMENT : elle appelle
   `RD[theme]` en ligne. Elle publie meme ses graines dans `cv.__c`. C'est le
   moteur, au pas absolu, sans attente et sans toucher a l'etat de l'app.

   ⚑ LE BORD SE LIT PAR PROJECTION, PAS PAR UNE BANDE DE TOLERANCE.
   Une bande gardait, a alpha partiel, les pixels d'antialiasing du VOISIN :
   d'ou le liseré mauve sale le long de l'escalier. Un pixel de bord est un
   MELANGE entre la couleur de la dalle et le fond. On projette donc sur le
   segment [fond -> dalle] : la part donne l'alpha, et le RESTE dit si le
   melange se faisait bien avec le fond. Un pixel melange a une autre dalle a
   un reste eleve : il est rejete, net.
   ════════════════════════════════════════════════════════════════════════════ */
window.DallesDeMonde=function(monde,opt){
  opt=opt||{};
  var CIB=opt.cellule||200;                 /* la taille visee d'une dalle */
  var PW=Math.round(CIB*5.5), PH=Math.round(PW*1.42);
  var cv=document.createElement('canvas'); cv.width=PW; cv.height=PH;
  var av=window._shAllColored;
  window._shAllColored=true;                /* toutes les cellules portent une couleur */
  try{ Toile.preview(cv,monde,PW,PH); }catch(e){ window._shAllColored=av; return []; }
  window._shAllColored=av;
  var meta=cv.__c; if(!meta||!meta.seeds) return [];

  var g=cv.getContext('2d'), im=g.getImageData(0,0,PW,PH), S=im.data;

  /* le fond : la teinte la plus sombre du canevas — c'est le remplissage que
     `preview` pose avant d'appeler le peintre du monde. */
  var fond=[255,255,255], fl=1e9, i;
  for(i=0;i<S.length;i+=4*37){
    var L=0.299*S[i]+0.587*S[i+1]+0.114*S[i+2];
    if(L<fl){fl=L;fond=[S[i],S[i+1],S[i+2]];}
  }

  /* ⚑ LES MONDES LIBRES GARDENT TOUT CE QUI N'EST PAS LE FOND.
     Une marque de `touffe` porte TROIS couleurs : le petale a la couleur de la
     dalle, le liseré est a l'encre, le coeur est orange. Une extraction par LA
     couleur lui retire donc son contour et son coeur — mesure a l'ecran : la
     sphere en touffe passait d'une boule fournie a des lambeaux. Idem pour les
     eclats d'un terrazzo et les lobes superposes d'une encre.
     Ce sont exactement les mondes que le moteur appelle LIBRE : leur marque a
     une FORME PROPRE et deborde de sa cellule. Pour eux on ne trie pas par
     teinte, on garde tout ce qui n'est pas le fond, et c'est LA GRAINE LA PLUS
     PROCHE qui dit a qui la marque appartient — la regle du moteur. */
  var EST_LIBRE=!!(window.DalleReelle&&window.DalleReelle.LIBRE[monde]);
  var sd=meta.seeds, esp=Math.sqrt(PW*PH/Math.max(1,sd.length)), OUT=[];
  var lim=Math.round(esp*1.35), res=opt.res!=null?opt.res:22;
  var nMax=opt.n||20;

  for(var k=0;k<sd.length && OUT.length<nMax;k++){
    var s=sd[k]; if(s.ci==null) continue;
    var sx=Math.round(s.x), sy=Math.round(s.y);
    var X0=Math.max(0,sx-lim), Y0=Math.max(0,sy-lim);
    var X1=Math.min(PW-1,sx+lim), Y1=Math.min(PH-1,sy+lim);
    if(X1-X0<8||Y1-Y0<8) continue;

    /* LA COULEUR DE CETTE DALLE : le mode des teintes colorees pres de sa graine */
    var hist={}, best=null, bn=0, x, y, o;
    var pr=Math.round(esp*0.34);
    for(y=Math.max(0,sy-pr);y<=Math.min(PH-1,sy+pr);y++)
      for(x=Math.max(0,sx-pr);x<=Math.min(PW-1,sx+pr);x++){
        o=(y*PW+x)*4;
        var mx=Math.max(S[o],S[o+1],S[o+2]), mn=Math.min(S[o],S[o+1],S[o+2]);
        if(mx<40||mx-mn<24) continue;
        var q=(S[o]>>3)+','+(S[o+1]>>3)+','+(S[o+2]>>3);
        var c2=(hist[q]=(hist[q]||0)+1);
        if(c2>bn){bn=c2;best=[S[o],S[o+1],S[o+2]];}
      }
    if(!best) continue;

    var vr=best[0]-fond[0], vg=best[1]-fond[1], vb=best[2]-fond[2];
    var vv=vr*vr+vg*vg+vb*vb; if(vv<200) continue;

    var W2=X1-X0+1, H2=Y1-Y0+1;
    var dc=document.createElement('canvas'); dc.width=W2; dc.height=H2;
    var dg=dc.getContext('2d');
    var dim=dg.createImageData(W2,H2), D=dim.data;
    var x1=W2,y1=H2,x2=-1,y2=-1;
    var vn=Math.sqrt(vv);
    for(y=0;y<H2;y++)for(x=0;x<W2;x++){
      var ax=x+X0, ay=y+Y0;
      o=(ay*PW+ax)*4;
      var pr2=S[o]-fond[0], pg2=S[o+1]-fond[1], pb2=S[o+2]-fond[2];
      var a, gr, gv, gb;
      if(EST_LIBRE){
        /* tout ce qui n'est pas le fond, et qui appartient a CETTE graine */
        var ec=Math.sqrt(pr2*pr2+pg2*pg2+pb2*pb2);
        if(ec<14) continue;
        var bq=-1, bdd=1e18;
        for(var z=0;z<sd.length;z++){
          var ddx=ax-sd[z].x, ddy=ay-sd[z].y, dq=ddx*ddx+ddy*ddy;
          if(dq<bdd){bdd=dq;bq=z;} }
        if(bq!==k) continue;
        a=Math.min(1,ec/vn*1.15);
        gr=S[o]; gv=S[o+1]; gb=S[o+2];
      } else {
        a=(pr2*vr+pg2*vg+pb2*vb)/vv;              /* la part de dalle */
        if(a<=0.06) continue;
        if(a>1)a=1;
        var er=pr2-a*vr, eg=pg2-a*vg, eb=pb2-a*vb; /* le reste : melange avec QUOI ? */
        if(Math.sqrt(er*er+eg*eg+eb*eb)>res) continue;
        gr=best[0]; gv=best[1]; gb=best[2];
      }
      var d4=(y*W2+x)*4;
      D[d4]=gr; D[d4+1]=gv; D[d4+2]=gb; D[d4+3]=Math.round(a*255);
      if(x<x1)x1=x; if(x>x2)x2=x; if(y<y1)y1=y; if(y>y2)y2=y;
    }
    if(x2<x1||y2<y1) continue;
    dg.putImageData(dim,0,0);
    var tw=x2-x1+1, th=y2-y1+1;
    if(tw<10||th<10) continue;
    var O=document.createElement('canvas'); O.width=tw; O.height=th;
    O.getContext('2d').drawImage(dc,x1,y1,tw,th,0,0,tw,th);
    OUT.push(O);
  }
  return OUT;
};
