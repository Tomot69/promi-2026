# -*- coding: utf-8 -*-
import io
P = 'app.html'; S = io.open(P, encoding='utf-8').read()
def rep(old, new, n=1):
    global S
    assert S.count(old) == n, (S.count(old), old[:90])
    S = S.replace(old, new)

# 1 · la zone d'ajout : un nœud qui peut porter le « + » (un <button> ne peut pas porter un bouton)
rep("""    h += '<button type="button" class="ph-o ph-add" data-add="1">+ ajouter quelqu’un</button>';
    host.innerHTML = h;""",
"""    h += '<div class="ph-o ph-add" data-add="1" role="button" tabindex="0">+ ajouter quelqu’un</div>';
    host.innerHTML = h;""")
rep("""        if(b.hasAttribute('data-add')){ barre(host, cfg, b, apres); return; }""",
"""        if(b.hasAttribute('data-add')){ if(ev.target.closest && ev.target.closest('.gn-plus')){ saValide(); return; } saOuvre(host, cfg); return; }""")
rep("""    try{ if(window._gensBorne){ requestAnimationFrame(window._gensBorne);
      [120, 400, 900].forEach(function(t){ setTimeout(window._gensBorne, t); }); } }catch(_){}
    return host;
  }""",
"""    try{ if(SA.actif && cfg.cle && cfg.cle === SA.cle){ SA.cfg = cfg; SA.host = host; saDecor(host.querySelector(':scope > .ph-add')); } }catch(_){}
    try{ if(window._gensBorne){ requestAnimationFrame(window._gensBorne);
      [120, 400, 900].forEach(function(t){ setTimeout(window._gensBorne, t); }); } }catch(_){}
    return host;
  }""")

