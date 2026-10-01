
/* ═══════════════════════════════════════════════════════════════════════════════════════
   SECTION 3 · LA PAGE + — le moteur. Même onde que la fiche (§2.1, primitives exposées par
   la section 1), même formule de hauteur (§2.5), mêmes cotes de dalle (§2.7).
   `base = max(196, 344 − 32 × (n − 1))`, n = nombre de lignes de la phrase, verbe compris ;
   `amp = 36` sur la page + (décision Tom, 1er sept. 2026 — l'onde passe à la borne basse
   du §2.4 bis, partout), `22` dès qu'un panneau de choix occupe le corps ;
   boîte SVG = `base + amp + 60`. L'interligne du §2.8 : `int(taille × 1,2) + 24`.
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  var W = 390;
  function $(s,r){ return (r||document).querySelector(s); }
  function pose(el,css){ if(!el) return; for(var k in css) el.style.setProperty(k,css[k],'important'); }

  /* quelle nature écrit-on ? on lit l'app, on ne devine pas. */
  /* MESURÉ, PAS DEVINÉ : les trois formulaires sont display:block EN MÊME TEMPS
     (#promiForm 709, #nueeForm 444, #draftForm 372) — l'app les fait DÉFILER dans #csMid,
     elle ne les masque pas. Tester leur display renvoyait « Nuée » sur un Promi.
     On regarde donc lequel recouvre réellement le cadre, et à défaut le mot du verbe. */
  function natureCourante(){
    try{
      var cs = document.getElementById('createSheet');
      /* ⚑ v21 — la nature est ce que le code POSE (`data-kind`, posé par la tuile), jamais d'abord une géométrie
         ni le texte de la phrase : pendant qu'une phrase se rebâtit, « chiche » manquait au texte et la page + d'un
         Chiche repassait en Promi (mesuré à 286 ms), ce qui faisait attendre l'ouverture jusqu'à 1 s. */
      var _dk = cs && cs.getAttribute('data-kind');
      if(_dk==='promi' || _dk==='chiche' || _dk==='nuee') return _dk;
      var cr = cs.getBoundingClientRect();
      var best = null, aire = 0;
      [['promi','promiForm'],['nuee','nueeForm']].forEach(function(p){
        var e = document.getElementById(p[1]); if(!e) return;
        var r = e.getBoundingClientRect();
        var h = Math.min(r.bottom, cr.bottom) - Math.max(r.top, cr.top);
        if(h > aire){ aire = h; best = p[0]; }
      });
      if(best && aire > 40){
        if(best === 'nuee') return 'nuee';
        var t = ($('#csPhrase .ph-txt')||{}).textContent || '';
        return /chiche/i.test(t) ? 'chiche' : 'promi';
      }
    }catch(e){}
    try{ var t2 = ($('#csPhrase .ph-txt')||{}).textContent || '';
      if(/chiche/i.test(t2)) return 'chiche';
      if(/lance une nu/i.test(t2)) return 'nuee'; }catch(e){}
    return 'promi';
  }
  /* LA PHRASE, LIGNE PAR LIGNE : on marche les nœuds de .ph-txt et on coupe sur les <br>.
     Pour chaque ligne : le nombre de caractères, le nombre de pastilles, le nombre de mots. */
  function decoupe(txt){
    var out = [{car:0, past:0, mots:0}];
    [].forEach.call(txt.childNodes, function(n){
      if(n.nodeType===1 && n.tagName==='BR'){ out.push({car:0, past:0, mots:0}); return; }
      var L = out[out.length-1];
      var t = (n.textContent||'').trim();
      if(!t) return;
      L.car += t.length; L.mots += 1;
      if(n.nodeType===1 && /ph-b|ph-m/.test(n.className||'')) L.past += 1;
    });
    return out.filter(function(L){ return L.car>0; });
  }

  /* le nombre de lignes de la phrase : les <br> du bloc, verbe compris (§2.5). */
  /* LA BOÎTE DE PHRASE ACTIVE. La Nuée écrit dans #nueePhrase (son propre formulaire),
     le Promi et le Chiche dans #csPhrase. Une seule des deux est à l'écran : on la marque
     `.pp-phrase` — c'est cette prise que suivent le juge et les cotes. */
  function boitePhrase(nat){
    var b = document.getElementById(nat==='nuee' ? 'nueePhrase' : 'csPhrase');
    var a = document.getElementById(nat==='nuee' ? 'csPhrase' : 'nueePhrase');
    if(a) a.classList.remove('pp-phrase');
    if(b) b.classList.add('pp-phrase');
    return b;
  }
  function lignes(nat){
    var b = document.getElementById(nat==='nuee' ? 'nueePhrase' : 'csPhrase');
    var t = b ? b.querySelector('.ph-txt') : null; if(!t) return 2;
    return Math.max(1, t.querySelectorAll('br').length + 1);
  }
  /* un panneau de choix occupe-t-il le corps ? (§2.4 bis : amp = 22, base = 196) */
  function choixOuvert(){
    /* LE PANNEAU DE CHOIX DE L'APP S'APPELLE #csChoix — il manquait à la liste, si bien que
       les trois cadres « Choix ouvert » restaient à base = 312/280 au lieu de 196 et que le
       trait passait 100 px trop bas (mesuré : trace à 358 au lieu de 236). Il ne compte
       QUE quand il est ouvert : `.ouvert` est la classe que pose `_phraseChoix`. */
    /* ⚠ NE JAMAIS TESTER LA HAUTEUR RENDUE DU PANNEAU : dès que ses éléments passent en
       absolu (les cotes du §5), #csChoix retombe à 0 de haut, « ouvert » devient faux, les
       cotes reviennent à l'état au repos, les éléments repassent en flux… et l'écran
       oscille d'une passe à l'autre (constaté : le mot de trace à 236 et la phrase à 392
       dans le même relevé). La classe `.ouvert`, posée par `_phraseChoix`, EST l'état. */
    var z = $('#csChoix');
    if(z && z.classList.contains('ouvert') && z.children.length) return true;
    /* ⚑ LA NUÉE S'OUVRE COMME LE PROMI ET LE CHICHE (lot-GENS, 13 sept. 2026) : sa zone `#nueeChoix` pleine est un choix
       ouvert — le trait monte au plancher du §2.4 bis et la liste a la même place. */
    var nzc = $('#nueeChoix'), csn = $('#createSheet');
    if(nzc && nzc.children.length && csn && csn.classList.contains('pp-nuee')) return true;
    var s = ['#csKeyboard','#csPersonnes','#csDates','#csChoixPanel'];
    for(var i=0;i<s.length;i++){ var e=$(s[i]);
      if(e && getComputedStyle(e).display!=='none' && e.getBoundingClientRect().height>40) return true; }
    return false;
  }

  function ecran(){
    var cs = document.getElementById('createSheet');
    var n = natureCourante(), ouvert = choixOuvert(), nl = lignes(n);
    var base = ouvert ? 196 : Math.max(196, 344 - 32*(nl-1));
    /* ⚑ L'ONDE PASSE À 36 PARTOUT. Décision Tom, 1er septembre 2026 : « l'ondulation du
   trait doit devenir celle du moodboard — moins d'amplitude — et partout ».
   Le §2.4 bis borne amp à [36, 52] : 36 est la borne BASSE, donc la valeur la plus
   calme que la spec autorise, et c'est celle des planches. L'onde garde sa loi
   (per 1,5 · mont = amp·0,34 · a = amp·0,62) : seule l'amplitude change.
   ⚠ DEUX EXCEPTIONS ÉCRITES, INTOUCHÉES : `amp = 22` dès qu'un panneau de choix
   occupe le corps (§2.4 bis), et la loi propre de la carte d'Index (§3.9,
   `amp = 13 × largeur/173`). */
    var amp  = ouvert ? 22 : 36;
    var boite = base + amp + 60;
    /* ⚑ LA BOÎTE DE LA DALLE DE LA PAGE + SE TIRE DE LA BASE, PAS DE LA CRÊTE DE L'ONDE.
       Relevée sur les cadres, deux bases et neuf écrans, au pixel :

           base 312 (cadres 2, 4, 24, 26, 28, 32)  →  dalle 244 × 200 à x = 73
           base 280 (cadres 6, 8, 10)              →  dalle 204 × 168 à x = 93

       soit **dh = base − 112** et **dw = 1,2 × dh**, centrée. (Les 244 et 204 sont la
       largeur du SVG, qui porte 2 px de marge de chaque côté : le centre, lui, tombe
       sur 195 dans les deux cas, comme le nôtre.)
       L'app calculait `(base − amp) − 88 − 12` : elle arrêtait la dalle 12 px AU-DESSUS
       de la crête de l'onde, alors que le cadre la laisse mordre dessus de 22 px.
       Résultat mesuré : 199 × 166 au lieu de 244 × 200 — la matière sortait d'un cinquième
       trop petite, et le duo comptait tout son pourtour comme un écart de dessin. */
    var dh = Math.min(300, base - 112);
    var dw = Math.min(320, Math.floor(1.2*dh));
    /* §2.6 · l'état du trait. « plate » : rien n'est tracé (les quinze cadres au repos).
       « cours » : le doigt est posé — le plein va de 0 à lui, borné au milieu exact. */
    /* « signe » : ma moitié est donnée — le plein s'arrête au milieu exact (195). */
    var doigt = (typeof window._ppDoigt === 'number') ? window._ppDoigt : null;
    var sig = !!window._ppSigne;
    /* LE PLANCHER (§2.5) : `base` ne descend jamais sous 196. Il est atteint sur un CHOIX
       OUVERT (base 196, amplitude 22) et sur une phrase de six lignes ou plus. C'est là — et
       seulement là — que la matière remplit le champ (voir la doctrine près de `champ()`). */
    var plancher = 196;
    return {cs:cs, nat:n, base:base, amp:amp, boite:boite, nl:nl, ouvert:ouvert,
            plancher:plancher, auPlancher:(base <= plancher),
            doigt:doigt, etat:(sig ? 'signe' : (doigt==null ? 'plate' : 'cours')),
            garde:!!window._ppGarde,
            dalle:{x:Math.floor((W-dw)/2), y:88, w:dw, h:dh}};
  }
  window._ppEcran = ecran;

  /* ═══ LE TRAIT (§2.6) — sur la page +, rien n'est tracé : amorce effilée, chevron, points. ═══ */
  function trait(){
    try{
      var O = window._onde; if(!O) return;
      var e = ecran(), cs = e.cs;
      if(!cs || !cs.classList.contains('pp')) return;
      var cv = document.getElementById('csTrameCv'); if(!cv) return;
      var y = O.onde(e.base, e.amp), H = e.boite;
      var largeur = cs.clientWidth || W, sc = largeur/W;
      var dpr = Math.max(2, Math.min(3, window.devicePixelRatio||2));
      cv.width = Math.round(largeur*dpr); cv.height = Math.round(H*sc*dpr);
      cv.style.setProperty('width', largeur+'px', 'important');
      cv.style.setProperty('height', (H*sc)+'px', 'important');
      var g = cv.getContext('2d'); if(!g) return;
      g.setTransform(dpr*sc,0,0,dpr*sc,0,0); g.clearRect(0,0,W,H);
      g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
      /* 1 · l'aplat de nature, borné en bas par l'onde.
         GARDÉ DE CÔTÉ : PAS D'APLAT. Rien n'est promis, donc il n'y a pas de champ — le
         cadre 27 montre la dalle et les points posés sur le corps nu. C'est exactement ce
         que fait la fiche d'un gardé de côté depuis la section 1 (`e.aplat = false`). */
      /* ⚠ TOUJOURS, SANS EXCEPTION — c'est l'écran que Tom a signalé : « sur la page + en
         thème clair, le champ est crème — la couleur du corps — au lieu de l'aplat de
         nature. La dalle flotte sur du vide et “trace pour planter” est sur du crème. »
         Le champ d'un gardé de côté était éteint ici, sur ma lecture fautive de Q83.
         Ce qui lui manque, c'est la matière ; le champ porte toujours sa nature. */
      g.beginPath(); O.chemin(g,y,0,W); g.lineTo(W,0); g.lineTo(0,0); g.closePath();
      g.fillStyle = O.NATCOL[e.nat]; g.fill();
      /* ⚑ LE CHAMP SE DÉCLARE — « un champ blanc n'existe jamais » (décision Tom, 29 août).
         Un contrôle au pixel ne peut pas trancher partout : sur une Nuée VIDE, les graines
         du §10.6 sont crème DANS LES DEUX THÈMES, et elles tombent pile sur la couleur du
         corps. Ce sont pourtant de la MATIÈRE posée sur un champ mauve, pas un champ nu.
         Le peintre, lui, sait ce qu'il a versé : il l'écrit. C'est la doctrine du §7 —
         on compare la COMPOSITION, pas la peinture. */
      try{ cv.setAttribute('data-champ', O.NATCOL[e.nat]); }catch(_){}
      /* 2 · la dalle — la vraie, celle du moteur, jamais teintée par la nature (CLAUDE.md §4) */
      /* LA DALLE DOIT ÊTRE DE LA NATURE COURANTE. Elle prenait la DERNIÈRE promesse posée :
         un Chiche affichait donc la dalle mauve d'un Promi (constaté au duo). On cherche une
         promesse de la nature écrite, et on retombe sur la dernière seulement à défaut. */
      var src = null, id = null;
      try{
        if(window._ppDalleId!=null) id = window._ppDalleId;
        else if(promises && promises.length){
          var pool = promises.filter(function(q){
            if(q.draft) return false;
            if(e.nat==='chiche') return !!q.chiche;
            if(e.nat==='nuee')   return !!q.nuee;
            return !q.chiche;
          });
          /* ⚑ v34 — de préférence une promesse dont la cellule ne touche PAS le bord de la Toile : sa dalle est entière */
          var _TT=(Toile.taille&&Toile.taille())||{w:1e9,h:1e9}, _int=pool.filter(function(q){ var a=Toile.dalleAbs&&Toile.dalleAbs(q.id);
            return a && a.minx>1 && a.miny>1 && a.minx+a.w<_TT.w-1 && a.miny+a.h<_TT.h-1; });
          id = (_int.length ? _int[_int.length-1] : (pool.length ? pool[pool.length-1] : promises[promises.length-1])).id;
        }
      }catch(_){}
      cv.__matRect=null; cv.__matLum=null;   /* v29 · la matière déclarée ne survit pas à l'écran d'avant */
      if(id!=null && window.Toile && Toile.dalleAbs && Toile.dalleAbs(id)){
        /* ⚑ v29 — la teinture de Q30 est PEINTE PAR LE MOTEUR (`opts.rampe`), à la taille finale de la dalle ;
           plus aucun pixel relu ni reposé ici (redteam_decoupe, familles B et C). La rampe reste celle de
           `teinteDalle`, et elle ne sort toujours pas de la bande haute (Q30 borné, CLAUDE.md §4). */
        src = {__id:id, __o:{rampe:window._ppRampe(e.nat), courant:1}, width:1};   /* v30 · la page + montre la dalle qu'on va planter : monde courant */
        /* LA MATIÈRE REMPLIT LE CHAMP **AU PLANCHER** (décision Tom corrigée, 19 août 2026).
           Ailleurs elle garde sa boîte : le vide n'est pas un défaut général, c'est un défaut
           du plancher (doctrine près de `champ()`). Un GARDÉ DE CÔTÉ n'a pas de champ (pas
           d'aplat) : sa dalle garde sa boîte, comme le cadre 27 la montre. Une phrase À PHOTO
           garde sa boîte aussi : la photo remplace la matière (Q57). */
        if(e.auPlancher && !e.garde && !(window._phrase && window._phrase.photo)){
          O.champ(g, y, function(H2){ var _cP=O.couvre(g, src, H2); cv.__matRect={x:0,y:0,w:W,h:H2};
            cv.__matLum=(_cP&&_cP.__dalleInfo)?_cP.__dalleInfo.lum:null; });
        } else {
          var _rP=window._poseDalle(g, id, e.dalle.x, e.dalle.y, e.dalle.w, e.dalle.h, src.__o);
          cv.__matRect=_rP?{x:_rP.x,y:_rP.y,w:_rP.w,h:_rP.h}:null; cv.__matLum=(_rP&&_rP.cv.__dalleInfo)?_rP.cv.__dalleInfo.lum:null;
          /* ⚑ Q74 · LA ZONE DE MATIÈRE DE LA PAGE +, DÉCLARÉE PAR CELUI QUI LA PEINT.
             ⚠ CE CANEVAS N'EST PAS CELUI DE `promiTrame`. `#csTrameCv` porte TOUT le champ
             de la page + depuis le portage de la section 3 — l'aplat, la dalle, l'onde,
             ses points, les flèches d'invite. `renderCsDalle` le peint AUSSI, plus tôt et
             avec d'autres cotes : la boîte qu'elle publiait (175, 237, 203 × 203, base
             390 × 844) était celle d'un dessin que la section 3 avait déjà recouvert.
             Vérifié en sortant le canevas en image (`scratchpad/pp_trame.png`) : la dalle
             réelle tient dans `e.dalle`, ici même, et nulle part ailleurs.
             Les unités sont l'écran 390 (le contexte est en `dpr*sc`), d'où la base. */
          try{ cv.setAttribute('data-matiere',
                 [Math.round(e.dalle.x),Math.round(e.dalle.y),
                  Math.round(e.dalle.w),Math.round(e.dalle.h)].join(','));
               cv.setAttribute('data-matiere-base', W+','+H); }catch(_){}
        }
      }
      /* 3 · la ligne : rien n'est tracé — amorce, chevron, puis des points Ø9 tous les 18 */
      /* §2.6 · au repos, l'amorce s'effile de −10 à 42 et les points prennent le relais.
         Pendant le geste, LE PLEIN VA DE 0 AU DOIGT, jamais plus loin que le milieu, et le
         chevron marque la frontière — c'est le même trait, à une coupe près. */
      /* §2.1 bis et §4 : `c = CLAIR[nat] si etat == "plate", TERRA sinon`. Dès que le
         doigt trace, LE TRAIT ENTIER passe en terracotta — le plein comme les points. */
      var col = (e.etat === 'plate') ? (O.NATTRAIT||O.NATCLAIR)[e.nat] : O.TERRA, ep = 10, rr = 4.5, esp = 18;
      /* ═══ UNE NUÉE SE LANCE EN TRAÇANT LE TRAIT ENTIER (décision Tom, 19 août 2026) ═══
         Pas une moitié : 0 → 390, le MODE COMPLET du §2.6 — celui d'une parole tenue.
         Une Nuée n'est promise à personne ; personne ne vient à sa rencontre, donc une
         demi-courbe n'aurait aucun sens. Un Promi et un Chiche gardent leur moitié : là,
         l'autre trace la sienne. */
      var ENTIER = (e.nat === 'nuee');
      var MI = ENTIER ? W : W/2;
      /* §2.6 · « ma moitié donnée » : 0 → 195, LE MILIEU EXACT, jamais plus loin. */
      var cx = (e.etat === 'signe') ? MI
             : (e.etat === 'cours') ? Math.max(W*0.11, Math.min(e.doigt, MI)) : W*0.11;
      g.strokeStyle = col; g.fillStyle = col; g.lineWidth = ep;
      g.lineCap = 'round'; g.lineJoin = 'round';
      /* ⚑ LE PINCEAU — la matière choisie remplace le ruban plein, jamais la COURBE.
         Les douze tracés de la planche sont posés sur l'onde du §2.1 (base 560, amp 36,
         vérifié à 0,05 px) : on reporte leur ligne moyenne sur CETTE onde et on découpe
         à la même abscisse. « Plein » est le trait d'aujourd'hui, mot pour mot. */
      /* ⚑ 23 SEPTEMBRE 2026 (Tom) — « LE TRAIT À SA GAUCHE DÉPASSE DE LA FLÈCHE. »
         Le trait s'arrêtait à `cx + ep·0,6` — c'est-à-dire À LA POINTE EXACTE du chevron
         (`chevron` pose sa pointe à `6·k` avec `k = ep/10`, donc `cx + 0,6·ep`). Le ruban et
         sa pointe effilée sortaient donc PAR la pointe du V, et ça se voit d'autant plus que
         le pinceau est épais — c'est la même chose sur les cinq pinceaux, à toutes les
         positions du trait. Il s'arrête maintenant EN DEÇÀ, à `cx − ep·0,15` : le V le
         recouvre (ses branches arrière vont jusqu'à `cx − 0,7·ep`) et plus rien ne dépasse. */
      var _bout = cx - ep*0.15;
      /* ⚑ v54 (Tom) — « un liseré sous le trait dans la page +, en mode sombre, pour les trois natures — le même que sur les
         fiches, sous le début du trait, à gauche de la flèche : sans lui on ne l'identifie pas sur fond sombre. » Le filet de
         `_ficheTrait` tel quel : 0,8 px, le crème adouci des filets, peint AVANT le trait (il passe dessous, la flèche le
         recouvre), le long de ce qui est TRACÉ seulement. */
      var _sombre = !document.getElementById('device').classList.contains('light') && !(window._sansFiletCercle && window._sansFiletCercle(cv));
      try{ cv.setAttribute('data-filet-trait', _sombre ? '1' : '0'); }catch(_){}
      if(_sombre){ var _f = 0.8, _dy = ep/2 + _f/2, _yb = function(x){ return y(x) + _dy; };
        g.save(); g.strokeStyle = window._FILET_DOUX || '#F7F0DE'; g.lineWidth = _f; g.lineCap = 'butt';
        /* ⚑ v76 (Tom) — « l'extrémité du liseret dépasse le trait en passant au-dessus : il faut l'arrêter avant. » Il finissait sous la
           pointe (`cx` ou `cx − 0,15·ep`), c'est-à-dire DANS le V, où aucune branche ne le couvre. Il s'arrête derrière le V : ses branches
           arrière finissent à `cx − 0,7·ep`, plus leur bout rond (0,3·ep). */
        var _finF = cx - ep - 4;   /* v82 (Tom) : « encore 1 mm avant la flèche » */
        if(e.etat === 'cours' || e.etat === 'signe'){ g.beginPath(); O.chemin(g, _yb, 0, _finF); g.stroke(); }
        else {   /* au repos le début du trait est un RUBAN effilé (22 → 1,5 px) : le filet suit SON bord, pas celui d'un trait plein */
          var _x0 = -W*0.03, _x1 = _bout, _e0 = ep*2.2, _e1 = ep*0.15, _n = 88; g.beginPath();
          for(var _i = 0; _i <= _n; _i++){ if(_x0 + (_x1 - _x0)*_i/_n > _finF) break; var _x = _x0 + (_x1 - _x0)*_i/_n, _e = (_e0 + (_e1 - _e0)*_i/_n)/2 + _f/2,
              _dd = (y(_x + 0.5) - y(_x - 0.5)), _L = Math.sqrt(1 + _dd*_dd), _px = _x - _dd/_L*_e, _py = y(_x) + _e/_L;
            if(_i === 0) g.moveTo(_px, _py); else g.lineTo(_px, _py); }
          g.stroke(); }
        g.restore();
        g.strokeStyle = col; g.fillStyle = col; g.lineWidth = ep; g.lineCap = 'round'; g.lineJoin = 'round'; }
      var _pin = (window.promiPinceau ? window.promiPinceau(null) : 'Plein'), _fait = false;
      if(_pin !== 'Plein' && window._matiereTrait)
        _fait = window._matiereTrait(g, _pin, e.base, e.amp, -W*0.03,
                  (e.etat === 'plate') ? _bout : cx, col);
      if(!_fait){
        if(e.etat === 'cours' || e.etat === 'signe'){
          g.beginPath(); O.chemin(g, y, 0, cx); g.stroke();
        } else {
          O.ruban(g, y, -W*0.03, _bout, ep*2.2, ep*0.15); g.fill();
        }
      }
      /* le trait entier d'une Nuée donnée : plus rien ne manque, donc ni chevron ni points. */
      if(!(ENTIER && e.etat === 'signe')){
        O.chevron(g, y, cx, col, ep);
        for(var x=cx+esp*1.3; x<W-rr; x+=esp){ g.beginPath(); g.arc(x,y(x),rr,0,6.2832); g.fill(); }
      }
      /* 4 · LA FLÈCHE D'INVITE (§2.4). Le code de référence du §4 ne la dessine que sur
         l'état « plate » — rien n'est tracé — c'est-à-dire la page + au repos. Elle
         manquait : le moodboard la montre sur tous les cadres de la page +, l'app n'en
         peignait aucun. Bézier bombée vers la gauche, épaisseur 4,5, bouts ronds ; la tête
         est calculée sur la tangente RÉELLE en B, deux ailes à ±32°, longueur 13 — jamais
         posée à la main. */
      if(e.etat === 'plate') fleche(g, e.base, W*0.11, col);
    }catch(err){}
  }
  /* ═══ LA TEINTE DE LA DALLE (§1.2) — décision Tom, Q30 ═══
     ZÉRO TON SUR TON, SANS EXCEPTION : la règle prime. Une dalle prend LA TEINTE DE SA
     PALETTE, jamais la couleur pleine du champ sur lequel elle est posée. Mesuré avant
     correction : sur les huit cadres à champ bleu, l'écart de luminosité entre la dalle et
     l'aplat #82AEF8 valait 16 en médiane — le seuil est 42 (CLAUDE.md §3).
     LA FORME NE BOUGE PAS : c'est toujours la vraie dalle du moteur (`Toile.dalleTrame`,
     CLAUDE.md §4, règle 1). On remappe seulement sa LUMINOSITÉ sur la rampe des trois
     teintes du §1.2 — rien n'est inventé, aucun polygone n'est reconstruit.
     Les trois rampes dégagent le seuil par construction : sur bleu (luminosité 91) les
     teintes du Promi donnent 59 · 94 · 135 ; sur framboise (84) le Chiche 82 · 116 · 145 ;
     sur mauve (112) la Nuée 64 · 93 · 124. */
  var DALPAL = {
    promi:  [[0xAE,0x86,0xF2],[0xCB,0xAA,0xFF],[0xE7,0xDA,0xFF]],
    chiche: [[0xF2,0x97,0x7A],[0xFF,0xC0,0xA8],[0xFF,0xE2,0xD2]],
    nuee:   [[0xC2,0xA4,0xF7],[0xDC,0xC6,0xFF],[0xF3,0xEA,0xFF]]
  };
  function teinteDalle(src, nat){
    try{
      var g = src.getContext('2d'); if(!g) return;
      var im = g.getImageData(0,0,src.width,src.height), d = im.data;
      var pal = DALPAL[nat] || DALPAL.promi;
      var mn = 255, mx = 0, i, L;
      for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue;
        L = 0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2];
        if(L<mn) mn=L; if(L>mx) mx=L; }
      var etendue = (mx-mn) || 1;
      for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue;
        L = (0.2126*d[i] + 0.7152*d[i+1] + 0.0722*d[i+2] - mn) / etendue;
        var t = L*2, k = (t<1) ? 0 : 1, f = (t<1) ? t : Math.min(1, t-1);
        var a = pal[k], z = pal[k+1];
        d[i]   = a[0] + (z[0]-a[0])*f;
        d[i+1] = a[1] + (z[1]-a[1])*f;
        d[i+2] = a[2] + (z[2]-a[2])*f;
      }
      g.putImageData(im,0,0);
    }catch(_){ }
  }
  window._ppTeinteDalle = teinteDalle;
  /* ⚑ v29 — la même rampe, donnée au MOTEUR (`dalleTrame(…, opts.rampe)`) : c'est lui qui la peint désormais.
     haut 2 = t = L × 2 sur trois teintes, exactement la formule ci-dessus. */
  window._ppRampe = function(nat){ return {cols:DALPAL[nat] || DALPAL.promi, haut:2}; };

  /* §2.4 — A = (chevron + 32, base + 46) · B = (chevron + 10, base + 14)
     C1 = (A.x − 10, A.y − 4) · C2 = (B.x + 3, B.y + 12) */
  function fleche(g, base, chev, col){
    var ax = chev + 32, ay = base + 46, bx = chev + 10, by = base + 14;
    var c1x = ax - 10, c1y = ay - 4, c2x = bx + 3, c2y = by + 12;
    g.save();
    g.strokeStyle = col; g.lineWidth = 4.5; g.lineCap = 'round'; g.lineJoin = 'round';
    var vx = bx - c2x, vy = by - c2y, L = Math.hypot(vx, vy) || 1; vx /= L; vy /= L;
    /* ⚑ 23 sept. (Tom) — MÊME DÉFAUT, MÊME PARADE : un bout ROND de 4,5 px de large dépasse
       de 2,25 px au-delà du point d'arrivée. La courbe s'arrête donc 2,25 px en deçà, et
       c'est son bout rond qui vient tomber exactement là où les deux ailes se rejoignent. */
    g.beginPath(); g.moveTo(ax, ay);
    g.bezierCurveTo(c1x, c1y, c2x, c2y, bx - vx*2.25, by - vy*2.25); g.stroke();
    function aile(deg){ var r = deg*Math.PI/180;
      return [bx - (vx*Math.cos(r) - vy*Math.sin(r))*13, by - (vx*Math.sin(r) + vy*Math.cos(r))*13]; }
    var g1 = aile(-32), g2 = aile(32);
    g.beginPath(); g.moveTo(g1[0], g1[1]); g.lineTo(bx, by); g.lineTo(g2[0], g2[1]); g.stroke();
    g.restore();
  }
  window._ppTrait = trait;

  /* ═══ LES COTES (§5) ═══ */
  /* ══ LE CRIBLE, ÉCRAN PAR ÉCRAN — NŒUD PAR NŒUD, JAMAIS PAR CONTENEUR. ══
     « Ce que l'inventaire ne liste pas ne se peint pas » vaut pour l'état AU REPOS de
     l'écran courant. Fermer un conteneur d'un coup ferme aussi les panneaux qu'un geste
     déplie — qui sont eux-mêmes des écrans du §5 (cadres 18 à 23) : redteam_verbe est
     tombé à 4/6 comme ça (CLAUDE.md §8). On énumère donc les nœuds de CET écran, on ferme
     ceux-là seulement, et JAMAIS quand un panneau de choix est ouvert. */
  var HORS_INVENTAIRE = [
    '.ph-slots', '.ph-addslot',       /* pastilles d'ajout de créneau : sur aucun cadre */
    '.cs-tenir-hint', '.cs-hint',     /* invites héritées : le mot de trace les remplace */
    '.garde-cote', '[data-gc]', '#addDraft'  /* le lien de brouillon : le nôtre est à 708 */
  ];
  function crible(cs, ouvert){
    HORS_INVENTAIRE.forEach(function(sel){
      cs.querySelectorAll(sel).forEach(function(n){
        /* un panneau de choix est ouvert : on ne ferme plus rien, l'écran courant est
           « Choix ouvert · … » et il a son propre inventaire. */
        n.style.setProperty('display', ouvert ? '' : 'none', 'important');
      });
    });
  }

  function cotes(){
    try{
      var e = ecran(), cs = e.cs;
      if(!cs || !cs.classList.contains('pp')) return;
      crible(cs, e.ouvert);
      cs.classList.remove('pp-promi','pp-chiche','pp-nuee');
      cs.classList.add('pp-'+e.nat);
      cs.classList.toggle('pp-ouvert', !!e.ouvert);
      /* le mot-marque dit la nature qu'on écrit (§5) */
      var mark = cs.querySelector('.cs-mark');
      /* ⚑ v46 (Tom) — on n'écrit le mot QUE s'il change : réécrit à chaque passe, il défaisait la composition du É (lot-V35-E-ACCENT)
         et le composeur, voyant plus de 20 réécritures en 2 s, renonçait — « NUÉE » restait sur le É de Gilbert. */
      var _mot = (e.nat==='chiche') ? 'Chiche' : (e.nat==='nuee' ? 'Cercle' : 'Promi');
      if(mark && mark.getAttribute('data-mot') !== _mot){ mark.textContent = _mot; mark.setAttribute('data-mot', _mot); mark.removeAttribute('aria-label'); }
      /* LE MOT DE TRACE — les mots sont ceux de l'inventaire, un par nature */
      var tr = cs.querySelector('.pp-trace');
      if(!tr){ tr = document.createElement('div'); tr.className = 'pp-trace'; cs.appendChild(tr); }
      /* ══ Q35 · UN SEUL MOT, JAMAIS DEUX (décision Tom) ══
         AU REPOS le mot dit « trace pour planter » pour un Promi et « trace pour lancer »
         pour un Chiche comme pour une Nuée. IL NE CHANGE PAS D'UN CADRE À L'AUTRE :
         l'app en portait DEUX pour la même chose — « trace ta moitié » au repos et
         « trace pour planter » dès qu'un choix s'ouvrait. Et IL DISPARAÎT dès que la
         moitié est tracée : le créneau porte alors l'état du geste, en terracotta.
         ══ Q36 · AUCUN VOCABULAIRE DE SAISON ══ « avant l'été » n'existe pas. Après
         signature, le mot dit une échéance QUE L'APP SAIT PRODUIRE : « À TENIR · <jour> »
         s'il y a une date, « UN JOUR » ou « EN L'AIR » sinon. */
      if(e.etat === 'cours'){
        tr.textContent = 'continue \u2192';
        pose(tr, {left:'160px', top:(e.boite - 46)+'px'});
      } else if(e.etat === 'signe'){
        tr.textContent = motSigne();
        pose(tr, {left:'180px', top:(e.boite - 46)+'px'});
      } else {
        /* ⚠ LE CADRE 2 DIT « TRACE TA MOITIÉ », pas « trace pour planter ». Vu au duo, deux
           thèmes. Les deux mots existent au moodboard et ne disent pas la même chose : sur
           la page + AU REPOS on trace SA moitié — l'autre tracera la sienne (§2.6, mode
           « moitié ») ; sur la REPRISE d'un gardé de côté, le cadre 26 écrit « trace pour
           planter », parce que rien n'a encore été posé. Le mot de la reprise est posé plus
           bas, dans le bloc `pp-garde-mot`, et il gagne : il passe après. Une Nuée garde
           « trace pour lancer » — elle se lance d'un trait entier, personne ne vient à sa
           rencontre (CLAUDE.md §4). */
        tr.textContent = (e.nat === 'promi')
          ? (e.ouvert ? 'trace pour planter' : 'trace ta part')
          : 'trace pour lancer';
        pose(tr, {left:'82px', top:(e.ouvert ? 236 : (e.boite - 60))+'px'});
      }
      cs.classList.toggle('pp-cours', e.etat === 'cours' || e.etat === 'signe');
      cs.classList.toggle('pp-garde', !!e.garde && !e.ouvert);
      /* LA PHRASE — §2.8 : 36 si ≤ 3 lignes, 34 à 4, 30 au-delà ; elle rétrécit tant qu'une
         ligne dépasse 342. L'interligne suit : int(taille × 1,2) + 24. */
      var ph = boitePhrase(e.nat);
      var txt = ph ? ph.querySelector('.ph-txt') : null;
      if(ph && txt){
        /* ⚑ v59 (latences) — ce calcul de taille force la mise en page des dizaines de fois (scrollWidth, getClientRects) et il
           tournait à CHAQUE passe de la page +, à chaque mouvement du doigt pendant le trait : 570 ms de fil principal mesurées
           pendant une plantation. Rien n'a changé depuis la dernière fois (même phrase, mêmes styles, même état, même largeur,
           polices chargées) → on garde le résultat. */
        var _cleP = [e.nat, e.ouvert?1:0, e.nl, e.etat==='plate'?1:0, cs.clientWidth, (document.fonts&&document.fonts.status)||'', txt.style.cssText, txt.innerHTML].join('§');
        if(txt.__phCle !== _cleP){
        /* §2.8 — `taille = min(estimation, mesure)`. (Décision Tom, 18 août 2026 ;
           la « correction du §2.8 » qui remplaçait l'estimation par la mesure est ANNULÉE
           pour de bon.)
           · L'ESTIMATION EST LA RÈGLE DE COMPOSITION — c'est elle qui a dessiné le
             moodboard, et elle redonne les tailles des cadres au caractère près :
             `Σ(caractères × taille × 0,53) + 32 par pastille + 11 par écart`.
           · LA MESURE NE SERT QU'À EMPÊCHER LE DÉBORDEMENT : l'estimation est optimiste
             sur certaines chaînes (« courir dimanche… ») et laisse une ligne passer à la
             ligne — ce qui décale TOUT ce qui suit de 32 px (§2.5).
           On rétrécit donc tant que L'UNE OU L'AUTRE dépasse 342 : c'est la plus petite
           des deux qui gagne. La mesure seule remplissait toujours les 342 et sortait la
           phrase trop grosse. */
        var lignesTx = decoupe(txt);
        function large(t){
          var m = 0;
          for(var i=0;i<lignesTx.length;i++){
            var L = lignesTx[i], w = L.car * t * 0.53 + 32*L.past + 11*Math.max(0, L.mots-1);
            if(w > m) m = w;
          }
          return m;
        }
        /* SUR UN CHOIX OUVERT LA PHRASE PART DE 30, pas de 36 — les trois cadres le
           montrent (30 · 30 · 28 après rétrécissement) et c'est la même logique que
           l'onde qui s'aplatit : le champ est réduit, la phrase suit. Voir Q32. */
        var taille = e.ouvert ? 30 : ((e.nl<=3) ? 36 : (e.nl===4 ? 34 : 30));
        var appli = function(t){
          txt.style.setProperty('font-size', t+'px', 'important');
          txt.style.setProperty('line-height', (Math.floor(t*1.2*(window._echTexte||1))+24)+'px', 'important');   /* ⚑ v102 : la hauteur d'une étiquette, c'est 1,2 × la taille × l'agrandissement des faces (v96) — sans lui, 5 px d'air perdus entre deux lignes de la phrase */
        };
        var mesure = function(t){
          appli(t);
          var av = txt.style.whiteSpace;
          txt.style.setProperty('white-space','nowrap','important');
          var w = txt.scrollWidth;   /* la ligne rendue, jamais l'estimation (§2.8 corrigé) */
          txt.style.removeProperty('white-space'); if(av) txt.style.whiteSpace = av;
          var sc2 = (cs.clientWidth||390)/390;
          return w / (sc2||1);
        };
        /* ⚠ CORRECTION DE LA CORRECTION (mesuré cadre par cadre, pas supposé).
           L'estimation du §2.8 N'EST PAS un pis-aller : c'est ELLE qui a composé le
           moodboard. Elle redonne, au caractère près, les tailles des dix-sept cadres —
           29 · 29 · 31 · 36 · 35 · 33 · 33 · 29 · 28 · 30. La mesure navigateur seule
           donnait 35 · 36 · 35 · 36 · 35 · 32 · 33 · 34 · 30 · 30 : elle remplit toujours
           les 342 px, et la phrase sortait systématiquement trop grosse.
           Mais la mesure reste nécessaire : l'estimation est OPTIMISTE sur certaines
           chaînes (« courir dimanche… ») et laisse une ligne passer à la ligne, ce qui
           décale tout ce qui suit de 32 px (§2.5). ON PREND DONC LA PLUS PETITE DES DEUX :
           l'estimation donne la composition, la mesure garantit qu'aucune ligne ne casse. */
        var mesurable = false;
        try{ mesurable = (mesure(taille) > 0); }catch(_){ mesurable = false; }
        /* ⚑ 23 SEPTEMBRE 2026 (Tom) — LA RÈGLE CHANGE, ET IL FAUT LE DIRE : « dans la page +
           les textes ne sont pas assez gros, on a perdu le côté arty et le côté simple
           intuitif ; quand on avait l'ancienne police c'était pas aussi petit justement. »
           CE QUI EST ABANDONNÉ : l'estimation du §2.8 comme CONTRAINTE. Elle a composé le
           moodboard avec la police de la planche ; depuis le 16 septembre la phrase est en
           Gilbert, plus étroit (coefficient remesuré : 0,44 contre 0,53 — `coef_phrase.py`),
           et elle sur-contraignait de 20 à 40 %. Mesuré avant ce lot : Promi 25 px, Chiche
           18 px, là où la planche compose entre 28 et 36.
           CE QUI LA REMPLACE : la MESURE fait foi, bornée en haut par la taille de départ du
           §2.8 (36 · 34 · 30 selon le nombre de lignes, 30 sur un choix ouvert). La phrase
           est donc la plus grande qui ne casse aucune ligne — jamais plus grosse que ce que
           la planche autorise. L'estimation reste, en REPLI : sans mise en page (un relevé
           hors navigateur), elle est la seule chose qui puisse borner la taille. */
        /* ⚑ v20 (Tom, 22 sept.) — UN EXEMPLE LONG PASSE À LA LIGNE, IL N'ÉCRASE PAS LA PHRASE.
           Les exemples qui tournent (lot-EXEMPLES-V20) faisaient descendre la phrase jusqu'au
           plancher de 16 px — mesuré : 52 exemples sur 80 sous 24 px. On arrête le
           rétrécissement à 28, la plus petite taille composée par la planche (29 · 29 · 31 ·
           36 · 35 · 33 · 33 · 29 · 28 · 30) ; au-delà, SEULE la pastille de l'objet (ou du nom
           de Nuée) passe à la ligne, son contour recopié sur chaque morceau. */
        var PLANCHER_PH = 28, tailleDepart = taille;
        var pmC = txt.querySelector('.ph-m.ph-vide[data-ph="titre"],.ph-m.ph-vide[data-np="nom"]');
        try{ txt.classList.remove('ph-coupe'); if(pmC && pmC.getAttribute('data-plein')) pmC.textContent = pmC.getAttribute('data-plein'); }catch(_){}
        /* ⚑ v46 (Tom) — « LE RESTE RESTE INDEMNE : seule la partie à partir du de / d’ — le mot et la pastille noire —
           rapetisse et s'étale sur deux lignes, trois au plus, puis points de suite ; jamais hors de l'écran, même marge que
           le reste. » La taille de la phrase se calcule donc comme si la parole tapée était courte (son premier mot) : une
           parole longue la faisait tomber au plancher de 16 px, TOUT le reste avec. La pastille est traitée après, seule. */
        var ptL = txt.querySelector('.ph-m[data-ph="titre"]:not(.ph-vide), .ph-m[data-np="nom"]:not(.ph-vide)'), ptOrig = null;
        if(ptL && !ptL.querySelector('*')){
          ptOrig = (ptL.getAttribute('data-ph') === 'titre' && window._phrase && window._phrase.titre) ? String(window._phrase.titre) : ptL.textContent.replace(/\u2026$/, '');
          ptL.style.removeProperty('font-size'); ptL.style.removeProperty('line-height');
          var liL0 = ptL.previousElementSibling; if(liL0 && liL0.classList.contains('ph-li')){ liL0.style.removeProperty('font-size'); liL0.style.removeProperty('line-height'); }
          ptL.textContent = (ptOrig.split(/\s+/)[0] || ptOrig).slice(0, 14);
        } else ptL = null;
        var tSans = taille;
        while(tSans > 16 && (mesurable ? (mesure(tSans) > 342) : (large(tSans) > 342))) tSans -= 1;
        taille = tSans;
        /* au-dessous du plancher, l'EXEMPLE (une pastille vide) se coupe en DEUX morceaux
           équilibrés, entre deux mots — jamais dans un trait d'union — à la plus grande taille
           où une coupe tient. Ce qu'on a tapé ne se coupe jamais : ça reste la règle d'avant. */
        /* dans un CHOIX OUVERT la phrase cède la place au panneau (Q32) : la règle d'avant */
        if(mesurable && tSans < PLANCHER_PH && pmC && !e.ouvert){
          var plein = pmC.getAttribute('data-plein') || pmC.textContent, mots = plein.split(' ');
          var bord = function(){ var R=txt.getBoundingClientRect(), sc3=(cs.clientWidth||390)/390, d=0;
            [].forEach.call(pmC.getClientRects(), function(q){ d=Math.max(d,(q.right-R.left)/sc3); }); return d; };
          var esc2 = function(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); };
          var trouve = null, html3 = function(ks){ var p=[0].concat(ks,[mots.length]), o=[];
              for(var j=0;j<p.length-1;j++) o.push('<span style="white-space:nowrap">'+esc2(mots.slice(p[j],p[j+1]).join(' '))+'</span>');
              return o.join('<br>'); };
          if(mots.length > 1){
            pmC.setAttribute('data-plein', plein); txt.classList.add('ph-coupe');
            for(var tt = tailleDepart; tt >= PLANCHER_PH && !trouve; tt--){
              appli(tt); var best = null;
              for(var kk = 1; kk < mots.length; kk++){
                pmC.innerHTML = '<span style="white-space:nowrap">'+esc2(mots.slice(0,kk).join(' '))+'</span><br><span style="white-space:nowrap">'+esc2(mots.slice(kk).join(' '))+'</span>';
                if(bord() > 342.5) continue;
                var rq=pmC.getClientRects(), rr=[].map.call(rq, function(q){return q.width;});
                var ec = rr.length>=2 ? Math.abs(rr[0]-rr[rr.length-1]) : 1e9;
                /* le premier morceau reste DERRIÈRE « de » : jamais un « de » seul sur sa ligne */
                if(rq.length && (rq[0].left - txt.getBoundingClientRect().left) < 20) ec += 1e6;
                if(!best || ec < best.ec) best = {k:kk, ec:ec};
              }
              if(best && best.ec < 1e6) trouve = {t:tt, ks:[best.k]};
            }
            /* aucune coupe en DEUX ne garde le premier morceau derrière « de » : en TROIS */
            for(var t3 = tailleDepart; t3 >= PLANCHER_PH && !trouve && mots.length > 2; t3--){
              appli(t3); var b3 = null;
              for(var a1=1;a1<mots.length-1;a1++) for(var a2=a1+1;a2<mots.length;a2++){
                pmC.innerHTML = html3([a1,a2]);
                if(bord() > 342.5) continue;
                var q3=pmC.getClientRects(); if(!q3.length || (q3[0].left - txt.getBoundingClientRect().left) < 20) continue;
                var w3=[].map.call(q3,function(q){return q.width;}), e3=Math.max.apply(null,w3.slice(1))-Math.min.apply(null,w3.slice(1));
                if(!b3 || e3 < b3.e) b3 = {ks:[a1,a2], e:e3};
              }
              if(b3) trouve = {t:t3, ks:b3.ks};
            }
          }
          if(trouve){ taille = trouve.t; appli(taille); pmC.innerHTML = html3(trouve.ks); }
          else { txt.classList.remove('ph-coupe'); pmC.textContent = plein; }
        }
        appli(taille);
        if(ptL){
          ptL.textContent = ptOrig;
          ptL.style.setProperty('overflow-wrap','anywhere','important');
          var liL = ptL.previousElementSibling; if(liL && !liL.classList.contains('ph-li')) liL = null;
          var sc4 = (cs.clientWidth||390)/390;
          var lignesDe = function(x){ var t = [], rg = document.createRange(); rg.selectNodeContents(x);   /* les lignes du TEXTE : une bande par ligne */
            [].forEach.call(rg.getClientRects(), function(r){ if(r.width < 1 || r.height < 1) return; var c = (r.top + r.bottom) / 2;
              for(var i=0;i<t.length;i++) if(c > t[i][0] && c < t[i][1]) return; t.push([r.top, r.bottom]); }); return t.length; };
          /* et la HAUTEUR : sous la phrase (et sous l'aide quand elle paraît), il doit rester la rangée du pinceau (44) avec
             20 d'air de chaque côté, avant « garder de côté » ou la barre Peaufiner (760) — sinon la rangée recouvre tout */
          var crS = cs.getBoundingClientRect(), gdS = cs.querySelector('.pp-garder'), aideH = 0;
          var finMax = 760; try{ if(gdS && gdS.offsetParent && getComputedStyle(gdS).display !== 'none') finMax = (gdS.getBoundingClientRect().top - crS.top)/sc4; }catch(_){}
          try{ if(!e.ouvert && e.etat === 'plate' && ph.querySelector('.ph-m.ph-vide')) aideH = 34 + 24; }catch(_){}
          var tient = function(lim){ if(lignesDe(ptL) > lim) return false; var R = txt.getBoundingClientRect(), ok = true;
            [].forEach.call(ptL.getClientRects(), function(q){ if((q.right - R.left)/sc4 > 342.5) ok = false; });
            if(ok && !e.ouvert && (R.bottom - crS.top)/sc4 + aideH + 20 + 44 + 20 > finMax) ok = false;
            return ok; };
          var taillePt = function(t){ [ptL, liL].forEach(function(x){ if(!x) return;
            x.style.setProperty('font-size', t+'px', 'important'); x.style.setProperty('line-height', Math.round(t*1.2)+'px', 'important'); }); };
          if(!tient(2)){
            var fait = false;
            for(var lim = 2; lim <= 3 && !fait; lim++) for(var tp = taille; tp >= 16; tp--){ taillePt(tp); if(tient(lim)){ fait = true; break; } }
            if(!fait){
              taillePt(16);
              for(var limT = 3; limT >= 1; limT--){
                var lo = 0, hi = ptOrig.length;
                while(lo < hi){ var mid = (lo + hi + 1) >> 1; ptL.textContent = ptOrig.slice(0, mid).replace(/\s+$/, '') + '\u2026'; if(tient(limT)) lo = mid; else hi = mid - 1; }
                ptL.textContent = ptOrig.slice(0, lo).replace(/\s+$/, '') + '\u2026';
                if(lo > 0) break;
              }
            }
          }
        }
        try{ txt.__phCle = [e.nat, e.ouvert?1:0, e.nl, e.etat==='plate'?1:0, cs.clientWidth, (document.fonts&&document.fonts.status)||'', txt.style.cssText, txt.innerHTML].join('§'); }catch(_){}
        }
        /* ⚑ v22 — LA COUPE CHANGE LE NOMBRE DE LIGNES APRÈS QUE LES COTES ONT ÉTÉ CALCULÉES (`e.nl`) : la phrase et le mot du
           trait restaient alors 32 px trop bas, selon l'ordre des passes (pris par releve-S3, par intermittence). On
           recalcule les cotes une fois, tout de suite, sur le vrai nombre de lignes. */
        if(!cotes.__encore && lignes(e.nat) !== e.nl){ cotes.__encore = true; try{ cotes(); } finally { cotes.__encore = false; } return; }
        /* la phrase descend de 30 px pendant le geste (424 → 454, §5 cadres 29-30) */
        pose(ph, {top:(e.ouvert ? 280 : (e.boite + (e.etat==='plate' ? 6 : 36)))+'px'});
      }
      /* la ligne d'aide : sa cote est absolue (24 / 574). On la laisse DANS la phrase et on
         la décale — la déplacer sur le cadre en laissait une copie à chaque rendu (compté
         1 → 2 → 4). Les copies égarées sont retirées. */
      cs.querySelectorAll(':scope > .ph-hint').forEach(function(x){ x.parentNode.removeChild(x); });
      var hint = ph ? ph.querySelector('.ph-hint') : null;
      /* la Nuée n'a pas de ligne d'aide dans son inventaire : celle de l'autre boîte de
         phrase, restée dans le DOM, se montrait par-dessus (collision relevée par le juge). */
      cs.querySelectorAll('.ph-hint').forEach(function(x){
        if(x !== hint) x.style.setProperty('display','none','important'); });
      /* L'AIDE ET LE LIEN S'EXCLUENT — c'est la logique du moodboard : « phrase vide » porte
         l'aide à 574 sans lien, les écrans remplis portent le lien à 708 sans aide. Ils se
         recouvraient (constaté au duo). */
      /* L'AIDE NE SE MONTRE JAMAIS QUAND UN PANNEAU DE CHOIX EST OUVERT : aucun des trois
         cadres « Choix ouvert » ne la porte, et elle recouvrait le panneau (mesuré : aide à
         611, panneau à 591). L'écran courant est « Choix ouvert · … », son inventaire ne la
         liste pas. */
      /* ⚑ Tom, 14 sept. 2026 : « c'est une notice, la phrase se comprend sans — on découvre Peaufiner en l'ouvrant ». Le Chiche
         n'a plus d'aide ; le Promi garde seulement « touche ⇄ pour changer d'intention ». */
      /* ⚑ 17 sept. 2026 (Tom) : LE CHICHE RETROUVE SON AIDE. « Retirer l'aide répare le
         mensonge mais laisse l'écran muet là où les deux autres parlent. » La décision du
         14 septembre (« le Chiche n'a plus d'aide ») est levée POUR LUI SEUL ; la condition
         `e.nat!=='chiche'` tombe, le reste de la règle ne bouge pas. */
      var vide = !e.ouvert && e.etat==='plate' && !!(ph && ph.querySelector('.ph-m.ph-vide'));
      if(hint) hint.style.setProperty('display', vide ? 'block' : 'none', 'important');
      if(hint && txt && vide){
        /* LE MOT DU MOODBOARD (§5, décision Tom) : l'app disait « touche Je me promets pour
           changer d'engagement ». Les mots viennent du document. */
        /* la phrase entière du cadre 2 — et sa troisième clause est désormais VRAIE :
           l'échéance a bien rejoint la Nuée dans Peaufiner (S3/Q28). */
        /* LE MOT DE CHAQUE CADRE, NATURE PAR NATURE (§5) — le Chiche n'a pas la même
           aide que le Promi : son cadre écrit « le compagnon et l'échéance sont dans
           Peaufiner ». On prend le mot du moodboard, on ne le généralise pas. */
        /* ⚑ 17 sept. 2026 (Tom), 2.4 et 3.6 du relevé de l'identité verbale.
           Le Chiche : « un Chiche se lance, il ne se retourne pas » — et c'est VRAI, sa
           bascule ⇄ n'existe pas (le code renvoie sans rien faire). L'ancienne aide du Promi
           mentait sur lui. Le Promi : « Je promets se retourne — touche-le », qui nomme le
           verbe au lieu du symbole. Mesuré : 231,8 px et 205,2 px dans 342. */
        var mot = (e.nat === 'chiche')
          ? 'un Chiche se lance, il ne se retourne pas'
          : ((window._phrase && window._phrase.sens === 'demander')
              ? 'promets-moi se retourne \u2014 touche\u2011le'
              : ((window._phrase && window._phrase.faireAutre)
                  ? 'Je promets se retourne \u2014 touche\u2011le'
                  : 'Je me promets se retourne \u2014 touche\u2011le'));   /* v96 : le texte a grandi (+12 %) — le trait d'union ne coupe plus « touche-le » (U+2011) */
        if(hint.textContent.trim() !== mot) hint.textContent = mot;
        /* sa cote : 34 px sous la phrase. Sur l'écran à DEUX lignes de l'inventaire, la
           phrase finit à 540 et l'aide tombe à 574 — la cote du document. Avec trois
           lignes elle suit, au lieu de recouvrir la troisième (constaté en capture). */
        /* ⚠ offsetHeight, pas getBoundingClientRect : quand .frame est mise à l'échelle, le rectangle
           est réduit et clientWidth ne l'est pas — l'aide remontait sur « avec qui ? » (12 sept. 2026). */
        pose(hint, {top:(txt.offsetHeight + 34)+'px'});
      }
      try{ if(window._pinceauRangee) window._pinceauRangee(); }catch(_){}
      /* « garder de côté » — le lien de l'app, à sa cote. On ne crée pas une fonction :
         on rebranche celle qui existe. */
      var g = cs.querySelector('.pp-garder');
      if(!g){
        g = document.createElement('div'); g.className = 'pp-garder';
        g.textContent = 'garder de côté';
        g.addEventListener('click', function(ev){ ev.stopPropagation();
          var b = document.querySelector('#addDraft,#csDraft,#csGarder,[data-garder],.cs-draft');
          if(b) b.click(); }, true);
        cs.appendChild(g);
      }
      /* le geste : posé en absolu sur le CADRE. Aucun ancêtre positionné ne s'intercale —
         c'est la parade du piège #tenirCv, appliquée d'emblée (CLAUDE.md §8). */
      /* aucun des trois cadres « Choix ouvert » ne porte le lien : l'inline bat la feuille,
         c'est donc ici qu'il faut le fermer, pas en CSS. */
      /* ni pendant le geste (cadres 29-30) ni sur un choix ouvert : l'inline bat la feuille */
      /* le lien disparaît dès que le doigt trace : ni le cadre 29 ni le cadre 30 ne le
         portent. C'est `e.etat !== 'plate'` qu'il faut lire, pas le seul « cours ». */
      if(g) g.style.setProperty('display', (vide || e.ouvert || e.etat!=='plate') ? 'none' : 'block', 'important');
      /* CADRE 27 · « Gardé de côté · après » : le mot d'état à 24 / 558, Apfel 500 / 12.5,
         interlettre .20em, dans la COULEUR PLEINE de la nature. Le mot de trace devient
         « trace pour planter » — rien n'est promis tant qu'on n'a pas tracé. */
      var gm = cs.querySelector('.pp-garde-mot');
      if(e.garde && !e.ouvert){
        if(!gm){ gm = document.createElement('div'); gm.className = 'pp-garde-mot';
          gm.textContent = 'GARDÉ DE CÔTÉ · RIEN N\u2019EST PROMIS'; cs.appendChild(gm); }
        gm.style.setProperty('display','block','important');
        /* ⚠ IL SE POSE SOUS LA PHRASE, PAS À UNE COTE FIGÉE — c'est l'écran que Tom a
           photographié : le mot touchait presque la pastille. Mesuré sur le cadre 26,
           l'air vaut **23 px** entre le bas de la pastille (« aller voir la mer », 47 de
           haut) et le haut du mot ; l'app n'en laissait que **9**, parce que sa pastille
           n'a pas la hauteur du dessin et que le `top:558px` du §5 ne le savait pas.
           On garde l'AIR du cadre et la cote suit la pastille : à hauteur égale, le mot
           retombe à 558 au pixel. La pastille est la DERNIÈRE ligne de la phrase — on
           prend son bas réel, jamais une hauteur devinée. */
        try{
          var _ph = cs.querySelector('.pp-phrase') || cs.querySelector('#csPhrase');
          var _last = null;
          if(_ph) _ph.querySelectorAll('.ph-m, .ph-b, .ph-o').forEach(function(n){
            var q = getComputedStyle(n);
            if(q.display==='none' || q.visibility==='hidden') return;
            var rr = n.getBoundingClientRect();
            if(!_last || rr.bottom > _last) _last = rr.bottom;
          });
          if(_last){
            var _dev = document.getElementById('device').getBoundingClientRect();
            var _sc = (_dev.width||390)/390;
            gm.style.setProperty('top', Math.round((_last - _dev.y)/_sc + 23) + 'px', 'important');
          }
        }catch(_){}
        if(tr && e.etat !== 'cours') tr.textContent = 'trace pour planter';
      } else if(gm){ gm.style.setProperty('display','none','important'); }
      /* ⚠ LE ROND PHOTO SUIT LE MÊME SORT QUE LE MOT — et c'est ICI qu'on le décide, dans
         les cotes, qui passent EN DERNIER sur chaque repeinte de la page +. Posé plus tôt
         (dans `poseBouton`, ou au site d'appel), le refus se faisait écraser par une passe
         suivante et le rond revenait : mesuré trois fois au duo, thème clair. Un gardé de
         côté n'a pas d'aplat (Q83) : le rond y perd son fond et sort en cercle vide, et les
         cadres 26/27 n'en portent aucun. */
      cs.querySelectorAll('.ph-photo-nid').forEach(function(n){
        n.style.setProperty('display', (e.garde && !e.ouvert) ? 'none' : 'block', 'important'); });
      ['planterZone','planterZoneN','planterZoneD'].forEach(function(id){
        var pz = document.getElementById(id);
        if(pz) pose(pz, {top:(e.base - 59)+'px'});
      });
      panneau(cs, e, ph);
    }catch(err){}
  }
  window._ppCotes = cotes;

  /* ══ LES TROIS CADRES « CHOIX OUVERT » (§5) ══
     Le panneau vit DANS #csPhrase, qui est déjà posé en absolu sur le cadre : ses cotes
     sont donc relatives au haut de la phrase (280). On ne le sort pas de son parent —
     le déplacer en laissait une copie à chaque rendu, la leçon de la ligne d'aide. */
  function panneau(cs, e, ph){
    var z = ph ? ph.querySelector('#csChoix') : null;
    cs.classList.remove('pp-saisie');
    if(!z || !e.ouvert){ return; }
    var haut = 280;                                   /* le haut de la phrase, cadre 18-23 */
    /* le panneau se cale sur le haut de la phrase : ses cotes du §5 sont donc absolues. */
    z.style.setProperty('top','0','important');
    var inp = z.querySelector('#phIn');
    var opts = z.querySelector('.ph-opts');
    /* ⚠ SOUS LA PHRASE, JAMAIS DESSUS (13 sept. 2026). 486 et 420 sont les cotes d'une phrase de DEUX lignes
       (elle finit à 390). Le Chiche en a quatre (fin à 514) : la grille recouvrait « avec qui ? ». La cote se
       dérive du bas réel des pastilles — 32 d'air sous la phrase pour la grille (celui du panneau d'une Nuée,
       454 → 486), 30 pour « DÉJÀ PROMIS » (celui du cadre, 390 → 420). */
    var finPh = 0;
    try{ var prr = ph.getBoundingClientRect(), kk = (document.getElementById('device').getBoundingClientRect().width/390)||1;
      [].forEach.call(ph.querySelectorAll('.ph-txt > .ph-m, .ph-txt > .ph-b'), function(x){
        var r = x.getBoundingClientRect(); if(r.height) finPh = Math.max(finPh, haut + (r.bottom - prr.top)/kk); });
    }catch(_){}
    if(opts){
      /* la grille des personnes : première ligne à 486 (§5) */
      opts.style.setProperty('position','absolute','important');
      opts.style.setProperty('top', (Math.max(486, Math.round(finPh + 32)) - haut)+'px', 'important');
      opts.style.setProperty('left','0','important');
      /* L'INITIALE (§5) : un cercle de 28 devant le prénom. On l'ajoute une fois. */
      opts.querySelectorAll('.ph-o').forEach(function(b){
        if(b.classList.contains('ph-add')){
          /* LE MOT DU CADRE : « + ajouter quelqu'un », pas un « + » seul (§5, décision Tom
             sur les mots du moodboard). */
          if(b.textContent.trim() !== '+ ajouter quelqu’un') b.textContent = '+ ajouter quelqu’un';
          return;
        }
        if(b.querySelector('.ppo-ini')) return;
        var nom = (b.getAttribute('data-v')||b.textContent||'').trim();
        var ini = document.createElement('span'); ini.className = 'ppo-ini';
        ini.textContent = nom.charAt(0).toUpperCase();
        b.insertBefore(ini, b.firstChild);
      });
    }
    if(inp){
      /* « écrire un mot » : le champ est la pastille ; l'entrée garde le focus, invisible.
         § 2.11 — la barre Peaufiner est masquée pendant la saisie. */
      cs.classList.add('pp-saisie');
      /* DÉJÀ PROMIS (§5) : le libellé à 420, deux pastilles à 446 (24 et 201).
         Les mots viennent des promesses RÉELLES — jamais inventés (CLAUDE.md §9). */
      var lab = z.querySelector('.ppo-deja');
      if(!lab){ lab = document.createElement('div'); lab.className = 'ppo-deja';
        lab.textContent = 'DÉJÀ PROMIS'; z.appendChild(lab); }
      var dec = Math.max(0, Math.round(finPh + 30) - 420);
      lab.style.setProperty('top', (420 + dec - haut)+'px', 'important');
      var row = z.querySelector('.ppo-dejarow');
      if(!row){ row = document.createElement('div'); row.className = 'ppo-dejarow'; z.appendChild(row); }
      row.style.setProperty('top', (446 + dec - haut)+'px', 'important');
      var mots = [];
      try{
        var cour = ((window._phrase && window._phrase.titre) || '').trim();
        promises.slice().reverse().forEach(function(q){
          var t = (q && q.title || '').trim();
          if(t && t !== cour && mots.indexOf(t) < 0 && mots.length < 2) mots.push(t);
        });
      }catch(_){}
      if(row.getAttribute('data-mots') !== mots.join('|')){
        row.setAttribute('data-mots', mots.join('|'));
        row.innerHTML = '';
        mots.forEach(function(m, i){
          var b = document.createElement('span'); b.className = 'ppo-d'; b.textContent = m;
          /* la seconde pastille commence à 201 (§5) : l'écart se calcule, il n'est pas figé */
          b.addEventListener('click', function(ev){ ev.stopPropagation();
            try{ var f = document.getElementById('phIn'); if(f){ f.value = m;
              f.dispatchEvent(new Event('input', {bubbles:true})); } }catch(_){ }
          }, true);
          row.appendChild(b);
        });
        row.style.setProperty('gap','21px','important');
        /* LES MOTS SONT CEUX DE L'UTILISATEUR, pas ceux du cadre : ils peuvent être plus
           longs. Deux pastilles qui ne tiennent pas dans les 342, c'est un débordement —
           on n'en garde qu'une. Le cadre en montre deux parce que les siens sont courts. */
        while(row.children.length > 1 && row.scrollWidth > 342) row.removeChild(row.lastChild);
      }
    } else {
      var l0 = z.querySelector('.ppo-deja'), r0 = z.querySelector('.ppo-dejarow');
      if(l0) l0.parentNode.removeChild(l0);
      if(r0) r0.parentNode.removeChild(r0);
    }
  }

  /* ═══════════════════════════════════════════════════════════════════════════════════
     LE PEAUFINER DE LA PAGE + — le MÊME bloc que la fiche (section 2), mêmes libellés,
     même ordre, mêmes cotes. Les briques viennent de `window._s2Briques` : on les emprunte,
     on ne les recrée pas. Les CONTRÔLES viennent de l'app (`#fWho`, `#dueChips`,
     `#nueeChips`, `#fNote`, `#csFiles`…) : ils sont DÉPLACÉS, jamais dupliqués — c'est ce
     que fait `emprunte()` / `rentre()`, et c'est pourquoi le plantage continue de les lire.
     PAS D'ICÔNE PARTAGER (§3.2) : la barre de la page + n'en porte pas, et n'en portera pas.
     ⚠ Aucun conteneur de cette page n'est l'ancêtre de #planterZone — parade #tenirCv.
     ═══════════════════════════════════════════════════════════════════════════════════ */
  function nomNuee(){
    try{ if(typeof selNuee!=='undefined' && selNuee) return (NUE[selNuee]||selNuee); }catch(_){}
    return 'aucune';
  }
  function motEcheance(){
    /* la valeur affichée est celle que l'app a retenue — lue sur SA prise, jamais sur un
       libellé (CLAUDE.md §8, chantier 56). */
    try{ var c = document.querySelector('#dueChips .chip.on'); if(c) return c.textContent.trim(); }catch(_){}
    try{ return (window._phrase && window._phrase.quand) || 'un jour'; }catch(_){ return 'un jour'; }
  }
  /* Q36 — LE MOT DE L'ÉTAT, APRÈS SIGNATURE. Aucune saison, aucun mot inventé : on lit
     l'échéance que l'app a retenue et on la dit telle quelle. */
  function motSigne(){
    var m = (motEcheance()||'').trim();
    if(!m || /un jour/i.test(m)) return 'UN JOUR';
    if(/en l/i.test(m)) return 'EN L\u2019AIR';
    return '\u00c0 TENIR \u00b7 ' + m.toUpperCase();
  }
  function aQui(){
    try{ var P = window._phrase||{};
      if(P.qui && P.qui!=='Moi' && P.qui!=='moi') return P.qui; }catch(_){}
    return 'moi';
  }
  function peaufTete(cs, titre){
    var B = window._s2Briques;
    var t = B.el('div','s2-tete');
    var a = B.el('div','s2-titre'); a.textContent = titre || '';
    var f = B.el('div','s2-fermer'); f.textContent = '\u2715 FERMER';
    /* ✕ FERMER ferme la page +, comme partout ailleurs sur cet écran */
    f.addEventListener('click', function(ev){ ev.stopPropagation();
      var c = cs.querySelector('.closeb'); if(c) c.click(); }, true);
    t.appendChild(a); t.appendChild(f);
    return t;
  }
  function peaufBati(){
    try{
      var cs = document.getElementById('createSheet'); if(!cs) return;
      var B = window._s2Briques; if(!B) return;
      var e = ecran(), n = e.nat;
      var corps = cs.querySelector(':scope > .dpd-corps');
      if(!corps){ corps = B.el('div','dpd-corps'); cs.appendChild(corps); }
      var liste = corps.querySelector('.s2-liste');
      if(!liste){ liste = B.el('div','s2-liste'); corps.appendChild(liste); }
      /* ⚑ CHANTIER 70 — COMPARER AVANT D'AGIR (CLAUDE §8). `tout()` repasse ici à chaque repeinte (les minuteries du pinceau
         0/120/400/900/1800 ms, après chaque clic 80/260/600 ms, l'observateur de classe) et la liste était VIDÉE PUIS REBÂTIE
         à chaque fois, sans que rien n'ait changé : mesuré, six zones neuves en 2,5 s, et un toucher sur l'encart du mur perdu
         quand le nœud était remplacé entre l'appui et le relâcher (2 sur 40, chantier 70). On calcule la SIGNATURE de ce qu'on
         va bâtir — nature, titre, à qui, échéance, Nuée, fichiers, compagnon, membres — et on ne rebâtit que si elle change,
         ou si un contrôle emprunté n'est plus dans la liste (il a été rendu à l'app à la fermeture). */
      var _P = window._phrase || {}, _sig = '';
      try{
        _sig = JSON.stringify([n, (_P.titre||'').trim(), (n==='nuee'?((document.getElementById('nName')||{}).value||''):''),
          (n!=='nuee'?aQui():''), (n!=='nuee'?motEcheance():''), ((n!=='nuee'&&n!=='chiche')?nomNuee():''), (_P.avec||''),
          ((document.getElementById('csFiles')||{}).childElementCount||0), (window.newNueeMembers||[]).join('|'),
          ((document.getElementById('nFirstList')||{}).childElementCount||0)]);
      }catch(_){ _sig = ''; }
      /* la Nuée n'emprunte plus #nMembers (lot-GENS) : son témoin est le choix des personnes qu'on y a posé */
      var _pris = (n === 'nuee') ? (liste.querySelector('.gn') || document.getElementById('nMembers')) : document.getElementById('fNote');
      if(_sig && liste.getAttribute('data-pp-sig') === _sig && liste.firstChild && _pris && liste.contains(_pris)) return;
      liste.setAttribute('data-pp-sig', '');
      /* tout contrôle emprunté rentre chez lui AVANT qu'on vide la liste : sans ça,
         innerHTML='' détruirait #fNote et #csFiles (la leçon de la section 2). */
      B.rentre(liste);
      liste.innerHTML = '';
      var P = window._phrase || {};
      var mot = {promi:'Promi', chiche:'Chiche', nuee:'Cercle'}[n] || 'Promi';
      var titre = (P.titre||'').trim();
      if(n==='nuee'){ try{ titre = (document.getElementById('nName')||{}).value || ''; }catch(_){ titre=''; } }
      liste.appendChild(peaufTete(cs, titre || mot));

      if(n === 'nuee'){
        /* PEAUFINER NUÉE (page +) : ce que la Nuée a AVANT d'être lancée. Les mots sont
           ceux de l'app (« Avec qui », « Les Promi de la Nuée »), l'ordre celui de la fiche. */
        var mem = '';
        try{ var L = window.newNueeMembers||[];
             mem = L.length ? (L.slice(0,2).join(' \u00b7 ') + (L.length>2?(' \u00b7 +'+(L.length-2)):''))
                            : 'personne encore'; }catch(_){ mem='personne encore'; }
        liste.appendChild(B.reg('MEMBRES', mem, {hote:(window._gensPage ? window._gensPage('nuee') : B.emprunte('nMembers'))}));
        liste.appendChild(B.reg('INVITER', '\u2192', {hote:B.emprunte('nInvite')}));
        var np = 0; try{ np = (document.getElementById('nFirstList')||{}).childElementCount||0; }catch(_){}
        liste.appendChild(B.reg('LES PROMI DU CERCLE', np+' Promi', {hote:B.emprunte('nFirst')}));
        liste.setAttribute('data-pp-sig', _sig);
        return;
      }

      var chiche = (n === 'chiche');
      var qui = (aQui()!=='moi') ? aQui() : null;
      var mv  = qui ? ('visible par '+qui) : 'priv\u00e9e \u2014 visible par toi seul';
      var mvs = qui ? ('visibles par '+qui) : 'priv\u00e9es \u2014 visibles par toi seul';
      /* 1 · à qui */
      /* ⚑ « JE ME PROMETS » EST À SOI : pas de « à qui » (Tom, 13 sept. 2026). Les personnes passent par lot-GENS. */
      var _soi = !chiche && P.sens === 'faire' && !P.faireAutre && /^(moi)?$/i.test(String(P.qui||'').trim());
      if(!_soi) liste.appendChild(B.reg(chiche?'\u00c0 QUI JE LANCE':'\u00c0 QUI', aQui(), {hote:(window._gensPage ? window._gensPage('qui') : B.emprunte('fWho'))}));
      /* 2 · le compagnon d'un Chiche — vide, il prend le contour pointillé (§3.3) */
      if(chiche) liste.appendChild(B.reg('AVEC', (P.avec||'personne'), {cls:(P.avec?'':'s2-vide'), hote:(window._gensPage ? window._gensPage('avec') : null)}));
      /* 3 · l'échéance — le contrôle de l'app, déplacé et non recréé */
      liste.appendChild(B.reg('AVANT', motEcheance(), {hote:B.emprunte('dueChips')}));
      /* 4 · la Nuée — un Chiche n'en a pas dans l'inventaire */
      if(!chiche) liste.appendChild(B.reg('DANS UN CERCLE', nomNuee(), {hote:B.emprunte('nueeChips')}));
      /* 5 · la note (§3.4, zone de 118) */
      liste.appendChild(B.zone('NOTE', B.emprunte('fNote'), mv));
      /* 6 · les pièces jointes */
      var nf = 0; try{ nf = (document.getElementById('csFiles')||{}).childElementCount||0; }catch(_){}
      liste.appendChild(B.reg('PI\u00c8CES JOINTES', nf+' fichier'+(nf>1?'s':''),
        {cls:'s2-vis2', vis:mvs, hote:B.emprunte('csFiles')}));
      liste.setAttribute('data-pp-sig', _sig);
      /* 7 · les deux réglages propres à la création. Ce sont des FONCTIONS de l'app :
         on ne les retire pas (CLAUDE.md §9), on les habille. */
      /* la valeur est celle que l'app a retenue, lue sur SA prise (`.is.on`) */
      var lu = function(id){ try{ var x=document.querySelector('#'+id+' .is.on');
        return x ? x.textContent.trim() : ''; }catch(_){ return ''; } };
      /* ⚠ « URGENT » NE REVIENT PAS (décision Tom) : le concept est abandonné, et l'app le
         savait déjà — l. 9705, « Urgent supprimé », suivi d'une règle qui masque #urgSeg.
         J'avais pris ce masquage pour un oubli de portage. Voir CLAUDE.md §9. */
    }catch(err){}
  }
  window._ppPeaufBati = peaufBati;

  function peaufOuvre(v){
    var cs = document.getElementById('createSheet'); if(!cs) return;
    if(v){ peaufBati(); cs.classList.add('pp-peauf','s2-ouv');
           /* les trois éléments que `cotes()` pose EN INLINE (l'inline bat la feuille,
              CLAUDE.md §8) : on les ferme ici, un par un, jamais par un balai. */
           ['.pp-garder','.pp-garde-mot','.pp-trace'].forEach(function(s){
             var x = cs.querySelector(s); if(x) x.style.setProperty('display','none','important'); });
           var c = cs.querySelector(':scope > .dpd-corps'); if(c) c.scrollTop = 0; }
    else { cs.classList.remove('pp-peauf','s2-ouv');
           /* on REND leur display aux trois éléments fermés à l'ouverture : `cotes()`
              repose leurs cotes mais pas leur display, et le mot de trace ne revenait pas. */
           ['.pp-garder','.pp-garde-mot','.pp-trace'].forEach(function(s){
             var x = cs.querySelector(s); if(x) x.style.removeProperty('display'); });
           var l = cs.querySelector(':scope > .dpd-corps .s2-liste');
           /* on REND ses contrôles à l'app avant de refermer : ils doivent retrouver leur
              place dans le formulaire, sinon le plantage ne les lit plus. */
           if(l && window._s2Briques) window._s2Briques.rentre(l);
           tout(); }
    var ch = cs.querySelector('#csBotBar .cbb-chev');
    if(ch) ch.textContent = v ? '\u25b4' : '\u25be';
  }
  window._ppPeaufOuvre = peaufOuvre;

  /* ── « CHOISIR → » : l'appel de chaque carte (§5). Le mot est celui de l'inventaire ; on
       l'ajoute une fois par carte, jamais à chaque passe. Les dalles sont peintes par le
       moteur (`renderTileIcons`), on ne les touche pas. ── */
  function natures(){
    try{
      var cs = document.getElementById('createSheet'); if(!cs) return;
      cs.querySelectorAll('.tiles .tile').forEach(function(t){
        if(!t.querySelector('.pp-choisir')){
          var a = document.createElement('div'); a.className = 'pp-choisir';
          a.textContent = 'CHOISIR \u2192';
          t.appendChild(a);
        }
      });
      if(window.renderTileIcons){ renderTileIcons(); setTimeout(window.renderTileIcons, 220); }
    }catch(_){ }
  }
  window._ppNatures = natures;

  function peaufBranche(){
    var bar = document.getElementById('csBotBar'); if(!bar || bar._pp) return;
    bar._pp = true;
    bar.addEventListener('click', function(ev){
      var cs = document.getElementById('createSheet');
      if(!cs || !cs.classList.contains('pp')) return;
      peaufOuvre(!cs.classList.contains('pp-peauf'));
      ev.stopPropagation();
    }, true);
  }

  function tout(){ try{
    var cs = document.getElementById('createSheet');
    if(cs && cs.classList.contains('pp-peauf')){ peaufBati(); return; }
    cotes(); trait();
    /* §10.6 · l'entête suit ce qui est peint sous lui — la matière remplit le champ, et
       elle peut passer sous le mot-marque. Une seule construction dans le produit. */
    if(cs && window._enteteLisible) window._enteteLisible('csTrameCv', cs, ['.cs-mark','.closeb']);
  }catch(e){} }
  window._ppTout = tout;

  /* les trois cartes du cadre 17 : le mot « CHOISIR → » est celui de l'inventaire, et la
     dalle de chaque carte est repeinte à sa nouvelle boîte (§4 · peindre après insertion). */
  function cartes(cs){
    try{
      /* LE CADRE COUPE LA QUESTION TOUT SEUL — « Qu'est-ce que tu / promets ? ». Le <br>
         codé en dur de l'app la coupait après « Qu'est-ce » et la faisait tomber sur TROIS
         lignes. On le remplace par une ESPACE : masquer le <br> collait les deux mots. */
      cs.querySelectorAll('#csQuest br').forEach(function(br){
        br.parentNode.replaceChild(document.createTextNode(' '), br); });
      cs.querySelectorAll('.tiles-track .tile').forEach(function(t){
        if(!t.querySelector('.pp-choisir')){
          var c = document.createElement('div'); c.className = 'pp-choisir';
          c.textContent = 'CHOISIR \u2192'; t.appendChild(c);
        }
      });
      if(!cs._ppCartesPeint){ cs._ppCartesPeint = 1;
        [0, 60, 200, 600].forEach(function(d){
          setTimeout(function(){ try{ if(window.renderTileIcons) renderTileIcons(); }catch(_){ } }, d); });
      }
    }catch(_){}
  }

  /* la page + s'arme quand une nature est choisie — l'écran « Choix des trois natures »
     est le seul des 17 qui montre la question et les tuiles. */
  function arme(){
    var cs = document.getElementById('createSheet'); if(!cs) return;
    var ouvert = cs.classList.contains('show');
    var forme = false;
    /* ⚑ v21 — L'ÉTAT EST CE QUE LE CODE POSE, JAMAIS UNE GÉOMÉTRIE (§8). « Nature choisie » se lisait dans la
       HAUTEUR RENDUE du formulaire (> 2 px) : un minuteur qui passait pendant un repli momentané remettait la page +
       sur les tuiles — mesuré, 131 ms d'écran des tuiles 770 ms après l'ouverture d'un Promi. `data-kind` est posé
       par la tuile et retiré par l'écran de choix (lot 5) : c'est lui l'état. */
    try{ forme = !!cs.getAttribute('data-kind'); }catch(e){}
    if(!ouvert && cs.classList.contains('pp-peauf')) peaufOuvre(false);
    /* « CHOIX DES TROIS NATURES » (cadre 17) : la feuille est ouverte, aucune nature n'est
       encore choisie — c'est l'écran de la question et des trois cartes. */
    var choix = ouvert && !forme;
    if(cs.classList.contains('pp-choix') !== choix) cs.classList.toggle('pp-choix', choix);
    if(choix) natures();
    /* ⚑ v21 — la page + GARDE SA MISE EN PAGE PENDANT QU'ELLE GLISSE hors de l'écran : retirer `pp` dès la
       fermeture faisait repasser l'ancienne en-tête (`cs-top`, `cs-mid`) ~200 ms sur la feuille qui s'en va. */
    if(!ouvert && cs._ouvertAvant){ cs._fermeT=performance.now(); setTimeout(arme, 620); }
    cs._ouvertAvant = ouvert;
    var doit = (ouvert && forme) || (!ouvert && cs.classList.contains('pp') && cs._fermeT && performance.now()-cs._fermeT < 600);
    if(cs.classList.contains('pp') !== doit) cs.classList.toggle('pp', doit);
    /* CADRE 17 — la page + ouverte avant qu'une nature soit choisie : la question et les
       trois cartes, rien d'autre. C'est un écran du §5, pas un en-tête de formulaire. */
    var choix = ouvert && !forme;
    if(cs.classList.contains('pp-choix') !== choix) cs.classList.toggle('pp-choix', choix);
    if(choix) cartes(cs);
    if(doit && ouvert) tout();   /* v60 (rythme) : une page + qui glisse hors de l'écran garde sa mise en page, mais ne se REPEINT plus — c'était ~180 ms (dalle et trait) pile quand la dalle plantée arrive */
  }
  window._ppArme = arme;
  try{ var _csO=document.getElementById('createSheet'); if(_csO){ var _vu=_csO.classList.contains('show');
    new MutationObserver(function(){ var o=_csO.classList.contains('show'); if(o===_vu) return; _vu=o; arme(); })
      .observe(_csO,{attributes:true,attributeFilter:['class']}); } }catch(_){}
  document.addEventListener('click', function(){ setTimeout(arme,60); setTimeout(arme,340); }, true);
  peaufBranche(); setInterval(peaufBranche, 800);
  document.addEventListener('input', function(ev){
    if(ev.target && ev.target.closest && ev.target.closest('#createSheet')) setTimeout(tout,40);
  }, true);
  ['resize','orientationchange'].forEach(function(ev){ window.addEventListener(ev, tout); });
  setInterval(arme, 500);
})();
