
/* ⚑ v117 (Tom) — « Les boutons Partager des fiches ne font rien — Promi, Chiche, Cercle. Corrige. Et vérifie que l'image
   produite ressemble à ce que donne Mon Folio quand on ne garde qu'une dalle. »
   CAUSE, mesurée : le rond appelait `ouvrirPartage()`, qui n'existe nulle part — il retombait sur `#shareScreen.show`
   posé à nu, sans `openShare()` : écran vide, rien de peint. Et AU DOIGT, la barre Peaufiner ne produit aucun `click`
   (§8, v104) : même la branche de secours ne partait pas.
   · le partage d'une fiche, c'est MON FOLIO réduit à cette parole — EXACTEMENT ce que donne Mon Folio quand on décoche
     tout le reste : mêmes peintres (`sharePlanche`, export `_shExporteCanevas`), sans la Pelote ;
   · un Cercle : son Folio, c'est-à-dire ses Promi (une Nuée n'a pas de case de Folio) ;
   · ce que l'utilisateur avait choisi au partage (`shareHidden`, le sujet, la Pelote) est RENDU à la fermeture et n'est
     jamais sauvegardé entre-temps. */
(function(){
  var AV=null, tDoigt=0;
  function sujet(){
    try{
      if(typeof curNuee!=='undefined' && curNuee){
        var dp=document.getElementById('detailPoster');
        if(dp && (dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')))
          return {ids:promises.filter(function(p){ return p.nuee===curNuee && !p.draft && !p.req; }).map(function(p){ return p.id; }), nuee:curNuee};
      }
      if(typeof cur!=='undefined' && cur) return {ids:[cur.id], nuee:null};
    }catch(_){}
    return null;
  }
  function rends(){
    if(!AV) return;
    try{ shareHidden=AV.h; window.shareHidden=AV.h; }catch(_){}
    try{ window.shPelote=AV.pel; }catch(_){}
    try{ var b=document.querySelector('#shMode button[data-mode="'+AV.mode+'"]'); AV=null; if(b) b.click(); }catch(_){ AV=null; }
    try{ if(window._majQpRail) _majQpRail(); }catch(_){}
  }
  window.ouvrirPartage=function(){
    var s=sujet(); if(!s || !s.ids.length) { try{ openShare(); }catch(_){} return; }
    if(!AV) AV={h:shareHidden, mode:(typeof shareMode!=='undefined'?shareMode:'toile'), pel:!!window.shPelote};
    var h={}; promises.forEach(function(p){ if(s.ids.indexOf(p.id)<0) h[p.id]=true; });
    try{ Object.keys(NUE).forEach(function(k){ if(k!==s.nuee) h['n:'+k]=true; }); }catch(_){}
    shareHidden=h; window.shareHidden=h; window.shPelote=false;
    window._partageFicheSujet=s;
    openShare();
    try{ var b=document.querySelector('#shMode button[data-mode="mosaic"]'); if(b) b.click(); }catch(_){}
    try{ if(window._majQpRail) _majQpRail(); }catch(_){}
  };
  /* la barre Peaufiner ne produit pas de `click` (§8 v104) — on lit le geste (appui, lever sans glisser) */
  var x0=0,y0=0,t0=0,sur=null;
  document.addEventListener('pointerdown', function(e){
    sur=e.target.closest && e.target.closest('#dpDetails .dpd-part'); x0=e.clientX; y0=e.clientY; t0=performance.now(); }, true);
  document.addEventListener('pointerup', function(e){
    var s=sur; sur=null; if(!s) return;   /* tous les pointeurs : à la souris non plus, le `click` n'arrive pas au rond (mesuré, v117) */
    if(Math.hypot(e.clientX-x0, e.clientY-y0)>10 || performance.now()-t0>600) return;
    tDoigt=performance.now(); e.stopPropagation();
    try{ window.ouvrirPartage(); }catch(_){}
  }, true);
  window._partageFiche={ deja:function(){ return performance.now()-tDoigt<800; }, rends:rends };
  /* la fermeture : `#shareScreen` PERD-il `.show` ? (§8 — vérifié à la mesure, `redteam_partage_fiche`) */
  function guette(){
    var sc=document.getElementById('shareScreen'); if(!sc){ setTimeout(guette, 300); return; }
    var etait=sc.classList.contains('show');
    new MutationObserver(function(){ var est=sc.classList.contains('show'); if(est===etait) return; etait=est;
      if(!est && AV) rends(); }).observe(sc, {attributes:true, attributeFilter:['class']});
  }
  guette();
  /* jamais sauvegardé pendant : la sauvegarde écrit ce que l'utilisateur avait choisi */
  (function enveloppe(n){
    if(typeof window.saveState!=='function'){ if(n<50) setTimeout(function(){ enveloppe(n+1); },100); return; }
    if(window.saveState.__v117) return;
    var f=window.saveState;
    var g=function(){ if(!AV) return f.apply(this, arguments);
      var tmp=shareHidden; shareHidden=AV.h; try{ return f.apply(this, arguments); } finally { shareHidden=tmp; } };
    g.__v117=true; window.saveState=g;
  })(0);
})();
