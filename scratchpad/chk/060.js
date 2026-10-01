
/* ═══════════════════════════════════════════════════════════════════════════════════════
   RIEN NE SURVIT À `closeAll` — LA RÈGLE, PAS LE CAS.

   Un écran qui masque un nœud le fait **en ligne**, en `display:none !important` : c'est le
   seul moyen de battre les cotes que les sections posent, elles aussi en ligne. Mais un
   style en ligne ne connaît pas la fin de son écran : il reste, et **l'écran SUIVANT
   hérite du masque**. C'est un mécanisme, pas un accident — et il a frappé quatre fois :

     · la classe héritée `dp-nuee` sur l'écran porté d'une Nuée ;
     · le `min-height` d'une Nuée, qui volait sa barre Peaufiner à la fiche suivante ;
     · les cartes du Peaufiner d'une Nuée, posées par-dessus le titre de la fiche suivante ;
     · et celui-ci, le pire : **le Peaufiner d'une Nuée masque `#dpTrameCv`** — le canevas
       du champ — plus `dAura`, `dptQui`, `dptTitre`, `dptQuand`, `dpNueeFil`. Après lui,
       **tout écran de fiche est vide** : le champ est peint (10 821 pixels, mesuré) mais
       jamais affiché. Le pas clair vient après le pas sombre : dans une passe complète,
       **la moitié des captures sortaient blanches.**

   LA RÈGLE, déjà écrite au §8 de CLAUDE.md et jamais appliquée en général :
   **on marque ce qu'on masque, et on ne rend que ça.**

   Les deux `cache()` du produit — celui de l'instant, celui du Peaufiner d'une Nuée —
   posent désormais `data-masque="1"`. Ce bloc les rend à `closeAll`, et à lui seul :
   l'écran qui s'ouvre ensuite remasquera ce dont il a besoin, comme il l'a toujours fait.
   On ne devine rien, on ne rend rien qu'on n'ait posé.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  function rend(){
    var n = document.querySelectorAll('[data-masque]');
    for(var i=0;i<n.length;i++){
      n[i].style.removeProperty('display');
      n[i].removeAttribute('data-masque');
    }
    /* ⚠ ET LES CLASSES D'ÉTAT D'UN PANNEAU OUVERT. `s2-ouv` dit « le Peaufiner de CETTE
       fiche est déplié » ; elle porte `#dpTrameCv{visibility:hidden}`. Restée sur le poster,
       elle éteint le champ de l'écran suivant — mesuré : la fiche d'une Nuée ouverte après
       un Peaufiner de fiche sortait sans champ, en clair. Une classe d'état ne se garde pas
       d'un écran à l'autre : celui qui s'ouvre la remet s'il en a besoin. */
    var dp = document.getElementById('detailPoster');
    if(dp) dp.classList.remove('s2-ouv');
    var dd = document.getElementById('dpDetails');
    if(dd) dd.classList.remove('ouvert');
    /* ⚠ ET CE QU'UN ÉCRAN A **AJOUTÉ**. La règle était à moitié écrite : je rendais ce
       qu'on avait masqué, je ne rangeais pas ce qu'on avait bâti. Vu à l'œil sur
       `fiche-tenue_light` — la fiche portait, par-dessus son titre, les cartes du
       Peaufiner d'une Nuée : « le potager », DESCRIPTION, MEMBRES, PIÈCES, COMMENTAIRES
       et « Planter un Promi dans la Nuée ». `rangeNuee()` existait et savait les retirer ;
       personne ne l'appelait à la fermeture.
       LA RÈGLE ENTIÈRE : **rien ne survit à `closeAll` — ni ce qu'un écran masque, ni ce
       qu'il ajoute.** Un écran qui bâtit déclare son rangeur ici, et `closeAll` les passe
       tous. C'est un registre, pas un cas : le prochain écran qui bâtira n'aura qu'à
       s'y inscrire, et rien à corriger dans ce bloc. */
    /* Et les propriétés posées en ligne par un écran qui bâtit (voir `pose` ci-dessus) :
       on retire exactement celles qu'on a notées, jamais une de plus. L'écran suivant
       repose les siennes à l'ouverture, comme il l'a toujours fait. */
    var q = document.querySelectorAll('[data-pose]');
    for(var k=0;k<q.length;k++){
      var props = (q[k].getAttribute('data-pose')||'').split(' ').filter(Boolean);
      for(var m=0;m<props.length;m++) q[k].style.removeProperty(props[m]);
      q[k].removeAttribute('data-pose');
    }
    var rg = window._rangeurs || [];
    for(var j=0;j<rg.length;j++){ try{ rg[j](); }catch(_){} }
  }
  window._rangeurs = window._rangeurs || [];
  window._rendMasques = rend;
  var _ca = window.closeAll;
  if(typeof _ca === 'function'){
    window.closeAll = function(){ var r = _ca.apply(this, arguments); rend(); return r; };
    try{ closeAll = window.closeAll; }catch(_){}
  }
})();
