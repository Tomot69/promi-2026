/* ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
   Promi — LES FLAQUES (v146, Tom, 14 oct. 2026 — C-094 le guide, C-118 « tenir »).

   « De l'eau qui monterait par en dessous dans du sable, vue du dessous. Des flaques naissent dans les creux, au hasard. Elles grossissent,
   leurs contours sont abstraits, elles se touchent quand elles sont pleines. »

   LA MATIÈRE. Un RELIEF tiré au hasard (le sable) : quelques creux, semés loin les uns des autres, chacun avec sa profondeur, sa largeur,
   son allongement ; le terrain entre eux est froissé (les contours ne sont jamais des cercles). L'EAU est un NIVEAU qui monte : est mouillé
   tout point dont le relief est sous le niveau. Les flaques naissent donc au fond des creux, l'une après l'autre, grossissent, se touchent
   (deux creux voisins se rejoignent par leur col), puis couvrent tout. Joué à l'envers, elles se vident.
   Rien n'est fondu : le bord d'une flaque est une LIGNE (le contour du niveau, tracé en vecteurs à la densité de l'écran), et ce qui est
   dedans est plein. Aucune forme ne se translate : seul le niveau bouge.

   L'ENTOURAGE (le Studio, le +) : une forme presque régulière — la boîte de ce qu'on montre, sa marge, des coins ronds, et un bord à peine
   irrégulier (quelques lobes larges, quelques pour-cent du rayon) — remplie par les mêmes flaques, plus petites, qui naissent DEDANS.

   Ce fichier ne dépend de rien. Il sert la page de démonstration (promi-guide-variantes.html?flaques=1, promi-tenir-variantes.html) et l'app.
   ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════ */
