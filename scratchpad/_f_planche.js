/* ════════════════════════════════════════════════════════════════════════════
   LA PLANCHE — LES VRAIES DALLES, ET RIEN D'AUTRE

   Le velours est retire : Tom a tranche, « le velours ca marche pas ». Ce qui
   reste est ce qui a ete PROUVE — la dalle telle que le moteur la peint sur la
   Toile, marque par marque, au pixel. La confrontation monde par monde est
   dans scratchpad/verite.html.
   Le seul ajout est la LUMIERE GENERALE, montree a part, sur sa propre
   colonne, pour qu'on puisse la refuser d'un coup d'oeil.
   ════════════════════════════════════════════════════════════════════════════ */
(function(){
var MONDES=['encre','mosaique','touffe','braille','pixel','terrazzo','gravure','sillons'];
var PW=368, PH=214, ZOOM=4, BOITE=196, PIDS=[2,5,9,11];
var DPR=Math.min(2,window.devicePixelRatio||1);

function neuf(w,h){var c=document.createElement('canvas');
  c.width=Math.round(w*DPR); c.height=Math.round(h*DPR);
  c.style.width=w+'px'; c.style.height=h+'px';
  c.getContext('2d').setTransform(DPR,0,0,DPR,0,0); return c;}

/* une loupe est TOUJOURS au plus proche : on regarde de plus pres, on
   n'invente aucun pixel et on ne lisse rien. */
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
function attends(ms){return new Promise(function(r){setTimeout(r,ms);});}
function col(band,el,lib){
  var w=document.createElement('div'); w.className='w';
  w.appendChild(el);
  var i=document.createElement('i'); i.textContent=lib; w.appendChild(i);
  band.appendChild(w); return w;
}

window.batirPlanche=async function(){
  var root=document.getElementById('pl'), mi, t;

  /* ── 1 · LES HUIT MONDES, DALLE PAR DALLE ──────────────────────────────── */
  for(mi=0;mi<MONDES.length;mi++){
    var monde=MONDES[mi];
    Toile.setTheme(monde);
    await attends(1500);                 /* le moteur repeint TOUTE la Toile */

    var row=document.createElement('div'); row.className='row';
    var band=document.createElement('div'); band.className='band';

    var a=neuf(PW,PH); a.className='p';
    try{ Toile.preview(a,monde,PW,PH); }catch(e){}
    col(band,a,'le moteur');

    var d1=window.DalleReelle(PIDS[mi%PIDS.length],monde);
    if(d1){ var l=loupe(d1,BOITE,ZOOM); l.className='p'; col(band,l,'la vraie dalle — loupe ×4'); }

    var trio=document.createElement('div'); trio.className='trio';
    for(t=0;t<3;t++){
      var dd=window.DalleReelle(PIDS[(mi+t+1)%PIDS.length],monde);
      if(!dd)continue;
      dd.style.width=(dd.width/DPR)+'px'; dd.style.height=(dd.height/DPR)+'px';
      dd.className='p1'; trio.appendChild(dd);
    }
    col(band,trio,'à 1:1 — la taille d’une cellule');

    row.appendChild(band);
    var cap=document.createElement('p'); cap.innerHTML='<b>'+monde.toUpperCase()+'</b>';
    row.appendChild(cap);
    root.appendChild(row);
  }

  /* ── 2 · UN MORCEAU DE TOILE ───────────────────────────────────────────── */
  var t2=document.createElement('div'); t2.className='tete2';
  t2.innerHTML='<h2>Un morceau de Toile — les vraies dalles, le vide entre elles</h2>'+
    '<p class="s">À gauche brut. À droite avec la lumière générale : une seule pour toute la '+
    'scène, jamais posée dalle par dalle. C’est le seul ajout, et il se refuse d’un coup d’œil.</p>';
  root.appendChild(t2);

  for(mi=0;mi<MONDES.length;mi++){
    var mo=MONDES[mi];
    Toile.setTheme(mo);
    await attends(1500);
    var D=[], pid;
    for(pid=1;pid<=14;pid++){
      var ab=null; try{ ab=Toile.dalleAbs(pid); }catch(e){}
      if(!ab||!ab.w)continue;
      var cvd=window.DalleReelle(pid,mo);
      if(!cvd||!cvd.width)continue;
      D.push({cx:ab.minx+ab.w/2, cy:ab.miny+ab.h/2, cv:cvd});
    }
    if(!D.length)continue;

    var x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
    D.forEach(function(d){
      var w=d.cv.width/DPR/2, h=d.cv.height/DPR/2;
      if(d.cx-w<x0)x0=d.cx-w; if(d.cx+w>x1)x1=d.cx+w;
      if(d.cy-h<y0)y0=d.cy-h; if(d.cy+h>y1)y1=d.cy+h;});
    var PWt=Math.ceil(x1-x0)+10, PHt=Math.ceil(y1-y0)+10;

    var monte=function(jour){
      var c=document.createElement('canvas');
      c.width=Math.round(PWt*DPR); c.height=Math.round(PHt*DPR);
      c.style.width=PWt+'px'; c.style.height=PHt+'px';
      var g=c.getContext('2d');
      D.forEach(function(d){
        g.drawImage(d.cv, Math.round((d.cx-x0+5)*DPR-d.cv.width/2),
                          Math.round((d.cy-y0+5)*DPR-d.cv.height/2));});
      if(jour&&window.Velours&&window.Velours.jour) window.Velours.jour(c);
      c.className='p'; return c;
    };
    var row2=document.createElement('div'); row2.className='row';
    var band2=document.createElement('div'); band2.className='band';
    col(band2,monte(false),'brut');
    col(band2,monte(true),'+ la lumière générale');
    row2.appendChild(band2);
    var cap2=document.createElement('p'); cap2.innerHTML='<b>'+mo.toUpperCase()+'</b>';
    row2.appendChild(cap2);
    root.appendChild(row2);
  }

  window.__pret=true;
};
})();
