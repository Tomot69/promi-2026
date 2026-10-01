
/* ⚑ LE PINCEAU · LA CIBLE DU CHOIX — un trait appartient à UNE parole (Q128).
   Trois porteurs, et un seul point de vérité pour tout le lot :
     · une fiche de Promi ou de Chiche  → `p.trait`
     · une Nuée                          → `TRAITS_NUEE[clé]`
     · un gardé de côté, repris à la page + → `p.trait` de CE brouillon
     · une création en cours à la page +  → `window._ppPinceau`, tant qu'aucune promesse
                                            n'existe pour le porter. */
(function(){
  var NUEE = {};
  window._pinceauNuee = function(cle){
    var n = cle && NUEE[cle];
    return (n && window._PINCEAU_TRACES && window._PINCEAU_TRACES[n]) ? n : 'Plein';
  };
  window._pinceauNueeEcrit = function(cle, v){ if(cle) NUEE[cle] = v; };

  /* ⚠ ON MÉMORISE LE BROUILLON REPRIS. `reprendreBrouillon` est l'endroit UNIQUE qui
     rouvre un gardé de côté dans la page + (il y pose déjà `_ppGarde`). On l'enveloppe —
     on ne l'écoute pas : un écouteur ne saurait pas DE QUEL brouillon il s'agit. */
  try{
    var _rb = window.reprendreBrouillon;
    if(_rb) window.reprendreBrouillon = function(p){
      try{ window._ppGardeP = p || null; }catch(_){}
      return _rb.apply(this, arguments);
    };
  }catch(_){}

  window._pinceauCible = function(){
    var dp = document.getElementById('detailPoster');
    if(dp && dp.classList.contains('show')){
      /* ⚠ `cur` ET `curNuee` NE SONT PAS SUR `window`. Ce sont des liaisons `let` de
         portée globale : visibles comme identifiants nus depuis n'importe quel script,
         absentes de l'objet global. `window.cur` rendait `null`, et le choix partait
         dans le repli global — c'est-à-dire dans le réglage unique que Q128 refuse.
         Mesuré : `window.cur` null, `cur` = {id:126, « faire les crêpes »}. */
      if(dp.classList.contains('dp-nuee') || dp.classList.contains('dp-mode-nuee')){
        var k = null; try{ k = curNuee; }catch(_){}
        if(k) return {lire:function(){return NUEE[k]||null;},
                      ecrire:function(v){NUEE[k]=v;}};
      }
      var p = null; try{ p = cur; }catch(_){}
      if(p) return {lire:function(){return p.trait||null;}, ecrire:function(v){p.trait=v;}};
    }
    var cs = document.getElementById('createSheet');
    if(cs && cs.classList.contains('show') && cs.classList.contains('pp-garde')){
      var g = null; try{ g = window._ppGardeP; }catch(_){}
      if(g) return {lire:function(){return g.trait||null;}, ecrire:function(v){g.trait=v;}};
    }
    return {lire:function(){ return window._ppPinceau||null; },
            ecrire:function(v){ window._ppPinceau = v; }};
  };

  /* le nom effectif, filtré : un trait inconnu retombe sur Plein, jamais sur du vide */
  window.promiPinceau = function(p){
    var n = (p && p.trait) || window._pinceauCible().lire();
    return (n && window._PINCEAU_TRACES && window._PINCEAU_TRACES[n]) ? n : 'Plein';
  };

  /* ── LA CARTE « LE TRAIT » D'UNE NUÉE — son rail est permanent (cotes absolues) ──
     On garnit la carte que `lot-NUEE-PEAUFINER` a bâtie : on ne la reconstruit pas. */
  function garnitNuee(){
    var c = document.getElementById('npTrait'); if(!c) return;
    var k = null; try{ k = curNuee; }catch(_){}    /* identifiant nu, pas `window` */
    var nom = window._pinceauNuee(k);
    var lab = c.querySelector('.np-lab');
    var teinte = 'currentColor';
    try{ if(lab) teinte = getComputedStyle(lab).color || teinte; }catch(_){}
    var META = window._PINCEAU_META || [];
    var sig = [k, nom, teinte].join('|');
    if(c.getAttribute('data-sig') === sig && c.querySelector('.pc-t')) return;    /* comparer avant d'agir (§8) — v99 : mais une carte refaite SANS son rail se regarnit */
    c.setAttribute('data-sig', sig);
    var v = c.querySelector('.np-val');
    var libre = META.some(function(m){ return m[0]===nom && m[1]; });
    if(v) v.textContent = nom + (libre ? '' : ' — 0,50 €');
    var r = c.querySelector('.pc-glisse');
    if(!r){ r = document.createElement('div'); r.className='pc-glisse';
            r.setAttribute('data-glisse','1');
            r.innerHTML = '<div class="pc-rail"></div>'; c.appendChild(r); }
    var bord = 'currentColor';
    try{ bord = getComputedStyle(c).borderTopColor || bord; }catch(_){}
    r.querySelector('.pc-rail').innerHTML = META.map(function(m){
      var n = m[0], lb = !!m[1], on = (n === nom), montre = lb || on;
      var fg = on ? teinte : bord;
      return '<button type="button" class="pc-t'+(on?' on':'')+'" data-t="'+n+'" data-nuee="1"'
           + ' style="border:2px '+(lb?'solid':'dashed')+' '+fg+';border-radius:22px;'
           + 'background:transparent">'
           + '<span class="pc-e" style="color:'+fg+';opacity:'+(montre?1:0)+'">'
           + (montre ? window._pinceauEchantillon(n, 60) : '') + '</span>'
           + '<span class="pc-n" style="color:'+fg+'">'+n+'</span></button>';
    }).join('');
  }
  window._pinceauNueeCarte = garnitNuee;

  document.addEventListener('click', function(ev){
    var b = ev.target && ev.target.closest && ev.target.closest('#npTrait .pc-t');
    if(!b) return;
    ev.preventDefault(); ev.stopPropagation();
    var k = null; try{ k = curNuee; }catch(_){}
    if(k) NUEE[k] = b.getAttribute('data-t');
    var c = document.getElementById('npTrait'); if(c) c.removeAttribute('data-sig');
    garnitNuee();
    try{ if(window._ficheTrait) window._ficheTrait(); }catch(_){}
    try{ if(navigator.vibrate) navigator.vibrate(8); }catch(_){}
  }, true);

  function tout(){ try{ garnitNuee(); }catch(_){} }
  [0,200,600,1300].forEach(function(d){ setTimeout(tout,d); });
  document.addEventListener('click', function(){ [100,320,700].forEach(function(d){setTimeout(tout,d);}); }, true);
})();
