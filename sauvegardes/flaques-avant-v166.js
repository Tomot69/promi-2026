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

  /* ── v147 (Tom, 15 oct. 2026, C-094, 3e RÉCIDIVE) — DE VRAIES FLAQUES : DES MÉTABALLES ────────────────────────────────────────────
     LA CAUSE, écrite avant le code : v146 faisait monter un NIVEAU dans un relief froissé ; les flaques naissaient bien au fond des creux,
     mais (1) la zone nette du Studio et du + était l'intérieur d'un ENTOURAGE presque régulier — un super-ellipse à 3,5 % d'irrégularité, une
     marge de 5 pt : les flaques nettes finissaient par le remplir et la forme finale ÉTAIT cet entourage, d'où « le Studio se découvre en rond » ;
     (2) la couverture avait dix creux nés sur 42 % de la montée, mais un même niveau pour tous : les flaques grossissaient au même pas, leurs
     bords figés, et se rejoignaient par un coin du relief plutôt que par un pont. La demande est autre : des flaques ABSTRAITES, chacune avec
     sa vie (naissance, vitesse, bord qui ondule), qui se rejoignent par un pont qui s'élargit — de l'eau.
     LE MODÈLE : chaque flaque est un germe (x, y) au rayon r(u) qui croît à SA vitesse depuis SA naissance ; son bord est ondulé — le rayon
     varie avec l'angle (harmoniques 2, 3, 4, de 15 à 25 % du rayon) et ces ondulations tournent lentement pendant qu'elle grandit ; le champ
     est la SOMME des (R(θ)/d)² : là où deux flaques s'approchent, la somme passe 1 entre elles avant qu'elles ne se touchent — un pont naît
     et s'élargit (les métaballes). Le contour f = 1 est tracé en vecteurs (carrés de marche) : un bord net, rien n'est fondu. */
  function harmo(R) { var k = [2, 3, 4], H = []; for (var i = 0; i < 3; i++) H.push({ k: k[i], c: 0.45 + 0.55 * R(), p: R() * 6.2832, w: (R() - 0.5) * 2.2 }); var s = 0; H.forEach(function (h) { s += h.c; }); H.forEach(function (h) { h.c /= s; }); return H; }
  /* l'ondulation d'un bord dans la direction (c, s) = (cos θ, sin θ), au temps τ (secondes de vie) : ∈ [−1, 1], sans trigonométrie par point */
  function onde(H, c, s, tau) {
    var c2 = c * c - s * s, s2 = 2 * s * c, c3 = c * (4 * c * c - 3), s3 = s * (3 - 4 * s * s), c4 = c2 * c2 - s2 * s2, s4 = 2 * s2 * c2, v = 0, i;
    for (i = 0; i < H.length; i++) { var h = H[i], ph = h.p + h.w * tau, cp = Math.cos(ph), sp = Math.sin(ph), a = h.k === 2 ? s2 * cp + c2 * sp : (h.k === 3 ? s3 * cp + c3 * sp : s4 * cp + c4 * sp); v += h.c * a; }
    return v; }
  /* les germes de la couverture : 12 à 20, au hasard (jamais collés), naissances étalées sur les 40 premiers % de la durée, vitesses différentes */
  function germesCouverture(l, h, R) {
    var n = 12 + Math.floor(R() * 9), G = [], essais = 0, ecart = Math.sqrt(l * h / n);
    while (G.length < n && essais < n * 120) { essais++; var x = R() * l, y = R() * h, ok = true;
      for (var i = 0; i < G.length; i++) { var dx = x - G[i].x, dy = y - G[i].y; if (dx * dx + dy * dy < ecart * ecart * 0.42) { ok = false; break; } }
      if (ok) G.push({ x: x, y: y }); }
    while (G.length < 12) G.push({ x: R() * l, y: R() * h });
    var ordre = G.map(function (g, q) { return q; }); for (var a = ordre.length - 1; a > 0; a--) { var b = (R() * (a + 1)) | 0, t = ordre[a]; ordre[a] = ordre[b]; ordre[b] = t; }
    ordre.forEach(function (q, i) { G[q].t = Math.min(0.4, 0.4 * (i / Math.max(1, G.length - 1)) * (0.88 + 0.12 * R())); });
    G.forEach(function (g) { g.v = 0.62 + 0.76 * R(); g.rmax = ecart * (0.86 + 0.5 * R()); g.A = 0.15 + 0.10 * R(); g.H = harmo(R); });
    return G; }
  /* le rayon d'un germe à l'avancée u : il naît à t, grandit à SA vitesse (x^(1/v) : une flaque rapide part vite, une lente part doucement), et toutes
     arrivent à leur taille à la fin — la surface monte sur TOUTE la durée (v147 : avec l'ancienne loi tout était couvert à mi-chemin, puis plus rien) */
  function rayonA(g, u, D) { if (u <= g.t) return 0; var x = Math.min(1, (u - g.t) / (1 - g.t)); return g.rmax * Math.pow(x, 0.9 / (g.v || 1)) * (D || 1); }
  /* L'AVANCÉE DE LA COUVERTURE dans le temps : la surface d'une union de flaques qui grandissent monte en S (lente, puis d'un coup quand elles se
     rejoignent, puis plus rien) ; le temps est donc remappé (une courbe monotone, relevée sur huit tirages) pour que l'eau monte régulièrement
     d'un bout à l'autre : ~3 % à 8 % du temps, ~55 % à mi-chemin, les derniers trous se ferment sur le dernier cinquième. */
  var AV_T = [0, 0.08, 0.2, 0.35, 0.5, 0.65, 0.8, 0.93, 1], AV_U = [0, 0.15, 0.28, 0.39, 0.47, 0.565, 0.655, 0.85, 1];
  function avance(t) { if (t <= 0) return 0; if (t >= 1) return 1; var i = 0; while (i < AV_T.length - 2 && t > AV_T[i + 1]) i++;
    var a = AV_T[i], b = AV_T[i + 1], k = (t - a) / (b - a), m0 = pente(i), m1 = pente(i + 1), h = b - a, k2 = k * k, k3 = k2 * k;
    return (2 * k3 - 3 * k2 + 1) * AV_U[i] + (k3 - 2 * k2 + k) * h * m0 + (-2 * k3 + 3 * k2) * AV_U[i + 1] + (k3 - k2) * h * m1; }
  function pente(i) { var n = AV_T.length; if (i === 0) return (AV_U[1] - AV_U[0]) / (AV_T[1] - AV_T[0]); if (i === n - 1) return (AV_U[n - 1] - AV_U[n - 2]) / (AV_T[n - 1] - AV_T[n - 2]);
    var d0 = (AV_U[i] - AV_U[i - 1]) / (AV_T[i] - AV_T[i - 1]), d1 = (AV_U[i + 1] - AV_U[i]) / (AV_T[i + 1] - AV_T[i]); return d0 * d1 <= 0 ? 0 : 2 / (1 / d0 + 1 / d1); }
  /* le champ des métaballes sur une grille : F[k] = Σ φ(d / R(θ)) − 1, avec un noyau À SUPPORT BORNÉ φ(q) = (1 − q²/4)³ / (3/4)³ (φ = 1 au bord d'une
     flaque, 0 à deux rayons) : seules des flaques VOISINES se rejoignent (un pont naît quand l'écart tombe sous ~0,55 rayon), et la surface suit les
     rayons (le noyau en 1/d² d'avant additionnait les queues de vingt flaques : tout l'écran passait d'un coup). Coût : la phase de chaque
     harmonique est calculée une fois par flaque et par image, une flaque n'est lue que dans sa boîte — v147 : 38 → quelques ms par image. */
  function champ(F, nx, ny, x0, y0, pas, G, u, tau) {
    var j, i, k, n = G.length, L = [];
    for (k = 0; k < n; k++) { var g0 = G[k], r0 = rayonA(g0, u); if (r0 <= 0) continue; var Hp = [], ph;
      for (var q = 0; q < g0.H.length; q++) { ph = g0.H[q].p + g0.H[q].w * (tau + g0.t * 7); Hp.push(g0.H[q].k, g0.H[q].c, Math.cos(ph), Math.sin(ph)); }
      var ext = 2 * r0 * (1 + g0.A) + pas; L.push({ x: g0.x, y: g0.y, r: r0, A: g0.A, Hp: Hp, x0: g0.x - ext, x1: g0.x + ext, y0: g0.y - ext, y1: g0.y + ext }); }
    var m = L.length;
    for (k = 0; k < F.length; k++) F[k] = -1;
    for (k = 0; k < m; k++) { var b = L[k], Hb = b.Hp, ia = Math.max(0, Math.floor((b.x0 - x0) / pas)), ib = Math.min(nx - 1, Math.ceil((b.x1 - x0) / pas)), ja = Math.max(0, Math.floor((b.y0 - y0) / pas)), jb = Math.min(ny - 1, Math.ceil((b.y1 - y0) / pas));
      for (j = ja; j <= jb; j++) { var dy = y0 + j * pas - b.y, row = j * nx;
        for (i = ia; i <= ib; i++) { if (F[row + i] > 1.4) continue;   /* déjà profondément dans l'eau : seul le signe compte, rien ne bouge au bord */
          var dx = x0 + i * pas - b.x, d2 = dx * dx + dy * dy; if (d2 > 4 * b.r * b.r * (1 + b.A) * (1 + b.A)) continue;
          var d = Math.sqrt(d2) || 1e-3, c = dx / d, s = dy / d;
          var c2 = c * c - s * s, s2 = 2 * s * c, v = 0;
          for (var h = 0; h < Hb.length; h += 4) { var kk = Hb[h], a;
            if (kk === 2) a = s2 * Hb[h + 2] + c2 * Hb[h + 3];
            else if (kk === 3) a = (s * (3 - 4 * s * s)) * Hb[h + 2] + (c * (4 * c * c - 3)) * Hb[h + 3];
            else a = (2 * s2 * c2) * Hb[h + 2] + (c2 * c2 - s2 * s2) * Hb[h + 3];
            v += Hb[h + 1] * a; }
          var Rr = b.r * (1 + b.A * v), qq = d2 / (4 * Rr * Rr);
          if (qq < 1) { var w = 1 - qq; F[row + i] += w * w * w * 2.3703704; } } } } }
  /* LA ZONE NETTE (le Studio, le +) : une forme à LOBES, serrée sur la boîte de l'icône et de son mot — sa marge varie de 6 à 10 pt (des lobes,
     harmoniques 3, 4, 5 : de 8 à 15 % de son rayon), elle RESPIRE tant qu'elle est ouverte (les lobes tournent, ±0,8 pt) ; 4 à 6 petites
     flaques nettes naissent DANS la boîte, grossissent, fusionnent, et la remplissent ; jouée à l'envers, elle se referme sur elle-même. */
  function zoneNette(boite, gr, opt) {
    opt = opt || {}; var R = alea((gr || 3) * 7919 + 17), cx = boite[0] + boite[2] / 2, cy = boite[1] + boite[3] / 2, hw = boite[2] / 2, hh = boite[3] / 2;
    /* la marge autour de la boîte, selon la direction : DE 6 À 10 pt (Tom, §10.2 ; M0 8 ± 1,6 de lobes ± 0,4 de souffle) — la boîte entière reste nette,
       rien au-delà de 10 pt ; les lobes (harmoniques 3, 4, 5 et 7, poids tirés) font jusqu'à 4 pt d'un creux à une bosse : 8 à 11 % du rayon moyen de la
       zone (36 à 49 pt) — la bande de 6 à 10 pt n'en permet pas plus (QUESTIONS). `opt.plafond` [gauche, haut, droite, bas] borne la marge d'un côté (le Studio : l'Aura est à 8,6 pt de sa boîte, à droite). */
    var M0 = opt.marge0 == null ? 8 : opt.marge0, AMP = opt.lobe == null ? 1.8 : opt.lobe, RESP = 0.2, HL = [], ks = [3, 4, 5, 7], q, PL = opt.plafond || null;
    for (q = 0; q < 4; q++) HL.push({ k: ks[q], c: 0.4 + 0.6 * R(), p: R() * 6.2832, w: (q % 2 ? -0.45 : 0.55) * (0.7 + 0.6 * R()) }); var sc = 0; HL.forEach(function (h) { sc += h.c; }); HL.forEach(function (h) { h.c /= sc; });
    /* les lobes vont d'un bout à l'autre de la bande : la somme des harmoniques est ramenée à [−1, 1] sur le tour (sinon elle n'en fait que ±0,7) */
    var vmin = 1e9, vmax = -1e9; for (q = 0; q < 360; q++) { var t0 = q * 0.017453, v0 = 0; HL.forEach(function (h) { v0 += h.c * Math.sin(h.k * t0 + h.p); }); if (v0 < vmin) vmin = v0; if (v0 > vmax) vmax = v0; }
    var vmil = (vmin + vmax) / 2, vdem = Math.max(1e-3, (vmax - vmin) / 2);
    function marge(c, s, tau) { var th = Math.atan2(s, c), v = 0;
      HL.forEach(function (h) { v += h.c * Math.sin(h.k * th + h.p + h.w * tau); });
      v = Math.max(-1, Math.min(1, (v - vmil) / vdem)); v = (v < 0 ? -1 : 1) * Math.pow(Math.abs(v), 0.45);   /* des lobes francs : la marge s'attarde près de 6 et de 10 pt */
      return M0 + AMP * v + RESP * Math.sin(tau * 1.9); }
    /* les germes : 4 à 6, dans la boîte, répartis (une grille bousculée) */
    var n = 4 + Math.floor(R() * 3), G = [], cols = n <= 4 ? 2 : 3, rows = Math.ceil(n / cols);
    for (q = 0; q < n; q++) { var ci = q % cols, ri = Math.floor(q / cols);
      G.push({ x: boite[0] + boite[2] * ((ci + 0.5) / cols + (R() - 0.5) * 0.3 / cols), y: boite[1] + boite[3] * ((ri + 0.5) / rows + (R() - 0.5) * 0.3 / rows) }); }
    var ordre = G.map(function (g, i) { return i; }); for (q = ordre.length - 1; q > 0; q--) { var b2 = (R() * (q + 1)) | 0, t2 = ordre[q]; ordre[q] = ordre[b2]; ordre[b2] = t2; }
    ordre.forEach(function (i, r) { G[i].t = 0.4 * r / Math.max(1, n - 1) * (0.85 + 0.15 * R()); });
    var dg = Math.sqrt(boite[2] * boite[3] / n);
    G.forEach(function (g) { g.v = 0.7 + 0.6 * R(); g.rmax = dg * (1.15 + 0.35 * R()); g.A = 0.15 + 0.08 * R(); g.H = harmo(R); });
    var Z = { G: G, M0: M0, AMP: AMP, RESP: RESP, boite: boite, cx: cx, cy: cy, hw: hw, hh: hh, marge: marge };
    /* dedans de la forme à lobes : la distance à la boîte, moins la marge de sa direction (≤ 0 dedans) — la boîte elle-même est toujours dedans */
    Z.forme = function (x, y, tau) { var dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy) || 1e-3, m = marge(dx / d, dy / d, tau);
      var ex = Math.max(0, Math.abs(dx) - hw), ey = Math.max(0, Math.abs(dy) - hh);
      /* une cible RONDE (le + : un disque dans son anneau) : la marge se compte depuis le disque, pas depuis les coins de sa boîte */
      var val = opt.rond ? (Math.max(0, d - Math.min(hw, hh)) - m) / 10 : null;
      if (val == null) {
      if (PL && ex + ey > 0) { var cap0 = (ex * (dx > 0 ? PL[2] : PL[0]) + ey * (dy > 0 ? PL[3] : PL[1])) / (ex + ey); if (m > cap0) m = cap0; }
      val = (Math.sqrt(ex * ex + ey * ey) - m) / 10; }
      /* `opt.dans` : la forme qui la contient (la barre : un rectangle aux bouts arrondis) — la zone reste à `retrait` pt EN DEÇÀ de son contour,
         sinon elle découvre le trait de la barre là où son bout s'arrondit (v147 : vu au coin du Studio) */
      if (opt.dans) { var B = opt.dans.b, rr = opt.dans.r, qx = Math.abs(x - (B[0] + B[2] / 2)) - (B[2] / 2 - rr), qy = Math.abs(y - (B[1] + B[3] / 2)) - (B[3] / 2 - rr);
        var sd = Math.sqrt(Math.max(qx, 0) * Math.max(qx, 0) + Math.max(qy, 0) * Math.max(qy, 0)) + Math.min(Math.max(qx, qy), 0) - rr;
        val = Math.max(val, (sd + (opt.dans.retrait || 5)) / 10); }
      return val;
      /* (le plafond d'un côté se lit depuis le point de la boîte le plus proche, pas depuis le centre : droit en face d'un côté, son plafond seul) */
    };
    Z.boiteMax = [boite[0] - M0 - AMP - RESP - 2, boite[1] - M0 - AMP - RESP - 2, boite[2] + 2 * (M0 + AMP + RESP + 2), boite[3] + 2 * (M0 + AMP + RESP + 2)];
    return Z; }

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
    var S = { l: l, h: h, flou: o.flou, uC: 0, uN: 0, sensC: 1, R: null, Rn: null, ent: null, F: null, Fn: null, tau: 0 };
    var PAS = 4, NX = Math.ceil(l / PAS) + 1, NY = Math.ceil(h / PAS) + 1;
    function tire(retrait) {
      graine = (Math.imul(graine, 1664525) + 1013904223) >>> 0;
      /* v147 : les germes des métaballes (12 à 20) ; `S.R` garde la forme d'avant pour les lecteurs (creux = les germes) */
      S.G = germesCouverture(l, h, alea(graine)); S.R = { creux: S.G, nx: NX, ny: NY, pas: PAS };
      S.F = new Float32Array(NX * NY); S.sensC = retrait ? -1 : 1;
    }
    tire(false);
    S.tire = tire;
    S.cible = function (boite, marge, gr, opt) {
      opt = opt || {};
      /* v147 : la zone nette à lobes, ses 4 à 6 flaques (la marge `marge` d'avant n'a plus d'objet : 6 à 10 pt, décidé par Tom) */
      var Z = zoneNette(boite, gr, opt), b = Z.boiteMax, pas = 1.25;
      var x0 = Math.floor(b[0]) - 1, y0 = Math.floor(b[1]) - 1, ll = Math.ceil(b[2]) + 2, hh = Math.ceil(b[3]) + 2, nx = Math.ceil(ll / pas) + 1, ny = Math.ceil(hh / pas) + 1;
      var ent = function (x, y) { return Z.forme(x, y, S.tau) + 1; }; ent.boite = b; ent.zone = Z;
      S.ent = ent; S.Z = Z; S.Rn = { nx: nx, ny: ny, creux: Z.G }; S.Fn = new Float32Array(nx * ny); S.Fm = new Float32Array(nx * ny); S.x0 = x0; S.y0 = y0; S.pasN = pas; S.llN = ll; S.hhN = hh; S.uN = 0;
      return ent;
    };
    /* la zone nette respire tant qu'elle est ouverte : τ en secondes (les lobes tournent, la marge bouge de ±0,8 pt) */
    S.respire = function (tau) { S.tau = tau; };
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
      else { champ(S.F, NX, NY, 0, 0, PAS, S.G, avance(S.uC), S.uC * 3.2); bords += contour(chemin, S.F, NX, NY, 0, 0, PAS); }
      g.save(); g.clip(chemin);
      if (S.flou) g.drawImage(S.flou, 0, 0, l, h); else { g.fillStyle = o.aplat || '#888'; g.fillRect(0, 0, l, h); }
      g.restore();
      /* ② la zone nette : un TROU dans l'eau — dans l'entourage ET sous le niveau « net » (les flaques nettes naissent dedans) */
      if (S.Rn && S.uN > 0) {
        var Rn = S.Rn, Fn = S.Fn, Fm = S.Fm, Z = S.Z, trou = new Path2D(), jj, ii;
        /* dedans de la forme à lobes (−forme) ET dans les flaques nettes (le champ) — à l'ouverture complète, la forme seule */
        if (S.uN < 1) champ(Fm, Rn.nx, Rn.ny, S.x0, S.y0, S.pasN, Z.G, S.uN, S.tau + S.uN * 2.4);
        for (jj = 0; jj < Rn.ny; jj++) for (ii = 0; ii < Rn.nx; ii++) { var q = jj * Rn.nx + ii, a = -Z.forme(S.x0 + ii * S.pasN, S.y0 + jj * S.pasN, S.tau);
          Fn[q] = S.uN >= 1 ? a : Math.min(a, Fm[q]); }
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
    AIR_STUDIO: [0, 0, 0, 0] };   /* v147 : 0 — la marge de 6 à 10 pt se compte depuis la boîte même de l'icône et de son mot (§10.2) */
  /* la boîte d'une cible, élargie de son air */
  function avecAir(b, air) { air = air || [0, 0, 0, 0]; return [b[0] - air[0], b[1] - air[1], b[2] + air[0] + air[2], b[3] + air[1] + air[3]]; }

  racine.Flaques = { GUIDE: GUIDE, avecAir: avecAir, alea: alea, relief: relief, entourage: entourage, contour: contour, niveau: niveau, Scene: Scene, Nappe: Nappe, floute: floute,
    germesCouverture: germesCouverture, zoneNette: zoneNette, champ: champ, rayonA: rayonA, onde: onde, avance: avance };
})(typeof window !== 'undefined' ? window : this);