(function (racine) {
  'use strict';

  /* un hasard qu'on peut rejouer (une graine = un tirage) */
  function alea(graine) {
    var s = (graine >>> 0) || 0x9E3779B9;
    return function () { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  }

  /* un bruit doux (valeurs tirées sur une grille, interpolées en cloche) — pour froisser le terrain */
  function bruit(R, nx, ny) {
    var v = new Float32Array((nx + 1) * (ny + 1)), i;
    for (i = 0; i < v.length; i++) v[i] = R() * 2 - 1;
    return function (x, y) {            /* x, y en unités de grille */
      var x0 = Math.floor(x), y0 = Math.floor(y), fx = x - x0, fy = y - y0;
      x0 = ((x0 % nx) + nx) % nx; y0 = ((y0 % ny) + ny) % ny;
      var x1 = x0 + 1, y1 = y0 + 1;
      fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy);
      var a = v[y0 * (nx + 1) + x0], b = v[y0 * (nx + 1) + x1], c = v[y1 * (nx + 1) + x0], d = v[y1 * (nx + 1) + x1];
      return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy;
    };
  }

  /* ── LE RELIEF ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
     o : { l, h (la zone, en points), pas (la maille, en points), graine, creux (combien), rayon (la portée d'un creux, en points),
           froisse (l'amplitude du froissement, en points), etale (0..1 : de combien les naissances s'étalent dans le temps),
           pente ([dx, dy, force] : un terrain qui penche — l'eau avance alors dans ce sens ; pour « tenir », vers le bas),
           dans (fonction (x, y) → ≤ 1 dedans : les creux ne naissent que là) }
     rend : { z (Float32Array, le relief sur la grille), nx, ny, pas, min, max, creux:[{x, y, t}] }                                    */
  function relief(o) {
    var R = alea(o.graine || 1), pas = o.pas || 4, nx = Math.ceil(o.l / pas) + 1, ny = Math.ceil(o.h / pas) + 1;
    var n = o.creux || 9, rayon = o.rayon || 150, fro = (o.froisse == null ? 22 : o.froisse), etale = (o.etale == null ? 0.42 : o.etale);
    var C = [], i, k, essais = 0;
    /* les creux : semés au hasard, mais jamais collés (le plus loin possible de ceux déjà là, parmi quelques tirages) */
    while (C.length < n && essais < n * 60) {
      essais++;
      var best = null, bd = -1;
      for (k = 0; k < 14; k++) {
        var x = R() * o.l, y = R() * o.h;
        if (o.dans && o.dans(x, y) > 0.72) continue;
        var d = 1e9;
        for (i = 0; i < C.length; i++) { var dx = x - C[i].x, dy = y - C[i].y; d = Math.min(d, dx * dx + dy * dy); }
        d = Math.min(d, 1e9) * (0.55 + 0.45 * R());          /* un peu de désordre : pas une grille déguisée */
        if (d > bd) { bd = d; best = { x: x, y: y }; }
      }
      if (!best) continue;
      var ang = R() * Math.PI, al = 0.72 + R() * 0.62;       /* son allongement et son sens */
      C.push({ x: best.x, y: best.y, t: 0, r: rayon * (0.78 + R() * 0.5), ca: Math.cos(ang), sa: Math.sin(ang), ax: al, ay: 1 / al });
    }
    /* l'ordre des naissances : au hasard, étalées sur `etale` de la montée */
    var ordre = C.map(function (c, q) { return q; });
    for (i = ordre.length - 1; i > 0; i--) { k = (R() * (i + 1)) | 0; var tq = ordre[i]; ordre[i] = ordre[k]; ordre[k] = tq; }
    for (i = 0; i < ordre.length; i++) C[ordre[i]].t = (C.length > 1 ? i / (C.length - 1) : 0) * etale * (0.9 + 0.2 * R());
    /* le froissement : deux échelles */
    var g1 = Math.max(3, Math.round(o.l / (rayon * 0.9)) + 2), g2 = Math.max(3, Math.round(o.h / (rayon * 0.9)) + 2);
    var bx = bruit(R, g1, g2), by = bruit(R, g1, g2), cx = bruit(R, g1 * 3, g2 * 3), cy = bruit(R, g1 * 3, g2 * 3), ex = bruit(R, g1 * 7, g2 * 7), ey = bruit(R, g1 * 7, g2 * 7);
    var ech1 = 1 / (rayon * 0.9), ech2 = 3 / (rayon * 0.9), ech3 = 7 / (rayon * 0.9);
    var z = new Float32Array(nx * ny), mn = 1e9, mx = -1e9, K = 0.16;
    var P = o.pente || null, pl = P ? Math.sqrt(P[0] * P[0] + P[1] * P[1]) || 1 : 1;
    for (var j = 0; j < ny; j++) {
      for (i = 0; i < nx; i++) {
        var X = i * pas, Y = j * pas;
        var wx = X + fro * bx(X * ech1, Y * ech1) + fro * 0.42 * cx(X * ech2, Y * ech2) + fro * 0.13 * ex(X * ech3, Y * ech3);
        var wy = Y + fro * by(X * ech1, Y * ech1) + fro * 0.42 * cy(X * ech2, Y * ech2) + fro * 0.13 * ey(X * ech3, Y * ech3);
        /* le plus bas des creux, fondu avec son voisin (deux flaques qui se touchent se rejoignent par un col, pas par un coin) */
        var v = 1e9;
        for (k = 0; k < C.length; k++) {
          var c = C[k], ddx = wx - c.x, ddy = wy - c.y, u = (ddx * c.ca + ddy * c.sa) / c.ax, w = (-ddx * c.sa + ddy * c.ca) / c.ay;
          var e = c.t + Math.sqrt(u * u + w * w) / c.r;
          if (v > 1e8) v = e; else { var hh = Math.max(0, Math.min(1, 0.5 + 0.5 * (v - e) / K)); v = v + (e - v) * hh - K * hh * (1 - hh); }
        }
        if (P) v = v * (1 - P[2]) + P[2] * ((X * P[0] + Y * P[1]) / pl) / (P[1] ? o.h : o.l) * 1.6;
        z[j * nx + i] = v; if (v < mn) mn = v; if (v > mx) mx = v;
      }
    }
    /* la table des niveaux par SURFACE : q[k] = le niveau sous lequel se trouvent k/256 des points (ceux de la zone, si `dans` est donné).
       Le temps commande ainsi la surface mouillée, pas la hauteur de l'eau : sans cela tout se jouait dans la première moitié. */
    var vals = [], jj, ii;
    for (jj = 0; jj < ny; jj++) for (ii = 0; ii < nx; ii++) { if (o.dans && o.dans(ii * pas, jj * pas) > 1) continue; vals.push(z[jj * nx + ii]); }
    vals.sort(function (p, q2) { return p - q2; });
    var Q = new Float32Array(257); for (k = 0; k <= 256; k++) Q[k] = vals.length ? vals[Math.min(vals.length - 1, Math.floor(k / 256 * (vals.length - 1)))] : 0;
    if (vals.length) { mn = vals[0]; mx = vals[vals.length - 1]; }
    return { z: z, nx: nx, ny: ny, pas: pas, min: mn, max: mx, l: o.l, h: o.h, creux: C, q: Q };
  }

  /* ── L'ENTOURAGE ────────────────────────────────────────────────────────────────────────────────────────────────────────────
     boite : [x, y, l, h] de ce qu'on montre ; marge : en points ; o : { graine, irregulier (0,035 par défaut : la part du rayon),
     carre (l'exposant de la forme : 2 = ellipse, 3 = coins ronds ; 2,6 par défaut) }
     rend une fonction (x, y) → s, s ≤ 1 dedans ; et sa boîte englobante.                                                              */
  function entourage(boite, marge, o) {
    o = o || {};
    var R = alea(o.graine || 7), cx = boite[0] + boite[2] / 2, cy = boite[1] + boite[3] / 2;
    var a = boite[2] / 2 + marge, b = boite[3] / 2 + marge, n = o.carre || 2.6, ir = (o.irregulier == null ? 0.035 : o.irregulier);
    /* quelques lobes LARGES (2, 3 et 5 par tour), de phases tirées : un contour à peine irrégulier, jamais dentelé */
    var p2 = R() * 6.2832, p3 = R() * 6.2832, p5 = R() * 6.2832, k2 = 0.5 + 0.3 * R(), k3 = 0.35 + 0.3 * R(), k5 = 0.12 + 0.15 * R(), ks = k2 + k3 + k5;
    function f(x, y) {
      var dx = (x - cx) / a, dy = (y - cy) / b, s = Math.pow(Math.pow(Math.abs(dx), n) + Math.pow(Math.abs(dy), n), 1 / n);
      var th = Math.atan2(dy, dx), m = (k2 * Math.sin(2 * th + p2) + k3 * Math.sin(3 * th + p3) + k5 * Math.sin(5 * th + p5)) / ks;
      return s / (1 + ir * m);
    }
    var d = 1 + ir + 0.02;
    f.boite = [cx - a * d, cy - b * d, 2 * a * d, 2 * b * d]; f.centre = [cx, cy]; f.demi = [a, b];
    return f;
  }

  /* ── LE CONTOUR D'UN NIVEAU, EN VECTEURS ────────────────────────────────────────────────────────────────────────────────────
     Ajoute à `chemin` (un Path2D, ou tout objet qui a moveTo / lineTo / closePath / rect) la région où F(i, j) > 0, maille par maille
     (carrés de marche, bords interpolés). Les mailles pleines d'une même rangée sont jointes en un seul rectangle. `F` est un
     Float32Array nx × ny ; x0, y0 : l'origine en points ; pas : la maille. Rend le nombre de mailles de bord (pour la mesure).          */
  function contour(chemin, F, nx, ny, x0, y0, pas) {
    var bords = 0, j, i;
    for (j = 0; j < ny - 1; j++) {
      var deb = -1, r0 = j * nx, r1 = r0 + nx, Y = y0 + j * pas;
      for (i = 0; i < nx - 1; i++) {
        var a = F[r0 + i], b = F[r0 + i + 1], c = F[r1 + i + 1], d = F[r1 + i];
        var m = (a > 0 ? 1 : 0) | (b > 0 ? 2 : 0) | (c > 0 ? 4 : 0) | (d > 0 ? 8 : 0);
        if (m === 15) { if (deb < 0) deb = i; continue; }
        if (deb >= 0) { chemin.rect(x0 + deb * pas, Y, (i - deb) * pas, pas); deb = -1; }
        if (m === 0) continue;
        bords++;
        var X = x0 + i * pas, X1 = X + pas, Y1 = Y + pas;
        /* où le niveau coupe chaque côté */
        var tx = X + pas * (a / (a - b)), rx = Y + pas * (b / (b - c)), bx = X + pas * (d / (d - c)), lx = Y + pas * (a / (a - d));
        switch (m) {
          case 1: chemin.moveTo(X, Y); chemin.lineTo(tx, Y); chemin.lineTo(X, lx); chemin.closePath(); break;
          case 2: chemin.moveTo(tx, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, rx); chemin.closePath(); break;
          case 3: chemin.moveTo(X, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, rx); chemin.lineTo(X, lx); chemin.closePath(); break;
          case 4: chemin.moveTo(X1, rx); chemin.lineTo(X1, Y1); chemin.lineTo(bx, Y1); chemin.closePath(); break;
          case 5: chemin.moveTo(X, Y); chemin.lineTo(tx, Y); chemin.lineTo(X1, rx); chemin.lineTo(X1, Y1); chemin.lineTo(bx, Y1); chemin.lineTo(X, lx); chemin.closePath(); break;
          case 6: chemin.moveTo(tx, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, Y1); chemin.lineTo(bx, Y1); chemin.closePath(); break;
          case 7: chemin.moveTo(X, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, Y1); chemin.lineTo(bx, Y1); chemin.lineTo(X, lx); chemin.closePath(); break;
          case 8: chemin.moveTo(X, lx); chemin.lineTo(bx, Y1); chemin.lineTo(X, Y1); chemin.closePath(); break;
          case 9: chemin.moveTo(X, Y); chemin.lineTo(tx, Y); chemin.lineTo(bx, Y1); chemin.lineTo(X, Y1); chemin.closePath(); break;
          case 10: chemin.moveTo(tx, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, rx); chemin.lineTo(bx, Y1); chemin.lineTo(X, Y1); chemin.lineTo(X, lx); chemin.closePath(); break;
          case 11: chemin.moveTo(X, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, rx); chemin.lineTo(bx, Y1); chemin.lineTo(X, Y1); chemin.closePath(); break;
          case 12: chemin.moveTo(X, lx); chemin.lineTo(X1, rx); chemin.lineTo(X1, Y1); chemin.lineTo(X, Y1); chemin.closePath(); break;
          case 13: chemin.moveTo(X, Y); chemin.lineTo(tx, Y); chemin.lineTo(X1, rx); chemin.lineTo(X1, Y1); chemin.lineTo(X, Y1); chemin.closePath(); break;
          case 14: chemin.moveTo(tx, Y); chemin.lineTo(X1, Y); chemin.lineTo(X1, Y1); chemin.lineTo(X, Y1); chemin.lineTo(X, lx); chemin.closePath(); break;
        }
      }
      if (deb >= 0) chemin.rect(x0 + deb * pas, Y, (nx - 1 - deb) * pas, pas);
    }
    return bords;
  }

  /* le niveau pour une avancée u (0 → 1) : il part juste sous le premier creux et finit juste au-dessus du dernier sommet.
     La courbe : la surface mouillée croît comme le carré du niveau — on monte donc d'abord vite (les naissances se voient), puis
     régulièrement ; aucune traîne à la fin. */
  function niveau(Rf, u) {
    u = Math.max(0, Math.min(1, u));
    if (u <= 0) return Rf.min - 0.01; if (u >= 1) return Rf.max + 0.01;
    /* la part de surface mouillée à l'avancée u : un départ un peu retenu (on voit naître les flaques une à une), puis un pas régulier */
    var a = 0.82 * u + 0.18 * u * u * (3 - 2 * u); a = a * (0.6 + 0.4 * u);
    a = a / 1.0; var x = a * 256, k = Math.floor(x), f = x - k, Q = Rf.q;
    if (!Q) return Rf.min + (Rf.max - Rf.min) * a;
    return Q[k] + (Q[Math.min(256, k + 1)] - Q[k]) * f;
  }

  /* ── LA SCÈNE DU GUIDE ──────────────────────────────────────────────────────────────────────────────────────────────────────
     Un canevas posé sur l'accueil. Il montre l'accueil FLOUTÉ À L'AVANCE (`o.flou` : une image ou un canevas, aux cotes de l'appareil) là
     où il y a de l'eau ; ailleurs il est transparent et l'accueil réel se voit, net. Une zone NETTE (l'entourage) est un trou dans l'eau.
       scene.couvre(u)          l'eau monte sur tout l'écran (0 → 1) ; scene.decouvre(u) : elle se retire (un autre tirage)
       scene.cible(boite, marge, graine)   prépare l'entourage d'une cible
       scene.net(u)             la zone nette s'ouvre en flaques (0 → 1) ; rejouer de 1 à 0 la referme sur elle-même
       scene.peint()            dessine l'état courant ; rend { ms, bords }
     Tout est une fonction de (u couverture, u net) : aucune horloge ici, la page ou l'app tient le temps. */
  function Scene(cv, o) {
    var l = o.l || 390, h = o.h || 844, dens = o.densite || 2;
    cv.width = Math.round(l * dens); cv.height = Math.round(h * dens);
    var g = cv.getContext('2d'), graine = (o.graine || 1) >>> 0;
    var S = { l: l, h: h, flou: o.flou, uC: 0, uN: 0, sensC: 1, R: null, Rn: null, ent: null, F: null, Fn: null };
    function tire(retrait) {
      graine = (Math.imul(graine, 1664525) + 1013904223) >>> 0;
      S.R = relief({ l: l, h: h, pas: 4, graine: graine, creux: o.creux || 10, rayon: o.rayon || 150, froisse: o.froisse == null ? 34 : o.froisse, etale: 0.42 });
      S.F = new Float32Array(S.R.nx * S.R.ny); S.sensC = retrait ? -1 : 1;
    }
    tire(false);
    S.tire = tire;
    S.cible = function (boite, marge, gr, opt) {
      opt = opt || {};
      var ent = entourage(boite, marge, { graine: gr || 3, irregulier: opt.irregulier, carre: opt.carre }), b = ent.boite, pas = 1.5;
      var x0 = Math.floor(b[0]) - 2, y0 = Math.floor(b[1]) - 2, ll = Math.ceil(b[2]) + 4, hh = Math.ceil(b[3]) + 4;
      var Rn = relief({ l: ll, h: hh, pas: pas, graine: (gr || 3) * 7919, creux: opt.creux || 4, rayon: Math.max(ll, hh) * 0.62, froisse: Math.min(ll, hh) * 0.16, etale: 0.5,
        dans: function (x, y) { return ent(x + x0, y + y0); } });
      /* l'entourage lui-même, sur la même grille (s − 1 : négatif dedans) */
      var E = new Float32Array(Rn.nx * Rn.ny), i, j;
      for (j = 0; j < Rn.ny; j++) for (i = 0; i < Rn.nx; i++) E[j * Rn.nx + i] = ent(x0 + i * pas, y0 + j * pas) - 1;
      S.ent = ent; S.Rn = Rn; S.En = E; S.Fn = new Float32Array(Rn.nx * Rn.ny); S.x0 = x0; S.y0 = y0; S.pasN = pas; S.llN = ll; S.hhN = hh; S.uN = 0;
      return ent;
    };
    S.sansCible = function () { S.ent = null; S.Rn = null; S.uN = 0; };
    S.couvre = function (u) { S.uC = Math.max(0, Math.min(1, u)); };
    S.net = function (u) { S.uN = Math.max(0, Math.min(1, u)); };
    S.peint = function () {
      var t0 = (racine.performance && performance.now) ? performance.now() : 0, bords = 0, i;
      g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-over'; g.clearRect(0, 0, cv.width, cv.height);
      if (S.uC <= 0) return { ms: 0, bords: 0 };
      g.setTransform(dens, 0, 0, dens, 0, 0);
      /* ① l'eau : l'accueil flouté, montré là où le relief est sous le niveau */
      var chemin = new Path2D();
      if (S.uC >= 1) chemin.rect(0, 0, l, h);
      else { var R = S.R, L = niveau(R, S.uC), z = R.z, F = S.F; for (i = 0; i < z.length; i++) F[i] = L - z[i]; bords += contour(chemin, F, R.nx, R.ny, 0, 0, R.pas); }
      g.save(); g.clip(chemin);
      if (S.flou) g.drawImage(S.flou, 0, 0, l, h); else { g.fillStyle = o.aplat || '#888'; g.fillRect(0, 0, l, h); }
      g.restore();
      /* ② la zone nette : un TROU dans l'eau — dans l'entourage ET sous le niveau « net » (les flaques nettes naissent dedans) */
      if (S.Rn && S.uN > 0) {
        var Rn = S.Rn, Ln = niveau(Rn, S.uN), zn = Rn.z, En = S.En, Fn = S.Fn, trou = new Path2D();
        if (S.uN >= 1) { for (i = 0; i < zn.length; i++) Fn[i] = -En[i]; }
        else { for (i = 0; i < zn.length; i++) { var a = -En[i], b = Ln - zn[i]; Fn[i] = a < b ? a : b; } }
        bords += contour(trou, Fn, Rn.nx, Rn.ny, S.x0, S.y0, S.pasN);
        g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000'; g.fill(trou); g.globalCompositeOperation = 'source-over';
      }
      return { ms: t0 ? performance.now() - t0 : 0, bords: bords };
    };
    return S;
  }

  /* ── UN APLAT QUI AVANCE EN FLAQUES (« tenir ») ─────────────────────────────────────────────────────────────────────────────
     o : { l, h, graine, sens ([dx, dy], par défaut vers le bas), force (0,55 : la part de la pente), creux, rayon }
     rend { chemin(u) → Path2D de ce qui est couvert pour une avancée u }                                                              */
  function Nappe(o) {
    var s = o.sens || [0, 1];
    var R = relief({ l: o.l, h: o.h, pas: o.pas || 3, graine: o.graine || 5, creux: o.creux || 9, rayon: o.rayon || 110, froisse: o.froisse == null ? 16 : o.froisse, etale: 0.3,
      pente: [s[0], s[1], o.force == null ? 0.55 : o.force] });
    var F = new Float32Array(R.nx * R.ny);
    return { relief: R, chemin: function (u, x0, y0) {
      var p = new Path2D(); if (u <= 0) return p; if (u >= 1) { p.rect(x0 || 0, y0 || 0, o.l, o.h); return p; }
      var L = niveau(R, u), z = R.z; for (var i = 0; i < z.length; i++) F[i] = L - z[i];
      contour(p, F, R.nx, R.ny, x0 || 0, y0 || 0, R.pas);
      var gx = (R.nx - 1) * R.pas, gy = (R.ny - 1) * R.pas; void gx; void gy;
      return p; } };
  }

  /* ── LE FLOU, FAIT À L'AVANCE ───────────────────────────────────────────────────────────────────────────────────────────────
     Safari n'a pas `filter` sur un canevas : trois passes de moyenne glissante valent une gaussienne (écart 4,8 pt, celui des murs).
     `src` : un canevas ; rend un canevas neuf, de la même taille. `sigma` en pixels du canevas.                                        */
  function floute(src, sigma) {
    var w = src.width, h = src.height, c = document.createElement('canvas'); c.width = w; c.height = h;
    var g = c.getContext('2d'); g.drawImage(src, 0, 0);
    var im = g.getImageData(0, 0, w, h), a = im.data, b = new Uint8ClampedArray(a.length);
    var W = Math.sqrt(12 * sigma * sigma / 3 + 1), r = Math.max(1, Math.round((W - 1) / 2));
    function passeH(s, d) {
      var n = 2 * r + 1;
      for (var y = 0; y < h; y++) {
        var o = y * w * 4, R0 = 0, G0 = 0, B0 = 0, A0 = 0, x, k;
        for (k = -r; k <= r; k++) { var q = o + Math.max(0, Math.min(w - 1, k)) * 4; R0 += s[q]; G0 += s[q + 1]; B0 += s[q + 2]; A0 += s[q + 3]; }
        for (x = 0; x < w; x++) {
          var p = o + x * 4; d[p] = R0 / n; d[p + 1] = G0 / n; d[p + 2] = B0 / n; d[p + 3] = A0 / n;
          var e = o + Math.min(w - 1, x + r + 1) * 4, f = o + Math.max(0, x - r) * 4;
          R0 += s[e] - s[f]; G0 += s[e + 1] - s[f + 1]; B0 += s[e + 2] - s[f + 2]; A0 += s[e + 3] - s[f + 3];
        }
      }
    }
    function passeV(s, d) {
      var n = 2 * r + 1;
      for (var x = 0; x < w; x++) {
        var R0 = 0, G0 = 0, B0 = 0, A0 = 0, y, k;
        for (k = -r; k <= r; k++) { var q = (Math.max(0, Math.min(h - 1, k)) * w + x) * 4; R0 += s[q]; G0 += s[q + 1]; B0 += s[q + 2]; A0 += s[q + 3]; }
        for (y = 0; y < h; y++) {
          var p = (y * w + x) * 4; d[p] = R0 / n; d[p + 1] = G0 / n; d[p + 2] = B0 / n; d[p + 3] = A0 / n;
          var e = (Math.min(h - 1, y + r + 1) * w + x) * 4, f = (Math.max(0, y - r) * w + x) * 4;
          R0 += s[e] - s[f]; G0 += s[e + 1] - s[f + 1]; B0 += s[e + 2] - s[f + 2]; A0 += s[e + 3] - s[f + 3];
        }
      }
    }
    for (var t = 0; t < 3; t++) { passeH(a, b); passeV(b, a); }
    g.putImageData(im, 0, 0); return c;
  }

  /* LES DURÉES DU GUIDE (ms) — les mêmes dans l'app et sur la page de démonstration. « Pas trop rapide, pour qu'on lise les flaques. Fluide,
     pas lent, plutôt vif. » Couverture 1,2 à 1,6 s ; ouverture et fermeture d'une zone nette 0,6 à 0,8 s. À régler avec Tom. */
  var GUIDE = { ATTENTE: 600, COUVRE: 1400, OUVRE: 700, FERME: 700, RETIRE: 1200, FLOU: 4.8, MARGE_STUDIO: 5, MARGE_PLUS: 5, CREUX: 10, RAYON: 150,
    /* la boîte de l'icône du Studio et de son mot, un peu élargie là où il y a de la place (le mot « STUDIO » touchait le bord du bas) : [gauche, haut, droite, bas] en points */
    AIR_STUDIO: [1.5, 1.5, 0, 2.5] };
  /* la boîte d'une cible, élargie de son air */
  function avecAir(b, air) { air = air || [0, 0, 0, 0]; return [b[0] - air[0], b[1] - air[1], b[2] + air[0] + air[2], b[3] + air[1] + air[3]]; }

  racine.Flaques = { GUIDE: GUIDE, avecAir: avecAir, alea: alea, relief: relief, entourage: entourage, contour: contour, niveau: niveau, Scene: Scene, Nappe: Nappe, floute: floute };
})(typeof window !== 'undefined' ? window : this);
