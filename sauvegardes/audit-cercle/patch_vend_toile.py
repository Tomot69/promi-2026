# L'ÉCRAN QUI VEND — REFAIT (Tom, 12 sept. 2026, second arbitrage).
# « La sphère en sort — elle est l'emblème de Promi, pas la preuve du Cercle. À sa place, une vraie Toile. »
# Le principe qui gouverne tout : UNE SEULE RUPTURE — la matière du pavage, et c'est elle qui vend.
# Appliqué sur la COPIE. app.html n'est pas touchée.
import hashlib, io, os
F = 'scratchpad/app-vend-toile.html'
S = io.open(F, encoding='utf-8').read()
avant = hashlib.md5(S.encode('utf-8')).hexdigest()
assert avant == '3ac4975ccaed06419950963a8804a212', 'copie inattendue : ' + avant
def r(old, new, quoi):
    global S
    assert S.count(old) == 1, 'motif absent ou multiple (%s) : %r' % (quoi, old[:80])
    S = S.replace(old, new); print('  ✔', quoi)

# ── 1 · LE PRIX, PARTOUT. 39 € l'année, 5,99 € le mois (Tom, 12 sept.). Plus de pourcentage.
r("Tout Promi pour <b>3,99&nbsp;€/mois</b>, arrête quand tu veux. Ou prends l'année : <b>29&nbsp;€</b> · soit 2,42&nbsp;€/mois · −39&nbsp;%.",
  "Tout Promi pour <b>5,99&nbsp;€/mois</b>, arrête quand tu veux. Ou prends l'année : <b>39&nbsp;€</b> · soit 3,25&nbsp;€/mois.",
  'prix · .pl-sub')
r('<button class="pl-buy prim" id="buyMonth">Essayer 14 jours, puis 3,99&nbsp;€/mois</button>',
  '<button class="pl-buy prim" id="buyMonth">Essayer 14 jours</button>', 'prix · #buyMonth')
r('<button class="pl-buy sec" id="buyYear">Prendre l\'année</button>',
  '<button class="pl-buy sec" id="buyYear">ou prendre l\'année — 39&nbsp;€</button>', 'prix · #buyYear')
r("px.textContent = '29\\u00a0€'", "px.textContent = '39\\u00a0€'", 'prix · ancien lot (cohérence)')
r("so.textContent = 'soit 2,42\\u00a0€/mois · −39\\u00a0%'", "so.textContent = 'soit 3,25\\u00a0€/mois'", 'prix · ancien lot (cohérence)')

# ── 2 · LA VITESSE — un tour en 100 s (Tom, 12 sept., validé). La sphère reste sur l'Aura.
r("var G = { AUTO:6.283185307/120,",
  "var G = { AUTO:6.283185307/100, /* ⚑ UN TOUR EN 100 s (Tom, 12 sept. 2026). Bornes : 84 s jugé TROP VIF (5 sept.),\n"
  "   120 s TOUJOURS TROP LENT (12 sept.) — 100 s entre les deux, +20 %. Décision, pas réglage : juge releve-aura.py, AUTO_DECIDE. */",
  'G.AUTO : un tour en 100 s')

