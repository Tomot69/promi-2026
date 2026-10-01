/* Promi — quatre mondes de la Toile, au CONTRAT-MONDE
 * Esquille · Bobinette · Ritournelle · Madrure — version d'intégration, 23 sept. 2026
 *
 * COLLAGE : le corps de chaque fonction se colle dans l'IIFE de la Toile, où g, W, H, DPR, seeds,
 * view, cOf, avg, cAt, isLightM, _dalleDeCle, curPAL, rampe, cleToile sont dans la fermeture.
 * Ici ces noms viennent d'une fabrique (creerMondes(env)) et sont rafraîchis par _sync().
 * À supprimer au collage : les lignes « _sync(); » et la fabrique autour. Rien d'autre.
 *
 * Signature : R<nom>(now, x0, y0, x1, y1) — (x0,y0,x1,y1) = rectangle visible, en coordonnées Toile.
 * Registres : Esquille LIBRE · Bobinette LIBRE + trame ancrée · Ritournelle CONTENUE · Madrure LIBRE.
 *
 * Garanties vérifiées sur ce fichier :
 *  - aucune image : ni getImageData, putImageData, drawImage, createPattern, toDataURL, createImageData,
 *    ni canevas hors écran — uniquement des chemins (Path2D, arc, Bézier) remplis ou tracés ;
 *  - aucune couleur écrite : toute couleur vient de cOf(), curPAL() ou rampe() ; les seules
 *    constantes sont des nuances (mélange vers le clair ou le sombre) d'une couleur reçue ;
 *  - toute longueur est une fraction de u (médiane des distances au plus proche voisin) ;
 *    sp = 1,2·u est l'écart moyen des prototypes, repris pour garder leurs proportions.
 *  - hasard : LCG amorcé par la clé stable de chaque cellule (_dalleDeCle), jamais par l'index.
 */
