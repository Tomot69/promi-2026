
/* ⚑ LE CLIC FANTÔME — trouvé au vrai doigt, 11 sept. 2026 (événements tactiles CDP ; les juges jouaient à la souris).
   Après un toucher, le navigateur synthétise mousedown / mouseup / click AU POINT DU DOIGT, APRÈS touchend. Une porte qui
   ouvre au lever du doigt (pointerup) ouvre donc AVANT ce clic — et le clic tombe sur ce qui vient de s'ouvrir.
   MESURÉ sur la porte des Noyaux de l'Aura (lot-AURA-PELOTE, gestesNoyaux) : toucher Marion → openPerson(Marion) →
   closeAll ← openSheet → touchend → click sur #scrim → la fiche se referme : l'Aura, rien d'ouvert. Sur un téléphone,
   toucher un Noyau n'ouvrait donc rien de visible. À la souris, ce clic arrive sur l'élément de départ : vert.
   LA PARADE — la forme exacte du défaut, rien de plus, et sans toucher à aucune porte existante : un clic ISSU D'UN
   TOUCHER qui tombe sur une COUCHE OUVERTE PENDANT LE GESTE (la plus proche couche `.show` du clic n'était pas ouverte
   quand le doigt s'est posé) est la queue du geste précédent : il est avalé, avant tout autre écouteur (window, capture).
   JAMAIS : un clic de souris (pointerType), un clic de script (isTrusted), un clic sur une couche déjà ouverte au toucher
   — toucher ✕, un bouton, une carte, le voile d'une feuille ouverte : tout marche comme avant, même si l'élément touché
   est redessiné sous le doigt. (Une première écriture comparait l'élément touché à l'élément cliqué : elle aurait avalé un
   vrai toucher sur un bouton que l'app redessine — remplacée avant toute série.) */
(function(){ try{
  var p0 = null;
  window.addEventListener('pointerdown', function(e){
    p0 = {type:e.pointerType, at:Date.now(), ouvertes:[].slice.call(document.querySelectorAll('.show'))};
  }, true);
  window.addEventListener('click', function(e){
    if(!e.isTrusted || !p0 || p0.type !== 'touch' || Date.now() - p0.at > 1000) return;
    var b = e.target; if(!b || !b.closest) return;
    var couche = b.closest('.show');
    if(!couche || p0.ouvertes.indexOf(couche) >= 0) return;
    e.stopPropagation(); e.preventDefault();
  }, true);
}catch(e){} })();