BLOC = r"""
<style id="lot-CERCLE-TOILE-css">
/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
   ⚑ L'ÉCRAN QUI VEND — UNE VRAIE TOILE (Tom, 12 sept. 2026). « La sphère en sort : elle est l'emblème de Promi,
   pas la preuve du Cercle. À sa place une vraie Toile — douze à quatorze dalles, dont trois en matière Cercle.
   Rien n'est flouté, rien n'est verrouillé : ces trois-là sont simplement autres. »
   UNE SEULE RUPTURE sur l'écran : la matière du pavage. L'écran d'avant en avait trois (la matière de la sphère,
   l'échelle du 29 €, le noir du bouton) — trois anomalies s'annulent.
   ⚠ LE CADRE EST EN PAYSAGE (346×276, ratio 1,254), LA VRAIE TOILE EN PORTRAIT (390×571, ratio 0,683) : le cadre
   est donc une FENÊTRE sur la Toile, recadrée sur sa bande la plus dense (mesurée, jamais à l'œil). Les cellules,
   les places et les matières sont celles du moteur — rien n'est reconstruit (§4 règle 1, §9).
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════ */
/* ce qui ne se montre plus : le visuel, le titre, la phrase, les cinq lignes, les notes, la pilule du plateau,
   et le cadre du lot précédent (un seul propriétaire à la fois). */
#plusScreen>#plHeroCv,#plusScreen>.pl-h,#plusScreen>.pl-sub,#plusScreen>.pl-feat,#plusScreen>.pl-plans,
#plusScreen>.pl-note,#plusScreen>.pl-eb,#plusScreen>.enh,#plusScreen #plCadre{display:none!important}
#plusScreen::before,.frame #plusScreen::before{display:none!important;content:none!important}
#plusScreen #pcCadre{position:absolute!important;width:390px!important;height:844px!important;margin:0!important;
  pointer-events:none;z-index:3;background:#F4EEE1}
#plusScreen #pcCadre>*{position:absolute!important;margin:0!important;box-sizing:border-box!important}
/* ✕ FERMER — glyphe seul, plus de pilule, plus de titre en haut */
#plusScreen #pcCadre .pc-x{left:348px!important;top:58px!important;width:20px!important;height:20px!important;
  opacity:.45!important;pointer-events:auto!important;cursor:pointer}
#plusScreen>.closeb{display:none!important}
/* LA TOILE — le cadre */
#plusScreen #pcCadre .pc-toile{left:22px!important;top:90px!important;width:346px!important;height:276px!important;
  border-radius:28px!important;background:#EFE3D5!important;overflow:hidden!important}
#plusScreen #pcCadre .pc-toile canvas{position:absolute;left:0;top:0;width:346px;height:276px;display:block}
/* LE TITRE, LE SOUS-TITRE */
#plusScreen #pcCadre .pc-h{left:49.5px!important;top:398px!important;width:291px!important;
  font-family:Fraunces,Georgia,serif;font-weight:600;font-size:32px;line-height:38px;color:#1A1613;-webkit-text-fill-color:#1A1613}
#plusScreen #pcCadre .pc-sub{left:49.5px!important;top:436px!important;width:291px!important;
  font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:15px;line-height:22px;color:#8A7E70;-webkit-text-fill-color:#8A7E70;white-space:nowrap}
/* LES TROIS ARGUMENTS */
#plusScreen #pcCadre .pc-arg{left:49.5px!important;width:291px!important}
#plusScreen #pcCadre .pc-arg b{display:block;font-family:ApfelMid,system-ui,sans-serif;font-weight:500;font-size:17px;
  line-height:22px;color:#1A1613;-webkit-text-fill-color:#1A1613}
#plusScreen #pcCadre .pc-arg i{display:block;font-style:normal;font-family:Apfel,system-ui,sans-serif;font-weight:400;
  font-size:13px;line-height:18px;color:#8A7E70;-webkit-text-fill-color:#8A7E70}
/* LE PRIX — « 39 € » à gauche, « soit 3,25 €/mois » à droite, MÊME LIGNE DE BASE */
#plusScreen #pcCadre .pc-prix{left:49.5px!important;top:652px!important;width:291px!important;
  display:flex!important;align-items:baseline!important;justify-content:space-between!important}
#plusScreen #pcCadre .pc-prix b{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:40px;line-height:40px;
  color:#1A1613;-webkit-text-fill-color:#1A1613}
#plusScreen #pcCadre .pc-prix i{font-style:normal;font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:13px;
  color:#8A7E70;-webkit-text-fill-color:#8A7E70}
/* LE CTA PRIMAIRE — ombre DURE, sans flou, qui disparaît à l'appui avec 3 px de translation */
#plusScreen #pcCadre #buyMonth{left:22px!important;top:700px!important;width:346px!important;max-width:346px!important;
  height:58px!important;min-height:58px!important;border-radius:29px!important;border:0!important;
  display:flex!important;align-items:center!important;justify-content:center!important;
  background:#FA2258!important;color:#F4EEE1!important;-webkit-text-fill-color:#F4EEE1!important;
  font-family:ApfelMid,system-ui,sans-serif!important;font-weight:500!important;font-size:17px!important;
  box-shadow:0 3px 0 0 #B8123F!important;pointer-events:auto!important;position:absolute!important;overflow:hidden!important;
  transition:box-shadow .12s linear,transform .12s linear}
#plusScreen #pcCadre #buyMonth:active{box-shadow:none!important;transform:translateY(3px)}
#plusScreen #pcCadre #buyMonth .pc-sig{position:absolute;left:0;top:0;width:346px;height:58px;opacity:0;pointer-events:none}
#plusScreen #pcCadre #buyMonth .pc-lb{position:relative;z-index:2}
/* LE CTA SECONDAIRE — texte souligné, sans contour */
#plusScreen #pcCadre #buyYear{left:22px!important;top:766px!important;width:346px!important;max-width:346px!important;
  height:24px!important;min-height:0!important;border:0!important;background:transparent!important;border-radius:0!important;
  display:flex!important;align-items:center!important;justify-content:center!important;box-shadow:none!important;
  font-family:Apfel,system-ui,sans-serif!important;font-weight:400!important;font-size:15px!important;
  color:#1A1613!important;-webkit-text-fill-color:#1A1613!important;text-decoration:underline!important;
  text-underline-offset:3px!important;pointer-events:auto!important;position:absolute!important}
/* LE LÉGAL */
#plusScreen #pcCadre .pc-legal{left:22px!important;top:806px!important;width:346px!important;text-align:center!important;
  font-family:Apfel,system-ui,sans-serif;font-weight:400;font-size:11px;line-height:14px;color:#8A7E70;-webkit-text-fill-color:#8A7E70}
</style>
<script id="lot-CERCLE-TOILE">
/* ⚑ L'ÉCRAN QUI VEND — la pose et la Toile. Voir le bloc CSS juste au-dessus. */
(function(){
  var CADW = 346, CADH = 276, MONDES_C = ['sillons', 'gravure', 'terrazzo'];
  var N_MAX = 14, PERIODE = 4500, MUE = 900, CASC = 420, PAS = 18;
  var MOTS = {
    h: 'Le Cercle', sub: 'ta parole, et celle qu’on te tient',
    args: [['L’autre moitié de ta Toile', 'ce que tes proches tiennent envers toi'],
           ['Une parole n’est pas l’autre', 'récurrence, rappel, importance, mémoire'],
           ['Ta Toile change de matière', 'Sillons, Gravure, Terrazzo']],
    prix: ['39 €', 'soit 3,25 €/mois'],
    legal: 'Sans engagement · résiliable à tout moment'
  };
  var TOPS = [494, 542, 590];
  var CAD = null, CV = null, G = null, DAL = [], t0 = 0, raf = 0, prochaine = 0, mue = null, ouvertA = 0, iMue = 0;
  function ps(){ return document.getElementById('plusScreen'); }
  function el(t, c){ var e = document.createElement(t); if(c) e.className = c; return e; }
  /* ── la matière d'une dalle, dans le monde demandé : TOUJOURS le moteur (§4 règle 1) ── */
  var CACHE = {};
  function matiere(id, m){
    var k = id + '|' + m; if(CACHE[k] !== undefined) return CACHE[k];
    var base = {}; try{ base = window.Toile.mondeCourant() || {}; }catch(_){ }
    var c = document.createElement('canvas'), ok = false;
    try{ ok = window.Toile.dalleTrame(c, id, 1, m ? {m:m, p:base.p, h:base.h} : undefined); }catch(_){ }
    return (CACHE[k] = (ok && c.width) ? c : null);
  }
  /* ── les dalles réelles et leurs cellules ─────────────────────────────────────── */
  function recense(){
    var ids = [];
    try{ ids = (typeof promises !== 'undefined' ? promises : []).filter(function(p){ return !p.draft && !p.req; }).map(function(p){ return p.id; }); }catch(_){ }
    if(!ids.length) return [];
    try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(_){ }
    var out = [];
    ids.forEach(function(id){ var d = null; try{ d = window.Toile.dalleAbs(id); }catch(_){ }
      if(d && d.w > 0 && d.h > 0) out.push({id:id, x:d.minx, y:d.miny, w:d.w, h:d.h}); });
    return out;
  }
  /* la fenêtre : on la CALE sur la bande la plus dense, en la MESURANT — jamais à l'œil (§8) */
  function fenetre(cells){
    var s = CADW / 390, vh = CADH / s;                       /* la hauteur de Toile que le cadre montre */
    var y0 = Math.min.apply(null, cells.map(function(c){ return c.y; }));
    var y1 = Math.max.apply(null, cells.map(function(c){ return c.y + c.h; }));
    var best = y0, bn = -1;
    for(var t = y0; t <= Math.max(y0, y1 - vh); t += 4){
      var n = 0;
      for(var i = 0; i < cells.length; i++){ var cy = cells[i].y + cells[i].h / 2;
        if(cy >= t && cy <= t + vh) n++; }
      if(n > bn){ bn = n; best = t; }
    }
    return {s:s, ox:0, oy:best, vh:vh, dedans:bn};
  }
  function bati(){
    var s = ps(); if(!s) return false;
    if(CAD && CAD.isConnected) return true;
    CAD = el('div'); CAD.id = 'pcCadre';
    var x = el('div', 'pc-x');
    x.innerHTML = '<svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true"><path d="M4 4 L16 16 M16 4 L4 16" stroke="#1A1613" stroke-width="1.5" fill="none" stroke-linecap="round"/></svg>';
    x.setAttribute('data-close', ''); CAD.appendChild(x);
    var t = el('div', 'pc-toile'); CV = document.createElement('canvas'); t.appendChild(CV); CAD.appendChild(t);
    var h = el('div', 'pc-h'); h.textContent = MOTS.h; CAD.appendChild(h);
    var su = el('div', 'pc-sub'); su.textContent = MOTS.sub; CAD.appendChild(su);
    MOTS.args.forEach(function(a, i){ var d = el('div', 'pc-arg'); d.style.setProperty('top', TOPS[i] + 'px', 'important');
      var b = el('b'); b.textContent = a[0]; var q = el('i'); q.textContent = a[1];
      d.appendChild(b); d.appendChild(q); CAD.appendChild(d); });
    var p = el('div', 'pc-prix'); var pb = el('b'); pb.textContent = MOTS.prix[0]; var pi = el('i'); pi.textContent = MOTS.prix[1];
    p.appendChild(pb); p.appendChild(pi); CAD.appendChild(p);
    var mo = document.getElementById('buyMonth'), yr = document.getElementById('buyYear');
    if(mo){ mo.textContent = ''; var sig = el('canvas', 'pc-sig'); var lb = el('span', 'pc-lb'); lb.textContent = 'Essayer 14 jours';
      mo.appendChild(sig); mo.appendChild(lb); mo.__sig = sig; CAD.appendChild(mo); }
    if(yr){ yr.textContent = 'ou prendre l’année — 39 €'; CAD.appendChild(yr); }
    var lg = el('div', 'pc-legal'); lg.textContent = MOTS.legal; CAD.appendChild(lg);
    s.appendChild(CAD);
    signature(mo);
    return true;
  }
  /* le cadre sur l'APPAREIL — cotes de disposition, l'écran vit sous .frame décalé de 16 (CLAUDE §8) */
  function off(e, anc){ var x = 0, y = 0; while(e && e !== anc){ x += e.offsetLeft; y += e.offsetTop; e = e.offsetParent; } return [x, y]; }
  function pose(){
    var s = ps(), dv = document.getElementById('device'); if(!s || !dv || !bati()) return;
    var fr = s.closest('.frame') || document.body, a = off(dv, fr), b = off(s, fr);
    CAD.style.setProperty('left', (a[0] - b[0]) + 'px', 'important');
    CAD.style.setProperty('top', (a[1] - b[1]) + 'px', 'important');
  }
  /* ── LA TOILE : on prépare les dalles, leur place et leur matière ─────────────── */
  function prepare(){
    var cells = recense(); if(!cells.length) return false;
    cells.sort(function(a, b){ return b.id - a.id; });
    var F = fenetre(cells);
    /* on garde celles qui tombent dans la fenêtre, au plus N_MAX, en ordre de Toile (déterministe) */
    var dans = cells.filter(function(c){ var cy = c.y + c.h / 2; return cy >= F.oy && cy <= F.oy + F.vh; });
    if(dans.length > N_MAX) dans = dans.slice(0, N_MAX);
    if(!dans.length) dans = cells.slice(0, N_MAX);
    dans.sort(function(a, b){ return (a.y - b.y) || (a.x - b.x); });
    var dpr = Math.min(2, window.devicePixelRatio || 1), base = null;
    try{ base = (window.Toile.mondeCourant() || {}).m; }catch(_){ }
    /* TROIS en matière Cercle, réparties, choisies DÉTERMINISTEMENT (jamais un tirage, §4) */
    var pas = Math.max(1, Math.floor(dans.length / 3));
    DAL = dans.map(function(c, i){
      var j = MONDES_C.indexOf(null); /* placeholder */
      var cercle = (i === pas - 1) ? 0 : (i === 2 * pas - 1) ? 1 : (i === 3 * pas - 1 ? 2 : -1);
      var m = cercle >= 0 ? MONDES_C[cercle] : base;
      var cv = matiere(c.id, m);
      if(!cv) return null;
      var dw = cv.width / dpr, dh = cv.height / dpr;
      var padX = (dw - c.w) / 2, padY = (dh - c.h) / 2;
      return {id:c.id, monde:m, cercle:cercle >= 0, cv:cv, alpha:0,
              X:(c.x - padX - F.ox) * F.s, Y:(c.y - padY - F.oy) * F.s, W:dw * F.s, H:dh * F.s};
    }).filter(Boolean);
    CV.width = Math.round(CADW * dpr); CV.height = Math.round(CADH * dpr);
    G = CV.getContext('2d'); G.setTransform(dpr, 0, 0, dpr, 0, 0);
    window._vendToile = {dalles:DAL.length, cercle:DAL.filter(function(d){ return d.cercle; }).map(function(d){ return d.monde; }),
                         fenetre:{y:Math.round(F.oy), hauteur:Math.round(F.vh), echelle:+F.s.toFixed(4), dedans:F.dedans},
                         base:base};
    return DAL.length > 0;
  }
  function bez(t){ /* cubic-bezier(.32,.72,0,1) — résolu par bissection sur x */
    var lo = 0, hi = 1, u = t, i, x;
    for(i = 0; i < 18; i++){ u = (lo + hi) / 2; var v = 1 - u;
      x = 3 * v * v * u * 0.32 + 3 * v * u * u * 0 + u * u * u;
      if(x < t) lo = u; else hi = u; }
    var v2 = 1 - u; return 3 * v2 * v2 * u * 0.72 + 3 * v2 * u * u * 1 + u * u * u;
  }
  function peint(t){
    G.clearRect(0, 0, CADW, CADH);
    for(var i = 0; i < DAL.length; i++){
      var d = DAL[i];
      /* la cascade d'entrée : 420 ms par dalle, 18 ms de décalage */
      var age = t - ouvertA - i * PAS, a = age <= 0 ? 0 : (age >= CASC ? 1 : bez(age / CASC));
      if(a <= 0) continue;
      G.globalAlpha = a;
      if(mue && mue.i === i){ var p = Math.min(1, (t - mue.t0) / MUE), e = bez(p);
        G.globalAlpha = a * (1 - e); G.drawImage(d.cv, d.X, d.Y, d.W, d.H);
        G.globalAlpha = a * e; G.drawImage(mue.cv, d.X, d.Y, d.W, d.H);
      } else G.drawImage(d.cv, d.X, d.Y, d.W, d.H);
    }
    G.globalAlpha = 1;
  }
  function image(t){
    raf = 0; var s = ps(); if(!s || !s.classList.contains('show')) return;   /* visible = porte `.show` (§8) */
    if(!ouvertA) ouvertA = t;
    /* UN SEUL MOUVEMENT : toutes les 4,5 s, UNE dalle change de matière */
    if(!mue && t >= prochaine && DAL.length){
      iMue = (iMue + 1) % DAL.length; var d = DAL[iMue];
      var suite = d.cercle ? null : MONDES_C[iMue % 3];
      var cv = matiere(d.id, suite);
      if(cv && cv !== d.cv) mue = {i:iMue, t0:t, cv:cv, monde:suite};
      prochaine = t + PERIODE;
    }
    if(mue && t - mue.t0 >= MUE){ var dd = DAL[mue.i]; dd.cv = mue.cv; dd.monde = mue.monde; dd.cercle = !!mue.monde; mue = null; }
    peint(t);
    raf = requestAnimationFrame(image);
  }
  /* ── LA SIGNATURE AU RELÂCHEMENT : le bouton se remplit de la matière du monde actif, 400 ms ── */
  function signature(mo){
    if(!mo || mo.__sigPose) return; mo.__sigPose = 1;
    mo.addEventListener('pointerup', function(){
      var sig = mo.__sig; if(!sig || !DAL.length) return;
      var src = matiere(DAL[0].id, null); if(!src) return;
      var dpr = Math.min(2, window.devicePixelRatio || 1);
      sig.width = Math.round(346 * dpr); sig.height = Math.round(58 * dpr);
      var g = sig.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
      var k = Math.max(346 / src.width * dpr, 58 / src.height * dpr);
      g.clearRect(0, 0, 346, 58);
      g.drawImage(src, (346 - src.width / dpr * k) / 2, (58 - src.height / dpr * k) / 2, src.width / dpr * k, src.height / dpr * k);
      var d0 = performance.now();
      (function pas(){ var p = (performance.now() - d0) / 400;
        if(p >= 1){ sig.style.opacity = 0; return; }
        sig.style.opacity = String(Math.sin(p * Math.PI) * 0.85); requestAnimationFrame(pas); })();
    }, {passive:true});
  }
  function demarre(){ if(!bati() || !prepare()) return; ouvertA = 0; prochaine = 0; mue = null; iMue = -1;
    if(!raf) raf = requestAnimationFrame(image); }
  function arrete(){ if(raf){ cancelAnimationFrame(raf); raf = 0; } }
  window._vendToileGo = demarre;
  var ouvert = false;
  function veille(){
    var s = ps(); if(!s) return;
    new MutationObserver(function(){
      var o = s.classList.contains('show'); if(o === ouvert) return; ouvert = o;   /* on compare avant d'agir (§8) */
      if(o){ try{ s.scrollTop = 0; pose(); }catch(_){ } setTimeout(demarre, 0); } else arrete();
    }).observe(s, {attributes:true, attributeFilter:['class']});
  }
  try{ bati(); pose(); veille(); }catch(_){ }
})();
</script>
"""
assert S.count('</body>') == 1
S = S.replace('</body>', BLOC + '</body>'); print('  ✔ lot-CERCLE-TOILE posé en fin de fichier')
io.open(F, 'w', encoding='utf-8').write(S)
print('copie', avant, '→', hashlib.md5(S.encode('utf-8')).hexdigest())
