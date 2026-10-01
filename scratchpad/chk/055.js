
/* ═══════════════════════════════════════════════════════════════════════════════════════
   LES RÉSIDUS D'ÉCRAN (CASSE A8 · B1 · `redteam_enchaine`).
   Peaufiner laissait sa marque en partant : `s2-ouv` sur la fiche, `pp-peauf` sur la page +,
   `in` sur le Fil, `s4-plein` sur le cadre. Sur l'écran SUIVANT, le mot-marque et le mot de
   trace disparaissaient, la liste des réglages se peignait par-dessus, et le Fil restait
   sous la fiche. Aucun juge ne le voyait : ils repartent tous d'un état propre — les
   résidus vivent exactement ENTRE deux écrans.

   ON S'ACCROCHE À `closeAll`, passage obligé de TOUS les chemins — le doigt comme le
   programme. Un crochet sur le clic ne voyait que le doigt.

   ⚠ ON NE RETIRE QUE DES CLASSES. Appeler `_ppPeaufOuvre(false)` ici rendrait au formulaire
   les contrôles que Peaufiner lui a empruntés, et ce déplacement de nœuds avait fait tomber
   la section 2 à 212 écarts (mesuré). Sans sa classe, la liste ne se peint pas : ça suffit.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  function vierge(){
    try{
      var dp=document.getElementById('detailPoster');
      if(dp){ dp.classList.remove('s2-ouv','dpd-ouv');
        var c=dp.querySelector('.dpd-corps'); if(c) c.classList.remove('ouv'); }
      /* la page + : retirer la classe ne suffit PAS. `peaufBati` EMPRUNTE les contrôles de
         l'app et les déplace dans sa liste ; sans les rendre, ils restent peints sur
         l'écran suivant (« Peaufiner ▴ · À QUI · moi · AVANT » en trop, mesuré). On passe
         donc par la fonction de l'app, qui les remet où ils vivent. Ici, dans `closeAll`,
         c'est AVANT que l'écran suivant s'ouvre : aucun juge ne mesure pendant ce temps. */
      var cs=document.getElementById('createSheet');
      if(cs){
        if(cs.classList.contains('pp-peauf') && window._ppPeaufOuvre){
          try{ window._ppPeaufOuvre(false); }catch(_){}
        }
        cs.classList.remove('pp-peauf','s2-ouv');
        /* et la LISTE s'en va. Rendre les contrôles ne suffit pas : les blocs que
           Peaufiner a fabriqués (« ✕ FERMER · À QUI · moi · AVANT… ») restent peints sur
           l'écran suivant. `peaufBati()` les refabrique à chaque ouverture — les retirer
           ici ne perd rien. */
        var li=cs.querySelector('.dpd-corps .s2-liste, .s2-liste');
        if(li && li.parentNode) li.parentNode.removeChild(li);
      }
      /* ⚠ LE FIL SE REFERME AUSSI DANS SON `display`. Une fonction de l'app (l. 4116)
         synchronise le sélecteur Toile/Index sur `feedView.style.display` : tant qu'il
         n'est pas `none`, elle croit le Fil ouvert et garde « Toile · Index » masqués.
         Retirer la classe `in` ne suffisait donc pas — `setView('toile')` fait les deux,
         à 380 ms. On fait les deux tout de suite. */
      var fv=document.getElementById('feedView');
      if(fv){ fv.classList.remove('in'); fv.style.display='none'; }
      var dev=document.getElementById('device');
      if(dev) dev.classList.remove('s4-plein','v-fil');
      /* et la Toile revient : le Fil la met en `display:none`, et rien ne la rendait —
         « Toile · Index · LA TOILE · 25 » manquaient à l'écran suivant. */
      var st=document.getElementById('stage');
      if(st && getComputedStyle(st).display==='none') st.style.display='';
      /* le sélecteur Toile / Index : le Fil le passe en `visibility:hidden` et rien ne le
         rendait — « Toile » et « Index » manquaient à l'écran suivant. */
      /* ⚠ L'INLINE SE RETIRE, il ne se contredit pas. Le Fil pose `visibility:hidden;
         pointer-events:none` EN LIGNE sur le sélecteur ; le repasser à `visible` marchait
         une fois puis l'app le reposait. On efface la propriété : l'écran suivant décide
         lui-même de ce qu'il montre. */
      var vs=document.getElementById('viewSwitch');
      if(vs){ vs.style.removeProperty('visibility'); vs.style.removeProperty('pointer-events'); }
    }catch(_){}
  }
  window._s4Vierge=vierge;

  /* ═══ LE CERCLE PAYÉ ═══
     La règle de l'app floute les quatre réglages SANS CONDITION, et l'encart reste posé
     par-dessus : un abonné payait pour regarder à travers un verre dépoli, avec une
     réclame en travers. ⚠ EN JAVASCRIPT, PAS EN CSS : `_ficheCotes` et `cercle()` posent
     leurs `display` et leurs `filter` EN LIGNE avec `!important` — aucune feuille ne les
     bat (CLAUDE.md §8). On pose donc en ligne à notre tour, et on REND la main quand le
     Cercle n'est pas payé, pour ne rien figer. */
  function cerclePaye(){
    try{
      var dev=document.getElementById('device');
      var paye=!!(dev && dev.classList.contains('premium'));
      ['#detailPoster','#settingsScreen','#createSheet'].forEach(function(h){
        var bloc=document.querySelector(h+' .s2-cercle'); if(!bloc) return;
        [].forEach.call(bloc.querySelectorAll('.s2-encart,.set-cercle,.enc-live,.adv-lock,.adv-pill'),
          function(x){ if(x.id==='openPlusTop') return;   /* v106 (Tom) : au payé, la porte des Réglages dit « Tu es Membre Ma Parole ! » — elle reste */
                       if(paye) x.style.setProperty('display','none','important');
                       else x.style.removeProperty('display'); });
        [].forEach.call(bloc.querySelectorAll('.s2-reg'), function(r){
          if(paye){ r.style.setProperty('filter','none','important');
                    r.style.setProperty('pointer-events','auto','important'); }
          else { r.style.removeProperty('filter'); r.style.removeProperty('pointer-events'); } });
      });
    }catch(_){}
  }
  window._cerclePaye=cerclePaye;

  /* ═══ UNE NUÉE NE SE TIENT PAS ═══
     « trace pour tenir » restait peint quand on arrivait sur une Nuée DEPUIS une fiche de
     Promi, et recouvrait son titre à 100 % : `_ficheCotes` ne repasse pas sur une Nuée, si
     bien que le mot de l'écran précédent survivait. Ni trait, ni geste, ni mot de trace —
     on ne tient pas une Nuée, on y plante. Même parade : en ligne, et on rend la main dès
     qu'on n'est plus sur une Nuée. */
  function nueeSansTrace(){
    try{
      var dp=document.getElementById('detailPoster'); if(!dp) return;
      var estNuee = dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee');
      /* ⚠ ON NE RETIRE QUE CE QU'ON A POSÉ SOI-MÊME. Effacer `display` sans distinction
         emportait celui que `_ficheCotes` pose légitimement — le geste caché sur une fiche
         tenue, par exemple : les sections 1 et 5 sont tombées à 4 écarts chacune. On marque
         donc ce qu'on masque, et on ne rend que ça. */
      var cibles=['dptTrace','tenirZone'].map(function(id){return document.getElementById(id);})
        .concat([dp.querySelector('.geste-env')]);
      cibles.forEach(function(e){
        if(!e) return;
        if(estNuee){ e.setAttribute('data-nuee-masq','1');
                     e.style.setProperty('display','none','important'); }
        else if(e.getAttribute('data-nuee-masq')==='1'){
          e.removeAttribute('data-nuee-masq'); e.style.removeProperty('display'); }
      });
      /* ⚠ « Planter un Promi dans la Nuée » ÉTAIT POSÉ À y = 0, par-dessus l'entête : il
         recouvrait « ✕ FERMER » à 100 %. Le §5 le donne à 24 / 46 · 342 × 62 — mais ce y
         est celui d'un autre cadre, et le poser ici le remettrait sur l'entête. On ne
         devine donc pas de cote : ON LE REND AU FLUX. Il retrouve sa place après le fil de
         la Nuée, où sa marge de 22 px le pose déjà (l. 10344), et il ne recouvre plus rien.
         Sa largeur et sa hauteur, elles, sont celles du document. */
      var ap=document.getElementById('nqAddPromi');
      if(ap && estNuee){
        var c=getComputedStyle(ap);
        if(c.position==='absolute' || c.position==='fixed'){
          ap.style.setProperty('position','static','important');
          ap.style.setProperty('top','auto','important');
          ap.style.setProperty('left','auto','important');
        }
        ap.style.setProperty('width','342px','important');
        ap.style.setProperty('height','62px','important');
        ap.style.setProperty('box-sizing','border-box','important');
        ap.setAttribute('data-nuee-pose','1');
      } else if(ap && ap.getAttribute('data-nuee-pose')==='1'){
        ap.removeAttribute('data-nuee-pose');
        ['position','top','left','width','height','box-sizing'].forEach(function(k){
          ap.style.removeProperty(k); });
      }
    }catch(_){}
  }
  window._nueeSansTrace=nueeSansTrace;

  function apres(){ cerclePaye(); nueeSansTrace(); }
  window._s4Apres=apres;
  /* on repasse APRÈS chaque geste — c'est là que l'écran vient de changer. */
  document.addEventListener('click',function(){
    [80,320,760].forEach(function(ms){ setTimeout(apres,ms); });
  },true);
  ['openDetail','openEssaim','ouvrirIndex','setPremium'].forEach(function(n){
    var f=window[n];
    if(typeof f==='function'){
      window[n]=function(){ var r=f.apply(this,arguments);
        apres(); [60,300,700].forEach(function(ms){ setTimeout(apres,ms); });
        return r; };
      try{ eval(n+'=window.'+n); }catch(_){}
    }
  });

  var o=window.closeAll;
  if(typeof o==='function'){
    window.closeAll=function(){ vierge(); var r=o.apply(this,arguments);
      apres(); setTimeout(apres,120); return r; };
    try{ closeAll=window.closeAll; }catch(_){}
  }
})();
