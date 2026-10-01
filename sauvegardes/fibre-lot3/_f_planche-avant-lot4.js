/* ════════════════════════════════════════════════════════════════════════════
   LA PLANCHE — LA VRAIE DALLE, ET CE QUE LE VELOURS LUI FAIT
   Une ligne par monde.
     1 · LE MOTEUR            Toile.preview, l'echelle de l'app (67 px la dalle)
     2 · LA VRAIE DALLE       Toile.dalleTrame(cv,pid,1) — le moteur peint, on
                              ne redessine rien. Agrandie x4 AU PLUS PROCHE,
                              pour l'inspection seulement.
     3 · + LE VELOURS         la meme, traitee en surface. Meme x4.
     4 · A 1:1                trois dalles a leur taille reelle, celle qu'aura
                              une cellule de l'Orbite.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var MONDES=[
 ['encre',    'ENCRE'],    ['mosaique','MOSAIQUE'],
 ['touffe',   'TOUFFE'],   ['braille', 'BRAILLE'],
 ['pixel',    'PIXEL'],    ['terrazzo','TERRAZZO'],
 ['gravure',  'GRAVURE'],  ['sillons', 'SILLONS']
];
var PW=368, PH=214, ZOOM=4, BOITE=210, PIDS=[2,5,9,11], DPR=Math.min(2,window.devicePixelRatio||1);

function neuf(w,h){var c=document.createElement('canvas');
  c.width=Math.round(w*DPR); c.height=Math.round(h*DPR);
  c.style.width=w+'px'; c.style.height=h+'px';
  c.getContext('2d').setTransform(DPR,0,0,DPR,0,0); return c;}

/* la loupe : un agrandissement AU PLUS PROCHE, pour inspecter. Ce n'est pas un
   dessin — aucun pixel n'est invente, on les regarde de plus pres. */
function loupe(sc,boite,z){
  var c=document.createElement('canvas');
  c.width=boite*DPR; c.height=boite*DPR;
  c.style.width=boite+'px'; c.style.height=boite+'px';
  var g=c.getContext('2d'); g.imageSmoothingEnabled=false;
  var w=sc.width*z/DPR, h=sc.height*z/DPR;
  var e=Math.min(1,boite/Math.max(w,h)); w*=e; h*=e;
  g.drawImage(sc,(boite-w)/2*DPR,(boite-h)/2*DPR,w*DPR,h*DPR);
  return c;
}

window.batirPlanche=function(){
  var root=document.getElementById('pl');

  MONDES.forEach(function(M,idx){
    var monde=M[0], pid=PIDS[idx%PIDS.length], mo={m:monde,p:'signal',h:0};

    var row=document.createElement('div'); row.className='row';
    var band=document.createElement('div'); band.className='band';

    function colonne(el,lib){
      var w=document.createElement('div'); w.className='w';
      w.appendChild(el);
      var i=document.createElement('i'); i.textContent=lib; w.appendChild(i);
      band.appendChild(w); return w;
    }

    /* 1 · LE MOTEUR */
    var a=neuf(PW,PH); a.className='p';
    try{ Toile.preview(a,monde,PW,PH); }catch(e){}
    colonne(a,'le moteur');

    /* 2 · LA VRAIE DALLE, brute */
    var brut=document.createElement('canvas');
    try{ Toile.dalleTrame(brut,pid,1,mo); }catch(e){}
    var l2=loupe(brut,BOITE,ZOOM); l2.className='p';
    colonne(l2,'la vraie dalle — ×4');

    /* 3 · LA MEME, EN VELOURS */
    var vel=window.Velours(brut,1);
    var l3=loupe(vel,BOITE,ZOOM); l3.className='p';
    colonne(l3,'+ le velours — ×4');

    /* 4 · A 1:1, la taille d'une cellule d'Orbite */
    var trio=document.createElement('div'); trio.className='trio';
    for(var t=0;t<3;t++){
      var b2=document.createElement('canvas');
      try{ Toile.dalleTrame(b2,PIDS[(idx+t+1)%PIDS.length],1,mo); }catch(e){}
      var v2=window.Velours(b2,1);
      v2.style.width=(v2.width/DPR)+'px'; v2.style.height=(v2.height/DPR)+'px';
      v2.className='p1';
      trio.appendChild(v2);
    }
    colonne(trio,'à 1:1 — la taille d’une cellule');

    row.appendChild(band);
    var cap=document.createElement('p');
    cap.innerHTML='<b>'+M[1]+'</b>';
    row.appendChild(cap);
    root.appendChild(row);
  });
  batirToile(root);
  window.__pret=true;
};

