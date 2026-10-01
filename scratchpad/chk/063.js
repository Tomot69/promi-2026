
/* ⚑ LE STUDIO · LA TOILE PLEIN ÉCRAN ET DEUX PLATEAUX — la pose.

   CE QUI EST DÉPLACÉ, JAMAIS REFAIT (§9 : aucune fonction ne disparaît) :
     · #stBg        le canevas du monde        → la Toile, bord à bord, 390 × 844
     · .closeb      ✕ Fermer                   → dans le plateau du haut
     · .st3-wn      le nom du monde            → sur la Toile, 46 px (#stpNom)
     · .st3-dot     les huit points            → rangée fine du plateau (#stpDots)
     · .st3-hint    « glisse pour changer… »   → invite qui meurt (#stpInv)
     · .st3-pals    les palettes du moteur     → dépliées au besoin (#stpPals)
     · .st3-spec    la jauge de teinte         → avec elles
     · #thToggle    sombre / clair             → la paire de disques (#stpVue)
     · #txToggle    le texte des dalles        → la paire de disques (#stpVue)
     · #stLockBuy   l'adoption à 1 €           → sur la Toile, au-dessus du plateau
     · #stLockCta   l'offre du Cercle          → encart §3.8 sur les réglages floutés
   Les DISQUES ne remplacent pas les bascules : ils les CLIQUENT. Le comportement reste
   celui de l'app, on ne déplace que la forme.

   ⚠ LES QUATRE TONS SONT CEUX DU MOTEUR. `Toile.palettes()[getPalette()].cols` — dix
   palettes nommées plus un décalage de teinte, relus à chaque pose. La loi
   « mère / écart / éclat » de la maquette n'existe pas dans le produit (Q130).

   ⚠ ON POSE `_shAllColored` AVANT DE RENDRE LA TOILE. Sans lui, `Toile.preview` ne teinte
   que ~12 graines groupées dans un coin — c'est l'aperçu d'une Toile à quinze Promi, et
   c'est ce que le Studio montrait jusqu'ici (Q132). Le moteur porte le drapeau, et
   `shareRender()` s'en sert déjà.

   ⚠ ON ENVELOPPE `buildStudio` (§8) : il reconstruit `#studioBody` de lui-même. Un lot qui
   ne repose sa mise en page qu'aux événements du doigt perd la main dès qu'il est appelé
   d'ailleurs. */
