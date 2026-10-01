
/* ══ LOT 1 · le geste pour PLANTER sur la page + ══
   Duplicata ISOLÉ du geste de tenir. N'appelle ni ne modifie _tenirInit.
   Points/tracé calqués sur peindre() de la fiche (r=19, x=38 des bords).
   Sur validation : clique #addPromi (l'action « planter » existante).
   À mutualiser avec le moteur du geste dans un lot dédié. */
(function(){
  function init(zone,cv,lab,alt){
    if(!zone||!cv||zone._pose) return;
    zone._pose=true;
    var g,W=0,H=0,dpr=1,pts=[],actif=false,arrive=false;
    function ink(){
      try{ var cs=document.getElementById('createSheet');
        var bg=getComputedStyle(cs).backgroundColor.match(/[\d.]+/g)||[247,240,222];
        var lum=(+bg[0]*299 + +bg[1]*587 + +bg[2]*114)/1000;
        /* sur la page + (fond de nature, foncé) les cercles/tracé sont BLANCS PURS,
           comme le moodboard (« cercles blancs contrastés ») — pas crème. */
        return lum>150 ? '#201908' : '#fff';
      }catch(_){ return '#201908'; }
    }
    function taille(){
      dpr=Math.min(2,window.devicePixelRatio||1);
      var r=cv.getBoundingClientRect();
      W=Math.round(r.width)||zone.clientWidth; H=Math.round(r.height)||zone.clientHeight;
      if(!W||!H){ g=null; return; }
      cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
      g=cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
    }
    /* positions EXACTES du moodboard (viewBox 308×118) : cx 42/266, cy 52, r 18 —
       mises à l'échelle du panneau réel. */
    function bornes(){ return { a:{x:W*42/308,y:H*52/118}, b:{x:W*266/308,y:H*52/118}, r:H*18/118 }; }
    function peindre(){
      if(!g) return; var c=ink(), B=bornes();
      g.clearRect(0,0,W,H);
      /* point gauche : plein blanc, opacité 1 (baisse à .34 pendant le tracé) */
      g.fillStyle=c; g.globalAlpha=actif?.34:1;
      g.beginPath(); g.arc(B.a.x,B.a.y,B.r,0,6.2832); g.fill(); g.globalAlpha=1;
      /* point droit : anneau (opacité .45, trait 2.2) + petit plein (opacité .45) ;
         les deux montent à 1 quand le doigt ARRIVE — moodboard exact. */
      g.strokeStyle=c; g.globalAlpha=arrive?1:.45; g.lineWidth=H*2.2/118;
      g.beginPath(); g.arc(B.b.x,B.b.y,B.r,0,6.2832); g.stroke();
      g.fillStyle=c; g.globalAlpha=arrive?1:.45;
      g.beginPath(); g.arc(B.b.x,B.b.y,B.r/3,0,6.2832); g.fill(); g.globalAlpha=1;
      /* le tracé : courbes quadratiques, jamais de segments droits */
      if(pts.length>1){
        g.strokeStyle=c; g.lineWidth=8; g.lineCap='round'; g.lineJoin='round';
        g.beginPath(); g.moveTo(pts[0].x,pts[0].y);
        if(pts.length===2){ g.lineTo(pts[1].x,pts[1].y); }
        else{ for(var i=1;i<pts.length-1;i++){ var mx=(pts[i].x+pts[i+1].x)/2,my=(pts[i].y+pts[i+1].y)/2; g.quadraticCurveTo(pts[i].x,pts[i].y,mx,my); }
          g.quadraticCurveTo(pts[pts.length-2].x,pts[pts.length-2].y,pts[pts.length-1].x,pts[pts.length-1].y); }
        g.stroke();
      }
    }
    function pos(e){ var r=cv.getBoundingClientRect(); var t=e.touches?e.touches[0]:e; return { x:t.clientX-r.left, y:t.clientY-r.top }; }
    function debut(e){ if(!g) taille(); var p=pos(e),B=bornes(); if(p.x>B.a.x+130) return;
      actif=true; arrive=false; pts=[{x:B.a.x,y:B.a.y}]; if(Math.hypot(p.x-B.a.x,p.y-B.a.y)>6)pts.push(p);
      zone.classList.add('ouvert'); peindre(); if(e.preventDefault)e.preventDefault(); }
    function bouge(e){ if(!actif) return; var p=pos(e); pts.push(p); var B=bornes();
      if(!arrive && p.x>B.a.x+(B.b.x-B.a.x)*0.66){ arrive=true; try{ if(navigator.vibrate)navigator.vibrate(14); }catch(_){}}
      peindre();
      /* LE DOIGT PUBLIE SA POSITION. Sur la page +, la surface où l'on trace est L'ONDE
         (§5, cadres 29-30 « Le geste · pendant ») : le plein va de 0 à la position du
         doigt, jamais au-delà du milieu (§2.6). On donne l'abscisse en coordonnées
         d'écran 390 ; le trait s'en occupe. */
      try{ window._ppDoigt = Math.max(0, Math.min(390, p.x * 390 / (W||390)));
        if(window._ppTout) _ppTout(); }catch(_){}
      if(e.preventDefault)e.preventDefault(); }
    function fin(){ if(!actif) return; actif=false;
      var parcouru=pts.length>1?pts[pts.length-1].x-pts[0].x:0;
      var ok=arrive||parcouru>W*0.5;
      zone.classList.remove('ouvert');
      if(ok){ try{ if(navigator.vibrate)navigator.vibrate([12,40,26]); }catch(_){}
        /* bug (d) : le geste plantait TOUJOURS un Promi (#addPromi) — une Nuée ou un
           Brouillon n'étaient jamais validés. On cible le bouton de la nature active. */
        var _k=window.createKind; if(!_k){ var _cs=document.getElementById('createSheet'); _k=_cs&&_cs.getAttribute('data-kind'); }
        var _bid=(_k==='nuee')?'addNuee':((_k==='draft')?'addDraft':'addPromi');
        var b=document.getElementById(_bid); if(b) b.click(); }
      arrive=false;
      try{ window._ppDoigt = null; if(window._ppTout) _ppTout(); }catch(_){}
      setTimeout(function(){ pts=[]; taille(); peindre(); },330); }
    zone.addEventListener('touchstart',debut,{passive:false});
    zone.addEventListener('touchmove',bouge,{passive:false});
    zone.addEventListener('touchend',fin,{passive:true});
    zone.addEventListener('mousedown',debut);
    window.addEventListener('mousemove',bouge);
    window.addEventListener('mouseup',fin);
    window.addEventListener('resize',function(){ taille(); peindre(); });
    /* bascule trait / bouton, ISOLÉE à la page + (ne touche pas #detailPoster) */
    /* bascule trait/bouton = deux petites flèches discrètes (pas une pastille) */
    var SW='<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6.5 8 L10 4.5 L13.5 8"/><path d="M6.5 12 L10 15.5 L13.5 12"/></svg>';
    if(alt){ alt.innerHTML=SW; alt.setAttribute('aria-label','trait ou bouton');
      alt.addEventListener('click',function(e){
        var cs=document.getElementById('createSheet');
        cs.classList.toggle('cs-geste-bouton');
        if(!cs.classList.contains('cs-geste-bouton')) setTimeout(function(){ taille(); peindre(); },30);
        e.stopPropagation();
      }); }
    taille(); peindre();
    (window._planterRepaint=window._planterRepaint||[]).push(function(){ taille(); peindre(); });
  }
  /* CHANTIER H — le geste vaut pour les TROIS natures : on câble une zone par
     formulaire (Promi/Nuée/Brouillon). La validation route déjà vers addPromi/
     addNuee/addDraft selon createKind (voir fin()). */
  function initAll(){
    [['planterZone','planterCv','planterLab','planterAlt'],
     ['planterZoneN','planterCvN','planterLabN','planterAltN'],
     ['planterZoneD','planterCvD','planterLabD','planterAltD']].forEach(function(p){
      init(document.getElementById(p[0]),document.getElementById(p[1]),document.getElementById(p[2]),document.getElementById(p[3]));
    });
  }
  window._planterPeindre=function(){ (window._planterRepaint||[]).forEach(function(f){ try{f();}catch(_){} }); };
  function go(){ initAll(); try{ if(window._planterPeindre)_planterPeindre(); }catch(_){}}
  if(document.readyState!=='loading') initAll(); else document.addEventListener('DOMContentLoaded',initAll);
  var cb=document.getElementById('createBtn');
  if(cb) cb.addEventListener('click',function(){ setTimeout(go,80); setTimeout(go,320); });
  document.addEventListener('click',function(e){
    var t=e.target.closest && e.target.closest('#createSheet .tile');
    if(t) setTimeout(go,60);
  },true);
})();
