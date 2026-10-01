
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ LE MUR DU CERCLE — POSÉ LÀ OÙ IL MANQUAIT (Tom, 11 sept. 2026) : « il ne s'agit pas de corriger un mur, il s'agit
   d'en poser un là où il n'y en a pas. Les quatre réglages doivent exister, visibles et verrouillés, dans le Peaufiner
   d'une fiche et de la page +. C'est là qu'on les découvre, c'est là qu'on veut les obtenir. »
   Mesuré avant : sur une fiche le mur existait (même plantée à neuf) ; sur la page + — et donc sur un gardé de côté,
   qui la rouvre — il manquait (`peaufBati` n'appelle pas `cercle()`).
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
(function(){
  /* comparer avant d'agir (CLAUDE §8) : on n'écrit une propriété que si elle diffère */
  function P(e, k, v){ if(!e) return; if(e.style.getPropertyValue(k) === v && e.style.getPropertyPriority(k) === 'important') return;
    e.style.setProperty(k, v, 'important'); }

  /* ── 1 · LE MUR DE LA PAGE + — la brique MÊME de l'app, en fin de liste (après les pièces jointes : la page + n'a ni
     commentaires, ni relance, ni suppression). ⚠ LA LISTE EST REBÂTIE DERRIÈRE : `peaufBati` repasse après les clics
     (les écouteurs du pinceau, 90 / 280 / 650 ms) — un bloc posé une fois disparaît en moins d'une seconde (mesuré à la
     planche 2). On le remet donc chaque fois que la liste est refaite SANS lui : un observateur, qui compare. ── */
  function murPagePlus(){
    var cs = document.getElementById('createSheet'); if(!cs || !cs.classList.contains('pp-peauf')) return;
    var l = cs.querySelector(':scope > .dpd-corps .s2-liste') || cs.querySelector('.s2-liste'); if(!l) return;
    if(l.querySelector('.s2-cercle')) return;
    if(!window._s2Briques || !window._s2Briques.cercle) return;
    l.appendChild(window._s2Briques.cercle());
    try{ if(window._cerclePaye) window._cerclePaye(); }catch(_){}
  }

  /* ── 2 · LES CHAMPS À TROIS LIGNES — le texte du milieu centré, et le champ qui grandit avec son texte ──
     Tom : « descends un peu « ajoute un mot, un contexte… » — elle n'est pas centrée entre le haut et le bas du
     contour. Mesure les deux écarts, ils doivent être égaux. » Et le chantier 68 : une note de trois lignes était
     PEINTE sur 56 px pour une max-height de 44, sa 3ᵉ ligne passait sous « visible par Rachel ».
     ⚑ LA COTE SE CALCULE (CLAUDE §8), jamais sur elle-même : le dessin d'une ligne de Bricolage 600 / 18 fait 22 dans sa
     ligne de 22,5 et commence en haut de sa boîte (mesuré). Pour des écarts égaux, son haut tombe à
     bord + (hauteur de base − 2 × bord − 22) / 2 — 48 dans une boîte de 118 — ET CE HAUT NE BOUGE PAS AVEC LE NOMBRE DE
     LIGNES : la boîte grandit d'une ligne (22,5) par ligne de texte en plus, par le bas, et la ligne de visibilité, clouée
     au bas, descend avec elle. La marge sous le libellé se calcule sur la position du LIBELLÉ, qui ne dépend pas d'elle. */
  var GLYPHE = 22, LH = 22.5;
  /* ⚑ LA BASCULE DU RAYON — Tom, 11 sept. : « rayon = moitié de la hauteur jusqu'à deux lignes, 30 au-delà. Un champ à une
     ligne garde sa pilule, un champ qui s'ouvre gagne l'air qu'il lui faut. La loi du §2 tient là où elle a du sens, et
     cède seulement là où elle produit un défaut. Mesure le seuil exact — à quelle hauteur la pilule commence à manger le
     texte — et pose la bascule là, pas à un nombre de lignes arbitraire. »
     MESURÉ SUR L'ENCRE (sauvegardes/audit-cercle/seuil_encre.py, _analyse, _bascule) : chaque champ capturé, sa distance
     encre → courbe intérieure recalculée pour tout rayon. « Manger » = serrer l'encre plus que ne le fait un champ OUVERT
     au rayon 30 (P, validé) : son air le plus serré vaut C = 15,19 (NOTE de la page +, la ligne de visibilité). Un champ à
     deux rangées qui s'ouvre (rangée du haut à sa place, rangée du bas clouée au bas) tient C en pilule jusqu'à 94,53 pour
     le plus serré (PIÈCES JOINTES de la page +), 96,21 (Nuée), 105,95 (fiche). ⇒ la bascule est à 94,5 : tout champ de
     92 garde sa pilule, tout champ de 104 et plus prend 30. Les réglages d'une ligne (64) ne sont jamais mangés : leur
     ligne passe par l'axe. ⚠ UN SEUL PROPRIÉTAIRE : cette fonction. La Nuée (lot-NUEE-PEAUFINER, `pose`) l'appelle ;
     les rangées de Peaufiner la reçoivent ci-dessous. */
  var SEUIL_PILULE = 94.5;
  function rayon(h){ return h <= SEUIL_PILULE ? h / 2 : 30; }
  window._rayonChamp = rayon; window._seuilPilule = SEUIL_PILULE;
  function nbLignes(t){
    if(!t || t.tagName !== 'TEXTAREA' || !t.value) return 1;
    var h = t.style.getPropertyValue('height'), pr = t.style.getPropertyPriority('height');
    t.style.setProperty('height', '0px', 'important');
    var lh = parseFloat(getComputedStyle(t).lineHeight) || LH;
    var n = Math.max(1, Math.round(t.scrollHeight / lh));
    if(h) t.style.setProperty('height', h, pr); else t.style.removeProperty('height');
    return n;
  }
  function caleZone(z){
    if(!z || !z.isConnected) return;
    var lab = z.querySelector('.s2-lab'), mid = z.querySelector('.s2-txt'); if(!lab || !mid) return;
    var bw = parseFloat(getComputedStyle(z).borderTopWidth) || 2;
    var H0 = z.classList.contains('s2-z104') ? 104 : 118;
    var lh = parseFloat(getComputedStyle(mid).lineHeight) || LH;
    var n = nbLignes(mid);
    var haut = bw + ((H0 - 2 * bw) - GLYPHE) / 2;
    /* ⚠ le bas du libellé se lit en FRACTION : offsetTop / offsetHeight arrondissent à l'entier (30,5 lu 31 sur la page +,
       le texte sortait centré à 45,5 / 46,5). Le rectangle, ramené à l'échelle du champ LUI-MÊME (largeur rendue ÷
       largeur de mise en page), ne dépend ni du cadre ni de la marge qu'on pose ensuite. */
    var zr = z.getBoundingClientRect(), lr = lab.getBoundingClientRect(), ech = (zr.width / (z.offsetWidth || zr.width)) || 1;
    var basLibelle = (lr.bottom - zr.top) / ech;
    var marge = Math.round((haut - basLibelle) * 10) / 10;
    /* ⚑ v97 (Tom, iPhone : « écris un mot est mal placé dans son encart, sur les fiches ») — la ligne du bas (« visible par… ») est
       clouée à 14 du bord : centré dans la CARTE, le mot la touchait presque (5,6 sur une carte de 104). Il se centre entre le bas du
       libellé et le haut de cette ligne. Ni l'un ni l'autre ne dépendent du mot : pas de boucle (§8). Sans ligne du bas, l'ancien centrage. */
    var vis = z.querySelector('.s2-vis');
    if(vis && vis.getClientRects().length && n === 1){ var vr = vis.getBoundingClientRect(), mr = mid.getBoundingClientRect();
      var hautVis = (vr.top - zr.top) / ech, hMot = (mid.tagName === 'TEXTAREA') ? n * lh : mr.height / ech;   /* v98 : la hauteur qu'on POSE juste après (une zone de texte porte encore sa hauteur par défaut, 56) */
      marge = Math.round(((hautVis - basLibelle - hMot) / 2) * 10) / 10; }
    P(mid, 'margin-top', marge + 'px');
    if(mid.tagName === 'TEXTAREA'){ P(mid, 'height', (n * lh) + 'px'); P(mid, 'max-height', 'none'); P(mid, 'overflow', 'hidden'); }
    P(z, 'height', (H0 + (n - 1) * lh) + 'px');
    P(z, 'border-radius', rayon(H0 + (n - 1) * lh) + 'px');      /* la hauteur CALCULÉE, jamais relue (§8) */
    if(z.getAttribute('data-cercle-lignes') !== String(n)) z.setAttribute('data-cercle-lignes', String(n));
  }
  /* les autres rangées de Peaufiner (une ligne, deux rangées) : leur hauteur vient du CSS et ne dépend pas du rayon —
     la lire ne crée aucune boucle. Échelle du champ lui-même (largeur rendue ÷ largeur de mise en page). */
  function arrondit(r){
    if(!r || !r.isConnected || r.classList.contains('s2-zone')) return;
    var q = r.getBoundingClientRect(); if(!q.height) return;
    var h = Math.round(q.height / ((q.width / (r.offsetWidth || q.width)) || 1) * 100) / 100;
    P(r, 'border-radius', rayon(h) + 'px');
  }
  function caleTout(){
    document.querySelectorAll('#detailPoster .s2-zone, #createSheet.pp-peauf .s2-zone').forEach(caleZone);
    document.querySelectorAll('#detailPoster .s2-liste .s2-reg, #createSheet.pp-peauf .s2-liste .s2-reg').forEach(arrondit);
  }
  window._cercleCaleZones = caleTout;

  var rafId = null;
  function passe(){ if(rafId) return; rafId = requestAnimationFrame(function(){ rafId = null;
    try{ murPagePlus(); }catch(_){ } try{ caleTout(); }catch(_){ } }); }
  window._cercleMurPasse = passe;
  ['detailPoster', 'createSheet'].forEach(function(id){
    var h = document.getElementById(id);
    /* childList seulement : nos propres écritures sont des STYLES — l'observateur ne se réveille pas lui-même (§8) */
    /* ⚠ la zone de la page + est rebâtie sans cesse (mesuré : six zones en 2,5 s) : on la recale DANS LA FOULÉE de la
       mutation, avant toute image — à l'image suivante, la zone neuve restait un instant à 118 avec trois lignes. */
    if(h) new MutationObserver(function(){ try{ caleTout(); }catch(_){ } passe(); }).observe(h, {childList:true, subtree:true});
  });
  document.addEventListener('input', function(ev){ var z = ev.target && ev.target.closest && ev.target.closest('.s2-zone'); if(z) caleZone(z); }, true);
  document.addEventListener('click', function(){ [80, 300, 700].forEach(function(d){ setTimeout(passe, d); }); }, true);
  [0, 200, 800].forEach(function(d){ setTimeout(passe, d); });

  /* ── 3 · LE CHEMIN — l'encart du mur ouvre la page du Cercle PAR-DESSUS, et l'achat ramène au même Peaufiner ──
     (planche 2 et 3 : « après l'achat, même place, nets » — c'est là qu'on les a découverts, c'est là qu'on les voulait).
     Aujourd'hui l'encart passait par ouvreCercle → closeAll : depuis la page + la phrase en cours était perdue, et l'achat
     menait à l'Aura. ⚠ Le « par-dessus » ne vaut QUE pour les encarts du mur ; les autres portes gardent leur chemin. */
  function ps(){ return document.getElementById('plusScreen'); }
  function ouvreDessus(){
    var p = ps(); if(!p) return;
    p.classList.add('cercle-dessus'); p.classList.add('show'); try{ p.scrollTop = 0; }catch(_){}
    var trace = function(){ try{ if(typeof drawCercleHero === 'function') drawCercleHero(); }catch(_){ } };
    try{ requestAnimationFrame(function(){ trace(); setTimeout(trace, 320); }); }catch(_){ trace(); }
  }
  function fermeDessus(){ var p = ps(); if(p){ p.classList.remove('show'); p.classList.remove('cercle-dessus'); } }
  window._cercleDessus = ouvreDessus;
  /* à la fenêtre, en capture : on passe AVANT l'écouteur de l'encart (qui clique #openPlusTop → ouvreCercle → closeAll) */
  window.addEventListener('click', function(ev){
    var t = ev.target; if(!t || !t.closest) return;
    if(t.closest('#detailPoster .s2-encart, #createSheet .s2-encart')){
      ev.preventDefault(); ev.stopImmediatePropagation(); ouvreDessus(); return; }
    var p = ps(); if(!p || !p.classList.contains('cercle-dessus')) return;
    if(t.closest('#buyYear, #buyMonth')){
      ev.preventDefault(); ev.stopImmediatePropagation();
      try{ setPremium(true); }catch(_){ }
      fermeDessus();
      try{ if(typeof toast === 'function') toast('Tu es Membre Ma Parole ! ✓ · tout Promi débloqué'); }catch(_){ }
      try{ if(window._cerclePaye) window._cerclePaye(); }catch(_){ }
      passe(); return; }
    if(t.closest('#plusScreen [data-close], #plusScreen .closeb')){
      ev.preventDefault(); ev.stopImmediatePropagation(); fermeDessus(); return; }
  }, true);
  /* rien ne survit à closeAll (CLAUDE §8) : le « par-dessus » est rendu avec le reste */
  (window._rangeurs = window._rangeurs || []).push(fermeDessus);

  /* ── 4 · L'ENCART DES RÉGLAGES — « ✦ Le Cercle », toujours (Q201). setPremium(true) le réécrivait en « Membre du
     Cercle ✓ », que setPremium(false) ne rendait jamais : un utilisateur gratuit le voyait après une fin d'abonnement
     (audit, P4). On repasse DERRIÈRE setPremium, on ne l'écoute pas (§8 « repeindre derrière le moteur »). ── */
  function encartReglages(){
    var op = document.getElementById('openPlusTop'); if(!op) return;
    var d = document.getElementById('device'), mot = (d && d.classList.contains('premium')) ? 'Tu es Membre Ma Parole\u00a0!' : 'Ma Parole\u00a0!';   /* v106 (Tom) : payé, les Réglages disent « Tu es Membre Ma Parole ! » */
    var t = op.querySelector('.sc-t'); if(t && t.textContent !== mot) t.textContent = mot;   /* v105 (Tom) : la porte des Réglages se renomme « Ma Parole ! » — le chemin délibéré vers l'offre */
  }
  var _sp = window.setPremium;
  if(typeof _sp === 'function'){
    window.setPremium = function(){ var r = _sp.apply(this, arguments);
      try{ encartReglages(); }catch(_){ } try{ if(window._cerclePaye) window._cerclePaye(); }catch(_){ } passe(); return r; };
  }
  encartReglages();
})();