# 2 · le menu d'ajout d'avant (un second encart, plein, avec ses suggestions) est REMPLACÉ
i = S.index("  function barre(host, cfg, bouton, apres){"); j = S.index("  window._gens = rend;", i)
NEUF = r"""  /* ⚑ v146 (C-122, Tom, 14 oct. 2026) — AJOUTER UNE PERSONNE : ON ÉCRIT DANS LA ZONE EN POINTILLÉS, ET NULLE PART AILLEURS.
     « Supprime l'encart supplémentaire. Toucher la zone en pointillés ouvre le clavier dans cette zone même. Validation : un « + »,
     à droite du nom, sur la même ligne, sans encart, orange #FB4C0D, gras, à la hauteur des majuscules ; il paraît dès le premier
     caractère. La touche Retour valide aussi. Le nom validé est posé ; une nouvelle ligne en pointillés se propose pour le suivant.
     Rien ne passe sous le clavier. »
     *Ce qui bloquait* : le toucher REMPLAÇAIT la zone par un second encart plein (`.gn-barre`) ; son champ prenait le clavier avec
     `preventScroll`, et rien dans l'app ne lisait la hauteur du clavier : sur l'iPhone la ligne restait dessous.
     *La manière* (celle du titre d'une parole et du nom d'un Cercle) : UNE entrée invisible, posée dans l'appareil, garde le clavier ;
     elle survit aux reconstructions de la liste (la fiche rebâtit son Peaufiner à chaque ajout). La zone en pointillés montre ce
     qu'on écrit, le curseur dessiné, puis le « + ». */
  var SA = { actif:false, cle:null, cfg:null, host:null, inp:null, plusVu:false, dec:0 };
  var PLUS = '<svg viewBox="0 0 10 10" aria-hidden="true"><path class="h" d="M0 5 H10"/><path class="v" d="M5 0 V10"/></svg>';
  function saChamp(){
    if(SA.inp && SA.inp.isConnected) return SA.inp;
    var dv = document.getElementById('device'); if(!dv) return null;
    var i = document.createElement('input'); i.type = 'text'; i.id = 'gnSaisie'; i.className = 'gn-saisie';
    [['autocomplete','off'],['autocorrect','off'],['autocapitalize','words'],['spellcheck','false'],['enterkeyhint','done'],
     ['maxlength','24'],['aria-label','Prénom']].forEach(function(a){ i.setAttribute(a[0], a[1]); });
    dv.appendChild(i);
    i.addEventListener('input', function(){ saPeint(); });
    i.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){ e.preventDefault(); saValide(); }
      else if(e.key === 'Escape'){ i.value = ''; saFerme(); } });
    i.addEventListener('focus', function(){ saPeint(); saSuis(); });
    /* le clavier se retire sur une zone VIDE : elle reprend son mot ; sur un nom écrit, il reste, avec son « + » */
    i.addEventListener('blur', function(){ setTimeout(function(){
      if(!SA.actif || document.activeElement === i) return;
      if(!i.value.trim()) saFerme(); else saPeint(); }, 0); });
    SA.inp = i; return i;
  }
  function saZones(){
    var l = [];
    [].forEach.call(document.querySelectorAll('.gn'), function(g){ if(g._gens && g._gens.cle && g._gens.cle === SA.cle){
      var z = g.querySelector(':scope > .ph-add'); if(z) l.push(z); } });
    if(SA.host && SA.host._gens && SA.host._gens.cle === SA.cle){ var z0 = SA.host.querySelector(':scope > .ph-add'); if(z0 && l.indexOf(z0) < 0) l.push(z0); }
    return l;
  }
  function saZoneVue(){ var l = saZones(); for(var q = 0; q < l.length; q++){ var r = l[q].getBoundingClientRect(); if(r.width > 4 && r.height > 4) return l[q]; } return null; }
  /* la hauteur des capitales et l'épaisseur du fût, LUES sur la police du nom : le « + » a la taille et la graisse de ce qu'on écrit */
  function saMetrique(el){
    var cs = getComputedStyle(el), f = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
    if(saMetrique._f === f && saMetrique._m) return saMetrique._m;
    var fs = parseFloat(cs.fontSize) || 16, cap = fs * 0.78, fut = fs * 0.2;
    try{ var c = saMetrique._c || (saMetrique._c = document.createElement('canvas').getContext('2d')); c.font = f;
      var H = c.measureText('H'), L = c.measureText('l');
      var a = Math.max(H.actualBoundingBoxAscent || 0, L.actualBoundingBoxAscent || 0); if(a > 4) cap = a;
      var w = (L.actualBoundingBoxLeft || 0) + (L.actualBoundingBoxRight || 0); if(w > 1 && w < cap * 0.5) fut = w;
    }catch(_){}
    saMetrique._f = f; return (saMetrique._m = { cap: cap, fut: fut });
  }
  /* le « + » se TRACE : la barre couchée de gauche à droite, puis la barre debout de haut en bas (deux traits nets, sans fondu) */
  function saPlus(PL, T, anime){
    var m = saMetrique(T), sv = PL.querySelector('svg'); if(!sv) return;
    sv.setAttribute('width', m.cap.toFixed(2)); sv.setAttribute('height', m.cap.toFixed(2));
    var ep = Math.max(1.6, Math.min(3.4, m.fut / m.cap * 10));
    var h = sv.querySelector('.h'), v = sv.querySelector('.v');
    [h, v].forEach(function(p){ p.setAttribute('stroke-width', ep.toFixed(2)); p.setAttribute('stroke-dasharray', '10'); p.setAttribute('stroke-dashoffset', '0'); });
    var calme = false; try{ calme = window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(_){}
    if(!anime || calme) return;
    h.setAttribute('stroke-dashoffset', '10'); v.setAttribute('stroke-dashoffset', '10');
    var t0 = performance.now(), D = 120;
    (function pas(){ var t = performance.now() - t0;
      var a = Math.min(1, t / D), b = Math.min(1, Math.max(0, (t - D * 0.7) / D));
      h.setAttribute('stroke-dashoffset', (10 * (1 - a)).toFixed(2)); v.setAttribute('stroke-dashoffset', (10 * (1 - b)).toFixed(2));
      if(b < 1 && PL.isConnected) requestAnimationFrame(pas); })();
  }
  function saDecor(z){
    if(!z || !SA.inp) return;
    var i = SA.inp, v = i.value, nom = v.replace(/\s+/g, ' ').trim();
    if(!z.classList.contains('gn-edit') || !z.querySelector('.gn-ligne')){
      z.classList.add('gn-edit'); z.setAttribute('role', 'group'); z.setAttribute('aria-label', 'Ajouter quelqu’un');
      z.innerHTML = '<span class="gn-ligne"><span class="gn-txt"></span><i class="ph-caret" aria-hidden="true"></i>'
        + '<span class="gn-ph">un prénom…</span><span class="gn-plus" role="button" tabindex="0" style="display:none">' + PLUS + '</span></span>';
    }
    var T = z.querySelector('.gn-txt'), PH = z.querySelector('.gn-ph'), PL = z.querySelector('.gn-plus');
    if(T.textContent !== v) T.textContent = v;
    var phd = v ? 'none' : ''; if(PH.style.display !== phd) PH.style.display = phd;
    z.classList.toggle('gn-repos', document.activeElement !== i);
    if(nom){ PL.setAttribute('aria-label', 'Ajouter ' + nom);
      if(PL.style.display === 'none'){ PL.style.display = ''; saPlus(PL, T, !SA.plusVu); } }
    else if(PL.style.display !== 'none'){ PL.style.display = 'none'; }
  }
  function saPeint(){
    if(!SA.actif || !SA.inp) return;
    saZones().forEach(saDecor);
    SA.plusVu = !!SA.inp.value.trim();
    saSuis();
  }
  function saRepos(z){ if(!z) return; z.classList.remove('gn-edit', 'gn-repos'); z.setAttribute('role', 'button'); z.removeAttribute('aria-label'); z.textContent = '+ ajouter quelqu’un'; }
  function saFerme(){
    if(!SA.actif) return; var l = saZones();
    SA.actif = false; SA.plusVu = false;
    l.forEach(saRepos); [].forEach.call(document.querySelectorAll('.gn > .ph-add.gn-edit'), saRepos);
    try{ if(SA.inp){ SA.inp.value = ''; if(document.activeElement === SA.inp) SA.inp.blur(); } }catch(_){}
    saClavier(0);
  }
  function saOuvre(host, cfg){
    var i = saChamp(); if(!i) return;
    var cle = cfg.cle || 'x';
    if(!(SA.actif && SA.cle === cle)){ if(SA.actif) saFerme(); i.value = ''; SA.plusVu = false; }
    SA.actif = true; SA.cle = cle; SA.cfg = cfg; SA.host = host;
    saPose();
    /* le focus DANS le geste : iOS n'ouvre le clavier qu'ainsi (v115) */
    try{ i.focus({preventScroll:true}); }catch(_){ try{ i.focus(); }catch(__){} }
    saPeint();
    [0, 160, 360, 620].forEach(function(t){ setTimeout(saSuis, t); });
  }
  function saValide(){
    var i = SA.inp; if(!SA.actif || !i) return;
    var n = i.value.replace(/\s+/g, ' ').trim(); if(!n) return;
    var cfg = SA.cfg; if(!cfg) return;
    /* un nom déjà connu garde SON écriture (« rachel » → « Rachel ») */
    try{ var c = connus(), b = n.toLowerCase(); for(var q = 0; q < c.length; q++){ if(c[q].toLowerCase() === b){ n = c[q]; break; } } }catch(_){}
    i.value = ''; SA.plusVu = false;
    try{ if((cfg.choisis() || []).indexOf(n) < 0) cfg.ajoute(n); }catch(_){}
    try{ if(cfg.rendu) cfg.rendu(); else rend(SA.host, cfg); }catch(_){}
    /* le nom est posé ; la ligne en pointillés se propose pour le suivant, le clavier reste (on est encore dans le geste) */
    try{ i.focus({preventScroll:true}); }catch(_){ try{ i.focus(); }catch(__){} }
    saPeint();
    [60, 220, 520, 760].forEach(function(t){ setTimeout(function(){ if(SA.actif){ saPeint(); } }, t); });
  }
  /* l'entrée invisible se tient SUR la zone : si le navigateur cherche le curseur, il le trouve là */
  function saPose(){
    try{ var z = saZoneVue(), i = SA.inp, dv = document.getElementById('device'); if(!z || !i || !dv) return;
      var d = dv.getBoundingClientRect(), k = d.width / 390 || 1, r = z.getBoundingClientRect();
      i.style.left = Math.round((r.left - d.left) / k + r.width / k / 2) + 'px';
      i.style.top = Math.round((r.top - d.top) / k + SA.dec + r.height / k / 2 - 10) + 'px'; }catch(_){}
  }
  /* ── LE CLAVIER : rien ne passe dessous. Le haut du clavier se LIT (visualViewport) ; ce qui défile défile, le reste monte. ── */
  function saClavierHaut(){
    var vv = window.visualViewport; if(!vv) return null;
    if((window.innerHeight - vv.height) < 100) return null;
    return vv.offsetTop + vv.height;
  }
  function saClavier(px){
    var dv = document.getElementById('device'); if(!dv) return;
    px = Math.max(0, Math.round(px)); if(px === SA.dec) return; SA.dec = px;
    if(px) dv.style.setProperty('translate', '0 ' + (-px) + 'px'); else dv.style.removeProperty('translate');
  }
  function saSuis(){
    try{
      var h = saClavierHaut(), z = SA.actif ? saZoneVue() : null;
      if(h == null || !z || document.activeElement !== SA.inp){ saClavier(0); saPose(); return; }
      var dv = document.getElementById('device'), k = dv.getBoundingClientRect().width / 390 || 1;
      var besoin = z.getBoundingClientRect().bottom + SA.dec * k + 14 * k - h;      /* 14 pt d'air au-dessus du clavier */
      if(besoin > 0.5){
        var sc = z.parentElement;
        while(sc && sc !== dv){ var cs = getComputedStyle(sc);
          if(/(auto|scroll)/.test(cs.overflowY) && sc.scrollHeight > sc.clientHeight + 2 && !sc.classList.contains('gn-liste')) break;
          sc = sc.parentElement; }
        if(sc && sc !== dv){ var av = sc.scrollTop; sc.scrollTop = av + besoin / k; besoin -= (sc.scrollTop - av) * k; }
      }
      saClavier(besoin > 0.5 ? besoin / k : 0); saPose();
    }catch(_){}
  }
  try{ if(window.visualViewport){ window.visualViewport.addEventListener('resize', saSuis); window.visualViewport.addEventListener('scroll', saSuis); } }catch(_){}
  window._gensSaisie = { etat: function(){ return { actif: SA.actif, cle: SA.cle, valeur: SA.inp ? SA.inp.value : '', decale: SA.dec, clavier: saClavierHaut() }; },
    ferme: saFerme, suis: saSuis };
"""
S = S[:i] + NEUF + S[j:]
rep("""  try{ (window._rangeurs = window._rangeurs || []).push(function(){ window._npGensOuvert = false; }); }catch(_){}

  /* ── JAMAIS SOUS PEAUFINER""",
"""  try{ (window._rangeurs = window._rangeurs || []).push(function(){ window._npGensOuvert = false; try{ saFerme(); }catch(_){} }); }catch(_){}

  /* ── JAMAIS SOUS PEAUFINER""")

