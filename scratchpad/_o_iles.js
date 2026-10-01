/* ════════════════════════════════════════════════════════════════════════════
   LES ÎLES — le renversement du 9 septembre 2026.

   ⚑ CE QUI CHANGE, ET POURQUOI ÇA RÈGLE QUINZE SÉRIES.
   On enroulait la Toile sur la sphere. Or UN PAVAGE PARTITIONNE : sa beaute
   est une fonction de sa densite. A une dalle c'est une sphere unie, a trois
   un quartier d'orange ; il ne devient beau que vers vingt ou trente. Une
   Orbite neuve doit etre belle DES LE PREMIER JOUR — elle est partageable et
   vendable des le premier jour.
   La bonne geometrie est l'inverse : UNE FOURRURE DENSE PAR DEFAUT, ET DES
   ILES DEDANS. L'etat de repos n'est pas le vide, c'est le PEIGNE. Chaque
   Promi est une ile. La densite croit par ACCRETION, jamais par subdivision.

   ⚑ ET CA REGLE LA MOITIE DU PROBLEME DE LUMINANCE : on n'eclairait pas un
   objet trop sombre, ON ECLAIRAIT UNE SURFACE PLATE. Une fourrure a un relief
   qui accroche la lumiere rasante ; une masse unie n'a rien a eclairer.
   ════════════════════════════════════════════════════════════════════════════ */

/* ── LA PALETTE DE L'ORBITE — elle vient du Studio ─────────────────────────
   Le sol n'est pas un gris : c'est la FAMILLE de la palette, profonde et
   saturee. Les iles sont les couleurs de la palette, pleines. C'est ce qui
   lie l'Orbite au reste de l'app — et ca ne pose plus le probleme du
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

function palOrbite(pal,opt){
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
   ne se subdivise pas. Deterministe : meme Orbite, meme semis. */
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
    var pose=null;
    for(t=0;t<220 && !pose;t++){
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
      if(ok) pose=p;
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
  var cols=palOrbite(pal,opt);          /* [0] = le sol, uniforme */
  var IL=semisIles(n,opt);
  var PXR=opt.pxr||293, MAG=opt.mag||2.2;
  var dpr=Math.min(2,window.devicePixelRatio||1);
  var cnt={}, BRUT=[], k, q, j;

  for(k=0;k<IL.length;k++){
    var I=IL[k];
    I.monde=opt.monde||MONDES_O[(_o_h(k*13+5)*MONDES_O.length)|0];
    var g=I.r*2*PXR/MAG*0.72;
    var P=_o_cellule(g, k*7919+31);
    var cv=document.createElement('canvas'), ok=false;
    try{ ok=Toile.dalleGeneree(cv,{monde:I.monde, palette:opt.palette||Toile.getPalette(),
          poly:P, site:[0,0], sp:g*1.05, ci:(_o_h(k*29+3)*4)|0,
          lit:(k*3)%5, ang:_o_h(k*47+9)*Math.PI,
          tone:[1.0,0.76,1.24,0.88,1.12][k%5], pad:10}); }catch(e){}
    if(!ok||!cv.width){ BRUT.push(null); continue; }
    var d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    for(q=0;q<d.length;q+=4){
      if(d[q+3]<24) continue;
      var q5=((d[q]>>3)<<10)|((d[q+1]>>3)<<5)|(d[q+2]>>3);
      cnt[q5]=(cnt[q5]||0)+1;
    }
    BRUT.push({w:cv.width, h:cv.height, d:d,
               sx:cv.__site[0]*dpr, sy:cv.__site[1]*dpr,
               k:PXR/MAG*dpr});
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
  return {iles:IL, col:cols, dl:new Int8Array(cols.length),
          nsol:1, plein:1, cle:'iles'+n+'/'+(opt.palette||''), dalles:[]};
}