(function(){
  var W=390, H=844;
  function $(s,r){return (r||document).querySelector(s);}
  function $$(s,r){return [].slice.call((r||document).querySelectorAll(s));}
  function T(){try{return window.Toile;}catch(e){return null;}}
  function clair(){try{return !!document.querySelector('.frame.light,.device.light,#device.light');}catch(e){return false;}}
  function hex(c){return '#'+c.map(function(v){return ('0'+(v|0).toString(16)).slice(-2);}).join('');}

  /* §8 · un `.screen` ne coïncide pas avec `#device` : on cale le cadre à la mesure.

     ⚠ MAIS ON NE MESURE PAS PENDANT LA TRANSITION D'OUVERTURE. Un `.screen` arrive de
     sous l'écran : tant que sa translation n'est pas finie, `sc.top` vaut ~880 pendant que
     `#device.top` vaut ~53, et le cadre se cale à **−823**. Vu à l'écran : le Studio sort
     entièrement vide, tout étant posé 860 px trop haut. Le garde est une plausibilité —
     le décalage attendu vaut quelques dizaines de pixels, jamais des centaines — et on
     REFUSE de caler tant qu'on n'y est pas. */
  /* ⚠ LE CADRE SE CALE SUR LA GÉOMÉTRIE DE MISE EN PAGE, PAS SUR L'ÉCRAN RENDU.
     C'est la correction du saut à l'ouverture (Tom, 1er septembre 2026 : « la page saute
     vers le haut puis revient, c'est pas fluide, hyper cheap »). La cause était à moi :
     `getBoundingClientRect()` mesure APRÈS transformation, or un `.screen` arrive de sous
     l'appareil. Tant que la translation courait, la mesure était fausse et je refusais de
     caler ; à la fin de la transition je calais d'un coup — et tout le contenu SAUTAIT de
     16 px. Le garde évitait le faux placement, il ne pouvait pas éviter le saut.
     `offsetWidth` et `offsetHeight`, eux, sont des cotes de MISE EN PAGE : ils ignorent
     les transformations. Le décalage se déduit donc immédiatement, dès le premier rendu,
     et il ne bouge plus jamais. Plus de mesure différée, plus de saut, aucun garde. */
  function cale(){
    try{
      var sc=$('#studioScreen'), cd=$('#stpCadre');
      if(!sc||!cd) return false;
      var ow=sc.offsetWidth, oh=sc.offsetHeight;
      if(!ow||!oh) return false;
      cd.style.left=((ow-W)/2).toFixed(2)+'px';
      cd.style.top =((oh-H)/2).toFixed(2)+'px';
      return true;
    }catch(e){ return false; }
  }

  function bati(){
    var sc=$('#studioScreen'); if(!sc) return null;
    sc.classList.add('st-plat');
    var cd=$('#stpCadre');
    if(cd) return sc;
    cd=document.createElement('div'); cd.id='stpCadre';
    sc.insertBefore(cd, sc.firstChild);

    /* la Toile passe dans le cadre, en fond */
    var bg=document.getElementById('stBg'); if(bg) cd.appendChild(bg);

    /* le plateau du haut : le mot-marque et FERMER */
    var ph=document.createElement('div'); ph.id='stpHaut';
    var t=document.createElement('div'); t.className='stp-t'; t.textContent='Le Studio';
    ph.appendChild(t);
    var cb=sc.querySelector(':scope > .closeb'); if(cb) ph.appendChild(cb);
    cd.appendChild(ph);

    /* le nom du monde, sur la Toile */
    var nm=document.createElement('div'); nm.id='stpNom'; cd.appendChild(nm);

    /* le plateau du bas, et ses trois rangées */
    var pb=document.createElement('div'); pb.id='stpBas'; cd.appendChild(pb);
    var tn=document.createElement('div'); tn.id='stpTons'; cd.appendChild(tn);
    var lb=document.createElement('div'); lb.id='stpLab'; cd.appendChild(lb);
    var vu=document.createElement('div'); vu.id='stpVue'; cd.appendChild(vu);
    var dt=document.createElement('div'); dt.id='stpDots'; cd.appendChild(dt);
    var iv=document.createElement('div'); iv.id='stpInv'; cd.appendChild(iv);

    /* le rail des palettes et la jauge — dépliés au besoin */
    var pl=document.createElement('div'); pl.id='stpPals'; cd.appendChild(pl);

    /* l'adoption : les deux nœuds de l'app, déplacés tels quels */
    var lk=document.getElementById('stLock'); if(lk) cd.appendChild(lk);
    return sc;
  }

  /* les quatre disques de vue : ils CLIQUENT les bascules de l'app, ils ne les remplacent pas */
  function poseVue(){
    var vu=$('#stpVue'); if(!vu) return;
    var th=document.getElementById('thToggle'), tx=document.getElementById('txToggle');
    var thL=th?th.querySelector('[data-th="light"]'):null, thD=th?th.querySelector('[data-th="dark"]'):null;
    var txOn=tx?tx.querySelector('[data-tx="on"]'):null, txOff=tx?tx.querySelector('[data-tx="off"]'):null;
    var estClair=clair();
    var mots=!!(txOn&&txOn.classList.contains('on'));
    /* ⚑ v95 (Tom : « 56 éléments reconstruits à chaque toucher du Studio — corrige-la, c'est un défaut en soi ») — chaque toucher au
       Studio repassait `poser()`, qui rebâtissait les disques, les tons, les points et l'invite. On compare avant d'écrire (§8) : l'état,
       ET l'identité des bascules de l'app que les disques cliquent (buildStudio peut les avoir recréées). */
    var sigV=estClair+'|'+mots; if(vu.__sig===sigV && vu.__cib===thL && vu.__cib2===txOn && vu.childNodes.length) return;
    vu.__sig=sigV; vu.__cib=thL; vu.__cib2=txOn;
    vu.innerHTML='';
    function disque(fond, actif, cible, barres){
      var d=document.createElement('div'); d.className='stp-d'+(actif?' on':'');
      if(fond) d.style.background=fond;
      if(barres){[18,23,13].forEach(function(w){var b=document.createElement('div');
        b.className='stp-bar'; b.style.width=w+'px'; d.appendChild(b);});}
      d.onclick=function(){ if(cible) cible.click(); setTimeout(poser,60); };
      vu.appendChild(d);
    }
    disque('#201908', !estClair, thD, false);
    var e1=document.createElement('div'); e1.className='stp-in'; vu.appendChild(e1);
    disque('#F7F0DE',  estClair, thL, false);
    var sep=document.createElement('div'); sep.className='stp-sep'; vu.appendChild(sep);
    disque(null,  mots, txOn,  true);
    var e2=document.createElement('div'); e2.className='stp-in'; vu.appendChild(e2);
    disque(null, !mots, txOff, false);

    /* ⚠ UN MOT PAR PAIRE — CELUI QUI EST CHOISI, et il change au doigt.
       Quatre mots sous quatre disques ne tiennent pas : « avec texte » mesure 75 px pour
       les 64 disponibles entre deux disques d'une paire, ils se chevaucheraient. Le mot
       de la paire dit donc l'état COURANT — « sombre » ou « clair », « avec texte » ou
       « sans texte » — et il est centré sur la paire, sur 108 px : la largeur exacte de
       deux disques et de leur écart. Ce sont les mots de `#thToggle` et `#txToggle`. */
    var lb=$('#stpLab'); if(!lb) return;
    lb.innerHTML='';
    [ (estClair?'clair':'sombre'), (mots?'avec texte':'sans texte') ].forEach(function(m,i){
      var d=document.createElement('div'); d.className='stp-l'; d.textContent=m;
      lb.appendChild(d);
      if(i===0){var s=document.createElement('div');s.className='stp-lsep';lb.appendChild(s);}
    });
  }

  function poseTons(){
    var tn=$('#stpTons'); if(!tn) return;
    var t=T(); if(!t||!t.palettes||!t.getPalette) return;
    var P=t.palettes()[t.getPalette()]; if(!P||!P.cols) return;
    var sigT=P.cols.map(hex).join(','); if(tn.__sig===sigT && tn.childNodes.length) return; tn.__sig=sigT;   /* v95 : on compare avant d'écrire */
    tn.innerHTML='';
    P.cols.forEach(function(c){
      var d=document.createElement('div'); d.className='stp-ton';
      d.style.background=hex(c);
      d.onclick=function(){ var sc=$('#studioScreen'); if(sc) sc.classList.toggle('stp-pals'); };
      tn.appendChild(d);
    });
  }

  function poseDots(){
    var dt=$('#stpDots'); if(!dt) return;
    var src=$$('#studioBody .st3-dot');
    var sigD=src.length+'|'+src.map(function(s){ return s.classList.contains('on')?1:0; }).join('');
    if(dt.__sig===sigD && dt.__src0===src[0] && dt.childNodes.length===src.length) return;   /* v95 : même rangée, mêmes points de l'app */
    dt.__sig=sigD; dt.__src0=src[0];
    dt.innerHTML='';
    src.forEach(function(s){
      var d=document.createElement('div');
      d.className='stp-dot'+(s.classList.contains('on')?' on':'');
      d.onclick=function(){ s.click(); setTimeout(poser,60); };
      dt.appendChild(d);
    });
    /* ⚑ v74 (Tom, capture) — LES POINTS RESTENT DANS L'ENCART. La rangée a été dessinée pour huit mondes (écart 13) ; à vingt elle
       faisait 432 px dans un encart de 342 et sortait des deux côtés. Elle tient dans l'encart (24 → 366) à la marge des pastilles de
       palette (22 px), et l'écart se CALCULE sur le nombre de points (jamais une mesure) : 13 au plus. */
    var n=src.length, larg=342-2*22, pts=9*Math.max(0,n-1)+14, gap=n>1?Math.min(13,(larg-pts)/(n-1)):0;
    dt.style.setProperty('left',(24+22)+'px','important'); dt.style.setProperty('width',larg+'px','important');
    dt.style.setProperty('gap',Math.max(2,gap).toFixed(2)+'px','important');
  }

  /* ⚑ v47 (Tom, deuxième demande) — LE NOM SUR TROIS LIGNES : « Esquille » tel quel · « en » en dessous, plus petit, sans
     gras · « Ingénu » en dessous, même traitement. Gilbert n'a qu'une graisse : les deux lignes du bas sont en Atkinson 400
     (la police du texte). Le nom de la palette est celui du moteur (PALS[clé].name) ; il suit le geste de couleur. */
  function poseNom(){
    var nm=$('#stpNom'); if(!nm) return;
    var wn=$('#studioBody .st3-wn'), monde=wn ? (wn.textContent||'').trim() : '', pal='';
    try{ var T0=window.Toile, P0=T0&&T0.palettes&&T0.palettes(), k0=T0&&T0.getPalette&&T0.getPalette(); pal=(P0&&P0[k0]&&P0[k0].name)||''; }catch(_){ }
    var esc=function(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;'); };
    var html='<span class="stp-m">'+esc(monde)+'</span>'+(pal?'<span class="stp-en">en</span><span class="stp-p">'+esc(pal)+'</span>':'');
    if(nm.getAttribute('data-nom')!==monde+'|'+pal){ nm.innerHTML=html; nm.setAttribute('data-nom',monde+'|'+pal); }   /* on compare avant d'écrire (§8) */
  }
  try{ var _opc=window.onPaletteChange; window.onPaletteChange=function(){ var r; try{ if(_opc) r=_opc.apply(this,arguments); }finally{ try{ poseNom(); }catch(_){ } } return r; }; }catch(_){ }

  function posePals(){
    var pl=$('#stpPals'); if(!pl) return;
    var pals=$('#studioBody .st3-pals'), spec=$('#studioBody .st3-spec');
    /* ⚑ DÉFAUT D'ORIGINE, trouvé le 17 septembre 2026 en comptant les nœuds rendus.
       `buildStudio()` reconstruit `#studioBody` à chaque ouverture ; `posePals` DÉPLAÇAIT la
       rangée neuve dans `#stpPals` SANS retirer l'ancienne. Mesuré sur `app.html` : 1, 2, 3
       puis 4 rangées après quatre ouvertures — 10, 20, 30, 40 pastilles. Avec les vingt
       palettes, la note est quadruplée. On retire ce qui n'est plus rattaché à `#studioBody`. */
    /* ⚠ et on ne nettoie QUE si une rangée neuve arrive : appelée alors que rien n'a été
       reconstruit, `pals` est nul et un nettoyage sec vide le panneau — mesuré, 0 pastille. */
    if(pals && pals.parentNode!==pl){
      [].slice.call(pl.querySelectorAll('.st3-pals')).forEach(function(v){
        if(v!==pals){ try{ v.parentNode.removeChild(v); }catch(_){ } } });
    }
    if(spec && spec.parentNode!==pl){
      [].slice.call(pl.querySelectorAll('.st3-spec')).forEach(function(v){
        if(v!==spec){ try{ v.parentNode.removeChild(v); }catch(_){ } } });
    }
    if(pals && pals.parentNode!==pl) pl.appendChild(pals);
    /* ⚑ 17 sept. : le NOM de la palette suit la rangée. Sans ça il reste dans #studioBody,
       qui fait 1 × 1 px une fois les plateaux posés — le nom existait et ne se voyait pas. */
    var pnom=document.getElementById('st3pn');
    if(pnom && pnom.parentNode!==pl) pl.appendChild(pnom);
    if(pnom && spec && spec.parentNode===pl) pl.insertBefore(pnom, spec);
    if(spec && spec.parentNode!==pl) pl.appendChild(spec);
  }

  /* l'invite : elle meurt dès que SON geste a été fait une fois */
  var CLE='promi_studio_glisse';
  function vue(){ try{return localStorage.getItem(CLE)==='1';}catch(e){return true;} }
  function poseInv(){
    var iv=$('#stpInv'), sc=$('#studioScreen'); if(!iv||!sc) return;
    var h=$('#studioBody .st3-hint');
    var mot=(h&&h.textContent)?h.textContent.replace(/[‹›]/g,'').trim():'glisse pour changer de monde';
    if(iv.__mot!==mot){ iv.__mot=mot; iv.innerHTML='<i>‹</i>'+mot+'<i>›</i>'; }   /* v95 : on compare avant d'écrire */
    sc.classList.toggle('stp-inv', !vue());
  }
  function inviteFaite(){ try{localStorage.setItem(CLE,'1');}catch(e){} var sc=$('#studioScreen'); if(sc)sc.classList.remove('stp-inv'); }

  /* ⚠ LA TOILE MONTRE LE MONDE AFFICHÉ, PAS LE MONDE ACTIF. Sur un monde VERROUILLÉ,
     `Toile.curWorld()` reste sur le dernier monde possédé : l'écran vendait « Gravure » en
     montrant la matière d'Encre. On lit donc le monde du POINT ACTIF (`.st3-dot[data-w]`),
     qui est celui que le nom annonce. « On doit voir ce qu'on n'a pas, sinon l'adoption ne
     veut rien dire » (Tom, 1er septembre 2026). */
  function mondeAffiche(){
    var d=$('#studioBody .st3-dot.on');
    var k=d?d.getAttribute('data-w'):null;
    if(k) return k;
    var t=T(); return (t&&t.curWorld)?t.curWorld():'encre';
  }
  /* ⚠ LA TOILE NE SE RESÈME QU'AU CHANGEMENT DE MONDE. `Toile.preview` sème avec
     `Math.random()` : appelé à chaque `poser()` — donc à chaque doigt levé, et cinq fois
     de suite à l'ouverture — il recomposait la Toile ENTIÈRE à chaque fois. C'était ça,
     « l'animation ultra violente » : pas une animation, un clignotement de compositions.
     On mémorise le monde peint et on ne repeint que s'il a changé. Au changement de monde,
     l'app appelle déjà `Toile.repaintWorld` qui GARDE les germes : c'est doux par
     construction. */
  var _mondePeint=null;
  /* ⚑ v44 (24 sept.) — ON NE PEINT PAS UN STUDIO QUI N'EST PAS À L'ÉCRAN. Le `transitionend` de #studioScreen remonte de
     TOUTE transition de ses descendants : à une plantation, il appelait `poser()` Studio fermé, qui repeignait `#stBg` et
     lançait 1,1 s de frémissement — sur un canevas invisible, 40 à 64 ms par image au ralenti ×4, en pleine tirée de la Toile
     (trouvé par le minutage des rappels). Le Studio est à l'écran s'il porte `.show` (le critère que `frame()` emploie
     déjà) ; son ouverture repeint de toute façon (`poseToile(true)` à l'observateur). */
  function _studioVu(){ var s=document.getElementById('studioScreen'); return !!(s&&s.classList.contains('show')); }
  function poseToile(force){
    var bg=document.getElementById('stBg'); var t=T();
    if(!bg||!t||!t.preview) return;
    if(!_studioVu()) return;
    var m=mondeAffiche();

    /* ⚠ ON NE SÈME QU'UNE FOIS PAR OUVERTURE. Semer, c'est composer une AUTRE Toile ;
       le faire à chaque monde donnerait le même clignotement qu'à chaque doigt levé. */
    if(force || !bg.__c){
      try{
        bg.width=W*window._toileDPR(); bg.height=H*window._toileDPR();   /* ⚑ v16 : la densité de la Toile */
        var av=window._shAllColored;
        window._shAllColored=true;               /* Q132 — sinon ~12 dalles dans un coin */
        bg.__vif=true; bg.__fam=null;            /* v75 : l'aperçu vit — et chaque ouverture repart d'un semis neuf, dans les deux familles */
        t.preview(bg, m, W, H);
        window._shAllColored=av;
        _mondePeint=m; anime();
      }catch(e){}
      return;
    }

    /* ⚠ AU CHANGEMENT DE MONDE, LES GERMES NE BOUGENT PAS. `setW` appelle déjà
       `Toile.repaintWorld(#stBg, monde)` : mêmes graines, mêmes places, matière neuve.
       On se contente de le constater et de faire frémir — c'est le geste doux voulu.
       (On rappelle `repaintWorld` par sécurité : si le monde a changé autrement que par
       `setW` — au premier rendu, ou après un `buildStudio` extérieur — il faut que la
       matière suive le nom affiché.) */
    if(m!==_mondePeint){
      try{ if(t.repaintWorld) t.repaintWorld(bg, m); }catch(e){}
      _mondePeint=m; anime();
    }
  }

  /* ⚑ LE FRÉMISSEMENT — celui de la Toile, pas celui de l'onboarding.

     L'app en a DEUX, et ils n'ont rien à voir :
       · `Toile_previewLive` découpe le rendu dans un BLOB qui ondule (`AMP = rx·0,05`)
         — c'est l'aperçu de l'onboarding, et c'est l'effet que Tom appelle « horrible » ;
       · `_quiv`, dans la boucle de la Toile, déplace CHAQUE GRAINE de quelques dixièmes
         de pixel, amorti en exponentielle. C'est celui-là qu'on veut.
     On reprend ses constantes telles quelles — rien d'inventé : durée 1100 ms (850 sur les
     mondes en grille), enveloppe `exp(-âge/380)` (300 en grille), amplitude 7 px en x et
     5 px en y, le tout multiplié par `window._liveAmp`, que l'app fixe à **0,07**. Soit un
     déplacement de l'ordre du demi-pixel : à peine discernable, et c'est voulu.
     Le rendu passe par `Toile.repaint(bg)`, qui relit `px/py` sur les graines mémorisées —
     on ne touche donc pas au moteur, on l'utilise. */
  /* ⚑ v75 (Tom, 27 sept.) — L'APERÇU S'ANIME. Une dalle arrive, repart, en boucle, au rythme de celebration-mondes : c'est le
     moteur de la Toile qui la fait vivre (`Toile.apercuImage`), une image à la fois, sur ce seul canevas — on ne regarde qu'un monde,
     le coût reste celui d'une Toile. Il remplace le frémissement (celui-ci reste nommé : `_studioFremir`).
     TOUT S'ARRÊTE quand on quitte le Studio (le ✕ lui retire `.show`), quand l'onglet se cache, ou quand une autre couche le couvre
     (on le lit AU DOIGT, `elementFromPoint` au centre, une image sur vingt — `#auraScreen` ne perd jamais `.show`, une classe ne dit
     pas qui est dessus). */
  var _araf=0, _anN=0, _anCouv=0;
  function _couvert(bg){ try{ var r=bg.getBoundingClientRect(); if(!r.width) return true; var el=document.elementFromPoint(r.left+r.width/2, r.top+r.height*0.45);
    var sc=document.getElementById('studioScreen');
    /* ⚑ v89 (Tom) : « ouvrir le Studio referme l'onboarding — on n'est plus dans l'accueil guidé ». Si ce qui recouvre l'aperçu est
       l'onboarding, on le termine au lieu de s'arrêter (l'onboarding non terminé figeait tous les aperçus). */
    var ob=document.getElementById('promiOnb'); if(el&&ob&&ob.contains(el)&&sc&&sc.classList.contains('show')&&window._onbTerminer){ window._onbTerminer(); el=document.elementFromPoint(r.left+r.width/2, r.top+r.height*0.45); }
    return !(el&&sc&&sc.contains(el)); }catch(_){ return false; } }
  function _arrete(bg,t){ _araf=0; try{ bg.__vif=false; t.apercuArret(bg); }catch(_){} }
  function anime(){
    if(_araf) return;
    var bg=document.getElementById('stBg'), t=T();
    if(!bg||!t||!t.apercuImage||!bg.__c) return;
    if(!_studioVu()||document.hidden) return;
    bg.__vif=true; _anN=0;
    if(_fraf){ cancelAnimationFrame(_fraf); _fraf=0; }
    (function pas(now){
      if(!_studioVu()||document.hidden){ _arrete(bg,t); return; }
      if((_anN++%20)===0&&_couvert(bg)){ _arrete(bg,t); clearTimeout(_anCouv); _anCouv=setTimeout(function(){ if(_studioVu()&&!_couvert(bg)) anime(); else if(_studioVu()) _anCouv=setTimeout(arguments.callee,500); },500); return; }
      var tDeb=performance.now();
      t.apercuImage(bg,now);
      if(_anN>2) prepare(bg,t,tDeb);
      _araf=requestAnimationFrame(pas);
    })(performance.now());
  }
  /* ⚑ v75 — CE QUI SE PRÉPARE D'AVANCE, et seulement dans le temps qui reste à l'image : l'image visible d'abord ; si elle a pris moins
     de 10 ms, 6 ms au plus pour préparer l'arrivée de Ramage et de Volubilis (les deux seuls mondes qui ne savent pas la montrer tout de
     suite) ; puis, une fois, le semis de l'autre famille — un saut par les points d'une famille à l'autre retrouve un semis préparé. */
  var LOURDS=['ramage','volubilis'];
  /* ⚑ v89 — la préparation ne travaille que quand l'aperçu est IMMOBILE : sous WebKit sa rastérisation se paie après son budget, et
     pendant un mouvement elle retardait une image sur deux — Madrure avançait en dents de scie (mesuré : 15 · 8,6 · 13 · 3,9 · 12,7
     niveaux d'une image à l'autre ; sans elle, une montée lisse). */
  var _prepPh=null, _prepT0=0;
  function prepare(bg,t,tDeb){ if(!t.apercuPrepare||!bg.__c) return;
    /* v89 : Ramage affiché et immobile — il prépare l'événement tiré d'avance (une image lente sur un aperçu immobile ne se voit pas) */
    if(bg.__c.th==='ramage'&&t.apercuPrepareProchain){ var cy0=bg.__c.cy, lim=window._ramBouge?12:(cy0&&cy0.prem&&cy0.n===1)?34:30;   /* v91 : la lecture du film ne coûte qu'une image posée — le prochain se prépare AUSSI pendant la pousse */   /* v90 : l'aperçu est immobile pendant cette préparation — 24 ms ne se voient pas */   /* v90 : le premier événement attend, rien ne bouge — un budget plus large */
      var r2=lim-(performance.now()-tDeb); if(r2>2) t.apercuPrepareProchain(bg,Math.min(lim-2,r2)); return; }
    /* v91 (Tom : « tous les mondes au même intervalle ») — Ramage prépare son premier événement (plumage et film) DÈS l'ouverture du Studio,
       quel que soit le monde affiché, par petites tranches (5 ms) : quand on arrive sur lui, sa pousse part tout de suite */
    if(bg.__c.th!=='ramage'){ var r3=10-(performance.now()-tDeb); if(r3>2){ var p3=performance.now(); if(!(window._apercuClair||{})[bg.__c.th]&&t.apercuCompose&&!(bg.__fam&&bg.__fam.clair)) t.apercuCompose(bg,'ramage'); else t.apercuPrepare(bg,'ramage',Math.min(5,r3)); _prepT.ramage=(_prepT.ramage||0)+(performance.now()-p3); } }   /* fait : elle rend vrai tout de suite (c.prep) */
    if(window._apPhase!==_prepPh){ _prepPh=window._apPhase; _prepT0=performance.now(); } if(performance.now()-_prepT0<4000) return;
    var cur=bg.__c.th, cl=!!(window._apercuClair||{})[cur];
    if(!cl&&t.apercuCompose&&!(bg.__fam&&bg.__fam.clair)){ if(performance.now()-tDeb<8) t.apercuCompose(bg,'ramage'); return; }
    for(var i=0;i<LOURDS.length;i++){ var m=LOURDS[i]; if(m===cur) continue; var reste=10-(performance.now()-tDeb); if(reste<2) return;
      var p0=performance.now(), ok=t.apercuPrepare(bg,m,Math.min(6,reste)); _prepT[m]=(_prepT[m]||0)+(performance.now()-p0); if(!ok) return; } }
  var _prepT={}; window._studioPrepT=function(){ return _prepT; };
  document.addEventListener('visibilitychange',function(){ if(!document.hidden) setTimeout(anime,0); });
  window._studioAnime=anime;
  window._studioAnimeEtat=function(){ var bg=document.getElementById('stBg'), t=T(); return {vit:!!_araf, etat:(t&&t.apercuEtat)?t.apercuEtat(bg):null}; };
  var _fraf=0;
  function fremis(){
    if(!_studioVu()) return;   /* v44 */
    var bg=document.getElementById('stBg'), t=T();
    if(!bg||!bg.__c||!t||!t.repaint) return;
    var S0=bg.__c.seeds; if(!S0||!S0.length) return;
    var monde=bg.__c.th;
    var grille=(monde==='pixel'||monde==='mosaique'||monde==='braille'||
                monde==='sillons'||monde==='gravure');
    var DUR=grille?850:1100, TAU=grille?300:380, AX=grille?11:7, AY=grille?8:5;
    var LA=(window._liveAmp!=null)?window._liveAmp:1;
    for(var i=0;i<S0.length;i++){
      if(S0[i].ph==null){ S0[i].ph=(i*2.399963); S0[i].am=0.6+((i*0.6180339887)%1)*0.7; }
    }
    var t0=(window.performance&&performance.now)?performance.now():0;
    if(_fraf) cancelAnimationFrame(_fraf);
    (function pas(){
      var age=((window.performance&&performance.now)?performance.now():0)-t0;
      var vif=age<DUR, env=Math.exp(-age/TAU);
      for(var k=0;k<S0.length;k++){
        var s=S0[k];
        if(vif){
          s.px=s.x+Math.sin(age*0.0092+s.ph)*AX*s.am*env*LA;
          s.py=s.y+Math.cos(age*0.0096+s.ph)*AY*s.am*env*LA;
        } else { s.px=s.x; s.py=s.y; }
      }
      try{ t.repaint(bg); }catch(e){}
      _fraf = vif ? requestAnimationFrame(pas) : 0;
    })();
  }

  function poser(){
    var sc=bati(); if(!sc) return;
    cale();
    sc.classList.toggle('stp-clair', clair());
    /* ⚠ `window._lockedWorld` N'EST JAMAIS EFFACÉ. `setW` fait `if(_locked)
       window._lockedWorld=order[ni]` — il l'écrit quand c'est verrouillé et ne le remet
       jamais à null. Le lire, c'est faire passer PAYANT tout monde visité après un monde
       payant : le bug relevé par Tom. L'app maintient en revanche correctement la classe
       `world-locked` sur l'écran (elle est basculée dans les deux sens) : c'est ELLE qui
       dit l'état. On la lit, et on ne touche pas à `setW`. */
    sc.classList.toggle('stp-verrou', sc.classList.contains('world-locked'));
    var _mA=mondeAffiche(); if(sc.getAttribute('data-stp-monde')!==_mA) sc.setAttribute('data-stp-monde', _mA);   /* v63 : le flou du verrou se règle par monde (Houle, Taille-douce en clair) */
    poseNom(); poseTons(); poseVue(); poseDots(); posePals(); poseInv();
    poseToile();          /* ne fait rien si le monde n'a pas changé */
    anime();              /* v75 : ne fait rien si l'aperçu vit déjà */
  }

  /* §8 · buildStudio reconstruit #studioBody : on l'enveloppe, on ne l'écoute pas */
  function enveloppe(){
    if(window.buildStudio && !window.buildStudio.__plat){
      var f=window.buildStudio;
      window.buildStudio=function(){ var r=f.apply(this,arguments);
        requestAnimationFrame(poser); setTimeout(poser,80);
        /* ⚑ v25 (Tom, 22 sept.) — ET LA TOILE AUSSI : `buildStudio` PEINT `#stBg` lui-même
           (`Toile.preview(bg,cur,…)`, l. 6768) — SANS `_shAllColored`. Il reste alors ~13
           cellules colorées dans un coin, le défaut que Q132 avait justement réglé. Le semis
           juste ne rejouait pas, parce qu'il est accroché à l'OBSERVATEUR DE `.show` — et
           `#studioScreen` NE PERD JAMAIS cette classe (mesuré : `.show` encore posée après
           `closeAll`, comme `#auraScreen`). Dès la DEUXIÈME ouverture, 14 cellules sur 72.
           §7 : deux propriétaires pour une même propriété — on en nomme UN, et on lui donne
           LE DERNIER MOT. `poseToile` repasse derrière `buildStudio`, toujours. */
        _mondePeint=null; setTimeout(function(){ poseToile(true); }, 0);
        return r; };
      window.buildStudio.__plat=true;
    }
  }

  document.addEventListener('pointerup', function(e){
    try{ if(e.target.closest && e.target.closest('#studioScreen')) { inviteFaite(); setTimeout(poser,60); } }catch(_){}
  }, true);
  window.addEventListener('resize', function(){ setTimeout(poser,40); });

  /* ⚠ ON RECALE À L'OUVERTURE, et on COMPARE AVANT D'AGIR (§8 : un observateur qui se
     déclenche lui-même fait ramer l'app). L'ouverture ajoute `.show` ; la transition dure,
     donc on repose sur plusieurs délais jusqu'à ce que `cale()` accepte. */
  try{
    var _sc0=document.getElementById('studioScreen');
    if(_sc0){
      var _vu=_sc0.classList.contains('show');
      new MutationObserver(function(){
        var m=_sc0.classList.contains('show');
        if(m===_vu) return;                 /* rien n'a changé : on ne réveille rien */
        _vu=m;
        if(m){
          _mondePeint=null;
          setTimeout(function(){ poseToile(true); },0);   /* on sème UNE fois, à l'ouverture */
          [0,90,240,520,900].forEach(function(d){setTimeout(poser,d);});
        }
      }).observe(_sc0,{attributes:true,attributeFilter:['class']});
      _sc0.addEventListener('transitionend',function(){ poser(); });
    }
  }catch(_){}

  /* ⚠ §8 · UN ROTATEUR RÉÉCRIT `#stBuyTx` AU HASARD — vu à l'écran : « Nouvelle trame ?
     — 1 € » à la place de « Adopte ce design — 1 € ». On le fige par un observateur QUI
     COMPARE AVANT D'AGIR : sans la comparaison, l'écriture réveille l'observateur, qui
     réécrit, qui se réveille — c'est le piège du MutationObserver qui s'auto-déclenche. */
  var MOT='Adopte ce design — 1 €';
  try{
    var _tx=document.getElementById('stBuyTx');
    if(_tx){
      var _fige=function(){ if(_tx.textContent!==MOT) _tx.textContent=MOT; };
      _fige();
      new MutationObserver(_fige).observe(_tx,{childList:true,characterData:true,subtree:true});
    }
  }catch(_){}

  enveloppe();
  [0,80,260,700,1600].forEach(function(d){ setTimeout(function(){ enveloppe(); poser(); }, d); });
  /* ⚠ ON SUIT LE NOM DU MONDE, PAS LES GESTES. `setW` est locale à `buildStudio` : on ne
     peut pas l'envelopper. Mais elle met toujours `.st3-wn` à jour — c'est le nœud que
     l'app tient pour dire quel monde est affiché. On l'observe, en COMPARANT avant d'agir
     (§8), et le lot suit alors TOUS les chemins : le glissement, le clic sur un point, et
     tout appel extérieur à `setW`. Sans ça, un chemin non prévu laisse le nom et les
     points sur l'ancien monde pendant que la matière a déjà changé. */
  try{
    var _obsNom=null, _dernierNom=null;
    var _suisNom=function(){
      var wn=$('#studioBody .st3-wn');
      if(!wn || wn===_obsNom) return;
      _obsNom=wn; _dernierNom=wn.textContent;
      new MutationObserver(function(){
        var v=wn.textContent;
        if(v===_dernierNom) return;      /* rien n'a changé : on ne réveille rien */
        _dernierNom=v; poser();
      }).observe(wn,{childList:true,characterData:true,subtree:true});
    };
    _suisNom();
    [200,700,1500].forEach(function(d){setTimeout(_suisNom,d);});
    var _bs=window.buildStudio;
    if(_bs){ window.buildStudio=function(){ var r=_bs.apply(this,arguments);
      setTimeout(_suisNom,20); return r; }; window.buildStudio.__plat=true; }
  }catch(_){}

  window._studioPlateaux=poser;
  /* ⚠ LE FRÉMISSEMENT SE MESURE, IL NE SE REGARDE PAS : un demi-pixel amorti sur une
     seconde n'est pas jugeable à l'œil sur une capture. L'app publie déjà ce qu'elle
     compose pour ses juges (`Toile_probe`, `_plancheComp`, `_noyauSig`) — on fait pareil.
     `_studioFremir()` le relance, `_studioFremiSonde()` rend le déplacement courant. */
  window._studioFremir=fremis;
  window._studioFremiSonde=function(){
    var bg=document.getElementById('stBg');
    if(!bg||!bg.__c||!bg.__c.seeds) return null;
    var S0=bg.__c.seeds, n=0, som=0, mx=0;
    for(var i=0;i<S0.length;i++){
      var s=S0[i]; if(s.px==null) continue;
      var d=Math.sqrt((s.px-s.x)*(s.px-s.x)+(s.py-s.y)*(s.py-s.y));
      if(d>0.001){ n++; som+=d; if(d>mx) mx=d; }
    }
    return {graines:S0.length, bougees:n, moyen:n?som/n:0, max:mx, monde:bg.__c.th};
  };
})();
