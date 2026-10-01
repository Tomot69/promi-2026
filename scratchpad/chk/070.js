
/* ⚑ LE PINCEAU — LE TRAIT SE CHOISIT LÀ OÙ LA PAROLE SE FAIT.
   Décision Tom, 31 août 2026 (Q128), reprise le 2 septembre : « Ça n'a pas de sens de
   mettre le choix du pinceau dans le Studio. Il le faut dans la page + lors de la création,
   puis adaptable depuis chaque fiche de Nuée, gardé de côté ou Promi. » Un choix de Studio
   s'appliquerait à toutes les fiches d'un coup — c'est exactement ce que le produit refuse.

   ⚑ LES DOUZE TRACÉS VIENNENT DE LA PLANCHE, ILS NE SONT PAS REDESSINÉS.
   `PLANCHE-DOUZE-TRAITS.html` porte les douze matières, quatre libres et huit à 0,50 €,
   toutes effilées par le même facteur (1 − 0,72·t, soit 22 → 6,2 sur les 390). Vérifié
   numériquement avant d'y toucher : elles sont posées sur L'ONDE DU §2.1, base 560,
   amplitude 36, effilement mesuré 21,2 → 5,9 — l'ajustement tombe à 0,05 px près sur les
   111 points de la ligne moyenne de « Plein ». Ce ne sont donc pas des dessins libres :
   c'est la courbe du produit, avec une matière par-dessus.

   ⚑ ON REMAPPE LA LIGNE MOYENNE, JAMAIS LA BOÎTE. Reporter un tracé sur une autre onde
   par une simple mise à l'échelle verticale (y' = base + (y−560)·amp/36) grossirait aussi
   L'ÉPAISSEUR du trait : 22 px deviendraient 28 sur la page + (amp 46). Or l'épaisseur est
   une constante du §2.3, pas une fonction de l'amplitude. On soustrait donc l'onde de la
   planche et on rajoute celle de l'écran :
       Y(x) = y_planche(x) − onde(560, 36)(x) + onde(base, amp)(x)
   La matière garde son épaisseur et son grain ; seule la vague sous elle change.

   ⚑ CE LOT NE TOUCHE PAS AU GESTE (Q118). Sur la page +, `#planterZone canvas` est à
   `opacity:0` : le trait qu'on voit est peint par `trait()` sur `#csTrameCv`. C'est là
   qu'on branche la matière — le moteur du geste n'est pas modifié d'une ligne. */
