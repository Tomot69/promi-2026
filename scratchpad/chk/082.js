
(function(){
  /* ⚑ v34 (Tom) : « elle vend ce qu'elle montre » — les SIX mondes payants, et eux seuls
     ⚑ v55 (Tom, 25 sept.) — RENVERSÉ : « la Toile de l'écran du Cercle doit montrer plus de mondes — même nombre de dalles, mais une
     plus grande variété de matières ». Les treize. */
  /* ⚑ v74 (Tom, 27 sept.) — « on ne prend là que des dalles de mondes normalement payants, pour donner envie — même densité, même
     placement, juste le choix des dalles ». Les douze du Cercle ; les couches et le nombre de poses ne bougent pas. */
  var CADW=346, CADH=206, MONDES=['sillons','gravure','terrazzo','bobinette','ritournelle','madrure','chantourne','ramage','volubilis','guingois','chamade','mascaret'];
  var NGERMES=460, PART_COL=1, PERIODE=4500, MUE=900, CASC=420;
  /* ⚑ DEUX FOIS PLUS DE DALLES, ET LA MATIÈRE NE « DÉZOOME » PAS (Tom, 12 sept.) : les motifs du moteur sont
     ancrés en COORDONNÉES ABSOLUES (braille tous les 9, mosaïque 11, pixel 5, sillons 6 — la table `PER` de
     `dalleTrame`), donc leur taille ne suit PAS celle de la cellule. Ajouter des germes ajoute des dalles
     sans réduire la matière : c'est de la saturation, pas un dézoom. */
  /* ⚑ PLUS AUCUNE CELLULE NEUTRE (Tom, 12 sept.) : « je veux ne plus voir le fond du tout ». Mesuré : les huit
     mondes sont OPAQUES à 100 % — ce n'était pas de la transparence, c'étaient les 6 % de cellules NEUTRES, qui
     se peignent dans les crèmes du thème et se lisaient comme du fond. Et on AJOUTE des germes (150) au lieu de
     rapetisser les mêmes. */
  /* ⚑ LA TOUFFE DOMINE NETTEMENT (Tom, 12 sept.) : « la matière la plus riche, celle qui fait vivre le pavage ». */
  var POIDS={encre:1, mosaique:1, touffe:3, braille:1, pixel:1, sillons:1, gravure:1, terrazzo:1};
  var MOTS={ h:'Ma Parole !', sub:'Retourne ta Toile',
    args:[['L’autre moitié de ta Toile','ce que tes proches tiennent envers toi'],
          ['Chaque parole se peaufine','récurrence, rappel, importance, mémoire'],
          ['Ta Toile change de matière','Douze mondes de plus']],   /* ⚑ v74 (Tom) : le compte à jour — douze mondes au Cercle (v70, v73) */
    prix:['39 € / AN','soit 3,25\u00a0€/\u2060mois'],   /* v96 : le texte a grandi (+12 %) — « 3,25 €/mois » ne se coupe plus après la barre ; s'il faut deux lignes, c'est après « soit » */   /* ⚑ v74 (Tom) : « AN » en capitales */   /* ⚑ v16 (Tom) : « 39 € » devient « 39 € / an » */
      /* ⚑ Tom, 14 sept. : l'ANNUEL en avant (39 €, Fraunces 40) ; le mois à 5,99 € est une option */ legal:'Sans engagement · résiliable à tout moment',
    option:'Bon, allez d’accord — 39\u00a0€ / an', mois:'ou 5,99\u00a0€ par mois' };   /* ⚑ v107 (Tom) : l'essai reste le bouton principal ; l'adhésion passe sur l'option, avec le prix annuel */
  var TOPS=[434,488,542];
  var CAD=null, CV=null, G=null, raf=0, prochaine=0, mue=null, ouvertA=0, posee=false, dpr=1;
  var SEEDS=[], SEED=[], POLY=[], OFF=null, MONDECV=[];
  function ps(){ return document.getElementById('plusScreen'); }
  function el(t,c){ var e=document.createElement(t); if(c) e.className=c; return e; }
  /* ── LE SEMIS : des POSITIONS, pas des formes. Un gabarit de germe pris au moteur (Toile.preview) est cloné,
       comme le fait déjà `Toile_previewLive` : tous les champs existent et sont du bon type. ── */
  function semis(tpl, PAL){
    var n=NGERMES, gc=Math.max(5,Math.round(Math.sqrt(n*CADW/CADH))), gr=Math.max(4,Math.round(n/gc));
    var cw=CADW/gc, ch=CADH/gr, out=[];
    for(var r0=0;r0<gr;r0++) for(var c0=0;c0<gc;c0++){
      var s={}; for(var k in tpl) s[k]=tpl[k];
      s.x=cw*(c0+.5)+(Math.random()-.5)*cw*.62;
      s.y=ch*(r0+.5)+(Math.random()-.5)*ch*.62;
      s.tx=s.x; s.ty=s.y; s.px=null; s.py=null; s.w=0; s.wt=0; s.t0=-99999; s.gc=null;
      s.ang=Math.random()*Math.PI; s.tone=[1.0,0.76,1.24,0.88,1.12][(Math.random()*5)|0];
      if(Math.random()<PART_COL){ s.kind='promi'; s.ci=(Math.random()*PAL.length)|0; s.c=PAL[s.ci]; }
      else { s.kind='gray'; s.ci=null; s.c=null; }
      out.push(s);
    }
    return out;
  }
  /* ═══════════════════════════════════════════════════════════════════════════════════════════════════════
     ⚑ DES DALLES QUI SE SUPERPOSENT (Tom, 12 sept. 2026). J'avais compris « pavage plus fin » et je densifiais :
     à 448 cellules chaque dalle tombait à 12 px, la matière n'y tenait plus qu'en fragment, et le fond du moteur
     paraissait DAVANTAGE (70 % en clair, mesuré). Ce qu'il faut est l'inverse : de GROSSES dalles EMPILÉES.
     L'architecture, mesurée :
       · UNE COLLECTION de vraies dalles — `dalleTrame(cv, id, k, monde)`, rendue À SA TAILLE FINALE par le
         moteur, avec sa forme, ses contours, sa matière. 3 Promi × 8 mondes × 2 tailles = 48 dalles, ~1,4 s,
         rendue UNE FOIS et gardée : elle ne dépend pas de l'ouverture, seulement du thème et de la palette.
       · DES POSES tirées à chaque ouverture — position, rotation, ordre. Mesuré : 700 poses = 5 ms. C'est ce
         qui rend la Toile différente à chaque réouverture, pour presque rien.
       · LE RECOUVREMENT supprime le fond : mesuré 0,86 % à 600 poses, 0,01 % à 900.
     ⚑ Aucune dalle n'est redimensionnée à la pose : on la dessine à la taille que le moteur lui a donnée. Seule
     la ROTATION varie — on pose une dalle, on ne l'étire pas.
     ═══════════════════════════════════════════════════════════════════════════════════════════════════════ */
  var COLL=[], COLL_CLE=null, POSES=[], OFF=null;
  /* ⚑ DE GROSSES DALLES ET PEU DE POSES — mesuré. À 760 poses de dalles de 70, le recouvrement vaut 21 fois la
     surface du cadre : chaque dalle en enterre une autre, il ne reste que des éclats, et la LONGUEUR MOYENNE DES
     PLAGES d'une même couleur tombe à 1,8 px — c'est du bruit, pas de la saturation. À 42 poses de dalles de 150
     elle remonte à 3,1 px (+72 %) et le fond reste à 2,4 %.
     ⚑ ET UN ORDRE, parce que la superposition en crée un : les mondes qui REMPLISSENT en dessous (ils tuent le
     fond), les mondes à LIGNES ensuite, la TOUFFE AU-DESSUS — elle est ajourée, elle ne se lit que posée sur de
     la couleur. « Plus de Touffe » veut donc dire : plus de poses dans la couche du HAUT. */
  /* ⚑ LA COLLECTION EST DIMENSIONNÉE SUR LE BUDGET D'UN TÉLÉPHONE, PAS SUR CELUI DU BANC. Mesuré, processeur
     ralenti ×4 (substitut de Lighthouse, pas un appareil) : une dalle coûte 74,6 ms à 50 de côté, 219 ms à 90,
     450,8 ms à 130, 614,9 ms à 150. Mes 48 dalles de 130 faisaient donc 21,6 s de calcul là-bas, et l'ouverture
     de l'écran mettait 17 à 27 s. 16 dalles de 100 coûtent ~4,3 s, en fond, par tranches. */
  var N_ID=3, N_TAILLE=1, COTE=100, N_POSE=0;
  var PLEIN=['terrazzo','ritournelle','madrure','chantourne','guingois','chamade','ramage'], LIGNE=['sillons','gravure'], HAUT=['bobinette','volubilis','mascaret'];   /* v74 : les douze payants — remplissent · lignes · ajourés */   /* v55 : les treize — chaque monde dans la couche de sa nature (remplit · lignes · ajouré) */   /* v34 : Bobinette, ajourée, prend la couche du dessus qu'avait la Touffe */
  /* les poses ne coûtent que 1 à 2 ms : on en met assez pour couvrir. À 70 poses de dalles de ~68 px le
     recouvrement ne valait que 2,5 fois la surface et le fond remontait à 10–19 % (mesuré). */
  var N_PLEIN=78, N_LIGNE=22, N_HAUT=16;   /* v55 : les lignes, opaques, enterraient les mondes qui remplissent — on voyait deux matières sur treize */   /* la Touffe reste dominante sur le dessus : 40/140 = 28,6 % */
  function cleCollection(){
    var m={}; try{ m=window.Toile.mondeCourant()||{}; }catch(_){ }
    var clair=!!document.querySelector('.frame.light, #device.light');
    return (m.p||'')+'|'+(m.h||0)+'|'+(clair?'clair':'sombre');
  }
  /* ⚑ LA COLLECTION SE BÂTIT AU DÉMARRAGE, EN FOND (Tom, 12 sept.) : « cinq secondes de cadre vide à la
     première ouverture de l'écran le plus cher, c'est inacceptable — on déplace le coût là où personne ne le
     voit. » Une dalle coûte ~100 ms au moteur : on ne peut pas la découper plus fin, donc on pose UNE dalle par
     tranche, espacée, et on commence par UN MONDE CHACUN — l'écran est utilisable dès la 8ᵉ dalle.
     ⚠ Le démarrage de l'app n'est pas touché : la première tranche n'part qu'après DEMARRE_APRES, et le travail
     s'arrête net si l'écran s'ouvre (il finit alors ce qui manque, tout de suite). */
  /* ⚑ LE BÂTI DE FOND NE PREND LE FIL QUE QUAND IL EST AU REPOS. Une dalle coûte ~100 ms : à une tranche
     toutes les 260 ms il mangeait 38 % du fil principal pendant quelques secondes, et `redteam_verbe` est
     tombé de 3/6 à 0/6 — la page + rendait des hauteurs NULLES parce que la mise en page n'avait pas le temps
     de se poser. C'est le piège du §8 (« l'app rame, les captures échouent »), et c'était un vrai défaut de
     produit, pas un artefact de test. On passe par `requestIdleCallback` : il n'entre jamais en concurrence. */
  var DEMARRE_APRES=1800, ENTRE_TRANCHES=420;
  function planifie(j, delai){
    if(typeof window.requestIdleCallback==='function')
      window.requestIdleCallback(function(){ fond(j); }, {timeout:3000});
    else setTimeout(function(){ fond(j); }, delai);
  }
  var TODO=null, TODO_I=0, FOND_LANCE=false, DEPART=null;
  function idsUtiles(){
    var ids=[];
    try{ ids=(typeof promises!=='undefined'?promises:[]).filter(function(p){ return !p.draft&&!p.req; }).map(function(p){ return p.id; }); }catch(_){ }
    return ids;
  }
  /* ⚑ LA COLLECTION NE SURVIT PAS À SES SOURCES (12 sept. 2026, trouvé par `preuve_vide.py`).
     `cleCollection()` ne portait que palette·teinte·thème : en vidant `promises`, `COLL` et `TODO` restaient,
     l'écran posait encore des dalles d'ids SUPPRIMÉS, et `pc-sans` n'était jamais posée. Le commentaire de
     `prepare()` annonçait « la classe suit les DONNÉES » — elle suivait un cache.
     On retient les ids dont la collection est FAITE (`SRC`), et elle se rebâtit dès que l'un d'eux disparaît.
     ⚠ Planter ne l'invalide PAS : une Toile de démonstration n'a jamais prétendu montrer tous les Promi, et
     tout jeter à chaque plantation ferait retomber la première ouverture aux 3 dalles du minimum vital —
     le défaut déjà mesuré (3 dalles, 3 mondes au lieu de 16 et 8). Le chemin normal ne bouge donc pas. */
  var SRC=null;
  function srcValide(){
    if(!SRC||!SRC.length) return true;
    var v={}, ids=idsUtiles(); for(var i=0;i<ids.length;i++) v[ids[i]]=1;
    for(var j=0;j<SRC.length;j++) if(!v[SRC[j]]) return false;
    return true;
  }
  function listeAFaire(){
    SRC=null;
    var ids=idsUtiles();
    if(!ids.length) return null;
    /* ⚑ ON NE SYNCHRONISE PAS LA TOILE SOI-MÊME. Mon lot appelait `Toile.sync(ids)` quand la liaison
       germes↔Promi n'était pas encore faite : passant AVANT celle de l'app, il imposait SON ordre d'ids et
       réattribuait les dalles. Mesuré par `redteam_toile` : « les dalles sont aux bonnes positions » tombait
       de 7/10 à 5/10, avec des écarts de 500 px. On attend que l'app l'ait faite ; sinon on renonce et on
       réessaie à la tranche suivante. */
    var lie=false; try{ lie=!!window.Toile.dalleAbs(ids[0]); }catch(_){ }
    if(!lie) return null;
    /* ⚑ LES PROMI SE CHOISISSENT RÉPARTIS, ET LE DÉPART EST TIRÉ PAR SESSION. `ids[(i*7)%n]` prenait TOUJOURS
       les mêmes : si leurs dalles portaient la même couleur de palette, toute Toile sortait monochrome — vu à la
       capture finale, un cadre entièrement lilas. En répartissant et en tirant le départ, la couleur change d'une
       session à l'autre et les chances d'avoir deux teintes différentes montent. */
    var choisis=[], pas=Math.max(1, Math.floor(ids.length/Math.max(1,N_ID)));
    if(DEPART==null) DEPART=(Math.random()*ids.length)|0;
    /* v55 : une parole de chaque nature quand elles existent — sous Ingénu la couleur dit la nature, trois Promi donnaient une Toile toute bleue */
    try{ var _parN={promi:[],chiche:[],nuee:[]}; promises.forEach(function(p){ if(p.draft||p.req||ids.indexOf(p.id)<0) return; (_parN[p.nuee?'nuee':(p.chiche?'chiche':'promi')]).push(p.id); });
      ['promi','chiche','nuee'].forEach(function(nt){ var L=_parN[nt]; if(L.length&&choisis.length<N_ID) choisis.push(L[(DEPART+L.length)%L.length]); }); }catch(_){ }
    for(var i=0;choisis.length<N_ID && i<ids.length;i++){ var _c=ids[(DEPART+i*pas)%ids.length]; if(choisis.indexOf(_c)<0) choisis.push(_c); }
    SRC=choisis.slice();
    var tailles=[];
    for(var t=0;t<N_TAILLE;t++) tailles.push(Math.round(COTE*(0.8+0.5*t/Math.max(1,N_TAILLE-1))));
    /* un monde chacun D'ABORD, puis le reste : la Toile est composable dès la huitième dalle */
    var a=[], b=[];
    MONDES.forEach(function(m){
      choisis.forEach(function(id,ii){ tailles.forEach(function(cote,tt){
        (ii===0 && tt===0 ? a : b).push({id:id, m:m, cote:cote}); }); });
    });
    return a.concat(b);
  }
  function rendUne(t){
    var base={}; try{ base=window.Toile.mondeCourant()||{}; }catch(_){ }
    var d=null; try{ d=window.Toile.dalleAbs(t.id); }catch(_){ }
    if(!d||!d.w||!d.h) return false;
    var k=t.cote/Math.max(d.w,d.h), cv=document.createElement('canvas'), ok=false;
    try{ ok=window.Toile.dalleTrame(cv, t.id, k, {m:t.m, p:base.p, h:base.h}, {courant:1}); }catch(_){ }   /* v30 · un aperçu de monde du Studio */
    if(!ok||!cv.width) return false;
    /* ⚑ L'ENCRE PERDAIT SA MATIÈRE DANS LE CERCLE (Tom, 13 sept. 2026). Mesuré dans le moteur : une dalle Encre, ce sont
       neuf ellipses d'une même couleur à 90 % d'opacité — sa « variation » est le sol qui transparaît sous chaque bord et
       chaque recouvrement. Sur la Toile ce sol est sombre (ou crème) : les ellipses se lisent. Ici les poses s'empilent
       sur d'autres dalles claires, et 10 % de bleu pâle sous du bleu pâle ne se voit plus — une tache pleine. On pose
       donc la dalle SUR SON SOL, dans sa seule silhouette, comme le moteur la montre. Rien n'est ajouté par-dessus. */
    if(t.m === 'encre'){
      try{
        var clairE = !!document.querySelector('.frame.light, #device.light');
        var sol = document.createElement('canvas'); sol.width = cv.width; sol.height = cv.height;
        var gs = sol.getContext('2d');
        gs.drawImage(cv, 0, 0); gs.globalCompositeOperation = 'source-in';
        gs.fillStyle = clairE ? '#F7F0DE' : '#201908'; gs.fillRect(0, 0, sol.width, sol.height);
        var fin = document.createElement('canvas'); fin.width = cv.width; fin.height = cv.height;
        var gf = fin.getContext('2d');
        for(var i3 = 0; i3 < 4; i3++) gf.drawImage(sol, 0, 0);   /* la silhouette à 90 % portée à ~100 % */
        gf.drawImage(cv, 0, 0);
        cv = fin;
      }catch(_){ }
    }
    /* ⚑ CHANTIER 76 (Tom, 14 sept. 2026) — LE DÉFAUT EST ICI, PAS DANS LE MOTEUR. Le diagnostic de départ était faux : le
       moteur ne peint pas de crème, les creux de Gravure, Braille et Sillons sont TRANSPARENTS (76 à 80 % d'une dalle) ; ce
       qu'on voyait, c'était le crème de CETTE page à travers. On pose donc ces trois mondes, sur cet écran seulement, sur un
       fond tiré de leur propre couleur : la silhouette des traits, dilatée au pas du motif (≤ 9), peinte d'un ton de la dalle.
       Le moteur, la Toile et les cartes ne bougent pas : une dalle reste identique partout où elle paraît. */
    if(t.m === 'gravure' || t.m === 'braille' || t.m === 'sillons'){
      try{
        var clairL = !!document.querySelector('.frame.light, #device.light');
        /* la couleur de la dalle vient du moteur (lecture), jamais d'une lecture de pixels sur cet écran */
        var mc = /rgb\((\d+),(\d+),(\d+)\)/.exec((window.Toile.colorOf && window.Toile.colorOf(t.id)) || '');
        if(mc){
          var cm=[+mc[1], +mc[2], +mc[3]], vers = clairL ? [255,255,255] : [32,25,8];
          var fondL = cm.map(function(v,i){ return Math.round(v + (vers[i]-v)*0.55); });
          var silL = document.createElement('canvas'); silL.width = cv.width; silL.height = cv.height;
          var gl = silL.getContext('2d'), R0 = Math.round(5*dpr);
          for(var ox=-R0; ox<=R0; ox+=Math.max(1,Math.round(R0/2))) for(var oy=-R0; oy<=R0; oy+=Math.max(1,Math.round(R0/2))){
            if(ox*ox+oy*oy <= R0*R0) gl.drawImage(cv, ox, oy); }
          gl.globalCompositeOperation = 'source-in'; gl.fillStyle = 'rgb('+fondL.join(',')+')'; gl.fillRect(0, 0, silL.width, silL.height);
          gl.globalCompositeOperation = 'source-over'; gl.drawImage(cv, 0, 0);
          cv = silL;
        }
      }catch(_){ }
    }
    COLL.push({cv:cv, w:cv.width/dpr, h:cv.height/dpr, monde:t.m, id:t.id, cote:t.cote});
    window._vendColl=COLL.map(function(d){ return d.monde+':'+Math.round(d.w)+'x'+Math.round(d.h); });   /* publié (mesure) */
    window._vendCollCv=COLL;
    return true;
  }
  /* ⚑ LA CHAÎNE REPART TOUT DE SUITE QUAND LA CLÉ CHANGE. Sans ça, après un changement de thème la veille
     mettait jusqu'à 1,2 s à le remarquer et la première ouverture ne montrait que les 3 dalles du minimum vital
     (mesuré : collection 3, 3 mondes en sombre juste après la bascule). Le jeton empêche deux chaînes de courir
     en parallèle — c'est le piège du §8, deux propriétaires pour une même propriété. */
  var JETON=0;
  function neuve(){
    COLL=[]; COLL_CLE=cleCollection(); TODO=listeAFaire(); TODO_I=0;
    JETON++; var j=JETON; planifie(j, 0);
  }
  /* ⚑ L'OUVERTURE NE BLOQUE JAMAIS (Tom : « c'est l'écran le plus cher »). Elle compose avec ce qui est PRÊT ;
     le bâti de fond continue, et la Toile s'enrichit d'une ouverture à l'autre. On ne rend en bloquant que le
     minimum vital — trois dalles — pour qu'il y ait toujours quelque chose à poser. */
  var MINI=3;
  function batCollection(){
    if(COLL_CLE!==cleCollection() || !srcValide()) neuve();
    if(!TODO){ TODO=listeAFaire(); TODO_I=0; if(!TODO) return COLL.length; }
    while(COLL.length<MINI && TODO_I<TODO.length) rendUne(TODO[TODO_I++]);
    return COLL.length;
  }
  /* ⚑ LE BÂTI DE FOND NE S'ARRÊTE JAMAIS DÉFINITIVEMENT : changer de thème ou de palette invalide la
     collection, et sans cette veille la chaîne était morte — en sombre la collection restait aux 3 dalles du
     minimum vital (mesuré : 3 dalles, 3 mondes au lieu de 16 et 8). */
  /* ⚑ v44 (Tom, 24 sept.) — SAFARI N'A PAS `requestIdleCallback`. Le repli était une minuterie de 420 ms qui rendait une
     dalle de ~100 ms D'UN BLOC, quoi qu'il se passe à l'écran : la plantation invalide la collection, et la première
     tranche tombait ~170 ms après, en pleine tirée (mesuré en WebKit : une image de 90 à 150 ms, dans TOUS les mondes).
     Et même avec `requestIdleCallback`, un rappel qui ne regarde pas son échéance occupe le fil 100 ms d'affilée.
     Donc : une tranche n'est rendue que si la Toile est AU REPOS (son moteur ne tourne pas) et qu'aucun doigt n'a touché
     l'écran depuis 700 ms ; sinon elle est remise à plus tard. */
  var _toucheA=0; try{ ['pointerdown','touchstart','wheel','keydown'].forEach(function(t){ document.addEventListener(t,function(){ _toucheA=performance.now(); },{capture:true,passive:true}); }); }catch(_){ }
  function _auRepos(){ try{ var st=window.Toile_state&&window.Toile_state(); if(st&&st.running) return false; }catch(_){ } if(window._tEcran && performance.now()-window._tEcran<2500) return false; return performance.now()-_toucheA>700; }   /* ⚑ v100 : et pas dans les 2,5 s d'un changement d'écran */
  function fond(j){
    if(j!=null && j!==JETON) return;                 /* une chaîne plus récente a pris la main */
    if(!_auRepos()){ var _mj=(j==null?JETON:j); setTimeout(function(){ planifie(_mj, 0); }, 350); return; }   /* v44 */
    if(COLL_CLE!==cleCollection() || !srcValide()){ neuve(); return; }
    if(!TODO){ TODO=listeAFaire(); TODO_I=0; }
    var mien=(j==null?JETON:j);
    if(TODO && TODO_I<TODO.length){
      rendUne(TODO[TODO_I++]);   /* il continue même écran ouvert : la Toile s'enrichit à l'ouverture suivante */
      window._vendFond={faites:TODO_I, total:TODO.length, cle:COLL_CLE};
      planifie(mien, ENTRE_TRANCHES);
      return;
    }
    window._vendFond={faites:TODO?TODO.length:0, total:TODO?TODO.length:0, cle:COLL_CLE};
    setTimeout(function(){ fond(mien); }, 1400);     /* rien à faire : on veille, au cas où le thème change */
  }
  function lanceFond(){
    if(FOND_LANCE) return; FOND_LANCE=true;
    dpr=Math.min(2,window.devicePixelRatio||1);
    JETON++; var j0=JETON; setTimeout(function(){ planifie(j0, 0); }, DEMARRE_APRES);
  }
  function tirePoses(){
    POSES=[];
    if(!COLL.length) return 0;
    function couche(mondes, n){
      /* v55 : une part ÉGALE par monde — on tire d'abord le monde, puis une de ses dalles (tirer une dalle au hasard donnait la
         part aux mondes qui ont le plus de dalles, et la couche du dessus enterrait les autres) */
      var parM={}; COLL.forEach(function(d,i){ if(mondes.indexOf(d.monde)>=0) (parM[d.monde]=parM[d.monde]||[]).push(i); });
      var ms=Object.keys(parM); if(!ms.length) return;
      for(var i=0;i<n;i++){
        var lm=parM[ms[(Math.random()*ms.length)|0]], k=lm[(Math.random()*lm.length)|0], d=COLL[k];
        POSES.push({k:k, x:Math.random()*CADW-d.w/2, y:Math.random()*CADH-d.h/2, r:Math.random()*6.2832});
      }
    }
    couche(PLEIN.concat(LIGNE), N_PLEIN+N_LIGNE);   /* v55 : une seule couche mêlée — les lignes ne recouvrent plus tout */
    couche(HAUT,  N_HAUT);           /* au-dessus : la Touffe, ajourée, elle se lit sur de la couleur */
    /* au moins une pose par monde : sans ça le tirage en oublie un (mesuré) */
    MONDES.forEach(function(w){
      if(POSES.some(function(p){ return COLL[p.k].monde===w; })) return;
      var cd=[]; COLL.forEach(function(d,i){ if(d.monde===w) cd.push(i); });
      if(!cd.length) return;
      var kk=cd[(Math.random()*cd.length)|0], dd=COLL[kk];
      POSES.splice(Math.min(POSES.length, N_PLEIN), 0,
        {k:kk, x:Math.random()*CADW-dd.w/2, y:Math.random()*CADH-dd.h/2, r:Math.random()*6.2832});
    });
    return POSES.length;
  }
  function poseUne(g, p, alpha){
    var d=COLL[p.k]; if(!d) return;
    g.save();
    if(alpha!=null) g.globalAlpha=alpha;
    g.translate(p.x+d.w/2, p.y+d.h/2); g.rotate(p.r);
    g.drawImage(d.cv, -d.w/2, -d.h/2, d.w, d.h);
    g.restore();
  }
  function peintTout(){
    OFF=document.createElement('canvas');
    OFF.width=Math.round(CADW*dpr); OFF.height=Math.round(CADH*dpr);
    var g=OFF.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
    for(var i=0;i<POSES.length;i++) poseUne(g, POSES[i], null);
    return POSES.length;
  }
  function prepare(){
    dpr=Math.min(2,window.devicePixelRatio||1);
    var PAL0=[]; try{ PAL0=window.Toile.cols()||[]; }catch(_){ }
    var t0=performance.now();
    var nColl=batCollection();
    var msColl=Math.round(performance.now()-t0);
    /* la classe suit les DONNÉES (§8) : aucune dalle à rendre → pas de Toile, et tout remonte */
    if(CAD.classList.contains('pc-sans') !== !nColl) CAD.classList.toggle('pc-sans', !nColl);
    if(!nColl){
      window._vendToile={superposees:true, collection:0, sans:true, poses:0, matieres:{}, ms:msColl,
        pastilles:0, fond:window._vendFond||null};
      return false;
    }
    var t1=performance.now();
    tirePoses();
    CV.width=Math.round(CADW*dpr); CV.height=Math.round(CADH*dpr);
    G=CV.getContext('2d'); if(!G) return false;
    var nPose=peintTout();
    var msPose=Math.round(performance.now()-t1);
    var ACC=accent(PAL0);
    if(ACC) CAD.style.setProperty('--pc-accent','rgb('+ACC.rgb.join(',')+')');
    var bouton=String(window._vendBouton||'2');
    CAD.classList.remove('pc-b1','pc-b2','pc-b3','pc-b4');
    if(bouton==='1'||bouton==='2'||bouton==='3'||bouton==='4') CAD.classList.add('pc-b'+bouton);
    var nPast=0; try{ nPast=pastilles(); }catch(_){ }
    var fondM=rgbDe(getComputedStyle(document.getElementById('plusScreen')).backgroundColor)||[247,240,222];
    var mauve=[41,21,71];
    var comptes={}; POSES.forEach(function(p){ var w=COLL[p.k].monde; comptes[w]=(comptes[w]||0)+1; });
    window._vendToile={ superposees:true, collection:nColl, collectionMs:msColl, poses:nPose, posesMs:msPose,
      fond:window._vendFond||null,
      cotes:COLL.slice(0,4).map(function(d){ return Math.round(d.w)+'×'+Math.round(d.h); }),
      matieres:comptes, palette:PAL0.length, dpr:dpr, bouton:bouton, accent:ACC, pastilles:nPast,
      mauve:{rgb:mauve, ecart:Math.round(Math.abs(lum(mauve)-lum(fondM)))},
      sig:POSES.map(function(p){ return p.k+','+Math.round(p.x)+','+Math.round(p.y)+','+p.r.toFixed(2); }).join('|') };
    return true;
  }
  /* l'accent : MESURÉ sur la palette du Studio, puis porté à 60 de luminosité d'écart avec le fond (§3) */
  function rgbDe(c){
    if(Array.isArray(c)) return [c[0]|0,c[1]|0,c[2]|0];
    var m=String(c).match(/\d+/g); if(m&&m.length>=3) return [+m[0],+m[1],+m[2]];
    var h=String(c).replace('#',''); if(h.length===6) return [parseInt(h.slice(0,2),16),parseInt(h.slice(2,4),16),parseInt(h.slice(4,6),16)];
    return null;
  }
  function lum(c){ return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]; }
  /* ⚑ LES COULEURS D'ÉTAT SONT EXCLUES (Tom, 12 sept.) : « menthe et terracotta ne servent qu'aux états, partout ».
     Mesuré : la plus saturée de la palette « signal » ÉTAIT le terracotta [240,122,46] — soit exactement « à tenir ».
     ⚠ L'accent n'a plus d'emploi sur cet écran (le sous-titre est passé en gras, le titre porte le mauve fixe) :
     la règle est gardée ici pour le jour où il resservira, et sa valeur est publiée. */
  var ETATS=[[143,224,143],[221,77,35]];   /* menthe #8FE08F, terracotta #DD4D23 */
  function estEtat(c){ return ETATS.some(function(e){ return Math.hypot(c[0]-e[0],c[1]-e[1],c[2]-e[2])<40; }); }
  function accent(PAL){
    var best=null, bs=-1;
    PAL.forEach(function(c0){ var c=rgbDe(c0); if(!c||estEtat(c)) return;
      var mx=Math.max(c[0],c[1],c[2]), mn=Math.min(c[0],c[1],c[2]), s=mx?(mx-mn)/mx:0;
      if(s>bs){ bs=s; best=c; } });
    if(!best) return null;
    var fond=rgbDe(getComputedStyle(document.getElementById('plusScreen')).backgroundColor)||[247,240,222];
    var lf=lum(fond), c=best.slice(), pas=0, vers=lf>128?-1:1;
    while(Math.abs(lum(c)-lf)<60 && pas<44){
      c=[Math.max(0,Math.min(255,c[0]+vers*6)),Math.max(0,Math.min(255,c[1]+vers*6)),Math.max(0,Math.min(255,c[2]+vers*6))];
      pas++;
    }
    return {rgb:c, depart:best, ecart:Math.round(Math.abs(lum(c)-lf)), pas:pas, fond:fond};
  }
  /* ⚑ LES PASTILLES — DE VRAIES DALLES, rendues par le moteur. Patron de `peintMinis` : la dalle ENTIÈRE de sa
     cellule, centrée et au rapport, dans un canevas à 3× la taille d'affichage. On choisit le Promi dont la
     cellule est la plus CARRÉE (mesuré) : à 16 px une cellule très allongée ne se lirait pas. */
  var PASTILLE_IDS=null, CH_PX=17;
  function idsCarres(){
    if(PASTILLE_IDS) return PASTILLE_IDS;
    var ids=[];
    try{ ids=(typeof promises!=='undefined'?promises:[]).filter(function(p){ return !p.draft&&!p.req; }).map(function(p){ return p.id; }); }catch(_){ }
    if(!ids.length) return (PASTILLE_IDS=[]);
    /* ⚑ ON NE SYNCHRONISE PAS LA TOILE SOI-MÊME. Mon lot appelait `Toile.sync(ids)` quand la liaison
       germes↔Promi n'était pas encore faite : passant AVANT celle de l'app, il imposait SON ordre d'ids et
       réattribuait les dalles. Mesuré par `redteam_toile` : « les dalles sont aux bonnes positions » tombait
       de 7/10 à 5/10, avec des écarts de 500 px. On attend que l'app l'ait faite ; sinon on renonce et on
       réessaie à la tranche suivante. */
    var lie=false; try{ lie=!!window.Toile.dalleAbs(ids[0]); }catch(_){ }
    if(!lie) return [];       /* pas encore lié : on ne CACHE pas, on réessaiera */
    var notes=[];
    ids.forEach(function(id){ var d=null; try{ d=window.Toile.dalleAbs(id); }catch(_){ }
      if(d&&d.w>0&&d.h>0) notes.push({id:id, ec:Math.abs(Math.log(d.w/d.h))}); });
    notes.sort(function(a,b){ return a.ec-b.ec; });
    if(!notes.length) return [];
    return (PASTILLE_IDS=notes.map(function(n){ return n.id; }));
  }
  function pastilles(){
    var ids=idsCarres(); if(!ids.length) return 0;
    var base={}; try{ base=window.Toile.mondeCourant()||{}; }catch(_){ }
    var n=0;
    [].forEach.call(document.querySelectorAll('#pcCadre .pc-ch'), function(ch, k){
      var w=ch.getAttribute('data-m');
      var id=ids[k%ids.length];
      /* ⚑ LE MOTEUR PEINT À LA TAILLE FINALE — mesuré : `dalleTrame` accepte une échelle `k` et rend directement
         un canevas de la taille voulue (k=0,25 → 51×36 ; k=0,16 → 33×20). On ne redimensionne donc RIEN : la dalle
         est peinte à sa cote d'affichage par le moteur, avec sa forme et ses contours. L'affichage suit le canevas
         au pixel — aucune mise à l'échelle, aucune découpe. */
      var d0=null; try{ d0=window.Toile.dalleAbs(id); }catch(_){ }
      if(!d0||!d0.w) return;
      var k=CH_PX/d0.h;   /* on cale sur la HAUTEUR : toutes les pastilles ont la même assise sur la ligne */
      var ok=false; try{ ok=window.Toile.dalleTrame(ch, id, k, {m:w, p:base.p, h:base.h}, {courant:1}); }catch(_){ }   /* v30 · un aperçu de monde du Studio */
      if(!ok||!ch.width) return;
      var dd=Math.min(2,window.devicePixelRatio||1);
      ch.style.setProperty('width',(ch.width/dd)+'px','important');
      ch.style.setProperty('height',(ch.height/dd)+'px','important');
      try{ ch.setAttribute('data-dalle', id); ch.setAttribute('data-echelle', k.toFixed(3));
           ch.setAttribute('data-matiere','0,0,'+ch.width+','+ch.height);
           ch.setAttribute('data-matiere-base', ch.width+','+ch.height); }catch(_){ }
      n++;
    });
    return n;
  }
  function bez(t){ var lo=0,hi=1,u=t,i,x;
    for(i=0;i<18;i++){ u=(lo+hi)/2; var v=1-u; x=3*v*v*u*0.32+u*u*u; if(x<t) lo=u; else hi=u; }
    var v2=1-u; return 3*v2*v2*u*0.72+3*v2*u*u*1+u*u*u; }
  /* LA MUE — une seule cellule, et on ne retouche QUE sa boîte : recomposer les 285 000 pixels par image
     coûterait trop cher (CLAUDE §8 : un mouvement se calcule sur le temps réel, pas sur le compte d'images). */
  /* LA MUE — une seule cellule change de matière. Les DEUX états sont des rendus du moteur : on repose le
     pavage (une copie de pixels du hors-écran, pas un choix de pixels) puis on pose la nouvelle cellule,
     découpée sur son polygone, en fondu. Rien n'est rogné. */
  function fondPavage(){ G.setTransform(1,0,0,1,0,0); G.clearRect(0,0,CV.width,CV.height); G.drawImage(OFF,0,0); }
  function image(t){
    raf=0; var s=ps(); if(!s||!s.classList.contains('show')) return;
    if(!ouvertA){ ouvertA=t; fondPavage(); }
    var age=t-ouvertA;
    if(age<CASC){
      var e=bez(age/CASC);
      fondPavage();
      G.save(); G.globalCompositeOperation='destination-in';
      var W=CV.width, H=CV.height, gd=G.createLinearGradient(0,0,W,H), q=e*1.35;
      gd.addColorStop(0,'rgba(0,0,0,1)');
      gd.addColorStop(Math.max(0,Math.min(1,q-0.18)),'rgba(0,0,0,1)');
      gd.addColorStop(Math.max(0,Math.min(1,q)),'rgba(0,0,0,0)');
      gd.addColorStop(1,'rgba(0,0,0,0)');
      G.fillStyle=gd; G.fillRect(0,0,W,H); G.restore();
      raf=requestAnimationFrame(image); return;
    }
    if(!posee){ posee=true; fondPavage(); }
    /* UN SEUL MOUVEMENT : toutes les 4,5 s, UNE dalle du dessus change de matière — reposée en fondu, à sa
       taille, sans toucher au reste. */
    if(!mue && t>=prochaine && POSES.length){
      var i2=(Math.random()*POSES.length)|0, p0=POSES[i2], d0=COLL[p0.k];
      var cand=[]; COLL.forEach(function(d,i){ if(d.monde!==d0.monde && Math.abs(d.w-d0.w)<2) cand.push(i); });
      if(cand.length){
        var kk=cand[(Math.random()*cand.length)|0];
        mue={i:i2, t0:t, p:{k:kk, x:p0.x, y:p0.y, r:p0.r}};
      }
      prochaine=t+PERIODE;
    }
    if(mue){
      var pr=Math.min(1,(t-mue.t0)/MUE), e2=bez(pr);
      fondPavage();
      G.setTransform(dpr,0,0,dpr,0,0);
      poseUne(G, mue.p, e2);
      if(t-mue.t0>=MUE){
        POSES[mue.i]=mue.p;
        var go=OFF.getContext('2d'); go.setTransform(dpr,0,0,dpr,0,0);
        poseUne(go, mue.p, null);
        mue=null; fondPavage();
      }
    }
    else if(!prochaine){ prochaine=t+PERIODE; }
    raf=requestAnimationFrame(image);
  }
function bati(){
    var s=ps(); if(!s) return false;
    if(CAD&&CAD.isConnected) return true;
    CAD=el('div'); CAD.id='pcCadre';
    var t=el('div','pc-toile'); CV=document.createElement('canvas'); t.appendChild(CV); CAD.appendChild(t);
    var h=el('div','pc-h');
    var h1=el('span','pc-h1'); h1.textContent='Ma ';
    var h2=el('span','pc-h2'); h2.textContent='Parole';
    var h3=el('span','pc-h3'); h3.textContent='\u00a0!';          /* le point d'exclamation reste en ENCRE (Tom) */
    h.appendChild(h1); h.appendChild(h2); h.appendChild(h3); CAD.appendChild(h);
    var su=el('div','pc-sub');
    var s1=el('span','pc-s1'); s1.textContent='';
    var s2=el('span','pc-s2'); s2.textContent='Retourne ta Toile';
    su.appendChild(s1); su.appendChild(s2); CAD.appendChild(su);
    MOTS.args.forEach(function(a,i){ var d=el('div','pc-arg pc-a'+(i+1));
      var b=el('b'); b.textContent=a[0]; var q=el('i');
      q.textContent=a[1];   /* ⚑ v34 (Tom, Q317) : « Six mondes de plus », sans les nommer — on découvre les noms au Studio */
      d.appendChild(b); d.appendChild(q); CAD.appendChild(d); });
    var p=el('div','pc-prix'); var pb=el('b'); (function(){ var m=/^(.*?)(AN)$/.exec(MOTS.prix[0]); if(m){ pb.textContent=m[1]; var an=el('span','pc-an'); an.textContent=m[2]; pb.appendChild(an); } else pb.textContent=MOTS.prix[0]; })();   /* ⚑ v89 (Tom) : « AN » deux fois et quart plus petit */ var pi=el('i'); pi.textContent=MOTS.prix[1];
    p.appendChild(pb); p.appendChild(pi); CAD.appendChild(p);
    var mo=document.getElementById('buyMonth'), yr=document.getElementById('buyYear');
    if(mo){ mo.textContent=''; var ec=el('span','pc-eclat');
      var lb=el('span','pc-lb'); lb.textContent='Essayer 14 jours'; var go=el('span','pc-go'); go.textContent='›';
      mo.appendChild(ec); mo.appendChild(lb); mo.appendChild(go); CAD.appendChild(mo); }
    if(yr){ yr.textContent=''; var yl=el('span'); yl.textContent=MOTS.option; yr.appendChild(yl); CAD.appendChild(yr); }
    var mo2=el('div','pc-mois'); mo2.textContent=MOTS.mois; CAD.appendChild(mo2);   /* ⚑ v108 (Tom) : « c'est elle qui rend les 39 € attractifs » — discrète, sous les deux boutons */
    var lg=el('div','pc-legal'); lg.textContent=MOTS.legal; CAD.appendChild(lg);
    s.appendChild(CAD); return true;
  }
  function off(e,anc){ var x=0,y=0; while(e&&e!==anc){ x+=e.offsetLeft; y+=e.offsetTop; e=e.offsetParent; } return [x,y]; }
  function pose(){
    var s=ps(), dv=document.getElementById('device'); if(!s||!dv||!bati()) return;
    var fr=s.closest('.frame')||document.body, a=off(dv,fr), b=off(s,fr);
    CAD.style.setProperty('left',(a[0]-b[0])+'px','important'); CAD.style.setProperty('top',(a[1]-b[1])+'px','important');
  }
  function demarre(){
    if(!bati()) return;
    var t0=performance.now(); if(!prepare()) return;
    window._vendToile.ms=Math.round(performance.now()-t0);
    ouvertA=0; posee=false; prochaine=0; mue=null;
    var mo=document.getElementById('buyMonth');
    if(mo){ mo.classList.remove('pc-pose'); void mo.offsetWidth; mo.classList.add('pc-pose'); }
    if(!raf) raf=requestAnimationFrame(image);
  }
  function arrete(){ if(raf){ cancelAnimationFrame(raf); raf=0; } }
  window._vendToileGo=demarre;
  var ouvert=false;
  function veille(){
    var s=ps(); if(!s) return;
    new MutationObserver(function(){
      var o=s.classList.contains('show'); if(o===ouvert) return; ouvert=o;
      if(o){ try{ s.scrollTop=0; pose(); }catch(_){ } setTimeout(demarre,0); } else arrete();
    }).observe(s,{attributes:true,attributeFilter:['class']});
  }
  try{ bati(); pose(); veille(); lanceFond(); }catch(_){ }
})();