# 3 · chaque liste se nomme : la saisie retrouve SA liste après une reconstruction
rep("""      nat: nat,
      choisis: function(){ return window._gensListe(P[champ]); },""",
"""      nat: nat, cle: 'ph-' + champ,
      choisis: function(){ return window._gensListe(P[champ]); },""")
rep("""      nat: 'nuee',
      choisis: function(){ return M().slice(); },""",
"""      nat: 'nuee', cle: 'nuee-neuve',
      choisis: function(){ return M().slice(); },""")
rep("""      nat: (kind === 'nuee') ? 'nuee' : (P.sens === 'chiche' ? 'chiche' : 'promi'),
      choisis: lire,""",
"""      nat: (kind === 'nuee') ? 'nuee' : (P.sens === 'chiche' ? 'chiche' : 'promi'), cle: 'pg-' + kind,
      choisis: lire,""")
rep("""      nat: nat(),
      choisis: lire,""",
"""      nat: nat(), cle: 'fi-' + kind,
      choisis: lire,""")

# 4 · l'ancien poseur de la page + réécrivait le mot de la zone : il laisse la zone qu'on écrit
rep("""          if(b.textContent.trim() !== '+ ajouter quelqu’un') b.textContent = '+ ajouter quelqu’un';""",
"""          if(!b.classList.contains('gn-edit') && b.textContent.trim() !== '+ ajouter quelqu’un') b.textContent = '+ ajouter quelqu’un';""")

