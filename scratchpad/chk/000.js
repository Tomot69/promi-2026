
/* ⚑ v52 (Tom, 24 sept. 2026) — « qu'ils puissent déjà payer sans compte, mais on leur spécifie TRÈS explicitement que leur achat
   sera perdu s'il n'y a pas de compte. On reste dans notre ton, mais on ne veut pas de plaintes après. Deux moments : avant de
   payer, clairement ; juste après. » Posé tôt dans le document : un écouteur de la fenêtre en capture passe dans l'ordre où
   il a été posé, et celui du Cercle (lot-CERCLE) achète dès le clic. Les mots sont à valider (QUESTIONS · Q326). */
(function(){
  var ACHAT='#buyYear, #buyMonth, #stLockBuy', feu=false;
  function sansCompte(){ try{ return !(window._onbCompteFait&&window._onbCompteFait()); }catch(_){ return false; } }
  window.addEventListener('click', function(ev){
    var t=ev.target&&ev.target.closest&&ev.target.closest(ACHAT); if(!t) return;
    if(feu||!sansCompte()||!window._onbCompte) return;
    ev.preventDefault(); ev.stopImmediatePropagation();
    window._onbCompte(null, function(k){
      feu=true; try{ t.click(); } finally { feu=false; }
      if(!k) setTimeout(function(){ if(sansCompte()) window._onbCompte(null, null, {
        lab:'Garder ton achat', tx:'Il est sur ce téléphone seulement. Garde ta Toile pour ne pas le perdre.' }); }, 900);
    }, { lab:'Avant d’acheter', tx:'Sans compte, ton achat reste sur ce téléphone : si tu en changes ou supprimes l’app, il est perdu.', tard:'Acheter sans compte' });
  }, true);
})();