(function () {

function creerMondes(env) {
  var g, W, H, DPR, seeds, view, cOf, avg, cAt, isLightM, _dalleDeCle, curPAL, rampe, cleToile, fondToile;
  var _enreg = false, _rec = null;
  // ⚑ intégration v32 : la géométrie GARDÉE (Madrure, carnets) se calcule sur la position de REPOS — sa signature
  // (_madSig) l'est déjà ; sans ce drapeau elle se bâtissait sur la position frémissante et restait décalée.
  var _repos = false;
  function _auRepos(f) { return function () { var o = _repos; _repos = true; try { return f.apply(this, arguments); } finally { _repos = o; } }; }
  var _MUET = { save: _nop, restore: _nop, beginPath: _nop, closePath: _nop, moveTo: _nop, lineTo: _nop, arc: _nop,
    bezierCurveTo: _nop, quadraticCurveTo: _nop, fill: _nop, stroke: _nop, clip: _nop, fillRect: _nop, setTransform: _nop,
    translate: _nop, scale: _nop, rect: _nop };
  function _nop() {}
  function _note(k, item) { if (!_rec) return; (_rec[k] || (_rec[k] = [])).push(item); }
  function _sync() {
    g = env.g; W = env.W; H = env.H; DPR = env.DPR; seeds = env.seeds; view = env.view;
    cOf = env.cOf; avg = env.avg; cAt = env.cAt; isLightM = env.isLightM;
    _dalleDeCle = env._dalleDeCle; curPAL = env.curPAL; rampe = env.rampe; cleToile = env.cleToile; fondToile = env.fondToile;
    if (_enreg) g = _MUET;
  }

  /* ---------- socle commun ------------------------------------------------ */

  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = (h * 16777619) >>> 0; } return h >>> 0; }

  // clé stable d'une cellule : jamais son index dans seeds, jamais son id
  function _cle(s) {
    if (s.pid != null && typeof _dalleDeCle === 'function') { var k = _dalleDeCle(s.pid); if (k != null) return k >>> 0; }
    if (s.nuee) return _fnv('n\u0000' + s.nuee);
    if (s.pid != null) return _fnv('p\u0000' + s.pid);
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lcg(k) { var sd = (k >>> 0) || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }

  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  // nuance d'une couleur de cOf : t>0 vers le clair, t<0 vers le sombre. Jamais une autre teinte.
  function _nu(c, t) {
    var b = t > 0 ? 255 : 0, a = Math.abs(t);
    return [c[0] + (b - c[0]) * a, c[1] + (b - c[1]) * a, c[2] + (b - c[2]) * a];
  }

  // index spatial : construit une fois par appel, O(n)
  function _idx() {
    var n = seeds.length, i, s, sx, sy;
    var x0 = 1e18, y0 = 1e18, x1 = -1e18, y1 = -1e18;
    for (i = 0; i < n; i++) {
      s = seeds[i]; sx = (_repos || s.px == null) ? s.x : s.px; sy = (_repos || s.py == null) ? s.y : s.py;
      if (sx < x0) x0 = sx; if (sy < y0) y0 = sy; if (sx > x1) x1 = sx; if (sy > y1) y1 = sy;
    }
    if (n === 0) { x0 = y0 = 0; x1 = y1 = 1; }
    var bs = Math.sqrt(Math.max(1, (x1 - x0 + 1) * (y1 - y0 + 1)) / Math.max(1, n));
    if (!(bs > 0)) bs = 32;
    var cols = Math.max(1, Math.ceil((x1 - x0 + 1) / bs)), rows = Math.max(1, Math.ceil((y1 - y0 + 1) / bs));
    var bk = new Array(cols * rows); for (i = 0; i < bk.length; i++) bk[i] = [];
    var P = new Array(n);
    for (i = 0; i < n; i++) {
      s = seeds[i]; sx = (_repos || s.px == null) ? s.x : s.px; sy = (_repos || s.py == null) ? s.y : s.py;
      P[i] = { s: s, x: sx, y: sy, w: s.w || 0, k: _cle(s) };
      var bx = Math.min(cols - 1, Math.max(0, Math.floor((sx - x0) / bs)));
      var by = Math.min(rows - 1, Math.max(0, Math.floor((sy - y0) / bs)));
      bk[by * cols + bx].push(P[i]);
    }
    function ring(x, y, r, out) {
      out.length = 0;
      var a = Math.max(0, Math.floor((x - x0 - r) / bs)), b = Math.min(cols - 1, Math.floor((x - x0 + r) / bs));
      var c = Math.max(0, Math.floor((y - y0 - r) / bs)), e = Math.min(rows - 1, Math.floor((y - y0 + r) / bs));
      for (var j = c; j <= e; j++) for (var i2 = a; i2 <= b; i2++) {
        var L = bk[j * cols + i2];
        for (var t = 0; t < L.length; t++) out.push(L[t]);
      }
      return out;
    }
    // propriétaire d'un point : règle pondérée du moteur, cherchée chez les voisines seulement
    var tmp = [];
    function owner(x, y) {
      var r = bs * 1.6, best = null, bd = 1e18, tries = 0;
      while (tries++ < 4) {
        ring(x, y, r, tmp);
        if (tmp.length) {
          bd = 1e18;
          for (var i3 = 0; i3 < tmp.length; i3++) {
            var p = tmp[i3], dx = x - p.x, dy = y - p.y;
            var d = Math.sqrt(dx * dx + dy * dy) - p.w;
            if (d < bd) { bd = d; best = p; }
          }
          if (best) return best;
        }
        r *= 2;
      }
      return P[0];
    }
    // voisines d'une graine, triées, et unité locale u = distance à la plus proche
    var nbuf = [];
    function near(p, howMany) {
      var r = bs * 1.8, got = [];
      for (var tries = 0; tries < 4; tries++) {
        ring(p.x, p.y, r, nbuf); got.length = 0;
        for (var i4 = 0; i4 < nbuf.length; i4++) {
          var q = nbuf[i4]; if (q === p) continue;
          var dx = q.x - p.x, dy = q.y - p.y;
          got.push({ p: q, d: Math.sqrt(dx * dx + dy * dy) });
        }
        if (got.length >= howMany) break;
        r *= 2;
      }
      got.sort(function (a, b) { return a.d - b.d; });
      return got.slice(0, howMany);
    }
    return { P: P, bs: bs, owner: owner, near: near, ring: ring, x0: x0, y0: y0 };
  }

  // unité globale d'une surface : médiane des distances au plus proche voisin (suit k, jamais des px)
  function _uGlobal(ix) {
    // plus proche voisin par compartiments, sans allocation ni tri par graine
    var P = ix.P, us = [], buf = [];
    for (var i = 0; i < P.length; i++) {
      var p = P[i], r = ix.bs * 1.8, best = 1e18, tries = 0;
      while (tries++ < 4) {
        ix.ring(p.x, p.y, r, buf);
        best = 1e18;
        for (var k = 0; k < buf.length; k++) {
          var q = buf[k]; if (q === p) continue;
          var dx = q.x - p.x, dy = q.y - p.y, d = dx * dx + dy * dy;
          if (d < best) best = d;
        }
        if (best < 1e17) break;
        r *= 2;
      }
      if (best < 1e17) us.push(Math.sqrt(best));
    }
    if (!us.length) return avg();
    us.sort(function (a, b) { return a - b; });
    return us[us.length >> 1] || avg();
  }

  /* ⚑ intégration v34 (Tom, PDF « la toile grandit ») — L'UNITÉ DE MATIÈRE EST FIXE. Elle était l'écart médian entre
     graines : juste tant que la Toile était un semis constant de 68 cellules ; faux depuis que le semis grandit avec les
     promesses (à 3 promesses, le fil de Bobinette et les bandes de Madrure devenaient énormes). Le moteur donne `env.uMat`,
     l'unité d'une Toile à la densité historique (√(W·H/68), × UK) ; chaque monde la multiplie par SON facteur, relevé sur
     le PDF validé : Esquille 0,5 (un éclat ~35 px), Bobinette 1,07 (douze anneaux sur la largeur),
     Madrure 1,38 (une bande ≈ 20 px). Ritournelle garde l'écart entre graines : sa coulée remplit SA cellule. */
  var U_ESQ = 0.5, U_BOB = 1.07, U_MAD = 1.38;   // relevés côte à côte avec les cadres du PDF (12 anneaux sur la largeur ; bande ≈ 20 px)
  function _uMonde(ix, f) { var um = env.uMat; return (typeof um === 'number' && um > 0) ? um * f : _uGlobal(ix); }
  var _tonsForces = null, _esqCache = null;
  function _ingenu() { if (!env.ingenu) return false; for (var i = 0; i < seeds.length; i++) if (seeds[i].apercu) return false; return true; }

  /* --- géométrie de polygone (aucune image, que des chemins) --------------- */
  function _clip(poly, px, py, nx, ny) {
    var out = [], n = poly.length;
    for (var i = 0, j = n - 1; i < n; j = i++) {
      var A = poly[j], B = poly[i];
      var da = (A[0] - px) * nx + (A[1] - py) * ny, db = (B[0] - px) * nx + (B[1] - py) * ny;
      if (db <= 0) { if (da > 0) { var t = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]); } out.push(B); }
      else if (da <= 0) { var t2 = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t2, A[1] + (B[1] - A[1]) * t2]); }
    }
    return out;
  }
  function _cent(p) { var x = 0, y = 0, n = p.length; for (var i = 0; i < n; i++) { x += p[i][0]; y += p[i][1]; } return [x / n, y / n]; }
  function _aire(p) { var a = 0, n = p.length; for (var i = 0, j = n - 1; i < n; j = i++) a += p[j][0] * p[i][1] - p[i][0] * p[j][1]; return Math.abs(a / 2); }
  function _retrait(p, d) {
    var c = _cent(p), out = [], n = p.length;
    for (var i = 0; i < n; i++) {
      var dx = c[0] - p[i][0], dy = c[1] - p[i][1], l = Math.sqrt(dx * dx + dy * dy) || 1;
      var m = Math.min(d, l * 0.48);
      out.push([p[i][0] + dx / l * m, p[i][1] + dy / l * m]);
    }
    return out;
  }
  // retrait à largeur CONSTANTE : chaque arête reculée de d, les angles restent vifs
  function _offset(p, d) {
    var n = p.length, c = _cent(p), li = [];
    for (var i = 0; i < n; i++) {
      var a = p[i], b = p[(i + 1) % n];
      var nx = b[1] - a[1], ny = -(b[0] - a[0]), l = Math.sqrt(nx * nx + ny * ny) || 1;
      nx /= l; ny /= l;
      if ((c[0] - a[0]) * nx + (c[1] - a[1]) * ny < 0) { nx = -nx; ny = -ny; }
      li.push([a[0] + nx * d, a[1] + ny * d, b[0] - a[0], b[1] - a[1]]);
    }
    var out = [];
    for (var k = 0; k < n; k++) {
      var A = li[k], B = li[(k + 1) % n], den = A[2] * B[3] - A[3] * B[2];
      if (Math.abs(den) < 1e-9) { out.push([B[0], B[1]]); continue; }
      var t = ((B[0] - A[0]) * B[3] - (B[1] - A[1]) * B[2]) / den;
      out.push([A[0] + A[2] * t, A[1] + A[3] * t]);
    }
    return out;
  }
  function _trace(p) { g.beginPath(); g.moveTo(p[0][0], p[0][1]); for (var i = 1; i < p.length; i++) g.lineTo(p[i][0], p[i][1]); g.closePath(); }
  function _traceDoux(p) {
    var n = p.length;
    g.beginPath();
    g.moveTo((p[n - 1][0] + p[0][0]) / 2, (p[n - 1][1] + p[0][1]) / 2);
    for (var i = 0; i < n; i++) {
      var a = p[i], b = p[(i + 1) % n];
      g.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
    }
    g.closePath();
  }
  // cellule approchée d'une graine : demi-plans pondérés de ses voisines
  function _cellule(p, vois, marge) {
    var poly = [[p.x - marge, p.y - marge], [p.x + marge, p.y - marge], [p.x + marge, p.y + marge], [p.x - marge, p.y + marge]];
    for (var i = 0; i < vois.length; i++) {
      var q = vois[i].p, d = vois[i].d; if (d <= 0) continue;
      var dx = (q.x - p.x) / d, dy = (q.y - p.y) / d;
      var t = 0.5 * d + (p.w - q.w) * 0.5;           // bissectrice décalée par les poids
      if (t < d * 0.12) t = d * 0.12; if (t > d * 0.88) t = d * 0.88;
      poly = _clip(poly, p.x + dx * t, p.y + dy * t, dx, dy);
      if (poly.length < 3) return null;
    }
    return poly;
  }
  function _visible(p, u, x0, y0, x1, y1) {
    return !(p.x < x0 - u * 2 || p.x > x1 + u * 2 || p.y < y0 - u * 2 || p.y > y1 + u * 2);
  }

  /* ---------- 1 · ESQUILLE — la plaque brisée ----------------------------- */
  /* LA PLAQUE SE CASSE AUTOUR DES PROMESSES, et UNE DALLE EST UN FRAGMENT.
     Chaque cassure sépare le semis en deux groupes, et on recommence : à la fin, chaque fragment
     contient exactement une cellule. Les cassures sont donc longues et partagées — c'est ça, une
     plaque brisée. Une promesse « prend plus de place » que la matière (1 + 1,9 − 1,6·sat), donc
     son fragment est plus gros tant que la Toile est vide, et rejoint la taille commune à
     saturation : l'œil trouve les dalles. Planter une promesse ne recasse que la branche où elle
     tombe : les voisines s'écartent, se reproportionnent, puis se stabilisent. La plaque part de la
     boîte des graines, jamais du canevas. */
  function Resq(now, x0, y0, x1, y1) {
    _sync();
    var ix = _idx(), P = ix.P;
    if (!P.length) return;
    var u = _uMonde(ix, U_ESQ), fel = u * 0.022, i;
    /* ⚑ intégration v34 — LA PLAQUE SE CASSE SUR UN SEMIS DE MATIÈRE À PAS FIXE (une graine par u, ancrée sur la
       Toile, tirée de la clé de la Toile), et chaque éclat prend la couleur de la PROMESSE qui possède son germe : « les
       éclats d'une même couleur font une promesse » (PDF). Avant, un éclat = une graine : à 3 promesses, 3 éclats. */
    function place(p) { return 1; }
    var cle0 = typeof cleToile === 'number' ? (cleToile >>> 0) : 0;
    // v34 : la cassure ne dépend que du semis de matière (taille, unité, clé) — elle est GARDÉE ; seule la couleur des
    // éclats suit les promesses. À la plantation, la plaque ne se recasse plus à chaque image : elle se recolore.
    var cleG = W + '|' + H + '|' + u.toFixed(3) + '|' + cle0, CG = _esqCache;
    if (CG && CG.cle === cleG) {
      var S = CG.S, feuilles = CG.feuilles;
      for (i = 0; i < S.length; i++) { var ow = ix.owner(S[i].x, S[i].y); S[i].s = ow.s; S[i].own = ow; }
    } else {
    var S = [], nxg = Math.ceil(W / u) + 1, nyg = Math.ceil(H / u) + 1;
    for (var gj = -1; gj < nyg; gj++) for (var gi = -1; gi < nxg; gi++) {
      var rg = _lcg((cle0 ^ Math.imul(gi + 7, 73856093) ^ Math.imul(gj + 7, 19349663)) >>> 0);
      var gx = (gi + 0.15 + 0.7 * rg()) * u, gy = (gj + 0.15 + 0.7 * rg()) * u, own = ix.owner(gx, gy);
      S.push({ x: gx, y: gy, k: (rg() * 4294967295) >>> 0, s: own.s, own: own });
    }
    if (!S.length) return;
    var bx0 = 1e18, by0 = 1e18, bx1 = -1e18, by1 = -1e18;
    for (i = 0; i < S.length; i++) { if (S[i].x < bx0) bx0 = S[i].x; if (S[i].y < by0) by0 = S[i].y; if (S[i].x > bx1) bx1 = S[i].x; if (S[i].y > by1) by1 = S[i].y; }
    var m = u * 0.7;
    var feuilles = [];
    function casser(poly, germes, prof) {
      if (germes.length === 1 || prof > 26) { feuilles.push({ p: poly, s: germes[0] }); return; }   // une feuille = une cellule = un fragment
      var cx = 0, cy = 0, k;
      for (k = 0; k < germes.length; k++) { cx += germes[k].x; cy += germes[k].y; }
      cx /= germes.length; cy /= germes.length;
      var xx = 0, yy = 0, xy = 0;
      for (k = 0; k < germes.length; k++) { var dx = germes[k].x - cx, dy = germes[k].y - cy; xx += dx * dx; yy += dy * dy; xy += dx * dy; }
      var ang = 0.5 * Math.atan2(2 * xy, xx - yy);
      var kx = 0; for (k = 0; k < germes.length; k++) kx = (kx ^ germes[k].k) >>> 0;
      var r = _lcg(kx);
      ang += (r() - 0.5) * 0.6;                               // la brisure : l'angle dévie
      var nx = Math.cos(ang), ny = Math.sin(ang);
      var proj = germes.map(function (s) { return { s: s, t: s.x * nx + s.y * ny }; }).sort(function (a, b) { return a.t - b.t; });
      var tot = 0; for (k = 0; k < proj.length; k++) tot += place(proj[k].s);
      var acc = 0, idx = 0;
      for (k = 0; k < proj.length - 1; k++) { acc += place(proj[k].s); idx = k; if (acc >= tot * 0.5) break; }
      var t0 = proj[idx].t, t1 = proj[idx + 1].t, w0 = place(proj[idx].s), w1 = place(proj[idx + 1].s);
      var cut = t0 + (t1 - t0) * (w0 / (w0 + w1)) * (0.75 + r() * 0.5);
      var px = nx * cut, py = ny * cut;
      var A = _clip(poly, px, py, nx, ny), B = _clip(poly, px, py, -nx, -ny);
      var GA = [], GB = [];
      for (k = 0; k < proj.length; k++) (k <= idx ? GA : GB).push(proj[k].s);
      if (A.length > 2 && GA.length) casser(A, GA, prof + 1);   // _clip garde le côté d ≤ 0
      if (B.length > 2 && GB.length) casser(B, GB, prof + 1);
    }
    casser([[bx0 - m, by0 - m], [bx1 + m, by0 - m], [bx1 + m, by1 + m], [bx0 - m, by1 + m]], S, 0);
    _esqCache = { cle: cleG, S: S, feuilles: feuilles };
    }

    for (i = 0; i < feuilles.length; i++) {
      var fe = feuilles[i], p = fe.p, s = fe.s;
      if (!p || p.length < 3 || !s) continue;
      var ar = _aire(p); if (ar < u * u * 0.006) continue;
      var c = _cent(p);
      if (c[0] < x0 - u || c[0] > x1 + u || c[1] < y0 - u || c[1] > y1 + u) continue;
      var col = cOf(s.s, now);
      if (_promesse(s.s)) {
        var tv = _lcg((s.own.k ^ 0x5bf03635) >>> 0)();
        if (tv < 0.18) col = _nu(col, -0.18);                  // l'éclat prend parfois une nuance
      }
      var peint = _offset(p, Math.min(fel, Math.sqrt(ar) * 0.16));
      if (_rec && _promesse(s.s)) _note(s.own.k, { poly: peint, col: col });
      g.fillStyle = _rgb(col);
      _trace(peint); g.fill();
    }
  }

  /* ---------- couleurs : palette, rampe, matière ------------------------- */
  function _arr(c) {
    if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
    return c;
  }
  function _pal() {
    var p = typeof curPAL === 'function' ? curPAL() : null;
    if (!p || p.length < 4) return null;
    return [_arr(p[0]), _arr(p[1]), _arr(p[2]), _arr(p[3])];
  }
  // une graine porte une promesse si elle a un pid ou une nuée ; sinon c'est de la matière
  function _promesse(s) { return s.pid != null || !!s.nuee; }
  // rampe de quatre tons d'une cellule (§10). Tant que le moteur ne la publie pas :
  // la couleur de la cellule, puis la palette dans son ordre ; la matière prend des nuances de sa couleur.
  function _rampe(s, now) {
    if (typeof rampe === 'function') { var r = rampe(s, now); if (r && r.length >= 4) return [_arr(r[0]), _arr(r[1]), _arr(r[2]), _arr(r[3])]; }
    var c = cOf(s, now), P = _pal();
    if (P && (_promesse(s) || s.apercu)) {                     // v35 : une cellule d'APERÇU (Studio) tourne la palette comme une promesse — sinon toutes ses strates avaient la même couleur
      var b = 0, bd = 1e9;
      for (var i = 0; i < 4; i++) { var d = Math.abs(c[0] - P[i][0]) + Math.abs(c[1] - P[i][1]) + Math.abs(c[2] - P[i][2]); if (d < bd) { bd = d; b = i; } }
      return [c, P[(b + 1) % 4], P[(b + 2) % 4], P[(b + 3) % 4]];
    }
    return [c, _nu(c, -0.07), _nu(c, 0.06), _nu(c, -0.035)];
  }
  // origine : sp = F.spacing ; au contrat, sp = 1,2 u (u = médiane des distances au plus proche voisin)
  var SP_U = 1.2;
  // Madrure : part minimale du tour qu'une strate doit envelopper pour devenir la dalle d'un nœud sans œil
  var SEUIL_STRATE = 0.70;

  /* ---------- 2 · BOBINETTE — le fil enroulé ------------------------------ */
  /* Portage de noeud() (mondes-origine.js). Changements :
     - c : le terme min(W,H)/9 est en px, il saute ; √(0,62·W·H/4n) = 0,394·sp est gardé, en u.
     - les bobines : une par PROMESSE, au sommet de trame le plus proche de son germe
       (l'origine les jetait au hasard) ; même règle d'exclusion des 8 voisins.
     - le gainage en trait bg saute : en Truchet deux arcs ne se recouvrent jamais,
       il ne peignait que du fond sur du fond. Rien ne change à l'image.
     - couleurs : C[c] → cOf ; C[c2] → rampe[1..3] choisie par la clé. */
  function Rbob(now, x0, y0, x1, y1) {
    _sync();
    var ix = _idx(), P = ix.P, i;
    if (!P.length) return;
    var sp = _uMonde(ix, U_BOB) * SP_U;
    var c = sp * 0.30, th = c * 0.26, extra = th * 0.55;   // origine mesurée sur Toile pleine : c = 0,30·sp
    var anneau = {}, tourne = {}, pris = {}, boucle = {};
    var ordre = P.slice().sort(function (a, b) { return a.k - b.k; });
    for (i = 0; i < ordre.length; i++) {
      var p = ordre[i]; if (!_promesse(p.s)) continue;
      var bi = Math.round(p.x / c), bj = Math.round(p.y / c), fait = false;
      for (var rr = 0; rr <= 2 && !fait; rr++) for (var a = -rr; a <= rr && !fait; a++) for (var b = -rr; b <= rr && !fait; b++) {
        if (Math.max(Math.abs(a), Math.abs(b)) !== rr) continue;
        var gi = bi + a, gj = bj + b, libre = true;
        for (var da = -1; da <= 1 && libre; da++) for (var db = -1; db <= 1; db++) if (pris[(gi + da) + '|' + (gj + db)]) { libre = false; break; }
        if (!libre) continue;
        pris[gi + '|' + gj] = 1; anneau[gi + '|' + gj] = p;
        tourne[(gi - 1) + ',' + (gj - 1)] = 1; tourne[gi + ',' + (gj - 1)] = 0; tourne[(gi - 1) + ',' + gj] = 0; tourne[gi + ',' + gj] = 1;
        fait = true;
      }
    }
    // l'origine posait ~1,7 anneau par cellule. Le surplus n'est pas une dalle : c'est le FIL d'une promesse
    // qui se referme sur lui-même près d'elle — une boucle fine, à sa couleur, jamais épaissie.
    // 0, 1 ou 2 boucles par promesse, tirées de sa clé (40 / 50 / 10 %) : 0,7 en moyenne.
    for (i = 0; i < ordre.length; i++) {
      var p2 = ordre[i]; if (!_promesse(p2.s)) continue;
      var t2 = (p2.k >>> 3) % 10, nb = t2 < 4 ? 0 : t2 < 9 ? 1 : 2;
      if (!nb) continue;
      var ci = Math.round(p2.x / c), cj = Math.round(p2.y / c), rot = p2.k % 8;
      for (var r2 = 1; r2 <= 3 && nb; r2++) {
        var cand = [];
        for (var a2 = -r2; a2 <= r2; a2++) for (var b2 = -r2; b2 <= r2; b2++) if (Math.max(Math.abs(a2), Math.abs(b2)) === r2) cand.push([ci + a2, cj + b2]);
        for (var q2 = 0; q2 < cand.length && nb; q2++) {
          var cc = cand[(q2 + rot) % cand.length], hi = cc[0], hj = cc[1], ok = true;
          // la boucle reste chez sa promesse : son centre doit appartenir à la cellule
          if (ix.owner(hi * c, hj * c) !== p2) continue;
          for (var ea = -1; ea <= 1 && ok; ea++) for (var eb = -1; eb <= 1; eb++) if (pris[(hi + ea) + '|' + (hj + eb)]) { ok = false; break; }
          if (!ok) continue;
          pris[hi + '|' + hj] = 1; boucle[hi + '|' + hj] = p2;
          tourne[(hi - 1) + ',' + (hj - 1)] = 1; tourne[hi + ',' + (hj - 1)] = 0; tourne[(hi - 1) + ',' + hj] = 0; tourne[hi + ',' + hj] = 1;
          nb--;
        }
      }
    }
    var buf = [];
    function near2(x, y) {
      var r = ix.bs * 1.6, s1 = null, d1 = 1e18, d2 = 1e18;
      for (var t = 0; t < 4; t++) {
        ix.ring(x, y, r, buf);
        if (buf.length >= 2) break;
        r *= 2;
      }
      for (var k = 0; k < buf.length; k++) {
        var q = buf[k], dx = x - q.x, dy = y - q.y, d = Math.sqrt(dx * dx + dy * dy) - q.w;
        if (d < d1) { d2 = d1; d1 = d; s1 = q; } else if (d < d2) d2 = d;
      }
      if (d2 > 1e17) d2 = d1 * 3;
      return { p: s1, d1: Math.max(0, d1), d2: Math.max(1e-6, d2) };
    }
    var lots = {};
    var i0 = Math.floor(x0 / c) - 1, i1 = Math.ceil(x1 / c), j0 = Math.floor(y0 / c) - 1, j1 = Math.ceil(y1 / c);
    for (var ti = i0; ti <= i1; ti++) for (var tj = j0; tj <= j1; tj++) {
      var x = ti * c, y = tj * c, f = tourne[ti + ',' + tj];
      if (f === undefined) f = _lcg(_fnv('b' + ti + ',' + tj))() < 0.5 ? 1 : 0;
      var arcs = f
        ? [[x, y, 0, Math.PI / 2], [x + c, y + c, Math.PI, Math.PI * 1.5]]
        : [[x + c, y, Math.PI / 2, Math.PI], [x, y + c, Math.PI * 1.5, Math.PI * 2]];
      for (var m = 0; m < 2; m++) {
        var A = arcs[m];
        var mx = A[0] + Math.cos((A[2] + A[3]) / 2) * c / 2, my = A[1] + Math.sin((A[2] + A[3]) / 2) * c / 2;
        var n = near2(mx, my); if (!n.p) continue;
        var col;
        if (n.d1 / (n.d1 + n.d2) > 0.42) col = _rampe(n.p.s, now)[1 + (n.p.k % 3)];
        else col = cOf(n.p.s, now);
        var vk = Math.round(A[0] / c) + '|' + Math.round(A[1] / c), dalle = !!anneau[vk], sienne = anneau[vk] || boucle[vk];
        if (_rec && sienne) { var exr = dalle ? extra : 0; _note(sienne.k, { A: A, r: c / 2 - exr / 2, w: th + exr, e: th * 0.05, col: col, dalle: dalle }); }
        var key = (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + '|' + (dalle ? 1 : 0);
        var L = lots[key]; if (!L) L = lots[key] = { col: col, dalle: dalle, a: [] };
        L.a.push(A);
      }
    }
    g.save(); g.lineCap = 'butt';
    for (var k2 in lots) {
      var L2 = lots[k2];
      // la bobine d'une promesse garde son diamètre extérieur et s'épaissit vers le centre
      var ex = L2.dalle ? extra : 0, rr2 = c / 2 - ex / 2;
      g.strokeStyle = _rgb(L2.col); g.lineWidth = th + ex;
      g.beginPath();
      for (var z = 0; z < L2.a.length; z++) {
        // raccord : l'arc est prolongé de 0,5 px le long de sa TANGENTE — celle de l'arc voisin au point de jonction.
        // (le prolongement de 0,05 rad suivait la courbure de l'arc, et s'écartait de la voisine en S)
        var A2 = L2.a[z], a0 = A2[2], a1 = A2[3], e = th * 0.05;       // recouvrement de raccord, en fraction du fil (donc de u)
        _arcRaccord(g, A2, rr2, e);
      }
      g.stroke();
    }
    g.restore();
  }

  // un arc de Truchet prolongé le long de sa tangente (raccord exact avec l'arc voisin)
  function _arcRaccord(T, A, r, e) {
    var a0 = A[2], a1 = A[3];
    var sx = A[0] + Math.cos(a0) * r, sy = A[1] + Math.sin(a0) * r, fx = A[0] + Math.cos(a1) * r, fy = A[1] + Math.sin(a1) * r;
    T.moveTo(sx + e * Math.sin(a0), sy - e * Math.cos(a0));
    T.lineTo(sx, sy);
    T.arc(A[0], A[1], r, a0, a1);
    T.lineTo(fx - e * Math.sin(a1), fy + e * Math.cos(a1));
  }

  /* ---------- 3 · RITOURNELLE — la coulée qui tourne et revient ----------- */
  /* Portage de coulee(). Le classement pixel par pixel (t = d/limite, k = ⌊t^0,8·rings⌋)
     devient une pile de contours : l'anneau k est exactement la région
     ((k)/rings)^1,25 ≤ t < ((k+1)/rings)^1,25, soit la limite homothétique de rapport
     ((k+1)/rings)^1,25, peinte de l'extérieur vers le centre. Même résultat, sans image.
     Paramètres inchangés : 144 angles depuis le centroïde de 16 rayons, trois harmoniques
     (2, 3, 5), 0,72 + 0,28·m, liseré 0,006·sp, lissage 8 passes [1 2 3 2 1]/9, rings 3–5.
     Couleurs : rgb[(k + off) % 4] → la rampe de la cellule, l'anneau extérieur portant sa couleur. */
  function Rrit(now, x0, y0, x1, y1) {
    _sync();
    var ix = _idx(), P = ix.P, NA = 144;
    if (!P.length) return;
    var sp = _uGlobal(ix) * SP_U, RMAX = sp * 2.4;
    var cs = new Float64Array(NA), sn = new Float64Array(NA);
    for (var a = 0; a < NA; a++) { cs[a] = Math.cos(a / NA * 6.283); sn[a] = Math.sin(a / NA * 6.283); }
    var lim = new Float64Array(NA), cr = new Float64Array(NA), tmp = new Float64Array(NA);
    for (var i = 0; i < P.length; i++) {
      var p = P[i];
      // ⚑ intégration v32 : pour une dalle seule, le moteur nomme sa graine (env.cible) — on ne peint que SA coulée.
      // Sans cela la coulée d'une voisine, rognée par une cellule APPROCHÉE, mordait sur la vraie cellule et restait
      // en éclat au bord de la dalle (vu à k = 1 et 2,5).
      if (env.cible != null && p.s.pid !== env.cible) continue;
      if (p.x < x0 - RMAX || p.x > x1 + RMAX || p.y < y0 - RMAX || p.y > y1 + RMAX) continue;
      var vois = ix.near(p, 10); if (!vois.length) continue;
      var HD = [];
      for (var v = 0; v < vois.length; v++) {
        var q = vois[v].p, dq = vois[v].d; if (dq <= 0) continue;
        var t0 = 0.5 * dq + (p.w - q.w) * 0.5;
        if (t0 < dq * 0.12) t0 = dq * 0.12; if (t0 > dq * 0.88) t0 = dq * 0.88;
        HD.push((q.x - p.x) / dq, (q.y - p.y) / dq, t0);
      }
      // v34 : une dalle SEULE bute aussi contre les bords de la Toile — sa coulée s'y arrondit au lieu d'être coupée net
      // au bord du canevas (vu sur « + Nuée »). Sur la Toile, rien ne change : c'est l'écran qui la rogne.
      if (env.cible != null && env.bords) { var BT = env.bords; HD.push(-1, 0, p.x - BT[0], 1, 0, BT[2] - p.x, 0, -1, p.y - BT[1], 0, 1, BT[3] - p.y); }
      // rayon de la cellule depuis un point (ox, oy), dans la direction a
      var ray = function (ox, oy, ca, sa) {
        var r = RMAX, ex = ox - p.x, ey = oy - p.y;
        for (var h = 0; h < HD.length; h += 3) {
          var pr = HD[h] * ca + HD[h + 1] * sa; if (pr <= 1e-6) continue;
          var lm = (HD[h + 2] - (ex * HD[h] + ey * HD[h + 1])) / pr;
          if (lm < r) r = lm;
        }
        return r > 0 ? r : 0;
      };
      var cx = 0, cy = 0;
      for (var k = 0; k < 16; k++) { var a16 = k / 16 * 6.283, c16 = Math.cos(a16), s16 = Math.sin(a16), r16 = ray(p.x, p.y, c16, s16); cx += p.x + c16 * r16; cy += p.y + s16 * r16; }
      cx /= 16; cy /= 16;
      var R = _lcg(p.k);
      var h2 = [2, R() * 6.283, 0.05 + R() * 0.03], h3 = [3, R() * 6.283, 0.022 + R() * 0.018], h5 = [5, R() * 6.283, 0.01 + R() * 0.01];
      var rings = 3 + Math.floor(R() * 3);
      for (a = 0; a < NA; a++) {
        var an = a / NA * 6.283;
        var m = 1 + Math.sin(an * h2[0] + h2[1]) * h2[2] + Math.sin(an * h3[0] + h3[1]) * h3[2] + Math.sin(an * h5[0] + h5[1]) * h5[2];
        var rv = ray(cx, cy, cs[a], sn[a]), stp = sp * 0.05;
        cr[a] = rv;
        var rq = stp * Math.max(1, Math.ceil(rv / stp) - 1);          // rayon marché de l'original : r ∈ [R − pas, R)
        lim[a] = rq * (0.72 + 0.28 * m) - sp * 0.006;
      }
      var sm = lim;
      for (var pass = 0; pass < 8; pass++) {
        for (a = 0; a < NA; a++) tmp[a] = (sm[(a - 2 + NA) % NA] + 2 * sm[(a - 1 + NA) % NA] + 3 * sm[a] + 2 * sm[(a + 1) % NA] + sm[(a + 2) % NA]) / 9;
        var sw = sm; sm = tmp; tmp = sw;
      }
      // original : un pixel hors de sa cellule appartient à la voisine, dont la coulée ne l'atteint pas → la Toile respire
      for (a = 0; a < NA; a++) if (sm[a] > cr[a]) sm[a] = cr[a];
      // léger adoucissement après le rognage : efface les fripures sans toucher aux espaces ni aux formes
      for (var ps = 0; ps < 2; ps++) {
        for (a = 0; a < NA; a++) tmp[a] = (sm[(a - 1 + NA) % NA] + 2 * sm[a] + sm[(a + 1) % NA]) / 4;
        for (a = 0; a < NA; a++) sm[a] = tmp[a];
      }
      var RP = _rampe(p.s, now);
      for (var kk = rings - 1; kk >= 0; kk--) {
        var sc = Math.pow((kk + 1) / rings, 1.25);
        g.fillStyle = _rgb(RP[(((kk - (rings - 1)) % 4) + 4) % 4]);
        g.beginPath();
        for (a = 0; a < NA; a++) {
          var rr = Math.max(0, sm[a]) * sc, X = cx + cs[a] * rr, Y = cy + sn[a] * rr;
          if (a === 0) g.moveTo(X, Y); else g.lineTo(X, Y);
        }
        g.closePath(); g.fill();
      }
      if (sm !== lim) { tmp = sm; } // les tampons tournent, rien à rendre
      lim = new Float64Array(NA);
    }
  }

  /* ---------- 4 · MADRURE — l'onde du bois -------------------------------- */
  /* Portage de ecume(). Champ inchangé :
       φ = x·cos θ + y·sin θ + Σ k / (1 + d²/r²),  k = band·(7,5…9,5),  r = sp·(0,36…0,48),  band = 0,17·sp
     sommé sur TOUS les nœuds — chaque promesse est un nœud, son bombement fait la dalle.
     Trois cas : fr < 0,11 → le filet ; m = 2 → le fond ; sinon les veines.
     Le classement par pixel devient un classement par triangle : φ est évalué sur une
     grille de pas 0,36·band, chaque triangle est découpé exactement entre les niveaux,
     et chaque classe est UN chemin rempli (union sans couture). Aucune image.
     Couleurs — comme l'origine : filet = palette[0], veine = palette[1], veine claire = palette[2].
     L'onde n'est pas découpée par les cellules : la dalle, c'est le nœud, son bombement.
     (Exception au §4.1 : trois tons sur trois viennent de la palette, voir DECISIONS-MONDES.md.) */
  /* ⚑ intégration v33 (Tom) — LA CONSTRUCTION PAR TRANCHES. `_madGen` est la construction d'origine, telle quelle,
     avec trois points où elle peut rendre la main (la grille du champ, le marching squares, le lissage des boucles).
     `_madBuild` la déroule d'un trait (dalles seules, première peinture d'une surface) ; `_madTranches` la déroule
     par tranches, l'ancienne onde restant affichée. */
  function* _madGen(now, x0, y0, x1, y1) {
    var ix = _idx(), P = ix.P, n = P.length, i;
    // v37 (Tom) : « Madrure est l'exception : son APERÇU est presque vide — beaucoup de lignes et quelques nœuds. C'est là
    // qu'elle intrigue ; pleine, elle ne vend pas. » Un aperçu du Studio garde CINQ nœuds (les cinq premières clés) ; l'unité,
    // l'onde et ses bandes ne bougent pas. Sur la Toile, rien ne change : chaque promesse reste un nœud.
    if (n > 5 && P[0].s && P[0].s.apercu) { P = P.slice().sort(function (a, b) { return a.k - b.k; }).slice(0, 5); n = P.length; }
    if (!n) return;
    var sp = _uMonde(ix, U_MAD) * SP_U, band = sp * 0.17;
    var th = typeof cleToile === 'number' ? _lcg(cleToile >>> 0)() * 6.283 : 0.6;
    var ct = Math.cos(th) / band, st = Math.sin(th) / band;
    var KX = new Float64Array(n), KY = new Float64Array(n), KK = new Float64Array(n), KR = new Float64Array(n);
    for (i = 0; i < n; i++) {
      var r0 = _lcg((P[i].k ^ 0x5bd1e995) >>> 0);
      KX[i] = P[i].x; KY[i] = P[i].y;
      KK[i] = 7.5 + r0() * 2;                                  // en unités de band
      var rr = sp * (0.36 + r0() * 0.12);
      // v34 : la bosse d'un nœud ne dépasse pas la moitié de l'écart à son plus proche voisin — sans quoi, à 40 promesses
      // et plus, les bosses s'additionnent en un dôme et l'onde tourne en anneaux concentriques (vu à 48)
      var dn = ix.near(P[i], 1); if (dn.length && dn[0].d * 0.5 < rr) rr = dn[0].d * 0.5;
      KR[i] = 1 / (rr * rr);
    }
    var pas = band * 0.5;
    var aire = (x1 - x0 + 4 * pas) * (y1 - y0 + 4 * pas);
    if (aire / (pas * pas) > 260000) pas = Math.sqrt(aire / 260000);
    var gx0 = Math.floor(x0 / pas) * pas - 2 * pas, gy0 = Math.floor(y0 / pas) * pas - 2 * pas;   // ancrée : même grille pour toute vue
    var nx = Math.ceil((x1 + 2 * pas - gx0) / pas), ny = Math.ceil((y1 + 2 * pas - gy0) / pas), rw = nx + 1;
    var V = new Float64Array(rw * (ny + 1)), vmin = 1e18, vmax = -1e18;
    // portée : au-delà de 6 u un nœud pèse moins de 0,04 band ; fondu doux de 4,5 à 6 u, jamais de saut
    var u6 = sp / SP_U * 6, u45 = u6 * 0.75, R6 = u6 * u6, R45 = u45 * u45, IR = 1 / (R6 - R45);
    var rowI = new Int32Array(n);
    for (var j = 0; j <= ny; j++) {
      var y = gy0 + j * pas, nr = 0;
      for (i = 0; i < n; i++) { var dyr = y - KY[i]; if (dyr * dyr < R6) rowI[nr++] = i; }
      for (var a = 0; a <= nx; a++) {
        var v;
        if (j === 0 || a === 0 || j === ny || a === nx) v = -1e9;     // bord, fixé plus bas sous le premier niveau
        else {
          var x = gx0 + a * pas; v = x * ct + y * st;
          for (var q = 0; q < nr; q++) {
            i = rowI[q];
            var dx = x - KX[i], dy = y - KY[i], d2 = dx * dx + dy * dy;
            if (d2 >= R6) continue;
            var w = 1;
            if (d2 > R45) { var tt = (d2 - R45) * IR; w = 1 - tt * tt * (3 - 2 * tt); }
            v += w * KK[i] / (1 + d2 * KR[i]);
          }
          if (v < vmin) vmin = v; if (v > vmax) vmax = v;
        }
        V[j * rw + a] = v;
      }
      if ((j & 1) === 1) yield;                                   // v33 : une tranche possible toutes les 2 rangées
    }
    // les niveaux : six par période de trois bandes, chacun rattaché à sa couche
    //   0 → filet (sous-couche) · 0,11 → veine · 1 → fin veine · 1,11 → claire · 2 → fin claire · 2,11 → fin sous-couche
    var OFF = [0, 0.11, 1, 1.11, 2, 2.11], CL = [0, 1, 1, 2, 2, 0];
    var lev = [], lay = [];
    for (var pj = Math.floor(vmin / 3) - 1; pj <= Math.floor(vmax / 3) + 1; pj++)
      for (var oi = 0; oi < 6; oi++) { lev.push(3 * pj + OFF[oi]); lay.push(CL[oi]); }
    var NL = lev.length;
    for (a = 0; a <= nx; a++) { V[a] = lev[0] - 0.5; V[ny * rw + a] = lev[0] - 0.5; }
    for (j = 0; j <= ny; j++) { V[j * rw] = lev[0] - 0.5; V[j * rw + nx] = lev[0] - 0.5; }
    var PJ0 = Math.floor(vmin / 3) - 1;
    function premier(val) {                         // index du premier niveau > val, en O(1)
      var p = Math.floor(val / 3), fr = val - 3 * p, c = 0;
      while (c < 6 && OFF[c] <= fr) c++;
      var r = (p - PJ0) * 6 + c;
      return r < 0 ? 0 : r > NL ? NL : r;
    }
    // marching squares sur tableaux typés : chaque croisement (arête, niveau) a un index fixe
    var NE = 2 * rw * (ny + 1);
    var base = new Int32Array(NE + 1), kS = new Int32Array(NE);
    var tot = 0;
    for (j = 0; j <= ny; j++) for (a = 0; a <= nx; a++) {
      var o = j * rw + a, va = V[o];
      for (var d2 = 0; d2 < 2; d2++) {
        var id = o * 2 + d2;
        base[id] = tot;
        if ((d2 === 0 && a === nx) || (d2 === 1 && j === ny)) { kS[id] = 0; continue; }
        var vb = d2 === 0 ? V[o + 1] : V[o + rw];
        var p0 = premier(Math.min(va, vb)), p1 = premier(Math.max(va, vb));
        kS[id] = p0; tot += p1 - p0;
      }
    }
    base[NE] = tot;
    var PX = new Float64Array(tot), PY = new Float64Array(tot), LA = new Int32Array(tot).fill(-1), LB = new Int32Array(tot).fill(-1);
    for (j = 0; j <= ny; j++) for (a = 0; a <= nx; a++) {
      var o2 = j * rw + a, v0 = V[o2], X0 = gx0 + a * pas, Y0 = gy0 + j * pas;
      for (var d3 = 0; d3 < 2; d3++) {
        var id2 = o2 * 2 + d3, cnt = base[id2 + 1] - base[id2]; if (!cnt) continue;
        var v1 = d3 === 0 ? V[o2 + 1] : V[o2 + rw];
        for (var c = 0; c < cnt; c++) {
          var t = (lev[kS[id2] + c] - v0) / (v1 - v0), pi = base[id2] + c;
          if (d3 === 0) { PX[pi] = X0 + pas * t; PY[pi] = Y0; } else { PX[pi] = X0; PY[pi] = Y0 + pas * t; }
        }
      }
    }
    function pt(i2, j2, e2, k) {
      var id3 = e2 === 0 ? (j2 * rw + i2) * 2 : e2 === 2 ? ((j2 + 1) * rw + i2) * 2 : e2 === 3 ? (j2 * rw + i2) * 2 + 1 : (j2 * rw + i2 + 1) * 2 + 1;
      return base[id3] + k - kS[id3];
    }
    var SA = new Int32Array(tot + 8), SB = new Int32Array(tot + 8), SK = new Int32Array(tot + 8), NS = 0;   // chaque croisement a deux segments : NS = tot
    function relier(pa, pb, k) {
      var si = NS++; SA[si] = pa; SB[si] = pb; SK[si] = k;
      if (LA[pa] < 0) LA[pa] = si; else LB[pa] = si;
      if (LA[pb] < 0) LA[pb] = si; else LB[pb] = si;
    }
    var PAIRES = [null, [3, 2], [2, 1], [3, 1], [0, 1], null, [0, 2], [3, 0], [3, 0], [0, 2], null, [0, 1], [3, 1], [2, 1], [3, 2], null];
    for (j = 0; j < ny; j++) { if ((j & 3) === 3) yield; for (a = 0; a < nx; a++) {   // v33 : une tranche toutes les 4 rangées
      var o3 = j * rw + a;
      var v00 = V[o3], v10 = V[o3 + 1], v01 = V[o3 + rw], v11 = V[o3 + rw + 1];
      var lo = Math.min(v00, v10, v01, v11), hi = Math.max(v00, v10, v01, v11);
      var kA = premier(lo), kB = premier(hi);
      for (var k = kA; k < kB; k++) {
        var L = lev[k];
        var cas = (v00 >= L ? 8 : 0) | (v10 >= L ? 4 : 0) | (v11 >= L ? 2 : 0) | (v01 >= L ? 1 : 0);
        if (cas === 0 || cas === 15) continue;
        if (cas === 5 || cas === 10) {
          var centre = (v00 + v10 + v11 + v01) / 4 >= L;
          if ((cas === 5) === centre) { relier(pt(a, j, 3, k), pt(a, j, 0, k), k); relier(pt(a, j, 1, k), pt(a, j, 2, k), k); }
          else { relier(pt(a, j, 0, k), pt(a, j, 1, k), k); relier(pt(a, j, 2, k), pt(a, j, 3, k), k); }
          continue;
        }
        var pr = PAIRES[cas];
        relier(pt(a, j, pr[0], k), pt(a, j, pr[1], k), k);
      }
    } }
    var PAL = _pal();
    var c0 = cOf(P[0].s, now);
    var TONS = PAL ? [PAL[0], PAL[1], PAL[2]] : [_nu(c0, -0.5), c0, _nu(c0, 0.3)];
    // φ en un point : interpolation bicubique (Catmull-Rom) de la grille. Continue et dérivable d'une maille
    // à l'autre, là où le marching squares interpolait linéairement sur les arêtes. Coût fixe, aucun nœud sommé.
    // (la grille garde φ brut ; on lit le bord réel, pas la valeur de fermeture posée sur le cadre)
    var FV = 0, FGX = 0, FGY = 0, wx = [0, 0, 0, 0], wy = [0, 0, 0, 0], dwx = [0, 0, 0, 0], dwy = [0, 0, 0, 0];
    function poids(t, w, dw) {
      var t2 = t * t, t3 = t2 * t;
      w[0] = (-t3 + 2 * t2 - t) / 2; w[1] = (3 * t3 - 5 * t2 + 2) / 2; w[2] = (-3 * t3 + 4 * t2 + t) / 2; w[3] = (t3 - t2) / 2;
      dw[0] = (-3 * t2 + 4 * t - 1) / 2; dw[1] = (9 * t2 - 10 * t) / 2; dw[2] = (-9 * t2 + 8 * t + 1) / 2; dw[3] = (3 * t2 - 2 * t) / 2;
    }
    function champ(x, y) {
      var fx = (x - gx0) / pas, fy = (y - gy0) / pas, ia = Math.floor(fx), ja = Math.floor(fy);
      if (ia < 2) ia = 2; if (ja < 2) ja = 2; if (ia > nx - 3) ia = nx - 3; if (ja > ny - 3) ja = ny - 3;
      poids(fx - ia, wx, dwx); poids(fy - ja, wy, dwy);
      var v = 0, gx = 0, gy = 0;
      for (var jj = 0; jj < 4; jj++) {
        var row = (ja - 1 + jj) * rw + ia - 1, r0 = 0, r1 = 0;
        for (var ii = 0; ii < 4; ii++) { var val = V[row + ii]; r0 += wx[ii] * val; r1 += dwx[ii] * val; }
        v += wy[jj] * r0; gx += wy[jj] * r1; gy += dwy[jj] * r0;
      }
      FV = v; FGX = gx / pas; FGY = gy / pas;
    }
    // recalage : un pas de Newton ramène le point sur φ = L (le marching squares l'avait interpolé linéairement)
    function recaler(arr, k2, L) {
      champ(arr[k2], arr[k2 + 1]);
      var g2 = FGX * FGX + FGY * FGY; if (g2 < 1e-12) return;
      var s = (FV - L) / g2, mx = s * FGX, my = s * FGY, lim = pas * 0.5, ln = Math.sqrt(mx * mx + my * my);
      if (ln > lim) { mx *= lim / ln; my *= lim / ln; }
      arr[k2] -= mx; arr[k2 + 1] -= my;
    }
    var bz = [];
    // boucles rangées par niveau
    var parNiveau = new Array(NL), TOL2 = 0.0625;
    var vu = new Uint8Array(NS), bx = new Float64Array(tot + 4), by = new Float64Array(tot + 4);
    var _nq = 0;
    for (var s0 = 0; s0 < NS; s0++) {
      if (vu[s0]) continue;
      if ((++_nq & 3) === 3) yield;                                 // v33 : une tranche toutes les 4 boucles
      var kk = SK[s0], depart = SA[s0], cur = SB[s0], sc = s0;
      vu[s0] = 1; var m = 0;
      bx[m] = PX[depart]; by[m++] = PY[depart];
      var garde = 0;
      while (cur !== depart && garde++ < 400000) {
        bx[m] = PX[cur]; by[m++] = PY[cur];
        var nxt = LA[cur] === sc ? LB[cur] : LA[cur];
        if (nxt < 0 || vu[nxt]) break;
        vu[nxt] = 1; sc = nxt;
        cur = SA[nxt] === cur ? SB[nxt] : SA[nxt];
      }
      if (m < 3) continue;
      var Lv = lev[kk];
      // 1 · points doubles : on fusionne ceux à moins de 0,15 pas (pic de Bézier dégénérée)
      bz.length = 0;
      for (var z = 0; z < m; z++) {
        var zl = bz.length;
        if (zl && Math.abs(bx[z] - bz[zl - 2]) + Math.abs(by[z] - bz[zl - 1]) < pas * 0.15) continue;
        bz.push(bx[z], by[z]);
      }
      if (bz.length > 4 && Math.abs(bz[0] - bz[bz.length - 2]) + Math.abs(bz[1] - bz[bz.length - 1]) < pas * 0.15) bz.length -= 2;
      if (bz.length < 6) continue;
      // boucle minuscule (plus petite qu'une maille) : le marching squares ne la résout pas, on la laisse tomber
      var bxa = 1e18, bxb = -1e18, bya = 1e18, byb = -1e18;
      for (z = 0; z < bz.length; z += 2) { if (bz[z] < bxa) bxa = bz[z]; if (bz[z] > bxb) bxb = bz[z]; if (bz[z + 1] < bya) bya = bz[z + 1]; if (bz[z + 1] > byb) byb = bz[z + 1]; }
      if (bxb - bxa < pas * 0.9 && byb - bya < pas * 0.9) continue;
      // 2 · recalage de chaque point sur l'iso-ligne exacte
      for (z = 0; z < bz.length; z += 2) recaler(bz, z, Lv);
      // 3 · rééchantillonnage à pas constant (0,8 maille) : les points du marching squares tombent à
      //     intervalles irréguliers, et chaque irrégularité faisait une facette dans la courbe
      var mz = bz.length / 2, lt = 0, cl = [0];
      for (z = 0; z < mz; z++) {
        var zn = ((z + 1) % mz) * 2, ddx = bz[zn] - bz[z * 2], ddy = bz[zn + 1] - bz[z * 2 + 1];
        lt += Math.sqrt(ddx * ddx + ddy * ddy); cl.push(lt);
      }
      var ns = Math.max(64, Math.round(lt / (pas * 0.8))), stp2 = lt / ns, rs = new Float64Array(ns * 2), seg = 0;   // ≥ 64 points : un œil reste rond
      for (z = 0; z < ns; z++) {
        var sd = z * stp2;
        while (seg < mz - 1 && cl[seg + 1] < sd) seg++;
        var s1 = seg * 2, s2 = ((seg + 1) % mz) * 2, sl = cl[seg + 1] - cl[seg], tt2 = sl > 0 ? (sd - cl[seg]) / sl : 0;
        rs[z * 2] = bz[s1] + (bz[s2] - bz[s1]) * tt2; rs[z * 2 + 1] = bz[s1 + 1] + (bz[s2 + 1] - bz[s1 + 1]) * tt2;
      }
      // 4 · lissage de Taubin (λ = 0,5 / μ = −0,53, 6 tours) : filtre les ondulations courtes — facettes,
      //     bruit du recalage, pointes des cols — sans rétrécir la boucle
      var tmp2 = new Float64Array(ns * 2);
      for (var it = 0; it < 12; it++) {
        var lam = (it & 1) ? -0.53 : 0.5;
        for (z = 0; z < ns; z++) {
          var zp2 = ((z - 1 + ns) % ns) * 2, zc2 = z * 2, zq2 = ((z + 1) % ns) * 2;
          tmp2[zc2] = rs[zc2] + lam * ((rs[zp2] + rs[zq2]) / 2 - rs[zc2]);
          tmp2[zc2 + 1] = rs[zc2 + 1] + lam * ((rs[zp2 + 1] + rs[zq2 + 1]) / 2 - rs[zc2 + 1]);
        }
        var sw2 = rs; rs = tmp2; tmp2 = sw2;
      }
      // 5 · chaque point est reposé sur la ligne de niveau exacte (champ bicubique, lisse) : la courbe
      //     finale suit le champ, pas la grille — plus de bosse, même sur un œil de quelques pixels
      for (z = 0; z < ns * 2; z += 2) recaler(rs, z, Lv);
      var out = parNiveau[kk]; if (!out) out = parNiveau[kk] = [];
      out.push(ns);
      for (z = 0; z < ns * 2; z++) out.push(rs[z]);
    }
    function tracer(T, list) {
      if (!list) return;
      for (var q = 0; q < list.length;) {
        var np = list[q], b0 = q + 1;
        // Catmull-Rom → Bézier cubiques : la courbe PASSE par chaque point du marching squares
        // (rien ne rétrécit, même les petites boucles) et sa tangente est continue partout
        // tangente en P_i = (P_i+1 − P_i−1) / (d_i−1 + d_i) : la courbe passe par chaque point,
        // tangente continue, et un segment court à côté d'un long ne fait pas de boucle
        T.moveTo(list[b0], list[b0 + 1]);
        var tx0 = 0, ty0 = 0;
        for (var z = 0; z <= np; z++) {
          var i0 = b0 + ((z - 1 + np) % np) * 2, i1 = b0 + (z % np) * 2, i2 = b0 + ((z + 1) % np) * 2;
          var da = Math.sqrt((list[i1] - list[i0]) * (list[i1] - list[i0]) + (list[i1 + 1] - list[i0 + 1]) * (list[i1 + 1] - list[i0 + 1]));
          var db = Math.sqrt((list[i2] - list[i1]) * (list[i2] - list[i1]) + (list[i2 + 1] - list[i1 + 1]) * (list[i2 + 1] - list[i1 + 1]));
          var sd = da + db || 1, mx = (list[i2] - list[i0]) / sd, my = (list[i2 + 1] - list[i0 + 1]) / sd;
          if (z > 0) {
            var ip = b0 + ((z - 1) % np) * 2, dp = da / 3;
            T.bezierCurveTo(list[ip] + tx0 * dp, list[ip + 1] + ty0 * dp, list[i1] - mx * dp, list[i1 + 1] - my * dp, list[i1], list[i1 + 1]);
          }
          tx0 = mx; ty0 = my;
        }
        T.closePath(); q += 1 + np * 2;
      }
    }
    // une bande [A, B) = les boucles de A et de B, remplies en pair-impair ; une bande, un remplissage
    var P2 = [new Path2D(), new Path2D(), new Path2D()];
    for (var k0 = 0; k0 < NL; k0++) { tracer(P2[lay[k0]], parNiveau[k0]); if ((k0 & 3) === 3) yield; }   // v33 : les chemins aussi, par paquets
    // le champ lui-même, pour les nœuds qui ne ferment pas de boucle (voir _carnet)
    function phi(x, y, sauf) {
      var v = x * ct + y * st;
      for (var ii = 0; ii < n; ii++) {
        if (ii === sauf) continue;
        var dx = x - KX[ii], dy = y - KY[ii], d2 = dx * dx + dy * dy;
        if (d2 >= R6) continue;
        var w = 1;
        if (d2 > R45) { var tt = (d2 - R45) * IR; w = 1 - tt * tt * (3 - 2 * tt); }
        v += w * KK[ii] / (1 + d2 * KR[ii]);
      }
      return v;
    }
    return { paths: P2, tons: TONS, boucles: parNiveau, P: P, u: sp / SP_U, phi: phi, tracer: tracer, pas: pas, lev: lev };
  }
  var _madBuild = _auRepos(function (now, x0, y0, x1, y1) { var it = _madGen(now, x0, y0, x1, y1), r; do { r = it.next(); } while (!r.done); return r.value; });

  // Le tracé de Madrure est gardé d'une image à l'autre : l'onde ne change qu'avec le semis.
  // Seule la GÉOMÉTRIE est gardée ; elle tombe à tout changement de semis (position, poids, clé — donc à la
  // plantation, une fois), de clé de Toile, et dès que la vue sort de la zone calculée.
  // Les couleurs ne sont jamais gardées : relues à chaque image, un changement de palette ou de thème est immédiat.
  // Seule la vue (plus 12 % de marge) est calculée et lissée.
  var _madCaches = [];
  function _madSig() {
    var h = 0x811c9dc5;
    function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(seeds.length);
    for (var i = 0; i < seeds.length; i++) {
      var s = seeds[i];
      mix(Math.round(s.x * 2)); mix(Math.round(s.y * 2));            // position de repos, au demi-pixel (v32 : au 1/16 le relâchement du moteur la changeait encore ~12 images)
      mix(Math.round((s.w || 0) * 2)); mix(_cle(s));
    }
    mix(typeof cleToile === 'number' ? cleToile : 0);
    return h >>> 0;
  }
  /* ⚑ intégration v32 (mesuré dans l'app) : à la plantation le moteur fait GRANDIR la dalle et relâche toute la Toile
     pendant ~1 s — poids et positions de repos bougent à CHAQUE image, donc la signature aussi. Reconstruire à chaque
     image, c'était une construction par image pendant toute la croissance. Règle : tant que le semis d'une surface
     BOUGE (sa signature a changé depuis l'image précédente), on repeint la dernière onde de cette surface ; on
     reconstruit dès qu'il est posé (même signature deux images de suite) — le moteur est relancé pour le voir.
     Et un cache par semis (quatre au plus) : la Toile et les aperçus du Studio ne se chassent plus l'un l'autre. */
  function Rmad(now, x0, y0, x1, y1) {
    _sync();
    var sig = _madSig(), C = null, i, cv = g && g.canvas;
    for (i = 0; i < _madCaches.length; i++) if (_madCaches[i].sig === sig) { C = _madCaches[i]; break; }
    var dans = function (Z) { return Z && !(x0 < Z.x0 || y0 < Z.y0 || x1 > Z.x1 || y1 > Z.y1); };
    if (!dans(C)) {
      var der = cv && cv.__madC;
      if (der && dans(der) && der.r) {
        C = der;                                                   // l'onde d'avant reste affichée
        if (cv.__madVu === sig) _madTranches(cv, sig, now, x0, y0, x1, y1);   // v33 : posé → on construit PAR TRANCHES
        else if (cv.__madJob) cv.__madJob = null;                  // il bouge encore : une construction en route est périmée
        if (typeof env.relance === 'function') env.relance();
      } else {
        var mw = (x1 - x0) * 0.12, mh = (y1 - y0) * 0.12;
        var t0 = (typeof performance !== 'undefined') ? performance.now() : 0;
        C = { sig: sig, x0: x0 - mw, y0: y0 - mh, x1: x1 + mw, y1: y1 + mh, r: _madBuild(now, x0 - mw, y0 - mh, x1 + mw, y1 + mh) };
        Rmad.derniere = { ms: ((typeof performance !== 'undefined') ? performance.now() : 0) - t0, n: seeds.length };
        Rmad.constructions = (Rmad.constructions || 0) + 1;
        for (i = 0; i < _madCaches.length; i++) if (_madCaches[i].sig === sig) { _madCaches.splice(i, 1); break; }
        _madCaches.unshift(C); if (_madCaches.length > 4) _madCaches.length = 4;
      }
    }
    if (cv) { var tn = _maint(); if (cv.__madT) cv.__madDt = tn - cv.__madT; cv.__madT = tn; cv.__madVu = sig; cv.__madC = C; }
    if (!C.r) return;
    // couleurs relues à chaque image : palette et thème ne peuvent jamais rester dans l'ancienne teinte
    var TN = _madTons(now);
    for (var c = 0; c < 3; c++) { g.fillStyle = _rgb(TN[c]); g.fill(C.r.paths[c], 'evenodd'); }
    if (_ingenu() && C.sig === sig) _madYeux(now);
  }
  /* ⚑ intégration v34 (Tom, Q315) — MADRURE SOUS INGÉNU. Ingénu dit : bleu = Promi, rose = Chiche, lilas = Nuée, et le
     crème dalle peint ce qui ne porte aucune parole. v35 (Tom, qui corrige v34) : l'onde GARDE les couleurs de la palette,
     comme sous toute palette ; seule la dalle de chaque promesse (son œil, sa strate fermée, son cercle) se repeint dans SA
     couleur de nature. */
  function _madTons(now) {
    var PL = _pal(), c0 = cOf(seeds[0], now);
    // v35 (Tom) : sous Ingénu aussi l'onde porte les couleurs de la palette ; ce sont les DALLES qui prennent leur nature
    return PL ? [PL[0], PL[1], PL[2]] : [_nu(c0, -0.5), c0, _nu(c0, 0.3)];
  }
  function _madNature(n) { return [_nu(n, -0.45), n, _nu(n, 0.25)]; }
  // les dalles des promesses, sur l'onde : calculées au plus 8 ms par image (une zone par nœud), gardées au carnet
  var _madYeux = function (now) {
    var o = _repos; _repos = true;
    try {
      var C = _carnet('madrure', now), t0 = _maint(), manque = false;
      for (var i = 0; i < seeds.length; i++) {
        var s = seeds[i]; if (!_promesse(s)) continue;
        if (!Object.prototype.hasOwnProperty.call(C.notes, _cle(s)) && _maint() - t0 > 8) { manque = true; continue; }
        var N = _madDalle(C, s, now); if (!N || !N.pts) continue;
        var a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18;
        for (var z = 0; z < N.pts.length; z++) { var X = N.pts[z][0], Y = N.pts[z][1]; if (X < a0) a0 = X; if (X > a1) a1 = X; if (Y < b0) b0 = Y; if (Y > b1) b1 = Y; }
        _tonsForces = _madNature(cOf(s, now));
        try { seule('madrure', s, now, (a0 + a1) / 2, (b0 + b1) / 2, Math.max(a1 - a0, b1 - b0)); } finally { _tonsForces = null; }
      }
      if (manque && typeof env.relance === 'function') env.relance();
    } finally { _repos = o; }
  };
  function _maint() { return (typeof performance !== 'undefined') ? performance.now() : Date.now(); }
  /* ⚑ v33 — une tranche vaut la MOITIÉ de l'image qu'on vient de peindre (bornée à 12–150 ms) : sur un appareil lent
     chaque image est déjà longue, des tranches courtes y multiplieraient les images (une tranche passe entre deux
     images). La première tranche part tout de suite, dans le contexte de la surface (`_idx` y lit ses graines) ;
     les suivantes, hors du dessin (`setTimeout`). Une construction dont le semis a rebougé est abandonnée. */
  function _madTranches(cv, sig, now, x0, y0, x1, y1) {
    var J = cv.__madJob;
    if (J && J.sig === sig) return;
    var mw = (x1 - x0) * 0.12, mh = (y1 - y0) * 0.12;
    var Z = { sig: sig, x0: x0 - mw, y0: y0 - mh, x1: x1 + mw, y1: y1 + mh, r: null };
    J = cv.__madJob = { sig: sig, it: _madGen(now, Z.x0, Z.y0, Z.x1, Z.y1), ms: 0, n: 0, t0: _maint() };
    function tranche() {
      if (cv.__madJob !== J) return false;
      var budget = Math.max(12, Math.min(150, (cv.__madDt || 32) * 0.5)), t0 = _maint(), r, o = _repos;
      _repos = true;
      try { do { r = J.it.next(); } while (!r.done && _maint() - t0 < budget); }
      catch (e) { cv.__madJob = null; return false; }
      finally { _repos = o; }
      J.ms += _maint() - t0; J.n++;
      if (!r.done) return true;
      cv.__madJob = null; Z.r = r.value;
      Rmad.derniere = { ms: J.ms, n: seeds.length, tranches: J.n, attente: _maint() - J.t0 };
      Rmad.constructions = (Rmad.constructions || 0) + 1;
      for (var i = 0; i < _madCaches.length; i++) if (_madCaches[i].sig === sig) { _madCaches.splice(i, 1); break; }
      _madCaches.unshift(Z); if (_madCaches.length > 4) _madCaches.length = 4;
      if (typeof env.relance === 'function') env.relance();
      return false;
    }
    function suite() { if (tranche()) setTimeout(suite, 0); }
    if (tranche()) setTimeout(suite, 0);
  }
  Rmad.invalider = function () { _madCaches = []; };
  /* ⚑ intégration v33 (Tom) — CE QUE MADRURE A PEINT en (x, y), sur la surface qui vient d'être peinte : l'encre d'un
     libellé se choisit sur ce qui est DESSOUS, pas sur la couleur de la cellule — ici elles n'ont rien à voir (l'onde
     porte la palette brute, et laisse voir le fond entre les veines). Même classement que le dessin : la période de
     trois bandes, filet [0 ; 0,11) [1 ; 1,11) [2 ; 2,11) · veine [0,11 ; 1) · veine claire [1,11 ; 2) · fond [2,11 ; 3). */
  Rmad.sous = function (x, y) {
    _sync();
    var cv = g && g.canvas, C = cv && cv.__madC; if (!C || !C.r || !C.r.phi) return null;
    var PL = _madTons(0);
    var v = C.r.phi(x, y, -1), fr = v - 3 * Math.floor(v / 3);
    if (fr < 0.11 || (fr >= 1 && fr < 1.11) || (fr >= 2 && fr < 2.11)) return PL[0];
    if (fr < 1) return PL[1];
    if (fr < 2) return PL[2];
    return typeof fondToile === 'function' ? _arr(fondToile()) : null;
  };

  /* ================= DALLE SEULE & CONTOUR PEINT (mondes LIBRES) =================
     La matière d'un monde libre naît de toute la Toile : on la calcule sur toute la Toile (contexte
     muet, rien n'est peint), on note ce qui appartient à chaque promesse, puis on ne peint QUE cela.
     Une dalle seule est donc exactement celle de la Toile — même géométrie, même grain, mêmes tons —
     engendrée en vecteurs à sa taille finale, posée sur rien. Jamais un rognage d'image, jamais un cadre.
       seule(nom, s, now, cx, cy, taille)  peint la dalle de la graine s, centrée en (cx, cy), taille = son plus grand côté
       contour(nom, s)                      le contour réellement peint, [[x, y], …] en coordonnées Toile
       toucher(nom, x, y)                   la graine dont la dalle PEINTE contient (x, y), ou null (le moteur retombe sur cAt)
     Carnet gardé tant que semis, clé de Toile, palette, thème et couleurs des cellules ne changent pas. */
  var _carnets = {};
  function _sigCarnet() {
    var h = _madSig();
    function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    var pl = typeof curPAL === 'function' ? curPAL() : null;
    mix(_fnv(JSON.stringify(pl || ''))); mix(isLightM && isLightM() ? 1 : 2);
    for (var i = 0; i < seeds.length; i++) { var c = cOf(seeds[i], 0); mix((c[0] << 16) ^ (c[1] << 8) ^ c[2]); }
    return h >>> 0;
  }
  function _bornes() {
    var a = 1e18, b = 1e18, c = -1e18, d = -1e18;
    for (var i = 0; i < seeds.length; i++) { var s = seeds[i]; if (s.x < a) a = s.x; if (s.y < b) b = s.y; if (s.x > c) c = s.x; if (s.y > d) d = s.y; }
    var m = Math.sqrt(Math.max(1, (c - a) * (d - b)) / Math.max(1, seeds.length));
    return [a - m, b - m, c + m, d + m];
  }
  function _pip(x, y, pts) {
    var ins = false, n = pts.length;
    for (var i = 0, j = n - 1; i < n; j = i++) {
      var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins;
    }
    return ins;
  }
  function _carnet(nom, now) {
    _sync();
    var sig = _sigCarnet(), C = _carnets[nom];
    if (C && C.sig === sig) return C;
    var B = _bornes(), notes = {}, formes = {}, derivees = {};
    if (nom === 'madrure') {
      // dalles calculées à la demande, nœud par nœud (_madDalle)
    } else {
      _enreg = true; _rec = notes;
      try { (nom === 'esquille' ? Resq : Rbob)(now, B[0], B[1], B[2], B[3]); }
      finally { _enreg = false; _rec = null; _sync(); }
      for (var key in notes) {
        var it = notes[key];
        if (nom === 'esquille') { var tous = []; for (var z1 = 0; z1 < it.length; z1++) tous = tous.concat(it[z1].poly); formes[key] = tous; }   // v34 : tous ses éclats
        else {
          // la bobine : le disque extérieur de l'anneau épaissi (les boucles de fil se touchent aussi)
          var ring = null;
          for (var z2 = 0; z2 < it.length; z2++) if (it[z2].dalle) { ring = it[z2]; break; }
          var ref = ring || it[0], R0 = ref.r + ref.w / 2, pc = [];
          for (var z3 = 0; z3 < 32; z3++) { var an = z3 / 32 * 6.2832; pc.push([ref.A[0] + Math.cos(an) * R0, ref.A[1] + Math.sin(an) * R0]); }
          formes[key] = pc;
        }
      }
    }
    return (_carnets[nom] = { sig: sig, notes: notes, formes: formes, derivees: derivees });
  }
  function _rayonNoeud(c, k, r) { return function (L) { var q = L - c; if (q >= k) return 0; if (q <= 0) return Infinity; return r * Math.sqrt(k / q - 1); }; }
  /* Madrure : la dalle d'une promesse est l'ŒIL de son nœud, tel qu'il paraît sur la Toile —
     la plus grande ligne de niveau fermée qui n'entoure que lui et qui est le bord EXTÉRIEUR d'un filet
     (la dalle finit sur son liseré noir). Dedans, la matière exacte de la Toile : mêmes lignes, mêmes tons.
     On ne calcule que la zone du nœud (grille ancrée : mêmes lignes que sur la Toile). Un nœud dont les
     lignes ne se referment pas sur lui (il ne fait que plier les veines) n'a pas d'œil : pas de dalle seule. */
  function _madDalle(C, s, now) {
    var k = _cle(s);
    if (Object.prototype.hasOwnProperty.call(C.notes, k)) return C.notes[k];
    var ix = _idx(), P = ix.P, p = null, i;
    for (i = 0; i < P.length; i++) if (P[i].k === k) { p = P[i]; break; }
    if (!p || !_promesse(p.s)) return (C.notes[k] = null);
    var u = _uMonde(ix, U_MAD), Z = u * 1.6;                   // 1,6 u suffit : mêmes yeux qu'à 2,6 u sur trois semis
    var r = _madBuild(now, p.x - Z, p.y - Z, p.x + Z, p.y + Z);
    if (!r) return (C.notes[k] = null);
    var marge = r.pas * 2, B = [];
    // toutes les boucles fermées de la zone, bords extérieurs des filets (niveaux 3j, 3j+1, 3j+2)
    for (var kk = 0; kk < r.boucles.length; kk += 2) {
      var list = r.boucles[kk]; if (!list) continue;
      for (var q = 0; q < list.length;) {
        var np = list[q], pts = [], a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18, ar = 0, z;
        for (z = 0; z < np; z++) {
          var X = list[q + 1 + z * 2], Y = list[q + 2 + z * 2]; pts.push([X, Y]);
          if (X < a0) a0 = X; if (X > a1) a1 = X; if (Y < b0) b0 = Y; if (Y > b1) b1 = Y;
        }
        var flat = list.slice(q, q + 1 + np * 2);
        q += 1 + np * 2;
        if (a0 < p.x - Z + marge || a1 > p.x + Z - marge || b0 < p.y - Z + marge || b1 > p.y + Z - marge) continue;   // touche la zone : trop grand
        for (z = 0; z < np; z++) { var Pa = pts[z], Pb = pts[(z + 1) % np]; ar += Pa[0] * Pb[1] - Pb[0] * Pa[1]; }
        B.push({ pts: pts, flat: flat, aire: Math.abs(ar) / 2, L: r.lev[kk], a0: a0, b0: b0, a1: a1, b1: b1, autour: p.x >= a0 && p.x <= a1 && p.y >= b0 && p.y <= b1 && _pip(p.x, p.y, pts) });
      }
    }
    var autres = function (lp) {
      for (var ii = 0; ii < P.length; ii++) {
        var o = P[ii]; if (o === p || o.x < lp.a0 || o.x > lp.a1 || o.y < lp.b0 || o.y > lp.b1) continue;
        if (_pip(o.x, o.y, lp.pts)) return true;
      }
      return false;
    };
    // 1 · l'œil strict : la plus grande boucle qui n'entoure que ce nœud
    var best = null;
    for (var t = 0; t < B.length; t++) { var lp = B[t]; if (!lp.autour || (best && lp.aire <= best.aire)) continue; if (!autres(lp)) best = lp; }
    // 2 · une ou deux strates de plus, parfois (tirées de la clé), quand elles restent serrées autour de l'œil :
    //     la boucle peut enjamber un nœud sans œil, jamais un autre œil ; jamais plus de 2,4 fois l'aire de l'œil
    if (best) {
      var voulu = [0, 1, 1, 2][(k >>> 5) % 4];
      var unPic = function (lp) {                       // aucune boucle plus haute, dedans, qui n'entoure pas ce nœud
        for (var t2 = 0; t2 < B.length; t2++) {
          var d2 = B[t2]; if (d2.L <= lp.L || d2.autour) continue;
          if (d2.a0 < lp.a0 || d2.a1 > lp.a1 || d2.b0 < lp.b0 || d2.b1 > lp.b1) continue;
          if (_pip(d2.pts[0][0], d2.pts[0][1], lp.pts)) return false;
        }
        return true;
      };
      for (var e = voulu; e >= 1; e--) {
        var cible = best.L - e, trouve = null;
        for (t = 0; t < B.length; t++) {
          var c2 = B[t];
          if (!c2.autour || Math.abs(c2.L - cible) > 1e-6 || c2.aire > best.aire * 2.4) continue;
          if (unPic(c2)) { trouve = c2; break; }
        }
        if (trouve) { best = trouve; break; }
      }
    }
    if (best) {
      C.formes[k] = best.pts;
      return (C.notes[k] = { r: r, flat: best.flat, pts: best.pts, nature: 'oeil' });
    }
    // Pas d'œil : les lignes enveloppent le nœud mais repartent avec l'onde. On prend la strate la plus
    // lointaine qui l'enveloppe sur au moins 85 % de son tour (rayon continu d'une direction à l'autre),
    // et on ferme le reste par une courbe douce (Hermite sur le rayon, tangentes prises aux deux bouts).
    var NA = 144, RM = u * 1.3, NS = 40, dr = RM / NS, v0 = r.phi(p.x, p.y, -1);
    // la strate fermée peut enjamber un nœud sans œil, jamais un nœud qui a son œil
    var enfermeUnOeil = function (pts, a0, b0, a1, b1) {
      for (var ii = 0; ii < P.length; ii++) {
        var o = P[ii]; if (o === p || o.x < a0 || o.x > a1 || o.y < b0 || o.y > b1 || !_pip(o.x, o.y, pts)) continue;
        for (var t4 = 0; t4 < B.length; t4++) {
          var lo4 = B[t4]; if (lo4.autour || o.x < lo4.a0 || o.x > lo4.a1 || o.y < lo4.b0 || o.y > lo4.b1 || !_pip(o.x, o.y, lo4.pts)) continue;
          var seulO = true;
          for (var jj = 0; jj < P.length && seulO; jj++) { var o2 = P[jj]; if (o2 !== o && o2.x >= lo4.a0 && o2.x <= lo4.a1 && o2.y >= lo4.b0 && o2.y <= lo4.b1 && _pip(o2.x, o2.y, lo4.pts)) seulO = false; }
          if (seulO) return true;
        }
      }
      return false;
    };
    var ray = new Float64Array(NA * (NS + 1)), csA = new Float64Array(NA), snA = new Float64Array(NA);
    for (var a = 0; a < NA; a++) {
      csA[a] = Math.cos(a / NA * 6.283185307179586); snA[a] = Math.sin(a / NA * 6.283185307179586);
      for (var sI = 0; sI <= NS; sI++) ray[a * (NS + 1) + sI] = sI ? r.phi(p.x + csA[a] * sI * dr, p.y + snA[a] * sI * dr, -1) : v0;
    }
    var choix = null;
    for (var jL = Math.floor(v0 / 3); jL > Math.floor(v0 / 3) - 5 && !choix; jL--) {
      for (var oL = 2; oL >= 0; oL--) {
        var L = 3 * jL + oL; if (L >= v0) continue;
        var rr = new Float64Array(NA), ok = new Uint8Array(NA);
        for (a = 0; a < NA; a++) {
          var base = a * (NS + 1);
          for (sI = 1; sI <= NS; sI++) if (ray[base + sI] < L) {
            // croisement exact par dichotomie entre les deux échantillons
            var lo = (sI - 1) * dr, hi = sI * dr;
            for (var bi = 0; bi < 10; bi++) { var md = (lo + hi) / 2; if (r.phi(p.x + csA[a] * md, p.y + snA[a] * md, -1) < L) hi = md; else lo = md; }
            rr[a] = (lo + hi) / 2; ok[a] = 1; break;
          }
        }
        // plus longue suite continue de directions valides (cyclique)
        var bestRun = 0, bestStart = 0;
        for (var st = 0; st < NA; st++) {
          if (!ok[st] || (ok[(st - 1 + NA) % NA] && Math.abs(rr[st] - rr[(st - 1 + NA) % NA]) < u * 0.12)) continue;
          var len = 1;
          while (len < NA) { var c1 = (st + len) % NA, c0 = (st + len - 1) % NA; if (!ok[c1] || Math.abs(rr[c1] - rr[c0]) >= u * 0.12) break; len++; }
          if (len > bestRun) { bestRun = len; bestStart = st; }
        }
        if (bestRun === 0) { var all = true; for (a = 0; a < NA; a++) if (!ok[a]) all = false; if (all) { bestRun = NA; bestStart = 0; } }
        if (bestRun < NA * SEUIL_STRATE) continue;
        // fermeture : Hermite sur le trou, tangentes des deux bords
        var R2 = new Float64Array(NA), gapN = NA - bestRun;
        for (a = 0; a < bestRun; a++) R2[(bestStart + a) % NA] = rr[(bestStart + a) % NA];
        if (gapN > 0) {
          var iA = (bestStart + bestRun - 1) % NA, iB = bestStart, iA0 = (iA - 1 + NA) % NA, iB1 = (iB + 1) % NA;
          var rA = rr[iA], rB = rr[iB], mA = rr[iA] - rr[iA0], mB = rr[iB1] - rr[iB], T = gapN + 1;
          for (var gI = 1; gI <= gapN; gI++) {
            var t = gI / T, t2 = t * t, t3 = t2 * t;
            R2[(iA + gI) % NA] = (2 * t3 - 3 * t2 + 1) * rA + (t3 - 2 * t2 + t) * mA * T + (-2 * t3 + 3 * t2) * rB + (t3 - t2) * mB * T;
          }
        }
        var pts = [], flat = [NA];
        for (a = 0; a < NA; a++) { var X2 = p.x + csA[a] * R2[a], Y2 = p.y + snA[a] * R2[a]; pts.push([X2, Y2]); flat.push(X2, Y2); }
        var a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18;
        for (a = 0; a < NA; a++) { a0 = Math.min(a0, pts[a][0]); a1 = Math.max(a1, pts[a][0]); b0 = Math.min(b0, pts[a][1]); b1 = Math.max(b1, pts[a][1]); }
        if (enfermeUnOeil(pts, a0, b0, a1, b1)) continue;
        // épaisseur du filet aux deux bords du trou : distance entre φ = L et φ = L + 0,11 le long du rayon
        var epais = 0, nEp = 0;
        if (gapN > 0) for (var eb = 0; eb < 2; eb++) {
          var ia = eb ? iB : iA, lo5 = 0, hi5 = rr[ia];
          for (var b5 = 0; b5 < 12; b5++) { var m5 = (lo5 + hi5) / 2; if (r.phi(p.x + csA[ia] * m5, p.y + snA[ia] * m5, -1) < L + 0.11) hi5 = m5; else lo5 = m5; }
          var w5 = rr[ia] - (lo5 + hi5) / 2; if (w5 > 0) { epais += w5; nEp++; }
        }
        choix = { pts: pts, flat: flat, couverture: bestRun / NA, trou: gapN > 0 ? [iA, gapN] : null, filet: nEp ? epais / nEp : u * 0.03 };
        break;
      }
    }
    if (choix) {
      C.formes[k] = choix.pts;
      return (C.notes[k] = { r: r, flat: choix.flat, pts: choix.pts, nature: 'fermee', couverture: choix.couverture, trou: choix.trou, filet: choix.filet });
    }
    // Dernier recours : le bombement du nœud, dans la COURBURE réelle du champ. On retire seulement la pente
    // des autres nœuds (leur gradient au nœud) : il reste le bombement et la courbure du voisinage, qui
    // déforment les anneaux comme le bois. Jamais pour un nœud qui a un œil.
    var ip = -1; for (i = 0; i < r.P.length; i++) if (r.P[i].k === k) { ip = i; break; }
    if (ip < 0) return (C.notes[k] = null);
    var hg = u * 0.01;
    var gxr = (r.phi(p.x + hg, p.y, ip) - r.phi(p.x - hg, p.y, ip)) / (2 * hg), gyr = (r.phi(p.x, p.y + hg, ip) - r.phi(p.x, p.y - hg, ip)) / (2 * hg);
    var psi = function (x, y) { return r.phi(x, y, -1) - gxr * (x - p.x) - gyr * (y - p.y); };
    var NC = 144, RC = u * 0.6, NSc = 30, drc = RC / NSc, vc0 = psi(p.x, p.y);
    var cC = new Float64Array(NC), sC = new Float64Array(NC), rayC = new Float64Array(NC * (NSc + 1));
    for (var ac = 0; ac < NC; ac++) {
      cC[ac] = Math.cos(ac / NC * 6.283185307179586); sC[ac] = Math.sin(ac / NC * 6.283185307179586);
      for (var sc = 0; sc <= NSc; sc++) rayC[ac * (NSc + 1) + sc] = sc ? psi(p.x + cC[ac] * sc * drc, p.y + sC[ac] * sc * drc) : vc0;
    }
    var anneau = function (L) {                          // ψ = L, rayon par direction ; null si l'anneau ne se ferme pas
      var pts = [], rmax = 0;
      for (var a3 = 0; a3 < NC; a3++) {
        var b3 = a3 * (NSc + 1), found = -1;
        for (var s3 = 1; s3 <= NSc; s3++) if (rayC[b3 + s3] < L) { found = s3; break; }
        if (found < 0) return null;
        var lo3 = (found - 1) * drc, hi3 = found * drc;
        for (var t3 = 0; t3 < 9; t3++) { var m3 = (lo3 + hi3) / 2; if (psi(p.x + cC[a3] * m3, p.y + sC[a3] * m3) < L) hi3 = m3; else lo3 = m3; }
        var rr3 = (lo3 + hi3) / 2; if (rr3 > rmax) rmax = rr3;
        pts.push([p.x + cC[a3] * rr3, p.y + sC[a3] * rr3]);
      }
      return { pts: pts, rmax: rmax };
    };
    // bord : le bord extérieur de filet le plus lointain dont l'anneau se ferme et reste sous 0,5 u
    var Ledge = null, bord = null;
    for (var Lc = Math.floor(vc0 - 0.12); Lc > vc0 - 12; Lc--) { var an0 = anneau(Lc); if (!an0 || an0.rmax > u * 0.5) break; Ledge = Lc; bord = an0; }
    if (Ledge === null) return (C.notes[k] = null);
    var OFF6 = [0, 0.11, 1, 1.11, 2, 2.11], niveaux = [];
    for (var jn = Math.floor(Ledge / 3); 3 * jn < vc0; jn++) for (var on = 0; on < 6; on++) {
      var Ln = 3 * jn + OFF6[on]; if (Ln < Ledge || Ln >= vc0) continue;
      var an1 = Ln === Ledge ? bord : anneau(Ln); if (an1) niveaux.push({ L: Ln, pts: an1.pts });
    }
    C.formes[k] = bord.pts;
    return (C.notes[k] = { nature: 'cercle', pts: bord.pts, niveaux: niveaux, top: vc0 });
  }
  function _rayonNoeud(c, k, r) { return function (L) { var q = L - c; if (q >= k) return 0; if (q <= 0) return Infinity; return r * Math.sqrt(k / q - 1); }; }
  function _cleDe(s) { for (var i = 0; i < seeds.length; i++) if (seeds[i] === s) return _cle(s); return _cle(s); }
  function nature(nom, s) { if (nom !== 'madrure') return contour(nom, s) ? 'dalle' : null; var N = _madDalle(_carnet(nom, 0), s, 0); return N ? N.nature : null; }
  function contour(nom, s) {
    var C = _carnet(nom, 0);
    if (nom === 'madrure') { var N = _madDalle(C, s, 0); return N ? N.pts : null; }
    return C.formes[_cleDe(s)] || null;
  }
  function toucher(nom, x, y) {
    var C = _carnet(nom, 0), meilleur = null, dMeilleur = 1e18;
    if (nom === 'madrure') {
      // on n'examine que les nœuds proches, du plus proche au plus lointain
      var ixt = _idx(), ut = _uMonde(ixt, U_MAD), cand = [];
      for (var it = 0; it < ixt.P.length; it++) { var pt = ixt.P[it], dd = (pt.x - x) * (pt.x - x) + (pt.y - y) * (pt.y - y); if (dd < ut * ut * 2.6 * 2.6) cand.push([dd, pt.s]); }
      cand.sort(function (a2, b2) { return a2[0] - b2[0]; });
      for (it = 0; it < cand.length; it++) { var Nt = _madDalle(C, cand[it][1], 0); if (Nt && _pip(x, y, Nt.pts)) return cand[it][1]; }
      return null;
    }
    for (var i = 0; i < seeds.length; i++) {
      var s = seeds[i], F = C.formes[_cle(s)]; if (!F) continue;

      if (nom === 'esquille') {                                   // v34 : chaque éclat de la promesse
        var ie = C.notes[_cle(s)] || [];
        for (var ze = 0; ze < ie.length; ze++) if (_pip(x, y, ie[ze].poly)) return s;
        continue;
      }
      if (nom === 'bobinette') {
        // disques : l'anneau et les boucles de fil de la promesse
        var it = C.notes[_cle(s)] || [];
        for (var z = 0; z < it.length; z++) { var dx = x - it[z].A[0], dy = y - it[z].A[1], R0 = it[z].r + it[z].w / 2; if (dx * dx + dy * dy <= R0 * R0) return s; }
        continue;
      }
      if (_pip(x, y, F)) return s;
    }
    return meilleur;
  }
  /* ⚑ intégration v32 — LA BOÎTE RÉELLEMENT PEINTE, en coordonnées Toile : [x0, y0, x1, y1].
     `seule` cale la dalle sur la boîte du CONTOUR ; mais les boucles de fil de Bobinette sortent du disque de la
     bobine, et le liseré d'une strate fermée de Madrure déborde de sa courbe. Le moteur dimensionne le canevas
     de la dalle sur cette boîte-ci — sinon ce qui dépasse est coupé net au bord. */
  function boite(nom, s) {
    var C = _carnet(nom, 0), k = _cleDe(s), F, a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18, i, e = 0;
    if (nom === 'madrure') { var N = _madDalle(C, s, 0); if (!N) return null; F = N.pts; e = N.filet || 0; }
    else F = C.formes[k];
    if (!F) return null;
    for (i = 0; i < F.length; i++) { var X = F[i][0], Y = F[i][1]; if (X < a0) a0 = X; if (X > a1) a1 = X; if (Y < b0) b0 = Y; if (Y > b1) b1 = Y; }
    if (nom === 'bobinette') {
      var arcs = C.notes[k] || [];
      for (i = 0; i < arcs.length; i++) { var q = arcs[i], R = q.r + q.w / 2 + q.e;
        if (q.A[0] - R < a0) a0 = q.A[0] - R; if (q.A[0] + R > a1) a1 = q.A[0] + R; if (q.A[1] - R < b0) b0 = q.A[1] - R; if (q.A[1] + R > b1) b1 = q.A[1] + R; }
    }
    return { x0: a0 - e, y0: b0 - e, x1: a1 + e, y1: b1 + e,
             fx0: F.reduce(function (m, v) { return Math.min(m, v[0]); }, 1e18), fy0: F.reduce(function (m, v) { return Math.min(m, v[1]); }, 1e18),
             fx1: F.reduce(function (m, v) { return Math.max(m, v[0]); }, -1e18), fy1: F.reduce(function (m, v) { return Math.max(m, v[1]); }, -1e18) };
  }
  function seule(nom, s, now, cx, cy, taille) {
    var C = _carnet(nom, now), k = _cleDe(s);
    if (nom === 'madrure' && !_madDalle(C, s, now)) return false;
    var F = C.formes[k];
    if (!F) return false;
    var a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18, i;
    for (i = 0; i < F.length; i++) { var X = F[i][0], Y = F[i][1]; if (X < a0) a0 = X; if (X > a1) a1 = X; if (Y < b0) b0 = Y; if (Y > b1) b1 = Y; }
    var sc = taille / Math.max(a1 - a0, b1 - b0, 1e-6);
    g.save();
    g.translate(cx, cy); g.scale(sc, sc); g.translate(-(a0 + a1) / 2, -(b0 + b1) / 2);
    if (nom === 'esquille') {
      var its = C.notes[k];                                        // v34 : tous les éclats de la promesse
      for (i = 0; i < its.length; i++) { g.fillStyle = _rgb(its[i].col); _trace(its[i].poly); g.fill(); }
    } else if (nom === 'bobinette') {
      g.lineCap = 'butt';
      var arcs = C.notes[k];
      for (i = 0; i < arcs.length; i++) { var q = arcs[i]; g.strokeStyle = _rgb(q.col); g.lineWidth = q.w; g.beginPath(); _arcRaccord(g, q.A, q.r, q.e); g.stroke(); }
    } else {
      var N = C.notes[k], PL = _pal(), c0 = cOf(s, now);
      var TN = PL ? [PL[0], PL[1], PL[2]] : [_nu(c0, -0.5), c0, _nu(c0, 0.3)];
      if (_tonsForces) TN = _tonsForces; else if (_ingenu()) TN = _madNature(c0);   // v34 : sous Ingénu, la dalle seule porte sa nature
      if (N.nature === 'cercle') {
        // anneaux de ψ, tracés par des courbes fermées ; une bande [A, B) = l'anneau A et l'anneau B en pair-impair
        var courbe = function (T, pts) {
          var n2 = pts.length; T.moveTo(pts[0][0], pts[0][1]);
          for (var z2 = 1; z2 <= n2; z2++) {
            var q0 = pts[(z2 - 2 + n2) % n2], q1 = pts[(z2 - 1) % n2], q2 = pts[z2 % n2], q3 = pts[(z2 + 1) % n2];
            T.bezierCurveTo(q1[0] + (q2[0] - q0[0]) / 6, q1[1] + (q2[1] - q0[1]) / 6, q2[0] - (q3[0] - q1[0]) / 6, q2[1] - (q3[1] - q1[1]) / 6, q2[0], q2[1]);
          }
          T.closePath();
        };
        var parL = {}; N.niveaux.forEach(function (nv) { parL[nv.L.toFixed(2)] = nv.pts; });
        if (typeof fondToile === 'function') { g.fillStyle = _rgb(_arr(fondToile())); g.beginPath(); courbe(g, N.pts); g.fill(); }
        var LAY3 = [[0, 2.11, 0], [0.11, 1, 1], [1.11, 2, 2]];
        for (var l3 = 0; l3 < 3; l3++) {
          var T3 = new Path2D(), vide = true;
          for (var j3 = Math.floor(N.niveaux[0].L / 3) - 1; 3 * j3 < N.top; j3++) {
            var A3 = parL[(3 * j3 + LAY3[l3][0]).toFixed(2)], B3 = parL[(3 * j3 + LAY3[l3][1]).toFixed(2)];
            if (!A3) { if (3 * j3 + LAY3[l3][0] < N.niveaux[0].L && 3 * j3 + LAY3[l3][1] > N.niveaux[0].L) A3 = N.pts; else continue; }
            courbe(T3, A3); vide = false;
            if (B3) courbe(T3, B3);
          }
          if (!vide) { g.fillStyle = _rgb(TN[LAY3[l3][2]]); g.fill(T3, 'evenodd'); }
        }
      } else {
        // l'œil (ou la strate fermée) tel qu'il paraît sur la Toile : la matière de la zone, découpée par la même courbe
        var clipP = new Path2D(); N.r.tracer(clipP, N.flat);
        g.clip(clipP);
        if (typeof fondToile === 'function') { g.fillStyle = _rgb(_arr(fondToile())); g.fill(clipP); }
        for (var c = 0; c < 3; c++) { g.fillStyle = _rgb(TN[c]); g.fill(N.r.paths[c], 'evenodd'); }
        if (N.trou) {
          // le liseré continue le long de la fermeture : la dalle finit toujours sur son trait noir.
          // Tracé à cheval sur le bord (moitié visible sous la découpe), épaisseur = celle du filet aux deux bords.
          var n = N.pts.length, i0 = N.trou[0], gN = N.trou[1];
          var PP = new Path2D();
          for (var zi = -2; zi <= gN + 3; zi++) {
            var pp = N.pts[((i0 + zi) % n + n) % n];
            if (zi === -2) PP.moveTo(pp[0], pp[1]); else PP.lineTo(pp[0], pp[1]);
          }
          g.strokeStyle = _rgb(TN[0]); g.lineWidth = N.filet * 2; g.lineCap = 'round'; g.lineJoin = 'round';
          g.stroke(PP);
        }
      }
    }
    g.restore();
    return true;
  }

  return { esquille: Resq, bobinette: Rbob, ritournelle: Rrit, madrure: Rmad, seule: _auRepos(seule), contour: _auRepos(contour), toucher: _auRepos(toucher), nature: _auRepos(nature), boite: _auRepos(boite) };
}

window.creerMondes = creerMondes;

})();
