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

    /* ⚑ v44 (Tom, 24 sept.) — « LA PLAQUE SE RECASSE EN SUIVANT LE MOUVEMENT. » Sur la Toile vivante, pendant une
       transition, un éclat qui change de propriétaire ne change plus de couleur d'une image à l'autre (c'était la saccade :
       des éclats qui clignotent un par un). Il SE CASSE : il se rétracte (la fissure s'ouvre autour de lui), pivote un peu
       et s'écarte dans le sens du mouvement — loin de la dalle qui arrive, vers celle qui part —, puis revient se poser.
       Sa couleur bascule au creux de la fissure, quand il est le plus petit : aucune couleur n'est inventée (aucun fondu).
       La cassure court d'elle-même : les éclats basculent à mesure que la cellule neuve pousse ses voisines.
       Ce qu'on garde d'une image à l'autre est la couleur AFFICHÉE de chaque éclat et l'heure de sa cassure — sur le
       germe, dans le cache de la plaque, et seulement sur la Toile vivante (une dalle, un export lisent le propriétaire). */
    var TR = env.trans, ESQ_D = 460;
    for (i = 0; i < feuilles.length; i++) {
      var fe = feuilles[i], p = fe.p, s = fe.s;
      if (!p || p.length < 3 || !s) continue;
      var ar = _aire(p); if (ar < u * u * 0.006) continue;
      var c = _cent(p);
      if (c[0] < x0 - u || c[0] > x1 + u || c[1] < y0 - u || c[1] > y1 + u) continue;
      var sv = s.s, ok = s.own, ph = -1;
      if (TR) {
        if (s.vs == null || s.vtr !== TR.n && s.ft == null) { if (s.vs == null) { s.vs = s.s; s.vo = s.own; } s.vtr = TR.n; }
        if (s.ft != null) { ph = (now - s.ft) / ESQ_D; if (ph >= 1) { s.ft = null; ph = -1; } }
        if (s.ft == null && s.vs !== s.s) { s.ft = now; s.fs = s.vs; s.fo = s.vo; ph = 0; }
        if (s.ft != null) { if (ph >= 0.5) { s.vs = s.s; s.vo = s.own; } sv = ph < 0.5 ? s.fs : s.s; ok = ph < 0.5 ? s.fo : s.own; }
        else { sv = s.vs; ok = s.vo; }
      } else if (env.vive) { s.vs = s.s; s.vo = s.own; s.ft = null; }   // hors de la Toile vivante (une dalle, un export) : on ne touche pas à l'état
      var col = cOf(sv, now);
      if (_promesse(sv)) {
        var tv = _lcg((ok.k ^ 0x5bf03635) >>> 0)();
        if (tv < 0.18) col = _nu(col, -0.18);                  // l'éclat prend parfois une nuance
      }
      var peint = _offset(p, Math.min(fel, Math.sqrt(ar) * 0.16));
      if (ph >= 0 && peint.length > 2) {
        var sb = Math.sin(Math.PI * ph), rk = _lcg((s.k ^ 0x2c1b3c6d) >>> 0), rot = (rk() - 0.5) * 0.5 * sb, sc = 1 - 0.34 * sb;
        var dxm = c[0] - TR.x, dym = c[1] - TR.y, lm = Math.sqrt(dxm * dxm + dym * dym) || 1, dir = TR.kind === 'depart' ? -1 : 1;
        var ox = dxm / lm * u * 0.28 * sb * dir, oy = dym / lm * u * 0.28 * sb * dir, cr = Math.cos(rot), srr = Math.sin(rot), q2 = [];
        for (var qi = 0; qi < peint.length; qi++) { var ex = (peint[qi][0] - c[0]) * sc, ey = (peint[qi][1] - c[1]) * sc;
          q2.push([c[0] + ex * cr - ey * srr + ox, c[1] + ex * srr + ey * cr + oy]); }
        peint = q2;
      }
      if (_rec && _promesse(s.s)) _note(s.own.k, { poly: peint, col: col });
      g.fillStyle = _rgb(col);
      _trace(peint); g.fill();
    }
  }

