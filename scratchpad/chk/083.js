
/* ⚑ LE CHOIX DES PERSONNES — le moteur partagé (voir lot-GENS-css). Toucher une personne l'ajoute ; la croix la
   retire ; « + ajouter quelqu'un » ouvre le menu d'ajout (un prénom, les personnes connues filtrées dessous). */
(function(){
  var X = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2 L10 10 M10 2 L2 10" fill="none" stroke-width="2" stroke-linecap="round"/></svg>';
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function connus(){
    var out = [];
    try{ promises.slice().reverse().forEach(function(p){ [p.who, p.from, p.avec].forEach(function(w){
      String(w||'').split(/\s*[,·]\s*/).forEach(function(n){ n=n.trim();
        if(n && !/^(moi|le groupe|tout le monde)$/i.test(n) && out.indexOf(n)<0) out.push(n); }); }); }); }catch(_){}
    try{ (typeof peopleList==='function' ? peopleList() : []).forEach(function(v){
      String(v||'').split(/\s*[,·]\s*/).forEach(function(n){ n=n.trim();
        if(n && !/^(moi|le groupe|tout le monde)$/i.test(n) && out.indexOf(n)<0) out.push(n); }); }); }catch(_){}
    return out;
  }
  window._gensConnus = connus;
  window._gensListe = function(v){ return String(v||'').split(/\s*[,·]\s*/).map(function(n){ return n.trim(); })
    .filter(function(n){ return n && !/^(moi|le groupe|qui \?|personne)$/i.test(n); }); };
  /* cfg : nat, choisis() → [noms], ajoute(nom), retire(nom), tete ('Moi' | 'tout le monde' | null), teteOn(), teteChoisie(),
           rendu() (optionnel : si l'hôte est reconstruit ailleurs), max (nombre de connus montrés) */
  function rend(host, cfg){
    if(!host) return;
    host._gens = cfg;
    host.classList.add('gn','ph-opts');
    host.setAttribute('data-nat', cfg.nat || 'promi');
    var pris = cfg.choisis() || [];
    var noms = pris.slice();
    connus().forEach(function(n){ if(noms.indexOf(n)<0 && noms.length < pris.length + (cfg.max == null ? 6 : cfg.max)) noms.push(n); });
    var h = '';
    /* « tout le monde » n'est pas une personne : pas d'initiale (elle n'aurait rien dit, et coupait le mot) */
    if(cfg.tete) h += '<button type="button" class="ph-o'+(cfg.teteOn()?' on':'')+'" data-gn-tete="1">'
      + (/^moi$/i.test(cfg.tete) ? '<span class="ppo-ini">M</span>' : '') + '<span class="ppo-nom">'+esc(cfg.tete)+'</span></button>';
    /* ⚑ §5 (14 sept.) : dans une Nuée, « tout le monde » passe devant, « Moi » ensuite */
    if(cfg.tete2) h += '<button type="button" class="ph-o'+(cfg.tete2On()?' on':'')+'" data-gn-tete2="1"><span class="ppo-ini">M</span><span class="ppo-nom">'+esc(cfg.tete2)+'</span></button>';
    noms.forEach(function(n){
      var on = pris.indexOf(n) >= 0;
      h += '<button type="button" class="ph-o'+(on?' on':'')+'" data-v="'+esc(n)+'"><span class="ppo-ini">'+esc(n.charAt(0).toUpperCase())
        + '</span><span class="ppo-nom">'+esc(n)+'</span>'+(on?'<span class="ppo-x" role="button" aria-label="retirer '+esc(n)+'">'+X+'</span>':'')+'</button>';
    });
    h += '<button type="button" class="ph-o ph-add" data-add="1">+ ajouter quelqu’un</button>';
    host.innerHTML = h;
    function apres(){ if(cfg.rendu) cfg.rendu(); else rend(host, cfg); }
    host.querySelectorAll('.ph-o').forEach(function(b){
      b.onclick = function(ev){
        ev.stopPropagation(); if(ev.preventDefault) ev.preventDefault();
        if(b.hasAttribute('data-add')){ barre(host, cfg, b, apres); return; }
        if(b.hasAttribute('data-gn-tete')){ cfg.teteChoisie(); apres(); return; }
        if(b.hasAttribute('data-gn-tete2')){ cfg.tete2Choisie(); apres(); return; }
        var n = b.getAttribute('data-v');
        if(ev.target.closest && ev.target.closest('.ppo-x')){ cfg.retire(n); apres(); return; }
        if(b.classList.contains('on')) return;
        cfg.ajoute(n); apres();
      };
    });
    try{ if(window._gensBorne){ requestAnimationFrame(window._gensBorne);
      [120, 400, 900].forEach(function(t){ setTimeout(window._gensBorne, t); }); } }catch(_){}
    return host;
  }
  function barre(host, cfg, bouton, apres){
    var br = document.createElement('div'); br.className = 'gn-barre';
    br.innerHTML = '<input type="text" class="gn-in ph-addwho" placeholder="un prénom…" autocomplete="off" spellcheck="false"><div class="gn-sug"></div>';
    host.replaceChild(br, bouton);
    var inp = br.querySelector('input'), sug = br.querySelector('.gn-sug');
    ['click','pointerdown','mousedown'].forEach(function(t){ br.addEventListener(t, function(e){ e.stopPropagation(); }); });
    function valide(n){ n = (n||'').trim(); if(!n) return; if((cfg.choisis()||[]).indexOf(n) < 0) cfg.ajoute(n); apres(); }
    inp.oninput = function(){
      var q = inp.value.trim().toLowerCase(), pris = cfg.choisis() || [];
      var l = q ? connus().filter(function(n){ return n.toLowerCase().indexOf(q) >= 0 && pris.indexOf(n) < 0; }).slice(0,4) : [];
      sug.innerHTML = l.map(function(n){ return '<button type="button" class="ph-o" data-pick="'+esc(n)+'"><span class="ppo-ini">'
        + esc(n.charAt(0).toUpperCase())+'</span><span class="ppo-nom">'+esc(n)+'</span></button>'; }).join('');
      sug.querySelectorAll('[data-pick]').forEach(function(p){ p.onclick = function(e){ e.stopPropagation(); valide(p.getAttribute('data-pick')); }; });
      try{ if(host.scrollHeight > host.clientHeight) host.scrollTop = host.scrollHeight; }catch(_){}
    };
    inp.onkeydown = function(e){ if(e.key === 'Enter'){ e.preventDefault(); valide(inp.value); } };
    setTimeout(function(){ try{ inp.focus(); }catch(_){} }, 30);
    try{ if(window._gensBorne) requestAnimationFrame(window._gensBorne); }catch(_){}
  }
  window._gens = rend;
  try{ (window._rangeurs = window._rangeurs || []).push(function(){ window._npGensOuvert = false; }); }catch(_){}

  /* ── JAMAIS SOUS PEAUFINER : la liste défile au-dessus de la barre (760), 16 d'air ── */
  window._gensBorne = function(){
    try{
      var dv = document.getElementById('device'); if(!dv) return;
      var dr = dv.getBoundingClientRect(), k = dr.width/390;
      document.querySelectorAll('#createSheet .gn').forEach(function(g){
        var r = g.getBoundingClientRect(); if(!r.height && !g.style.maxHeight) return;
        var haut = (r.top - dr.top)/k;
        /* « + ajouter quelqu'un » RESTE VISIBLE : la liste défile au-dessus de la barre, et le bouton (ou le menu
           d'ajout) reste collé en bas de ce qui défile, sur la couleur du corps. */
        var fond = getComputedStyle(document.getElementById('createSheet')).backgroundColor;
        var br = g.querySelector(':scope > .gn-barre');
        if(br && !br._vu){ br._vu = 1; g.scrollTop = g.scrollHeight; }
        [].forEach.call(g.querySelectorAll(':scope > .ph-add'), function(a){
          if(a.style.getPropertyValue('background-color') !== fond){
            a.style.setProperty('position','sticky','important'); a.style.setProperty('bottom','0','important');
            a.style.setProperty('z-index','2','important'); a.style.setProperty('background-color', fond, 'important');
            a.style.setProperty('box-shadow','0 0 0 8px '+fond,'important'); } });
        /* la hauteur tombe sur des RANGÉES ENTIÈRES (52 + 8) au-dessus du bouton collé : aucune pastille coupée au repos */
        var rangs = Math.max(1, Math.floor((744 - haut - 66 + 8) / 60));
        var mh = Math.min(Math.floor(744 - haut), rangs * 60 + 62);
        var v = mh + 'px';
        if(g.style.getPropertyValue('max-height') !== v){
          g.style.setProperty('max-height', v, 'important');
          g.style.setProperty('overflow-y', 'auto', 'important');
          g.style.setProperty('overflow-x', 'hidden', 'important');
          g.style.setProperty('padding-bottom', '4px', 'important');
        }
      });
    }catch(_){}
  };
  try{ var _t = window._ppTout; if(_t && !_t._gn){ var w = function(){ var r = _t.apply(this, arguments);
      try{ requestAnimationFrame(window._gensBorne); }catch(_){} return r; }; w._gn = 1; window._ppTout = w; } }catch(_){}

  /* ⚠ UN PANNEAU QUI S'OUVRE REPOSE L'ÉCRAN (13 sept. 2026) : une liste (à qui, avec qui) ouvrait le choix sans repasser
     par `_ppTout` — le trait descendait au plancher du choix ouvert, mais le rond photo restait à sa cote d'avant et tombait
     sur les pointillés (Chiche : 166 au lieu de 126). Un mot, lui, repassait par le focus. */
  try{ var _pc = window._phraseChoix; if(_pc && !_pc._gn){ var wpc = function(){ var r = _pc.apply(this, arguments);
      try{ requestAnimationFrame(function(){ try{ if(window._ppTout) window._ppTout(); }catch(_){} }); }catch(_){} return r; };
    wpc._gn = 1; window._phraseChoix = wpc; } }catch(_){}
  try{ var _nc = window._nueeChoix; if(_nc && !_nc._gn){ var wnc = function(){ var r = _nc.apply(this, arguments);
      try{ requestAnimationFrame(function(){ try{ if(window._ppTout) window._ppTout(); }catch(_){} }); }catch(_){} return r; };
    wnc._gn = 1; window._nueeChoix = wnc; } }catch(_){}
  /* et quand elle se referme, l'écran revient au repos : le trait redescend, le rond photo avec lui */
  try{ var _npr = window._nueePhraseRendu; if(_npr && !_npr._gn){ var wnp = function(){ var r = _npr.apply(this, arguments);
      try{ requestAnimationFrame(function(){ try{ if(window._ppTout) window._ppTout(); }catch(_){} }); }catch(_){} return r; };
    wnp._gn = 1; window._nueePhraseRendu = wnp; } }catch(_){}

  /* ── LA PAGE + : « à qui », « qui tu défies », « avec qui » ── */
  window._gensPhrase = function(zone, cle){
    var P = window._phrase; if(!P || !zone) return;
    var host = zone.querySelector('.ph-opts'); if(!host){ host = document.createElement('div'); zone.appendChild(host); }
    var nat = (P.sens === 'chiche') ? 'chiche' : 'promi';
    var champ = (cle === 'avec') ? 'avec' : 'qui';
    function pose(l){
      if(champ === 'avec'){ P.avec = l.join(', '); return; }
      if(l.length){ P.qui = l.join(', '); }
      else { P.qui = (P.sens === 'faire' && !P.faireAutre) ? 'Moi' : ''; }
      try{ window.newWhoSel = l.slice(); }catch(_){}
      try{ var w = document.getElementById('fWho'); if(w){ w.value = l.join(', ') || (P.qui||''); w.dispatchEvent(new Event('input',{bubbles:true})); } }catch(_){}
    }
    var dansNuee = false; try{ dansNuee = !!document.querySelector('#createSheet.cs-nuee'); }catch(_){}
    rend(host, {
      nat: nat,
      choisis: function(){ return window._gensListe(P[champ]); },
      ajoute: function(n){ var l = window._gensListe(P[champ]); if(l.indexOf(n)<0) l.push(n); pose(l); },
      retire: function(n){ pose(window._gensListe(P[champ]).filter(function(x){ return x !== n; })); },
      tete: (champ === 'qui') ? 'Moi' : null,
      teteOn: function(){ return !window._gensListe(P.qui).length && /^moi$/i.test(String(P.qui||'')); },
      teteChoisie: function(){ P.qui = 'Moi'; try{ window.newWhoSel = []; }catch(_){}
        try{ var w = document.getElementById('fWho'); if(w){ w.value = 'Moi'; w.dispatchEvent(new Event('input',{bubbles:true})); } }catch(_){} },
      rendu: function(){
        try{ window._phraseRendu(); }catch(_){}
        var el = document.querySelector('#csPhrase [data-ph='+cle+']');
        try{ window._phraseChoix(cle, el); }catch(_){}
        try{ if(window._ppTout) window._ppTout(); }catch(_){}
      }
    });
    void dansNuee;
  };

  /* ── LA NUÉE, à la création : « avec qui » ── */
  window._gensNuee = function(zone){
    if(!zone) return;
    zone.innerHTML = '<div class="ph-lab">AVEC QUI</div><div class="ph-opts"></div>';
    var host = zone.querySelector('.ph-opts');
    var M = function(){ return (window.newNueeMembers = window.newNueeMembers || []); };
    rend(host, {
      nat: 'nuee',
      choisis: function(){ return M().slice(); },
      ajoute: function(n){ window._nueeMoiSeul = false; if(M().indexOf(n)<0) M().push(n); },
      retire: function(n){ var i = M().indexOf(n); if(i>=0) M().splice(i,1); },
      tete: 'tout le monde',
      teteOn: function(){ return !M().length && !window._nueeMoiSeul; },
      teteChoisie: function(){ window._nueeMoiSeul = false; window.newNueeMembers = []; },
      tete2: 'Moi',                                  /* « Avec toi seulement » : aucune autre personne */
      tete2On: function(){ return !M().length && !!window._nueeMoiSeul; },
      tete2Choisie: function(){ window._nueeMoiSeul = true; window.newNueeMembers = []; },
      rendu: function(){
        try{ if(window.buildNueeMembers) buildNueeMembers(); }catch(_){}
        try{ window._nueePhraseRendu(); }catch(_){}
        var m = document.querySelector('#nueePhrase .ph-m[data-np=avec]');
        try{ if(m) window._nueeChoix('avec', m); }catch(_){}
      }
    });
  };

  /* ── LA PAGE + : son Peaufiner (À QUI · À QUI JE LANCE · AVEC · MEMBRES) — le même choix, sur la parole en cours ── */
  window._gensPage = function(kind){
    var host = document.createElement('div');
    var P = window._phrase || {};
    var cfg;
    function lire(){
      if(kind === 'nuee') return (window.newNueeMembers || []).slice();
      return window._gensListe(kind === 'avec' ? P.avec : P.qui);
    }
    function ecrire(l){
      if(kind === 'nuee'){ window.newNueeMembers = l.slice(); try{ if(window.buildNueeMembers) buildNueeMembers(); }catch(_){} return; }
      if(kind === 'avec'){ P.avec = l.join(', '); return; }
      P.qui = l.length ? l.join(', ') : ((P.sens === 'faire' && !P.faireAutre) ? 'Moi' : '');
      try{ window.newWhoSel = l.slice(); }catch(_){}
      try{ var w = document.getElementById('fWho'); if(w){ w.value = l.join(', '); w.dispatchEvent(new Event('input',{bubbles:true})); } }catch(_){}
    }
    cfg = {
      nat: (kind === 'nuee') ? 'nuee' : (P.sens === 'chiche' ? 'chiche' : 'promi'),
      choisis: lire,
      ajoute: function(n){ var l = lire(); if(l.indexOf(n)<0) l.push(n); ecrire(l); },
      retire: function(n){ ecrire(lire().filter(function(x){ return x !== n; })); },
      tete: null,
      rendu: function(){
        var reg = host.closest && host.closest('.s2-reg');
        var lab = reg ? ((reg.querySelector('.s2-lab')||{}).textContent||'') : '';
        rend(host, cfg);
        try{ if(kind === 'nuee') window._nueePhraseRendu(); else window._phraseRendu(); }catch(_){}
        try{ if(window._ppTout) window._ppTout(); }catch(_){}
        try{ if(window._ppPeaufBati) window._ppPeaufBati(); }catch(_){}
        if(lab){ [0, 60, 200, 500].forEach(function(t){ setTimeout(function(){
          [].forEach.call(document.querySelectorAll('#createSheet .dpd-corps .s2-reg'), function(r){
            var L = r.querySelector('.s2-lab');
            if(L && L.textContent === lab && !r.classList.contains('s2-ouv')) r.classList.add('s2-ouv'); });
        }, t); }); }
      }
    };
    rend(host, cfg);
    ['click','pointerdown','mousedown'].forEach(function(t){ host.addEventListener(t, function(e){ e.stopPropagation(); }); });
    return host;
  };

  /* ── LA FICHE : Peaufiner, sur une parole déjà plantée ── */
  window._gensFiche = function(kind){
    var host = document.createElement('div');
    var dp = document.getElementById('detailPoster');
    function nat(){ return (dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee')) ? 'nuee'
      : (dp.classList.contains('dp-chiche') ? 'chiche' : 'promi'); }
    function p(){ return (typeof cur !== 'undefined') ? cur : null; }
    function lire(){
      if(kind === 'nuee'){ try{ return ((typeof NUEEMEM!=='undefined' && NUEEMEM[curNuee]) || []).slice(); }catch(_){ return []; } }
      var q = p(); return q ? window._gensListe(kind === 'avec' ? q.avec : q.who) : [];
    }
    function ecrire(l){
      if(kind === 'nuee'){ try{ NUEEMEM[curNuee] = l.slice(); }catch(_){} }
      else { var q = p(); if(!q) return;
        if(kind === 'avec') q.avec = l.join(', ');
        else q.who = l.length ? l.join(', ') : 'moi'; }
    }
    function val(l){
      if(kind === 'nuee') return l.slice(0,2).join(' · ') + (l.length>2 ? (' · +'+(l.length-2)) : '');
      if(kind === 'avec') return l.length ? l.join(', ') : 'personne';
      return l.length ? l.join(', ') : 'moi';
    }
    var cfg = {
      nat: nat(),
      choisis: lire,
      ajoute: function(n){ var l = lire(); if(l.indexOf(n)<0) l.push(n); ecrire(l); },
      retire: function(n){ ecrire(lire().filter(function(x){ return x !== n; })); },
      tete: null,
      rendu: function(){
        rend(host, cfg);
        var reg = host.closest && host.closest('.s2-reg');
        var lab = reg ? ((reg.querySelector('.s2-lab')||{}).textContent||'') : '';
        if(reg){ var v = reg.querySelector('.s2-val'); var l = lire(); if(v) v.textContent = val(l);
          if(kind === 'avec') reg.classList.toggle('s2-vide', !l.length); }
        try{ if(window.syncAll) syncAll(); }catch(_){}
        try{ if(kind === 'nuee'){ if(window._ficheNuee) _ficheNuee(); }
             else { if(typeof renderDetail === 'function') renderDetail(); else if(window._fichePose) _fichePose(); } }catch(_){}
        try{ if(window._ficheTout) _ficheTout(); }catch(_){}
        /* la fiche se repose et Peaufiner se rebâtit : la carte qu'on avait ouverte le reste */
        if(lab){ [0, 60, 200, 500].forEach(function(t){ setTimeout(function(){
          [].forEach.call(document.querySelectorAll('#dpdCorps .s2-reg'), function(r){
            var L = r.querySelector('.s2-lab');
            if(L && L.textContent === lab && !r.classList.contains('s2-ouv')) r.classList.add('s2-ouv'); });
        }, t); }); }
      }
    };
    rend(host, cfg);
    ['click','pointerdown','mousedown'].forEach(function(t){ host.addEventListener(t, function(e){ e.stopPropagation(); }); });
    return host;
  };
})();
