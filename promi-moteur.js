/* ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
   promi-moteur.js — LE MOTEUR DE LA TOILE ET SES VINGT MONDES. FICHIER DE RÉFÉRENCE (assainissement, Tom, 30 sept. 2026).

   C'est la SOURCE : app.html le charge (<script src="promi-moteur.js">) à l'endroit exact où ces blocs vivaient, dans le
   même ordre — rien d'autre ne change. Il n'existe plus aucune copie (promi-mondes.js et promi-mondes-integre-v32.js,
   périmées de ~1 100 lignes, sont rangées dans sauvegardes/fossiles/).

   Ce que le portage Swift traduit, c'est CE fichier ; ce qui juge la traduction, c'est banc_rendu.py (280 images au pixel).
   Le contrat d'un monde : CONTRAT-MONDE.md. Les blocs d'origine sont gardés tels quels, séparés par leur nom de lot :
   ⚠ jadis chacun était un <script> à part — une erreur levée au niveau haut d'un bloc arrêtait CE bloc seulement ; dans
   un seul fichier elle arrête la suite. Aucun ne lève aujourd'hui (vérifié : aucune erreur au chargement, WebKit et Chromium).
   ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */


/* ══════════════════ bloc « lot-V32-MONDES » ══════════════════ */
/* ⚑ v32 (Tom, 23 sept. 2026) — ESQUILLE · BOBINETTE · RITOURNELLE · MADRURE, livrés par le chat qui code les mondes
   (`promi-mondes.js`, `INTEGRATION-MONDES.md`). Collé TEL QUEL, à quatre retouches près, toutes marquées « intégration v32 » :
   la position de repos pour la géométrie gardée · la signature au demi-pixel · le cache de Madrure par semis et SANS
   reconstruction pendant que le semis bouge · `boite()`, la boîte réellement peinte. La fabrique reçoit du moteur un
   environnement à accesseurs (`creerMondes(env)`) : ses noms sont relus à chaque appel, jamais gardés. */
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
  var _enreg = false, _rec = null, _calque = null;
  // ⚑ intégration v32 : la géométrie GARDÉE (Madrure, carnets) se calcule sur la position de REPOS — sa signature
  // (_madSig) l'est déjà ; sans ce drapeau elle se bâtissait sur la position frémissante et restait décalée.
  var _repos = false, _versCible = false;   // v47 : Esquille lit la place d'ARRIVÉE (tx, ty) des graines
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
    if (_calque) g = _calque;   // v38 : l'œil de Madrure se peint dans son calque (voir _madCalque)
  }

  /* ---------- socle commun ------------------------------------------------ */

  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = (h * 16777619) >>> 0; } return h >>> 0; }

  // clé stable d'une cellule : jamais son index dans seeds, jamais son id
  function _cle(s) {
    // v43 : une dalle PARTIE garde la clé de sa parole (le moteur la note dans partPid / partNuee) — sans quoi elle changerait
    // de forme et de tons au moment même où elle se retire
    var pid = s.pid != null ? s.pid : s.partPid, nuee = s.nuee || s.partNuee;
    if (pid != null && typeof _dalleDeCle === 'function') { var k = _dalleDeCle(pid); if (k != null) return k >>> 0; }
    if (nuee) return _fnv('n\u0000' + nuee);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
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
    var SD = _versCible ? seeds.filter(function (q) { return q.part == null; }) : seeds;   // v47 : pour Esquille, une dalle qui part cesse de compter à l'instant
    var n = SD.length, i, s, sx, sy, _fin = _versCible ? env.finale : null;   // v47 : Esquille lit l'ÉQUILIBRE de la Toile (il ne dérive pas quand les graines glissent)
    var x0 = 1e18, y0 = 1e18, x1 = -1e18, y1 = -1e18;
    for (i = 0; i < n; i++) {
      s = SD[i]; var _fq = _versCible && _fin ? _fin.get(s) : null; sx = _fq ? _fq[0] : (_versCible && s.tx != null) ? s.tx : (_repos || s.px == null) ? s.x : s.px; sy = _fq ? _fq[1] : (_versCible && s.ty != null) ? s.ty : (_repos || s.py == null) ? s.y : s.py;
      if (sx < x0) x0 = sx; if (sy < y0) y0 = sy; if (sx > x1) x1 = sx; if (sy > y1) y1 = sy;
    }
    if (n === 0) { x0 = y0 = 0; x1 = y1 = 1; }
    var bs = Math.sqrt(Math.max(1, (x1 - x0 + 1) * (y1 - y0 + 1)) / Math.max(1, n));
    if (!(bs > 0)) bs = 32;
    var cols = Math.max(1, Math.ceil((x1 - x0 + 1) / bs)), rows = Math.max(1, Math.ceil((y1 - y0 + 1) / bs));
    var bk = new Array(cols * rows); for (i = 0; i < bk.length; i++) bk[i] = [];
    var P = new Array(n);
    for (i = 0; i < n; i++) {
      s = SD[i]; var _fq2 = _versCible && _fin ? _fin.get(s) : null; sx = _fq2 ? _fq2[0] : (_versCible && s.tx != null) ? s.tx : (_repos || s.px == null) ? s.x : s.px; sy = _fq2 ? _fq2[1] : (_versCible && s.ty != null) ? s.ty : (_repos || s.py == null) ? s.y : s.py;
      P[i] = { s: s, x: sx, y: sy, w: (_versCible ? ((s.wAt && s.wFin != null) ? s.wFin : (s.wt != null ? s.wt : s.w)) : s.w) || 0, k: _cle(s) };   // v54 : l'équilibre, c'est aussi le poids d'arrivée
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
  /* ⚑ v45 (Tom, 24 sept. 2026) — LA RÉPARTITION DU PDF. « C'est trop fragmenté, et tous les fragments font la même taille.
     On veut de grands axes coupants qui traversent la plaque, et une vraie diversité de tailles — de grands éclats à côté
     de petits. Le fragment d'une promesse reste nettement plus gros que la matière. »
     Avant : une grille de germes au pas u, chaque germe un éclat — un pavage régulier (l'ancien Resq : app-avant-v45).
     Désormais, un ARBRE DE CASSURES fixe pour une Toile (tiré de sa clé et de sa taille, jamais des promesses) :
       1 · de grandes cassures traversantes — 4 à 6 droites qui coupent toute la plaque, en directions variées ;
       2 · la refente — chaque morceau se recoupe en travers de sa plus grande longueur, à une place variable.
     Ce qu'on PEINT est une coupe de cet arbre, décidée par les promesses : un morceau qui en porte plusieurs se refend ; un
     morceau qui n'en porte qu'une s'arrête dès qu'il est à la taille d'un grand éclat (c'est SA dalle) ; un morceau de
     matière s'arrête à une taille tirée pour lui, plus petite et variable (0,3 à 0,85 × l'éclat d'une promesse, qui lui s'arrête
     jusqu'à 1,6 ×).
     Couleur : l'éclat d'une promesse porte sa couleur ; la matière prend surtout les autres tons de la palette de la
     promesse la plus proche (le sien une fois sur six) — la promesse se détache d'un coup d'œil.
     Le mouvement (v44) est gardé : un éclat qui change de couleur, se refend ou se ressoude SE CASSE. */
  var _esqArbre = null;
  function _esqNoeud(id, poly, R) {
    return { id: id, poly: poly, aire: _aire(poly), c: _cent(poly), v: R(), kids: null, ok: true, r: R };
  }
  function _esqRefend(nd) {
    if (nd.kids || !nd.ok) return nd.kids;
    var p = nd.poly, c = nd.c, xx = 0, yy = 0, xy = 0, k;
    for (k = 0; k < p.length; k++) { var dx = p[k][0] - c[0], dy = p[k][1] - c[1]; xx += dx * dx; yy += dy * dy; xy += dx * dy; }
    var R = _lcg(_fnv('e' + nd.id + '|' + nd.sd)), ang = 0.5 * Math.atan2(2 * xy, xx - yy) + (R() - 0.5) * 0.9;
    var nx = Math.cos(ang), ny = Math.sin(ang), t0 = 1e18, t1 = -1e18;
    for (k = 0; k < p.length; k++) { var t = p[k][0] * nx + p[k][1] * ny; if (t < t0) t0 = t; if (t > t1) t1 = t; }
    var cut = t0 + (t1 - t0) * (0.28 + R() * 0.44), px = nx * cut, py = ny * cut;
    var A = _clip(p, px, py, nx, ny), B = _clip(p, px, py, -nx, -ny);
    if (A.length < 3 || B.length < 3) { nd.ok = false; return null; }
    var a = _esqNoeud(nd.id + '0', A, R), b = _esqNoeud(nd.id + '1', B, R);
    a.sd = nd.sd; b.sd = nd.sd; nd.cut = [nx, ny, cut];
    nd.kids = [a, b]; return nd.kids;
  }
  function _esqRacines(cle, u) {
    var cleA = W + '|' + H + '|' + cle;
    if (_esqArbre && _esqArbre.cle === cleA) return _esqArbre;
    var m = u * 0.6, R = _lcg((cle ^ 0x6a09e667) >>> 0);
    var pieces = [[[-m, -m], [W + m, -m], [W + m, H + m], [-m, H + m]]];
    var K = Math.max(3, Math.round((4 + R() * 2.4) * Math.sqrt(W * H / (390 * 844)))), base = R() * Math.PI;
    for (var i = 0; i < K; i++) {
      var ang = base + i * Math.PI / K + (R() - 0.5) * 0.5, nx = Math.cos(ang), ny = Math.sin(ang);
      var qx = W * (0.12 + 0.76 * R()), qy = H * (0.1 + 0.8 * R()), out = [];
      for (var j = 0; j < pieces.length; j++) {
        var A = _clip(pieces[j], qx, qy, nx, ny), B = _clip(pieces[j], qx, qy, -nx, -ny);
        if (A.length > 2 && _aire(A) > 1) out.push(A); if (B.length > 2 && _aire(B) > 1) out.push(B);
      }
      pieces = out;
    }
    pieces.sort(function (p1, p2) { var c1 = _cent(p1), c2 = _cent(p2); return (c1[1] - c2[1]) || (c1[0] - c2[0]); });
    var rac = pieces.map(function (p, i2) { var n = _esqNoeud('g' + i2, p, R); n.sd = cle; return n; });
    _esqArbre = { cle: cleA, rac: rac, vus: null, anim: {} };
    return _esqArbre;
  }
  function Resq(now, x0, y0, x1, y1) {
    _sync();
    var _vc0 = _versCible; _versCible = true; var ix; try { ix = _idx(); } finally { _versCible = _vc0; }   // v47 : partout (Toile, fiche, toucher), l'équilibre — les trois restent d'accord
    var P = ix.P;
    if (!P.length) return;
    var u = _uMonde(ix, U_ESQ), i;
    var cle0 = typeof cleToile === 'number' ? (cleToile >>> 0) : 0;
    var A = _esqRacines(cle0, u);
    // les promesses, à leur position de repos (le frémissement ne les fait pas changer d'éclat)
    var PR = [];
    // ⚑ v47 (Tom, troisième fois : « un frémissement, pas un séisme ») — la plaque se découpe sur la place D'ARRIVÉE des
    // promesses (tx, ty) : elle se recasse UNE fois, au premier instant, au lieu de se refendre pendant tout le ressort ;
    // et une dalle qui part cesse tout de suite de compter.
    /* ⚑ v78 (Tom : « Esquille, le mouvement ne rend rien au Studio ») — la plaque ne se FEND qu'autour des promesses ; une graine
       d'aperçu n'en porte aucune : l'aperçu n'était que de grands éclats bruts, et une arrivée n'y recolorait que trois ou quatre
       d'entre eux. Une graine d'aperçu fend la plaque comme une parole — c'est une Toile de paroles qu'on montre. */
    for (i = 0; i < P.length; i++) if ((_promesse(P[i].s) || P[i].s.apercu) && P[i].s.part == null) PR.push({ x: P[i].x, y: P[i].y, p: P[i] });   // P porte déjà la place finale (ou d'arrivée) sur la Toile vivante
    var nP = Math.max(1, PR.length), Ac = W * H / nP, Ap = Math.min(0.62 * Ac, W * H / 7), tiny = u * u * 0.05;
    var frag = [];
    /* ⚑ v57 (Tom : « plus aucune onde, jamais ») — le seuil de refente dépend du NOMBRE de promesses (Ap) : une plantation le
       changeait pour tous les morceaux, et toute la plaque se recassait en une image, jusqu'à l'autre bout de l'écran. Chaque
       morceau garde sa décision (refendu ou entier) ; seuls ceux qui sont près de la dalle qui arrive ou qui part la reprennent
       (et ceux qui doivent séparer deux promesses se refendent toujours). La mémoire suit la Toile vivante ; les autres rendus
       (fiche, toucher) la lisent. */
    var TRq = env.trans, dm = A.dec || (A.dec = {}), RAD = Math.sqrt(Ap) * 2.1, QX = TRq && TRq.x != null ? TRq.x : null, QY = QX != null ? TRq.y : null;
    function visite(nd, S, prof) {
      var stop;
      if (S.length > 1) stop = false;
      else if (S.length === 1) stop = nd.aire <= Ap * 1.6;
      else stop = nd.aire <= Ap * (0.3 + 0.55 * nd.v * nd.v);   // la matière : 0,3 à 0,85 × l'éclat d'une promesse, tiré par morceau
      if (S.length <= 1) {
        var pres = QX != null && Math.hypot(nd.c[0] - QX, nd.c[1] - QY) < RAD + Math.sqrt(nd.aire) * 0.5;
        if (!pres && dm[nd.id] !== undefined) stop = dm[nd.id];
        else if (env.vive) dm[nd.id] = stop;
      }
      if (!stop && prof < 24 && nd.aire > tiny) {
        var K2 = _esqRefend(nd);
        if (K2) {
          var cu = nd.cut, SA = [], SB = [];
          for (var q = 0; q < S.length; q++) (S[q].x * cu[0] + S[q].y * cu[1] <= cu[2] ? SA : SB).push(S[q]);
          visite(K2[0], SA, prof + 1); visite(K2[1], SB, prof + 1); return;
        }
      }
      frag.push({ nd: nd, pr: S.length ? S[0].p : null });
    }
    for (i = 0; i < A.rac.length; i++) {
      var rn = A.rac[i], S0 = [];
      for (var q = 0; q < PR.length; q++) if (_pip(PR[q].x, PR[q].y, rn.poly)) S0.push(PR[q]);
      visite(rn, S0, 0);
    }
    // v45 : la composition, publiée (§7 : un juge lit la composition, jamais les pixels d'une matière)
    if (env.vive) { var _ap = [], _am = []; for (i = 0; i < frag.length; i++) (frag[i].pr ? _ap : _am).push(Math.round(frag[i].nd.aire));
      window._esqComp = { promesses: PR.length, eclatsPromesse: _ap.length, matiere: _am.length, airesPromesse: _ap, airesMatiere: _am, Ap: Math.round(Ap), plaque: Math.round(W * H) }; }
    var fel = (typeof env.uMat === 'number' && env.uMat > 0 ? env.uMat : u * 2) * 0.024;
    /* ⚑ v55 (Tom : « supprime l'onde, ça fait cheap ; on ne veut pas une vague qui traverse : les fragments autour doivent réagir
       et se reformer, chacun pour lui-même ») — le retard était proportionnel à la distance à la dalle (un front qui court) et la
       poussée partait d'elle en rayons. Chaque éclat a maintenant SON retard, tiré de sa clé (0 à 140 ms), et SA direction. */
    /* ⚑ v57 (Tom : « plus aucune onde, jamais ; chaque fragment réagit pour lui-même, à son propre moment, parce que la dalle voisine
       le pousse ; beaucoup plus doux ») — mesuré sur la carte des différences : les éclats qui changeaient BASCULAIENT d'un coup à
       mi-parcours (160 ms, l'ancienne couleur puis la nouvelle en une image), plusieurs au même instant près de la dalle — on lisait
       un front. Maintenant :
       · la couleur se FOND de l'ancienne à la nouvelle (620 ms, lissée) — plus aucune bascule ;
       · les éclats VOISINS de la dalle qui arrive (ou part) sont POUSSÉS : un léger glissement vers l'extérieur puis un retour,
         d'amplitude selon leur proximité, à un moment tiré de LEUR clé (0 à 320 ms) — aucun ordre de distance ;
       · loin de la dalle, rien ne bouge. */
    var TR = env.trans, vive = !!env.vive, ESQ_D = 620, anim = A.anim, vus = {};
    var _retard = function (id) { var h = _fnv('d' + id); return (h % 1000) / 1000 * 320; };
    var PX = TR && TR.x != null ? TR.x : null, PY = TR && TR.x != null ? TR.y : null, PO = u * 2.2;
    if (vive && TR && A.trN !== TR.n) { A.trN = TR.n; A.pousse = {}; }   // une nouvelle transition : de nouvelles poussées
    // la couleur d'un éclat : sa promesse ; sinon la matière de la promesse la plus proche
    function source(f) {
      if (f.pr) return { s: f.pr.s, k: f.pr.k, t: -1 };
      var ow = ix.owner(f.nd.c[0], f.nd.c[1]), h = _fnv('m' + f.nd.id), t = (h % 6) === 0 ? 0 : 1 + (h >>> 3) % 3;
      return { s: ow.s, k: ow.k, t: t };
    }
    function couleur(src) {
      if (src.t < 0) return cOf(src.s, src.s.t0 != null ? Math.max(now, src.s.t0 + 1e5) : now);
      return _rampe(src.s, now)[src.t];
    }
    function lisse(t) { t = t < 0 ? 0 : t > 1 ? 1 : t; return t * t * t * (t * (6 * t - 15) + 10); }
    function peindre(poly, col, ph, c, k, amp) {
      var ar = _aire(poly); if (ar < u * u * 0.004) return;
      var pe = _offset(poly, Math.min(fel, Math.sqrt(ar) * 0.16));
      if (ph >= 0 && ph < 1 && amp > 0 && pe.length > 2) {
        var sb = Math.sin(Math.PI * lisse(ph)), rk = _lcg(_fnv('r' + k)), rot = (rk() - 0.5) * 0.012 * sb * amp;
        var dx = PX != null ? c[0] - PX : Math.cos(rk() * 6.283), dy = PX != null ? c[1] - PY : Math.sin(rk() * 6.283), dl = Math.sqrt(dx * dx + dy * dy) || 1;
        if (TR && TR.kind === 'depart') { dx = -dx; dy = -dy; }
        var ox = dx / dl * u * 0.05 * sb * amp, oy = dy / dl * u * 0.05 * sb * amp, cr = Math.cos(rot), sr = Math.sin(rot), q2 = [];
        for (var z = 0; z < pe.length; z++) { var ex = pe[z][0] - c[0], ey = pe[z][1] - c[1]; q2.push([c[0] + ex * cr - ey * sr + ox, c[1] + ex * sr + ey * cr + oy]); }
        pe = q2;
      }
      g.fillStyle = _rgb(col); _trace(pe); g.fill();
    }
    /* ⚑ v80 (Tom : « Esquille n'est pas fait : c'est un fondu, une image puis une autre. Les fragments réagissent, se déplacent, se
       reforment. ») — UN ÉCLAT SE REFORME. Un éclat qui naît sort de celui qu'il fend : il part de SA forme et se reforme jusqu'à la
       sienne ; un éclat qui se ressoude reprend la forme de celui qui le remplace. Deux éclats (convexes) sont échantillonnés sur les
       mêmes 36 rayons, depuis un centre qui est dans les deux, et on glisse de l'un à l'autre. Aucune onde : chacun à SON moment. */
    function rayon(poly, cx, cy, ca, sa) { var best = 1e18; for (var e = 0, m = poly.length; e < m; e++) { var p1 = poly[e], p2 = poly[(e + 1) % m];
        var ex = p2[0] - p1[0], ey = p2[1] - p1[1], den = ca * ey - sa * ex; if (Math.abs(den) < 1e-12) continue;
        var t = ((p1[0] - cx) * ey - (p1[1] - cy) * ex) / den, uu = ((p1[0] - cx) * sa - (p1[1] - cy) * ca) / den;
        if (t > 0 && uu >= -1e-6 && uu <= 1 + 1e-6 && t < best) best = t; } return best < 1e17 ? best : 0; }
    function reforme(de, vers, cx, cy, t) { var q = [], N = 36; for (var k = 0; k < N; k++) { var an2 = k / N * 6.283185307179586, ca = Math.cos(an2), sa = Math.sin(an2);
        var r0 = rayon(de, cx, cy, ca, sa), r1 = rayon(vers, cx, cy, ca, sa); if (!(r0 > 0) || !(r1 > 0)) return null;   // un rayon qui manque un bord : pas de reformage (sinon une étoile)
        var r = r0 * (1 - t) + r1 * t; q.push([cx + ca * r, cy + sa * r]); } return q; }
    function melange(a1, b1, t) { return [a1[0] + (b1[0] - a1[0]) * t, a1[1] + (b1[1] - a1[1]) * t, a1[2] + (b1[2] - a1[2]) * t]; }
    var _eqA = 0, _eqR = 0; if (vive && A.partis) { A.partis = A.partis.filter(function (pa) { var ph = (now - pa.t) / ESQ_D; if (ph >= 1) return false;
        var tt = ph < 0 ? 0 : lisse(ph), col = pa.vers.src ? melange(pa.col, couleur(pa.vers.src), ph < 0 ? 0 : lisse(Math.min(1, ph / 0.4))) : pa.col;
        var pq = reforme(pa.poly, pa.vers.poly, pa.c[0], pa.c[1], tt); if (!pq) return false; peindre(pq, col, -1, pa.c, pa.id, 0); return true; }); if (A.partis.length) window._mondeEncore = true; }
    for (i = 0; i < frag.length; i++) {
      var f = frag[i], nd = f.nd, c = nd.c;
      if (c[0] < x0 - u * 3 || c[0] > x1 + u * 3 || c[1] < y0 - u * 3 || c[1] > y1 + u * 3) continue;
      var src = source(f), sig = (src.s ? _cle(src.s) : 0) + ':' + src.t;
      if (_rec && f.pr) _note(f.pr.k, { poly: _offset(nd.poly, Math.min(fel, Math.sqrt(nd.aire) * 0.16)), col: cOf(f.pr.s, now) });
      if (vive && A.vus) {
        var av = A.vus[nd.id], an = anim[nd.id];
        if (!av && !an) {                                                              // un éclat qui naît : il part de ce qu'il remplace
          var dePr = null;
          for (var idv in A.vus) { var ov = A.vus[idv]; if (ov.poly && _pip(c[0], c[1], ov.poly)) { dePr = ov; break; } }
          anim[nd.id] = an = { t: now + _retard(nd.id), de: dePr };
        }
        else if (av && av.sig !== sig && !an) anim[nd.id] = an = { t: now + _retard(nd.id), de: av };   // un éclat qui change de couleur
        // la poussée : les voisins de la dalle, une fois par transition
        var amp = 0;
        if (TR && PX != null) { var dd = Math.hypot(c[0] - PX, c[1] - PY); if (dd < PO) amp = 1 - dd / PO; }
        if (amp > 0 && A.pousse && !A.pousse[nd.id]) A.pousse[nd.id] = { t: now + _retard(nd.id), a: amp };
        var pu = A.pousse && A.pousse[nd.id], php = pu ? (now - pu.t) / ESQ_D : -1;
        if (an) {
          var ph = (now - an.t) / ESQ_D, colA = couleur(src);
          if (ph >= 1) { delete anim[nd.id]; }
          else { var colD = an.de ? couleur(an.de.src) : colA; colA = melange(colD, colA, ph < 0 ? 0 : lisse(Math.min(1, ph / 0.4))); }   /* v82 (Tom) : la couleur AVANT la forme — le ton lavé se lisait comme une transparence */
          var polyA = nd.poly; if (an.de && an.de.poly && ph < 1 && an.de.poly !== nd.poly && _pip(c[0], c[1], an.de.poly)) { polyA = reforme(an.de.poly, nd.poly, c[0], c[1], ph < 0 ? 0 : lisse(ph)) || nd.poly; if (polyA !== nd.poly) _eqR++; }
          _eqA++;
          peindre(polyA, colA, php, c, nd.id, pu ? pu.a : 0);
          vus[nd.id] = { sig: sig, src: src, poly: nd.poly, c: c }; continue;
        }
        if (pu) { peindre(nd.poly, couleur(src), php, c, nd.id, pu.a); vus[nd.id] = { sig: sig, src: src, poly: nd.poly, c: c }; continue; }
      }
      peindre(nd.poly, couleur(src), -1, c, nd.id, 0);
      vus[nd.id] = { sig: sig, src: src, poly: nd.poly, c: c };
    }
    if (vive) {
      // un éclat refendu ou ressoudé cède sa place d'un coup : ceux qui le remplacent couvrent la même surface, à pleine
      // taille, dans SA couleur — puis se cassent (v45 : réduits chacun autour de son centre, les deux ne coïncidaient pas)

      /* v80 — les éclats qui ont disparu (ressoudés) : ils restent le temps de se reformer vers celui qui les couvre maintenant */
      if (A.vus) { A.partis = A.partis || []; for (var idp in A.vus) { if (vus[idp]) continue; var op = A.vus[idp]; if (!op.poly || !op.c) continue;
          var cible = null; for (var idn in vus) { if (vus[idn].poly && _pip(op.c[0], op.c[1], vus[idn].poly)) { cible = vus[idn]; break; } }
          if (cible && A.partis.length < 400) A.partis.push({ id: idp, poly: op.poly, c: op.c, col: couleur(op.src), vers: cible, t: now + _retard(idp) }); } }
      A.vus = vus; window._esqAnim = { anim: _eqA, reforme: _eqR, partis: (A.partis || []).length, eclats: frag.length };   // v80 : lecture (juges)
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
  function _promesse(s) { return s.pid != null || !!s.nuee || s.partPid != null || !!s.partNuee; }   // v43 : une dalle qui part reste une promesse jusqu'au bout
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
  /* ⚑ v45 (Tom, 24 sept.) — « LES FILS SE RETISSENT. » Sur la Toile vivante, pendant une transition, un arc qui change —
     de couleur, de sens (la tuile se retourne autour d'une bobine qui arrive), d'épaisseur (il devient bobine) — ne bascule
     plus d'une image à l'autre : l'ancien fil SE RETIRE le long de son arc, puis le nouveau SE TISSE le long du sien
     (520 ms). Ce qu'on garde d'une image à l'autre : l'arc affiché de chaque demi-tuile, et l'heure de son retissage —
     seulement sur la Toile vivante. Et la trame se lit sur la position de REPOS des promesses (au repos c'est la même) :
     pendant le frémissement d'une plantation, une bobine sautait d'une case à l'autre. */
  var _bobEtat = null, _bobPlace = null, BOB_D = 1300;   // v58 : 1,3 s — le train de couleurs se voit parcourir le fil   // v56 : 700 → 900 ms   // v55 : 520 → 700 ms — on voit le fil se tirer
  function _arcPart(T, A, r, f0, f1) {
    var a0 = A[2] + (A[3] - A[2]) * f0, a1 = A[2] + (A[3] - A[2]) * f1;
    if (a1 - a0 < 1e-3) return;
    T.moveTo(A[0] + Math.cos(a0) * r, A[1] + Math.sin(a0) * r); T.arc(A[0], A[1], r, a0, a1);
  }
  function Rbob(now, x0, y0, x1, y1) {
    _sync();
    /* ⚑ v54 (Tom : « tout bouge en même temps, des tornades de scintillement ; les fils se tirent pour redéfinir la Toile là
       où c'est nécessaire, localement ; la couleur vit dans le mouvement, elle ne clignote pas ; on doit voir quelle dalle vient
       de naître ») — pendant une transition la trame se lisait sur les positions EN MOUVEMENT (le poids qui grandit, les graines
       qui glissent, le relâchement de la poussée à 380 ms) : des arcs changeaient de propriétaire partout, plusieurs fois.
       1 · pendant une transition la trame se lit sur l'ÉTAT FINAL (positions et poids d'arrivée, `_versCible`) : un arc ne
           change qu'une fois ; au repos, rien ne change (la trame au repos est celle d'avant) ;
       2 · chaque retissage attend son tour selon sa DISTANCE à la dalle qui arrive ou qui part : les fils se tirent depuis elle ;
       3 · la couleur COULE le long du fil par-dessus l'ancienne — jamais un instant sans fil ; si l'arc change de forme,
           l'ancien se retire pendant que le nouveau avance ; le fil part toujours du bout tourné vers la dalle. */
    var TRb = env.trans, viveb = !!env.vive;
    var ix; if (viveb && TRb) { var _vcb = _versCible; _versCible = true; try { ix = _idx(); } finally { _versCible = _vcb; } }
    else { var _r0 = _repos; _repos = true; try { ix = _idx(); } finally { _repos = _r0; } }
    var P = ix.P, i;
    var EB = (viveb && TRb) ? (_bobEtat || {}) : null, EBn = viveb ? {} : null, anb = [];
    var OX = TRb && TRb.x != null ? TRb.x : null, OY = TRb && TRb.y != null ? TRb.y : null;
    if (!P.length) return;
    var sp = _uMonde(ix, U_BOB) * SP_U;
    var c = sp * 0.30, th = c * 0.26, extra = th * 0.55;   // origine mesurée sur Toile pleine : c = 0,30·sp
    var anneau = {}, tourne = {}, pris = {}, boucle = {};
    /* ⚑ v56 — les anneaux se placent dans l'ORDRE DE PLANTATION (puis par clé) : une dalle neuve se place en dernier et ne déloge
       personne. Dans l'ordre des clés, elle s'insérait au milieu et chaque anneau suivant cherchait une autre place — 57 tuiles se
       retournaient pour une seule plantation, partout. L'ordre est permanent : rien ne change à la fin de la transition. */
    var ordre = P.slice().sort(function (a, b) { var ta = a.s.t0 || 0, tb = b.s.t0 || 0; return (ta - tb) || (a.k - b.k); });
    /* ⚑ v56 — UNE PLACE FIDÈLE. Un anneau (une boucle) garde sa case tant que sa parole est encore à moins d'une case et demie
       d'elle et qu'elle reste libre : les paroles voisines qui bougent un peu pour faire de la place ne font plus sauter leur
       anneau d'une case — 59 tuiles se retournaient jusqu'à 13 cases de la dalle. La mémoire suit la Toile vivante. */
    var placeAv = _bobPlace && _bobPlace.c === c ? _bobPlace : null, placeNv = { c: c, a: {}, b: {} };
    function libreEn(gi, gj) { for (var da = -1; da <= 1; da++) for (var db = -1; db <= 1; db++) if (pris[(gi + da) + '|' + (gj + db)]) return false; return true; }
    function poseAnneau(gi, gj, p) { pris[gi + '|' + gj] = 1; anneau[gi + '|' + gj] = p; placeNv.a[p.k] = [gi, gj];
      tourne[(gi - 1) + ',' + (gj - 1)] = 1; tourne[gi + ',' + (gj - 1)] = 0; tourne[(gi - 1) + ',' + gj] = 0; tourne[gi + ',' + gj] = 1; }
    for (i = 0; i < ordre.length; i++) {
      var p = ordre[i]; if (!_promesse(p.s)) continue;
      var bi = Math.round(p.x / c), bj = Math.round(p.y / c), fait = false;
      var av = placeAv && placeAv.a[p.k];
      if (av && Math.abs(av[0] - p.x / c) <= 1.5 && Math.abs(av[1] - p.y / c) <= 1.5 && libreEn(av[0], av[1])) { poseAnneau(av[0], av[1], p); continue; }
      for (var rr = 0; rr <= 2 && !fait; rr++) for (var a = -rr; a <= rr && !fait; a++) for (var b = -rr; b <= rr && !fait; b++) {
        if (Math.max(Math.abs(a), Math.abs(b)) !== rr) continue;
        var gi = bi + a, gj = bj + b, libre = true;
        for (var da = -1; da <= 1 && libre; da++) for (var db = -1; db <= 1; db++) if (pris[(gi + da) + '|' + (gj + db)]) { libre = false; break; }
        if (!libre) continue;
        poseAnneau(gi, gj, p);
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
      var bav = placeAv && placeAv.b[p2.k]; placeNv.b[p2.k] = [];
      if (bav) for (var bq = 0; bq < bav.length && nb; bq++) { var hb = bav[bq];
        if (Math.abs(hb[0] - p2.x / c) <= 3.5 && Math.abs(hb[1] - p2.y / c) <= 3.5 && ix.owner(hb[0] * c, hb[1] * c) === p2 && libreEn(hb[0], hb[1])) {
          pris[hb[0] + '|' + hb[1]] = 1; boucle[hb[0] + '|' + hb[1]] = p2; placeNv.b[p2.k].push(hb);
          tourne[(hb[0] - 1) + ',' + (hb[1] - 1)] = 1; tourne[hb[0] + ',' + (hb[1] - 1)] = 0; tourne[(hb[0] - 1) + ',' + hb[1]] = 0; tourne[hb[0] + ',' + hb[1]] = 1; nb--; } }
      for (var r2 = 1; r2 <= 3 && nb; r2++) {
        var cand = [];
        for (var a2 = -r2; a2 <= r2; a2++) for (var b2 = -r2; b2 <= r2; b2++) if (Math.max(Math.abs(a2), Math.abs(b2)) === r2) cand.push([ci + a2, cj + b2]);
        for (var q2 = 0; q2 < cand.length && nb; q2++) {
          var cc = cand[(q2 + rot) % cand.length], hi = cc[0], hj = cc[1], ok = true;
          // la boucle reste chez sa promesse : son centre doit appartenir à la cellule
          if (ix.owner(hi * c, hj * c) !== p2) continue;
          for (var ea = -1; ea <= 1 && ok; ea++) for (var eb = -1; eb <= 1; eb++) if (pris[(hi + ea) + '|' + (hj + eb)]) { ok = false; break; }
          if (!ok) continue;
          pris[hi + '|' + hj] = 1; boucle[hi + '|' + hj] = p2; placeNv.b[p2.k].push([hi, hj]);
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
    /* ⚑ v56 (Tom, 25 sept. 2026) — « TU TRICHES : une image fixe de fils et une onde de couleur qui passe dessous comme sous un
       pochoir. Chaque élément a son propre comportement. C'est une toile qui file : les fils bougent, les couleurs suivent les
       fils, chacune vers sa direction, seulement là où c'est concerné. Une dalle arrive : un anneau apparaît à sa place, les fils
       voisins se tirent pour lui faire de la place, la couleur coule sur ces fils-là. Et multicolore, comme le PDF. »
       Chaque ARC est un élément :
       1 · il se DÉFORME s'il est dans le champ du mouvement (la toile se tire autour de la dalle qui arrive, se referme autour de
           celle qui part, et file d'un léger tour) — un champ continu : deux arcs qui se touchent gardent leur point commun ;
           hors du champ il reste l'arc exact, immobile ;
       2 · s'il change de couleur, la nouvelle COULE le long de lui, depuis le bout par où elle arrive, À SON TOUR — le tour se
           compte en ARCS le long des fils depuis l'anneau (de proche en proche), pas en distance à vol d'oiseau ;
       3 · s'il est l'anneau d'une dalle qui naît, il GRANDIT depuis son centre, pendant que les fils qui passaient là se retirent.
       Couleurs : sous Ingénu, les fils prennent la couleur de palette figée de leur cellule (multicolore, comme la genèse) ;
       l'anneau d'une parole garde sa nature. */
    var P4 = _pal(), ING = _ingenu() && P4;
    function couleurFil(p, prBord) {
      var base = (ING && p.s.ci != null) ? P4[p.s.ci % 4] : cOf(p.s, now);
      if (!prBord) return base;
      if (ING && p.s.ci != null) return P4[(p.s.ci + 1 + (p.k % 3)) % 4];
      return _rampe(p.s, now)[1 + (p.k % 3)];
    }
    // le moment : où est la dalle qui arrive (ou part), et depuis quand
    var T0 = TRb ? TRb.t0 : 0, tt = TRb ? (now - T0) / 1000 : 0, KIND = TRb ? TRb.kind : null, NEUVE = null;
    if (TRb) for (var qn = 0; qn < P.length; qn++) { var sq = P[qn].s; if (sq.t0 != null && sq.part == null && now - sq.t0 < 2400 && _promesse(sq)) { if (!NEUVE || sq.t0 > NEUVE.s.t0) NEUVE = P[qn]; } }
    var CX = NEUVE ? NEUVE.x : OX, CY = NEUVE ? NEUVE.y : OY;
    var champ = null;
    if (TRb && CX != null) {
      var tau = KIND === 'depart' ? 0.32 : 0.3, amp = (KIND === 'depart' ? -0.42 : 0.6) * c, Rf = c * 1.6;
      var At = amp * (tt / tau) * Math.exp(1 - tt / tau);
      var sgn = (TRb.n & 1) ? 1 : -1;
      /* ⚑ v58 (Tom : « encore un effet d'onde, goutte d'eau, cheap — supprime-le ») : la déformation radiale autour de la dalle
         EST cette goutte d'eau. Supprimée : aucun fil ne se déforme plus ; seules les tuiles tournent sur leur axe. */
      champ = null;
    }
    function depl(x, y) {
      var dx = x - CX, dy = y - CY, r = Math.sqrt(dx * dx + dy * dy); if (r < 1e-6) return [x, y];
      var q = r / champ.R, gq = q * Math.exp(0.5 * (1 - q * q)), m = champ.A * gq, ux = dx / r, uy = dy / r;
      return [x + ux * m - uy * m * champ.sw, y + uy * m + ux * m * champ.sw];
    }
    function touche(A) { return champ && Math.hypot(A[0] - CX, A[1] - CY) < champ.lim; }
    // un morceau d'arc [f0, f1], au rayon r, déformé si le champ le touche ; e : raccord le long de la tangente
    function morceau(T, A, r, f0, f1, e) {
      var a0 = A[2] + (A[3] - A[2]) * f0, a1 = A[2] + (A[3] - A[2]) * f1;
      if (a1 - a0 < 1e-3) return;
      if (!touche(A)) {
        if (e && f0 === 0 && f1 === 1) { _arcRaccord(T, A, r, e); return; }
        T.moveTo(A[0] + Math.cos(a0) * r, A[1] + Math.sin(a0) * r); T.arc(A[0], A[1], r, a0, a1); return;
      }
      var n = Math.max(3, Math.ceil((a1 - a0) / 0.12)), pts = [];
      for (var z = 0; z <= n; z++) { var a = a0 + (a1 - a0) * z / n; pts.push(depl(A[0] + Math.cos(a) * r, A[1] + Math.sin(a) * r)); }
      var ee = e || 0, p0 = pts[0], p1 = pts[1], L0 = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]) || 1, pn = pts[n], pm = pts[n - 1], Ln = Math.hypot(pn[0] - pm[0], pn[1] - pm[1]) || 1;
      T.moveTo(p0[0] - (p1[0] - p0[0]) / L0 * ee, p0[1] - (p1[1] - p0[1]) / L0 * ee);
      for (z = 0; z <= n; z++) T.lineTo(pts[z][0], pts[z][1]);
      T.lineTo(pn[0] + (pn[0] - pm[0]) / Ln * ee, pn[1] + (pn[1] - pm[1]) / Ln * ee);
    }
    var lots = {}, nouveaux = [], naissants = [];
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
        var vk = Math.round(A[0] / c) + '|' + Math.round(A[1] / c), dalle = !!anneau[vk], sienne = anneau[vk] || boucle[vk];
        var bord = n.d1 / (n.d1 + n.d2) > 0.42, col;
        if (dalle && anneau[vk] === n.p) col = bord ? couleurFil(n.p, true) : cOf(n.p.s, now);   // l'anneau d'une parole : sa nature (et ses quartiers de bord)
        else col = couleurFil(n.p, bord);
        if (_rec && sienne) { var exr = dalle ? extra : 0; _note(sienne.k, { A: A, r: c / 2 - exr / 2, w: th + exr, e: th * 0.05, col: col, dalle: dalle }); }
        if (EBn) {
          var kb = ti + ',' + tj + ',' + m, sgb = f + '|' + (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + '|' + (dalle ? 1 : 0);
          var eb0 = EB ? EB[kb] : null, nb0 = { sg: sgb, A: A, col: col, dalle: dalle, an: eb0 && eb0.an, tk: ti + ',' + tj, tc: [x + c / 2, y + c / 2], f: f };
          if (EB && eb0 && eb0.sg !== sgb && !nb0.an) {
            var ne = dalle && anneau[vk] && anneau[vk].s.t0 != null && now - anneau[vk].s.t0 < 1500 && !eb0.dalle;
            nb0.an = { t: null, de: eb0, ne: ne, t0: ne ? anneau[vk].s.t0 : null };
            nouveaux.push(nb0);
          }
          if (nb0.an && nb0.an.t != null && now - nb0.an.t >= (nb0.an.d || BOB_D) && !nb0.an.ne) nb0.an = null;
          if (nb0.an && nb0.an.ne && now - nb0.an.t0 >= 900) nb0.an = null;
          if (nb0.an && nb0.an.de && nb0.an.de.an) nb0.an.de = { A: nb0.an.de.A, col: nb0.an.de.col, dalle: nb0.an.de.dalle, sg: nb0.an.de.sg };
          EBn[kb] = nb0;
          if (nb0.an) { (nb0.an.ne ? naissants : anb).push(nb0); continue; }
        }
        var key = (col[0] | 0) + ',' + (col[1] | 0) + ',' + (col[2] | 0) + '|' + (dalle ? 1 : 0);
        var L = lots[key]; if (!L) L = lots[key] = { col: col, dalle: dalle, a: [] };
        L.a.push(A);
      }
    }
    /* ⚑ v57 (Tom : « supprime l'effet de goutte d'eau qui se propage — c'est une onde ») — le tour de chaque arc se comptait de
       proche en proche depuis l'anneau : un front. Chaque arc concerné part maintenant à SON moment (tiré de sa clé, 0 à 420 ms),
       dans SON sens (tiré de sa clé) ; aucun ordre de distance. */
    /* ⚑ v58 (Tom : « faut que les lignes fils concernées aient la couleur à différents segments, traversés dans le sens »). Un arc
       n'est qu'un quart de cercle : un train de couleurs posé sur un arc seul faisait des confettis. Les arcs qui changent sont
       d'abord RELIÉS EN FILS (bout à bout), et le train parcourt chaque FIL d'un bout à l'autre ; puis la nouvelle couleur le
       gagne par ses deux bouts et se referme. Chaque fil a son moment et son sens, tirés de sa clé — aucun ordre de distance. */
    if (nouveaux.length) {
      var R2 = c / 2, bouts = {}, cleP = function (px, py) { return Math.round(px / c * 8) + ',' + Math.round(py / c * 8); };
      for (var u1 = 0; u1 < nouveaux.length; u1++) { var Au = nouveaux[u1].A;
        var E = [[Au[0] + Math.cos(Au[2]) * R2, Au[1] + Math.sin(Au[2]) * R2], [Au[0] + Math.cos(Au[3]) * R2, Au[1] + Math.sin(Au[3]) * R2]]; nouveaux[u1].E = E;
        for (var e1 = 0; e1 < 2; e1++) { var kp = cleP(E[e1][0], E[e1][1]); (bouts[kp] = bouts[kp] || []).push([u1, e1]); } }
      var voisin = function (u, e) { var kp = cleP(nouveaux[u].E[e][0], nouveaux[u].E[e][1]), L = bouts[kp]; for (var z = 0; z < L.length; z++) if (L[z][0] !== u) return L[z]; return null; };
      var fait = new Array(nouveaux.length), PLa = _pal();
      var ordreU = []; for (u1 = 0; u1 < nouveaux.length; u1++) ordreU.push(u1);
      ordreU.sort(function (x, y) { return (voisin(x, 0) && voisin(x, 1) ? 1 : 0) - (voisin(y, 0) && voisin(y, 1) ? 1 : 0); });   // d'abord les bouts de fil
      for (var oi = 0; oi < ordreU.length; oi++) {
        var st = ordreU[oi]; if (fait[st]) continue;
        // on part par le bout libre (s'il y en a un) et on suit le fil
        var ent = voisin(st, 0) ? 1 : 0, chaine = [], cu = st, eIn = ent;
        if (!voisin(st, 0) && !voisin(st, 1)) eIn = 0; else if (!voisin(st, 0)) eIn = 0; else if (!voisin(st, 1)) eIn = 1; else eIn = 0;
        while (cu != null && !fait[cu]) { fait[cu] = 1; chaine.push([cu, eIn]); var nx = voisin(cu, 1 - eIn); if (!nx || fait[nx[0]]) break; cu = nx[0]; eIn = nx[1]; }
        var cl = chaine.length, hC = _fnv('f' + nouveaux[chaine[0][0]].A.join(',') + cl), rev = ((hC >>> 7) & 1) === 1;
        var dC = Math.min(2000, 900 + 180 * cl), tC = now + (hC % 1000) / 1000 * Math.max(0, 2300 - dC - 60) * 0.35;
        var cn = nouveaux[chaine[0][0]].col, acs = [];
        if (PLa) for (var ia = 0; ia < 4; ia++) { var ca = PLa[(ia + (hC >>> 3)) % 4]; if (Math.abs(ca[0] - cn[0]) + Math.abs(ca[1] - cn[1]) + Math.abs(ca[2] - cn[2]) > 60) acs.push(ca); }
        for (var ci2 = 0; ci2 < cl; ci2++) { var an2 = nouveaux[chaine[ci2][0]].an;
          an2.t = tC; an2.d = dC; an2.cl = cl; an2.pos = rev ? cl - 1 - ci2 : ci2; an2.dir = (chaine[ci2][1] === 0) !== rev; an2.acs = acs.slice(0, 3); }
      }
    }
    g.save(); g.lineCap = 'butt';
    for (var k2 in lots) {
      var L2 = lots[k2];
      // la bobine d'une promesse garde son diamètre extérieur et s'épaissit vers le centre
      var ex = L2.dalle ? extra : 0, rr2 = c / 2 - ex / 2;
      g.strokeStyle = _rgb(L2.col); g.lineWidth = th + ex;
      g.beginPath();
      for (var z = 0; z < L2.a.length; z++) morceau(g, L2.a[z], rr2, 0, 1, th * 0.05);
      g.stroke();
    }
    /* 2 bis · UNE TUILE QUI SE RETOURNE TOURNE : ses deux fils pivotent d'un quart de tour autour de son centre (le quart de tour
       d'une tuile de Truchet EST l'autre orientation), la nouvelle couleur coulant sur eux ; au bout, ils sont exactement à leur
       nouvelle place. (Avant : l'ancien fil se retirait pendant qu'un autre poussait ailleurs — des pointillés.) */
    var parTuile = {}, restent = [];
    for (var zt = 0; zt < anb.length; zt++) { var it = anb[zt], od0 = it.an.de;
      if (od0 && od0.sg && od0.sg.charAt(0) !== String(it.f)) (parTuile[it.tk] = parTuile[it.tk] || []).push(it); else restent.push(it); }
    for (var tk in parTuile) {
      var G = parTuile[tk], tq = 1e18; for (var zg = 0; zg < G.length; zg++) tq = Math.min(tq, G[zg].an.t);
      var ph = Math.max(0, Math.min(1, (now - tq) / 900)), qq = ph * ph * (3 - 2 * ph), th0 = qq * Math.PI / 2, cs0 = Math.cos(th0), sn0 = Math.sin(th0), TC = G[0].tc;
      for (zg = 0; zg < G.length; zg++) {
        var oA = G[zg].an.de.A, ocx = oA[0] - TC[0], ocy = oA[1] - TC[1];
        var Ar = [TC[0] + ocx * cs0 - ocy * sn0, TC[1] + ocx * sn0 + ocy * cs0, oA[2] + th0, oA[3] + th0];
        // la couleur visée : celle du nouveau fil qu'occupera ce fil au bout du quart de tour
        var fx = TC[0] - ocy, fy = TC[1] + ocx, cible = G[zg];
        for (var zh = 0; zh < G.length; zh++) if (Math.abs(G[zh].A[0] - fx) < 0.5 && Math.abs(G[zh].A[1] - fy) < 0.5) cible = G[zh];
        var dO2 = G[zg].an.de.dalle ? extra : 0, rO2 = c / 2 - dO2 / 2;
        g.strokeStyle = _rgb(G[zg].an.de.col); g.lineWidth = th + dO2; g.beginPath(); morceau(g, Ar, rO2, 0, 1, th * 0.05); g.stroke();
        if (qq > 0) { g.strokeStyle = _rgb(cible.col); g.beginPath(); if (G[zg].an.inv) morceau(g, Ar, rO2, 1 - qq, 1); else morceau(g, Ar, rO2, 0, qq); g.stroke(); }
      }
    }
    anb = restent;
    window._bobTuiles = { n: Object.keys(parTuile).length, d: Object.keys(parTuile).map(function (k) { var T2 = parTuile[k][0].tc; return CX != null ? +(Math.hypot(T2[0] - CX, T2[1] - CY) / c).toFixed(1) : -1; }) };
    /* 2 · LA COULEUR VOYAGE DANS LE FIL (v57, Tom : « un fil concerné porte plusieurs segments de couleur différents. La couleur
       circule le long du fil, dans son sens, puis revient par l'autre bout en même temps, et tout se stabilise et s'emboîte. Le fil
       est le chemin, la couleur le parcourt. ») — pour chaque arc, indépendamment :
       · deux segments d'autres tons de la palette entrent par un bout et parcourent le fil jusqu'à l'autre ;
       · la nouvelle couleur gagne le fil par LES DEUX BOUTS à la fois, derrière eux, et se referme au milieu ;
       · à la fin, le fil n'a plus qu'une couleur : la sienne. */
    for (var zb = 0; zb < anb.length; zb++) {
      var nb1 = anb[zb], o1 = nb1.an.de, an3 = nb1.an, D3 = an3.d || BOB_D, q = (now - an3.t) / D3;
      var A1 = nb1.A, exN = nb1.dalle ? extra : 0, wN = th + exN, rN = c / 2 - exN / 2, colO = o1 ? o1.col : nb1.col;
      var cl3 = an3.cl || 1, p0 = an3.pos || 0, dir = an3.dir !== false;
      // un intervalle [s0, s1] du FIL (en arcs) → le morceau correspondant de CET arc
      function part(s0, s1, col) { var f0 = Math.max(0, s0 - p0), f1 = Math.min(1, s1 - p0); if (f1 - f0 < 0.004) return;
        g.strokeStyle = _rgb(col); g.beginPath(); if (dir) morceau(g, A1, rN, f0, f1); else morceau(g, A1, rN, 1 - f1, 1 - f0); g.stroke(); }
      g.lineWidth = wN;
      part(0, cl3, colO);                                                    // le fil, dans son ancienne couleur
      if (q <= 0) continue;
      q = Math.min(1, q); var qs = q * q * (3 - 2 * q), acs = an3.acs || [], TL = 1.1;
      var head = -0.2 + (cl3 + acs.length * TL + 0.2) * Math.min(1, qs * 1.3);   // le train de couleurs parcourt le fil
      for (var sgi = 0; sgi < acs.length; sgi++) part(head - (sgi + 1) * TL, head - sgi * TL, acs[sgi]);
      var e = Math.max(0, (qs - 0.42) / 0.58); e = e * e * (3 - 2 * e) * cl3 / 2;   // la nouvelle couleur, par les deux bouts du fil
      if (e > 0) { part(0, e + 0.002, nb1.col); part(cl3 - e - 0.002, cl3, nb1.col); }
    }
    // 3 · l'anneau qui naît : il grandit depuis son centre, les fils qui passaient là se retirent
    for (var zn = 0; zn < naissants.length; zn++) {
      var nn = naissants[zn], qn2 = Math.max(0, Math.min(1, (now - nn.an.t0 - 60) / 700)); qn2 = qn2 * qn2 * (3 - 2 * qn2);
      var od = nn.an.de; if (od && qn2 < 1) { var exd = od.dalle ? extra : 0; g.strokeStyle = _rgb(od.col); g.lineWidth = th + exd; g.beginPath(); morceau(g, od.A, c / 2 - exd / 2, qn2 * 0.5, 1 - qn2 * 0.5); g.stroke(); }
      if (qn2 > 0.01) { var exn = extra, wn = (th + exn) * qn2, rn = (c / 2 - exn / 2) * qn2; g.strokeStyle = _rgb(nn.col); g.lineWidth = wn; g.beginPath(); morceau(g, nn.A, rn, 0, 1, th * 0.05 * qn2); g.stroke(); }
    }
    if (EBn) _bobEtat = TRb ? EBn : EBn;
    if (EBn) window._bobEtatPub = EBn;   // publié (mesure)
    if (viveb) _bobPlace = placeNv;
    /* publié : un juge lit la composition, pas les pixels (§7) */
    if (viveb) window._bobAnim = { n: anb.length + naissants.length, coulent: anb.length, naissent: naissants.length, champ: champ ? +(champ.A / c).toFixed(3) : 0, sp: sp,
      cles: anb.concat(naissants).map(function (a) { return a.A[0].toFixed(1) + ',' + a.A[1].toFixed(1) + ',' + a.A[2].toFixed(2); }), dist: [] };
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
  /* ⚑ v43 (Tom, 24 sept. 2026) — LA TRANSITION DE RITOURNELLE. « Les coulées se tirent comme si des doigts les étiraient
     depuis l'extérieur de l'écran, puis se reforment en suivant leurs contours. »
     Trois à quatre DOIGTS, posés hors de l'écran (le premier dans la direction de la dalle qui arrive), tirent la Toile vers
     eux : un champ de déplacement continu, nul au centre de l'écran, plein au bord, étroit en travers — les coulées voisines
     s'étirent ensemble, comme une étoffe. Le bord d'une coulée est tiré en entier, ses strates intérieures moins (centre
     ancré : la coulée S'ÉTIRE, elle ne glisse pas) et EN RETARD (elles suivent le contour). Puis les doigts lâchent : un
     ressort amorti, un léger rebond vers l'intérieur, et chaque coulée se reforme dans sa cellule — que la dalle neuve est
     en train de pousser. Tout est tiré de la clé de la Toile et du numéro de la transition : jamais de hasard.
     Rien n'est gardé d'une image à l'autre : le moteur tient le moment (`env.trans`), la géométrie se recalcule. */
  var RIT_PULL = 460, RIT_TAU = 260, RIT_PER = 760, RIT_LAG = 85;
  var RIT_BANDE = 0.34, RIT_MIN = 2, RIT_MAX = 5, RIT_PART = 0.34;   // v63 : une coulée occupe de 66 % à 100 % de sa cellule   // v63 : la largeur d'une strate, en unité de matière ; bornes du nombre de strates
  function _ritA(t) {
    if (t <= 0) return 0;
    if (t < RIT_PULL) { var u = 1 - t / RIT_PULL; return 1 - u * u * u; }
    var r = t - RIT_PULL; return Math.exp(-r / RIT_TAU) * Math.cos(r * 6.283185307179586 / RIT_PER);
  }
  function _ritDoigts(T, x0, y0, x1, y1, sp) {
    var R = _lcg((((typeof cleToile === 'number' ? cleToile : 7) ^ Math.imul(T.n | 0, 2654435761)) >>> 0) || 1);
    var cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, hw = Math.max(1, (x1 - x0) / 2), hh = Math.max(1, (y1 - y0) / 2);
    var th0 = (T.x != null) ? Math.atan2(T.y - cy, T.x - cx) : R() * 6.283;
    var nF = 3 + (R() < 0.5 ? 1 : 0), out = [], m = Math.min(hw, hh);
    for (var f = 0; f < nF; f++) {
      var th = th0 + f * 6.283185307179586 / nF + (f ? (R() - 0.5) * 0.7 : 0);
      var ux = Math.cos(th), uy = Math.sin(th);
      var Rf = Math.min(Math.abs(ux) > 1e-6 ? hw / Math.abs(ux) : 1e9, Math.abs(uy) > 1e-6 ? hh / Math.abs(uy) : 1e9);
      out.push({ th: th, ux: ux, uy: uy, cx: cx, cy: cy, Rf: Rf, sg: m * (0.30 + R() * 0.16),
        amp: sp * (f ? 1.05 + R() * 0.45 : 1.7), dl: f ? 40 + R() * 150 : 0, rph: R() * 6.283, rot: 0.14 + R() * 0.16 });
    }
    return out;
  }
  function Rrit(now, x0, y0, x1, y1) {
    _sync();
    var ix = _idx(), P = ix.P, NA = 144;
    if (!P.length) return;
    var sp = _uGlobal(ix) * SP_U, RMAX = sp * 2.4;
    if (!env.trans && env.cible == null && env.vive) window._ritComp = [];
    // v43 : la transition (Toile vivante seulement)
    var TR = env.trans, tt = TR ? now - TR.t0 : -1, FG = null, trq = 0, WF = null;
    if (TR && tt < Rrit.transDur) {
      FG = _ritDoigts(TR, x0, y0, x1, y1, sp); WF = new Float64Array(FG.length * NA);
      // v44 : le passage au rayon continu ENTRE en 300 ms comme il sort en 350 — posé d'un coup, toutes les coulées bougeaient
      // de quelques pixels à la première image (11,8 niveaux sur la Toile entière)
      trq = Math.min(Math.max(0, tt) / 300, tt > Rrit.transDur - 350 ? Math.max(0, (Rrit.transDur - tt) / 350) : 1, 1); trq = trq * trq * (3 - 2 * trq);
    }
    window._ritTrans = FG ? { tt: Math.round(tt), n: TR.n, doigts: FG.length, trq: +trq.toFixed(3) } : null;   // v43 : publié (les juges lisent la composition, §7)
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
        // v44 : une voisine qui PART cesse peu à peu de borner la coulée (sa limite recule jusqu'à ne plus compter) —
        // sans quoi, au moment où le moteur la retire, toutes ses voisines sautaient d'un coup (mesuré : 4,3 niveaux à 631 ms)
        if (q.s.part != null) { var fq = Math.min(1, Math.max(0, (now - q.s.part) / 560)); fq = fq * fq * (3 - 2 * fq); t0 = t0 + (RMAX + dq - t0) * fq; }
        // v44 : et une voisine qui ARRIVE ne coupe la coulée que peu à peu (elle la tranchait d'un coup à la première image)
        else if (TR && q.s.t0 != null && now - q.s.t0 < 700) { var fa = Math.max(0, (now - q.s.t0) / 700); fa = fa * fa * (3 - 2 * fa); t0 = t0 + (RMAX + dq - t0) * (1 - fa); }
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
      var rj = R(), rings = 3;   // v63 : le nombre de strates suit la taille de la coulée (plus bas)
      for (a = 0; a < NA; a++) {
        var an = a / NA * 6.283;
        var m = 1 + Math.sin(an * h2[0] + h2[1]) * h2[2] + Math.sin(an * h3[0] + h3[1]) * h3[2] + Math.sin(an * h5[0] + h5[1]) * h5[2];
        var rv = ray(cx, cy, cs[a], sn[a]), stp = sp * 0.05;
        cr[a] = rv;
        var rq = stp * Math.max(1, Math.ceil(rv / stp) - 1);          // rayon marché de l'original : r ∈ [R − pas, R)
        // v43 : pendant une transition le pas de marche ferait frémir le bord à chaque image — on prend le rayon continu,
        // et on revient au rayon marché dans les 350 dernières ms (la coulée au repos est celle d'avant, au pixel)
        if (trq > 0) rq = rq + (Math.max(stp, rv - stp * 0.5) - rq) * trq;
        lim[a] = rq * (0.72 + 0.28 * m) - sp * 0.006;
      }
      var sm = lim;
      for (var pass = 0; pass < 8; pass++) {
        for (a = 0; a < NA; a++) tmp[a] = (sm[(a - 2 + NA) % NA] + 2 * sm[(a - 1 + NA) % NA] + 3 * sm[a] + 2 * sm[(a + 1) % NA] + sm[(a + 2) % NA]) / 9;
        var sw = sm; sm = tmp; tmp = sw;
      }
      // original : un pixel hors de sa cellule appartient à la voisine, dont la coulée ne l'atteint pas → la Toile respire
      for (a = 0; a < NA; a++) if (sm[a] > cr[a]) sm[a] = cr[a];
      /* ⚑ v63 (Tom, 27 sept.) — « des dalles variées, une Toile un peu moins chargée, des formes qui suivent » ; « la matière ne
         dézoome pas » (12 sept., v34 : uMat). Les strates avaient une LARGEUR proportionnelle à la cellule (3 à 5 par coulée,
         quelle que soit sa taille) : à 40 paroles tout rapetissait d'un coup. Elles ont maintenant une largeur FIXE (RIT_BANDE ×
         l'unité de matière) : une grande coulée en porte davantage, une petite moins. Le nombre est CONTINU (une strate naît du
         centre en grandissant quand la coulée grandit) : rien ne saute pendant une plantation. */
      /* la PART de sa cellule qu'occupe la coulée, tirée de sa clé : grandir les POIDS du moteur rapprochait les dalles (mesuré : 15
         paires à moins de 40 px à 40 paroles, contre 7) ; déborder de la cellule serait coupé net sur la fiche (dalle contenue). */
      var pk = 1 - RIT_PART * Math.pow(_lcg(p.k ^ 0x51e)(), 1.3); for (a = 0; a < NA; a++) sm[a] *= pk;
      var rmoy = 0; for (a = 0; a < NA; a++) rmoy += sm[a]; rmoy /= NA;
      var uB = (typeof env.uMat === 'number' && env.uMat > 0 ? env.uMat : sp) * RIT_BANDE;
      rings = rmoy / uB + (rj - 0.5); rings = rings < RIT_MIN ? RIT_MIN : rings > RIT_MAX ? RIT_MAX : rings;
      if (window._ritComp && !FG && env.cible == null) window._ritComp.push({ r: +rmoy.toFixed(1), n: +rings.toFixed(2) });
      // léger adoucissement après le rognage : efface les fripures sans toucher aux espaces ni aux formes
      for (var ps = 0; ps < 2; ps++) {
        for (a = 0; a < NA; a++) tmp[a] = (sm[(a - 1 + NA) % NA] + 2 * sm[a] + sm[(a + 1) % NA]) / 4;
        for (a = 0; a < NA; a++) sm[a] = tmp[a];
      }
      var RP = _rampe(p.s, now);
      // v43 : une dalle PARTIE (`part`, posé par le moteur) se retire dans sa cellule, du bord vers le centre
      // v44 : sur la Toile vivante, une coulée qui ARRIVE naît de rien (elle apparaissait d'un coup à 12 % de sa cellule)
      if (TR && p.s.t0 != null && now - p.s.t0 < 700 && p.s.part == null) { var fn = Math.max(0, (now - p.s.t0) / 700); fn = fn * fn * (3 - 2 * fn);
        for (a = 0; a < NA; a++) sm[a] *= fn;
        /* ⚑ v53 — au bord de l'écran, le centre de la cellule tombe hors du cadre (les rayons y vont jusqu'à RMAX) : la coulée
           naissait d'un point invisible. Pendant l'arrivée, elle grandit depuis le centre de sa partie VISIBLE (homothétie de
           centre V, rapport fn) — au repos (fn = 1), rien ne change. */
        var vx = 0, vy = 0; for (a = 0; a < NA; a += 9) { var ex2 = Math.min(x1, Math.max(x0, cx + cs[a] * cr[a])), ey2 = Math.min(y1, Math.max(y0, cy + sn[a] * cr[a])); vx += ex2; vy += ey2; }
        vx /= NA / 9; vy /= NA / 9; cx = vx + (cx - vx) * fn; cy = vy + (cy - vy) * fn; }
      if (p.s.part != null) { var fp = Math.min(1, Math.max(0, (now - p.s.part) / 560)); fp = 1 - fp * fp * (3 - 2 * fp);
        if (fp <= 0.01) { if (sm !== lim) tmp = sm; lim = new Float64Array(NA); continue; } for (a = 0; a < NA; a++) sm[a] *= fp; }
      // v43 : le poids de chaque doigt au bord de la coulée (une fois par coulée)
      // la coulée est prise ou non selon SA place (centre), et c'est le bord TOURNÉ vers le doigt qui part : une langue,
      // pas un glissement en bloc
      if (FG) for (var f = 0; f < FG.length; f++) {
        var D = FG[f], i2s = 1 / (2 * D.sg * D.sg);
        var bx = cx - D.cx, by = cy - D.cy, al = (bx * D.ux + by * D.uy) / D.Rf, pe = bx * D.uy - by * D.ux;
        var wc = al <= -0.15 ? 0 : Math.exp(-pe * pe * i2s) * Math.pow(Math.min(1, Math.max(0, al + 0.15) / 1.15), 1.2);
        for (a = 0; a < NA; a++) {
          var fa = cs[a] * D.ux + sn[a] * D.uy;
          WF[f * NA + a] = fa <= 0 || wc < 1e-4 ? 0 : wc * Math.pow(fa, 2.2);
        }
      }
      // v63 : les strates comptées depuis le BORD (jj = 0 dehors) — un nombre entier redonne exactement l'ancien dessin
      for (var jj = 0; jj < rings; jj++) {
        var sc = Math.pow((rings - jj) / rings, 1.25);
        g.fillStyle = _rgb(RP[(((-jj) % 4) + 4) % 4]);
        // v43 : chaque doigt, à SON heure — les strates intérieures en retard, étirées à proportion de leur rayon
        var DX = null, DY = null;
        if (FG) {
          DX = []; DY = [];
          var lag = jj * RIT_LAG, ks = Math.pow(sc, 0.9);
          for (var f2 = 0; f2 < FG.length; f2++) {
            var D2 = FG[f2], tf = tt - D2.dl - lag, Af = D2.amp * _ritA(tf) * ks;
            var ro = D2.th + Math.sin(D2.rph + tf * 0.0042) * D2.rot;
            DX.push(Af * Math.cos(ro)); DY.push(Af * Math.sin(ro));
          }
        }
        g.beginPath();
        for (a = 0; a < NA; a++) {
          var rr = Math.max(0, sm[a]) * sc, X = cx + cs[a] * rr, Y = cy + sn[a] * rr;
          if (DX) for (var f3 = 0; f3 < DX.length; f3++) { var wv = WF[f3 * NA + a]; if (wv > 1e-4) { X += DX[f3] * wv; Y += DY[f3] * wv; } }
          if (a === 0) g.moveTo(X, Y); else g.lineTo(X, Y);
        }
        g.closePath(); g.fill();
      }
      if (sm !== lim) { tmp = sm; } // les tampons tournent, rien à rendre
      lim = new Float64Array(NA);
    }
  }

  /* ---------- 5 · CABOCHON — les pierres polies ------------------------- */
  /* ⚑ v48 (Tom, 24 sept. 2026) — « ce design n'existe pas, on va le rajouter aux mondes gratuits, exactement comme il est ».
     Le dessin du moodboard de la célébration, figé : chaque parole est une cellule pondérée (la règle du moteur : la
     bissectrice décalée par les poids), arrondie aux coins, séparée de ses voisines par un JOUR où l'on voit le fond de la
     Toile. Une couleur par dalle (cOf), rien d'autre. Longueurs en fraction de l'écart entre graines : jour 0,09, rayon 0,17
     (relevés sur le moodboard : 9 px et 16 px pour un écart d'environ 100). Monde CONTENU : sa dalle seule est sa cellule
     (`env.cible`). Une dalle qui arrive naît de rien, une dalle qui part se retire vers son centre. */
  function _traceArrondi(T, p, r) {
    var n = p.length; T.beginPath();
    for (var i = 0; i < n; i++) {
      var a = p[(i - 1 + n) % n], b = p[i], c = p[(i + 1) % n];
      var l1 = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, l2 = Math.hypot(c[0] - b[0], c[1] - b[1]) || 1, rr = Math.min(r, l1 / 2, l2 / 2);
      var p1x = b[0] + (a[0] - b[0]) / l1 * rr, p1y = b[1] + (a[1] - b[1]) / l1 * rr, p2x = b[0] + (c[0] - b[0]) / l2 * rr, p2y = b[1] + (c[1] - b[1]) / l2 * rr;
      if (i === 0) T.moveTo(p1x, p1y); else T.lineTo(p1x, p1y);
      T.quadraticCurveTo(b[0], b[1], p2x, p2y);
    }
    T.closePath();
  }
  /* ⚑ v50 (Tom, 24 sept. 2026) — HALIN.
     · des dalles de tailles et de formes différentes : chaque dalle a un écart de poids stable, tiré de sa CLÉ (±0,16 u) ;
     · des jours légèrement inégaux : chaque jour a son épaisseur, tirée des clés de ses deux dalles (0,72 à 1,28 × le jour) —
       sans quoi on voit une mosaïque, pas un vivant ;
     · le retrait va au bout (la dalle qui part cède toute sa place avant d'être retirée) et le mouvement est doux :
       pas de poussée à l'arrivée, un ressort plus long (RD.halin : douce, omx, omw, partDur) ; l'impact est un souffle (0,6 %) ;
     · les bulles : de PETITS triangles aux coins arrondis, dans une jonction sur trois, orientés vers ses trois jours et
       rétrécis jusqu'à tenir dans l'espace libre mesuré (jamais tronqués) ; quelques rares bulles dans les jours.
     Tirage par les CLÉS (jamais la position), couleur d'une voisine, jamais dans une dalle seule. */
  var HAL_RET = 760;
  function _halPart(s, now) { if (s.part == null) return 0; var a = Math.min(1, Math.max(0, (now - s.part) / HAL_RET)); return a * a * (3 - 2 * a); }
  var _halBiais = {};
  function _halW(p, u) { var b = _halBiais[p.k]; if (b == null) { b = ((_fnv('b' + p.k) % 1000) / 1000 - 0.5); _halBiais[p.k] = b; } return p.w + b * u * 0.32; }
  function _halJour(p, q, jour) { var h = _fnv(p.k < q.k ? p.k + ':' + q.k : q.k + ':' + p.k); return jour * (0.72 + (h % 1000) / 1000 * 0.56); }
  var HAL_ARR = 900;
  function _halArr(s, now) { if (!env.trans || s.part != null || s.t0 == null) return 1; var a = (now - s.t0) / HAL_ARR; if (a >= 1) return 1; if (a <= 0) return 0; return a * a * (3 - 2 * a); }
  function _halFront(p, q, d, now, u) {
    var t = 0.5 * d + (_halW(p, u) - _halW(q, u)) * 0.5;
    if (t < d * 0.06) t = d * 0.06; if (t > d * 0.94) t = d * 0.94;
    var fp = _halPart(p.s, now), fq = _halPart(q.s, now);
    if (fp > 0) t *= (1 - fp);                                     // celle qui part cède sa place…
    if (fq > 0) t = d - (d - t) * (1 - fq) + fq * fq * fq * fq * d; // …et ses voisines la prennent, jusqu'au bout
    /* ⚑ v54 (Tom : « la dalle et les contours ne bougent pas à la même vitesse — elle apparaît plus vite que les jours qui
       l'entourent, ça dépasse ») — la dalle neuve grandissait par une mise à l'échelle À ELLE (800 ms) pendant que ses jours
       suivaient les graines. Elle naît maintenant PAR LA MÊME FRONTIÈRE que ses jours : un seul calcul, les deux côtés du jour
       bougent ensemble, par construction. */
    var ap = _halArr(p.s, now), aq = _halArr(q.s, now);
    if (ap < 1) t *= ap;
    if (aq < 1) t = d - (d - t) * aq;
    return t;
  }
  function _halCellule(p, vois, M, jour, now, u) {
    var poly = [[p.x - M, p.y - M], [p.x + M, p.y - M], [p.x + M, p.y + M], [p.x - M, p.y + M]];
    for (var v = 0; v < vois.length && poly.length > 2; v++) {
      var q = vois[v].p, d = vois[v].d; if (d <= 0) continue;
      var nx = (q.x - p.x) / d, ny = (q.y - p.y) / d, t = _halFront(p, q, d, now, u) - (jour ? _halJour(p, q, jour) : 0) / 2;
      poly = _clip(poly, p.x + nx * t, p.y + ny * t, nx, ny);
    }
    return poly;
  }
  // le contour arrondi, aplati — EXACTEMENT la géométrie de _traceArrondi
  function _halContour(p, r) {
    var n = p.length, o = [];
    for (var i = 0; i < n; i++) {
      var a = p[(i - 1 + n) % n], b = p[i], c = p[(i + 1) % n];
      var l1 = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, l2 = Math.hypot(c[0] - b[0], c[1] - b[1]) || 1, rr = Math.min(r, l1 / 2, l2 / 2);
      var p1x = b[0] + (a[0] - b[0]) / l1 * rr, p1y = b[1] + (a[1] - b[1]) / l1 * rr, p2x = b[0] + (c[0] - b[0]) / l2 * rr, p2y = b[1] + (c[1] - b[1]) / l2 * rr;
      for (var k = 0; k <= 4; k++) { var t = k / 4, u1 = 1 - t; o.push(u1 * u1 * p1x + 2 * u1 * t * b[0] + t * t * p2x, u1 * u1 * p1y + 2 * u1 * t * b[1] + t * t * p2y); }
    }
    o.push(o[0], o[1]);
    return o;
  }
  function _halRayon(ox, oy, dx, dy, C, lim) {
    var best = lim;
    for (var c = 0; c < C.length; c++) {
      var o = C[c].o;
      for (var i = 0; i + 3 < o.length; i += 2) {
        var ax = o[i], ay = o[i + 1], ex = o[i + 2] - ax, ey = o[i + 3] - ay, den = dx * ey - dy * ex;
        if (den > -1e-9 && den < 1e-9) continue;
        var wx = ax - ox, wy = ay - oy, s = (wx * ey - wy * ex) / den; if (s <= 0 || s >= best) continue;
        var uu = (wx * dy - wy * dx) / den; if (uu >= 0 && uu <= 1) best = s;
      }
    }
    return best;
  }
  function _halDedans(x, y, o) {
    var ins = false;
    for (var i = 0, j = o.length - 4; i + 1 < o.length - 2; j = i, i += 2) {
      var xi = o[i], yi = o[i + 1], xj = o[j], yj = o[j + 1];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) ins = !ins;
    }
    return ins;
  }
  function _halVoisines(ox, oy, lim, cells) {
    var C = [];
    for (var c = 0; c < cells.length; c++) { var b = cells[c].bb; if (b[0] > ox + lim || b[2] < ox - lim || b[1] > oy + lim || b[3] < oy - lim) continue; C.push(cells[c]); }
    for (var c2 = 0; c2 < C.length; c2++) if (_halDedans(ox, oy, C[c2].o)) return null;
    return C;
  }
  // un polygone convexe (triangle ou œuf) autour de (ox, oy) rétréci jusqu'à tenir dans l'espace libre, avec une marge
  function _halTient(ox, oy, pts, C, marge) {
    for (var e = 1; e > 0.3; e *= 0.85) {
      var ok = true, n = pts.length;
      for (var i = 0; i < n && ok; i++) {
        var a = pts[i], b = pts[(i + 1) % n];
        var ch = [[a[0] * e, a[1] * e], [(a[0] + b[0]) / 2 * e, (a[1] + b[1]) / 2 * e]];
        for (var k = 0; k < 2 && ok; k++) { var L = Math.hypot(ch[k][0], ch[k][1]) || 1e-6;
          if (_halRayon(ox, oy, ch[k][0] / L, ch[k][1] / L, C, L + marge * 2) < L + marge) ok = false; }
      }
      if (ok) return e;
    }
    return 0;
  }
  function _halCalme(p, u) {   // 1 quand la dalle est posée, 0 quand elle bouge ou naît ou part
    var s = p.s; if (s.part != null) return 0;
    var m = Math.hypot((s.tx != null ? s.tx : p.x) - p.x, (s.ty != null ? s.ty : p.y) - p.y) + 0.5 * Math.abs((s.wt != null ? s.wt : s.w) - s.w);
    var a = Math.min(1, Math.max(0, (m - u * 0.01) / (u * 0.05))); return 1 - a * a * (3 - 2 * a);
  }
  var _halMem = {}, _halT = 0, _halJourPub = 1;
  function Rhal(now, x0, y0, x1, y1) {
    _sync();
    var ix = _idx(), P = ix.P;
    if (!P.length) return;
    var u = _uGlobal(ix), jour = u * 0.09, rayon = u * 0.17, M = Math.max(W, H, u * 3), TR = env.trans, seule = env.cible != null;
    var cells = [];
    for (var i = 0; i < P.length; i++) {
      var p = P[i];
      if (seule && p.s.pid !== env.cible) continue;
      if (p.x < x0 - u * 3 || p.x > x1 + u * 3 || p.y < y0 - u * 3 || p.y > y1 + u * 3) continue;
      var vois = ix.near(p, 12), poly = _halCellule(p, vois, M, jour, now, u);
      if (seule && env.bords && poly.length > 2) { var BT = env.bords;
        poly = _clip(poly, BT[0], 0, -1, 0); if (poly.length > 2) poly = _clip(poly, BT[2], 0, 1, 0);
        if (poly.length > 2) poly = _clip(poly, 0, BT[1], 0, -1); if (poly.length > 2) poly = _clip(poly, 0, BT[3], 0, 1); }
      if (poly.length < 3) continue;
      /* v54 : ni mise à l'échelle à l'arrivée (la frontière s'en charge), ni rebond d'impact — il faisait bouger la dalle
         sans ses jours */
      var aP = _halArr(p.s, now), f = aP < 1 ? 0.999 : 1, sc = 1;
      /* du côté où la dalle neuve n'a pas de voisine (le bord de l'écran), aucune frontière ne la retient : un disque qui grandit
         avec elle la borne là — côté voisines, ce sont toujours les jours qui décident */
      if (aP < 1 && poly.length > 2) { var RA = aP * u * 2.2, NG = 20;
        for (var gq = 0; gq < NG && poly.length > 2; gq++) { var ga = gq / NG * 6.283185307179586, gnx = Math.cos(ga), gny = Math.sin(ga);
          poly = _clip(poly, p.x + gnx * RA, p.y + gny * RA, gnx, gny); }
        if (poly.length < 3) continue; }
      /* ⚑ v53 (Tom : « quand une dalle apparaît au bord de l'écran, l'animation bugue ») — une cellule au bord s'étend jusqu'à la
         borne M, loin hors de l'écran : son centre y tombait, la dalle grandissait depuis un point invisible et n'entrait dans
         le cadre que tard, d'un bloc. Elle grandit maintenant depuis le centre de sa partie VISIBLE. */
      if (sc < 1) { var vis = poly; vis = _clip(vis, x0, 0, -1, 0); if (vis.length > 2) vis = _clip(vis, x1, 0, 1, 0); if (vis.length > 2) vis = _clip(vis, 0, y0, 0, -1); if (vis.length > 2) vis = _clip(vis, 0, y1, 0, 1);
        var cc = _cent(vis.length > 2 ? vis : poly); poly = poly.map(function (q2) { return [cc[0] + (q2[0] - cc[0]) * sc, cc[1] + (q2[1] - cc[1]) * sc]; }); }
      cells.push({ p: p, poly: poly, f: f, vois: vois, r: rayon * Math.min(1, f + 0.2), part: p.s.part != null });
    }
    cells.sort(function (a1, b1) { return (b1.part ? 1 : 0) - (a1.part ? 1 : 0); });
    for (var c2 = 0; c2 < cells.length; c2++) {
      var D = cells[c2]; if (D.f <= 0.01) continue;
      g.fillStyle = _rgb(cOf(D.p.s, now)); _traceArrondi(g, D.poly, D.r); g.fill();
    }
    if (seule) return;
    for (var c3 = 0; c3 < cells.length; c3++) { var E = cells[c3], o = _halContour(E.poly, E.r), bx0 = 1e9, by0 = 1e9, bx1 = -1e9, by1 = -1e9;
      for (var k = 0; k < o.length; k += 2) { if (o[k] < bx0) bx0 = o[k]; if (o[k] > bx1) bx1 = o[k]; if (o[k + 1] < by0) by0 = o[k + 1]; if (o[k + 1] > by1) by1 = o[k + 1]; }
      E.o = o; E.bb = [bx0, by0, bx1, by1]; }
    var vus = {}; window._halBulles = [];   /* publié : un juge lit les bulles, pas les pixels (§7) */
    /* ⚑ v53 (Tom : « les bulles ont des bugs d'affichage ») — mesuré : 18 bulles SAUTAIENT en trois mouvements (deux plantations,
       un retrait) — elles apparaissaient ou disparaissaient d'une image à l'autre, à pleine taille : des seuils francs (la place,
       le coin, le centre) et une clé qui change quand le voisinage change. Chaque bulle garde maintenant la MÉMOIRE de sa taille
       affichée, qui rejoint sa cible en ~0,3 s : elle naît en grandissant et, quand ses conditions tombent, elle rétrécit sur
       place au lieu de disparaître. Tant qu'une bulle n'a pas rejoint sa taille, Halin demande des images (`_mondeEncore`). */
    var dtB = _halT ? Math.min(0.1, Math.max(0, (now - _halT) / 1000)) : 0.016; _halT = now; _halJourPub = jour;
    var kE = 1 - Math.exp(-dtB / 0.11), vuB = {};
    function bulle(cle0, x, y, rel, r0, col, cible) {
      var m = _halMem[cle0]; if (!m) m = _halMem[cle0] = { e: 0 };
      m.e += (cible - m.e) * kE; if (Math.abs(cible - m.e) > 0.01) window._mondeEncore = true;
      /* la TAILLE PROPRE aussi est lissée : quand les coins autour d'une jonction changent, sa géométrie saute d'une image à l'autre */
      if (m.r == null) m.r = r0; else m.r += (r0 - m.r) * kE;
      var sR = r0 > 1e-6 ? m.r / r0 : 1;
      m.k = cle0; m.x = x; m.y = y; m.rel = rel.map(function (q6) { return [q6[0] * sR, q6[1] * sR]; }); m.col = col; vuB[cle0] = 1;
      trace(m);
    }
    function trace(m) {
      if (m.e < 0.02) return;
      g.fillStyle = m.col; _traceArrondi(g, m.rel.map(function (q5) { return [m.x + q5[0] * m.e, m.y + q5[1] * m.e]; }), m.r * m.e); g.fill();
      var ar = 0, lg = 0; for (var q7 = 0; q7 < m.rel.length; q7++) { var A7 = m.rel[q7], B7 = m.rel[(q7 + 1) % m.rel.length]; ar += A7[0] * B7[1] - B7[0] * A7[1]; lg = Math.max(lg, Math.hypot(A7[0], A7[1])); }
      window._halBulles.push({ k: m.k, x: m.x, y: m.y, t: m.r * m.e, j: _halJourPub, a: Math.abs(ar) / 2 * m.e * m.e, l: lg * m.e });
    }
    for (var c = 0; c < cells.length; c++) {
      var C0 = cells[c], p0 = C0.p; if (C0.part || C0.f < 1) continue;
      var calme0 = _halCalme(p0, u); if (calme0 <= 0.01) continue;
      // (1) aux jonctions QUI ONT DE LA PLACE (une sur trois) : un triangle aux coins arrondis qui ÉPOUSE l'espace. Chacune des trois dalles
      //     présente un coin arrondi (centre Ci, rayon ri) ; chaque côté de la bulle est parallèle à ce coin, à un jeu fixe :
      //     {x : (x − Ci)·ni ≥ ri + jeu}, ni pointant du coin vers la jonction. Une dalle est convexe, elle est tout entière de
      //     l'autre côté de cette droite : la bulle ne peut pas la toucher. Ses pointes filent dans les jours, bornées.
      var brut = _halCellule(p0, C0.vois, M, 0, now, u);
      for (var z = 0; z < brut.length; z++) {
        var J = brut[z]; if (J[0] < 0 || J[1] < 0 || J[0] > W || J[1] > H) continue;
        var tri = [[Math.hypot(J[0] - p0.x, J[1] - p0.y) - _halW(p0, u), p0]];
        for (var n = 0; n < C0.vois.length; n++) { var ov = C0.vois[n].p; tri.push([Math.hypot(J[0] - ov.x, J[1] - ov.y) - _halW(ov, u), ov]); }
        tri.sort(function (a1, b1) { return a1[0] - b1[0]; }); if (tri.length < 3) continue;
        var cle = [tri[0][1].k, tri[1][1].k, tri[2][1].k].sort().join('|'); if (vus[cle]) continue; vus[cle] = 1;
        var h = _fnv('a' + cle); if (h % 3 !== 0) continue;
        var calme = Math.min(calme0, _halCalme(tri[1][1], u), _halCalme(tri[2][1], u)); if (calme <= 0.01) continue;
        var coins = [], ok = true;
        for (var e2 = 0; e2 < 3 && ok; e2++) {
          var Ce = null; for (var y = 0; y < cells.length; y++) if (cells[y].p === tri[e2][1]) { Ce = cells[y]; break; }
          if (!Ce) { ok = false; break; }
          var Pl = Ce.poly, NP = Pl.length, bi = -1, bd = 1e18;
          for (var y2 = 0; y2 < NP; y2++) { var dd = Math.hypot(Pl[y2][0] - J[0], Pl[y2][1] - J[1]); if (dd < bd) { bd = dd; bi = y2; } }
          if (bd > jour * 2.5) { ok = false; break; }
          var Va = Pl[(bi - 1 + NP) % NP], Vb = Pl[bi], Vc = Pl[(bi + 1) % NP];
          var l1 = Math.hypot(Va[0] - Vb[0], Va[1] - Vb[1]) || 1, l2 = Math.hypot(Vc[0] - Vb[0], Vc[1] - Vb[1]) || 1, rr = Math.min(Ce.r, l1 / 2, l2 / 2);
          var ax = (Va[0] - Vb[0]) / l1, ay = (Va[1] - Vb[1]) / l1, cx2 = (Vc[0] - Vb[0]) / l2, cy2 = (Vc[1] - Vb[1]) / l2;
          var bx = ax + cx2, by = ay + cy2, bl = Math.hypot(bx, by) || 1e-6, demi = Math.acos(Math.max(-1, Math.min(1, ax * cx2 + ay * cy2))) / 2;
          var dc = rr / Math.max(0.05, Math.sin(demi)), Cx = Vb[0] + bx / bl * dc, Cy = Vb[1] + by / bl * dc;
          var nx0 = J[0] - Cx, ny0 = J[1] - Cy, nl = Math.hypot(nx0, ny0) || 1e-6;
          coins.push({ cx: Cx, cy: Cy, r: rr, nx: nx0 / nl, ny: ny0 / nl, s: tri[e2][1].s });
        }
        if (!ok) continue;
        var jeu = jour * 0.32, poly = [[J[0] - M, J[1] - M], [J[0] + M, J[1] - M], [J[0] + M, J[1] + M], [J[0] - M, J[1] + M]];
        for (var e3 = 0; e3 < 3 && poly.length > 2; e3++) { var K = coins[e3];   // garder (x − C)·n ≥ r + jeu
          poly = _clip(poly, K.cx + K.nx * (K.r + jeu), K.cy + K.ny * (K.r + jeu), -K.nx, -K.ny); }
        if (poly.length < 3) continue;
        // le rayon inscrit : la place qu'offre la jonction ; en dessous, pas de bulle
        var gx = 0, gy = 0; for (var y3 = 0; y3 < poly.length; y3++) { gx += poly[y3][0]; gy += poly[y3][1]; } gx /= poly.length; gy /= poly.length;
        var ins = 1e9; for (var e4 = 0; e4 < 3; e4++) { var K2 = coins[e4]; ins = Math.min(ins, (gx - K2.cx) * K2.nx + (gy - K2.cy) * K2.ny - K2.r - jeu); }
        var fIns = Math.max(0, Math.min(1, (ins - jour * 0.16) / (jour * 0.14))); fIns = fIns * fIns * (3 - 2 * fIns); if (fIns <= 0) continue;   // la place : adoucie, plus un seuil franc
        // les pointes s'arrêtent : 2,4 × le rayon inscrit depuis le centre
        for (var e5 = 0; e5 < 3 && poly.length > 2; e5++) { var K3 = coins[e5], vx = -K3.nx, vy = -K3.ny;   // la pointe opposée au coin e5
          poly = _clip(poly, gx + vx * ins * 2.4, gy + vy * ins * 2.4, vx, vy); }
        /* ⚑ v55 (Tom : « parfois elles deviennent trop grosses ») — mesuré pendant les mouvements : jusqu'à 4,7 jour² et 6 jours de
           long (au repos : 1,3 et 1,1) — quand deux coins sont presque parallèles, les pointes filaient loin dans les jours. Une bulle
           tient TOUJOURS dans un disque de 1,2 jour autour de son centre. */
        for (var e7 = 0; e7 < 12 && poly.length > 2; e7++) { var a7 = e7 / 12 * 6.283185307179586, c7 = Math.cos(a7), s7 = Math.sin(a7), R7 = Math.min(ins * 2.4, jour * 1.2);
          poly = _clip(poly, gx + c7 * R7, gy + s7 * R7, c7, s7); }
        if (poly.length < 3) continue;
        var C = _halVoisines(gx, gy, ins * 4, cells); if (!C) continue;
        var ech = (0.72 + ((h >>> 3) % 8) / 8 * 0.2) * calme * fIns;
        var relB = poly.map(function (q3) { return [q3[0] - gx, q3[1] - gy]; }), aB = 0;
        for (var q8 = 0; q8 < relB.length; q8++) { var A8 = relB[q8], B8 = relB[(q8 + 1) % relB.length]; aB += A8[0] * B8[1] - B8[0] * A8[1]; }
        aB = Math.abs(aB) / 2; var capB = 1.4 * jour * jour, kB = aB > capB ? Math.sqrt(capB / aB) : 1;   // v55 : jamais plus grosse qu'au repos (1,3 jour² mesuré)
        if (kB < 1) relB = relB.map(function (q9) { return [q9[0] * kB, q9[1] * kB]; });
        bulle(cle, gx, gy, relB, ins * 0.9 * kB, _rgb(cOf(coins[(h >>> 22) % 3].s, now)), ech);
      }
      // (2) très rarement, dans un jour LARGE : une pilule fine, couchée dans le jour
      for (var v2 = 0; v2 < Math.min(6, C0.vois.length); v2++) {
        var q = C0.vois[v2].p, d = C0.vois[v2].d; if (d <= 0) continue;
        var cle2 = p0.k < q.k ? p0.k + ':' + q.k : q.k + ':' + p0.k; if (vus[cle2]) continue; vus[cle2] = 1;
        var jr = _halJour(p0, q, jour); if (jr < jour * 1.1) continue;
        var h2 = _fnv('j' + cle2); if (h2 % 5 !== 0) continue;
        var calme2 = Math.min(calme0, _halCalme(q, u)); if (calme2 <= 0.01) continue;
        var nx = (q.x - p0.x) / d, ny = (q.y - p0.y) / d, t = _halFront(p0, q, d, now, u);
        var gl = (((h2 >>> 4) % 100) / 100 - 0.5) * u * 0.3, cx = p0.x + nx * t - ny * gl, cy = p0.y + ny * t + nx * gl;
        if (ix.owner(cx + nx * jour, cy + ny * jour) !== q || ix.owner(cx - nx * jour, cy - ny * jour) !== p0) continue;
        var ep = jr * 0.2, la = ep * (2.2 + ((h2 >>> 12) % 8) / 8 * 0.8);
        var pil = [[-ny * la - nx * ep, nx * la - ny * ep], [-ny * la + nx * ep, nx * la + ny * ep], [ny * la + nx * ep, -nx * la + ny * ep], [ny * la - nx * ep, -nx * la - ny * ep]];
        var C2 = _halVoisines(cx, cy, la * 2, cells); if (!C2) continue;
        if (_halTient(cx, cy, pil, C2, jr * 0.1) < 0.999) continue;
        bulle(cle2, cx, cy, pil, ep, _rgb(cOf((h2 >>> 24) % 2 ? p0.s : q.s, now)), calme2);
      }
    }
    for (var kM in _halMem) { if (vuB[kM]) continue; var mM = _halMem[kM]; mM.e -= mM.e * kE;
      if (mM.e < 0.02) { delete _halMem[kM]; continue; } window._mondeEncore = true; trace(mM); }
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
  /* ⚑ v45 — LE CHAMP DE MADRURE, SEUL : la pente, les trois ondes, les bosses des nœuds. Sorti de `_madGen` tel quel, pour
     que la construction (courbes, dalles) et le rendu GPU de la Toile vivante lisent EXACTEMENT les mêmes nombres. */
  function _madParams(ix, poids) {
    var P = ix.P, n = P.length, i;
    // v37 (Tom) : « Madrure est l'exception : son APERÇU est presque vide — beaucoup de lignes et quelques nœuds. C'est là
    // qu'elle intrigue ; pleine, elle ne vend pas. » Un aperçu du Studio garde CINQ nœuds (les cinq premières clés) ; l'unité,
    // l'onde et ses bandes ne bougent pas. Sur la Toile, rien ne change : chaque promesse reste un nœud.
    // v40 (Tom, 24 sept.) : « il n'y a plus assez de nœuds, mets-en deux fois plus » — DIX nœuds dans l'aperçu (étaient cinq)
    if (n > 10 && P[0].s && P[0].s.apercu) {
      /* ⚑ v79 — au Studio, les nœuds sont ceux que la composition a désignés (`_nd`, les dix premières clés) et les dalles qui
         arrivent (`_x`) : un retrait ou un ajout d'un nœud se voit (sa bosse descend, monte) ; les autres cellules ne font pas l'onde. */
      var Q = P.filter(function (p) { return p.s._nd || p.s._x != null; });
      P = Q.length ? Q : P.slice().sort(function (a, b) { return a.k - b.k; }).slice(0, 10); n = P.length; }
    if (!n) return null;
    var sp = _uMonde(ix, U_MAD) * SP_U, band = sp * 0.17;
    var th = typeof cleToile === 'number' ? _lcg(cleToile >>> 0)() * 6.283 : 0.6;
    var ct = Math.cos(th) / band, st = Math.sin(th) / band;
    /* ⚑ v40 (Tom, 24 sept.) — L'ONDE N'EST PLUS UN PLAN. « Là ça me fait que des lignes parallèles et des nœuds parfois ; on
       veut des vagues — pas des parallèles, c'est perdre l'âme de la madrure. » Le champ valait x·cos θ + y·sin θ + les
       bosses : hors des nœuds, les lignes de niveau d'un plan SONT des parallèles, à chaque ouverture. On y ajoute trois
       ondes lentes, tirées de la clé de la Toile (stables pour une Toile, différentes d'une Toile à l'autre) : deux courent
       LE LONG des lignes (elles les font onduler), une EN TRAVERS (elle les resserre et les écarte, comme un veinage).
       ⚠ LA SOMME DE LEURS PENTES (0,87) RESTE SOUS CELLE DU PLAN (1) : le champ croît toujours dans le sens θ, donc AUCUNE
       boucle fermée ne naît hors d'un nœud — pas de faux œil. À vide, la tendance reste des lignes qui courent. Les mêmes
       ondes entrent dans `phi` (les yeux relisent le champ). */
    var _rw = _lcg(((typeof cleToile === 'number' ? cleToile : 7) ^ 0x2f6a1c3b) >>> 0), WV = [];
    [[Math.PI / 2, 0.6, 3.2, 1.6, 0.40], [Math.PI / 2, 1.2, 6.0, 3.0, 0.25], [0, 0.8, 2.2, 1.0, 0.22]].forEach(function (c) {
      var d = th + c[0] + (_rw() - 0.5) * c[1], L = sp * (c[2] + _rw() * c[3]), f = 6.283185307179586 / L;
      WV.push({ fx: f * Math.cos(d), fy: f * Math.sin(d), A: c[4] * L / (6.283185307179586 * band), ph: _rw() * 6.283185307179586 });
    });
    function onde(x, y) { var s = 0; for (var q = 0; q < WV.length; q++) { var w = WV[q]; s += w.A * Math.sin(w.fx * x + w.fy * y + w.ph); } return s; }
    var KX = new Float64Array(n), KY = new Float64Array(n), KK = new Float64Array(n), KR = new Float64Array(n);
    var _tL = (window._apImage && window._madLisOn) ? performance.now() : 0, _om = window._madOmega || 3;
    var _fin = null; if (_tL) { try { _fin = env.finale; } catch (_) { _fin = null; } }
    for (i = 0; i < n; i++) {
      var r0 = _lcg((P[i].k ^ 0x5bd1e995) >>> 0);
      KX[i] = P[i].x; KY[i] = P[i].y;
      /* ⚑ v89 (Tom : « Madrure au Studio se lit comme une suite d'images ») — mesuré : depuis v83 (le semis clairsemé), une dizaine de
         nœuds font toute l'onde ; le ressort du moteur part à sa vitesse la plus grande à la première image, et chaque pixel de
         déplacement d'un nœud déplace toutes les bandes — 10 à 14 niveaux d'une image à l'autre au début d'un événement (2,3 avant v83).
         Dans l'aperçu, un nœud SUIT sa graine (amortissement critique, ω 3/s) : il part à vitesse nulle, accélère, se pose. La Toile
         vivante n'y passe pas (son rythme est validé). */
      if (_tL) { var kL = P[i].k, L = _madLis[kL], fq = _fin ? _fin.get(P[i].s) : null, TXq = fq ? fq[0] : P[i].x, TYq = fq ? fq[1] : P[i].y;   /* au Studio, la place d'ÉQUILIBRE (la composition d'ouverture n'y est pas : le premier événement relâchait tout) */
        if (!L || _tL - L.t > 400) L = _madLis[kL] = { x: TXq, y: TYq, vx: 0, vy: 0, t: _tL };
        else if (_tL > L.t) { var dL = Math.min(0.1, (_tL - L.t) / 1000), nS = Math.max(1, Math.ceil(dL / 0.004)), hS = dL / nS, W2 = _om * _om;
          for (var q = 0; q < nS; q++) { L.vx += (W2 * (TXq - L.x) - 2 * _om * L.vx) * hS; L.vy += (W2 * (TYq - L.y) - 2 * _om * L.vy) * hS; L.x += L.vx * hS; L.y += L.vy * hS; }
          L.t = _tL; if (Math.abs(L.x - TXq) + Math.abs(L.y - TYq) > 0.05 || Math.abs(L.vx) + Math.abs(L.vy) > 0.5) window._mondeEncore = true; }
        KX[i] = L.x; KY[i] = L.y; }
      /* ⚑ v45 (Tom + PDF : « une onde continue se referme d'elle-même autour de CHAQUE promesse ») — LA BOSSE EST PLUS
         SERRÉE ET PLUS FRANCHE. Avec 7,5–9,5 band sur 0,36–0,48 sp, sa pente maximale (0,65·k/r) ne dépassait pas toujours
         celle de l'onde et des vagues (jusqu'à 1,87/band) : un nœud sur trois n'avait pas d'œil, et sa dalle était une
         strate fermée DE FORCE (galet coupé de bandes arbitraires). 10–12,5 band sur 0,26–0,34 sp : pente ≥ 1,6 × celle
         du fond, et un œil assez profond pour porter plusieurs anneaux — l'œil se forme dans le champ lui-même, plus petit, et le bois s'enroule autour. */
      KK[i] = 10 + r0() * 2.5;                                 // en unités de band
      var rr = sp * (0.26 + r0() * 0.08);
      // v34 : la bosse d'un nœud ne dépasse pas la moitié de l'écart à son plus proche voisin — sans quoi, à 40 promesses
      // et plus, les bosses s'additionnent en un dôme et l'onde tourne en anneaux concentriques (vu à 48)
      if (!poids) { var dn = ix.near(P[i], 1); if (dn.length && dn[0].d * 0.5 < rr) rr = dn[0].d * 0.5; }
      else {   // v45 : une voisine qui arrive (ou part) ne resserre la bosse qu'à mesure qu'elle pousse (ou s'efface) — d'un coup, le
               // champ sautait à la première image (mesuré en WebKit : |Δφ| 0,57 bande, puis 0,06)
        var dv = ix.near(P[i], 4); for (var jv = 0; jv < dv.length; jv++) { var gv = poids(dv[jv].p.s); if (gv <= 0.001) continue; var ev = dv[jv].d * 0.5 / gv; if (ev < rr) rr = ev; } }
      KR[i] = 1 / (rr * rr);
    }
    var u6 = sp / SP_U * 6, u45 = u6 * 0.75;
    return { P: P, n: n, sp: sp, band: band, th: th, ct: ct, st: st, WV: WV, onde: onde, KX: KX, KY: KY, KK: KK, KR: KR,
             R6: u6 * u6, R45: u45 * u45, IR: 1 / (u6 * u6 - u45 * u45) };
  }
  function* _madGen(now, x0, y0, x1, y1) {
    var ix = _idx(), MP = _madParams(ix), i;
    if (!MP) return;
    var P = MP.P, n = MP.n, sp = MP.sp, band = MP.band, th = MP.th, ct = MP.ct, st = MP.st, WV = MP.WV, onde = MP.onde,
        KX = MP.KX, KY = MP.KY, KK = MP.KK, KR = MP.KR;
    var pas = band * 0.5;
    var aire = (x1 - x0 + 4 * pas) * (y1 - y0 + 4 * pas);
    if (aire / (pas * pas) > 260000) pas = Math.sqrt(aire / 260000);
    var gx0 = Math.floor(x0 / pas) * pas - 2 * pas, gy0 = Math.floor(y0 / pas) * pas - 2 * pas;   // ancrée : même grille pour toute vue
    var nx = Math.ceil((x1 + 2 * pas - gx0) / pas), ny = Math.ceil((y1 + 2 * pas - gy0) / pas), rw = nx + 1;
    var V = new Float64Array(rw * (ny + 1)), vmin = 1e18, vmax = -1e18;
    var WSX = [], WCX = [], WSY = new Float64Array(WV.length), WCY = new Float64Array(WV.length);
    for (var qw = 0; qw < WV.length; qw++) { var sxa = new Float64Array(nx + 1), cxa = new Float64Array(nx + 1);
      for (var aw = 0; aw <= nx; aw++) { var xw = WV[qw].fx * (gx0 + aw * pas); sxa[aw] = Math.sin(xw); cxa[aw] = Math.cos(xw); }
      WSX.push(sxa); WCX.push(cxa); }
    // portée : au-delà de 6 u un nœud pèse moins de 0,04 band ; fondu doux de 4,5 à 6 u, jamais de saut
    var u6 = sp / SP_U * 6, u45 = u6 * 0.75, R6 = u6 * u6, R45 = u45 * u45, IR = 1 / (R6 - R45);
    var rowI = new Int32Array(n);
    for (var j = 0; j <= ny; j++) {
      var y = gy0 + j * pas, nr = 0;
      for (var qy = 0; qy < WV.length; qy++) { var yw = WV[qy].fy * y + WV[qy].ph; WSY[qy] = Math.sin(yw); WCY[qy] = Math.cos(yw); }
      for (i = 0; i < n; i++) { var dyr = y - KY[i]; if (dyr * dyr < R6) rowI[nr++] = i; }
      for (var a = 0; a <= nx; a++) {
        var v;
        if (j === 0 || a === 0 || j === ny || a === nx) v = -1e9;     // bord, fixé plus bas sous le premier niveau
        else {
          var x = gx0 + a * pas; v = x * ct + y * st;
          for (var qv = 0; qv < WV.length; qv++) v += WV[qv].A * (WSX[qv][a] * WCY[qv] + WCX[qv][a] * WSY[qv]);   // v40 : les ondes
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
      var v = x * ct + y * st + onde(x, y);   // v40 : les mêmes ondes que la grille
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
  /* ⚑ v45 (Tom, 24 sept.) — MADRURE SUR LE GPU, SUR LA TOILE VIVANTE. « Les veines se lient, se délient, ondulent, puis se
     stabilisent — jamais de saut. » L'onde se construisait sur le CPU (100–240 ms) et ne pouvait être refaite qu'une fois le
     semis posé : pendant une plantation on voyait l'onde d'AVANT, puis la neuve d'un coup (mesuré : une image de 29 niveaux,
     ses voisines à 0,1). Ici le champ (`_madParams`, les MÊMES nombres que la construction) est évalué à chaque pixel,
     à chaque image, et classé comme le dessin CPU : filet [0 ; 0,11) [1 ; 1,11) [2 ; 2,11) · veine [0,11 ; 1) · veine claire
     [1,11 ; 2) · fond [2,11 ; 3), bord anticrénelé sur la dérivée du champ. Pendant une transition, la bosse d'un nœud qui
     arrive MONTE de zéro, celle d'un nœud qui part DESCEND : l'onde se déforme continûment jusqu'à se poser.
     Sous Ingénu, l'œil de chaque promesse prend ses tons de nature DANS le shader (au-dessus de son niveau d'œil, dans son
     rayon) : il suit le champ au pixel — plus de galet posé sur l'onde.
     Seulement sur la Toile vivante ; la dalle d'une fiche, un export, un aperçu gardent le chemin CPU. Sans WebGL2 (ou au-delà
     de 64 nœuds), le chemin CPU aussi. `window._perfAncien` le coupe (preuve). */
  var _mgl = null, _mgL = {}, _mgT = 0, _mgS = {}, _mgHC = 0, _mgRev = 0;   /* v79 : _mgS, le dernier calcul de chaque œil ; _mgRev, la révision du champ */
  var _MGVS = '#version 300 es\nin vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  /* ⚑ v79 (Tom : « supprime le plafond définitivement ») — LES NŒUDS ET LES YEUX DANS DES TEXTURES, RANGÉS PAR CELLULE. Le shader
     recevait les nœuds dans un tableau d'uniformes de 64 places (`uK[64]`) : au-delà, le chemin processeur, sans mouvement. Désormais
     un texel par nœud (x, y, poids, raideur) et par œil ; la Toile vue est découpée en cellules de la PORTÉE d'une bosse (√R6), et
     chaque cellule liste les nœuds et les yeux qui peuvent l'atteindre. Un pixel ne parcourt que la liste de sa cellule : même champ,
     même classement, même œil — mais plus aucun plafond, et un coût par pixel qui ne grandit plus avec le nombre de paroles. */
  var _MGFS = '#version 300 es\nprecision highp float;precision highp int;precision highp sampler2D;\n' +
    'uniform vec2 uRes;uniform float uS;uniform mat3 uInv;uniform vec2 uCS;uniform vec4 uWV[3];uniform vec3 uR;uniform vec3 uT[3];uniform vec3 uNT[48];' +
    'uniform sampler2D tK;uniform sampler2D tC;uniform sampler2D tI;uniform sampler2D tJ;uniform sampler2D tE;uniform sampler2D tEM;uniform vec4 uG;uniform ivec2 uGN;out vec4 o;\n' +
    'vec4 lit(sampler2D t,int i){return texelFetch(t,ivec2(i-1024*(i/1024),i/1024),0);}\n' +
    'float bosse(int k,vec2 q){vec4 K=lit(tK,k);vec2 d=q-K.xy;float d2=dot(d,d);if(d2>=uR.x)return 0.;float w=1.;if(d2>uR.y){float t=(d2-uR.y)*uR.z;w=1.-t*t*(3.-2.*t);}return w*K.z/(1.+d2*K.w);}\n' +
    'float bx(float f,float a,float b,float w){return clamp((f-a)/w+.5,0.,1.)-clamp((f-b)/w+.5,0.,1.);}\n' +
    'void main(){vec2 px=vec2(gl_FragCoord.x,uRes.y-gl_FragCoord.y);vec2 q=(uInv*vec3(px,1.)).xy;' +
    'float v=q.x*uCS.x+q.y*uCS.y;for(int i=0;i<3;i++)v+=uWV[i].z*sin(uWV[i].x*q.x+uWV[i].y*q.y+uWV[i].w);' +
    'ivec2 c=ivec2(floor((q-uG.xy)*uG.w));bool dd=c.x>=0&&c.y>=0&&c.x<uGN.x&&c.y<uGN.y;vec4 C=dd?texelFetch(tC,c,0):vec4(0.);' +
    'int a0=int(C.x),n0=int(C.y);for(int j=0;j<n0;j++)v+=bosse(int(lit(tI,a0+j).x),q);' +
    'float w=max(fwidth(v)*uS,1e-4);float f=v-3.*floor(v/3.);' +
    'float fi=bx(f,-1.,-.89,w)+bx(f,0.,.11,w)+bx(f,1.,1.11,w)+bx(f,2.,2.11,w)+bx(f,3.,3.11,w);' +
    'float b1=bx(f,-2.89,-2.,w)+bx(f,.11,1.,w)+bx(f,3.11,4.,w);float b2=bx(f,-1.89,-1.,w)+bx(f,1.11,2.,w)+bx(f,4.11,5.,w);' +
    'vec3 T0=uT[0],T1=uT[1],T2=uT[2];' +
    'int a1=int(C.z),n1=int(C.w);for(int j=0;j<n1;j++){int e=int(lit(tJ,a1+j).x);vec4 E=lit(tE,e);vec2 de=q-E.xy;float dq=dot(de,de);if(dq<E.z){float s=clamp((v-E.w)/w+.5,0.,1.)*smoothstep(E.z,E.z*.82,dq);' +
    'if(s>0.){vec4 M=lit(tEM,e);s*=M.z;int t=int(M.x);float bk=bosse(int(M.y),q);s*=clamp((E.w-(v-bk))/w+.5,0.,1.);T0=mix(T0,uNT[t*3],s);T1=mix(T1,uNT[t*3+1],s);T2=mix(T2,uNT[t*3+2],s);}}}' +
    'o=vec4(fi*T0+b1*T1+b2*T2,fi+b1+b2);}';
  /* v79 — jusqu'à 64 nœuds : le shader d'origine (tableaux d'uniformes), le plus rapide en WebKit — les textures flottantes y coûtent
     (mesuré : 136 → 100 images en 2,5 s à 40 paroles). Au-delà : le shader à textures, sans plafond. */
  var _MGFS64 = '#version 300 es\nprecision highp float;\n' +
    'uniform vec2 uRes;uniform mat3 uInv;uniform vec2 uCS;uniform vec4 uWV[3];uniform int uN;uniform vec4 uK[64];uniform vec3 uR;uniform vec3 uT[3];' +
    'uniform int uNE;uniform vec4 uE[64];uniform vec4 uEM[16];uniform vec3 uNT[48];out vec4 o;\n' +
    'float champ(vec2 q){float v=q.x*uCS.x+q.y*uCS.y;for(int i=0;i<3;i++)v+=uWV[i].z*sin(uWV[i].x*q.x+uWV[i].y*q.y+uWV[i].w);' +
    'for(int i=0;i<64;i++){if(i>=uN)break;vec2 d=q-uK[i].xy;float d2=dot(d,d);if(d2>=uR.x)continue;float w=1.;if(d2>uR.y){float t=(d2-uR.y)*uR.z;w=1.-t*t*(3.-2.*t);}v+=w*uK[i].z/(1.+d2*uK[i].w);}return v;}\n' +
    'float bx(float f,float a,float b,float w){return clamp((f-a)/w+.5,0.,1.)-clamp((f-b)/w+.5,0.,1.);}\n' +
    'void main(){vec2 px=vec2(gl_FragCoord.x,uRes.y-gl_FragCoord.y);vec2 q=(uInv*vec3(px,1.)).xy;float v=champ(q);float w=max(fwidth(v),1e-4);' +
    'float f=v-3.*floor(v/3.);' +
    'float fi=bx(f,-1.,-.89,w)+bx(f,0.,.11,w)+bx(f,1.,1.11,w)+bx(f,2.,2.11,w)+bx(f,3.,3.11,w);' +
    'float b1=bx(f,-2.89,-2.,w)+bx(f,.11,1.,w)+bx(f,3.11,4.,w);float b2=bx(f,-1.89,-1.,w)+bx(f,1.11,2.,w)+bx(f,4.11,5.,w);' +
    'vec3 T0=uT[0],T1=uT[1],T2=uT[2];' +
    'for(int i=0;i<64;i++){if(i>=uNE)break;vec2 d=q-uE[i].xy;float dd=dot(d,d);if(dd<uE[i].z){float s=clamp((v-uE[i].w)/w+.5,0.,1.)*smoothstep(uE[i].z,uE[i].z*.82,dd);if(s>0.){float mf=uEM[i/4][i-4*(i/4)];int m=int(floor(mf));s*=fract(mf);int j=m-16*(m/16);int k=m/16;vec2 dk=q-uK[k].xy;float d2k=dot(dk,dk);float wk=1.;if(d2k>=uR.x)wk=0.;else if(d2k>uR.y){float tk=(d2k-uR.y)*uR.z;wk=1.-tk*tk*(3.-2.*tk);}float bk=wk*uK[k].z/(1.+d2k*uK[k].w);s*=clamp((uE[i].w-(v-bk))/w+.5,0.,1.);T0=mix(T0,uNT[j*3],s);T1=mix(T1,uNT[j*3+1],s);T2=mix(T2,uNT[j*3+2],s);}}}' +
    'o=vec4(fi*T0+b1*T1+b2*T2,fi+b1+b2);}';
  function _madGLctx() {
    if (_mgl !== null) return _mgl;
    _mgl = false;
    try {
      if (typeof document === 'undefined') return false;
      var cv = document.createElement('canvas'); cv.addEventListener('webglcontextcreationerror', function (e) { window._madGLerr = 'création refusée : ' + ((e && e.statusMessage) || '(sans message)'); });   /* v93 : la raison EXACTE du refus, donnée par le navigateur */
      var gl = cv.getContext('webgl2', { premultipliedAlpha: true, antialias: false, alpha: true, depth: false, stencil: false, failIfMajorPerformanceCaveat: !window._madGLlibre });   /* sans vrai GPU (rendu logiciel : une image par seconde, mesuré), le chemin CPU */
      if (!gl) return false;
      var sh = function (t, src) { var s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
      var prog = function (fs) { var p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, _MGVS)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p);
        if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); return p; };
      var pr = prog(_MGFS), pr64 = prog(_MGFS64);
      var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      var loc = {}; ['uRes', 'uS', 'uInv', 'uCS', 'uWV', 'uR', 'uT', 'uNT', 'tK', 'tC', 'tI', 'tJ', 'tE', 'tEM', 'uG', 'uGN'].forEach(function (n) { loc[n] = gl.getUniformLocation(pr, n); });
      var tx = {}; ['tK', 'tC', 'tI', 'tJ', 'tE', 'tEM'].forEach(function (n) { var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); tx[n] = t; });
      var loc64 = {}; ['uRes', 'uInv', 'uCS', 'uWV', 'uN', 'uK', 'uR', 'uT', 'uNE', 'uE', 'uEM', 'uNT'].forEach(function (n) { loc64[n] = gl.getUniformLocation(pr64, n); });
      _mgl = { cv: cv, gl: gl, pr: pr, loc: loc, ap: gl.getAttribLocation(pr, 'p'), b: b, tx: tx, pr64: pr64, loc64: loc64, ap64: gl.getAttribLocation(pr64, 'p') };
      cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); _mgl = null; });
    } catch (e) { _mgl = false; try { window._madGLerr = String(e && e.message || e); } catch (_) { } }
    return _mgl;
  }
  /* v79 — une texture de données : 1024 texels par ligne (le shader lit l'index i en (i mod 1024, i / 1024)) */
  function _mgRang(n) { return Math.max(1024, Math.ceil(Math.max(1, n) / 1024) * 1024); }
  function _mgTex(gl, t, u, loc, data, comp) { var n = data.length / comp, h = Math.max(1, Math.ceil(n / 1024)), need = 1024 * h * comp, d = data;
    if (d.length < need) { d = new Float32Array(need); d.set(data); }
    gl.activeTexture(gl.TEXTURE0 + u); gl.bindTexture(gl.TEXTURE_2D, t);
    if (comp === 4) gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA32F, 1024, h, 0, gl.RGBA, gl.FLOAT, d); else gl.texImage2D(gl.TEXTURE_2D, 0, gl.R32F, 1024, h, 0, gl.RED, gl.FLOAT, d);
    gl.uniform1i(loc, u); }
  /* v79 — les listes par cellule : chaque objet (centre, portée) va dans toutes les cellules que son disque touche */
  function _mgListes(n, de, gx0, gy0, Gp, GW, GH) { var nb = new Int32Array(GW * GH), bo = [], k, a, cx, cy;
    for (k = 0; k < n; k++) { a = de(k); var cxa = Math.max(0, Math.floor((a[0] - a[2] - gx0) / Gp)), cxb = Math.min(GW - 1, Math.floor((a[0] + a[2] - gx0) / Gp)),
        cya = Math.max(0, Math.floor((a[1] - a[2] - gy0) / Gp)), cyb = Math.min(GH - 1, Math.floor((a[1] + a[2] - gy0) / Gp)); bo.push([cxa, cxb, cya, cyb]);
      for (cy = cya; cy <= cyb; cy++) for (cx = cxa; cx <= cxb; cx++) nb[cy * GW + cx]++; }
    var deb = new Int32Array(GW * GH), tot = 0, mx = 0; for (k = 0; k < GW * GH; k++) { deb[k] = tot; tot += nb[k]; if (nb[k] > mx) mx = nb[k]; }
    var idx = new Int32Array(Math.max(1, tot)), pos = new Int32Array(GW * GH); for (k = 0; k < n; k++) { var B = bo[k];
      for (cy = B[2]; cy <= B[3]; cy++) for (cx = B[0]; cx <= B[1]; cx++) { var c = cy * GW + cx; idx[deb[c] + pos[c]++] = k; } }
    var idxF = new Float32Array(Math.max(1, tot)); for (k = 0; k < tot; k++) idxF[k] = idx[k];
    return { deb: deb, nb: nb, idx: idx, idxF: idxF, max: mx }; }
  // l'âge d'une transition sur un nœud : 1 posé, 0 → 1 à l'arrivée, 1 → 0 au départ
  var _madLis = {}, _madPl = {};
  /* v89 — le POIDS d'un nœud suit aussi, dans l'aperçu : sa bosse (10 à 12 bandes) naissait en 800 ms — ses anneaux jaillissaient
     du centre plus vite que l'œil ne les suit. Même amortissement critique que les places. */
  function _madPoidsLisse(p, now, TR) { var c = _madPoids(p.s, now, TR); if (!window._apImage || !window._madLisOn) return c;
    var t = performance.now(), om = window._madOmega || 3, L = _madPl[p.k];
    if (!L || t - L.t > 400) { L = _madPl[p.k] = { w: c, v: 0, t: t }; return c; }
    if (c <= L.w) { L.w = c; L.v = 0; L.t = t; return c; }   /* à la descente, l'effacement d'origine (560 ms, déjà progressif) : lissé, il était en retard sur le retrait de la graine — la bosse disparaissait d'un coup */
    if (t > L.t) { var d = Math.min(0.1, (t - L.t) / 1000), nS = Math.max(1, Math.ceil(d / 0.004)), h = d / nS;
      for (var q = 0; q < nS; q++) { L.v += (om * om * (c - L.w) - 2 * om * L.v) * h; L.w += L.v * h; } L.t = t;
      if (Math.abs(L.w - c) > 0.002 || Math.abs(L.v) > 0.01) window._mondeEncore = true; }
    return Math.max(0, Math.min(1, L.w)); }
  function _madPoids(s, now, TR) {
    if (!TR && !window._apImage) return s.part != null ? 0 : 1;   /* v92 : l'aperçu n'a pas de transition du moteur — le poids y passait d'un coup, seules les graines bougeaient */
    /* v92 (Tom : « un peu rapide — aligne-la sur le moodboard ») — sur la Toile, un événement bouge 2,25 s (la dalle ET le relâchement
       de toutes les graines) ; l'aperçu n'a pas de relâchement, il ne restait que ce poids — 0,9 à 1,3 s. Au Studio le poids prend donc
       la durée visible de la Toile : 1 350 ms d'horloge d'aperçu (×0,6) = 2,25 s. */
    var _mDP = window._apImage ? 1350 : 560, _mDA = window._apImage ? 1350 : 800;
    if (s.part != null) { var a = Math.min(1, Math.max(0, (now - s.part) / _mDP)); return 1 - a * a * (3 - 2 * a); }
    if (s.t0 != null && now - s.t0 < _mDA) { var b = Math.max(0, (now - s.t0) / _mDA); return b * b * (3 - 2 * b); }
    return 1;
  }
  function _madGL(now, x0, y0, x1, y1) {
    var cv = g && g.canvas; if (!cv || !g.getTransform || window._perfAncien) return false;
    var M0 = _madGLctx(); if (!M0) return false;
    var _mgT0 = performance.now();
    var TR = env.trans, o = _repos; _repos = true; var ix, MP; try { ix = _idx(); MP = _madParams(ix, function (s2) { return _madPoids(s2, now, TR); }); } finally { _repos = o; }
    if (!MP) return true;
    if (MP.n > 1024 * 1024) return false;   /* v79 : la texture des nœuds (1024 × 1024) — pratiquement sans limite */
    /* ⚑ v89 (Tom : « Madrure sous Safari au-delà de 90 paroles ») — au-delà de 90 nœuds, le champ se calcule à une densité plafonnée
       (1,5 à 1,8 pixel par point) : chaque pixel additionne les bosses voisines, et leur nombre croît avec la densité des paroles —
       mesuré en WebKit : 61 images en 2,5 s à 90, 31 à 200. Le seuil est fixe (jamais un changement en plein mouvement). */
    var _dpr = cv.width / Math.max(1, W), rsM = (MP.n > 90 && !window._madPleinePx) ? Math.min(1, Math.max(0.5, (MP.n > 150 ? 1.2 : 1.5) / Math.max(1, _dpr))) : 1;   /* au-delà de 150 : 1,2 pixel par point */
    var P64 = MP.n <= 64 && !window._madTexForce, gl = M0.gl, L = P64 ? M0.loc64 : M0.loc, W2 = Math.round(cv.width * rsM), H2 = Math.round(cv.height * rsM), i;   /* v79 : ≤ 64 nœuds, le shader d'origine */
    if (M0.cv.width !== W2 || M0.cv.height !== H2) { M0.cv.width = W2; M0.cv.height = H2; }
    var Mt = g.getTransform(), Mi = Mt.inverse();
    gl.viewport(0, 0, W2, H2); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(P64 ? M0.pr64 : M0.pr);
    gl.bindBuffer(gl.ARRAY_BUFFER, M0.b); var AP = P64 ? M0.ap64 : M0.ap; gl.enableVertexAttribArray(AP); gl.vertexAttribPointer(AP, 2, gl.FLOAT, false, 0, 0);
    gl.uniform2f(L.uRes, W2, H2); if (!P64 && L.uS) gl.uniform1f(L.uS, rsM);   /* v89 : l'anticrénelage en pixels d'ÉCRAN — à densité réduite, les filets fins pâlissaient */
    gl.uniformMatrix3fv(L.uInv, false, new Float32Array([Mi.a / rsM, Mi.b / rsM, 0, Mi.c / rsM, Mi.d / rsM, 0, Mi.e, Mi.f, 1]));
    gl.uniform2f(L.uCS, MP.ct, MP.st);
    var wv = new Float32Array(12); for (i = 0; i < 3; i++) { var q = MP.WV[i] || { fx: 0, fy: 0, A: 0, ph: 0 }; wv[i * 4] = q.fx; wv[i * 4 + 1] = q.fy; wv[i * 4 + 2] = q.A; wv[i * 4 + 3] = q.ph; }
    gl.uniform4fv(L.uWV, wv);
    var KKe = new Float64Array(MP.n), K = new Float32Array(_mgRang(MP.n) * 4);
    for (i = 0; i < MP.n; i++) { KKe[i] = MP.KK[i] * _madPoidsLisse(MP.P[i], now, TR); K[i * 4] = MP.KX[i]; K[i * 4 + 1] = MP.KY[i]; K[i * 4 + 2] = KKe[i]; K[i * 4 + 3] = MP.KR[i]; }
    gl.uniform3f(L.uR, MP.R6, MP.R45, MP.IR);
    /* la grille : des cellules de la portée d'une bosse, sur la Toile vue (x0..y1, coordonnées de la Toile) */
    var RP = Math.sqrt(MP.R6), Gp = Math.max(RP, 8), gx0 = x0 - 1, gy0 = y0 - 1, GW = Math.max(1, Math.ceil((x1 - gx0) / Gp) + 1), GH = Math.max(1, Math.ceil((y1 - gy0) / Gp) + 1);
    var LN = _mgListes(MP.n, function (k) { return [MP.KX[k], MP.KY[k], RP]; }, gx0, gy0, Gp, GW, GH);
    var phiN = function (x, y) { var cx = Math.floor((x - gx0) / Gp), cy = Math.floor((y - gy0) / Gp); if (cx < 0 || cy < 0 || cx >= GW || cy >= GH) return null; var c = cy * GW + cx; return [LN.deb[c], LN.nb[c]]; };
    var TN = _madTons(now); gl.uniform3fv(L.uT, new Float32Array([TN[0][0] / 255, TN[0][1] / 255, TN[0][2] / 255, TN[1][0] / 255, TN[1][1] / 255, TN[1][2] / 255, TN[2][0] / 255, TN[2][1] / 255, TN[2][2] / 255]));
    // le champ, tel que le shader le voit (pour les yeux et pour l'encre des libellés, `Rmad.sous`)
    var phi = function (x, y) {
      var v = x * MP.ct + y * MP.st + MP.onde(x, y), cel = phiN(x, y), J0 = cel ? cel[0] : 0, J1 = cel ? cel[0] + cel[1] : 0, tout = !cel;
      for (var jj = (tout ? 0 : J0); jj < (tout ? MP.n : J1); jj++) { var j = tout ? jj : LN.idx[jj]; var dx = x - MP.KX[j], dy = y - MP.KY[j], d2 = dx * dx + dy * dy; if (d2 >= MP.R6) continue;
        var w = 1; if (d2 > MP.R45) { var t = (d2 - MP.R45) * MP.IR; w = 1 - t * t * (3 - 2 * t); } v += w * KKe[j] / (1 + d2 * MP.KR[j]); }
      return v;
    };
    var nE = 0, _mgTy0 = performance.now(), E = new Float32Array(4), EM = new Float32Array(4);   /* v82 : sans Ingénu, pas d'yeux — mais les tableaux existent (ils manquaient : Madrure plantait à chaque image sous toute autre palette) */
    if (_ingenu()) {
      E = new Float32Array(_mgRang(MP.n) * 4); EM = new Float32Array(_mgRang(MP.n) * 4); var NT = [], cles = {}, u = MP.sp / SP_U, NA = 24, NS = 30, dr = u * 1.5 / NS;
      var dt = _mgT ? (function (d) { return d > 0.25 ? 0.1 : d; })((now - _mgT) / 1000) : 0.016;   // ⚑ v61 : une image lente (jusqu'à 250 ms) compte son temps vrai — plafonnée à 100 ms, l'œil perdait du temps sous charge ; un trou plus long (la boucle repart) garde les 100 ms d'avant
      /* ⚑ v79 (Tom : « supprime le plafond ») — LES YEUX NE SE RECALCULENT QUE QUAND LE CHAMP BOUGE, AU BUDGET. Chaque œil balayait
         son voisinage (24 × 30 évaluations du champ, chacune sur TOUS les nœuds) à chaque image : quadratique — 35 ms à 60 paroles,
         343 ms à 200 (mesuré). Le calcul d'un œil est inchangé ; il ne se refait que si le champ a bougé depuis (positions, poids),
         d'abord les yeux les plus proches de la dalle qui arrive ou part, dans 6 ms par image. Au repos : aucun calcul. */
      var hC = MP.n; for (i = 0; i < MP.n; i++) hC = (Math.imul(hC ^ (Math.round(MP.KX[i] * 4) * 31 + Math.round(MP.KY[i] * 4) * 17 + Math.round(KKe[i] * 100) * 7 + Math.round(MP.KR[i] * 1e6)), 16777619)) >>> 0;
      if (hC !== _mgHC) { _mgHC = hC; _mgRev++; }
      var cand = [];
      for (i = 0; i < MP.n; i++) { var sq = MP.P[i].s; if (!_promesse(sq)) continue; var zq = _mgS[MP.P[i].k]; if (!zq || zq.rev !== _mgRev) cand.push(i); }
      var TX = TR && TR.x != null ? TR.x : null, TY = TX != null ? TR.y : null;
      cand.sort(function (p1, p2) { var z1 = _mgS[MP.P[p1].k], z2 = _mgS[MP.P[p2].k]; if (!z1 !== !z2) return z1 ? 1 : -1;
        if (TX != null) return Math.hypot(MP.KX[p1] - TX, MP.KY[p1] - TY) - Math.hypot(MP.KX[p2] - TX, MP.KY[p2] - TY); return (z1 ? z1.tv : 0) - (z2 ? z2.tv : 0); });
      var tB = performance.now(), fait = 0;
      for (var ci = 0; ci < cand.length; ci++) { if (fait && performance.now() - tB > 6) { window._mondeEncore = true; break; }
        i = cand[ci]; var s = MP.P[i].s;
        var cx = MP.KX[i], cy = MP.KY[i], v0 = phi(cx, cy), selle = -1e18, rs = [];
        for (var a = 0; a < NA; a++) {
          var ca = Math.cos(a / NA * 6.283185307179586), sa = Math.sin(a / NA * 6.283185307179586), mn = 1e18, col = [];
          for (var st2 = 1; st2 <= NS; st2++) { var val = phi(cx + ca * st2 * dr, cy + sa * st2 * dr); col.push(val); if (val < mn) mn = val; }
          if (mn > selle) selle = mn; rs.push([ca, sa, col]);
        }
        /* v45 — un œil ÉVOLUE : son niveau, son rayon et sa teinte glissent (constante 0,17 s) pendant une transition ;
           posés d'un coup, un œil qui naissait se teintait en une image (mesuré : 12 niveaux, voisines à 3,9). */
        var Lt = Math.floor(selle) + 1, ouvert = Lt < v0 - 0.15;                 // les bords de filet : 3j, 3j + 1, 3j + 2 — les entiers
        if (ouvert && [0, 0, 0, 1][(_cle(s) >>> 5) % 4] && Lt - 1 > selle) Lt -= 1;   // la strate de plus, comme la dalle d'une fiche
        var Rt = 0; if (ouvert) for (a = 0; a < NA; a++) { var cc = rs[a][2], r1 = NS * dr; for (st2 = 0; st2 < NS; st2++) if (cc[st2] < Lt) { r1 = (st2 + 1) * dr; break; } if (r1 > Rt) Rt = r1; }
        _mgS[MP.P[i].k] = { L: Lt, R: Rt, o: ouvert, rev: _mgRev, tv: tB }; fait++;
      }
      for (i = 0; i < MP.n; i++) {
        var s = MP.P[i].s; if (!_promesse(s)) continue;
        var cx = MP.KX[i], cy = MP.KY[i], zS = _mgS[MP.P[i].k]; if (!zS) continue;   // pas encore calculé : il paraîtra à l'image suivante
        var Lt = zS.L, Rt = zS.R, ouvert = zS.o;
        var kS = MP.P[i].k, e0 = _mgL[kS], kf = (TR || (window._apImage && window._madLisOn)) ? Math.min(1, dt * 6) : 1;   /* v89 : dans l'aperçu, un œil glisse toujours — il se posait d'un coup à la fin de la transition */
        if (!ouvert && !(e0 && e0.a > 0.01)) { if (e0) e0.a = 0; continue; }
        if (!e0) e0 = _mgL[kS] = { L: Lt, R: Rt, a: (TR || (window._apImage && window._madLisOn)) ? 0 : 1 };
        if (ouvert) { e0.L += (Lt - e0.L) * kf; e0.R += (Rt - e0.R) * kf; }
        e0.a += ((ouvert ? 1 : 0) - e0.a) * kf;
        var Ld = e0.L, Rm = e0.R;
        var tn = _madNature(cOf(s, now)), kc = tn.map(function (c) { return (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0); }).join('|');
        var j2 = cles[kc]; if (j2 == null) { if (NT.length >= 48) continue;   /* seize triplets au plus */ j2 = cles[kc] = NT.length / 3; NT.push(tn[0], tn[1], tn[2]); }
        E[nE * 4] = cx; E[nE * 4 + 1] = cy; var Rb = Rm * 1.25 + dr; E[nE * 4 + 2] = Rb * Rb; E[nE * 4 + 3] = Ld; EM[nE * 4] = j2; EM[nE * 4 + 1] = i; EM[nE * 4 + 2] = Math.max(0, Math.min(1, e0.a)); nE++;   // le ton, et le nœud (sa bosse décide de l'œil : un point en est s'il n'est au-dessus du niveau QUE par elle)
      }
      var nt = new Float32Array(144); for (i = 0; i < NT.length; i++) { nt[i * 3] = NT[i][0] / 255; nt[i * 3 + 1] = NT[i][1] / 255; nt[i * 3 + 2] = NT[i][2] / 255; }
      gl.uniform3fv(L.uNT, nt);
    }
    var _mgTy = performance.now() - _mgTy0;
    _mgT = now;
    if (P64) {   /* le shader d'origine : ses tableaux, son codage de l'œil (ton + 16 × nœud + opacité) */
      var K64 = new Float32Array(256), E64 = new Float32Array(256), EM64 = new Float32Array(64);
      K64.set(K.subarray(0, Math.min(256, MP.n * 4))); var nE64 = Math.min(64, nE); E64.set(E.subarray(0, nE64 * 4));
      for (i = 0; i < nE64; i++) EM64[i] = EM[i * 4] + 16 * EM[i * 4 + 1] + 0.001 + 0.998 * EM[i * 4 + 2];
      gl.uniform1i(L.uN, MP.n); gl.uniform4fv(L.uK, K64); gl.uniform1i(L.uNE, nE64); gl.uniform4fv(L.uE, E64); gl.uniform4fv(L.uEM, EM64);
    } else {
    var LE = _mgListes(nE, function (e) { return [E[e * 4], E[e * 4 + 1], Math.sqrt(E[e * 4 + 2])]; }, gx0, gy0, Gp, GW, GH);
    var CT = new Float32Array(GW * GH * 4); for (i = 0; i < GW * GH; i++) { CT[i * 4] = LN.deb[i]; CT[i * 4 + 1] = LN.nb[i]; CT[i * 4 + 2] = LE.deb[i]; CT[i * 4 + 3] = LE.nb[i]; }
    _mgTex(gl, M0.tx.tK, 0, L.tK, K, 4); _mgTex(gl, M0.tx.tI, 2, L.tI, LN.idxF, 1); _mgTex(gl, M0.tx.tJ, 3, L.tJ, LE.idxF, 1);
    _mgTex(gl, M0.tx.tE, 4, L.tE, E, 4); _mgTex(gl, M0.tx.tEM, 5, L.tEM, EM, 4);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, M0.tx.tC); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA32F, GW, GH, 0, gl.RGBA, gl.FLOAT, CT); gl.uniform1i(L.tC, 1);
    gl.uniform4f(L.uG, gx0, gy0, Gp, 1 / Gp); gl.uniform2i(L.uGN, GW, GH);
    }
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); if (rsM < 1) g.drawImage(M0.cv, 0, 0, cv.width, cv.height); else g.drawImage(M0.cv, 0, 0); g.restore();
    cv.__madC = { r: { phi: function (x, y) { return phi(x, y); } } }; cv.__madVu = null;
    window._madGPU = { n: MP.n, yeux: nE, t: now, cellules: GW * GH, parCellule: LN.max, js: Math.round((performance.now() - _mgT0) * 10) / 10, yeuxMs: Math.round((_mgTy || 0) * 10) / 10 };
    return true;
  }
  function Rmad(now, x0, y0, x1, y1) {
    _sync();
    var _mgOk = env.vive && _madGL(now, x0, y0, x1, y1);   // v45 : la Toile vivante, sur le GPU
    /* v92 (Tom : « fais afficher quel chemin est pris ») — le chemin de CHAQUE image, et pourquoi */
    window._madChemin = _mgOk ? 'GPU' : ('PROCESSEUR — ' + (!env.vive ? 'Toile non vivante' : _mgl === false ? ('WebGL refusé' + (window._madGLerr ? ' : ' + window._madGLerr : ' (rendu logiciel : failIfMajorPerformanceCaveat)')) : 'GPU indisponible pour cette image'));
    if (_mgOk) return;
    var sig = _madSig(), C = null, i, cv = g && g.canvas;
    for (i = 0; i < _madCaches.length; i++) if (_madCaches[i].sig === sig) { C = _madCaches[i]; break; }
    var dans = function (Z) { return Z && !(x0 < Z.x0 || y0 < Z.y0 || x1 > Z.x1 || y1 > Z.y1); };
    if (!dans(C)) {
      var der = cv && cv.__madC;
      /* ⚑ v79 (Tom : « une parole plantée qui n'apparaît pas est le défaut le plus grave de l'app ») — au passage de 63 à 64 nœuds, le
         chemin GPU laisse sur le canevas SON onde : le champ seul, sans tracés ni bornes (`dans` la croyait toujours valable). Prise pour
         « l'onde d'avant », elle plantait à chaque image (paths[0] indéfini) : la Toile restait figée, la parole n'apparaissait jamais.
         Une onde d'avant n'est bonne que si elle a ses tracés ; sinon on construit tout de suite. */
      if (der && der.r && der.r.paths && der.x0 != null && dans(der)) {
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
    window._madCPU = { t: now, cache: C && C.sig === sig, job: !!(cv && cv.__madJob), constructions: Rmad.constructions || 0, derniere: Rmad.derniere || null, n: seeds.length };   // v79 : le chemin processeur publie où il en est (lecture)
    if (!C.r) return;
    // couleurs relues à chaque image : palette et thème ne peuvent jamais rester dans l'ancienne teinte
    var TN = _madTons(now);
    if (window._perfAncien || DPR > 3 || !g.getTransform || !cv) { for (var c = 0; c < 3; c++) { g.fillStyle = _rgb(TN[c]); g.fill(C.r.paths[c], 'evenodd'); } }
    else {
      /* ⚑ v38 (perf) — L'ONDE SE PEINT UNE FOIS PAR CONSTRUCTION, DANS UN CALQUE DE LA TAILLE DU CANEVAS, ET SE POSE 1:1.
         Mêmes trois remplissages, même transformation (fraction comprise) : mêmes pixels. Il se refait si l'onde, ses tons,
         la vue ou la taille du canevas changent ; il vit sur l'onde en cache (C), donc la Toile et ses rendus le partagent. */
      var M = g.getTransform(), cw = cv.width, ch = cv.height, kS = [M.a, M.b, M.c, M.d, M.e, M.f, cw, ch, _rgb(TN[0]), _rgb(TN[1]), _rgb(TN[2])].join('|'), Sp = C.__spr;
      if (!Sp || Sp.k !== kS) {
        var sc = (Sp && Sp.cv) || document.createElement('canvas'); sc.width = cw; sc.height = ch;
        var G = sc.getContext('2d'); G.setTransform(M.a, M.b, M.c, M.d, M.e, M.f);
        for (var c2 = 0; c2 < 3; c2++) { G.fillStyle = _rgb(TN[c2]); G.fill(C.r.paths[c2], 'evenodd'); }
        Sp = C.__spr = { k: kS, cv: sc };
      }
      g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(Sp.cv, 0, 0); g.restore();
    }
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
        try { if (window._perfAncien || DPR > 3 || !g.getTransform) seule('madrure', s, now, (a0 + a1) / 2, (b0 + b1) / 2, Math.max(a1 - a0, b1 - b0)); else _madCalque(s, N, now, a0, b0, a1, b1); } finally { _tonsForces = null; }
      }
      if (manque && typeof env.relance === 'function') env.relance();
    } finally { _repos = o; }
  };
  /* ⚑ v38 (perf) — UN ŒIL SE PEINT UNE FOIS, DANS SON CALQUE, ET SE POSE 1:1. Chaque œil était découpé à sa forme (clip)
     puis rempli quatre fois, à chaque image : ~20 yeux, 13 ms. Le calque reçoit EXACTEMENT la transformation du canevas,
     translation comprise à la fraction près, décalée d'un nombre ENTIER de pixels : il se pose donc sans rééchantillonnage,
     au pixel près. Il se refait si l'œil change (nouvelle note au carnet), si ses tons ou le fond changent, ou si la vue
     bouge. `_perfAncien` et l'export (DPR > 3) gardent le chemin direct. */
  function _madCalque(s, N, now, a0, b0, a1, b1) {
    var M = g.getTransform(), f = N.flat, mx = 0, np = f ? f[0] : 0;
    for (var z = 0; z < np; z++) { var z2 = 1 + ((z + 1) % np) * 2, dx = f[z2] - f[1 + z * 2], dy = f[z2 + 1] - f[2 + z * 2], d = Math.sqrt(dx * dx + dy * dy); if (d > mx) mx = d; }
    var m = mx / 3 + (N.filet || 0) * 1.5 + 1;
    var X = [a0 - m, a1 + m, a0 - m, a1 + m], Y = [b0 - m, b0 - m, b1 + m, b1 + m], dx0 = 1e18, dy0 = 1e18, dx1 = -1e18, dy1 = -1e18;
    for (var q = 0; q < 4; q++) { var u = M.a * X[q] + M.c * Y[q] + M.e, v = M.b * X[q] + M.d * Y[q] + M.f; if (u < dx0) dx0 = u; if (u > dx1) dx1 = u; if (v < dy0) dy0 = v; if (v > dy1) dy1 = v; }
    var OX = Math.floor(dx0) - 2, OY = Math.floor(dy0) - 2, w = Math.ceil(dx1) - OX + 2, h = Math.ceil(dy1) - OY + 2;
    var k = [M.a, M.b, M.c, M.d, M.e, M.f, JSON.stringify(_tonsForces), String(typeof fondToile === 'function' ? fondToile() : ''), OX, OY, w, h].join('|');
    var C = N.__cal;
    if (!C || C.k !== k) {
      var cv = (C && C.cv) || document.createElement('canvas');
      cv.width = Math.max(1, w); cv.height = Math.max(1, h);
      var G = cv.getContext('2d'); G.setTransform(M.a, M.b, M.c, M.d, M.e - OX, M.f - OY);
      _calque = G;
      try { seule('madrure', s, now, (a0 + a1) / 2, (b0 + b1) / 2, Math.max(a1 - a0, b1 - b0)); }
      finally { _calque = null; _sync(); }
      C = N.__cal = { k: k, cv: cv, OX: OX, OY: OY };
    }
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(C.cv, C.OX, C.OY); g.restore();
  }
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
      var voulu = [0, 0, 0, 1][(k >>> 5) % 4];   // v45 (Tom : « trop gros en unique sur les fiches ») : l'œil seul, une strate de plus une fois sur quatre (était 0·1·1·2)
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
        // v55 : la dalle finit sur son trait sombre TOUT AUTOUR (à cheval sur la découpe : la moitié intérieure se voit)
        g.strokeStyle = _rgb(TN[0]); g.lineWidth = (N.filet || 1) * 2; g.lineJoin = 'round'; g.stroke(clipP);
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

  Rrit.transDur = 1900;
  Resq.sansPoussee = true;   // v47 : une seule vague
  Resq.transDur = 1400;   // v47 : la place d'arrivée bouge encore tant que la dalle neuve grandit (~1 s) ; chaque éclat qui change y garde sa cassure courte (160 ms)
  Rbob.transDur = 2400;
  Object.defineProperty(Rmad, 'partDur', { get: function () { return window._apImage ? 1400 : undefined; } });   /* v92 : au Studio, la graine qui part reste jusqu'à ce que son poids (1 350 ms d'aperçu) soit nul */
  Rmad.transDur = 2400;   // v45 : les bosses montent et descendent (800 / 560 ms) pendant que le semis se pose   // v45 : le ressort du moteur + un retissage (520 ms)   // v44 : le ressort du moteur (~1,6 s pour se poser) + une cassure (460 ms)   // v43 : la tirée (460 ms) + le ressort (≈ 1 400 ms) ; le moteur tourne tant qu'elle court
  Rhal.transDur = 1800; Rhal.douce = true; Rhal.omx = 6.2; Rhal.omw = 5.2; Rhal.partDur = 900;   // v50 : pas de poussée, un ressort plus long, un retrait qui va au bout   // v48 : la cellule neuve naît (600 ms), celle qui part se retire (560 ms)
  return { esquille: Resq, bobinette: Rbob, ritournelle: Rrit, madrure: Rmad, halin: Rhal, seule: _auRepos(seule), contour: _auRepos(contour), toucher: _auRepos(toucher), nature: _auRepos(nature), boite: _auRepos(boite) };
}

window.creerMondes = creerMondes;

})();


/* ══════════════════ bloc « lot-V72-CALQUE » ══════════════════ */
/* ⚑ v72 (passe de budget de la saison 2, Tom) — LE CALQUE DE REPOS, commun aux mondes de la saison 2.
   Au repos, une Toile ne change pas d'une image à l'autre : le monde se peint UNE fois dans un calque transparent de la taille du
   canevas, avec la transformation du canevas, et le calque se repose tel quel (1:1, au pixel — le précédent de Madrure et de Houle,
   CONTRAT-MONDE §8.4-8.5). Un calque transparent reposé par-dessus le fond donne les mêmes pixels que la peinture directe (le
   « source-over » est associatif), à l'arrondi près. La SIGNATURE que le monde fournit porte tout ce dont l'image dépend hors de la
   vue (géométrie, couleurs, encre, thème) ; la vue est ajoutée ici. Tant que la vue bouge (deux images de suite différentes), on peint
   directement : un calque refait à chaque image coûterait plus que rien. */
window._calqueRepos = function () {
  var L = null, avant = null;
  return { pose: function (g, sig, peindre) {
    var cv0 = g && g.canvas; if (!cv0 || !g.getTransform || window._perfAncien || window._v72SansCalque) return false;   // `_v72SansCalque` : la preuve (peinture directe)
    var M = g.getTransform(); if (M.b || M.c) return false;
    var k = sig + '|' + [M.a, M.d, M.e, M.f, cv0.width, cv0.height].join(','), stable = (k === avant); avant = k;
    if (!L || L.k !== k) {
      if (!stable) return false;   // la vue ou le contenu bouge : peinture directe
      var cv = (L && L.cv) || document.createElement('canvas'); if (cv.width !== cv0.width) cv.width = cv0.width; if (cv.height !== cv0.height) cv.height = cv0.height;
      var G = cv.getContext('2d'); G.setTransform(1, 0, 0, 1, 0, 0); G.clearRect(0, 0, cv.width, cv.height); G.setTransform(M.a, 0, 0, M.d, M.e, M.f);
      peindre(G); L = { cv: cv, k: k };
    }
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(L.cv, 0, 0); g.restore(); return true;
  }, oublie: function () { L = null; avant = null; } };
};

/* ══════════════════ bloc « lot-V62-BROUILLAMINI » ══════════════════ */
/* ⚑ v62 (27 sept. 2026) — BROUILLAMINI, la gouache découpée. Porté de `decoupe()` (planche « Trois matières », qui fait foi
   pour l'aspect) au CONTRAT-MONDE. Décisions : PORTAGE-SAISON2.md, et Tom le 27 sept. :
   · u = avg() du moteur. Pendant une transition, le compte des graines est pondéré par leur arrivée ou leur départ : sans
     cela u sauterait d'un coup de √(n/(n+1)) à la plantation, et toutes les formes au bord de la Toile avec lui.
     La MATIÈRE a pour unité l'avg de la Toile VIDE (68 graines, `env.uMat`) : elle ne change pas de taille avec les paroles.
   · LCG amorcé par la clé stable. Proportions de la planche : un cœur sur quatre (clé % 4), 55 % de chutes, 40 % de trous
     parmi les autres ; les formes de 5 lobes et plus ont leurs échancrures creusées (F^1,5).
   · La dalle porte cOf — plus aucune dalle à l'encre. La chute prend une NUANCE de la couleur de sa dalle, jamais un autre ton
     de palette (sous Ingénu, un autre ton dirait une autre nature).
   · La matière : des découpes de la même famille, plus petites et plus sages (3 à 5 lobes, un cœur sur quatre, ni trou ni
     chute), dans les tons de la rampe TH du monde. Elles cèdent la place aux dalles en rétrécissant, jamais d'un coup.
   · Rien n'est peint en couleur de papier : le trou est un pair-impair, on y voit le fond du moteur.
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerBrouillamini(env) {
  var g, W, H, seeds, cOf, avg;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; avg = env.avg; }
  var TAU = 6.283185307179586, N = 200;
  var ARR = 900, RET = 760;                  // arrivée (une dalle neuve grandit), retrait (celle qui part cède sa place)
  var CA = new Float64Array(N), SA = new Float64Array(N);
  for (var i0 = 0; i0 < N; i0++) { CA[i0] = Math.cos(i0 / N * TAU); SA[i0] = Math.sin(i0 / N * TAU); }

  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  // la clé stable d'une cellule : titre + personne (jamais l'id), le nom d'une Nuée, sinon sa position de repos arrondie
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) return k >>> 0; }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  // 1 au repos ; 0 → 1 pendant l'arrivée (Toile vivante seulement) ; 1 → 0 pendant le départ
  function _fac(s, now) {
    if (s.part != null) return 1 - _lisse((now - s.part) / RET);
    if (env.trans && s.t0 != null) return _lisse((now - s.t0) / ARR);
    return 1;
  }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _lumR(c) { function l(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); } return 0.2126 * l(c[0]) + 0.7152 * l(c[1]) + 0.0722 * l(c[2]); }
  // la chute : une nuance de la couleur de SA dalle — vers le sombre si elle est claire, vers le clair si elle est sombre
  var NUANCE = 0.38;
  function _nuance(c) { var b = _lumR(c) > 0.3 ? 0 : 255; return [c[0] + (b - c[0]) * NUANCE, c[1] + (b - c[1]) * NUANCE, c[2] + (b - c[2]) * NUANCE]; }

  /* --- le vocabulaire de la planche : `coupe` (lobes libres), `facette` (ciseaux droits), `trace` (courbe par milieux) --- */
  function _coupe(q, lobes) {
    var n = 180, amps = [], wid = [], k;
    for (k = 0; k < lobes; k++) { amps.push(0.55 + 0.45 * q()); wid.push(0.55 + 0.9 * q()); }
    var pinch = 0.28 + 0.3 * q(), sk = (q() - 0.5) * 0.9, pts = [];
    for (var i = 0; i < n; i++) {
      var a = i / n * TAU, u2 = (a / TAU) * lobes, kk = Math.floor(u2), f = u2 - kk, w = wid[kk % lobes];
      var lob = Math.pow(Math.sin(Math.PI * Math.pow(f, w > 1 ? 1 / w : 1)), 0.55 + 0.4 * w * 0.5);
      var r = (pinch + (1 - pinch) * lob * amps[kk % lobes]) * (1 + sk * Math.sin(a) * 0.3);
      pts.push([Math.cos(a) * r, Math.sin(a) * r]);
    }
    return pts;
  }
  function _facette(q, rot) {   // unité : centrée en 0, taille 1
    var m = 5 + Math.floor(q() * 3), el = 0.45 + 0.35 * q(), pts = [], a = q() * TAU;
    for (var k = 0; k < m; k++) { a += (TAU / m) * (0.55 + 0.9 * q()); var r = 0.55 + 0.45 * q(), lx = Math.cos(a) * r, ly = Math.sin(a) * r * el;
      pts.push([lx * Math.cos(rot) - ly * Math.sin(rot), lx * Math.sin(rot) + ly * Math.cos(rot)]); }
    return pts;
  }
  function _trace(T, pts) {
    var n = pts.length, a = pts[n - 1], b = pts[0];
    T.moveTo((a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
    for (var i = 0; i < n; i++) { var p = pts[i], q2 = pts[(i + 1) % n]; T.quadraticCurveTo(p[0], p[1], (p[0] + q2[0]) / 2, (p[1] + q2[1]) / 2); }
    T.closePath();
  }
  function _poly(T, pts) { T.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) T.lineTo(pts[i][0], pts[i][1]); T.closePath(); }
  function _coeurPts(w1, w2, n) {
    var pts = [];
    for (var k = 0; k < n; k++) { var t = k / n * TAU, s = Math.sin(t);
      pts.push([16 * s * s * s * (s > 0 ? w1 : w2), -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) - 3]); }
    return pts;
  }

  /* --- ce qu'une dalle tire de SA clé, une fois pour toutes (le profil, les méplats, le trou, la chute) --- */
  var _par = {};
  function _param(k) {
    var P = _par[k]; if (P) return P;
    var q = _lcg(k ^ 0xa11e), coeur = (k % 4) === 0, F = new Float64Array(N), i, mx = 0, rot;
    if (coeur) {
      rot = (q() - 0.5) * 0.6;
      var pts = _coeurPts(0.9 + 0.2 * q(), 0.9 + 0.2 * q(), 200), ang = pts.map(function (v) { return [Math.atan2(v[1], v[0]), Math.hypot(v[0], v[1])]; });
      for (i = 0; i < N; i++) { var a = i / N * TAU - Math.PI, bd = 9, br = 0;
        for (var j = 0; j < ang.length; j++) { var d = Math.abs(ang[j][0] - a); d = Math.min(d, TAU - d); if (d < bd) { bd = d; br = ang[j][1]; } }
        F[(i + N / 2) % N] = br; if (br > mx) mx = br; }
    } else {
      rot = q() * TAU;
      var nl = 3 + Math.floor(q() * 6), cp = _coupe(q, nl);
      for (i = 0; i < N; i++) { var v = cp[Math.floor(i * cp.length / N)]; F[i] = Math.hypot(v[0], v[1]); if (F[i] > mx) mx = F[i]; }
    }
    for (i = 0; i < N; i++) F[i] /= (mx || 1);
    if (!coeur && nl >= 5) for (i = 0; i < N; i++) F[i] = Math.pow(F[i], 1.5);   // étoiles et fleurs : échancrures tirées vers l'intérieur
    var M = new Float64Array(N), sh = Math.round(rot / TAU * N);
    for (i = 0; i < N; i++) { var fr = Math.max(0.05, F[((i - sh) % N + N) % N]); M[i] = coeur ? 0.5 + 0.5 * fr : 0.3 + 0.7 * fr; }
    // le coup de ciseaux : de petits méplats, là où la lame a tourné
    var mep = [];
    for (i = 0; i < N - 8; i += 7 + Math.floor(q() * 6)) mep.push([i, Math.min(N - 1, i + 3 + Math.floor(q() * 4))]);
    var trou = null;
    if (q() < 0.4) { var ha = q() * TAU, hr = 0.42 + 0.12 * q(), hs = 0.22 + 0.14 * q(), hrot = q() * TAU; trou = { a: ha, r: hr, s: hs, pts: _facette(q, hrot) }; }
    var chute = null;
    if (q() < 0.55) {
      var ci = Math.floor(q() * N), sf = 0.38 + 0.14 * q(), m = 5 + Math.floor(q() * 3), el = 0.4 + 0.35 * q(), rj = (q() - 0.5) * 1.6, a2 = q() * TAU, loc = [];
      for (var kk = 0; kk < m; kk++) { a2 += (TAU / m) * (0.55 + 0.9 * q()); var rr = 0.55 + 0.45 * q(); loc.push([Math.cos(a2) * rr, Math.sin(a2) * rr * el]); }
      chute = { i: ci, s: sf, rj: rj, loc: loc };
    }
    var z = _lcg(k ^ 0x5eed)();
    return (_par[k] = { M: M, mep: mep, trou: chute ? null : trou, chute: chute, z: z });
  }

  /* ⚑ v67 — AU REPOS, UNE POSITION RESTE GELÉE. Au-delà d'une trentaine de paroles, le moteur n'arrive jamais tout à fait au repos : ses
     graines oscillent d'une image à l'autre, sans fin (mesuré à 40 : 0,5 à 3 px, deux graines qui rebondissent) — la géométrie se
     refaisait à chaque image. Hors transition, une graine garde sa position tant qu'elle ne s'en éloigne pas de plus de 0,25 × l'unité
     de matière (un vrai ressemis la déplace bien plus) ; pendant une
     transition, les positions vivent (et le gel reprend exactement où elles finissent). */
  var _gel = {};
  function _geler(L) { var tol = (env.uMat || 70) * 0.25, vive = env.vive, tr = env.trans;
    L.forEach(function (e) { var k = e.k != null ? e.k : e.h, f = _gel[k];
      if (vive && tr) { _gel[k] = [e.x, e.y]; return; }
      if (f && Math.abs(e.x - f[0]) < tol && Math.abs(e.y - f[1]) < tol) { e.x = f[0]; e.y = f[1]; }
      else if (vive) _gel[k] = [e.x, e.y]; }); }
  /* --- la géométrie de toutes les dalles d'une surface, gardée tant que rien ne bouge (au demi-pixel) --- */
  var _geo = {};   // par surface (W×H), au plus quatre
  function _dalles(now) {
    var D = [], i, s, n = seeds.length, perte = 0;
    for (i = 0; i < n; i++) { s = seeds[i]; if (s.kind === 'gray') continue;
      var f = _fac(s, now); perte += 1 - f;
      D.push({ s: s, k: _cle(s), x: s.x, y: s.y, f: f }); }   // la position de REPOS : le frémissement du moteur n'est pas pour ce monde (contrat §7.1)
    var u = avg() * Math.sqrt(Math.max(1, n) / Math.max(1, n - perte));
    _geler(D);
    var h = 2166136261;
    function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(u * 16)); mix(Math.round((env.uMat || 0) * 16)); mix(env.cleToile == null ? 0 : env.cleToile);
    for (i = 0; i < D.length; i++) { mix(D[i].k); mix(Math.round(D[i].x * 2)); mix(Math.round(D[i].y * 2)); mix(Math.round(D[i].f * 512)); }
    var cle = Math.round(W) + 'x' + Math.round(H), G = _geo[cle];
    if (G && G.h === h) return G;
    D.sort(function (a, b) { return (b.s.part != null ? 1 : 0) - (a.s.part != null ? 1 : 0) || a.k - b.k; });
    for (i = 0; i < D.length; i++) _forme(D[i], D, u);
    var ks = Object.keys(_geo); if (ks.length > 4 && !_geo[cle]) delete _geo[ks[0]];
    return (_geo[cle] = { h: h, D: D, u: u, mat: null });
  }
  function _forme(p, D, u) {
    var P = _param(p.k), R = u * (0.36 + 0.2 * P.z + 0.26 * P.z * P.z * P.z) * window._tailleApercu(p.s), R3 = R * 3 * p.f, lim = new Float64Array(N), i, j;
    p.vide = p.f < 0.01;
    if (p.vide) return;
    for (i = 0; i < N; i++) lim[i] = R3;
    // la place, direction par direction : jusqu'à la part de l'écart qui revient à cette dalle (la moitié au repos ;
    // une dalle qui arrive ou qui part n'en a que sa part, ses voisines prennent le reste — jamais un saut)
    for (j = 0; j < D.length; j++) {
      var o = D[j]; if (o === p || o.f <= 0) continue;
      var dx = o.x - p.x, dy = o.y - p.y, d = Math.hypot(dx, dy); if (d < 1e-6) continue;
      var ux = dx / d, uy = dy / d, dd = d * p.f / (p.f + o.f);
      for (i = 0; i < N; i++) { var c = ux * CA[i] + uy * SA[i]; if (c > 0.02) { var L = dd / c; if (L < lim[i]) lim[i] = L; } }
    }
    var mean = 0; for (i = 0; i < N; i++) { lim[i] *= 0.99; mean += Math.min(lim[i], R3); } mean /= N;
    var cap = Math.max(mean * 1.9, R3); for (i = 0; i < N; i++) if (lim[i] > cap) lim[i] = cap;
    for (var pass = 0; pass < 6; pass++) { var c2 = lim.slice(); for (i = 0; i < N; i++) lim[i] = (c2[(i + N - 2) % N] + c2[(i + N - 1) % N] + 2 * c2[i] + c2[(i + 1) % N] + c2[(i + 2) % N]) / 6; }
    var rad = new Float64Array(N), main = new Array(N), rmax = 0;
    for (i = 0; i < N; i++) { rad[i] = lim[i] * 1.07 * P.M[i]; if (rad[i] > rmax) rmax = rad[i]; main[i] = [p.x + CA[i] * rad[i], p.y + SA[i] * rad[i]]; }
    for (var e = 0; e < P.mep.length; e++) { var a0 = P.mep[e][0], b0 = P.mep[e][1], A = main[a0], B = main[b0];
      for (var k = a0 + 1; k < b0; k++) { var t = (k - a0) / (b0 - a0); main[k] = [A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]; } }
    p.rad = rad; p.rmax = rmax; p.main = main; p.trou = null; p.chute = null; p.T = null; p.C = null; p.cx = p.x; p.cy = p.y; p.cr = 0;
    if (P.trou) { var it = Math.floor(P.trou.a / TAU * N) % N, rr = Math.hypot(main[it][0] - p.x, main[it][1] - p.y) * P.trou.r,
        hx = p.x + Math.cos(P.trou.a) * rr, hy = p.y + Math.sin(P.trou.a) * rr, hs = rr * P.trou.s;
      p.trou = P.trou.pts.map(function (v) { return [hx + v[0] * hs, hy + v[1] * hs]; }); }
    if (P.chute) {
      var mR = 0; for (i = 0; i < N; i++) mR += Math.hypot(main[i][0] - p.x, main[i][1] - p.y); mR /= N;
      var v = main[P.chute.i], far = Math.hypot(v[0] - p.x, v[1] - p.y) || 1e-6, sz = mR * P.chute.s, dirx = (v[0] - p.x) / far, diry = (v[1] - p.y) / far,
          ix = v[0] - dirx * sz * 0.25, iy = v[1] - diry * sz * 0.25, rot = Math.atan2(diry, dirx) + P.chute.rj, cr = Math.cos(rot), sr = Math.sin(rot), cm = 0;
      p.chute = P.chute.loc.map(function (w) { var lx = w[0] * sz, ly = w[1] * sz, X = ix + lx * cr - ly * sr, Y = iy + lx * sr + ly * cr; cm = Math.max(cm, Math.hypot(X - ix, Y - iy)); return [X, Y]; });
      p.cx = ix; p.cy = iy; p.cr = cm;
    }
  }

  /* --- la matière : un semis de découpes à pas propre, tiré de la clé de la Toile ; chacune rétrécit pour laisser la place --- */
  var _champs = {};
  function _champ(um) {
    var ct = env.cleToile, cle = Math.round(W) + 'x' + Math.round(H) + ':' + Math.round(um * 8) + ':' + (ct == null ? 0 : ct);
    if (_champs[cle]) return _champs[cle];
    var q = _lcg(((ct == null ? 1 : ct) ^ 0xb0e11a) >>> 0), rmin = um * 0.12, rmax = um * 0.30, jeu = um * 0.07,
        pas = rmax * 2 + jeu, cols = Math.ceil((W + 2 * rmax) / pas) + 1, rows = Math.ceil((H + 2 * rmax) / pas) + 1, grille = {}, L = [], rate = 0, essais = 0;
    while (rate < 1800 && essais < 40000) {
      essais++;
      var x = -rmax + q() * (W + 2 * rmax), y = -rmax + q() * (H + 2 * rmax), v = q(), r = rmin + (rmax - rmin) * v * v;
      var gx = Math.floor((x + rmax) / pas), gy = Math.floor((y + rmax) / pas), ok = true;
      for (var a = gx - 1; a <= gx + 1 && ok; a++) for (var b = gy - 1; b <= gy + 1 && ok; b++) {
        var cel = grille[a + ',' + b]; if (!cel) continue;
        for (var z = 0; z < cel.length; z++) { var o = cel[z]; if (Math.hypot(o.x - x, o.y - y) < r + o.r + jeu) { ok = false; break; } } }
      if (!ok) { rate++; continue; }
      rate = 0;
      var pc = { x: x, y: y, r: r, ton: Math.floor(q() * 5), pts: null }, coeur = q() < 0.25, pts, i, mx = 0;
      if (coeur) {
        var rot = (q() - 0.5) * 0.6, cr = Math.cos(rot), sr = Math.sin(rot);
        pts = _coeurPts(0.9 + 0.2 * q(), 0.9 + 0.2 * q(), 48).map(function (w) { return [w[0] * cr - w[1] * sr, w[0] * sr + w[1] * cr]; });
        for (i = 0; i < pts.length; i++) mx = Math.max(mx, Math.hypot(pts[i][0], pts[i][1]));
        pts = pts.map(function (w) { var d = Math.hypot(w[0], w[1]) || 1e-6, rr = (0.5 + 0.5 * d / mx); return [w[0] / d * rr, w[1] / d * rr]; });
      } else {
        var nl = 3 + Math.floor(q() * 3), rot2 = q() * TAU, cp = _coupe(q, nl), c3 = Math.cos(rot2), s3 = Math.sin(rot2);
        for (i = 0; i < cp.length; i++) mx = Math.max(mx, Math.hypot(cp[i][0], cp[i][1]));
        pts = [];
        for (i = 0; i < cp.length; i += 4) { var w = cp[i], d = Math.hypot(w[0], w[1]) || 1e-6, F = d / mx; if (nl >= 5) F = Math.pow(F, 1.5);
          var rr2 = 0.3 + 0.7 * F, X = w[0] / d * rr2, Y = w[1] / d * rr2; pts.push([X * c3 - Y * s3, X * s3 + Y * c3]); }
      }
      mx = 0; for (i = 0; i < pts.length; i++) mx = Math.max(mx, Math.hypot(pts[i][0], pts[i][1]));
      pc.pts = pts.map(function (w) { return [w[0] / mx, w[1] / mx]; });
      L.push(pc); (grille[gx + ',' + gy] || (grille[gx + ',' + gy] = [])).push(pc);
    }
    var ks = Object.keys(_champs); if (ks.length > 3) delete _champs[ks[0]];
    return (_champs[cle] = { L: L, jeu: jeu });
  }
  // la matière posée : chaque découpe rétrécit jusqu'à tenir hors des dalles, à un jeu près (continûment : jamais d'un coup)
  function _matiere(G) {
    if (G.mat) return G.mat;
    var um = env.uMat, C = _champ(um), T = [new Path2D(), new Path2D(), new Path2D(), new Path2D(), new Path2D()], D = G.D, nv = 0;
    for (var i = 0; i < C.L.length; i++) {
      var pc = C.L[i], lib = 1e18;
      for (var j = 0; j < D.length; j++) {
        var p = D[j]; if (p.vide) continue;
        var dx = pc.x - p.x, dy = pc.y - p.y, d = Math.hypot(dx, dy);
        if (d - p.rmax - pc.r * 2 < lib) {
          var a = Math.atan2(dy, dx); if (a < 0) a += TAU;
          var f = a / TAU * N, i0 = Math.floor(f) % N, t = f - Math.floor(f), rp = p.rad[i0] * (1 - t) + p.rad[(i0 + 1) % N] * t;
          if (d - rp < lib) lib = d - rp;
        }
        if (p.chute) { var dc = Math.hypot(pc.x - p.cx, pc.y - p.cy) - p.cr; if (dc < lib) lib = dc; }
      }
      var e1 = Math.max(0, Math.min(1, (lib - C.jeu) / pc.r)), sc = e1 * _lisse((e1 - 0.3) / 0.4);
      if (sc < 0.02) continue;
      var rr = pc.r * sc; nv++;
      _trace(T[pc.ton], pc.pts.map(function (w) { return [pc.x + w[0] * rr, pc.y + w[1] * rr]; }));
    }
    return (G.mat = { T: T, n: nv });
  }

  // les tracés d'une dalle se font une fois par géométrie (ils vivent sur elle, et elle ne vit que tant que rien ne bouge)
  function _peindre(p, now) {
    var col = cOf(p.s, now);
    if (!p.T) { p.T = new Path2D(); _trace(p.T, p.main); if (p.trou) _trace(p.T, p.trou.slice().reverse());
      if (p.chute) { p.C = new Path2D(); _poly(p.C, p.chute); } }
    g.fillStyle = _rgb(col); g.fill(p.T, 'evenodd');
    if (p.C) { g.fillStyle = _rgb(_nuance(col)); g.fill(p.C); }
  }

  function Rbro(now, x0, y0, x1, y1) {
    _sync();
    var G = _dalles(now), M = _matiere(G), R = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, i;
    if (R) for (i = 0; i < 5; i++) { g.fillStyle = _rgb(R[i % R.length]); g.fill(M.T[i]); }
    for (i = 0; i < G.D.length; i++) if (!G.D[i].vide) _peindre(G.D[i], now);
    window._broComp = { dalles: G.D.length, matiere: M.n, u: G.u };   /* publié : un juge lit la composition, pas les pixels (§7) */
  }

  function _trouve(s, now) { var G = _dalles(now || performance.now()), k = _cle(s);
    for (var i = 0; i < G.D.length; i++) if (G.D[i].s === s) return G.D[i];
    for (i = 0; i < G.D.length; i++) if (G.D[i].k === k) return G.D[i];
    return null; }
  function _bb(p) { var a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18, L = p.chute ? p.main.concat(p.chute) : p.main;
    for (var i = 0; i < L.length; i++) { var X = L[i][0], Y = L[i][1]; if (X < a0) a0 = X; if (X > a1) a1 = X; if (Y < b0) b0 = Y; if (Y > b1) b1 = Y; }
    return [a0, b0, a1, b1]; }
  function _pip(x, y, pts) { var ins = false, n = pts.length;
    for (var i = 0, j = n - 1; i < n; j = i++) { var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins; }
    return ins; }

  function seule(nom, s, now, cx, cy, taille) {
    _sync(); var p = _trouve(s, now); if (!p || p.vide) return false;
    var B = _bb(p), sc = taille / Math.max(B[2] - B[0], B[3] - B[1], 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(B[0] + B[2]) / 2, -(B[1] + B[3]) / 2);
    _peindre(p, now); g.restore();
    return true;
  }
  function contour(nom, s) { _sync(); var p = _trouve(s); return p && !p.vide ? p.main.slice() : null; }
  function nature(nom, s) { _sync(); var p = _trouve(s); return p && !p.vide ? 'dalle' : null; }
  function boite(nom, s) { _sync(); var p = _trouve(s); if (!p || p.vide) return null; var B = _bb(p);
    return { x0: B[0], y0: B[1], x1: B[2], y1: B[3], fx0: B[0], fy0: B[1], fx1: B[2], fy1: B[3] }; }
  // le toucher : sur ce qui est PEINT — la chute, la découpe hors de son trou ; de la dalle du dessus vers celle du dessous
  function toucher(nom, x, y) {
    _sync(); var G = _dalles(performance.now());
    for (var i = G.D.length - 1; i >= 0; i--) { var p = G.D[i]; if (p.vide || p.s.part != null) continue;
      if (p.chute && _pip(x, y, p.chute)) return p.s;
      if (Math.hypot(x - p.x, y - p.y) > p.rmax + 1e-6) continue;
      if (_pip(x, y, p.main) && !(p.trou && _pip(x, y, p.trou))) return p.s; }
    return null;
  }

  Rbro.transDur = 1600; Rbro.douce = true; Rbro.partDur = 900; Rbro.toucheStrict = true;
  return { brouillamini: Rbro, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerBrouillamini = creerBrouillamini;
})();

/* ══════════════════ bloc « lot-V63-CHAMADE » ══════════════════ */
/* ⚑ v63 (27 sept. 2026) — CHAMADE, la page rayée au feutre. Porté de `coeurs()` (la SECONDE définition de la planche « Trois
   matières », l. 2398 — PORTAGE-SAISON2 n° 8) au CONTRAT-MONDE, sur le patron de Brouillamini (§15.13) :
   · u = avg() (compte pondéré pendant une transition) pour les cœurs ; la PAGE (bandes, marges, joints, traits) a pour unité
     celle de la matière, `uMat` : elle ne dézoome pas. K = uMat / 53,55 ramène les cotes de la planche (Toile 300 × 650).
   · LCG sur la clé stable ; la page tirée de `Toile.cle()`.
   · La dalle, c'est le cœur : sa couleur est cOf ; la « seconde couleur » de la planche devient une NUANCE de cOf (décision
     de Tom pour Brouillamini : une autre couleur de palette dirait une autre nature). L'ENCRE — les bandes, le trait qui cerne
     un cœur, l'anneau d'encre d'une coulée — est l'encre du produit (`_tfInk`, le précédent de Touffe), jamais un ton de palette.
   · « Le cœur efface la page sous lui » : sur la Toile, les bandes sont peintes HORS des cœurs (un découpage pair-impair,
     une fois) ; on voit le fond du moteur, jamais une couleur de papier posée par-dessus. La dalle seule, elle, porte son
     papier : `fondToile()`.
   · Arrivée : le cœur neuf grandit de rien, ses voisins s'écartent peu à peu. Départ : il rétrécit, ils reprennent la place.
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerChamade(env) {
  var g, W, H, seeds, cOf, avg;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; avg = env.avg; }
  var TAU = 6.283185307179586, UPL = 53.55;   // l'unité de matière de la planche (300 × 650, 68 graines)
  var ARR = 900, RET = 760;

  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    /* v98 (500 paroles) : la clé d'une parole se cherche parmi toutes les paroles ; gardée une seconde sur la graine */
    if (pid != null && s._chK != null && s._chKp === pid && performance.now() - s._chKt < 1000) return s._chK;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) { s._chK = k >>> 0; s._chKp = pid; s._chKt = performance.now(); return k >>> 0; } }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  function _fac(s, now) {
    if (s.part != null) return 1 - _lisse((now - s.part) / RET);
    if (env.trans && s.t0 != null) return _lisse((now - s.t0) / ARR);
    return 1;
  }
  function _arr(c) { if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; } return c; }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _lumR(c) { function l(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); } return 0.2126 * l(c[0]) + 0.7152 * l(c[1]) + 0.0722 * l(c[2]); }
  var NUANCE = 0.38;   // la même que Brouillamini (Q330)
  // un point sur trois, les deux bouts gardés : la courbe par les milieux redonne la même ligne (budget)
  function _clairseme(P) { var o = []; for (var i = 0; i < P.length; i += 3) o.push(P[i]); if ((P.length - 1) % 3) o.push(P[P.length - 1]); return o; }
  function _nuance(c) { var b = _lumR(c) > 0.3 ? 0 : 255; return [c[0] + (b - c[0]) * NUANCE, c[1] + (b - c[1]) * NUANCE, c[2] + (b - c[2]) * NUANCE]; }
  function _encre() { return _arr(typeof env.encre === 'function' ? env.encre() : env.encre); }
  // un trait de feutre : presque droit, il ondule doucement (amplitudes de la planche, × K)
  function _feutre(R, len, K) {
    var ph = [R() * 6.28, R() * 6.28, R() * 6.28], am = [0.6 + 0.8 * R(), 0.25 + 0.4 * R(), 0.15 + 0.2 * R()], fr = [1.1 + 0.8 * R(), 3 + 2 * R(), 7 + 4 * R()];
    return function (u) { return K * (am[0] * Math.sin(u / len * fr[0] * 6.28 + ph[0]) + am[1] * Math.sin(u / len * fr[1] * 6.28 + ph[1]) + am[2] * Math.sin(u / len * fr[2] * 6.28 + ph[2])); };
  }
  function _traceMil(T, pts) {
    var n = pts.length, a = pts[n - 1], b = pts[0];
    T.moveTo((a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
    for (var i = 0; i < n; i++) { var p = pts[i], q2 = pts[(i + 1) % n]; T.quadraticCurveTo(p[0], p[1], (p[0] + q2[0]) / 2, (p[1] + q2[1]) / 2); }
    T.closePath();
  }
  function _poly(T, pts) { T.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) T.lineTo(pts[i][0], pts[i][1]); T.closePath(); }
  function _pip(x, y, pts) { var ins = false, n = pts.length;
    for (var i = 0, j = n - 1; i < n; j = i++) { var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins; }
    return ins; }

  /* --- ce qu'un cœur tire de SA clé (la planche : rng(p.h ^ 0xc0e5), puis rng(p.h ^ 0x77) pour son remplissage) --- */
  var _par = {};
  function _param(k) {
    var P = _par[k]; if (P) return P;
    var q = _lcg(k ^ 0xc0e5);
    P = { sx: 0.78 + 0.5 * q(), sy: 0.78 + 0.45 * q(), lobe: 0.55 + 0.9 * q(), tip: 0.7 + 0.7 * q(), tilt: (q() - 0.5) * 1.1, asym: (q() - 0.5) * 0.45,
          plump: q() * 0.45, lobeL: 0.8 + 0.4 * q(), lobeR: 0.8 + 0.4 * q() };
    P.q0 = q() * 6.28; P.q1 = q() * 6.28; P.mode = q() < 0.45 ? 3 : (q() < 0.5 ? 0 : 2); P.ang = (q() - 0.5) * 1.4;
    P.z = _lcg(k ^ 0x5eed)();
    return (_par[k] = P);
  }

  /* --- la page : bandes d'encre presque horizontales, une grande onde commune, des remous — tirée de la clé de la Toile --- */
  var _pages = {};
  function _page(K) {
    var ct = env.cleToile, cle = Math.round(W) + 'x' + Math.round(H) + ':' + Math.round(K * 4096) + ':' + (ct == null ? 0 : ct);
    if (_pages[cle]) return _pages[cle];
    var R = _lcg(((ct == null ? 1 : ct) ^ 0x5e1f) >>> 0), L3 = 300 * K, per = L3 / 21, k = K, ph = [R() * 6.28, R() * 6.28, R() * 6.28, R() * 6.28];
    var zones = []; for (var z = 0; z < 3; z++) zones.push([R() * W, R() * H, L3 * (0.18 + 0.15 * R()), (R() < 0.5 ? -1 : 1) * (10 + 10 * R()) * k, 30 + 30 * R()]);
    function D(x, y) {
      var amp = 1 + 0.75 * Math.sin(y / (210 * k) + ph[2] * 1.3) * Math.sin(x / (160 * k) + ph[1]);
      var d = amp * k * (16 * Math.sin(x / (95 * k) + y / (170 * k) + ph[0]) + 9 * Math.sin(x / (52 * k) - y / (230 * k) + ph[1]) + 7 * Math.sin(y / (120 * k) + ph[2]) * Math.sin(x / (75 * k) + ph[3]));
      for (var i = 0; i < zones.length; i++) { var Z = zones[i], r2 = ((x - Z[0]) * (x - Z[0]) + (y - Z[1]) * (y - Z[1])) / (Z[2] * Z[2]); d += Z[3] * Math.exp(-r2) * Math.sin((x - Z[0]) / (Z[4] * k)); }
      return d;
    }
    /* ⚑ budget — la planche échantillonne tous les 5 × K, en segments. Un point tous les 10 × K relié par des COURBES (par les
       milieux) redonne la même ligne : le plus fin tremblé du feutre a une longueur d'onde d'au moins ~35 px. Moitié moins de sommets. */
    var T = new Path2D(), m = 4 * K, pas = 10 * K;
    for (var y = -per * 3; y < H + per * 3; y += per * (0.92 + 0.16 * R())) {
      var top = _feutre(R, W, K), bot = _feutre(R, W, K), th = per * (0.42 + 0.16 * R()), x, P = [];
      P.push([-m, y + D(-m, y) + top(-m)]);
      for (x = 0; x <= W + m; x += pas) P.push([x, y + D(x, y) + top(x)]);
      for (x = W + m; x >= -m; x -= pas) P.push([x, y + th + D(x, y + th) + bot(x)]);
      _traceMil(T, P);
    }
    var ks = Object.keys(_pages); if (ks.length > 3) delete _pages[ks[0]];
    return (_pages[cle] = { T: T });
  }

  /* --- les cœurs : chacun à sa forme, ramené dans la page, écarté des autres, jamais touchant --- */
  /* ⚑ la relaxation de la planche est GLOBALE et repart de zéro : refaite à chaque image sur des graines qui glissent, elle faisait
     bouger TOUS les cœurs, par à-coups (mesuré : 6 à 25 niveaux d'une image à l'autre, 30 images/s). Pendant une transition, on
     calcule donc DEUX dispositions — celle qu'on voyait, et celle d'arrivée, sur les places finales que le moteur publie
     (`env.finale`) — et chaque cœur glisse de l'une à l'autre ; le neuf grandit, celui qui part rétrécit. La FORME d'un cœur se
     calcule une fois (à son échelle) et se pose par une translation et une échelle. Au repos, l'image est celle de la planche. */
  var MOVE = 1200, _tr = null, _aff = null, _fige = null;   // _fige : la disposition d'arrivée de la dernière transition, gardée au repos
  var _geo = {};
  function _unite() { return env.uMat / UPL; }
  // les places : celles où le moteur POSE les graines (`env.finale`, son point fixe) — au repos comme à l'arrivée d'une transition,
  // sans quoi la disposition de fin de transition et celle du repos diffèrent, et la Toile saute à la dernière image
  /* ⚑ v98 (Tom : 500 paroles) — le point fixe du moteur se recalcule dès qu'une graine bouge ; à 500 il coûte cher et le cœur le
     demande plusieurs fois par image. Quand il a coûté plus de 40 ms, on garde la réponse précédente pendant quatre fois ce coût (une
     graine neuve, absente de l'ancienne réponse, prend sa place courante) ; le repos le redemande, donc l'état posé est exact. */
  var _fC = null, _fCout = 0, _fFin = 0;
  function _fin() { if (_fC && _fCout > 40 && performance.now() - _fFin < _fCout * 4) { if (typeof env.relance === 'function') env.relance(); return _fC; }
    var t0 = performance.now(), F = null; try { F = env.finale || null; } catch (_) { F = null; }
    var dt = performance.now() - t0; if (dt > 5 || !_fC) { _fC = F; _fFin = performance.now(); _fCout = dt; } else if (F !== _fC) { _fC = F; _fCout = dt; } return F; }
  function _liste(now, fin) {
    var D = [], i, s, n = seeds.length, perte = 0, FP = fin || _fin();
    for (i = 0; i < n; i++) { s = seeds[i]; if (s.kind === 'gray') continue;
      if (fin && s.part != null) continue;
      var f = fin ? 1 : _fac(s, now); perte += 1 - f;
      var q = FP ? FP.get(s) : null;
      D.push({ s: s, k: _cle(s), x: q ? q[0] : (s.px != null ? s.px : s.x), y: q ? q[1] : (s.py != null ? s.py : s.y), f: f }); }
    var nn = fin ? D.length : n - perte;
    return { D: D, u: avg() * Math.sqrt(Math.max(1, n) / Math.max(1, nn)) };   // u = avg(), le compte pondéré par l'arrivée et le départ
  }
  function _trie(D) { D.sort(function (a, b) { return (b.s.part != null ? 1 : 0) - (a.s.part != null ? 1 : 0) || a.k - b.k; }); }
  var _chCout = 0, _chFin = 0;
  function _coeurs(now) {
    var K = _unite(), TR = env.vive ? env.trans : null, D, u, i;
    if (TR) {
      if (!_tr || _tr.n !== TR.n) _tr = { n: TR.n, L0: _aff, L1: null };
      if (!_tr.L1) { var F = null; try { F = env.finale; } catch (_) { F = null; }
        var A = _liste(now, F || new Map()); _trie(A.D); _pose(A.D, A.u, K);
        _tr.L1 = {}; A.D.forEach(function (p) { if (!p.vide) _tr.L1[p.k] = { s: p.s, P: p.P, R: p.R, cx: p.cx, cy: p.cy, sc: p.sc }; }); }
      var a = _lisse((now - TR.t0) / MOVE), L0 = _tr.L0 || {}, L1 = _tr.L1, k;
      D = [];
      for (k in L1) { var e1 = L1[k], e0 = L0[k];
        if (e0) D.push({ s: e1.s, k: +k, P: e1.P, R: e1.R, f: 1, cx: e0.cx + (e1.cx - e0.cx) * a, cy: e0.cy + (e1.cy - e0.cy) * a, sc: e0.sc + (e1.sc - e0.sc) * a, sref: e1.sc });
        else D.push({ s: e1.s, k: +k, P: e1.P, R: e1.R, f: a, cx: e1.cx, cy: e1.cy, sc: e1.sc * a, sref: e1.sc }); }
      for (k in L0) if (!L1[k]) { var d0 = L0[k]; D.push({ s: d0.s, k: +k, P: d0.P, R: d0.R, f: 1 - a, cx: d0.cx, cy: d0.cy, sc: d0.sc * (1 - a), sref: d0.sc }); }
      _trie(D); u = null;
      if (a >= 1) _fige = L1;
    } else if ((env.vive && _fige && _memesCles(_fige)) || (!env.vive && _aff && _affW === W && _affH === H && _memesCles(_aff))) {
      var _src = env.vive ? _fige : _aff;
      /* au repos après une transition : la disposition d'arrivée RESTE. Recalculée ici, elle tomberait sur un autre point fixe du
         moteur (mesuré : un cœur sautait de 42 px à la fin de la transition). Elle ne se recalcule qu'au changement suivant. */
      D = []; for (var kf in _src) { var ef = _src[kf]; D.push({ s: ef.s, k: +kf, P: ef.P, R: ef.R, f: 1, cx: ef.cx, cy: ef.cy, sc: ef.sc, sref: ef.sc }); }
      _trie(D); u = null;
    } else {
      if (env.vive) _fige = null;
      var L = _liste(now, null); D = L.D; u = L.u;
      var h = 2166136261;
      function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
      mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(u * 16)); mix(Math.round(env.uMat * 16));
      for (i = 0; i < D.length; i++) { mix(D[i].k); mix(Math.round(D[i].x * 2)); mix(Math.round(D[i].y * 2)); mix(Math.round(D[i].f * 512)); }
      var cle = Math.round(W) + 'x' + Math.round(H), G0 = _geo[cle];
      if (G0 && G0.h === h) { if (env.vive) _memo(G0.D); return G0; }
      /* ⚑ v98 (Tom : 500 paroles) — le budget de Mascaret : une disposition qui a coûté plus de 40 ms n'est refaite qu'après quatre
         fois son coût ; entre-temps on garde la précédente, et le moteur est relancé pour revenir poser l'état final. */
      if (G0 && _chCout > 40 && performance.now() - _chFin < _chCout * 4) { if (typeof env.relance === 'function') env.relance(); if (env.vive) _memo(G0.D); return G0; }
      else { var _chT0 = performance.now();
      _trie(D); _pose(D, u, K); D.forEach(function (p) { p.sref = p.sc; });
      var G1 = { h: h, D: D, u: u, K: K };
      var ks = Object.keys(_geo); if (ks.length > 4 && !_geo[cle]) delete _geo[ks[0]];
      _geo[cle] = G1; for (var _pi = 0; _pi < D.length; _pi++) _place(D[_pi], K); _chFin = performance.now(); _chCout = _chFin - _chT0; }
    }
    for (i = 0; i < D.length; i++) _place(D[i], K);
    if (env.vive) _memo(D);
    return { D: D, u: u, K: K };
  }
  function _memesCles(M) { var n = 0, i, s; for (i = 0; i < seeds.length; i++) { s = seeds[i]; if (s.kind === 'gray' || s.part != null) continue; n++; if (!M[_cle(s)]) return false; } return n === Object.keys(M).length; }
  var _affW = 0, _affH = 0;
  function _memo(D) { _affW = W; _affH = H; var m = {}; D.forEach(function (p) { if (!p.vide && p.s.part == null) m[p.k] = { s: p.s, P: p.P, R: p.R, cx: p.cx, cy: p.cy, sc: p.sc }; }); _aff = m; }
  function _pose(D, u, K) {
    var L3 = 300 * K, mg = L3 * 0.03, jeu = L3 * 0.02, i, j, it, hs = [];
    for (i = 0; i < D.length; i++) { var p = D[i]; p.vide = p.f < 0.01; var P = _param(p.k), Rp = u * (0.36 + 0.2 * P.z + 0.26 * P.z * P.z * P.z) * window._tailleApercu(p.s);
      p.P = P; p.R = Rp; p.sc = Rp * 0.95 * p.f; p.cx = p.x; p.cy = p.y; if (!p.vide) hs.push(p); }
    function rad(q) { return q.sc * Math.max(q.P.sx, q.P.sy); }
    /* ⚑ v98 (Tom : « 1,2 seconde par image à 500 paroles, inutilisable ») — LES VOISINS, PAS TOUTES LES PAIRES. Les quatre passes
       comparaient chaque cœur à tous les autres, 77 fois : 10 millions de paires à 500. Au-delà de 80 cœurs, une grille donne pour chaque
       cœur les seuls cœurs assez proches pour le toucher (plus loin que la somme des deux plus grands rayons, une paire ne fait rien),
       dans le même ordre croissant. Jusqu'à 80 cœurs, toutes les paires, comme avant : l'aspect validé ne bouge pas. */
    var _TOUS = hs.length <= 80, _VL = null;
    function _vois() { if (_TOUS) return; var rm = 0, t; for (t = 0; t < hs.length; t++) rm = Math.max(rm, rad(hs[t]));
      var C = rm * 2 * 1.02 + jeu + 1e-6, G = new Map(), GX = [], GY = []; _VL = [];
      for (t = 0; t < hs.length; t++) { var gx = Math.floor(hs[t].cx / C), gy = Math.floor(hs[t].cy / C), kk = gx + ',' + gy; GX[t] = gx; GY[t] = gy; if (!G.has(kk)) G.set(kk, []); G.get(kk).push(t); }
      for (t = 0; t < hs.length; t++) { var o = []; for (var ox = -1; ox <= 1; ox++) for (var oy = -1; oy <= 1; oy++) { var Lb = G.get((GX[t] + ox) + ',' + (GY[t] + oy)); if (Lb) for (var z = 0; z < Lb.length; z++) if (Lb[z] > t) o.push(Lb[z]); }
        o.sort(function (x, y) { return x - y; }); _VL.push(o); } }
    function VO(i) { if (_TOUS) { var o = []; for (var t = i + 1; t < hs.length; t++) o.push(t); return o; } return _VL[i]; }
    function sMin(q) { return Math.max(q.R * 0.55, L3 * 0.05) * q.f / Math.max(q.P.sx, q.P.sy); }
    function borne(q) { var ex = q.sc * q.P.sx * 1.15, ey = q.sc * q.P.sy * 1.2;
      q.cx = Math.min(W - mg - ex, Math.max(mg + ex, q.cx)); q.cy = Math.min(H - mg - ey, Math.max(mg + ey, q.cy)); }
    // aucun cœur n'est coupé par le bord : il rentre dans la page, et rétrécit s'il le faut
    hs.forEach(function (q) { q.sc = Math.min(q.sc, (W - 2 * mg) / (2 * q.P.sx * 1.15), (H - 2 * mg) / (2 * q.P.sy * 1.2)); borne(q); });
    // d'abord les cœurs s'écartent, ensuite seulement le plus grand des deux rétrécit — jamais sous une taille lisible
    for (it = 0; it < 40; it++) { _vois(); for (i = 0; i < hs.length; i++) for (var q1 = 0, V1 = VO(i); q1 < V1.length; q1++) { j = V1[q1];
      var a = hs[i], b = hs[j], dx = b.cx - a.cx, dy = b.cy - a.cy, d = Math.hypot(dx, dy) || 1e-6, need = (rad(a) + rad(b)) * 1.02 + jeu;
      if (d < need) { var m2 = (need - d) * 0.25; a.cx -= dx / d * m2; a.cy -= dy / d * m2; b.cx += dx / d * m2; b.cy += dy / d * m2; } } }
    hs.forEach(borne);
    for (it = 0; it < 6; it++) { _vois(); for (i = 0; i < hs.length; i++) for (var q2 = 0, V2 = VO(i); q2 < V2.length; q2++) { j = V2[q2];
      var a2 = hs[i], b2 = hs[j], d2 = Math.hypot(a2.cx - b2.cx, a2.cy - b2.cy), need2 = (rad(a2) + rad(b2)) * 1.02 + jeu;
      if (d2 < need2) { var big = rad(a2) >= rad(b2) ? a2 : b2, oth = big === a2 ? b2 : a2, room = d2 - rad(oth) * 1.02 - jeu;
        big.sc = Math.max(sMin(big), Math.min(big.sc, room / (1.02 * Math.max(big.P.sx, big.P.sy)))); } } }
    // puis on écarte encore, bord de page compris ; en dernier recours seulement, les deux cœurs rétrécissent ensemble
    for (it = 0; it < 30; it++) { var bouge = false; _vois();
      for (i = 0; i < hs.length; i++) for (var q3 = 0, V3 = VO(i); q3 < V3.length; q3++) { j = V3[q3];
        var a3 = hs[i], b3 = hs[j], dx3 = b3.cx - a3.cx, dy3 = b3.cy - a3.cy, d3 = Math.hypot(dx3, dy3) || 1e-6, need3 = (rad(a3) + rad(b3)) * 1.02 + jeu;
        if (d3 < need3) { bouge = true; var m3 = (need3 - d3) * 0.3; a3.cx -= dx3 / d3 * m3; a3.cy -= dy3 / d3 * m3; b3.cx += dx3 / d3 * m3; b3.cy += dy3 / d3 * m3; borne(a3); borne(b3); } }
      if (!bouge) break; }
    _vois(); for (i = 0; i < hs.length; i++) for (var q4 = 0, V4 = VO(i); q4 < V4.length; q4++) { j = V4[q4];
      var a4 = hs[i], b4 = hs[j], d4 = Math.hypot(a4.cx - b4.cx, a4.cy - b4.cy), need4 = (rad(a4) + rad(b4)) * 1.02 + jeu;
      if (d4 < need4) { var kf = Math.max(0.3, (d4 - jeu) / ((rad(a4) + rad(b4)) * 1.02)); a4.sc *= kf; b4.sc *= kf; } }
  }
  var _locs = {};
  function _loc(h, K) {
    var L = _locs[h.k];
    if (L && L.K === K && Math.abs(h.sref / L.s - 1) < 0.03) return L;
    var o = { k: h.k, P: h.P, cx: 0, cy: 0, sc: h.sref, f: 1 }; _forme(o, K);
    return (_locs[h.k] = { K: K, s: h.sref, pts: o.pts, box: o.box, contour: o.contour, couches: o.couches, emprise: o.emprise });
  }
  function _place(h, K) {
    h.vide = h.f < 0.01 || !(h.sc > 0) || !(h.sref > 0); if (h.vide) return;
    var L = _loc(h, K), r = h.sc / L.s; h.L = L; h.r = r;
    h.pts = L.pts.map(function (v) { return [h.cx + v[0] * r, h.cy + v[1] * r]; });
    h.box = [h.cx + L.box[0] * r, h.cy + L.box[1] * r, h.cx + L.box[2] * r, h.cy + L.box[3] * r];
    h.lw = Math.max(1.2 * K * h.f, (h.box[2] - h.box[0]) * 0.035) * 1.6;
  }
  function _forme(h, K) {
    var P = h.P, N = 120, pts = [], ca = Math.cos(P.tilt), sa = Math.sin(P.tilt), i;
    for (i = 0; i < N; i++) {
      var t = i / N * TAU, st = Math.sin(t);
      var x = 16 * st * st * st * (1 + P.asym * (st > 0 ? 1 : st < 0 ? -1 : 0)), y = -(13 * Math.cos(t) - 5 * P.lobe * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
      if (y > 0) y *= P.tip; else y *= st < 0 ? P.lobeL : P.lobeR;
      var ex = 15 * Math.sin(t), ey = -14 * Math.cos(t); x = x * (1 - P.plump) + ex * P.plump; y = y * (1 - P.plump) + ey * P.plump;
      x *= P.sx / 16; y *= P.sy / 16;
      var wob = 1 + 0.035 * Math.sin(t * 3 + P.q0) + 0.025 * Math.sin(t * 5 + P.q1); x *= wob; y *= wob;
      pts.push([h.cx + (x * ca - y * sa) * h.sc, h.cy + (x * sa + y * ca) * h.sc - h.sc * 0.1]);
    }
    var x0 = 1e18, x1 = -1e18, y0 = 1e18, y1 = -1e18; pts.forEach(function (v) { if (v[0] < x0) x0 = v[0]; if (v[0] > x1) x1 = v[0]; if (v[1] < y0) y0 = v[1]; if (v[1] > y1) y1 = v[1]; });
    h.pts = pts; h.box = [x0, y0, x1, y1];
    var hw = x1 - x0, hh = y1 - y0, cx = (x0 + x1) / 2;
    h.contour = new Path2D(); _poly(h.contour, pts);
    // le remplissage, tiré de la clé (rng(p.h ^ 0x77) dans la planche) — des tracés, gardés avec la géométrie
    var q = _lcg(h.k ^ 0x77), per = hh / (8 + Math.floor(q() * 4)), bow = 0.35 + 0.35 * q();
    h.couches = [];   // [{T, ton}] : ton 0 = la couleur, 1 = sa nuance, 2 = l'encre
    var eb = [x0, y0, x1, y1]; function _e(w) { if (w[0] < eb[0]) eb[0] = w[0]; if (w[0] > eb[2]) eb[2] = w[0]; if (w[1] < eb[1]) eb[1] = w[1]; if (w[1] > eb[3]) eb[3] = w[1]; }
    if (P.mode === 3) {
      // la coulée : de la peinture versée au centre, anneau après anneau, de moins en moins cœur vers l'intérieur
      var hc = [cx + (q() - 0.5) * hw * 0.1, y0 + hh * (0.45 + 0.06 * q())], rings = 3 + Math.floor(q() * 3), off = [0, 1, 3][Math.floor(q() * 3)], n2 = 200;
      var seq = [0, 1, 2, 0, 1];   // la couche du dessus est toujours en couleur, jamais à l'encre
      var rH = new Float64Array(n2), m = pts.length;
      for (i = 0; i < n2; i++) { var a = i / n2 * TAU, ux = Math.cos(a), uy = Math.sin(a), best = 0;
        for (var j = 0; j < m; j++) { var p1 = pts[j], p2 = pts[(j + 1) % m], exx = p2[0] - p1[0], eyy = p2[1] - p1[1], den = ux * eyy - uy * exx; if (Math.abs(den) < 1e-12) continue;
          var tt = ((p1[0] - hc[0]) * eyy - (p1[1] - hc[1]) * exx) / den, uu = ((p1[0] - hc[0]) * uy - (p1[1] - hc[1]) * ux) / den; if (tt > 0 && uu >= 0 && uu <= 1 && tt > best) best = tt; }
        rH[i] = best; }
      var mR = 0; for (i = 0; i < n2; i++) mR += rH[i]; mR /= n2;
      var hp = []; for (var kq = 0; kq < 3; kq++) hp.push([kq + 2, q() * 6.28, (0.035 + 0.03 * q()) / (kq + 1)]);
      var flaque = []; for (i = 0; i < n2; i++) { var a1 = i / n2 * TAU, mm = 1; hp.forEach(function (e) { mm += e[2] * Math.sin(e[0] * a1 + e[1]); }); flaque.push(mR * mm); }
      var mele = function (w) { var bb = [], c2, pass, ii; for (ii = 0; ii < n2; ii++) bb.push(w * rH[ii] + (1 - w) * flaque[ii]);
        for (pass = 0; pass < 3; pass++) { c2 = bb.slice(); for (ii = 0; ii < n2; ii++) bb[ii] = (c2[(ii + n2 - 1) % n2] + 2 * c2[ii] + c2[(ii + 1) % n2]) / 4; } return bb; };
      var T0 = new Path2D(); _poly(T0, pts); h.couches.push({ T: T0, ton: seq[off % 5] });
      for (var L = 1; L < rings; L++) {
        var sc = Math.pow((rings - L) / rings, 1.25), bL = mele(0.72 - 0.45 * L / rings), w1 = q() * 6.28, w2 = q() * 6.28, am = 0.03 + 0.04 * q();
        var p2s = bL.map(function (r, ii) { var aa = ii / n2 * TAU, rr = r * sc * (1 + am * Math.sin(2 * aa + w1) + am * 0.6 * Math.sin(3 * aa + w2)); return [hc[0] + Math.cos(aa) * rr, hc[1] + Math.sin(aa) * rr]; });
        p2s.forEach(_e); var TL = new Path2D(); _traceMil(TL, p2s.filter(function (_, ii) { return ii % 3 === 0; })); h.couches.push({ T: TL, ton: seq[(L + off) % 5] });
      }
    } else {
      // des rayures en chevrons qui épousent la pointe (mode 0), ou en biais (mode 2 : tournées autour du centre)
      var ctr = [(x0 + x1) / 2, (y0 + y1) / 2], rot = P.mode === 2 ? P.ang : 0, cr = Math.cos(rot), sr = Math.sin(rot);
      var R2 = function (X, Y) { if (!rot) return [X, Y]; var dx = X - ctr[0], dy = Y - ctr[1]; return [ctr[0] + dx * cr - dy * sr, ctr[1] + dx * sr + dy * cr]; };
      var bowM = P.mode === 2 ? 0.08 : 1, TS = new Path2D();
      /* ⚑ budget — la planche trace chaque rayure bien au-delà du cœur (0,4 × sa largeur de chaque côté, 0,6 × sa hauteur au-dessus),
         puis la découpe. On ne garde que ce qui peut paraître DANS le cœur (ses bornes dans le repère des rayures) : même phase,
         mêmes tirages, mêmes points sur la même grille — la même image, moitié moins à remplir. */
      var gx0 = 1e18, gx1 = -1e18, gy0 = 1e18, gy1 = -1e18;
      pts.forEach(function (w) { var dx = w[0] - ctr[0], dy = w[1] - ctr[1], X2 = ctr[0] + dx * cr + dy * sr, Y2 = ctr[1] - dx * sr + dy * cr;
        if (X2 < gx0) gx0 = X2; if (X2 > gx1) gx1 = X2; if (Y2 < gy0) gy0 = Y2; if (Y2 > gy1) gy1 = Y2; });
      for (var v = y0 - hh * 0.6; v < y1 + per; v += per) {
        var f1 = _feutre(q, hw, K), f2 = _feutre(q, hw, K), th = per * (0.48 + 0.1 * q()), bw = bow * bowM, xa = x0 - hw * 0.4, xb = x1 + hw * 0.4, st2 = hw / 40, X, pA = [], pB = [];
        var yA = function (xx) { return v + bw * hw * 0.5 - bw * Math.sqrt((xx - cx) * (xx - cx) + (hw * 0.08) * (hw * 0.08)) + f1(xx) * 0.5; };
        var yB = function (xx) { return v + th + bw * hw * 0.5 - bw * Math.sqrt((xx - cx) * (xx - cx) + (hw * 0.08) * (hw * 0.08)) + f2(xx) * 0.5; };
        var xs = [], ymin = 1e18, ymax = -1e18;
        for (X = xa; X <= xb; X += st2) if (X >= gx0 - 2 * st2 && X <= gx1 + 2 * st2) xs.push(X);
        if (xs.length < 2) continue;
        for (var ix = 0; ix < xs.length; ix++) { var ya = yA(xs[ix]), yb = yB(xs[ix]); if (ya < ymin) ymin = ya; if (yb > ymax) ymax = yb; }
        if (ymax < gy0 - 1 || ymin > gy1 + 1) continue;
        for (ix = 0; ix < xs.length; ix++) pA.push(R2(xs[ix], yA(xs[ix])));
        for (ix = xs.length - 1; ix >= 0; ix--) pB.push(R2(xs[ix], yB(xs[ix])));
        pA.forEach(_e); pB.forEach(_e); _traceMil(TS, _clairseme(pA).concat(_clairseme(pB)));
      }
      h.couches.push({ T: TS, ton: 0 });
    }
    h.emprise = eb;
  }

  function _peindreCoeur(h, now, seule) {
    var col = cOf(h.s, now), tons = [col, _nuance(col), _encre()], L = h.L, r = h.r;
    g.save(); g.translate(h.cx, h.cy); g.scale(r, r); g.clip(L.contour);
    if (seule && typeof env.fondToile === 'function') { g.fillStyle = _rgb(_arr(env.fondToile())); g.fill(L.contour); }   // la dalle seule porte son papier
    for (var i = 0; i < L.couches.length; i++) { g.fillStyle = _rgb(tons[L.couches[i].ton]); g.fill(L.couches[i].T); }
    g.restore();
    g.save(); g.translate(h.cx, h.cy); g.scale(r, r);   // le trait qui cerne, au feutre
    g.strokeStyle = _rgb(tons[2]); g.lineWidth = h.lw / r; g.lineJoin = 'round'; g.stroke(L.contour); g.restore();
  }

  var _CR = window._calqueRepos ? window._calqueRepos() : null;
  function Rcha(now, x0, y0, x1, y1) {
    _sync();
    var G = _coeurs(now), Pg = _page(G.K), i, D = G.D;
    if (env.vive && !env.trans && _CR) {   // v72 : au repos, le calque (signature : les cœurs posés, leurs couleurs, l'encre)
      var sg = [Math.round(W), Math.round(H), Math.round(G.K * 4096), _rgb(_encre())];
      for (i = 0; i < D.length; i++) { var h0 = D[i]; sg.push(h0.vide ? 'v' : h0.k + ':' + Math.round(h0.cx * 64) + ':' + Math.round(h0.cy * 64) + ':' + Math.round(h0.sc * 256) + ':' + _rgb(cOf(h0.s, now))); }
      if (_CR.pose(g, sg.join('|'), function (C) { var g0 = g; g = C; try { _peintCha(G, Pg, D, now); } finally { g = g0; } })) { _dernier = G; window._chaComp = { coeurs: D.length, u: G.u, centres: D.map(function (p) { return [p.k, +(p.cx || 0).toFixed(1), +(p.cy || 0).toFixed(1), +(p.sc || 0).toFixed(2)]; }) }; return; }
    }
    _peintCha(G, Pg, D, now);
  }
  /* ⚑ v72 (budget) — SUR LA TOILE VIVANTE, LA PAGE SANS DÉCOUPAGE. Le découpage pair-impair de toute la page autour des cœurs
     coûtait la rastérisation d'un masque à chaque image (Chamade à 40 paroles : 26 ms). La page se peint d'un bloc — en calque dès
     que la vue est posée, elle ne bouge pas pendant une plantation —, puis le PAPIER du moteur (le fond même, `env.papier`) sous
     chaque cœur. Au bord d'un cœur, le mélange est le même : bande × (1 − c) + fond × c, où c est la couverture du cœur. Le trait
     du cœur passe ensuite dessus, comme avant. Ailleurs (dalle seule, export, aperçus) : le découpage d'origine. */
  var _CRp = window._calqueRepos ? window._calqueRepos() : null;
  function _peintCha(G, Pg, D, now) { var i;
    if (env.vive && typeof env.papier === 'function' && _CRp && !window._perfAncien && !window._v72SansCalque) {
      var ink = _rgb(_encre()), pap = env.papier(), Zc = new Path2D(), nz = 0;
      if (!_CRp.pose(g, 'page|' + Math.round(W) + 'x' + Math.round(H) + '|' + Math.round(G.K * 4096) + '|' + env.cleToile + '|' + ink, function (C) { C.fillStyle = ink; C.fill(Pg.T); })) { g.fillStyle = ink; g.fill(Pg.T); }
      for (i = 0; i < D.length; i++) if (!D[i].vide) { _poly(Zc, D[i].pts); nz++; }
      if (nz && pap) { g.fillStyle = pap; g.fill(Zc); }
      for (i = 0; i < D.length; i++) if (!D[i].vide) _peindreCoeur(D[i], now, false);   /* v74 : un calque par cœur a été essayé (Q341) — 73 % des cœurs changent de taille pendant une plantation, gain nul : retiré */
      _dernier = G; window._chaComp = { coeurs: D.length, u: G.u, centres: D.map(function (p) { return [p.k, +(p.cx || 0).toFixed(1), +(p.cy || 0).toFixed(1), +(p.sc || 0).toFixed(2)]; }) };
      return;
    }
    // la page : ses bandes d'encre, HORS des cœurs (un seul découpage pair-impair) — elles viennent toucher le trait
    g.save();
    var Z = new Path2D(), m = 10 * G.K; Z.rect(-m - W, -m - H, 3 * W + 2 * m, 3 * H + 2 * m);
    for (i = 0; i < D.length; i++) if (!D[i].vide) _poly(Z, D[i].pts);
    g.clip(Z, 'evenodd');
    g.fillStyle = _rgb(_encre()); g.fill(Pg.T);
    g.restore();
    for (i = 0; i < D.length; i++) if (!D[i].vide) _peindreCoeur(D[i], now, false);
    _dernier = G; window._chaComp = { coeurs: D.length, u: G.u, centres: D.map(function (p) { return [p.k, +(p.cx || 0).toFixed(1), +(p.cy || 0).toFixed(1), +(p.sc || 0).toFixed(2)]; }) };
  }

  var _dernier = null;   // la géométrie de la dernière image peinte : l'ancre des titres et le toucher la lisent, sans refaire les cœurs
  function _trouve(s, now, G) { G = G || _coeurs(now || performance.now()); var k = _cle(s), i;
    for (i = 0; i < G.D.length; i++) if (G.D[i].s === s) return G.D[i];
    for (i = 0; i < G.D.length; i++) if (G.D[i].k === k) return G.D[i];
    return null; }
  function _bb(h) { var e = h.lw / 2 + 0.5; return [h.box[0] - e, h.box[1] - e, h.box[2] + e, h.box[3] + e]; }
  function seule(nom, s, now, cx, cy, taille) {
    _sync(); var h = _trouve(s, now); if (!h || h.vide) return false;
    var B = _bb(h), sc = taille / Math.max(B[2] - B[0], B[3] - B[1], 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(B[0] + B[2]) / 2, -(B[1] + B[3]) / 2);
    _peindreCoeur(h, now, true); g.restore();
    return true;
  }
  function contour(nom, s) { _sync(); var h = _trouve(s); return h && !h.vide ? h.pts.slice() : null; }
  function nature(nom, s) { _sync(); var h = _trouve(s); return h && !h.vide ? 'dalle' : null; }
  function boite(nom, s) { _sync(); var h = _trouve(s); if (!h || h.vide) return null; var B = _bb(h);
    return { x0: B[0], y0: B[1], x1: B[2], y1: B[3], fx0: B[0], fy0: B[1], fx1: B[2], fy1: B[3] }; }
  // le toucher : dans le cœur peint (trait compris), jamais dans les bandes de la page
  function toucher(nom, x, y) {
    _sync(); var G = _dernier || _coeurs(performance.now());
    for (var i = G.D.length - 1; i >= 0; i--) { var h = G.D[i]; if (h.vide || h.s.part != null) continue;
      var B = _bb(h); if (x < B[0] || x > B[2] || y < B[1] || y > B[3]) continue;
      if (_pip(x, y, h.pts)) return h.s; }
    return null;
  }

  // v63 : où le cœur est PEINT (centre de sa boîte) et sa largeur — le moteur y pose le titre
  Rcha.ancre = function (s) { _sync(); var h = _trouve(s, 0, _dernier); if (!h || h.vide) return null; return [(h.box[0] + h.box[2]) / 2, (h.box[1] + h.box[3]) / 2, h.box[2] - h.box[0]]; };
  Rcha.transDur = 1600; Rcha.douce = true; Rcha.partDur = 900; Rcha.toucheStrict = true;
  return { chamade: Rcha, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerChamade = creerChamade;
})();

/* ══════════════════ bloc « lot-V64-VOLUBILIS » ══════════════════ */
/* ⚑ v64 (27 sept. 2026) — VOLUBILIS, le jardin découpé. Porté de `volBuild`, `volFeuilles`, `volTan`, `volR`, `volFleurPts` et
   `jardin` (planche « Trois matières ») au CONTRAT-MONDE, sur le patron de Brouillamini et de Chamade (§15.13, §15.14) :
   · le CODE de la planche est gardé tel quel (méthodes devenues fonctions) ; seules changent ses unités et ses sources :
     toute longueur `W × …` / `H × …` devient l'unité de matière (L3 = 300·K, LH = 650·K, K = uMat / 53,55) — le jardin ne
     dézoome pas ; les POSITIONS (le cadre W − M, H − M, le bas de la page H + step) restent celles de la Toile ;
   · LCG sur la clé stable (fleur), sur la clé de la Toile (jardin) ; la grille d'occupation, lue seulement par l'ancienne
     méthode « gardée en secours » (morte), est retirée — même dessin ;
   · la fleur (la dalle) est cOf ; les feuilles, les tiges, les fleurs d'encre sont l'encre du produit (`_tfInk`, Q331) ;
     le cœur d'une fleur est découpé (pair-impair : on y voit le fond) — et dans la dalle seule, il est en PAPIER (`fondToile`, décision Tom) ;
   · la construction est globale (un jardin entier) : pendant une transition, deux jardins — celui qu'on voyait, celui d'arrivée
     sur `env.finale` —, les fleurs glissent de l'un à l'autre (centre et contour), le feuillage passe de l'un à l'autre en fondu ;
     au repos le jardin d'arrivée RESTE (§15.14). ⚠ Construire un jardin coûte (planche : 500–900 ms) : c'est au tableau du budget.
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerVolubilis(env) {
  var g, W, H, seeds, L3 = 300, LH = 650, _vd = { clip: 0, area: 0, inr: 0 };
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; }
  var TAU = 6.283185307179586, UPL = 53.55, ARR = 900, RET = 760, MOVE = 1200;
  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) return k >>> 0; }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  function _arr(c) { if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; } return c; }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _encre() { return _arr(typeof env.encre === 'function' ? env.encre() : env.encre); }
  function _clipH(poly, mx, my, nx, ny) {
    var out = [];
    for (var i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      var A = poly[j], B = poly[i], da = (A[0] - mx) * nx + (A[1] - my) * ny, db = (B[0] - mx) * nx + (B[1] - my) * ny;
      if (db <= 0) { if (da > 0) { var t = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]); } out.push(B); }
      else if (da <= 0) { var t2 = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t2, A[1] + (B[1] - A[1]) * t2]); }
    }
    return out;
  }
  function _trace(T, pts) {
    var n = pts.length, a = pts[n - 1], b = pts[0];
    T.moveTo((a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
    for (var i = 0; i < n; i++) { var p = pts[i], q2 = pts[(i + 1) % n]; T.quadraticCurveTo(p[0], p[1], (p[0] + q2[0]) / 2, (p[1] + q2[1]) / 2); }
    T.closePath();
  }
  function _pip(x, y, pts) { var ins = false, n = pts.length;
    for (var i = 0, j = n - 1; i < n; j = i++) { var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins; }
    return ins; }

  /* ================= le code de la planche (Promi - Trois matières), aux unités près ================= */
  function _volFleurPts(cx, cy, R, q) {
    // la fleur de la référence : une masse molle et large, 4 à 6 pétales de tailles très inégales,
    // des échancrures nettes mais arrondies, et une silhouette d'ensemble irrégulière (plus large que haute, penchée)
    const P = 4 + Math.floor(q() * 3), n = 120, rot = q() * 6.283, amp = [], wd = [];
    for (let k = 0; k < P; k++) { amp.push(0.72 + 0.4 * q()); wd.push(0.6 + 0.8 * q()); }
    const tot = wd.reduce((a, b) => a + b, 0), cum = [0]; wd.forEach(w => cum.push(cum[cum.length - 1] + w / tot));
    const sq = 0.8 + 0.18 * q(), sa = q() * 3.1416, h2 = [q() * 6.283, 0.07 + 0.06 * q()], h3 = [q() * 6.283, 0.04 + 0.04 * q()], pts = [];
    for (let i = 0; i < n; i++) {
      const th = i / n * 6.2832, f = (((th - rot) / 6.2832) % 1 + 1) % 1;
      let k = 0; while (k < P - 1 && f > cum[k + 1]) k++;
      const fr = (f - cum[k]) / (cum[k + 1] - cum[k]), bump = Math.pow(Math.sin(Math.PI * fr), 0.42);
      const r = R * (0.68 + 0.32 * amp[k] * bump) * (1 + h2[1] * Math.sin(2 * th + h2[0]) + h3[1] * Math.sin(3 * th + h3[0]));
      let x = Math.cos(th) * r, y = Math.sin(th) * r;
      const ca = Math.cos(sa), sn = Math.sin(sa), u1 = x * ca + y * sn, v1 = -x * sn + y * ca, u2 = u1 * sq;
      pts.push([cx + u2 * ca - v1 * sn, cy + u2 * sn + v1 * ca]);
    }
    return pts;
  }
  function _volBuild(S) {
    const R = _lcg((S.g ^ 0x7011) >>> 0), M = 0, gut = L3 * 0.012, sw = L3 * 0.011;   // v85 (Tom) : « son jardin doit couvrir tout l'écran, plus de marge de fond nu » — le cadre (L3 × 0,055) retiré
    const X0 = M, X1 = W - M, Y0 = M, Y1 = H - M, OUT = L3 * 0.04;
    // (la grille d'occupation de la planche n'était LUE que par l'ancienne méthode, morte : retirée — même dessin)
    let occ = null, occS = null, occB = null; const markPoly = function () {}, markDisc = function () {};
    // 1 · les fleurs, une par promesse, à sa place — leur taille se partage avec les voisines
    const fl = S.pr.map(p => ({ p, x: p.x, y: p.y }));
    // les fleurs s'écartent un peu avant d'être dimensionnées, pour rester grandes comme dans la référence
    for (let it = 0; it < 30; it++) fl.forEach(f1 => { fl.forEach(o => { if (o === f1) return; const dx = f1.x - o.x, dy = f1.y - o.y, d = Math.hypot(dx, dy) || 1, want = Math.min(L3 * 0.3, Math.sqrt((X1 - X0) * (Y1 - Y0) / Math.max(1, fl.length)) * 0.9); if (d < want) { const k = (want - d) / d * 0.25; f1.x += dx * k; f1.y += dy * k; } }); f1.x = Math.min(X1 - L3 * 0.12, Math.max(X0 + L3 * 0.12, f1.x)); f1.y = Math.min(Y1 - L3 * 0.12, Math.max(Y0 + L3 * 0.12, f1.y)); });
    // comme dans la référence, les fleurs couronnent le haut : la plus haute vient toujours près du bord supérieur
    if (fl.length) {
      const ys = fl.map(f1 => f1.y), y0 = Math.min(...ys), y1 = Math.max(...ys), top = Y0 + L3 * 0.09;
      fl.forEach(f1 => { f1.y = y1 > y0 + L3 / 300 ? top + (f1.y - y0) * (y1 - top) / (y1 - y0) : top; });
      // les deux coins du haut sont toujours tenus par une fleur (comme dans la référence) : la plus proche vient s'y loger
      const used = new Set();
      // toute la bande du haut est tenue : les deux coins, et le centre dès qu'il y a assez de fleurs
      const slots = [[X0 + L3 * 0.15, Y0 + L3 * 0.13], [X1 - L3 * 0.15, Y0 + L3 * 0.13]];
      if (fl.length >= 5) slots.push([(X0 + X1) / 2, Y0 + L3 * 0.13]);
      for (const [tx, ty] of slots) {
        let bf = null, bd = 1e9; fl.forEach(f1 => { if (used.has(f1)) return; const d = Math.hypot(f1.x - tx, f1.y - ty); if (d < bd) { bd = d; bf = f1; } });
        if (!bf) continue; used.add(bf);
        if (Math.hypot(bf.x - tx, bf.y - ty) > L3 * 0.05) { bf.x += (tx - bf.x) * 0.85; bf.y += (ty - bf.y) * 0.85; }
      }
    }
    fl.forEach(f => {
      let dn = 1e9; fl.forEach(o => { if (o !== f) dn = Math.min(dn, Math.hypot(o.x - f.x, o.y - f.y)); });
      const q = _lcg(f.p.h ^ 0xf1a);
      // la fleur garde la place du feuillage : sa taille suit la densité de la Toile
      const cellF = Math.sqrt((X1 - X0) * (Y1 - Y0) / Math.max(1, fl.length));
      f.R = Math.max(Math.min(L3 * 0.1, cellF * 0.24), Math.min(fl.length <= 6 ? L3 * 0.27 : L3 * 0.2, cellF * 0.36, (Math.max(dn, L3 * 0.36) * 0.5 - gut) / 1.12)) * (0.92 + 0.16 * q()) * window._tailleApercu(f.p.s);
      // tenue dans le cadre : la fleur vient vers l'intérieur plutôt que de rétrécir
      // les fleurs viennent contre le cadre et s'y aplatissent (comme dans la référence) : pas de poche entre elles et le bord
      const mg = f.R * 0.8 + gut;
      f.x = Math.min(X1 - mg, Math.max(X0 + mg, f.x)); f.y = Math.min(Y1 - mg, Math.max(Y0 + mg, f.y));
      f.R = Math.min(f.R, (Math.min(f.x - X0, X1 - f.x, f.y - Y0, Y1 - f.y) - gut) / 0.8);
      f.pts = _volFleurPts(f.x, f.y, f.R, q);
      const nP = 3 + Math.floor(q() * 5), dots = [], cx = f.x + (q() - 0.5) * f.R * 0.3, cy = f.y + (q() - 0.5) * f.R * 0.25, dr = f.R * 0.2, rr = f.R * 0.06;
      for (let t = 0; t < 80 && dots.length < nP; t++) {
        const a = q() * 6.283, d = dr * Math.sqrt(q()), x = cx + Math.cos(a) * d, y = cy + Math.sin(a) * d * 0.85, r = rr * (0.65 + 0.7 * q());
        if (dots.every(o => Math.hypot(o[0] - x, o[1] - y) > (o[2] + r) * 1.35)) dots.push([x, y, r, 0.85 + 0.3 * q(), q() * 3]);
      }
      f.dots = dots;
      markPoly(f.pts, gut);
    });
    // 1b · la vraie forme des fleurs : chacune prend sa place entre ses voisines et le cadre (comme dans la référence,
    //      elles s'aplatissent contre les bords), contour lissé, puis découpé en pétales par des échancrures inégales
    fl.forEach(f => {
      const q = _lcg(f.p.h ^ 0xfa11), NS = 96, e1 = 0.9 + 0.2 * q(), ea = q() * 3.1416;
      let poly = [];
      // gabarit libre, jamais un cercle : une masse irrégulière (2, 3 et 5 lobes lents), que les voisines et le cadre viennent aplatir
      const a2 = q() * 6.28, a3 = q() * 6.28, a5 = q() * 6.28, k2 = 0.14 + 0.1 * q(), k3 = 0.08 + 0.08 * q(), k5 = 0.03 + 0.04 * q();
      for (let k = 0; k < 40; k++) { const th = k / 40 * 6.2832, rr = f.R * ((fl.length <= 6 ? 1.6 : fl.length <= 14 ? 1.36 : 1.18) + k2 * Math.sin(2 * th + a2) + k3 * Math.sin(3 * th + a3) + k5 * Math.sin(5 * th + a5)), ux = Math.cos(th) * rr * Math.min(1, e1), uy = Math.sin(th) * rr * Math.min(1, 1 / e1); poly.push([f.x + ux * Math.cos(ea) - uy * Math.sin(ea), f.y + ux * Math.sin(ea) + uy * Math.cos(ea)]); }
      for (const o of fl) { if (o === f) continue; const dx = o.x - f.x, dy = o.y - f.y, d2 = dx * dx + dy * dy, d = Math.sqrt(d2); if (d > (f.R + o.R) * 1.4) continue; const t = Math.min(0.8, Math.max(0.2, 0.5 + (f.R * f.R - o.R * o.R) / (2 * d2))) - gut * 1.5 / d; poly = _clipH(poly, f.x + dx * t, f.y + dy * t, dx, dy); if (poly.length < 3) break; }
      if (poly.length >= 3) { poly = _clipH(poly, X0 + gut, 0, -1, 0); poly = _clipH(poly, X1 - gut, 0, 1, 0); poly = _clipH(poly, 0, Y0 + gut, 0, -1); poly = _clipH(poly, 0, Y1 - gut, 0, 1); }
      if (poly.length < 3) return;
      const rc = new Float64Array(NS);
      for (let a = 0; a < NS; a++) {
        const th = a / NS * 6.2832, cx = Math.cos(th), sy = Math.sin(th); let best = 1e9;
        for (let i = 0; i < poly.length; i++) { const p1 = poly[i], p2 = poly[(i + 1) % poly.length], ex = p2[0] - p1[0], ey = p2[1] - p1[1], den = cx * ey - sy * ex; if (Math.abs(den) < 1e-12) continue; const t = ((p1[0] - f.x) * ey - (p1[1] - f.y) * ex) / den, uu = ((p1[0] - f.x) * sy - (p1[1] - f.y) * cx) / den; if (t > 0 && uu >= 0 && uu <= 1 && t < best) best = t; }
        rc[a] = best < 1e9 ? best : f.R;
      }
      // lissage circulaire (et non une série tronquée, qui fait onduler les côtés plats)
      let lp = Float64Array.from(rc);
      for (let pass = 0; pass < 10; pass++) { const nx = new Float64Array(NS); for (let a = 0; a < NS; a++) nx[a] = (lp[(a - 2 + NS) % NS] + 2 * lp[(a - 1 + NS) % NS] + 3 * lp[a] + 2 * lp[(a + 1) % NS] + lp[(a + 2) % NS]) / 9; lp = nx; }
      let kmin = 1; for (let a = 0; a < NS; a++) kmin = Math.min(kmin, rc[a] * 0.985 / Math.max(lp[a], 1e-3));
      // les pétales : 4 à 6 échancrures, chacune à sa profondeur et sa largeur ; les pétales ont des tailles inégales
      const nP = 4 + Math.floor(q() * 3), rot = q() * 6.2832, notch = [];
      let acc = 0; const ws = []; for (let k = 0; k < nP; k++) { const w = 0.6 + 0.8 * q(); ws.push(w); acc += w; }
      // comme dans la référence : peu d'échancrures, mais franches et étroites ; entre elles les pétales se bombent
      let cum = 0; for (let k = 0; k < nP; k++) { cum += ws[k] / acc; notch.push([rot + cum * 6.2832, 0.14 + 0.1 * q(), 0.14 + 0.1 * q()]); }
      // la fleur de la référence : une union de pétales ronds de tailles inégales, groupés autour du cœur —
      // les pincements naissent là où deux pétales se rejoignent ; puis elle s'aplatit doucement contre sa place
      // cœur petit, pétales écartés : là où deux pétales se rejoignent, le pincement se lit nettement
      // un pétale pointe toujours vers la plus grande place libre au-dessus de la fleur (vers le cadre, où aucune tige ne monte)
      let rotU = rot, bestUp = 0; for (let a = 0; a < NS; a++) { const th = a / NS * 6.2832; if (Math.sin(th) < -0.2 && rc[a] > bestUp) { bestUp = rc[a]; rotU = th; } }
      const UP = [[0, 0, f.R * (0.34 + 0.06 * q())]];
      for (let k = 0; k < nP; k++) { const an = rotU + (k + (k ? (q() - 0.5) * 0.3 : 0)) / nP * 6.2832, dd = f.R * (0.55 + 0.07 * q()), rk = f.R * (0.36 + 0.1 * q()); UP.push([Math.cos(an) * dd, Math.sin(an) * dd, rk]); }
      const U = new Float64Array(NS);
      for (let a = 0; a < NS; a++) {
        const th = a / NS * 6.2832, ux = Math.cos(th), uy = Math.sin(th); let best = 0;
        for (const [cx, cy, r0] of UP) { const pr = ux * cx + uy * cy, disc = r0 * r0 - (cx * cx + cy * cy) + pr * pr; if (disc >= 0) best = Math.max(best, pr + Math.sqrt(disc)); }
        U[a] = best;
      }
      let mU = 0, mC = 0; for (let a = 0; a < NS; a++) { mU += U[a]; mC += rc[a]; }
      // les pétales tiennent presque entiers dans la place (quantile bas du rapport place/pétales), et l'aplatissement ne fait que les effleurer
      const ratios = []; for (let a = 0; a < NS; a++) ratios.push(rc[a] / Math.max(1e-6, U[a])); ratios.sort((x, y) => x - y);
      const sU = ratios[Math.floor(NS * 0.25)] * 0.97, kS = f.R * 0.08;
      const smin = (a1, b1) => -kS * Math.log(Math.exp(-a1 / kS) + Math.exp(-b1 / kS));
      // là où la place s'étend loin au-delà des pétales, un pétale de plus y pousse : la fleur remplit sa place en restant une grappe de pétales
      const U2 = new Float64Array(NS); for (let a = 0; a < NS; a++) U2[a] = U[a] * sU;
      for (let rep = 0; rep < 3; rep++) {
        // le pétale de plus pousse vers le haut ou les côtés — et vers le haut (le cadre, où aucune tige ne monte) dès qu'il y a un peu de place
        // jamais entre deux pétales (ça comblerait le pincement) : seulement dans l'axe d'un pétale existant
        const onAxis = th => UP.slice(1).some(([cx, cy]) => { let d = th - Math.atan2(cy, cx); while (d > Math.PI) d -= 6.2832; while (d < -Math.PI) d += 6.2832; return Math.abs(d) < (fl.length > 12 ? 0.42 : 0.25); });
        // quand les fleurs sont nombreuses, le pétale de plus peut aussi pousser vers le bas et les côtés (contre le cadre)
        let ba = -1, bv = 0; for (let a = 0; a < NS; a++) { const th = a / NS * 6.2832, sn = Math.sin(th); if ((sn > 0.55 && fl.length <= 12) || !onAxis(th)) continue; const v = rc[a] / Math.max(1e-6, U2[a]), thr = sn < -0.3 ? 1.12 : (fl.length > 12 ? 1.12 : 1.3); if (v > thr && v - thr > bv) { bv = v - thr; ba = a; } }
        if (ba < 0) break;
        // un pétale de plus reste un pétale : rond, de taille mesurée, et jamais collé au bord de la place
        const th = ba / NS * 6.2832, inner = U2[ba] * 0.6, outer = Math.min(rc[ba] - f.R * 0.12, U2[ba] * 1.3), rp = Math.min(f.R * 0.45, Math.max(0, (outer - inner) / 2 * 1.1)), dc = outer - rp;
        if (rp < f.R * 0.15) break;
        const cx = Math.cos(th) * dc, cy = Math.sin(th) * dc;
        for (let a = 0; a < NS; a++) { const t2 = a / NS * 6.2832, ux = Math.cos(t2), uy = Math.sin(t2), pr = ux * cx + uy * cy, disc = rp * rp - (cx * cx + cy * cy) + pr * pr; if (disc >= 0) U2[a] = Math.max(U2[a], pr + Math.sqrt(disc)); }
      }
      const pts = []; f.rad = new Float64Array(NS);
      for (let a = 0; a < NS; a++) {
        // comme la référence : chaque pétale est un lobe bien rond, et deux pétales se rejoignent par un pincement court
        const th = a / NS * 6.2832, rel = (((th - rot) / 6.2832) % 1 + 1) % 1;
        let k = 0; while (k < nP - 1 && rel >= (notch[k][0] - rot) / 6.2832) k++;
        const c0 = k ? (notch[k - 1][0] - rot) / 6.2832 : 0, c1 = (notch[k][0] - rot) / 6.2832, fr = Math.min(1, Math.max(0, (rel - c0) / Math.max(1e-6, c1 - c0)));
        // chaque pétale penche un peu d'un côté (lobe asymétrique), a sa propre ampleur, et le pincement est court et en V doux
        const hk = ((k * 7919 + f.p.h) % 997) / 997, sk = 0.75 + 0.5 * hk, frs = Math.pow(fr, sk);
        const dL = notch[k ? k - 1 : nP - 1][1], dR = notch[k][1], dp = (frs < 0.5 ? dL : dR) * 1.05, pa = 0.9 + 0.1 * ((k * 104729 + f.p.h) % 89) / 89;
        const m = pa * (1 - dp * (1 - Math.pow(Math.sin(Math.PI * frs), 0.3)));
        const r = Math.min(smin(U2[a], rc[a] * 0.97), rc[a] * 0.97); f.rad[a] = r;
        pts.push([f.x + Math.cos(th) * r, f.y + Math.sin(th) * r]);
      }
      f.pts = pts; f.Rhit = Math.max(...f.rad);
    });
    // 2 · les tiges : de longues S qui descendent de chaque fleur ; les plus hautes se greffent sur celles d'en dessous
    const stems = [], step = L3 * 0.012;
    for (const f of fl.slice().sort((a, b) => b.y - a.y)) {
      const q = _lcg(f.p.h ^ 0x57e), ph = q() * 6.283, lam = LH * (0.35 + 0.25 * q()), A = 0.35 + 0.2 * q();
      let x = f.x + (q() - 0.5) * f.R * 0.3, y = f.y + f.R * 0.6, hd = Math.PI / 2 + (q() - 0.5) * 0.4, joinedF = false;
      const pts = [[f.x, f.y], [x, y]];
      for (let k = 0; k < 500; k++) {
        let want = Math.PI / 2 + A * Math.sin(y / lam * 6.2832 + ph);
        for (const o of fl) {
          if (o === f) continue;
          const dx = x - o.x, dy = y - o.y, d = Math.hypot(dx, dy), lim = o.R + gut * 2 + sw;
          if (d < lim * 1.5) { const away = Math.atan2(dy, dx); want += (d < lim * 1.1 ? 1.3 : 0.5) * Math.sin(away - want); }
        }
        let bd = 1e9, bp = null;
        if (k > 3) for (const s of stems) for (const v of s.pts) { if (v[1] < y) continue; const d = Math.hypot(v[0] - x, v[1] - y); if (d < bd) { bd = d; bp = v; } }
        if (bp && bd < L3 * 0.2) { const to = Math.atan2(bp[1] - y, bp[0] - x); want += 0.35 * Math.sin(to - want); }
        if (x < X0 + L3 * 0.1) want = Math.min(want, Math.PI / 2 - 0.6);
        if (x > X1 - L3 * 0.1) want = Math.max(want, Math.PI / 2 + 0.6);
        want = Math.max(0.35, Math.min(Math.PI - 0.35, want));
        hd += Math.max(-0.12, Math.min(0.12, want - hd));
        if (bp && bd < step * 1.5) { pts.push(bp.slice()); joinedF = true; break; }
        // contrainte dure : la tige ne touche jamais une autre fleur — elle vire jusqu'à trouver le passage
        const clear = (h) => { const nx = x + Math.cos(h) * step, ny = y + Math.sin(h) * step; for (const o of fl) { if (o === f) continue; if (Math.hypot(nx - o.x, ny - o.y) < _volR(o, nx, ny) + gut + sw) return false; } return true; };
        if (!clear(hd)) { let ok = false; for (let da = 0.15; da < 1.6 && !ok; da += 0.15) for (const sg of [1, -1]) if (clear(hd + sg * da)) { hd += sg * da; ok = true; break; } if (!ok) break; }
        // près du cadre, la tige tourne vers l'intérieur au lieu de le longer
        const nx0 = x + Math.cos(hd) * step;
        if (nx0 < X0 + sw + gut * 2) hd = Math.min(hd, 0.9);
        if (nx0 > X1 - sw - gut * 2) hd = Math.max(hd, Math.PI - 0.9);
        const ox = x, oy = y;
        x += Math.cos(hd) * step; y += Math.sin(hd) * step;
        // jamais de croisement : si le pas coupe une tige déjà tracée, la tige s'y greffe au point exact de rencontre
        let cut = null;
        if (pts.length > 3) for (const s2 of stems) { const Q = s2.pts; for (let j = 0; j < Q.length - 1 && !cut; j++) { const b0 = Q[j], b1 = Q[j + 1], d1x = x - ox, d1y = y - oy, d2x = b1[0] - b0[0], d2y = b1[1] - b0[1], den = d1x * d2y - d1y * d2x; if (Math.abs(den) < 1e-9) continue; const t1 = ((b0[0] - ox) * d2y - (b0[1] - oy) * d2x) / den, t2 = ((b0[0] - ox) * d1y - (b0[1] - oy) * d1x) / den; if (t1 >= 0 && t1 <= 1 && t2 >= 0 && t2 <= 1) cut = Q[t2 < 0.5 ? j : j + 1]; } if (cut) break; }
        if (cut) { pts.push(cut); joinedF = true; break; }
        pts.push([x, y]);
        if (y > H + step) break;
      }
      stems.push({ pts, f, dead: !joinedF && y <= H });
      occ = occS; for (let i = 2; i < pts.length; i++) markDisc(pts[i][0], pts[i][1], sw * 0.55 + gut); occ = occB;
    }
    // quand un grand vide reste (Toile peu remplie), une branche feuillue monte du bas pour le peupler
    const tried = [];
    for (let rep = 0; rep < 10; rep++) {
      let best = null, bdv = 0;
      for (let gy = 0; gy < 24; gy++) for (let gx = 0; gx < 12; gx++) {
        const px = X0 + (gx + 0.5) / 12 * (X1 - X0), py = Y0 + (gy + 0.5) / 24 * (Y1 - Y0);
        if (tried.some(t => Math.hypot(t[0] - px, t[1] - py) < L3 * 0.15)) continue;
        let d = 1e9; for (const o of fl) d = Math.min(d, Math.hypot(px - o.x, py - o.y) - o.R);
        for (const s of stems) for (let i = 0; i < s.pts.length; i += 2) d = Math.min(d, Math.hypot(px - s.pts[i][0], py - s.pts[i][1]));
        if (d > bdv) { bdv = d; best = [px, py]; }
      }
      if (!best || bdv < L3 * 0.1) break;
      const clearF = (qx, qy) => fl.every(o => Math.hypot(qx - o.x, qy - o.y) > _volR(o, qx, qy) + gut + sw);
      tried.push(best);
      // la branche se greffe sur la tige la plus proche (ou naît au bas si aucune n'est à portée) et pousse vers le vide
      let gp = null, gd = 1e9;
      for (const s of stems) for (let i = 2; i < s.pts.length; i++) { const v = s.pts[i], d = Math.hypot(v[0] - best[0], v[1] - best[1]); if (d < gd && d > L3 * 0.12) { gd = d; gp = v; } }
      let x, y, hd;
      if (gp && gd < L3 * 0.9) { x = gp[0]; y = gp[1]; hd = Math.atan2(best[1] - y, best[0] - x); }
      else { x = Math.min(X1 - L3 * 0.1, Math.max(X0 + L3 * 0.1, best[0])); y = H + step; hd = -Math.PI / 2; }
      const pts = [[x, y]], ph = R() * 6.283, lam = LH * (0.3 + 0.2 * R()), A = 0.2 + 0.12 * R(); let okB = false;
      for (let k = 0; k < 400; k++) {
        const tx = best[0] - x, ty = best[1] - y;
        if (Math.hypot(tx, ty) < L3 * 0.05 || y < Y0 + L3 * 0.06) { okB = true; break; }
        let want = Math.atan2(ty, tx) + A * Math.sin(y / lam * 6.2832 + ph);
        for (const s of stems) for (let i = 0; i < s.pts.length; i += 3) { const dx = x - s.pts[i][0], dy = y - s.pts[i][1], d = Math.hypot(dx, dy); if (d < L3 * 0.07) { want += 0.6 * Math.sin(Math.atan2(dy, dx) - want) * (1 - d / (L3 * 0.07)); } }
        const blocked = h => !clearF(x + Math.cos(h) * step * 2, y + Math.sin(h) * step * 2);
        if (blocked(want)) { let fnd = false; for (let da = 0.15; da < 2 && !fnd; da += 0.15) for (const sg of [1, -1]) if (!blocked(want + sg * da)) { want += sg * da; fnd = true; break; } if (!fnd) break; }
        if (x < X0 + L3 * 0.1) want = Math.max(want, -Math.PI / 2 + 0.4) > 0 ? want : Math.max(want, -Math.PI / 2 + 0.4);
        if (x > X1 - L3 * 0.1) want = Math.min(want, -Math.PI / 2 - 0.4);
        let dh = want - hd; while (dh > Math.PI) dh -= 6.2832; while (dh < -Math.PI) dh += 6.2832;
        hd += Math.max(-0.1, Math.min(0.1, dh));
        x += Math.cos(hd) * step; y += Math.sin(hd) * step; pts.push([x, y]);
      }
      if (!okB || pts.length < 8) {
        // pas de passage depuis une tige : la liane entre par le bord du haut, comme une branche retombante
        const a2l = R() * 6.28, sgE = R() < 0.5 ? -1 : 1;
        const tp = [], cx = Math.min(X1 - L3 * 0.08, Math.max(X0 + L3 * 0.08, best[0] - sgE * L3 * 0.12)); let hx = cx, hy = Y0 - step * 3, hh = Math.PI / 2 + sgE * 0.7, ok2 = false;
        tp.push([hx, hy]);
        for (let k = 0; k < 200; k++) {
          if (Math.hypot(best[0] - hx, best[1] - hy) < L3 * 0.05) { ok2 = true; break; }
          // une liane qui retombe en S, jamais une tige raide
          let want = Math.atan2(best[1] - hy, best[0] - hx) + 0.55 * Math.sin(hy / (LH * 0.12) * 6.2832 + a2l);
          const blocked = h => !clearF(hx + Math.cos(h) * step * 2, hy + Math.sin(h) * step * 2) || hx + Math.cos(h) * step < X0 + sw + gut || hx + Math.cos(h) * step > X1 - sw - gut;
          if (blocked(want)) { let fnd = false; for (let da = 0.15; da < 2 && !fnd; da += 0.15) for (const sg of [1, -1]) if (!blocked(want + sg * da)) { want += sg * da; fnd = true; break; } if (!fnd) break; }
          let dh = want - hh; while (dh > Math.PI) dh -= 6.2832; while (dh < -Math.PI) dh += 6.2832;
          hh += Math.max(-0.1, Math.min(0.1, dh)); hx += Math.cos(hh) * step; hy += Math.sin(hh) * step; tp.push([hx, hy]);
        }
        // la branche part de la tige de la fleur voisine du vide, fait le tour de la fleur au joint, puis entre dans le vide
        let fo = null, fd = 1e9; fl.forEach(o => { const d = Math.hypot(o.x - best[0], o.y - best[1]) - o.R; if (d < fd) { fd = d; fo = o; } });
        const own = fo && stems.find(s => s.f === fo);
        if (!own || own.pts.length < 3) continue;
        const rOfL = th => { const NSr = fo.rad.length; let a = th / 6.2832 * NSr; a = ((a % NSr) + NSr) % NSr; const i = Math.floor(a), t = a - i; return fo.rad[i] * (1 - t) + fo.rad[(i + 1) % NSr] * t; };
        const root = own.pts[1], th0 = Math.atan2(root[1] - fo.y, root[0] - fo.x), th1 = Math.atan2(best[1] - fo.y, best[0] - fo.x);
        let dth = th1 - th0; while (dth > Math.PI) dth -= 6.2832; while (dth < -Math.PI) dth += 6.2832;
        const wp = [root], nW = Math.max(6, Math.ceil(Math.abs(dth) * (fo.R + gut + sw) / step)); let okW = true;
        if (Math.abs(dth) > 1.2) continue;          // jamais de boucle autour d'une fleur
        const clearO = (qx, qy) => qx > X0 + sw + gut && qx < X1 - sw - gut && qy > Y0 + sw + gut && fl.every(o => o === fo || Math.hypot(qx - o.x, qy - o.y) > _volR(o, qx, qy) + gut + sw)
          && stems.every(s2 => s2 === own || s2.pts.every(v => Math.hypot(v[0] - qx, v[1] - qy) > sw + gut * 1.5));
        for (let k = 1; k <= nW; k++) { const th = th0 + dth * k / nW, rr = rOfL(th) + gut + sw * 0.9, qx = fo.x + Math.cos(th) * rr, qy = fo.y + Math.sin(th) * rr; if (!clearO(qx, qy)) { okW = false; break; } wp.push([qx, qy]); }
        if (!okW) continue;
        let wx = wp[wp.length - 1][0], wy = wp[wp.length - 1][1];
        for (let k = 0; k < 60; k++) {
          const dx = best[0] - wx, dy = best[1] - wy, d = Math.hypot(dx, dy); if (d < L3 * 0.05) break;
          const nxp = wx + dx / d * step, nyp = wy + dy / d * step; if (!clearO(nxp, nyp)) break;
          wx = nxp; wy = nyp; wp.push([wx, wy]);
        }
        if (wp.length < 6) continue;
        stems.push({ pts: wp, f: null, dead: true, rev: true });
        occ = occS; wp.forEach(v => markDisc(v[0], v[1], sw * 0.55 + gut)); occ = occB;
        continue;
      }
      stems.push({ pts, f: null, dead: true, rev: true });   // base au bord du bas, bout dans le vide (il reçoit sa feuille)
      occ = occS; for (let i = 0; i < pts.length; i++) markDisc(pts[i][0], pts[i][1], sw * 0.55 + gut); occ = occB;
    }
    // les tiges, lissées : une courbe continue, jamais cassée — les greffes restent collées à leur tige
    const eq = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-6;
    stems.forEach(s => { const P = s.pts, a = P[0], z = P[P.length - 1]; stems.forEach(o => { if (o === s) return; o.pts.forEach((v, j) => { if (!s.gS && eq(v, a) && P.length > 2) s.gS = [o, j]; if (!s.gE && eq(v, z)) s.gE = [o, j]; }); }); });
    stems.forEach(s => {
      let P = s.pts;
      for (let pass = 0; pass < 6; pass++) { const nq = P.map(v => v.slice()); for (let i = 2; i < P.length - 2; i++) { nq[i] = [(P[i - 2][0] + P[i - 1][0] + P[i][0] + P[i + 1][0] + P[i + 2][0]) / 5, (P[i - 2][1] + P[i - 1][1] + P[i][1] + P[i + 1][1] + P[i + 2][1]) / 5]; } P = nq; }
      s.pts = P;
    });
    // aucune tige ne touche une fleur qui n'est pas la sienne : on la repousse au joint, selon le vrai contour de la fleur
    const rOf = (o, th) => { if (!o.rad) return o.R; const NS = o.rad.length; let a = th / 6.2832 * NS; a = ((a % NS) + NS) % NS; const i = Math.floor(a), t = a - i; return o.rad[i] * (1 - t) + o.rad[(i + 1) % NS] * t; };
    for (let pass = 0; pass < 3; pass++) stems.forEach(s => {
      const P = s.pts;
      for (let i = (s.f ? 2 : 1); i < P.length; i++) for (const o of fl) {
        if (o === s.f) continue;
        const dx = P[i][0] - o.x, dy = P[i][1] - o.y, d = Math.hypot(dx, dy) || 1e-6, need = rOf(o, Math.atan2(dy, dx)) + gut + sw * 0.6;
        if (d < need) { P[i] = [o.x + dx / d * need, o.y + dy / d * need]; }
      }
    });
    stems.forEach(s => { if (s.gE) s.pts[s.pts.length - 1] = s.gE[0].pts[s.gE[1]]; if (s.gS) s.pts[0] = s.gS[0].pts[s.gS[1]]; });
    // le repoussage a pu créer des coudes : on relisse (Chaikin), puis on revérifie le joint — deux fois
    for (let round = 0; round < 2; round++) {
      stems.forEach(s => {
        let P = s.pts; if (P.length < 4) return;
        for (let pass = 0; pass < 2; pass++) { const nq = [P[0]]; for (let i = 0; i < P.length - 1; i++) { const a = P[i], b = P[i + 1]; if (i > 0) nq.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25]); if (i < P.length - 2) nq.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } nq.push(P[P.length - 1]); P = nq; }
        // on ré-échantillonne à pas régulier pour garder une épaisseur régulière
        const out = [P[0]]; let acc = 0;
        for (let i = 1; i < P.length; i++) { acc += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); if (acc >= step || i === P.length - 1) { out.push(P[i]); acc = 0; } }
        s.pts = out;
      });
      stems.forEach(s => {
        const P = s.pts;
        for (let i = (s.f ? 2 : 1); i < P.length - 1; i++) for (const o of fl) {
          if (o === s.f) continue;
          const dx = P[i][0] - o.x, dy = P[i][1] - o.y, d = Math.hypot(dx, dy) || 1e-6, need = rOf(o, Math.atan2(dy, dx)) + gut + sw * 0.6;
          if (d < need) P[i] = [o.x + dx / d * need, o.y + dy / d * need];
        }
      });
      stems.forEach(s => { if (s.gE) s.pts[s.pts.length - 1] = s.gE[0].pts[Math.min(s.gE[0].pts.length - 1, s.gE[1])]; if (s.gS) s.pts[0] = s.gS[0].pts[Math.min(s.gS[0].pts.length - 1, s.gS[1])]; });
    }
    // les greffes, recalées sur le point le plus proche de leur tige après ré-échantillonnage
    stems.forEach(s => { for (const key of ['gE', 'gS']) { const g2 = s[key]; if (!g2) continue; const ix = key === 'gE' ? s.pts.length - 1 : 0, me = s.pts[ix]; let bj = 0, bd = 1e9; g2[0].pts.forEach((v, j) => { const d = Math.hypot(v[0] - me[0], v[1] - me[1]); if (d < bd) { bd = d; bj = j; } }); s.pts[ix] = g2[0].pts[bj]; } });
    const V2 = _volFeuilles(W, H, R, fl, stems, X0, X1, Y0, Y1, gut, sw);
    if (V2) {
      // les derniers vides reçoivent de rares fleurs d'encre, qui ne sont pas des dalles (comme dans la référence)
      const occP = [];
      V2.leaves.forEach(P => { for (let i = 0; i < P.length; i += 2) occP.push([P[i][0], P[i][1], 0]); });
      stems.forEach(s => s.pts.forEach(v => occP.push([v[0], v[1], sw * 0.5])));
      V2.pets.forEach(pl => pl.forEach(v => occP.push([v[0], v[1], sw * 0.4])));
      fl.forEach(o => { for (let i = 0; i < o.pts.length; i += 2) occP.push([o.pts[i][0], o.pts[i][1], 0]); });
      const deco = [];
      for (let rep = 0; rep < 6; rep++) {
        let best = null, bdv = 0;
        for (let gy = 0; gy < 44; gy++) for (let gx = 0; gx < 20; gx++) {
          const px = X0 + (gx + 0.5) / 20 * (X1 - X0), py = Y0 + (gy + 0.5) / 44 * (Y1 - Y0);
          let d = Math.min(px - X0, X1 - px, py - Y0, Y1 - py);
          for (const o of occP) { const dd = Math.hypot(o[0] - px, o[1] - py) - o[2]; if (dd < d) { d = dd; if (d < bdv) break; } }
          if (d > bdv) { bdv = d; best = [px, py]; }
        }
        if (deco.length >= (fl.length < 8 ? 1 : 2)) break;
        if (!best || bdv - gut * 1.6 < L3 * 0.1) break;
        const q = _lcg(((S.g ^ 0xdec0) + rep * 977) >>> 0), r0 = Math.min(L3 * 0.13, bdv - gut * 1.6), nP = 4 + Math.floor(q() * 3), rot = q() * 6.2832, notch = [], NS = 72, pts = [];
        let acc2 = 0; const ws = []; for (let k = 0; k < nP; k++) { const w = 0.6 + 0.8 * q(); ws.push(w); acc2 += w; }
        let cum = 0; for (let k = 0; k < nP; k++) { cum += ws[k] / acc2; notch.push([rot + cum * 6.2832, 0.12 + 0.12 * q(), 0.08 + 0.08 * q()]); }
        const h2 = q() * 6.28, h3 = q() * 6.28;
        for (let a = 0; a < NS; a++) {
          const th = a / NS * 6.2832; let m = 0.93 + 0.04 * Math.sin(2 * th + h2) + 0.03 * Math.sin(3 * th + h3);
          for (const [an, dp, wd] of notch) { let d = th - an; while (d > Math.PI) d -= 6.2832; while (d < -Math.PI) d += 6.2832; m -= dp * Math.exp(-(d / wd) * (d / wd)); }
          pts.push([best[0] + Math.cos(th) * r0 * m, best[1] + Math.sin(th) * r0 * m]);
        }
        const dots = [], nD = 3 + Math.floor(q() * 4);
        for (let t = 0; t < 60 && dots.length < nD; t++) { const a = q() * 6.28, d = r0 * 0.2 * Math.sqrt(q()), x = best[0] + Math.cos(a) * d, y = best[1] + Math.sin(a) * d, rr = r0 * 0.055 * (0.7 + 0.6 * q()); if (dots.every(o => Math.hypot(o[0] - x, o[1] - y) > (o[2] + rr) * 1.4)) dots.push([x, y, rr, 0.85 + 0.3 * q(), q() * 3]); }
        // la fleur d'encre a sa tige : elle part de la tige la plus proche et monte jusque sous la fleur, sans rien toucher
        let sp2 = null, sd2 = 1e9; stems.forEach(s => s.pts.forEach((v, i) => { if (i < 2) return; const d = Math.hypot(v[0] - best[0], v[1] - best[1]); if (d < sd2) { sd2 = d; sp2 = v; } }));
        if (!sp2) continue;
        const stp = L3 * 0.012, pl = [sp2]; let px = sp2[0], py = sp2[1], hd = Math.atan2(best[1] - py, best[0] - px), reached = false;
        const clearAt = (x, y, k) => {
          if (x < X0 + sw + gut || x > X1 - sw - gut || y < Y0 + sw + gut) return false;
          if (!fl.every(o => Math.hypot(x - o.x, y - o.y) > rOf(o, Math.atan2(y - o.y, x - o.x)) + gut + sw)) return false;
          if (k < 4) return true;
          for (const o of occP) if (Math.hypot(o[0] - x, o[1] - y) < o[2] + gut + sw * 0.5) return false;
          return true;
        };
        for (let k = 0; k < 140; k++) {
          if (Math.hypot(best[0] - px, best[1] - py) < r0 * 0.85) { reached = true; break; }
          let want = Math.atan2(best[1] - py, best[0] - px);
          const blocked = h => !clearAt(px + Math.cos(h) * stp * 2, py + Math.sin(h) * stp * 2, k);
          if (blocked(want)) { let fnd = false; for (let da = 0.15; da < 2 && !fnd; da += 0.15) for (const sg of [1, -1]) if (!blocked(want + sg * da)) { want += sg * da; fnd = true; break; } if (!fnd) break; }
          let dh = want - hd; while (dh > Math.PI) dh -= 6.2832; while (dh < -Math.PI) dh += 6.2832;
          hd += Math.max(-0.12, Math.min(0.12, dh)); px += Math.cos(hd) * stp; py += Math.sin(hd) * stp; pl.push([px, py]);
        }
        if (!reached || pl.length < 4) { occP.push([best[0], best[1], r0]); continue; }   // pas de tige possible : pas de fleur
        for (let pass = 0; pass < 3; pass++) { const nq = [pl[0]]; for (let i = 0; i < pl.length - 1; i++) { const a = pl[i], b = pl[i + 1]; if (i > 0) nq.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25]); if (i < pl.length - 2) nq.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } nq.push(pl[pl.length - 1]); pl.length = 0; nq.forEach(v => pl.push(v)); }
        V2.pets.push(pl);
        deco.push({ pts, dots });
        pts.forEach(v => occP.push([v[0], v[1], 0])); pl.forEach(v => occP.push([v[0], v[1], sw * 0.4]));
      }
      return { fl, stems, leaves: V2.leaves, pets: V2.pets, deco, M, sw };
    }
  }
  function _volFeuilles(W, H, R, fl, stems, X0, X1, Y0, Y1, gut, sw) {
    // les tiges sont lissées une dernière fois AVANT d'y accrocher les feuilles : chaque col touche la courbe finale
    stems.forEach(s => {
      let P = s.pts; if (P.length < 4) return;
      // pas régulier d'abord (les grands sauts font des coudes que le lissage n'efface pas)
      { const st2 = L3 * 0.008, out = [P[0]]; for (let i = 1; i < P.length; i++) { const a = out[out.length - 1], b = P[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]); if (d > st2 * 1.5) { const n2 = Math.ceil(d / st2); for (let k = 1; k < n2; k++) out.push([a[0] + (b[0] - a[0]) * k / n2, a[1] + (b[1] - a[1]) * k / n2]); } out.push(b); } P = out; }
      for (let pass = 0; pass < 6; pass++) { const nq = [P[0]]; for (let i = 0; i < P.length - 1; i++) { const a = P[i], b = P[i + 1]; if (i > 0) nq.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25]); if (i < P.length - 2) nq.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } nq.push(P[P.length - 1]); P = nq; }
      { const st3 = L3 * 0.011, out = [P[0]]; let acc = 0; for (let i = 1; i < P.length; i++) { acc += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); if (acc >= st3 || i === P.length - 1) { out.push(P[i]); acc = 0; } } P = out; }
      s.pts = P;
    });
    // deux tiges qui se frôlent se greffent l'une sur l'autre au premier contact : jamais deux tiges collées
    for (let j = 1; j < stems.length; j++) {
      const P = stems[j].pts;
      // seulement quand elles courent vraiment ensemble (plusieurs points de suite), pas un simple frôlement
      let run = 0, first = null;
      outer: for (let k = 2; k < P.length - 1; k++) {
        let hit = null;
        for (let i = 0; i < j && !hit; i++) { const Q = stems[i].pts; for (let m2 = 0; m2 < Q.length; m2++) if (Math.hypot(Q[m2][0] - P[k][0], Q[m2][1] - P[k][1]) < sw + gut * 1.2) { hit = [i, m2, k]; break; } }
        if (hit) { run++; if (!first) first = hit; if (run >= 4) { const [i, m2, k0] = first; stems[j].pts = P.slice(0, k0).concat([stems[i].pts[m2]]); stems[j].gE = [stems[i], m2]; stems[j].dead = false; break outer; } }
        else { run = 0; first = null; }
      }
    }
    // et après lissage, un croisement franc devient une greffe au point de rencontre
    for (let j = 1; j < stems.length; j++) {
      const P = stems[j].pts; let done = false;
      for (let k = 2; k < P.length - 2 && !done; k++) for (let i = 0; i < j && !done; i++) {
        const Q = stems[i].pts;
        for (let m2 = 0; m2 < Q.length - 1; m2++) {
          const a0 = P[k], a1 = P[k + 1], b0 = Q[m2], b1 = Q[m2 + 1], d1x = a1[0] - a0[0], d1y = a1[1] - a0[1], d2x = b1[0] - b0[0], d2y = b1[1] - b0[1], den = d1x * d2y - d1y * d2x;
          if (Math.abs(den) < 1e-9) continue;
          const t1 = ((b0[0] - a0[0]) * d2y - (b0[1] - a0[1]) * d2x) / den, t2 = ((b0[0] - a0[0]) * d1y - (b0[1] - a0[1]) * d1x) / den;
          if (t1 >= 0 && t1 <= 1 && t2 >= 0 && t2 <= 1) { const mj = t2 < 0.5 ? m2 : m2 + 1; stems[j].pts = P.slice(0, k + 1).concat([Q[mj]]); stems[j].gE = [stems[i], mj]; stems[j].dead = false; done = true; break; }
        }
      }
    }
    stems.forEach(s => { if (!s.gE) return; const me = s.pts[s.pts.length - 1]; let bj = 0, bd = 1e9; s.gE[0].pts.forEach((v, j) => { const d = Math.hypot(v[0] - me[0], v[1] - me[1]); if (d < bd) { bd = d; bj = j; } }); s.pts[s.pts.length - 1] = s.gE[0].pts[bj]; });
    const clipH = (poly, mx, my, nx, ny) => _clipH(poly, mx, my, nx, ny);
    const obst = [];
    stems.forEach(s => { for (let i = 2; i < s.pts.length; i += 2) obst.push([s.pts[i][0], s.pts[i][1], sw * 0.5 + gut]); });
    fl.forEach(o => { for (let i = 0; i < o.pts.length; i += 3) obst.push([o.pts[i][0], o.pts[i][1], gut]); });
    const attachPool = []; stems.forEach(s => { for (let i = 2; i < s.pts.length; i++) attachPool.push(s.pts[i]); });
    const inFrame = (x, y, m) => x > X0 + m && x < X1 - m && y > Y0 + m && y < Y1 - m;
    const farFromFlowers = (x, y, m) => fl.every(o => Math.hypot(x - o.x, y - o.y) > _volR(o, x, y) + m);
    // l'espacement des feuilles suit la place disponible : peu de fleurs, de grandes feuilles espacées
    const seeds = [], pets = [], sp0 = L3 * (fl.length <= 6 ? 0.15 : fl.length <= 14 ? 0.115 : 0.06), off = L3 * (fl.length > 20 ? 0.045 : 0.062);
    // une tige qui s'arrête en chemin se termine sur une feuille, posée d'abord à son bout
    stems.forEach(s => {
      if (!s.dead || s.pts.length < 4) return;
      const P = s.pts, a = P[P.length - 1], b = P[P.length - 3], d = Math.atan2(a[1] - b[1], a[0] - b[0]);
      const x = a[0] + Math.cos(d) * L3 * 0.07, y = a[1] + Math.sin(d) * L3 * 0.07;
      const sd = { x, y, A: a, tipOf: s }; seeds.push(sd); s.tipSeed = sd;
    });
    // (a) le long des tiges, alternées d'un côté et de l'autre
    stems.forEach(s => {
      const P = s.pts; let acc = sp0 * R(), side = R() < 0.5 ? 1 : -1;
      for (let i = 3; i < P.length - 1; i++) {
        acc += Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); if (acc < sp0 * (0.6 + 0.9 * R())) continue;
        acc = 0; side = -side;
        const t = Math.atan2(P[i + 1][1] - P[i - 1][1], P[i + 1][0] - P[i - 1][0]), nx = -Math.sin(t), ny = Math.cos(t), back = (R() - 0.3) * L3 * 0.03;
        // on essaie un côté puis l'autre, de loin puis de près : dans un couloir étroit entre deux fleurs, une petite feuille trouve sa place
        let placed = false;
        for (const [sd, fo] of [[side, 1], [-side, 1], [side, 0.6], [-side, 0.6], [side, 0.42], [-side, 0.42]]) {
          const o2 = off * fo * (0.7 + 0.6 * R()), bk = back + (fo < 1 ? L3 * 0.02 : 0) + (R() - 0.5) * L3 * 0.03;
          const x = P[i][0] + nx * sd * o2 - Math.cos(t) * bk, y = P[i][1] + ny * sd * o2 - Math.sin(t) * bk;
          if (!inFrame(x, y, L3 * 0.015) || !farFromFlowers(x, y, L3 * 0.03 * fo)) continue;
          if (seeds.some(q => Math.hypot(q.x - x, q.y - y) < L3 * 0.07 * Math.max(0.65, fo))) continue;
          seeds.push({ x, y, A: P[i], stem: s, idx: i, narrow: !farFromFlowers(x, y, off * 1.5) }); placed = true; break;
        }
        if (!placed) continue;
      }
    });
    // (b) les vides : la feuille reçoit une tige secondaire depuis la tige la plus proche — jamais de feuille flottante
    const nearObst = (x, y, m) => obst.some(o => Math.hypot(o[0] - x, o[1] - y) < o[2] + m);
    for (let it = 0; it < 10000; it++) {
      const x = X0 + R() * (X1 - X0), y = Y0 + R() * (Y1 - Y0), spc = it < 3000 ? L3 * 0.1 : it < 6500 ? L3 * 0.085 : L3 * 0.064;
      if (!inFrame(x, y, L3 * 0.025) || !fl.every(o => Math.hypot(x - o.x, y - o.y) > o.R * 1.05 + gut + L3 * 0.012)) continue;
      if (seeds.some(q => Math.hypot(q.x - x, q.y - y) < spc)) continue;
      if (nearObst(x, y, L3 * 0.025)) continue;
      let bd = 1e9, bp = null; for (const v of attachPool) { const d = Math.hypot(v[0] - x, v[1] - y); if (d < bd) { bd = d; bp = v; } }
      if (!bp || bd > L3 * 0.6) continue;
      if (bd < L3 * 0.085) { seeds.push({ x, y, A: bp }); continue; }
      // la tige secondaire pousse pas à pas vers le vide et contourne les fleurs, comme une vraie tige
      const pl = [bp]; let px = bp[0], py = bp[1], hd = _volTan(stems, pets, bp, x, y), reached = false; const stp = L3 * 0.012, curl = (R() - 0.5) * 0.25;
      // vers une poche située au-dessus de la racine (au-dessus des fleurs du haut), la tige a le droit de contourner
      const up = y < bp[1] - L3 * 0.05, maxK = up ? 180 : 90, maxTurn = up ? 3.3 : 1.6;
      for (let k = 0; k < maxK; k++) {
        const tx = x - px, ty = y - py; if (Math.hypot(tx, ty) < L3 * 0.05) { reached = true; break; }
        let want = Math.atan2(ty, tx) + curl * Math.max(0, 1 - k / 30);
        const blocked = h => { const qx = px + Math.cos(h) * stp * 3, qy = py + Math.sin(h) * stp * 3; return !farFromFlowers(qx, qy, gut + sw) || qx < X0 + sw + gut || qx > X1 - sw - gut || qy < Y0 + sw + gut; };
        if (blocked(want)) { let fnd = false; for (let da = 0.2; da < 2.6 && !fnd; da += 0.2) for (const sg of [1, -1]) if (!blocked(want + sg * da)) { want += sg * da; fnd = true; break; } if (!fnd) break; }
        let dh = want - hd; while (dh > Math.PI) dh -= 6.2832; while (dh < -Math.PI) dh += 6.2832;
        const turn = Math.max(-0.12, Math.min(0.12, dh)); hd += turn; pl.turn = (pl.turn || 0) + Math.abs(turn);
        px += Math.cos(hd) * stp; py += Math.sin(hd) * stp; pl.push([px, py]);
      }
      if (!reached || pl.length < 3 || (pl.turn || 0) > maxTurn) continue;
      // lissage (Chaikin), la racine reste sur sa tige et le bout reste au col de la feuille
      for (let pass = 0; pass < 3; pass++) {
        const nq = [pl[0]];
        for (let i = 0; i < pl.length - 1; i++) { const a = pl[i], b = pl[i + 1]; if (i > 0) nq.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25]); if (i < pl.length - 2) nq.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); }
        nq.push(pl[pl.length - 1]); pl.length = 0; nq.forEach(v => pl.push(v));
      }
      let ok = true;
      for (let k = 2; k < pl.length && ok; k++) {
        const px = pl[k][0], py = pl[k][1];
        if (!farFromFlowers(px, py, gut + sw)) ok = false;
        else if (seeds.some(q => Math.hypot(q.x - px, q.y - py) < L3 * 0.03)) ok = false;
        else if (k > 3 && stems.some(s => s.pts.some(v => Math.hypot(v[0] - px, v[1] - py) < sw + gut))) ok = false;
        else if (pets.some(p2 => p2.some(v => Math.hypot(v[0] - px, v[1] - py) < sw + gut))) ok = false;
      }
      if (!ok) continue;
      if (bp.pet) pl.parent = bp.pet;
      pets.push(pl); pl.slice(2).forEach(v => { obst.push([v[0], v[1], sw * 0.4 + gut]); v.pet = pl; attachPool.push(v); });
      const sd = { x, y, A: pl[pl.length - 1], pet: pl }; pl.seed = sd; seeds.push(sd);
    }
    // (c) chaque feuille remplit sa place, aplatie par ses voisines, tenue au joint des tiges et des fleurs
    const Rc = L3 * 0.16, leaves = [];
    seeds.forEach(s => {
      const ax = s.x - s.A[0], ay = s.y - s.A[1], al = Math.hypot(ax, ay) || 1, ux = ax / al, uy = ay / al, poly0 = [];
      // c'est la place, pas un gabarit, qui borne la feuille : elle grandit jusqu'au joint de ses voisines
      const Rs = L3 * (0.2 + 0.06 * R());
      for (let k = 0; k < 18; k++) { const th = k / 18 * 6.2832, rx = Math.cos(th) * Rs * 1.15, ry = Math.sin(th) * Rs * 0.95; poly0.push([s.x + rx * ux - ry * uy, s.y + rx * uy + ry * ux]); }
      let poly = poly0;
      for (const q of seeds) { if (q === s) continue; const dx = q.x - s.x, dy = q.y - s.y, d = Math.hypot(dx, dy); if (d > Rs * 2.8 || d < 1e-6) continue; const t = (d / 2 - gut / 2) / d; poly = clipH(poly, s.x + dx * t, s.y + dy * t, dx, dy); if (poly.length < 3) break; }
      if (poly.length >= 3) for (const o of obst) { const dx = o[0] - s.x, dy = o[1] - s.y, d = Math.hypot(dx, dy); if (d > Rs * 1.4 + o[2] || d < 1e-6) continue; const t = Math.max(0.05, (d - o[2]) / d); poly = clipH(poly, s.x + dx * t, s.y + dy * t, dx, dy); if (poly.length < 3) break; }
      // le cadre garde son joint, comme entre deux formes (le bas reste ouvert : les tiges en sortent)
      if (poly.length >= 3) { poly = clipH(poly, X0 + gut, 0, -1, 0); poly = clipH(poly, X1 - gut, 0, 1, 0); poly = clipH(poly, 0, Y0 + gut, 0, -1); poly = clipH(poly, 0, Y1, 0, 1); }
      const vd = _vd;
      if (poly.length < 3) { vd.clip++; return; }
      let ar = 0; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) ar += poly[j][0] * poly[i][1] - poly[i][0] * poly[j][1];
      // une feuille portée le long d'une tige a le droit d'être petite : un couloir étroit garde ses feuilles
      // plus il y a de fleurs, plus les feuilles ont le droit d'être petites : le feuillage reste dense, jamais de vide
      const dens = fl.length > 20 ? 0.62 : fl.length > 12 ? 0.8 : 1;
      const small = !!s.narrow, fA = (small ? 0.026 : 0.04) * dens, fI = (small ? 0.016 : 0.025) * dens, fK = small ? 0.2 : 0.3, fB = (small ? 0.02 : 0.03) * dens;
      if (Math.abs(ar) / 2 < (L3 * fA) ** 2) { vd.area++; return; }
      if (ar < 0) poly.reverse();
      let per = 0; for (let i = 0; i < poly.length; i++) { const p1 = poly[i], p2 = poly[(i + 1) % poly.length]; per += Math.hypot(p2[0] - p1[0], p2[1] - p1[1]); }
      if (2 * Math.abs(ar) / 2 / per < L3 * fI) { vd.inr++; return; }          // rayon inscrit trop petit : ce serait un éclat
      // la feuille n'est pas la case : c'est une forme lisse (le contour de la case filtré à 3 harmoniques),
      // réduite d'un seul facteur jusqu'à tenir entièrement dedans — aucune arête droite, le joint est tenu
      const cellP = poly.slice();
      // la feuille est centrée sur sa place (centroïde de la case), pas sur la graine collée à la tige
      let Cx = 0, Cy = 0, A6 = 0;
      for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const cr = poly[j][0] * poly[i][1] - poly[i][0] * poly[j][1]; A6 += cr; Cx += (poly[j][0] + poly[i][0]) * cr; Cy += (poly[j][1] + poly[i][1]) * cr; }
      if (Math.abs(A6) > 1e-9) { Cx /= 3 * A6; Cy /= 3 * A6; } else { Cx = s.x; Cy = s.y; }
      const NS = 48, rc = new Float64Array(NS);
      for (let a = 0; a < NS; a++) {
        const th = a / NS * 6.2832, cx2 = Math.cos(th), sy2 = Math.sin(th); let best = 1e9;
        for (let i = 0; i < poly.length; i++) {
          const p1 = poly[i], p2 = poly[(i + 1) % poly.length], ex = p2[0] - p1[0], ey = p2[1] - p1[1], den = cx2 * ey - sy2 * ex;
          if (Math.abs(den) < 1e-12) continue;
          const t = ((p1[0] - Cx) * ey - (p1[1] - Cy) * ex) / den, uu = ((p1[0] - Cx) * sy2 - (p1[1] - Cy) * cx2) / den;
          if (t > 0 && uu >= 0 && uu <= 1 && t < best) best = t;
        }
        rc[a] = best < 1e9 ? best : 0;
      }
      const cf = []; for (let h = 0; h <= 2; h++) { let re = 0, im = 0; for (let a = 0; a < NS; a++) { const th = a / NS * 6.2832; re += rc[a] * Math.cos(h * th); im += rc[a] * Math.sin(h * th); } cf.push([re / NS * (h ? 2 : 1), im / NS * (h ? 2 : 1)]); }
      const lp = new Float64Array(NS); let kmin = 1;
      for (let a = 0; a < NS; a++) { const th = a / NS * 6.2832; let r = 0; cf.forEach(([re, im], h) => { r += re * Math.cos(h * th) + im * Math.sin(h * th); }); lp[a] = Math.max(r, 1e-3); kmin = Math.min(kmin, rc[a] * 0.98 / lp[a]); }
      if (!(kmin > fK)) { vd.inr++; return; }
      poly = []; for (let a = 0; a < NS; a++) { const th = a / NS * 6.2832, r = lp[a] * kmin; poly.push([Cx + Math.cos(th) * r, Cy + Math.sin(th) * r]); }
      // le corps de la feuille vient jusqu'à sa tige (au joint près) : jamais de longue queue
      { let kk = 0, dk = 1e9; poly.forEach((v, i) => { const d = Math.hypot(v[0] - s.A[0], v[1] - s.A[1]); if (d < dk) { dk = d; kk = i; } });
        // … mais sans jamais sortir de sa case : les cases sont disjointes, donc aucune feuille ne peut en toucher une autre
        const want = sw * 0.5 + gut * 1.1;
        if (dk > want) {
          const V0 = poly[kk], ux2 = (s.A[0] - V0[0]) / dk, uy2 = (s.A[1] - V0[1]) / dk, mvMax = dk - want;
          const nC = cellP.length, sg0 = (() => { let a = 0; for (let i = 0; i < nC; i++) { const p1 = cellP[i], p2 = cellP[(i + 1) % nC]; a += p1[0] * p2[1] - p2[0] * p1[1]; } return a > 0 ? 1 : -1; })();
          const inCell = (x, y) => { for (let i = 0; i < nC; i++) { const p1 = cellP[i], p2 = cellP[(i + 1) % nC]; if (sg0 * ((p2[0] - p1[0]) * (y - p1[1]) - (p2[1] - p1[1]) * (x - p1[0])) < 0) return false; } return true; };
          const fitsAt = mv => poly.every(v => inCell(v[0] + ux2 * mv, v[1] + uy2 * mv));
          let lo = 0, hi = mvMax; if (fitsAt(hi)) lo = hi; else for (let it = 0; it < 12; it++) { const md = (lo + hi) / 2; if (fitsAt(md)) lo = md; else hi = md; }
          if (lo > 0) poly = poly.map(v => [v[0] + ux2 * lo, v[1] + uy2 * lo]);
        } }
      // le col : la feuille s'amincit juste avant de toucher sa tige
      let k = 0, kd = 1e9; poly.forEach((v, i) => { const d = Math.hypot(v[0] - s.A[0], v[1] - s.A[1]); if (d < kd) { kd = d; k = i; } });
      const n = poly.length, V = poly[k], A = s.A, L = Math.hypot(A[0] - V[0], A[1] - V[1]) || 1, dx = (A[0] - V[0]) / L, dy = (A[1] - V[1]) / L, nx = -dy, ny = dx;
      // une petite feuille au bout d'un long col ferait une fléchette : on la retire
      let rb = 0; for (let a = 0; a < NS; a++) rb += lp[a] * kmin; rb /= NS;
      if (rb < L3 * fB || L > 1.6 * rb) { vd.inr++; return; }
      // le col, lisse : on retire l'arc du contour tourné vers la tige, et ses deux bouts rejoignent la tige
      // par des courbes qui partent dans le prolongement du contour et se pincent jusqu'à la largeur de la tige
      const wa = sw * 0.45, m = 7, i1 = (k - m + n) % n, i2 = (k + m) % n, E1 = poly[i1], E2 = poly[i2];
      const T1 = poly[(i1 - 1 + n) % n], T2 = poly[(i2 + 1) % n];
      let t1x = E1[0] - T1[0], t1y = E1[1] - T1[1], t1l = Math.hypot(t1x, t1y) || 1; t1x /= t1l; t1y /= t1l;
      let t2x = E2[0] - T2[0], t2y = E2[1] - T2[1], t2l = Math.hypot(t2x, t2y) || 1; t2x /= t2l; t2y /= t2l;
      const sg = ((E1[0] - A[0]) * nx + (E1[1] - A[1]) * ny) > 0 ? 1 : -1;
      const A1 = [A[0] + nx * wa * sg, A[1] + ny * wa * sg], A2 = [A[0] - nx * wa * sg, A[1] - ny * wa * sg];
      const d1 = Math.hypot(A1[0] - E1[0], A1[1] - E1[1]), d2 = Math.hypot(A2[0] - E2[0], A2[1] - E2[1]);
      const bez = (P0, C1, C2, P3, out) => { for (let j = 1; j <= 8; j++) { const t = j / 8, v = 1 - t; out.push([v * v * v * P0[0] + 3 * v * v * t * C1[0] + 3 * v * t * t * C2[0] + t * t * t * P3[0], v * v * v * P0[1] + 3 * v * v * t * C1[1] + 3 * v * t * t * C2[1] + t * t * t * P3[1]]); } };
      const neck = [];
      bez(E1, [E1[0] + t1x * d1 * 0.45, E1[1] + t1y * d1 * 0.45], [A1[0] - dx * d1 * 0.4, A1[1] - dy * d1 * 0.4], A1, neck);
      neck.push(A2);
      bez(A2, [A2[0] - dx * d2 * 0.4, A2[1] - dy * d2 * 0.4], [E2[0] + t2x * d2 * 0.45, E2[1] + t2y * d2 * 0.45], E2, neck);
      const body = []; for (let j = 0; j <= n - 2 * m; j++) body.push(poly[(i2 + j) % n]);
      leaves.push(body.concat(neck.slice(0, -1))); s.ok = true;
    });
    // si la feuille du bout n'a pas trouvé sa place, la tige est raccourcie jusqu'à sa dernière feuille
    // passe de couverture : tant qu'un point reste loin de tout motif, une tige secondaire vient y porter une feuille
    {
      const occ = [];
      leaves.forEach(P => { for (let i = 0; i < P.length; i += 2) occ.push([P[i][0], P[i][1], 0]); });
      stems.forEach(s => s.pts.forEach(v => occ.push([v[0], v[1], sw * 0.5])));
      pets.forEach(pl => pl.forEach(v => occ.push([v[0], v[1], sw * 0.4])));
      fl.forEach(o => { for (let i = 0; i < o.pts.length; i += 2) occ.push([o.pts[i][0], o.pts[i][1], 0]); });
      const dist = (x, y, lim) => { let d = Math.min(x - X0, X1 - x, y - Y0, Y1 - y); for (const o of occ) { const dd = Math.hypot(o[0] - x, o[1] - y) - o[2]; if (dd < d) { d = dd; if (d < lim) return d; } } return d; };
      const pool = []; stems.forEach(s => { for (let i = 2; i < s.pts.length; i++) pool.push(s.pts[i]); }); pets.forEach(pl => pl.forEach(v => pool.push(v)));
      const tried2 = [];
      for (let rep = 0; rep < 45; rep++) {
        let best = null, bdv = 0;
        for (let gy = 0; gy < 40; gy++) for (let gx = 0; gx < 18; gx++) {
          const px = X0 + (gx + 0.5) / 18 * (X1 - X0), py = Y0 + (gy + 0.5) / 40 * (Y1 - Y0);
          if (tried2.some(t => Math.hypot(t[0] - px, t[1] - py) < L3 * 0.08)) continue;
          const d = dist(px, py, bdv); if (d > bdv) { bdv = d; best = [px, py]; }
        }
        if (!best || bdv < L3 * (fl.length > 20 ? 0.032 : 0.045)) break;
        tried2.push(best);
        const rr = bdv - gut * 1.3;
        let bp = null, bd = 1e9; pool.forEach(v => { const d = Math.hypot(v[0] - best[0], v[1] - best[1]); if (d < bd) { bd = d; bp = v; } });
        if (!bp) continue;
        const stp = L3 * 0.012, pl = [bp]; let px = bp[0], py = bp[1], hd = _volTan(stems, pets, bp, best[0], best[1]), ok = false;
        const blocked = (h, k) => { const qx = px + Math.cos(h) * stp * 2, qy = py + Math.sin(h) * stp * 2; if (qx < X0 + sw + gut || qx > X1 - sw - gut || qy < Y0 + sw + gut || qy > Y1) return true; if (!fl.every(o => Math.hypot(qx - o.x, qy - o.y) > _volR(o, qx, qy) + gut + sw)) return true; if (k < 3) return false; return dist(qx, qy, sw * 0.5 + gut) < sw * 0.5 + gut; };
        for (let k = 0; k < 150; k++) {
          if (Math.hypot(best[0] - px, best[1] - py) < rr * 0.95) { ok = true; break; }
          let want = Math.atan2(best[1] - py, best[0] - px);
          if (blocked(want, k)) { let fnd = false; for (let da = 0.15; da < 2 && !fnd; da += 0.15) for (const sg of [1, -1]) if (!blocked(want + sg * da, k)) { want += sg * da; fnd = true; break; } if (!fnd) break; }
          let dh = want - hd; while (dh > Math.PI) dh -= 6.2832; while (dh < -Math.PI) dh += 6.2832;
          hd += Math.max(-0.12, Math.min(0.12, dh)); px += Math.cos(hd) * stp; py += Math.sin(hd) * stp; pl.push([px, py]);
        }
        if (!ok || pl.length < 3) {
          // aucun chemin depuis une tige : la feuille part de la tige de la fleur voisine, contourne la fleur au joint, puis entre dans le vide
          let fo = null, fd = 1e9; fl.forEach(o => { const d = Math.hypot(o.x - best[0], o.y - best[1]) - o.R; if (d < fd) { fd = d; fo = o; } });
          const own = fo && stems.find(s2 => s2.f === fo);
          if (!own || own.pts.length < 3 || !fo.rad) continue;
          const root = own.pts[1], th0 = Math.atan2(root[1] - fo.y, root[0] - fo.x), th1 = Math.atan2(best[1] - fo.y, best[0] - fo.x);
          let dth = th1 - th0; while (dth > Math.PI) dth -= 6.2832; while (dth < -Math.PI) dth += 6.2832;
          // on essaie les deux sens autour de la fleur (jusqu'à un demi-tour), et on garde le premier chemin libre
          const clr = (qx, qy) => qx > X0 + sw + gut && qx < X1 - sw - gut && qy > Y0 + sw + gut && fl.every(o => o === fo || Math.hypot(qx - o.x, qy - o.y) > _volR(o, qx, qy) + gut + sw) && dist(qx, qy, sw * 0.5 + gut) >= sw * 0.5 + gut * 0.9;
          const dirs = [dth, dth > 0 ? dth - 6.2832 : dth + 6.2832].filter(d => Math.abs(d) <= Math.PI * 1.05).sort((a, b) => Math.abs(a) - Math.abs(b));
          let found = null;
          for (const dd of dirs) {
            const wp = [root], nW = Math.max(6, Math.ceil(Math.abs(dd) * (fo.R + gut + sw) / stp)); let okW = true;
            for (let k = 1; k <= nW; k++) { const th = th0 + dd * k / nW, r2 = _volR(fo, fo.x + Math.cos(th), fo.y + Math.sin(th)) + gut + sw * 0.9, qx = fo.x + Math.cos(th) * r2, qy = fo.y + Math.sin(th) * r2; if (k > 2 && !clr(qx, qy)) { okW = false; break; } wp.push([qx, qy]); }
            if (!okW) continue;
            let wx = wp[wp.length - 1][0], wy = wp[wp.length - 1][1], reached2 = false;
            for (let k = 0; k < 80; k++) { const dx = best[0] - wx, dy = best[1] - wy, d = Math.hypot(dx, dy); if (d < rr * 0.95) { reached2 = true; break; } const nxp = wx + dx / d * stp, nyp = wy + dy / d * stp; if (!clr(nxp, nyp)) break; wx = nxp; wy = nyp; wp.push([wx, wy]); }
            if (reached2) { found = wp; break; }
          }
          if (!found) continue;
          // lissage de la tige qui contourne (pas de coude au départ du contour)
          let F2 = found; for (let pass = 0; pass < 3; pass++) { const nq = [F2[0]]; for (let i = 0; i < F2.length - 1; i++) { const a = F2[i], b = F2[i + 1]; if (i > 0) nq.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25]); if (i < F2.length - 2) nq.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } nq.push(F2[F2.length - 1]); F2 = nq; }
          pl.length = 0; F2.forEach(v => pl.push(v));
        }
        for (let pass = 0; pass < 3; pass++) { const nq = [pl[0]]; for (let i = 0; i < pl.length - 1; i++) { const a = pl[i], b = pl[i + 1]; if (i > 0) nq.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25]); if (i < pl.length - 2) nq.push([a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); } nq.push(pl[pl.length - 1]); pl.length = 0; nq.forEach(v => pl.push(v)); }
        // la feuille : un ovale qui tient dans le vide, allongé vers sa tige, avec son col court
        const E = pl[pl.length - 1], ang = Math.atan2(best[1] - E[1], best[0] - E[0]), cxl = best[0], cyl = best[1], rx = rr * 0.98, ry = rr * (0.7 + 0.2 * R()), body = [];
        for (let a = 0; a < 40; a++) { const th = a / 40 * 6.2832, ux = Math.cos(th) * rx, uy = Math.sin(th) * ry; body.push([cxl + ux * Math.cos(ang) - uy * Math.sin(ang), cyl + ux * Math.sin(ang) + uy * Math.cos(ang)]); }
        let kk = 0, dk = 1e9; body.forEach((v, i) => { const d = Math.hypot(v[0] - E[0], v[1] - E[1]); if (d < dk) { dk = d; kk = i; } });
        const nx2 = -Math.sin(ang), ny2 = Math.cos(ang), wa2 = sw * 0.45, m3 = 5, nB = body.length;
        const E1 = body[(kk - m3 + nB) % nB], E2 = body[(kk + m3) % nB];
        const neck = [[E[0] + nx2 * wa2, E[1] + ny2 * wa2], [E[0] - nx2 * wa2, E[1] - ny2 * wa2]];
        const s1 = ((E1[0] - E[0]) * nx2 + (E1[1] - E[1]) * ny2) > 0;
        const out = []; for (let j = 0; j <= nB - 2 * m3; j++) out.push(body[(kk + m3 + j) % nB]);
        leaves.push(out.concat(s1 ? neck : neck.reverse()));
        pets.push(pl);
        out.forEach(v => occ.push([v[0], v[1], 0])); pl.forEach(v => { occ.push([v[0], v[1], sw * 0.4]); pool.push(v); });
        const sd = { x: best[0], y: best[1], A: E, pet: pl, ok: true }; pl.seed = sd; seeds.push(sd);
      }
    }
    // une tige secondaire n'existe que si elle porte une feuille (ou une autre tige qui en porte une)
    const keep = new Set();
    pets.forEach(pl => { if (pl.seed && pl.seed.ok) { let q = pl; while (q && !keep.has(q)) { keep.add(q); q = q.parent; } } });
    const kept = pets.filter(pl => keep.has(pl));
    // tout ce qui s'accroche réellement à une tige : feuilles gardées, racines des tiges secondaires, greffes des autres tiges
    const anchors = [];
    seeds.forEach(q => { if (q.ok) anchors.push(q.A); });
    kept.forEach(pl => anchors.push(pl[0]));
    stems.forEach(o => anchors.push(o.pts[o.pts.length - 1]));
    const same = (a, b) => a === b || Math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-6;
    stems.forEach(s => {
      if (!s.dead || (s.tipSeed && s.tipSeed.ok)) return;
      // la tige s'arrête juste après son dernier point d'attache — jamais en dessous d'une feuille qui y tient
      const P = s.pts; let last = 1;
      for (let i = 2; i < P.length - 1; i++) if (anchors.some(a => a !== P[P.length - 1] && same(a, P[i]))) last = i;
      s.pts = P.slice(0, last + 1);
    });

    return { leaves, pets: kept };
  }
  // une tige secondaire quitte sa tige dans le sens de celle-ci (du côté de sa cible) : elle s'en détache en douceur, sans coude
  function _volTan(stems, pets, bp, tx, ty) {
    const to = Math.atan2(ty - bp[1], tx - bp[0]);
    const lists = stems.map(s => s.pts).concat(pets);
    for (const P of lists) {
      const i = P.indexOf(bp); if (i < 0) continue;
      const a = P[Math.max(0, i - 2)], b = P[Math.min(P.length - 1, i + 2)]; let t = Math.atan2(b[1] - a[1], b[0] - a[0]);
      let d = to - t; while (d > Math.PI) d -= 6.2832; while (d < -Math.PI) d += 6.2832;
      if (Math.abs(d) > Math.PI / 2) { t += Math.PI; d = to - t; while (d > Math.PI) d -= 6.2832; while (d < -Math.PI) d += 6.2832; }
      return t + Math.max(-0.45, Math.min(0.45, d));       // un départ à peine écarté de la tige
    }
    return to;
  }
  function _volR(o, x, y) {
    if (!o.rad) return o.R * 1.12;
    const NS = o.rad.length; let a = Math.atan2(y - o.y, x - o.x) / 6.2832 * NS; a = ((a % NS) + NS) % NS;
    const i = Math.floor(a), t = a - i; return o.rad[i] * (1 - t) + o.rad[(i + 1) % NS] * t;
  }  /* ================= fin du code de la planche ================= */

  // le semis du jardin : une fleur par promesse (et par Nuée), aux places où le moteur POSE les graines (`env.finale`)
  function _fin() { try { return env.finale || null; } catch (_) { return null; } }
  /* ⚑ v91 (Tom : « voir les tiges et les feuilles se tisser, pas une transition fondue suivie d'un nouvel état ») — au Studio, une fleur
     GARDE SA PLACE d'un événement à l'autre (comme les yeux de Ramage) : le moteur relâchait toutes les places à chaque événement, et
     tout le jardin se retraçait — le feuillage du centre se défaisait en fragments. Seule la fleur qui arrive prend la sienne. */
  var _volGel = null;
  function _semis(sansDeparts) {
    var F = _fin(), pr = [], i, s, gel = null;
    /* ⚑ v92 (Tom : « Volubilis — porte-le aussi sur la vraie Toile ») — la Toile vivante garde aussi les places : sa clé est celle de son
       semis (comme les yeux de Ramage). Une dalle rendue ailleurs (Index, Fil : la Toile n'est pas vivante) garde l'équilibre du moteur. */
    if ((window._apImage || env.vive) && !window._volGelOff) { var sem = window._apImage ? String(window._apPhase || '').split('|')[0] : 'T' + (env.cleToile == null ? 0 : env.cleToile) + ':' + Math.round(W) + 'x' + Math.round(H); if (!_volGel || _volGel.sem !== sem) _volGel = { sem: sem, pos: {} }; gel = _volGel.pos; }
    for (i = 0; i < seeds.length; i++) { s = seeds[i]; if (s.kind === 'gray') continue; if (sansDeparts && s.part != null) continue;
      var h = _cle(s), q = gel && gel[h] ? gel[h] : (F ? F.get(s) : null); if (gel && !gel[h] && q) gel[h] = [q[0], q[1]];
      pr.push({ s: s, h: h, x: q ? q[0] : s.x, y: q ? q[1] : s.y }); }
    pr.sort(function (a, b) { return a.h - b.h; });
    return pr;
  }
  function _sig(pr) { var h = 2166136261; function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(env.uMat * 16)); mix(env.cleToile == null ? 0 : env.cleToile);
    pr.forEach(function (p) { mix(p.h); mix(Math.round(p.x * 2)); mix(Math.round(p.y * 2)); }); return h >>> 0; }
  var _jardins = {}, _nJ = [];
  function _jardin(pr) {
    var sig = _sig(pr); if (_jardins[sig]) return _jardins[sig];
    var K = env.uMat / UPL; L3 = 300 * K; LH = 650 * K;
    var t0 = performance.now(), ct = env.cleToile;
    var B = _volBuild({ pr: pr, g: (ct == null ? 1 : ct) >>> 0 });
    B.duree = performance.now() - t0; return _finitJardin(B, sig, K, ct); }
  /* ⚑ v72 (budget) — LE JARDIN D'ARRIVÉE SE CONSTRUIT DANS UN WORKER. Construire un jardin coûte 0,5 à 1,3 s (planche : 500–900 ms) ;
     à la plantation il se faisait d'un bloc, l'image gelée. Le MÊME code (les fonctions de la planche, recopiées telles quelles dans
     le Worker) le construit hors du fil principal, sur les mêmes données : le jardin rendu est identique. Pendant ce temps, le jardin
     qu'on voyait reste affiché ; le glissement part à son arrivée. Sans Worker (ou s'il échoue) : la construction d'avant, sur place. */
  var _W = null, _WA = {}, _WN = 0;
  function _worker() { if (_W !== null) return _W; _W = false;
    try { var src = 'var W,H,L3,LH,_vd={clip:0,area:0,inr:0},window={_tailleApercu:function(s){return s&&s.__t!=null?s.__t:1;}};\n' +
        [_fnv, _lcg, _clipH, _pip, _volFleurPts, _volBuild, _volFeuilles, _volTan, _volR].map(function (f) { return f.toString(); }).join('\n') +
        '\nonmessage=function(e){var d=e.data;W=d.W;H=d.H;L3=d.L3;LH=d.LH;var t0=Date.now();try{var B=_volBuild(d.S);B.dureeW=Date.now()-t0;postMessage({id:d.id,B:B});}catch(x){postMessage({id:d.id,err:String(x)});}};';
      _W = new Worker(URL.createObjectURL(new Blob([src], { type: 'text/javascript' })));
      _W.onmessage = function (e) { var d = e.data, J = _WA[d.id]; delete _WA[d.id]; if (!J) return;
        if (d.err || !d.B) { J.echec = true; window._volWorker = { err: d.err }; if (typeof env.relance === 'function') env.relance(); return; }
        var B = d.B, parH = {}; J.pr.forEach(function (p) { parH[p.h] = p; });
        B.fl.forEach(function (f) { var p0 = parH[f.p.h]; if (p0) f.p.s = p0.s; });
        B.duree = performance.now() - J.t0; var t1 = performance.now(); _finitJardin(B, J.sig, J.K, J.ct);
        window._volWorker = { attente: Math.round(B.duree), worker: B.dureeW, finition: Math.round(performance.now() - t1) };
        if (typeof env.relance === 'function') env.relance(); };
      _W.onerror = function () { _W = false; for (var k in _WA) _WA[k].echec = true; }; }
    catch (_) { _W = false; }
    return _W; }
  // le jardin de ces places : tout de suite s'il est déjà fait ; sinon demandé au Worker (rend null tant qu'il n'est pas là)
  function _jardinFond(pr) { var sig = _sig(pr); if (_jardins[sig]) { var Jc = _jardins[sig]; pr.forEach(function (p) { var f = Jc.parCle[p.h]; if (f && f.s !== p.s) { f.s = p.s; if (f.p) f.p.s = p.s; } }); return Jc; }   /* v92 : un jardin préparé sur la plantation simulée se rattache aux vraies graines */
    for (var k in _WA) if (_WA[k].sig === sig) return _WA[k].echec ? _jardin(pr) : null;
    var w = _worker(); if (!w) return _jardin(pr);
    var K = env.uMat / UPL, ct = env.cleToile, id = ++_WN;
    _WA[id] = { sig: sig, pr: pr, K: K, ct: ct, t0: performance.now() };
    try { w.postMessage({ id: id, W: W, H: H, L3: 300 * K, LH: 650 * K, S: { pr: pr.map(function (p) { return { h: p.h, x: p.x, y: p.y, s: { __t: window._tailleApercu(p.s) } }; }), g: (ct == null ? 1 : ct) >>> 0 } }); }
    catch (_) { delete _WA[id]; return _jardin(pr); }
    return null; }
  function _finitJardin(B, sig, K, ct) {
    B.sig = sig; B.K = K; B.W = W; B.H = H; B.ct = ct;
    B.parCle = {}; B.fl.forEach(function (f) { f.k = f.p.h; f.s = f.p.s; B.parCle[f.k] = f; f.rad = f.rad || _radDe(f); f.Rhit = f.Rhit || Math.max.apply(null, f.rad); });
    _feuillage(B);
    _jardins[sig] = B; _nJ.push(sig); if (_nJ.length > 6) delete _jardins[_nJ.shift()];
    window._volConstruit = { ms: Math.round(B.duree), fleurs: B.fl.length, feuilles: B.leaves.length };   /* publié : le coût d'une construction */
    return B;
  }
  // une fleur dont la vraie forme n'a pu se faire garde le gabarit de volFleurPts : on en relit le rayon, angle par angle
  function _radDe(f) { var NS = 96, r = new Float64Array(NS);
    for (var a = 0; a < NS; a++) { var th = a / NS * TAU, best = 0, bd = 9;
      f.pts.forEach(function (v) { var d = Math.abs(((Math.atan2(v[1] - f.y, v[0] - f.x) - th) % TAU + TAU * 1.5) % TAU - Math.PI); if (d < bd) { bd = d; best = Math.hypot(v[0] - f.x, v[1] - f.y); } }); r[a] = best; }
    return r; }
  // le feuillage d'un jardin : un seul tracé (feuilles, tiges, bouts ronds, fleurs d'encre et leurs cœurs découpés), et les tiges fines
  function _feuillage(B) {
    // feuilles et tiges : DEUX tracés, comme la planche — réunis, un col de feuille posé sur une tige de sens inverse y perçait un trou
    var Fe = new Path2D(), T = new Path2D(), P = new Path2D(), sw = B.sw;
    B.leaves.forEach(function (Q) { _trace(Fe, Q); }); B.Fe = Fe;
    B.stems.forEach(function (s, si) {
      var Q = s.pts, n = Q.length, Lf = [], Rr = [];
      for (var k = 0; k < n; k++) {
        var a = Q[Math.max(0, k - 1)], b = Q[Math.min(n - 1, k + 1)], d = Math.atan2(b[1] - a[1], b[0] - a[0]), t = k / Math.max(1, n - 1);
        var w = sw * (0.8 + 0.4 * (s.rev ? 1 - t : t)) * (1 + 0.08 * Math.sin(k * 0.35 + si * 1.7)) / 2;
        Lf.push([Q[k][0] - Math.sin(d) * w, Q[k][1] + Math.cos(d) * w]); Rr.push([Q[k][0] + Math.sin(d) * w, Q[k][1] - Math.cos(d) * w]);
      }
      T.moveTo(Lf[0][0], Lf[0][1]); Lf.forEach(function (v) { T.lineTo(v[0], v[1]); }); Rr.reverse().forEach(function (v) { T.lineTo(v[0], v[1]); }); T.closePath();
      var e = Q[n - 1], we = Math.hypot(Lf[n - 1][0] - e[0], Lf[n - 1][1] - e[1]); s._cap = [e[0], e[1], we];
    });
    B.T = T;
    var C = new Path2D(); B.stems.forEach(function (s) { if (s._cap) { var c = s._cap; C.moveTo(c[0] + c[2], c[1]); C.arc(c[0], c[1], c[2], 0, TAU); } }); B.C = C;
    B.pets.forEach(function (pl) { P.moveTo(pl[0][0], pl[0][1]); for (var i = 1; i < pl.length - 1; i++) { var mx = (pl[i][0] + pl[i + 1][0]) / 2, my = (pl[i][1] + pl[i + 1][1]) / 2; P.quadraticCurveTo(pl[i][0], pl[i][1], mx, my); } var e2 = pl[pl.length - 1]; P.lineTo(e2[0], e2[1]); });
    B.P = P;
    var D = new Path2D(); (B.deco || []).forEach(function (d) { _trace(D, d.pts); d.dots.forEach(function (o) { D.moveTo(o[0] + o[2], o[1]); D.ellipse(o[0], o[1], o[2], o[2] * o[3], o[4], 0, TAU); }); }); B.D = D;
  }
  // une fleur, posée : son contour (rayon par angle autour de son centre) et son cœur de pois, à l'échelle `sc`
  function _fleur(f, cx, cy, rad, sc) {
    var NS = rad.length, pts = [];
    for (var a = 0; a < NS; a++) { var th = a / NS * TAU, r = rad[a] * sc; pts.push([cx + Math.cos(th) * r, cy + Math.sin(th) * r]); }
    var dots = f.dots.map(function (o) { return [cx + (o[0] - f.x) * sc, cy + (o[1] - f.y) * sc, o[2] * sc, o[3], o[4]]; });
    return { f: f, s: f.s, k: f.k, x: cx, y: cy, pts: pts, dots: dots, Rhit: Math.max.apply(null, rad) * sc };
  }
  // ce qu'on voit : un jardin, ou le glissement de l'un à l'autre
  var _tr = null, _aff = null, _fige = null;
  function _volInclus(B) { var cl = {}, i; for (i = 0; i < seeds.length; i++) if (seeds[i].kind !== 'gray' && seeds[i].part == null) cl[_cle(seeds[i])] = 1; for (i = 0; i < B.fl.length; i++) if (!cl[B.fl[i].k]) return false; return true; }
  function _memesCles(B) { var n = 0, i, s; for (i = 0; i < seeds.length; i++) { s = seeds[i]; if (s.kind === 'gray' || s.part != null) continue; n++; if (!B.parCle[_cle(s)]) return false; } return n === B.fl.length; }
  function _scene(now) {
    var TR = env.vive ? env.trans : null;
    if (TR || (_tr && !_tr.fini && env.vive)) {
      if (TR && (!_tr || _tr.n !== TR.n)) { var J0 = _aff;
        /* v75 — au Studio, on ARRIVE sur Volubilis : le jardin qu'on voyait n'est pas celui de cette Toile (c'est celui d'une autre, ou d'un
           autre tour) ; on part du jardin de repos, préparé d'avance par le Worker — à défaut, construit sur place, comme avant. */
        if (window._apImage && TR.kind === 'arrive' && (!J0 || J0.W !== W || J0.H !== H || !_volInclus(J0))) { var iD = -1, sD = null, prB; for (var q = 0; q < seeds.length; q++) if (seeds[q].t0 != null && seeds[q].t0 >= TR.t0 - 1 && seeds[q].part == null) { iD = q; sD = seeds[q]; break; }
          if (iD >= 0) seeds.splice(iD, 1); try { prB = _semis(false); } finally { if (iD >= 0) seeds.splice(iD, 0, sD); }   // le repos d'avant l'arrivée : sans la dalle neuve (sa place d'équilibre aussi)
          J0 = _jardinFond(prB) || _jardin(prB); }
        _tr = { n: TR.n, J0: J0, J1: null, t: 0, fini: false, o: TR.x != null ? [TR.x, TR.y] : null }; }
      // l'horloge du glissement part à l'image QUI SUIT la construction : l'heure de l'image où l'on construit est déjà en retard
      if (!_tr.J1) { if (!_tr.pr1) _tr.pr1 = _semis(true); _tr.J1 = _jardinFond(_tr.pr1); _tr.t = Infinity;   /* les places d'arrivée : lues UNE fois, à la première image (comme avant) */
        _tr.neuf = true; window._mondeEncore = true;
        // v72 : le jardin d'arrivée n'est pas encore là — celui qu'on voyait reste, tel quel
        if (!_tr.J1) { if (window._apImage) window._volBouge = true; var Jv = _tr.J0 || _jardin(_semis(false)), Fv = Jv.fl.map(function (f) { return _fleur(f, f.x, f.y, f.rad, 1); }), bu = _bourgeon(TR, now); if (bu) Fv.push(bu);
          return { fleurs: Fv, feuilles: [[Jv, 1]], J: Jv }; } }
      else if (_tr.t === Infinity) { _tr.t = now; if (window._volMesure) window._volPaire = { J0: _tr.J0, J1: _tr.J1 }; }
      var MV = 1800;   /* v91 : au Studio, le tissage prend 1,8 s — ⚑ v93 (Tom, 28 sept. : « passe-le à 1,8 s, comme au Studio. Tous les mondes au même rythme des deux côtés ») : la Toile aussi */
      var a = _lisse((now - _tr.t) / MV), J0 = _tr.J0, J1 = _tr.J1, F = [], k;
      if (a >= 1) { _tr.fini = true; _fige = J1; _aff = J1; }
      else window._mondeEncore = true;
      if (window._apImage) window._volBouge = !_tr.fini;   /* v91 : au Studio, l'événement suivant attend la fin du tissage (sinon il repart du jardin d'avant : saut) */
      for (k in J1.parCle) { var f1 = J1.parCle[k], f0 = J0 && J0.parCle[k];
        if (f0) { var rad = new Float64Array(f1.rad.length); for (var i = 0; i < rad.length; i++) rad[i] = f0.rad[i % f0.rad.length] + (f1.rad[i] - f0.rad[i % f0.rad.length]) * a;
          var fl = _fleur(f1, f0.x + (f1.x - f0.x) * a, f0.y + (f1.y - f0.y) * a, rad, 1);
          fl.dots = f1.dots.map(function (o, j) { var p0 = f0.dots[j] || o; return [p0[0] + (o[0] - p0[0]) * a, p0[1] + (o[1] - p0[1]) * a, p0[2] + (o[2] - p0[2]) * a, o[3], o[4]]; });
          F.push(fl); }
        else if (_tr.bud && _tr.bud.k === +k) { var b0 = _tr.bud.sc; F.push(_fleur(f1, _tr.bud.x + (f1.x - _tr.bud.x) * a, _tr.bud.y + (f1.y - _tr.bud.y) * a, f1.rad, b0 + (1 - b0) * a)); }   // v85 : le bourgeon s'ouvre, sans retomber
        else F.push(_fleur(f1, f1.x, f1.y, f1.rad, a)); }
      if (J0) for (k in J0.parCle) if (!J1.parCle[k]) { var d0 = J0.parCle[k]; F.push(_fleur(d0, d0.x, d0.y, d0.rad, 1 - a)); }
      return { fleurs: F, feuilles: [[J1, 1]], J: J1, tr: (J0 && a < 1) ? { J0: J0, J1: J1, t: (now - _tr.t) / MV, T0: _tr, o: (TR && TR.x != null) ? [TR.x, TR.y] : (_tr.o || null) } : null };
    }
    var J;
    if (env.vive && _fige && _memesCles(_fige)) J = _fige;   // au repos, le jardin d'arrivée reste (§15.14)
    /* la dalle seule, l'export, le contour, le toucher de CETTE Toile lisent le jardin qu'on voit — reconstruit sur les places du
       moteur, qui peuvent avoir bougé, il en serait un autre (mesuré : 4 % des touchers à côté, une dalle d'une autre taille) */
    else if (!env.vive && _aff && _aff.W === W && _aff.H === H && _aff.ct === env.cleToile && _memesCles(_aff)) J = _aff;
    else { J = _jardin(_semis(false)); if (env.vive) _fige = J; }
    if (env.vive) _aff = J;   // le jardin qu'on voit : celui d'où partira la prochaine transition
    return { fleurs: J.fl.map(function (f) { return _fleur(f, f.x, f.y, f.rad, 1); }), feuilles: [[J, 1]], J: J };
  }
  function _chemFleur(fl) { var T = new Path2D(); _trace(T, fl.pts); fl.dots.forEach(function (o) { T.moveTo(o[0] + o[2], o[1]); T.ellipse(o[0], o[1], o[2], o[2] * o[3], o[4], 0, TAU); }); return T; }

  var _dernier = null;
  var _CR = window._calqueRepos ? window._calqueRepos() : null;
  function Rvol(now, x0, y0, x1, y1) {
    _sync();
    var S = _scene(now);
    if (env.vive && !env.trans && !S.tr && _CR && S.feuilles.length === 1) {   // v72 : au repos, le calque (v85 : jamais pendant que le feuillage pousse) (signature : le jardin, les couleurs, l'encre)
      var sg = [S.J.sig, _rgb(_encre())]; S.fleurs.forEach(function (fl) { sg.push(fl.k + ':' + _rgb(env.cOf(fl.s, now))); });
      if (_CR.pose(g, sg.join('|'), function (C) { var g0 = g; g = C; try { _peintVol(S, now); } finally { g = g0; } })) { _dernier = S; window._volComp = { fleurs: S.fleurs.length, feuilles: S.J.leaves.length }; return; }
    }
    _peintVol(S, now);
  }
  /* ⚑ v85 (Tom : « les fleurs éclosent, les tiges et les feuilles se tissent ; à la disparition elles se défont — pas de fondu ») — LE
     FEUILLAGE POUSSE. Pendant une transition, chaque élément a SON moment, tiré de sa distance au point où la fleur arrive ou part
     (le plus proche d'abord : 45 % du temps pour l'échelonnement, 55 % pour son geste) :
     · une tige qui mène à la MÊME fleur dans les deux jardins se déforme de l'une à l'autre (24 points à même abscisse curviligne) ;
       une tige neuve POUSSE depuis sa base, une tige disparue se RÉTRACTE vers la sienne ;
     · les feuilles, les tiges fines et les fleurs d'encre de l'ancien jardin se REPLIENT vers leur point d'attache, celles du
       nouveau s'y DÉPLIENT. Les fleurs, elles, éclosent, se referment ou glissent (déjà le cas).
     À la fin, le jardin exact prend la relève (tiges en ruban au lieu d'un trait rond : écart mesuré). */
  function _reech(Q, n) { var L = [0], i, tot; for (i = 1; i < Q.length; i++) L.push(L[i - 1] + Math.hypot(Q[i][0] - Q[i - 1][0], Q[i][1] - Q[i - 1][1])); tot = L[L.length - 1] || 1;
    var out = [], j = 0; for (i = 0; i < n; i++) { var s = tot * i / (n - 1); while (j < Q.length - 2 && L[j + 1] < s) j++; var u = (s - L[j]) / ((L[j + 1] - L[j]) || 1); out.push([Q[j][0] + (Q[j + 1][0] - Q[j][0]) * u, Q[j][1] + (Q[j + 1][1] - Q[j][1]) * u]); } return out; }
  function _partiel(Q, f) { if (f >= 0.999) return Q; if (f <= 0.001) return null; var R = _reech(Q, Math.max(2, Math.ceil(Q.length * f) + 1)), n = Math.max(2, Math.round(24 * f)); return _reech(Q, 24).slice(0, n); }
  /* v85 — LE BOURGEON (« aucune latence ») : le jardin d'arrivée se construit dans le Worker (0,5 à 2 s) ; pendant ce temps la fleur
     neuve bourgeonne déjà à sa place — SA forme (`_volFleurPts`, même tirage sur sa clé que dans le jardin), qui monte jusqu'au tiers
     de sa taille, puis s'ouvre pleinement quand le jardin arrive. */
  function _bourgeon(TR, now) { if (!TR || TR.kind !== 'arrive' || !_tr) return null; var D = null, i;
    for (i = 0; i < seeds.length; i++) { var s = seeds[i]; if (s.kind !== 'gray' && s.part == null && s.t0 != null && s.t0 >= TR.t0 - 1) { D = s; break; } } if (!D) return null;
    var h = _cle(D); if (!_tr.bud || _tr.bud.k !== h) { var q = _lcg(h ^ 0xf1a); q(); var R0 = L3 * 0.14 * window._tailleApercu(D); _tr.bud = { k: h, x: D.x, y: D.y, R: R0, rel: _volFleurPts(0, 0, R0, q), sc: 0 }; }
    var B = _tr.bud, sc = 0.35 * _lisse(Math.min(1, (now - TR.t0) / 1500)); B.sc = sc; if (sc < 0.02) return null;
    return { f: null, s: D, k: h, x: B.x, y: B.y, pts: B.rel.map(function (v) { return [B.x + v[0] * sc, B.y + v[1] * sc]; }), dots: [], Rhit: B.R * sc }; }
  /* ⚑ v88 (Tom, 28 sept. : « je veux voir les tiges et les feuilles pousser — et se dé-pousser. Aucun fondu nulle part. ») — PLUS
     AUCUNE INTERPOLATION DE FORME. Une tige POUSSE de sa base vers sa pointe ; chaque feuille, chaque fleur d'encre se DÉPLIE quand
     la tige passe son point d'attache. Au départ, l'inverse : les feuilles se replient d'abord, puis la tige se rétracte vers sa base.
     Une tige ou une feuille ne GLISSE d'un jardin à l'autre que si les deux sont presque identiques (≤ 0,1 L3 pour une tige, 0,12 L3
     pour une feuille : un déplacement, pas une métamorphose) — au-delà, l'interpolation se lisait comme une forme qui fond.
     Plus d'échelonnement depuis le point d'arrivée : chaque élément suit SA tige, pas une onde. */
  var POUSSE = 0.7;   // la part du temps où la tige pousse ; les feuilles finissent de se déplier dans le reste
  function _volAssoc(J0, J1) { var lim = L3 * 0.2, tolT = L3 * 0.1, tolF = L3 * 0.12, R = { t1: new Map(), t0g: new Set(), f1: new Map(), f0g: new Set(), phi: new Map() };
    var p0 = {}; J0.stems.forEach(function (s) { if (s.f && s.f.k != null) p0[s.f.k] = s; });
    var pris = new Set();
    J1.stems.forEach(function (s1) { var s0 = (s1.f && s1.f.k != null) ? p0[s1.f.k] : null;
      if (!s0) { var b = s1.pts[0], bd = L3 * 0.08; J0.stems.forEach(function (c) { if (pris.has(c) || (c.f && c.f.k != null)) return; var d = Math.hypot(c.pts[0][0] - b[0], c.pts[0][1] - b[1]); if (d < bd) { bd = d; s0 = c; } }); }
      if (!s0 || pris.has(s0)) return; var A = _reech(s0.pts, 24), B = _reech(s1.pts, 24), m = 0; for (var i = 0; i < 24; i++) m = Math.max(m, Math.hypot(A[i][0] - B[i][0], A[i][1] - B[i][1]));
      if (m <= tolT) { pris.add(s0); R.t1.set(s1, s0); } });
    J0.stems.forEach(function (s) { if (pris.has(s)) R.t0g.add(s); });
    var prisF = new Set();
    J1.leaves.forEach(function (Q1) { var bd = lim, b = null; J0.leaves.forEach(function (Q0) { if (prisF.has(Q0)) return; var d = Math.hypot(Q0[0][0] - Q1[0][0], Q0[0][1] - Q1[0][1]); if (d < bd) { bd = d; b = Q0; } });
      if (!b) return; var A = _reech(b.concat([b[0]]), 32), B = _reech(Q1.concat([Q1[0]]), 32), m = 0; for (var i = 0; i < 32; i++) m = Math.max(m, Math.hypot(A[i][0] - B[i][0], A[i][1] - B[i][1]));
      if (m <= tolF) { prisF.add(b); R.f1.set(Q1, b); } });
    J0.leaves.forEach(function (Q) { if (prisF.has(Q)) R.f0g.add(Q); });
    // le point d'attache de chaque feuille, de chaque fleur d'encre, de chaque tige fine : la place, le long de sa tige, où la pousse la déplie
    [J0, J1].forEach(function (J) { var ech = J.stems.map(function (s) { return _reech(s.pts, 24); });
      function phi(x, y) { var bd = L3 * 0.12, f = 0.5; ech.forEach(function (Q) { for (var i = 0; i < 24; i++) { var d = Math.hypot(Q[i][0] - x, Q[i][1] - y); if (d < bd) { bd = d; f = i / 23; } } }); return f; }
      J.leaves.forEach(function (Q) { R.phi.set(Q, phi(Q[0][0], Q[0][1])); });
      (J.pets || []).forEach(function (pl) { if (pl && pl.length) R.phi.set(pl, phi(pl[0][0], pl[0][1])); });
      (J.deco || []).forEach(function (d) { var cx = 0, cy = 0; d.pts.forEach(function (v) { cx += v[0]; cy += v[1]; }); R.phi.set(d, phi(cx / d.pts.length, cy / d.pts.length)); }); });
    return R; }
  function _feuillageTr(T, ink) { var J0 = T.J0, J1 = T.J1, t = Math.max(0, Math.min(1, T.t)), CT = T.T0 || T, A = CT.assoc || (CT.assoc = _volAssoc(J0, J1));   /* v91 : calculés UNE fois par transition */
    /* ⚑ v91 (Tom : « je veux voir les tiges et les feuilles se tisser, pas une transition fondue suivie d'un nouvel état ») — UN FRONT
       PART DE LA FLEUR QUI ARRIVE (ou qui part). Là où il passe, l'ancien se défait (les feuilles se replient vers leur attache, puis la
       tige se rétracte vers sa base), et juste derrière, au même endroit, le nouveau se tisse : la tige pousse depuis sa base, chaque
       feuille se déplie quand la pointe la dépasse. Rien ne change avant le front ; tout est posé derrière lui. */
    if (!CT.fr) { var o = T.o, pts = [];
      J1.stems.forEach(function (s) { if (!A.t1.get(s)) pts.push(s.pts[0]); }); J0.stems.forEach(function (s) { if (!A.t0g.has(s)) pts.push(s.pts[0]); });
      J1.leaves.forEach(function (Q) { if (!A.f1.has(Q)) pts.push(Q[0]); }); J0.leaves.forEach(function (Q) { if (!A.f0g.has(Q)) pts.push(Q[0]); });
      if (!o) { var cx = 0, cy = 0; pts.forEach(function (v) { cx += v[0]; cy += v[1]; }); o = pts.length ? [cx / pts.length, cy / pts.length] : [W / 2, H / 2]; }
      var dm = 1; pts.forEach(function (v) { var d = Math.hypot(v[0] - o[0], v[1] - o[1]); if (d > dm) dm = d; });
      CT.fr = { o: o, dm: dm }; }
    var FR = CT.fr, RET = 0.45, D0 = 0.24, D1 = 0.0;   /* le front parcourt la zone en 45 % du temps ; l'ancien se défait en 24 %, le nouveau se tisse 8 % derrière lui (47 %) — l'endroit ne se vide jamais */
    function av(p) { return Math.min(1, Math.hypot(p[0] - FR.o[0], p[1] - FR.o[1]) / FR.dm) * RET; }
    function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
    var gl = _lisse(t);
    function tisse(p0) { return _lisse(clamp((t - av(p0) - D1) / (1 - RET - D1))); }        // 0 → 1 : le nouveau se tisse (l'ancien se replie avec lui)
    /* v91 — LE MÊME DESSIN QUE LE JARDIN EXACT (`_feuillage`) : feuilles et fleurs d'encre en courbes (`_trace`), tiges en ruban effilé
       à bout rond, tiges fines en courbes, dans le même ordre. Aux deux bouts de la transition l'image EST celle du jardin (avant : des
       traits ronds et des polygones — à l'entrée et à la sortie, toutes les tiges changeaient d'aspect d'un coup). */
    function mix(P0, P1, u) { var Q = []; for (var i = 0; i < P1.length; i++) Q.push([P0[i][0] + (P1[i][0] - P0[i][0]) * u, P0[i][1] + (P1[i][1] - P0[i][1]) * u]); return Q; }
    function coupe(Q, f) { var n = Q.length, m = (n - 1) * Math.min(1, f), k0 = Math.floor(m), fr = m - k0, P = Q.slice(0, k0 + 1);
      if (fr > 1e-4 && k0 + 1 < n) P.push([Q[k0][0] + (Q[k0 + 1][0] - Q[k0][0]) * fr, Q[k0][1] + (Q[k0 + 1][1] - Q[k0][1]) * fr]); return { P: P, m: m, k0: k0 }; }
    function feuille(Q, px, py, sc) { if (sc <= 0.01) return; var Pf = new Path2D(); _trace(Pf, sc >= 0.999 ? Q : Q.map(function (v) { return [px + (v[0] - px) * sc, py + (v[1] - py) * sc]; })); g.fill(Pf); }
    function ruban(s, si, f, sw, pts) { var Q = pts || s.pts, n = Q.length; if (f <= 0.001 || n < 2) return; var c = coupe(Q, f), P = c.P, np = P.length; if (np < 2) return;
      var Lf = [], Rr = [];
      for (var k = 0; k < np; k++) { var a = P[Math.max(0, k - 1)], b = k + 1 < np ? P[k + 1] : P[k], kk = k <= c.k0 ? k : c.m;
        var d = Math.atan2(b[1] - a[1], b[0] - a[0]), tk = kk / Math.max(1, n - 1);
        var w = sw * (0.8 + 0.4 * (s.rev ? 1 - tk : tk)) * (1 + 0.08 * Math.sin(kk * 0.35 + si * 1.7)) / 2;
        Lf.push([P[k][0] - Math.sin(d) * w, P[k][1] + Math.cos(d) * w]); Rr.push([P[k][0] + Math.sin(d) * w, P[k][1] - Math.cos(d) * w]); }
      var T = new Path2D(); T.moveTo(Lf[0][0], Lf[0][1]); Lf.forEach(function (v) { T.lineTo(v[0], v[1]); }); Rr.slice().reverse().forEach(function (v) { T.lineTo(v[0], v[1]); }); T.closePath(); g.fill(T);
      var e = P[np - 1], we = Math.hypot(Lf[np - 1][0] - e[0], Lf[np - 1][1] - e[1]), C = new Path2D(); C.moveTo(e[0] + we, e[1]); C.arc(e[0], e[1], we, 0, TAU); g.fill(C); }
    function fine(pl, f, lw) { if (f <= 0.001 || !pl || pl.length < 2) return; var P = coupe(pl, f).P; if (P.length < 2) return; var T = new Path2D(); T.moveTo(P[0][0], P[0][1]);
      for (var i = 1; i < P.length - 1; i++) { var mx = (P[i][0] + P[i + 1][0]) / 2, my = (P[i][1] + P[i + 1][1]) / 2; T.quadraticCurveTo(P[i][0], P[i][1], mx, my); } var e2 = P[P.length - 1]; T.lineTo(e2[0], e2[1]); g.lineWidth = lw; g.stroke(T); }
    function deco(d, cx, cy, sc) { if (sc <= 0.01) return; var D = new Path2D(), mp = function (v) { return sc >= 0.999 ? v : [cx + (v[0] - cx) * sc, cy + (v[1] - cy) * sc]; };
      _trace(D, d.pts.map(mp)); d.dots.forEach(function (o) { var c = mp(o); D.moveTo(c[0] + o[2] * sc, c[1]); D.ellipse(c[0], c[1], o[2] * sc, o[2] * o[3] * sc, o[4], 0, TAU); }); g.fill(D, 'evenodd'); }
    function rech(P0, n) { return P0.length === n ? P0 : _reech(P0, n); }
    function rechF(Q0, n) { return Q0.length === n ? Q0 : _reech(Q0.concat([Q0[0]]), n + 1).slice(0, n); }
    function ancien(ph, p0) { var u = tisse(p0); return 1 - _lisse(clamp((u - 0.3 - (1 - ph) * 0.1) / 0.3)); }   /* l'ancien se replie PENDANT que le nouveau se déplie au même endroit — la densité reste */
    function neuf(ph, p0) { var u = tisse(p0); return _lisse(clamp((u - ph * 0.7) / 0.3)); }
    // 1 · les feuilles (comme `B.Fe`)
    J1.leaves.forEach(function (Q1) { var Q0 = A.f1.get(Q1); if (Q0) feuille(gl >= 1 ? Q1 : mix(rechF(Q0, Q1.length), Q1, gl), 0, 0, 1); });
    J0.leaves.forEach(function (Q) { if (A.f0g.has(Q)) return; feuille(Q, Q[0][0], Q[0][1], Math.sqrt(ancien(A.phi.get(Q) || 0, Q[0]))); });
    J1.leaves.forEach(function (Q) { if (A.f1.has(Q)) return; feuille(Q, Q[0][0], Q[0][1], Math.sqrt(neuf(A.phi.get(Q) || 0, Q[0]))); });
    // 2 · les tiges, en ruban, et leur bout rond (comme `B.T`, `B.C`)
    J1.stems.forEach(function (s1, si) { var s0 = A.t1.get(s1); if (s0) ruban(s1, si, 1, J1.sw, gl >= 1 ? null : mix(rech(s0.pts, s1.pts.length), s1.pts, gl)); });
    J0.stems.forEach(function (s0, si) { if (A.t0g.has(s0)) return; ruban(s0, si, 1 - _lisse(clamp((tisse(s0.pts[0]) - 0.55) / 0.4)), J0.sw); });   /* elle ne se retire qu'une fois ses feuilles remplacées */
    J1.stems.forEach(function (s1, si) { if (A.t1.get(s1)) return; ruban(s1, si, _lisse(clamp(tisse(s1.pts[0]) / 0.7)), J1.sw); });   /* la tige neuve pousse depuis sa base */
    // 3 · les tiges fines (comme `B.P`)
    [[J0, true], [J1, false]].forEach(function (c) { (c[0].pets || []).forEach(function (pl) { if (!pl || pl.length < 2) return; var ph = A.phi.get(pl) || 0; fine(pl, c[1] ? ancien(ph, pl[0]) : neuf(ph, pl[0]), c[0].sw * 0.75); }); });
    // 4 · les fleurs d'encre et leurs cœurs (comme `B.D`)
    [[J0, true], [J1, false]].forEach(function (c) { (c[0].deco || []).forEach(function (d) { var cx = 0, cy = 0; d.pts.forEach(function (v) { cx += v[0]; cy += v[1]; }); cx /= d.pts.length; cy /= d.pts.length; var ph = A.phi.get(d) || 0;
      deco(d, cx, cy, Math.sqrt(c[1] ? ancien(ph, [cx, cy]) : neuf(ph, [cx, cy]))); }); });
  }
  function _peintVol(S, now) {
    var J = S.J, M = J.M, ink = _rgb(_encre());
    g.save(); g.beginPath(); g.rect(M, M, W - 2 * M, H - 2 * M); g.clip();   // le jardin est tenu dans son cadre
    g.fillStyle = ink; g.strokeStyle = ink; g.lineCap = 'round';
    if (S.tr) _feuillageTr(S.tr, ink); else
    S.feuilles.forEach(function (e) { var B = e[0], al = e[1]; if (al <= 0.001) return; g.globalAlpha = al;
      g.fill(B.Fe); g.fill(B.T); g.fill(B.C); g.lineWidth = B.sw * 0.75; g.stroke(B.P); g.fill(B.D, 'evenodd'); });
    g.globalAlpha = 1;
    S.fleurs.forEach(function (fl) { if (!(fl.Rhit > 0.3)) return; g.fillStyle = _rgb(env.cOf(fl.s, now)); g.fill(_chemFleur(fl), 'evenodd'); });
    g.restore();
    _dernier = S; window._volComp = { fleurs: S.fleurs.length, feuilles: J.leaves.length };
  }

  function _trouve(s, S) { S = S || _scene(performance.now()); var k = _cle(s);
    for (var i = 0; i < S.fleurs.length; i++) if (S.fleurs[i].s === s) return S.fleurs[i];
    for (i = 0; i < S.fleurs.length; i++) if (S.fleurs[i].k === k) return S.fleurs[i];
    return null; }
  function _bb(fl) { var a0 = 1e18, b0 = 1e18, a1 = -1e18, b1 = -1e18; fl.pts.forEach(function (v) { if (v[0] < a0) a0 = v[0]; if (v[0] > a1) a1 = v[0]; if (v[1] < b0) b0 = v[1]; if (v[1] > b1) b1 = v[1]; }); return [a0, b0, a1, b1]; }
  function seule(nom, s, now, cx, cy, taille) {
    _sync(); var fl = _trouve(s); if (!fl || !(fl.Rhit > 0.3)) return false;
    var B = _bb(fl), sc = taille / Math.max(B[2] - B[0], B[3] - B[1], 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(B[0] + B[2]) / 2, -(B[1] + B[3]) / 2);
    var T = new Path2D(); _trace(T, fl.pts); g.fillStyle = _rgb(env.cOf(fl.s, now)); g.fill(T);
    // le cœur de la fleur, en PAPIER (décision Tom : pas à 72 % de blanc)
    var Pc = new Path2D(); fl.dots.forEach(function (o) { Pc.moveTo(o[0] + o[2], o[1]); Pc.ellipse(o[0], o[1], o[2], o[2] * o[3], o[4], 0, TAU); });
    if (typeof env.fondToile === 'function') { g.fillStyle = _rgb(_arr(env.fondToile())); g.fill(Pc); }
    g.restore(); return true;
  }
  function contour(nom, s) { _sync(); var fl = _trouve(s); return fl ? fl.pts.slice() : null; }
  function nature(nom, s) { _sync(); var fl = _trouve(s); return fl && fl.Rhit > 0.3 ? 'dalle' : null; }
  function boite(nom, s) { _sync(); var fl = _trouve(s); if (!fl || !(fl.Rhit > 0.3)) return null; var B = _bb(fl);
    return { x0: B[0] - 0.5, y0: B[1] - 0.5, x1: B[2] + 0.5, y1: B[3] + 0.5, fx0: B[0] - 0.5, fy0: B[1] - 0.5, fx1: B[2] + 0.5, fy1: B[3] + 0.5 }; }
  // le toucher : dans la fleur PEINTE (son cœur compris : le doigt ne vise pas un pois) ; jamais dans le feuillage
  function toucher(nom, x, y) {
    _sync(); var S = _dernier || _scene(performance.now());
    for (var i = S.fleurs.length - 1; i >= 0; i--) { var fl = S.fleurs[i]; if (fl.s.part != null || !(fl.Rhit > 0.3)) continue;
      if (Math.hypot(x - fl.x, y - fl.y) > fl.Rhit + 1e-6) continue; if (_pip(x, y, fl.pts)) return fl.s; }
    return null;
  }
  Rvol.ancre = function (s) { _sync(); var fl = _trouve(s, _dernier); if (!fl) return null; var B = _bb(fl); return [(B[0] + B[2]) / 2, (B[1] + B[3]) / 2, B[2] - B[0]]; };
  Rvol._preuveWorker = function () { _sync(); var pr = _semis(false), sig = _sig(pr) ^ 0x5a5a; var K = env.uMat / UPL; L3 = 300 * K; LH = 650 * K; var ct = env.cleToile;
    var B0 = _volBuild({ pr: pr, g: (ct == null ? 1 : ct) >>> 0 }); var w = _worker(); if (!w) return Promise.resolve({ worker: false });
    return new Promise(function (res) { var id = ++_WN; _WA[id] = { sig: sig, pr: pr, K: K, ct: ct, t0: performance.now(), preuve: res, B0: B0 };
      var of = _W.onmessage; _W.onmessage = function (e) { if (e.data.id !== id) return of.call(this, e); _W.onmessage = of; delete _WA[id];
        function net(B) { return JSON.stringify({ fl: B.fl.map(function (f) { return [f.x, f.y, f.R, f.pts, f.dots]; }), st: B.stems.map(function (s) { return s.pts; }), lv: B.leaves, pe: B.pets, de: B.deco, M: B.M, sw: B.sw }); }
        res({ worker: true, identique: net(e.data.B) === net(B0), octets: net(B0).length }); };
      w.postMessage({ id: id, W: W, H: H, L3: 300 * K, LH: 650 * K, S: { pr: pr.map(function (p) { return { h: p.h, x: p.x, y: p.y, s: { __t: window._tailleApercu(p.s) } }; }), g: (ct == null ? 1 : ct) >>> 0 } }); }); };
  window._volPreuve = Rvol._preuveWorker;
  /* v75 — préparer d'avance (au Studio) : le jardin de repos (1) et celui de l'arrivée (2), demandés au Worker ; vrai quand il est là */
  /* ⚑ v92 — pendant une plantation simulée (`Toile.simule`) : le jardin d'arrivée part au Worker, sous la signature qu'aura la Toile.
     Les places gardées ne retiennent RIEN de la simulation (la fleur prédite ne doit pas épingler la vraie). */
  Rvol.prepareToile = function () { _sync(); var sv = _volGel ? { sem: _volGel.sem, pos: Object.assign({}, _volGel.pos) } : null;
    try { _jardinFond(_semis(true)); return true; } finally { _volGel = sv; } };
  Rvol.prepare = function (now, budget, quoi) { _sync(); var pr = (quoi === 2) ? _semis(true) : _semis(false); return !!_jardinFond(pr); };
  Rvol.transDur = 1600; Rvol.douce = true; Rvol.partDur = 900; Rvol.toucheStrict = true;
  return { volubilis: Rvol, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerVolubilis = creerVolubilis;
})();

/* ══════════════════ bloc « lot-V65-GUINGOIS » ══════════════════ */
/* ⚑ v65 (27 sept. 2026) — GUINGOIS, le quadrillage sur l'étoffe froissée. Porté de `froisseBuild` et `froisse` (planche « Trois
   matières ») au CONTRAT-MONDE, sur le patron des trois précédents :
   · longueurs : le pas de la grille, les reliefs, les zones, les cassures de fond en unité de matière (L3 = 300·K) ; les plis des
     promesses en u = avg() (leur « place » R, comme la planche) ; POSITIONS de la Toile inchangées ;
   · LCG : l'étoffe (houles, zones, bosses, cassures) sur la clé de la Toile, chaque pli sur la clé de sa promesse ; L'ASYMÉTRIE D'UNE
     ARÊTE vient de sa clé, plus de sa position (PORTAGE n° 2) ;
   · la dalle : les cases au cœur du pli, d'une seule couleur (cOf) ; la grille : l'encre du produit (`_tfInk`) ; rien n'est peint en
     papier (le fond est celui du moteur) ;
   · ⚑ AUCUNE PROMESSE SANS DALLE (PORTAGE n° 7 ; la planche en laissait 14 sur 120 à 40 promesses) : une promesse restée sans case
     reprend, autour du centre de son pli, les cases où elle est la plus forte, seuils abaissés, sans toucher une autre dalle ;
   · deux adaptations sans effet sur le dessin : le centre déformé d'un pli se calcule une fois (la planche le refaisait pour chaque
     case) ; une ligne de la grille se trace d'un trait (la planche traçait chaque segment à part, bouts ronds : la même ligne) ;
   · transition : les plis glissent de leur place à la place d'arrivée (`env.finale`), celui qui arrive se creuse peu à peu, celui qui
     part s'efface — l'étoffe se déforme continûment ; au repos la disposition d'arrivée reste (§15.14) ; tout rendu de CETTE Toile
     lit ce qu'on voit.
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerGuingois(env) {
  var g, W, H, seeds, cOf, avg;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; avg = env.avg; }
  var TAU = 6.283185307179586, UPL = 53.55, ARR = 900, RET = 760, MOVE = 1200;
  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) return k >>> 0; }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  function _arr(c) { if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; } return c; }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _encre() { return _arr(typeof env.encre === 'function' ? env.encre() : env.encre); }
  function _fin() { try { return env.finale || null; } catch (_) { return null; } }
  function _pip(x, y, pts) { var ins = false, n = pts.length;
    for (var i = 0, j = n - 1; i < n; j = i++) { var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins; }
    return ins; }

  /* --- l'étoffe d'une Toile : pas, houles, zones froissées, bosses, cassures de fond — tirés de la clé de la Toile --- */
  var _etoffes = {};
  function _etoffe(K) {
    var ct = env.cleToile, cle = Math.round(W) + 'x' + Math.round(H) + ':' + Math.round(K * 4096) + ':' + (ct == null ? 0 : ct);
    if (_etoffes[cle]) return _etoffes[cle];
    var L3 = 300 * K, R = _lcg(((ct == null ? 1 : ct) ^ 0xf201) >>> 0), c = L3 / (20 + Math.floor(R() * 4)), fond = [];
    for (var z = 0; z < 2 + Math.floor(R() * 2); z++) { var a = R() * 3.1416, s0 = L3 * (0.16 + 0.1 * R());
      fond.push({ p: null, x: W * (0.15 + 0.7 * R()), y: H * (0.1 + 0.8 * R()), s: s0, tx: Math.cos(a), ty: Math.sin(a), L: L3 * (0.5 + 0.4 * R()), sg: s0 * 0.4, k: 0.78 + 0.15 * R(), sl: (R() - 0.5) * 1.3, bend: (R() - 0.5) * 0.8 / s0 }); }
    var ph = [R() * 6.28, R() * 6.28, R() * 6.28, R() * 6.28, R() * 6.28, R() * 6.28];
    var zones = []; for (z = 0; z < 1 + (R() < 0.6 ? 1 : 0); z++) zones.push({ x: W * (0.2 + 0.6 * R()), y: H * (0.2 + 0.6 * R()), r: L3 * (0.38 + 0.2 * R()) });
    function inZone() { var zn = zones[Math.floor(R() * zones.length)], a2 = R() * TAU, d = zn.r * Math.sqrt(R()) * 0.8; return [zn.x + Math.cos(a2) * d, zn.y + Math.sin(a2) * d]; }
    var bumps = [];
    [[2, 0.35, 0.55, 0.12, 0.2, false], [6, 0.12, 0.22, 0.24, 0.42, true], [5, 0.07, 0.12, 0.2, 0.34, true]].forEach(function (B) {
      for (var z2 = 0; z2 < B[0] + Math.floor(R() * 2); z2++) { var an = R() * 3.1416, el = 0.45 + 0.55 * R(), P = B[5] ? inZone() : [R() * W, R() * H];
        bumps.push({ x: P[0], y: P[1], s: L3 * (B[1] + (B[2] - B[1]) * R()), el: el, ca: Math.cos(an), sa: Math.sin(an), a: (R() < 0.5 ? 1 : -1) * (B[3] + (B[4] - B[3]) * R()) }); } });
    // les cassures de fond naissent dans les zones froissées ; leur asymétrie est tirée (la planche la lisait dans leur position)
    fond.forEach(function (n) { var P = inZone(); n.x = P[0]; n.y = P[1]; n.asy = 0.55 + 0.9 * R(); n.sharp = n.asy > 1.05; });
    var E = { c: c, ph: ph, zones: zones, bumps: bumps, fond: fond, K: K };
    var ks = Object.keys(_etoffes); if (ks.length > 3) delete _etoffes[ks[0]];
    return (_etoffes[cle] = E);
  }
  // le pli d'une promesse : tiré de SA clé (la planche : rng(p.h ^ 0xfe0)), sa place R en u = avg()
  var _par = {};
  function _param(k) { var P = _par[k]; if (P) return P; var q = _lcg(k ^ 0xfe0), a = q() * 3.1416;
    P = { tx: Math.cos(a), ty: Math.sin(a), s: 0.9 + 0.4 * q(), L: 1.4 + 1.0 * q(), sg: 0.35 + 0.2 * q(), k: 0.72 + 0.22 * q(), sl: (q() - 0.5) * 1.4, bend: (q() - 0.5) * 0.9 };
    P.asy = 0.55 + 0.9 * q(); P.sharp = P.asy > 1.05; P.z = _lcg(k ^ 0x5eed)();
    return (_par[k] = P); }
  // les plis posés : place, force (f : 0 → 1 à l'arrivée, 1 → 0 au départ) — et l'étoffe qui en découle
  function _plis(E, L, u, TRv) {
    var knots = [];
    /* ⚑ v89 (Tom : « les volumes, les plis et les froissements évoluent, pas seulement les couleurs ») — PENDANT UNE TRANSITION
       L'ÉTOFFE SE FROISSE. Une enveloppe b = sin(π·a), nulle au début et à la fin (au repos, rien ne change, aucun saut) : le pli qui
       arrive ou part se creuse au-delà de sa profondeur (×1,9 au milieu), ses voisins se creusent un peu, et trois froissements
       passagers naissent autour du lieu de l'événement puis s'effacent. Ils ne prennent aucune case (f = 0) : de l'étoffe, pas une dalle. */
    var bT = TRv ? TRv.b : 0;
    L.forEach(function (e) { var P = _param(e.k), R = u * (0.36 + 0.2 * P.z + 0.26 * P.z * P.z * P.z) * window._tailleApercu(e.s), f = e.f;
      var zin = Math.max.apply(null, E.zones.map(function (zn) { return Math.exp(-(((e.x - zn.x) * (e.x - zn.x) + (e.y - zn.y) * (e.y - zn.y)) / (zn.r * zn.r))); }));
      var mul = 1; if (bT > 0) { if (f < 0.999) mul = 1 + 0.9 * bT; else { var dd = (e.x - TRv.x) * (e.x - TRv.x) + (e.y - TRv.y) * (e.y - TRv.y), r3 = 3 * u; mul = 1 + 0.6 * bT * Math.exp(-dd / (r3 * r3)); } }
      knots.push({ p: e, s: e.s, k0: e.k, x: e.x, y: e.y, R: R, f: f, sc: R * P.s * Math.max(f, 1e-3), tx: P.tx, ty: P.ty, L: R * P.L, sg: R * P.sg,
        k: (0.45 + 0.45 * zin) * f * mul, sl: P.sl * (0.6 + 0.8 * zin) * f * mul, bend: P.bend / R, asy: P.asy, sharp: P.sharp }); });
    if (bT > 0.001) { var qT = _lcg((TRv.n * 2654435761) >>> 0);
      for (var zT = 0; zT < 3; zT++) { var aT = qT() * TAU, dT = u * (0.7 + 0.9 * qT()), oT = qT() * 3.1416, RT = u * (0.5 + 0.3 * qT());
        knots.push({ p: null, s: null, k0: -1 - zT, x: TRv.x + Math.cos(aT) * dT, y: TRv.y + Math.sin(aT) * dT, R: RT, f: 0, sc: 1e-3, tx: Math.cos(oT), ty: Math.sin(oT), L: RT * (1.2 + 0.6 * qT()), sg: RT * (0.3 + 0.15 * qT()),
          k: 0.55 * bT, sl: (qT() - 0.5) * 1.2 * bT, bend: (qT() - 0.5) * 0.8 / RT, asy: 0.55 + 0.9 * qT(), sharp: qT() > 0.5 }); } }
    var all = knots.concat(E.fond), bumps = E.bumps, ph = E.ph, k0 = E.K, PV = window._v72Preuve;   // PV : la sonde de preuve, lue une fois (jamais dans la boucle)
    /* ⚑ v72 (budget) — CHAQUE PLI ET CHAQUE BOSSE À SA PORTÉE. Au-delà de 3,6 fois sa longueur ou sa largeur, un pli pèse exp(−13) ≈ 2·10⁻⁶
       de son amplitude (moins d'un cent-millième de pixel), une bosse au-delà de qq = 4 pèse exp(−16) : on les saute.
       ⚑ ET LA PART FIXE DE L'ÉTOFFE SE CALCULE UNE FOIS. Les ondes de fond, les bosses et les cassures de fond ne dépendent pas des
       paroles : pour un point donné, elles valent la même chose à chaque image, à chaque plantation. On les garde par étoffe (`_fixe`) ;
       seuls les plis des paroles se recalculent. Les termes s'additionnent dans le MÊME ordre qu'avant (fond, bosses, plis, cassures). */
    all.forEach(function (n) { n._pL = 3.6 * n.L; n._pS = 3.6 * n.sg * Math.max(n.asy, 1 / n.asy); });
    bumps.forEach(function (b) { b._p2 = 4 * b.s * b.s; });
    var nf = E.fond.length, NR = 5 + 3 * nf;
    function _terme(n, x, y, o) {   // un pli en (x, y) : [dcx, dcy, dcont], ou rien
      if (!(n.k > 0) && !n.sl) return false;
      var dx2 = x - n.x, dy2 = y - n.y, l = dx2 * n.tx + dy2 * n.ty; if (l > n._pL || l < -n._pL) return false; var s = -dx2 * n.ty + dy2 * n.tx;
      s -= n.bend * l * l; if (s > n._pS || s < -n._pS) return false;
      var sgS = s > 0 ? n.sg * n.asy : n.sg / n.asy, wl = Math.exp(-((l / n.L) * (l / n.L))), sx = s / (n.sharp ? sgS * 0.6 : sgS), es = Math.exp(-(sx * sx));
      var dn = -n.k * s * es * wl, dt = n.sl * 0.7 * n.sg * es * wl;
      o[0] = -n.ty * dn + n.tx * dt; o[1] = n.tx * dn + n.ty * dt; o[2] = n.k * es * wl + Math.abs(n.sl) * 0.35 * es * wl; return true; }
    var _t3 = [0, 0, 0];
    function _fixe(x, y, R, o) {   // la part fixe en (x, y), écrite dans R à partir de o
      var X = x + k0 * (10 * Math.sin(y / (85 * k0) + ph[0]) + 4 * Math.sin((x + y) / (48 * k0) + ph[1]) + 3 * Math.sin(y / (31 * k0) + ph[4]));
      var Y = y + k0 * (10 * Math.sin(x / (95 * k0) + ph[2]) + 4 * Math.sin((x - y) / (55 * k0) + ph[3]) + 3 * Math.sin(x / (29 * k0) + ph[5]));
      var cx = 0, cy = 0, cont = 0, i;
      for (i = 0; i < bumps.length; i++) { var b = bumps[i], dx = x - b.x, dy = y - b.y, u1 = dx * b.ca + dy * b.sa, v1 = (-dx * b.sa + dy * b.ca) / b.el, q0 = u1 * u1 + v1 * v1; if (q0 > b._p2) continue; var qq = q0 / (b.s * b.s), e = Math.exp(-qq * qq);
        if (b.a > 0) { X += dx * b.a * e; Y += dy * b.a * e; } else { cx += dx * b.a * e; cy += dy * b.a * e; cont += -b.a * e; } }
      R[o] = X; R[o + 1] = Y; R[o + 2] = cx; R[o + 3] = cy; R[o + 4] = cont;
      for (i = 0; i < nf; i++) { var q = o + 5 + 3 * i; if (_terme(E.fond[i], x, y, _t3)) { R[q] = _t3[0]; R[q + 1] = _t3[1]; R[q + 2] = _t3[2]; } else { R[q] = 0; R[q + 1] = 0; R[q + 2] = 0; } } }
    function _dyn(x, y, R, o) {   // la part des paroles, puis les cassures de fond, dans l'ordre d'origine
      var X = R[o], Y = R[o + 1], cx = R[o + 2], cy = R[o + 3], cont = R[o + 4], i;
      for (i = 0; i < knots.length; i++) if (_terme(knots[i], x, y, _t3)) { cx += _t3[0]; cy += _t3[1]; cont += _t3[2]; }
      for (i = 0; i < nf; i++) { var q = o + 5 + 3 * i; if (R[q] !== 0 || R[q + 1] !== 0 || R[q + 2] !== 0) { cx += R[q]; cy += R[q + 1]; cont += R[q + 2]; } }
      var sc = cont > 0.86 ? 0.86 / cont : 1;
      var out = [X + cx * sc, Y + cy * sc];
      if (PV) { var an = _warpAncien(x, y), dd = Math.max(Math.abs(an[0] - out[0]), Math.abs(an[1] - out[1])), P = PV; P.gui = Math.max(P.gui || 0, dd); P.guiN = (P.guiN || 0) + 1; }
      if (PV && PV.ancien) return _warpAncien(x, y);
      return out; }
    function _warpAncien(x, y) {   // v72 : la déformation d'origine, sans portée ni part fixe (preuve seulement)
      var X = x + k0 * (10 * Math.sin(y / (85 * k0) + ph[0]) + 4 * Math.sin((x + y) / (48 * k0) + ph[1]) + 3 * Math.sin(y / (31 * k0) + ph[4]));
      var Y = y + k0 * (10 * Math.sin(x / (95 * k0) + ph[2]) + 4 * Math.sin((x - y) / (55 * k0) + ph[3]) + 3 * Math.sin(x / (29 * k0) + ph[5]));
      var cx = 0, cy = 0, cont = 0, i, n;
      for (i = 0; i < bumps.length; i++) { var b = bumps[i], dx = x - b.x, dy = y - b.y, u1 = dx * b.ca + dy * b.sa, v1 = (-dx * b.sa + dy * b.ca) / b.el, qq = (u1 * u1 + v1 * v1) / (b.s * b.s), e = Math.exp(-qq * qq);
        if (b.a > 0) { X += dx * b.a * e; Y += dy * b.a * e; } else { cx += dx * b.a * e; cy += dy * b.a * e; cont += -b.a * e; } }
      for (i = 0; i < all.length; i++) { n = all[i]; if (!(n.k > 0) && !n.sl) continue;
        var dx2 = x - n.x, dy2 = y - n.y, l = dx2 * n.tx + dy2 * n.ty, s = -dx2 * n.ty + dy2 * n.tx;
        s -= n.bend * l * l;
        var sgS = s > 0 ? n.sg * n.asy : n.sg / n.asy, wl = Math.exp(-((l / n.L) * (l / n.L))), sx = s / (n.sharp ? sgS * 0.6 : sgS), es = Math.exp(-(sx * sx));
        var dn = -n.k * s * es * wl, dt = n.sl * 0.7 * n.sg * es * wl;
        cx += -n.ty * dn + n.tx * dt; cy += n.tx * dn + n.ty * dt; cont += n.k * es * wl + Math.abs(n.sl) * 0.35 * es * wl; }
      var sc = cont > 0.86 ? 0.86 / cont : 1;
      return [X + cx * sc, Y + cy * sc]; }
    var M = E._fm || (E._fm = new Map()), R1 = new Float64Array(NR);
    function warp(x, y) { var m = M.get(x); if (!m) { m = new Map(); M.set(x, m); } var r = m.get(y); if (!r) { r = new Float64Array(NR); _fixe(x, y, r, 0); m.set(y, r); } return _dyn(x, y, r, 0); }
    function warpLibre(x, y) { _fixe(x, y, R1, 0); return _dyn(x, y, R1, 0); }   // un point qu'on ne reverra pas (le centre d'un pli)
    return { knots: knots, warp: warp, warpLibre: warpLibre, fixe: _fixe, dyn: _dyn, NR: NR };
  }
  // les cases : chacune au pli le plus fort, au cœur de ce pli ; jamais voisine d'une autre dalle ; d'un seul tenant — et aucune promesse sans case
  function _cases(E, PL) {
    var c = E.c, warp = PL.warp, i0 = -3, i1 = Math.ceil(W / c) + 3, j0 = -3, j1 = Math.ceil(H / c) + 3, own = {}, fort = {}, i, j, key;
    var KN = PL.knots.filter(function (n) { return n.f > 0.001; });
    KN.forEach(function (n) { var w = PL.warpLibre(n.x, n.y); n.wx = w[0]; n.wy = w[1]; });   // une fois par pli (la planche : une fois par case)
    for (i = i0; i < i1; i++) for (j = j0; j < j1; j++) {
      var C = warp((i + 0.5) * c, (j + 0.5) * c), bn = null, bw = 0, sw2 = 0;
      for (var m = 0; m < KN.length; m++) { var n = KN[m], r2 = ((C[0] - n.wx) * (C[0] - n.wx) + (C[1] - n.wy) * (C[1] - n.wy)) / (n.sc * n.sc * 0.45), w = Math.exp(-r2);
        if (w > bw) { sw2 = bw; bw = w; bn = n; } else if (w > sw2) sw2 = w; }
      key = i + ',' + j; fort[key] = [bn, bw, sw2, C];
      if (bn && bw > 0.42 && bw - sw2 > 0.15) own[key] = bn;
    }
    var V8 = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]], V4 = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    function libre(ii, jj, n, O) { return !V8.some(function (d) { var o = O[(ii + d[0]) + ',' + (jj + d[1])]; return o && o !== n; }); }
    var cells = [];
    for (key in own) { var ij = key.split(',').map(Number); if (libre(ij[0], ij[1], own[key], own)) cells.push({ i: ij[0], j: ij[1], n: own[key] }); }
    var keep = {}; cells.forEach(function (ce) { keep[ce.i + ',' + ce.j + ',' + ce.n.k0] = 1; });
    cells = cells.filter(function (ce) { return V4.some(function (d) { return keep[(ce.i + d[0]) + ',' + (ce.j + d[1]) + ',' + ce.n.k0]; }); });
    /* « Toujours d'un seul tenant » (NUANCES, Guingois) : la planche ne retirait que les cases ISOLÉES ; une dalle pouvait garder deux
       morceaux. Chaque dalle garde son plus grand morceau d'un seul tenant (voisinage par les côtés). */
    (function () { var par = {}; cells.forEach(function (ce) { (par[ce.n.k0] || (par[ce.n.k0] = [])).push(ce); }); var garde = [];
      for (var kd in par) { var L = par[kd], ix = {}, vu = {}, best = []; L.forEach(function (ce) { ix[ce.i + ',' + ce.j] = ce; });
        L.forEach(function (ce) { var k0 = ce.i + ',' + ce.j; if (vu[k0]) return; var comp = [], pile = [ce]; vu[k0] = 1;
          while (pile.length) { var q = pile.pop(); comp.push(q); V4.forEach(function (d) { var kk = (q.i + d[0]) + ',' + (q.j + d[1]); if (ix[kk] && !vu[kk]) { vu[kk] = 1; pile.push(ix[kk]); } }); }
          if (comp.length > best.length) best = comp; });
        garde = garde.concat(best); }
      cells = garde; })();
    // ⚑ PORTAGE n° 7 — une promesse restée sans case reprend, autour du centre de son pli, les cases où elle est la plus forte
    var aDes = {}; cells.forEach(function (ce) { aDes[ce.n.k0] = 1; });
    KN.forEach(function (n) {
      if (aDes[n.k0] || n.f < 0.999) return;
      var O = {}; cells.forEach(function (ce) { O[ce.i + ',' + ce.j] = ce.n; });
      var bi = null, bd = 1e18; for (var k2 in fort) { var F2 = fort[k2]; if (F2[0] !== n) continue; var d = Math.hypot(F2[3][0] - n.wx, F2[3][1] - n.wy); if (d < bd) { bd = d; bi = k2; } }
      if (!bi) { for (var k3 in fort) { var F3 = fort[k3], d3 = Math.hypot(F3[3][0] - n.wx, F3[3][1] - n.wy); if (d3 < bd) { bd = d3; bi = k3; } } }
      if (!bi) return;
      var file = [bi], vu = {}, pris = [];
      vu[bi] = 1;
      while (file.length && pris.length < 6) { var k4 = file.shift(), p4 = k4.split(',').map(Number);
        if (!O[k4] && libre(p4[0], p4[1], n, O)) { pris.push(p4); O[k4] = n; }
        V4.forEach(function (d) { var kk = (p4[0] + d[0]) + ',' + (p4[1] + d[1]), F4 = fort[kk]; if (vu[kk] || !F4) return; vu[kk] = 1; if (F4[0] === n || pris.length === 0) file.push(kk); }); }
      pris.forEach(function (p4) { cells.push({ i: p4[0], j: p4[1], n: n, repris: true }); });
      if (pris.length) window._guiRepris = (window._guiRepris || 0) + 1;   // publié : combien de promesses la reprise a sauvées
    });
    return cells;
  }
  // tracés : les cases de chaque dalle, le contour de chaque case (dalle seule), les lignes de la grille (une ligne = un trait)
  function _quad(E, warp, i, j, rapide) { var c = E.c, pts = [], n = rapide ? 5 : 10, k;   // v72 : 5 points par côté pendant une transition (une case fait ~14 px : l'étoffe y est presque plane)
    for (k = 0; k < n; k++) pts.push(warp((i + k / n) * c, j * c)); for (k = 0; k < n; k++) pts.push(warp((i + 1) * c, (j + k / n) * c));
    for (k = 0; k < n; k++) pts.push(warp((i + 1 - k / n) * c, (j + 1) * c)); for (k = 0; k < n; k++) pts.push(warp(i * c, (j + 1 - k / n) * c)); return pts; }
  function _poly(T, pts) { T.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) T.lineTo(pts[i][0], pts[i][1]); T.closePath(); }
  // v72 : un tracé qu'on REMPLIT seulement se ferme de lui-même (le remplissage ferme chaque sous-tracé) — même surface, sans closePath
  function _polyR(T, pts) { T.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) T.lineTo(pts[i][0], pts[i][1]); }
  /* ⚑ v72 (budget) — deux cases voisines partagent un côté, et le bord d'une dalle repasse par les mêmes points : chaque point du
     quadrillage se déforme UNE fois (mémo, même valeur rendue). Le bord d'une dalle se calcule à la demande (le toucher, la dalle
     seule) — pendant une transition, personne ne le lit. Et pendant une transition SEULEMENT, une ligne de la grille s'échantillonne
     tous les c/4,5 au lieu de c/9 : ses courbes ont un rayon d'au moins ~30 px, l'écart d'une corde de 3 px à l'arc est sous 0,04 px ;
     au repos, l'échantillonnage d'origine. */
  function _construit(E, PL, rapide) {
    var c = E.c, warp0 = PL.warp, lw = c * 0.11, cells = _cases(E, PL), parDalle = {}, memo = new Map();
    function warpM(x, y) { var m = memo.get(x); if (!m) { m = new Map(); memo.set(x, m); } var r = m.get(y); if (!r) { r = warp0(x, y); m.set(y, r); } return r; }
    var warp = warp0;
    cells.forEach(function (ce) { var pts = _quad(E, warpM, ce.i, ce.j, rapide), d = parDalle[ce.n.k0] || (parDalle[ce.n.k0] = { n: ce.n, s: ce.n.s, k: ce.n.k0, T: new Path2D(), quads: [], ij: [], x0: 1e18, y0: 1e18, x1: -1e18, y1: -1e18 });
      _polyR(d.T, pts); d.quads.push(pts); d.ij.push([ce.i, ce.j]); pts.forEach(function (v) { if (v[0] < d.x0) d.x0 = v[0]; if (v[0] > d.x1) d.x1 = v[0]; if (v[1] < d.y0) d.y0 = v[1]; if (v[1] > d.y1) d.y1 = v[1]; }); });
    var i0 = -3, i1 = Math.ceil(W / c) + 3, j0 = -3, j1 = Math.ceil(H / c) + 3, st = rapide ? c / 4.5 : c / 9, lignes = [];
    function wob(k, a) { return c * 0.035 * (Math.sin(a / (c * 3.1) + k * 1.7) + 0.4 * Math.sin(a / (c * 1.6) + k * 3.1)); }
    var LG = (E._lg || (E._lg = {}))[st] || (E._lg[st] = []), nl = 0, NR = PL.NR;
    function ligne(xy, a0, a1, base) { var Lg = LG[nl++];
      if (!Lg) { var xs = [], ys = [], a = a0, p = xy(a); xs.push(p[0]); ys.push(p[1]); for (a = a0 + st; a <= a1 + 1e-6; a += st) { p = xy(a); xs.push(p[0]); ys.push(p[1]); }
        Lg = LG[nl - 1] = { x: xs, y: ys, R: new Float64Array(xs.length * NR) }; for (var z = 0; z < xs.length; z++) PL.fixe(xs[z], ys[z], Lg.R, z * NR); }
      var T = new Path2D(), n = Lg.x.length, q; q = PL.dyn(Lg.x[0], Lg.y[0], Lg.R, 0); T.moveTo(q[0], q[1]);
      for (var k = 1; k < n; k++) { q = PL.dyn(Lg.x[k], Lg.y[k], Lg.R, k * NR); T.lineTo(q[0], q[1]); } lignes.push([T, base]); }
    for (var i = i0; i <= i1; i++) (function (ii) { ligne(function (a) { return [ii * c + wob(ii, a), a]; }, j0 * c, j1 * c, lw * (0.85 + 0.3 * ((ii * 7919 >>> 0) % 13) / 13)); })(i);
    for (var j = j0; j <= j1; j++) (function (jj) { ligne(function (a) { return [a, jj * c + wob(jj + 50, a)]; }, i0 * c, i1 * c, lw * (0.85 + 0.3 * ((jj * 104729 >>> 0) % 13) / 13)); })(j);
    // (le quadrillage d'une dalle seule, `contour`, se trace à la demande : seule la dalle seule le lit)
    for (var k2 in parDalle) (function (d) { d._bordF = function () { return _bord(E, warpM, d.ij); }; })(parDalle[k2]);
    return { dalles: parDalle, lignes: lignes, lw: lw };
  }

  /* --- ce qu'on voit : l'étoffe au repos, ou les plis qui glissent pendant une transition --- */
  var _tr = null, _aff = null, _fige = null, _cache = {}, _nCa = [], _CR = window._calqueRepos ? window._calqueRepos() : null;
  function _liste(fin, now) { var F = fin ? (_fin() || new Map()) : _fin(), L = [], i, s, perte = 0;
    for (i = 0; i < seeds.length; i++) { s = seeds[i]; if (s.kind === 'gray') continue; if (fin && s.part != null) continue;
      var f = fin ? 1 : (s.part != null ? 1 - _lisse((now - s.part) / RET) : 1); perte += 1 - f;
      var q = F ? F.get(s) : null; L.push({ s: s, k: _cle(s), x: q ? q[0] : s.x, y: q ? q[1] : s.y, f: f }); }
    L.sort(function (a, b) { return a.k - b.k; });
    return { L: L, u: avg() * Math.sqrt(Math.max(1, seeds.length) / Math.max(1, (fin ? L.length : seeds.length - perte))) }; }
  function _memesCles(M) { var n = 0, i, s; for (i = 0; i < seeds.length; i++) { s = seeds[i]; if (s.kind === 'gray' || s.part != null) continue; n++; if (!M.parCle[_cle(s)]) return false; } return n === M.L.length; }
  function _etat(L, u, E) { var M = { L: L, u: u, W: W, H: H, ct: env.cleToile, parCle: {} }; L.forEach(function (e) { M.parCle[e.k] = e; }); return M; }
  function _scene(now) {
    var K = env.uMat / UPL, E = _etoffe(K), TR = env.vive ? env.trans : null, M, L, u, a = 1;
    if (TR || (_tr && !_tr.fini && env.vive)) {
      if (TR && (!_tr || _tr.n !== TR.n)) _tr = { n: TR.n, M0: _aff, M1: null, t: TR.t0, fini: false };
      if (!_tr.M1) { var A = _liste(true, now); _tr.M1 = _etat(A.L, A.u, E); }
      a = _lisse((now - _tr.t) / MOVE); var M0 = _tr.M0, M1 = _tr.M1, k;
      if (a >= 1) { _tr.fini = true; _fige = M1; } else window._mondeEncore = true;
      L = [];
      for (k in M1.parCle) { var e1 = M1.parCle[k], e0 = M0 && M0.parCle[k];
        L.push(e0 ? { s: e1.s, k: e1.k, x: e0.x + (e1.x - e0.x) * a, y: e0.y + (e1.y - e0.y) * a, f: 1 } : { s: e1.s, k: e1.k, x: e1.x, y: e1.y, f: a }); }
      if (M0) for (k in M0.parCle) if (!M1.parCle[k]) { var d0 = M0.parCle[k]; L.push({ s: d0.s, k: d0.k, x: d0.x, y: d0.y, f: 1 - a }); }
      L.sort(function (x, y) { return x.k - y.k; });
      u = M0 ? M0.u + (M1.u - M0.u) * a : M1.u; M = _etat(L, u, E);
      var ox = TR && TR.x != null ? TR.x : null, oy = TR && TR.y != null ? TR.y : null;
      if (ox == null) { for (k in M1.parCle) if (!(M0 && M0.parCle[k])) { ox = M1.parCle[k].x; oy = M1.parCle[k].y; break; } }
      if (ox == null && M0) { for (k in M0.parCle) if (!M1.parCle[k]) { ox = M0.parCle[k].x; oy = M0.parCle[k].y; break; } }
      if (ox != null && a < 1) M.tr = { x: ox, y: oy, b: Math.sin(Math.PI * a), n: _tr.n };
      if (a >= 1) _aff = M1;
      return _peinture(E, M, false);
    }
    if (env.vive && _fige && _memesCles(_fige)) M = _fige;
    else if (!env.vive && !window._v72Preuve && _aff && _aff.W === W && _aff.H === H && _aff.ct === env.cleToile && _memesCles(_aff)) M = _aff;   // CETTE Toile : ce qu'on voit
    else { var B = _liste(false, now); M = _etat(B.L, B.u, E); if (env.vive) _fige = M; }
    if (env.vive) _aff = M;
    return _peinture(E, M, true);
  }
  function _peinture(E, M, garder) {
    var h = 2166136261; function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(E.K * 4096)); mix(Math.round(M.u * 16)); mix(env.cleToile == null ? 0 : env.cleToile);
    M.L.forEach(function (e) { mix(e.k); mix(Math.round(e.x * 2)); mix(Math.round(e.y * 2)); mix(Math.round(e.f * 512)); });
    if (M.tr) mix(Math.round(M.tr.b * 512) + 7);
    if (_cache[h] && !window._v72Preuve) return _cache[h];
    var t0 = performance.now(), PL = _plis(E, M.L, M.u, M.tr), P = _construit(E, PL, !garder); P.ms = performance.now() - t0; P.h = h;
    if (garder) { _cache[h] = P; _nCa.push(h); if (_nCa.length > 6) delete _cache[_nCa.shift()]; window._guiConstruit = { ms: Math.round(P.ms), dalles: Object.keys(P.dalles).length }; }   // v72 : par ordre d'entrée (Object.keys range les clés entières par valeur)
    return P;
  }

  var _dernier = null;
  function Rgui(now, x0, y0, x1, y1) {
    _sync();
    var P = _scene(now), k, ink = _rgb(_encre()), cols = [];
    for (k in P.dalles) cols.push(_rgb(cOf(P.dalles[k].s, now)));
    function peint(G) { var i = 0; for (k in P.dalles) { G.fillStyle = cols[i++]; G.fill(P.dalles[k].T); }   // la dalle : ses cases teintes
      G.strokeStyle = ink; G.lineCap = 'round'; G.lineJoin = 'round';
      for (var j = 0; j < P.lignes.length; j++) { G.lineWidth = P.lignes[j][1]; G.stroke(P.lignes[j][0]); } }   // épaisseur constante : l'ombre naît du rapprochement
    // v72 : au repos, le calque (la signature : la géométrie, les couleurs, l'encre)
    if (!(env.vive && !env.trans && _CR && _CR.pose(g, P.h + '#' + ink + '#' + cols.join(','), peint))) peint(g);
    _dernier = P; window._guiComp = { dalles: Object.keys(P.dalles).length };
  }

  function _trouve(s, P) { P = P || _scene(performance.now()); var k = _cle(s); for (var kk in P.dalles) { var d = P.dalles[kk]; if (d.s === s || d.k === k) return d; } return null; }
  function seule(nom, s, now, cx, cy, taille) {
    _sync(); var P = _scene(now), d = _trouve(s, P); if (!d) return false;
    var e = P.lw, sc = taille / Math.max(d.x1 - d.x0 + e, d.y1 - d.y0 + e, 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(d.x0 + d.x1) / 2, -(d.y0 + d.y1) / 2);
    g.fillStyle = _rgb(cOf(d.s, now)); g.fill(d.T);
    if (!d.contour) { d.contour = new Path2D(); d.quads.forEach(function (q) { _poly(d.contour, q); }); }
    g.strokeStyle = _rgb(_encre()); g.lineWidth = P.lw; g.lineJoin = 'round'; g.stroke(d.contour);   // son seul quadrillage
    g.restore(); return true;
  }
  /* le VRAI bord d'une dalle : les côtés de ses cases qu'aucune autre de ses cases ne partage, enchaînés en boucle, puis déformés
     comme l'étoffe (10 points par côté, comme une case) — la plus longue boucle est le bord extérieur */
  function _bord(E, warp, ij) {
    var c = E.c, cote = {}, i, a, b, k;
    function ajoute(x0, y0, x1, y1) { var inv = x1 + ',' + y1 + '>' + x0 + ',' + y0; if (cote[inv]) delete cote[inv]; else cote[x0 + ',' + y0 + '>' + x1 + ',' + y1] = [x0, y0, x1, y1]; }
    ij.forEach(function (p) { var x = p[0], y = p[1]; ajoute(x, y, x + 1, y); ajoute(x + 1, y, x + 1, y + 1); ajoute(x + 1, y + 1, x, y + 1); ajoute(x, y + 1, x, y); });
    var depuis = {}; for (k in cote) { var e = cote[k]; (depuis[e[0] + ',' + e[1]] || (depuis[e[0] + ',' + e[1]] = [])).push(e); }
    var boucles = [], pris = {};
    for (k in cote) { if (pris[k]) continue; var bcl = [], e0 = cote[k], cur = e0, garde = 0;
      while (cur && garde++ < 100000) { var kc = cur[0] + ',' + cur[1] + '>' + cur[2] + ',' + cur[3]; if (pris[kc]) break; pris[kc] = 1; bcl.push(cur);
        var suiv = (depuis[cur[2] + ',' + cur[3]] || []).filter(function (x) { return !pris[x[0] + ',' + x[1] + '>' + x[2] + ',' + x[3]]; }); cur = suiv[0]; }
      boucles.push(bcl); }
    boucles.sort(function (p, q) { return q.length - p.length; });
    var pts = []; (boucles[0] || []).forEach(function (e) { for (var s = 0; s < 10; s++) { var t = s / 10; pts.push(warp((e[0] + (e[2] - e[0]) * t) * c, (e[1] + (e[3] - e[1]) * t) * c)); } });
    return pts;
  }
  function _enveloppe(d) { var pts = []; d.quads.forEach(function (q) { pts = pts.concat(q); }); pts.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
    function cr(o, a, b) { return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]); }
    var lo = [], up = [], i; for (i = 0; i < pts.length; i++) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], pts[i]) <= 0) lo.pop(); lo.push(pts[i]); }
    for (i = pts.length - 1; i >= 0; i--) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], pts[i]) <= 0) up.pop(); up.push(pts[i]); }
    return lo.slice(0, -1).concat(up.slice(0, -1)); }
  function contour(nom, s) { _sync(); var d = _trouve(s); if (d && !d.bord && d._bordF) d.bord = d._bordF(); return d ? (d.bord && d.bord.length > 2 ? d.bord.slice() : _enveloppe(d)) : null; }
  function nature(nom, s) { _sync(); return _trouve(s) ? 'dalle' : null; }
  function boite(nom, s) { _sync(); var P = _scene(performance.now()), d = _trouve(s, P); if (!d) return null; var e = P.lw / 2 + 0.5;
    return { x0: d.x0 - e, y0: d.y0 - e, x1: d.x1 + e, y1: d.y1 + e, fx0: d.x0 - e, fy0: d.y0 - e, fx1: d.x1 + e, fy1: d.y1 + e }; }
  // le toucher : dans une case teinte de la dalle — jamais dans l'étoffe blanche
  function toucher(nom, x, y) {
    _sync(); var P = _dernier || _scene(performance.now());
    for (var k in P.dalles) { var d = P.dalles[k]; if (d.s.part != null || x < d.x0 || x > d.x1 || y < d.y0 || y > d.y1) continue;
      for (var i = 0; i < d.quads.length; i++) if (_pip(x, y, d.quads[i])) return d.s; }
    return null;
  }
  Rgui.ancre = function (s) { _sync(); var d = _trouve(s, _dernier); if (!d) return null; return [(d.x0 + d.x1) / 2, (d.y0 + d.y1) / 2, d.x1 - d.x0]; };
  Rgui._vu = window._guiVu = function () { return _dernier; };   // v72 : lecture seule (bancs)
  Rgui.transDur = 1600; Rgui.douce = true; Rgui.partDur = 900; Rgui.toucheStrict = true;
  return { guingois: Rgui, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerGuingois = creerGuingois;
})();

/* ══════════════════ bloc « lot-V66-CHANTOURNE » ══════════════════ */
/* ⚑ v66 (27 sept. 2026) — CHANTOURNÉ, la soie chinée. Porté de `chine()` (planche « Trois matières ») au CONTRAT-MONDE :
   · la chaîne : des fils verticaux (tw = L3/86), teints par écheveaux en flammes libres (lam = L3/5,2) — tirés de la clé de la Toile ;
     leurs trois tons sont ceux de la rampe TH du monde (la décision de Brouillamini : la matière dans les tons de la rampe) ;
   · la dalle : le médaillon au bord frangé fil à fil — cœur (la NUANCE de la couleur), champ (cOf), filet sombre, bordure (cOf),
     liseré (l'encre du produit, `_tfInk`) ; pas de liseré là où deux médaillons se touchent ; sa taille en u = avg() ;
   · l'échantillonnage le long d'un fil : un pas de K (la planche : 1 px sur une Toile de 300) ;
   · la dalle seule garde le cadrage de la planche (NUANCES : « un recadrage trop serré rendait les fils gros et flous ») ;
   · une accélération sans effet sur le dessin : un fil n'interroge que les médaillons à moins de 2 R (plus loin, un médaillon ne peut
     ni gagner le point ni changer le liseré — mesuré dans la formule : ee ≥ 1,42 > 1,0375 + 0,2) ;
   · la transition suit les graines, continûment (le médaillon neuf grandit, celui qui part se retire) : la soie ne se recompose pas.
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerChantourne(env) {
  var g, W, H, seeds, cOf, avg;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; avg = env.avg; }
  var UPL = 53.55, ARR = 900, RET = 760, THR = [0.3, 0.6, 0.76, 1.0];
  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) return k >>> 0; }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  function _fac(s, now) { if (s.part != null) return 1 - _lisse((now - s.part) / RET); if (env.trans && s.t0 != null) return _lisse((now - s.t0) / ARR); return 1; }
  function _arr(c) { if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; } return c; }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _lumR(c) { function l(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); } return 0.2126 * l(c[0]) + 0.7152 * l(c[1]) + 0.0722 * l(c[2]); }
  var NUANCE = 0.38;
  function _nuance(c) { var b = _lumR(c) > 0.3 ? 0 : 255; return [c[0] + (b - c[0]) * NUANCE, c[1] + (b - c[1]) * NUANCE, c[2] + (b - c[2]) * NUANCE]; }
  function _encre() { return _arr(typeof env.encre === 'function' ? env.encre() : env.encre); }

  /* --- la chaîne d'une Toile : chaque fil, son décalage, ses seuils, ses flammes — tirés de la clé de la Toile (planche : rng(S.g ^ 0x5eed)) --- */
  var _chaines = {};
  function _chaine(K) {
    var ct = env.cleToile == null ? 1 : env.cleToile, cle = Math.round(W) + 'x' + Math.round(H) + ':' + Math.round(K * 4096) + ':' + ct;
    if (_chaines[cle]) return _chaines[cle];
    var L3 = 300 * K, R = _lcg((ct ^ 0x5eed) >>> 0), tw = L3 / 86, lam = L3 / 5.2, fils = [];
    for (var c = -1; c * tw < W + tw; c++) {
      var x = c * tw + tw / 2, dOff = (R() - 0.5) * tw * 2.8, off = THR.map(function () { return (R() - 0.5) * 0.075; }); R();   // (le mOff de la planche : tiré, jamais lu)
      var bundle = Math.floor((c + 7) / 4.3), br = _lcg(((ct ^ 0xf1a) + bundle * 7919) >>> 0), segs = [];
      for (var y0 = -tw * 12; y0 < H + tw * 12;) { segs.push([y0 + (R() - 0.5) * tw * 0.6, Math.floor(br() * 3)]); y0 += lam * (0.06 + 0.55 * br() * br()); }
      fils.push({ c: c, x: x, dOff: dOff, off: off, segs: segs });
    }
    var ks = Object.keys(_chaines); if (ks.length > 3) delete _chaines[ks[0]];
    return (_chaines[cle] = { tw: tw, K: K, fils: fils });
  }
  // un médaillon : ce qu'il tire de SA clé (planche : rng(p.h), rng(p.h ^ 7), rng(p.h ^ 0x1ca7))
  var _par = {};
  function _param(k) { var P = _par[k]; if (P) return P; var q = _lcg(k ^ 0x1ca7);
    P = { ph: [_lcg(k)() * 6.28, _lcg(k ^ 7)() * 6.28], sz: 0.78 + 0.37 * q(), lz: 0.05 + 0.75 * q(), gap: q(), dt: [(q() - 0.5) * 0.08, (q() - 0.5) * 0.08, (q() - 0.5) * 0.05], z: _lcg(k ^ 0x5eed)() };
    return (_par[k] = P); }
  /* ⚑ v67 — AU REPOS, UNE POSITION RESTE GELÉE. Au-delà d'une trentaine de paroles, le moteur n'arrive jamais tout à fait au repos : ses
     graines oscillent d'une image à l'autre, sans fin (mesuré à 40 : 0,5 à 3 px, deux graines qui rebondissent) — la géométrie se
     refaisait à chaque image. Hors transition, une graine garde sa position tant qu'elle ne s'en éloigne pas de plus de 0,25 × l'unité
     de matière (un vrai ressemis la déplace bien plus) ; pendant une
     transition, les positions vivent (et le gel reprend exactement où elles finissent). */
  var _gel = {};
  function _geler(L) { var tol = (env.uMat || 70) * 0.25, vive = env.vive, tr = env.trans;
    L.forEach(function (e) { var k = e.k != null ? e.k : e.h, f = _gel[k];
      if (vive && tr) { _gel[k] = [e.x, e.y]; return; }
      if (f && Math.abs(e.x - f[0]) < tol && Math.abs(e.y - f[1]) < tol) { e.x = f[0]; e.y = f[1]; }
      else if (vive) _gel[k] = [e.x, e.y]; }); }
  function _medaillons(now) {
    var M = [], i, s, n = seeds.length, perte = 0;
    for (i = 0; i < n; i++) { s = seeds[i]; if (s.kind === 'gray') continue; var f = _fac(s, now); perte += 1 - f;
      M.push({ s: s, k: _cle(s), x: s.x, y: s.y, f: f }); }   // la position de REPOS (contrat §7.1 : le frémissement est facultatif)
    var u = avg() * Math.sqrt(Math.max(1, n) / Math.max(1, n - perte));
    _geler(M);
    M.forEach(function (m) { var P = _param(m.k), R = u * (0.36 + 0.2 * P.z + 0.26 * P.z * P.z * P.z) * window._tailleApercu(m.s); m.P = P; m.R = R;
      m.Rr = Math.min(R, u * 0.52) * P.sz * m.f; m.vide = m.Rr < 1e-3; });
    M.sort(function (a, b) { return a.k - b.k; });
    return { M: M, u: u };
  }
  /* --- le tissage : fil par fil, point par point (pas K), la couleur de chaque point ; des tronçons de même couleur, gardés --- */
  var _tissus = {};
  function _tisse(now) {
    var K = env.uMat / UPL, C = _chaine(K), A = _medaillons(now), M = A.M.filter(function (m) { return !m.vide; });
    var h = 2166136261; function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(K * 4096)); mix(env.cleToile == null ? 0 : env.cleToile);
    M.forEach(function (m) { mix(m.k); mix(Math.round(m.x * 2)); mix(Math.round(m.y * 2)); mix(Math.round(m.Rr * 8)); });
    var PV = window._v72Preuve, PVA = !!(PV && PV.ancien);   // la sonde de preuve, lue une fois
    if (_tissus[h] && !PV) return _tissus[h];
    var tw = C.tw, pas = K, runs = [];   // [x, y0, y1, code, médaillon] ; code : 0 cœur, 1 champ, 2 encre, 10+t matière
    C.fils.forEach(function (F) {
      /* v72 (budget) — et en y : ee ≥ 0,89 × |dy| / (1,25 R) (le bosselage ≥ 0,89, la plus petite des deux distances) ; au-delà de
         |y − y_m| ≥ 2,72 R (dy = 0,64 Δy), ee ≥ 1,2375 = 1,0375 + 0,2 : le médaillon ne peut ni gagner le point ni changer le liseré. */
      var x = F.x, near = M.filter(function (m) { m._ly = 2.72 * m.Rr; return Math.abs(x - m.x) < m.Rr * 2; }), fl = 0, run = null;
      function flush() { if (run) runs.push(run); run = null; }
      for (var y = -2 * K; y <= H + 2 * K; y += pas) {
        var yy = y + F.dOff, best = -1, e = 9, e2 = 9, ein = 9;
        for (var j = 0; j < near.length; j++) { var m = near[j]; if ((yy - m.y >= m._ly || m.y - yy >= m._ly) && !PVA) continue; var P = m.P, dx = x - m.x, dy = (yy - m.y) * 0.64;
          /* v72 (budget) : la même formule sans hypot, atan2 ni sinus — cos a = dx / r, sin a = dy / r, et sin(3a + φ), sin(5a + φ)
             par les polynômes de l'angle multiple (écart au bit près : 10⁻¹⁵) */
          var r0 = Math.sqrt(dx * dx + dy * dy), ca = r0 > 0 ? dx / r0 : 1, sa = r0 > 0 ? dy / r0 : 0, c2 = ca * ca, s2 = sa * sa;
          if (!P._cs) P._cs = [Math.cos(P.ph[0]), Math.sin(P.ph[0]), Math.cos(P.ph[1]), Math.sin(P.ph[1])];
          var dE = r0 / m.Rr, dD = (Math.abs(dx) + Math.abs(dy)) / (m.Rr * 1.25);
          var s3 = sa * (3 - 4 * s2), c3 = ca * (4 * c2 - 3), s5 = sa * (16 * s2 * s2 - 20 * s2 + 5), c5 = ca * (16 * c2 * c2 - 20 * c2 + 5);
          var wob = 1 + 0.075 * (s3 * P._cs[0] + c3 * P._cs[1]) + 0.035 * (s5 * P._cs[2] + c5 * P._cs[3]), ee = (dE + (dD - dE) * P.lz) * wob;
          if (PV) { var a0 = Math.atan2(dy, dx), wA = 1 + 0.075 * Math.sin(3 * a0 + P.ph[0]) + 0.035 * Math.sin(5 * a0 + P.ph[1]), eA = (Math.hypot(dx, dy) / m.Rr + (dD - Math.hypot(dx, dy) / m.Rr) * P.lz) * wA;
            PV.chi = Math.max(PV.chi || 0, Math.abs(eA - ee)); PV.chiN = (PV.chiN || 0) + 1; if (PV.ancien) { dE = Math.hypot(dx, dy) / m.Rr; wob = wA; ee = eA; } }
          if (ee < e) { e2 = e; e = ee; best = j; ein = (dE + (dD - dE) * Math.min(0.9, P.lz + 0.35)) * wob; } else if (ee < e2) e2 = ee; }
        var code, own = null;
        if (e < THR[3] + F.off[3]) {
          own = near[best]; var dt = own.P.dt, t0 = THR[0] + F.off[0] + dt[0], t1 = THR[1] + F.off[1] + dt[1], t2 = THR[2] + F.off[2] + dt[2];
          code = ein < t0 ? 0 : ein < t1 ? 1 : e < t2 ? 2 : (e < THR[3] + F.off[3] - 0.07 || e2 - e < 0.2) ? 1 : 2;   // pas de liseré là où deux médaillons se touchent
        } else {
          while (fl < F.segs.length - 1 && yy > F.segs[fl + 1][0]) fl++;
          code = 10 + F.segs[fl][1];
        }
        if (!run || run[3] !== code || run[4] !== own) { flush(); run = [x, y, y, code, own]; } else run[2] = y;
      }
      flush();
    });
    // les tracés : par médaillon et par ton, et la matière par ton — quelques remplissages en tout
    var parM = {}, mat = [new Path2D(), new Path2D(), new Path2D()], dem = tw * 0.42, larg = tw * 0.84, rab = 0.35 * K;
    runs.forEach(function (r) { var T;
      if (r[3] >= 10) T = mat[r[3] - 10];
      else { var o = parM[r[4].k] || (parM[r[4].k] = { m: r[4], s: r[4].s, T: [new Path2D(), new Path2D(), new Path2D()], runs: [] }); T = o.T[r[3]]; o.runs.push(r); }
      T.rect(r[0] - dem, r[1], larg, r[2] - r[1] + rab); });
    var R0 = { parM: parM, mat: mat, u: A.u, K: K, tw: tw, M: A.M, h: h };
    var ks = Object.keys(_tissus); if (ks.length > 6) delete _tissus[ks[0]]; _tissus[h] = R0;
    return R0;
  }

  var _dernier = null;
  function _peindreMed(o, now) { var col = cOf(o.s, now), tons = [_nuance(col), col, _encre()];
    for (var i = 0; i < 3; i++) { g.fillStyle = _rgb(tons[i]); g.fill(o.T[i]); } }
  var _CR = window._calqueRepos ? window._calqueRepos() : null;
  function Rchi(now, x0, y0, x1, y1) {
    _sync();
    var T = _tisse(now), Rm = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, k;
    if (env.vive && !env.trans && _CR) {   // v72 : au repos, le calque (signature : le tissage, la rampe, les couleurs, l'encre)
      var sg = [T.h, JSON.stringify(Rm), _rgb(_encre())]; for (k in T.parM) sg.push(_rgb(cOf(T.parM[k].s, now)));
      if (_CR.pose(g, sg.join('|'), function (C) { var g0 = g; g = C; try { _peintChi(T, Rm, now); } finally { g = g0; } })) { _dernier = T; window._chiComp = { medaillons: Object.keys(T.parM).length }; return; }
    }
    _peintChi(T, Rm, now);
  }
  function _peintChi(T, Rm, now) { var k;
    if (Rm) for (var i = 0; i < 3; i++) { g.fillStyle = _rgb(Rm[i % Rm.length]); g.fill(T.mat[i]); }   // le fond chiné : les fils teints par écheveaux
    for (k in T.parM) _peindreMed(T.parM[k], now);
    _dernier = T; window._chiComp = { medaillons: Object.keys(T.parM).length };
  }

  function _trouve(s, T) { T = T || _tisse(performance.now()); var k = _cle(s); for (var kk in T.parM) { var o = T.parM[kk]; if (o.s === s || o.m.k === k) return o; } return null; }
  // le cadrage de la planche (sa `boite` pour chine) : le médaillon et sa marge, jamais sa boîte au plus juste
  function _cadre(o) { var m = o.m, r = m.Rr * 1.12, ry = r / 0.64; return [m.x - r, m.y - ry, m.x + r, m.y + ry]; }
  function seule(nom, s, now, cx, cy, taille) {
    _sync(); var T = _tisse(now), o = _trouve(s, T); if (!o) return false;
    var B = _cadre(o), sc = taille / Math.max(B[2] - B[0], B[3] - B[1], 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(B[0] + B[2]) / 2, -(B[1] + B[3]) / 2); _peindreMed(o, now); g.restore();
    return true;
  }
  // le bord du médaillon (e = seuil du bord), relevé rayon par rayon — ce que le fil peint, au frangé près
  function _bordMed(m) { var P = m.P, pts = [], N = 72;
    for (var a = 0; a < N; a++) { var th = a / N * 6.283185307179586, lo = 0, hi = m.Rr * 3;
      for (var it = 0; it < 22; it++) { var r = (lo + hi) / 2, dx = Math.cos(th) * r, dy = Math.sin(th) * r, aa = Math.atan2(dy, dx);   // dy : déjà dans le repère aplati (× 0,64) de la formule
        var dE = Math.hypot(dx, dy) / m.Rr, dD = (Math.abs(dx) + Math.abs(dy)) / (m.Rr * 1.25), wob = 1 + 0.075 * Math.sin(3 * aa + P.ph[0]) + 0.035 * Math.sin(5 * aa + P.ph[1]);
        if ((dE + (dD - dE) * P.lz) * wob < THR[3]) lo = r; else hi = r; }
      pts.push([m.x + Math.cos(th) * lo, m.y + Math.sin(th) * lo / 0.64]); }
    return pts; }
  function contour(nom, s) { _sync(); var o = _trouve(s); return o ? _bordMed(o.m) : null; }
  function nature(nom, s) { _sync(); return _trouve(s) ? 'dalle' : null; }
  function boite(nom, s) { _sync(); var o = _trouve(s); if (!o) return null; var B = _cadre(o);
    return { x0: B[0], y0: B[1], x1: B[2], y1: B[3], fx0: B[0], fy0: B[1], fx1: B[2], fy1: B[3] }; }
  // le toucher : sur un tronçon PEINT du médaillon (le fil entier, jour entre deux fils compris : un doigt ne vise pas un fil)
  function toucher(nom, x, y) {
    _sync(); var T = _dernier || _tisse(performance.now()), dem = T.tw / 2;
    for (var k in T.parM) { var o = T.parM[k]; if (o.s.part != null) continue;
      for (var i = 0; i < o.runs.length; i++) { var r = o.runs[i]; if (Math.abs(x - r[0]) <= dem && y >= r[1] && y <= r[2] + T.K) return o.s; } }
    return null;
  }
  Rchi.transDur = 1600; Rchi.douce = true; Rchi.partDur = 900; Rchi.toucheStrict = true;
  return { chantourne: Rchi, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerChantourne = creerChantourne;
})();

/* ══════════════════ bloc « lot-V67-MASCARET » ══════════════════ */
/* ⚑ v67 (27 sept. 2026) — MASCARET, l'affiche d'op art. Porté de `plisseBuild` et `plisse` (variantes retenues : 'DEF') de la planche
   « Trois matières » au CONTRAT-MONDE :
   · les bandes d'encre (l'encre du produit, `_tfInk`), d'épaisseur constante, horizontales ou verticales, période L3/(19…23) ; chaque
     promesse soulève la page par une lame (bosse, vague, cascade), sa place en u = avg() ;
   · la dalle : les traits de couleur (cOf) qui remplissent toute l'épaisseur de leur bande, bouts ronds ; le point de ponctuation (E),
     entier ou absent ; les épines de papier (D) et la bande dédoublée (F) sont du papier : `fondToile()` ;
   · PORTAGE n° 2 : la coupe d'un trait long et la taille des épines se tirent de la CLÉ de la promesse et du RANG de la bande et du
     trait — plus jamais d'une position calculée ;
   · PORTAGE n° 7 : AUCUNE PROMESSE SANS TRAIT (la planche en laissait 2 sur 120) — une promesse sans trait en reçoit un, sur la bande
     la plus proche du centre de sa lame, là où il ne touche aucun autre trait ;
   · l'échantillonnage le long d'une bande : un pas de 3·K (la planche : 3 px sur une Toile de 300) ; les autres cotes en K ou en per ;
   · la transition suit les graines, continûment (la lame neuve se lève, celle qui part retombe).
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerMascaret(env) {
  var g, W, H, seeds, cOf, avg;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; avg = env.avg; }
  var UPL = 53.55, ARR = 900, RET = 760;
  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) return k >>> 0; }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  function _fac(s, now) { if (s.part != null) return 1 - _lisse((now - s.part) / RET); if (env.trans && s.t0 != null) return _lisse((now - s.t0) / ARR); return 1; }
  function _arr(c) { if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; } return c; }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _encre() { return _arr(typeof env.encre === 'function' ? env.encre() : env.encre); }
  // le papier : sur la Toile vivante, le dégradé même du fond (env.papier, recalé sur la vue) ; ailleurs le fond du moteur
  function _papier() { if (typeof env.papier === 'function') return env.papier(); return typeof env.fondToile === 'function' ? _rgb(_arr(env.fondToile())) : null; }
  function _pip(x, y, pts) { var ins = false, n = pts.length;
    for (var i = 0, j = n - 1; i < n; j = i++) { var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) ins = !ins; }
    return ins; }

  // la page d'une Toile : orientation et période (planche : rng(S.g ^ 0x9115))
  function _page(K) { var ct = env.cleToile == null ? 1 : env.cleToile, R = _lcg((ct ^ 0x9115) >>> 0), vert = R() < 0.4, L3 = 300 * K;
    return { vert: vert, per: L3 / (19 + Math.floor(R() * 5)), K: K }; }
  // une lame : ce qu'elle tire de SA clé (planche : rng(p.h ^ 0xf01d))
  var _par = {};
  function _param(k) { var P = _par[k]; if (P) return P; var q = _lcg(k ^ 0xf01d);
    var kind = q() < 0.4 ? 0 : q() < 0.55 ? 1 : 2;
    P = { kind: kind, su: 0.8 + 0.5 * q(), sv: 0.9 + 0.6 * q(), A: (1.1 + 1.1 * q()) * (q() < 0.5 ? -1 : 1), z: _lcg(k ^ 0x5eed)() };
    return (_par[k] = P); }

  /* ⚑ v67 — AU REPOS, UNE POSITION RESTE GELÉE. Au-delà d'une trentaine de paroles, le moteur n'arrive jamais tout à fait au repos : ses
     graines oscillent d'une image à l'autre, sans fin (mesuré à 40 : 0,5 à 3 px, deux graines qui rebondissent) — la géométrie se
     refaisait à chaque image. Hors transition, une graine garde sa position tant qu'elle ne s'en éloigne pas de plus de 0,25 × l'unité
     de matière (un vrai ressemis la déplace bien plus) ; pendant une
     transition, les positions vivent (et le gel reprend exactement où elles finissent). */
  var _gel = {};
  function _geler(L) { var tol = (env.uMat || 70) * 0.25, vive = env.vive, tr = env.trans;
    L.forEach(function (e) { var k = e.k != null ? e.k : e.h, f = _gel[k];
      if (vive && tr) { _gel[k] = [e.x, e.y]; return; }
      if (f && Math.abs(e.x - f[0]) < tol && Math.abs(e.y - f[1]) < tol) { e.x = f[0]; e.y = f[1]; }
      else if (vive) _gel[k] = [e.x, e.y]; }); }
  var _faits = {}, _dernier = null;
  /* ⚑ v98 (Tom, 29 sept. : « 3 secondes par image à 500 paroles, inutilisable ») — LE BUDGET DE CONSTRUCTION. À 500 paroles une
     construction coûte ~0,8 s (WebKit) ; pendant que la Toile se pose, les positions changent à chaque image et la construction se
     refaisait à chaque image : une image par seconde pendant 16 s. Quand la dernière construction a coûté plus de 40 ms, on repeint
     la précédente et on ne reconstruit qu'après quatre fois son coût — le moteur est relancé pour revenir construire l'état posé.
     Sous ~100 paroles une construction reste sous 40 ms : rien ne change. L'état final est toujours construit. */
  var _mB = null, _mCout = 0, _mFin = 0;
  function _construit(now) {
    var K = env.uMat / UPL, PG = _page(K), vert = PG.vert, per = PG.per, U = vert ? H : W, V = vert ? W : H, i, s, n = seeds.length, perte = 0, L = [];
    for (i = 0; i < n; i++) { s = seeds[i]; if (s.kind === 'gray') continue; var f = _fac(s, now); perte += 1 - f;
      L.push({ s: s, k: _cle(s), x: s.x, y: s.y, f: f }); }   // la position de REPOS (contrat §7.1 : le frémissement est facultatif)
    var u0 = avg() * Math.sqrt(Math.max(1, n) / Math.max(1, n - perte));
    _geler(L);
    L.sort(function (a, b) { return a.k - b.k; });
    var h = 2166136261; function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(K * 4096)); mix(env.cleToile == null ? 0 : env.cleToile); mix(Math.round(u0 * 16));
    L.forEach(function (e) { mix(e.k); mix(Math.round(e.x * 2)); mix(Math.round(e.y * 2)); mix(Math.round(e.f * 512)); });
    var PV = window._v72Preuve, PVA = !!(PV && PV.ancien);   // la sonde de preuve, lue une fois
    if (_faits[h] && !PV) return _faits[h];
    if (!PV && _mB && _mCout > 40 && performance.now() - _mFin < _mCout * 4) { if (typeof env.relance === 'function') env.relance(); return _mB; }
    var _mT0 = performance.now();
    window._masConstr = (window._masConstr || 0) + 1;   // publié : combien de constructions (une par état)
    var folds = L.filter(function (e) { return e.f > 0.001; }).map(function (e) {
      var P = _param(e.k), R = u0 * (0.36 + 0.2 * P.z + 0.26 * P.z * P.z * P.z) * window._tailleApercu(e.s);
      return { p: e, s: e.s, k: e.k, u: vert ? e.y : e.x, v: vert ? e.x : e.y, kind: P.kind,
        su: Math.max(per * 1.6, R * P.su) * e.f, sv: Math.max(per * 2.2, R * P.sv) * e.f, A: per * P.A * e.f }; });
    /* ⚑ v72 (budget) — une lame à plus de 4 fois sa hauteur de la bande pèse exp(−16) ≈ 10⁻⁷ de son amplitude (moins d'un cent-millième
       de pixel) : on la saute avant l'exponentielle. */
    /* ⚑ v72 (budget) — LA HAUTEUR D'UNE BANDE, PRÉCALCULÉE. Sur une bande, D n'est demandée qu'à ses deux bords et à son milieu : le
       facteur vertical de chaque lame y est une constante (3 × n exponentielles par bande). Le long de la bande, les échantillons
       tombent sur la même grille pour toutes les bandes : le facteur horizontal (l'amplitude et la forme de la lame) s'y calcule une
       fois par construction. D est alors une somme de produits — les MÊMES produits, dans le même ordre : même résultat au bit près. */
    var GU = new Map();
    function _guDe(u) { var r = new Float64Array(folds.length);
      for (var j = 0; j < folds.length; j++) { var F = folds[j], du = (u - F.u) / F.su;
        r[j] = F.kind === 0 ? F.A * Math.exp(-du * du) : F.kind === 1 ? F.A * Math.sin(du * 2.2) * Math.exp(-du * du * 0.5) : F.A * 0.5 * (1 + Math.tanh(du * 1.8)); }
      return r; }
    function Db(bd, u, v) { var m = bd.gv || (bd.gv = new Map()), gv = m.get(v), j;
      if (!gv) { gv = new Float64Array(folds.length); var nz0 = []; for (j = 0; j < folds.length; j++) { var F = folds[j], dv = (v - F.v) / F.sv; gv[j] = (dv > 4 || dv < -4) ? 0 : Math.exp(-dv * dv); if (gv[j] !== 0) nz0.push(j); } gv.nz = nz0; m.set(v, gv); }   /* v98 : les lames qui atteignent la bande, dans l'ordre */
      var gu = GU.get(u), d = 0;
      if (PV) { var dA = 0; for (j = 0; j < folds.length; j++) { var H0 = folds[j], du0 = (u - H0.u) / H0.su, dv0 = (v - H0.v) / H0.sv, gv0 = Math.exp(-dv0 * dv0);
          dA += H0.kind === 0 ? H0.A * Math.exp(-du0 * du0) * gv0 : H0.kind === 1 ? H0.A * Math.sin(du0 * 2.2) * Math.exp(-du0 * du0 * 0.5) * gv0 : H0.A * 0.5 * (1 + Math.tanh(du0 * 1.8)) * gv0; }
        var P0 = PV, dN = Db0(gv, gu, u); P0.mas = Math.max(P0.mas || 0, Math.abs(dN - dA)); P0.masN = (P0.masN || 0) + 1; return P0.ancien ? dA : dN; }
      return Db0(gv, gu, u); }
    function Db0(gv, gu, u) { var j, d = 0, nz = gv.nz, q, nq = nz ? nz.length : gv.length;   /* v98 (500 paroles) : on ne parcourt que les lames non nulles — mêmes termes, même ordre */
      if (gu) { for (q = 0; q < nq; q++) { j = nz ? nz[q] : q; if (gv[j] !== 0) d += gu[j] * gv[j]; } return d; }
      for (q = 0; q < nq; q++) { j = nz ? nz[q] : q; if (gv[j] === 0) continue; var G = folds[j], du = (u - G.u) / G.su;   // hors de la grille (les traits) : la lame seulement si elle atteint la bande
        d += (G.kind === 0 ? G.A * Math.exp(-du * du) : G.kind === 1 ? G.A * Math.sin(du * 2.2) * Math.exp(-du * du * 0.5) : G.A * 0.5 * (1 + Math.tanh(du * 1.8))) * gv[j]; }
      return d; }
    var FL = folds;
    function D(u, v) { var d = 0; for (var j = 0; j < FL.length; j++) { var F = FL[j], dv = (v - F.v) / F.sv; if (dv > 4 || dv < -4) continue; var du = (u - F.u) / F.su, gv = Math.exp(-dv * dv);
        if (F.kind === 0) d += F.A * Math.exp(-du * du) * gv; else if (F.kind === 1) d += F.A * Math.sin(du * 2.2) * Math.exp(-du * du * 0.5) * gv; else d += F.A * 0.5 * (1 + Math.tanh(du * 1.8)) * gv; }
      return d; }
    var bands = []; for (var jb = -4; jb * per < V + 4 * per; jb++) bands.push({ j: jb, b0: jb * per, b1: (jb + 0.5) * per });
    var du = 3 * K, P2 = function (a, b) { return vert ? [b, a] : [a, b]; };
    for (var ag = -6 * K; ag <= U + 6 * K + 1e-6; ag += du) GU.set(ag, _guDe(ag));   // la grille des échantillons (même départ, même pas, même cumul que les boucles)
    function edge(bd, a, top) { return top ? bd.b0 + Db(bd, a, bd.b0) : bd.b1 + Db(bd, a, bd.b1); }
    function thk(bd, a) { var p = edge(bd, a, true), q = edge(bd, a, false); return [(p + q) / 2, q - p]; }
    // l'encre : toutes les bandes, un seul tracé
    var encre = new Path2D(), m6 = 6 * K;
    bands.forEach(function (bd) { var pts = [], a; for (a = -m6; a <= U + m6 + 1e-6; a += du) pts.push(P2(a, edge(bd, a, true))); for (a = U + m6; a >= -m6 - 1e-6; a -= du) pts.push(P2(a, edge(bd, a, false)));
      encre.moveTo(pts[0][0], pts[0][1]); for (var z = 1; z < pts.length; z++) encre.lineTo(pts[z][0], pts[z][1]); encre.closePath(); });
    // v72 : `lim` (facultatif) — si x² + y² ≥ lim, le poids ne peut pas dépasser e^−lim : rien à calculer (0), la décision est la même
    function wOf(F, a, v, lim) { var x = (a - F.u) / (F.su * (F.kind === 2 ? 1.05 : 0.8)), y = (v - F.v) / (F.sv * 0.7); if (lim != null && x * x + y * y >= lim && !PVA) return 0; return Math.exp(-x * x - y * y); }
    function nearCol(a, v) { return folds.some(function (F) { return wOf(F, a, v, 1.61) > 0.2; }); }
    // F · la bande dédoublée : un filet de papier, sur une bande sur trois, là où la lame est haute, loin des traits
    var filet = new Path2D();
    bands.forEach(function (bd) { if (((bd.j * 7919) >>> 0) % 3 !== 0) return; var bm = (bd.b0 + bd.b1) / 2, on = false;
      for (var a = -m6; a <= U + m6; a += du) { var dm = Db(bd, a, bm), hi = Math.abs(dm) > per * 0.85 && !nearCol(a, bm + dm), mm = (edge(bd, a, true) + edge(bd, a, false)) / 2, q2 = P2(a, mm);
        if (hi) { if (on) filet.lineTo(q2[0], q2[1]); else filet.moveTo(q2[0], q2[1]); on = true; } else on = false; } });
    // la dalle : chaque point de bande au pli le plus fort, au cœur du pli ; tronçons ; capsules à bouts ronds ; point ; épines
    var parF = {}, epines = new Path2D(), capsules = [];
    folds.forEach(function (F) { parF[F.k] = { F: F, s: F.s, k: F.k, T: new Path2D(), pieces: [], x0: 1e18, y0: 1e18, x1: -1e18, y1: -1e18 }; });
    function capsule(bd, s0, s1, F, rang, dernier, runs, rIdx) {
      if (s1 - s0 < per * 0.6) return;
      var o = parF[F.k], pts = [], capR = thk(bd, (s0 + s1) / 2)[1] * 0.5, capL = Math.min(capR, (s1 - s0) / 2);
      var sh = function (a) { var d = Math.min(a - s0, s1 - a); return d >= capL ? 1 : Math.sqrt(Math.max(0, 1 - (1 - d / capL) * (1 - d / capL))); };
      var n2 = Math.max(8, Math.ceil((s1 - s0) / (1.2 * K))), ii, a, t;
      var TK = [];   // v72 : l'épaisseur en chaque point, calculée une fois (les deux bords du trait la relisaient)
      for (ii = 0; ii <= n2; ii++) { a = s0 + (s1 - s0) * ii / n2; t = TK[ii] = thk(bd, a); pts.push(P2(a, t[0] - t[1] * 0.5 * sh(a))); }
      for (ii = n2; ii >= 0; ii--) { a = s0 + (s1 - s0) * ii / n2; t = TK[ii]; pts.push(P2(a, t[0] + t[1] * 0.5 * sh(a))); }
      o.T.moveTo(pts[0][0], pts[0][1]); for (ii = 1; ii < pts.length; ii++) o.T.lineTo(pts[ii][0], pts[ii][1]); o.T.closePath(); o.pieces.push(pts);
      pts.forEach(function (v) { if (v[0] < o.x0) o.x0 = v[0]; if (v[0] > o.x1) o.x1 = v[0]; if (v[1] < o.y0) o.y0 = v[1]; if (v[1] > o.y1) o.y1 = v[1]; });
      var hk = _fnv(F.k + ':' + bd.j + ':' + rang);   // PORTAGE n° 2 : la clé, le rang de la bande et du trait — jamais une position
      // E · le point de ponctuation, entier ou absent, seulement après le dernier trait du tronçon
      if (dernier) { var ue = s1 + per * 0.75, te = thk(bd, ue), rd = Math.abs(te[1]) * 0.42, nxt = null;
        for (var r2 = rIdx + 1; r2 < runs.length; r2++) if (runs[r2].u0 > runs[rIdx].u1) { nxt = runs[r2]; break; }
        if (rd > 0.3 * K && ue + rd < U - 2 * K && (!nxt || nxt.u0 - per * 0.4 > ue + rd)) { var c2 = P2(ue, te[0]); o.T.moveTo(c2[0] + rd, c2[1]); o.T.arc(c2[0], c2[1], rd, 0, 6.2832);
          var cp = []; for (var z = 0; z < 16; z++) cp.push([c2[0] + Math.cos(z / 16 * 6.2832) * rd, c2[1] + Math.sin(z / 16 * 6.2832) * rd]); o.pieces.push(cp);
          if (c2[0] - rd < o.x0) o.x0 = c2[0] - rd; if (c2[0] + rd > o.x1) o.x1 = c2[0] + rd; if (c2[1] - rd < o.y0) o.y0 = c2[1] - rd; if (c2[1] + rd > o.y1) o.y1 = c2[1] + rd; } }
      // D · deux fines épines de papier juste après chaque bout, trois tailles, parfois une seule
      [[s0, -1], [s1, 1]].forEach(function (E2) { var ue2 = E2[0], sgn = E2[1], rq = (((hk * (sgn > 0 ? 7 : 13)) >>> 0) % 97) / 97, lev = rq < 0.34 ? 0 : rq < 0.72 ? 0.5 : 1;
        var a2 = ue2 + sgn * per * (0.09 + 0.08 * lev), tt = thk(bd, a2), w = per * (0.045 + 0.04 * lev), dep = tt[1] * (0.3 + 0.25 * lev);
        (rq > 0.9 ? [rq > 0.95 ? -1 : 1] : [-1, 1]).forEach(function (side) { var e = tt[0] + side * tt[1] / 2, tip = e - side * dep;
          var A1 = P2(a2 - w, e + side * 0.6 * K), B1 = P2(a2 + w, e + side * 0.6 * K), C1 = P2(a2 + sgn * w * 0.4, tip);
          epines.moveTo(A1[0], A1[1]); epines.lineTo(B1[0], B1[1]); epines.lineTo(C1[0], C1[1]); epines.closePath(); }); });
    }
    var parBande = [];
    bands.forEach(function (bd) {
      var bm = (bd.b0 + bd.b1) / 2, runs = [], cur = null;
      for (var a = -m6; a <= U + m6; a += du) { var bf = null, bw = 0.45, lim = -Math.log(0.45), vd = bm + Db(bd, a, bm); for (var j = 0; j < folds.length; j++) { var w = wOf(folds[j], a, vd, lim); if (w > bw) { bw = w; bf = folds[j]; lim = -Math.log(bw); } }   // v72 : D ne dépend pas de la lame — calculée une fois (elle l'était 40 fois)
        if (cur && cur.F === bf) cur.u1 = a; else { if (cur && cur.F) runs.push(cur); cur = { F: bf, u0: a, u1: a }; } }
      if (cur && cur.F) runs.push(cur);
      parBande.push({ bd: bd, runs: runs });
      var rang = {};
      runs.forEach(function (r, rIdx) {
        if (r.u1 - r.u0 < per * 1.1) return;
        var L0 = r.u1 - r.u0, rg = rang[r.F.k] = (rang[r.F.k] || 0) + 1, cut = L0 > per * 5 && _fnv(r.F.k + ':' + bd.j + ':coupe:' + rg) % 3 === 0;
        var segs = cut ? [[r.u0, r.u0 + L0 * 0.58], [r.u0 + L0 * 0.64, r.u1]] : [[r.u0 + per * 0.15, r.u1 - per * 0.15]];
        segs.forEach(function (sg, si) { capsule(bd, sg[0], sg[1], r.F, rg * 4 + si, si === segs.length - 1, runs, rIdx); });
      });
    });
    // PORTAGE n° 7 : une lame sans trait en reçoit un — sur la bande la plus proche du centre de sa lame, sans toucher un autre trait
    folds.forEach(function (F) {
      if (parF[F.k].pieces.length || F.p.f < 0.999) return;
      /* v98 (Tom : « 3 secondes par image à 500 paroles, inutilisable ») — les cinq bandes les plus proches, sans trier toutes les
         bandes pour chaque lame (77 % du temps à 500). Même choix que le tri stable d'avant : à distance égale, la première. */
      var dd = parBande.map(function (p) { return Math.abs((p.bd.b0 + p.bd.b1) / 2 + Db(p.bd, F.u, (p.bd.b0 + p.bd.b1) / 2) - F.v); }), cand = [], pris5 = {};
      for (var c5 = 0; c5 < Math.min(5, dd.length); c5++) { var b5 = -1; for (var i5 = 0; i5 < dd.length; i5++) if (!pris5[i5] && (b5 < 0 || dd[i5] < dd[b5])) b5 = i5; pris5[b5] = 1; cand.push(parBande[b5]); }
      for (var c = 0; c < Math.min(5, cand.length); c++) { var PB = cand[c], s0 = F.u - per * 0.75, s1 = F.u + per * 0.75;
        var libre = PB.runs.every(function (r) { return r.u1 - r.u0 < per * 1.1 || s1 + per * 0.4 < r.u0 || s0 - per * 0.4 > r.u1; });
        if (libre) { capsule(PB.bd, s0, s1, F, 999, true, [], 0); window._masRepris = (window._masRepris || 0) + 1; break; } }
    });
    var R0 = { parF: parF, encre: encre, filet: filet, epines: epines, per: per, K: K, h: h };
    _mB = R0; _mFin = performance.now(); _mCout = _mFin - _mT0;
    var ks = Object.keys(_faits); if (ks.length > 6) delete _faits[ks[0]]; _faits[h] = R0;
    return R0;
  }

  var _CR = window._calqueRepos ? window._calqueRepos() : null;
  function Rmas(now, x0, y0, x1, y1) {
    _sync();
    var B = _construit(now), k;
    if (env.vive && !env.trans && _CR) {   // v72 : au repos, le calque (signature : la construction, les couleurs, l'encre, le thème — le papier suit la vue)
      var sg = [B.h, _rgb(_encre()), env.isLightM() ? 1 : 0]; for (k in B.parF) sg.push(_rgb(cOf(B.parF[k].s, now)));
      if (_CR.pose(g, sg.join('|'), function (C) { var g0 = g; g = C; try { _peintMas(B, now); } finally { g = g0; } })) { _dernier = B; window._masComp = { lames: Object.keys(B.parF).length }; return; }
    }
    _peintMas(B, now);
  }
  function _peintMas(B, now) { var pap = _papier(), k;
    g.fillStyle = _rgb(_encre()); g.fill(B.encre);
    if (pap) { g.strokeStyle = pap; g.lineCap = 'round'; g.lineWidth = B.per * 0.12; g.stroke(B.filet); }
    for (k in B.parF) { var o = B.parF[k]; if (!o.pieces.length) continue; g.fillStyle = _rgb(cOf(o.s, now)); g.fill(o.T); }
    if (pap) { g.fillStyle = pap; g.fill(B.epines); }
    _dernier = B; window._masComp = { lames: Object.keys(B.parF).length };
  }
  function _trouve(s, B) { B = B || _construit(performance.now()); var k = _cle(s); for (var kk in B.parF) { var o = B.parF[kk]; if ((o.s === s || o.k === k) && o.pieces.length) return o; } return null; }
  function seule(nom, s, now, cx, cy, taille) {
    _sync(); var o = _trouve(s, _construit(now)); if (!o) return false;
    var sc = taille / Math.max(o.x1 - o.x0, o.y1 - o.y0, 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(o.x0 + o.x1) / 2, -(o.y0 + o.y1) / 2);
    g.fillStyle = _rgb(cOf(o.s, now)); g.fill(o.T); g.restore(); return true;
  }
  function _enveloppe(o) { var pts = []; o.pieces.forEach(function (q) { pts = pts.concat(q); }); pts.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
    function cr(q, a, b) { return (a[0] - q[0]) * (b[1] - q[1]) - (a[1] - q[1]) * (b[0] - q[0]); }
    var lo = [], up = [], i; for (i = 0; i < pts.length; i++) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], pts[i]) <= 0) lo.pop(); lo.push(pts[i]); }
    for (i = pts.length - 1; i >= 0; i--) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], pts[i]) <= 0) up.pop(); up.push(pts[i]); }
    return lo.slice(0, -1).concat(up.slice(0, -1)); }
  // (une dalle de Mascaret est faite de plusieurs traits : son contour est l'enveloppe de ses traits ; le toucher, lui, vise chaque trait)
  function contour(nom, s) { _sync(); var o = _trouve(s); return o ? _enveloppe(o) : null; }
  function nature(nom, s) { _sync(); return _trouve(s) ? 'dalle' : null; }
  function boite(nom, s) { _sync(); var o = _trouve(s); if (!o) return null; return { x0: o.x0 - 0.5, y0: o.y0 - 0.5, x1: o.x1 + 0.5, y1: o.y1 + 0.5, fx0: o.x0 - 0.5, fy0: o.y0 - 0.5, fx1: o.x1 + 0.5, fy1: o.y1 + 0.5 }; }
  function toucher(nom, x, y) {
    _sync(); var B = _dernier || _construit(performance.now());
    for (var k in B.parF) { var o = B.parF[k]; if (o.s.part != null || x < o.x0 || x > o.x1 || y < o.y0 || y > o.y1) continue;
      for (var i = 0; i < o.pieces.length; i++) if (_pip(x, y, o.pieces[i])) return o.s; }
    // un trait fait ~ une demi-période : trop fin pour un doigt. Hors d'un trait, l'enveloppe des traits d'une dalle (la plus petite)
    var best = null, ba = 1e18;
    for (var k2 in B.parF) { var o2 = B.parF[k2]; if (o2.s.part != null || !o2.pieces.length || x < o2.x0 || x > o2.x1 || y < o2.y0 || y > o2.y1) continue;
      var E = o2.env || (o2.env = _enveloppe(o2)); if (!_pip(x, y, E)) continue; var ar = (o2.x1 - o2.x0) * (o2.y1 - o2.y0); if (ar < ba) { ba = ar; best = o2.s; } }
    return best;
  }
  Rmas.ancre = function (s) { _sync(); var o = _trouve(s, _dernier); if (!o) return null; return [(o.x0 + o.x1) / 2, (o.y0 + o.y1) / 2, o.x1 - o.x0]; };
  Rmas.transDur = 1600; Rmas.douce = true; Rmas.partDur = 900; Rmas.toucheStrict = true;
  return { mascaret: Rmas, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerMascaret = creerMascaret;
})();

/* ══════════════════ bloc « lot-V68-RAMAGE » ══════════════════ */
/* ⚑ v68 (27 sept. 2026) — RAMAGE, le plumage. Porté de `parure()` (planche « Trois matières »), jugé « 99,99 % parfait » par Tom :
   à l'identique, sans rien améliorer (NUANCES). Au CONTRAT-MONDE :
   · le CODE de dessin de la planche est gardé tel quel ; il trace dans un ENREGISTREUR (un tracé par remplissage ou par trait, noté
     avec un JETON de couleur), et la peinture rejoue la liste en résolvant les jetons : la couleur de la promesse (cOf), sa nuance
     (la seconde couleur, Q330), l'encre du produit (`_tfInk`), la matière (la rampe TH), le papier ; le croissant « 30 % de blanc »
     de la planche est une nuance de la couleur de sa plume (aucune couleur écrite) ;
   · le PAPIER (les découpes entre les plumes) : sur la Toile vivante, le fond même du moteur, recalé dans le repère du monde
     (`env.papier`) — un aplat ferait des traits d'une autre teinte sur le dégradé de l'accueil ; ailleurs `fondToile()` ;
   · longueurs : le pas des plumes en unité de matière (sp = L3 / 40) ; l'œil en u = avg() (la place R de la planche) ;
   · LCG sur la clé de la Toile (le plumage) et sur la clé de chaque promesse (son œil, sa touffe) ;
   · la dalle seule : la planche en mode `only` (ses découpes effacent : `destination-out`, sur le canevas de la dalle seulement) ;
   · la transition : l'œil neuf s'ouvre (sa place grandit), celui qui part se referme — le plumage suit, continûment.
   Aucune image, aucune couleur écrite, toute longueur en fraction de u. */
(function () {
function creerRamage(env) {
  var g, W, H, seeds, cOf, avg, L3 = 300;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; avg = env.avg; }
  var UPL = 53.55, ARR = 900, RET = 760;
  function _fnv(t) { var h = 0x811c9dc5; for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; }
  function _lcg(k) { var sd = (k >>> 0) % 0x7fffffff || 1; return function () { sd = (sd * 1103515245 + 12345) & 0x7fffffff; return sd / 0x7fffffff; }; }
  function _cle(s) {
    var pid = s.pid != null ? s.pid : s.partPid;
    /* v98 (500 paroles) : la clé d'une parole se cherche parmi toutes les paroles ; gardée une seconde sur la graine */
    if (pid != null && s._raK != null && s._raKp === pid && performance.now() - s._raKt < 1000) return s._raK;
    if (pid != null && typeof env._dalleDeCle === 'function') { var k = env._dalleDeCle(pid); if (k != null) { s._raK = k >>> 0; s._raKp = pid; s._raKt = performance.now(); return k >>> 0; } }
    var nu = s.nuee || s.partNuee; if (nu) return _fnv('n\u0000' + nu);
    if (pid != null) return _fnv('p\u0000' + pid);
    if (s._cleAp != null) return s._cleAp;   // v75 : une graine d'aperçu du Studio garde la clé de sa place de REPOS — la même que l'aperçu fixe, stable pendant qu'elle bouge
    return _fnv('v\u0000' + Math.round(s.x) + '\u0000' + Math.round(s.y));
  }
  function _lisse(a) { return a <= 0 ? 0 : a >= 1 ? 1 : a * a * (3 - 2 * a); }
  function _fac(s, now) { if (s.part != null) return 1 - _lisse((now - s.part) / RET); if (env.trans && s.t0 != null) return _lisse((now - s.t0) / ARR); return 1; }
  function _arr(c) { if (typeof c === 'string') { var h = c.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; } return c; }
  function _rgb(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function _lumR(c) { function l(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); } return 0.2126 * l(c[0]) + 0.7152 * l(c[1]) + 0.0722 * l(c[2]); }
  function _nuance(c) { var b = _lumR(c) > 0.3 ? 0 : 255; return [c[0] + (b - c[0]) * 0.38, c[1] + (b - c[1]) * 0.38, c[2] + (b - c[2]) * 0.38]; }
  function _encre() { return _arr(typeof env.encre === 'function' ? env.encre() : env.encre); }
  // les couleurs de la planche deviennent des JETONS, résolus à la peinture
  function _mix(a, b, t) { return 'X|' + a + '|' + b + '|' + t; }

  /* ---- l'enregistreur : la planche y trace comme dans un canevas ; chaque remplissage / trait devient une opération ---- */
  function _enreg() {
    var R = { ops: [], cur: null, fillStyle: 'B', strokeStyle: 'B', lineWidth: 1, globalCompositeOperation: 'source-over', b: [1e18, 1e18, -1e18, -1e18] };
    function bb(x, y) { if (x < R.b[0]) R.b[0] = x; if (y < R.b[1]) R.b[1] = y; if (x > R.b[2]) R.b[2] = x; if (y > R.b[3]) R.b[3] = y;
      var q = R.pb; if (x < q[0]) q[0] = x; if (y < q[1]) q[1] = y; if (x > q[2]) q[2] = x; if (y > q[3]) q[3] = y; }
    R.eye = null; R.pb = [1e18, 1e18, -1e18, -1e18];   // v72 : l'œil du tracé, et sa boîte
    R.beginPath = function () { R.cur = new Path2D(); R.pb = [1e18, 1e18, -1e18, -1e18]; };
    R.moveTo = function (x, y) { R.cur.moveTo(x, y); bb(x, y); };
    R.lineTo = function (x, y) { R.cur.lineTo(x, y); bb(x, y); };
    R.bezierCurveTo = function (a, b, c, d, x, y) { R.cur.bezierCurveTo(a, b, c, d, x, y); bb(a, b); bb(c, d); bb(x, y); };
    R.quadraticCurveTo = function (a, b, x, y) { R.cur.quadraticCurveTo(a, b, x, y); bb(a, b); bb(x, y); };
    R.closePath = function () { R.cur.closePath(); };
    R.fill = function () { R.ops.push([0, R.cur, R.fillStyle, 0, R.globalCompositeOperation, R.eye, R.pb]); };
    R.stroke = function () { R.ops.push([1, R.cur, R.strokeStyle, R.lineWidth, R.globalCompositeOperation, R.eye, R.pb]); };
    return R;
  }
  var _l = null;   // les promesses de l'enregistrement en cours (les jetons P/N se lisent par leur rang)

  /* ================= le code de la planche (Promi - Trois matières), aux unités près ================= */
  function _cutStroke(g, iso, bg, w) {
    if (iso) { g.globalCompositeOperation = 'destination-out'; g.strokeStyle = 'B'; } else g.strokeStyle = bg;
    g.lineWidth = w; g.stroke(); g.globalCompositeOperation = 'source-over';
  }

  /* ---------------- I · PARURE — le plumage et ses yeux ---------------- */
  function _parure(g, S, T, only, Q) {   // v72 : Q (facultatif) — les plumes sont mises en FILE, dans le même ordre, au lieu d'être tracées
    const _pt0 = S.prof ? performance.now() : 0; const R = _lcg(S.g >>> 0), th0 = R() * 2 * Math.PI, bx = Math.cos(th0), by = Math.sin(th0);
    const _apBorne = (!!window._apImage || !!window._ramToileAp) && !window._ramFilmOff;
    const sp = L3 / 40, anchors = [];
    for (let y = -sp * 2; y < H + sp * 2; y += sp) for (let x = -sp * 2; x < W + sp * 2; x += sp) { const a = [x + (R() - 0.5) * sp * 0.7, y + (R() - 0.5) * sp * 0.7, R(), R()]; if (!S.filtre || S.filtre(a[0], a[1])) anchors.push(a); }   /* v90 : le film filtre dès l'ancre — la même suite de tirages, donc les mêmes places */
    const F = [];
    // chaque œil a sa taille ; chaque plume sa taille et sa largeur
    const ez = new Map(S.pr.map(p => [p, 0.78 + 0.5 * _lcg((p.h ^ 0xe7e) >>> 0)()]));
    for (const [x, y, r1, r2] of anchors) {
      let best = null, bd = 1e9, vx = bx * 0.8, vy = by * 0.8;
      for (const p of S.pr) {
        const dx = x - p.x, dy = y - p.y, d = Math.hypot(dx, dy) || 1e-6, t = d / (p.R * ez.get(p));
        if (t < bd) { bd = t; best = p; }
        let w = 1.9 * Math.exp(-t * t * 0.7);
        /* ⚑ v90 — au Studio seulement : la poussée d'un œil s'éteint entre 1,8 et 2,4 rayons. Sans borne, elle ne s'annulait jamais : un œil
           neuf tournait d'un ou deux degrés TOUTES les plumes de la Toile, et 26 % des pixels basculaient d'un coup à la fin de la pousse
           (mesuré, `_ramFilmEcart`). La vraie Toile ne change pas. */
        if (_apBorne) { if (t >= 2.4) w = 0; else if (t > 1.8) { const u = (2.4 - t) / 0.6; w *= u * u * (3 - 2 * u); } }
        vx += dx / d * w; vy += dy / d * w;
      }
      const l = Math.hypot(vx, vy) || 1; vx /= l; vy /= l;
      const sc = (1 + 0.7 * Math.exp(-bd * bd * 1.2)) * (0.8 + 0.4 * ((r1 * 7.31 + r2 * 3.7) % 1));
      F.push({ x, y, vx, vy, sc, p: best, t: bd, r1, r2, pr: x * bx + y * by });
    }
    // les plumes d'aval d'abord : chaque plume recouvre la base de la suivante
    F.sort((a, b) => b.pr - a.pr); const _pt1 = S.prof ? performance.now() : 0;
    const bands = t => t < 0.22 ? 1 : t < 0.42 ? 0 : t < 0.58 ? 2 : t < 0.8 ? 0 : t < 0.9 ? 2 : -1;
    const PL = (e, ...a) => { if (Q) Q.push(() => { g.eye = e; plume(...a); }); else if (S.cachePL && g.ops) {   /* v90 : le film réemploie les tracés d'une plume identique au bit près */
        let f = a[0];
        if (S.quant) { const an = Math.atan2(f.vy, f.vx), qa = Math.round(an / S.quant) * S.quant; if (qa !== an) { f = { x: f.x, y: f.y, vx: Math.cos(qa), vy: Math.sin(qa), sc: f.sc, p: f.p, t: f.t, r1: f.r1, r2: f.r2, pr: f.pr }; a = a.slice(); a[0] = f; } }   /* v91 : le film arrondit l'angle d'une plume à S.quant (0,3°, ≤ 0,07 px) — une plume qui tourne d'un rien retrouve ses tracés */
        const cle = e + '|' + f.x + '|' + f.y + '|' + f.vx + '|' + f.vy + '|' + f.r1 + '|' + a.slice(1).join('|'), hit = S.cachePL.get(cle);
        if (hit) { for (let i = 0; i < hit.length; i++) g.ops.push(hit[i]); } else { g.eye = e; const n0 = g.ops.length; plume(...a); S.cachePL.set(cle, g.ops.slice(n0)); } }
      else { g.eye = e; plume(...a); } };   // e : l'œil (sa clé), ou rien (la matière)
    const plume = (f, col, L, Wd, detail, crescent, nocut, veinCol) => {
      const vx = f.vx, vy = f.vy, nx = -vy, ny = vx, q = _lcg(((f.r1 * 1e7) | 0) >>> 0);
      const aL = 0.5 + (f.r1 - 0.5) * 0.16, aR = 0.5 - (f.r1 - 0.5) * 0.16, tipT = (q() - 0.5) * 0.12;
      const X = (s, t) => f.x + vx * L * s + nx * Wd * t, Y = (s, t) => f.y + vy * L * s + ny * Wd * t;
      g.beginPath();
      g.moveTo(X(0, -0.14), Y(0, -0.14));
      g.bezierCurveTo(X(0.12, -aL * 1.1), Y(0.12, -aL * 1.1), X(0.72, -aL * 1.08), Y(0.72, -aL * 1.08), X(1, tipT), Y(1, tipT));
      g.bezierCurveTo(X(0.72, aR * 1.08), Y(0.72, aR * 1.08), X(0.12, aR * 1.1), Y(0.12, aR * 1.1), X(0, 0.14), Y(0, 0.14));
      g.closePath();
      g.fillStyle = col; g.fill();
      // au cœur de l'œil, la découpe se fait à l'encre : jamais un trait de fond au centre
      if (nocut === 'ink') _cutStroke(g, false, T.ink, sp * 0.06 * Math.min(1, L / (sp * 1.85)));
      else if (!nocut) _cutStroke(g, !!only, T.bg, sp * 0.075 * Math.min(1, L / (sp * 1.85)));
      if (!detail) return;
      // les nervures : des fentes pleines et effilées, découpées dans la plume comme au scalpel — jamais un trait fin
      const cut = pts => {
        if (only && !veinCol) g.globalCompositeOperation = 'destination-out';
        g.beginPath(); g.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]); g.closePath();
        g.fillStyle = veinCol || (only ? 'B' : T.bg); g.fill(); g.globalCompositeOperation = 'source-over';
      };
      // une fente de (s0,t0) à (s1,t1), large w à sa base, courbée de c, qui s'effile jusqu'à rien
      const fente = (s0, t0, s1, t1, w, c) => {
        const A = [], B = [], N = 8;
        for (let i = 0; i <= N; i++) {
          const k = i / N, s = s0 + (s1 - s0) * k, t = t0 + (t1 - t0) * k + c * Math.sin(Math.PI * k), ww = w * (1 - k) ** 0.8;
          const px = X(s, t), py = Y(s, t), ds = (s1 - s0) * L, dt = (t1 - t0) * Wd, l = Math.hypot(ds, dt) || 1;
          const ox = (-dt * vx + ds * nx) / l, oy = (-dt * vy + ds * ny) / l;
          A.push([px + ox * ww / 2, py + oy * ww / 2]); B.push([px - ox * ww / 2, py - oy * ww / 2]);
        }
        cut(A.concat(B.reverse()));
      };
      const bend = (q() - 0.5) * 0.22, len = 0.62 + 0.28 * q(), wr = sp * (0.07 + 0.04 * q());
      if (q() < 0.85) fente(0.04, 0, len, bend * 0.5 + tipT * 0.5, wr, bend);
      // les barbes : de chaque côté, parallèles entre elles et penchées vers la pointe, plus courtes vers le bout,
      // avec un espacement et un départ propres à chaque côté
      for (const sd of [-1, 1]) {
        const n = 1 + Math.floor(q() * 3.2), s0 = 0.14 + q() * 0.12, gap = (len - s0 - 0.08) / Math.max(1, n), ang = 0.34 + q() * 0.14;
        for (let k = 0; k < n; k++) {
          const s = s0 + k * gap + (q() - 0.3) * gap * 0.35, lf = 1 - 0.45 * (s / len), mid = bend * (s / len) * 0.8;
          fente(s, mid + sd * 0.03, s + (0.13 + 0.07 * q()) * lf, mid + sd * ang * lf, wr * (0.55 + 0.25 * q()), sd * 0.03);
        }
      }
      // une encoche à la pointe, de temps en temps : la plume devient pétale
      if (q() < 0.28) { g.beginPath(); g.moveTo(X(1.02, tipT), Y(1.02, tipT)); g.lineTo(X(0.82, tipT * 0.5 + (q() - 0.5) * 0.1), Y(0.82, tipT * 0.5)); _cutStroke(g, !!only, T.bg, sp * 0.05); }
      if (crescent) {
        const c0 = 0.74 + q() * 0.06;
        g.beginPath(); g.moveTo(X(c0, -0.28), Y(c0, -0.28)); g.quadraticCurveTo(X(0.99, tipT), Y(0.99, tipT), X(c0, 0.3), Y(c0, 0.3));
        g.quadraticCurveTo(X(c0 + 0.1, tipT * 0.5), Y(c0 + 0.1, tipT * 0.5), X(c0, -0.28), Y(c0, -0.28)); g.closePath();
        g.fillStyle = _mix(col, 'W', 0.3); g.fill();
      }
    };
    for (const f of F) {
      if (S.filtre && !S.filtre(f.x, f.y)) continue;   /* v90 : le film de la pousse ne recalcule que le disque qui change */
      const b = f.p ? bands(f.t + (f.r2 - 0.5) * 0.05) : -1;
      if (only && (f.p !== only || b < 0)) continue;
      const col = b < 0 ? T.mat[Math.floor(f.r1 * 4)] : b === 2 ? T.ink : b === 1 ? T.cols[f.p.ci2] : T.cols[f.p.ci];
      const core = f.p && f.t < 0.45;
      PL(b >= 0 ? f.p.h : null, f, col, sp * 1.85 * f.sc, sp * 1.02 * f.sc * (0.82 + 0.4 * ((f.r2 * 5.13) % 1)), f.sc > 1.05 && !core, b >= 0 && b !== 2, core ? 'ink' : false);
    }
    const _pt2 = S.prof ? performance.now() : 0; if (S.prof) { S.prof.champ += _pt1 - _pt0; S.prof.plumes += _pt2 - _pt1; S.prof.n += F.length; }
    // le cœur : une rosette de petites plumes, posée par-dessus, qui comble le centre de l'œil
    for (const p of S.pr) {
      if (only && p !== only) continue;
      if (S.filtreOeil && !S.filtreOeil(p)) continue;
      const tS = p.tS == null ? 1 : p.tS;   /* v90 : la rosette d'un œil qui pousse grandit avec lui (film de la pousse seulement) */
      // le cœur : l'œil se développe depuis son centre — des plumes minuscules au milieu, qui partent vers
      // l'extérieur en spirale (angle d'or) et grandissent à mesure qu'elles s'en écartent ; les plus proches
      // du centre sont peintes en dernier, par-dessus, comme les pétales d'un bouton
      const q = _lcg((p.h ^ 0xc0e) >>> 0), Rc = p.R * ez.get(p) * (0.5 + 0.08 * q()), m = 200 + Math.floor(q() * 40), a0 = q() * 6.283;
      const tuft = [];
      for (let k = 0; k <= m; k++) {
        // plus dense au centre (r ∝ t^0,72), des feuilles plus petites et plus variées là, toujours en forme de feuille
        const t = k / m, r = Rc * Math.pow(t, 0.72) * 0.92, a = a0 + k * 2.39996;
        const d = a + (q() - 0.5) * 0.18, L = sp * (0.24 + 1.45 * t) * (0.65 + 0.7 * q()) * tS, Wd = L * (0.52 + 0.14 * q()), back = t < 0.35 ? 0.42 : 0.3;
        const col = t < 0.1 ? T.ink : t < 0.45 ? (q() < 0.75 ? T.cols[p.ci] : T.ink) : (q() < 0.7 ? T.cols[p.ci2] : T.cols[p.ci]);
        // la base de chaque plume recule un peu vers le centre : les plus petites s'y rejoignent sans laisser de jour
        tuft.push({ f: { x: p.x + Math.cos(a) * r - Math.cos(d) * L * back, y: p.y + Math.sin(a) * r - Math.sin(d) * L * back, vx: Math.cos(d), vy: Math.sin(d), r1: q() }, L, Wd, col, t });
      }
      // le tout premier cœur : six feuilles minuscules qui partent du centre même, dans tous les sens
      for (let k = 0; k < 6; k++) { const d = a0 + k * 1.047 + (q() - 0.5) * 0.4, L = sp * (0.48 + 0.12 * q()) * tS; tuft.unshift({ f: { x: p.x - Math.cos(d) * L * 0.35, y: p.y - Math.sin(d) * L * 0.35, vx: Math.cos(d), vy: Math.sin(d), r1: q() }, L, Wd: L * 0.7, col: T.ink, t: 0 }); }
      // les petites plumes restent lisibles : chacune garde sa découpe, sauf les toutes premières au cœur
      // un fond plein sous le cœur : le polygone des pointes des premières plumes, dans l'ordre de leurs angles —
      // irrégulier comme la touffe elle-même, il bouche tous les interstices
      // sous-couche dans la couleur de l'œil (ni noire, ni ronde) : les premières feuilles, peintes 1,4× plus larges,
      // sans découpe — elle bouche les derniers interstices
      // ⚑ v68 — la spec (VRAIS-MONDES-SPEC, Ramage) : « le centre de l'œil est toujours plein : un fond d'encre sous la touffe centrale,
      // qui suit la pointe des feuilles et n'est jamais un cercle ». Quand l'œil est très grand (peu de paroles), la touffe s'écarte et le
      // papier perçait au milieu — le défaut que NUANCES interdit. À la densité de la planche, ce fond reste caché sous les plumes.
      (Q ? (fn) => Q.push(fn) : (fn) => fn())(() => { g.eye = p.h; const pointes = tuft.filter(t => t.t < 0.3).map(t => [t.f.x + t.f.vx * t.L, t.f.y + t.f.vy * t.L]).sort((a, b) => Math.atan2(a[1] - p.y, a[0] - p.x) - Math.atan2(b[1] - p.y, b[0] - p.x));
        if (pointes.length > 2) { g.beginPath(); g.moveTo(pointes[0][0], pointes[0][1]); for (let z = 1; z < pointes.length; z++) g.lineTo(pointes[z][0], pointes[z][1]); g.closePath(); g.fillStyle = T.ink; g.fill(); } });
      tuft.filter(t => t.t < 0.3).forEach(t => PL(p.h, t.f, T.cols[p.ci], t.L * 1.1, t.Wd * 1.4, false, false, true));
      // certaines petites feuilles portent leurs nervures, comme les grandes
      // quelques petites feuilles portent un veinage épars, comme les grandes — tracé dans un ton plus sombre de la feuille,
      // jamais en clair : le centre reste plein
      tuft.reverse().forEach(t => {
        const vein = t.t >= 0.5 ? null : (t.t > 0.12 && t.f.r1 < 0.3 ? _mix(t.col, T.ink, 0.5) : null);
        PL(p.h, t.f, t.col, t.L, t.Wd, (t.t >= 0.5 && t.L > sp * 0.55) || !!vein, false, t.t < 0.4 ? 'ink' : false, vein);
      });
    }
  }

  /* ---------------- II · CHINÉ — la chaîne teinte avant tissage ---------------- */  /* ================= fin du code de la planche ================= */

  // au repos, une position reste gelée (v67 : à 40 paroles le moteur ne se pose pas, le plumage se refaisait à chaque image)
  var _gel = {};
  function _geler(L) { var tol = (env.uMat || 70) * 0.25, vive = env.vive, tr = env.trans;
    L.forEach(function (e) { var k = e.h, f = _gel[k]; if (vive && tr) { _gel[k] = [e.x, e.y]; return; }
      if (f && Math.abs(e.x - f[0]) < tol && Math.abs(e.y - f[1]) < tol) { e.x = f[0]; e.y = f[1]; } else if (vive) _gel[k] = [e.x, e.y]; }); }
  function _liste(now) { var L = [], i, s, n = seeds.length, perte = 0;
    for (i = 0; i < n; i++) { s = seeds[i]; if (s.kind === 'gray') continue; var f = _fac(s, now); perte += 1 - f;
      L.push({ s: s, h: _cle(s), x: s.x, y: s.y, f: f }); }   // la position de REPOS (contrat §7.1 : le frémissement est facultatif)
    var u = avg() * Math.sqrt(Math.max(1, n) / Math.max(1, n - perte));
    _geler(L);
    L.sort(function (a, b) { return a.h - b.h; });
    L = L.filter(function (p) { return p.f > 0.001; });   // puis on numérote : les jetons P/N se lisent par le rang DANS cette liste
    L.forEach(function (p, i2) { var z = _lcg((p.h ^ 0x5eed) >>> 0)(); p.R = u * (0.36 + 0.2 * z + 0.26 * z * z * z) * window._tailleApercu(p.s) * Math.max(p.f, 1e-3); p.ci = 2 * i2; p.ci2 = 2 * i2 + 1; });
    return { L: L, u: u };
  }
  function _T(L) { var cols = []; L.forEach(function (p, i) { cols.push('P' + i, 'N' + i); }); return { cols: cols, mat: ['M0', 'M1', 'M2', 'M3'], ink: 'I', bg: 'B' }; }
  var _plumages = {}, _nPl = [], _mainC = {}, _mainK = [];   // v72 : les dalles seules (64) et les plumages de la Toile (3), par ordre d'entrée
  function _garde(P) { if (!_mainC[P.h]) { _mainC[P.h] = P; _mainK.push(P.h); } while (_mainK.length > 3) delete _mainC[_mainK.shift()]; }
  function _cache(P) { if (_mainC[P.h] && !!_mainC[P.h].borne !== !!P.borne) { _mainC[P.h] = P; return; } _garde(P); }   /* v90 : un plumage d'un autre mode est remplacé, jamais gardé à sa place */
  function _fait(R, L, h) { var P = { ops: R.ops, L: L, b: R.b, h: h }, vus = {}; P.toks = []; R.ops.forEach(function (o) { if (!vus[o[2]]) { vus[o[2]] = 1; P.toks.push(o[2]); } }); return P; }
  function _plumage(now, only) {
    var K = env.uMat / UPL; L3 = 300 * K;
    var A = _liste(now), h = 2166136261; function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(K * 4096)); mix(env.cleToile == null ? 0 : env.cleToile); mix(only ? only : 0);
    A.L.forEach(function (p) { mix(p.h); mix(Math.round(p.x * 2)); mix(Math.round(p.y * 2)); mix(Math.round(p.R * 8)); });
    if (_plumages[h]) return _plumages[h];
    var R = _enreg(), S = { pr: A.L, g: (env.cleToile == null ? 1 : env.cleToile) };
    if (!only && _mainC[h] && !_mainC[h].borne) return _mainC[h];
    var cible = null; if (only) A.L.forEach(function (p) { if (p.h === only) cible = p; });
    if (only && !cible) return null;
    _parure(R, S, _T(A.L), cible || undefined);
    var P = _fait(R, A.L, h);
    if (!only) _cache(P); else { _plumages[h] = P; _nPl.push(h); if (_nPl.length > 64) delete _plumages[_nPl.shift()]; }
    return P;
  }
  // un jeton → une couleur (ou le papier du moteur)
  var _fin = false;   // v72 : vrai pendant qu'on résout les couleurs d'un calque — la couleur ACQUISE (fin de son allumage, 760 ms)
  function _col(s, now) { if (_fin && s.tOut == null && s.t0 != null && now < s.t0 + 761) now = s.t0 + 761; return cOf(s, now); }
  function _resout(tok, L, now, pap, rm) {
    if (tok === 'I') return _rgb(_encre());
    if (tok === 'B') return pap;
    if (tok === 'W') return 'W';
    var c0 = tok.charAt(0);
    if (c0 === 'M') return _rgb(rm[+tok.slice(1) % rm.length]);
    if (c0 === 'P') return _rgb(_col(L[+tok.slice(1)].s, now));
    if (c0 === 'N') return _rgb(_nuance(_col(L[+tok.slice(1)].s, now)));
    if (c0 === 'X') { var q = tok.split('|'), a = _arr(_brut(q[1], L, now, rm)), t = +q[3];
      var CANAL = 255, b = q[2] === 'W' ? a.map(function () { return CANAL; }) : _arr(_brut(q[2], L, now, rm));   // 'W' : vers la pleine clarté (la borne d'un canal) — une nuance de la couleur de la plume
      return _rgb([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]); }
    return pap;
  }
  function _brut(tok, L, now, rm) { var c0 = tok.charAt(0);
    if (tok === 'I') return _encre(); if (c0 === 'M') return rm[+tok.slice(1) % rm.length];
    if (c0 === 'P') return _col(L[+tok.slice(1)].s, now); if (c0 === 'N') return _nuance(_col(L[+tok.slice(1)].s, now));
    return _arr(env.fondToile()); }
  function _rejoue(P, now) {
    g.lineCap = 'butt'; g.lineJoin = 'miter';   // v72 : les réglages de la planche — sans eux le trait héritait de ceux du peintre précédent (mesuré : 6 à 8 % des pixels)
    var pap = typeof env.papier === 'function' ? env.papier() : (typeof env.fondToile === 'function' ? _rgb(_arr(env.fondToile())) : null);
    var rm = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, memo = {};
    for (var i = 0; i < P.ops.length; i++) { var o = P.ops[i], st = memo[o[2]] || (memo[o[2]] = _resout(o[2], P.L, now, pap, rm));
      if (o[4] !== 'source-over') g.globalCompositeOperation = o[4];
      if (o[0]) { g.strokeStyle = st; g.lineWidth = o[3]; g.stroke(o[1]); } else { g.fillStyle = st; g.fill(o[1]); }
      if (o[4] !== 'source-over') g.globalCompositeOperation = 'source-over'; }
  }
  var _dernier = null; window._ramDernierP = function () { return _dernier; };
  window._ramGraine = function (pid) { var s = null; seeds.forEach(function (q) { if (q.pid === pid) s = q; }); if (!s) return null; var F = null; try { F = env.finale; } catch (_) {} var f = F ? F.get(s) : null;
    return { x: Math.round(s.x), y: Math.round(s.y), tx: s.tx != null ? Math.round(s.tx) : null, ty: s.ty != null ? Math.round(s.ty) : null, fin: f ? [Math.round(f[0]), Math.round(f[1])] : null, trans: !!env.trans, W: W, H: H }; };
  window._ramEtats = function () { var now = performance.now(), A = _etatRepos(now), B = _etatFinal(), m = function (E) { var r = 0; E.L.forEach(function (p) { r += p.R; }); return +(r / Math.max(1, E.L.length)).toFixed(2); };
    return { avg: +avg().toFixed(2), seeds: seeds.length, gris: seeds.filter(function (s) { return s.kind === 'gray'; }).length, repos: { n: A.L.length, R: m(A) }, fin: { n: B.L.length, R: m(B) }, trans: !!env.trans, K: A.K, uMat: env.uMat, Rs: A.L.map(function (p) { return Math.round(p.R); }).join(','), Rvus: (_dernier ? _dernier.L.map(function (p) { return Math.round(p.R); }).join(',') : ''), rm: JSON.stringify(typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat), pap: typeof env.papier === 'function' ? env.papier() : null, tailleAp: window._tailleApercu(seeds[0]) }; };
  // (la preuve `_v72SansCalque` : le même plumage que le calque, peint directement)
  function RramDirect(now) { var P = (env.vive && window._v72SansCalque) ? _plumeDe(_cible(now)) : _plumage(now, 0); g.save(); _rejoue(P, now); g.restore(); _dernier = P; window._ramComp = { ops: P.ops.length, yeux: P.L.length }; }
  /* ⚑ v72 (passe de budget, Tom) — LE PLUMAGE SE PEINT UNE FOIS, DANS UN CALQUE, ET SE POSE 1:1. Ramage rejouait ~30 000 tracés
     (3 paroles) à ~49 000 (40) à CHAQUE image : 210 à 570 ms en Chromium, 1 à 3 s en WebKit. Le plumage est fixe au repos : on le
     peint dans un calque de la taille du canevas, avec la transformation du canevas (le fond du moteur d'abord, puis les tracés
     dans le même ordre, le papier compris) — et on repose ce calque tel quel, au pixel. Il se refait si la vue, le plumage ou une
     couleur changent.
     ⚠ LA TRANSITION CHANGE (à valider par Tom) : elle ne peut pas suivre les graines image par image — un seul plumage coûte
     plusieurs centaines de millisecondes. À la plantation, le plumage d'ARRIVÉE (places finales du moteur, `env.finale`, couleurs
     acquises) se peint PAR TRANCHES pendant que l'ancien reste affiché, puis passe sur lui en fondu (ARR = 900 ms). Au repos, ce
     plumage d'arrivée reste (§15.14), tant que les graines ne s'en écartent pas de plus que le gel.
     `_perfAncien`, l'export (DPR > 3), les aperçus, la dalle seule : le chemin direct, inchangé. */
  var _vS = null, _vJ = null, _vF = null, _vTr = null, _vAppel = 0;
  /* ⚑ v75 — L'APERÇU DU STUDIO (`window._apImage`) : son cycle ne visite que deux ou trois plumages (le repos, l'arrivée, le départ) ;
     on en garde les calques (clé : le semis et l'étape, quatre au plus) ; une arrivée préparée d'avance (`prepare`) passe en fondu DÈS SA PREMIÈRE IMAGE. La Toile
     vivante n'y touche pas : sans `_apImage`, rien ne change. */
  var _calC = [], _pJ = null, _aJ = null, _aS = null, _aF = null, _aK = null;
  function _calGarde(S) { for (var i = _calC.length - 1; i >= 0; i--) if (_calC[i].K === S.K) _calC.splice(i, 1); _calC.push(S); if (_calC.length > 4) _calC.shift(); }
  function _calAp(K, ms, cw, ch, now) { for (var i = _calC.length - 1; i >= 0; i--) { var e = _calC[i]; if (e.K === K && e.ms === ms && e.cw === cw && e.ch === ch && _tons(e.P, now).sig === e.tsig) return e; } return null; }
  function _calDe(J, K) { return { K: K, sem: K.split('|')[0], plein: J.C.plein, cv: J.C.cv, M: J.M, ms: J.ms, P: J.P, tsig: J.tons.sig, cw: J.cw, ch: J.ch }; }
  // l'aperçu : la clé est l'ÉTAPE du cycle (« n°semis|repos » ou « n°semis|arrivee »), que le moteur publie (window._apPhase)
  function RramAp(now, t, M, ms, cv0) {
    var K = window._apPhase || '0|repos', sem = K.split('|')[0], Kb0 = window._apPhaseBase || (sem + '|repos'), repos = (K === Kb0), cw = cv0.width, ch = cv0.height, veut = _calAp(K, ms, cw, ch, now);
    if (window._ramFilmDbg) { var _lg2 = window._ramCtLog = window._ramCtLog || []; var _e2 = ["vu", K, Kb0, env.cleToile, env.uMat, W, H]; if (!_lg2.length || _lg2[_lg2.length - 1].join() !== _e2.join()) _lg2.push(_e2); }
    if (!veut) {
      if (!_aS || _aS.sem !== sem || _aS.ms !== ms) {   // rien de cette Toile à montrer : le repos, d'un bloc (le premier passage, sans préparation)
        var Kb = Kb0, Cb = _calAp(Kb, ms, cw, ch, now);
        if (!Cb) { var Eb = _etatFinal(), Pb = _plumeDe(Eb), tb = performance.now(), Tb = _tons(Pb, now), C0 = _calque(Pb, Tb, M, cw, ch); _tranche(C0, 1e9, tb);
          Cb = { K: Kb, sem: sem, plein: C0.plein, cv: C0.cv, M: M, ms: ms, P: Pb, tsig: Tb.sig, cw: cw, ch: ch }; _calGarde(Cb); window._ramCalque = { direct: ((window._ramCalque || {}).direct || 0) + 1, ms: Math.round(performance.now() - tb) }; }
        _aS = Cb; _aF = null; if (repos) veut = Cb; }
      if (!veut) {   // l'arrivée se construit par tranches, ce qu'on voit reste ; puis le fondu
        var _cwA = (!window._ramPleinSansWorker && _filmPool()) ? _calDemande(_etatFinal(), K, ms, M, cw, ch, now) : false;   /* v91 : par le Worker */
        if (_cwA) { veut = _cwA; _calGarde(veut); } else if (_cwA === null) window._mondeEncore = true; else {
        if (!_aJ || _aJ.K !== K || _aJ.ms !== ms) { _aJ = _travail(_etatFinal(), now, M, cw, ch, ms); _aJ.K = K; _aJ.pousse = true; }   /* v87 : construit à part, jamais montré en cours */
        var dt = t - (RramAp.t || t); RramAp.t = t; var budget = Math.max(4, Math.min(9, (dt > 0 && dt < 200 ? dt : 16.7) * 0.5));
        /* v87 : comme sur la Toile — le glissé part dès que les plumes sont enregistrées et la matière peinte ; l'exact se construit
           ensuite, une fois tout immobile */
        var _jg = !!(_aK && _aK.Vjob === _aJ), _pause = _jg && (_aK.att ? !!_aK.Pn : _gBouge(_aK, t)), _petit = _pause && !_aK.att && dt > 0 && dt < 20;
        if ((!_pause || _petit) && _avance(_aJ, now, _petit ? 3 : budget, dt || 16.7)) { veut = _calDe(_aJ, K); _calGarde(veut); window._ramCalque = { travail: Math.round(_aJ.t), images: _aJ.n }; if (_jg) { _aK.pret = veut; _aK.V = veut; } _aJ = null; }
        else window._mondeEncore = true;
        if (false && _aJ && !_jg && _aJ.P && _aS && _aS.sem === sem && _aS.ms === ms && _aS.sprOk && _fondPret(ms) && !(_aK && _gActif(_aK))) {
          _aK = { base: _aS, items: [], attente: [], Vjob: _aJ }; _gAttend(_aK, _aJ.P, _aJ.P, _aK, _fondPret(ms)); } } } }
    RramAp.t = t;
    _aF = null;
    if (veut && !veut.film && _filmsK[K + '|' + ms]) veut.film = _filmsK[K + '|' + ms];
    if (window._ramToileAp && veut && veut !== _aS && !(_aK && _aK.V === veut) && veut.film && !_filmAssez(veut.film) && !veut.film.echec) { window._mondeEncore = true; veut = null; }   /* v92 : sur la Toile, pas de pousse sans son film */
    /* v87 : l'état voulu est prêt — les yeux qui arrivent poussent sur ce qu'on voit, ceux qui partent se résorbent sur l'exact */
    if (veut && (_aK ? _aK.V !== veut : veut !== _aS)) {
      if (window._ramDbgOn) (window._ramDbg = window._ramDbg || []).push({ t: Math.round(t), K: K, base: _aS ? _aS.P.L.map(function (e) { return [e.h % 1000, Math.round(e.x), Math.round(e.y), Math.round(e.R)]; }) : null, baseK: _aS && _aS.K, veut: veut.P.L.map(function (e) { return [e.h % 1000, Math.round(e.x), Math.round(e.y), Math.round(e.R)]; }), veutK: veut.K, sem: [_aS && _aS.sem, veut.sem, _aS && _aS.ms === ms] });
      if (!_aS || _aS.sem !== veut.sem || _aS.ms !== ms) { _aS = veut; _aK = null; }
      else { var _Fa = _fondPret(ms);
        if (false && !(_aK && _gActif(_aK)) && _Fa && _aS.sprOk) { _aK = { base: _aS, items: [], attente: [], sprN: veut }; _gAttend(_aK, veut.P, veut.P, veut, _Fa); _gAttente(_aK, t, now, cw, ch, 6); }   /* v89 : au Studio les yeux restent en place — plus de glissé */
        else { if (!_aK) _aK = { base: _aS, items: [], attente: [] }; _gCible(_aK, veut.P, t, now); }
        _aK.pret = veut; _aK.V = veut; } }
    if (_aK) { _gAttente(_aK, t, now, cw, ch, 6); var _cuitAv = _aK.cuit; if (_gPas(_aK, t)) window._mondeEncore = true;
      if (_aK.cuit && !_cuitAv) { var _cb = _aK.pret || _aK.base; if (_cb.cuit && !_cb.K) { _cb.K = K; _cb.sem = sem; _calGarde(_cb); } if (_aJ && _aK.Vjob === _aJ) _aJ = null; }
      _aS = _aK.base; if (!_gActif(_aK) && !_aK.pret) _aK = null; }
    var _pret = true;
    if (false && !_aK && !_aJ && _aS && _aS.ms === ms) { var _pr = _fondAvance(ms, M, cw, ch, now, 8) && _sprAvance(_aS, now, 8); _pret = _pr;   /* v89 : plus de glissé au Studio, plus d'empreintes à préparer */   /* v87 : l'aperçu est immobile — un budget plus large */
      if (_pr) _calC.forEach(function (e) { if (_pr && e !== _aS && e.ms === ms && e.P) { if (!e.mat && !_matAvance(e, e.P, e.M, cw, ch, now, 8)) _pr = false; else if (e.mat && !_sprAvance(e, now, 8)) _pr = false; } });   /* la matière et les empreintes des états prêts d'avance */
      if (!_pr) window._mondeEncore = true; }
    /* le prochain événement attend que le mouvement en cours soit fini ET que les empreintes de ce qu'on voit soient prêtes : sans
       elles l'arrivée ne peut que sauter (au premier événement, le moteur relâche toutes les graines vers les bords) */
    if (_aS) _apGelDe(_aS);
    window._apOccupe = !!_aK; window._ramBouge = !!_aK;   /* v89 : sans glissé, plus besoin d'attendre les empreintes */
    window._ramAp = { K: K, pousse: _aK ? _aK.items.length : 0, job: _aJ && _aJ.C ? Math.round(100 * _aJ.C.i / Math.max(1, _aJ.C.P.ops.length)) : null };
    g.save();
    if (_aK) _gDessine(_aK, M, t); else _pose(_aS, M);
    g.restore();
    _dernier = _aS.P; window._ramComp = { ops: (_aS.P.ops || []).length, yeux: _aS.P.L.length, apercu: K };
  }
  // un ÉTAT du plumage : ses yeux (places, rayons, rangs) et sa signature — sans le tracer
  function _hEtat(L, K, fin) { var h = 2166136261; function mix(v) { h ^= (v | 0); h = Math.imul(h, 16777619) >>> 0; }
    mix(Math.round(W)); mix(Math.round(H)); mix(Math.round(K * 4096)); mix(env.cleToile == null ? 0 : env.cleToile); mix(fin ? 0x7a2 : 0);
    L.forEach(function (p) { mix(p.h); mix(Math.round(p.x * 2)); mix(Math.round(p.y * 2)); mix(Math.round(p.R * 8)); }); return h; }
  function _etatRepos(now) { var K = env.uMat / UPL, A = _liste(now); return { L: A.L, K: K, h: _hEtat(A.L, K, false) }; }
  var _apGel = null;   /* v89 : les places des yeux de l'aperçu (par semis), gelées d'un état à l'autre */
  function _apGelDe(C) { if (!C || !C.P || !C.P.L) return; var sem = String(C.sem || (C.K || '').split('|')[0]); if (_apGel && _apGel.sem === sem && _apGel.P === C.P) return;
    var pos = (_apGel && _apGel.sem === sem) ? _apGel.pos : {}; var vus = {}; C.P.L.forEach(function (e) { pos[e.h] = [e.x, e.y, e.R]; vus[e.h] = 1; });
    _apGel = { sem: sem, pos: pos, P: C.P }; }
  /* ⚑ v98 (Tom : 500 paroles) — le budget de Chamade : le point fixe du moteur se recalcule dès qu'une graine bouge ; quand il a
     coûté plus de 40 ms, la réponse précédente sert pendant quatre fois ce coût, et le moteur est relancé pour revenir la demander. */
  var _rfC = null, _rfCout = 0, _rfFin = 0;
  function _finR() { if (_rfC && _rfCout > 40 && performance.now() - _rfFin < _rfCout * 4) { if (typeof env.relance === 'function') env.relance(); return _rfC; }
    var t0 = performance.now(), F = null; try { F = env.finale; } catch (_) { F = null; }
    var dt = performance.now() - t0; if (dt > 5 || !_rfC) { _rfC = F; _rfFin = performance.now(); _rfCout = dt; } else if (F !== _rfC) { _rfC = F; _rfCout = dt; } return F; }
  function _etatFinal() { var K = env.uMat / UPL, F = _finR();
    var L = [], i, s, n = seeds.length;   // l'état d'arrivée : places finales du moteur, paroles entières, départs exclus
    var partent = 0, gel = ((window._apImage || window._ramToileAp) && _apGel && _apGel.sem === String(window._apPhase || '').split('|')[0]) ? _apGel.pos : null;
    for (i = 0; i < n; i++) { s = seeds[i]; if (s.kind === 'gray') continue; if (s.part != null) { partent++; continue; } var q = F ? F.get(s) : null, hq = _cle(s), gq = gel ? gel[hq] : null;
      if (gq) q = gq;   /* ⚑ v89 — au Studio, un œil qui reste garde SA place : l'événement n'est qu'une dalle qui pousse ou se résorbe */
      L.push({ s: s, h: hq, x: q ? q[0] : s.x, y: q ? q[1] : s.y, f: 1 }); }
    /* ⚑ v87 — la MÊME unité que le repos (`_liste` : √(n / (n − départs)), n comptant les graines grises). On divisait par le seul
       nombre de paroles : dans un semis à cellules grises (l'aperçu du Studio, 68 graines pour ~12 paroles) les yeux d'arrivée
       sortaient 2,4 fois plus grands que ceux du repos — chaque aller-retour sautait (la construction de la v84 le cachait). */
    var u = avg() * Math.sqrt(Math.max(1, n) / Math.max(1, n - partent));
    L.sort(function (a, b) { return a.h - b.h; });
    L.forEach(function (p, i2) { var z = _lcg((p.h ^ 0x5eed) >>> 0)(); p.R = u * (0.36 + 0.2 * z + 0.26 * z * z * z) * window._tailleApercu(p.s); p.ci = 2 * i2; p.ci2 = 2 * i2 + 1;
      if (gel && gel[p.h] && gel[p.h][2]) p.R = gel[p.h][2]; });   /* v89 : et SA taille — l'unité (avg) change à chaque événement, tous les yeux changeaient de taille à l'échange */
    return { L: L, K: K, h: _hEtat(L, K, true), fin: true, W: W, H: H, ct: env.cleToile }; }
  /* le plumage d'arrivée RESTE au repos tant que les mêmes paroles sont là, sur la même Toile (§15.14, comme Chamade, Guingois,
     Volubilis) — le moteur ne se pose pas exactement aux places annoncées (mesuré : une graine à 100 px) ; refaire le plumage sur
     ses places réelles, c'était un second fondu, une seconde après le premier */
  function _reste(E) { if (E.W !== W || E.H !== H || E.ct !== env.cleToile) return false; var n = 0, par = {}, i, s; E.L.forEach(function (e) { par[e.h] = 1; });
    for (i = 0; i < seeds.length; i++) { s = seeds[i]; if (s.kind === 'gray' || s.part != null) continue; n++; if (!par[_cle(s)]) return false; }
    return n === E.L.length; }
  function _cible(now) { var TR = env.trans;
    if (TR) { if (!_vTr || _vTr.n !== TR.n) _vTr = { n: TR.n, E: _etatFinal() }; return _vTr.E; }
    if (_vTr && _reste(_vTr.E)) return _vTr.E;
    _vTr = null; var E = _etatRepos(now); _geleEtat = E; return E; }
  var _geleEtat = null;
  function _borneM() { return (!!window._apImage || !!window._ramToileAp) && !window._ramFilmOff; }   /* v90 : un plumage à poussée bornée (Studio) n'est jamais celui d'un autre mode */
  function _mainDe(h) { var P = _mainC[h]; return P && !!P.borne === _borneM() ? P : null; }
  function _plumeDe(E) { var P0 = _mainDe(E.h); if (P0) return P0; L3 = 300 * E.K; var R = _enreg();   // tout de suite (pas de calque encore)
    _parure(R, { pr: E.L, g: (env.cleToile == null ? 1 : env.cleToile) }, _T(E.L), undefined); var P = _fait(R, E.L, E.h); P.borne = _borneM(); _cache(P); return P; }
  function _tons(P, now) { var rm = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, m = {}, sig = [];
    _fin = true; try { P.toks.forEach(function (t) { if (t === 'B') return; var c = _resout(t, P.L, now, null, rm); m[t] = c; sig.push(c); }); } finally { _fin = false; }
    return { m: m, sig: (env.isLightM() ? 'c' : 's') + sig.join('|') }; }
  function _calque(P, tons, M, cw, ch, nu, centre) {   // un calque à peindre : le fond du moteur, puis les tracés (par tranches) — v81 : `nu`, sans le fond
    var cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
    var G = cv.getContext('2d'); G.setTransform(M.a, M.b, M.c, M.d, M.e, M.f);
    var pap = typeof env.papier === 'function' ? env.papier() : null;
    if (pap && !nu) { G.fillStyle = pap; G.fillRect((0 - M.e) / M.a - 2, (0 - M.f) / M.d - 2, cw / M.a + 4, ch / M.d + 4); }
    /* ⚑ v74 (Tom : « refais l'image nette dès que le pincement s'arrête ») — le calque ne peint que les plumes qui TOUCHENT la zone
       vue, plus une marge de 8 % de chaque côté. Une plume hors de cette zone ne dépose aucun pixel sur le canevas : le calque est le
       même. Au zoom ×2, ~34 % de la surface. Si la vue dépasse ensuite cette zone (un dézoom pendant le geste), le dernier calque ENTIER
       se pose dessous : jamais de trou. */
    var vw = cw / M.a, vh = ch / M.d, vx = (0 - M.e) / M.a, vy = (0 - M.f) / M.d, z = [vx - vw * 0.08, vy - vh * 0.08, vx + vw * 1.08, vy + vh * 1.08];
    return { cv: cv, G: G, P: P, tons: tons, pap: pap, i: 0, z: z, M: M, cw: cw, ch: ch, ordre: (nu && centre) ? _ordreRosaces(P, centre[0], centre[1]) : null, plein: z[0] <= 0 && z[1] <= 0 && z[2] >= W && z[3] >= H }; }
  /* ⚑ v81 (Tom : « le plumage se construit et se défait, plume par plume ; jamais de fondu ») — LE PLUMAGE SE CONSTRUIT SOUS LES YEUX.
     Le plumage neuf se peint PAR-DESSUS celui qu'on voit, tracé après tracé, dans l'ordre même de son dessin (l'ordre du peintre est
     gardé : chaque plume recouvre ce qu'elle doit recouvrir) ; quand le dernier tracé est posé, le papier passe DESSOUS
     (`destination-over`) et le calque est exactement celui qu'on aurait peint d'un bloc. Plus aucun fondu entre deux images. */
  var DUR_K = 1200;
  /* ⚑ v84 (Tom : « les plumes arrivent et se développent pour former la dalle ; la matière naît de la promesse et repousse ses voisines »)
     — LES ROSACES DEPUIS LA PROMESSE. Chaque tracé appartient à un œil (`o[5]` ; une plume du fond, à l'œil le plus proche). Les
     rosaces démarrent l'une après l'autre, la plus proche de la promesse d'abord (60 % du temps pour l'échelonnement), et se
     construisent chacune sur 40 % du temps DANS SON ORDRE DE DESSIN (chaque pétale recouvre ce qu'il doit). Entre deux rosaces qui se
     touchent, l'ordre du peintre change : le plumage fini n'est pas exactement le calcul — il est remplacé par l'exact à la fin (mesuré). */
  function _ordreRosaces(P, cx, cy) { var L = P.L, E = {}, i, n = P.ops.length; if (!L || !L.length || !n) return null;
    L.forEach(function (e) { E[e.h] = e; }); var dmax = 1; L.forEach(function (e) { var d = Math.hypot(e.x - cx, e.y - cy); if (d > dmax) dmax = d; });
    var grp = new Array(n), taille = {}, rang = new Int32Array(n);
    for (i = 0; i < n; i++) { var o = P.ops[i], e = o[5] != null ? E[o[5]] : null;
      if (!e) { var b = o[6], mx = b ? (b[0] + b[2]) / 2 : cx, my = b ? (b[1] + b[3]) / 2 : cy, bd = 1e18; for (var j = 0; j < L.length; j++) { var dd = (L[j].x - mx) * (L[j].x - mx) + (L[j].y - my) * (L[j].y - my); if (dd < bd) { bd = dd; e = L[j]; } } }
      grp[i] = e; var k = e.h; rang[i] = taille[k] || 0; taille[k] = rang[i] + 1; }
    var cle = new Float64Array(n), idx = new Array(n);
    for (i = 0; i < n; i++) { var g0 = grp[i], dep = Math.hypot(g0.x - cx, g0.y - cy) / dmax; cle[i] = dep * 0.6 + 0.4 * rang[i] / Math.max(1, taille[g0.h] - 1); idx[i] = i; }
    idx.sort(function (a, b) { return cle[a] - cle[b] || a - b; }); return idx; }
  function _papierDessous(C) { if (!C.pap) return; var G = C.G, M = C.M; G.save(); G.setTransform(M.a, M.b, M.c, M.d, M.e, M.f); G.globalCompositeOperation = 'destination-over';
    G.fillStyle = C.pap; G.fillRect((0 - M.e) / M.a - 2, (0 - M.f) / M.d - 2, C.cw / M.a + 4, C.ch / M.d + 4); G.restore(); }
  function _peintJusqua(C, fin, budget, t0) { var G = C.G, ops = C.P.ops, m = C.tons.m, i = C.i, Z = C.z, R = C.ordre; fin = Math.min(fin, ops.length);
    for (; i < fin; i++) { var o = ops[R ? R[i] : i], bx = o[6];
      if (Z && bx && (bx[2] < Z[0] || bx[0] > Z[2] || bx[3] < Z[1] || bx[1] > Z[3])) continue;
      var st = o[2] === 'B' ? C.pap : m[o[2]]; if (o[4] !== 'source-over') G.globalCompositeOperation = o[4];
      if (o[0]) { G.strokeStyle = st; G.lineWidth = o[3]; G.stroke(o[1]); } else { G.fillStyle = st; G.fill(o[1]); }
      if (o[4] !== 'source-over') G.globalCompositeOperation = 'source-over';
      if ((i & 31) === 31 && performance.now() - t0 > budget) { i++; break; } }
    C.i = i; return i >= ops.length; }
  // une construction rejouée (le plumage est déjà prêt) : la part des tracés suit le temps (DUR_K), au budget de l'image
  function _kAvance(K, t) { var n = K.C.P.ops.length, cible = Math.ceil(n * Math.min(1, (t - K.t0) / DUR_K));
    var fini = _peintJusqua(K.C, cible, 8, performance.now()); return fini && K.C.i >= n; }
  // ce qu'on voit (un calque, et une construction par-dessus) cuit en un seul calque : une construction interrompue ne recule jamais
  function _ecartCalques(a, b) { try { var w = Math.min(a.width, b.width), h = Math.min(a.height, b.height), x = a.getContext('2d').getImageData(0, 0, w, h).data, y = b.getContext('2d').getImageData(0, 0, w, h).data, n = 0;
      for (var i = 0; i < x.length; i += 4) if (Math.max(Math.abs(x[i] - y[i]), Math.abs(x[i + 1] - y[i + 1]), Math.abs(x[i + 2] - y[i + 2])) > 12) n++; return Math.round(10000 * n / (x.length / 4)) / 100; } catch (_) { return null; } }
  function _cuire(L, sur, M, cw, ch) { var cv = document.createElement('canvas'); cv.width = cw; cv.height = ch; var G = cv.getContext('2d');
    G.drawImage(L.cv, 0, 0); if (sur) G.drawImage(sur.cv, 0, 0); return { cv: cv, M: M, ms: L.ms, P: L.P, tsig: L.tsig, sem: L.sem, K: 'cuit', cw: cw, ch: ch, plein: L.plein }; }
  /* le pas d'une tranche se compte en TRACÉS et se règle sur la durée réelle des images : le temps de JavaScript ne dit pas ce que
     la rastérisation coûte ensuite (mesuré en Chromium : 9 ms de commandes, 70 à 120 ms d'image) */
  var _pasT = 200, _pasI = 1500;
  function _tranche(J, budget, t0, dt) { var G = J.G, ops = J.P.ops, m = J.tons.m, i = J.i;
    /* v74 — une Toile IMMOBILE qu'on refait nette (seule la vue a changé, et elle est posée) : rien ne bouge à l'écran, une image plus
       longue ne se voit pas — on vise ~45 ms par image au lieu de 16,7, pour que le net arrive vite (WebKit : un tracé y coûte ~5 fois plus) */
    if (budget < 1e8) { if (J.immobile) { if (dt > 60) _pasI = Math.max(300, _pasI * 0.6); else if (dt < 45) _pasI = Math.min(8000, _pasI * 1.5); }
      else if (dt > 21) _pasT = Math.max(100, _pasT * 0.5); else if (dt < 18.5) _pasT = Math.min(J.vue ? 1500 : 900, _pasT * 1.1); }   // v73 : plancher 100 (~0,6 ms en Chromium) — une image lente pour une autre raison (la page + qui se ferme) ne doit pas étirer la construction
    var reste = budget < 1e8 ? (J.pasFond ? 100 : Math.round(J.immobile ? _pasI : _pasT)) : 1e12, Z = J.z;
    for (; i < ops.length && reste > 0; i++) { var o = ops[i], bx = o[6];
      if (Z && bx && (bx[2] < Z[0] || bx[0] > Z[2] || bx[3] < Z[1] || bx[1] > Z[3])) continue;   // hors de la zone vue : rien à peindre
      reste--; var st = o[2] === 'B' ? J.pap : m[o[2]];
      if (o[4] !== 'source-over') G.globalCompositeOperation = o[4];
      if (o[0]) { G.strokeStyle = st; G.lineWidth = o[3]; G.stroke(o[1]); } else { G.fillStyle = st; G.fill(o[1]); }
      if (o[4] !== 'source-over') G.globalCompositeOperation = 'source-over';
      if ((i & 31) === 31 && performance.now() - t0 > budget) { i++; break; } }
    J.i = i; return i >= ops.length; }
  // un travail : enregistrer le plumage (ses plumes en file), puis le peindre dans son calque — le tout par tranches
  function _travail(E, now, M, cw, ch, ms) { var J = { E: E, ms: ms, M: M, cw: cw, ch: ch, P: _mainDe(E.h), t: 0, n: 0, borne: _borneM() };
    if (!J.P) { L3 = 300 * E.K; J.R = _enreg(); J.Q = []; J.qi = 0; J.Lx = E.L;
      _parure(J.R, { pr: E.L, g: (env.cleToile == null ? 1 : env.cleToile) }, _T(E.L), undefined, J.Q); }
    return J; }
  function _avance(J, now, budget, dt) { var t0 = performance.now(); J.n++;
    if (!J.P) { var Q = J.Q, i = J.qi; while (i < Q.length) { Q[i++](); if ((i & 15) === 0 && performance.now() - t0 > budget) break; } J.qi = i;
      if (i < Q.length) { J.t += performance.now() - t0; return false; }
      J.P = _fait(J.R, J.Lx, J.E.h); J.P.borne = J.borne; _cache(J.P); J.R = J.Q = null; }
    if (!J.C) { J.tons = _tons(J.P, now); J.C = _calque(J.P, J.tons, J.M, J.cw, J.ch, J.nu, J.centre); J.tC = performance.now(); J.C.vue = J.vue; J.C.immobile = J.immobile; J.C.pasFond = J.pasFond; J.neuf = true; }
    if (J.neuf) { J.neuf = false; J.t += performance.now() - t0; return false; }   // la tranche d'après, dans l'image suivante
    var cibK = Math.ceil(J.P.ops.length * Math.min(1, (performance.now() - J.tC) / DUR_K));
    var fini = J.nu ? (_peintJusqua(J.C, cibK, budget, t0) && J.C.i >= J.P.ops.length)   // v81 : une construction suit l'horloge (DUR_K)
      : J.pousse ? (_peintJusqua(J.C, J.P.ops.length, budget, t0) && J.C.i >= J.P.ops.length)   /* v87 : un plumage caché se peint au budget de TEMPS de l'image (le pas en tracés tombait à 100 sous WebKit : 30 s) */
      : _tranche(J.C, budget, t0, dt); J.t += performance.now() - t0; return fini; }
  /* ⚑ la VUE bouge pendant une plantation (le cadrage suit les graines : 0,1 % d'échelle et quelques dixièmes de pixel par image).
     Pendant qu'elle bouge, un calque se pose avec l'écart de vue (translation et échelle relatives, ≤ 1 % en pratique) ; dès qu'elle
     est posée (deux images identiques), il se refait EXACT, par tranches, et passe en fondu. Au repos : 1:1, au pixel. */
  /* ⚑ v87 (Tom, 28 sept. : « chaque dalle se déploie depuis son centre ; les plumes apparaissent au cœur, grossissent vers
     l'extérieur. Pas de vague, pas de fondu, pas de voile, pas de balayage. La dalle pousse. ») — UN ŒIL QUI ARRIVE POUSSE, UN ŒIL
     QUI PART SE RÉSORBE. Le plumage qu'on voit reste ; l'œil neuf est retracé EN VECTEUR (ses propres tracés, dans leur ordre) à
     l'échelle s autour de son centre, s de 0 à 1 (DUR_P) — rien n'est réduit en image, chaque image est tracée à sa taille. Quand il
     est entier et que le plumage exact est prêt, le plumage exact se pose (l'œil y est le même). Au départ, l'inverse : le plumage
     exact sans l'œil se pose, et l'œil qui part se retrace par-dessus, de 1 à 0. */
  var DUR_P = 1100;
  /* v89 — la CELLULE d'un œil : ses tracés et ceux de la matière qui lui reviennent (le plus proche en rayons, comme la planche attribue
     une plume à un œil) — c'est elle qui pousse ou se résorbe au Studio ; à pleine taille elle est le plumage exact de sa zone */
  function _celluleDe(P, k) { if (!P.ops) return []; var c = P.cel || (P.cel = {}); if (c[k]) return c[k]; var e = null, ops = [];
    for (var j = 0; j < P.L.length; j++) if (P.L[j].h === k) { e = P.L[j]; break; } if (!e) return (c[k] = _oeilDe(P, k));
    /* la ZONE d'influence de l'œil (la planche : poids 1,9·e^(−0,7·t²), t = d / (R·ez)) : ses tracés, ceux des voisins à moins de 1,3 t
       (leurs bandes s'y recoupent), la matière à moins de 2,2 t (elle s'y réoriente) — à pleine taille, tout ce que son arrivée change */
    var ez = 0.78 + 0.5 * _lcg((k ^ 0xe7e) >>> 0)(), Rz = Math.max(1, e.R * ez);
    P.ops.forEach(function (o) { if (o[5] === k) { ops.push(o); return; } var b = o[6]; if (!b) return;
      var t = Math.hypot((b[0] + b[2]) / 2 - e.x, (b[1] + b[3]) / 2 - e.y) / Rz;
      if (t < 1.3 || (o[5] == null && t < (window._ramZone || 2.2))) ops.push(o); });   /* v90 : 2,8 couvre la poussée bornée à 2,4 (plus la demi-plume) */
    return (c[k] = ops); }
  function _oeilDe(P, k) { if (!P.ops) return []; var c = P.oe2 || (P.oe2 = {}); if (c[k]) return c[k]; var ops = []; P.ops.forEach(function (o) { if (o[5] === k) ops.push(o); }); return (c[k] = ops); }
  function _gS(it, t) { var s = _lisse(Math.min(1, Math.max(0, (t - it.t0) / DUR_P))); return it.dir > 0 ? it.s0 + (1 - it.s0) * s : it.s0 * (1 - s); }
  function _gCible(G, P, t, now) { var dans = {}, avant = {}, pap = typeof env.papier === 'function' ? env.papier() : null, tn = null, tb = null;
    P.L.forEach(function (e) { dans[e.h] = e; }); G.base.P.L.forEach(function (e) { avant[e.h] = e; });
    var vieux = G.items; G.items = []; G.attente = [];
    vieux.forEach(function (it) { var s = _gS(it, t);
      if (it.dir > 0 && dans[it.k]) { tn = tn || _tons(P, now); it.e = dans[it.k]; it.ops = ((window._apImage || window._ramToileAp) ? _celluleDe : _oeilDe)(P, it.k); it.m = tn.m; it.bx = null; it.job = null; G.items.push(it); }
      else if (it.dir > 0) { if (s > 0.002) G.items.push({ k: it.k, e: it.e, ops: it.ops, m: it.m, pap: it.pap, t0: t, s0: s, dir: -1 }); }
      else if (s > 0.002) G.items.push(it); });
    P.L.forEach(function (e) { if (avant[e.h]) return; for (var i = 0; i < G.items.length; i++) if (G.items[i].k === e.h && G.items[i].dir > 0) return;
      tn = tn || _tons(P, now); G.items.push({ k: e.h, e: e, ops: ((window._apImage || window._ramToileAp) ? _celluleDe : _oeilDe)(P, e.h), m: tn.m, pap: pap, t0: t, s0: 0, dir: 1 }); });
    G.base.P.L.forEach(function (e) { if (dans[e.h]) return; tb = tb || _tons(G.base.P, now); G.attente.push({ k: e.h, e: e, ops: ((window._apImage || window._ramToileAp) ? _celluleDe : _oeilDe)(G.base.P, e.h), m: tb.m, pap: pap, s0: 1, dir: -1 }); });
    if ((window._apImage || window._ramToileAp) && !window._ramFilmOff) { var Fm = null; for (var q = _calC.length - 1; q >= 0; q--) if (_calC[q].P === P && _calC[q].film && _filmAssez(_calC[q].film) && _calC[q].film.de === G.base) { Fm = _calC[q].film; break; }
      if (window._ramFilmDbg) { var dbg = { calC: _calC.length, avecP: 0, film: 0, fini: 0, de: 0 }; _calC.forEach(function (e) { if (e.P === P) { dbg.avecP++; if (e.film) { dbg.film++; if (e.film.fini) dbg.fini++; if (e.film.de === G.base) dbg.de++; } } }); (window._ramFilmLog = window._ramFilmLog || []).push(dbg); }
      if (Fm) { Fm.enJeu = true; G.items.forEach(function (it) { var f = Fm.items[it.k + '+']; if (it.dir > 0 && !it.s0 && f && (f.fr.length || f.ss)) { it.film = f.fr; it.filmSs = f.ss; } });
        G.attente.forEach(function (it) { var f = Fm.items[it.k + '-']; if (f && (f.fr.length || f.ss)) { it.film = f.fr; it.filmSs = f.ss; } }); window._ramFilmUse = (window._ramFilmUse || 0) + 1; } }
    G.P = P; G.pret = null; }
  /* ⚑ v90 (Tom, 28 sept. : « Ramage au Studio avance encore par petites étapes : finis-le ») — LE FILM DE LA POUSSE, TRACÉ D'AVANCE.
     Une étape de pousse retrace toute la zone de l'œil (des centaines de tracés) : elle tenait sur plusieurs images, et on voyait 9 à
     17 images bouger sur 80, par sauts. Or au Studio l'événement suivant est connu d'avance (`apercuPrepareProchain`) : pendant le
     repos on trace CHAQUE étape, en vecteur, à SA taille (jamais une image agrandie ou réduite), une par image de la pousse (DUR_P) ;
     pendant le mouvement on pose l'étape de l'instant, 1:1. Même zone, mêmes tracés, mêmes échelles qu'avant — seulement à l'heure.
     Sans film prêt (première ouverture, un changement de vue), le chemin d'avant, par étapes, reste le secours. */
  /* ⚑ v91 (Tom : « tous les mondes au même intervalle ») — LE FILM SE CALCULE DANS UN WORKER. Le même code de la planche (`_parure`,
     `_enreg`, `_cutStroke`, `_mix`, `_T`, recopiés tels quels comme pour le jardin de Volubilis), les mêmes données (les yeux, les
     couleurs déjà résolues), la même géométrie de disque : chaque image revient toute faite (ImageBitmap) et se pose 1:1. Le fil
     principal ne paie plus que la pose — le film se prépare en même temps que tout le reste, dès que les yeux de l'arrivée sont connus.
     Sans Worker (ou s'il échoue) : le chemin d'avant, sur place. */
  var _FW = null, _FWN = 0, _FWJ = {}, _filmsK = {}, _FWP = null;
  function _filmPool() { if (_FWP !== null) return _FWP; var n = window._ramFilmPool || Math.max(1, Math.min(3, (navigator.hardwareConcurrency || 2) - 1)), P = [];
    for (var i = 0; i < n; i++) { _FW = null; var w = _filmWorker(); if (!w) break; P.push(w); } _FWP = P.length ? P : false; return _FWP; }
  function _filmWorker() { if (_FW !== null) return _FW; _FW = false; if (window._ramFilmSansWorker || typeof Worker === 'undefined' || typeof OffscreenCanvas === 'undefined') return false;
    try { var corps = [
        "function _rgbW(c){return 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';}",
        "function _brutW(t,C){if(t==='I')return C.I;var c0=t.charAt(0);if(c0==='M')return C.M[+t.slice(1)%C.M.length];if(c0==='P')return C.P[+t.slice(1)];if(c0==='N')return C.N[+t.slice(1)];return C.F;}",
        "function _resW(t,C,m){var v=m[t];if(v!==undefined)return v;if(t==='B')v=C.pap;else if(t==='I')v=_rgbW(C.I);else{var c0=t.charAt(0);if(c0==='M'||c0==='P'||c0==='N')v=_rgbW(_brutW(t,C));else if(c0==='X'){var q=t.split('|'),a=_brutW(q[1],C),b=q[2]==='W'?[255,255,255]:_brutW(q[2],C),k=+q[3];v=_rgbW([a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k,a[2]+(b[2]-a[2])*k]);}else v=C.pap;}m[t]=v;return v;}",
        "function _peint(c,ops,C,memo){for(var j=0;j<ops.length;j++){var o=ops[j],st=_resW(o[2],C,memo);if(o[4]!=='source-over')c.globalCompositeOperation=o[4];if(o[0]){c.strokeStyle=st;c.lineWidth=o[3];c.stroke(o[1]);}else{c.fillStyle=st;c.fill(o[1]);}if(o[4]!=='source-over')c.globalCompositeOperation='source-over';}}",
        "onmessage=function(ev){var d=ev.data;W=d.W;H=d.H;L3=d.L3;if(d.C&&d.C.pap&&typeof d.C.pap==='object'){var q=d.C.pap,gr=new OffscreenCanvas(1,1).getContext('2d').createLinearGradient(q.l[0],q.l[1],q.l[2],q.l[3]);gr.addColorStop(0,q.a);gr.addColorStop(1,q.b);d.C.pap=gr;}if(d.plein){try{var tq=performance.now();var Rp=_enreg();_parure(Rp,{pr:d.L,g:d.g},_T(d.L),undefined);var op=new OffscreenCanvas(d.cw,d.ch),cp=op.getContext('2d',CTX);cp.setTransform(d.M[0],0,0,d.M[1],d.M[2],d.M[3]);if(d.C.pap){cp.fillStyle=d.C.pap;cp.fillRect((0-d.M[2])/d.M[0]-2,(0-d.M[3])/d.M[1]-2,d.cw/d.M[0]+4,d.ch/d.M[1]+4);}cp.lineCap='butt';cp.lineJoin='miter';_peint(cp,Rp.ops,d.C,{});var vu={},toks=[];Rp.ops.forEach(function(o){if(!vu[o[2]]){vu[o[2]]=1;toks.push(o[2]);}});var bp=op.transferToImageBitmap();postMessage({id:d.id,plein:true,bm:bp,toks:toks,dur:Math.round(performance.now()-tq),ops:Rp.ops.length},[bp]);}catch(x){postMessage({id:d.id,err:String(x&&x.stack||x)});}return;}var memo={},cache=new Map(),e=null,ie=-1;d.L.forEach(function(p,i){if(p.h===d.k){e=p;ie=i;}});",
        "try{var sp=L3/40,M=d.M,non=function(){return false;};",
        /* les rosettes des yeux voisins ne changent pas pendant la pousse : peintes une fois, en deux calques (sous et sur celle de l'œil qui pousse, dans l'ordre du dessin) */
        "var rcM=0;d.frames.forEach(function(f){if(f.rc>rcM)rcM=f.rc;});var lox=Math.floor(M[0]*(e.x-rcM)+M[2])-2,loy=Math.floor(M[1]*(e.y-rcM)+M[3])-2,lw=Math.ceil(M[0]*2*rcM)+6,lh=Math.ceil(M[1]*2*rcM)+6;",
        "var pres=function(p){var ez2=0.78+0.5*_lcg((p.h^0xe7e)>>>0)();return Math.hypot(p.x-e.x,p.y-e.y)-(p.R*ez2*0.62+sp*2.2)<rcM;};",
        "var calque=function(avant){var R=_enreg();_parure(R,{pr:d.L,g:d.g,cachePL:cache,filtre:non,filtreOeil:function(p){var i=d.L.indexOf(p);return p.h!==e.h&&(avant?i<ie:i>ie)&&pres(p);}},_T(d.L),undefined);if(!R.ops.length)return null;var oc=new OffscreenCanvas(lw,lh),c=oc.getContext('2d',CTX);c.setTransform(M[0],0,0,M[1],M[2]-lox,M[3]-loy);c.lineCap='butt';c.lineJoin='miter';_peint(c,R.ops,d.C,memo);return oc;};",
        "var PR={champ:0,plumes:0,n:0},D0=Date.now(),T0=performance.now(),tp=0,td=0,n1=0;var sous=calque(true),sur=calque(false);var tc=performance.now()-T0;",
        "for(var i=0;i<d.frames.length;i++){var f=d.frames[i],s=f.s,rc=f.rc,ra=f.ra;",
        "var Ls=d.L.map(function(p){if(p.h!==d.k)return p;var c={};for(var q in p)c[q]=p[q];c.R=p.R*Math.max(s,1e-3);c.tS=s;return c;});",
        "var t1=performance.now();var R1=_enreg();_parure(R1,{pr:Ls,g:d.g,cachePL:cache,prof:PR,quant:(s<1?0.005236:0),filtre:function(fx,fy){var dx=fx-e.x,dy=fy-e.y;return dx*dx+dy*dy<ra*ra;},filtreOeil:non},_T(Ls),undefined);",
        "var R2=_enreg();_parure(R2,{pr:Ls,g:d.g,cachePL:cache,filtre:non,filtreOeil:function(p){return p.h===e.h;}},_T(Ls),undefined);",
        "tp+=performance.now()-t1;n1+=R1.ops.length+R2.ops.length;var t2=performance.now();var oc=new OffscreenCanvas(f.w,f.h),c=oc.getContext('2d',CTX);c.setTransform(M[0],0,0,M[1],M[2]-f.ox,M[3]-f.oy);",
        "if(d.C.pap){c.fillStyle=d.C.pap;c.fillRect(e.x-rc-2,e.y-rc-2,2*rc+4,2*rc+4);}c.lineCap='butt';c.lineJoin='miter';",
        "_peint(c,R1.ops,d.C,memo);",
        "if(sous){c.setTransform(1,0,0,1,0,0);c.drawImage(sous,lox-f.ox,loy-f.oy);c.setTransform(M[0],0,0,M[1],M[2]-f.ox,M[3]-f.oy);}",
        "_peint(c,R2.ops,d.C,memo);",
        "if(sur){c.setTransform(1,0,0,1,0,0);c.drawImage(sur,lox-f.ox,loy-f.oy);c.setTransform(M[0],0,0,M[1],M[2]-f.ox,M[3]-f.oy);}",
        "c.globalCompositeOperation='destination-in';c.beginPath();c.arc(e.x,e.y,rc,0,6.2832);c.fillStyle='#000';c.fill();",
        "td+=performance.now()-t2;var bm=oc.transferToImageBitmap();postMessage({id:d.id,i:i,s:s,ox:f.ox,oy:f.oy,w:f.w,h:f.h,bm:bm},[bm]);}",
"postMessage({id:d.id,fin:true,pr:[Math.round(PR.champ),Math.round(PR.plumes),PR.n,cache.size],d0:D0,d1:Date.now(),tc:Math.round(tc),tp:Math.round(tp),td:Math.round(td),ops:n1,nf:d.frames.length});}catch(x){postMessage({id:d.id,err:String(x&&x.stack||x)});}};"].join('\n');
      var src = 'var W,H,L3,window={_apImage:true},CTX=' + (window._ramFilmGPU ? '{}' : '{willReadFrequently:true}') + ';\n'   /* v91 : rendu processeur — le Worker ne passe pas par le processus graphique de l'affichage */ + [_lcg, _mix, _cutStroke, _enreg, _T, _parure].map(function (f) { return f.toString(); }).join('\n') + '\n' + corps;
      _FW = new Worker(URL.createObjectURL(new Blob([src], { type: 'text/javascript' })));
      _FW.onmessage = function (ev) { var d = ev.data, J = _FWJ[d.id]; if (!J) { if (d.bm && d.bm.close) d.bm.close(); return; }
        if (d.err) { delete _FWJ[d.id]; if (J.F) J.F.echec = true; if (J.plein && J.WJ[J.cle]) J.WJ[J.cle].echec = true; window._ramFilmErr = d.err; return; }
        if (d.plein) { (window._ramPleinW = window._ramPleinW || []).push([Math.round(performance.now()), d.dur, d.ops, J.K]); delete _FWJ[d.id]; var Pw = { L: J.E.L, toks: d.toks, h: J.E.h, ops: null };
          var Cw = { K: J.K, sem: String(J.K).split('|')[0], plein: true, cv: d.bm, M: J.M, ms: J.ms, P: Pw, tsig: _tons(Pw, performance.now()).sig, cw: J.cw, ch: J.ch, worker: true };
          if (J.WJ[J.cle]) J.WJ[J.cle].C = Cw; if (typeof env.relance === 'function') env.relance(); return; }
        if (d.fin) { (window._ramFilmW = window._ramFilmW || []).push([d.tc, d.tp, d.td, d.ops, d.nf, J.poste, d.d0, d.d1, d.d1 - d.d0, d.pr]); delete _FWJ[d.id]; if (--J.F.jobs === 0) { J.F.fini = true; J.F.t = performance.now() - J.F.t0; J.F.finT = Math.round(performance.now()); window._ramFilm = { images: J.F.n, Mpx: +(J.F.px / 1e6).toFixed(1), ms: Math.round(J.F.t), worker: true }; if (typeof env.relance === 'function') env.relance(); } return; }
        if (J.F.jete) { if (d.bm && d.bm.close) d.bm.close(); return; }   /* v94 : le film a été jeté pendant qu'il se calculait */
        J.x.fr.push({ cv: d.bm, s: d.s, ox: d.ox, oy: d.oy, w: d.w, h: d.h }); J.F.n++; J.F.px += d.w * d.h; };
      _FW.onerror = function (e) { window._ramFilmErr = String(e && e.message || e); for (var k in _FWJ) { if (_FWJ[k].F) _FWJ[k].F.echec = true; if (_FWJ[k].plein && _FWJ[k].WJ[_FWJ[k].cle]) _FWJ[k].WJ[_FWJ[k].cle].echec = true; } _FWJ = {}; _FWP = false; };
    } catch (e) { _FW = false; window._ramFilmErr = String(e && e.message || e); }
    return _FW; }
  function _couleursL(L, now, pap) { var rm = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, C = { P: [], N: [], M: (rm || []).map(_arr), I: _encre(), F: _arr(env.fondToile()), pap: (pap && typeof pap !== 'string') ? (typeof env.papierDesc === 'function' ? env.papierDesc() : null) : pap }; _fin = true;
    try { L.forEach(function (p) { var c = _col(p.s, now); C.P.push([c[0], c[1], c[2]]); var n = _nuance(c); C.N.push([n[0], n[1], n[2]]); }); } finally { _fin = false; } return C; }
  /* ⚑ v91 — un PLUMAGE ENTIER (l'état d'un aperçu) peint par le Worker : null tant qu'il n'est pas revenu, false s'il n'y a pas de Worker */
  var _calWJ = {};
  /* v92 : sur la Toile, l'état d'arrivée a SON Worker — dans la file d'un Worker du film, il retardait un tiers des images de 0,55 s */
  var _FWPL = null;
  function _pleinWorker() { if (_FWPL !== null) return _FWPL; if (!_filmPool()) return (_FWPL = false); var f0 = _FW; _FW = null; _FWPL = _filmWorker() || false; _FW = f0; return _FWPL; }
  function _calDemande(E, K, ms, M, cw, ch, now) { var cle = K + '|' + ms, J = _calWJ[cle];
    if (J) { if (J.C) { delete _calWJ[cle]; return J.C; } return J.echec ? false : null; }
    var pool = _filmPool(); if (!pool) return false;
    var pap = typeof env.papier === 'function' ? env.papier() : null, id = ++_FWN; _calWJ[cle] = { E: E };
    _FWJ[id] = { plein: true, cle: cle, E: E, K: K, ms: ms, M: M, cw: cw, ch: ch, WJ: _calWJ };
    ((window._ramToileAp && _pleinWorker()) || pool[id % pool.length]).postMessage({ id: id, plein: true, W: W, H: H, L3: 300 * E.K, g: (env.cleToile == null ? 1 : env.cleToile), M: [M.a, M.d, M.e, M.f], cw: cw, ch: ch,
      C: _couleursL(E.L, now, pap), L: E.L.map(function (p) { return { h: p.h, x: p.x, y: p.y, R: p.R, ci: p.ci, ci2: p.ci2 }; }) });
    return null; }
  /* un film demandé au Worker : de la liste des yeux LA (ce qu'on voit) à LB (l'arrivée) */
  function _filmLance(A, LA, LB, ms, M, now) { var pool = _filmPool(); if (!pool) return null;
    var dA = {}, dB = {}, its = {}, N = window._ramFilmN || Math.max(12, Math.round(DUR_P / 16.7)), pap = typeof env.papier === 'function' ? env.papier() : null;
    LA.forEach(function (e) { dA[e.h] = e; }); LB.forEach(function (e) { dB[e.h] = e; });
    var F = { de: A, ms: ms, items: its, fini: false, n: 0, px: 0, t0: performance.now(), jobs: 0, worker: true, pap: pap }; (window._ramFL = window._ramFL || []).push(F); if (window._ramFL.length > 3) window._ramFL.shift();   /* v94 : bornée — elle gardait TOUS les films (≈ 70 Mo d'images chacun) */ F.lanceT = Math.round(performance.now());
    var K = env.uMat / UPL, L3v = 300 * K, sp = L3v / 40, Lmax = sp * 3.9, cw0 = Math.round(M.a * W + M.e * 2), ch0 = Math.round(M.d * H + M.f * 2);
    function couleurs(L) { return _couleursL(L, now, pap); }
    var memoL = new Map();
    function lance(e, L, dir) { var x = { k: e.h, e: e, dir: dir, L: L, fr: [] }; its[e.h + (dir > 0 ? '+' : '-')] = x;
      var ez = 0.78 + 0.5 * _lcg((e.h ^ 0xe7e) >>> 0)(), Rz = Math.max(1, e.R * ez), fr = [], ss = [];
      for (var j = 1; j <= N; j++) ss.push(_lisse(j / N)); if (dir < 0) ss.push(0.0005);
      ss.forEach(function (s) { var rc = 2.4 * Rz * s + Lmax + 2, ra = rc + Lmax;
        var ox = Math.max(0, Math.floor(M.a * (e.x - rc) + M.e) - 2), oy = Math.max(0, Math.floor(M.d * (e.y - rc) + M.f) - 2),
          w = Math.max(2, Math.min(cw0, Math.ceil(M.a * (e.x + rc) + M.e) + 3) - ox), h = Math.max(2, Math.min(ch0, Math.ceil(M.d * (e.y + rc) + M.f) + 3) - oy);
        fr.push({ s: s, rc: rc, ra: ra, ox: ox, oy: oy, w: w, h: h }); });
      fr.sort(function (a, b) { return dir > 0 ? a.s - b.s : b.s - a.s; });   /* v92 : produites dans l'ordre où on les lit — un départ lit les grandes tailles d'abord */
      x.ss = ss.slice(); F.nT = (F.nT || 0) + fr.length; F.pxL = F.pxL || []; fr.forEach(function (f, j) { F.pxL[j] = (F.pxL[j] || 0) + f.w * f.h; });   /* v92 : l'ordre des tailles et le compte des images, connus avant qu'elles reviennent (le film se joue pendant qu'il arrive) */
      /* v98 (500 paroles) : les couleurs et la liste des yeux ne dépendent que de L — une fois par liste, pas une fois par œil */
      var CL = memoL.get(L); if (!CL) { CL = { C: couleurs(L), L: L.map(function (p) { return { h: p.h, x: p.x, y: p.y, R: p.R, ci: p.ci, ci2: p.ci2 }; }) }; memoL.set(L, CL); }
      var C0 = CL.C, L0 = CL.L;
      pool.forEach(function (w, wi) { var part = fr.filter(function (_, j) { return j % pool.length === wi; }); if (!part.length) return;   /* les images, réparties entre les Workers */
        var id = ++_FWN; _FWJ[id] = { F: F, x: x, poste: Date.now() }; F.jobs++; F.dirs = (F.dirs || '') + (dir > 0 ? '+' : '-');
        w.postMessage({ id: id, W: W, H: H, L3: L3v, g: (env.cleToile == null ? 1 : env.cleToile), k: e.h, M: [M.a, M.d, M.e, M.f], frames: part, C: C0, L: L0 }); }); }
    /* ⚑ v98 (Tom : 500 paroles) — un film est celui d'UNE parole qui pousse ou se résorbe. Quand la Toile entière change d'un coup
       (500 paroles chargées ensemble : 500 films, 41 s pour la première image en WebKit), au-delà de 24 yeux on ne filme pas —
       l'état d'arrivée se pose, comme sans Worker. Une plantation, un retrait : le film, inchangé. */
    var _nMv = 0; LB.forEach(function (e) { if (!dA[e.h]) _nMv++; }); LA.forEach(function (e) { if (!dB[e.h]) _nMv++; });
    if (_nMv > 24) { window._ramFL.pop(); return null; }
    LB.forEach(function (e) { if (!dA[e.h]) lance(e, LB, 1); });
    LA.forEach(function (e) { if (!dB[e.h]) lance(e, LA, -1); });
    if (!F.jobs) F.fini = true;
    return F; }
  function _filmAvance(A, B, M, now, budget, cap) { var F = B.film;
    if (F && F.de === A && F.ms === B.ms && !F.echec) return F.fini;
    if (!window._ramFilmSansWorker) { var Fw = _filmLance(A, A.P.L, B.P.L, B.ms, M, now); if (Fw) { B.film = Fw; return Fw.fini; } }
    var dA = {}, dB = {}, its = {}, q = [], pap = typeof env.papier === 'function' ? env.papier() : null, N = window._ramFilmN || Math.max(12, Math.round(DUR_P / 16.7));
    A.P.L.forEach(function (e) { dA[e.h] = e; }); B.P.L.forEach(function (e) { dB[e.h] = e; });
    function pose(e, L, dir) { var x = { k: e.h, e: e, dir: dir, L: L, fr: [] }; its[e.h + (dir > 0 ? '+' : '-')] = x; for (var j = 1; j <= N; j++) q.push({ x: x, s: _lisse(j / N) }); if (dir < 0) q.push({ x: x, s: 0.0005 }); }
    B.P.L.forEach(function (e) { if (!dA[e.h]) pose(e, B.P.L, 1); });
    A.P.L.forEach(function (e) { if (!dB[e.h]) pose(e, A.P.L, -1); });
    F = B.film = { de: A, ms: B.ms, items: its, q: q, qi: 0, job: null, fini: !q.length, n: 0, px: 0, t: 0, pap: pap }; return F.fini; }
  /* une image du film : le plumage recalculé avec l'œil à la taille s, dans le seul disque qui peut changer (la poussée bornée à 2,4
     rayons + la longueur d'une plume), sur le papier, dans l'ordre exact des plumes, à l'échelle 1. À s → 0 ce disque est l'ancien
     plumage, à s = 1 le nouveau : aucun saut aux deux bouts, et hors du disque rien ne change. */
  function _filmImageDe(x, s, M, now, pap) { var e = x.e, K = env.uMat / UPL; L3 = 300 * K; var sp = L3 / 40, Lmax = sp * 3.9;
    var ez = 0.78 + 0.5 * _lcg((e.h ^ 0xe7e) >>> 0)(), Rz = Math.max(1, e.R * ez), rc = 2.4 * Rz * s + Lmax + 2, ra = rc + Lmax;   /* à la taille s, l'œil n'agit que jusqu'à 2,4 × (R·s) : le disque grandit avec lui */
    var Ls = x.L.map(function (p) { if (p.h !== e.h) return p; var c = {}; for (var k in p) c[k] = p[k]; c.R = p.R * Math.max(s, 1e-3); c.tS = s; return c; });
    var R = _enreg(), S = { pr: Ls, g: (env.cleToile == null ? 1 : env.cleToile), cachePL: x.cache || (x.cache = new Map()),
      filtre: function (fx, fy) { var dx = fx - e.x, dy = fy - e.y; return dx * dx + dy * dy < ra * ra; },
      filtreOeil: function (p) { var ez2 = 0.78 + 0.5 * _lcg((p.h ^ 0xe7e) >>> 0)(); return Math.hypot(p.x - e.x, p.y - e.y) - (p.R * ez2 * 0.62 + sp * 2.2) < rc; } };
    var _tp = performance.now(); _parure(R, S, _T(Ls), undefined); var _TT = window._ramFilmT = window._ramFilmT || [0, 0, 0]; _TT[0] += performance.now() - _tp; _TT[2]++;
    var P = _fait(R, Ls, 0), m = _tons(P, now).m; window._ramFilmDisc = [Math.round(rc), Math.round(Rz), Math.round(sp), P.ops.length, Math.round(W), Math.round(H), Math.round(e.x), Math.round(e.y)];
    var cw0 = Math.round(M.a * W + M.e * 2), ch0 = Math.round(M.d * H + M.f * 2);   /* le canevas de l'aperçu : une image ne garde que ce qui s'y voit */
    var ox = Math.max(0, Math.floor(M.a * (e.x - rc) + M.e) - 2), oy = Math.max(0, Math.floor(M.d * (e.y - rc) + M.f) - 2),
      w = Math.max(2, Math.min(cw0, Math.ceil(M.a * (e.x + rc) + M.e) + 3) - ox), h = Math.max(2, Math.min(ch0, Math.ceil(M.d * (e.y + rc) + M.f) + 3) - oy);
    var cv = document.createElement('canvas'); cv.width = w; cv.height = h; var c = cv.getContext('2d');
    c.setTransform(M.a, 0, 0, M.d, M.e - ox, M.f - oy);   /* pas de clip() : sous WebKit il se paie à chaque tracé (§8) — le disque se découpe à la fin, d'un seul masque */
    if (pap) { c.fillStyle = pap; c.fillRect(e.x - rc - 2, e.y - rc - 2, 2 * rc + 4, 2 * rc + 4); }
    c.lineCap = 'butt'; c.lineJoin = 'miter';
    return { c: c, cv: cv, ops: P.ops, m: m, i: 0, s: s, ox: ox, oy: oy, w: w, h: h, cx: e.x, cy: e.y, rc: rc }; }
  function _filmPas(B, M, budget, cap) { var F = B.film; if (!F || F.fini) return true; if (F.worker) return false;   /* le Worker le fait */ var t0 = performance.now(), n = 0, now = performance.now(); window._ramFilmProg = [F.qi, F.q.length, Math.round(F.t)];
    while (F.qi < F.q.length) { var Q = F.q[F.qi], x = Q.x, J = F.job;
      if (!J) { J = F.job = _filmImageDe(x, Q.s, M, now, F.pap); F.px += J.w * J.h; n += 200; }
      var ops = J.ops, c2 = J.c, m = J.m, _td = performance.now();
      for (; J.i < ops.length; J.i++) { var o = ops[J.i], st = o[2] === 'B' ? F.pap : m[o[2]];
        if (o[4] !== 'source-over') c2.globalCompositeOperation = o[4];
        if (o[0]) { c2.strokeStyle = st; c2.lineWidth = o[3]; c2.stroke(o[1]); } else { c2.fillStyle = st; c2.fill(o[1]); }
        if (o[4] !== 'source-over') c2.globalCompositeOperation = 'source-over';
        if (++n >= cap || ((n & 15) === 0 && performance.now() - t0 > budget)) { J.i++; window._ramFilmT[1] += performance.now() - _td; if (J.i >= ops.length) break; F.t += performance.now() - t0; return false; } }
      window._ramFilmT[1] += performance.now() - _td;
      if (J.i >= ops.length) { c2.globalCompositeOperation = 'destination-in'; c2.beginPath(); c2.arc(J.cx, J.cy, J.rc, 0, 6.2832); c2.fillStyle = '#000'; c2.fill(); c2.globalCompositeOperation = 'source-over';
        x.fr.push({ cv: J.cv, s: J.s, ox: J.ox, oy: J.oy, w: J.w, h: J.h }); F.job = null; F.qi++; F.n++; if (performance.now() - t0 > budget) { F.t += performance.now() - t0; return F.qi >= F.q.length ? (F.fini = true, F.q = null, true) : false; } } }
    F.t += performance.now() - t0; F.fini = true; F.q = null; if (window._ramFilmDbg) _filmDer = { B: B, F: F }; window._ramFilm = { images: F.n, Mpx: +(F.px / 1e6).toFixed(1), ms: Math.round(F.t) }; return true; }
  var _filmDer = null;
  window._ramFilmEcart = function () { var D = _filmDer; if (!D) return null; var A = D.F.de, B = D.B, cv = document.createElement('canvas'); cv.width = A.cw; cv.height = A.ch; var c = cv.getContext('2d');
    c.drawImage(A.cv, 0, 0); var zb = [1e9, 1e9, -1e9, -1e9];
    for (var k in D.F.items) { var x = D.F.items[k]; if (x.dir > 0 && x.fr.length) { var f = x.fr[x.fr.length - 1]; c.drawImage(f.cv, f.ox, f.oy); zb = [Math.min(zb[0], f.ox), Math.min(zb[1], f.oy), Math.max(zb[2], f.ox + f.w), Math.max(zb[3], f.oy + f.h)]; } }
    var a = c.getImageData(0, 0, cv.width, cv.height).data, b = B.cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data, n = 0, nz = 0, bb = [1e9, 1e9, -1e9, -1e9], W2 = cv.width;
    for (var i = 0; i < a.length; i += 4) { if (Math.max(Math.abs(a[i] - b[i]), Math.abs(a[i + 1] - b[i + 1]), Math.abs(a[i + 2] - b[i + 2])) > 12) { n++; var px = (i / 4) % W2, py = ((i / 4) / W2) | 0; if (px >= zb[0] && px < zb[2] && py >= zb[1] && py < zb[3]) nz++; if (px < bb[0]) bb[0] = px; if (py < bb[1]) bb[1] = py; if (px > bb[2]) bb[2] = px; if (py > bb[3]) bb[3] = py; } }
    var dmax = 0, rmax = 0, pa = {}; A.P.L.forEach(function (e) { pa[e.h] = e; }); B.P.L.forEach(function (e) { var q = pa[e.h]; if (!q) return; dmax = Math.max(dmax, Math.hypot(q.x - e.x, q.y - e.y)); rmax = Math.max(rmax, Math.abs(q.R - e.R)); });
    var coul = []; try { var now9 = performance.now(); B.P.L.forEach(function (e) { var q = pa[e.h]; if (!q) return; var ca = _rgb(_col(q.s, now9)), cb = _rgb(_col(e.s, now9)); if (ca !== cb || q.s !== e.s) coul.push([e.h % 1000, ca, cb, q.s === e.s, q.s.ci, e.s.ci, q.s.kind, e.s.kind, q.s.tone, e.s.tone, !!q.s.gray, !!e.s.gray]); }); } catch (x) { coul = String(x); }
    window._ramFilmCoul = coul;
    try { var ta = A.tsig.split('|'), tb = B.tsig.split('|'), ka = A.P.toks.filter(function (t) { return t !== 'B'; }), kb = B.P.toks.filter(function (t) { return t !== 'B'; }), mA = {}, dd = []; ka.forEach(function (t, i) { mA[t] = ta[i]; });
      kb.forEach(function (t, i) { if (t.charAt(0) !== 'P' && t.charAt(0) !== 'N' && t.indexOf('P') < 0 && t.indexOf('N') < 0 && mA[t] !== undefined && mA[t] !== tb[i]) dd.push(t + ':' + mA[t] + '>' + tb[i]); }); window._ramFilmTons = { mat: dd, tA: ta[0].slice(0, 1), tB: tb[0].slice(0, 1), nA: A.P.ops.length, nB: B.P.ops.length, hA: A.P.h, hB: B.P.h, WA: A.cw, WB: B.cw, HA: A.ch, HB: B.ch, bA: A.P.b, bB: B.P.b }; } catch (x) { window._ramFilmTons = String(x); }
    var red = function (src) { var r = document.createElement('canvas'); r.width = 96; r.height = 208; var x = r.getContext('2d'); x.drawImage(src, 0, 0, 96, 208); return x.getImageData(0, 0, 96, 208).data; };
    var ra = red(cv), rb = red(B.cv), rs = 0; for (var i2 = 0; i2 < ra.length; i2 += 4) rs += Math.abs(ra[i2] - rb[i2]) + Math.abs(ra[i2 + 1] - rb[i2 + 1]) + Math.abs(ra[i2 + 2] - rb[i2 + 2]); window._ramFilmSaut = +(rs / (ra.length / 4) / 3).toFixed(2);
    if (window._ramFilmImg) window._ramFilmImgs = [cv.toDataURL(), B.cv.toDataURL()];
    return { dep: +dmax.toFixed(2), dR: +rmax.toFixed(3), tons: A.tsig === B.tsig, KA: A.K, KB: B.K, diff: n, dansZone: nz, part: +(100 * n / (a.length / 4)).toFixed(2), bbDiff: bb, zone: zb, dir: Object.keys(D.F.items) }; };
  /* ⚑ v92 — SUR LA TOILE, LE FILM SE JOUE PENDANT QU'IL ARRIVE. L'événement n'y est pas connu d'avance (au Studio, si) : on part dès que
     la production, au rythme mesuré, finira avant que la lecture n'atteigne la dernière image. Une image en retard fait TENIR la lecture
     (l'horloge attend), jamais sauter. */
  function _filmAssez(F) { if (!F || F.echec) return false; if (F.fini) return true; if (!window._ramToileAp || !F.nT) return false;
    var el = performance.now() - F.t0; if (F.n < 3 || el < 1 || !F.pxL) return false;
    /* au rythme mesuré EN PIXELS (une image grandit avec l'œil), chaque image doit être revenue avant que la lecture ne l'atteigne */
    var v = F.px / el, per = DUR_P / F.pxL.length, cum = 0;
    for (var k = 0; k < F.pxL.length; k++) { cum += F.pxL[k]; var reste = cum - F.px; if (reste > 0 && reste / v > k * per + 60) return false; }
    return true; }
  /* ⚑ v94 (Tom, iPhone : « l'app bugue après quelques clics, puis recharge toute seule ») — Un film = ≈ 66 images, ≈ 70 Mo. La liste de
     diagnostic (`_ramFL`) les gardait TOUS, pour toujours : elle est bornée. Un film REFUSÉ (l'arrivée n'est pas la sienne) ferme ses
     images tout de suite : il ne peut servir nulle part.
     Un film en cours de lecture (`enJeu`) n'est jamais fermé ici : c'est `_libere` qui le fait, image posée. */
  function _filmJette(F) { if (!F || F.enJeu || F.jete) return; F.jete = true; for (var k in F.items) { var x = F.items[k]; (x.fr || []).forEach(function (f) { if (f.cv && f.cv.close) try { f.cv.close(); } catch (_) { } }); x.fr = []; } }
  function _filmOte(cle) { var F = _filmsK[cle]; delete _filmsK[cle]; _filmJette(F); }
  function _filmsBorne() { var kk = Object.keys(_filmsK); if (kk.length > 4) delete _filmsK[kk[0]]; }   /* la réserve d'avant (quatre) : un film poussé dehors est seulement oublié — il peut être encore en calcul, ou attendu par un événement du Studio (le fermer bloquait le Studio, mesuré). Le ramasse-miettes le reprend. */
  function _libere(it) { if (!it.film) return; it.film.forEach(function (f) { if (f.cv && f.cv.close) try { f.cv.close(); } catch (_) { } }); it.film = null; }   /* v91 : les images du Worker se libèrent dès que la pousse est posée */
  function _filmImage(it, s) { var fr = it.film, best = null, d = 1e9; for (var i = 0; i < fr.length; i++) { var dd = Math.abs(fr[i].s - s); if (dd < d) { d = dd; best = fr[i]; } } return best; }
  function _gPas(G, t) { var pousse = false; G.items.forEach(function (it) { if (it.dir > 0 && !_gFin(it)) pousse = true; });
    if (G.mv) { G.a = _lisse(Math.min(1, (t - G.t0) / DUR_P)); if (G.a < 1) pousse = true; for (var q in G.arr) pousse = true; }
    if (G.att) pousse = true;
    if (!G.pret && !pousse && G.mv && G.Pfin && G.fond && !G.attente.length) { G.pret = _gCuit(G, t); G.cuit = true; }
    if (G.pret && !pousse && (G.attente || []).every(function (it) { return !!it.vu; })) { if (G.pret.film) G.pret.film = null; /* v90 : le film a servi */ G.mv = null; G.fond = null; G.E = null; G.mat = null; G.base = G.pret; G.pret = null; G.P = null; G.items = G.items.filter(function (it) { if (it.dir < 0) return true; _libere(it); return false; }); G.attente.forEach(function (it) { it.t0 = t; it.prep = false; G.items.push(it); }); G.attente = []; }
    G.items = G.items.filter(function (it) { var f = it.dir < 0 && _gFin(it); if (f) _libere(it); return !f; });
    return G.items.length > 0 || !!G.P; }
  /* l'œil qui pousse est tracé dans SON canevas, à sa taille, PAR TRANCHES : l'étape précédente reste affichée (posée 1:1) pendant
     que la suivante se trace, puis elles s'échangent. Chaque étape vise l'échelle qu'il faudra quand elle paraîtra (le temps de la
     précédente). La tranche se règle sur la durée des images : sous Chromium une étape par image ; sous WebKit — où 1 500 chemins
     à une échelle neuve coûtent ~80 ms — une étape toutes les quelques images, et le reste de l'image (le glissé) ne ralentit pas. */
  var _gN = 600, _gL = 0;
  function _gFin(it) { return it.vu && (it.dir > 0 ? it.vu.s >= 1 : it.vu.s <= 0.002); }
  function _gPeint(G, M, t) { var now = performance.now(), fdt = now - (_gL || now); _gL = now;
    if (fdt > 0 && fdt < 250) { if (fdt > 22) _gN = Math.max(60, _gN * 0.65); else if (fdt < 18.5) _gN = Math.min(6000, _gN * 1.3); }
    var reste = Math.round(_gN);
    /* v89 : un œil qui VA partir trace d'abord son image entière, sans être montré ; l'échange attend qu'elle soit prête */
    (G.attente || []).forEach(function (it) { if (it.vu || reste <= 0) return; it.t0 = it.t0 == null ? -1e9 : it.t0; it.prep = true; });
    G.items.concat((G.attente || []).filter(function (it) { return it.prep && !it.vu; })).forEach(function (it) {
      if (it.film) {   /* v90 : l'étape de l'instant, tracée d'avance, posée 1:1 — v91 : UNE IMAGE NEUVE À CHAQUE AFFICHAGE, l'horloge en garde-fou */
        var cmpS = function (a, b) { return it.dir > 0 ? a - b : b - a; };   /* les Workers les rendent dans le désordre : on les lit par TAILLE */
        if (!it.ord) it.ord = (it.filmSs || it.film.map(function (f) { return f.s; })).slice().sort(cmpS);
        if (it.fmN !== it.film.length) { it.fm = {}; it.film.forEach(function (f) { it.fm[f.s] = f; }); it.fmN = it.film.length; }
        var ord = it.ord, nF = ord.length, fF, at = function (k) { return it.fm[ord[k]] || null; };
        if (it.prep) { fF = at(it.dir > 0 ? nF - 1 : 0); if (!fF) return; it.cvA = fF.cv; it.vu = { s: 1, ox: fF.ox, oy: fF.oy, w: fF.w, h: fF.h }; return; }
        if (it.fi != null && it.fi < nF - 1 && !at(it.fi + 1)) { it.t0 += t - (it.tl == null ? t : it.tl); it.tl = t; window._mondeEncore = true; fF = at(it.fi); if (fF) { g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(fF.cv, fF.ox, fF.oy); } return; }   /* v92 : l'image suivante n'est pas revenue — la lecture tient */
        it.tl = t; if (it.fi == null && !at(0)) { it.t0 = t; window._mondeEncore = true; return; }
        var per = DUR_P / nF, cible = Math.max(0, (t - it.t0) / per);
        /* on avance d'une image par affichage (jamais deux fois la même, jamais un saut sur un simple flottement d'horloge) ; si un
           affichage a vraiment pris du retard, on rattrape l'horloge ; sur un écran plus rapide que 60 Hz, on ne la dépasse pas */
        it.fi = it.fi == null ? 0 : Math.max(it.fi, Math.min(Math.max(it.fi + 1, Math.floor(cible)), Math.ceil(cible)));
        while (it.fi > 0 && !at(it.fi)) it.fi--;   /* v92 : jamais au-delà de ce qui est revenu */
        if (it.fi >= nF - 1) { it.fi = nF - 1; fF = at(nF - 1); it.vu = { s: it.dir > 0 ? 1 : 0, ox: fF.ox, oy: fF.oy, w: fF.w, h: fF.h }; it.cvA = fF.cv; if (it.dir < 0) return; }
        else { fF = at(it.fi); it.cvA = fF.cv; it.vu = { s: Math.max(0.003, fF.s), ox: fF.ox, oy: fF.oy, w: fF.w, h: fF.h }; }
        g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(fF.cv, fF.ox, fF.oy); return; }
      if (!it.ops || !it.ops.length) { it.vu = { s: it.dir > 0 ? 1 : 0 }; return; }   /* v91 : un plumage du Worker n'a pas de tracés — sans film, l'œil se pose d'un coup (secours) */
      if (!it.bx) { var b = [1e18, 1e18, -1e18, -1e18]; it.ops.forEach(function (o) { var q = o[6]; if (!q) return; if (q[0] < b[0]) b[0] = q[0]; if (q[1] < b[1]) b[1] = q[1]; if (q[2] > b[2]) b[2] = q[2]; if (q[3] > b[3]) b[3] = q[3]; }); it.bx = b; it.lag = 0; }
      if (!it.job && !_gFin(it) && reste > 0) {   // une étape neuve, à l'échelle qu'il faudra quand elle paraîtra
        var s = it.prep ? 1 : _gS({ t0: it.t0, s0: it.s0, dir: it.dir }, t + it.lag); if (it.dir > 0 && s > 0.985) s = 1; if (it.dir < 0 && s < 0.015) s = 0;
        var b2 = it.bx, cx = it.e.x, cy = it.e.y, x0 = cx + (b2[0] - cx) * s, y0 = cy + (b2[1] - cy) * s, x1 = cx + (b2[2] - cx) * s, y1 = cy + (b2[3] - cy) * s;
        var ox = Math.floor(M.a * x0 + M.e) - 4, oy = Math.floor(M.d * y0 + M.f) - 4, w = Math.max(2, Math.ceil(M.a * x1 + M.e) + 4 - ox), h = Math.max(2, Math.ceil(M.d * y1 + M.f) + 4 - oy);
        var cv = it.cvB || (it.cvB = document.createElement('canvas')); if (cv.width < w || cv.height < h) { cv.width = Math.max(cv.width, w); cv.height = Math.max(cv.height, h); }
        var c = cv.getContext('2d'); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, cv.width, cv.height);
        c.setTransform(M.a * s, 0, 0, M.d * s, M.e - ox + M.a * cx * (1 - s), M.f - oy + M.d * cy * (1 - s)); c.lineCap = 'butt'; c.lineJoin = 'miter';
        it.job = { c: c, cv: cv, i: 0, s: s, ox: ox, oy: oy, w: w, h: h, t0: t }; }
      var J = it.job;
      if (J) { var c2 = J.c, n2 = it.ops.length;
        if (J.s > 0.002) for (; J.i < n2 && reste > 0; J.i++, reste--) { var o = it.ops[J.i], st = o[2] === 'B' ? it.pap : it.m[o[2]];
          if (o[4] !== 'source-over') c2.globalCompositeOperation = o[4];
          if (o[0]) { c2.strokeStyle = st; c2.lineWidth = o[3]; c2.stroke(o[1]); } else { c2.fillStyle = st; c2.fill(o[1]); }
          if (o[4] !== 'source-over') c2.globalCompositeOperation = 'source-over'; }
        else J.i = n2;
        if (J.i >= n2) { var A = it.cvA; it.cvA = J.cv; it.cvB = A; it.vu = { s: J.s, ox: J.ox, oy: J.oy, w: J.w, h: J.h }; it.lag = Math.max(0, t - J.t0); it.job = null; } }
      if (it.prep) return;
      if (it.vu && it.vu.s > 0.002) { g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(it.cvA, 0, 0, it.vu.w, it.vu.h, it.vu.ox, it.vu.oy, it.vu.w, it.vu.h); }
      else if (!it.vu && it.spr0) { g.setTransform(1, 0, 0, 1, 0, 0); g.drawImage(it.spr0.cv, it.spr0.ox, it.spr0.oy); } }); }
  /* ⚑ v87 — ET LES YEUX QUI RESTENT GLISSENT. À chaque plantation le moteur redispose TOUTES les graines (mesuré : ~50 px pour
     chaque œil). La v84 le cachait en reconstruisant tout le plumage rosace par rosace — la vague. Désormais : au repos, chaque œil
     est rendu une fois EN VECTEUR, à sa taille et à la vue du moment (son empreinte, posée 1:1, jamais agrandie ni réduite), et un
     plumage SANS ŒIL (la matière seule) est prêt. À la plantation, la matière seule se pose, les yeux qui restent glissent de leur
     place à la nouvelle (DUR_P), l'œil neuf pousse depuis son centre, celui qui part se résorbe ; puis le plumage exact se pose.
     Si l'empreinte n'est pas prête (vue qui vient de changer), on retombe sur la pousse seule. */
  var _fonds = [], _fJ = null;
  function _fondSig(ms, K) { var rm = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, pap = typeof env.papier === 'function' ? env.papier() : '';
    return [ms, Math.round(W), Math.round(H), Math.round(K * 4096), env.cleToile, JSON.stringify(rm), pap, env.isLightM() ? 'c' : 's'].join('|'); }
  function _fondPret(ms) { var sig = _fondSig(ms, env.uMat / UPL); for (var i = 0; i < _fonds.length; i++) if (_fonds[i].sig === sig) return _fonds[i]; return null; }
  function _fondAvance(ms, M, cw, ch, now, budget) { var K = env.uMat / UPL, sig = _fondSig(ms, K), F = _fondPret(ms); if (F) return F;
    if (!_fJ || _fJ.sig !== sig) { L3 = 300 * K; _fJ = { sig: sig, R: _enreg(), Q: [], qi: 0, M: M, cw: cw, ch: ch, ms: ms };
      _parure(_fJ.R, { pr: [], g: (env.cleToile == null ? 1 : env.cleToile) }, _T([]), undefined, _fJ.Q); return null; }
    var J = _fJ, t0 = performance.now();
    if (!J.P) { var Q = J.Q, k = J.qi; while (k < Q.length) { Q[k++](); if ((k & 15) === 0 && performance.now() - t0 > budget) break; } J.qi = k; if (k < Q.length) return null;
      J.P = _fait(J.R, [], 0); J.R = J.Q = null; J.C = _calque(J.P, _tons(J.P, now), J.M, J.cw, J.ch); return null; }
    if (_peintJusqua(J.C, J.P.ops.length, budget, t0)) { F = { sig: sig, cv: J.C.cv, M: J.M, ms: J.ms }; _fonds.push(F); if (_fonds.length > 3) _fonds.shift(); _fJ = null; return F; }
    return null; }
  function _sprAvance(B, now, budget) { if (B.sprOk) return true; var P = B.P, M = B.M, t0 = performance.now();
    if (!B.spr) { B.spr = {}; B.sprL = P.L.map(function (e) { return e.h; }); B.sprI = 0; B.sprM = _tons(P, now).m; B.sprPap = typeof env.papier === 'function' ? env.papier() : null; }
    while (B.sprI < B.sprL.length) { var k = B.sprL[B.sprI], Sp = B.spr[k];
      if (!Sp) { var ops = [], b = [1e18, 1e18, -1e18, -1e18], i0 = -1, j;
        for (j = 0; j < P.ops.length; j++) { var q = P.ops[j]; if (q[5] !== k) continue; if (i0 < 0) i0 = j; q = q[6]; if (!q) continue;
          if (q[0] < b[0]) b[0] = q[0]; if (q[1] < b[1]) b[1] = q[1]; if (q[2] > b[2]) b[2] = q[2]; if (q[3] > b[3]) b[3] = q[3]; }
        if (i0 < 0 || b[0] > b[2]) { B.sprI++; continue; }
        /* l'œil tel qu'il est DANS le plumage : les tracés qui le suivent et le chevauchent (la matière, un voisin) le recouvrent
           là où il est peint — `source-atop` — sans rien peindre au-delà de lui (au-delà, c'est la matière seule qui est dessous) */
        for (j = i0; j < P.ops.length; j++) { var o3 = P.ops[j], q3 = o3[6];
          if (o3[5] === k) ops.push(o3); else if (q3 && !(q3[2] < b[0] || q3[0] > b[2] || q3[3] < b[1] || q3[1] > b[3])) ops.push([o3[0], o3[1], o3[2], o3[3], o3[4] === 'source-over' ? 'source-atop' : o3[4], o3[5], o3[6]]); }
        var ox = Math.floor(M.a * b[0] + M.e) - 4, oy = Math.floor(M.d * b[1] + M.f) - 4, w = Math.ceil(M.a * b[2] + M.e) + 4 - ox, h = Math.ceil(M.d * b[3] + M.f) + 4 - oy;
        var cv = document.createElement('canvas'); cv.width = Math.max(1, w); cv.height = Math.max(1, h); var G = cv.getContext('2d');
        G.setTransform(M.a, 0, 0, M.d, M.e - ox, M.f - oy); G.lineCap = 'butt'; G.lineJoin = 'miter';
        Sp = B.spr[k] = { cv: cv, G: G, ox: ox, oy: oy, ops: ops, i: 0 }; }
      var o2 = Sp.ops, G2 = Sp.G, m = B.sprM;
      for (; Sp.i < o2.length; Sp.i++) { var o = o2[Sp.i], st = o[2] === 'B' ? B.sprPap : m[o[2]];
        if (o[4] !== 'source-over') G2.globalCompositeOperation = o[4];
        if (o[0]) { G2.strokeStyle = st; G2.lineWidth = o[3]; G2.stroke(o[1]); } else { G2.fillStyle = st; G2.fill(o[1]); }
        if (o[4] !== 'source-over') G2.globalCompositeOperation = 'source-over';
        if ((Sp.i & 31) === 31 && performance.now() - t0 > budget) { Sp.i++; return false; } }
      Sp.fini = true; Sp.G = null; Sp.ops = null; B.sprI++; }
    B.sprOk = true; return true; }
  /* la matière du plumage d'arrivée (ses tracés sans œil), sans papier : sous les yeux qui glissent — l'échange final ne change plus qu'eux */
  function _matAvance(X, P, M, cw, ch, now, budget) { if (X.mat) return X.mat; var J = X.matJ;
    if (!J) { J = X.matJ = _calque(P, _tons(P, now), M, cw, ch, true); J.i = 0; return null; }
    var G = J.G, ops = P.ops, m = J.tons.m, t0 = performance.now(), i = J.i, Z = J.z, n = 0;
    for (; i < ops.length; i++) { var o = ops[i], bx = o[6]; if (o[5] != null) continue;
      if (Z && bx && (bx[2] < Z[0] || bx[0] > Z[2] || bx[3] < Z[1] || bx[1] > Z[3])) continue;
      var st = o[2] === 'B' ? J.pap : m[o[2]]; if (o[4] !== 'source-over') G.globalCompositeOperation = o[4];
      if (o[0]) { G.strokeStyle = st; G.lineWidth = o[3]; G.stroke(o[1]); } else { G.fillStyle = st; G.fill(o[1]); }
      if (o[4] !== 'source-over') G.globalCompositeOperation = 'source-over';
      if ((++n & 31) === 0 && performance.now() - t0 > budget) { i++; break; } }
    J.i = i; if (i >= ops.length) { X.mat = { cv: J.cv, M: M }; X.matJ = null; return X.mat; } return null; }
  function _gAttend(G, E, P, X, F) { G.att = true; G.Eg = E; G.Pn = P; G.matX = X; G.Fd = F; G.P = E; G.items = []; G.attente = []; }
  function _gAttente(G, t, now, cw, ch, budget) {   // une glisse en attente de sa matière : quand elle est prête, le glissé part
    if (!G.att || !G.Pn) return; var Mt = _matAvance(G.matX, G.Pn, G.base.M, cw, ch, now, budget); if (!Mt) { window._mondeEncore = true; return; }
    if (G.sprN && !G.sprN.sprOk && !_sprAvance(G.sprN, now, budget)) G.sprN = null;   /* pas prêtes : les empreintes du repos (les déplacements sont faibles à l'équilibre) */
    G.att = false; _gGlisse(G, G.Eg, t, now, G.Fd, Mt); _gArrivees(G, G.Pn, t, now); G.Pn = null; G.matX = null; }
  function _gGlisse(G, E, t, now, F, Mt) { G.mat = Mt; window._ramGlisse = (window._ramGlisse || 0) + 1; var B = G.base, avant = {}, dans = {}, pap = typeof env.papier === 'function' ? env.papier() : null, tb = null;
    B.P.L.forEach(function (e) { avant[e.h] = e; }); E.L.forEach(function (e) { dans[e.h] = e; });
    G.fond = F; G.t0 = t; G.a = 0; G.mv = []; G.items = []; G.attente = []; G.arr = {}; G.E = E; G.P = E;   /* l'exact déjà prêt (le Studio le prépare d'avance) reste */
    var N = G.sprN && G.sprN.sprOk ? G.sprN : null;   /* v87 : au Studio l'état voulu est prêt d'avance — ses yeux glissent DANS LEUR NOUVELLE FORME */
    E.L.forEach(function (e) { var a = avant[e.h], Sn = N && N.spr[e.h], Sp = a && B.spr[e.h];
      if (a && Sn && Sn.fini) G.mv.push({ k: e.h, S: Sn, M: N.M, neuf: true, x0: a.x, y0: a.y, x1: e.x, y1: e.y });
      else if (Sp && Sp.fini) G.mv.push({ k: e.h, S: Sp, M: B.M, x0: a.x, y0: a.y, x1: e.x, y1: e.y }); else if (!a) G.arr[e.h] = 1; });
    B.P.L.forEach(function (e) { if (dans[e.h]) return; tb = tb || _tons(B.P, now); var S0 = B.spr && B.spr[e.h];
      G.items.push({ k: e.h, e: e, ops: _oeilDe(B.P, e.h), m: tb.m, pap: pap, t0: t, s0: 1, dir: -1, spr0: S0 && S0.fini ? S0 : null }); }); }   /* spr0 : l'œil entier, tant que sa première étape n'est pas tracée */
  function _gArrivees(G, P, t, now) { G.Pfin = P; var pap = typeof env.papier === 'function' ? env.papier() : null, tn = null;
    P.L.forEach(function (e) { if (!G.arr[e.h]) return; delete G.arr[e.h]; tn = tn || _tons(P, now); G.items.push({ k: e.h, e: e, ops: _oeilDe(P, e.h), m: tn.m, pap: pap, t0: t, s0: 0, dir: 1 }); }); }
  function _gBouge(G, t) { if (G.att) return true; if (G.mv && G.a < 1) return true; for (var i = 0; i < G.items.length; i++) if (!_gFin(G.items[i])) return true; for (var q in (G.arr || {})) return true; return false; }
  /* ce qu'on voit à la fin du glissé, cuit en un calque : il devient le plumage (comme la v84 gardait le construit) — l'exact ne se
     construit plus derrière, et la boucle s'arrête avec le mouvement */
  function _gCuit(G, t) { var B = G.base, cv = document.createElement('canvas'); cv.width = B.cw; cv.height = B.ch; var c = cv.getContext('2d');
    c.drawImage(G.fond.cv, 0, 0); if (G.mat) c.drawImage(G.mat.cv, 0, 0);
    G.mv.forEach(function (v) { var q = v.neuf ? 0 : 1, dx = Math.round(v.M.a * (v.x1 - v.x0) * q), dy = Math.round(v.M.d * (v.y1 - v.y0) * q); c.drawImage(v.S.cv, v.S.ox + dx, v.S.oy + dy); });
    G.items.forEach(function (it) { if (it.dir > 0 && it.vu && it.vu.s >= 1) c.drawImage(it.cvA, 0, 0, it.vu.w, it.vu.h, it.vu.ox, it.vu.oy, it.vu.w, it.vu.h); });
    var P = G.Pfin; return { plein: B.plein, cv: cv, M: B.M, ms: B.ms, P: P, tsig: _tons(P, t).sig, cw: B.cw, ch: B.ch, cuit: true }; }
  function _gActif(G) { return G.items.length > 0 || !!G.P || !!G.mv; }
  function _gDessine(G, M, t) {   // ce qu'on voit : le plumage de base (ou la matière seule et les yeux qui glissent), puis les yeux qui poussent
    if (G.mv) { _pose(G.fond, M); if (G.mat) _pose(G.mat, M); g.setTransform(1, 0, 0, 1, 0, 0); var B = G.base.M, a = G.a;
      G.mv.forEach(function (v) { var q = v.neuf ? a - 1 : a, dx = Math.round(v.M.a * (v.x1 - v.x0) * q), dy = Math.round(v.M.d * (v.y1 - v.y0) * q); g.drawImage(v.S.cv, v.S.ox + dx, v.S.oy + dy); }); }
    else _pose(G.base, M);
    _gPeint(G, M, t); }
  window._ramTestSpr = function (mode) { var B = _vS; if (!B || !B.sprOk) return 'pas prêt'; var F = _fondPret(B.ms) || _fonds[_fonds.length - 1]; if (!F) return 'pas de fond ' + _fonds.length;
    var cv = document.createElement('canvas'); cv.width = B.cw; cv.height = B.ch; var G = cv.getContext('2d');
    if (mode !== 'sans-fond') G.drawImage(F.cv, 0, 0); if (mode !== 'sans-yeux') B.P.L.forEach(function (e) { var Sp = B.spr[e.h]; if (Sp && Sp.fini) G.drawImage(Sp.cv, Sp.ox, Sp.oy); });
    var x = cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data, y = B.cv.getContext('2d').getImageData(0, 0, cv.width, cv.height).data, ne = 0, de = 0, nm = 0, dm = 0;
    var cv2 = document.createElement('canvas'); cv2.width = B.cw; cv2.height = B.ch; var G2 = cv2.getContext('2d'); B.P.L.forEach(function (e) { var Sp = B.spr[e.h]; if (Sp && Sp.fini) G2.drawImage(Sp.cv, Sp.ox, Sp.oy); });
    var al = G2.getImageData(0, 0, cv.width, cv.height).data;
    for (var i = 0; i < x.length; i += 4) { var d = Math.max(Math.abs(x[i] - y[i]), Math.abs(x[i + 1] - y[i + 1]), Math.abs(x[i + 2] - y[i + 2])) > 12; if (al[i + 3] > 128) { ne++; if (d) de++; } else { nm++; if (d) dm++; } }
    return { pct: _ecartCalques(cv, B.cv), oeil: +(100 * de / ne).toFixed(2), matiere: +(100 * dm / nm).toFixed(2), partOeil: +(100 * ne / (ne + nm)).toFixed(1), url: cv.toDataURL() }; };
  window._ramMatUrl = function () { return _vG && _vG.mat ? _vG.mat.cv.toDataURL() : null; };
  window._ramBancOeil = function () { var P = _vS && _vS.P; if (!P) return null; var e = P.L[0], ops = _oeilDe(P, e.h), m = _tons(P, performance.now()).m, pap = env.papier ? env.papier() : '#fff';
    var cv = document.createElement('canvas'); cv.width = _vS.cw; cv.height = _vS.ch; var G = cv.getContext('2d'); var M = _vS.M, R = {};
    function run(nom, f, s) { var best = 1e9; for (var rep = 0; rep < 4; rep++) { G.setTransform(1, 0, 0, 1, 0, 0); G.clearRect(0, 0, cv.width, cv.height); G.getImageData(0, 0, 1, 1); var t0 = performance.now();
        G.setTransform(M.a, 0, 0, M.d, M.e, M.f); G.translate(e.x, e.y); G.scale(s, s); G.translate(-e.x, -e.y); var n = 0;
        ops.forEach(function (o) { if (!f(o)) return; n++; var st = o[2] === 'B' ? pap : m[o[2]]; if (o[0]) { G.strokeStyle = st; G.lineWidth = o[3]; G.stroke(o[1]); } else { G.fillStyle = st; G.fill(o[1]); } });
        G.getImageData(0, 0, 1, 1); best = Math.min(best, performance.now() - t0); } R[nom + '@' + s] = [n, +best.toFixed(1)]; }
    [1, 0.5].forEach(function (s) { run('tout', function () { return true; }, s); run('aplats', function (o) { return !o[0]; }, s); run('traits', function (o) { return o[0]; }, s); run('couleurs', function (o) { return !o[0] && o[2] !== 'B'; }, s); run('papier', function (o) { return !o[0] && o[2] === 'B'; }, s); });
    return R; };
  var _vG = null, _tMouv = -1e9, _prepRel = null;
  var _msAv = null, _aAv = null, _vBase = null, _tBouge = 0;   // _vBase : le dernier calque ENTIER, posé sous un calque borné à la vue
  function _pose(L, M, alpha) { var A = L.M, ia = 1 / A.a, id = 1 / A.d, sx = M.a * ia, sy = M.d * id;
    g.setTransform(sx, 0, 0, sy, M.e - A.e * sx, M.f - A.f * sy); if (alpha != null) g.globalAlpha = alpha; g.drawImage(L.cv, 0, 0); g.globalAlpha = 1; }
  var _ctxTo = null, _msT = null, _tMsT = 0;
  function _gardeCtx() { return { calC: _calC, pJ: _pJ, aJ: _aJ, aS: _aS, aF: _aF, aK: _aK, gel: _apGel, films: _filmsK, calWJ: _calWJ, t: RramAp.t }; }
  function _prendCtx(c) { _calC = c.calC; _pJ = c.pJ; _aJ = c.aJ; _aS = c.aS; _aF = c.aF; _aK = c.aK; _apGel = c.gel; _filmsK = c.films; _calWJ = c.calWJ; RramAp.t = c.t; }
  function _cleToile() { var L = []; for (var i = 0; i < seeds.length; i++) { var s = seeds[i]; if (s.kind === 'gray' || s.part != null) continue; L.push(_cle(s)); } L.sort(function (a, b) { return a - b; });
    var h = 2166136261; L.forEach(function (v) { h ^= v; h = Math.imul(h, 16777619) >>> 0; }); return 'T' + (env.cleToile == null ? 0 : env.cleToile) + ':' + Math.round(W) + 'x' + Math.round(H) + '|' + (h >>> 0).toString(36) + '.' + L.length; }
  var _GLOB = ['_ramBouge', '_apOccupe', '_ramAp', '_ramComp', '_ramCalque', '_apPhase', '_apPhaseBase'];
  var _vueTo = null;   /* v92 : la vue et la taille de la dernière image de la Toile — la préparation d'avance s'y cale */
  function RramToile(now, cv0) { var M = g.getTransform(), ms = [M.a, M.d, M.e, M.f, cv0.width, cv0.height].join(','), t = performance.now(), sv = {}, ap = _gardeCtx(); _vueTo = { M: M, ms: ms, cw: cv0.width, ch: cv0.height };
    _GLOB.forEach(function (k) { sv[k] = window[k]; });
    _prendCtx(_ctxTo || (_ctxTo = { calC: [], pJ: null, aJ: null, aS: null, aF: null, aK: null, gel: null, films: {}, calWJ: {}, t: undefined }));
    window._ramToileAp = true; var K = _cleToile(); window._apPhase = K; window._apPhaseBase = K;
    try {
      /* la vue a changé (zoom, glissé) : l'état affiché se pose à la nouvelle vue ; le net se refait quand la vue est posée (comme avant) */
      if (_aS && _aS.sem === K.split('|')[0] && _aS.ms !== ms && !_aK) { if (ms !== _msT) { _msT = ms; _tMsT = t; }
        var Cz = (t - _tMsT > 150) ? _calDemande(_etatFinal(), K, ms, M, cv0.width, cv0.height, now) : null;
        if (Cz) { _calGarde(Cz); _aS = Cz; } else { window._mondeEncore = true; g.save(); _pose(_aS, M); g.restore(); _dernier = _aS.P; return; } }
      var Fp = _filmsK[K + '|' + ms]; if (Fp && Fp.avance && !Fp.valide) {   /* v92 : un film préparé d'avance ne sert que si l'arrivée est bien celle qu'il a préparée (places, couleurs) */
        if (_sigL(_etatFinal().L) !== Fp.sigB) { _filmOte(K + '|' + ms); delete _calWJ[K + '|' + ms]; _calC = _calC.filter(function (c) { return !(c.K === K && c.ms === ms); }); window._ramAvanceRate = (window._ramAvanceRate || 0) + 1; }
        else { Fp.valide = true; window._ramAvanceBon = (window._ramAvanceBon || 0) + 1; } }
      if (_aS && _aS.sem === K.split('|')[0] && _aS.ms === ms && _aS.K !== K && !_filmsK[K + '|' + ms]) {   /* une parole plantée ou retirée : le film part tout de suite, depuis ce qu'on voit */
        var A4 = (_aK && (_aK.pret || _aK.V)) || _aS; if (_aK && (_aK.pret || _aK.V)) _apGelDe(A4);
        if (!window._ramPleinSansWorker) { var Cp4 = _calDemande(_etatFinal(), K, ms, M, cv0.width, cv0.height, now); if (Cp4) _calGarde(Cp4); }   /* v92 : l'état d'arrivée part AVANT le film — il ne fait plus attendre la pousse */
        var F4 = _filmLance(A4, A4.P.L, _etatFinal().L, ms, M, now); if (F4) { _filmsK[K + '|' + ms] = F4; _filmsBorne(); } }
      try { RramAp(now, t, M, ms, cv0); } catch (eT) { window._ramToileErr = String(eT && eT.stack || eT); throw eT; }
      window._ramToileEtat = { K: K, aS: _aS ? _aS.K : null, aK: !!_aK, calC: _calC.length, films: Object.keys(_filmsK).length, ms: ms };
    } finally { window._ramToileAp = false; window._ramToileBouge = !!_aK; _ctxTo = _gardeCtx(); _prendCtx(ap); _GLOB.forEach(function (k) { window[k] = sv[k]; }); } }
  /* ⚑ v92 (Tom : « feu vert pour préparer le film avant le geste ») — appelée PENDANT une plantation simulée (`Toile.simule`) : les
     graines sont celles d'après le geste. On lance le film et l'état d'arrivée sous la clé qu'aura la Toile ; au vrai geste, RramToile
     les trouve prêts (ou en cours : la lecture progressive prend le relais). */
  function _sigL(L) { return L.map(function (e) { return e.h + ':' + Math.round(e.x) + ':' + Math.round(e.y) + ':' + e.s.ci + ':' + (e.s.lit | 0); }).join('|'); }
  Rram.prepareToile = function () { if (window._ramToileAncien || !_filmPool() || !_vueTo || !_ctxTo || !_ctxTo.aS) return false;
    _sync(); var sv = {}, ap = _gardeCtx(), r = false; _GLOB.forEach(function (k) { sv[k] = window[k]; }); _prendCtx(_ctxTo);
    window._ramToileAp = true; var K = _cleToile(); window._apPhase = K; window._apPhaseBase = K;
    try { var ms = _vueTo.ms, M = _vueTo.M, now = performance.now();
      var E = _etatFinal(), F0 = _filmsK[K + '|' + ms];
      if (F0 && F0.avance && F0.sigB !== _sigL(E.L)) { _filmOte(K + '|' + ms); delete _calWJ[K + '|' + ms]; _calC = _calC.filter(function (c) { return !(c.K === K && c.ms === ms); }); }   /* même clé, autre arrivée (un autre tirage) : on refait */
      if (_aS && _aS.ms === ms && _aS.K !== K && !_filmsK[K + '|' + ms]) { var A4 = (_aK && (_aK.pret || _aK.V)) || _aS;
        if (!window._ramPleinSansWorker) { var Cp = _calDemande(E, K, ms, M, _vueTo.cw, _vueTo.ch, now); if (Cp) _calGarde(Cp); }
        var F4 = _filmLance(A4, A4.P.L, E.L, ms, M, now); if (F4) { F4.avance = true; F4.sigB = _sigL(E.L); _filmsK[K + '|' + ms] = F4; _filmsBorne(); }
        r = K; } }
    finally { window._ramToileAp = false; _ctxTo = _gardeCtx(); _prendCtx(ap); _GLOB.forEach(function (k) { window[k] = sv[k]; }); }
    return r; };
  Rram.filmEnCours = function () { for (var k in _ctxTo ? _ctxTo.films : {}) { var F = _ctxTo.films[k]; if (F && F.avance && !F.fini && !F.echec) return true; } return false; };
  function Rram(now, x0, y0, x1, y1) {
    _sync(); var cv0 = g && g.canvas;
    if (!env.vive || window._perfAncien || window._v72SansCalque || env.DPR > 3 || !cv0 || !g.getTransform || Math.abs(g.getTransform().b) > 1e-9) return RramDirect(now);
    if (window._apImage) { var Ma = g.getTransform(); return RramAp(now, performance.now(), Ma, [Ma.a, Ma.d, Ma.e, Ma.f, cv0.width, cv0.height].join(','), cv0); }
    /* ⚑ v92 (Tom : « Ramage au Studio est parfait — porte exactement ce mouvement sur la vraie Toile ») — LA TOILE PREND LE CHEMIN DU
       STUDIO : les yeux gardent leur place et leur taille, l'œil qui arrive pousse (film des Workers), celui qui part se résorbe. Son
       état est à elle (jamais celui de l'aperçu), sa clé est celle des yeux présents. `_ramToileAncien` rend l'ancien chemin. */
    if (!window._ramToileAncien && _filmPool()) return RramToile(now, cv0);   // v75 : l'aperçu du Studio a son propre chemin
    var M = g.getTransform(), ms = [M.a, M.d, M.e, M.f, cv0.width, cv0.height].join(','), E = _cible(now), tr = !!env.trans;
    var t = performance.now(), dt = t - _vAppel; _vAppel = t; var stable = ms === _msAv; _msAv = ms;
    /* ⚑ v74 — dès que l'ÉCHELLE est posée, le calque net se refait, même si la vue glisse encore (l'élan après le lâcher dure
       jusqu'à ~0,8 s) : pendant ce glissé, il se pose décalé — une translation, pas un agrandissement. */
    if (!stable) _tBouge = t; var echS = (M.a === _aAv), immobile = stable && t - _tBouge > 120; _aAv = M.a;   // immobile : la vue n'a pas bougé depuis 120 ms (entre deux mouvements d'un doigt, deux images identiques ne suffisent pas) if (!stable && echS && _vS && _vS.M.a !== M.a) stable = true;
    // ce qui est à l'écran est-il la cible ? même état, mêmes couleurs, et — si la vue est posée — la même vue
    var _cur = (_vG && _vG.pret) ? _vG.pret : _vS;   /* v87 : un plumage exact prêt, qui attend que l'œil ait fini de pousser */
    var ok = _cur && _cur.P.h === E.h && (!stable || _cur.ms === ms), tons = ok ? _tons(_cur.P, now) : null; if (ok && tons.sig !== _cur.tsig) ok = false;
    if (!ok) {
      if (!_vS || (!tr && !_vF && !_vJ && dt > 400) || (_vS.cw !== cv0.width || _vS.ch !== cv0.height)) {   // aucun calque, ou un changement après un long repos : tout de suite
        var P0 = _plumeDe(E), t0 = performance.now(), T0 = _tons(P0, now), C0 = _calque(P0, T0, M, cv0.width, cv0.height); _tranche(C0, 1e9, t0);
        _vS = { plein: C0.plein, cv: C0.cv, M: M, ms: ms, P: P0, tsig: T0.sig, cw: cv0.width, ch: cv0.height }; _vJ = null; _vF = null; _vG = null;
        window._ramCalque = { direct: ((window._ramCalque || {}).direct || 0) + 1, ms: Math.round(performance.now() - t0) };
      } else {   // la cible a changé : elle se construit par tranches, ce qu'on voyait reste à l'écran, puis elle passe dessus en fondu
        if (!_vJ || _vJ.E.h !== E.h || (stable && _vJ.M.a !== M.a) || (_vJ.tons && tons && _vJ.tons.sig !== tons.sig)) { if (_vJ && _vJ.nu && _vJ.C && _vJ.C.i > 0 && _vS && _vJ.ms === _vS.ms) _vS = _cuire(_vS, _vJ.C, _vJ.M, _vJ.cw, _vJ.ch);   // v81 : une construction interrompue reste à l'écran
          _vJ = _travail(E, now, M, cv0.width, cv0.height, ms); _vJ.vue = !!(_vS && _vS.P.h === E.h); _vJ.pousse = !_vJ.vue && !(_vS && _vS.approx && _vS.P.h === E.h); }   /* v87 : un plumage NEUF se construit à part ; ses yeux neufs poussent */   // vue : la même Toile, à une autre vue ; nu : un plumage NEUF, qui se construit sous les yeux
        var budget = Math.max(4, Math.min(9, (dt > 0 && dt < 200 ? dt : 16.7) * 0.5)); _vJ.immobile = !!(_vJ.vue && immobile && !tr && !(_vS && _vS.approx));   /* v84 : le plumage exact qui remplace les rosaces se refait au budget d'une image, pas au grand pas de la netteté */ if (_vJ.C) _vJ.C.immobile = _vJ.immobile;
        if (_vJ.pousse && !_vJ.gl && !_vJ.gc) { _vJ.gl = true; var _Fd = _fondPret(ms);
          if (!(_vG && _gActif(_vG)) && _Fd && _vS.sprOk && _vS.ms === ms) { _vG = { base: _vS, items: [], attente: [] }; _gAttend(_vG, E, null, null, _Fd); _vJ.glisse = true; } }
        /* v87 : pendant que les yeux glissent ou poussent, AUCUN autre travail — le plumage exact se construit une fois tout immobile
           (sous WebKit sa rastérisation coûte ~2 s : répartie sur le glissé, elle le mettait à 300 ms par image) */
        var _gb = _vJ.glisse && _vG && _vJ.P && (_vG.att ? !!_vG.Pn : _gBouge(_vG, t));   /* pendant le glissé : l'exact n'avance qu'à petit budget, et seulement si les images restent rapides (Chromium) — sous WebKit sa rastérisation les ralentit, il s'arrête de lui-même */
        var _fini = (_gb && !(dt > 0 && dt < 20 && !_vG.att)) ? false : _avance(_vJ, now, _gb ? 3 : budget, dt);
        if (_vJ.pousse && _vJ.P && !_vJ.gc) { _vJ.gc = true; if (_vJ.glisse && _vG && _vG.att) { _vG.Pn = _vJ.P; _vG.matX = _vG; } else { if (!_vG) _vG = { base: _vS, items: [], attente: [] }; _gCible(_vG, _vJ.P, t, now); } }
        if (_fini && _vJ.pousse) { _vF = null; if (!_vJ.C.plein) { if (_vS.plein !== false) _vBase = _vS; } else _vBase = null; _vG.pret = { plein: _vJ.C.plein, cv: _vJ.C.cv, M: _vJ.M, ms: _vJ.ms, P: _vJ.P, tsig: _vJ.tons.sig, cw: _vJ.cw, ch: _vJ.ch };
          window._ramCalque = { travail: Math.round(_vJ.t), images: _vJ.n, direct: (window._ramCalque || {}).direct || 0 }; _vJ = null; }
        else if (_fini) { var _apx = !!(_vS && _vS.approx); if (false) { } else if (_apx) { if (window._ramMesure) window._ramCorr = _ecartCalques(_vS.cv, _vJ.C.cv); _vF = null; } else _vF = { de: _vS, t0: t, dur: (_vJ.P === _vS.P && _vJ.tons.sig === _vS.tsig) ? 150 : ARR };   /* v81 : construit sous les yeux — pas de fondu */   /* v74 : la même Toile, nette à la nouvelle vue — un fondu court */ if (!_vJ.C.plein) { if (_vS.plein !== false) _vBase = _vS; } else _vBase = null; /* v84 : le plumage construit dans l'ordre des rosaces RESTE (il ne diffère de l'exact que par l'ordre de recouvrement aux frontières des
             rosaces, ~4 % des pixels, mesuré) : aucun échange, donc aucune correction visible. L'exact revient au prochain changement de vue. */
          _vS = { plein: _vJ.C.plein, cv: _vJ.C.cv, M: _vJ.M, ms: _vJ.ms, P: _vJ.P, tsig: _vJ.tons.sig, cw: _vJ.cw, ch: _vJ.ch };
          window._ramCalque = { travail: Math.round(_vJ.t), images: _vJ.n, direct: (window._ramCalque || {}).direct || 0 }; _vJ = null; }
        window._mondeEncore = true;
      }
    }
    if (!stable) window._mondeEncore = true;   // la vue bouge encore : on revient poser le calque exact
    if (_vG) { _gAttente(_vG, t, now, cv0.width, cv0.height, 10); if (_gPas(_vG, t)) window._mondeEncore = true; _vS = _vG.base; if (_vS.cuit && _vJ && _vJ.P === _vS.P) _vJ = null; if (!_gActif(_vG) && !_vG.pret) _vG = null; }
    else if (!_vJ && !_vF && immobile && !tr && _vS && _vS.ms === ms) {   /* au repos : la matière seule et les empreintes des yeux, par petites tranches */
      /* elle ne tient pas la boucle éveillée juste après un mouvement (le mouvement est fini ; rien ne bouge à l'écran) : elle attend
         que la boucle se soit arrêtée, et la relance elle-même un peu plus tard */
      if (t - _tMouv < 600) { if (!_prepRel && !(_fondPret(ms) && _vS.sprOk)) _prepRel = setTimeout(function () { _prepRel = null; try { env.relance(); } catch (_) {} }, 700); }
      else if (!_fondAvance(ms, M, cv0.width, cv0.height, now, 8) || !_sprAvance(_vS, now, 8)) window._mondeEncore = true; }
    if (_vG || _vJ || tr) _tMouv = t;
    g.save();
    if (_vBase && _vS.plein === false && _vBase.P.h === _vS.P.h) _pose(_vBase, M);
    if (_vF && t - _vF.t0 < (_vF.dur || ARR)) { _vF.a = _lisse((t - _vF.t0) / (_vF.dur || ARR)); _pose(_vF.de, M); _pose(_vS, M, _vF.a); window._mondeEncore = true; }
    else if (_vG) { _vF = null; _gDessine(_vG, M, t); }   // v87 : la matière et les yeux qui glissent, ceux qui poussent ou se résorbent
    else { _vF = null; _pose(_vS, M); }
    g.restore();
    _dernier = (_vF ? _vF.de.P : _vS.P); window._ramComp = { ops: _vS.P.ops.length, yeux: _vS.P.L.length };
  }

  /* ⚑ v72 — L'ŒIL D'UNE DALLE SEULE SE LIT DANS LE PLUMAGE DE LA TOILE. La planche le refaisait en mode « only » : tout le champ
     des plumes recalculé (~150 ms) pour n'en tracer qu'une rosace — et le pré-rendu des dalles (Index, Fil, page +) le payait pour
     chacune. Les tracés de l'œil sont ceux du plumage, dans le même ordre (le mode « only » sautait les autres plumes, rien de plus),
     et le papier y EFFACE (`destination-out`), exactement ce que fait « only ». Le plumage lu est celui qu'on voit. */
  function _etatVu(now) { if (_vTr && (env.trans || _reste(_vTr.E))) return _vTr.E; return _etatRepos(now); }
  function _oeil(s, now) { _sync(); var k = _cle(s), E = _etatVu(now), P = (_dernier && _dernier.h === E.h) ? _dernier : _plumeDe(E);
    var O = (P.oeils || (P.oeils = {}))[k]; if (O !== undefined) return O;
    var ops = [], b = [1e18, 1e18, -1e18, -1e18]; P.ops.forEach(function (o) { if (o[5] !== k) return; ops.push(o); var q = o[6];
      if (q[0] < b[0]) b[0] = q[0]; if (q[1] < b[1]) b[1] = q[1]; if (q[2] > b[2]) b[2] = q[2]; if (q[3] > b[3]) b[3] = q[3]; });
    return (P.oeils[k] = ops.length ? { ops: ops, L: P.L, b: b } : null); }
  function seule(nom, s, now, cx, cy, taille) {
    if (window._v72Preuve && window._v72Preuve.ancien) { _sync(); var PA = _plumage(now, _cle(s)); if (!PA) return false; var BA = PA.b, scA = taille / Math.max(BA[2] - BA[0], BA[3] - BA[1], 1e-6);
      g.save(); g.translate(cx, cy); g.scale(scA, scA); g.translate(-(BA[0] + BA[2]) / 2, -(BA[1] + BA[3]) / 2); _rejoue(PA, now); g.restore(); return true; }
    var O = _oeil(s, now); if (!O) return false; var B = O.b, sc = taille / Math.max(B[2] - B[0], B[3] - B[1], 1e-6);
    g.save(); g.translate(cx, cy); g.scale(sc, sc); g.translate(-(B[0] + B[2]) / 2, -(B[1] + B[3]) / 2);
    var rm = typeof env.rampeMat === 'function' ? env.rampeMat() : env.rampeMat, memo = {};
    for (var i = 0; i < O.ops.length; i++) { var o = O.ops[i], pap = o[2] === 'B', st = pap ? '#000' : (memo[o[2]] || (memo[o[2]] = _resout(o[2], O.L, now, null, rm)));
      if (pap) g.globalCompositeOperation = 'destination-out';
      if (o[0]) { g.strokeStyle = st; g.lineWidth = o[3]; g.stroke(o[1]); } else { g.fillStyle = st; g.fill(o[1]); }
      if (pap) g.globalCompositeOperation = 'source-over'; }
    g.restore(); return true;
  }
  // le contour de l'œil : l'enveloppe de ce que sa dalle seule trace (l'œil est une rosace : son enveloppe est son bord)
  var _env = {};
  function _enveloppe(s) { _sync(); var k = _cle(s), P = _dernier || _plumage(performance.now(), 0); if (!P) return null;
    var c = _env[k]; if (c && c.P === P) return c.pts;
    var e = null; for (var i = 0; i < P.L.length; i++) if (P.L[i].h === k) { e = P.L[i]; break; } if (!e) return null;
    var pts = [], N = 48, r = e.R * 0.9;
    // v68b : le contour EST ce que le toucher prend — le cœur de l'œil posé dans la Toile, au rayon 0,9 R (un seul propriétaire de la forme touchable)
    for (var a = 0; a < N; a++) pts.push([e.x + Math.cos(a / N * 6.2832) * r, e.y + Math.sin(a / N * 6.2832) * r]);
    _env[k] = { P: P, pts: pts }; return pts; }
  function contour(nom, s) { return _enveloppe(s); }
  function nature(nom, s) { return _oeil(s, performance.now()) ? 'dalle' : null; }
  function boite(nom, s) { var P = (window._v72Preuve && window._v72Preuve.ancien) ? (_sync(), _plumage(performance.now(), _cle(s))) : _oeil(s, performance.now()); if (!P) return null; var B = P.b;
    return { x0: B[0] - 0.5, y0: B[1] - 0.5, x1: B[2] + 0.5, y1: B[3] + 0.5, fx0: B[0] - 0.5, fy0: B[1] - 0.5, fx1: B[2] + 0.5, fy1: B[3] + 0.5 }; }
  // le toucher : dans l'œil — la rosace de la promesse la plus proche dont le point est au cœur
  function toucher(nom, x, y) { _sync(); var P = _dernier || _plumage(performance.now(), 0), best = null, bd = 1e18;
    P.L.forEach(function (p) { if (p.s.part != null) return; var d = Math.hypot(x - p.x, y - p.y) / (p.R * 0.9); if (d < 1 && d < bd) { bd = d; best = p.s; } });
    return best; }
  function _anc(P, k) { if (!P) return null; for (var i = 0; i < P.L.length; i++) if (P.L[i].h === k) return [P.L[i].x, P.L[i].y, P.L[i].R * 1.4]; return null; }
  // v72 : pendant le fondu, le titre glisse de l'œil d'avant à l'œil d'arrivée (au lieu de sauter à la fin)
  Rram.ancre = function (s) { var k = _cle(s);
    if (_vG && _vG.mv) { var B0 = _anc(_vG.base.P, k), B1 = _anc(_vG.E, k), ga = _vG.a; if (B0 && B1) return [B0[0] + (B1[0] - B0[0]) * ga, B0[1] + (B1[1] - B0[1]) * ga, B0[2] + (B1[2] - B0[2]) * ga]; if (B1) return B1; }
    if (!window._ramToileAncien && _ctxTo && _ctxTo.aS) { var At = _anc(_ctxTo.aS.P, k); if (At) return At; }   /* v92 : l'œil de la Toile est là où le chemin du Studio l'a posé */
    var A1 = _anc(_vS ? _vS.P : _dernier, k), A0 = _vF ? _anc(_vF.de.P, k) : null;
    if (A0 && A1 && _vF.a != null) { var a = _vF.a; return [A0[0] + (A1[0] - A0[0]) * a, A0[1] + (A1[1] - A0[1]) * a, A0[2] + (A1[2] - A0[2]) * a]; }
    return A1 || A0 || _anc(_dernier, k); };
  // v72 — preuve : le même plumage peint d'un bloc, puis par tranches (une relecture d'un pixel entre deux tranches vide le lot du GPU)
  window._ramTranches = function (pas) { _sync(); var E = _cible(performance.now()), P = _plumeDe(E), M = g.getTransform(), cw = g.canvas.width, ch = g.canvas.height, T0 = _tons(P, performance.now());
    var A = _calque(P, T0, M, cw, ch); _tranche(A, 1e9, performance.now());
    var B = _calque(P, T0, M, cw, ch); for (var i = 0; i < P.ops.length; i += pas) { var fin = Math.min(P.ops.length, i + pas), ops = P.ops; for (var j = i; j < fin; j++) { var o = ops[j], st = o[2] === 'B' ? B.pap : T0.m[o[2]]; if (o[0]) { B.G.strokeStyle = st; B.G.lineWidth = o[3]; B.G.stroke(o[1]); } else { B.G.fillStyle = st; B.G.fill(o[1]); } } B.G.getImageData(0, 0, 1, 1); }
    var a = A.G.getImageData(0, 0, cw, ch).data, b = B.G.getImageData(0, 0, cw, ch).data, n = 0, mx = 0; for (var k = 0; k < a.length; k += 4) { var d = Math.max(Math.abs(a[k] - b[k]), Math.abs(a[k + 1] - b[k + 1]), Math.abs(a[k + 2] - b[k + 2])); if (d > 2) n++; if (d > mx) mx = d; }
    return { pct: +(100 * n / (a.length / 4)).toFixed(3), max: mx }; };
  window._ramVue = function () { return { items: _vG ? _vG.items.map(function (it) { return [it.dir, it.vu ? +it.vu.s.toFixed(2) : null, it.job ? it.job.i + '/' + it.ops.length : null, it.k, Math.round(it.e.x), Math.round(it.e.y)]; }) : null, arr: _vG && _vG.arr ? Object.keys(_vG.arr).length : null, mv: _vG && _vG.mv ? _vG.mv.length : null, spr: !!(_vS && _vS.sprOk), sprI: _vS && _vS.sprI, fond: !!(_vS && _fondPret(_vS.ms)), fJ: _fJ ? (_fJ.P ? 'peint ' + (_fJ.C && _fJ.C.i) : 'file ' + _fJ.qi) : null, vG: _vG ? (_vG.att ? 'attend' : _vG.mv ? 'glisse' : 'pousse') : null, vu: _vS && _vS.ms, M: _vS && [_vS.M.a, _vS.M.e, _vS.M.f], av: _msAv, travail: !!_vJ, fondu: _vF ? _vF.dur : null, vtr: !!_vTr, qi: _vJ ? _vJ.qi : null, Q: _vJ && _vJ.Q ? _vJ.Q.length : null, ci: _vJ && _vJ.C ? _vJ.C.i : null, pas: Math.round(_pasT), n: _vJ ? _vJ.n : null }; };   // lecture (bancs)
  /* v75 — préparer d'avance, par tranches, le calque d'un état de l'aperçu (1 : le repos, 2 : l'arrivée) ; vrai quand il est prêt */
  Rram.prepare = function (now, budget, quoi, vite) { _sync(); var cv0 = g && g.canvas; if (!cv0 || !g.getTransform) return true;
    var M = g.getTransform(), ms = [M.a, M.d, M.e, M.f, cv0.width, cv0.height].join(','), K = window._apPhase, t0p = performance.now();
    var Cx = K ? _calAp(K, ms, cv0.width, cv0.height, now) : null;
    if (window._ramFilmDbg) { var _lg = window._ramCtLog = window._ramCtLog || []; var _e = [quoi, K, window._apPhaseBase, env.cleToile, env.uMat, W, H]; if (!_lg.length || _lg[_lg.length - 1].join() !== _e.join()) _lg.push(_e); }
    if (!K) return true;
    if (Cx && quoi === 1) _apGelDe(Cx);
    if (Cx && quoi === 2 && !window._ramFilmOff) {   /* v90 : le film de la pousse, d'avance — depuis ce qu'on voit, ou (Ramage pas encore
                                                       à l'écran, `apercuPrepare`) depuis le repos déjà préparé : le premier événement l'a aussi */
      var _aP = _aK && (_aK.pret || _aK.V);   /* v91 : pendant une pousse, la base du prochain est l'état qu'elle atteint (déjà prêt) */
      var Ax = (_aP && _aP.sem === Cx.sem && _aP.ms === ms) ? _aP : (_aS && _aS.sem === Cx.sem && _aS.ms === ms) ? _aS : _calAp(window._apPhaseBase, ms, cv0.width, cv0.height, now);
      if (Ax && Ax !== Cx) { _filmAvance(Ax, Cx, M, now, budget); return _filmPas(Cx, M, Math.max(1, budget - (performance.now() - t0p)), 1e9); } }   /* le film se trace sur ses propres canevas : son coût est payé DANS le budget (mesuré), pas après */
    if (Cx) {   /* ⚑ v89 — le plumage est prêt : on prépare aussi ce que son glissé lira (la matière seule, les empreintes du repos et de l'arrivée,
                   la matière de l'arrivée) — sans quoi, à l'ouverture de Ramage, le premier événement attendait ~1 s */
      return true; }   /* v89 : au Studio plus de glissé — le plumage prêt suffit (les yeux qui partent se résorbent en vecteur) */
    /* v87 : au Studio, Ramage se lit TOUJOURS à l'équilibre du moteur (`env.finale`) — la composition d'ouverture de l'aperçu n'y
       est pas encore : au premier événement le moteur relâchait toutes les graines de plusieurs centaines de pixels, et un plumage
       ne peut pas suivre un tel mouvement sans sauter. À l'équilibre, un événement ne déplace ses voisines que de quelques pixels. */
    if (!window._ramPleinSansWorker && _filmPool()) {   /* v91 : l'état entier se peint dans le Worker — le fil principal n'en paie que la pose */
      if (quoi === 2 && _aK && (_aK.pret || _aK.V)) _apGelDe(_aK.pret || _aK.V);   /* v91 : pendant une pousse, l'œil qui pousse garde SA taille dans l'état suivant (sans quoi il y est recalculé, et la pousse suivante saute) */
      var Ew = _etatFinal(), Cw = _calDemande(Ew, K, ms, M, cv0.width, cv0.height, now);
      if (quoi === 2 && !window._ramFilmOff && !_filmsK[K + '|' + ms]) { var _aP3 = _aK && (_aK.pret || _aK.V), sem3 = String(K).split('|')[0];
        var A3 = (_aP3 && String(_aP3.sem) === sem3 && _aP3.ms === ms) ? _aP3 : (_aS && String(_aS.sem) === sem3 && _aS.ms === ms) ? _aS : _calAp(window._apPhaseBase, ms, cv0.width, cv0.height, now);
        if (A3 && A3.P) { var F3 = _filmLance(A3, A3.P.L, Ew.L, ms, M, now); if (F3) { _filmsK[K + '|' + ms] = F3; _filmsBorne(); } } }
      if (Cw) { var Fk3 = _filmsK[K + '|' + ms]; if (Fk3 && !Cw.film) Cw.film = Fk3; _calGarde(Cw); if (quoi === 1) _apGelDe(Cw); }
      if (Cw !== false) return false; }
    if (!_pJ || _pJ.K !== K || _pJ.ms !== ms) { _pJ = _travail(_etatFinal(), now, M, cv0.width, cv0.height, ms); _pJ.K = K;
      /* v91 : le film part au Worker tout de suite — il ne lit que les yeux, pas le plumage */
      if (quoi === 2 && !window._ramFilmOff && !_filmsK[K + '|' + ms]) { var _aP2 = _aK && (_aK.pret || _aK.V), sem2 = String(K).split('|')[0];
        var A2 = (_aP2 && String(_aP2.sem) === sem2 && _aP2.ms === ms) ? _aP2 : (_aS && String(_aS.sem) === sem2 && _aS.ms === ms) ? _aS : _calAp(window._apPhaseBase, ms, cv0.width, cv0.height, now);
        if (A2 && A2.P) { var F2 = _filmLance(A2, A2.P.L, _pJ.E.L, ms, M, now); if (F2) { _filmsK[K + '|' + ms] = F2; _filmsBorne(); } } } }
    /* v89 : une préparation de fond avance au pas PLANCHER (100 tracés) : sous WebKit la rastérisation se paie après le budget en
       JavaScript — au pas de 900, chaque image de préparation durait 70 à 87 ms, et l'aperçu visible en saccadait */
    _pJ.pasFond = !vite; if (_avance(_pJ, now, budget, 16.7)) { var Cn = _calDe(_pJ, K); var Fk = _filmsK[K + '|' + ms]; if (Fk && !Cn.film) Cn.film = Fk; _calGarde(Cn); if (quoi === 1) _apGelDe(Cn); _pJ = null; }
    return false; };   /* v89 : le plumage fait, la suite (matière, empreintes) se prépare aux appels suivants */
  /* v89 : l'état K (tiré d'avance au Studio) est-il prêt à glisser — plumage, matière, empreintes ? */
  window._ramBaseSig = function () { if (!_aS) return null; var T = _tons(_aS.P, performance.now()); if (T.sig === _aS.tsig) return 'ok'; var a = _aS.tsig.split('|'), b = T.sig.split('|'), d = []; _aS.P.toks.filter(function (t) { return t !== 'B'; }).forEach(function (t, i) { if (a[i] !== b[i]) d.push(t + ':' + a[i] + '>' + b[i]); }); return d.slice(0, 6).join(' ; ') + ' (' + d.length + ')'; };
  window._ramPret = function (K) { for (var i = _calC.length - 1; i >= 0; i--) { var e = _calC[i]; if (e.K === K) return window._ramFilmOff || !(_aS && _aS !== e && _aS.sem === e.sem && _aS.ms === e.ms) || !!(e.film && e.film.fini && e.film.de === _aS); } return false; };   /* v90 : et son film tracé */
  Rram.transDur = 1600; Rram.douce = true; Rram.partDur = 900; Rram.toucheStrict = true;
  return { ramage: Rram, seule: seule, contour: contour, toucher: toucher, nature: nature, boite: boite };
}
window.creerRamage = creerRamage;
})();

/* ══════════════════ bloc « moteur (la Toile) » ══════════════════ */
(function(){
var host=document.getElementById('toileCv'); if(!host)return;
var SIGNAL=[[255,214,10],[255,122,162],[0,95,115],[255,244,194]];
/* ⚑ v36 (Tom, 24 sept.) — « les filets autour des disques et sous le trait sont trop marqués, trop clairs : ça dénote ».
   Même crème que le contour des plateaux et l'anneau du bouton de tri (#F7F0DE, mesuré identique au pixel), mais à 55 % :
   un filet est une aide discrète de différenciation, pas un élément. Une seule valeur pour tous les peintres. */
window._FILET_DOUX='rgba(247,240,222,.55)';
var PALS={signal:{name:'Ingénu',cols:[[130,174,248],[255,184,210],[201,168,245],[239,227,199]]},primesautier:{name:'Primesautier',cols:[[255,214,10],[255,122,162],[0,95,115],[255,244,194]]},candide:{name:'Candide',cols:[[205,180,255],[255,200,162],[189,224,168],[255,181,200]]},gouailleur:{name:'Gouailleur',cols:[[156,74,26],[224,122,31],[233,184,36],[125,139,46]]},alangui:{name:'Alangui',cols:[[196,166,159],[125,106,138],[221,203,176],[140,151,171]]},irascible:{name:'Irascible',cols:[[255,45,26],[255,138,28],[184,15,46],[43,10,10]]},hurluberlu:{name:'Hurluberlu',cols:[[200,255,0],[123,47,247],[255,61,154],[43,20,0]]},beat:{name:'Béat',cols:[[31,79,209],[255,194,26],[255,255,255],[224,103,63]]},minaudier:{name:'Minaudier',cols:[[255,159,200],[224,17,95],[255,224,236],[181,242,255]]},chafouin:{name:'Chafouin',cols:[[169,180,31],[230,163,190],[108,70,117],[63,167,214]]},frivole:{name:'Frivole',cols:[[255,113,206],[1,205,254],[5,255,161],[255,251,150]]},cajoleur:{name:'Cajoleur',cols:[[159,230,207],[75,43,31],[255,240,212],[226,62,87]]},allegre:{name:'Allègre',cols:[[31,179,106],[126,200,255],[14,94,74],[239,251,234]]},lunatique:{name:'Lunatique',cols:[[43,196,196],[217,162,27],[194,24,91],[30,27,58]]},flegmatique:{name:'Flegmatique',cols:[[207,232,255],[111,168,220],[74,90,106],[255,179,167]]},narquois:{name:'Narquois',cols:[[255,154,90],[122,31,162],[255,232,214],[255,47,109]]},truculent:{name:'Truculent',cols:[[255,62,0],[0,229,255],[86,0,214],[246,255,0]]},petulant:{name:'Pétulant',cols:[[255,138,0],[104,0,224],[0,200,90],[255,170,200]]},fantasque:{name:'Fantasque',cols:[[0,255,140],[230,0,115],[0,64,255],[255,247,222]]},fielleux:{name:'Fielleux',cols:[[26,20,0],[90,51,0],[255,230,0],[179,143,0]]},sibyllin:{name:'Sibyllin',cols:[[10,10,31],[42,27,77],[94,44,165],[0,224,255]]},veneneux:{name:'Vénéneux',cols:[[20,0,20],[74,0,51],[255,0,122],[192,192,192]]},atrabilaire:{name:'Atrabilaire',cols:[[10,46,54],[27,111,128],[255,158,0],[242,242,242]]},taciturne:{name:'Taciturne',cols:[[11,13,79],[42,42,212],[143,140,255],[228,226,255]]}};
var palKey='signal',hueShift=0;   /* ⚑ 20 sept. (Tom) : la palette par défaut est celle de l'identité */
function rotc(c,deg){var r=c[0]/255,gg=c[1]/255,bb=c[2]/255,mx=Math.max(r,gg,bb),mn=Math.min(r,gg,bb),l=(mx+mn)/2,hh,s,d=mx-mn;if(d===0){hh=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);hh=mx===r?((gg-bb)/d+(gg<bb?6:0)):mx===gg?((bb-r)/d+2):((r-gg)/d+4);hh/=6;}hh=(hh+deg/360)%1;if(hh<0)hh+=1;function h2(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}var q=l<0.5?l*(1+s):l+s-l*s,pp=2*l-q;return [Math.round(h2(pp,q,hh+1/3)*255),Math.round(h2(pp,q,hh)*255),Math.round(h2(pp,q,hh-1/3)*255)];}
function curPAL(){var base=PALS[palKey].cols;return hueShift?base.map(function(c){return rotc(c,hueShift);}):base;}
var PAL=SIGNAL;
/* ⚑ v116 (Tom) — LE MODE SOMBRE EST L'ENCRE DE SEICHE (OKLCH h 50°, −2 % de L, mesurée après conversion en hex : aucune valeur ne quitte 40–57°).
   Les cinq rampes des cellules vides sombres prennent ses tons (L 0,136–0,161, C ≈ 0,014)  ; l'ancienne ligne vit dans sauvegardes/promi-moteur-avant-v116.js. */
var GPIX=[[14,8,5],[16,9,6],[13,7,4],[18,12,8],[15,8,6]], GBRA=[[14,8,5],[16,9,6],[13,7,4],[18,12,8],[15,8,6]], GLI=[[14,8,5],[16,9,6],[13,7,4],[18,12,8],[15,8,6]];var GMOS=[[14,8,5],[16,9,6],[13,7,4],[18,12,8],[15,8,6]], GENC=[[14,8,5],[16,9,6],[13,7,4],[18,12,8],[15,8,6]];
var TON=[1.0,0.76,1.24,0.88,1.12];
/* LUMIERE sur les dalles colorees : lift de clarte en HSL -> teinte et saturation STRICTEMENT preservees.
   LITS[0]=0 -> le code couleur exact de la palette est toujours present. Aucun assombrissement. */
var LITS=[0,0.10,0.04,0.14,0.07];
function _r2h(c){var r=c[0]/255,g2=c[1]/255,b2=c[2]/255,mx=Math.max(r,g2,b2),mn=Math.min(r,g2,b2),h,s,l=(mx+mn)/2,d=mx-mn;if(d===0){h=s=0;}else{s=l>0.5?d/(2-mx-mn):d/(mx+mn);h=mx===r?((g2-b2)/d+(g2<b2?6:0)):mx===g2?((b2-r)/d+2):((r-g2)/d+4);h/=6;}return [h,s,l];}
function _h2r(h,s,l){function f(p,q,t){if(t<0)t+=1;if(t>1)t-=1;if(t<1/6)return p+(q-p)*6*t;if(t<1/2)return q;if(t<2/3)return p+(q-p)*(2/3-t)*6;return p;}if(s===0){var v=l*255;return [v,v,v];}var q=l<0.5?l*(1+s):l+s-l*s,p=2*l-q;return [f(p,q,h+1/3)*255,f(p,q,h)*255,f(p,q,h-1/3)*255];}
var _palLit=null;
function PALL(){if(_palLit)return _palLit;var base=curPAL(),out=[];for(var i=0;i<base.length;i++){var hs=_r2h(base[i]),row=[];for(var k=0;k<LITS.length;k++){row.push(LITS[k]===0?[base[i][0],base[i][1],base[i][2]]:_h2r(hs[0],hs[1],Math.min(0.965,hs[2]+LITS[k]*(1-hs[2]))));}out.push(row);}_palLit=out;return out;}
/* OMBRE sur les dalles grises : assombrit vers le noir, eclaire vers le blanc — jamais d'ecretage. */
function _shadeG(c,tone,shade){
  var t=(tone||1)-1, sh=shade||1, o=[0,0,0];
  var clair=isLightM();
  /* En clair, les dalles vides sont une crème CHAUDE : le ton ne les assombrit
     qu'à peine (sinon elles virent au gris terne), et ce qu'il enlève, il l'enlève
     surtout au bleu — l'ombre reste chaude au lieu de devenir cendreuse. */
  if(clair){
    /* le ton module doucement — assez pour qu'on voie la mosaïque, jamais assez
       pour la ternir. Et ce qu'il enlève, il l'enlève surtout au bleu : l'ombre
       reste chaude, elle ne vire pas à la cendre. */
    var d=(t<0)?(1+t*0.30):(1+t*0.12);
    var chaud=[1.0,0.985,0.958];
    for(var i=0;i<3;i++){
      var v=c[i]*d*(1+(sh-1)*0.5);
      if(t<0)v*=chaud[i];
      o[i]=v<0?0:(v>255?255:v);
    }
    return o;
  }
  for(var i=0;i<3;i++){var v=c[i];v=(t<0)?v*(1+t*0.9):(v+(255-v)*(t*0.35));v*=sh;o[i]=v<0?0:(v>255?255:v);}
  return o;
}
var TH={pixel:{g:GPIX},braille:{g:GBRA},sillons:{g:GLI},gravure:{g:GLI},mosaique:{g:GMOS},encre:{g:GENC},terrazzo:{g:GENC},touffe:{g:GENC}};
/* ⚑ v32 — les rampes de matière des quatre mondes neufs (CONTRAT-MONDE §4 bis) : Esquille prend celle d'Encre (demande de
   Tom), Madrure aussi (ses cellules vides ne se peignent jamais : l'onde a ses trois tons de palette) ; Bobinette, un fil,
   prend celle des lignes (Sillons, Gravure) ; Ritournelle, des coulées qui remplissent, celle de Mosaïque. Toutes brunes. */
TH.esquille={g:GENC};TH.bobinette={g:GLI};TH.ritournelle={g:GMOS};TH.madrure={g:GENC};TH.halin={g:GMOS};TH.brouillamini={g:GPIX};TH.chamade={g:GENC};TH.volubilis={g:GENC};TH.guingois={g:GENC};TH.chantourne={g:GPIX};TH.mascaret={g:GENC};TH.ramage={g:GPIX};   /* v68 : le plumage « dans le ton du papier » : la rampe de Brouillamini (Q330) */    /* v66 : les flammes de fond dans les tons de la rampe — celle de Brouillamini (Q330) */    /* v63 : Chamade ne peint aucune cellule vide (sa page est à l'encre) ; la rampe n'y sert qu'au moteur */    /* v62 : la rampe dont l'écart au fond (ΔE 11,2) est le plus proche de celui de la planche (8,4) */   /* v48 : Halin, des aplats qui remplissent, comme Ritournelle */
/* ⚑ v29 (Tom, 23 sept.) — L'UNITÉ D'UN MONDE. `UK` vaut 1 sur la Toile et `k` pendant `dalleTrame(…, k)` : tout pas de
   trame s'écrit « valeur de référence × UK ». À k = 1 rien ne bouge ; à k ≠ 1 la dalle est la MÊME image, plus grande. */
var UK=1;
var theme='encre', g,W,H,DPR, seeds=[], lastChange=0, running=false, lastNuee=null, view={s:1,ox:0,oy:0}, _qT0=0;
/* ⚑ ASSAINISSEMENT (Tom, 30 sept. 2026) — LES RÉGLAGES DÉCLARÉS PAR CHAQUE MONDE. Le moteur testait les mondes PAR LEUR NOM
   (36 tests `theme==='…'` et une table de pas de trame écrite dans le code) ; il lit désormais ce que chaque monde DÉCLARE.
   Valeurs et sens inchangés, au pixel (banc_rendu.py). Pour un monde neuf : on déclare ici, on ne teste jamais un nom.
     ressort        [kW, kX, redem]  les deux ressorts de la plantation (poids, position), à l'horloge (v61) ; redem = un
                                     redémarrage de la boucle compte pour UNE image
     elanPlante     1                la dalle plantée pousse d'un élan amorti (_tPlante, 360 ms) — Pochade, Touffe
     libre          1                la matière déborde la cellule (dalleTrame ne la recadre pas sur la grille)
     grille         1                monde à trame régulière : le frémissement dure 850 ms au lieu de 1 100
     pasTrame       px               le pas de la trame à k = 1 (dalleTrame le multiplie par k)
     finaleAuRepos  1                relit la finale à chaque image au repos (Esquille)
     relaxLocal     1                le relâchement est local autour de la plantation (Bobinette, Esquille)
     ondeNoeuds     1                seuls les nœuds font l'onde (Madrure)
     donneesPropres 1                le monde rend lui-même ses données de dalle, et déclare sa nature (Madrure)
     compagnons     1                deux cellules neutres accompagnent une Toile d'une parole (Halin, v97)
     apercuPause    [fanion, ms]     l'aperçu du Studio attend que ce fanion retombe avant l'événement suivant
     apercuFilm     1                l'aperçu attend le film de la pousse (Ramage, v90)
     apercuPetit    1                au Studio, les graines d'aperçu sont ramenées aux petites tailles (Volubilis, v94) */
var REGLAGES_MONDE={
  encre:    {ressort:[0.838,0.79,0], elanPlante:1, libre:1},
  touffe:   {ressort:[0.838,0.79,0], elanPlante:1, libre:1},
  terrazzo: {ressort:[0.83,0.78,1],  libre:1},
  mosaique: {ressort:[0.83,0.78,1],  grille:1, pasTrame:11},
  braille:  {ressort:[0.83,0.78,1],  grille:1, pasTrame:9},
  pixel:    {ressort:[0.83,0.78,1],  grille:1, pasTrame:5},
  gravure:  {ressort:[0.83,0.78,1],  grille:1},
  sillons:  {grille:1, pasTrame:6},
  esquille: {finaleAuRepos:1, relaxLocal:1},
  bobinette:{relaxLocal:1},
  madrure:  {ondeNoeuds:1, donneesPropres:1},
  halin:    {compagnons:1},
  ramage:   {apercuPause:['_apOccupe',120], apercuFilm:1},
  volubilis:{apercuPause:['_volBouge',60], apercuPetit:1}
};
function _rg(p,m){ var d=REGLAGES_MONDE[m||theme]; return d?d[p]:undefined; }
window.Toile_reglages=function(m){ return REGLAGES_MONDE[m]||{}; };   /* lecture seule — le portage lit la table */
/* ⚑ ASSAINISSEMENT (30 sept.) — LE CONTEXTE DE RENDU, EXPLICITE. Le moteur peint à travers des variables de module (le
   contexte `g`, la taille W×H, le semis, la vue, le monde, la palette, la teinte, le pas `UK`…). Une fonction qui les
   emprunte les PREND d'un geste et les REND d'un geste, dans un `finally` — jamais à la main, champ par champ.
   C'est ce que le portage traduit en un objet de contexte passé au rendu. */
/* ⚑ ASSAINISSEMENT (30 sept.) — LE SEMIS EST AMORCÉ PAR LA CLÉ DE LA TOILE. Le moteur tirait au hasard (Math.random, 66
   tirages) : la FORME d'une cellule changeait à chaque chargement (CONTRAT-MONDE §7.2). Tous les tirages passent désormais par
   `_alea()`, un générateur du moteur (mulberry32), RÉAMORCÉ à chaque construction du semis — semis de base, synchronisation,
   plantation — à partir de la clé de la Toile (`Toile.cle()` : la graine de la personne) et de ce qu'on construit. Même Toile,
   même semis, à chaque ouverture, sur tout appareil. Les rejeux d'une plantation simulée échangent CE générateur (`_aleaF`). */
var _aleaE=1;
function _aleaCle(){ try{ if(window.Toile&&window.Toile.cle) return window.Toile.cle()>>>0; }catch(_){ }
  try{ return ((window.USER&&USER.seed!=null)?USER.seed:(window._grainePropre?_grainePropre():0))>>>0; }catch(_){ return 0; } }
function _aleaRepart(sel){ var h=0x811c9dc5^_aleaCle(); sel=String(sel||''); for(var i=0;i<sel.length;i++){ h^=sel.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } _aleaE=h||1; }
function _aleaMb(){ _aleaE=(_aleaE+0x6D2B79F5)>>>0; var t=_aleaE; t=Math.imul(t^(t>>>15),t|1); t^=t+Math.imul(t^(t>>>7),t|61); return ((t^(t>>>14))>>>0)/4294967296; }
var _aleaF=_aleaMb;
function _alea(){ return _aleaF(); }
function _ctxPrend(){ return {g:g, W:W, H:H, seeds:seeds, view:{s:view.s,ox:view.ox,oy:view.oy}, theme:theme, palKey:palKey,
  hueShift:hueShift, palLit:_palLit, UK:UK, nAvg:_nAvg, WT:_WT}; }
function _ctxRend(C){ g=C.g; W=C.W; H=C.H; seeds=C.seeds; view=C.view; theme=C.theme; palKey=C.palKey; hueShift=C.hueShift;
  _palLit=C.palLit; UK=C.UK; _nAvg=C.nAvg; _WT=C.WT; }
/* ⚑ v43 (Tom, 24 sept. 2026) — LA TRANSITION D'UN MONDE. Le moteur garde LE MOMENT où une dalle arrive (ou part) et
   son lieu ; un monde le lit par `env.trans` — seulement sur la Toile vivante (`frame`), jamais dans une dalle, un export ou
   un aperçu (§1 amendé du CONTRAT-MONDE). Un monde qui anime son arrivée déclare sa durée : `RD[monde].transDur` (ms) ;
   le moteur tourne tant qu'elle court. Le numéro `n` rend la transition déterministe (tiré avec la clé de la Toile). */
var _trans=null, _transN=0, _transVive=false, PART_DUR=620;
var _REPLI={encre:1,touffe:1,mosaique:1,braille:1,pixel:1,terrazzo:1,sillons:1,gravure:1}, REPLI_DUR=700;   /* Houle et Taille-douce suivent (Tom, 27 sept. : « tous les mondes pareil ») */   /* la durée d'un repli, sur le temps (le poids avançait de 25 % par image : 0,15 s, invisible) */   /* v76 : les six mondes où une dalle qui part se replie (Tom) */
/* le poids d'une cellule repliée : 1,8 écart entre graines — sous ~1 écart, la cellule garde un îlot autour de son centre (mesuré à −45 : il en restait un) */
function _repliW(){ return -avg()*1.8; }
/* ⚑ v83 (Tom : « dans l'onboarding, c'est illisible quand il y a des dalles sous les éléments — on ne sait ni quoi lire ni où tracer ;
   écarte les dalles des éléments, en clair comme en sombre ; la Toile reste fournie sauf sous les éléments ») — `Toile.ecarte(rects)` :
   une graine VIDE (jamais une parole) dont la tache toucherait un rectangle (marge : 0,7 écart entre graines) se replie comme une
   dalle qui part (REPLI_DUR) ; le rectangle parti, elle regrandit. */
var _ecZ=null, _ecActif=false;
function _ecDans(s){ var m=avg()*0.7; for(var i=0;i<_ecZ.length;i++){ var r=_ecZ[i]; if(s.x>r.x-m&&s.x<r.x+r.w+m&&s.y>r.y-m&&s.y<r.y+r.h+m) return true; } return false; }
function _replie(s,now){ s.part=now; s.rT0=now; s.rW0=s.w; s.wt=s.wFin=_repliW(); s.wAt=0; }
/* v76 — Éclisse et Touffe ne pavent pas : ils posent des éclats, des fleurs, AUTOUR de la graine, sans lire le poids. Leur repli est
   une échelle tirée du poids : 1 dès qu'il est positif, 0 quand la cellule est repliée — elle rétrécit au départ, regrandit à l'arrivée. */
function _repliF(s){ var w=(s.w!=null?s.w:0); if(w>=0) return 1; return Math.max(0,Math.min(1,1-w/_repliW())); }
/* ⚑ v66 — LE FOND DE LA TOILE VIVANTE, un seul propriétaire : `frame()` le peint, et un monde qui « découpe » en papier (Ramage,
   Mascaret) le REPREND par `env.papier`, recalé dans son repère (la vue) — un aplat ferait des traits d'une autre teinte sur le dégradé. */
/* v92 : les deux tons du fond vif, lus aussi par le Worker de Ramage (un dégradé ne passe pas un postMessage : on lui en envoie la description) */
/* ⚑ v118 (Tom) — LE FOND DE LA TOILE EST À PLAT, EN CLAIR COMME EN SOMBRE : la Pelote est le seul volume de l'app (redteam_volume).
   Le clair portait encore un dégradé #E6D1AE → #D8C29A (ΔE00 3,8 d'un coin à l'autre) : il prend leur ton médian, #DFCAA4
   (OKLCH L 0,847 — hors de la plage du kaki). `_fondVif` rend désormais une COULEUR, plus un dégradé. */
function _fondVifDesc(xa,ya,xb,yb){ var l=isLightM(); return {l:[xa,ya,xb,yb],a:l?'#DFCAA4':'#050302',b:l?'#DFCAA4':'#050302'}; }
function _fondVif(gg,xa,ya,xb,yb){ return _fondVifDesc(xa,ya,xb,yb).a; }

/* ⚑ v47 — OÙ LES GRAINES VONT SE POSER. Au début d'une transition, le moteur rejoue son propre écartement (`relax`, même
   formule) avec les poids FINAUX jusqu'à l'équilibre : un monde qui préfère se recomposer une fois plutôt que suivre le glissé
   (Esquille) lit ces places par `env.finale`. Calculé une fois par transition. */
var _finC=null;
function _semisFinal(){ var h=2166136261, _lc=_relaxLocal();
  /* ⚑ v54 (Bobinette) — pendant une transition locale, l'état final se calcule UNE FOIS (par transition, sur le poids d'arrivée) :
     les graines y vont (relax pose leurs cibles dessus) et la trame s'y lit — la Toile s'arrête exactement là où la trame
     l'annonçait, rien ne se rattrape après coup. */
  if(_lc){ var hl=(_trans.n*2654435761)>>>0, nz=0; for(var zl=0;zl<seeds.length;zl++){ var sl=seeds[zl]; if(sl.part!=null) continue; hl^=Math.round(((sl.wAt&&sl.wFin!=null)?sl.wFin:(sl.wt!=null?sl.wt:sl.w))*2)+(nz++)*31; hl=Math.imul(hl,16777619)>>>0; }
    if(_finC&&_finC.hl===hl) return _finC.m; }   /* la clé ignore la dalle qui part (le moteur la retire en cours de route : rien ne doit se recalculer) */
  else if(_lc){ h^=Math.round(_lc.x)*7+Math.round(_lc.y)*13; h=Math.imul(h,16777619)>>>0; } for(var z=0;z<seeds.length;z++){ var sz=seeds[z]; var tz=[Math.round(sz.x),Math.round(sz.y),Math.round(((sz.wAt&&sz.wFin!=null)?sz.wFin:(sz.wt!=null?sz.wt:sz.w))*2)]; for(var q=0;q<3;q++){ h^=(tz[q]|0); h=Math.imul(h,16777619)>>>0; } }
  if(_finC&&_finC.h===h&&_finC.len===seeds.length) return _finC.m;   /* v47 : un point fixe par semis (au pixel près), pas par transition */
  /* ⚑ v57 — en mode local, les graines éloignées partent de leur place FINALE d'avant (pas de leur place courante, qui n'est qu'à peu
     près au point fixe) : sinon toutes bougeaient d'un rien, et dans Esquille chaque promesse qui franchissait une cassure
     changeait d'éclat — la plaque se recomposait d'un coup sur tout l'écran. */
  var _fp=(_lc&&_finPrev&&_rg('finaleAuRepos'))?_finPrev:null;   /* Esquille seul lit la finale à chaque image au repos : ailleurs elle serait périmée */
  var S2=seeds.filter(function(s){ return s.part==null; }).map(function(s){ var w=(s.wAt&&s.wFin!=null)?s.wFin:(s.wt!=null?s.wt:s.w); var q=_fp&&_fp.get(s); return {s:s,x:q?q[0]:s.x,y:q?q[1]:s.y,w:w}; });   /* une dalle qui part ne compte plus */
  var ac=avg();
  for(var it=0;it<50;it++){ var mx=0, T=[];
    for(var i=0;i<S2.length;i++){ var a=S2[i],fx=0,fy=0; for(var j=0;j<S2.length;j++){ if(j===i)continue; var o=S2[j],dx=a.x-o.x,dy=a.y-o.y,d=Math.sqrt(dx*dx+dy*dy),wr=ac*(0.92+a.w*0.026+o.w*0.026); if(d<wr&&d>0.01){ var f=(wr-d)/d*0.16; fx+=dx*f; fy+=dy*f; } }
      var _B=_bornes(); T.push([Math.max(_B[0],Math.min(_B[1],a.x+fx)),Math.max(_B[2],Math.min(_B[3],a.y+fy))]); }
    for(i=0;i<S2.length;i++){ if(_lc&&Math.hypot(S2[i].s.x-_lc.x,S2[i].s.y-_lc.y)>_lc.r) continue; mx=Math.max(mx,Math.abs(T[i][0]-S2[i].x)+Math.abs(T[i][1]-S2[i].y)); S2[i].x=T[i][0]; S2[i].y=T[i][1]; }
    if(mx<0.05) break; }
  var m=new Map(); S2.forEach(function(q){ m.set(q.s,[q.x,q.y]); }); _finC={h:h,hl:(_lc?hl:null),len:seeds.length,m:m}; if(!_lc) _finPrev=m; return m; }
function _transPose(kind,x,y){ _trans={t0:performance.now(), kind:kind, x:x, y:y, n:++_transN}; if(_qT0 && performance.now()-_qT0<150) _qT0=0; }
/* ⚑ v60 (rythme) — LE MOMENT DE L'ARRIVÉE EST PROTÉGÉ. Les passes qui corrigent l'interface après un clic (polices, plateau,
   titres, couleurs sur fond sombre) tombaient pile pendant l'impression et l'arrivée de la dalle : par le vrai chemin, l'arrivée
   dans Pochade comptait 31 images au lieu de 42–48 (celle que Tom a validée). Pendant ce moment, elles sont reportées — de
   2 s au plus, comptées depuis la demande : un écran ouvert juste après ne reste jamais longtemps sans elles. */
window._apresMouvement=function(fn){ var t0=performance.now(); (function essaie(){ var occupe=!!window._tirageActive || (window._arriveeEnCours&&window._arriveeEnCours());
  if(occupe && performance.now()-t0<((_apVu&&_apVu.vif)?5000:2000)) setTimeout(essaie, 120); else fn(); })(); };   /* v75 : au Studio, on attend le REPOS de l'aperçu (il vient à chaque tour, entre l'arrivée et le départ) */
window._arriveeEnCours=function(){ var t=performance.now(); return !!((_trans&&t-_trans.t0<900) || (window._tPlante&&t-window._tPlante<900) || (window._tMouv&&t-window._tMouv<900) || (_apVu&&_apVu.vif&&_apVu.encore&&t-_apVu.tImg<200)); };   /* v75 : l'aperçu vivant du Studio, tant qu'il bouge */
window._trans_en_cours=function(){ var t=performance.now(); return !!(_trans&&RD[theme]&&RD[theme].transDur&&t-_trans.t0<RD[theme].transDur+300) || (t-lastChange<1200); };   /* v59 : le réchauffage des dalles attend que la Toile soit posée */
function isLightM(){if(typeof window!=='undefined'&&window._shThemeOverride!=null)return window._shThemeOverride;var d=document.getElementById('device');return d&&d.classList.contains('light');}
/* mode clair : du CRÈME, pas du gris. La Toile doit respirer, pas ternir. */
var GLIGHT=[[253,235,205],[250,243,229],[248,226,194],[254,238,212],[250,230,199]];
function grays(){return isLightM()?GLIGHT:TH[theme].g;}
function size(){
  var st=host.parentNode;
  var w=st.clientWidth, h=st.clientHeight;
  /* la Toile est cachée (on est dans le Fil) : on ne touche à RIEN.
     Sans ce garde-fou, un redimensionnement pendant le Fil — la barre d'URL du
     téléphone qui bouge au scroll, par exemple — mettait le canvas à 0x0
     et la Toile ne revenait jamais. */
  if(!w||!h)return;
  DPR=Math.min(2,window.devicePixelRatio||1);
  W=w; H=h; host.width=W*DPR; host.height=H*DPR;
  g=host.getContext('2d'); if(!seeds.length)seedGray(); kick();
}
window.Toile_resize=size;
function mk(x,y,k){return {x:x,y:y,tx:x,ty:y,gray:grays()[(_alea()*5)|0],gc:null,ci:null,c:null,t0:0,kind:k||'gray',w:0,wt:0,tone:TON[(_alea()*TON.length)|0],lit:0,shade:0.96+_alea()*0.08,ang:_alea()*Math.PI,ph:_alea()*6.28,am:0.6+_alea()*0.7};}
var _nAvg=null, _WT=null;   /* ⚑ v29 — pendant dalleTrame, le NOMBRE de graines de la Toile (les voisines seules sont passées au monde) */
function avg(){return Math.sqrt(W*H/Math.max(1,_nAvg||seeds.length));}
function seedGray(){_aleaRepart('semis');seeds=[];var base=72,gc=Math.max(2,Math.round(W/base)),gr=Math.max(3,Math.round(H/base)),cw=W/gc,ch=H/gr;for(var r=0;r<gr;r++)for(var c=0;c<gc;c++){if(_alea()<0.14)continue;seeds.push(mk(cw*(c+.5)+(_alea()-.5)*cw*.55,ch*(r+.5)+(_alea()-.5)*ch*.55));}var ex=Math.round(gc*gr*0.28);for(var e=0;e<ex;e++)seeds.push(mk(_alea()*W,_alea()*H));}
function nbU(s){var u={},l=avg()*1.6;l*=l;for(var j=0;j<seeds.length;j++){var o=seeds[j];if(o===s||o.ci==null)continue;var dx=s.x-o.x,dy=s.y-o.y;if(dx*dx+dy*dy<l)u[o.ci]=true;}return u;}
function iposNuee(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();if(!col.length)return ipos();var cx=0,cy=0;col.forEach(function(s){cx+=s.x;cy+=s.y;});cx/=col.length;cy/=col.length;var topB=H*0.17,botB=H*0.84;for(var t=0;t<40;t++){var a=_alea()*6.28,r=(1.7+_alea()*0.7)*ac;var x=Math.max(8,Math.min(W-8,cx+Math.cos(a)*r)),y=Math.max(8,Math.min(H-8,cy+Math.sin(a)*r));if(col.length<15&&(y<topB||y>botB))continue;var ok=true;for(var j=0;j<col.length;j++){var dx=x-col[j].x,dy=y-col[j].y;if(dx*dx+dy*dy<(ac*1.45)*(ac*1.45)){ok=false;break;}}if(ok)return {x:x,y:y};}return {x:Math.max(8,Math.min(W-8,cx+(_alea()-.5)*ac*2)),y:Math.max(topB,Math.min(botB,cy+(_alea()-.5)*ac*2))};}
function ipos(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();var few=col.length<15,topB=H*0.17,botB=H*0.84;function danger(x,y){if(!few)return false;if(y<topB||y>botB)return true;if(x>W*0.6&&y<H*0.2)return true;return false;}if(!col.length)return {x:W/2+(_alea()-.5)*ac,y:H*0.5+(_alea()-.5)*ac};var an=col[(_alea()*col.length)|0];for(var t=0;t<12;t++){var sp=(_alea()<0.72)?(0.95+_alea()*0.22):(1.45+_alea()*0.7);var a=_alea()*6.28,r=ac*sp;var x=Math.max(8,Math.min(W-8,an.x+Math.cos(a)*r)),y=Math.max(8,Math.min(H-8,an.y+Math.sin(a)*r));if(!danger(x,y))return {x:x,y:y};}return {x:Math.max(8,Math.min(W-8,an.x+(_alea()-.5)*ac)),y:Math.max(topB,Math.min(botB,an.y+(_alea()-.5)*ac))};}
function cc(s){var u=nbU(s),av=[];for(var p=0;p<PAL.length;p++)if(!u[p])av.push(p);return av.length?av[(_alea()*av.length)|0]:((_alea()*PAL.length)|0);}
function tones(){var col=seeds.filter(function(s){return s.kind!=='gray';});var ac=avg();for(var i=0;i<col.length;i++)col[i].lit=null;for(var i=0;i<col.length;i++){var s=col[i],u={};for(var j=0;j<col.length;j++){if(j===i)continue;var o=col[j];if(o.lit==null)continue;var dx=s.x-o.x,dy=s.y-o.y;if(dx*dx+dy*dy<(ac*1.5)*(ac*1.5))u[o.lit]=true;}var pk=0;for(var t=0;t<LITS.length;t++){if(!u[t]){pk=t;break;}}s.lit=pk;}_dalleFigee();}
/* ⚑ LA COULEUR FIGÉE (Q213) — une dalle reliée à un Promi reprend SA couleur, `p.dalle`. Un Promi sans couleur
   figée la reçoit ici : PLANTÉ À L'INSTANT (`vivant`, depuis `addPromi`), il garde celle que la Toile vient de
   tirer pour lui, loin de ses voisines ; sinon (jeu de démonstration reconstruit après le démarrage, sauvegarde
   ancienne), celle de sa clé — jamais un nouveau tirage. */
function _dalleFigee(vivant){try{if(typeof promises==='undefined')return;var m={};for(var i=0;i<promises.length;i++)m[promises[i].id]=promises[i];
  for(var k=0;k<seeds.length;k++){var s=seeds[k];if(s.kind==='gray'||s.pid==null)continue;var p=m[s.pid];if(!p)continue;
    s.nat=p.chiche?1:0;   /* ⚑ v17 INGÉNU — lue par cOf seulement sous la palette par défaut */
    if(p.dalle&&p.dalle.ci!=null&&p.dalle.ci<PAL.length){if(s.ci!==p.dalle.ci){s.ci=p.dalle.ci;s.c=PAL[s.ci];s.gc=null;}s.lit=(p.dalle.lit|0)%LITS.length;s.rgb=(p.dalle.rgb&&p.dalle.rgb.length===3)?[+p.dalle.rgb[0],+p.dalle.rgb[1],+p.dalle.rgb[2]]:null;s.choisi=p.dalle.choisi?1:0;}
    else if(s.ci!=null){if(vivant){p.dalle={ci:s.ci,lit:(s.lit|0)};}else if(window._dalleDeCle){p.dalle=window._dalleDeCle(p);s.ci=p.dalle.ci;s.c=PAL[s.ci];s.gc=null;s.lit=p.dalle.lit;}}}
  /* ⚑ LA DALLE D'UNE NUÉE (Tom, 13 sept.) : sa couleur est à ELLE (`NUEDALLE[clé]`), tirée de son nom comme un Promi l'est de son titre ; le code du Cercle y passe. */
  var ND=window.NUEDALLE||(window.NUEDALLE={});
  for(var n=0;n<seeds.length;n++){var t=seeds[n];if(t.kind!=='nuee'||!t.nuee||t.ci==null)continue;t.nat=2;var d=ND[t.nuee];
    if(!(d&&d.ci!=null&&d.ci<PAL.length)){d=ND[t.nuee]=window._dalleDeCle?window._dalleDeCle({title:(typeof NUE!=='undefined'&&NUE[t.nuee])||t.nuee,who:'nuee'}):{ci:t.ci,lit:0};}
    if(t.ci!==d.ci){t.ci=d.ci;t.c=PAL[t.ci];t.gc=null;}t.lit=(d.lit|0)%LITS.length;t.rgb=(d.rgb&&d.rgb.length===3)?[+d.rgb[0],+d.rgb[1],+d.rgb[2]]:null;t.choisi=d.choisi?1:0;}
  }catch(e){}}
/* ---------- LE RECUL ----------
   Une Toile de 70 cellules avec un seul Promi, vue en entier, c'est un écran vide
   et triste. On se rapproche donc des premières dalles — puis, à CHAQUE dalle
   plantée, la vue RECULE d'un cran. Les proportions ne changent jamais : c'est le
   cadrage qui s'ouvre, à mesure que la Toile se remplit de couleur.
   Au-delà d'une dizaine de Promi, on voit la Toile entière : elle se suffit. */
var vTarget=null;
/* ⚑ v46 (Tom, 24 sept. 2026) — LE ZOOM « COMME UNE PHOTO SUR L'IPHONE ». Fluide, sans à-coup, vectoriel (la Toile se
   repeint à chaque image dans sa transformation : les contours restent nets même très zoomés). On dézoome jusqu'à voir la
   Toile ENTIÈRE (ZMIN), et à ce niveau les encarts du haut et du bas s'effacent. Le zoom PERSISTE d'une page à l'autre ; il
   ne revient au défaut qu'à la fermeture de l'app, à la création ou à la suppression d'une dalle — en douceur. Le défaut
   dépend du nombre de dalles : plus il y en a, plus la vue recule. Un double toucher y ramène.
   Au-delà des bornes la Toile résiste (élastique), au lâcher le glissé garde son élan, puis tout revient dans les bornes par
   un ressort calé sur le TEMPS (§8), jamais par image. */
var ZMIN=0.72, ZMAX=5, _inert=null, _pan=null;
function _zDef(n){ return n<20 ? Math.min(1.1, 1+(20-n)*0.005) : 1; }   /* ⚑ v47 (Tom) : « par défaut la Toile prend tout l'écran, angles compris, aucun fond autour — c'est ENSUITE qu'on zoome ou dézoome ». Jamais sous 1 ; plus zoomée quand il y a peu de dalles */
function _vueDefaut(){ window._vueMain=false; window._recadreDemande=true; _inert=null; autoView(); kick(); try{ if(window._majRecadre) window._majRecadre(); }catch(_){} }
function _borne(){ var s=Math.max(ZMIN,Math.min(ZMAX,view.s)), cx=W/2, cy=H/2, ox=view.ox, oy=view.oy;
  if(s!==view.s){ ox=cx-(cx-view.ox)*(s/view.s); oy=cy-(cy-view.oy)*(s/view.s); }
  if(s<1){ ox=(W-W*s)/2; oy=(H-H*s)/2; } else { ox=Math.max(W-W*s,Math.min(0,ox)); oy=Math.max(H-H*s,Math.min(0,oy)); }
  if(Math.abs(s-view.s)<1e-4&&Math.abs(ox-view.ox)<0.05&&Math.abs(oy-view.oy)<0.05) return null; return {s:s,ox:ox,oy:oy}; }
var _voileAv=-1;
function _voile(){ var a=Math.max(0,Math.min(1,(view.s-0.74)/(0.88-0.74))); a=Math.round(a*50)/50; if(a===_voileAv) return; _voileAv=a;
  try{ var dv=document.getElementById('device'); if(!dv) return; dv.style.setProperty('--toile-voile', String(a)); dv.classList.toggle('toile-recul', a<1); dv.classList.toggle('toile-entiere', a<0.05); }catch(_){} }
function _rub(v,lo,hi){ return v<lo ? lo-(lo-v)*0.35 : v>hi ? hi+(v-hi)*0.35 : v; }
/* le champ clair : la barre du haut (titre + bascule Toile/Fil) et le dock */
var HAUT_LIBRE=176, BAS_LIBRE=138;
function autoView(){
  /* ⚑ Q212 (Tom) : « la vue qui revient à 1 à chaque plantation » est un défaut. Une vue posée par la main n'est reprise
     que par le recadrage (le rond, ou le double toucher sur une case vide). */
  if(window._vueMain && !window._recadreDemande) return;
  window._recadreDemande=false;
  /* Zoom intelligent : on cadre les dalles COLOREES (pas toute la Toile),
     en gardant une marge et en plafonnant le zoom pour ne jamais tomber
     dans le vide ni grossir betement une seule dalle. Beaucoup de dalles
     => Toile entiere (elle se suffit). Barre du haut et dock evites. */
  var col=seeds.filter(function(s){return s.kind!=='gray'||s.compagnon;});   /* v97 : les deux cellules compagnes de Halin se cadrent avec la parole */
  if(!col.length){ vTarget={s:1,ox:0,oy:0}; return; }
  /* ⚑ v34 — sans cellule vide, la Toile EST ses promesses : on la montre entière, il n'y a rien à cadrer */
  if(col.length===seeds.length){ var s0=_zDef(col.length); vTarget={s:s0,ox:(W-W*s0)/2,oy:(H-H*s0)/2}; return; }   /* v46 : plus il y a de dalles, plus la vue recule */
  var n=col.length;
  if(n>=20){ var s1=_zDef(n); vTarget={s:s1,ox:(W-W*s1)/2,oy:(H-H*s1)/2}; return; }   /* Toile bien remplie : Toile entière, et elle recule à mesure qu'elle se remplit (v46) */
  /* bounding-box de TOUTES les dalles colorees -> on les cadre toutes a l'ecran */
  var minX=1e9,maxX=-1e9,minY=1e9,maxY=-1e9;
  col.forEach(function(s){if(s.x<minX)minX=s.x;if(s.x>maxX)maxX=s.x;if(s.y<minY)minY=s.y;if(s.y>maxY)maxY=s.y;});
  var pad=avg()*1.3;                        /* marge d'une dalle autour */
  minX-=pad;maxX+=pad;minY-=pad;maxY+=pad;
  var bw=Math.max(1,maxX-minX), bh=Math.max(1,maxY-minY);
  var topB=HAUT_LIBRE, botB=H-BAS_LIBRE;    /* zone utile (barre haut + dock evites) */
  var availW=W*0.92, availH=Math.max(1,botB-topB);
  var s=Math.min(availW/bw, availH/bh);
  s=Math.max(1.0, Math.min(s, 2.0));        /* jamais plus loin que la Toile entiere, plafond 2.0 */
  var cx=(minX+maxX)/2, cy=(minY+maxY)/2, scx=W/2, scy=(topB+botB)/2;
  var _ox=scx-cx*s, _oy=scy-cy*s;
  /* clamp : les bords de la Toile restent colles aux bords de l ecran (jamais de vide) */
  _ox=Math.max(W-W*s, Math.min(0, _ox));
  _oy=Math.max(H-H*s, Math.min(0, _oy));
  vTarget={ s:s, ox:_ox, oy:_oy };
}
window.Toile_autoView=function(){autoView();kick();};
/* ⚑ Q212 · REVENIR AU CADRAGE DE DÉPART — le rond « recadrer » et le double toucher y mènent tous deux. */
window.Toile_recadre=function(){ window._recadreDemande=true; window._vueMain=false; autoView(); kick(); try{ if(window._majRecadre) window._majRecadre(); }catch(_){} };
/* ⚑ v54 (Bobinette, Tom : « les fils se tirent pour redéfinir la Toile LÀ OÙ C'EST NÉCESSAIRE. Localement, pas partout ») —
   mesuré au repos, avant et après une plantation : 556 arcs sur 1 156 changeaient, 358 à plus de 3 pas de la dalle — parce que
   CHAQUE graine de la Toile se redistribuait. Pendant une transition de Bobinette, seules les graines proches de la dalle qui
   arrive ou qui part bougent (1,25 pas moyen : ses voisines directes) ; les autres restent en place, et poussent toujours leurs voisines. */
var _finPrev=null;
function _relaxLocal(){ if(!_rg('relaxLocal')||!_trans||_trans.x==null) return null;   /* v57 : Esquille aussi — chaque plantation redistribuait toute la Toile, des éclats changeaient de couleur loin de la dalle */ var d=(RD[theme]&&RD[theme].transDur||0)+4000; if(performance.now()-_trans.t0>d) return null;   /* la fenêtre dure au-delà de la transition : un relâchement tardif (les poids qui finissent de se poser) redevenait global — 58 arcs sautaient après coup */ return {x:_trans.x,y:_trans.y,r:avg()*1.5}; }   /* v56 : 2 → 1,5 pas, les fils bougent maintenant vraiment · v55 (Tom : « trop loin dans le local, c'est devenu ennuyeux ») : 1,25 → 2 pas moyens */
/* ⚑ v89 (Tom : « la parole neuve posée dans un coin, à moitié hors de l'écran ») — sur une Toile faite de ses paroles, la relaxation
   chassait une graine jusqu'au cran de 6 px du bord : mesuré (384, 6), sous le plateau du titre. Le CENTRE d'une dalle (son œil, son
   titre) reste désormais dans la zone utile : 13 % de la largeur sur les côtés (la demi-largeur d'un titre), 17 % de la hauteur en haut
   (sous le plateau), 15 % en bas (la barre). Les cellules vont toujours jusqu'au bord. Les huit anciens (semis constant) gardent le cran d'origine. */
function _bornes(){ if(!_semisNeuf()||(window._apImage&&!(window._apercuClair||{})[theme])) return [6,W-6,6,H-6];   /* v92 : un aperçu en grille (Madrure) couvre tout le canevas, comme les anciens mondes — pas de marges */ var mx=W*0.13, mt=H*0.17, mb=H*0.15; return [mx,W-mx,mt,H-mb]; }
function relax(){var ac=avg(),_dx=!!(RD[theme]&&RD[theme].douce),_lc=_relaxLocal();if(_lc){var _fm=_semisFinal();for(var _fi=0;_fi<seeds.length;_fi++){var _fs=seeds[_fi],_fp=_fm.get(_fs);if(_fp){_fs.tx=_fp[0];_fs.ty=_fp[1];}else{_fs.tx=_fs.x;_fs.ty=_fs.y;}}return;}/* ⚑ v54 (Halin) : une dalle qui part ne pousse plus personne — ses voisines visent tout de suite leur place finale, en même temps qu'elle se retire */for(var i=0;i<seeds.length;i++){var s=seeds[i],fx=0,fy=0;if(_dx&&s.part!=null){s.tx=s.x;s.ty=s.y;continue;}if(_lc&&Math.hypot(s.x-_lc.x,s.y-_lc.y)>_lc.r){s.tx=s.x;s.ty=s.y;continue;}for(var j=0;j<seeds.length;j++){if(j===i)continue;var o=seeds[j];if(_dx&&o.part!=null)continue;var dx=s.x-o.x,dy=s.y-o.y,d=Math.sqrt(dx*dx+dy*dy);var w=ac*(0.92+s.w*0.026+o.w*0.026);if(d<w&&d>0.01){var f=(w-d)/d*0.16;fx+=dx*f;fy+=dy*f;}}var _B=_bornes();s.tx=Math.max(_B[0],Math.min(_B[1],s.x+fx));s.ty=Math.max(_B[2],Math.min(_B[3],s.y+fy));}
}
/* ⚑ v53 (Tom, 25 sept. 2026) — LE VERT DE CÉLÉBRATION EST ABANDONNÉ, PARTOUT. « Une dalle qui naît est déjà un événement : la
   Toile bouge, une forme apparaît. Une couleur par-dessus souligne ce qui se voit déjà. La célébration, c'est le mouvement
   lui-même. » (Six passes, v47 → v52 ; code d'avant : sauvegardes/app-avant-v53.html.) */
function ease(p){return p<0?0:p>1?1:p*p*(3-2*p);}
function kick(){if(!running){running=true;frame._redem=1;requestAnimationFrame(frame);}}   /* v61 : la boucle repart — la première image fait UN pas, comme avant l'horloge */
/* ⚑ v60 (Tom : « les mouvements dans l'app sont-ils identiques à ceux de celebration-mondes.html ? ») — NON, mesuré : fermer
   un écran (`closeAll`) fait frémir toute la Toile (7 à 11 px, ~1 s) — et une plantation ou une suppression ferment un écran.
   Le frémissement se superposait donc au mouvement du monde, que Tom a validé SANS lui. Une arrivée ou un départ prend la
   main : pendant l'impression d'une plantation (`_tirageActive`) la Toile ne frémit pas, et un départ ou une arrivée posé
   dans les 150 ms d'un frémissement l'annule (même geste : aucune image ne l'a encore dessiné). */
function liven(){ if(window._tirageActive || (window._tMouv && performance.now()-window._tMouv<900)) { kick(); return; } _qT0=performance.now();kick();}   /* v60 : pendant qu'une parole arrive ou part, le frémissement ne se superpose pas à son mouvement */window.Toile_liven=liven;window.Toile_probe=function(){var o=[];for(var i=0;i<seeds.length;i++){if(seeds[i].kind!=='gray'){var s=seeds[i];o.push([Math.round(((s.px==null?s.x:s.px)-s.x)*10)/10,Math.round(((s.py==null?s.y:s.py)-s.y)*10)/10]);}}return o;};window.Toile_state=function(){return {running:running,qt:_qT0,theme:theme};};window.Toile_graines=function(){return seeds.map(function(s){return [s.pid==null?null:s.pid,Math.round(s.x),Math.round(s.y),s.kind];});};   /* v89 : lecture (bancs) */window.Toile_previewLive=function(pcv,th,pw,ph){
  if(!pcv||!pcv.getContext)return;
  th=(th&&TH[th])?th:'encre';
  var dpr=Math.min(2,window.devicePixelRatio||1);
  pcv.width=Math.round(pw*dpr);pcv.height=Math.round(ph*dpr);pcv.style.width=pw+'px';pcv.style.height=ph+'px';
  if(!pcv.__pls||pcv.__plth!==th||Math.abs((pcv.__plpw||0)-pw)>2){
    try{window.Toile.preview(pcv,th,pw,ph);}catch(e){}
    var src=(pcv.__c&&pcv.__c.seeds)?pcv.__c.seeds:[];
    var tpl=null;for(var _i=0;_i<src.length;_i++){if(src[_i].kind!=='gray'){tpl=src[_i];break;}}
    tpl=tpl||src[0]||{ci:0,c:null,tone:1,lit:0,shade:1,ang:0,w:0};
    pcv.__pls=src.map(function(o){return {x:o.x,y:o.y,gray:false,gc:null,ci:tpl.ci,c:tpl.c,kind:'promi',tone:tpl.tone,lit:tpl.lit,shade:tpl.shade,ang:o.ang,w:o.w,t0:-99999};});
    var im=(typeof _pdImgs!=='undefined'&&_pdImgs[th])?_pdImgs[th]:null;
    var iw=(im&&im.naturalWidth)||420, ih=(im&&im.naturalHeight)||420;
    var TAR=pw*0.52, kk=TAR/Math.max(iw,ih), bw=iw*kk, bh=ih*kk;
    var bL=pw-Math.round(pw*0.03)-bw, bT=Math.round(ph*0.40)-bh/2;
    pcv.__box={cx:bL+bw/2, cy:bT+bh/2, rx:bw/2, ry:bh/2};
    var N=48, pts=[];for(var _a=0;_a<N;_a++){pts.push({ang:_a/N*6.2832, ph:_alea()*6.28, fr:1.4+_alea()*1.9});}
    pcv.__cpts=pts;
    pcv.__plth=th;pcv.__plpw=pw;pcv.__plph=ph;
  }
  pcv.__plqt=performance.now();
  if(pcv.__plraf)cancelAnimationFrame(pcv.__plraf);
  var _d=pcv.width/pw;
  function step(){
    var age=performance.now()-pcv.__plqt, DUR=1300, quiv=age<DUR, env=Math.exp(-age/430);
    var box=pcv.__box, pts=pcv.__cpts;
    var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};
    try{
      g=pcv.getContext('2d');W=pw;H=ph;theme=th;view={s:1,ox:0,oy:0};seeds=pcv.__pls;
      g.setTransform(_d,0,0,_d,0,0);g.clearRect(0,0,pw,ph);
      var AMP=quiv?(box.rx*0.05)*env+2.5*env:0;
      var P=[];
      for(var i=0;i<pts.length;i++){
        var pt=pts[i];
        var wob=Math.sin(age*0.004*pt.fr+pt.ph)*AMP + Math.sin(age*0.0026+pt.ang*3+pt.ph)*AMP*0.55;
        P.push([box.cx+Math.cos(pt.ang)*(box.rx+wob), box.cy+Math.sin(pt.ang)*(box.ry+wob)]);
      }
      g.save();g.beginPath();
      var n=P.length, mx=(P[n-1][0]+P[0][0])/2, my=(P[n-1][1]+P[0][1])/2;
      g.moveTo(mx,my);
      for(var j=0;j<n;j++){var c=P[j], nnx=(P[j][0]+P[(j+1)%n][0])/2, nny=(P[j][1]+P[(j+1)%n][1])/2;g.quadraticCurveTo(c[0],c[1],nnx,nny);}
      g.closePath();g.clip();
      RD[theme](performance.now(),0,0,pw,ph);
      g.restore();
    }catch(e){}
    g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;
    if(quiv)pcv.__plraf=requestAnimationFrame(step);else pcv.__plraf=0;
  }
  step();
};
/* ⚑ v30 (Tom, 23 sept. 2026) — LA GRAINE PROPRIÉTAIRE SE CHERCHE PARMI LES VOISINES, PAS PARMI TOUTES.
   Cinq mondes (Pixel, Braille, Mosaïque, Gravure, Sillons) cherchaient, pour chaque échantillon, la graine qui minimise
   |p−k| − w_k en parcourant TOUTES les graines : Gravure coûtait 440 ms par Toile (1,9 s à ×4). Cet index range les graines
   dans une grille de pas `avg()` et parcourt des anneaux de cases autour du point ; il s'arrête dès qu'aucune case
   restante ne peut faire mieux : une graine hors des r premiers anneaux est à ≥ r·pas du point, donc son score est
   ≥ r·pas − w_max. **Même graine gagnante, au pixel près** (à égalité, la plus petite, comme la boucle d'origine).
   Construit une fois par passe de peinture ; retombe sur la boucle complète si la grille serait démesurée. */
function _grilleProp(){
  var n=seeds.length; if(n<24) return null;
  var cs=Math.max(8,avg()), X=new Float64Array(n), Y=new Float64Array(n), Wt=new Float64Array(n), mw=0, x0=1e18,y0=1e18,x1=-1e18,y1=-1e18;
  for(var k=0;k<n;k++){ var s=seeds[k]; X[k]=s.px==null?s.x:s.px; Y[k]=s.py==null?s.y:s.py; Wt[k]=s.w||0; if(Wt[k]>mw) mw=Wt[k];
    if(X[k]<x0)x0=X[k]; if(X[k]>x1)x1=X[k]; if(Y[k]<y0)y0=Y[k]; if(Y[k]>y1)y1=Y[k]; }
  var gx0=Math.floor(x0/cs), gy0=Math.floor(y0/cs), gw=Math.floor(x1/cs)-gx0+1, gh=Math.floor(y1/cs)-gy0+1;
  if(!(gw>0&&gh>0) || gw*gh>40000) return null;
  var C=new Array(gw*gh); for(var q=0;q<C.length;q++) C[q]=[];
  for(k=0;k<n;k++) C[(Math.floor(Y[k]/cs)-gy0)*gw + (Math.floor(X[k]/cs)-gx0)].push(k);
  var rmax=gw+gh+2, res={bi:0,bd:1e18,bd2:1e18};
  function prop(x,y){
    var ci=Math.floor(x/cs)-gx0, cj=Math.floor(y/cs)-gy0, bd=1e18, bd2=1e18, bi=-1;
    var rmin=Math.max(0, -ci, -cj, ci-(gw-1), cj-(gh-1));   /* le premier anneau qui touche la grille */
    for(var r=0;r<=rmax+rmin;r++){
      for(var j=cj-r;j<=cj+r;j++){ if(j<0||j>=gh) continue;
        var pas=(j===cj-r||j===cj+r)?1:2*r;
        for(var i=ci-r;i<=ci+r;i+=(pas||1)){ if(i<0||i>=gw) continue;
          var L=C[j*gw+i];
          for(var m=0;m<L.length;m++){ var kk=L[m], dx=x-X[kk], dy=y-Y[kk], d=Math.sqrt(dx*dx+dy*dy)-Wt[kk];
            if(d<bd || (d===bd && kk<bi)){ bd2=bd; bd=d; bi=kk; } else if(d<bd2) bd2=d; } } }
      if(r>=rmin && bd2 <= r*cs - mw) break;                 /* aucune case restante ne peut faire mieux, ni le second */
    }
    res.bi=bi<0?0:bi; res.bd=bd; res.bd2=bd2; return res;
  }
  return {prop:prop, X:X, Y:Y, Wt:Wt};   /* v38 : les coordonnées et poids que `prop` compare — Gravure s'en sert pour écarter un point sans requête */
}
function cAt(x,y){var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=x-_kx,dy=y-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}return seeds[bi];}
function cOf(s,now){var g0=s.gc||(s.gc=_shadeG(s.gray,s.tone,s.shade));if(s.tOut!=null&&s.cOut){var pO=ease(Math.max(0,(now-s.tOut)/760));if(pO<1)return [s.cOut[0]+(g0[0]-s.cOut[0])*pO,s.cOut[1]+(g0[1]-s.cOut[1])*pO,s.cOut[2]+(g0[2]-s.cOut[2])*pO];s.tOut=null;s.cOut=null;}   /* ⚑ v55 : une dalle qui part (semis constant) éteint sa couleur vers son gris, en 760 ms comme elle l'a allumée */if(s.kind==='gray'&&(s.t0===0||now-s.t0>760))return g0;var p=ease((now-s.t0)/760);var to=s.ci!=null?(s.rgb||((palKey==='signal'&&!s.apercu&&!s.choisi)?((s.nat==null&&!isLightM())?[31,22,17]:PALL()[s.nat!=null?s.nat:3][s.lit|0]):PALL()[s.ci][s.lit|0])):g0;   /* ⚑ v27 (Tom, Q307 tranché) : « sous Ingénu, un ton de palette CHOISI À LA MAIN passe devant la nature, comme le code libre le fait déjà. Ingénu colore par nature PAR DÉFAUT ; un choix explicite prime toujours. » */   /* ⚑ v17 INGÉNU (Tom) : la couleur dit la nature — Promi 0 bleu, Chiche 1 rose, Nuée 2 lilas ; une cellule sans parole prend le crème dalle (3) ; un code libre du Cercle, choisi à la main, passe toujours devant */   /* ⚑ Cercle · LA COULEUR (Tom 13 sept.) : un code libre passe devant la palette — jamais sur une dalle masquée (ci nul) */var c=[g0[0]+(to[0]-g0[0])*p,g0[1]+(to[1]-g0[1])*p,g0[2]+(to[2]-g0[2])*p];for(var q=0;q<3;q++){if(c[q]>255)c[q]=255;if(c[q]<0)c[q]=0;}return c;}
/* ⚑ v89 (Tom, Q348) — LE NOIR ET BLANC. La Toile passe au ton de la Toile vide : en sombre, du crème sur le fond sombre ; en clair,
   l'inverse. Chaque couleur de dalle (et de graine vide) est ramenée à ce ton ; il ne reste qu'une légère différence de clarté, que la
   JAUGE dose (0 : les dalles ne se distinguent plus des vides ; 1 : des tons francs). L'agencement, le monde, rien d'autre ne change.
   Une seule décision de teinte (cOf) : tous les mondes, la Toile et les aperçus, la suivent. */
var _cOfBrut=cOf;
cOf=function(s,now){ var c=_cOfBrut(s,now); var nb=window._promiNB; if(!nb||!nb.on||!c) return c;
  var lt=isLightM(), base=lt?[32,25,8]:[239,227,199], fond=lt?[241,236,217]:[5,3,2], L=(0.2126*c[0]+0.7152*c[1]+0.0722*c[2])/255, j=nb.j;
  var k=0.05+j*0.62*(lt?L:(1-L)); if(k<0)k=0; if(k>0.72)k=0.72;
  return [base[0]+(fond[0]-base[0])*k, base[1]+(fond[1]-base[1])*k, base[2]+(fond[2]-base[2])*k]; };
function RpixDirect(now,x0,y0,x1,y1){var STEP=5*UK,_G=_grilleProp();g.setTransform(DPR,0,0,DPR,0,0);for(var sy=0;sy<H;sy+=STEP){for(var sx=0;sx<W;sx+=STEP){var lx=(sx+STEP/2-view.ox)/view.s,ly=(sy+STEP/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H)continue;var bi=0;if(_G){bi=_G.prop(lx,ly).bi;}else{var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx,sy,STEP+UK,STEP+UK);}}}
/* ⚑ v39 (perf) — BUVARD FUSIONNE LES CARRÉS VOISINS DE MÊME COULEUR. ~13 000 `fillRect` de STEP+UK, opaques, sur des cotes de la grille : une suite de n carrés de la même couleur sur une rangée devient UN rectangle de n·STEP+UK — même surface couverte, même couleur, rien en transparence. La couleur n'est reposée que si elle change. `_perfAncien` = l'ancien. */
function Rpix(now,x0,y0,x1,y1){if(window._perfAncien)return RpixDirect(now,x0,y0,x1,y1);var _rs=null,_rx=0,_rn=0,_ry=0,_ps=null;function _rv(){if(_rs===null)return;if(_rs!==_ps){g.fillStyle=_rs;_ps=_rs;}g.fillRect(_rx,_ry,_rn*STEP+UK*_vv,STEP+UK*_vv);_rs=null;}var _vv=(g.canvas&&g.canvas.id==='toileCv')?view.s:1,_gx=(g.canvas&&g.canvas.id==='toileCv')?view.ox:0,_gy=(g.canvas&&g.canvas.id==='toileCv')?view.oy:0;   /* ⚑ v46 : la grille est celle de la Toile, à la taille du zoom — à l'échelle 1, exactement celle d'avant */
  var STEP=5*UK*_vv,_G=_grilleProp();g.setTransform(DPR,0,0,DPR,0,0);var _sy0=_gy-Math.ceil(_gy/STEP)*STEP,_sx0=_gx-Math.ceil(_gx/STEP)*STEP;for(var sy=_sy0;sy<H;sy+=STEP){for(var sx=_sx0;sx<W;sx+=STEP){var lx=(sx+STEP/2-view.ox)/view.s,ly=(sy+STEP/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H){_rv();continue;}var bi=0;if(_G){bi=_G.prop(lx,ly).bi;}else{var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var sb=seeds[bi],c=cOf(sb,now),col='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';if(col===_rs&&_ry===sy&&Math.abs(_rx+_rn*STEP-sx)<1e-9){_rn++;}else{_rv();_rs=col;_rx=sx;_ry=sy;_rn=1;}}_rv();}}
function Rbra(now,x0,y0,x1,y1){var _G=_grilleProp(),DOT=9*UK,sx=Math.floor(x0/DOT)*DOT+DOT*.5,sy=Math.floor(y0/DOT)*DOT+DOT*.5;for(var y=sy;y<y1;y+=DOT){for(var x=sx;x<x1;x+=DOT){var bd=1e18,bd2=1e18,bi=0;if(_G){var _P=_G.prop(x,y);bi=_P.bi;bd=_P.bd;bd2=_P.bd2;}else{for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=x-_kx,dy=y-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd2=bd;bd=d;bi=k;}else if(d<bd2)bd2=d;}}var s=seeds[bi],c=cOf(s,now),ed=(bd2-bd)<5*UK,rad=((s.kind==='gray')?2:(ed?2:2.9))*UK;g.beginPath();g.arc(x,y,rad,0,6.2832);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fill();}}}
function RsilDirect(now,x0,y0,x1,y1){var _G=_grilleProp();g.lineCap='round';g.lineJoin='round';var SP=6*UK,AMP=4.5*UK,WL=0.018/UK,LS=6*UK;function wv(xx,ln){return AMP*Math.sin(xx*WL+ln*.55)+AMP*.62*Math.sin(xx*WL*2.4-ln*.42+1.2);}var li=Math.floor(y0/SP);for(var bY=li*SP+SP*.5;bY<y1;bY+=SP,li++){var sX=Math.max(0,x0),run=[],rk=null,rcl=false;function flush(){if(run.length>1){g.beginPath();g.strokeStyle='rgb('+rk+')';g.lineWidth=(rcl?1.5:0.85)*UK;g.moveTo(run[0][0],run[0][1]);for(var q=1;q<run.length;q++)g.lineTo(run[q][0],run[q][1]);g.stroke();}}for(var x=sX;x<=x1;x+=LS){var y=bY+wv(x,li);var s=_G?seeds[_G.prop(x,bY).bi]:cAt(x,bY),c=cOf(s,now),key=(c[0]|0)+','+(c[1]|0)+','+(c[2]|0);if(rk!==null&&key!==rk){var last=run[run.length-1];flush();run=[last];}run.push([x,y]);rk=key;rcl=(s.kind!=='gray');}flush();}}
/* ⚑ v39 (perf) — HOULE : LES ONDES SONT FIXES, SEULES LEURS COULEURS DÉPENDENT DU SEMIS. On calcule à chaque image la suite
   exacte des morceaux (couleur, épaisseur, points) — le même calcul que `RsilDirect` — et sa signature ; si elle n'a pas
   changé (ni la transformation ni la taille du canevas), on repose le calque 1:1, sinon on le repeint avec LES MÊMES
   tracés, dans le même ordre. Tracer ~9 000 segments fins coûtait 16 ms à chaque image. `_perfAncien` = l'ancien. */
var _silCal=null;
function Rsil(now,x0,y0,x1,y1){var cv0=g&&g.canvas;if(window._perfAncien||DPR>3||!cv0||!g.getTransform||_cibleDalle||!(cv0.id==='toileCv'||cv0===_rtCible))return RsilDirect(now,x0,y0,x1,y1);
  var _G=_grilleProp(),SP=6*UK,AMP=4.5*UK,WL=0.018/UK,LS=6*UK,R=[],sig=[];
  function wv(xx,ln){return AMP*Math.sin(xx*WL+ln*.55)+AMP*.62*Math.sin(xx*WL*2.4-ln*.42+1.2);}
  var li=Math.floor(y0/SP);
  for(var bY=li*SP+SP*.5;bY<y1;bY+=SP,li++){var sX=Math.max(0,x0),run=[],rk=null,rcl=false;
    var flush=function(){if(run.length>1){R.push([rk,rcl,run]);sig.push(rk+(rcl?'#':'.')+run.length+'@'+run[0][0]);}};
    for(var x=sX;x<=x1;x+=LS){var y=bY+wv(x,li);var s=_G?seeds[_G.prop(x,bY).bi]:cAt(x,bY),c=cOf(s,now),key=(c[0]|0)+','+(c[1]|0)+','+(c[2]|0);
      if(rk!==null&&key!==rk){var last=run[run.length-1];flush();run=[last];}run.push([x,y]);rk=key;rcl=(s.kind!=='gray');}
    flush();}
  var M=g.getTransform(),k=[M.a,M.b,M.c,M.d,M.e,M.f,cv0.width,cv0.height,UK,x0,y0,x1,y1,sig.join(';')].join('|'),C=_silCal;
  if(!C||C.k!==k){var sc=(C&&C.cv)||document.createElement('canvas');sc.width=cv0.width;sc.height=cv0.height;
    var G=sc.getContext('2d');G.setTransform(M.a,M.b,M.c,M.d,M.e,M.f);G.lineCap='round';G.lineJoin='round';
    for(var i=0;i<R.length;i++){var r=R[i],p=r[2];G.beginPath();G.strokeStyle='rgb('+r[0]+')';G.lineWidth=(r[1]?1.5:0.85)*UK;G.moveTo(p[0][0],p[0][1]);for(var q=1;q<p.length;q++)G.lineTo(p[q][0],p[q][1]);G.stroke();}
    C=_silCal={k:k,cv:sc};}
  g.save();g.setTransform(1,0,0,1,0,0);g.drawImage(C.cv,0,0);g.restore();g.lineCap='round';g.lineJoin='round';}
function RgraDirect(now,x0,y0,x1,y1){g.lineCap='round';g.lineJoin='round';var HS=8*UK,SS=5*UK,ac=avg(),_G=_grilleProp();for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=(cl?2:1.05)*UK;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0;if(_G){bi=_G.prop(qx,qy).bi;}else{for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,ex=qx-_kx,ey=qy-_ky,d=Math.sqrt(ex*ex+ey*ey)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var ins=(bi===ci)&&qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins&&!run){run=true;g.beginPath();g.moveTo(qx,qy);}else if(ins){g.lineTo(qx,qy);}else if(run){g.stroke();run=false;}}if(run)g.stroke();}}}
/* ⚑ v38 (perf) — UN POINT DE HACHURE HORS DE SA CELLULE S'ÉCARTE SANS REQUÊTE. Le propriétaire du point précédent (`_der`) est comparé à la graine qui trace, par LA MÊME formule que `prop` (mêmes coordonnées X/Y/Wt, même règle d'égalité : l'indice le plus bas gagne) : s'il est strictement meilleur, la graine ne possède pas le point — la décision est celle de `prop`, exactement. Sinon la requête complète. Le cadre est testé AVANT (l'ordre ne change pas le résultat). L'ancien chemin reste pour la preuve (`_perfAncien`). */
function Rgra(now,x0,y0,x1,y1){if(window._perfAncien)return RgraDirect(now,x0,y0,x1,y1);g.lineCap='round';g.lineJoin='round';var HS=8*UK,SS=5*UK,ac=avg(),_G=_grilleProp(),_GX=_G&&_G.X,_GY=_G&&_G.Y,_GW=_G&&_G.Wt,_der=-1,_lx=null,_ly=0;for(var ci=0;ci<seeds.length;ci++){var s=seeds[ci];if(s.x<x0-100||s.x>x1+100||s.y<y0-100||s.y>y1+100)continue;var R=ac*1.85+s.w,an=s.ang,dx=Math.cos(an),dy=Math.sin(an),px=-dy,py=dx,c=cOf(s,now),cl=(s.kind!=='gray');g.strokeStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.lineWidth=(cl?2:1.05)*UK;for(var off=-R;off<=R;off+=HS){var ox=s.x+px*off,oy=s.y+py*off,run=false;for(var t=-R;t<=R;t+=SS){var qx=ox+dx*t,qy=oy+dy*t,bd=1e18,bi=0,ins=qx>=x0-2&&qx<=x1+2&&qy>=y0-2&&qy<=y1+2;if(ins){if(_G){var _ex=qx-_GX[ci],_ey=qy-_GY[ci],_dc=Math.sqrt(_ex*_ex+_ey*_ey)-_GW[ci],_ecarte=false;if(_der>=0&&_der!==ci){var _fx=qx-_GX[_der],_fy=qy-_GY[_der],_dl=Math.sqrt(_fx*_fx+_fy*_fy)-_GW[_der];_ecarte=(_dl<_dc||(_dl===_dc&&_der<ci));}if(_ecarte)ins=false;else{bi=_G.prop(qx,qy).bi;_der=bi;ins=(bi===ci);}}else{for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,ex=qx-_kx,ey=qy-_ky,d=Math.sqrt(ex*ex+ey*ey)-seeds[k].w;if(d<bd){bd=d;bi=k;}}ins=(bi===ci);}}if(ins&&!run){run=true;g.beginPath();g.moveTo(qx,qy);_lx=null;}else if(ins){_lx=qx;_ly=qy;}else if(run){if(_lx!==null)g.lineTo(_lx,_ly);g.stroke();run=false;}}if(run){if(_lx!==null)g.lineTo(_lx,_ly);g.stroke();}}}}   /* v38 : une hachure est une DROITE — ses points intermédiaires, alignés, n'ajoutaient que des sommets au traceur ; on va du premier au dernier */
function Rmos(now,x0,y0,x1,y1){var _vv=(g.canvas&&g.canvas.id==='toileCv')?view.s:1,_gx=(g.canvas&&g.canvas.id==='toileCv')?view.ox:0,_gy=(g.canvas&&g.canvas.id==='toileCv')?view.oy:0;   /* ⚑ v46 : la grille est celle de la Toile, à la taille du zoom */
  var T=11*UK*_vv,_G=_grilleProp();g.setTransform(DPR,0,0,DPR,0,0);var _sy0=_gy-Math.ceil(_gy/T)*T,_sx0=_gx-Math.ceil(_gx/T)*T;for(var sy=_sy0;sy<H;sy+=T){for(var sx=_sx0;sx<W;sx+=T){var lx=(sx+T/2-view.ox)/view.s,ly=(sy+T/2-view.oy)/view.s;if(lx<0||lx>W||ly<0||ly>H)continue;var bi=0;if(_G){bi=_G.prop(lx,ly).bi;}else{var bd=1e18,bi=0;for(var k=0;k<seeds.length;k++){var _kx=seeds[k].px==null?seeds[k].x:seeds[k].px,_ky=seeds[k].py==null?seeds[k].y:seeds[k].py,dx=lx-_kx,dy=ly-_ky,d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;if(d<bd){bd=d;bi=k;}}}var c=cOf(seeds[bi],now);g.fillStyle='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';g.fillRect(sx+UK*_vv,sy+UK*_vv,T-2*UK*_vv,T-2*UK*_vv);}}}
function Renc(now,x0,y0,x1,y1){g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);var px=_sx*view.s+view.ox,py=_sy*view.s+view.oy;var rad=sp*0.6*view.s;if(px<-rad*2.5||px>W+rad*2.5||py<-rad*2.5||py>H+rad*2.5)continue;var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);g.save();g.translate(px,py);if(_rf<0.999)g.scale(_rf,_rf);   /* v76 : le repli */if(s.drot)g.rotate(s.drot);if(s.dsx)g.scale(s.dsx,s.dsy);g.fillStyle='rgba('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+',.9)';var sd=((k+1)*2654435761)>>>0,rnd=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};for(var b=0;b<9;b++){var _ex=(rnd()-.5)*rad*1.2,_ey=(rnd()-.5)*rad,_rx=rad*(.32+rnd()*.42),_ry=rad*(.16+rnd()*.32),_ea=rnd()*3.14;if(s.dw){var _wp=s.ph+b*1.7;_ex+=Math.sin(now*0.006+_wp)*rad*0.22*s.dw;_ey+=Math.cos(now*0.0072+_wp)*rad*0.18*s.dw;_rx*=1+Math.sin(now*0.0085+_wp)*0.26*s.dw;_ry*=1+Math.cos(now*0.0079+_wp)*0.26*s.dw;_ea+=Math.sin(now*0.005+_wp)*0.6*s.dw;}g.beginPath();g.ellipse(_ex,_ey,_rx,_ry,_ea,0,6.3);g.fill();}g.restore();}}
/* assainissement (30 sept.) : Rblok retiré — le monde Éclats n'existait plus au Studio (Q102) */

function Rterr(now,x0,y0,x1,y1){if(!(g.canvas&&g.canvas.id==='toileCv'))g.setTransform(DPR,0,0,DPR,0,0);   /* ⚑ v46 : sur la Toile vivante, la vue (le zoom) est gardée */var sp=Math.sqrt(W*H/Math.max(1,seeds.length));for(var k=0;k<seeds.length;k++){var s=seeds[k];var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);var _sx=(s.px!=null?s.px:s.x),_sy=(s.py!=null?s.py:s.y);var sd=((k+1)*2654435761)>>>0;var rr=function(){sd=(sd*1103515245+12345)&0x7fffffff;return sd/0x7fffffff;};g.fillStyle="rgb("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+")";for(var e=0;e<7;e++){var a=rr()*6.2832,rd=rr()*sp*0.46*_rf;var ex=_sx+Math.cos(a)*rd,ey=_sy+Math.sin(a)*rd;var w2=sp*(0.11+rr()*0.19)*_rf,h2=sp*(0.08+rr()*0.15)*_rf;   /* v76 : _rf, le repli */g.save();g.translate(ex,ey);g.rotate(rr()*3.1416);g.beginPath();var sides=4+((rr()*3)|0);for(var s2=0;s2<sides;s2++){var an=s2/sides*6.2832;var px=Math.cos(an)*w2*(0.7+rr()*0.5),py=Math.sin(an)*h2*(0.7+rr()*0.5);s2?g.lineTo(px,py):g.moveTo(px,py);}g.closePath();g.fill();g.restore();}}}
function _tfInk(){return isLightM()?[34,28,21]:[246,241,231];}
/* ⚑ v115 (Tom) — L'ENCRE DE TOUFFE, EN SOMBRE, EST NEUTRE : #F4F2F0 (OKLCH C 0,003). #F6F1E7 (h 84,6°, C 0,014) composée en sRGB sur un fond
   brun passait le seuil du kaki (C 0,015–0,016 : les fleurs vides). Touffe seulement — l'encre du produit (`_tfInk`) reste celle des autres mondes ;
   le mode clair ne change pas. */
function _tfInkTouffe(){return isLightM()?[34,28,21]:[244,242,240];}
function _tfHand(g,pts,jit,rnd){g.beginPath();var n=pts.length;for(var i=0;i<=n;i++){var A=pts[i%n],B=pts[(i+1)%n];var ax=A[0]+(rnd()-.5)*jit, ay=A[1]+(rnd()-.5)*jit;if(i===0){g.moveTo(ax,ay);continue;}var mx=(A[0]+B[0])/2+(rnd()-.5)*jit*1.3, my=(A[1]+B[1])/2+(rnd()-.5)*jit*1.3;g.quadraticCurveTo(mx,my,ax,ay);}g.closePath();}
function _tfStroke(g,w,col,alpha){g.lineJoin="round";g.lineCap="round";g.strokeStyle="rgba("+(col[0]|0)+","+(col[1]|0)+","+(col[2]|0)+","+(alpha==null?1:alpha)+")";g.lineWidth=w;g.stroke();}
function _tfFill(g,col,rnd,off){g.save();g.translate((rnd()-.5)*off,(rnd()-.5)*off);g.fillStyle="rgb("+(col[0]|0)+","+(col[1]|0)+","+(col[2]|0)+")";g.fill();g.restore();}
function _tfPetal(g,len,wid,bend,rnd,jit){var j=function(){return (rnd()-.5)*jit;};g.beginPath();g.moveTo(j(),j());g.bezierCurveTo(wid+j(), len*0.3+j(), wid*0.72+bend+j(), len*0.8+j(), j()*0.6, len+j());g.bezierCurveTo(-wid*0.72+bend+j(), len*0.8+j(), -wid+j(), len*0.3+j(), j(), j());g.closePath();}
function _tfPetalR(g,len,wid,bend,rnd,jit){var j=function(){return (rnd()-.5)*jit;};var tw=wid*0.3;g.beginPath();g.moveTo(j(),j());g.bezierCurveTo(wid+j(), len*0.3+j(), wid*0.72+bend+j(), len*0.82, tw+bend+j(), len*0.95);g.quadraticCurveTo(bend+j(), len*1.0, -tw+bend+j(), len*0.95);g.bezierCurveTo(-wid*0.72+bend+j(), len*0.82+j(), -wid+j(), len*0.3+j(), j(), j());g.closePath();}
function RtoufDirect(now,x0,y0,x1,y1){var _viv=(g.canvas&&g.canvas.id==='toileCv');if(!_viv)g.setTransform(DPR,0,0,DPR,0,0);var sp=Math.sqrt(W*H/Math.max(1,seeds.length));var ink=_tfInkTouffe();for(var i=0;i<seeds.length;i++){var s=seeds[i];var sx=(s.px!=null?s.px:s.x),sy=(s.py!=null?s.py:s.y);if(_viv&&(sx<x0-sp*1.3||sx>x1+sp*1.3||sy<y0-sp*1.3||sy>y1+sp*1.3))continue;   /* ⚑ v46 : très zoomé, on ne peint que ce qui se voit */var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);var _sd=((i+1)*2654435761)>>>0;var rnd=function(){_sd=(_sd*1103515245+12345)&0x7fffffff;return _sd/0x7fffffff;};var heart=[c[0]+(ink[0]-c[0])*0.45,c[1]+(ink[1]-c[1])*0.45,c[2]+(ink[2]-c[2])*0.45];   /* ⚑ v29 (Tom) : le cœur était #DD4D23, la couleur « à tenir » — un monde ne porte jamais une couleur d'état. Il est désormais la couleur de SA cellule, poussée vers l'encre du contour : une nuance de cOf, rien d'inventé. */var n=3+((rnd()*3)|0);for(var f2=0;f2<n;f2++){var ox=sx+(rnd()-.5)*sp*0.86, oy=sy+(rnd()-.5)*sp*0.8;var R=sp*(0.13+rnd()*0.2);var stage=rnd();g.strokeStyle="rgba("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+",0.6)";g.lineWidth=Math.max(1.2,R*0.2);g.lineCap="round";g.beginPath();g.moveTo(ox+(rnd()-.5)*5,oy+sp*0.5);g.quadraticCurveTo(ox+(rnd()-.5)*R,oy+sp*0.2,ox,oy);g.stroke();g.save();g.translate(ox,oy);g.rotate(rnd()*6.2832);if(stage<0.24){var bp=[[-R*0.4,R*0.3],[-R*0.34,-R*0.4],[0,-R*0.72],[R*0.34,-R*0.4],[R*0.4,R*0.3]];_tfHand(g,bp,R*0.08,rnd);_tfFill(g,c,rnd,R*0.08);_tfHand(g,bp,R*0.08,rnd);_tfStroke(g,Math.max(1.1,R*0.17),ink,0.9);}else{var np=6+((rnd()*3)|0);for(var k=0;k<np;k++){if(stage>0.8&&rnd()<0.2)continue;g.save();g.rotate(k/np*6.2832+(rnd()-.5)*0.34);var len=R*(0.85+rnd()*0.6), wid=R*(0.26+rnd()*0.16);var _rd=(((i*13+f2*7+k*5)%10)<2);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfFill(g,c,rnd,R*0.09);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfStroke(g,Math.max(1,R*0.16),ink,0.88);g.restore();}g.beginPath();g.arc((rnd()-.5)*R*0.12,(rnd()-.5)*R*0.12,R*0.3,0,6.2832);g.fillStyle="rgb("+heart[0]+","+heart[1]+","+heart[2]+")";g.fill();_tfStroke(g,Math.max(1,R*0.15),ink,0.85);}g.restore();}}}
function _toufGraine(g,i,c,sx,sy,sp,ink){var _sd=((i+1)*2654435761)>>>0;var rnd=function(){_sd=(_sd*1103515245+12345)&0x7fffffff;return _sd/0x7fffffff;};var heart=[c[0]+(ink[0]-c[0])*0.45,c[1]+(ink[1]-c[1])*0.45,c[2]+(ink[2]-c[2])*0.45];   /* ⚑ v29 (Tom) : le cœur était #DD4D23, la couleur « à tenir » — un monde ne porte jamais une couleur d'état. Il est désormais la couleur de SA cellule, poussée vers l'encre du contour : une nuance de cOf, rien d'inventé. */var n=3+((rnd()*3)|0);for(var f2=0;f2<n;f2++){var ox=sx+(rnd()-.5)*sp*0.86, oy=sy+(rnd()-.5)*sp*0.8;var R=sp*(0.13+rnd()*0.2);var stage=rnd();g.strokeStyle="rgba("+(c[0]|0)+","+(c[1]|0)+","+(c[2]|0)+",0.6)";g.lineWidth=Math.max(1.2,R*0.2);g.lineCap="round";g.beginPath();g.moveTo(ox+(rnd()-.5)*5,oy+sp*0.5);g.quadraticCurveTo(ox+(rnd()-.5)*R,oy+sp*0.2,ox,oy);g.stroke();g.save();g.translate(ox,oy);g.rotate(rnd()*6.2832);if(stage<0.24){var bp=[[-R*0.4,R*0.3],[-R*0.34,-R*0.4],[0,-R*0.72],[R*0.34,-R*0.4],[R*0.4,R*0.3]];_tfHand(g,bp,R*0.08,rnd);_tfFill(g,c,rnd,R*0.08);_tfHand(g,bp,R*0.08,rnd);_tfStroke(g,Math.max(1.1,R*0.17),ink,0.9);}else{var np=6+((rnd()*3)|0);for(var k=0;k<np;k++){if(stage>0.8&&rnd()<0.2)continue;g.save();g.rotate(k/np*6.2832+(rnd()-.5)*0.34);var len=R*(0.85+rnd()*0.6), wid=R*(0.26+rnd()*0.16);var _rd=(((i*13+f2*7+k*5)%10)<2);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfFill(g,c,rnd,R*0.09);(_rd?_tfPetalR:_tfPetal)(g,len,wid,(rnd()-.5)*R*0.3,rnd,R*0.09);_tfStroke(g,Math.max(1,R*0.16),ink,0.88);g.restore();}g.beginPath();g.arc((rnd()-.5)*R*0.12,(rnd()-.5)*R*0.12,R*0.3,0,6.2832);g.fillStyle="rgb("+heart[0]+","+heart[1]+","+heart[2]+")";g.fill();_tfStroke(g,Math.max(1,R*0.15),ink,0.85);}g.restore();}}
function Rtouf(now,x0,y0,x1,y1){
  /* ⚑ v38 (perf) — CHAQUE GRAINE PEINT SES FLEURS UNE FOIS, dans un calque à sa taille finale, posé 1:1 ensuite.
     Le dessin est le MÊME (`_toufGraine` est le corps d'origine, recopié) ; la fraction de pixel de la graine est
     intégrée au calque, qui se pose donc sur une cote ENTIÈRE : aucun rééchantillonnage. Le calque se refait si sa
     couleur, son pas, l'encre ou la densité changent — et, s'il a bougé, dès qu'il est posé (pendant le mouvement il se
     pose à la cote entière la plus proche : ≤ ½ pixel d'appareil). Touffe ignore la vue (setTransform(DPR)) et ses fleurs
     ne dépendent pas des voisines : c'est ce qui rend le calque exact. Le chemin direct garde les dalles (`_cibleDalle`),
     les aperçus et l'export (DPR > 3). Mesuré au dessin forcé : 61 → voir CONTRAT-MONDE §8.4. */
  var cv0=g&&g.canvas;
  if(window._perfAncien||_cibleDalle||DPR>3||!cv0||!(cv0.id==='toileCv'||cv0===_rtCible))return RtoufDirect(now,x0,y0,x1,y1);
  /* ⚑ v46 (Tom : « le zoom dans tous les mondes, comme une photo ») — Touffe ignorait la vue : ses fleurs ne grossissaient
     jamais. Les calques sont désormais posés à la place ET à la taille du zoom. Pendant un geste (pincement, élan, retour),
     un calque dont l'échelle a changé de moins d'un tiers est seulement mis à l'échelle (fluide) ; il se redessine net dès
     que le zoom se pose. Au-delà de ×1,3 le chemin direct (vectoriel, et qui ne peint que ce qui se voit) prend le relais. */
  var vs=(cv0.id==='toileCv')?view.s:1, vox=(cv0.id==='toileCv')?view.ox:0, voy=(cv0.id==='toileCv')?view.oy:0;
  var mouv=!!(pinch||_inert||_pan||vTarget&&Math.abs(vTarget.s-view.s)>0.0015);
  if(vs>1.3&&!mouv)return RtoufDirect(now,x0,y0,x1,y1);   /* posé et très zoomé : les vecteurs, nets */
  var sv=Math.min(vs,1.3);   /* un calque ne se bâtit jamais plus grand que ×1,3 */
  var sp=Math.sqrt(W*H/Math.max(1,seeds.length)),ink=_tfInkTouffe(),B=Math.ceil(1.1*sp*DPR*sv)+4,T=2*B+2;
  g.save();g.setTransform(1,0,0,1,0,0);
  for(var i=0;i<seeds.length;i++){var s=seeds[i];var _rf=_repliF(s);if(_rf<0.02)continue;var c=cOf(s,now);var sx=(s.px!=null?s.px:s.x),sy=(s.py!=null?s.py:s.y);
    var X=(sx*vs+vox)*DPR,Y=(sy*vs+voy)*DPR,k=i+'|'+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+'|'+(+c[0]).toFixed(3)+','+(+c[1]).toFixed(3)+','+(+c[2]).toFixed(3)+'|'+sp+'|'+ink[0]+'|'+DPR,C=s.__tf;
    var Bv=B*vs/sv; if(X<-Bv||Y<-Bv||X>cv0.width+Bv||Y>cv0.height+Bv)continue;
    var fx=X-Math.floor(X),fy=Y-Math.floor(Y),pose=(s.__tfX===X&&s.__tfY===Y);s.__tfX=X;s.__tfY=Y;
    if(C&&C.k===k&&C.vs!==vs&&mouv){var r=vs/C.vs;g.drawImage(C.cv,X-(C.B+C.fx)*r,Y-(C.B+C.fy)*r,C.T*r,C.T*r);continue;}   /* en mouvement : mis à l'échelle, redessiné net quand le zoom se pose */
    if(!C||C.k!==k||C.vs!==sv||(pose&&(C.fx!==fx||C.fy!==fy))){
      if(!C){C=s.__tf={cv:document.createElement('canvas')};}
      if(C.cv.width!==T||C.cv.height!==T){C.cv.width=T;C.cv.height=T;}
      var G=C.cv.getContext('2d');G.setTransform(1,0,0,1,0,0);G.clearRect(0,0,T,T);G.setTransform(DPR*sv,0,0,DPR*sv,B+fx,B+fy);
      _toufGraine(G,i,c,0,0,sp,ink);C.k=k;C.fx=fx;C.fy=fy;C.vs=sv;C.B=B;C.T=T;}
    if(_rf<0.999){ g.drawImage(C.cv,X-(C.B+C.fx)*_rf*vs/C.vs,Y-(C.B+C.fy)*_rf*vs/C.vs,C.T*_rf*vs/C.vs,C.T*_rf*vs/C.vs); continue; }   /* v76 : le temps de son repli (ou de sa repousse), la fleur suit l'échelle */
    if(C.vs===vs) g.drawImage(C.cv,Math.round(X-C.fx)-C.B,Math.round(Y-C.fy)-C.B);
    else { var r2=vs/C.vs; g.drawImage(C.cv,X-(C.B+C.fx)*r2,Y-(C.B+C.fy)*r2,C.T*r2,C.T*r2); }}
  g.restore();g.setTransform(DPR,0,0,DPR,0,0);}
var RD={pixel:Rpix,braille:Rbra,sillons:Rsil,gravure:Rgra,mosaique:Rmos,encre:Renc,terrazzo:Rterr,touffe:Rtouf};
/* ⚑ v32 — LES QUATRE MONDES NEUFS. `creerMondes` (bloc lot-V32-MONDES) reçoit le moteur par ACCESSEURS : g, W, H, seeds,
   view sont relus à chaque appel, donc un monde neuf suit les échanges de globales des cinq chemins (§1 du contrat).
   · cOf(s, 0) rendait le GRIS de départ d'une dalle colorée (l'animation part de t0) : le carnet des mondes l'appelle à 0,
     il reçoit donc la couleur posée.  · `_dalleDeCle(pid)` : l'entier stable du titre et de la personne (jamais l'id).
   · `rampe` : aucune — la rampe v29 ne vaut que pour une dalle, jamais sur la Toile (§12 ter, Q3).
   · `cleToile` : Toile.cle() (v31).  · `fondToile()` : le fond du moteur, un seul propriétaire (v26).
   · `relance` : Madrure repeint l'onde d'avant tant que le semis bouge ; le moteur doit revenir la construire. */
var _cleVue={}; var _envM=null; var _MN=null, _MNLIB={esquille:1,bobinette:1,madrure:1}, _cibleDalle=null, _bordsDalle=null; var _rtCible=null;
try{ if(window.creerMondes){ _MN=window.creerMondes(_envM={
  get g(){return g;}, get W(){return W;}, get H(){return H;}, get DPR(){return DPR;}, get seeds(){return seeds;}, get view(){return view;},
  cOf:function(s,now){ return cOf(s, now||performance.now()); },
  avg:avg, cAt:cAt, isLightM:isLightM, curPAL:curPAL, rampe:null,
  _dalleDeCle:function(pid){ try{ for(var i=0;i<promises.length;i++){ if(promises[i].id===pid){ var p=promises[i], t=String(p.title||'')+'|'+String(p.who||''), h=2166136261;
    for(var j=0;j<t.length;j++){ h^=t.charCodeAt(j); h=Math.imul(h,16777619)>>>0; } _cleVue[pid]=h; return h; } } }catch(e){} return _cleVue[pid]!=null?_cleVue[pid]:null; },   /* ⚑ v43 : la dernière clé vue — une parole supprimée garde la sienne le temps de partir */
  get cleToile(){ try{ return (window.Toile&&window.Toile.cle)?window.Toile.cle():undefined; }catch(e){ return undefined; } },
  fondToile:function(){ return window.Toile.fondToile(); },
  relance:function(){ lastChange=performance.now(); kick(); },
  get cible(){ return _cibleDalle; },
  get bords(){ return _bordsDalle; },
  /* ⚑ v34 — l'unité de matière à la densité historique de la Toile (68 cellules), indépendante du nombre de promesses */
  get uMat(){ var a=_WT?_WT[0]*_WT[1]:W*H; return Math.sqrt(Math.max(1,a)/68)*UK; },   /* v63 : dans dalleTrame, W×H est la boîte de la cellule — l'unité reste celle de la Toile */
  get ingenu(){ return palKey==='signal'; },
  /* ⚑ v43 — la transition en cours, sur la Toile vivante seulement ; null partout ailleurs */
  get trans(){ if(!_transVive||!_trans||window._transCoupe) return null; var d=RD[theme]&&RD[theme].transDur; return (d&&performance.now()-_trans.t0<d)?_trans:null; },   /* v44 : éteinte à la fin de SA durée ; `_transCoupe` = preuve (la Toile sans transition) */
  get vive(){ return _transVive; },
  /* v66 — le papier : sur la Toile vivante, le dégradé même du fond, dans le repère de la vue ; ailleurs le fond du moteur */
  papierDesc:function(){ return (_transVive&&!_AP)?_fondVifDesc((0-view.ox)/view.s,(0-view.oy)/view.s,(W*0.55-view.ox)/view.s,(H-view.oy)/view.s):null; },
  papier:function(){ if(_transVive&&!_AP) return _fondVif(g,(0-view.ox)/view.s,(0-view.oy)/view.s,(W*0.55-view.ox)/view.s,(H-view.oy)/view.s); var c=window.Toile.fondToile(); return typeof c==='string'?c:'rgb('+c[0]+','+c[1]+','+c[2]+')'; },
  get finale(){ try{ return _semisFinal(); }catch(_){ return null; } }   /* v47 : l'équilibre de la Toile (point fixe de relax), partout */
});
  RD.esquille=_MN.esquille; RD.bobinette=_MN.bobinette; RD.ritournelle=_MN.ritournelle; RD.madrure=_MN.madrure; RD.halin=_MN.halin; } }catch(e){ _MN=null; }
/* ⚑ v62 — BROUILLAMINI (bloc lot-V62-BROUILLAMINI) : sa propre fabrique, le même environnement, plus la rampe de matière du
   monde (`rampeMat` = grays() : TH[monde].g en sombre, GLIGHT en clair). Monde LIBRE : ses dalles débordent la cellule, elles
   se peignent, se découpent et se touchent sur ce qu'il a peint ; `_MN` lui passe la main pour son nom. */
try{ if(_MN&&_envM&&window.creerBrouillamini){ var _MB=window.creerBrouillamini(Object.create(_envM,{rampeMat:{get:function(){ return grays(); }}}));
  RD.brouillamini=_MB.brouillamini; _MNLIB.brouillamini=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='brouillamini'?_MB[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v63 — CHAMADE (bloc lot-V63-CHAMADE), même patron ; en plus : l'ENCRE du produit (`_tfInk`, le précédent de Touffe) pour ses
   bandes et le trait de ses cœurs, et le fond du moteur (`fondToile`) pour le papier de sa dalle seule. */
try{ if(_MN&&_envM&&window.creerChamade){ var _MC=window.creerChamade(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.chamade=_MC.chamade; _MNLIB.chamade=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='chamade'?_MC[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v64 — VOLUBILIS (bloc lot-V64-VOLUBILIS), même patron, même encre du produit (Q331). */
try{ if(_MN&&_envM&&window.creerVolubilis){ var _MV=window.creerVolubilis(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.volubilis=_MV.volubilis; _MNLIB.volubilis=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='volubilis'?_MV[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v65 — GUINGOIS (bloc lot-V65-GUINGOIS), même patron, même encre. */
try{ if(_MN&&_envM&&window.creerGuingois){ var _MG=window.creerGuingois(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.guingois=_MG.guingois; _MNLIB.guingois=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='guingois'?_MG[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v66 — CHANTOURNÉ (bloc lot-V66-CHANTOURNE) : l'encre du produit, et la rampe de matière (ses flammes de fond). */
try{ if(_MN&&_envM&&window.creerChantourne){ var _MH=window.creerChantourne(Object.create(_envM,{encre:{get:function(){ return _tfInk; }},rampeMat:{get:function(){ return grays(); }}}));
  RD.chantourne=_MH.chantourne; _MNLIB.chantourne=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='chantourne'?_MH[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v67 — MASCARET (bloc lot-V67-MASCARET) : l'encre du produit ; son papier est celui du moteur (env.papier). */
try{ if(_MN&&_envM&&window.creerMascaret){ var _MS=window.creerMascaret(Object.create(_envM,{encre:{get:function(){ return _tfInk; }}}));
  RD.mascaret=_MS.mascaret; _MNLIB.mascaret=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='mascaret'?_MS[f]:o).apply(null,arguments); }; }); } }catch(e){}
/* ⚑ v68 — RAMAGE (bloc lot-V68-RAMAGE) : l'encre du produit, la rampe de matière (son plumage), le papier du moteur. */
try{ if(_MN&&_envM&&window.creerRamage){ var _MR=window.creerRamage(Object.create(_envM,{encre:{get:function(){ return _tfInk; }},rampeMat:{get:function(){ return grays(); }}}));
  RD.ramage=_MR.ramage; _MNLIB.ramage=1;
  ['seule','contour','toucher','nature','boite'].forEach(function(f){ var o=_MN[f]; _MN[f]=function(nom){ return (nom==='ramage'?_MR[f]:o).apply(null,arguments); }; }); } }catch(e){}

/* --- LES ÉTIQUETTES, sur la Toile elle-même ---
   L'app fournit le texte (window.Toile.labelOf) et dit si le mode est actif
   (window.Toile.labelsOn). L'encre est choisie par dalle : claire sur une
   dalle sombre, sombre sur une dalle claire — jamais de contour, jamais de voile. */
function _lum(c){
  function l(v){v/=255;return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4);}
  return 0.2126*l(c[0])+0.7152*l(c[1])+0.0722*l(c[2]);
}
function _fit(gg,txt,max){
  if(gg.measureText(txt).width<=max)return txt;
  var t=txt;
  while(t.length>1&&gg.measureText(t+'…').width>max)t=t.slice(0,-1);
  return t+'…';
}
function _labels(now){
  /* pendant l'onboarding, la Toile est un décor : pas de texte sur les dalles,
     même si le Studio est réglé « avec texte » */
  var _ob=document.getElementById('promiOnb');
  if(_ob&&!_ob.classList.contains('gone'))return;
  var T=window.Toile;
  if(!T||typeof T.labelsOn!=='function'||!T.labelsOn())return;
  if(typeof T.labelOf!=='function')return;
  g.setTransform(DPR,0,0,DPR,0,0);
  g.textAlign='center';g.textBaseline='middle';
  var ac=avg();                                  /* écart moyen entre dalles */
  if(ac*view.s<48) return;                       /* v98 : aucune dalle n'a la place de porter son titre (voir plus bas) */
  for(var i=0;i<seeds.length;i++){
    var s=seeds[i];
    if(s.kind==='gray')continue;
    /* un Promi masque au partage n'affiche pas son texte non plus */
    if(window._shLabels!==undefined&&s.pid!=null&&(window.shareHidden||{})[s.pid])continue;
    var L=null;try{L=T.labelOf(s);}catch(e){}
    if(!L||!L.title)continue;
    /* la dalle est dessinée à px/py (position réellement occupée) : l'étiquette doit suivre,
       sinon le texte reste à côté de sa dalle. */
    var _lx=(s.px!=null?s.px:s.x), _ly=(s.py!=null?s.py:s.y), _la=null;
    /* ⚑ v63 — un monde qui DÉPLACE sa dalle (Chamade écarte ses cœurs) déclare où il l'a posée, et sa largeur : le titre y va */
    if(RD[theme]&&RD[theme].ancre){ try{ _la=RD[theme].ancre(s); }catch(_e){ _la=null; } if(_la){ _lx=_la[0]; _ly=_la[1]; } }
    var sx=_lx*view.s+view.ox, sy=_ly*view.s+view.oy;
    if(sx<-60||sy<-40||sx>W+60||sy>H+40)continue;
    /* ⚑ v98 (Tom, 29 sept. : « illisibles à 200-500 paroles, c'est normal, on zoome pour lire — mais vérifie qu'ils disparaissent
       proprement plutôt que de s'empiler en bouillie ») — le titre ne se pose que si la dalle, À L'ÉCRAN, a la place de le porter :
       écart moyen × zoom ≥ 48 px (la taille de lettre y vaut 7,5, le plancher d'origine) ; il s'efface sur les 8 px au-dessous
       du plafond de 56. On zoome : les titres reviennent. Avant : bornés à 28 px de large et 7,5 px de haut, ils se chevauchaient
       — et `_fit` les rognait lettre à lettre (8 700 mesures de texte par image à 500, 1,4 s en WebKit). */
    var _ecr=ac*view.s; if(_ecr<48) continue; var _lab=Math.min(1,(_ecr-48)/8);
    var wmax=Math.max(28, ac*view.s*0.86);       /* on reste DANS la dalle */
    if(_la&&_la[2]) wmax=Math.max(28, Math.min(wmax, _la[2]*view.s*0.8));
    var col=cOf(s,now);
    var ink=(_lum(col)>0.179)?'#1E1301':'#FFFFFF';
    /* ⚑ v33 (Tom) — l'encre se choisit sur ce qui est PEINT dessous. Un monde qui sait ce qu'il a peint le dit
       (`RD[theme].sous`, Madrure) : cinq points le long du titre, luminance moyenne. Les autres gardent la cellule. */
    if(RD[theme]&&RD[theme].sous){ var _sm=0,_sn=0; for(var _k=-2;_k<=2;_k++){ var _c=null;
        try{ _c=RD[theme].sous(_lx+_k*wmax*0.2/view.s, _ly+fs*0.34/view.s); }catch(_e){}
        if(_c){ _sm+=_lum(_c); _sn++; } }
      if(_sn) ink=((_sm/_sn)>0.179)?'#1E1301':'#FFFFFF'; }
    var fs=Math.max(7.5, Math.min(13, ac*view.s*0.155));
    g.fillStyle=ink;
    if(L.who){
      g.font='600 '+(fs*0.68).toFixed(1)+'px Atkinson,system-ui,sans-serif';
      g.globalAlpha=0.72*_lab;
      g.fillText(_fit(g,String(L.who).toUpperCase(),wmax), sx, sy-fs*0.72);
      g.globalAlpha=1;
    }
    g.font='500 '+fs.toFixed(1)+'px Atkinson,system-ui,sans-serif';
    if(_lab<1) g.globalAlpha=_lab;
    g.fillText(_fit(g,L.title,wmax), sx, sy+fs*0.34);
    g.globalAlpha=1;
  }
}

/* --- LA FORME RÉELLE D'UNE DALLE ---
   Pour que l'Index montre la MÊME dalle que la Toile, et non un pictogramme.
   On découpe le cadre par les bissectrices, exactement comme le rendu. */
function _cellPoly(s){
  var poly=[[0,0],[W,0],[W,H],[0,H]];
  for(var k=0;k<seeds.length;k++){
    var o=seeds[k]; if(o===s)continue;
    var dx=o.x-s.x, dy=o.y-s.y;
    var d=Math.sqrt(dx*dx+dy*dy); if(d<0.001)continue;
    var nx=dx/d, ny=dy/d;
    /* la frontière se décale du côté de la dalle la plus « lourde » */
    var m=d/2 + ((s.w||0)-(o.w||0))/2;
    var px=s.x+nx*m, py=s.y+ny*m;
    var out=[],n=poly.length;
    for(var i=0;i<n;i++){
      var A=poly[i], B=poly[(i+1)%n];
      var da=(A[0]-px)*nx+(A[1]-py)*ny;
      var db=(B[0]-px)*nx+(B[1]-py)*ny;
      if(da<=0)out.push(A);
      if((da<0&&db>0)||(da>0&&db<0)){
        var t=da/(da-db);
        out.push([A[0]+(B[0]-A[0])*t, A[1]+(B[1]-A[1])*t]);
      }
    }
    poly=out; if(poly.length<3)return null;
  }
  return poly;
}
var LIVE={encre:1,terrazzo:1,touffe:1};
function frame(now){if(!g){running=false;return;}var _ss=document.getElementById('studioScreen');if(!_AP&&_ss&&_ss.classList.contains('show')){requestAnimationFrame(frame);return;}var _stg=document.getElementById('stage');if(!_AP&&_stg&&_stg.style.display==='none'){running=false;return;}   /* ⚑ v75 : `_AP` — la même image, pour un aperçu du Studio (voir Toile.apercuImage) */
  /* ⚑ v43 — une dalle partie se retire au bout de PART_DUR ; tant qu'il en reste une, la Toile tourne */
  var _parts=false;for(var _pq=seeds.length-1;_pq>=0;_pq--){if(seeds[_pq].part!=null){if(performance.now()-seeds[_pq].part>(seeds[_pq].rT0!=null?REPLI_DUR+60:((RD[theme]&&RD[theme].partDur)||PART_DUR))){var _po=seeds[_pq];if(!_semisNeuf()&&(_REPLI[theme]||_AP)){var _pv=mk(_po.x,_po.y,'gray');_pv._b=_po._b;_pv.tx=_po.tx;_pv.ty=_po.ty;_pv.px=_po.px;_pv.py=_po.py;_pv.w=_pv.wt=_pv.wFin=_po.w;_pv.wAt=0;_pv.gray=_po.gray;_pv.tone=_po.tone;_pv.shade=_po.shade;_pv.ang=_po.ang;_pv.ph=_po.ph;_pv.am=_po.am;seeds[_pq]=_pv;}else seeds.splice(_pq,1);relax();}   /* v76 : repliée, elle reste au semis constant (grise, invisible) */else _parts=true;}}
  /* une dalle qui vient de se planter GRANDIT : elle pousse ses voisines, et la
     Toile entière se réajuste autour d'elle tant que la place n'est pas faite. */
  /* ⚑ v44 (Tom, 24 sept.) — DANS LES QUATRE MONDES NEUFS, LA TOILE BOUGE COMME UN RESSORT, SUR LE TEMPS RÉEL. « Tout doux,
     logique, puis se stabilise ; là ça saute. » Le mouvement d'origine avançait de 22 % de la distance À CHAQUE IMAGE : vitesse
     maximale dès la première image (un à-coup), traîne exponentielle coupée net au seuil de 0,6 px, et une vitesse qui dépend
     de la cadence (§8 : un mouvement se calcule sur le temps). Ici : un ressort à amortissement critique (position ET poids),
     vitesse nulle au départ, pas de rebond, posé en ~0,7 s ; il ne s'arrête que quand position ET vitesse sont sous le
     dixième de pixel. Les huit anciens mondes gardent leur mouvement d'origine, au pixel. */
  if(!_AP&&(_ecZ||_ecActif)){ var _ecN=0; for(var _ei=0;_ei<seeds.length;_ei++){ var _es=seeds[_ei]; if(_es.pid!=null||_es.kind==='nuee'||_es.part!=null) continue; var _ed=!!(_ecZ&&_ecDans(_es));
      if(_ed&&!_es._ec){ _es._ec=1; _es._ecW=(_es.wt!=null?_es.wt:_es.w)||0; _es.rT0=now; _es.rW0=_es.w||0; _es.wt=_es.wFin=_repliW(); _es.wAt=0; }
      else if(!_ed&&_es._ec){ _es._ec=0; _es.rT0=now; _es.rW0=_es.w||0; _es.wt=_es.wFin=_es._ecW; _es.wAt=0; }
      if(_es._ec) _ecN++; } _ecActif=_ecN>0; }   /* v83 : l'écartement (Toile.ecarte) — voir plus bas */
  var _ressort=_semisNeuf(), _rdt=0;
  if(_ressort){ _rdt=Math.max(0,(now-(frame._t||now))/1000); if(frame._redem||_rdt>0.25)_rdt=1/60; }   /* ⚑ v61 (Tom : « la durée ne doit pas dépendre de la charge ») — le pas était plafonné à 50 ms, et toute image de plus de 100 ms comptait pour 1/60 s : sur un appareil lent le ressort perdait du temps. Il intègre maintenant le temps VRAI, en sous-pas de 1/60 s au plus (stable) ; seul un redémarrage de la boucle (ou un trou de plus de 250 ms) compte pour une image, comme avant. À 60 i/s : un sous-pas, identique. */ var _nsub=_ressort?Math.max(1,Math.ceil(_rdt*60-1e-6)):1, _h=_rdt/_nsub;   /* au redémarrage de la boucle (pause), un pas d'une image : sinon le premier pas ferait 20 % du chemin */
  frame._t=now;
  var grow=false;
  if(!_ressort){
  for(var q=0;q<seeds.length;q++){
    var sq=seeds[q];
    if(sq.rT0!=null){ var _ra=Math.min(1,(now-sq.rT0)/REPLI_DUR); var _re=_ra*_ra*(3-2*_ra); sq.w=sq.rW0+(sq.wt-sq.rW0)*_re; grow=true; if(_ra>=1&&sq.part==null){ sq.w=sq.wt; sq.rT0=null; } continue; }   /* v76 : le repli, sur le temps */
    if(sq.wt==null)sq.wt=sq.w;
    if(Math.abs(sq.wt-sq.w)>0.04){ sq.w+=(sq.wt-sq.w)*0.13; grow=true; }
    else if(sq.w!==sq.wt){ sq.w=sq.wt; grow=true; }
  }
  if(grow)relax();
  }
  var mv=false,grow=false;
  /* ⚑ v54 (Pochade, Touffe) — ces mondes avancent d'une FRACTION FIXE du chemin restant à chaque image : le mouvement est le
     plus rapide à son tout premier instant — « trop sec, trop soudain ». Le pas monte en 300 ms après une plantation, puis
     reprend son rythme exact. */
  /* ⚑ v55 (Tom : « une fois lent, une fois rapide ») — ces pas étaient une fraction fixe du chemin PAR IMAGE : chaque image un
     peu plus longue ou plus courte changeait la vitesse (mesuré sur Touffe : 1,5 · 2,9 · 1,8 · 2,4 d'une image à l'autre). Dans
     Pochade et Touffe ils se calculent sur le TEMPS écoulé — les mêmes 0,17 et 0,22 à 60 images par seconde. */
  var _kW=0.17, _kX=0.22, _redem=frame._redem; frame._redem=0; var _dtf=frame._tp?Math.min(4,Math.max(0.2,(now-frame._tp)/16.667)):1; var _rs=_rg('ressort'); if(_rs){ if(_rs[2]&&_redem) _dtf=1; _kW=1-Math.pow(_rs[0],_dtf); _kX=1-Math.pow(_rs[1],_dtf); }   /* ⚑ v61 (Tom : « ce n'est pas un changement de rythme : à 60 images par seconde, rien ne bouge ») — Tesselle, Braille, Buvard, Éclisse, Taille-douce passent à l'HORLOGE : à 16,67 ms par image ce sont exactement 0,17 et 0,22 ; sur une image lente le pas grandit, la durée validée tient. ⚑ EXCEPTION : HOULE (sillons) RESTE PAR IMAGE — elle tourne à ~30 i/s sur la page validée ; à l'horloge elle deviendrait plus rapide que ce que Tom a validé. */   /* v56 (Tom : « très très peu, à peine perceptible, mais ça fera la diff ») : 0,17 → 0,162 et 0,22 → 0,21 par image */ frame._tp=now;
  var _amo=1; if(_rg('elanPlante')&&window._tPlante){ var _ta=(now-window._tPlante)/360;   /* v56 : 300 → 360 ms */ if(_ta<1){ _ta=Math.max(0.04,_ta); _amo=_ta*_ta*(3-2*_ta); } }
  var OMX=(RD[theme]&&RD[theme].omx)||9, OMW=(RD[theme]&&RD[theme].omw)||8;   /* rad/s — position, poids (v50 : un monde peut demander un ressort plus doux) */
  for(var i=0;i<seeds.length;i++){
    var s=seeds[i];
    /* la poussée retombe : la dalle s'est fait sa place, elle se détend */
    if(s.wAt&&now>=s.wAt){s.wt=s.wFin;s.wAt=0;}
    if(_ressort){
      if(s.wt==null)s.wt=s.w; if(s.vw==null)s.vw=0; if(s.vx==null){s.vx=0;s.vy=0;}
      var ew=s.wt-s.w, ex=s.tx-s.x, ey=s.ty-s.y;
      for(var _q=0;_q<_nsub;_q++){ var _ew=s.wt-s.w; s.vw+=(OMW*OMW*_ew-2*OMW*s.vw)*_h; s.w+=s.vw*_h;
        var _ex=s.tx-s.x, _ey=s.ty-s.y; s.vx+=(OMX*OMX*_ex-2*OMX*s.vx)*_h; s.vy+=(OMX*OMX*_ey-2*OMX*s.vy)*_h; s.x+=s.vx*_h; s.y+=s.vy*_h; }
      if(Math.abs(ew)>0.02||Math.abs(s.vw)>0.05)grow=true; else {s.w=s.wt;s.vw=0;}
      if(Math.abs(ex)+Math.abs(ey)>0.1||Math.abs(s.vx)+Math.abs(s.vy)>0.5)mv=true; else {s.x=s.tx;s.y=s.ty;s.vx=0;s.vy=0;}
      continue;
    }
    if(s.rT0==null&&s.wt!==undefined&&Math.abs(s.wt-s.w)>0.04){s.w+=(s.wt-s.w)*_kW*_amo;grow=true;}
    s.x+=(s.tx-s.x)*_kX*_amo;s.y+=(s.ty-s.y)*_kX*_amo;
    if(Math.abs(s.tx-s.x)+Math.abs(s.ty-s.y)>.6)mv=true;
  }
  /* tant qu'une dalle grandit, la Toile entière se recalcule autour d'elle */
  /* la poussée se propage de proche en proche : toute la Toile réagit */
  if(grow){relax();relax();relax();mv=true;}
  if(grow)mv=true;var an=mv;for(i=0;i<seeds.length;i++)if(seeds[i].kind!=='gray'&&now-seeds[i].t0<760)an=true;if(!_AP&&!Object.keys(ptrs).length){
    /* ⚑ v46 — l'élan du glissé, puis le retour dans les bornes (ou vers le cadrage demandé) : un ressort sur le TEMPS */
    var _dv=(now-(frame._tv||0))/1000; if(!(_dv>0)||_dv>0.1) _dv=1/60; frame._tv=now;
    if(_inert){ view.ox+=_inert.vx*_dv; view.oy+=_inert.vy*_dv; var _dk=Math.exp(-_dv*4.2); _inert.vx*=_dk; _inert.vy*=_dk; an=true;
      var _bi=_borne(); if(_bi&&(Math.abs(_bi.ox-view.ox)>0.5||Math.abs(_bi.oy-view.oy)>0.5)){ var _dk2=Math.exp(-_dv*16); _inert.vx*=_dk2; _inert.vy*=_dk2; }
      if(Math.abs(_inert.vx)+Math.abs(_inert.vy)<12) _inert=null; }
    var _tg=_inert?null:(vTarget||_borne());
    if(_tg){ var _kz=1-Math.exp(-_dv*7.5), ds=_tg.s-view.s, dx=_tg.ox-view.ox, dy=_tg.oy-view.oy;
      if(Math.abs(ds)>0.0015||Math.abs(dx)>0.3||Math.abs(dy)>0.3){ view.s+=ds*_kz; view.ox+=dx*_kz; view.oy+=dy*_kz; an=true; }
      else { view.s=_tg.s; view.ox=_tg.ox; view.oy=_tg.oy; } }
  }g.setTransform(DPR,0,0,DPR,0,0);g.clearRect(0,0,W,H);var bg=_AP?window.Toile.fondToile():_fondVif(g,0,0,W*0.55,H);   /* v75 : un aperçu garde le fond de l'aperçu */   /* v66 : le fond, un seul propriétaire (_fondVif) */
  g.fillStyle=bg;g.fillRect(0,0,W,H);if(!_AP&&!isLightM()){ if(!window.__grainSeiche){ var _gc=document.createElement('canvas'); _gc.width=_gc.height=160; var _gx=_gc.getContext('2d'), _im=_gx.createImageData(160,160), _s7=7; for(var _i=0;_i<_im.data.length;_i+=4){ _s7=(_s7*1103515245+12345)&0x7fffffff; var _q=(_s7>>16)&255; _im.data[_i]=_im.data[_i+1]=_im.data[_i+2]=_q; _im.data[_i+3]=255; } _gx.putImageData(_im,0,0); window.__grainSeiche=_gx.createPattern(_gc,'repeat'); } g.save(); g.globalAlpha=0.05; g.globalCompositeOperation='overlay'; g.fillStyle=window.__grainSeiche; g.fillRect(0,0,W,H); g.restore(); }   /* v116 : le grain léger de l'encre de seiche (planche série 4) */
  g.setTransform(view.s*DPR,0,0,view.s*DPR,view.ox*DPR,view.oy*DPR);var x0=Math.max(0,(-view.ox)/view.s),y0=Math.max(0,(-view.oy)/view.s),x1=Math.min(W,(-view.ox)/view.s+W/view.s),y1=Math.min(H,(-view.oy)/view.s+H/view.s);var rr=14;g.save();g.beginPath();g.moveTo(rr,0);g.arcTo(W,0,W,H,rr);g.arcTo(W,H,0,H,rr);g.arcTo(0,H,0,0,rr);g.arcTo(0,0,W,0,rr);g.closePath();var _clipA=!!window._perfAncien;if(_clipA)g.clip();var _isG=!!_rg('grille');var _dur=_isG?850:1100;var _qa=performance.now()-_qT0,_quiv=(_qT0>0&&_qa>=0&&_qa<_dur);for(var _pi=0;_pi<seeds.length;_pi++){var _ps=seeds[_pi];if(_ps.kind==='gray'){_ps.px=_ps.x;_ps.py=_ps.y;continue;}if(_ps.ph==null){_ps.ph=_alea()*6.28;_ps.am=0.6+_alea()*0.7;}if(_quiv){var _LA=(typeof window!=='undefined'&&window._liveAmp!=null)?window._liveAmp:1;var _env=Math.exp(-_qa/(_isG?300:380));var _pa=_isG?11:7,_pay=_isG?8:5;_ps.px=_ps.x+Math.sin(_qa*0.0092+_ps.ph)*_pa*_ps.am*_env*_LA;_ps.py=_ps.y+Math.cos(_qa*0.0096+_ps.ph)*_pay*_ps.am*_env*_LA;_ps.dsx=1+Math.sin(_qa*0.0100+_ps.ph)*0.09*_env*_LA;_ps.dsy=1+Math.cos(_qa*0.0112+_ps.ph*1.2)*0.09*_env*_LA;_ps.drot=Math.sin(_qa*0.0085+_ps.ph*0.7)*0.08*_env*_LA;_ps.dw=_env*_LA;}else{_ps.px=_ps.x;_ps.py=_ps.y;_ps.dsx=1;_ps.dsy=1;_ps.drot=0;_ps.dw=0;}}if(seeds.length){_transVive=true;try{window._mondeEncore=false;RD[theme](now,x0,y0,x1,y1);}finally{_transVive=false;}}g.restore();if(!_clipA&&!_AP){g.beginPath();g.moveTo(rr,0);g.arcTo(W,0,W,H,rr);g.arcTo(W,H,0,H,rr);g.arcTo(0,H,0,0,rr);g.arcTo(0,0,W,0,rr);g.closePath();g.setTransform(DPR,0,0,DPR,0,0);g.rect(0,0,W,H);g.fillStyle=bg;g.fill('evenodd');}   /* ⚑ v38 (perf) — LE COIN ARRONDI N'EST PLUS UN clip() : on peint la matière sans découpage, puis le fond (même dégradé) autour du rectangle arrondi. Mêmes pixels (le clip antialiasé et l'aplat du complément ont la même couverture) ; WebKit faisait payer le clip à CHAQUE tracé — Touffe 205 → 51 ms par image, Gravure 56 → 33. `_perfAncien` rend l'ancien chemin (preuve). */
  if(!_AP){_voile();
  try{_labels(now);}catch(e){}}var _trv=!!(_trans&&RD[theme]&&RD[theme].transDur&&now-_trans.t0<RD[theme].transDur);   /* ⚑ v43 */
  if(_AP){_AP.encore=!!(an||now-lastChange<170||_quiv||_trv||_parts||window._mondeEncore);return;}   /* v75 : l'aperçu tient sa propre boucle */
  if(an||now-lastChange<170||_quiv||_trv||_parts||window._mondeEncore)requestAnimationFrame(frame);else running=false;}
function addP(k){
  /* ⚑ v34/v35 — monde neuf : on ne ressème pas le semis vide, il s'efface ; monde ancien : le code d'origine */
  if(_semisNeuf()) _sansGris(); else if(!seeds.length) seedGray();
  var p=(k==='nuee')?iposNuee():ipos();
  var s=mk(p.x,p.y,k||'promi');
  s.ci=cc(s);s.c=PAL[s.ci];s.t0=performance.now();
  /* Elle naît minuscule, POUSSE pour se faire une place — les voisines s'écartent —
     puis se détend jusqu'à sa taille de croisière. C'est le geste : une dalle s'insère,
     la Toile entière se réajuste autour d'elle, puis se repose. */
  s.w=-22; s.wt=(k==='nuee')?18:12;
  s.wFin=(k==='nuee')?14:3.4; s.wAt=performance.now()+380;
  seeds.push(s);
  if(k==='nuee'){lastNuee=s;}
  /* ⚑ v47 (Tom : « un frémissement, pas un séisme ») — un monde qui DÉCLARE `sansPoussee` (Esquille) : la dalle naît à sa
     taille finale. La poussée (naître à 12, repousser les voisines, retomber à 3,4) faisait deux vagues — l'aller et le
     retour — sur une plaque dont les éclats sont fixes : deux vagues de recoloration. Ici les voisines glissent UNE fois. */
  if(RD[theme]&&RD[theme].sansPoussee){ s.w=s.wFin; s.wt=s.wFin; s.wAt=0; }
  if(RD[theme]&&RD[theme].douce){ s.wt=s.wFin; s.wAt=0; }   /* v50 : Halin grandit sans pousser ses voisines */
  _transPose('arrive',s.x,s.y);
  window._vueMain=false; window._recadreDemande=true;   /* v46 : une dalle créée ramène le zoom par défaut */   /* ⚑ v43 — le moment où la dalle arrive */
  relax();tones();lastChange=s.t0;var te=document.getElementById('toileEmpty');if(te)te.style.display='none';kick();return s;}
/* ⚑ v34 — les graines grises (le semis de la Toile VIDE, §10.6) s'effacent dès qu'une vraie parole arrive. */
/* ⚑ v35 — la famille du monde courant : les quatre neufs ont le semis qui grandit, les huit anciens le semis constant */
var _NEUFS={esquille:1,bobinette:1,ritournelle:1,madrure:1,halin:1,brouillamini:1,chamade:1,volubilis:1,guingois:1,chantourne:1,mascaret:1,ramage:1}, _semisDe=null;   /* v48 : Halin est une Toile faite de ses paroles */
function _semisNeuf(){ return !!_NEUFS[theme]; }
/* ⚑ v98 (Tom, 29 sept. : « Ajoute des cellules aux huit anciens. Une parole qui n'apparaît pas est inacceptable — la décision
   v35 valait pour l'aspect, pas pour perdre des paroles. Garde leur semis constant tant qu'il y a de la place, et n'ajoute que
   lorsqu'il est plein. ») — dans un monde ancien, `plantOne` rend null quand il n'y a plus de cellule vide : la parole restait
   sans dalle. On pose alors une cellule DE PLUS, au plus grand vide (`_auVide`, tiré de la clé de la Toile), déjà posée
   (poids de croisière) : le relâchement final de `sync` la fait sa place. Au-dessous du plein, rien ne change. */
function _celluleEnPlus(k,i){ var p=_auVide(i), s=mk(p.x,p.y,k); s.ci=cc(s); s.c=PAL[s.ci]; s.t0=performance.now()-900;
  s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; seeds.push(s); window.Toile.paintOrder=null; return s; }
/* ⚑ v45 (Tom, 24 sept.) — « IL EN FAUT DE TAILLES UN PEU DIFFÉRENTES, COMME DANS LE PDF ; sinon il paraît trop régulier et on
   perd son côté esthétique. » Dans les quatre mondes neufs toutes les paroles avaient le MÊME poids (3,4) : cellules égales,
   coulées égales. Chaque parole reçoit désormais son AMPLEUR, stable (tirée de son titre et de sa personne, jamais de l'id
   ni du hasard) : un poids de −0,09 à +0,22 × l'écart moyen entre graines (réparti vers le haut : quelques
   grandes coulées, aucune écrasée — ±0,3 donnait des coulées minuscules et des étiquettes qui se chevauchent). Le toucher,
   les étiquettes, la dalle d'une fiche lisent la même règle pondérée : ils suivent sans rien changer. Une Nuée garde sa
   base plus large (14). Les huit anciens mondes ne sont pas touchés. */
function _ampleur(s){ var t='', h=2166136261, j;
  if(s.pid!=null){ try{ for(j=0;j<promises.length;j++){ if(promises[j].id===s.pid){ t=String(promises[j].title||'')+'|'+String(promises[j].who||''); break; } } }catch(_){ } if(!t) t='p'+s.pid; }
  else if(s.nuee) t='n'+s.nuee; else return null;
  for(j=0;j<t.length;j++){ h^=t.charCodeAt(j); h=Math.imul(h,16777619)>>>0; }
  h^=h>>>15; h=Math.imul(h,2246822507)>>>0; h^=h>>>13;
  var u=(h%10007)/10006; return -0.09+0.31*u*u; }   /* de −0,09 à +0,22 × l'écart moyen : plus de grandes que de petites, aucune écrasée */
function _amplifie(){ if(!_semisNeuf()) return; var a=avg();
  for(var i=0;i<seeds.length;i++){ var s=seeds[i]; if(s.part!=null) continue; var d=_ampleur(s); if(d==null) continue;
    var base=(s.kind==='nuee')?14:3.4, f=base+d*a; s.wFin=f; if(!s.wAt){ s.wt=f; if(s._amp==null) s.w=f; } s._amp=1; } }
function _sansGris(){ var n=seeds.length; seeds=seeds.filter(function(s){ return s.kind!=='gray'; }); if(seeds.length!==n){ window.Toile.paintOrder=null; } }
/* ⚑ v34 — le plus grand vide, tiré de la clé de la Toile et du rang : 24 candidats, on garde le plus loin des graines. */
function _auVide(i){ var cle=0; try{ cle=(window.Toile&&window.Toile.cle)?window.Toile.cle():0; }catch(_){ }
  var sd=((cle^Math.imul(i+1,2654435761))>>>0)||1, r=function(){ sd=(Math.imul(sd,1103515245)+12345)&0x7fffffff; return sd/0x7fffffff; };
  var best=null, bd=-1;
  for(var c=0;c<24;c++){ var x=W*(0.1+0.8*r()), y=H*(0.1+0.8*r()), d=1e18;
    for(var k=0;k<seeds.length;k++){ var dx=x-seeds[k].x, dy=y-seeds[k].y, dd=dx*dx+dy*dy; if(dd<d) d=dd; }
    if(d>bd){ bd=d; best={x:x,y:y}; } }
  return best||{x:W/2,y:H/2}; }
var nueeCells={};window.Toile={addPromi:function(id){_aleaRepart('plante|'+id+'|'+seeds.length);/* ⚑ v34/v35 — dans un monde neuf une plantation AJOUTE sa cellule ; dans un ancien elle colore une cellule du semis */var s=null;if(_semisNeuf()){_sansGris();s=addP('promi');}else{s=window.Toile.plantOne();if(!s)s=addP('promi');}if(s&&id!=null){s.pid=id;_dalleFigee(true);}if(s&&_semisNeuf()){_amplifie();relax();}return s;},
  /* la dalle sous le doigt : même métrique que le rendu, au pixel près */
  hit:function(cx,cy){
    if(!seeds.length)return null;
    var lx=(cx-view.ox)/view.s, ly=(cy-view.oy)/view.s;
    /* ⚑ v34 — la Toile n'a plus de case vide dès sa première parole : HORS de son rectangle (vue reculée), c'est le vide —
       le double toucher y recadre (Q212), et un toucher n'y ouvre aucune dalle. */
    if(lx<0||ly<0||lx>W||ly>H) return null;
    /* ⚑ v32 — un monde libre neuf se touche sur la dalle qu'il a PEINTE ; hors d'elle, la règle de la cellule reprend. */
    if(_MN&&_MNLIB[theme]){ try{ var _tt=_MN.toucher(theme,lx,ly); if(_tt&&_tt.kind!=='gray') return {pid:(_tt.pid!=null?_tt.pid:null), kind:_tt.kind, nuee:_tt.nuee||null}; }catch(_e){}
      if(RD[theme]&&RD[theme].toucheStrict) return null; }   /* v62 : Brouillamini se touche sur le contour peint, jamais sur la cellule */
    var bd=1e18,bs=null;
    for(var k=0;k<seeds.length;k++){
      var dx=lx-seeds[k].x, dy=ly-seeds[k].y;
      var d=Math.sqrt(dx*dx+dy*dy)-seeds[k].w;
      if(d<bd){bd=d;bs=seeds[k];}
    }
    if(!bs||bs.kind==='gray')return null;
    return {pid:(bs.pid!=null?bs.pid:null), kind:bs.kind, nuee:bs.nuee||null};
  },
  /* remet la Toile en accord avec les Promi réels : 1 Promi = 1 dalle */
  sync:function(list){
    _aleaRepart('sync|'+(list||[]).join(','));   /* ⚑ assainissement : le semis se tire de la clé de la Toile et de ce qu'on synchronise */
    /* ⚑ v35 (Tom, 23 sept.) — LE SEMIS QUI GRANDIT EST UNE EXCEPTION DES QUATRE MONDES NEUFS. Pochade, Tesselle, Touffe,
       Braille, Buvard, Houle, Taille-douce et Éclisse gardent le semis CONSTANT d'origine et leur aspect d'origine ; seuls
       Esquille, Bobinette, Ritournelle et Madrure ont une Toile faite de ses seules promesses. Incohérence assumée (voir
       CLAUDE.md) : les anciens mondes ont été dessinés, réglés et validés sur le semis constant. Le code d'origine suit,
       tel quel ; un semis venu de l'autre famille est d'abord ressemé. */
    /* ⚑ v46 — une dalle CRÉÉE ou SUPPRIMÉE ramène le zoom par défaut (les autres synchronisations — changer de monde,
       rafraîchir — le laissent où la main l'a mis) */
    try{ var _avP={}, _nA=0, _chg=false; for(var _zi=0;_zi<seeds.length;_zi++){ var _zs=seeds[_zi]; if(_zs.kind!=='gray'&&_zs.pid!=null&&_zs.part==null){ _avP[_zs.pid]=1; _nA++; } }
      var _nL=0; (list||[]).forEach(function(id){ _nL++; if(!_avP[id]) _chg=true; }); if(_nL!==_nA) _chg=true;
      if(_chg){ window._vueMain=false; window._recadreDemande=true; _inert=null; if(_qT0 && performance.now()-_qT0<150) _qT0=0; window._tMouv=performance.now(); } }catch(_z){}   /* v60 : une parole qui part ou arrive prend la main sur le frémissement du même geste, et son moment est protégé */
    _semisDe=_semisNeuf()?'neuf':'ancien';
    if(_semisDe==='ancien'){
      if(seeds.length && !seeds.some(function(s){ return s.kind==='gray'; })){ seeds=[]; }
    if(!seeds.length)seedGray();
      /* Les dalles REDEVIENNENT des cellules vides — on ne les SUPPRIME pas.
         Avant, sync() les arrachait du tableau : quand l'onboarding laissait une
         Toile pleine de couleur (donc zéro cellule vide), il ne restait qu'une
         poignée de cellules. La Toile paraissait alors monstrueusement zoomée. */
      /* ⚑ v55 (Tom : « Pochade et Touffe — adoucis le départ, 24,8 et 47,4 d'écart, c'est brutal ») — chaque synchronisation
         remettait TOUTES les dalles en cellules grises puis replantait chaque parole sur une cellule grise TIRÉE AU HASARD : au
         retrait d'une seule, toutes les autres sautaient ailleurs, et les grises prenaient une allure neuve. Sur une Toile déjà
         peuplée : les dalles qui restent GARDENT leur place et leur allure ; celle qui part redevient une cellule grise AU MÊME
         ENDROIT, de la même forme, sa couleur s'éteignant vers son gris ; seules les paroles nouvelles se plantent. */
      var _garde={}, _gardeN={}, _tn=performance.now(), _dejaCol=false;
      for(var _li=0;_li<list.length;_li++) _garde[list[_li]]=1;
      try{ if(typeof NUE!=='undefined'){ for(var _nk0 in NUE){ if(_nk0!=='soi') _gardeN[_nk0]=1; } } }catch(_e){}
      for(var i=0;i<seeds.length;i++){ if(seeds[i].kind!=='gray'){ _dejaCol=true; break; } }
      var _restent={}, _restentN={};
      for(var i=0;i<seeds.length;i++){
        var s=seeds[i];
        if(s.kind!=='gray'){
          if(_dejaCol && s.kind!=='nuee' && s.pid!=null && _garde[s.pid] && !_restent[s.pid]){ _restent[s.pid]=s; continue; }
          if(_dejaCol && s.kind==='nuee' && s.nuee && _gardeN[s.nuee] && !_restentN[s.nuee]){ _restentN[s.nuee]=s; continue; }
          if(s.part!=null) continue;   /* v76 : une dalle qui se replie finit de se replier */
          /* ⚑ v76 (Tom) — « un trou noir à la place de la dalle supprimée, pas un recouvrement par les dalles autour qui se
             rapprochent ». Dans ces six mondes la dalle qui part RESTE une dalle, de sa couleur, pendant que son poids descend
             et que ses voisines la recouvrent (le départ `part` de v43) ; recouverte, elle redevient une cellule grise REPLIÉE,
             gardée au semis (densité constante, v35), qu'une plantation reprend d'abord et fait regrandir — l'inverse exact. */
          if(_REPLI[theme]&&_dejaCol&&s.kind!=='nuee'){ s.partPid=s.pid; s.pid=null; _replie(s,_tn); continue; }
          var v=mk(s.x,s.y,'gray');
          v.px=s.px; v.py=s.py; v.tx=s.tx; v.ty=s.ty; v.gray=s.gray; v.gc=s.gc; v.tone=s.tone; v.shade=s.shade; v.ang=s.ang; v.ph=s.ph; v.am=s.am;
          if(_dejaCol){ try{ v.cOut=cOf(s,_tn); v.tOut=_tn; }catch(_c){} }
          v.w=s.w; v.wt=0; v.wFin=0; v.wAt=0;
          /* ⚑ v76 (Tom) — « un trou noir à la place de la dalle supprimée, pas un recouvrement par les dalles autour qui se
             rapprochent ». Dans ces six mondes, la dalle qui part se REPLIE : sa couleur s'éteint (cOut) pendant que son poids
             descend, et ses voisines la recouvrent. La cellule reste au semis, repliée : une plantation la reprend d'abord
             (plantOne), et elle regrandit en poussant — l'inverse exact. La densité du semis ne bouge pas (v35). */
          seeds[i]=v;
        }
      }
      nueeCells={};
      /* chaque Promi reprend sa place parmi les cellules vides : le nombre de
         cellules ne bouge pas, la Toile garde ses proportions */
      for(var j=0;j<list.length;j++){
        if(_restent[list[j]]) continue;
        var np=window.Toile.plantOne(true);
        if(!np) np=_celluleEnPlus('promi',j);   /* ⚑ v98 (Tom) — « une parole qui n'apparaît pas est inacceptable » : semis plein, on ajoute */
        if(np)np.pid=list[j];
      }
      /* ⚑ UNE NUÉE A SA DALLE (Tom, 13 sept. 2026) — sync l'effaçait à chaque plantation : une Nuée était invisible sur la
         Toile, même portant neuf paroles. Une dalle par Nuée nommée (« soi » n'est pas une Nuée), à la taille de dalle de Nuée
         que le moteur donne déjà (`addP('nuee')` : wFin 14). */
      try{ if(typeof NUE!=='undefined'){ for(var _nk in NUE){ if(_nk==='soi')continue;
        if(_restentN[_nk]){ nueeCells[_nk]=_restentN[_nk]; lastNuee=_restentN[_nk]; continue; }
        var _ns=window.Toile.plantOne(true); if(!_ns)_ns=_celluleEnPlus('nuee',list.length+_nk.length);
        _ns.kind='nuee'; _ns.nuee=_nk; _ns.w=14; _ns.wt=14; _ns.wFin=14; nueeCells[_nk]=_ns; lastNuee=_ns; } } }catch(_e){}
      relax();tones();lastChange=performance.now();
      autoView();
      kick();
      return;
    }
    var nk=[]; try{ if(typeof NUE!=='undefined'){ for(var _nk in NUE){ if(_nk!=='soi') nk.push(_nk); } } }catch(_e){}
    if(!list.length && !nk.length){ seeds=[]; seedGray(); nueeCells={}; relax();tones();lastChange=performance.now();autoView();kick(); return; }
    var avant={}; for(var i=0;i<seeds.length;i++){ var s0=seeds[i]; if(s0.kind==='gray') continue;
      if(s0.pid!=null) avant['p'+s0.pid]=s0; else if(s0.kind==='nuee'&&s0.nuee) avant['n'+s0.nuee]=s0; }
    var now=performance.now(); seeds=[]; nueeCells={};
    for(var j=0;j<list.length;j++){ var s=avant['p'+list[j]];
      if(!s){ var p=_auVide(j); s=mk(p.x,p.y,'promi'); s.ci=cc(s); s.c=PAL[s.ci]; s.t0=now-900; s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; }
      s.pid=list[j]; seeds.push(s); }
    for(var q=0;q<nk.length;q++){ var t=avant['n'+nk[q]];
      if(!t){ var p2=_auVide(list.length+q); t=mk(p2.x,p2.y,'nuee'); t.ci=cc(t); t.c=PAL[t.ci]; t.t0=now-900; }
      t.kind='nuee'; t.nuee=nk[q]; t.w=14; t.wt=14; t.wFin=14; t.wAt=0; seeds.push(t); nueeCells[nk[q]]=t; lastNuee=t; }
    /* ⚑ v43 — LE DÉPART D'UNE DALLE. Dans un monde qui anime ses transitions (`transDur`), la dalle qui part ne disparaît
       pas d'une image à l'autre : elle reste le temps de se retirer (`part` = l'heure du départ, sans pid — plus rien ne la
       touche ni ne l'étiquette), ses voisines prennent sa place, et le moteur la retire au bout de PART_DUR. Une ou deux
       dalles seulement : au-delà, c'est une resynchronisation (changement de famille, réinitialisation), pas un départ. */
    try{ if(RD[theme]&&RD[theme].transDur){ var _pris={}; for(var _k2=0;_k2<seeds.length;_k2++) _pris[seeds[_k2].pid!=null?'p'+seeds[_k2].pid:'n'+seeds[_k2].nuee]=1;
      var _dep=[]; for(var _ak in avant){ if(!_pris[_ak]&&!avant[_ak].part) _dep.push(avant[_ak]); }
      if(_dep.length&&_dep.length<=2){ for(var _d=0;_d<_dep.length;_d++){ var _g=_dep[_d]; _g.part=now; _g.partPid=_g.pid; _g.partNuee=_g.nuee; _g.pid=null; _g.nuee=null; _g.wt=_g.w-30; _g.wFin=_g.wt; _g.wAt=0; if(RD[theme].sansPoussee) _g.w=_g.wt; seeds.push(_g); }
        _transPose('depart',_dep[0].x,_dep[0].y); } } }catch(_e){}
    _amplifie();   /* v45 */
    relax();relax();relax();tones();lastChange=performance.now();
    autoView();
    kick();
  },
  /* --- completion : on colore les cellules DEJA en place, dans un ordre fixe --- */
  paintOrder:null,
  /* la forme EXACTE de la dalle d'un Promi, ramenée dans un carré de côté `box`
     (l'Index montre ainsi la même dalle que la Toile, pas un pictogramme) */
  dalleAbs:function(pid){
    var s=null;for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){s=seeds[i];break;}}
    if(!s)return null;var poly=null;try{poly=_cellPoly(s);}catch(e){}
    if(!poly||poly.length<3)return null;
    var st=null;try{st=STRUCT[state.structure];}catch(e){}
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var j=0;j<poly.length;j++){if(poly[j][0]<minx)minx=poly[j][0];if(poly[j][0]>maxx)maxx=poly[j][0];if(poly[j][1]<miny)miny=poly[j][1];if(poly[j][1]>maxy)maxy=poly[j][1];}
    return {poly:poly,minx:minx,miny:miny,w:maxx-minx,h:maxy-miny,round:(st&&st.round)||2,stroke:(st&&st.stroke)||'none',sw:(st&&st.sw)||1};
  },
  roundPathOf:function(pts,r){try{return roundPath(pts,r);}catch(e){return null;}},
  shapeOf:function(pid,box){
    box=box||30;
    var s=null;
    for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){s=seeds[i];break;}}
    if(!s)return null;
    var poly=null; try{poly=_cellPoly(s);}catch(e){}
    if(!poly||poly.length<3)return null;
    var minx=1e9,miny=1e9,maxx=-1e9,maxy=-1e9;
    for(var j=0;j<poly.length;j++){
      if(poly[j][0]<minx)minx=poly[j][0]; if(poly[j][0]>maxx)maxx=poly[j][0];
      if(poly[j][1]<miny)miny=poly[j][1]; if(poly[j][1]>maxy)maxy=poly[j][1];
    }
    var w=maxx-minx, h=maxy-miny; if(w<=0||h<=0)return null;
    var pad=box*0.12, inner=box-pad*2;
    var k=Math.min(inner/w, inner/h);
    var ox=pad+(inner-w*k)/2, oy=pad+(inner-h*k)/2;
    var d='';
    for(var q=0;q<poly.length;q++){
      var X=(ox+(poly[q][0]-minx)*k).toFixed(1), Y=(oy+(poly[q][1]-miny)*k).toFixed(1);
      d+=(q?'L':'M')+X+' '+Y+' ';
    }
    return d+'Z';
  },
  reserved:[],
  /* L'onboarding plante de VRAIES dalles : elles s'insèrent entre les autres,
     qui s'écartent. Le même geste que dans l'app — plus aucun fondu. */
  plantOne:function(dejaPosee){
    var gris=[];
    for(var i=0;i<seeds.length;i++)if(seeds[i].kind==='gray')gris.push(seeds[i]);
    if(!gris.length)return null;
    /* le champ clair : ni sous la barre du haut, ni sous le dock. Une dalle plantée
       là serait illisible — on préfère toujours une cellule dégagée. */
    var libres=gris.filter(function(s){return s.y>HAUT_LIBRE && s.y<H-BAS_LIBRE;});
    /* v76 — une cellule REPLIÉE (une dalle partie) est reprise d'abord : la nouvelle dalle regrandit d'où l'autre s'est retirée */
    if(_REPLI[theme]){ var _rw=_repliW()/2, _rp=gris.filter(function(s){return (s.wt!=null?s.wt:s.w)<_rw;}); if(_rp.length) libres=_rp; }
    var pool=libres.length?libres:gris;
    var cible=pool[(_alea()*pool.length)|0];
    var a=avg();
    var jx=(_alea()-.5)*a*0.5, jy=(_alea()-.5)*a*0.5;
    var s=mk(Math.max(8,Math.min(W-8,cible.x+jx)), Math.max(8,Math.min(H-8,cible.y+jy)), 'promi');
    s.ci=cc(s);s.c=PAL[s.ci];
    s.t0=performance.now();      /* la dalle se REMPLIT (gris -> couleur) en prenant sa place */
    if(dejaPosee){ s.w=3.4; s.wt=3.4; s.wFin=3.4; s.wAt=0; s.t0=performance.now()-900; }
    else { s.w=-22; s.wt=12; s.wFin=3.4; s.wAt=performance.now()+380; if(RD[theme]&&RD[theme].douce){ s.wt=3.4; s.wAt=0; } }
    var k=seeds.indexOf(cible);      /* la cellule grise qui l'accueille s'efface : densite constante */
    /* ⚑ v54 (Tom : « Pochade et Touffe — le début du mouvement est trop sec, trop soudain ») — mesuré : à la première image,
       écart 6,7 (Pochade) et 28,2 (Touffe), puis ~1 et ~4. La cellule grise était retirée et la dalle neuve ajoutée EN FIN DE
       LISTE, ailleurs (décalée au hasard), minuscule (poids −22), avec un autre gris : trois ruptures à l'image zéro — et dans
       Touffe le rang changé redessinait d'autres fleurs. Dans ces deux mondes, la dalle neuve PREND LA PLACE de la cellule
       grise : même rang, même lieu, même poids, même allure ; elle ne fait qu'ENSUITE son mouvement (sa place décalée, sa
       poussée, sa couleur). Les autres mondes ne changent pas. */
    if(k>=0&&_rg('elanPlante')&&!dejaPosee){
      window._tPlante=performance.now();
      s.tx=s.x; s.ty=s.y; s.x=cible.x; s.y=cible.y; s.px=cible.px; s.py=cible.py;
      s.gray=cible.gray; s.gc=cible.gc; s.tone=cible.tone; s.shade=cible.shade; s.ang=cible.ang; s.ph=cible.ph; s.am=cible.am;
      s.w=cible.w||0; seeds[k]=s;
    } else {
      seeds.push(s);
      if(k>=0)seeds.splice(k,1);
    }
    window.Toile.paintOrder=null;
    relax();tones();lastChange=performance.now();
    window._vueMain=false; window._recadreDemande=true;   /* v46 : une dalle créée ramène le zoom par défaut */
    autoView();      /* la vue recule d'un cran */
    kick();
    return s;
  },
  unplantOne:function(){
    for(var i=seeds.length-1;i>=0;i--){
      if(seeds[i].kind==='promi'&&seeds[i].pid==null){
        var s=seeds[i];
        var g=mk(s.x,s.y,'gray'); g.w=-9; g.wt=0;
        seeds.splice(i,1,g);
        window.Toile.paintOrder=null;
        relax();tones();lastChange=performance.now();kick();
        return true;
      }
    }
    return false;
  },
  colored:function(){var n=0;for(var i=0;i<seeds.length;i++)if(seeds[i].kind!=='gray')n++;return n;},
  scale:function(){return view.s;},       /* le zoom courant : sert à distinguer un pincement d'un appui long */
  fingers:function(){return Object.keys(ptrs).length;},
  /* la Toile s'eclaircit sous les blocs de texte : a reappliquer des qu'elle bouge */
  applyReserve:function(){
    var R=window.Toile.reserved; if(!R||!R.length||!seeds.length)return;
    var lite=0,bl=-1;
    for(var p=0;p<PAL.length;p++){
      var c=PAL[p], L=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
      if(L>bl){bl=L;lite=p;}
    }
    for(var z=0;z<R.length;z++){
      var rz=R[z];
      for(var py=rz.y-4;py<=rz.y+rz.h+4;py+=6){
        for(var px=rz.x-4;px<=rz.x+rz.w+4;px+=6){
          var bd=1e18,bs=null;
          for(var m=0;m<seeds.length;m++){
            var sm=seeds[m];
            var dd=Math.sqrt((px-sm.x)*(px-sm.x)+(py-sm.y)*(py-sm.y))-sm.w;
            if(dd<bd){bd=dd;bs=sm;}
          }
          if(bs&&bs.kind!=='gray'&&bs.kind!=='nuee'&&bs.pid==null&&bs.ci!==lite){bs.ci=lite;bs.c=PAL[lite];bs.gc=null;}/* ⚑ Q213 : une dalle reliée à un Promi garde SA couleur — la réserve de l'onboarding n'est jamais vidée après lui, elle repeignait en lilas toute dalle passée sous ses anciens textes */
        }
      }
    }
  },
  /* NB : window.Toile.repaint est déjà pris par le Studio — d'où un autre nom */
  redraw:function(){lastChange=performance.now();kick();},
  /* la Toile elle-même : Partager s'en sert pour poster CE QU'ON VOIT.
     Ces deux méthodes étaient appelées par shareToile() mais n'existaient pas :
     le poster retombait sur un vieux rendu mosaïque figé, en « pixel ». */
  canvas:function(){return host;},
  isLight:function(){return isLightM();},
  /* la Toile telle qu'elle est, à l'instant : c'est elle qu'on partage */
  canvas:function(){return host;},
  isLight:function(){return isLightM();},
  /* la couleur EXACTE qu'a la dalle en ce moment sur la Toile */
  colorOf:function(pid){
    for(var i=0;i<seeds.length;i++){
      var s=seeds[i];
      if(s.pid===pid&&s.kind!=='gray'){
        var c=cOf(s,performance.now());
        return 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';
      }
    }
    return null;
  },
  reserve:function(rects){window.Toile.reserved=rects||[];},
  ecarte:function(rects){ _ecZ=(rects&&rects.length)?rects:null; lastChange=performance.now(); kick(); },
  cells:function(){if(!seeds.length)seedGray();return seeds.length;},
  paint:function(n){
    if(!seeds.length)seedGray();
    var T=window.Toile;
    if(!T.paintOrder||T.paintOrder.length!==seeds.length){
      var o=[];for(var i=0;i<seeds.length;i++)o.push(i);
      for(var j=o.length-1;j>0;j--){var r=(_alea()*(j+1))|0;var t=o[j];o[j]=o[r];o[r]=t;}
      T.paintOrder=o;
    }
    /* la teinte la plus CLAIRE de la palette : c'est elle qui passe sous le texte */
    function _lightest(){
      var best=0,bl=-1;
      for(var p=0;p<PAL.length;p++){
        var c=PAL[p];
        var L=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
        if(L>bl){bl=L;best=p;}
      }
      return best;
    }
    var ord=T.paintOrder,now=performance.now(),changed=0;
    n=Math.max(0,Math.min(ord.length,n|0));
    for(var q=0;q<ord.length;q++){
      var s=seeds[ord[q]];if(!s)continue;
      if(q<n){                                   /* doit etre coloree */
        if(s.kind==='gray'){
          s.kind='promi';s.ci=cc(s);s.c=PAL[s.ci];s.gc=null;
          s.t0=now-900;                 /* sa couleur est là tout de suite : aucun fondu */
          s.w=-9; s.wt=3.4;             /* elle arrive minuscule, puis prend sa place */
          changed++;
        }
      }else{                                     /* doit revenir au gris */
        if(s.kind==='promi'){s.kind='gray';s.gray=grays()[(_alea()*5)|0];s.ci=null;s.t0=0;s.gc=null;s.w=0;s.wt=0;changed++;}
      }
    }
    /* la Toile RÉAGIT à l'arrivée des dalles puis se stabilise — exactement comme dans l'app */
    /* toute la Toile se réajuste, puis se stabilise — comme dans l'app */
    if(changed){relax();relax();relax();}
    /* aucune dalle bleue ne doit recouvrir les accents bleus du texte (le « i » de Promi,
       le libellé « Promi… ») : leur couleur, elle, ne s'adapte pas. On échantillonne
       vraiment la zone — le centre d'une grande dalle peut être loin tout en la couvrant. */
    /* LA TOILE FAIT DE LA PLACE AU TEXTE : toute dalle qui passe sous un bloc de
       texte prend la teinte la plus claire de la palette. L'encre sombre est alors
       lisible partout, sans jamais rien recalculer. On échantillonne vraiment la
       zone : le centre d'une grande dalle peut être loin d'elle tout en la couvrant. */
    var R=window.Toile.reserved;
    if(R&&R.length){
      var lite=_lightest();
      for(var z=0;z<R.length;z++){
        var rz=R[z];
        for(var py=rz.y-4;py<=rz.y+rz.h+4;py+=5){
          for(var px=rz.x-4;px<=rz.x+rz.w+4;px+=5){
            var bd2=1e18,bs=null;
            for(var m=0;m<seeds.length;m++){
              var sm=seeds[m];
              var dd=Math.sqrt((px-sm.x)*(px-sm.x)+(py-sm.y)*(py-sm.y))-sm.w;
              if(dd<bd2){bd2=dd;bs=sm;}
            }
            if(bs&&bs.kind!=='gray'&&bs.kind!=='nuee'&&bs.pid==null&&bs.ci!==lite){bs.ci=lite;bs.c=PAL[lite];bs.gc=null;}/* ⚑ Q213 : une dalle reliée à un Promi garde SA couleur — la réserve de l'onboarding n'est jamais vidée après lui, elle repeignait en lilas toute dalle passée sous ses anciens textes */
          }
        }
      }
    }
    tones();lastChange=now;kick();
  },
  removePromi:function(){for(var i=seeds.length-1;i>=0;i--){if(seeds[i].kind==='promi'){seeds.splice(i,1);relax();tones();lastChange=performance.now();kick();break;}}},cols:function(){return curPAL();},addNuee:function(key){if(key&&nueeCells[key]&&seeds.indexOf(nueeCells[key])>=0)return nueeCells[key];/* ⚑ 14 sept. : une Nuée qui a déjà sa dalle n'en reçoit pas une seconde */var s=addP('nuee');if(key){nueeCells[key]=s;s.nuee=key;}if(key)nueeCells[key]=s;return s;},addMember:function(key,id){/* ⚑ 14 sept. (Tom) : la dalle d'un Promi planté dans une Nuée est RELIÉE à ce Promi — sans `pid` elle n'avait ni fiche au doigt, ni couleur figée, ni boîte pour sa fiche */var an=(key&&nueeCells[key])?nueeCells[key]:lastNuee;if(!an){var s0=addP('promi');if(s0&&id!=null){s0.pid=id;_dalleFigee(true);}return s0;}var a=_alea()*6.28,r=avg()*.9;var s=mk(an.x+Math.cos(a)*r,an.y+Math.sin(a)*r,'promi');s.ci=cc(s);s.c=PAL[s.ci];s.t0=performance.now();seeds.push(s);_transPose('arrive',s.x,s.y);if(id!=null)s.pid=id;relax();tones();if(id!=null)_dalleFigee(true);lastChange=s.t0;_vueDefaut();kick();return s;},setTheme:function(t){if(!TH[t])return;var _famAv=_semisNeuf();theme=t;/* ⚑ v35 — changer de FAMILLE de monde ressème la Toile, avec les mêmes promesses */if(_famAv!==_semisNeuf()&&_semisDe){try{var _ids=[];for(var _qi=0;_qi<seeds.length;_qi++){if(seeds[_qi].pid!=null&&seeds[_qi].kind!=='gray')_ids.push(seeds[_qi].pid);}seeds=[];/* ⚑ assainissement : le ressemis part de zéro, depuis la clé — il ne réutilise plus les places de l'autre famille (qui venaient d'un démarrage dépendant du minutage) */window.Toile.sync(_ids);}catch(_e){}}/* le fond des pages suit le design choisi */try{setTimeout(function(){(window._apresMouvement||function(f){f();})(function(){if(window.auTrame)window.auTrame();if(window.shTrame)window.shTrame();if(window.csDalles)window.csDalles();if(window.shFond)window.shFond();if(window.ixTrame)window.ixTrame();if(window.fdRefresh)window.fdRefresh();if(window.stRefresh)window.stRefresh();if(window.dpRefresh)window.dpRefresh();if(window.esRefresh)window.esRefresh();/* les miniatures de l'Index suivent le design choisi */if(window.peintMinis)window.peintMinis(document.getElementById('indexList'));});},60);}catch(e){}   /* ⚑ v75 : ~400 ms de dalles pour des écrans cachés — ils attendent que le mouvement se pose (l'arrivée de l'aperçu du Studio en est un) */try{localStorage.setItem('promi_monde',t);}catch(e){}   /* le MONDE, pas le mode clair/sombre : deux choses distinctes */seeds.forEach(function(s){s.gray=grays()[(_alea()*5)|0];s.gc=null;});lastChange=performance.now();kick();},getTheme:function(){return theme;},setPalette:function(k){if(PALS[k]){palKey=k;hueShift=0;_palLit=null;lastChange=performance.now();try{window.onPaletteChange&&window.onPaletteChange();}catch(e){}kick();}},setHue:function(d){hueShift=+d||0;_palLit=null;lastChange=performance.now();try{window.onPaletteChange&&window.onPaletteChange();}catch(e){}kick();},getPalette:function(){return palKey;},getHue:function(){return hueShift;},   /* ⚑ 20 sept. : le geste de couleur a besoin de LIRE la teinte, pas seulement de l'écrire */palettes:function(){return PALS;},count:function(){return seeds.filter(function(s){return s.kind!=='gray'&&s.part==null;}).length;}};
window.Toile.repaintWorld=function(pcv,w){
  var c=pcv&&pcv.__c; if(!c||!TH[w])return;
  /* ⚑ v69 (Tom, 27 sept.) — ON RESSÈME QUAND ON CHANGE DE FAMILLE. Garder les graines est le geste doux voulu (v25) — mais entre deux
     familles de semis ce n'est plus la même Toile : un monde neuf atteint depuis Encre héritait de la grille de 72 cellules, et
     l'aperçu clairsemé (v55) ne paraissait QUE si le Studio s'ouvrait sur lui. Mesuré : 72 graines sur les vingt mondes du rail. */
  var _AC=window._apercuClair||{};
  if(_apFam(w)!==_apFam(c.th)&&pcv.__vif){ var _F=pcv.__fam||(pcv.__fam={}); _F[_apFam(c.th)]=c; var _gd=_F[_apFam(w)]; if(_gd&&_gd.pw===c.pw&&_gd.ph===c.ph){ pcv.__c=c=_gd; } }   /* v75 : on retrouve le semis de cette famille */
  if(_apFam(w)!==_apFam(c.th)&&window.Toile.preview){ var _av=window._shAllColored; window._shAllColored=true; try{ window.Toile.preview(pcv,w,c.pw,c.ph); }finally{ window._shAllColored=_av; } return; }
  c.th=w;
  /* les gris du monde suivent le THÈME de l'app : en mode clair ce sont les crèmes.
     On prenait la palette sombre du monde quoi qu'il arrive — d'où un Pixel sombre
     alors que le sélecteur affichait Clair. */
  var pal=isLightM()?GLIGHT:TH[w].g;
  c.seeds.forEach(function(s){s.gray=pal[(_alea()*5)|0];s.gc=null;});
  if(pcv.__vif&&c.vif){ try{ window.Toile.apercuImage(pcv); }catch(_){} return; }   /* v75 : l'aperçu vivant passe au monde suivant dès cette image — son arrivée démarre tout de suite */
  window.Toile.repaint(pcv);
};
/* ⚑ v75 (Tom, 27 sept. 2026) — LES APERÇUS DU STUDIO S'ANIMENT. « Une dalle s'ajoute, une dalle se retire, en boucle, au même
   rythme » que `celebration-mondes.html` : arrivée à 0, départ à 2,4 s, nouvelle arrivée à 4,4 s. Rien d'autre ne change — la vue
   reste entière (1:1), le semis est celui de l'aperçu, le fond celui de l'aperçu.
   ⚑ UN SEUL MOTEUR. L'aperçu n'a pas de copie du mouvement : `Toile.apercuImage` échange l'état du moteur (les graines, la vue, la
   transition, l'horloge du ressort — le patron de `preview`, `repaint`, `renderTo`), fait passer `frame()` UNE image en mode aperçu
   (`_AP`), puis rend l'état de la Toile tel quel. Ressort, poussée, arrivée, départ, `env.trans` : le code de la Toile, au pixel.
   ⚑ LE CYCLE EST PÉRIODIQUE. Une dalle neuve (monde à semis qui grandit) ou une cellule qui se colore (monde à semis constant) arrive
   toujours au même endroit, de la même couleur ; après son départ, les voisines reviennent à leur place (ressort du moteur), et
   chaque arrivée repart de la composition d'origine, exacte. Même Toile à chaque tour : mêmes dalles, même composition. */
var _AP=null, _apVu=null;   /* _apVu : le dernier aperçu vivant (et l'heure de sa dernière image) */
function _apLit(){ return {g:g,W:W,H:H,DPR:DPR,seeds:seeds,theme:theme,view:view,_trans:_trans,_finC:_finC,_finPrev:_finPrev,lastChange:lastChange,_qT0:_qT0,_inert:_inert,vTarget:vTarget,lastNuee:lastNuee,nueeCells:nueeCells,
  ft:frame._t,ftp:frame._tp,fr:frame._redem,ftv:frame._tv,tP:window._tPlante,tM:window._tMouv,me:window._mondeEncore,vm:window._vueMain,rd:window._recadreDemande}; }
function _apPose(e){ g=e.g;W=e.W;H=e.H;DPR=e.DPR;seeds=e.seeds;theme=e.theme;view=e.view;_trans=e._trans;_finC=e._finC;_finPrev=e._finPrev;lastChange=e.lastChange;_qT0=e._qT0;_inert=e._inert;vTarget=e.vTarget;lastNuee=e.lastNuee;nueeCells=e.nueeCells;
  frame._t=e.ft;frame._tp=e.ftp;frame._redem=e.fr;frame._tv=e.ftv;window._tPlante=e.tP;window._tMouv=e.tM;window._mondeEncore=e.me;window._vueMain=e.vm;window._recadreDemande=e.rd; }
/* ⚑ v76 (Tom, 27 sept.) — « Il faut aléatoirement plusieurs ajouts et plusieurs suppressions, sinon la boucle est lassante ; et le
   mouvement plus lent et plus espacé. » L'aperçu ne rejoue plus un aller-retour : chaque dalle de la composition a son EMPLACEMENT
   (sa place et sa couleur de repos), et trois emplacements de plus attendent dans un semis qui grandit. Des événements tirés au hasard
   retirent une dalle présente ou en ramènent une absente, en restant entre −3 et +3 autour de la composition (dans un semis constant,
   jamais au-delà : la densité ne grandit pas). Espacés de 1,8 à 3,2 s de temps d'aperçu, parfois deux presque ensemble. Tout le temps
   de l'aperçu s'écoule à ×0,6 (AP_LENT) : ressort, poussée, transitions des mondes — le même mouvement, plus lent.
   Après chaque événement, quand il s'est posé, les dalles reviennent à leur emplacement : la composition ne dérive pas. */
var AP_LENT=1, AP_ECART=[3000,5300], AP_SERRE=[800,1500], AP_POSE=2300;   /* ⚑ v83 (Tom : « les mouvements au Studio sont devenus lents, comme s'ils chargeaient ») — le ralenti ×0,6 de v76 retiré : les mondes y ont leur rythme validé ; l'espacement réel des événements est gardé (3 à 5,3 s) */
function _apCle(x,y){ var t='v\u0000'+Math.round(x)+'\u0000'+Math.round(y), h=0x811c9dc5; for(var i=0;i<t.length;i++){ h^=t.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return h>>>0; }   /* la clé de repli des mondes neufs, prise UNE fois, au repos */
function _apCopie(s){ var o={}; for(var k in s) if(Object.prototype.hasOwnProperty.call(s,k)) o[k]=s[k]; return o; }
function _apRemet(c){ c.prochain=null;   /* la composition d'origine, exacte ; les gris restent ceux du monde affiché (repaintWorld les tire) */
  var gr={}; seeds.forEach(function(s){ if(s._b!=null) gr[s._b]=[s.gray,s.gc]; });
  var out=c.base.map(function(b){ var s=_apCopie(b); var q=gr[s._b]; if(q){ s.gray=q[0]; s.gc=q[1]; } else { s.gray=grays()[(_alea()*5)|0]; s.gc=null; } s.px=s.x; s.py=s.y; return s; });
  seeds.length=0; Array.prototype.push.apply(seeds,out); _trans=null; _finC=null; _finPrev=null; }
/* les trois emplacements de plus d'un semis qui grandit : tirés une fois, sur la composition d'origine */
function _apExtras(c){ if(c.extras) return c.extras; c.extras=[];
  for(var i=0;i<3;i++){ var p=ipos(), s=mk(p.x,p.y,'promi'); seeds.push(s); var ci=cc(s); seeds.pop(); c.extras.push({pos:[p.x,p.y],ci:ci,w:3.4,cle:_apCle(p.x,p.y)}); }
  return c.extras; }
function _apPresent(s){ return s.kind!=='gray'&&s.part==null; }
function _apMasque(c){ var B=c.base.length, m=[], i; for(i=0;i<B;i++) m.push('0'); var X=[0,0,0];
  seeds.forEach(function(s){ if(!_apPresent(s)) return; if(s._b!=null) m[s._b]='1'; else if(s._x!=null) X[s._x]=1; });
  return m.join('')+(_semisNeuf()?X.join(''):''); }
function _apMasqueBase(c){ var m=''; for(var i=0;i<c.base.length;i++) m+='1'; return m+(_semisNeuf()?'000':''); }
/* une dalle arrive à son emplacement : `b` (la composition) ou `x` (un emplacement de plus) */
function _apAjoute(c,sl,now){ var s;
  if(_semisNeuf()){
    var P=sl.x!=null?c.extras[sl.x]:null, b=sl.b!=null?c.base[sl.b]:null, pos=P?P.pos:[b.x,b.y];
    s=mk(pos[0],pos[1],'promi'); s.ci=P?P.ci:b.ci; s.c=PAL[s.ci]; s.t0=now; s.apercu=1; s._cleAp=P?P.cle:b._cleAp;
    if(P) s._x=sl.x; else s._b=sl.b;
    var wf=P?P.w:b.w; s.w=-22; s.wt=Math.max(12,wf); s.wFin=wf; s.wAt=now+380;
    if(RD[theme]&&RD[theme].sansPoussee){ s.w=s.wFin; s.wt=s.wFin; s.wAt=0; }
    if(RD[theme]&&RD[theme].douce){ s.wt=s.wFin; s.wAt=0; }
    seeds.push(s); _transPose('arrive',s.x,s.y);
  } else {   /* Toile.plantOne : la cellule repliée regrandit à sa place, de sa couleur d'origine, en poussant ses voisines */
    var k=-1, i; for(i=0;i<seeds.length;i++) if(seeds[i]._b===sl.b){ k=i; break; } if(k<0) return;
    var v=seeds[k], bb=c.base[sl.b];
    s=mk(v.x,v.y,'promi'); s._b=sl.b; s.apercu=1; s.ci=bb.ci; s.c=bb.c; s.t0=now; s.w=v.w; s.wt=12; s.wFin=bb.w||0; s.wAt=now+380; s.tx=bb.x; s.ty=bb.y;
    if(RD[theme]&&RD[theme].douce){ s.wt=s.wFin; s.wAt=0; }
    s.gray=v.gray; s.gc=v.gc; s.tone=v.tone; s.shade=v.shade; s.ang=v.ang; s.ph=v.ph; s.am=v.am; s.px=v.px; s.py=v.py;
    if(_rg('elanPlante')) window._tPlante=now;
    seeds[k]=s;   /* au rang de la cellule : un motif tiré du rang ne se rebat pas */
  }
  relax(); tones(); lastChange=now; }
/* une dalle présente s'en va : dans un semis qui grandit elle se retire (v43) ; dans un semis constant elle se replie (v76) */
function _apRetire(c,s,now){ var k=seeds.indexOf(s); if(k<0) return;
  if(_semisNeuf()){
    if(RD[theme]&&RD[theme].transDur){ s.part=now; s.partPid=null; s.partNuee=null; s.wt=s.w-30; s.wFin=s.wt; s.wAt=0; if(RD[theme].sansPoussee) s.w=s.wt; _transPose('depart',s.x,s.y); }
    else seeds.splice(k,1);
  } else { _replie(s,now); }   /* au Studio, tout semis constant replie (Houle et Taille-douce compris) */
  relax(); relax(); relax(); tones(); lastChange=now; }
/* quand l'événement s'est posé : chaque dalle retourne à son emplacement */
function _apRetourne(c){ var ex=c.extras||[];
  seeds.forEach(function(s){ if(s.part!=null) return; var q=s._b!=null?c.base[s._b]:(s._x!=null?ex[s._x]:null); if(!q) return;
    var x=q.x!=null?q.x:q.pos[0], y=q.y!=null?q.y:q.pos[1]; s.tx=x; s.ty=y; if(s.kind!=='gray'){ s.wt=s.wFin=(q.w!=null?q.w:3.4); s.wAt=0; } });
  lastChange=performance.now(); }
function _apEvenement(c,now,premier){ var neuf=_semisNeuf(), B=c.base.length; if(neuf) _apExtras(c);
  var pres=[], abs=[], vus={}, i;
  seeds.forEach(function(s){ if(s._b!=null) vus['b'+s._b]=s; else if(s._x!=null) vus['x'+s._x]=s; if(_apPresent(s)) pres.push(s); });
  var nds=!!_rg('ondeNoeuds');   /* v79 : dans Madrure seuls les nœuds font l'onde */
  if(nds) pres=pres.filter(function(s){ return s._nd||s._x!=null; });
  for(i=0;i<B;i++){ if(nds&&!c.base[i]._nd) continue; var sb=vus['b'+i]; if(!sb||(!neuf&&sb.kind==='gray')) abs.push({b:i}); }
  if(neuf) for(i=0;i<3;i++) if(!vus['x'+i]) abs.push({x:i});
  var Bn=nds?10:B, n=pres.length, min=Bn-3, max=neuf?Bn+3:Bn, peutA=abs.length&&n<max, peutR=pres.length&&n>min;
  /* la première, tout de suite : un semis qui grandit reçoit son premier emplacement de plus (celui que Ramage et Volubilis
     préparent d'avance) ; un semis constant replie une dalle */
  if(premier){ if(neuf&&peutA){ _apAjoute(c,{x:0},now); c.prochain={th:theme,D:_apTire(c)}; return; } if(peutR){ _apRetire(c,pres[(_alea()*pres.length)|0],now); c.prochain={th:theme,D:_apTire(c)}; return; } }
  /* ⚑ v89 — l'événement suivant est TIRÉ D'AVANCE (c.prochain), juste après celui-ci : un monde qui prépare son arrivée (Ramage) la
     prépare pendant le repos, et l'événement ne vient qu'une fois elle prête — il glisse dès sa première image, dans sa vraie forme. */
  var D=(c.prochain&&c.prochain.th===theme)?c.prochain.D:_apTire(c); c.prochain=null;
  if(D&&D.a){ var e=D.a; if(!(e.b!=null&&neuf&&vus['b'+e.b])&&!(e.x!=null&&vus['x'+e.x]&&_apPresent(vus['x'+e.x]))) _apAjoute(c,e,now); }
  else if(D&&D.r){ var sr=vus[D.r]; if(sr&&_apPresent(sr)&&pres.indexOf(sr)>=0) _apRetire(c,sr,now); }
  c.prochain={th:theme,D:_apTire(c)}; }
function _apTire(c){ var neuf=_semisNeuf(), B=c.base.length, pres=[], abs=[], vus={}, i;
  seeds.forEach(function(s){ if(s._b!=null) vus['b'+s._b]=s; else if(s._x!=null) vus['x'+s._x]=s; if(_apPresent(s)) pres.push(s); });
  var nds=!!_rg('ondeNoeuds'); if(nds) pres=pres.filter(function(s){ return s._nd||s._x!=null; });
  for(i=0;i<B;i++){ if(nds&&!c.base[i]._nd) continue; var sb=vus['b'+i]; if(!sb||(!neuf&&sb.kind==='gray')) abs.push({b:i}); }
  if(neuf) for(i=0;i<3;i++) if(!vus['x'+i]) abs.push({x:i});
  var Bn=nds?10:B, n=pres.length, min=Bn-3, max=neuf?Bn+3:Bn, peutA=abs.length&&n<max, peutR=pres.length&&n>min;
  if(peutA&&(!peutR||_alea()<0.5)) return {a:abs[(_alea()*abs.length)|0]};
  if(peutR){ var s=pres[(_alea()*pres.length)|0]; return {r:s._b!=null?'b'+s._b:'x'+s._x}; }
  return null; }
var _apSemN=0;
function _apBase(c){ if(c.base) return; c.semId=++_apSemN;
  c.seeds.forEach(function(s){ s._cleAp=_apCle(s.x,s.y); });
  var nd=c.seeds.slice().sort(function(a,b){ return a._cleAp-b._cleAp; }).slice(0,10); nd.forEach(function(s){ s._nd=1; });   /* v79 : les dix nœuds d'un aperçu de Madrure (v40) */
  c.base=c.seeds.map(function(s,i){ s._b=i; if(s.tx==null){ s.tx=s.x; s.ty=s.y; } if(s.wt==null) s.wt=s.w||0; if(s.wFin==null) s.wFin=s.wt; s.wAt=0; s.w=s.w||0; return _apCopie(s); }); }
/* ⚑ v92 (Tom, 28 sept. : « feu vert pour préparer le film avant le geste. Tu peux toucher au moteur pour tirer la couleur et la place
   à l'avance ») — LA PLANTATION SIMULÉE. Sur des COPIES des graines, avec un tirage semé (`g0`), on joue la plantation (ou le retrait)
   telle que le vrai geste la jouera, et le monde prépare ce qu'il lui faut (Ramage : le film de la pousse). Tout l'état du moteur est
   rendu à l'identique (`_apLit`/`_apPose`, `_transN`, la couleur figée des paroles). Le tirage est GARDÉ : la vraie plantation, si la
   Toile n'a pas bougé entre-temps (`_simSig`), tire la même place et la même couleur — sinon elle tire comme avant, et le monde
   retombe sur sa lecture progressive. */
var _simRand=null;
function _lcgSim(g0){ var s=(g0>>>0)||1; return function(){ s=(Math.imul(s,1103515245)+12345)&0x7fffffff; return s/0x7fffffff; }; }
function _simSig(){ var h=2166136261; for(var i=0;i<seeds.length;i++){ var s=seeds[i]; h^=(Math.round(s.x*2)*7+Math.round(s.y*2)*13+((s.ci|0)+1)*17+(s.part!=null?991:0)+(s.pid!=null?(s.pid|0)%9973:0))|0; h=Math.imul(h,16777619)>>>0; } return h+':'+seeds.length+':'+theme; }
window.Toile.simule=function(ajouts,retraits,fn){
  if(!_semisNeuf()||!g||_AP||window._simOff) return false;
  var M=_apLit(), tn=_transN, mr=_aleaF, sig=_simSig(), faux=[], dal=[], r=false;
  var g0=(_simRand&&_simRand.sig===sig&&_simRand.used===0&&_simRand.n===(ajouts?ajouts.length:0))?_simRand.g0:((mr()*2147483600)|0)+1;   /* la Toile n'a pas bougé : le MÊME tirage (un film déjà préparé reste juste) */
  var copie=seeds.map(function(s){ var c={}; for(var k in s) c[k]=s[k]; return c; });
  try{
    promises.forEach(function(p){ dal.push([p,p.dalle]); });
    _apPose(Object.assign({},M,{seeds:copie,view:{s:M.view.s,ox:M.view.ox,oy:M.view.oy},nueeCells:Object.assign({},M.nueeCells)}));
    if(ajouts&&ajouts.length){ _aleaF=_lcgSim(g0);
      ajouts.forEach(function(a,i){ var id=a.id; if(id==null){ var f={id:-(9e8+i),title:a.title||'',who:a.who||'moi',chiche:!!a.chiche,draft:false}; promises.push(f); faux.push(f); id=f.id; } _addPromiNu(id); });
      _aleaF=mr; }
    if(retraits&&retraits.length) window.Toile.sync(promises.filter(function(q){ return !q.draft&&retraits.indexOf(q.id)<0; }).map(function(q){ return q.id; }));
    var tv=_transVive; _transVive=true; try{ r=fn?fn():true; } finally{ _transVive=tv; }   /* comme pendant une image de la Toile : le monde est vivant (places gardées, papier de la Toile) */
  }catch(e){ window._simErr=String(e&&e.stack||e); r=false; }
  finally{ _aleaF=mr; for(var fi=promises.length-1;fi>=0;fi--) if(faux.indexOf(promises[fi])>=0) promises.splice(fi,1); dal.forEach(function(d){ d[0].dalle=d[1]; }); _apPose(M); _transN=tn; }
  if(ajouts&&ajouts.length) _simRand={f:_lcgSim(g0),g0:g0,sig:sig,n:ajouts.length,used:0,t:performance.now()};
  return r; };
window.Toile.ancrePid=function(pid){ var s=null; for(var i=0;i<seeds.length;i++) if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){ s=seeds[i]; break; } if(!s) return null; var a=null; try{ a=(RD[theme]&&RD[theme].ancre)?RD[theme].ancre(s):null; }catch(_){ } return a?[a[0],a[1]]:[s.x,s.y]; };   /* v93 : pour les juges — où le monde pose la parole (l'œil de Ramage, la fleur de Volubilis) */
/* ⚑ v97 (Tom, iPhone : « Halin avec une seule dalle : elle prend tout l'écran, on ne comprend rien. Il en faut au moins deux autres, non
   choisies, pour qu'on voie la structure. À partir de deux paroles, le principe reprend ») — la Toile de Halin est faite de ses paroles :
   à une parole, une seule cellule. On lui adjoint DEUX cellules neutres (des graines grises, que Halin sait peindre — la Toile vide du
   §10.6), au plus grand vide (`_auVide`, tiré de la clé de la Toile : même Toile, même place), au poids d'une parole. Leur aspect vient de
   leur rang, jamais du hasard. Dès deux paroles, elles partent. Zéro parole : le semis de la Toile vide reste tel quel. */
function _compagnonsHalin(){
  if(!_rg('compagnons')||_AP) return false;
  var n=0, comp=[]; for(var i=0;i<seeds.length;i++){ var s=seeds[i]; if(s.compagnon) comp.push(s); else if(s.kind!=='gray'&&s.part==null) n++; }
  if(n===1){ if(comp.length===2) return false;
    seeds=seeds.filter(function(s){ return !s.compagnon; });
    for(var k=0;k<2;k++){ var q=_auVide(90+k), g=mk(q.x,q.y,'gray'); g.compagnon=1; g.gray=grays()[(k*2+1)%grays().length]; g.tone=TON[(k+1)%TON.length]; g.shade=1; g.ang=0.9+1.7*k; g.ph=1.3+2.1*k; g.am=1;
      g.w=3.4; g.wt=3.4; seeds.push(g); }
    window.Toile.paintOrder=null; try{ relax(); }catch(_){ } kick(); return true; }
  if(comp.length){ seeds=seeds.filter(function(s){ return !s.compagnon; }); window.Toile.paintOrder=null; try{ relax(); }catch(_){ } kick(); return true; }
  return false; }
window._compagnonsHalin=_compagnonsHalin;
(function(){ ['addPromi','sync','setTheme','removePromi'].forEach(function(nom){ var f=window.Toile[nom]; if(typeof f!=='function') return;
  window.Toile[nom]=function(){ var r=f.apply(this,arguments); try{ _compagnonsHalin(); }catch(_){ } return r; }; }); })();
window._simOublie=function(){ var a=!!_simRand; _simRand=null; return a; };   /* pour les juges : le tirage oublié, la prédiction manquée */
var _addPromiNu=window.Toile.addPromi;
window.Toile.addPromi=function(id){ var R=_simRand;
  if(R&&R.used===0&&(R.sig!==_simSig()||performance.now()-R.t>120000)) R=_simRand=null;
  if(!R) return _addPromiNu.apply(this,arguments);
  var mr=_aleaF; _aleaF=R.f; try{ return _addPromiNu.apply(this,arguments); } finally{ _aleaF=mr; if(++R.used>=R.n) _simRand=null; } };
/* les trois moments où l'on sait ce qui va arriver : la phrase qui s'écrit (pause de 700 ms), le trait de la plantation, la
   confirmation d'une suppression. Ramage et Volubilis : les deux mondes dont l'arrivée se calcule. */
(function(){
  function ramage(){ return !!(RD[theme]&&RD[theme].prepareToile); }   /* v92 : Ramage et Volubilis — les mondes qui savent préparer */
  function prepare(ajouts,retraits){ if(!ramage()) return false; var th=theme; return window.Toile.simule(ajouts,retraits,function(){ return RD[th].prepareToile(); }); }
  window._simPrepare=prepare;
  function formulaire(){ var t=((document.getElementById('fTitle')||{}).value||'').trim(); if(!t) return null;
    var rc=(typeof window.newWhoSel!=='undefined'&&window.newWhoSel&&window.newWhoSel.length)?window.newWhoSel.slice():[];
    if(!rc.length){ var ty=((document.getElementById('fWho')||{}).value||'').trim(); if(ty&&ty.toLowerCase()!=='moi'&&ty.indexOf(',')<0) rc=[ty]; }
    if(!rc.length) rc=['moi']; if(rc.length>1) rc=rc.filter(function(r){ return r&&r!=='moi'; });
    var ch=!!(window._phrase&&window._phrase.sens==='chiche');
    return rc.map(function(w){ return {title:t,who:w,chiche:ch}; }); }
  var tmr=null, der='';
  function planifie(){ clearTimeout(tmr); tmr=setTimeout(function(){ var cs=document.getElementById('createSheet'); if(!cs||!cs.classList.contains('show')||!ramage()) return;
      if((cs.getAttribute('data-kind')||'promi')!=='promi'||(typeof selNuee!=='undefined'&&selNuee)) return;
      var A=formulaire(); if(!A) return; var cle=JSON.stringify(A); if(cle===der&&_simRand) return;
      if(RD[theme].filmEnCours&&RD[theme].filmEnCours()){ planifie(); return; }   /* un film déjà en calcul : on attend qu'il finisse */
      der=cle; prepare(A,null); },700); }
  document.addEventListener('input',function(e){ if(e.target&&(e.target.id==='fTitle'||e.target.id==='fWho')) planifie(); },true);
  document.addEventListener('pointerup',function(e){ if(e.target&&e.target.closest&&e.target.closest('#createSheet')) planifie(); },true);
  /* le trait : les paroles viennent d'être créées (promises), la Toile ne les a pas encore — on prépare avec les VRAIES */
  function enveloppe(){ if(window.printTirage&&window.printTirage.__sim) return; var pt=window.printTirage; if(typeof pt==='function'){ window.printTirage=function(){ var r=pt.apply(this,arguments);
    setTimeout(function(){ try{ if(!ramage()) return; var sur={}; seeds.forEach(function(s){ if(s.pid!=null) sur[s.pid]=1; });
      var A=promises.filter(function(p){ return !p.draft&&!p.nuee&&!sur[p.id]; }).map(function(p){ return {id:p.id}; }); if(A.length) prepare(A,null); }catch(_){ } },0);
    return r; }; window.printTirage.__sim=true; }
  var sp=window._v16SupprimerPromi; if(typeof sp==='function'&&!sp.__sim){ window._v16SupprimerPromi=function(p){ var r=sp.apply(this,arguments);
    try{ var q=p||(typeof cur!=='undefined'?cur:null); if(q&&!q.draft) prepare(null,[q.id]); }catch(_){ } return r; }; window._v16SupprimerPromi.__sim=true; } }
  window.addEventListener('load',function(){ setTimeout(enveloppe,0); });   /* les deux portes sont définies plus loin dans le fichier */
}());   /* ⚑ jamais « })(); » en début de ligne ici : redteam_decoupe y lit la fin du moteur */
function _apCycle(c,now){ var cy=c.cy;
  if(!cy||cy.th!==c.th){   /* un monde neuf à l'écran : la composition d'origine, et le premier événement TOUT DE SUITE */
    if(cy) _apRemet(c);
    cy=c.cy={th:c.th,suiv:now+60,pose:0,n:0};
    /* ⚑ v90 — Ramage : son premier événement (un emplacement de plus) est tiré d'avance comme les suivants — il attend son plumage
       et le film de sa pousse, 4 s au plus comme les suivants (la composition au repos, comme entre deux événements), puis part comme avant */
    if(c.th==='ramage'&&_semisNeuf()&&!window._ramFilmOff){ c.prochain={th:'ramage',D:{a:{x:0}}}; cy.n=1; cy.prem=now; } }   /* v80 : une image de la composition d'abord — un monde qui anime ses éclats (Esquille) doit savoir d'où ils partent */
  var _apP=_rg('apercuPause'); if(_apP&&window[_apP[0]]&&now>=cy.suiv){ cy.suiv=now+_apP[1]; return; }   /* v91 : Volubilis finit son tissage avant l'événement suivant */   /* v87 : Ramage finit son glissé avant l'événement suivant */
  if(_rg('apercuFilm')&&now>=cy.suiv&&c.prochain&&_rg('apercuFilm',c.prochain.th)&&(!c.prochain.pret||(window._ramPret&&!window._ramPret(c.prochain.K)))){ if(!cy.att) cy.att=now; if(now-cy.att<8000){ cy.suiv=now+(cy.prem&&cy.n===1?30:60); return; } }   /* v90 : on attend le film (8 s au plus) plutôt que de pousser par étapes */   /* v89 : l'événement tiré d'avance n'est pas encore prêt */
  if(now>=cy.suiv) cy.att=0;
  if(now>=cy.suiv){ _apEvenement(c,now,cy.n===0); cy.n++; cy.pose=now+AP_POSE;
    var serre=_alea()<0.3, E=serre?AP_SERRE:AP_ECART; cy.suiv=now+E[0]+_alea()*(E[1]-E[0]); if(cy.suiv<cy.pose&&!serre) cy.pose=cy.suiv; return; }
  if(cy.pose&&now>=cy.pose){ cy.pose=0; _apRetourne(c); } }
/* une image de l'aperçu vivant — rend vrai tant qu'il reste du mouvement (il en reste toujours : le cycle ne s'arrête pas) */
var _pnVrai=performance.now.bind(performance);
window.Toile.apercuImage=function(pcv){ var c=pcv&&pcv.__c; if(!c||!RD[c.th]) return false;
  /* v76 — l'aperçu a sa propre horloge, à ×0,6 (AP_LENT) : TOUT ce qui se lit dans l'image (performance.now, le ressort, les
     transitions des mondes) avance moins vite. Une image de plus de 250 ms (une pause) ne compte que pour une image. */
  var rv=_pnVrai(); if(c.vt==null){ c.vt=rv; c.rt=rv; } var dr=rv-c.rt; if(dr>250) dr=16.7; c.vt+=dr*AP_LENT; c.rt=rv; var vt0=c.vt, rt0=rv;
  performance.now=function(){ return vt0+(_pnVrai()-rt0)*AP_LENT; };
  var now=vt0;   /* une seule horloge : l'heure d'une image (rAF) peut précéder celle du clic qui a changé de monde */
  var M=_apLit(), ok=false;
  try{
    if(!c.etat||c.etat.seeds!==c.seeds||c.etat.g.canvas!==pcv){
      _apBase(c);
      c.etat={g:pcv.getContext('2d'),W:c.pw,H:c.ph,DPR:pcv.width/c.pw,seeds:c.seeds,theme:c.th,view:{s:1,ox:0,oy:0},_trans:null,_finC:null,_finPrev:null,lastChange:0,_qT0:0,_inert:null,vTarget:null,lastNuee:null,nueeCells:{},
        ft:undefined,ftp:undefined,fr:1,ftv:undefined,tP:0,tM:0,me:false,vm:false,rd:false}; }
    c.etat.theme=c.th; c.etat.seeds=c.seeds; c.etat.view={s:1,ox:0,oy:0};
    _apPose(c.etat); _AP=c; c.vif=true; var _rtA=_rtCible; _rtCible=pcv; window._apImage=true;   /* la Toile entière, vue 1:1 : les calques de Touffe et de Houle s'y posent (le patron de renderTo) */
    _apCycle(c,now); window._apPhase=c.semId+'|'+_apMasque(c); window._apPhaseBase=c.semId+'|'+_apMasqueBase(c);   /* l'état de l'aperçu : quelles dalles sont là */
    frame(now); ok=true; _apVu=c; c.tImg=rt0;
  }catch(e){ window._apErreur=String(e&&e.stack||e); }
  finally{ performance.now=_pnVrai; _AP=null; window._apImage=false; if(typeof _rtA!=='undefined') _rtCible=_rtA; try{ c.etat=_apLit(); c.seeds=c.etat.seeds; }catch(_){ } _apPose(M); }
  return ok; };
/* ⚑ v75 — LA PRÉPARATION À L'AVANCE (Ramage, Volubilis). Deux mondes ne savent pas montrer leur arrivée tout de suite : Ramage peint
   son plumage d'arrivée par tranches (0,9 à 1 s), Volubilis construit son jardin (0,5 à 1,3 s, d'un bloc à la première image). Tant que
   l'aperçu montre un autre monde du même semis, on leur fait préparer, par petites tranches et sur un canevas caché de la même taille,
   les deux états que leur arrivée lira : le repos (la composition d'origine) et l'arrivée (la dalle neuve à sa place). Même état du
   moteur que l'arrivée réelle — mêmes graines, même dalle neuve, même transition — donc mêmes signatures : à l'arrivée, ils trouvent
   ce qu'ils cherchent. Un monde qui n'a pas `RD[m].prepare` n'a rien à préparer. */
var _apPrepCv=null;
function _apFam(th){ return (window._apercuClair&&window._apercuClair[th])?'clair':'grille'; }
window.Toile.apercuPrepare=function(pcv,monde,budget){
  if(!RD[monde]||!RD[monde].prepare) return true;
  var F=pcv.__fam||{}, cc0=pcv.__c, c=(cc0&&_apFam(cc0.th)===_apFam(monde))?cc0:F[_apFam(monde)]; if(!c) return false;
  var cle=monde+'|'+_apFam(monde)+'|'+palKey+'|'+hueShift+'|'+isLightM(); c.prep=c.prep||{};   /* une autre palette, un autre thème : d'autres couleurs, on reprépare */ if(c.prep[cle]) return true;
  if(!_apPrepCv) _apPrepCv=document.createElement('canvas');
  if(_apPrepCv.width!==pcv.width) _apPrepCv.width=pcv.width; if(_apPrepCv.height!==pcv.height) _apPrepCv.height=pcv.height;
  var M=_apLit(), fini=false, now=performance.now(), tv=_transVive, rt=_rtCible;
  try{
    _apBase(c);
    var pal=isLightM()?GLIGHT:TH[monde]?TH[monde].g:null;
    var sb=c.base.map(function(b){ var s=_apCopie(b); s.px=s.x; s.py=s.y; return s; });
    var e={g:_apPrepCv.getContext('2d'),W:c.pw,H:c.ph,DPR:_apPrepCv.width/c.pw,seeds:sb,theme:monde,view:{s:1,ox:0,oy:0},_trans:null,_finC:null,_finPrev:null,lastChange:0,_qT0:0,_inert:null,vTarget:null,lastNuee:null,nueeCells:{},ft:undefined,ftp:undefined,fr:1,ftv:undefined,tP:0,tM:0,me:false,vm:false,rd:false};
    _apPose(e); _AP=c; _transVive=true; _rtCible=_apPrepCv; window._apImage=true;
    g.setTransform(DPR,0,0,DPR,0,0);
    var d=null; if(_semisNeuf()){ var X0=_apExtras(c)[0]; d={x:X0.pos[0],y:X0.pos[1]}; }
    _transPose('arrive',d?d.x:c.pw/2,d?d.y:c.ph/2);   /* le repos se lit comme à l'arrivée réelle : transition en cours, sans la dalle neuve */
    window._apPhase=window._apPhaseBase=c.semId+'|'+_apMasqueBase(c); var t0=performance.now(), a=RD[monde].prepare(now,budget,1), b=false;
    if(a&&d&&performance.now()-t0<budget){ _apAjoute(c,{x:0},now); _finC=null; window._apPhase=c.semId+'|'+_apMasque(c); b=RD[monde].prepare(now,Math.max(1,budget-(performance.now()-t0)),2); }
    fini=!!(a&&(b||!d));
  }catch(err){ window._apErreur=String(err&&err.stack||err); fini=true; }
  finally{ _AP=null; window._apImage=false; _transVive=tv; _rtCible=rt; _apPose(M); }
  if(fini) c.prep[cle]=true;
  return fini; };
/* ⚑ v89 — préparer L'ÉVÉNEMENT TIRÉ D'AVANCE du monde affiché (Ramage), sur une copie des graines : son plumage d'arrivée se construit
   pendant le repos ; le monde en prépare ensuite la matière et les empreintes (son propre repos). */
window.Toile.apercuPrepareProchain=function(pcv,budget){ var c=pcv&&pcv.__c; if(!c||!c.vif||!c.base||!RD[c.th]||!RD[c.th].prepare) return true;
  var P=c.prochain; if(!P||!P.D||P.th!==c.th||P.pret) return true;
  if(!_apPrepCv) _apPrepCv=document.createElement('canvas');
  if(_apPrepCv.width!==pcv.width) _apPrepCv.width=pcv.width; if(_apPrepCv.height!==pcv.height) _apPrepCv.height=pcv.height;
  var M=_apLit(), fini=false, now=performance.now(), tv=_transVive, rt=_rtCible, ph=window._apPhase, phb=window._apPhaseBase;
  try{
    var sb=c.seeds.map(function(s){ var q=_apCopie(s); if(q.px==null) q.px=q.x; if(q.py==null) q.py=q.y; return q; }), vus={};
    sb.forEach(function(s){ if(s._b!=null) vus['b'+s._b]=s; else if(s._x!=null) vus['x'+s._x]=s; });
    var e={g:_apPrepCv.getContext('2d'),W:c.pw,H:c.ph,DPR:_apPrepCv.width/c.pw,seeds:sb,theme:c.th,view:{s:1,ox:0,oy:0},_trans:null,_finC:null,_finPrev:null,lastChange:0,_qT0:0,_inert:null,vTarget:null,lastNuee:null,nueeCells:{},ft:undefined,ftp:undefined,fr:1,ftv:undefined,tP:0,tM:0,me:false,vm:false,rd:false};
    _apPose(e); _AP=c; _transVive=true; _rtCible=_apPrepCv; window._apImage=true; g.setTransform(DPR,0,0,DPR,0,0);
    if(!P.fait){ if(P.D.a&&P.D.a.x!=null&&_semisNeuf()) _apExtras(c);   /* v90 : le premier événement (x:0) lit les emplacements de plus */
      if(P.D.a) _apAjoute(c,P.D.a,now); else if(P.D.r&&vus[P.D.r]) _apRetire(c,vus[P.D.r],now); _finC=null; P.K=c.semId+'|'+_apMasque(c); P.seeds=sb; P.e=e; P.fait=true; }
    else { _apPose(P.e); }
    window._apPhase=P.K; window._apPhaseBase=phb;
    fini=RD[c.th].prepare(now,budget,2,true);
    P.e=_apLit();
  }catch(err){ window._apErreur=String(err&&err.stack||err); fini=true; }
  finally{ _AP=null; window._apImage=false; _transVive=tv; _rtCible=rt; _apPose(M); window._apPhase=ph; window._apPhaseBase=phb; }
  if(fini) P.pret=true;
  return fini; };
/* le semis de l'autre famille, composé d'avance (sans rien peindre) : un doigt qui saute d'une famille à l'autre retrouve un semis préparé */
window.Toile.apercuCompose=function(pcv,monde){ var F=pcv.__fam||(pcv.__fam={}), f=_apFam(monde); if(F[f]) return F[f];
  var cv=document.createElement('canvas'); cv.width=pcv.width; cv.height=pcv.height; cv.__compose=true;
  var av=window._shAllColored; window._shAllColored=true; try{ window.Toile.preview(cv,monde,pcv.__c?pcv.__c.pw:390,pcv.__c?pcv.__c.ph:844); }finally{ window._shAllColored=av; }
  if(cv.__c){ F[f]=cv.__c; } return F[f]||null; };
function _apMasqueLu(c){ var B=c.base?c.base.length:0, m=[], X=[0,0,0], i; for(i=0;i<B;i++) m.push('0'); c.seeds.forEach(function(s){ if(s.kind==='gray'||s.part!=null) return; if(s._b!=null) m[s._b]='1'; else if(s._x!=null) X[s._x]=1; }); return m.join('')+'·'+X.join(''); }
/* l'aperçu cesse de vivre : `repaint` peint de nouveau (fixe) */
window.Toile.apercuArret=function(pcv){ var c=pcv&&pcv.__c; if(c) c.vif=false; };
/* lecture seule, pour les juges : où en est le cycle */
window.Toile.apercuEtat=function(pcv){ var c=pcv&&pcv.__c; if(!c||!c.cy) return null; var n=0; c.seeds.forEach(function(s){ if(s.kind!=='gray') n++; });
  return {monde:c.th, tour:c.cy.n, masque:_apMasqueLu(c), graines:c.seeds.length, colorees:n, base:c.base?c.base.length:0, vif:!!c.vif}; };
window.Toile.resetView=function(){view={s:1,ox:0,oy:0};vTarget=null;};
/* ⚑ Cercle · LA COULEUR (Tom 13 sept.) — relire les couleurs choisies, et donner les quatre tons d'une palette du Studio (teinte comprise). */
window.Toile.refigeCouleurs=function(){_dalleFigee(false);lastChange=performance.now();kick();};
window.Toile.colorOfNuee=function(k){for(var i=0;i<seeds.length;i++){var s=seeds[i];if(s.kind==='nuee'&&s.nuee===k){var c=cOf(s,performance.now());return 'rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';}}return null;};   /* lecture seule */
window.Toile.tonsDe=function(k,h){var b=(PALS[k]||PALS[palKey]).cols;h=+h||0;return b.map(function(c){return h?rotc(c,h):[c[0],c[1],c[2]];});};
/* CHANTIER 1 — rend la VRAIE Toile hors ecran : memes germes, memes positions,
   meme monde. Contrairement a preview(), qui regenere une grille aleatoire.
   Meme patron que repaint() : on echange les globales, on peint, on restaure. */
window.Toile.renderTo=function(cv,ech,clair){
  if(!cv||!cv.getContext)return false;
  if(!seeds.length){try{seedGray();}catch(e){}}
  ech=ech||2;
  var _g=g,_W=W,_H=H,_v={s:view.s,ox:view.ox,oy:view.oy};
  var _ov=window._shThemeOverride;
  var ok=false;
  /* ⚑ v29 — `DPR` VAUT `ech` LE TEMPS DU RENDU. Six mondes remplacent la transformation par `setTransform(DPR…)`
     (CONTRAT-MONDE §11) : tant que renderTo n'était appelé qu'à la densité de la Toile, ça ne se voyait pas. Rendue
     à l'échelle exacte de l'export (redteam_decoupe, famille D), la Toile se peignait à la densité 2 dans un canevas
     de densité 5,5 — petite, dans un coin. Mesuré : écart export/aperçu 112 niveaux. */
  var _dpr0=DPR;
  try{
    DPR=ech;
    cv.width=Math.max(2,Math.round(W*ech));
    cv.height=Math.max(2,Math.round(H*ech));
    g=cv.getContext('2d'); if(!g)throw 0;
    if(clair!=null)window._shThemeOverride=!!clair;
    view={s:1,ox:0,oy:0};                 /* Toile entiere, sans cadrage */
    g.setTransform(ech,0,0,ech,0,0);
    g.clearRect(0,0,W,H);
    /* ⚑ v26 — même fond que la vraie Toile (voir `Toile.preview`) : sur Braille et Touffe,
       les deux tiers de la surface SONT ce fond, et `#120E05` s'y lisait comme un voile. */
    g.fillStyle=(clair!=null?clair:isLightM())?'#EFE2C5':'#050302';   /* v116 : l'encre de seiche */
    g.fillRect(0,0,W,H);
    /* ⚑ v44 — LA COMPOSITION DU RENDU EST PUBLIÉE (§7 : un juge compare la composition, jamais un pixel d'une matière
       texturée). Ce sont les graines que le monde VA recevoir — publiées juste avant l'appel, jamais après (une publication faite après ne voit pas ce qui a été fait pendant). */
    try{ window._renduComp={W:W,H:H,ech:ech,monde:theme,graines:seeds.filter(function(s){return s.pid!=null;}).map(function(s){return {pid:s.pid,x:(s.px!=null?s.px:s.x),y:(s.py!=null?s.py:s.y),w:s.w};})}; }catch(_){ }   /* v38 : `_rtCible` — le rendu entier de la Toile peut se servir des calques de Touffe */

    _rtCible=cv; try{ RD[theme](performance.now(),0,0,W,H); }finally{ _rtCible=null; }  /* les VRAIS germes */    /* CHANTIER 39 — le texte des dalles : frame() appelle _labels apres
       RD[theme], renderTo ne le faisait pas. Sans lui « Avec / Sans texte »
       n'avait aucun effet sur l'image partagee. */
    if(window._shLabels!==false){
      try{ if(typeof _labels==='function')_labels(performance.now()); }catch(_l){}
    }
    /* les Promi masques au partage : leur dalle revient au gris du fond.
       On repeint par-dessus plutot que de retirer le germe, ce qui
       changerait le pavage entier. */
    try{ var _hid=window.shareHidden||{};
      if(Object.keys(_hid).length){
        for(var _i=0;_i<seeds.length;_i++){
          var _s=seeds[_i];
          if(_s.pid==null||!_hid[_s.pid])continue;
          var _sv={ci:_s.ci,kind:_s.kind,gc:_s.gc};
          _s.ci=null; _s.kind='gray'; _s.gc=null;
          _s.__sv=_sv;
        }
        g.setTransform(ech,0,0,ech,0,0);
        RD[theme](performance.now(),0,0,W,H);
        for(var _j=0;_j<seeds.length;_j++){
          var _t=seeds[_j]; if(!_t.__sv)continue;
          _t.ci=_t.__sv.ci; _t.kind=_t.__sv.kind; _t.gc=_t.__sv.gc; delete _t.__sv;
        }
        if(window._shLabels!==false){
          try{ if(typeof _labels==='function')_labels(performance.now()); }catch(_l2){}
        }
      } }catch(_h){}
    ok=true;
  }catch(e){}
  g=_g;W=_W;H=_H;view=_v;window._shThemeOverride=_ov;DPR=_dpr0;
  return ok;
};
/* ⚑ v26 — LE FOND D'UNE TOILE, NOMMÉ UNE FOIS. Trois fonctions le peignaient chacune de
   son côté (`preview`, `repaintWorld`, `repaint`) : corriger l'une ne changeait rien,
   car `repaint` repasse à chaque frémissement. §7 — un seul propriétaire. */
window.Toile.fondToile=function(clair){ return (clair!=null?clair:isLightM())
  ? (window._shAllColored?'#DDD2B8':'#F1ECD9') : '#050302'; };   /* v116 : l'encre de seiche */
window.Toile.repaint=function(pcv){var c=pcv&&pcv.__c;if(!c)return;if(c.vif)return;   /* v75 : l'aperçu vivant se peint dans sa boucle */var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};try{g=pcv.getContext('2d');W=c.pw;H=c.ph;seeds=c.seeds;theme=c.th;view={s:1,ox:0,oy:0};var dpr=pcv.width/c.pw;g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,c.pw,c.ph);g.fillStyle=window.Toile.fondToile();g.fillRect(0,0,c.pw,c.ph);RD[c.th](performance.now(),0,0,c.pw,c.ph);}catch(e){}g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;};
window.Toile.reGray=function(){seeds.forEach(function(s){s.gray=grays()[(_alea()*5)|0];s.gc=null;});lastChange=performance.now();kick();};
window.Toile.reGrayStudio=function(pcv){var c=pcv&&pcv.__c;if(!c)return;c.seeds.forEach(function(s){s.gray=grays()[(_alea()*5)|0];s.gc=null;});window.Toile.repaint(pcv);};
window.Toile.curWorld=function(){return theme;};
window.Toile.taille=function(){return {w:W,h:H};};   /* v34 · lecture seule */
window.Toile.semisNeuf=function(){ return _semisDe==='neuf'; };   /* v35 · la famille du semis EN PLACE */
/* ⚑ v34 — le semis, en lecture seule : toutes les graines, les colorées, les vides. */
window.Toile.graines=function(){ var c=0; for(var i=0;i<seeds.length;i++) if(seeds[i].kind!=='gray') c++; return {total:seeds.length, colorees:c, vides:seeds.length-c}; };
/* ⚑ v32 — la nature de la dalle seule d'un monde libre neuf (Madrure : 'oeil' · 'fermee' · 'cercle') et son contour peint. */
window.Toile.natureDalle=function(pid,m){ var t=m||theme; if(!_MN||!_MNLIB[t])return null; for(var i=0;i<seeds.length;i++){ if(seeds[i].pid===pid&&seeds[i].kind!=='gray') return _MN.nature(t,seeds[i]); } return null; };
window.Toile.contourDalle=function(pid,m){ var t=m||theme; if(!_MN||!_MNLIB[t])return null; for(var i=0;i<seeds.length;i++){ if(seeds[i].pid===pid&&seeds[i].kind!=='gray') return _MN.contour(t,seeds[i]); } return null; };
window.Toile._madrure=function(inv){ if(inv&&_MN&&_MN.madrure) _MN.madrure.invalider(); return (_MN&&_MN.madrure)?{derniere:_MN.madrure.derniere||null, constructions:_MN.madrure.constructions||0}:null; };
window.Toile.dalleCapture=function(dcv,pid,ech){
  try{
    var D=window.Toile.dalleAbs(pid); if(!D||!D.w||!D.h) return false;
    var cv=document.getElementById('toileCv'); if(!cv) return false;
    var tgt=null;
    for(var i=0;i<seeds.length;i++){if(seeds[i].pid===pid&&seeds[i].kind!=='gray'){tgt=seeds[i];break;}}
    if(!tgt) return false;
    /* marge : encre, terrazzo et touffe debordent de leur cellule */
    var LIBRE=!!_rg('libre');
    var sp=Math.sqrt(W*H/Math.max(1,seeds.length));
    var mar=LIBRE?sp*0.85:sp*0.10;
    var lx0=D.minx-mar, ly0=D.miny-mar, lw=D.w+2*mar, lh=D.h+2*mar;
    var sx=(lx0*view.s+view.ox)*DPR, sy=(ly0*view.s+view.oy)*DPR;
    var sw=lw*view.s*DPR, sh=lh*view.s*DPR;
    /* si la marge sort du cadre, on rogne au bord plutot que de renoncer */
    var rx0=Math.max(0,sx), ry0=Math.max(0,sy);
    var rx1=Math.min(cv.width,sx+sw), ry1=Math.min(cv.height,sy+sh);
    if(rx1-rx0<8||ry1-ry0<8) return false;
    lx0=lx0+(rx0-sx)/(view.s*DPR); ly0=ly0+(ry0-sy)/(view.s*DPR);
    lw=(rx1-rx0)/(view.s*DPR); lh=(ry1-ry0)/(view.s*DPR);
    sx=rx0; sy=ry0; sw=rx1-rx0; sh=ry1-ry0;
    ech=ech||1;
    var dw=Math.max(1,Math.round(sw*ech)), dh=Math.max(1,Math.round(sh*ech));
    dcv.width=dw; dcv.height=dh;
    var gg=dcv.getContext('2d'); if(!gg) return false;
    gg.setTransform(1,0,0,1,0,0); gg.clearRect(0,0,dw,dh);
    gg.imageSmoothingQuality='high';
    gg.drawImage(cv, sx, sy, sw, sh, 0, 0, dw, dh);
    /* on ne garde que les pixels de CETTE dalle, avec la regle exacte du moteur */
    var im=gg.getImageData(0,0,dw,dh), d2=im.data, ns=seeds.length;
    for(var yy=0;yy<dh;yy++){
      var ly=ly0+(yy+0.5)*lh/dh;
      for(var xx=0;xx<dw;xx++){
        var lx=lx0+(xx+0.5)*lw/dw, bd=1e18, bs=null;
        for(var q=0;q<ns;q++){var s2=seeds[q];
          var ex=lx-s2.x, ey=ly-s2.y;
          var dq=Math.sqrt(ex*ex+ey*ey)-(s2.w||0);
          if(dq<bd){bd=dq;bs=s2;}}
        var o4=(yy*dw+xx)*4;
        if(bs!==tgt){ d2[o4+3]=0; }
        else {
          /* le fond de la Toile devient transparent, la matiere reste pleine */
          var r=d2[o4],g2=d2[o4+1],b2=d2[o4+2];
          var mx=Math.max(r,g2,b2), mn=Math.min(r,g2,b2);
          if((mx-mn)<26 && mx>150) d2[o4+3]=0;
        }
      }
    }
    gg.putImageData(im,0,0);
    /* recadrage au plus juste */
    var x0=dw,y0=dh,x1=-1,y1=-1;
    for(var y3=0;y3<dh;y3++)for(var x3=0;x3<dw;x3++){
      if(d2[(y3*dw+x3)*4+3]>8){if(x3<x0)x0=x3;if(x3>x1)x1=x3;if(y3<y0)y0=y3;if(y3>y1)y1=y3;}}
    if(x1>x0&&y1>y0){
      var tw=x1-x0+1, th=y1-y0+1;
      var tp=document.createElement('canvas'); tp.width=tw; tp.height=th;
      tp.getContext('2d').drawImage(dcv,x0,y0,tw,th,0,0,tw,th);
      dcv.width=tw; dcv.height=th;
      var g3=dcv.getContext('2d'); g3.setTransform(1,0,0,1,0,0); g3.drawImage(tp,0,0);
    }
    return true;
  }catch(e){ return false; }
};
window.Toile.vue=function(){return {s:view.s,ox:view.ox,oy:view.oy,dpr:DPR};};
window.Toile.dalleTrame=function(dcv,pid,k,monde,opts){
  /* ⚑ v29 (Tom, 23 sept.) — DEUX AJOUTS AU MOTEUR, ET RIEN D'AUTRE.
     1 · `k` agrandit AUSSI les pas de trame (`UK`, voir plus haut) : une dalle se rend À SA TAILLE FINALE et se
         pose 1:1. Plus aucun appelant ne redimensionne (redteam_decoupe, famille B).
     2 · `opts` (facultatif) — ce que les appelants faisaient APRÈS le moteur, sur les pixels, le moteur le peint :
         · opts.rampe  = {cols:[[r,g,b]…], haut:h}  la clarté remappée sur une rampe (Q30 : haut 2 ; Q297 : 0,9 ou
                          la hauteur choisie). MÊME formule que `teinteDalle` et `_ingenuTeinte`, au pixel près.
         · opts.decale = {a:ca, b:cb}               la teinte déplacée en Lab, clarté gardée (chantier 59).
         · opts.donnees = true                       le moteur rend aussi SES pixels (`dcv.__dalleDonnees`) —
                          la Pelote en fait une fourrure, elle ne pose pas d'image.
     Et le moteur DÉCLARE ce qu'il a peint (`dcv.__dalleInfo`) : couleur la plus saturée, clarté moyenne, Lab
     moyen, part pleine — ce que les appelants relisaient au pixel (§7 : on lit la composition publiée). */
  /* Peint la matiere du design actif pour LA dalle du Promi demande,
     decoupee sur sa vraie cellule. Meme mecanique que Toile.repaint.

     LE MONDE D'ALORS -- 4 septembre 2026, decision Tom.
     `monde` est FACULTATIF : {m:design, p:palette, h:teinte}. Absent, la fonction se
     comporte EXACTEMENT comme avant -- les six appels existants ne bougent pas.
     Present, elle peint la dalle dans le monde de SA PLANTATION et non dans le monde
     courant : une dalle est figee au jour ou on l'a plantee, et changer de monde au
     Studio ne repeint pas les anciennes.
     On sauve et on restaure sur l'idiome que la fonction porte deja pour g/W/H/seeds/view.
     ATTENTION _palLit est un MEMO de la palette calculee : il doit etre invalide a
     l'aller (sinon la palette de l'appelant fuit dans la dalle) et restaure au retour
     (sinon celle de la dalle fuit dans la Toile). */
  /* ⚑ assainissement — une FONCTION PURE vue du dehors : (dcv, pid, k, monde, opts) → dcv peint + dcv.__dalleInfo.
     Tout ce qu'elle emprunte au moteur est pris d'un geste (_ctxPrend) et rendu d'un geste dans le `finally` (_ctxRend) :
     rien de global ne reste modifié, même sur une erreur, et elle est réentrante (_WT et _nAvg sont RENDUS, plus remis à null). */
  var C=_ctxPrend(), ok=false;
  var _W=C.W,_H=C.H,_s=C.seeds,_uk=C.UK; _WT=[_W,_H];
  /* ⚑ v30 (Tom, 23 sept.) — « UNE DALLE GARDE SON MONDE PARTOUT. » Sans monde fourni, la dalle se peint dans celui
     de SA PLANTATION (`p.monde`), jamais dans le monde courant du Studio : 22 appels sur 29 l'oubliaient. Seuls ceux
     qui montrent le monde courant EXPRÈS le passent eux-mêmes et le déclarent (`opts.courant`) — la page +, qui montre
     la dalle qu'on va planter, et les aperçus du Studio. Le monde réellement employé est publié (`__dalleInfo.monde`). */
  /* ⚑ v34 (Tom, 23 sept.) — LA RÈGLE S'INVERSE : « tout suit le Studio — le Fil, l'Index, la Toile, la Toile du Cercle, les
     fiches, la page +, Partager. Seule exception : l'Aura » (la Pelote et « Ce que tu as tenu » gardent le monde et la couleur
     de plantation — elles le passent EXPRÈS). Le monde de plantation n'est donc plus le défaut : il se demande (`opts.plantation`). */
  if(!monde && opts && opts.plantation){ try{ for(var _qi=0;_qi<promises.length;_qi++){ if(promises[_qi].id===pid){ if(promises[_qi].monde) monde=promises[_qi].monde; break; } } }catch(_){ } }
  try{
    if(monde){
      if(monde.m&&RD[monde.m])theme=monde.m;
      if(monde.p&&PALS[monde.p])palKey=monde.p;
      if(monde.h!=null)hueShift=+monde.h||0;
      _palLit=null;
    }
    var D=window.Toile.dalleAbs(pid); if(!D||!D.w||!D.h) throw 0;
    k=k||1;
    /* ⚑ v32 — Esquille, Bobinette, Madrure peignent EUX-MÊMES leur dalle seule (`seule`), en vecteurs, à sa taille finale :
       leur matière naît de toute la Toile, un découpage pondéré la trahirait. */
    if(_MN&&_MNLIB[theme]){ _dalleNeuve(dcv,pid,k,opts); } else {
    /* Sur la Toile, encre / terrazzo / touffe DEBORDENT de leur cellule :
       les decouper dessus les tronquait. On leur laisse une marge et aucun
       decoupage ; les mondes a trame restent contenus dans leur cellule. */
    var LIBRE=!!_rg('libre');
    var spReal=Math.sqrt(_W*_H/Math.max(1,_s.length))*k;
    var pad=Math.round(spReal*(LIBRE?0.85:0.30));   /* marge : la vraie cellule ponderee peut deborder du polygone */
    /* Les motifs a trame sont ancres sur les coordonnees absolues de la Toile
       (points tous les 9, tesselles tous les 11, carres tous les 5, sillons tous les 6).
       En deplacant la cellule il faut donc translater d'un multiple de la periode,
       sinon le motif ne retombe pas au meme endroit que sur la Toile. */
    var PER=(_rg('pasTrame')||0)*k;   /* ⚑ v29 : le pas suit k (UK) */
    var padX=pad, padY=pad;
    if(PER){
      /* alignement EXACT, fractions comprises : un arrondi suffit a decaler un motif a gros pas.
         ⚑ v29 : a tout k — la grille de la Toile (multiples de PER) tombe sur celle de la dalle (multiples de PER·k). */
      padX=pad+((D.minx*k-pad)%PER+PER)%PER;
      padY=pad+((D.miny*k-pad)%PER+PER)%PER;
    }
    var dw=Math.ceil(D.w*k+2*padX), dh=Math.ceil(D.h*k+2*padY);
    dcv.width=Math.round(dw*DPR); dcv.height=Math.round(dh*DPR);
    seeds=_s.map(function(s){var o={};for(var q in s)o[q]=s[q];
      o.x=(s.x-D.minx)*k+padX; o.y=(s.y-D.miny)*k+padY;
      o.px=(s.px!=null)?((s.px-D.minx)*k+padX):null;
      o.py=(s.py!=null)?((s.py-D.miny)*k+padY):null;
      o.w=(s.w||0)*k; return o;});
    W=dw; H=dh; view={s:1,ox:0,oy:0};
    if(LIBRE){
      var ti=-1;
      for(var z=0;z<seeds.length;z++){if(seeds[z].pid===pid&&seeds[z].kind!=='gray'){ti=z;break;}}
      if(ti>=0){
        for(var z2=0;z2<seeds.length;z2++){ if(z2===ti) continue;
          seeds[z2].x=-1e7; seeds[z2].y=-1e7; seeds[z2].px=null; seeds[z2].py=null; }
        /* sp doit valoir celui de la Toile : sp = racine(W*H / nombre de graines) */
        var nn=Math.max(1,seeds.length);
        W=spReal*Math.sqrt(nn); H=W;
      }
    }
    /* ⚑ v29 — LES VOISINES SEULES. Rendue à sa taille finale, une dalle a beaucoup de pixels ; chercher leur graine
       propriétaire parmi TOUTES les graines coûtait 1,9 s pour une dalle Pixel de 200 px (mesuré). Or une graine k ne
       peut posséder AUCUN point du canevas si |t−k| ≥ 2·Rmax + w_k − w_t (Rmax : la distance de la graine t au coin le
       plus lointain) — inégalité triangulaire. On ne passe donc au monde et au masque que les graines sous cette borne :
       l'appartenance à LA cellule est exacte, au pixel. `avg()` garde le nombre de graines de la Toile. */
    if(!LIBRE){
      var _tg=null; for(var z3=0;z3<seeds.length;z3++){ if(seeds[z3].pid===pid&&seeds[z3].kind!=='gray'){ _tg=seeds[z3]; break; } }
      if(_tg){
        var _Rm=0; [[0,0],[dw,0],[0,dh],[dw,dh]].forEach(function(c){ _Rm=Math.max(_Rm, Math.hypot(c[0]-_tg.x, c[1]-_tg.y), Math.hypot(c[0]-(_tg.px!=null?_tg.px:_tg.x), c[1]-(_tg.py!=null?_tg.py:_tg.y))); });
        var _cand=seeds.filter(function(s){ if(s===_tg) return true;
          var dd=Math.min(Math.hypot(s.x-_tg.x, s.y-_tg.y), Math.hypot((s.px!=null?s.px:s.x)-(_tg.px!=null?_tg.px:_tg.x), (s.py!=null?s.py:s.y)-(_tg.py!=null?_tg.py:_tg.y)));
          return dd < 2*_Rm + (s.w||0) - (_tg.w||0) + 2; });
        _nAvg=seeds.length; seeds=_cand;
      }
    }
    g=dcv.getContext('2d',{willReadFrequently:true}); if(!g) throw 0;   /* ⚑ v100 — la dalle est RELUE trois fois (masque exact, recadrage, finition) : déclarée dès la création, elle vit en mémoire processeur et chaque relecture cesse d'être un rapatriement depuis la carte graphique. Mesuré : 1re ouverture d'une Nuée, 2 à 3 s de gel dont 2 s de getImageData. */
    g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,dw,dh);
    g.save();
    var _bT=[(0-D.minx)*k+padX,(0-D.miny)*k+padY,(_W-D.minx)*k+padX,(_H-D.miny)*k+padY];
    UK=k; _cibleDalle=pid; _bordsDalle=_bT;
    try{ RD[theme](performance.now(),0,0,dw,dh); }finally{ _cibleDalle=null; _bordsDalle=null; } UK=_uk;   /* ⚑ v34 : et les bords de la Toile, dans le repère de la dalle */   /* ⚑ v32 : la graine de la dalle, nommée au monde (Ritournelle ne peint qu'elle) */
    g.restore();
    if(!LIBRE){
      /* Le moteur attribue chaque pixel a la graine la plus proche AU SENS PONDERE
         (distance moins poids). Le polygone de _cellPoly n'en est qu'une approximation :
         des que les poids different, la vraie frontiere est courbe. On refait donc
         l'attribution pixel par pixel, avec la regle exacte du moteur. */
      var tg2=null;
      for(var z2=0;z2<seeds.length;z2++){if(seeds[z2].pid===pid&&seeds[z2].kind!=='gray'){tg2=seeds[z2];break;}}
      if(tg2){
        var img2=g.getImageData(0,0,dcv.width,dcv.height), dd=img2.data;
        var iw=dcv.width, ih=dcv.height, sx2=dw/iw, sy2=dh/ih, ns=seeds.length;
        /* ⚑ v29 — MÊME RÈGLE, MÊME RÉSULTAT, moins de calcul. Un point p appartient à la cible t sauf si une graine k
           y fait mieux : |p−k|−w_k < |p−t|−w_t. Comme |p−k| ≥ |t−k|−|p−t|, seule une graine avec
           |t−k| − w_k + w_t < 2·|p−t| peut gagner. On range les autres graines sur cette clé : pour chaque pixel on
           s'arrête à la première qui ne peut plus gagner — au cœur de la cellule, il n'y en a presque aucune. */
        var _tw=(tg2.w||0), _ord=[];
        for(var q2=0;q2<ns;q2++){ var sq0=seeds[q2]; if(sq0===tg2) continue;
          _ord.push({s:sq0, e:Math.hypot(sq0.x-tg2.x, sq0.y-tg2.y)-(sq0.w||0)+_tw}); }
        _ord.sort(function(a,b){ return a.e-b.e; });
        var _no=_ord.length;
        for(var yy=0;yy<ih;yy++){
          var ly=(yy+0.5)*sy2;
          for(var xx=0;xx<iw;xx++){
            var o4=(yy*iw+xx)*4;
            if(dd[o4+3]===0) continue;
            var lx=(xx+0.5)*sx2, ex0=lx-tg2.x, ey0=ly-tg2.y, r0=Math.sqrt(ex0*ex0+ey0*ey0), dt=r0-_tw, lim=2*r0, perd=false;
            /* ⚑ v34 — une cellule du BORD n'a pas de fin : sa dalle s'arrête au bord de la Toile, là où l'écran l'arrête, et plus
               au hasard de la marge du canevas (depuis que la Toile n'est faite que de promesses, presque toutes touchent le bord). */
            if(lx<_bT[0]||lx>_bT[2]||ly<_bT[1]||ly>_bT[3]){ dd[o4+3]=0; continue; }
            for(var q3=0;q3<_no;q3++){ var oq=_ord[q3]; if(oq.e>=lim) break; var sq=oq.s;
              var ex=lx-sq.x, ey=ly-sq.y;
              if(Math.sqrt(ex*ex+ey*ey)-(sq.w||0)<dt){ perd=true; break; } }
            if(perd) dd[o4+3]=0;
          }
        }
        g.putImageData(img2,0,0);
      }
    }
    /* on recadre au plus juste sur la matiere : plus aucune marge morte */
    try{
      var im=g.getImageData(0,0,dcv.width,dcv.height).data;
      var x0=dcv.width,y0=dcv.height,x1=-1,y1=-1;
      for(var yy=0;yy<dcv.height;yy++)for(var xx=0;xx<dcv.width;xx++){
        if(im[(yy*dcv.width+xx)*4+3]>8){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(yy<y0)y0=yy;if(yy>y1)y1=yy;}}
      if(x1>x0&&y1>y0){
        var tw=x1-x0+1, th=y1-y0+1;
        var tmp=document.createElement('canvas'); tmp.width=tw; tmp.height=th;
        tmp.getContext('2d').drawImage(dcv,x0,y0,tw,th,0,0,tw,th);
        dcv.width=tw; dcv.height=th;
        var g2=dcv.getContext('2d'); g2.setTransform(1,0,0,1,0,0); g2.clearRect(0,0,tw,th);
        g2.drawImage(tmp,0,0);
      }
    }catch(e){}
    try{ _dalleFinit(dcv, opts||null); dcv.__dalleInfo.monde={m:theme,p:palKey,h:hueShift}; dcv.__dalleInfo.courant=!!(opts&&opts.courant); }catch(e){}
    }
    ok=true;
  }catch(e){}
  finally{ _ctxRend(C); }
  return ok;
};
/* ⚑ v100 (Tom : « deux à trois secondes où l'app se fige ») — LE MOTEUR RETIENT SES RENDUS UN INSTANT. À l'ouverture d'une Nuée,
   la fiche, son fil et ses vignettes se reposent deux à trois fois en 200 ms, et leurs peintres appellent `dalleTrame` en
   direct, sans cache : les MÊMES dalles (même id, même k, même taille) étaient rendues deux à trois fois — 130 ms par passe,
   mesuré. Même rendu demandé dans les 1,5 s — même dalle, même k, même monde, mêmes options, même palette, même thème, même
   boîte au demi-pixel, même couleur — : l'image est RECOPIÉE 1:1 dans le canevas demandé, avec ce que le moteur déclare
   (`__dalleInfo`). Rien n'est redimensionné ni découpé. La Pelote (`opts.donnees`) lit les données du rendu : elle passe
   toujours par le moteur. Le délai court borne ce que la clé ne voit pas (la matière respire). */
(function(){
  var _dt=window.Toile.dalleTrame, MEMO={}, ORD=[];
  function cleM(pid,k,monde,opts){
    var D=null, C='', M={}; try{ D=Toile.dalleAbs(pid); C=String(Toile.colorOf?Toile.colorOf(pid):''); M=Toile.mondeCourant()||{}; }catch(_){ }
    var clair=!!(document.getElementById('device')&&document.getElementById('device').classList.contains('light'));
    return [pid, Math.round((+k||1)*1000), JSON.stringify(monde||null), JSON.stringify(opts||null), M.m, M.p, M.h, clair,
            D?[D.minx,D.miny,D.w,D.h].map(function(v){ return Math.round(v*2); }).join(','):'', C, window.devicePixelRatio||1].join('|');
  }
  window.Toile.dalleTrame=function(dcv,pid,k,monde,opts){
    if(!dcv || (opts && opts.donnees)) return _dt.apply(this,arguments);
    var c; try{ c=cleM(pid,k,monde,opts); }catch(_){ return _dt.apply(this,arguments); }
    var m=MEMO[c], t=performance.now();
    if(m && t-m.t<1500){
      try{ dcv.width=m.cv.width; dcv.height=m.cv.height;
           var gx=dcv.getContext('2d',{willReadFrequently:true}); gx.setTransform(1,0,0,1,0,0); gx.clearRect(0,0,dcv.width,dcv.height);
           gx.drawImage(m.cv,0,0);
           var inf={}; for(var q in (m.info||{})) inf[q]=m.info[q]; dcv.__dalleInfo=inf; return true; }catch(_){ }
    }
    var r=_dt.apply(this,arguments);
    try{ if(r && dcv.width && dcv.height){
      var cp=document.createElement('canvas'); cp.width=dcv.width; cp.height=dcv.height; cp.getContext('2d').drawImage(dcv,0,0);
      if(!MEMO[c]) ORD.push(c); MEMO[c]={cv:cp, info:dcv.__dalleInfo||null, t:t}; if(ORD.length>40) delete MEMO[ORD.shift()]; } }catch(_){ }
    return r;
  };
}());   /* (fermée ainsi, et non par « })(); » en début de ligne : redteam_decoupe borne le moteur à la première ligne qui commence par là) */
/* ⚑ v32 — LA DALLE SEULE D'UN MONDE LIBRE NEUF. Le canevas prend la boîte RÉELLEMENT peinte (`boite`, bobines et liserés
   compris) à l'échelle k, plus un pixel ; `seule` y cale la boîte du contour. Aucune image lue, aucune découpe : on appelle
   le monde sur la Toile même (graines vraies, W et H vrais), seul le contexte change. Échoue (throw) si le monde n'a pas de
   dalle pour cette graine — `dalleTrame` rend alors false. */
function _dalleNeuve(dcv,pid,k,opts){
  var ts=null; for(var q=0;q<seeds.length;q++){ if(seeds[q].pid===pid&&seeds[q].kind!=='gray'){ ts=seeds[q]; break; } }
  if(!ts) throw 0;
  var B=_MN.boite(theme,ts); if(!B) throw 0;
  /* la marge suit k : fixe (1 px), elle rendait la taille non proportionnelle à k, et la seconde passe de `_rendDalle`
     tombait 4 px court — l'Aura (`width:auto`, plafond 64) étirait alors la dalle de 3 % (redteam_decoupe, famille G). */
  var pd=0.5*k, dw=(B.x1-B.x0)*k+2*pd, dh=(B.y1-B.y0)*k+2*pd;   /* arrondi au pixel d'APPAREIL : au pixel CSS, 2 px d'écart de plus */
  dcv.width=Math.max(1,Math.ceil(dw*DPR)); dcv.height=Math.max(1,Math.ceil(dh*DPR)); dw=dcv.width/DPR; dh=dcv.height/DPR;
  g=dcv.getContext('2d'); if(!g) throw 0;
  g.setTransform(DPR,0,0,DPR,0,0); g.clearRect(0,0,dw,dh);
  var cx=((B.fx0+B.fx1)/2-B.x0)*k+pd, cy=((B.fy0+B.fy1)/2-B.y0)*k+pd, taille=Math.max(B.fx1-B.fx0,B.fy1-B.fy0)*k;
  if(!_MN.seule(theme,ts,performance.now(),cx,cy,taille)) throw 0;
  /* ⚑ v55 (Tom) — l'œil de Madrure garde les couleurs EXACTES de la Toile, fini sur son trait sombre : la teinture de Q30
     (rampe de la nature) rabattait ses strates voisines sur un même ton et éclaircissait le trait (mesuré : une dalle de Chiche
     sortait en disque uni). C'est le trait sombre qui la détache du champ. */
  _dalleFinit(dcv, (_rg('donneesPropres')&&opts)?{donnees:opts.donnees}:(opts||null));
  dcv.__dalleInfo.monde={m:theme,p:palKey,h:hueShift}; dcv.__dalleInfo.courant=!!(opts&&opts.courant);
  dcv.__dalleInfo.nature=_rg('donneesPropres')?_MN.nature(theme,ts):'dalle';
}
/* ⚑ v29 — LA FIN D'UNE DALLE, DANS LE MOTEUR : la rampe ou le décalage (opts), puis ce qu'il déclare avoir peint. */
function _dLin(v){ v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4); }
function _dFl(t){ return t>0.008856?Math.pow(t,1/3):7.787*t+16/116; }
function _dLab(r,g2,b){ r=_dLin(r); g2=_dLin(g2); b=_dLin(b);
  var X=(0.4124*r+0.3576*g2+0.1805*b)/0.95047, Y=0.2126*r+0.7152*g2+0.0722*b, Z=(0.0193*r+0.1192*g2+0.9505*b)/1.08883;
  var fx=_dFl(X), fy=_dFl(Y), fz=_dFl(Z); return [116*fy-16, 500*(fx-fy), 200*(fy-fz)]; }
function _dFi(t){ var t3=t*t*t; return t3>0.008856?t3:(t-16/116)/7.787; }
function _dO(v){ v=v<=0.0031308?12.92*v:1.055*Math.pow(Math.max(0,v),1/2.4)-0.055; return v<0?0:(v>1?255:Math.round(v*255)); }
function _dRgb(L,a,b){ var fy=(L+16)/116, fx=fy+a/500, fz=fy-b/200;
  var X=_dFi(fx)*0.95047, Y=_dFi(fy), Z=_dFi(fz)*1.08883;
  return [_dO(3.2406*X-1.5372*Y-0.4986*Z), _dO(-0.9689*X+1.8758*Y+0.0415*Z), _dO(0.0557*X-0.2040*Y+1.0570*Z)]; }
function _dalleFinit(dcv, o){
  var gg=dcv.getContext('2d'); if(!gg||!dcv.width||!dcv.height) return;
  var im=gg.getImageData(0,0,dcv.width,dcv.height), d=im.data, i, L;
  if(o && o.rampe && o.rampe.cols && o.rampe.cols.length>1){
    /* la clarté normalisée par l'étendue de la dalle, puis t = min(2, L·haut)/2 · (n−1) sur la rampe */
    var pal=o.rampe.cols, h=(o.rampe.haut!=null?o.rampe.haut:2), mn=255, mx=0;
    /* ⚑ v34 — l'étendue se lit entre les centiles 5 et 95 : quelques pixels de bord (0,3 % sur une dalle Pixel) suffisaient
       à étirer mn–mx et à rabattre toute la dalle sur le premier ton. */
    /* (les centiles servent SEULEMENT à reconnaître une dalle d'une couleur ; la normalisation reste le min–max d'origine —
       la changer déplaçait la clarté des îles de la Pelote, mesuré par releve-aura : ΔE 13 au lieu de 27 en sombre) */
    var HL=new Uint32Array(256), nL=0;
    for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; L=0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2]; HL[L|0]++; nL++; if(L<mn) mn=L; if(L>mx) mx=L; }
    var cum=0, q5=nL*0.05, q95=nL*0.95, p5=-1, p95=0; for(var bi=0;bi<256;bi++){ cum+=HL[bi]; if(p5<0&&cum>=q5) p5=bi; if(cum>=q95){ p95=bi+1; break; } } if(p5<0) p5=0;
    var et=(mx-mn)||1, uni=(p95-p5)<12 && h>=2;   /* seulement les bandes de Q30 (rampe pleine, haut 2) : la Pelote (0,85) y perdait ses îles, ΔE 7 */   /* ⚑ v34 — une dalle d'UNE couleur (Pixel, Mosaïque…) n'a pas d'étendue de clarté : normalisée,
       elle tombait toute sur le PREMIER ton de la rampe — le plus proche du champ (lilas sur lilas : `(194,164,247)` sur `#C9A8F5`, vu
       sur « + Nuée »). Elle prend le ton le plus haut, celui qui se détache du champ (Q30 : zéro ton sur ton). */
    for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue;
      L=uni?1:(0.2126*d[i]+0.7152*d[i+1]+0.0722*d[i+2]-mn)/et;
      var t=Math.min(2,L*h)/2*(pal.length-1), kk=Math.min(pal.length-2,Math.floor(t)), f=Math.min(1,t-kk), a=pal[kk], z=pal[kk+1];
      d[i]=a[0]+(z[0]-a[0])*f; d[i+1]=a[1]+(z[1]-a[1])*f; d[i+2]=a[2]+(z[2]-a[2])*f; }
    gg.putImageData(im,0,0);
  } else if(o && o.decale && o.decale.a!=null){
    /* chaque pixel garde sa CLARTÉ et son écart de teinte au centre du nuage ; le nuage va en (a, b) */
    var n=0, sa=0, sb=0, q;
    for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; q=_dLab(d[i],d[i+1],d[i+2]); n++; sa+=q[1]; sb+=q[2]; }
    if(n){ var ma=sa/n, mb=sb/n;
      for(i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; q=_dLab(d[i],d[i+1],d[i+2]);
        var e=_dRgb(q[0], o.decale.a+(q[1]-ma), o.decale.b+(q[2]-mb)); d[i]=e[0]; d[i+1]=e[1]; d[i+2]=e[2]; }
      gg.putImageData(im,0,0); }
  }
  /* ce que le moteur a peint — lu par les appelants à la place des pixels.
     Le Lab moyen coûte (trois puissances par pixel) : il n'est calculé que pour qui demande les données (la Pelote). */
  var _avecLab=!!(o&&o.donnees);
  var bs=-1, sr=0, sv=0, sb2=0, nL=0, sL=0, nb=0, lL=0, la=0, lb=0, tot=d.length/4;
  for(i=0;i<d.length;i+=4){
    var r=d[i], v=d[i+1], b=d[i+2], al=d[i+3];
    if(al>=120){ var M=Math.max(r,v,b), m=Math.min(r,v,b); if(M>=26&&m<=246){ var s=(M-m)/M; if(s>bs){ bs=s; sr=r; sv=v; sb2=b; } } }
    if(al>200 && (i/4)%11===0){ nL++; sL+=0.2126*r+0.7152*v+0.0722*b; }
    if(_avecLab && al>=24 && (i/4)%4===0){ var q2=_dLab(r,v,b); nb++; lL+=q2[0]; la+=q2[1]; lb+=q2[2]; }
  }
  var pleins=0; for(i=3;i<d.length;i+=4) if(d[i]>=24) pleins++;
  dcv.__dalleInfo={sat:bs>=0?[sr,sv,sb2]:null, satS:bs, lum:nL>40?sL/nL:null, lab:nb?[lL/nb,la/nb,lb/nb]:null, plein:pleins/tot};
  dcv.__dalleDonnees=(o&&o.donnees)?new Uint8ClampedArray(d):null;
}
/* le monde courant, en LECTURE SEULE : ce qu'on fige sur un Promi a sa plantation */
window.Toile.mondeCourant=function(){return {m:theme,p:palKey,h:hueShift};};
/* ⚑ v69 (Tom, 27 sept.) — UN APERÇU DU STUDIO DONNE ENVIE : peu de dalles, des tailles franchement différentes. Les mondes de la
   saison 2 tirent la taille d'une dalle de SA CLÉ (la place R de la planche) et ignorent le poids : sur un aperçu, rien ne variait.
   Un seul propriétaire : une graine d'APERÇU (`s.apercu`) porte un facteur tiré de son poids ; toute graine de la vraie Toile rend 1,
   au pixel près. */
window._tailleApercu=function(s){ if(!s||!s.apercu||!(s.w>0)) return 1; var k=Math.max(0.55,Math.min(1.9,Math.sqrt(s.w/8)));
  /* ⚑ v94 (Tom, iPhone : « la Toile aléatoire : les fleurs de Volubilis prennent tout l'écran. Mets-y uniquement des petites fleurs — une
     exception à Volubilis ») — au Studio seulement (une graine d'aperçu), l'écart de taille gardé, ramené aux petites fleurs */
  return _rg('apercuPetit')?Math.max(0.32,Math.min(0.62,k*0.5)):k; };
window._apercuClair={ritournelle:1,halin:1,brouillamini:1,chamade:1,volubilis:1,guingois:1,chantourne:1,mascaret:1,ramage:1,esquille:1,bobinette:1};   /* tous les mondes neufs — ⚑ v92 (Tom : « remets l'animation de la toute première intégration ») : Madrure revient à son exception d'origine (v75–v82), la grille de 72 graines dont 10 nœuds font l'onde ; le semis clairsemé (v83) retournait tout le champ à chaque événement */
/* ⚑ v83 (Tom : « Madrure ne s'anime toujours pas au Studio ») — son aperçu était une grille de 72 cellules dont DIX seulement font l'onde
   (v40) : une arrivée poussait ses voisines immédiates — presque toujours des cellules sans effet sur l'onde. Seule une petite bosse
   montait ; le reste ne bougeait pas (vu à l'écran, par le vrai chemin, en Chromium et en WebKit). Son aperçu prend le semis clairsemé des
   mondes neufs : une dizaine de dalles, TOUTES des nœuds — l'exception de v40 (« quelques nœuds, beaucoup de lignes ») est gardée, et la
   poussée déplace maintenant des nœuds : l'onde entière se réécoule, comme sur la vraie Toile. L'écartement des lignes ne dépend pas du
   nombre de cellules (l'unité de la Toile, `env.uMat`). */
window.Toile.preview=function(pcv,th,pw,ph){if(!TH[th])th='pixel';var _g=g,_W=W,_H=H,_s=seeds,_t=theme,_v={s:view.s,ox:view.ox,oy:view.oy};try{g=pcv.getContext('2d');W=pw;H=ph;theme=th;view={s:1,ox:0,oy:0};var dpr=pcv.width/pw;seeds=[];var base=Math.max(20,pw/5.5),gc=Math.max(2,Math.round(pw/base)),gr=Math.max(2,Math.round(ph/base)),cw=pw/gc,ch=ph/gr;for(var r=0;r<gr;r++)for(var c=0;c<gc;c++)seeds.push(mk(cw*(c+.5)+(_alea()-.5)*cw*.42,ch*(r+.5)+(_alea()-.5)*ch*.42));/* ⚑ v55 (Tom : « au Studio, les aperçus de Ritournelle et Halin sont trop chargés et trop réguliers — toutes les dalles font la
   même taille ; ce n'est pas fidèle à la Toile ») — une grille à peine bousculée, poids tous nuls. Ces deux mondes ont une Toile
   faite de ses paroles : leur aperçu en pose une comme la vraie — le nombre de cellules d'une Toile d'une vingtaine de paroles,
   semées librement, de poids variés (surtout des paroles, quelques moyennes, de rares grandes comme une Nuée). */
if(window._apercuClair&&window._apercuClair[th]){ seeds=[]; var _AP=window._apercuSemis||{n:10,w:[[0.2,34],[0.5,12],[1,2]],d:0.55};   /* v69 : ~10 dalles à plein écran (21 avant), un cinquième de grandes, un tiers de moyennes, le reste petites */ var _na=Math.max(6,Math.round(pw*ph/(390*844)*_AP.n)), _dm=Math.sqrt(pw*ph/_na)*_AP.d, _tr=0;
  while(seeds.length<_na&&_tr<4000){ _tr++; var _x=pw*(0.03+_alea()*0.94), _y=ph*(0.03+_alea()*0.94), _ok=true;
    for(var _q=0;_q<seeds.length;_q++){ if(Math.hypot(seeds[_q].x-_x,seeds[_q].y-_y)<_dm){ _ok=false; break; } }
    if(!_ok) continue; var _sa=mk(_x,_y), _rw=_alea(); var _wv=_AP.w[_AP.w.length-1][1]; for(var _wi=0;_wi<_AP.w.length;_wi++){ if(_rw<_AP.w[_wi][0]){ _wv=_AP.w[_wi][1]; break; } } _sa.w=_sa.wt=_sa.wFin=_wv*(0.85+_alea()*0.3); seeds.push(_sa); } }   /* ⚠ pas `_s` : c'est la réserve des graines de la vraie Toile */var cx=pw*(0.28+_alea()*0.44),cy=ph*(0.34+_alea()*0.26);var cen=seeds.filter(function(s){return s.y>ph*0.2&&s.y<ph*0.72&&s.x>pw*0.06&&s.x<pw*0.94;});cen.forEach(function(s){s._sc=((s.x-cx)*(s.x-cx)+(s.y-cy)*(s.y-cy))*(0.35+_alea()*1.6);});cen.sort(function(a,b){return a._sc-b._sc;});var nc=11+(_alea()*2|0);   /* 5 dalles colorées de plus dans le Studio */for(var i=0;i<nc&&i<cen.length;i++){var s=cen[i];s.ci=cc(s);s.c=PAL[s.ci];s.kind='promi';s.t0=-99999;}var far=cen.slice(Math.floor(cen.length*0.55));var det=1+(_alea()*2|0);for(var f=0;f<det&&far.length;f++){var ss2=far[(_alea()*far.length)|0];if(ss2&&ss2.ci==null){ss2.ci=cc(ss2);ss2.c=PAL[ss2.ci];ss2.kind='promi';ss2.t0=-99999;}}if(window._shAllColored){for(var _ac=0;_ac<seeds.length;_ac++){var _sac=seeds[_ac];if(_sac.ci==null){_sac.ci=cc(_sac);_sac.c=PAL[_sac.ci];_sac.kind='promi';_sac.t0=-99999;}}}
/* ⚑ v25 (Tom, 22 sept.) — UN APERÇU N'EST PAS UNE TOILE DE PAROLES, ET IL SE DÉCLARE.
   L'exception Ingénu (v17) fait dire la NATURE à la couleur : `cOf` lit `s.nat`, et une
   cellule sans nature prend le crème dalle — la règle juste pour la vraie Toile (« une
   cellule colorée qui ne porte aucune parole »). Mais l'aperçu du Studio n'a AUCUNE parole :
   toutes ses cellules tombaient sur le crème, et le fond du Studio est devenu beige uni.
   Mesuré par bissection : 47,9 % de pixels colorés avant le lot v17, 11,4 % après.
   On marque donc les graines d'aperçu ; `cOf` leur rend la rotation de la palette. */
for(var _ap=0;_ap<seeds.length;_ap++) seeds[_ap].apercu=1;
tones();try{pcv.__c={seeds:seeds.map(function(s){return {x:s.x,y:s.y,gray:s.gray,gc:null,ci:s.ci,c:s.c,kind:s.kind,tone:s.tone,lit:s.lit,shade:s.shade,ang:s.ang,w:s.w,apercu:1,t0:-99999};}),th:th,pw:pw,ph:ph};}catch(e){}g.setTransform(dpr,0,0,dpr,0,0);g.clearRect(0,0,pw,ph);/* ⚑ v26 (Tom, 22 sept.) — LE FOND D'UN APERÇU EST CELUI DE LA VRAIE TOILE.
   Il était peint en `#120E05` (l'encre profonde) alors que la Toile de l'accueil laisse
   voir le fond du mode, `#201908` — 16 niveaux de luminance plus clair. Sur Encre,
   Pixel ou Mosaïque on ne le voit jamais : la matière couvre tout. Sur BRAILLE, dont
   les pois ne couvrent que **34,9 %** de la surface (pas 9 px, rayon 2,9 — mesuré,
   inchangé depuis le lot v14), les 65 % restants SONT ce fond : il se lisait comme un
   voile sombre, et les pois paraissaient petits et ternes. Même remarque pour Touffe. */
g.fillStyle=isLightM()?(window._shAllColored?'#DDD2B8':'#F1ECD9'):'#050302';g.fillRect(0,0,pw,ph);if(!pcv.__vif&&!pcv.__compose)RD[th](performance.now(),0,0,pw,ph);}catch(e){}g=_g;W=_W;H=_H;seeds=_s;theme=_t;view=_v;if(pcv.__vif&&!pcv.__compose){try{window.Toile.apercuImage(pcv);}catch(_){}}};   /* v75 : un aperçu VIVANT ne peint pas d'image fixe — sa première image vivante, tout de suite, dans la même tâche */

var ptrs={},pinch=null;function cp(){var mx=0,my=0;var lx=Math.min(0,W-W*view.s),hx=Math.max(0,W-W*view.s);view.ox=Math.max(lx-mx,Math.min(hx+mx,view.ox));var ly=Math.min(0,H-H*view.s),hy=Math.max(0,H-H*view.s);view.oy=Math.max(ly-my,Math.min(hy+my,view.oy));}
host.style.touchAction='none';
/* ⚑ v46 — LES DOIGTS, EN COORDONNÉES DE LA TOILE : l'appareil peut être réduit (la fenêtre de l'app, mesuré à 0,72) — pris en
   pixels d'écran, le zoom glissait sous les doigts. Pincement élastique au-delà des bornes, glissé élastique aux bords,
   élan au lâcher (vitesse des 100 dernières ms, à l'heure de l'événement), retour dans les bornes par ressort (frame). */
function _loc(e){ var r=host.getBoundingClientRect(), f=r.width?W/r.width:1; return {x:(e.clientX-r.left)*f, y:(e.clientY-r.top)*f, t:e.timeStamp||performance.now()}; }
function _bornesPan(){ var s=view.s; return s>=1 ? [W-W*s,0,H-H*s,0] : [(W-W*s)/2,(W-W*s)/2,(H-H*s)/2,(H-H*s)/2]; }
host.addEventListener('pointerdown',function(e){e.stopPropagation();try{host.setPointerCapture(e.pointerId);}catch(_){}vTarget=null;_inert=null;window._panMain=0;   /* le doigt reprend la main : le cadrage automatique lâche prise */
  ptrs[e.pointerId]=_loc(e);var k=Object.keys(ptrs);
  if(k.length===2){var a=ptrs[k[0]],b=ptrs[k[1]];pinch={d:Math.hypot(a.x-b.x,a.y-b.y)||1,s:view.s,cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,ox:view.ox,oy:view.oy};_pan=null;}
  else if(k.length===1){_pan={ox:view.ox,oy:view.oy,h:[[ptrs[k[0]].t,ptrs[k[0]].x,ptrs[k[0]].y]]};}
  kick();});
host.addEventListener('pointermove',function(e){if(!ptrs[e.pointerId])return;e.stopPropagation();var pr=ptrs[e.pointerId],L=_loc(e);ptrs[e.pointerId]=L;var k=Object.keys(ptrs);
  if(k.length===2&&pinch){var a=ptrs[k[0]],b=ptrs[k[1]];var d=Math.hypot(a.x-b.x,a.y-b.y);var raw=pinch.s*d/pinch.d;
    var ns=raw<ZMIN?ZMIN*Math.pow(raw/ZMIN,0.3):(raw>ZMAX?ZMAX*Math.pow(raw/ZMAX,0.3):raw);   /* au-delà des bornes, la Toile résiste */
    var cx=(a.x+b.x)/2,cy=(a.y+b.y)/2;view.ox=cx-(pinch.cx-pinch.ox)*(ns/pinch.s);view.oy=cy-(pinch.cy-pinch.oy)*(ns/pinch.s);view.s=ns;kick();window._vueMain=true;}
  else if(k.length===1&&_pan){var dx=L.x-pr.x,dy=L.y-pr.y;_pan.ox+=dx;_pan.oy+=dy;var B=_bornesPan();view.ox=_rub(_pan.ox,B[0],B[1]);view.oy=_rub(_pan.oy,B[2],B[3]);
    _pan.h.push([L.t,L.x,L.y]);while(_pan.h.length>2&&L.t-_pan.h[0][0]>100)_pan.h.shift();kick();
    window._panMain=(window._panMain||0)+Math.abs(dx)+Math.abs(dy);if(window._panMain>10)window._vueMain=true;}   /* ⚑ Q212 : la vue appartient à la main dès qu'elle la déplace vraiment — jamais sur un toucher */
});
function pu(e){e.stopPropagation();var L=ptrs[e.pointerId];delete ptrs[e.pointerId];var k=Object.keys(ptrs);
  if(k.length<2)pinch=null;
  if(k.length===1){var r1=ptrs[k[0]];_pan={ox:view.ox,oy:view.oy,h:[[r1.t,r1.x,r1.y]]};}   /* du pincement au glissé, sans saut */
  else if(!k.length){ if(_pan&&_pan.h.length>1&&window._panMain>10){var h0=_pan.h[0],h1=_pan.h[_pan.h.length-1],dt=(h1[0]-h0[0])/1000;
      if(dt>0.008){var vx=(h1[1]-h0[1])/dt,vy=(h1[2]-h0[2])/dt,vm=Math.hypot(vx,vy);if(vm>2400){vx*=2400/vm;vy*=2400/vm;}if(vm>60)_inert={vx:vx,vy:vy};}}
    _pan=null;kick();}}
host.addEventListener('pointerup',pu);host.addEventListener('pointercancel',pu);
window.addEventListener('resize',size);
setTimeout(size,60);
})();

/* ══════════════════ bloc « lot-V31-CLE » ══════════════════ */
/* ⚑ v31 (Tom, 23 sept. 2026) — LA CLÉ D'UNE TOILE, pour les mondes qui tirent un paramètre global (l'angle de l'onde
   de Madrure). Stable pour une Toile donnée, ET qui ne bouge pas quand on plante : on ne la tire donc ni des graines
   (le semis est refait à chaque chargement et à chaque plantation, CONTRAT-MONDE §7.2), ni d'une horloge, ni d'un
   `Math.random`. Elle vient de la graine de l'utilisateur, SAUVEGARDÉE (`promi_graine`, `_grainePropre`) — la même
   depuis la première ouverture —, hachée avec un sel à elle (FNV-1a) pour ne pas se confondre avec le visage.
   Hors du moteur : `window.Toile.cle()` → un entier 32 bits non signé. `Toile.cleUnite()` → le même, ramené à [0, 1). */
(function(){
  function fnv(s){ var h=2166136261; for(var i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return h>>>0; }
  function arme(){ if(!window.Toile||window.Toile.cle) return;
    window.Toile.cle=function(){ var g=0; try{ g=(window.USER&&USER.seed!=null)?USER.seed:(window._grainePropre?_grainePropre():0); }catch(_){ }
      return fnv('toile|'+g); };
    window.Toile.cleUnite=function(){ return window.Toile.cle()/4294967296; }; }
  arme(); if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',arme); setTimeout(arme,0);
})();

/* ══════════════════ bloc « lot-V29-DALLE » ══════════════════ */
/* ══ v29 (Tom, 23 sept. 2026) — UNE DALLE SE REND À SA TAILLE FINALE ET SE POSE 1:1 ══════════════════════
   « Une dalle est peinte par le moteur, dans sa cellule, avec son propre contour, à sa taille finale. Jamais une
     image rognée, jamais un canevas recadré, jamais un morceau de Toile. »
   UN SEUL POSEUR pour tous les appelants (§7 : un propriétaire). On calcule la taille visée EN PIXELS DE
   L'APPAREIL (cotes × transformation du contexte), on demande au moteur la dalle à ce `k` — il agrandit aussi les
   pas de trame (UK) — puis on la pose à 1:1, au pixel entier, rotation gardée. Contrôlé par redteam_decoupe.py.
   `o` : {monde, rampe, decale, donnees, haut:'centre'|'bas'} — monde de plantation, rampe Q30/Q297, décalage ch. 59. */
(function(){
  var CACHE={}, ORDRE=[], RHO={};
  /* ⚑ LA CLÉ PORTE TOUT CE DONT L'IMAGE DÉPEND — et rien ne l'expire à l'horloge. Une première écriture vidait le
     cache toutes les 1,2 s : la page + repeignait une dalle de 800 px (120 ms) à chaque toucher d'un mot, et le choix
     des personnes ne s'ouvrait plus toujours (redteam_gens, 38 → 30/32). La clé : l'id, la taille à 4 px près, les
     options, le monde et la palette courants, le thème, et LA BOÎTE DE LA CELLULE — elle change dès que la Toile
     bouge (plantation, sync), donc une dalle au pavage neuf est toujours repeinte. 60 entrées au plus. */
  function cle(id,tw,th,o){ var M={}, D=null, C=''; try{ M=Toile.mondeCourant()||{}; D=Toile.dalleAbs(id); C=String(Toile.colorOf?Toile.colorOf(id):''); }catch(_){}
    var clair=!!(document.getElementById('device')&&document.getElementById('device').classList.contains('light'));
    return [id,Math.round(tw/4),Math.round(th/4),JSON.stringify(o&&o.monde||null),JSON.stringify(o&&o.rampe||null),
      JSON.stringify(o&&o.decale||null),o&&o.donnees?1:0,M.m,M.p,M.h,clair,
      D?[D.minx,D.miny,D.w,D.h].map(function(v){return Math.round(v*2);}).join(','):'', C].join('|'); }   /* ⚑ v100 — la boîte au DEMI-PIXEL (§8 : une signature se prend à la précision que l'œil voit). Au dixième, le frémissement de la Toile cachée sous une fiche (0,1 px) changeait la clé de TOUTES les dalles : la petite Toile d'une Nuée se re-rendait en entier 1,5 s après son ouverture (mesuré : dalle 131, 269 × 535, rendue à 332 ms puis encore à 1 951 ms). */   /* la couleur : une dalle en transition (760 ms) n'est jamais figée à mi-chemin */
  function garde(k,cv){ if(!CACHE[k]){ ORDRE.push(k); if(ORDRE.length>60){ delete CACHE[ORDRE.shift()]; } } CACHE[k]=cv; return cv; }
  function frais(){}
  /* ⚑ v59 (latences, Tom : « entre le clic sur + et le chargement de la page, ça accroche ») — mesuré : une dalle de page + coûte
     ~340 ms au moteur, les cartes de l'Index ~370 ms à elles toutes, la trame des Réglages ~280 ms. Au repos le cache tient (la
     boîte d'une cellule ne bouge pas), mais chaque plantation change toutes les cellules : la PROCHAINE ouverture repeignait tout.
     LE RAPPEL : on retient les dernières dalles demandées (les arguments, pas l'image), et quand l'app est au repos depuis 1,5 s —
     aucun doigt, aucune transition — on re-rend en tâche de fond, une à la fois, celles que le cache a perdues. L'ouverture
     suivante les trouve prêtes. Les mêmes calculs, faits quand personne n'attend. */
  var RAPPEL=[], _dernierDoigt=0;
  ['pointerdown','pointermove','wheel','keydown'].forEach(function(t){ window.addEventListener(t,function(){ _dernierDoigt=performance.now(); },{capture:true,passive:true}); });
  function retiens(id,tw,th,o){ var s=id+'|'+Math.round(tw/4)+'|'+Math.round(th/4)+'|'+JSON.stringify(o||null);
    for(var i=0;i<RAPPEL.length;i++) if(RAPPEL[i].s===s){ RAPPEL.splice(i,1); break; }
    RAPPEL.unshift({s:s,id:id,tw:tw,th:th,o:o}); if(RAPPEL.length>40) RAPPEL.pop(); }
  function rechauffe(){
    var calme = performance.now()-_dernierDoigt > 1500 && !(window._trans_en_cours && window._trans_en_cours()) && !document.hidden
      && !(window.Toile_state && window.Toile_state().running) && !(window._tEcran && performance.now()-window._tEcran<2500);   /* ⚑ v100 : ni dans les 2,5 s d'un changement d'écran — il tournait pendant l'ouverture d'une Nuée (19 dalles, 0,5 s) */   /* ⚑ v72 : ni pendant que la Toile anime (fondu, relâchement) — une dalle re-rendue y coûtait une image de 100 à 330 ms */
    if(calme){
      for(var i=0;i<RAPPEL.length;i++){ var R=RAPPEL[i], o=R.o||{};
        if(!promises.some(function(p){ return p.id===R.id; })){ RAPPEL.splice(i,1); i--; continue; }
        var oo=o; if(o.courant){ oo={}; for(var _k in o) oo[_k]=o[_k]; try{ oo.monde=Toile.mondeCourant(); }catch(_){ } }
        var k0; try{ k0=cle(R.id,R.tw,R.th,oo); }catch(_){ continue; }
        if(!CACHE[k0]){ try{ window._rendDalle(R.id,R.tw,R.th,R.o,true); }catch(_){ } break; }   /* UNE par passage */
      }
    }
    setTimeout(function(){ if(window.requestIdleCallback) requestIdleCallback(rechauffe,{timeout:2000}); else rechauffe(); }, 400);
  }
  setTimeout(rechauffe, 4000);
  window._rendDalle=function(id, twDev, thDev, o, _deFond){
    if(!_deFond) try{ retiens(id,twDev,thDev,o); }catch(_){ }
    o=o||{}; if(!(window.Toile&&Toile.dalleTrame&&Toile.dalleAbs)) return null;
    if(!(twDev>2&&thDev>2)) return null;
    /* le monde : celui de la plantation (le moteur le trouve seul), sauf quand l'écran montre EXPRÈS le monde courant */
    if(o.courant){ var _o2={}; for(var _k in o) _o2[_k]=o[_k]; try{ _o2.monde=Toile.mondeCourant(); }catch(_){ } o=_o2; }
    frais(); var c0=cle(id,twDev,thDev,o); if(CACHE[c0]) return CACHE[c0];
    if(o.siPret) return null;   /* ⚑ v100 : « déjà prête ? » — un peintre sous budget demande sans faire rendre */
    var D=Toile.dalleAbs(id); if(!D||!D.w||!D.h) return null;
    var E=(Toile.vue&&Toile.vue().dpr)||Math.min(2,window.devicePixelRatio||1);
    var op={}; if(o.rampe) op.rampe=o.rampe; if(o.decale) op.decale=o.decale; if(o.donnees) op.donnees=true; if(o.courant) op.courant=1;
    /* L'ESTIMATION APPREND : le rapport entre la taille rendue et la boîte de la cellule dépend du monde (un monde
       libre déborde, une trame se recadre). On le retient par monde : la plupart des dalles se rendent en UN passage.
       Une seconde passe seulement si la dalle DÉPASSE sa boîte ou en remplit moins de 95 % — jamais une troisième.
       (Mesuré : trois passes pour la dalle qui dérive derrière la page +, 231 ms, et le toucher sur une tuile perdu.) */
    var wld=(o.monde&&o.monde.m)||((Toile.curWorld&&Toile.curWorld())||''), rho=RHO[wld]||1;
    var k=Math.min(twDev/(D.w*E*rho), thDev/(D.h*E*rho)), cv=null;
    for(var n=0;n<2;n++){
      var c=document.createElement('canvas');
      if(!Toile.dalleTrame(c,id,k,o.monde||undefined,op)||!c.width) return null;
      cv=c; var f=Math.min(twDev/c.width, thDev/c.height);
      RHO[wld]=Math.max(c.width/(D.w*E*k), c.height/(D.h*E*k));
      if(f>=1 && f<=1.05) break;               /* elle tient, et remplit au moins 95 % — on ne la tire jamais */
      if(n===0) k*=f*0.995;                    /* la seconde passe est acceptée telle quelle : elle est déjà juste à ~1 % */
    }
    return garde(c0, cv);
  };
  /* pose `cv` 1:1, centré sur le point (cx, cy) des coordonnées COURANTES du contexte */
  window._poseUn=function(g, cv, cx, cy){
    var T=g.getTransform(), X=T.a*cx+T.c*cy+T.e, Y=T.b*cx+T.d*cy+T.f;
    var sx=Math.hypot(T.a,T.b)||1, sy=Math.hypot(T.c,T.d)||1;
    g.save();
    if(Math.abs(T.b)<1e-6 && Math.abs(T.c)<1e-6){
      g.setTransform(T.a<0?-1:1,0,0,T.d<0?-1:1,0,0);
      g.drawImage(cv, Math.round((T.a<0?-X:X)-cv.width/2), Math.round((T.d<0?-Y:Y)-cv.height/2));
    } else {
      g.setTransform(T.a/sx,T.b/sx,T.c/sy,T.d/sy,X,Y);
      g.drawImage(cv, -cv.width/2, -cv.height/2);
    }
    g.restore();
    return {w:cv.width/sx, h:cv.height/sy};
  };
  /* rend et pose la dalle `id` dans la boîte (x, y, w, h) des coordonnées courantes — « contain », centrée
     (ou posée sur le bas de la boîte). Rend {cv, x, y, w, h} : ce qui a VRAIMENT été peint, pour qui le déclare. */
  window._poseDalle=function(g, id, x, y, w, h, o){
    try{
      o=o||{}; var T=g.getTransform(), sx=Math.hypot(T.a,T.b)||1, sy=Math.hypot(T.c,T.d)||1;
      var cv=window._rendDalle(id, w*sx, h*sy, o); if(!cv) return null;
      var dw=cv.width/sx, dh=cv.height/sy, cx=x+w/2, cy=(o.haut==='bas')?(y+h-dh/2):(y+h/2);
      window._poseUn(g, cv, cx, cy);
      return {cv:cv, x:cx-dw/2, y:cy-dh/2, w:dw, h:dh};
    }catch(e){ return null; }
  };
})();
