
/* ⚑ SUR L'ÉCRAN PORTÉ D'UNE NUÉE, LA CLASSE HÉRITÉE `dp-nuee` N'A PAS DE PLACE.
   L'écran porté est piloté par `dp-mode-nuee`. Toutes ses règles sont écrites en paires
   `#detailPoster.dp-nuee, #detailPoster.dp-mode-nuee …` : la seconde moitié suffit.
   `dp-nuee`, elle, réveille tout le CSS d'AVANT le portage. Mesuré, deux thèmes :

       sans dp-nuee   #detailPoster  display:flex  position:absolute  height:844  ch:844
                      barre Peaufiner  y = 760                      ✔ l'écran juste
       avec dp-nuee   #detailPoster  display:block position:relative height:0    ch:0
                      barre Peaufiner  y =   0     par-dessus « ✕ FERMER »       ✘

   Elle n'arrive pas toujours : `renderNueeDetail` la pose (l. 9420) et `_fichePose` la
   repose (l. 5467), tandis que `renderDetail` (l. 3557) et le bascule de la l. 5912 la
   retirent — selon qu'une fiche de Promi a été ouverte AVANT ou non, l'écran est juste
   ou cassé. C'est ce qui faisait dire à `redteam_aveugle` « FERMER ⨯ Peaufiner▾ ».

   On ne touche NI au CSS d'origine, NI à `renderNueeDetail`, NI à `_fichePose` : on
   remet simplement l'écran porté dans l'état où il est juste — celui du premier passage.
   Le §8 interdit le `MutationObserver` qui se réveille lui-même : on n'observe rien, on
   se greffe sur les fonctions qui posent l'écran, et on repasse aux temps de `peintMinis`. */
(function(){
  function nettoie(){
    var dp=document.getElementById('detailPoster'); if(!dp) return;
    if(dp.classList.contains('dp-mode-nuee') && dp.classList.contains('dp-nuee'))
      dp.classList.remove('dp-nuee');
  }
  window._nueeClasseNettoie = nettoie;
  ['renderNueeDetail','_fichePose','renderDetail','openEssaim'].forEach(function(n){
    var f=window[n]; if(typeof f!=='function') return;
    window[n]=function(){ var r=f.apply(this,arguments);
      nettoie(); [0,60,200,600].forEach(function(ms){ setTimeout(nettoie,ms); });
      return r; };
  });
})();
