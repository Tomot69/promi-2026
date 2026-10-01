
/* ⚑ LE « i » DE PROMI GARDE SON ACCENT — il était le second chemin du dessin. Le mot-marque de
   l'accueil l'a déjà (`Prom<i>i</i>`) ; la page + et la fiche écrivent « Promi » en texte.
   ⚠ UN OBSERVATEUR QUI COMPARE AVANT D'AGIR (§8) : on ne réécrit que le texte nu « Promi ». */
(function(){
  var SEL = '#createSheet .cs-mark, #detailPoster #dptNat, #shWordmark';
  function pose(){
    var els=[]; try{ els=[].slice.call(document.querySelectorAll(SEL)); }catch(e){ return; }
    els.forEach(function(el){
      if(el.querySelector('.mm-i')) return;
      if(el.children.length || (el.textContent||'').trim()!=='Promi') return;
      el.innerHTML='Prom<i class="mm-i">i</i>';
    });
  }
  function armer(){
    pose();
    try{ new MutationObserver(pose).observe(document.body,{childList:true,subtree:true,characterData:true}); }catch(e){}
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', armer);
  else armer();
  window._titresDessins = pose;   /* l'ancien nom reste appelable */
})();