# 5 · le dessin
CSS = r"""<style id="lot-V146-AJOUT-css">
/* ⚑ v146 (C-122, Tom) — AJOUTER UNE PERSONNE : on écrit DANS la zone en pointillés. Aucun second encart : la zone garde sa place,
   sa taille (342 × 52 sur la page +), son pointillé. Le nom à l'encre du mode, le mot d'attente dans la teinte de la zone, puis le
   « + » : l'orange du point de départ d'une action (`--c-orange-depart`), tracé, à la hauteur des capitales du nom. */
#device .gn-saisie{position:absolute!important;width:2px!important;height:20px!important;opacity:0!important;border:0!important;padding:0!important;
  margin:0!important;background:transparent!important;outline:0!important;box-shadow:none!important;pointer-events:none!important;
  font-size:16px!important;line-height:20px!important;z-index:1!important;caret-color:transparent!important;color:transparent!important;-webkit-text-fill-color:transparent!important}
#device .gn .ph-o.ph-add.gn-edit{cursor:text!important;gap:0!important;padding:0 16px!important;justify-content:center!important}
#device .gn .ph-add.gn-edit .gn-ligne{display:inline-block!important;white-space:pre!important;line-height:1!important;max-width:100%!important}
#device .gn .ph-add.gn-edit .gn-txt,#device .gn .ph-add.gn-edit .ph-caret{color:var(--c-creme95)!important;-webkit-text-fill-color:var(--c-creme95)!important}
#device.device.light .gn .ph-add.gn-edit .gn-txt,#device.device.light .gn .ph-add.gn-edit .ph-caret{color:var(--c-brun09)!important;-webkit-text-fill-color:var(--c-brun09)!important}
#device .gn .ph-add.gn-edit.gn-repos .ph-caret{display:none!important}
#device .gn .ph-add.gn-edit .gn-plus{display:inline-block;position:relative!important;margin:0 0 0 .62em!important;padding:0!important;line-height:0!important;
  vertical-align:baseline!important;cursor:pointer!important;color:var(--c-orange-depart)!important;border:0!important;background:transparent!important}
#device .gn .ph-add.gn-edit .gn-plus::before{content:""!important;position:absolute!important;left:-14px!important;right:-18px!important;top:-20px!important;bottom:-20px!important}
#device .gn .ph-add.gn-edit .gn-plus svg{display:block!important;overflow:visible!important}
#device .gn .ph-add.gn-edit .gn-plus svg path{stroke:var(--c-orange-depart)!important;fill:none!important;stroke-linecap:butt!important}
</style>
"""
rep("""<style id="lot-CURSEUR-css">""", CSS + """<style id="lot-CURSEUR-css">""")
io.open(P, 'w', encoding='utf-8').write(S)
print('ok')
