
/* ══ LE MOT-MARQUE DE LA PAGE + DIT TOUJOURS SA NATURE ══════════════════════════════════
   Tom, 20 septembre 2026 : « Page + : un Chiche ou une Nuée affiche « Promi » en titre. »

   CE QUE J'AI MESURÉ AVANT DE TOUCHER : par les trois pilules de l'accueil, AU VRAI DOIGT,
   les trois natures sortent justes, et les six enchaînements aussi (0 fautif sur 6). Le mot
   n'est donc pas faux sur ce chemin-là. MAIS il n'est posé qu'à UN endroit, et sous garde :
   `if(!cs.classList.contains('pp')) return;`. Le HTML, lui, écrit « Promi » en dur
   (l. 2565). Tout chemin qui ouvre la feuille sans lui donner la classe `pp` — ou qui la
   lui donne après coup — laisse donc le mot du HTML.

   LA PARADE EST CELLE DU §8 : on suit l'ATTRIBUT qui fait autorité, `data-kind`, et pas un
   chemin. Un observateur QUI COMPARE AVANT D'AGIR (sans quoi il se réveille lui-même) tient
   le mot d'accord avec la nature, quel que soit le chemin. Aucune fonction n'est déplacée :
   le poseur d'origine reste, celui-ci le rattrape.
   ══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  var MOT={promi:'Promi', chiche:'Chiche', nuee:'Cercle'};
  function accorde(){
    try{
      var cs=document.getElementById('createSheet'); if(!cs) return;
      var k=cs.getAttribute('data-kind'); var m=MOT[k]; if(!m) return;
      var el=cs.querySelector('.cs-mark'); if(!el) return;
      /* ⚑ v46 — un É COMPOSÉ (lot-V35-E-ACCENT) se lit « NuE’e » : comparé tel quel, le mot paraissait faux, on le réécrivait,
         la composition tombait, et l'on recommençait — « NUÉE » ne gardait jamais son accent PromiLate. On lit le mot d'origine. */
      var lu=(el.querySelector('.v35-e') ? (el.getAttribute('aria-label')||'') : (el.textContent||'')).trim();
      if(lu===m) return;                      /* rien n'a changé : on ne réveille rien */
      el.textContent=m; el.removeAttribute('aria-label');
      /* le « i » de Promi garde son accent — c'est lot-TITRES-POLICE qui le repose */
      try{ if(window._titresDessins) window._titresDessins(); }catch(e){}
    }catch(e){}
  }
  function armer(){
    accorde();
    try{
      var cs=document.getElementById('createSheet'); if(!cs) return;
      new MutationObserver(accorde).observe(cs,{attributes:true,attributeFilter:['data-kind','class']});
      new MutationObserver(accorde).observe(cs,{childList:true,subtree:true,characterData:true});
    }catch(e){}
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',armer); else armer();
  window._marqueNature=accorde;
})();
