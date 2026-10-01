/* Promi — quatre mondes écrits au CONTRAT-MONDE (23 sept. 2026)
 *
 * Esquille · Bobinette · Ritournelle · Madrure
 *
 * Dans le moteur, le corps de chaque fonction se colle tel quel dans l'IIFE de la Toile :
 * g, W, H, DPR, seeds, view, cOf, avg, cAt, isLightM y sont déjà dans la fermeture.
 * Ici, pour pouvoir mesurer hors de l'app, ces noms sont fournis par une fabrique et
 * rafraîchis par _sync() au début de chaque fonction. LA SEULE LIGNE À SUPPRIMER
 * AU COLLAGE EST `_sync();` — rien d'autre ne change.
 *
 * Aucun getImageData / putImageData / drawImage / createPattern / toDataURL.
 * Toute longueur est en fraction de l'unité locale u (distance à la graine voisine).
 * Tout hasard vient d'un LCG amorcé par la clé stable de la dalle.
 */
(function () {

function creerMondes(env) {
  var g, W, H, DPR, seeds, view, cOf, avg, cAt, isLightM, _dalleDeCle, curPAL, rampe, cleToile;
  function _sync() {
    g = env.g; W = env.W; H = env.H; DPR = env.DPR; seeds = env.seeds; view = env.view;
    cOf = env.cOf; avg = env.avg; cAt = env.cAt; isLightM = env.isLightM;
    _dalleDeCle = env._dalleDeCle; curPAL = env.curPAL; rampe = env.rampe; cleToile = env.cleToile;
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
      s = seeds[i]; sx = s.px == null ? s.x : s.px; sy = s.py == null ? s.y : s.py;
      if (sx < x0) x0 = sx; if (sy < y0) y0 = sy; if (sx > x1) x1 = sx; if (sy > y1) y1 = sy;
    }
    if (n === 0) { x0 = y0 = 0; x1 = y1 = 1; }
    var bs = Math.sqrt(Math.max(1, (x1 - x0 + 1) * (y1 - y0 + 1)) / Math.max(1, n));
    if (!(bs > 0)) bs = 32;
    var cols = Math.max(1, Math.ceil((x1 - x0 + 1) / bs)), rows = Math.max(1, Math.ceil((y1 - y0 + 1) / bs));
    var bk = new Array(cols * rows); for (i = 0; i < bk.length; i++) bk[i] = [];
    var P = new Array(n);
    for (i = 0; i < n; i++) {
      s = seeds[i]; sx = s.px == null ? s.x : s.px; sy = s.py == null ? s.y : s.py;
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
    var u = _uGlobal(ix), fel = u * 0.022, i;
    var nPromi = 0;
    for (i = 0; i < P.length; i++) if (P[i].s.kind !== 'gray') nPromi++;
    var sat = nPromi / Math.max(1, P.length);
    // une promesse pèse BEAUCOUP plus lourd que la matière : 8× sur une Toile vide, 2× à saturation.
    // C'est ce poids, et lui seul, qui rend les dalles repérables d'un coup d'œil.
    function place(p) { return p.s.kind === 'gray' ? 1 : 1 + (7 - 5 * sat); }

    var S = [];
    for (i = 0; i < P.length; i++) {
      var p0 = P[i];
      if (p0.x > x0 - u * 1.5 && p0.x < x1 + u * 1.5 && p0.y > y0 - u * 1.5 && p0.y < y1 + u * 1.5) S.push(p0);
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

    for (i = 0; i < feuilles.length; i++) {
      var fe = feuilles[i], p = fe.p, s = fe.s;
      if (!p || p.length < 3 || !s) continue;
      var ar = _aire(p); if (ar < u * u * 0.006) continue;
      var c = _cent(p);
      if (c[0] < x0 - u || c[0] > x1 + u || c[1] < y0 - u || c[1] > y1 + u) continue;
      var col = cOf(s.s, now);
      if (s.s.kind !== 'gray') {
        var tv = _lcg((s.k ^ 0x5bf03635) >>> 0)();
        if (tv < 0.18) col = _nu(col, -0.18);                  // l'éclat prend parfois une nuance
      }
      g.fillStyle = _rgb(col);
      _trace(_offset(p, Math.min(fel, Math.sqrt(ar) * 0.16))); g.fill();
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
    if (P && _promesse(s)) {
      var b = 0, bd = 1e9;
      for (var i = 0; i < 4; i++) { var d = Math.abs(c[0] - P[i][0]) + Math.abs(c[1] - P[i][1]) + Math.abs(c[2] - P[i][2]); if (d < bd) { bd = d; b = i; } }
      return [c, P[(b + 1) % 4], P[(b + 2) % 4], P[(b + 3) % 4]];
    }
    return [c, _nu(c, -0.07), _nu(c, 0.06), _nu(c, -0.035)];
  }
  // origine : sp = F.spacing ; au contrat, sp = 1,2 u (u = médiane des distances au plus proche voisin)
  var SP_U = 1.2;

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
    var sp = _uGlobal(ix) * SP_U;
    var c = sp * 0.30, th = c * 0.26, extra = th * 0.55;   // origine mesurée sur Toile pleine : c = 0,30·sp
    var anneau = {}, tourne = {}, pris = {};
    var ordre = P.slice().sort(function (a, b) { return a.k - b.k; });
    for (i = 0; i < ordre.length; i++) {
      var p = ordre[i]; if (!_promesse(p.s)) continue;
      var bi = Math.round(p.x / c), bj = Math.round(p.y / c), fait = false;
      for (var rr = 0; rr <= 2 && !fait; rr++) for (var a = -rr; a <= rr && !fait; a++) for (var b = -rr; b <= rr && !fait; b++) {
        if (Math.max(Math.abs(a), Math.abs(b)) !== rr) continue;
        var gi = bi + a, gj = bj + b, libre = true;
        for (var da = -1; da <= 1 && libre; da++) for (var db = -1; db <= 1; db++) if (pris[(gi + da) + '|' + (gj + db)]) { libre = false; break; }
        if (!libre) continue;
        pris[gi + '|' + gj] = 1; anneau[gi + '|' + gj] = 1;
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
          pris[hi + '|' + hj] = 1;
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
        var dalle = !!anneau[Math.round(A[0] / c) + '|' + Math.round(A[1] / c)];
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
        var A2 = L2.a[z], a0 = A2[2], a1 = A2[3], e = 0.5;
        var sx = A2[0] + Math.cos(a0) * rr2, sy = A2[1] + Math.sin(a0) * rr2;
        var ex = A2[0] + Math.cos(a1) * rr2, ey = A2[1] + Math.sin(a1) * rr2;
        g.moveTo(sx + e * Math.sin(a0), sy - e * Math.cos(a0));
        g.lineTo(sx, sy);
        g.arc(A2[0], A2[1], rr2, a0, a1);
        g.lineTo(ex - e * Math.sin(a1), ey + e * Math.cos(a1));
      }
      g.stroke();
    }
    g.restore();
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
      if (p.x < x0 - RMAX || p.x > x1 + RMAX || p.y < y0 - RMAX || p.y > y1 + RMAX) continue;
      var vois = ix.near(p, 10); if (!vois.length) continue;
      var HD = [];
      for (var v = 0; v < vois.length; v++) {
        var q = vois[v].p, dq = vois[v].d; if (dq <= 0) continue;
        var t0 = 0.5 * dq + (p.w - q.w) * 0.5;
        if (t0 < dq * 0.12) t0 = dq * 0.12; if (t0 > dq * 0.88) t0 = dq * 0.88;
        HD.push((q.x - p.x) / dq, (q.y - p.y) / dq, t0);
      }
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
  function _madBuild(now, x0, y0, x1, y1) {
    var ix = _idx(), P = ix.P, n = P.length, i;
    if (!n) return;
    var sp = _uGlobal(ix) * SP_U, band = sp * 0.17;
    var th = typeof cleToile === 'number' ? _lcg(cleToile >>> 0)() * 6.283 : 0.6;
    var ct = Math.cos(th) / band, st = Math.sin(th) / band;
    var KX = new Float64Array(n), KY = new Float64Array(n), KK = new Float64Array(n), KR = new Float64Array(n);
    for (i = 0; i < n; i++) {
      var r0 = _lcg((P[i].k ^ 0x5bd1e995) >>> 0);
      KX[i] = P[i].x; KY[i] = P[i].y;
      KK[i] = 7.5 + r0() * 2;                                  // en unités de band
      var rr = sp * (0.36 + r0() * 0.12); KR[i] = 1 / (rr * rr);
    }
    var pas = band * 0.5;
    var aire = (x1 - x0 + 4 * pas) * (y1 - y0 + 4 * pas);
    if (aire / (pas * pas) > 260000) pas = Math.sqrt(aire / 260000);
    var gx0 = x0 - 2 * pas, gy0 = y0 - 2 * pas;
    var nx = Math.ceil((x1 - x0) / pas) + 4, ny = Math.ceil((y1 - y0) / pas) + 4, rw = nx + 1;
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
    for (j = 0; j < ny; j++) for (a = 0; a < nx; a++) {
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
    }
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
    for (var s0 = 0; s0 < NS; s0++) {
      if (vu[s0]) continue;
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
      var ns = Math.max(8, Math.round(lt / (pas * 0.8))), stp2 = lt / ns, rs = new Float64Array(ns * 2), seg = 0;
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
    for (var k0 = 0; k0 < NL; k0++) tracer(P2[lay[k0]], parNiveau[k0]);
    return { paths: P2, tons: TONS };
  }

  // Le tracé de Madrure est gardé d'une image à l'autre : l'onde ne change qu'avec le semis.
  // Seule la GÉOMÉTRIE est gardée ; elle tombe à tout changement de semis (position, poids, clé — donc à la
  // plantation, une fois), de clé de Toile, et dès que la vue sort de la zone calculée.
  // Les couleurs ne sont jamais gardées : relues à chaque image, un changement de palette ou de thème est immédiat.
  // Seule la vue (plus 12 % de marge) est calculée et lissée.
  var _madCache = null;
  function _madSig() {
    var h = 0x811c9dc5;
    function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(seeds.length);
    for (var i = 0; i < seeds.length; i++) {
      var s = seeds[i];
      mix(Math.round(s.x * 16)); mix(Math.round(s.y * 16));          // position de repos : le frémissement ne reconstruit pas
      mix(Math.round((s.w || 0) * 16)); mix(_cle(s));
    }
    mix(typeof cleToile === 'number' ? cleToile : 0);
    return h >>> 0;
  }
  function Rmad(now, x0, y0, x1, y1) {
    _sync();
    var sig = _madSig(), C = _madCache;
    if (!C || C.sig !== sig || x0 < C.x0 || y0 < C.y0 || x1 > C.x1 || y1 > C.y1) {
      var mw = (x1 - x0) * 0.12, mh = (y1 - y0) * 0.12;
      C = _madCache = { sig: sig, x0: x0 - mw, y0: y0 - mh, x1: x1 + mw, y1: y1 + mh, r: _madBuild(now, x0 - mw, y0 - mh, x1 + mw, y1 + mh) };
    }
    if (!C.r) return;
    // couleurs relues à chaque image : palette et thème ne peuvent jamais rester dans l'ancienne teinte
    var PL = _pal(), c0 = cOf(seeds[0], now);
    var TN = PL ? [PL[0], PL[1], PL[2]] : [_nu(c0, -0.5), c0, _nu(c0, 0.3)];
    for (var c = 0; c < 3; c++) { g.fillStyle = _rgb(TN[c]); g.fill(C.r.paths[c], 'evenodd'); }
  }
  Rmad.invalider = function () { _madCache = null; };

  return { esquille: Resq, bobinette: Rbob, ritournelle: Rrit, madrure: Rmad };
}

window.creerMondesAvant = creerMondes;

})();
