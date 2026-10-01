/* ════════════════════════════════════════════════════════════════════════════
   LE PEINTRE — un decoupage par cellule, et le moteur peint dedans.
   Cout par image : ~40 chemins et ~40 drawImage. Rien a voir avec les 150 000
   tampons d'avant ; le budget n'est plus le sujet.
   ════════════════════════════════════════════════════════════════════════════ */
var D=2;

function projette(P, cl,sl,ct,st, R,FOC, CX,CY){
  var out=new Array(P.length), dev=0, n=0;
  for(var k=0;k<P.length;k++){
    var x=P[k][0], y=P[k][1], z=P[k][2];
    var X2=x*cl+z*sl, Zt=-x*sl+z*cl, Y2=y*ct-Zt*st, Z2=y*st+Zt*ct;
    var q=FOC/(FOC-Z2*R);
    out[k]=[CX+X2*R*q, CY+Y2*R*q, Z2];
    dev+=Z2; n++;
  }
  out.moy=dev/n;
  return out;
}
/* le chemin, coins ARRONDIS — comme le moteur arrondit ses dalles */
function chemin(g, pts, r){
  var n=pts.length;
  g.beginPath();
  for(var i=0;i<n;i++){
    var a=pts[(i-1+n)%n], b=pts[i], c=pts[(i+1)%n];
    var v1=[a[0]-b[0], a[1]-b[1]], v2=[c[0]-b[0], c[1]-b[1]];
    var l1=Math.hypot(v1[0],v1[1])||1, l2=Math.hypot(v2[0],v2[1])||1;
    var rr=Math.min(r, l1*0.45, l2*0.45);
    var p1=[b[0]+v1[0]/l1*rr, b[1]+v1[1]/l1*rr];
    var p2=[b[0]+v2[0]/l2*rr, b[1]+v2[1]/l2*rr];
    if(i===0) g.moveTo(p1[0],p1[1]); else g.lineTo(p1[0],p1[1]);
    g.quadraticCurveTo(b[0],b[1], p2[0],p2[1]);
  }
  g.closePath();
}

