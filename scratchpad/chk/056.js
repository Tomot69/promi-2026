
/* ═══════════════════════════════════════════════════════════════════════════════════════
   CE QUI RESTAIT POSÉ ENTRE DEUX PARCOURS : LE TUTORIEL.
   Trois rouges de `redteam_aveugle` — « tenir au geste » (deux thèmes) et « planter » au
   second passage — n'avaient qu'UNE cause, et ce n'était pas un état de la page +.
   Instrumenté à `elementsFromPoint`, sous le doigt : `DIV#tutoOv.tuto-ov2 in [0,0 390x844]
   z=120 pe=auto`. **Le tutoriel du premier Promi.** `addPromi` le lance 450 ms après la
   plantation (`_tutoSeen`) ; il couvre tout l'écran, il prend les événements — et
   `closeAll()` ne le connaît pas. Tout geste postérieur va donc au tutoriel : le geste de
   la fiche ne tient rien, et au parcours suivant le geste de la page + ne plante rien.
   C'est bien « la même famille que ceux que closeAll a absorbés » : un calque de chrome
   qu'aucune fermeture n'atteint. On le lui ajoute — avec SA sortie, celle du tutoriel
   lui-même (`out`, puis retrait à 340 ms) : rien n'est réécrit, rien n'est inventé.
   ⚠ L'ordre est sans risque : `addPromi` appelle `closeAll()` AVANT de programmer le
   tutoriel. On ne le tue pas à la naissance ; on l'empêche de survivre à l'écran suivant —
   ce que dit déjà son propre bouton final, « Explorer mon Promi ».
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  var _ca = window.closeAll;
  if(typeof _ca !== 'function') return;
  window.closeAll = function(){
    var r = _ca.apply(this, arguments);
    try{
      var ov = document.getElementById('tutoOv');
      if(ov){ window._tutoSeen = true; ov.classList.add('out');
        setTimeout(function(){ if(ov.parentNode) ov.parentNode.removeChild(ov); }, 340); }
    }catch(_){}
    return r;
  };
  try{ closeAll = window.closeAll; }catch(_){}
})();
