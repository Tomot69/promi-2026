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
  window.__pret=true;
};
})();