var _ATNF=new Float32Array(257);
(function(){for(var i=0;i<=256;i++)_ATNF[i]=Math.atan(i/256);})();
function secteurF(x,y,n){
  var ax=x<0?-x:x, ay=y<0?-y:y, a;
  if(ax>=ay) a=_ATNF[(ay/(ax||1e-9)*256)|0];
  else       a=1.5707963268-_ATNF[(ax/(ay||1e-9)*256)|0];
  if(x<0) a=3.1415926536-a;
  if(y<0) a=6.283185307179586-a;
  var s=(a/6.283185307179586*n)|0; return s>=n?n-1:(s<0?0:s);
}
function peint(cv, o){
  var CSS=o.css||470, W=CSS*D;
  cv.width=W; cv.height=W;
  var g=cv.getContext('2d');
  g.fillStyle=o.fond||'#131319'; g.fillRect(0,0,W,W);
  /* ⚑ LA DALLE NE SE VOIT PAS — ELLE DONNE SA COULEUR AUX POILS.
     On la peint sur un calque SOURCE, jamais a l'ecran. Ce qu'on voit est
     100 % de la fourrure : elle prend la teinte du pixel qu'elle recouvre, donc
     la vraie forme de la cellule, la vraie couleur de la dalle, et le clair-
     obscur de sa trame — sans qu'un seul aplat plat n'apparaisse. C'est ce qui
     fait le FLUFFY : il n'y a plus de surface lisse nulle part. */
  if(!cv.__src || cv.__src.width!==W){
    cv.__src=document.createElement('canvas'); cv.__src.width=W; cv.__src.height=W;
    cv.__sg=cv.__src.getContext('2d',{willReadFrequently:true});
  }
  var gs=cv.__sg;
  gs.setTransform(1,0,0,1,0,0);
  gs.fillStyle='#000'; gs.fillRect(0,0,W,W);
  var gPeint=g; g=gs;
  var R=CSS*(o.R||0.425)*D, FOC=R*5.4, CX=W/2, CY=W/2;
  var cl=Math.cos(o.lac), sl=Math.sin(o.lac), ct=Math.cos(o.tan), st=Math.sin(o.tan);
  var S=o.sites, CEL=o.cells, DAL=o.dalles, PL=o.plant;
  var t0=performance.now(), n=0;

  /* on peint du fond vers l'avant : le recouvrement fait le volume */
  var ordre=[];
  for(var i=0;i<S.length;i++){
    var s=S[i];
    var Zs=s[1]*st+(-s[0]*sl+s[2]*cl)*ct;
    ordre.push([i,Zs]);
  }
  ordre.sort(function(a,b){return a[1]-b[1];});

  for(var q=0;q<ordre.length;q++){
    var id=ordre[q][0], Zs=ordre[q][1];
    if(Zs<-0.30) continue;                 /* franchement au dos : rien a voir */
    var P=CEL[id]; if(!P || P.length<3) continue;
    var pts=projette(P, cl,sl,ct,st, R,FOC, CX,CY);
    /* la dalle du moteur, a l'echelle 1, calee sur la boite de la cellule */
    var d=DAL[(hh(id*31+11)*DAL.length)|0];
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var k=0;k<pts.length;k++){
      if(pts[k][0]<minx)minx=pts[k][0]; if(pts[k][0]>maxx)maxx=pts[k][0];
      if(pts[k][1]<miny)miny=pts[k][1]; if(pts[k][1]>maxy)maxy=pts[k][1];
    }
    var bw=maxx-minx, bh=maxy-miny;
    if(bw<3||bh<3) continue;
    g.save();
    chemin(g, pts, (o.rond||6)*D);
    g.clip();
    /* ⚑ LE MOTEUR PEINT, A L'ECHELLE 1 : le pas du motif est le vrai, la
       couleur est la vraie, les strates sont les vraies. On centre la dalle sur
       la cellule et on laisse le decoupage faire le contour. */
    /* ⚑ AUCUNE REPETITION. La Toile est agrandie avant qu'on releve ses dalles :
       elles font 200 a 380 px quand une cellule en fait 70 a 110. La dalle
       couvre donc toujours sa cellule, et on la pose A L'ECHELLE 1 — le pas du
       motif est exactement celui du moteur.
       ⚠ Ma premiere version repetait la dalle AU MIROIR quand elle etait trop
       petite : ca fabriquait des papillons et des kaleidoscopes, tres visibles
       sur encre. Le probleme n'etait pas le repli, c'etait la taille. */
    var sw=Math.min(d.width, bw), sh=Math.min(d.height, bh);
    var sx=(d.width-sw)*0.5+(hh(id*5+1)-0.5)*(d.width-sw)*0.7;
    var sy=(d.height-sh)*0.5+(hh(id*7+3)-0.5)*(d.height-sh)*0.7;
    if(!PL[id]) g.globalAlpha=0.16;        /* la cellule vide : sa trame, en sourdine */
    g.drawImage(d, sx,sy,sw,sh, minx+(bw-sw)*0.5, miny+(bh-sh)*0.5, sw, sh);
    g.globalAlpha=1;
    g.restore();
    n++;
  }
  g=gPeint;

  /* ── LE COTON, PAR-DESSUS ─────────────────────────────────────────────
     ⚑ LA FIBRE PREND LA COULEUR DE CE QU'IL Y A DESSOUS.
     C'est ce qui debloque tout : le moteur a deja peint la dalle, donc la
     fibre n'a plus a dire ou est le motif — elle le duvete. On relit l'image
     une fois, et chaque touffe se colore du pixel de sa racine, eclairci vers
     sa pointe. Le motif reste intact dessous, et la surface devient molle.
     ⚠ Et les fibres DEBORDENT de la silhouette : c'est ce debord qui fait le
     coton. Le contour reste un cercle — c'est un cercle duveteux. */
  if(o.fibres){
    var FB=o.fibres, AF=lieFib(o.atlasFib, W), OFF=AF.__off, ALF=AF.__al, STF=AF.__st;
    /* ⚑ LA FOURRURE SUR SA PROPRE COUCHE.
       Fondre chaque pixel dans l'image — lire, interpoler trois canaux, ecrire
       — coutait 30 a 50 ms. Sur une couche TRANSPARENTE, une simple comparaison
       d'alpha suffit (c'est la technique acquise), et le fondu se fait UNE
       SEULE FOIS, par le drawImage final. */
    var im=gs.getImageData(0,0,W,W), B=new Uint32Array(im.data.buffer);
    if(!cv.__fur || cv.__fur.width!==W){
      cv.__fur=document.createElement('canvas'); cv.__fur.width=W; cv.__fur.height=W;
      cv.__fg=cv.__fur.getContext('2d');
      cv.__fim=cv.__fg.createImageData(W,W);
      cv.__fb=new Uint32Array(cv.__fim.data.buffer);
    }
    var L=cv.__fb; L.fill(0);
    var ORI=o.oriFib||24, NT=o.taiFib||3;
    var FOND=(o.fondPack!==undefined)?o.fondPack:0x191913;
    var nf=0;
    for(var f=0;f<FB.n;f++){
      var fx=FB.P[f*3], fy=FB.P[f*3+1], fz=FB.P[f*3+2];
      var Zt2=-fx*sl+fz*cl, Z3=fy*st+Zt2*ct;
      if(Z3<0.02) continue;
      var X3=fx*cl+fz*sl, Y3=fy*ct-Zt2*st;
      var k3=FOC/(FOC-Z3*R);
      var px=(CX+X3*R*k3)|0, py=(CY+Y3*R*k3)|0;
      if(px<26||py<26||px>W-26||py>W-26) continue;
      var src=B[py*W+px];
      var sr=src&255, sg=(src>>8)&255, sb=(src>>16)&255;
      /* ⚑ LE DEBORD FAIT LE COTON, MAIS IL VIENT DE LA DALLE.
         Une touffe ne pousse que si SA RACINE est dans la matiere ; c'est en
         s'etendant qu'elle passe par-dessus le joint et par-dessus la
         silhouette. Ma premiere version allait rechercher une couleur VERS
         L'INTERIEUR quand la racine tombait dans le vide : ca semait de la
         fourrure DANS les joints, et tout devenait boueux. */
      if(sr+sg+sb < 122) continue;
      /* la pointe s'eclaircit — c'est le duvet qui prend la lumiere */
      /* ⚠ COTON, PAS POIL. Des fibres sombres et longues font un pelage de
         bete ; ce qu'on veut, c'est un duvet — court, fin, et qui PREND LA
         LUMIERE a sa pointe. On eclaircit franchement. */
      /* ⚠ ET IL FAUT QUE CA RESTE COLORE. A 0,30 + 0,42 la pointe montait a
         72 % vers le blanc : toute la palette du Studio se lavait en beige.
         Le duvet eclaircit A PEINE — c'est le LISERE du limbe qui donne la
         lumiere, pas le blanchiment de chaque fibre. */
      var ecl=0.05+0.19*Z3;
      var cr=(sr+(255-sr)*ecl)|0, cg=(sg+(255-sg)*ecl)|0, cb=(sb+(255-sb)*ecl)|0;

      /* l'orientation : le peignage, projete */
      var vx=FB.F[f*3], vy=FB.F[f*3+1], vz=FB.F[f*3+2];
      var wX=vx*cl+vz*sl, wZt=-vx*sl+vz*cl, wY=vy*ct-wZt*st;
      var ori=secteurF(wX,wY,ORI);
      var tai=(Z3*NT)|0; if(tai>=NT)tai=NT-1;
      var idx=tai*ORI+ori, a0=STF[idx], a1=STF[idx+1], bas=py*W+px;
      var col=((cb<<16)|(cg<<8)|cr)>>>0;
      /* ⚠ sur la couche transparente, une comparaison d'alpha suffit. Sur
         l'image opaque, ce meme test echouait TOUJOURS (l'alpha du fond vaut
         255) et la passe n'ecrivait rien — elle a tourne vingt millisecondes
         pour rien avant que je le voie. */
      for(var j=a0;j<a1;j++){
        var oo=bas+OFF[j], al=ALF[j];
        if(al>(L[oo]>>>24)) L[oo]=((al<<24)|col)>>>0;
      }
      nf++;
    }
    cv.__fg.putImageData(cv.__fim,0,0);
    g.drawImage(cv.__fur,0,0);
    window.__fib=nf;
  }
  g=gPeint;                                /* fini pour le calque source */
  /* ⚑ UN VELOURS, PAS UN PLASTIQUE.
     Ma premiere version posait un degrade radial avec une TACHE SPECULAIRE
     blanche : c'est la signature d'une bille de verre, et ca sortait « mega
     cheap ». Le velours et le coton font l'inverse — leur loi de reflexion est
     RETRO-REFLECTIVE : ils sont plus clairs AU BORD, la ou les fibres se voient
     de profil, et la lumiere y tombe en douceur, sans point chaud. On garde
     donc un ambiant large, une cle tres molle, et un LISERE DE DUVET au limbe. */
  var rr=R*1.005;
  g.save();
  g.beginPath(); g.arc(CX,CY,rr,0,TAU); g.clip();
  /* la cle : molle, sans point chaud */
  var gl=g.createRadialGradient(CX-rr*0.34, CY-rr*0.38, rr*0.10, CX, CY, rr*1.45);
  gl.addColorStop(0,   'rgba(255,250,242,0.10)');
  gl.addColorStop(0.55,'rgba(255,250,242,0.00)');
  gl.addColorStop(1,   'rgba(10,11,16,0.42)');
  g.fillStyle=gl; g.fillRect(CX-rr,CY-rr,rr*2,rr*2);
  /* LE DUVET DU LIMBE : c'est lui qui dit « fibre », pas un reflet */
  var g3=g.createRadialGradient(CX,CY,rr*0.70, CX,CY,rr*1.02);
  g3.addColorStop(0,   'rgba(255,255,255,0)');
  g3.addColorStop(0.82,'rgba(246,244,255,0.10)');
  g3.addColorStop(1,   'rgba(252,250,255,0.26)');
  g.fillStyle=g3; g.fillRect(CX-rr,CY-rr,rr*2,rr*2);
  g.restore();

  return {n:n, ms:+(performance.now()-t0).toFixed(1)};
}
