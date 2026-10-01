
(function(){
  /* ⚠ LE TITRE S'AJUSTE, IL NE SE ROGNE PAS. On descend la taille par pas de 1 px
     jusqu'à ce qu'il tienne dans le plateau, avec un plancher à 19 px — en dessous, ce
     n'est plus un titre. On COMPARE avant d'écrire, sinon on relance la mise en page à
     chaque passe (§8). */
  function ajusteTitres(){
    [].forEach.call(document.querySelectorAll('.enh'), function(b){
      var t=b.querySelector('.enh-t'); if(!t) return;
      var r=b.getBoundingClientRect(); if(r.width<40) return;
      /* ⚑ v59 (latences) — même texte, même plateau, même police, et la taille posée la dernière fois est toujours là : le
         titre est déjà ajusté. Sans ce garde, chaque passe (huit par ouverture d'écran) repartait de la taille de départ puis
         rétrécissait pas à pas — une mise en page forcée à chaque pas, sur tous les titres, écrans fermés compris. */
      var _cleT = ((document.fonts&&document.fonts.status)||'')+'|'+t.textContent+'|'+b.clientWidth+'|'+(b.closest('.screen,.sheet,.poster')||{}).id+'|'+getComputedStyle(t).fontFamily;
      if(t.__ajCle === _cleT && t.style.getPropertyValue('font-size') === t.__ajFs) return;
      /* ⚑ v36 (Tom : « INDEX plus gros, comme les autres ») — LA PLACE SE MESURE DANS L'UNITÉ DU TITRE. `scrollWidth` est
         en pixels de mise en page ; `getBoundingClientRect` suit la mise à l'échelle de l'appareil. Dès que l'app est
         affichée réduite (fenêtre plus petite que le téléphone), la place paraissait plus étroite qu'elle n'est et les
         titres longs rétrécissaient : mesuré à l'échelle 0,72, Index, Réglages et L'aura à 23 px, Fil à 31. */
      var kE=(b.offsetWidth>0)?(r.width/b.offsetWidth):1; if(!(kE>0)) kE=1;
      var cs=getComputedStyle(b);
      var dispo=r.width/kE-parseFloat(cs.paddingLeft||0)-parseFloat(cs.paddingRight||0);
      var cb=b.querySelector('.closeb');
      if(cb) dispo-=cb.getBoundingClientRect().width/kE+18;
      /* ⚑ 8 · GILBERT REMONTE D'UN CRAN (Tom, 18 septembre 2026). Le départ passe de 27 à 33
         et le plancher de 19 à 23 : ×1,217, le facteur MESURÉ au canevas (Gilbert rend 21,7 %
         plus étroit que la face qu'il remplace, médiane sur sept chaînes réelles).
         La boucle d'ajustement ne change pas : le titre s'ajuste toujours, il ne se rogne pas. */
      var fs=33, plancher=23;
      /* ⚑ UN TITRE EN PromiLate PART DE 27 (Tom, 18 sept. 2026) : c'est la cote des dessins qu'il
         remplace — capitale 0,700 em × 27 = 18,9. Le 33 ci-dessus est celui de Gilbert. */
      /* ⚑ 23 SEPTEMBRE 2026, second tour (Tom) — « GROSSIS-LES. » Le départ passe de **27
         à 31**. C'est ICI que ça se décide, et nulle part ailleurs : `ajusteTitres` est le SEUL
         propriétaire de la taille d'un titre de plateau — il la pose en ligne avec `important`,
         donc toute règle de feuille perd contre lui (§8, « la taille qu'on LIT n'est écrite par
         aucune règle » ; je l'ai repayé en écrivant d'abord du CSS, qui n'a rien peint).
         ET LA BOUCLE D'AJUSTEMENT FAIT LE RESTE : chaque titre prend la plus grande taille que
         SON plateau autorise, `dispo` étant déjà la largeur moins ✕ FERMER et 18 px d'air.
         Mesuré après : Index 31 · Réglages 31 · L'aura 31 · Fil 31 · Partager 29 · Le Studio 28
         — les deux derniers sont les plus longs, et c'est leur plateau qui les borne, pas un
         choix. Aucun ne touche ✕ FERMER : c'est la boucle qui le garantit, au pixel. */
      if(/^\s*["']?PromiLate/i.test(getComputedStyle(t).fontFamily)){ fs=t.classList.contains('cs-mark')?29:31; plancher=19; }
      /* ⚑ v20 (Tom, 22 sept.) — « Partager, Réglages, Index et L'aura sont trop petits à côté du Studio et de
         Fil. Ce n'est pas l'air, c'est la taille des caractères. » Mesuré : en PIXELS ils ne le sont pas (29 ·
         31 · 31 · 31 contre 27 et 31) — c'est l'ŒIL : « Le Studio » et « Fil » sont faits de lettres à hampe,
         les quatre autres surtout de minuscules basses. Ces quatre-là partent donc de 35, et l'air devant
         ✕ FERMER passe de 18 à 16 : la boucle leur donne la plus grande
         taille que LEUR plateau autorise. Studio et Fil ne bougent pas. */
      var _v20 = !!b.closest('#shareScreen,#settingsScreen,#indexSheet,#auraScreen') && !t.classList.contains('cs-mark')
                 && /^\s*["']?PromiLate/i.test(getComputedStyle(t).fontFamily);
      if(_v20){ fs=35; if(cb) dispo+=2; }   /* air 16 : à 12, « Réglages » venait à 8 px du ✕ à l'œil */
      /* ⚠ EN `important`, sinon la règle d'origine du titre reprend la main : un style
         en ligne SANS important perd contre un `!important` de feuille. */
      t.style.setProperty('font-size',fs+'px','important');
      /* ⚑ 1 · ET LA BOÎTE SUIT LA POLICE. Mesuré : « Réglages » en Gilbert 27 dans une boîte de
         27 px — les glyphes en demandent 27,5 (montée 18,9 + descente 8,6), le jambage du « g »
         était coupé de 3,2 px. Une hauteur figée en px ne survit pas à un changement de police :
         on la pose en EM, ici même, où la taille est décidée (§8, « une cote dérivée n'est pas
         un espace »). */
      t.style.setProperty('line-height','1.06em','important');
      t.style.setProperty('height','auto','important');
      t.style.setProperty('padding-bottom','1px','important');
      for(var i=0;i<12;i++){
        if(t.scrollWidth<=dispo+0.5) break;
        fs-=1; if(fs<plancher) break;
        t.style.setProperty('font-size',fs+'px','important');
      }
      t.__ajCle = _cleT; t.__ajFs = t.style.getPropertyValue('font-size');
    });
  }
  var _derT=-1e9, _attT=0;
  function tout(){   /* v59 : jamais deux passes à moins de 80 ms — la dernière demande est reportée, une fois */
    var t=performance.now(); if(t-_derT<80){ if(!_attT) _attT=setTimeout(function(){ _attT=0; tout(); }, 80-(t-_derT)); return; }
    _derT=t;
    try{ if(window._encartHaut) window._encartHaut(); }catch(_){ }
    try{ ajusteTitres(); }catch(_){ }
  }
  [0,180,500,1000,2000].forEach(function(d){ setTimeout(tout,d); });
  document.addEventListener('click',function(){ [120,340,700].forEach(function(d){setTimeout(function(){ (window._apresMouvement||function(f){f();})(tout); },d);}); },true);
  try{ if(document.fonts&&document.fonts.ready) document.fonts.ready.then(tout); }catch(_){}

  /* ⚠ ON SUIT L'OUVERTURE RÉELLE DES ÉCRANS, PAS DES MINUTEURS.
     C'est l'erreur de méthode que Tom a rattrapée : je vérifiais en appelant
     `_encartHaut()` et `_harmonie()` À LA MAIN et en forçant `.show` — donc je mesurais
     un état que je fabriquais. Dans le parcours réel, rien ne tournait au bon moment :
     l'encart de l'Index sortait à 54 au lieu de 40, la barre de recherche le CHEVAUCHAIT
     de 6 px, le titre restait à 38 px et la recherche gardait son bord de 3 px.
     Un observateur sur la classe `show` de chaque écran, qui COMPARE avant d'agir. */
  try{
    var _etats={};
    var _ecrans=[].slice.call(document.querySelectorAll('.screen,.sheet,.poster'));
    _ecrans.forEach(function(sc){
      if(!sc.id) return;
      _etats[sc.id]=sc.classList.contains('show');
      new MutationObserver(function(){
        var v=sc.classList.contains('show');
        if(v===_etats[sc.id]) return;         /* rien n'a changé : on ne réveille rien */
        _etats[sc.id]=v;
        if(v) [0,60,180,400,800].forEach(function(d){ setTimeout(function(){ (window._apresMouvement||function(f){f();})(tout); },d); });
      }).observe(sc,{attributes:true,attributeFilter:['class']});
    });
  }catch(_){}
  window._harmonie=tout;
  window._harmonieSonde=function(){
    return [].map.call(document.querySelectorAll('.enh'),function(b){
      var t=b.querySelector('.enh-t'); var r=b.getBoundingClientRect();
      var sc=b.closest('.screen,.sheet,.poster');
      return [(sc&&sc.id)||'?', t?t.textContent.trim().slice(0,22):'-',
              Math.round(r.width), t?getComputedStyle(t).fontSize:'-',
              t?(t.scrollWidth<=t.clientWidth+1?'tient':'DEBORDE'):'-'];
    });
  };
})();