(function(){
  var W = 390, BASE_P = 560, AMP_P = 36;

  function ondeP(x){ var t=Math.max(0,Math.min(1,x/W));
    return BASE_P - AMP_P*0.34*t - AMP_P*0.62*Math.sin(2*Math.PI*1.5*t); }

  /* ── LE CHOIX ────────────────────────────────────────────────────────────
     Il appartient à UNE parole. `_ppPinceau` porte celui de la page + en cours ;
     `p.trait` porte celui d'un Promi planté. Rien n'est global : c'est toute la
     décision de Q128. */
  function nomsLibres(){ return (window._PINCEAU_META||[]).filter(function(m){return m[1];})
                                .map(function(m){return m[0];}); }
  window.promiPinceau = function(p){
    var n = (p && p.trait) || window._ppPinceau || 'Plein';
    return (window._PINCEAU_TRACES && window._PINCEAU_TRACES[n]) ? n : 'Plein';
  };

  /* ── LA MATIÈRE, PEINTE ──────────────────────────────────────────────────
     On découpe à [x0, x1] : au repos c'est l'amorce, pendant le geste c'est la moitié
     donnée. La coupe est FRANCHE, et c'est juste — le chevron du §2.3 marque la
     frontière juste après, comme il le fait déjà pour le trait plein. */
  window._matiereTrait = function(g, nom, base, amp, x0, x1, col){
    var T = window._PINCEAU_TRACES && window._PINCEAU_TRACES[nom];
    if(!T || !T.length) return false;
    var O = window._onde; if(!O) return false;
    var yc = O.onde(base, amp);
    function Y(x, y){ return y - ondeP(x) + yc(x); }
    g.save();
    g.beginPath(); g.rect(x0, 0, x1-x0, 900); g.clip();
    g.fillStyle = col; g.strokeStyle = col;
    g.lineCap = 'round'; g.lineJoin = 'round';
    for(var i=0;i<T.length;i++){
      var p = T[i];
      if(p[0] === 0){                       /* un contour plein : M/L/Z */
        g.beginPath();
        for(var k=1;k<p.length;k+=2){
          var x=p[k], y=Y(x, p[k+1]);
          if(k===1) g.moveTo(x,y); else g.lineTo(x,y);
        }
        g.closePath(); g.fill();
      } else if(p[0] === 1){                /* une barre : x1 y1 x2 y2 épaisseur */
        g.lineWidth = p[5];
        g.beginPath(); g.moveTo(p[1], Y(p[1],p[2])); g.lineTo(p[3], Y(p[3],p[4])); g.stroke();
      } else if(p[0] === 2){                /* un grain, une perle, une goutte */
        g.beginPath(); g.arc(p[1], Y(p[1],p[2]), p[3], 0, 6.2832); g.fill();
      }
    }
    g.restore();
    return true;
  };

  /* ── L'ÉCHANTILLON D'UNE PASTILLE ────────────────────────────────────────
     Le même tracé, à l'échelle de la pastille. On ne redessine rien : on met la
     planche à l'échelle, en gardant sa propre onde (560 / 36). */
  function echantillon(nom, w, col){
    /* ⚑ `currentColor` PAR DÉFAUT, ET C'EST LA BONNE VALEUR. Appelé sans couleur — ce que
       font le Peaufiner d'une fiche et la carte d'une Nuée, qui la posent sur le porteur —
       les chemins sortaient en `fill="undefined"` et RIEN NE SE PEIGNAIT : le svg mesurait
       96 × 18,7 à l'écran, sa couleur calculée était juste, et la rangée paraissait vide.
       Avec `currentColor`, l'échantillon suit ce qui le porte : la teinte claire de la
       nature dans Peaufiner, l'encre ou la teinte sur une pastille. Six cas, une règle. */
    if(!col) col = 'currentColor';
    var T = window._PINCEAU_TRACES && window._PINCEAU_TRACES[nom]; if(!T) return '';
    var h = w*76/390, k = w/390, d = [], j;
    for(var i=0;i<T.length;i++){
      var p = T[i];
      if(p[0]===0){
        var s='M';
        for(j=1;j<p.length;j+=2) s += (j>1?'L':'') + (p[j]*k).toFixed(1) + ' ' + ((p[j+1]-518)*k).toFixed(1);
        d.push('<path d="'+s+'Z" fill="'+col+'"/>');
      } else if(p[0]===1){
        d.push('<line x1="'+(p[1]*k).toFixed(1)+'" y1="'+((p[2]-518)*k).toFixed(1)+
               '" x2="'+(p[3]*k).toFixed(1)+'" y2="'+((p[4]-518)*k).toFixed(1)+
               '" stroke="'+col+'" stroke-width="'+Math.max(0.4,p[5]*k).toFixed(2)+'" stroke-linecap="round"/>');
      } else {
        d.push('<circle cx="'+(p[1]*k).toFixed(1)+'" cy="'+((p[2]-518)*k).toFixed(1)+
               '" r="'+Math.max(0.3,p[3]*k).toFixed(2)+'" fill="'+col+'"/>');
      }
    }
    return '<svg width="'+w+'" height="'+h.toFixed(1)+'" viewBox="0 0 '+w+' '+h.toFixed(1)+
           '" fill="none" aria-hidden="true">'+d.join('')+'</svg>';
  }
  window._pinceauEchantillon = echantillon;

  /* ── LA RANGÉE, À LA PAGE + ──────────────────────────────────────────────
     Emplacement B, choisi par Tom le 2 septembre : la bande 637 → 760, relevée à
     l'écran, est libre. AUCUNE cote de la page + ne bouge — la phrase reste à 414,
     l'invite à 564, « garder de côté » à 708.
     Grammaire des contours (loi 2) : trait 2, couleur du corps, rayon = hauteur ÷ 2,
     donc 31 pour une pastille de 62. Le nom est à 12 px — le plancher d'une carte
     étroite (loi 3), jamais un facteur.
     ⚠ POSÉE EN LIGNE AVEC `important` : `#createSheet>*:not(#csTrameCv):not(.closeb)
     :not(.pd-drift)` impose `position:relative; z-index:1; max-width:84%` à tout enfant
     direct — deux id, il bat une règle de feuille à `!important` égal (CLAUDE.md §8).
     C'est la parade que `.closeb` emploie déjà. */
  /* ⚑ LA COTE SE CALCULE, ELLE NE SE MESURE PAS SUR ELLE-MÊME (CLAUDE.md §8).
     La bande libre va du bas de l'invite (637,5, relevé à l'écran) au haut de « garder de
     côté » (708, cote du moodboard) : 70,5 px. Une pastille de 62 la remplissait au pixel
     près — elle TOUCHAIT « garder de côté », zéro air. À 44, il reste 26,5 px, soit
     13,25 de chaque côté quand on centre : le plancher du §6, des deux bords.
     ⚠ 708 EST UNE CONSTANTE DU MOODBOARD, PAS UNE MESURE : « garder de côté » est masqué
     sur un Promi à soi rempli, et s'y fier aurait donné une rangée qui déborde dès qu'il
     revient. 44 / rayon 22 est par ailleurs une famille de la grammaire des contours —
     celle du sélecteur, 167 × 44 × 2 × 22. */
  var HAUT = 651, PH = 78, PHT = 44, ECART = 10;
  var INK_AIDE = 7, INK_MOT = 3, INK_LIEN = 0.5;   /* retraits d'encre, mesurés à l'image (voir bati) */

  function corpsEncre(){
    var clair = !!document.querySelector('#device.light,.device.light,.frame.light');
    return clair ? '#201908' : '#F7F0DE';
  }

  function bati(){
    var cs = document.getElementById('createSheet'); if(!cs) return null;
    var r = document.getElementById('csPinceau');
    if(!r){
      r = document.createElement('div'); r.id = 'csPinceau';
      r.setAttribute('data-glisse','1');   /* la rangée se DÉCLARE glissante — Q128 §3 */
      r.innerHTML = '<div class="pc-rail" id="csPinceauRail"></div>';
      cs.appendChild(r);
      /* ⚑ IL EST BÂTI : IL S'INSCRIT AU RANGEUR. Rien ne survit à `closeAll` — un nœud
         bâti par un écran se peint sur le suivant si personne ne le range (CLAUDE.md §8,
         `redteam_vide`). */
      try{ (window._rangeurs = window._rangeurs || []).push(function(){
             var n = document.getElementById('csPinceau');
             if(n) n.style.setProperty('display','none','important'); }); }catch(_){}
    }
    /* ⚑ À MI-CHEMIN, À L'ENCRE (Tom, 13 sept. 2026) : autant d'air entre le bas du texte au-dessus et la
       rangée qu'entre la rangée et ce qui la suit (« garder de côté » s'il est là, sinon la barre Peaufiner).
       Les retraits d'encre sont MESURÉS sur l'image rendue : l'aide (Bricolage 17,5 / 1,4) finit 7 au-dessus
       de sa boîte ; une pastille finit sur sa boîte. */
    var haut = HAUT;
    try{
      var cr = cs.getBoundingClientRect(), k = cr.width/390;
      var vu = function(x){ return x && x.offsetParent && getComputedStyle(x).display !== 'none'
                                 && getComputedStyle(x).visibility !== 'hidden'; };
      var bas = function(x){ return (x.getBoundingClientRect().bottom - cr.top)/k; };
      var hautDe = function(x){ return (x.getBoundingClientRect().top - cr.top)/k; };
      var dessus = 0;
      [].forEach.call(cs.querySelectorAll('#csPhrase .ph-txt > .ph-m, #csPhrase .ph-txt > .ph-b,'
                    + ' #nueePhrase .ph-txt > .ph-m, #nueePhrase .ph-txt > .ph-b'), function(x){
        if(vu(x)) dessus = Math.max(dessus, bas(x)); });
      [].forEach.call(cs.querySelectorAll('.ph-hint'), function(x){
        if(vu(x)) dessus = Math.max(dessus, bas(x) - INK_AIDE); });
      var gm = cs.querySelector('.pp-garde-mot');
      if(vu(gm)) dessus = Math.max(dessus, bas(gm) - INK_MOT);
      var dessous = 760;
      var gl = cs.querySelector('.pp-garder');
      if(vu(gl)) dessous = hautDe(gl) + INK_LIEN;
      if(k && dessus > 0) haut = Math.round((dessus + (dessous - dessus - PHT)/2)*4)/4;
    }catch(_){}
    var geo = haut + '|' + PHT;
    if(r.getAttribute('data-geo') === geo) return r;   /* on compare avant d'agir (§8) */
    r.setAttribute('data-geo', geo);
    ['position:absolute','left:0px','top:'+haut+'px','width:390px','height:'+PHT+'px',
     'max-width:none','margin:0','padding:0','overflow:hidden','z-index:6'
    ].forEach(function(d){ var i=d.indexOf(':');
      r.style.setProperty(d.slice(0,i), d.slice(i+1), 'important'); });
    return r;
  }

  function peint(){
    var cs = document.getElementById('createSheet');
    if(!cs) return;
    /* ⚠ SANS `.pp` (l'écran des trois choix n'en porte pas), la rangée se RANGE — un simple
       retour la laissait peinte par-dessus la carte « Une Nuée ». */
    if(!cs.classList.contains('pp')){
      var r0 = document.getElementById('csPinceau');
      if(r0 && r0.style.getPropertyValue('display') !== 'none') r0.style.setProperty('display','none','important');
      return;
    }
    /* ⚠ PAS SUR L'ÉCRAN DES TROIS CHOIX. `pp-choix` est nu par construction (§9 : on ne
       démasque pas ce qu'on n'a pas décidé) — et il n'y a pas encore de parole à signer.
       Pas non plus sous Peaufiner déplié, qui recouvre la bande. */
    /* ⚑ NI PENDANT QU'ON REMPLIT UN CRÉNEAU (Tom, 13 sept. 2026) : elle recouvrait ce qu'on saisit. `pp-ouvert`
       est la classe que le code pose (Promi, Chiche) ; la Nuée a sa propre zone, `#nueeChoix`, pleine quand
       un créneau est ouvert. Elle revient dès que le créneau se referme. */
    var nz = document.getElementById('nueeChoix');
    var saisie = cs.classList.contains('pp-ouvert')
              || (cs.classList.contains('pp-nuee') && !!nz && nz.children.length > 0);
    var nu = cs.classList.contains('pp-choix') || cs.classList.contains('pp-peauf') || saisie;
    var r = bati(); if(!r) return;
    if(nu){ r.style.setProperty('display','none','important'); return; }
    r.style.setProperty('display','block','important');

    var O = window._onde, e = window._ppEcran && window._ppEcran();
    var nat = (e && e.nat) || 'promi';
    var plein  = (O && O.NATCOL   && O.NATCOL[nat])   || '#82AEF8';
    var clair2 = (O && (O.NATTRAIT||O.NATCLAIR) && (O.NATTRAIT||O.NATCLAIR)[nat]) || '#022140';
    var encre  = corpsEncre();
    var choisi = window.promiPinceau(null);
    var META = window._PINCEAU_META || [];

    var sig = [nat, encre, choisi].join('|');
    if(r.getAttribute('data-sig') === sig) return;   /* on compare avant d'agir (§8) */
    r.setAttribute('data-sig', sig);

    var rail = r.querySelector('.pc-rail');
    rail.innerHTML = META.map(function(m){
      var nom = m[0], libre = !!m[1], on = (nom === choisi);
      var bd  = on ? plein : encre;
      var fg  = on ? clair2 : encre;
      /* le MOT d'une pastille prise est en crème, comme le verbe (« Je lance une Nuée ») : la teinte claire
         sortait pâle sur le mauve (13 sept. 2026). Le trait garde la teinte claire (§2.1 bis). */
      var mot = on ? '#F7F0DE' : encre;
      /* ⚑ CE QUI N'EST PAS À TOI EST EN POINTILLÉ, SANS MATIÈRE (Q128 §4) — le dessin que
         le produit emploie déjà pour un gardé de côté (Q83) : le champ est là, la matière
         n'y est pas. Aucun cadenas, aucun badge, aucune couleur d'alerte.
         ⚑ ON ESSAIE D'ABORD, ON PAIE ENSUITE (Q128 §5) : dès qu'on le touche, il montre
         sa matière, ici et sur le trait du haut. */
      var montre = libre || on;
      return '<button type="button" class="pc-t'+(on?' on':'')+'" data-t="'+nom+'"'
           + ' style="border:2px '+(libre?'solid':'dashed')+' '+bd+';border-radius:'+(PHT/2)+'px;'
           + 'background:'+(on?plein:'transparent')+'">'
           + '<span class="pc-e" style="color:'+fg+';opacity:'+(montre?1:0)+'">'
           + (montre ? echantillon(nom, PH-18, fg) : '') + '</span>'
           + '<span class="pc-n" style="color:'+mot+';-webkit-text-fill-color:'+mot+'">'+nom+'</span></button>';
    }).join('');
  }
  window._pinceauRangee = peint;

  /* ── LE DOIGT ────────────────────────────────────────────────────────────
     Un toucher choisit, et le trait du haut se refait aussitôt. */
  document.addEventListener('click', function(ev){
    var b = ev.target && ev.target.closest && ev.target.closest('#csPinceau .pc-t');
    if(!b) return;
    ev.preventDefault(); ev.stopPropagation();
    window._ppPinceau = b.getAttribute('data-t');
    var r = document.getElementById('csPinceau'); if(r) r.removeAttribute('data-sig');
    peint();
    try{ if(window._ppTout) window._ppTout(); }catch(_){}
    try{ if(navigator.vibrate) navigator.vibrate(8); }catch(_){}
  }, true);

  /* ── LE TRAIT PLANTÉ GARDE SON PINCEAU ───────────────────────────────────
     On ne touche pas aux trois fabriques (§9, et elles sont minifiées) : on marque les
     promesses NÉES depuis le clic. */
  ['addPromi','addNuee','addDraft'].forEach(function(id){
    var b = document.getElementById(id); if(!b) return;
    b.addEventListener('click', function(){
      var avant = {};
      /* ⚑ CHANTIER 69 (11 sept., nuit) : le jeu est un `let promises` — il n'est PAS sur `window`. `window.promises` valait
         undefined : aucun Promi n'était vu « avant », aucun n'était marqué « né » — et aucun ne gardait son pinceau. */
      var _liste = function(){ try{ return (typeof promises !== 'undefined' && promises) || window.promises || []; }catch(_){ return window.promises || []; } };
      try{ _liste().forEach(function(p){ avant[p.id]=1; }); }catch(_){}
      var t = window.promiPinceau(null);
      setTimeout(function(){
        try{ _liste().forEach(function(p){
               if(!avant[p.id] && !p.trait) p.trait = t; }); }catch(_){}
      }, 0);
    }, true);
  });

  /* ── ON REPASSE DERRIÈRE LE MOTEUR, ON N'ÉCOUTE PAS SEULEMENT (CLAUDE.md §8) ──
     `_ppTout` est le repeintre du produit ; `peint` refait la rangée. Les deux sont
     enveloppés autour du peintre du champ, sinon un rendu venu d'ailleurs les efface. */
  function tout(){ try{ peint(); }catch(_){ } }
  [0,120,400,900,1800].forEach(function(d){ setTimeout(tout, d); });
  document.addEventListener('click', function(){ [80,260,600].forEach(function(d){setTimeout(tout,d);}); }, true);
  try{ if(document.fonts && document.fonts.ready) document.fonts.ready.then(tout); }catch(_){}
  try{
    var cs = document.getElementById('createSheet');
    if(cs) new MutationObserver(function(){ tout(); })
             .observe(cs, {attributes:true, attributeFilter:['class','data-kind']});
    /* la zone de choix d'une Nuée se remplit et se vide sans toucher aux classes de la feuille */
    if(cs) new MutationObserver(function(ms){
             for(var i=0;i<ms.length;i++){ var t=ms[i].target;
               if(t && (t.id==='nueeChoix' || t.id==='nueePhrase')){ tout(); return; } } })
             .observe(cs, {childList:true, subtree:true});
  }catch(_){}

  /* ── « DÈS QU'ON A FINI » (13 sept. 2026) — un créneau ouvert doit pouvoir se refermer, sinon la rangée
     ne revient jamais. Un mot : Entrée referme, comme le nom d'une Nuée le faisait déjà. Une liste (à qui,
     avec qui) : toucher hors du panneau et hors de la phrase referme, comme un mot perd déjà son champ.
     Et un panneau ouvert ne survit pas à `closeAll` : il passait d'une page + à la suivante (une Nuée
     s'ouvrait « en saisie », après un Chiche laissé sur « avec qui »). ── */
  document.addEventListener('keydown', function(ev){
    if(ev.key === 'Enter' && ev.target && ev.target.id === 'phIn'){ ev.preventDefault(); ev.target.blur(); }
  }, true);
  document.addEventListener('click', function(ev){
    var cs = document.getElementById('createSheet');
    if(!cs || !cs.classList.contains('show') || !cs.classList.contains('pp')) return;
    var t = ev.target; if(!t || !t.closest) return;
    if(t.closest('#csChoix, #nueeChoix, .ph-m, .ph-b, .ph-o, .ph-addbar, input, textarea')) return;
    var z = document.getElementById('csChoix');
    if(z && z.classList.contains('ouvert') && !z.querySelector('#phIn')){
      z.classList.remove('ouvert'); try{ window._phraseRendu(); }catch(_){}
    }
    var nz = document.getElementById('nueeChoix');
    if(nz && nz.children.length && cs.classList.contains('pp-nuee') && !nz.querySelector('input')){
      try{ window._nueePhraseRendu(); }catch(_){ nz.innerHTML=''; }
    }
  }, false);
  try{ (window._rangeurs = window._rangeurs || []).push(function(){
    var z = document.getElementById('csChoix');
    if(z && z.classList.contains('ouvert')){ z.classList.remove('ouvert'); z.innerHTML = ''; }
    var nz = document.getElementById('nueeChoix'); if(nz && nz.children.length) nz.innerHTML = '';
  }); }catch(_){}
})();