/* ════════════════════════════════════════════════════════════════════════════
   UN MORCEAU DE TOILE — c'est la que la lumiere se juge
   Une dalle isolee ne peut pas montrer une « belle lumiere generale » : posee
   par dalle, la lumiere se repete a l'identique sur chacune et rien ne se
   tient. On compose donc un vrai morceau : les vraies dalles du moteur, a leur
   place, LE VIDE ENTRE ELLES (l'exigence 4), et UNE SEULE lumiere par-dessus.
   C'est exactement le montage qu'aura l'Orbite.
   ⚠ Ce qui est approche ici, et rien d'autre : la POSITION. `dalleTrame`
   recadre au plus juste et n'expose pas son decalage ; on centre donc chaque
   dalle sur le centre de sa cellule (`dalleAbs`). La dalle elle-meme, sa
   forme, sa trame et ses couleurs sont celles du moteur, au pixel.
   ════════════════════════════════════════════════════════════════════════════ */
function batirToile(root){
  var MOND=['encre','touffe','braille','gravure'];
  var t=document.createElement('div'); t.className='tete2';
  t.innerHTML='<h2>Un morceau de Toile — les vraies dalles, le vide entre elles, une seule lumière</h2>';
  root.appendChild(t);

  MOND.forEach(function(monde){
    var mo={m:monde,p:'signal',h:0}, D=[], pid;
    for(pid=1;pid<=14;pid++){
      var ab=null; try{ ab=Toile.dalleAbs(pid); }catch(e){}
      if(!ab||!ab.w)continue;
      var cvd=document.createElement('canvas');
      try{ Toile.dalleTrame(cvd,pid,1,mo); }catch(e){ continue; }
      if(!cvd.width)continue;
      D.push({cx:ab.minx+ab.w/2, cy:ab.miny+ab.h/2, cv:window.Velours(cvd,1)});
    }
    if(!D.length)return;
    var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
    D.forEach(function(d){
      var w=d.cv.width/DPR/2, h=d.cv.height/DPR/2;
      if(d.cx-w<x0)x0=d.cx-w; if(d.cx+w>x1)x1=d.cx+w;
      if(d.cy-h<y0)y0=d.cy-h; if(d.cy+h>y1)y1=d.cy+h;});
    var PWt=Math.ceil(x1-x0)+8, PHt=Math.ceil(y1-y0)+8;

    function monte(z){
      var c=document.createElement('canvas');
      c.width=Math.round(PWt*z*DPR); c.height=Math.round(PHt*z*DPR);
      c.style.width=(PWt*z)+'px'; c.style.height=(PHt*z)+'px';
      var g=c.getContext('2d');
      g.imageSmoothingEnabled=false;   /* jamais de raster agrandi et LISSE : au plus proche, et c'est une loupe, pas un dessin */
      D.forEach(function(d){
        var w=d.cv.width/DPR, h=d.cv.height/DPR;
        g.drawImage(d.cv, Math.round((d.cx-x0-w/2+4)*z*DPR), Math.round((d.cy-y0-h/2+4)*z*DPR),
                    Math.round(w*z*DPR), Math.round(h*z*DPR));});
      window.Velours.jour(c);
      c.className='p'; return c;
    }
    var row=document.createElement('div'); row.className='row';
    var band=document.createElement('div'); band.className='band';
    [[1,'à 1:1'],[2,'loupe ×2 — au plus proche']].forEach(function(z){
      var w=document.createElement('div'); w.className='w';
      w.appendChild(monte(z[0]));
      var i=document.createElement('i'); i.textContent=z[1]; w.appendChild(i);
      band.appendChild(w);});
    row.appendChild(band);
    var cap=document.createElement('p'); cap.innerHTML='<b>'+monde.toUpperCase()+'</b>';
    row.appendChild(cap);
    root.appendChild(row);
  });
}
})();
