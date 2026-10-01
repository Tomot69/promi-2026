
(function(){
  /* ⚠ LA LISTE EST NOMMÉE, ÉCRAN PAR ÉCRAN — jamais un balayage par famille (§8 : « un
     crible posé EN BLOC casse ce qu'un geste ouvre »). Chaque entrée dit son titre. */
  var MOITIE_1 = [
    ['#settingsScreen', 'h1.scr-ti'],
    ['#shareScreen',    'h2.scr-t'],
    /* ⚠ LE FIL, C'EST `#feedView` — PAS `#feedScreen`. Je m'étais trompé d'écran :
       `#feedScreen` porte bien un `h1` « Fil d'actu », mais il ne s'affiche JAMAIS
       (`show` toujours faux). Le Fil qu'on voit est `#feedView`, avec la classe `.s4`,
       son titre `h2.fd-h2.scr-ti` (« Fil » + son compteur) et son propre `#fdClose`.
       Conséquence du sous-entendu : mes règles de grammaire visaient bien `#feedView.s4`
       — la barre y était déjà passée à 124 et la liste à 212 — mais **sans encart**, ce
       qui laissait un trou de 16 px en haut. On corrige la liste, pas les cotes. */
    ['#feedView',       'h2.fd-h2'],
    ['#feedScreen',     'h1'],
    ['#auraScreen',     'h2.scr-t'],
    ['#indexSheet',     'h2.scr-ti'],
    ['#arrangeSheet',   'h2'],
    ['#auraHelp',       'h2.ah-head'],
    ['#langScreen',     'h2'],

    /* ── SECONDE MOITIÉ ────────────────────────────────────────────────────────
       ⚠ TROIS ÉCRANS SUR SEPT, ET C'EST DÉLIBÉRÉ. Les quatre autres n'ont pas la
       même grammaire, et les forcer casserait des compositions mesurées :
         · #personSheet   le titre vit DANS `.ps-head`, une rangée flex avec l'avatar —
                          y insérer un plateau brise la rangée ;
         · #previewScreen n'a pas de titre en haut du tout (le sien est en bas, sous
                          l'aperçu) ;
         · #createSheet   la page + porte le mot-marque du §5 dans `.cs-top`, et sa
                          composition est celle que `releve-S3-page-plus` mesure ;
       ⚠ ET J'AVAIS ÉCRIT ICI UNE CHOSE FAUSSE SUR LA FICHE — « elle n'a aucun nœud de
       mot-marque dans son DOM ». Elle en a un : **`.dpt-nat`**, qui porte le NOM DE LA
       NATURE — « Promi », « Chiche » — en Fraunces 600 / 27, à y 38, avec « FERMER » à
       x 282, y 38. C'est très exactement le contenu d'un plateau, à la bonne taille et
       presque à la bonne place. Ce qui lui manquait n'était pas le mot : c'était LA BOÎTE.
       Elle rejoint donc la liste (décision Tom, 2 septembre 2026).
       Les trois autres demandent chacun leur lot, avec leur juge. Les forcer ici, c'est
       exactement le « crible posé en bloc » que le §8 interdit. */
    ['#privScreen',     'h2.scr-t'],
    ['#aboutScreen',    'h2.scr-t'],
    ['#legalScreen',    'h2.scr-t'],
    ['#notifScreen',    'h2.scr-t'],   /* v109 */
    ['#essaimSheet',    'h2#esTitle'],
    ['#plusScreen',     '.pl-eb'],
    ['#detailPoster',   '.dpt-nat'],
    /* ⚠ LA PAGE D'UNE PERSONNE — le nom EST le nom de l'écran. Elle avait déjà son
       « ✕ Fermer » à y 38, en ApfelMid 12 : la bonne place et la bonne taille. Ce qui
       manquait, comme ailleurs, c'était la boîte. Le modèle est celui du Cercle : le
       plateau porte le nom de l'écran, l'avatar et « votre harmonie » restent dessous. */
    ['#personSheet',    '#psName'],
    /* ⚠ LA PAGE + AUSSI — décision Tom, 2 septembre 2026 : « page + à intelligemment
       intégrer ». Elle a DÉJÀ son mot-marque, `.cs-mark` (« Promi », Fraunces 600 / 29),
       et son FERMER — mais mesuré, le mot-marque est **à x −20, y −44 : hors cadre**.
       Seul « FERMER » se voyait, tout seul en haut à droite. Le plateau le ramène à sa
       place et lui rend son voisin. */
    ['#createSheet',    '.cs-mark']
  ];

  /* ⚠ ON NE MESURE JAMAIS UN ÉCRAN HORS CHAMP. Un `.screen` fermé est translaté sous
     l'appareil : ses rectangles sont ceux d'un ailleurs. Mesurée là, la compensation est
     fausse — vu sur Réglages : marge basse de **+52 px**, tout le contenu poussé hors du
     cadre, et `redteam_air` qui perdait **56 paires**. Un contrôle qui mesure moins n'est
     pas vert, il est aveugle. C'est exactement le piège de `cale()` sur le Studio, et la
     parade est la même : on ne pose et on n'ajuste que sur un écran VISIBLE. */
  /* ⚠ ON NE DEVINE PAS LA VISIBILITÉ PAR UNE CLASSE. Je testais `show` — mais le Fil,
     lui, s'ouvre avec `in` (`#feedView` porte `feedview tuto-fond tf-fil in s4`). Résultat :
     l'encart ne s'y posait pas, alors que la grammaire de sa barre, elle, s'appliquait —
     donc la colonne descendait de 16 px sans que le plateau soit là. Un trou.
     On mesure la géométrie : l'écran est visible s'il occupe vraiment la place de
     l'appareil. Aucune classe à connaître, aucun écran à oublier. */
  function visible(sc){
    try{
      var cs = getComputedStyle(sc);
      /* v103 — une page + TENUE CACHÉE le temps de se composer (`acc-passe`, lot-ACCUEIL) est ouverte : son plateau se
         pose pendant qu'elle est cachée, sinon il naissait à l'instant où elle se montre, vide (~90 ms sans encre). */
      var tenue = sc.classList.contains('acc-passe') && sc.classList.contains('show');
      if(cs.display === 'none' || (cs.visibility === 'hidden' && !tenue)) return false;
      if(parseFloat(cs.opacity || 1) < 0.05 && !tenue) return false;
      var r = sc.getBoundingClientRect();
      if(r.width < 40 || r.height < 40) return false;
      var d = document.getElementById('device');
      if(d){ var b = d.getBoundingClientRect();
        /* ⚑ v21 — ON POSE DÈS QUE L'ÉCRAN ENTRE : attendre la fin du glissement laissait voir l'ancien titre nu,
           puis le plateau sauter à sa place (film des Réglages : titre nu 290 → 450 ms, saut de 46 px à 700 ms).
           Les cotes mesurées par `pose` sont RELATIVES (titre et voisin glissent ensemble) : la transition n'y
           change rien. On garde seulement « l'écran est bien là » : ouvert, pas glissé hors du cadre. */
        var ov = Math.min(r.bottom, b.bottom) - Math.max(r.top, b.top);
        if(ov < 1 && !sc.classList.contains('show') && !sc.classList.contains('in')) return false;
      }
      return true;
    }catch(e){ return false; }
  }

  function pose(sel, tsel){
    var sc = document.querySelector(sel); if(!sc) return false;
    if(!visible(sc)) return false;
    if(sc.querySelector('.enh')) return true;               /* déjà posé */
    /* ⚠ LE TITRE N'EST PAS TOUJOURS UN ENFANT DIRECT. Sur Réglages il vit dans
       `#stScroll`, sur Partager dans `.sh-top` — deux conteneurs posés par des lots
       antérieurs. On le cherche donc où qu'il soit, et on pose le plateau À SA PLACE,
       dans SON parent : le flux local est préservé, quel que soit l'emboîtement. */
    var t  = sc.querySelector(tsel); if(!t) return false;
    var cb = sc.querySelector('.closeb');

    /* ⚠ ON VISE LE VOISIN SUIVANT, PAS LA HAUTEUR DU TITRE. Rendre au flux la hauteur du
       titre ne suffit pas : le plateau CENTRE le titre verticalement, donc le contenu du
       titre lui-même se décale, et tout ce qui suit avec. `redteam_air` l'a vu — 1,5 px
       de resserrement sur l'Index, entre le compteur et « à Rachel ». On mémorise donc
       l'ORDONNÉE du premier élément qui suit, et on règle la marge pour qu'il y revienne
       exactement. C'est ce que la batterie mesure, donc c'est ce qu'on vise. */
    var nx = t.nextElementSibling;
    while(nx && nx.getBoundingClientRect().height < 1) nx = nx.nextElementSibling;
    /* ⚠ ON PRÉSERVE L'ÉCART, PAS LA POSITION. Ma première compensation ramenait le voisin
       à SON ancienne ordonnée — mais le plateau fait 60 px là où le titre en faisait 40 :
       il descendait donc PLUS BAS que le titre et recouvrait un voisin resté en place.
       Le juge de collisions l'a vu sur CINQ écrans : `.enh × .sub` sur Arranger, la langue
       et la confidentialité, `.enh × .keyebrow` sur Comprendre ton Aura, `.enh × .pl-h`
       sur Le Cercle — 342 px de large à chaque fois, donc la ligne entière recouverte.
       Ce qu'il faut garder, c'est **l'air entre le titre et ce qui le suit** : le voisin se
       repose sous le plateau à la même distance qu'il était sous le titre. Le contenu
       descend de la différence de hauteur, et c'est normal — un plateau prend plus de
       place qu'un titre nu. */
    var yAvant = nx ? nx.getBoundingClientRect().top : null;
    var ecart0 = (nx && yAvant != null) ? (yAvant - t.getBoundingClientRect().bottom) : null;

    var enh = document.createElement('div'); enh.className = 'enh';
    t.parentNode.insertBefore(enh, t);
    t.classList.add('enh-t');
    t.style.margin = '0'; t.style.padding = '0';
    enh.appendChild(t);
    if(cb){
      enh.appendChild(cb);
      /* ⚠ §8 · PIÈGE DE SPÉCIFICITÉ. `.closeb` est cloué en `position:absolute` par des
         règles à UN IDENTIFIANT (`#settingsScreen .closeb`, `#shareScreen .closeb`…) qui
         battent une règle à deux classes, `!important` ou pas. La feuille ne peut donc pas
         le déplacer — vu à l'écran : « ✕ FERMER » tombait sous le plateau. On pose donc
         les cotes EN LIGNE et en `important`, ce que le §8 recommande nommément. */
      ['position:static','top:auto','right:auto','left:auto','bottom:auto',
       'width:auto','margin:0','padding:0','transform:none'].forEach(function(d){
        var i=d.indexOf(':'); cb.style.setProperty(d.slice(0,i), d.slice(i+1), 'important');
      });
      cb.setAttribute('data-pose','enh');     /* on note ce qu'on écrit (lot RIEN-NE-SURVIT) */
    }

    /* ⚠ LE FLUX NE BOUGE PAS : on rend au suivant exactement ce que le titre prenait.
       ⚠ ET ON RECALCULE QUAND LES POLICES SONT PRÊTES. Mesuré trop tôt, le titre n'a pas
       encore sa vraie hauteur : `redteam_air` a attrapé un resserrement de **2 px** sur
       l'Index (184 → 182 entre le compteur et « à Rachel »). C'est le même piège que le
       chantier 50 sur `releve-design`. On mémorise ce que le titre prenait, on recalcule
       après `fonts.ready`, et **on arrondit vers le haut** : on rend toujours au moins ce
       qu'on a pris, jamais moins. Un resserrement est un défaut ; une respiration, non. */
    enh.__nx = nx; enh.__ecart = ecart0;
    ajuste(enh);
    return true;
  }

  function ajuste(enh){
    if(!enh || !enh.__nx || enh.__ecart == null) return;
    enh.style.marginTop = '0px';
    var m = parseFloat(enh.style.marginBottom || 0) || 0;
    /* deux passes suffisent : la mise en page est synchrone */
    for(var i = 0; i < 2; i++){
      var e = enh.__nx.getBoundingClientRect().top - enh.getBoundingClientRect().bottom;
      var d = e - enh.__ecart;
      if(Math.abs(d) < 0.25) break;
      m -= d;
      if(m < 0) m = 0;          /* l'écart d'origine ne se resserre jamais */
      enh.style.marginBottom = m.toFixed(2) + 'px';
    }
  }

  function tout(){
    MOITIE_1.forEach(function(e){ try{ pose(e[0], e[1]); }catch(_){ } });
    [].forEach.call(document.querySelectorAll('.enh'), function(b){
      var sc = b.closest('.screen,.sheet,.poster');
      if(sc && visible(sc)) ajuste(b);
    });
  }
  try{ if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ tout(); }); }catch(_){}
  [0, 120, 400, 900, 1800].forEach(function(d){ setTimeout(tout, d); });
  document.addEventListener('click', function(){
    [90, 320, 700].forEach(function(d){ setTimeout(tout, d); });
  }, true);
  window._encartHaut = tout;
  /* v21 — et on pose AU MOMENT où un écran s'ouvre, image par image, pas 90 / 320 / 700 ms après le clic */
  try{ var _ouv={};
    new MutationObserver(function(ms){ ms.forEach(function(m){ var sc=m.target; if(!sc.classList || !(sc.classList.contains('screen')||sc.classList.contains('sheet')||sc.classList.contains('poster')||sc.id==='feedView')) return;
        var o=sc.classList.contains('show')||sc.classList.contains('in'), k=sc.id||'';
        if(o && !_ouv[k]){ var n=0; (function f(){ try{ tout(); if(window._plateauRecale) window._plateauRecale(); }catch(_){} if(++n<20) requestAnimationFrame(f); })(); }
        _ouv[k]=o; }); })
      .observe(document.getElementById('device')||document.body,{subtree:true,attributes:true,attributeFilter:['class']}); }catch(_){}
  window._encartHautSonde = function(){
    return MOITIE_1.map(function(e){
      var sc = document.querySelector(e[0]); if(!sc) return [e[0], 'absent'];
      var b = sc.querySelector('.enh');
      if(!b) return [e[0], 'pas d encart'];
      var t = b.querySelector('.enh-t'), c = b.querySelector('.closeb');
      return [e[0], (t ? (t.textContent||'').trim().slice(0,22) : '—') + ' · ' + (c ? 'FERMER' : 'pas de fermer')];
    });
  };
})();
