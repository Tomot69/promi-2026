
/* ⚑ v29 (redteam_decoupe, famille G) — L'APERÇU DE PARTAGER S'AFFICHE À LA TAILLE OÙ IL EST PEINT.
   `shareRender` calcule sa taille sur la largeur de `#shareScreen` (422 px, §8 : un .screen ne coïncide pas avec
   #device), et le CSS l'affichait ensuite dans une zone plus étroite : le navigateur réduisait la Toile de ×0,86.
   On mesure une fois le rapport entre ce qui est AFFICHÉ et ce qui est peint, et on repeint à la bonne taille.
   Rien ne bouge à l'écran — la boîte affichée est la même ; seul ce qu'elle contient cesse d'être redimensionné. */
(function(){
  function arme(){
    var _sr=window.shareRender; if(typeof _sr!=='function'||_sr.__aj) return;
    var w=function(){ var r=_sr.apply(this,arguments);
      try{ if(!window.__shAjEnCours){
        var cv=document.getElementById('shCanvas'), dev=document.getElementById('device'); if(!cv||!dev||!cv.width) return r;
        var rr=cv.getBoundingClientRect(); if(rr.width<6) return r;
        var sc=dev.getBoundingClientRect().width/390, dpr=window.devicePixelRatio||1, f=(rr.width/sc*dpr)/cv.width;
        if(Math.abs(f-1)>0.03){ window._shAj=(window._shAj||1)*f; window.__shAjEnCours=1;
          try{ _sr.apply(this,arguments); }finally{ window.__shAjEnCours=0; } } } }catch(_){}
      return r; };
    w.__aj=1; window.shareRender=w;
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',function(){ setTimeout(arme,0); }); else setTimeout(arme,0);
  setTimeout(arme,1500);
})();
