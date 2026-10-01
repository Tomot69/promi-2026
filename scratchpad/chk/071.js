
/* ⚑ LE PINCEAU · SA REPRISE DANS PEAUFINER — variante D (Tom, 2 septembre 2026).
   « La rangée de 64 garde le rythme de Peaufiner. E fait descendre le reste de 134 px pour
   un aperçu plus grand, mais dans Peaufiner on REPREND un choix déjà fait, on ne le
   découvre pas — le grand aperçu, c'est à la page +. »

   HAUT DE LISTE, SUR LES QUATRE NATURES. On insère juste après `.s2-tete`, avant « À QUI »
   d'un Promi ou d'un Chiche et avant « DESCRIPTION » d'une Nuée : un seul point de pose,
   et le gardé de côté est couvert par la même ligne.

   ⚠ ON N'APPELLE PAS LE BÂTISSEUR — IL EST DANS SA FERMETURE. On observe `.s2-liste`, et
   on COMPARE AVANT D'AGIR : un observateur dont la réaction modifie ce qu'il observe se
   réveille lui-même sans fin (CLAUDE.md §8, « l'app rame, les captures échouent »).

   ⚠ LA RANGÉE SUIT SES VOISINES, PAS LA LOI. La grammaire des contours (trait 2, rayon =
   h ÷ 2) a été posée aux Réglages — `#settingsScreen .s2-reg` est à 2 / 32 — mais PAS aux
   rangées de Peaufiner d'une fiche, restées à 3 / 22. Ma rangée prend la classe `.s2-reg`
   et hérite donc de 3 / 22, comme ses voisines : une rangée à 2 / 32 au milieu de six à
   3 / 22 jurerait. L'écart entre les deux écrans est signalé dans QUESTIONS.md ; le
   corriger est un lot à part, avec son avant/après. */
