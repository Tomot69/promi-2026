
(function(){
  /* LE PLATEAU NE DÉFILE PAS. Aux Réglages il vivait dans `#stScroll`, le conteneur qui
     défile : posé en absolu il y aurait été rogné par son `overflow`, et il serait parti
     avec le doigt. Au Studio le plateau est un ENFANT DIRECT de l'écran — on le remet là.
     ⚠ Déplacer un nœud le sort de tout sélecteur qui le visait par sa PLACE (§8) : `.enh`
     n'est visé que par sa classe, et le §1 ci-dessus est écrit en `#device .enh`. */
  function remonte(){
    [].forEach.call(document.querySelectorAll('.enh'), function(b){
      var sc = b.closest('.screen,.sheet,.poster,.feedview');
      if(sc && b.parentElement !== sc) sc.appendChild(b);
    });
  }
  /* ⚠ §8 · UN `.screen` NE COÏNCIDE PAS AVEC `#device` — ET LA CAUSE EST STATIQUE.
     Mesuré en cotes de DISPOSITION (`offsetParent`, `offsetLeft` — insensibles aux
     transformations, contrairement à `getBoundingClientRect`) :

         #settingsScreen #auraScreen #auraHelp #indexSheet #arrangeSheet #feedView
             390 × 844, offsetParent = #device        → rien à corriger
         #langScreen #privScreen #plusScreen
             422 × 876, offsetParent = .frame         → l'appareil y est à 16, 16

     Ces trois-là ne vivent pas DANS l'appareil : ils sont frères de lui, dans le cadre.
     Un `left:24px` y tombe donc à 8 en cotes d'appareil, et un `top:40px` à 24.

     ⚠ ET C'EST POURQUOI LA VERSION PRÉCÉDENTE ÉTAIT PIRE QUE LE MAL. Elle corrigeait en
     comparant deux `getBoundingClientRect` — donc en mesurant PENDANT la transition
     d'ouverture, quand les rectangles ne veulent rien dire. Elle a écrit des cotes
     fausses en dur sur trois écrans qui étaient justes : Réglages large de 242,7 au lieu
     de 342, le Fil à x −20,7, l'Index à y −65. C'est le piège de `cale()` au Studio,
     repayé. On ne mesure donc plus une position : on lit l'offsetParent, qui est un fait
     de structure et ne bouge pas avec l'animation. */
  /* ⚠ ET LA GÉOMÉTRIE SE POSE EN LIGNE, PAS EN FEUILLE — LE PIÈGE DE SPÉCIFICITÉ DU §8.
     Aux Réglages, un crible d'écran écrase la largeur de tout enfant direct :

         #settingsScreen > :not(#stTrameCv) { width:auto!important; max-width:none!important }

     Le `:not(#stTrameCv)` compte l'id qu'il contient : ce sélecteur pèse DEUX ids, il bat
     donc `#device .enh` qui n'en a qu'un. Le plateau retombait en largeur automatique dans
     un parent en `flex`, donc à la largeur de son contenu — et comme le titre rétrécit à
     son tour pour tenir dedans, LA LARGEUR SE RECALCULAIT SUR ELLE-MÊME : 342 → 242,7 →
     209,4 d'une passe à l'autre, avec le titre qui suivait, 27 → 19. C'est la boucle du §8
     (« une cote mesurée sur elle-même fait osciller l'écran »), déclenchée cette fois par
     un crible et non par une mesure.
     La parade est celle que `.closeb` emploie déjà : un style EN LIGNE avec `important`,
     que rien dans la feuille ne peut battre. Les valeurs sont des constantes du §5 —
     aucune ne vient d'une mesure, donc rien ne peut osciller. */
  var REF = {left:24, top:40, width:342, height:60};
  function recale(){
    var dv = document.getElementById('device'); if(!dv) return;
    [].forEach.call(document.querySelectorAll('.enh'), function(b){
      var sc = b.parentElement; if(!sc) return;
      /* Les écrans frères de l'appareil (dans `.frame`) portent son décalage.
         ⚠ ON LE LIT DANS L'ARBRE, PAS DANS LA DISPOSITION. `offsetParent` vaut `null`
         tant qu'un écran est en `display:none` : le décalage n'était donc appliqué qu'à
         la PREMIÈRE ouverture passée, et la sonde lisait « x 8 · y 24 » au premier
         passage, puis 24/40 aux suivants. `contains` est vrai ou faux avant même que
         l'écran soit peint — la correction est donc posée dès le chargement. */
      var dehors = !dv.contains(sc);
      var dx = dehors ? dv.offsetLeft : 0, dy = dehors ? dv.offsetTop : 0;
      b.style.setProperty('position','absolute','important');
      b.style.setProperty('left',   (REF.left + dx) + 'px', 'important');
      b.style.setProperty('top',    (REF.top  + dy) + 'px', 'important');
      b.style.setProperty('right',  'auto', 'important');
      b.style.setProperty('bottom', 'auto', 'important');
      b.style.setProperty('width',  REF.width  + 'px', 'important');
      /* ⚑ Q213 · L'INDEX PORTE « N paroles · N Nuées » SOUS SON TITRE : son plateau fait 88 (rayon 44, h ≤ 94,5).
         `recale` est LE propriétaire de cette cote (§7) : l'exception s'écrit ici, pas dans une règle qui perdrait. */
      b.style.setProperty('height', ((sc.id === 'indexSheet') ? 88 : REF.height) + 'px', 'important');
      b.style.setProperty('max-width','none','important');
      b.style.setProperty('min-width','0','important');
      b.style.setProperty('box-sizing','border-box','important');
      b.style.setProperty('margin','0','important');
      b.style.setProperty('flex','0 0 auto','important');
    });

    /* ⚠ LE HÉROS DU CERCLE SORT DU TÉLÉPHONE — MÊME CAUSE, MÊME PARADE. `#plHeroCv` est
       un fond pleine largeur, dessiné pour son écran ; comme cet écran est le CADRE et non
       l'appareil, il déborde de 16 px à gauche et 24 à droite (mesuré au balayage). Il
       peint donc par-dessus la marge du cadre, hors du téléphone. Il prend le même
       décalage que le plateau — c'est le même fait de structure, pas une seconde règle. */
    var hero = document.getElementById('plHeroCv');
    if(hero && hero.parentElement && !dv.contains(hero.parentElement)){
      hero.style.setProperty('left', dv.offsetLeft + 'px', 'important');
      hero.style.setProperty('right','auto','important');
      hero.style.setProperty('width','390px','important');
      hero.style.setProperty('max-width','none','important');
    }
  }

  /* ⚠ LE BLOC `lot-POLICES` ÉCRIT SON COUPLE EN LIGNE, AVEC `!important` — il bat donc
     la feuille de style, si bien que « Le Cercle » restait en ApfelMid 500, la police de
     son ancien sur-titre. Le §6 prévoit ce cas : « la passe se RELIT, elle ne fige pas ».
     On retire donc SON inline sur les titres de plateau et on la laisse relire — elle
     verra Bricolage 700, qui est embarqué, et le réécrira tel quel. */
  function relitPolice(){
    [].forEach.call(document.querySelectorAll('.enh .enh-t[data-pol]'), function(t){
      t.style.removeProperty('font-family');
      t.style.removeProperty('font-weight');
      t.style.removeProperty('font-style');
      t.removeAttribute('data-pol');
    });
  }

  /* ⚠ ON CHAÎNE, ON NE COURT PAS. Le plateau est BÂTI par `lot-ENCART-HAUT`, et les deux
     lots écoutent le même événement : à la toute première ouverture d'un écran, `recale`
     passait AVANT que le nœud existe. Mesuré : « Le Fil : aucun plateau », « La langue :
     x 8 · y 24 » au premier passage, tout juste aux suivants — un défaut qui ne se voit
     qu'une fois, donc précisément celui qu'une vérification pressée déclare vert.
     On appelle donc le bâtisseur d'abord, et on repasse après lui. */
  /* ⚠ L'ENCRE DU PLATEAU D'UNE FICHE S'ÉCRIT EN LIGNE — LA FEUILLE NE PEUT PAS GAGNER.
     Un lot de fiche peint le mot de nature et le FERMER en `color: crème !important`
     DIRECTEMENT SUR LE NŒUD : c'est la clause du §3, « la zone haute et ses éléments
     gardent le traitement du moodboard sur couleur pleine ». Elle était juste tant qu'ils
     étaient posés à nu sur la bande de nature. Dans un plateau crème, elle rend le mot
     invisible — mesuré : « Promi » à `rgb(247,240,222)` sur un fond `rgb(247,240,222)`,
     largeur 74,8 px de rien du tout, et le plateau paraissait vide.
     Un style en ligne avec `important` bat toute la feuille, quelle que soit sa
     spécificité : on répond donc dans la même monnaie, et APRÈS lui — la passe est chaînée
     derrière le bâtisseur, elle parle en dernier. */
  /* ⚠ SUR L'ÉCRAN DES TROIS CHOIX, LA PAGE + N'A PAS DE PLATEAU — ET C'EST UNE DÉCISION
     QUI EXISTAIT AVANT MOI. Une règle du produit masque nommément le mot-marque, la trame
     et la grappe quand `#createSheet` porte `pp-choix` :
         #device #createSheet.pp-choix .cs-mark, … { display:none }
     Cet écran-là est nu par construction : la QUESTION (« Qu'est-ce que tu promets ? », 46 px)
     y fait titre, et rien d'autre ne doit peser. Un plateau bordé avec un titre vide — c'est
     ce que j'avais produit — y ajoute un cadre que l'écran n'a jamais eu, et la question le
     chevauchait. Le §9 est clair : on ne démasque pas ce qu'on n'a pas décidé.
     Le plateau se retire donc de CET état, et **le FERMER ressort avec lui** — sans quoi on
     perdrait la seule porte de sortie de l'écran. Aux autres étapes (la phrase, l'à-qui,
     l'échéance), le mot-marque existe et le plateau est là, comme partout. */
  function pageplus(){
    var sc = document.getElementById('createSheet'); if(!sc) return;
    var b = sc.querySelector('.enh'); if(!b) return;
    /* ⚠ ON LE CHERCHE DANS L'ÉCRAN, PAS DANS LE PLATEAU. Une fois sorti pour l'écran des
       choix, `.closeb` n'est plus DANS `.enh` : le chercher là rendait `null`, et la
       branche qui devait le faire revenir ne pouvait jamais s'exécuter. Mesuré : FERMER
       restait à y −6 dans `.cs-top`, hors cadre, à l'étape de la phrase. */
    var cb = sc.querySelector('.closeb');
    var nu = sc.classList.contains('pp-choix');
    if(nu){
      if(cb){
        var top = sc.querySelector('.cs-top') || sc;
        if(cb.parentNode !== top){
          top.insertBefore(cb, top.firstChild);
          ['position','top','right','left','bottom','width','margin','padding','transform']
            .forEach(function(k){ cb.style.removeProperty(k); });
          cb.removeAttribute('data-pose');
        }
        /* ⚠ L'ENCRE EN LIGNE D'UN AUTRE ÉCRAN NE SUIT PAS FERMER ICI (12 sept. 2026) : `enteteLisible`
           avait laissé le ✕ en crème, et le ✕ disparaissait sur la page crème. Il reprend la feuille. */
        [cb].concat([].slice.call(cb.querySelectorAll('*'))).forEach(function(n){
          ['color','-webkit-text-fill-color','stroke'].forEach(function(k){
            if(n.style.getPropertyValue(k)) n.style.removeProperty(k); }); });
      }
      b.style.setProperty('display','none','important');
    }else{
      b.style.removeProperty('display');
      /* ⚠ ET IL FAUT LE FAIRE REVENIR — `pose()` ne repasse jamais sur un plateau déjà
         bâti (« déjà posé », il sort aussitôt). Sorti une fois pour l'écran des choix, le
         FERMER restait dans `.cs-top`, mesuré à y −6 : hors cadre, donc perdu, à l'étape
         de la phrase. On le remet, avec les cotes en ligne que le §8 impose ici. */
      if(cb && cb.parentNode !== b){
        b.appendChild(cb);
        ['position:static','top:auto','right:auto','left:auto','bottom:auto',
         'width:auto','margin:0','padding:0','transform:none'].forEach(function(d){
          var i = d.indexOf(':');
          cb.style.setProperty(d.slice(0,i), d.slice(i+1), 'important');
        });
        cb.setAttribute('data-pose','enh');
      }
    }
  }

  function encreFiche(){
    ['detailPoster','createSheet'].forEach(encreUn);
    pageplus();
  }
  window._encrePlateau = function(id){ encreUn(id); };   /* v103 : la page + se montre avec son plateau déjà à l'encre (lot-ACCUEIL, revele) */
  function encreUn(id){
    var sc = document.getElementById(id); if(!sc) return;
    var b = sc.querySelector('.enh'); if(!b) return;
    var clair = !!document.querySelector('#device.light,.device.light,.frame.light');
    var encre = clair ? '#201908' : '#F7F0DE';
    /* ⚠ ET ON DESCEND DANS LES ENFANTS. Le mot « FERMER » d'une fiche ne vit pas sur
       `.closeb` : il est dans un enfant, qui porte SA propre encre en ligne. Peindre le
       parent ne l'atteint pas — vu à l'écran : le ✕ est passé à l'encre, le mot est resté
       crème sur crème. On peint donc le nœud ET sa descendance. */
    var cibles = [b.querySelector('.enh-t'), b.querySelector('.closeb')];
    var cb = b.querySelector('.closeb');
    if(cb) [].push.apply(cibles, cb.querySelectorAll('*'));
    cibles.forEach(function(n){
      if(!n || n.tagName === 'svg' || n.ownerSVGElement) return;
      n.style.setProperty('color', encre, 'important');
      n.style.setProperty('-webkit-text-fill-color', encre, 'important');
    });
  }

  /* ⚑ « GROSSIS UN PEU LE RESTE » — ET LE DOCUMENT DONNAIT DÉJÀ LE PLANCHER.
     Décision Tom, 2 septembre 2026 : « mets la même taille de police dans tous les titres
     que dans Studio — Studio actuel est la ref — grossis un peu le reste ». Les titres y
     étaient déjà (Bricolage 700 / 27, relevé sur `#stpHaut`). C'est le RESTE qui manquait,
     et le relevé dit pourquoi ça se voyait :

         Index    10px × 6      Aura      10px × 4      Le Fil    11px × 4
         Réglages 11.5px × 8    Arranger  11px × 1

     Le §6 est formel — « Tailles minimales : rien en dessous de 12 px ». Un tiers du petit
     texte du produit était SOUS son propre plancher. Ce n'est donc pas un goût, c'est une
     règle qu'on applique enfin.

     ⚠ LA LOI EST UN PLANCHER, PAS UN FACTEUR — ET C'EST LA MESURE QUI L'A DÉCIDÉ.
     J'ai d'abord posé un facteur uniforme de 1,08. `redteam_air` a répondu : **156 paires
     de textes resserrées**, dont, dans l'Index, `« planter un arbre » → « TENUE »` qui
     passe de **2 px à 0** — le titre touche sa ligne d'état, sur les six cartes et dans les
     deux thèmes.

     La cause est écrite noir sur blanc au §8, et elle vaut pour tout ce produit : **une
     carte d'Index est en cotes ABSOLUES** — `top: 124 / 141 / 174`, calculées pour les
     tailles d'alors. Un texte qui grossit ne déplace aucun `top` : c'est sa HAUTEUR qui
     grandit, vers le bas, et l'air se mange en silence. Un facteur global se bat donc
     contre toute la mise en page absolue du portage, écran par écran.

     LA LOI RETENUE : `max(13, taille)`, et seulement sous 20.
       · **le plancher, pas un facteur** — il ne touche QUE ce qui était trop petit, donc
         il ne peut resserrer que là où un texte était sous son propre minimum ;
       · **13 et non 12** : le §6 pose 12 comme minimum absolu ; 13 le respecte et donne le
         « un peu plus » demandé, sans toucher aux blocs déjà à 13, 14, 15 ;
       · le plafond 20 protège ce qui est déjà décidé — le compte du Fil et de l'Index vient
         d'y être posé, les titres sont à 27.
     Aller plus loin demande de RECALCULER les cotes absolues de chaque écran : c'est un lot
     par écran, avec son juge. Je ne l'ai pas fait ici, et je le dis.

     ⚠ ELLE SE RELIT, ELLE NE FIGE RIEN — ET J'AI DÛ LA RÉÉCRIRE POUR ÇA.
     Ma première version mémorisait la taille d'origine dans `data-t0` et calculait à partir
     d'elle. C'est faux, parce que **plusieurs tailles de ce produit sont FLUIDES** :
     `.tenir-lab` (le libellé du geste) mesure **14,403 px dans le viewport du juge et 17
     dans le mien** ; `.dpt-quand` (l'état d'une fiche) donne **13,5 à un instant et 12,5 à
     un autre**. Mémoriser, c'est GELER : la passe écrivait en pixels durs une cote qui
     devait respirer, et le juge lisait « 14,403 → 17 » — un écart que je n'avais pas
     demandé.
     Le §6 donne la marche à suivre, mot pour mot, à propos de `lot-POLICES` : « La passe se
     RELIT, elle ne fige pas : sur un élément déjà touché elle retire d'abord son propre
     inline, relit ce que la cascade dit vraiment, puis décide. » C'est exactement ce qu'on
     fait ici — on ne garde AUCUNE valeur, seulement une marque disant « c'est moi qui ai
     écrit ». */
  /* ⚑ L'ÉTAT D'UNE CARTE TIENT DANS SA CARTE — SIGNALÉ PAR TOM, CAPTURE À L'APPUI.
     Mesuré : `« 9 PROMI · 3 TENUS »` demande **180 px pour 140 disponibles**, et
     `« GARDÉ DE CÔTÉ »` 153 pour 140. Ils étaient coupés net au bord de la carte.
     ⚠ CE N'EST PAS LE PLANCHER QUI L'A FAIT : la taille lue est **16 px** et `data-ech`
     est nul — ma passe n'y a jamais touché. C'est la taille naturelle, et elle est fluide.
     Le défaut est antérieur ; il se voit d'autant mieux que le reste est propre.
     On applique donc à CES lignes-là — et à elles seules — l'arbitrage déjà en vigueur
     pour le titre du plateau : on redescend par pas de 0,5 jusqu'à ce que le mot tienne,
     **butée à 12**, le minimum absolu du §6. La passe se relit : elle retire d'abord son
     propre inline, lit la taille vraie, puis décide — une cote fluide n'est jamais gelée. */
  /* ⚑ Q158 · UN SEUL PROPRIÉTAIRE, ET IL PARLE EN DERNIER.
     Cette passe ajuste l'état d'une carte d'Index à la largeur de sa carte. Elle était
     appelée EN TÊTE de `echelle()` — donc AVANT le plancher, qui repassait derrière elle et
     retirait son inline (voir la garde `_estEtat` plus bas). Elle est maintenant appelée
     à la FIN : le plancher pose sa taille, l'ajustement la ramène dans la carte, et c'est
     ce dernier mot qui reste. Le corps de la passe n'a pas changé d'une ligne. */
  function etatsDeCarte(){
    [].forEach.call(document.querySelectorAll('.s4-carte .s4-et'), function(n){
      /* ⚠ ON NE DÉFAIT RIEN TANT QU'ON NE PEUT PAS REDÉCIDER. La passe retirait son
         propre inline AVANT de vérifier que la carte est disposée : appelée pendant que
         l'Index est fermé (`clientWidth` 0), elle rendait le mot à sa taille NATURELLE de
         16 px et sortait aussitôt — sans jamais le réajuster. Mesuré en rejouant la
         séquence de `redteam_air`, qui enchaîne 15 écrans sur une seule page :
         « 9 PROMI · 3 TENUS » à 12,5 px au passage sombre, à **16 px** au passage clair,
         et l'air sous « le potager » tombait de 5,5 à 2. Le défaut est latent — il ne
         dépend que du moment où la passe tombe — et c'est la même famille que le §7 :
         un traitement qui se relit doit d'abord s'assurer qu'il a de quoi lire. */
      if(!n.clientWidth) return;
      if(n.hasAttribute('data-fit')){ n.style.removeProperty('font-size'); n.removeAttribute('data-fit');
        if(n.hasAttribute('data-fit-ls')){ n.style.removeProperty('letter-spacing'); n.removeAttribute('data-fit-ls'); }
        if(!n.clientWidth) return; }
      var t = parseFloat(getComputedStyle(n).fontSize);
      if(!t || n.scrollWidth <= n.clientWidth + 1) return;
      var g = 0;
      while(n.scrollWidth > n.clientWidth + 1 && t > 12 && g++ < 16){
        t -= 0.5;
        n.style.setProperty('font-size', t + 'px', 'important');
      }
      /* ⚑ 16 sept. 2026 — la butée de 12 est le plancher du §6 : on ne descend pas dessous.
         S'il faut encore gagner, c'est l'INTERLETTRE qui cède, par pas de 0,01em, bornée à
         .12em. Relevé : « 9 PROMI · 3 TENUS » en Atkinson, 144,2 px d'encre pour 140 de boîte. */
      if(n.scrollWidth > n.clientWidth + 1){
        var em = parseFloat(getComputedStyle(n).letterSpacing) / t;
        if(!isFinite(em)) em = 0.18;
        var h = 0;
        while(n.scrollWidth > n.clientWidth + 1 && em > 0.12 && h++ < 12){
          em -= 0.01;
          n.style.setProperty('letter-spacing', em.toFixed(3) + 'em', 'important');
        }
        n.setAttribute('data-fit-ls', '1');
      }
      n.setAttribute('data-fit', '1');
    });
  }

  /* ⚑ ON REPASSE DERRIÈRE LE MOTEUR DE L'INDEX, ON N'ATTEND PAS UN MINUTEUR (§8).
     L'ajustement des états de carte dépend de `clientWidth` : il vaut 197 sur une mise en
     page large, 140 à deux par ligne, 90 à trois. `_s4Index()` REMET L'INDEX EN PAGE — si
     la passe ne repasse pas derrière lui, un mot ajusté pour 197 reste à 16 px dans une
     carte de 140, et l'air sous le titre tombe de 5,5 à 2. C'est ce qui faisait osciller
     `redteam_air` d'un passage à l'autre, vert puis rouge puis vert, après même que la
     passe eut été rendue idempotente. On enveloppe, on n'écoute pas : c'est le piège
     « une mise en page posée par un lot est défaite sans qu'on y touche ». */
  try{
    var _s4o = window._s4Index;
    if(_s4o && !_s4o._ech) {
      var _w = function(){ var r = _s4o.apply(this, arguments);
        try{ requestAnimationFrame(function(){ etatsDeCarte(); }); }catch(_){}
        return r; };
      _w._ech = true; window._s4Index = _w;
    }
  }catch(_){}
  function echelle(){
    var ecrans = document.querySelectorAll('.screen,.sheet,.poster,.feedview');
    var _dv = document.getElementById('device'), _dr = _dv ? _dv.getBoundingClientRect() : null;
    [].forEach.call(ecrans, function(sc){
      var r = sc.getBoundingClientRect();
      if(r.width < 10 || r.height < 10) return;          /* écran fermé : on ne mesure pas */
      /* ⚑ v89 — un écran FERMÉ n'a pas une boîte nulle : il est glissé hors champ (§8). La passe les reprenait tous, nœud par nœud
         (retirer, relire la cascade, reposer) : 51 ms sous WebKit à chaque passe, lancée en plein mouvement au Studio — Madrure en
         saccadait. On ne traite que ce qui recouvre l'appareil ; un écran se traite à son ouverture (la passe suit sa classe). */
      if(_dr && (r.bottom <= _dr.top + 2 || r.top >= _dr.bottom - 2 || r.right <= _dr.left + 2 || r.left >= _dr.right - 2)) return;
      [].forEach.call(sc.querySelectorAll('*'), function(n){
        /* ⚑ UN SEUL PROPRIÉTAIRE PAR PROPRIÉTÉ — Q158, la vraie cause.
           `etatsDeCarte` ajuste l'état d'une carte d'Index à la largeur de sa carte, et
           il respecte déjà le plancher de 12 du §6. Le plancher général, lui, marquait ces
           mêmes nœuds de `data-ech` dès que l'ajustement descendait sous 13 — et au
           passage suivant il RETIRAIT un inline qu'il n'avait pas écrit : le mot revenait
           à sa taille naturelle de 16 px, la relecture le trouvait au-dessus du plancher,
           et plus personne ne le réajustait.
           C'est ce qui faisait osciller `redteam_air` — vert, rouge, vert — et qui a résisté
           à trois correctifs successifs (la passe rendue idempotente, le moteur de l'Index
           enveloppé, un observateur de largeur) : aucun ne pouvait rien, puisque le
           défaut n'était pas dans la passe mais dans CELLE D'À CÔTÉ.
           Mesuré : `inline:'-'` avec `data-fs0:'16'` et `data-cw:'140'` — un ajustement
           calculé, puis effacé par un tiers.
           L'état d'une carte n'appartient donc qu'à `etatsDeCarte`. Même forme que les deux
           exclusions déjà là (`.np-carte`, `.enh`), et posée AVANT le retrait. */
        var _estEtat = n.classList && n.classList.contains('s4-et') && !!n.closest('.s4-carte');
        var mien = n.hasAttribute('data-ech');
        /* on retire d'abord SA PROPRE trace, pour relire ce que la cascade dit vraiment —
           ⚠ SAUF SUR L'ÉTAT D'UNE CARTE, dont l'inline appartient à `etatsDeCarte`.
           Le retrait le rendait à sa taille de feuille, 16 px ; la relecture le trouvait
           alors AU-DESSUS du plancher et sortait aussitôt, laissant un mot de 180 px dans
           une carte de 140. C'est la vraie cause de l'oscillation de `redteam_air`, et
           elle a résisté à trois correctifs qui visaient tous la mauvaise passe.
           ⚠ ON NE SAUTE QUE LE RETRAIT, PAS LE TRAITEMENT. Ma première version sortait
           d'emblée sur ces nœuds : le plancher ne s'appliquait plus, et `releve-S4` est
           passé de 0 à 34 écarts — des états à 6,4 · 10 · 11 px, sous le minimum du §6.
           Le plancher reste ; c'est le retrait qui s'arrête à la porte. */
        if(mien && !_estEtat){ n.style.removeProperty('font-size'); n.removeAttribute('data-ech'); }
        /* ⚠ LA CARTE DU PEAUFINER D'UNE NUÉE A UNE HAUTEUR QUI NE BOUGE PAS. Son
           « visibles par les membres » est cloué en absolu au bas d'une boîte de 104 px ;
           tout ce qui grossit au-dessus vient le toucher — mesuré, l'écart tombait de
           5 px à −1. Ses textes gardent donc leur taille : le plancher s'arrête à sa porte. */
        if(n.closest('.np-carte')) return;
        if(n.closest('.enh')) return;                    /* le plateau porte la référence */
        if(n.tagName === 'svg' || n.ownerSVGElement) return;
        var propre = [].some.call(n.childNodes, function(x){
          return x.nodeType === 3 && x.textContent.trim(); });
        if(!propre) return;
        var t = parseFloat(getComputedStyle(n).fontSize);
        /* ⚠ SUR UNE CARTE ÉTROITE, LE PLANCHER EST 12 ET NON 13 — sinon il écrase la
           hiérarchie. Mesuré par le juge S4 sur l'Index à TROIS cartes par ligne (106 px de
           large) : le titre y vaut 12,9 et l'état montait à 13 — l'état devenait plus gros
           que le titre qu'il accompagne. 12 est le minimum absolu du §6 ; il laisse au titre
           les neuf dixièmes de point qui disent lequel des deux commande. */
        var etroite = !!n.closest('.s4-carte') && n.closest('.s4-carte').getBoundingClientRect().width < 120;
        var sol = etroite ? 12 : 13;
        if(!t || t >= sol) return;       /* déjà au-dessus du plancher : on n'y touche pas */
        var t1 = sol;
        n.style.setProperty('font-size', t1 + 'px', 'important');
        n.setAttribute('data-ech', '1');
        /* ⚠ ET SI LE MOT NE TIENT PLUS, IL REDESCEND — JAMAIS SOUS LE PLANCHER DU §6.
           Une carte d'Index a une largeur utile FIXE de 140 px. « 9 PROMI · 3 TENUS »,
           passé de 10 à 13, demandait 146 : il était coupé net au bord de la carte, sur la
           seule carte de Nuée. Repli par pas de 0,5, avec 12 pour butée — le minimum absolu
           du §6, jamais franchi. */
        if(n.clientWidth > 0){
          var g = 0;
          while(n.scrollWidth > n.clientWidth + 1 && t1 > 12 && g++ < 6){
            t1 -= 0.5;
            n.style.setProperty('font-size', t1 + 'px', 'important');
          }
        }
        /* ⚠ ET IL REDESCEND AUSSI S'IL TOUCHE SON VOISIN DU DESSOUS.
           Mesuré dans le Peaufiner d'une Nuée : « écris un mot… » grossi de 12,5 à 13
           passait de **4,5 px d'écart à −0,5** avec « visibles par les membres » — donc un
           CHEVAUCHEMENT, pas un resserrement. C'est encore le §8 : la boîte grandit vers le
           bas, le `top` du voisin ne bouge pas. Un texte qui se lit mal parce qu'il est
           petit vaut mieux qu'un texte illisible parce qu'il en recouvre un autre : on
           redescend, même pas et même butée à 12. */
        var vs = n.nextElementSibling;
        while(vs && vs.getBoundingClientRect().height < 1) vs = vs.nextElementSibling;
        /* ⚠ UN VOISIN « À CÔTÉ » N'EST PAS UN VOISIN « DESSOUS » — décision Tom, 3 sept. 2026.
           Ce repli protège un texte qui, en grossissant, viendrait RECOUVRIR le bloc placé
           SOUS lui. Sur une RANGÉE (`display:flex` en ligne), le frère suivant est à CÔTÉ :
           les deux boîtes se chevauchent verticalement par construction, la condition est
           donc vraie d'emblée, et le repli s'enclenche pour rien — il redescend le texte
           jusqu'à sa butée de 12 sans qu'aucun recouvrement n'existe.
           Mesuré sur Peaufiner : les CINQ libellés de rangée (`.s2-lab` d'un `.s2-reg`)
           sortaient à **12** — le plancher les avait bien posés à 13, ce repli les reprenait —
           quand NOTE et COMMENTAIRES, eux dans une ZONE (pile verticale), gardaient **13**.
           Sept libellés de même nature, deux tailles : c'est le défaut que `releve-S2 · style 12`
           montrait depuis deux passes, et le juge le lisait comme « 11,5 attendu ».
           LA GARDE : le frère ne compte comme « dessous » que s'il COMMENCE dans la moitié
           basse de notre propre boîte, ou plus bas. Une pile verticale passe (son haut est à
           notre bas ou en dessous) ; une rangée ne passe pas. Le test est géométrique, pas
           une classe : il vaut pour toute mise en page. Relevé : 24 nœuds du produit étaient
           retenus à 12 par ce repli sans voisin dessous. */
        if(vs){
          var _a0 = n.getBoundingClientRect(), _b0 = vs.getBoundingClientRect();
          if(!(_b0.top >= _a0.bottom - _a0.height * 0.5)) vs = null;
        }
        if(vs){
          var h = 0;
          while(t1 > 12 && h++ < 6 &&
                n.getBoundingClientRect().bottom > vs.getBoundingClientRect().top - 1){
            t1 -= 0.5;
            n.style.setProperty('font-size', t1 + 'px', 'important');
          }
        }
      });
    });
    /* ⚑ ET L'AJUSTEMENT DES ÉTATS PARLE EN DERNIER (Q158). Le plancher pose sa taille,
       l'ajustement la ramène dans la carte : le dernier mot revient à celui qui connaît la
       largeur. Appelé en tête, comme il l'était, il se faisait effacer par la boucle
       ci-dessus — `redteam_air` oscillait, vert puis rouge, et `releve-S4` sortait des
       états à 16 px dans une carte de 140. */
    etatsDeCarte();
  }

  /* ⚑ LE PLATEAU NE PART JAMAIS AVEC LE DOIGT — décision prise le 2 septembre 2026, Tom
     m'ayant laissé trancher. Sur six écrans il tenait, sur trois il partait : Aura,
     Comprendre ton Aura et Le Cercle sont **leur propre conteneur de défilement**, et un
     enfant en `position:absolute` d'un conteneur qui défile s'en va avec son contenu.
     Mesuré : le plateau tombait de 40 à **−360**, et « ✕ FERMER » avec lui — la seule
     porte de sortie de l'écran, hors du pouce.
     Un élément commun qui reste ici et part là n'est pas commun : le Studio et l'Index
     font référence, ils le gardent fixe. Donc il reste, partout.

     ⚠ `position:fixed` NE MARCHE PAS ICI — mesuré, il tombe à −360 pareil : ces écrans
     portent une transformation, qui devient le bloc englobant de tout `fixed` qu'ils
     contiennent. On compense donc le défilement : le plateau se translate d'exactement ce
     que le doigt a fait défiler. Ce n'est pas une cote dérivée d'une géométrie (le §8) —
     le défilement ne dépend pas de la position du plateau, il n'y a pas de boucle.

     ⚠ ET IL FAUT PROTÉGER LA BANDE AU-DESSUS. Le plateau commence à 40 : sans rien, le
     contenu remonterait dans les quarante premiers pixels et se lirait par-dessus lui.
     C'est le défaut qu'on a déjà corrigé aux Réglages, où la parade était le conteneur
     qui commence sous le plateau. Ici l'écran EST le conteneur : on pose donc un aplat du
     FOND DE L'ÉCRAN, haut de 40, sous le plateau et au-dessus du contenu. Ce n'est pas une
     forme inventée (§9) — c'est le fond de l'écran, à sa place, prolongé. */
  /* ⚠ ON PARCOURT LES PLATEAUX, PAS UNE LISTE D'ÉCRANS. Ma première version énumérait
     cinq id : le Fil n'y était pas, et son plateau tombait de 40 à 24. Une liste écrite à
     la main oublie toujours quelqu'un — on part du plateau et on remonte à son écran. */
  function suitLeDoigt(){
    [].forEach.call(document.querySelectorAll('.enh'), function(b){
      var sc = b.parentElement; if(!sc) return;
      var cs = getComputedStyle(sc);
      var propre = (cs.overflowY === 'auto' || cs.overflowY === 'scroll');
      if(!propre || sc.scrollHeight <= sc.clientHeight + 4){
        b.style.removeProperty('transform');
        var v0 = sc.querySelector(':scope > .enh-voile'); if(v0) v0.style.display = 'none';
        return;
      }
      var y = sc.scrollTop || 0;
      b.style.setProperty('transform', 'translateY(' + y + 'px)', 'important');
      /* ⚠ LE VOILE NE VA QUE LÀ OÙ IL SERT — TROIS ÉCRANS, NOMMÉMENT.
         Généralisé à tous les plateaux, il a fait tomber `redteam_tonsurton` de **26/26 à
         22/26** : mesuré sur la sauvegarde d'avant ce lot, puis sur celle d'avant les
         contours — vert dans les deux cas, donc la régression est bien de moi. Le Fil, lui,
         fait défiler sa LISTE (`#feedList`, posée à 212) et non son écran : rien n'y remonte
         jamais au-dessus du plateau, et un aplat de plus n'y protège rien — il perturbe.
         Le déplacement du plateau, lui, reste général : c'est le voile qu'on borne. */
      if(['auraScreen','auraHelp','plusScreen'].indexOf(sc.id) < 0){
        var vx = sc.querySelector(':scope > .enh-voile'); if(vx) vx.style.display = 'none';
        return;
      }
      var v = sc.querySelector(':scope > .enh-voile');
      if(!v){
        v = document.createElement('div');
        v.className = 'enh-voile';
        v.setAttribute('aria-hidden','true');
        sc.appendChild(v);
      }
      v.style.display = 'block';
      v.style.background = cs.backgroundColor;
      /* ⚠ LE VOILE PORTE LE MÊME DÉCALAGE QUE LE PLATEAU. Les écrans frères de l'appareil
         (dans `.frame`) commencent 16 px plus haut : mesuré sur Le Cercle, le voile sortait
         à **−16 → 24** au lieu de 0 → 40 — il protégeait donc au-dessus du téléphone et
         laissait seize pixels à découvert sous lui. Même fait de structure, même correction
         que `recale()`. */
      var _dv = document.getElementById('device');
      var _dh = (_dv && !_dv.contains(sc)) ? _dv.offsetTop : 0;
      v.style.setProperty('top', _dh + 'px', 'important');
      v.style.setProperty('transform', 'translateY(' + y + 'px)', 'important');
    });
  }
  /* un écouteur par écran, passif, replacé sur la frame suivante */
  var _att2 = false;
  function _surDefile(){ if(_att2) return; _att2 = true;
    requestAnimationFrame(function(){ _att2 = false; suitLeDoigt(); }); }
  function brancheDefile(){
    [].forEach.call(document.querySelectorAll('.enh'), function(b){
      var sc = b.parentElement; if(!sc || sc.__defile) return;
      sc.__defile = 1;
      sc.addEventListener('scroll', _surDefile, {passive:true});
    });
  }
  [0,300,1200].forEach(function(d){ setTimeout(brancheDefile,d); });

  /* ⚑ v59 (latences) — la passe était demandée par le clic (+120, +420 ms) ET par le changement de classe de l'écran (+90,
     +420 ms) : deux passes complètes à 30 ms d'écart, puis deux autres ensemble. Elles sont FUSIONNÉES : jamais deux passes à
     moins de 100 ms ; une demande qui tombe dans cet intervalle est reportée à sa fin, une seule fois. */
  var _derP = -1e9, _attP = 0;
  function passe(){
    var t = performance.now();
    if(t - _derP < 100){ if(!_attP) _attP = setTimeout(function(){ _attP = 0; passe(); }, 100 - (t - _derP)); return; }
    _derP = t;
    passeVraie();
  }
  function passeVraie(){
    var _T=window._passeT, _c=function(n,f){ var t=performance.now(); f(); if(_T) _T[n]=(_T[n]||0)+performance.now()-t; };
    try{ if(window._encartHaut) _c('encart',window._encartHaut); }catch(_){ }
    _c('remonte',remonte); _c('police',relitPolice); _c('recale',recale); _c('encre',encreFiche); _c('echelle',echelle);
    _c('defile',brancheDefile); _c('doigt',suitLeDoigt);
    /* ⚠ ET ON REND LA MAIN AU LOT QUI DIMENSIONNE LES TITRES. Rappeler le bâtisseur
       repose le titre dans sa taille d'origine — le Fil est reparti à 38 px dès que
       `passe()` a commencé à l'appeler. La taille du plateau est décidée par
       `ajusteTitres` (27, puis rétréci s'il ne tient pas) : c'est donc lui qui doit
       parler EN DERNIER. */
    try{ if(window._harmonie) window._harmonie(); }catch(_){ }
  }
  [0,150,450,1000,2000].forEach(function(d){ setTimeout(passe,d); });
  /* v22 — la partie légère (constantes, aucune mesure) : appelée IMAGE PAR IMAGE à l'ouverture d'un écran (lot du plateau) */
  window._plateauRecale = function(){ remonte(); recale(); };
  window.addEventListener('resize', function(){ setTimeout(recale,60); });
  document.addEventListener('click', function(){ [120,420].forEach(function(d){ setTimeout(function(){ (window._apresMouvement||function(f){f();})(passe); },d); }); }, true);
  try{ if(document.fonts&&document.fonts.ready) document.fonts.ready.then(passe); }catch(_){}

  /* ⚠ UN CORRECTIF QUI DÉPEND DU DOIGT N'EST PAS UN CORRECTIF. Accroché au seul clic, le
     recalage ne tournait pas quand un écran s'ouvre par le code — et c'est ainsi que la
     sonde l'a pris en défaut : « x 8 · y 24 » sur les trois écrans gonflés, inchangés.
     On écoute donc l'ÉTAT de chaque écran, comme le fait déjà l'encart.
     ⚠ §8 · L'OBSERVATEUR COMPARE AVANT D'AGIR : `passe()` écrit des attributs de style,
     ce qui réveillerait un observateur qui ne filtrerait pas — on ne regarde que `class`,
     et on ne relance que si la classe a VRAIMENT changé. */
  var _vus = new WeakMap(), _att = 0;
  function surveille(){
    [].forEach.call(document.querySelectorAll('.screen,.sheet,.poster,.feedview'), function(sc){
      if(_vus.has(sc)) return;
      _vus.set(sc, sc.className);
      new MutationObserver(function(){
        var c = sc.className;
        if(c === _vus.get(sc)) return;      /* comparer avant d'agir */
        _vus.set(sc, c);
        clearTimeout(_att);
        _att = setTimeout(function(){ (window._apresMouvement||function(f){f();})(passe); }, 90);
        setTimeout(function(){ (window._apresMouvement||function(f){f();})(passe); }, 420);   /* après le bâtisseur, quoi qu'il arrive — v60 : jamais pendant l'arrivée d'une dalle */
      }).observe(sc, {attributes:true, attributeFilter:['class']});
    });
  }
  [0,300,1200].forEach(function(d){ setTimeout(surveille,d); });

  /* ⚠ UNE LISTE QUI SE RECONSTRUIT NE CHANGE AUCUNE CLASSE — donc rien ne réveillait la
     passe. Mesuré par le juge S4 : à trois cartes par ligne, l'état sortait à **6,4 px**,
     très sous le plancher de 12 du §6, alors que la même vue ouverte à la main donne 12-13.
     Ce n'était pas un défaut de règle mais une COURSE : `ouvrirIndex()` reconstruit
     `#indexList` après coup, sans toucher à l'écran.
     ⚠ ET L'OBSERVATEUR NE SE RÉVEILLE PAS LUI-MÊME (§8) : la passe écrit des styles EN
     LIGNE, jamais des enfants — on n'observe que `childList`, donc elle ne peut pas se
     rappeler elle-même. */
  var _attL = 0;
  function surveilleListes(){
    ['indexList','feedList'].forEach(function(id){
      var l = document.getElementById(id); if(!l || l.__obsL) return;
      l.__obsL = 1;
      new MutationObserver(function(){
        clearTimeout(_attL);
        _attL = setTimeout(function(){ echelle(); etatsDeCarte(); }, 60);
      }).observe(l, {childList:true, subtree:true});
    });
  }
  [0,300,1200].forEach(function(d){ setTimeout(surveilleListes,d); });

  window._plateauPartout = passe;
})();
