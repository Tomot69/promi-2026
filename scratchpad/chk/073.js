
/* ⚑ LE PARTAGE · L'IMAGE EST L'ÉCRAN — la pose. Décision Tom, 2 septembre 2026.
   Ce lot RESTAURE avant de ranger : on ne range pas un écran dont un tiers est mort. */
(function(){
  var W = 390;
  function $(s,r){ return (r||document).querySelector(s); }
  function $$(s,r){ return [].slice.call((r||document).querySelectorAll(s)); }

  /* ⚑ 18 sept. 2026 — Tom : « la prévisualisation est trop haute, elle est tronquée sous
     l'encart du titre et sous les choix ; baisse un peu les éléments du cadre du bas. »
     Les deux encarts descendent de 12 px : la barre finit à 820 au lieu de 808, et
     l'encart du bas du Studio vient s'aligner dessus (point 2, `lot-CINQ-POINTS`). */
  var Y_LIGNE = 686, Y_BARRE = 758, Y_LIGNE_OUV = 120;

  /* ── LA LIGNE DIT OÙ L'ON EN EST ────────────────────────────────────────
     « Une ligne posée dessus dit où l'on en est. » Elle nomme LE SUJET et LE FORMAT —
     les deux choses qu'on vient régler. Les mots sont ceux de l'écran, aucun n'est
     inventé : ils sont lus sur les boutons eux-mêmes. */
  function motSujet(){
    var b = $('#shMode button.on');
    return b ? b.textContent.trim() : 'Ma Toile';
  }
  function motFormat(){
    var f = $('#shFormats .sh-fmt.on b') || $('#shFormats .sh-fmt.on');
    return f ? f.textContent.trim().split('\n')[0] : '';
  }
  function ligne(){
    var pf = $('#shcPeaufiner'); if(!pf) return;
    var t = pf.querySelector('.shp-t'); if(!t) return;
    var sc = $('#shareScreen');
    var ouvert = sc && sc.classList.contains('shc-ouvert');
    /* ouverte, la ligne redevient la poignée du panneau et reprend son mot */
    var mot = ouvert ? 'Peaufiner'
                     : (motSujet() + (motFormat() ? ' · ' + motFormat() : ''));
    if(t.textContent !== mot) t.textContent = mot;   /* comparer avant d'agir (§8) */
    var c = pf.querySelector('.shp-c');
    if(c){ var s = ouvert ? '‹' : '›'; if(c.textContent !== s) c.textContent = s; }
  }

  /* ── LE PANNEAU PORTE LE SUJET — et les VRAIS boutons, pas une copie ─────
     ⚠ AU REPOS LE SUJET N'EST PLUS DEHORS : la ligne le dit. `#shMode` descend donc dans
     la rangée « LE SUJET » du panneau. On DÉPLACE le nœud, on ne le recrée pas (§9) —
     sinon le gestionnaire d'origine, posé bouton par bouton, serait perdu. */
  function sujetDansPanneau(){
    var m = $('#shMode'); if(!m) return;
    var pile = $('#shcPile'); if(!pile) return;
    var rang = null;
    $$('#shcPile .shc-reg').forEach(function(r){
      var l = r.querySelector('.l,.sh-lab');
      if(l && /LE SUJET/i.test(l.textContent||'')) rang = r;
    });
    if(!rang) return;
    if(m.parentNode !== rang){
      rang.appendChild(m);
      m.className = '';
      m.removeAttribute('style');
    }
  }

  /* ── DÉFAUT 3 · LES SIX COMMANDES DU NOYAU ÉTAIENT INATTEIGNABLES ────────
     Elles vivent dans `#shNoyauParts`, dans le panneau. Mesuré avant : le panneau sortait
     à 390 × 148 pour un contenu qui descendait à y 1109 — les six tombaient sous le pli,
     par quelque chemin qu'on prenne. Le panneau DÉFILE désormais (feuille ci-dessus), et
     la classe `shc-noyau` les ouvre dès que le mode Noyau est pris. */
  function noyauClasse(){
    var sc = $('#shareScreen'); if(!sc) return;
    var on = (window.shareMode === 'noyau');
    if(sc.classList.contains('shc-noyau') !== on) sc.classList.toggle('shc-noyau', on);
  }

  /* ── DÉFAUT 4 · DEUX GESTIONNAIRES SANS NŒUD ────────────────────────────
     `#shOptVis` et `.sh-opts` n'existent plus dans le DOM — vérifié, 0 nœud pour chacun.
     Leurs gestionnaires, eux, restaient posés : du code qui ne peut plus rien faire, et
     qui ferait croire à une fonction vivante au prochain qui lira l'écran. On les
     NEUTRALISE en les nommant, on ne balaie pas (§8 : jamais un crible en bloc). */
  function orphelins(){
    /* rien à retirer si le nœud n'existe pas : on le CONSTATE, et on le dit au relevé.
       Les deux gestionnaires (l. 7412 et 7415) sont gardés par un `if(nœud)` : ils ne
       s'enregistrent jamais. C'est du code mort, pas un bug actif — et il est nommé ici
       pour que le prochain qui lira l'écran ne le prenne pas pour une fonction vivante. */
    window._shOrphelins = { shOptVis: !!document.getElementById('shOptVis'),
                            shOpts: document.querySelectorAll('.sh-opts').length };
  }

  /* ⚑ ET DERRIÈRE L'ORPHELIN, UNE FONCTION QUI N'ARRIVAIT PAS JUSQU'À L'IMAGE.
     `#shOptVis` pilotait `shareVis` — « les noms sur l'image ». Le nœud a disparu ; la
     VARIABLE, elle, est restée à `true` et **`shareExport` la lit encore** pour le mode
     Noyau et Mes Promi (`if(shareVis) shareLabels(...)`), tout comme `paintPreview`.
     Pendant ce temps la commande vivante — « Avec texte / Sans texte » (`#shTxRow`) —
     écrit `window.shLabels`. Deux noms pour une même intention : l'aperçu de Ma Toile
     avait été rebranché (chantier 39), **l'export ne l'avait pas été**. Choisir « Sans
     texte » puis partager sortait donc une image AVEC les noms.
     On relie les deux à la source du bouton, et l'orphelin n'a plus de raison d'être.
     ⚠ On ENVELOPPE `shareExport`, on ne le réécrit pas (§9). */
  function relieTexte(){
    try{
      var v = (window.shLabels === undefined) ? true : !!window.shLabels;
      if(window.shareVis !== v) window.shareVis = v;   /* comparer avant d'agir (§8) */
    }catch(_){}
    try{
      var _ex = window.shareExport;
      if(_ex && !_ex.__vis){
        var w = function(){
          try{ window.shareVis = (window.shLabels === undefined) ? true : !!window.shLabels; }catch(_){}
          return _ex.apply(this, arguments);
        };
        w.__vis = true; window.shareExport = w;
      }
    }catch(_){}
  }

  /* ── DÉFAUT 5 · « FORMAT » EN DOUBLE ────────────────────────────────────
     Le premier coiffe `#shNoyauParts` : il doit dire ce que le Noyau MONTRE. On corrige
     le mot, jamais le nœud. */
  function libelleNoyau(){
    var np = $('#shNoyauParts'); if(!np) return;
    var l = np.previousElementSibling;
    if(l && l.classList && (l.classList.contains('sh-lab') || l.classList.contains('l'))
       && /^\s*Format\s*$/i.test(l.textContent||'')) l.textContent = 'Ce qu’il montre';
  }

  /* ── DÉFAUT 2 · LA BORNE DU SUR-MESURE ──────────────────────────────────
     `shCustomClamp` borne à 3840 et l'export prédéfini sort en 4K, mais les `+`
     s'éteignaient à 2160 : la moitié de la course était injoignable. On ENVELOPPE la
     fonction — l'envelopper et non l'écouter, c'est le §8 — et on rétablit l'état des
     deux boutons sur la vraie borne. */
  function borne4k(){
    if(!window.shCustomClamp || window.shCustomClamp.__4k) return;
    var f = window.shCustomClamp;
    window.shCustomClamp = function(){
      var r = f.apply(this, arguments);
      try{
        var a = (window.shCW||1080)/(window.shCH||1920);
        var bW = $('#shCustom .sh-step button[data-d="w+"]') || $$('#shCustom .sh-step button')[1];
        var bH = $$('#shCustom .sh-step button')[3];
        if(bW) bW.disabled = (window.shCW >= 3840 || a >= 2.5);
        if(bH) bH.disabled = (window.shCH >= 3840 || a <= 0.42);
      }catch(_){}
      return r;
    };
    window.shCustomClamp.__4k = true;
  }

  /* ── L'IMAGE PREND L'ÉCRAN ──────────────────────────────────────────────
     « L'image est l'écran, entière. » `shareRender()` dimensionne `#shWrap` EN LIGNE pour
     la zone qu'il connaît — l'ancienne carte de 233 × 415. Agrandir la zone ne suffisait
     donc pas : le cadre grandissait, l'image restait une vignette au milieu. Mesuré :
     zone 390 × 844, image 233,7 × 415,4.
     ⚑ ELLE ENTRE, ELLE NE SE FAIT PAS ROGNER. On prend la plus grande taille qui TIENNE
     dans l'écran au rapport choisi — c'est la composition de quelqu'un qu'on montre, on
     n'en coupe pas les bords pour remplir un coin. À 9:16 cela donne 390 × 693 centré :
     l'image occupe 82 % de l'écran et n'y perd rien.
     ⚑ ET ELLE PERD SES COINS RONDS. Une carte a des coins ; un écran n'en a pas. C'est ce
     qui la faisait lire comme une vignette posée sur un fond. */
  function image(){
    var wrap = $('#shWrap'); if(!wrap) return;
    var sc = $('#shareScreen');
    var ouvert = !!(sc && sc.classList.contains('shc-ouvert'));
    var a = (window.shCW || 1080) / (window.shCH || 1920);
    if(!(a > 0)) a = 0.5625;
    /* ⚑ LA BANDE, PAS L'ÉCRAN — Tom, 18 septembre 2026 : « on doit la voir entière ».
       « L'image est l'écran » la cadrait dans 390 × 844 : à 9:16 elle sortait 390 × 693
       centrée à y 75 — MESURÉ — donc 25 px sous le plateau du titre (40 → 100) et 94 px
       sous les encarts du bas (674). Elle était rognée aux DEUX bouts.
       Elle tient maintenant dans la bande libre : sous le plateau (100 + 12 d'air) et
       au-dessus de l'encart du bas descendu (686 − 12). Soit 112 → 674, HB = 562.
       Vérifié sur tous les formats — 9:16 316×562 · 9:19,5 259×562 · 1:1 390×390 ·
       4:5 390×487 · 16:9 390×219 · sur mesure au plus étroit (0,42) 236×562. */
    var HT = 112, HB = 562;
    var w = W, h = W / a;
    if(h > HB){ h = HB; w = HB * a; }
    var x = Math.round((W - w) / 2), y = Math.round(HT + (HB - h) / 2);
    /* ⚑ ET QUAND LE PANNEAU S'OUVRE, L'IMAGE RECULE — décision Tom, 3 septembre 2026 :
       « L'image est la composition de quelqu'un — on ne la rogne pas, on ne la borne pas.
       La ligne est un état, pas un cadre. Si le mot-marque est masqué au repos, il
       réapparaît dès que le panneau s'ouvre et que l'image recule. »
       AU REPOS le mot-marque de l'image tombe à y 741 et passe sous les deux boutons
       (746 → 808) — mesuré au doigt, `elementFromPoint` y rend `shcBarre`. C'est admis.
       À L'OUVERTURE il doit reparaître. On fait donc reculer l'image pour de bon : elle
       passe à 90 % et se cale par le BAS à 740, juste au-dessus des boutons. Son
       mot-marque remonte alors à 715 → 730, dans la bande que le panneau libère
       (198 → 700). Rien n'est rogné, rien n'est borné : l'image recule, entière. */
    if(ouvert){
      /* la barre est descendue de 12 : le calage par le bas suit (740 → 752), et
         l'image reste ENTIÈRE — on borne aussi sa hauteur à la bande libérée. */
      var HO = 752 - 192;                                  /* sous la ligne ouverte (120+62+10) */
      w = Math.round(W * 0.90); h = Math.round(w / a);
      if(h > HO){ h = Math.round(HO); w = Math.round(h * a); }
      x = Math.round((W - w) / 2); y = Math.round(752 - h);
    }
    [['left', x+'px'], ['top', y+'px'], ['width', Math.round(w)+'px'],
     ['height', Math.round(h)+'px'], ['border-radius','0px'], ['margin','0']]
      .forEach(function(d){ wrap.style.setProperty(d[0], d[1], 'important'); });
    var cv = $('#shCanvas');
    if(cv){ ['width:100%','height:100%','border-radius:0px','max-width:none'].forEach(function(d){
      var i=d.indexOf(':'); cv.style.setProperty(d.slice(0,i), d.slice(i+1), 'important'); }); }
  }

  /* ── LA POSE ────────────────────────────────────────────────────────────
     ⚠ ON REPASSE DERRIÈRE LE MOTEUR (§8). `shareRender()` repose la taille ET la place de
     `#shWrap` en ligne ; `buildStudio` et le lot « feuille » reprennent l'écran quelques
     centaines de millisecondes plus tard. Un lot qui ne pose qu'aux événements du doigt
     perd la main dès qu'une de ces fonctions est appelée d'ailleurs. */
  function pose(){
    var sc = $('#shareScreen'); if(!sc) return;
    if(!sc.classList.contains('sh-plein')) sc.classList.add('sh-plein');
    var pf = $('#shcPeaufiner'), ba = $('#shcBarre'), pa = $('#shPreviewArea');
    var ouvert = sc.classList.contains('shc-ouvert');
    if(pf){ pf.style.setProperty('top', (ouvert ? Y_LIGNE_OUV : Y_LIGNE) + 'px', 'important'); }
    if(ba){ ba.style.setProperty('top', Y_BARRE + 'px', 'important');
            ba.style.setProperty('bottom', 'auto', 'important'); }
    /* l'image prend TOUT l'écran, ouverte comme fermée : elle reste entière derrière */
    if(pa){ ['top:0px','left:0px','width:390px','height:844px','bottom:auto'].forEach(function(d){
      var i=d.indexOf(':'); pa.style.setProperty(d.slice(0,i), d.slice(i+1), 'important'); }); }
    image();
    sujetDansPanneau(); noyauClasse(); libelleNoyau(); borne4k(); orphelins(); relieTexte(); ligne();
  }
  window._shPlein = pose;

  [0,150,400,900,1600,2600].forEach(function(d){ setTimeout(pose, d); });
  document.addEventListener('click', function(){ [60,220,500,900].forEach(function(d){setTimeout(pose,d);}); }, true);
  try{ if(document.fonts && document.fonts.ready) document.fonts.ready.then(pose); }catch(_){}

  /* on enveloppe le moteur, on ne se contente pas d'écouter le doigt */
  try{
    var _sr = window.shareRender;
    if(_sr && !_sr.__plein){
      var w = function(){ var r = _sr.apply(this, arguments);
        /* ⚑ v21 — DANS LA MÊME TÂCHE, pas à l'image suivante : entre les deux, la taille du moteur se peignait et
           l'aperçu alternait 316×562 / 366×651 / 234×415 pendant la première seconde. */
        try{ pose(); }catch(_){}
        try{ requestAnimationFrame(pose); }catch(_){}
        return r; };
      w.__plein = true; window.shareRender = w;
    }
  }catch(_){}

  /* un observateur sur l'écran, QUI COMPARE AVANT D'AGIR — sans quoi il se réveille
     lui-même, c'est le piège du §8 payé plusieurs fois sur ce projet. */
  try{
    var scr = document.getElementById('shareScreen');
    if(scr){
      var _cls = scr.className;
      new MutationObserver(function(){
        if(scr.className === _cls) return;
        _cls = scr.className;
        pose();
      }).observe(scr, {attributes:true, attributeFilter:['class']});
    }
  }catch(_){}
})();