(function(){
  /* ⚠ UNE SEULE VÉRITÉ : `window._pinceauCible`, posée par `lot-PINCEAU-CIBLE`. Ce lot
     portait sa propre copie — deux tables pour un même trait, c'est un bug qui attend. */
  function courant(){ return window._pinceauCible ? window._pinceauCible() : null; }

  /* le nom du trait de la fiche ouverte — jamais un réglage global (Q128) */
  function nomCourant(){
    var c = courant(); var n = c && c.lire();
    return (n && window._PINCEAU_TRACES && window._PINCEAU_TRACES[n]) ? n : 'Plein';
  }
  window._pinceauFiche = nomCourant;

  function el(t,c){ var d=document.createElement(t); if(c) d.className=c; return d; }

  function bati(liste){
    var tete = liste.querySelector('.s2-tete'); if(!tete) return;
    var r = liste.querySelector('#dpTraitReg');
    if(!r){
      r = el('div','s2-reg'); r.id = 'dpTraitReg';
      r.appendChild(el('div','s2-lab')).textContent = 'LE TRAIT';
      r.appendChild(el('div','pc-ap'));
      r.appendChild(el('div','s2-val'));
      var ctl = el('div','s2-ctl');
      var gl  = el('div','pc-glisse'); gl.setAttribute('data-glisse','1');
      gl.appendChild(el('div','pc-rail'));
      ctl.appendChild(gl); r.appendChild(ctl);
      r.addEventListener('click', function(ev){
        if(ev.target.closest && ev.target.closest('.s2-ctl')) return;
        r.classList.toggle('s2-ouv'); ev.stopPropagation(); }, true);
    }
    /* haut de liste : juste après la tête, jamais ailleurs */
    if(tete.nextSibling !== r) liste.insertBefore(r, tete.nextSibling);
    garni(r);
  }

  function garni(r){
    var META = window._PINCEAU_META || [];
    var nom  = nomCourant();
    var lab  = r.querySelector('.s2-lab');
    /* ⚑ LA TEINTE SE RELÈVE À L'ÉCRAN, JAMAIS DANS UNE RÈGLE. Le libellé porte déjà la
       teinte claire de la nature — #C4A2F5, #F5AC9E, #C9A8F5 en sombre, la couleur pleine
       en clair — et six règles s'en disputent la valeur selon la nature et le thème. On
       lit celle qui a gagné, et l'aperçu la reprend : il est juste dans les six cas sans
       qu'on recopie une seule couleur. */
    var teinte = 'currentColor';
    try{ teinte = getComputedStyle(lab).color || teinte; }catch(_){}
    var libre = META.some(function(m){ return m[0]===nom && m[1]; });
    var sig = [nom, teinte].join('|');
    if(r.getAttribute('data-sig') === sig) return;   /* on compare avant d'agir (§8) */
    r.setAttribute('data-sig', sig);

    r.querySelector('.s2-val').textContent = nom + (libre ? '' : ' — 0,50 €');
    r.querySelector('.pc-ap').innerHTML =
      (window._pinceauEchantillon ? window._pinceauEchantillon(nom, 96) : '');
    try{ r.querySelector('.pc-ap svg').style.color = teinte; }catch(_){}

    var encre = 'currentColor';
    try{ encre = getComputedStyle(r).borderTopColor || encre; }catch(_){}
    r.querySelector('.pc-rail').innerHTML = META.map(function(m){
      var n = m[0], lb = !!m[1], on = (n === nom);
      var montre = lb || on;
      var fg = on ? teinte : encre;
      return '<button type="button" class="pc-t'+(on?' on':'')+'" data-t="'+n+'"'
           + ' style="border:2px '+(lb?'solid':'dashed')+' '+(on?teinte:encre)+';'
           + 'border-radius:22px;background:transparent">'
           + '<span class="pc-e" style="color:'+fg+';opacity:'+(montre?1:0)+'">'
           + (montre ? window._pinceauEchantillon(n, 60) : '') + '</span>'
           + '<span class="pc-n" style="color:'+fg+'">'+n+'</span></button>';
    }).join('');
  }

  /* ── le doigt, dans Peaufiner ── */
  document.addEventListener('click', function(ev){
    var b = ev.target && ev.target.closest && ev.target.closest('#dpTraitReg .pc-t');
    if(!b) return;
    ev.preventDefault(); ev.stopPropagation();
    var c = courant(); if(!c) return;
    c.ecrire(b.getAttribute('data-t'));
    var r = document.getElementById('dpTraitReg');
    if(r){ r.removeAttribute('data-sig'); garni(r); }
    /* le trait de la fiche se refait sous les yeux — c'est la règle « on essaie d'abord » */
    try{ if(window._ficheTrait) window._ficheTrait(); }catch(_){}
    try{ if(window.renderDetail) renderDetail(); }catch(_){}
    try{ if(navigator.vibrate) navigator.vibrate(8); }catch(_){}
  }, true);

  /* ── ON OBSERVE, EN COMPARANT AVANT D'AGIR ── */
  function passe(){
    try{
      var liste = document.querySelector('#detailPoster .dpd-corps .s2-liste');
      if(!liste || !liste.querySelector('.s2-tete')) return;
      /* ⚠ SUR UNE NUÉE, `.s2-liste` EST MASQUÉE. `lot-NUEE-PEAUFINER` bâtit ses propres
         cartes (`npTete`, `npDesc`…) dans `#dpdCorps` et met la liste de la section 2 en
         `display:none`. Y insérer une rangée la peint dans le vide — mesuré : la boîte
         sortait à 0 × 0 en (−20, −44). La Nuée a SA carte, `#npTrait`, garnie par
         `lot-PINCEAU-CIBLE`. */
      if(getComputedStyle(liste).display === 'none') return;
      bati(liste);
    }catch(_){}
  }
  window._pinceauPeaufiner = passe;
  [0,180,500,1100].forEach(function(d){ setTimeout(passe, d); });
  document.addEventListener('click', function(){ [90,280,650].forEach(function(d){setTimeout(passe,d);}); }, true);
  try{
    var dp = document.getElementById('detailPoster');
    if(dp) new MutationObserver(function(){
      /* ⚠ SANS CE GARDE, L'OBSERVATEUR SE RÉVEILLE LUI-MÊME : `bati` insère un nœud dans
         `.s2-liste`, ce qui est précisément ce qu'on observe. On ne repasse que si la
         rangée MANQUE ou si la liste a été refaite sans elle. */
      var l = dp.querySelector('.dpd-corps .s2-liste');
      if(!l || !l.querySelector('.s2-tete')) return;
      if(l.querySelector('#dpTraitReg')) return;
      passe();
    }).observe(dp, {childList:true, subtree:true});
  }catch(_){}
})();
