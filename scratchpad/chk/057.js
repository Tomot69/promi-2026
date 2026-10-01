
/* ═══════════════════════════════════════════════════════════════════════════════════════
   LE PEAUFINER D'UNE NUÉE — moodboard, cadres 84 à 87.
   Quatre écrans : deux thèmes × deux pages. Il n'existait PAS : toucher la barre d'une
   fiche de Nuée ne dépliait rien (relevé : `#dpDetails.className` reste vide après le clic).
   C'est ici que vit « Planter un Promi dans la Nuée » — le §12 de la spécification ne le
   met nulle part sur la fiche au repos, et le cadre 86 le pose ici, avec DISSOUDRE LA NUÉE.

   ⚠ ON NE RECRÉE PAS LE BOUTON : on DÉPLACE `#nfAdd`, celui de l'app, avec son `onclick`.
   Le retirer et en dessiner un autre supprimerait la fonction le temps d'un lot — et c'est
   la fonction même d'une Nuée (CLAUDE.md §9).

   ⚠ CE QUE LE DOCUMENT NE DIT PAS, et que j'ai tranché : l'écart entre COMMENTAIRES (qui
   finit à 522) et « Planter » du cadre 86. Les deux cadres sont deux ÉTATS du même panneau
   — 86 n'a pas d'entête, c'est 84 défilé. J'ai repris LE RYTHME DU CADRE 86 lui-même :
   62 de haut + 16 d'écart = 78, d'où Planter à 538 et DISSOUDRE à 616. Voir QUESTIONS.md
   · Q65, « à valider ».
   ═══════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  var W = 390;
  var MAUVE = '#291547', CLAIRN = '#C9A8F5', CREME = '#F7F0DE', ENCRE = '#201908';

  function pose(el, css){ if(!el) return;
    /* ⚠ ON MARQUE CE QU'ON POSE, pas seulement ce qu'on masque. `rangeNuee` retirait bien
       les cartes qu'il avait bâties, mais pas le `display:block !important; position:
       absolute; z-index:30` qu'il avait posé sur `#dpdCorps` — et le contenu d'origine du
       tiroir (« le potager », MEMBRES, PIÈCES, « Planter un Promi dans la Nuée ») se
       peignait par-dessus le titre de la fiche SUIVANTE, tiroir fermé. Vu à l'œil sur
       `fiche-tenue_light`. Même mécanisme que le masque qui survit, un cran au-dessus :
       un style en ligne ne connaît pas la fin de son écran. On note les propriétés
       écrites ; `closeAll` retire exactement celles-là, et rien d'autre. */
    var v = (el.getAttribute('data-pose')||'').split(' ').filter(Boolean);
    for(var k in css){ el.style.setProperty(k, css[k], 'important');
      if(v.indexOf(k) < 0) v.push(k); }
    el.setAttribute('data-pose', v.join(' ')); }
  /* ⚑ ON MARQUE CE QU'ON MASQUE — voir `_rendMasques`. */
  function cache(el){ if(!el) return; pose(el, {display:'none'}); el.setAttribute('data-masque','1'); }
  function rend(el){ if(el) el.style.removeProperty('display'); }

  function estNuee(dp){ return !!(dp && (dp.classList.contains('dp-nuee') || dp.classList.contains('dp-mode-nuee'))); }
  function ouvert(){ var d = document.getElementById('dpDetails');
                     return !!(d && d.classList.contains('ouvert')); }

  /* ── LES CINQ BLOCS DU CADRE 84 + LES DEUX DU CADRE 86 ──
       cote y · hauteur · libellé · valeur · note de bas de carte  (§ cadres 84 et 86) */
  /* ═══ DEUX PAGES DE 760, ET ON DESCEND DE L'UNE À L'AUTRE ═══
     Les cadres 84 et 86 sont deux PAGES, pas deux moitiés d'une colonne (décision Tom) :
     86 n'a pas d'entête et repart de 46. Le geste qui manquait est LE DÉFILEMENT, et il se
     porte comme sur les autres Peaufiner (§2) : `.dpd-corps` devient un défileur plein
     cadre, **0 → 760**, et la barre reste clouée à 760. Rien ne monte, rien ne recouvre —
     le défileur s'arrête où la barre commence.
     Les deux pages sont donc empilées à **760 d'écart** : la page 2 au repos, c'est
     exactement le cadre 86, `Planter` à 46 et `DISSOUDRE` à 124 dans le cadre.
     L'ENTÊTE EST DANS LE DÉFILEUR, pas sur le poster : c'est ce qui fait qu'elle a disparu
     du cadre 86. Le mot-marque de la fiche (`#dptNat`) reste où la section 1 l'a posé. */
  var PAGE = 760;
  /* ⚑ « LE TRAIT » EN TÊTE — décision Tom, 2 septembre 2026 : « le pinceau se reprend
     depuis Peaufiner, haut de liste, sur une fiche COMME SUR UNE NUÉE ».
     ⚠ ET ELLE DÉCALE LE CADRE, JE LE DIS. Le §5 de CLAUDE.md pose qu'un ajout validé hors
     inventaire « ne décale AUCUNE cote du cadre » — mais cette règle vise un ajout qu'un
     GESTE fait paraître, pas une rangée permanente demandée en tête de liste. Ici la
     consigne est postérieure et explicite : les quatre cartes de la page 1 descendent
     donc de 80 (110 → 190, 230 → 310, 310 → 390, 418 → 498), l'écart de 80 étant celui
     que les cartes ont déjà entre elles. `npDiss` vit sur la page 2 et ne bouge pas.
     ⚠ ET LE RAIL Y EST PERMANENT, LÀ OÙ LA FICHE LE DÉPLIE. Les cartes d'une Nuée sont
     en POSITION ABSOLUE, à cote fixe : une rangée qui s'ouvre recouvrirait la suivante,
     ou obligerait à déplacer quatre cartes en JavaScript à chaque doigt. La carte prend
     donc 118 de haut — la hauteur haute que le cadre emploie déjà pour une NOTE — et
     porte son rail en permanence. L'écart entre cartes reste 16, comme partout :
     110 + 118 + 16 = 244, puis 364, 444, 552, la page 1 finissant à 656 pour 760.
     Les cadres 84-87 ne sont plus superposables sur ce point, et c'est un ajout demandé,
     pas une dérive. */
  var PLAN = [
    {id:'npTrait', y:110, h:118, lab:'LE TRAIT',       val:'trait',        ph:null, bas:null},
    {id:'npDesc',  y:244, h:104, lab:'DESCRIPTION',    val:null,           ph:'présente le Cercle, son but…', bas:'visible par tous les membres'},
    {id:'npMemb',  y:364, h:64,  lab:'MEMBRES',        val:'membres',      ph:null, bas:null},
    {id:'npFich',  y:444, h:92,  lab:'PIÈCES JOINTES', val:'fichiers',     ph:null, bas:'visibles par le Cercle'},
    {id:'npComm',  y:552, h:104, lab:'COMMENTAIRES',   val:null,           ph:'écris un mot…', bas:'visibles par les membres du Cercle'},
    {id:'npDiss',  y:PAGE+124, h:64, lab:'DISSOUDRE LE CERCLE', val:'→',    ph:null, bas:null}
  ];

  function valeurs(cle){
    var out = {membres:'personne encore', fichiers:'aucun fichier',
               trait:(window._pinceauNuee ? window._pinceauNuee(cle) : 'Plein')};
    try{
      var m = (typeof NUEEMEM !== 'undefined' && NUEEMEM[cle]) ? NUEEMEM[cle].slice() : [];
      /* ⚠ « +N » COMPTE LES NON NOMMÉS, MOI COMPRIS — la même règle que la ligne « à qui »
         de la fiche (cadre 58 : « Avec Rachel, Adrien, +3 » pour quatre membres). Le cadre
         86 écrit « Rachel · Adrien · +3 » ; l'app comptait `m.length-2` et sortait « +2 ». */
      if(m.length) out.membres = (m.length > 3)
        ? (m.slice(0,2).join(' · ') + ' · +' + (m.length-1)) : m.join(' · ');
      var n = 0;
      promises.forEach(function(q){ if(q.nuee === cle && q.files && q.files.length) n += q.files.length; });
      out.fichiers = n ? (n + ' fichier' + (n>1?'s':'')) : 'aucun fichier';
    }catch(_){ }
    return out;
  }

  /* ⚠ LES CARTES NE VIVENT PAS DANS `#dpdCorps`. Il porte la transition de dépliage
     (`max-height` + `overflow`) : ses enfants, même en position absolue, sortaient à
     **0 × 0 en (−14, −30)** — mesuré sur les quatre écrans. Les cotes du cadre 84 sont des
     coordonnées d'ÉCRAN ; les cartes sont donc filles du poster, comme tout le reste de la
     section 1. */
  function bati(corps){
    /* ⚠ LE GARDE SE PREND SUR LE DOM, PAS SUR UN DRAPEAU. Un drapeau posé sur `#dpdCorps`
       survit à une reconstruction du poster : `openEssaim` rebâtit ses enfants, les cartes
       disparaissent, le drapeau reste — et `bati` sortait sans rien reconstruire. Mesuré :
       les six blocs à « masqué » sur les quatre écrans du Peaufiner, après vingt écrans de
       fiche. On regarde donc si la carte EST LÀ. C'est le piège n° 4 du §8 de l'état des
       lieux : « un rendu qui remplace son propre marquage doit mémoriser ses entrées ». */
    if(document.getElementById(PLAN[0].id)) return;
    var h = '<div class="np-tete" id="npTete">'
          +   '<span id="npNom"></span>'
          +   '<span id="npFermer">\u2715 FERMER</span>'
          + '</div>';
    PLAN.forEach(function(b){
      h += '<div class="np-carte" id="' + b.id + '">'
         +   '<div class="np-lab"></div>'
         +   (b.ph  ? '<div class="np-ph"></div>' : '')
         +   (b.val ? '<div class="np-val"></div>' : '')
         +   (b.bas ? '<div class="np-bas"></div>' : '')
         + '</div>';
    });
    corps.insertAdjacentHTML('beforeend', h);
    /* ✕ FERMER : on ne réinvente pas la fermeture, on appelle celle du poster. */
    /* ⚑ MEMBRES S'OUVRE COMME « À QUI » SUR UNE FICHE (lot-GENS, 13 sept. 2026) : la carte grandit et porte le
       choix des personnes ; les cartes du dessous descendent d'autant. */
    var mb = document.getElementById('npMemb');
    if(mb) mb.addEventListener('click', function(ev){
      if(ev.target.closest && ev.target.closest('.gn')) return;
      ev.stopPropagation(); window._npGensOuvert = !window._npGensOuvert;
      try{ if(window._ficheTout) _ficheTout(); else window._nueePeaufiner(); }catch(_){} }, true);
    var f = document.getElementById('npFermer');
    if(f) f.addEventListener('click', function(ev){ ev.stopPropagation();
      var cb = document.querySelector('#detailPoster>.closeb');
      if(cb) cb.click(); else if(window.closeAll) closeAll(); });
  }

  /* ⚑ LE PEAUFINER D'UNE NUÉE NE SURVIT PAS À LA FICHE SUIVANTE.
     Il bâtit ses cartes dans `#dpdCorps` (`np-tete`, `np-carte`) et ne les retirait jamais :
     on ouvre le potager, on déplie son Peaufiner, on le ferme, on ouvre un Promi — et la
     fiche montre « DESCRIPTION · présente la Nuée, son but… · MEMBRES · PIÈCES JOINTES »
     par-dessus son titre. Mesuré : la fiche passe de **10 à 24 nœuds de texte visibles**,
     et perd `dpt-qui`, `dpt-titre` et `dpt-quand` sous les cartes.
     Vu à l'œil, pas à la sonde : c'est le duo côte à côte qui l'a sorti, parce qu'il ouvre
     les écrans les uns après les autres comme un doigt le ferait. Même famille que la
     hauteur d'une Nuée qui volait sa barre à la fiche suivante — on referme ce qu'on a
     ouvert, à l'endroit qui l'a ouvert. */
  /* v111 — l'emprunt des vrais champs par les cartes (voir la pose des cartes) : noté la première fois, rendu au départ */
  window._npChamp = function(carte, id, P, couleur, invite){
    var f = document.getElementById(id); if(!f) return;
    if(!f._npChez){ f._npChez = [f.parentNode, f.nextSibling, f.getAttribute('style'), f.getAttribute('placeholder'), f.getAttribute('rows')]; }
    if(f.parentNode !== carte) carte.insertBefore(f, P.nextSibling);
    P.style.setProperty('display','none','important');
    if(invite) f.setAttribute('placeholder', invite);
    if(f.tagName === 'TEXTAREA') f.setAttribute('rows','1');
    var cs = getComputedStyle(P);
    f.style.cssText = 'display:block!important;width:100%!important;box-sizing:border-box!important;margin:5.25px 0 0 0!important;padding:0!important;'
      + 'border:0!important;outline:0!important;background:none!important;box-shadow:none!important;resize:none!important;'
      + 'font-family:var(--f-libelle)!important;font-size:18px!important;line-height:1.25!important;height:22.5px!important;overflow:hidden!important;'
      + 'color:'+couleur+'!important;-webkit-text-fill-color:'+couleur+'!important;caret-color:'+couleur+'!important;'
      + 'position:relative!important;z-index:2!important;pointer-events:auto!important;-webkit-user-select:text!important;user-select:text!important;'
      + 'visibility:visible!important;opacity:1!important;font-size:max(18px,16px)!important';
    f.classList.add('np-champ');
  };
  window._npRendChamps = function(){
    ['nqNote','dCommentInput'].forEach(function(id){ var f = document.getElementById(id); if(!f || !f._npChez) return;
      var c = f._npChez; f._npChez = null; f.classList.remove('np-champ');
      if(c[2] == null) f.removeAttribute('style'); else f.setAttribute('style', c[2]);
      if(c[3] == null) f.removeAttribute('placeholder'); else f.setAttribute('placeholder', c[3]);
      if(f.tagName === 'TEXTAREA'){ if(c[4] == null) f.removeAttribute('rows'); else f.setAttribute('rows', c[4]); }
      try{ if(c[0]) c[0].insertBefore(f, (c[1] && c[1].parentNode === c[0]) ? c[1] : null); }catch(_){ } });
  };
  function rangeNuee(){
    try{ window._npRendChamps(); }catch(_){ }
    var corps = document.getElementById('dpdCorps');
    if(corps){
      var n = corps.querySelectorAll('.np-tete, .np-carte');
      for(var i=0;i<n.length;i++){ if(n[i].parentNode) n[i].parentNode.removeChild(n[i]); }
    }
    /* ⚠ ET LES `display` EN LIGNE QU'IL A POSÉS. Le Peaufiner d'une Nuée masque les trois
       lignes de l'entête (`display:none` en ligne) pour laisser la place à ses cartes, et
       montre son bouton « Planter un Promi dans la Nuée ». Sur la fiche suivante, la fiche
       n'avait plus ni « à qui », ni titre, ni état — et gardait le bouton de la Nuée.
       On RETIRE ce qu'il a posé, on ne pose rien de neuf : `_ficheCotes` repose ensuite ses
       cotes, et la cascade rend son `display` d'origine. */
    ['dptQui','dptTitre','dptQuand'].forEach(function(id){
      var e = document.getElementById(id);
      if(e && e.style.getPropertyValue('display')) e.style.removeProperty('display');
    });
    /* ⚠ SANS `!important` : le Peaufiner d'une Nuée montre CELUI QU'IL GARDE avec un
       `display:flex !important` à lui, et il repasse après nous. Une priorité ici le
       clouait fermé — mesuré : « Planter un Promi dans la Nuée » disparaissait du cadre 86,
       les deux jumeaux à `none !important`. On range, on ne verrouille pas. */
    ['nfAdd','nqAddPromi'].forEach(function(id){
      var e = document.getElementById(id);
      if(e && e.style.getPropertyValue('display') !== 'none') e.style.display = 'none';
    });
  }
  window._nueePeaufinerRange = rangeNuee;
  /* Le Peaufiner d'une Nuée BÂTIT (ses cartes) autant qu'il masque : il s'inscrit au
     registre des rangeurs, et `closeAll` le passe comme les autres. */
  (window._rangeurs = window._rangeurs || []).push(rangeNuee);

  window._nueePeaufiner = function(){ try{
    var dp = document.getElementById('detailPoster');
    if(!dp || !dp.classList.contains('show') || !estNuee(dp)){ rangeNuee(); return false; }
    var corps = document.getElementById('dpdCorps');
    var cle = (typeof curNuee !== 'undefined') ? curNuee : null;
    if(!corps || !cle) return false;
    var clair = document.getElementById('device').classList.contains('light');
    var encre = clair ? ENCRE : CREME;
    var lab   = clair ? MAUVE : CLAIRN;
    /* ⚠ IL Y A DEUX BOUTONS « PLANTER DANS LA NUÉE », et c'est la vraie histoire du
       défaut signalé à y = 0 : `#nqAddPromi`, celui du balisage d'origine du poster
       (l. ~2622), et `#nfAdd`, bâti par l'entête du fil. Le premier se posait par-dessus
       « ✕ FERMER » — relevé par `redteam_aveugle` : « FERMER ⨯ ✦ Planter un Prom ».
       Le §12 n'en met AUCUN sur la fiche au repos : leur place est le Peaufiner (cadre 86).
       On en garde donc UN SEUL, ici, et on masque l'autre — sans rien retirer du produit :
       les deux mènent au même geste, planter dans la Nuée. */
    var nfAdd = document.getElementById('nfAdd') || document.getElementById('nqAddPromi');
    var jumeau = (nfAdd && nfAdd.id === 'nfAdd') ? document.getElementById('nqAddPromi')
                                                 : document.getElementById('nfAdd');
    if(jumeau) cache(jumeau);
    /* ⚠ ET IL Y EN A UN TROISIÈME. La liste de Peaufiner de la SECTION 2 bâtit son propre
       « Planter un Promi dans la Nuée » (`.s2-bouton`), qui ne porte ni `nfAdd` ni
       `nqAddPromi` : le garde ci-dessus ne le voyait pas. Mesuré au balayage des
       collisions : deux textes identiques superposés à 100 % dans `#dpdCorps`, en clair.
       Même règle que le jumeau — on en garde UN, on range les autres, rien n'est retiré du
       produit : ils mènent tous au même geste. On vise par LE MOT, parce que c'est ce qui
       fait le doublon aux yeux. */
    try{
      var mot = (nfAdd && (nfAdd.textContent||'').trim()) || 'Planter un Promi dans le Cercle';
      var corps0 = document.getElementById('dpdCorps');
      if(corps0) [].slice.call(corps0.querySelectorAll('.s2-bouton, button, a'))
        .forEach(function(x){
          if(x===nfAdd || x===jumeau) return;
          if((x.textContent||'').trim() === mot) cache(x);
        });
    }catch(_){}

    if(!ouvert()){
      /* le panneau est replié : on rend l'écran à `_ficheNuee`, et le bouton à sa place. */
      [].forEach.call(corps.querySelectorAll('.np-carte'), cache);
      if(nfAdd && nfAdd.getAttribute('data-np-pris') === '1'){
        nfAdd.removeAttribute('data-np-pris');
        nfAdd.removeAttribute('style');
        /* ON LE REND À SON NID. Le déplacer, c'est aussi devoir le remettre : sans ça il
           resterait sur le poster, hors du fil, et la fiche au repos aurait deux boutons
           — ou aucun. Le nid est mémorisé au moment de la prise. */
        try{ var nid = document.getElementById(nfAdd.getAttribute('data-np-nid') || '');
             if(nid && nfAdd.parentNode !== nid) nid.insertBefore(nfAdd, nid.firstChild); }catch(_){ }
        if(nfAdd.getAttribute('data-np-mot')) nfAdd.textContent = nfAdd.getAttribute('data-np-mot');
      }
      /* ⚠ AU REPOS, LA FICHE NE PORTE PAS CE BOUTON. Cherché dans les vingt écrans du §12 :
         aucune ligne « Planter ». Cherché dans `promi-nuee-toile.html` : zéro occurrence. Il
         n'existe qu'aux cadres 86/87 — DANS LE PEAUFINER. Laissé sur la fiche, il tombait à
         y = 776 sous une barre qui commence à 760, et c'était le dernier rouge de
         `redteam_aveugle` (« Nuée · rien ne se superpose », deux thèmes).
         ON NE LE RETIRE PAS DU PRODUIT — sa place est portée, il y est, et c'est là qu'on
         plante dans une Nuée. On le masque seulement là où l'inventaire ne le met pas. */
      /* ⚑ Q213 (Tom, 13 sept.) : AU REPOS, LA FICHE PORTE L'ENTRÉE — dernière ligne du fil, sous la dernière carte d'une
         Nuée pleine, sous « ENCORE AUCUNE PAROLE » d'une Nuée vide. Elle n'est plus masquée ici : la raison d'hier
         (elle tombait à y 776 sous la barre) ne vaut plus — le fil défile et `#dpMain` porte sa hauteur. */
      var pd = document.getElementById('npPied'); if(pd) cache(pd);
      cache(document.getElementById('npTete'));
      dp.classList.remove('s2-ouv');
      try{ corps.removeAttribute('style'); }catch(_){ }
      return false;
    }

    bati(corps);
    var v = valeurs(cle);
    var nom = (typeof NUE !== 'undefined' && NUE[cle]) ? NUE[cle] : cle;

    /* ── LE DÉFILEUR (§2, même mécanique) : `s2-ouv` fait de `.dpd-corps` une page pleine,
         0 → 760, et cloue la barre à 760. On lui donne DEUX pages de haut. ── */
    dp.classList.add('s2-ouv');
    pose(corps, {display:'block', position:'absolute', left:'0', top:'0',
                 width:'390px', height:'760px', 'overflow-y':'auto', 'overflow-x':'hidden',
                 'max-height':'none', margin:'0', padding:'0', 'z-index':'30'});
    /* ⚠ RIEN D'AUTRE QUE LES DEUX PAGES DANS LE DÉFILEUR. Le tiroir de l'app y déverse
       aussi les blocs d'une Nuée (thème, membres, invitation, dissolution) : laissés là, ils
       s'ajoutent au défilement — relevé `scrollHeight` 2330 pour deux pages de 760 — et on
       descend dans du vide après le cadre 86. C'est le même piège que la section 2 avait
       rencontré, et qu'un commentaire du bloc `lot-S2` décrit déjà : « ils réapparaissaient
       SOUS la page ». On masque nœud par nœud, jamais par un conteneur. */
    [].forEach.call(corps.children, function(x){
      if(x.id === 'npPied' || x.id === 'npTete' || x.id === 'nfAdd') return;
      if(x.classList && x.classList.contains('np-carte')) return;
      cache(x);
    });
    var pied = document.getElementById('npPied');
    if(!pied){ pied = document.createElement('div'); pied.id = 'npPied'; corps.appendChild(pied); }
    pose(pied, {display:'block', position:'relative', width:'1px',
                height:(2*PAGE)+'px', margin:'0', padding:'0', background:'none'});

    /* ── L'ENTÊTE (cadre 84), DANS le défileur : elle s'en va avec la page 1 ── */
    var tete = document.getElementById('npTete');
    pose(tete, {visibility:'visible', display:'flex', position:'absolute',
                left:'24px', top:'36px', width:'342px', height:'40px',
                'align-items':'center', 'justify-content':'space-between',
                margin:'0', padding:'0', background:'none'});
    var nomEl = document.getElementById('npNom');
    if(nomEl){ nomEl.textContent = nom;
      pose(nomEl, {visibility:'visible', 'font-family':'var(--f-libelle)',
                   'font-weight':'700', 'font-size':'26px', 'letter-spacing':'-.03em',
                   color:encre, '-webkit-text-fill-color':encre}); }
    var ferm = document.getElementById('npFermer');
    /* ⚑ LE MÊME ✕ FERMER QUE LE PEAUFINER D'UNE FICHE (13 sept. 2026) : il sortait en Apfel 16 avec deux espaces
       insécables, plus large de 25 px que celui d'un Promi. */
    if(ferm && ferm.textContent !== '\u2715 FERMER') ferm.textContent = '\u2715 FERMER';
    if(ferm) pose(ferm, {visibility:'visible', 'font-family':'var(--f-texte)',
                         'font-weight':'500', 'font-size':'13px', 'letter-spacing':'.20em', 'white-space':'nowrap',
                         cursor:'pointer', color:encre, '-webkit-text-fill-color':encre});

    /* ── LA FICHE S'EFFACE : le cadre 84 ne porte NI Toile, NI Noyaux, NI fil ── */
    ['dpTrameCv','dAura','dptQui','dptTitre','dptQuand','dpNueeFil'].forEach(function(id){
      cache(document.getElementById(id)); });
    pose(dp, {'--nuee-bande':'0px'});

    /* ── LES CARTES, à leurs cotes absolues ── */
    var gensH = 0, gHote = null;
    try{
      var mbEl = document.getElementById('npMemb');
      gHote = mbEl ? mbEl.querySelector('.gn') : null;
      if(window._npGensOuvert && mbEl && window._gensFiche){
        if(!gHote){ gHote = window._gensFiche('nuee'); mbEl.appendChild(gHote); }
        pose(gHote, {display:'grid', visibility:'visible', width:'100%'});
        gensH = Math.ceil(gHote.offsetHeight) + 14 + 16;
      } else if(gHote){ pose(gHote, {display:'none'}); }
    }catch(_){ gensH = 0; }
    PLAN.forEach(function(b){
      var el = document.getElementById(b.id); if(!el) return;
      var bY = b.y + ((gensH && b.y > 364) ? gensH : 0), bH = b.h + ((gensH && b.id === 'npMemb') ? gensH : 0);
      /* ⚠ `visibility` EXPLICITE. Quand le panneau s'ouvre, le poster prend la classe
         `s2-ouv` — le crible de la SECTION 2, écrit pour le Peaufiner d'une PROMESSE : il
         passe en `visibility:hidden` tout ce que son inventaire ne liste pas, et les cartes
         d'une Nuée n'y sont pas. Mesuré : `display:block` et pourtant « masqué » sur les
         quatre écrans. On ne touche pas au crible — il protège la section 2 — on déclare
         ces six nœuds-ci visibles, nommément. C'est le §8 de CLAUDE.md : un crible se pose
         nœud par nœud, et se lève de même. */
      pose(el, {visibility:'visible', display:'block', position:'absolute', left:'24px', top:bY+'px',
                width:'342px', height:bH+'px', 'box-sizing':'border-box',
                /* ⚑ LA GRAMMAIRE DES CONTOURS (loi 2, Q157) — trait 2, couleur du corps,
                   RAYON = HAUTEUR ÷ 2. La hauteur vient de `PLAN`, pas d'une mesure : une
                   cote se calcule, elle ne se lit jamais sur elle-même (CLAUDE.md §8). */
                border:'2px solid '+encre,
                /* ⚑ P (Tom, 11 sept. 2026, chantier 65) : un champ de TROIS LIGNES ET PLUS — libellé, texte, ligne de
                   visibilité — prend le rayon 30 du grand panneau de la grammaire. Rayon = hauteur ÷ 2 y collait la 1re et la
                   dernière ligne à la courbe (7,4 / 5,8 px ; la norme du champ à deux lignes est 12,9). */
                'border-radius':(window._rayonChamp ? window._rayonChamp(bH) : bH/2)+'px',   /* la règle de hauteur (lot-CERCLE-MUR) */
                /* ⚑ LE CADRE NE SE SOUSTRAIT PAS — C'EST LE RESTE QUI MONTE JUSQU'À LUI
                   (loi 2). Le trait passé de 3 à 2 rend 1 px de boîte de contenu sur chaque
                   bord : sans compensation, TOUT ce que la carte porte remonte d'un pixel.
                   Mesuré par `redteam_air` : « visible par tous les membres » → « Rachel ·
                   Adrien · +3 » tombait de 54 à 53, dans les deux thèmes. On rend au padding
                   le pixel que le trait a lâché ; rien à l'intérieur ne bouge. */
                padding:(b.ph ? '17px 23px' : '1px 23px'), margin:'0', background:'none'});
      var L = el.querySelector('.np-lab');
      pose(L, {'font-family':'var(--f-texte)', 'font-weight':'500',
               'font-size':'11.5px', 'letter-spacing':'.18em',
               color:lab, '-webkit-text-fill-color':lab});
      if(L) L.textContent = b.lab;
      var P = el.querySelector('.np-ph');
      if(P){ P.textContent = b.ph;
        pose(P, {'font-family':'var(--f-libelle)', 'font-weight':'600',
                 'font-size':'18px',
                 /* ⚑ LE TEXTE DU MILIEU CENTRÉ ENTRE LE HAUT ET LE BAS DU CONTOUR (Tom, 11 sept.) : carte de 104, trait 2,
                    dessin du texte 22 → son haut à 2 + (100 − 22) / 2 = 41 ; le libellé finit à 34 → 7 (était 9 : 41 / 37). */
                 'margin-top':'5.25px', 'line-height':'1.25',   /* ⚑ v96 : le texte a grandi (+12 %) — le mot se CENTRE entre le libellé (34) et la ligne du bas (67) : (67 − 34 − 22,5) / 2 = 5,25 de chaque côté (était 7 au-dessus, 3,5 dessous) */
                 color:lab, '-webkit-text-fill-color':lab}); }
      /* ⚑ v111 (Tom : « dans un Cercle, sur le simulateur, je ne peux pas taper de texte ») — ces deux cartes ne peignaient que
         le TEXTE D'INVITE : aucun champ n'y était branché (le constructeur de la section 2, qui alterne avec celui-ci, empruntait
         les vrais). On y emprunte les VRAIS champs du poster — la description (#nqNote, gardée dans NUENOTE) et le mot
         (#dCommentInput) — posés à la place du texte, à sa police et à sa couleur ; ils rentrent chez eux quand les cartes partent. */
      if(P && (b.id === 'npDesc' || b.id === 'npComm') && window._npChamp)
        window._npChamp(el, b.id === 'npDesc' ? 'nqNote' : 'dCommentInput', P, lab, b.ph);
      var V = el.querySelector('.np-val');
      if(V){ V.textContent = (b.val === 'membres') ? v.membres
                           : (b.val === 'fichiers') ? v.fichiers
                           : (b.val === 'trait')    ? v.trait : b.val;
        pose(V, {'font-family':'var(--f-libelle)', 'font-weight':'700',
                 'font-size':'18px', color:encre, '-webkit-text-fill-color':encre}); }
      var B = el.querySelector('.np-bas');
      if(B){ B.textContent = b.bas;
        pose(B, {'font-family':'var(--f-libelle)', 'font-weight':'600',
                 'font-size':'14px', color:lab, '-webkit-text-fill-color':lab}); }
      /* MEMBRES, PIÈCES JOINTES et DISSOUDRE portent leur valeur À DROITE, sur une ligne */
      if(!b.ph){ pose(el, {display:'flex', 'align-items':'center',
                           'justify-content':'space-between', 'flex-wrap':'wrap'}); }
      if(b.id === 'npMemb'){ pose(el, gensH ? {'align-content':'flex-start', 'padding-top':'20px'}
                                            : {'align-content':'normal', 'padding-top':'1px'}); }
      if(b.bas && !b.ph){ pose(B, {width:'100%'}); }
      /* ⚑ CHANTIER 66 — PIÈCES JOINTES D'UNE NUÉE PREND LES PLACES DE CELLE D'UNE FICHE (un composant commun ne se
         décline pas, CLAUDE §5) : libellé à 23, bas à 50,8 du haut de la carte, comme sur la fiche. Rangées collées en
         haut, puis calées (mesuré). Avant : 14,8 / 60,3 — à 6,35 px de la courbe contre 12,9 sur la fiche. */
      if(b.id === 'npFich'){ pose(el, {'align-content':'flex-start', 'padding-top':'17.5px'}); if(B) pose(B, {'margin-top':'9.3px'}); }
      /* ⚑ ET LE NŒUD CLOUÉ EN ABSOLU SE RECALE À LA MAIN. Pour un enfant `absolute`,
         `bottom` et `left` partent du BORD DE PADDING — que le trait passé de 3 à 2 a
         déplacé d'un pixel vers l'extérieur. Le padding n'y change rien : il ne déplace
         que le flux. Mesuré par `redteam_air` : « visible par tous les membres » tombait
         de 331 à 332 et l'air sous lui de 54 à 53, dans les deux thèmes. On rend le pixel
         que le trait a lâché — le cadre ne se soustrait pas (loi 2). */
      if(b.ph && B){ pose(B, {position:'absolute', left:'23px', bottom:'15px'}); }
    });

    /* ── « PLANTER UN PROMI DANS LA NUÉE » — le bouton de l'app, déplacé (cadre 86) ── */
    if(nfAdd && nfAdd.parentNode !== corps){
      /* ⚠ ON LE SORT DE SON NID. `#nfAdd` vit dans `.nf-tete`, à l'intérieur de
         `#dpNueeFil` — que le Peaufiner masque. Laissé là, il sortait à **0 × 0 en
         (−14, −30)**, mesuré. On le déplace sur le poster, et on note d'où il vient. */
      if(nfAdd.getAttribute('data-np-pris') !== '1'){
        try{ var nidEl = nfAdd.parentNode;
             if(nidEl && !nidEl.id) nidEl.id = 'npNidAdd';
             nfAdd.setAttribute('data-np-nid', nidEl ? nidEl.id : '');
             nfAdd.setAttribute('data-np-mot', (nfAdd.textContent||'').trim());
             corps.appendChild(nfAdd); }catch(_){ }
      }
      nfAdd.setAttribute('data-np-pris', '1');
      pose(nfAdd, {visibility:'visible', display:'flex', position:'absolute', left:'24px', top:(PAGE+46+gensH)+'px',
                   /* 348 × 68 hors tout, et non 342 × 62 : le bloc du cadre 86 porte
                      `width:342 + border:3` SANS `box-sizing:border-box` — les cartes, elles,
                      l'ont. Le bouton est donc 6 px plus large que DISSOUDRE dans la planche.
                      C'est étrange, et le §8 bis de CLAUDE.md dit qu'une valeur étrange l'est
                      pour une raison : on suit le moodboard, on n'arrondit pas. */
                   width:'348px', height:'68px', margin:'0', padding:'0',
                   'align-items':'center', 'justify-content':'center',
                   background:MAUVE, border:'3px solid '+MAUVE, 'border-radius':'31px',
                   'font-family':'var(--f-libelle)', 'font-weight':'700',
                   'font-size':'19px', color:CREME, '-webkit-text-fill-color':CREME});
      /* ⚑ Q213 : le mot vit dans le bouton lui-même, « Planter dans la Nuée » — on ne le réécrit plus */
    }
    if(nfAdd && nfAdd.getAttribute('data-np-pris') === '1') pose(nfAdd, {top:(PAGE+46+gensH)+'px'});
    if(pied) pose(pied, {height:(2*PAGE+gensH)+'px'});
    /* ⚑ v99 — LA CARTE « LE TRAIT » SE GARNIT ICI, QUAND ELLE EST POSÉE. Son garnisseur ne passait qu'à heure fixe après un clic
       (100 · 320 · 700 ms) : en WebKit la carte naît plus tard, et elle restait vide jusqu'au clic suivant (mesuré : 0 pastille à
       la 2e ouverture, 12 à la 3e). Le placement l'appelle, à chaque ouverture — il compare avant d'agir. */
    try{ if(window._pinceauNueeCarte) window._pinceauNueeCarte(); }catch(_){ }
    return true;
  }catch(err){ return false; } };

  /* ── ON SE BRANCHE APRÈS `_ficheTout` : la fiche pose ses cotes, le Peaufiner reprend
       la main quand il est ouvert. §13 : « sur cette page, Peaufiner ne s'ouvre qu'en
       touchant sa barre » — on ne câble donc AUCUN autre déclencheur. ── */
  var _tout = window._ficheTout;
  if(typeof _tout === 'function'){
    window._ficheTout = function(){ var r = _tout.apply(this, arguments);
      try{ window._nueePeaufiner(); }catch(_){ } return r; };
  }
  var _nuee = window._ficheNuee;
  if(typeof _nuee === 'function'){
    window._ficheNuee = function(){ var r = _nuee.apply(this, arguments);
      try{ window._nueePeaufiner(); }catch(_){ } return r; };
  }
  /* ── LA BARRE OUVRE LE PANNEAU. §13 : « sur cette page, Peaufiner ne s'ouvre qu'en
       touchant SA BARRE. Partout ailleurs c'est l'inverse. »
       ⚠ Le clic ne basculait rien sur une fiche de Nuée : mesuré, `#dpDetails.className`
       reste vide après un clic sur `.dpd-tog`. Le seul écouteur de bascule est posé À LA
       CRÉATION de `#dpDetails`, dans `renderDetail` — et une fiche de Nuée passe par
       `openEssaim`, pas par lui. On pose donc la bascule ici, POUR LA NUÉE SEULEMENT, et
       nulle part ailleurs : le Peaufiner d'une promesse garde le sien. ── */
  document.addEventListener('click', function(ev){
    if(!ev.target || !ev.target.closest) return;
    if(!ev.target.closest('#dpDetails .dpd-tog')) return;
    var dp = document.getElementById('detailPoster');
    if(estNuee(dp)){
      var d = document.getElementById('dpDetails');
      if(d && !d.classList.contains('ouvert')) d.classList.add('ouvert');
    }
    setTimeout(function(){ try{ (window._ficheTout||window._ficheNuee)(); }catch(_){ } }, 30);
    setTimeout(function(){ try{ (window._ficheTout||window._ficheNuee)(); }catch(_){ } }, 420);
  }, true);
})();
