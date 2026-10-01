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
  var LST=[];
  try{ LST=window.DallesDeMonde(Toile.getTheme(),{cellule:200,n:pids.length}); }catch(e){}
  var BRUT=[];
  for(var q=0;q<LST.length;q++){
    var c=LST[q], g=c.getContext('2d');
    BRUT.push({w:c.width, h:c.height, d:g.getImageData(0,0,c.width,c.height).data});
  }
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
              cx:(bx+bX)*0.5, cy:(by+bY)*0.5});
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
