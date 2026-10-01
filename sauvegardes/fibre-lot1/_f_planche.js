/* ════════════════════════════════════════════════════════════════════════════
   LA PLANCHE — LA FIBRE EST-ELLE LE TRAIT DU MONDE ?
   Une ligne par monde. A gauche LE MOTEUR (Toile.preview, echelle reelle :
   pw/5.5 = 67 px par dalle, celle de l'app). Au milieu LA FIBRE A LA LOUPE
   (x3). A droite LA FIBRE A L'ECHELLE REELLE, 67 px — celle qu'aura une
   cellule de l'Orbite.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var MONDES=[
 ['encre',    'ENCRE',     'peluche froissee — la silhouette lobee et les strates viennent des neuf ellipses du moteur, le sens vient du champ'],
 ['mosaique', 'MOSAIQUE',  'tapisserie — un carreau de poils peignes, la gouttiere reste nue, le sens alterne en damier'],
 ['touffe',   'TOUFFE',    'le monde ou la fibre et le motif etaient deja la meme chose : chaque petale est un faisceau, le coeur reste orange'],
 ['braille',  'BRAILLE',   'tapis a points — une rosette par noeud de la grille de 9, rien entre'],
 ['pixel',    'PIXEL',     'peluche rase — dense et peignee d’un seul mouvement, le contour quantifie a 5 px'],
 ['terrazzo', 'TERRAZZO',  'velours froisse — chaque tesson est une plaque de poil a son propre peignage'],
 ['gravure',  'GRAVURE',   'velours cotele — une rangee de poils couches, un sens sur deux inverse'],
 ['sillons',  'SILLONS',   'soie moiree — les poils couches le long de l’onde, rangee par rangee']
];
var PW=368, PH=224, LOUPE=200, VRAI=67, DPR=2;

function polyCellule(){
  /* un vrai pavage : des sites sur une grille jitteree, on prend celui du
     centre. inset = le JOINT, le vide entre deux dalles. */
  var S=[],G=67,rnd=window.Fibre.graine(31);
  for(var j=-2;j<=2;j++)for(var i=-2;i<=2;i++)
    S.push([i*G+(rnd()-.5)*G*0.42, j*G+(rnd()-.5)*G*0.42]);
  var c=12;                                   /* l'indice du site central */
  var best=1e9,bi=0;
  for(var q=0;q<S.length;q++){var d=Math.hypot(S[q][0],S[q][1]);if(d<best){best=d;bi=q;}}
  return window.Fibre.cellulePlane(S,bi,-2.0);
}
function recadre(P,taille){
  var b=window.Fibre.boite(P),w=b[2]-b[0],h=b[3]-b[1];
  var s=taille/Math.max(w,h),Q=[];
  for(var i=0;i<P.length;i++)
    Q.push([(P[i][0]-b[0])*s+(taille-w*s)/2, (P[i][1]-b[1])*s+(taille-h*s)/2]);
  return Q;
}

function cv(w,h){
  var c=document.createElement('canvas');
  c.width=w*DPR; c.height=h*DPR;
  c.style.width=w+'px'; c.style.height=h+'px';
  c.getContext('2d').setTransform(DPR,0,0,DPR,0,0);
  return c;
}

window.batirPlanche=function(){
  var root=document.getElementById('pl');
  var PAL=(window.Toile&&Toile.cols)?Toile.cols():[[208,176,255],[58,84,255],[240,122,46],[143,160,255]];
  var Pbase=polyCellule();
  var Ploupe=recadre(Pbase,LOUPE), Pvrai=recadre(Pbase,VRAI);
  var kL=LOUPE/VRAI, total=0;

  MONDES.forEach(function(M,idx){
    var monde=M[0];
    var col=PAL[idx%PAL.length];
    var ang=window.Fibre.hh(idx*17+3)*Math.PI;

    var row=document.createElement('div'); row.className='row';
    var band=document.createElement('div'); band.className='band';

    /* 1 · LE MOTEUR, a l'echelle de l'app */
    var a=cv(PW,PH); a.className='p';
    try{ Toile.preview(a,monde,PW,PH); }catch(e){}
    var w1=document.createElement('div'); w1.className='w';
    w1.appendChild(a);
    var l1=document.createElement('i'); l1.textContent='le moteur'; w1.appendChild(l1);

    /* 2 · LA FIBRE, A LA LOUPE */
    var b=cv(LOUPE,LOUPE); b.className='p';
    var gb=b.getContext('2d');
    total+=window.Fibre.peintCellule(gb,monde,Ploupe,kL,col,idx*101+7,ang);
    var w2=document.createElement('div'); w2.className='w';
    w2.appendChild(b);
    var l2=document.createElement('i'); l2.textContent='la fibre, ×3'; w2.appendChild(l2);

    /* 3 · LA FIBRE, A L'ECHELLE REELLE D'UNE CELLULE DE L'ORBITE */
    var holder=document.createElement('div'); holder.className='trio';
    for(var t=0;t<3;t++){
      var c=cv(VRAI,VRAI); c.className='p';
      window.Fibre.peintCellule(c.getContext('2d'),monde,Pvrai,1,PAL[(idx+t)%PAL.length],idx*101+7+t*13,ang);
      holder.appendChild(c);
    }
    var w3=document.createElement('div'); w3.className='w';
    w3.appendChild(holder);
    var l3=document.createElement('i'); l3.textContent='à l’échelle réelle — 67 px'; w3.appendChild(l3);

    band.appendChild(w1); band.appendChild(w2); band.appendChild(w3);
    row.appendChild(band);
    var cap=document.createElement('p');
    cap.innerHTML='<b>'+M[1]+'</b> — '+M[2];
    row.appendChild(cap);
    root.appendChild(row);
  });
  window.__touffes=total;
  window.__pret=true;
};
})();
