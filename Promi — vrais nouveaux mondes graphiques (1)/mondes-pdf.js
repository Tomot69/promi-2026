/* RÉFÉRENCE SEULEMENT — les quatre matières telles qu'elles ont été validées (planche PDF).
 * Ce fichier N'EST PAS livrable : Ritournelle et Madrure y sont peintes pixel par pixel
 * (createImageData / putImageData), ce que le contrat interdit. Il ne sert qu'à comparer,
 * à semis et palette identiques, avec la version écrite au contrat (mondes.js).
 */
(function () {
function creerMondesPDF(env) {
  var g, W, H, seeds, cOf, bg;
  function _sync() { g = env.g; W = env.W; H = env.H; seeds = env.seeds; cOf = env.cOf; bg = env.bg || '#EFE9DE'; }

  function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function hexOf(c) { return 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')'; }
  function nu(c, t) { var b = t > 0 ? 255 : 0, a = Math.abs(t); return [c[0] + (b - c[0]) * a, c[1] + (b - c[1]) * a, c[2] + (b - c[2]) * a]; }
  function cent(p) { var x = 0, y = 0; for (var i = 0; i < p.length; i++) { x += p[i][0]; y += p[i][1]; } return [x / p.length, y / p.length]; }
  function aire(p) { var a = 0; for (var i = 0, j = p.length - 1; i < p.length; j = i++) a += p[j][0] * p[i][1] - p[i][0] * p[j][1]; return Math.abs(a / 2); }
  function clip(p, px, py, nx, ny) {
    var out = [];
    for (var i = 0, j = p.length - 1; i < p.length; j = i++) {
      var A = p[j], B = p[i], da = (A[0] - px) * nx + (A[1] - py) * ny, db = (B[0] - px) * nx + (B[1] - py) * ny;
      if (db <= 0) { if (da > 0) { var t = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]); } out.push(B); }
      else if (da <= 0) { var t2 = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t2, A[1] + (B[1] - A[1]) * t2]); }
    }
    return out;
  }
  function inset(p, d) {
    var c = cent(p), o = [];
    for (var i = 0; i < p.length; i++) { var dx = c[0] - p[i][0], dy = c[1] - p[i][1], l = Math.hypot(dx, dy) || 1, m = Math.min(d, l * 0.5); o.push([p[i][0] + dx / l * m, p[i][1] + dy / l * m]); }
    return o;
  }
  function path(p) { g.beginPath(); g.moveTo(p[0][0], p[0][1]); for (var i = 1; i < p.length; i++) g.lineTo(p[i][0], p[i][1]); g.closePath(); }
  function smooth(p) {
    var n = p.length; g.beginPath(); g.moveTo((p[n - 1][0] + p[0][0]) / 2, (p[n - 1][1] + p[0][1]) / 2);
    for (var i = 0; i < n; i++) { var a = p[i], b = p[(i + 1) % n]; g.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); }
    g.closePath();
  }
  function sp() { return Math.sqrt(W * H / Math.max(1, seeds.length)); }
  function near(x, y) {
    var b = seeds[0], bd = 1e18, b2 = 1e18;
    for (var i = 0; i < seeds.length; i++) { var s = seeds[i], d = Math.hypot(x - s.x, y - s.y) - (s.w || 0); if (d < bd) { b2 = bd; bd = d; b = s; } else if (d < b2) b2 = d; }
    return { s: b, d1: bd, d2: b2 };
  }
  function shapeOf(s, N, ox, oy) {
    var st = sp() * 0.05, pts = [], cx = ox === undefined ? s.x : ox, cy = oy === undefined ? s.y : oy;
    for (var i = 0; i < N; i++) {
      var a = i / N * 6.283, cs = Math.cos(a), sn = Math.sin(a), r = st;
      while (r < sp() * 2.4) { if (near(cx + cs * (r + st), cy + sn * (r + st)).s !== s) break; r += st; }
      pts.push([cx + cs * r, cy + sn * r]);
    }
    return pts;
  }
  function relax(p, it) {
    var q = p.map(function (v) { return v.slice(); });
    for (var t = 0; t < it; t++) { var n = q.length, r = []; for (var i = 0; i < n; i++) { var a = q[(i - 1 + n) % n], b = q[i], c = q[(i + 1) % n]; r.push([(a[0] + 2 * b[0] + c[0]) / 4, (a[1] + 2 * b[1] + c[1]) / 4]); } q = r; }
    return q;
  }
  function hex(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }

  /* Esquille — la plaque brisée : la Toile ENTIÈRE est cassée, la couleur suit le propriétaire */
  function esquille(now) {
    _sync();
    var R = rng(1234567), s0 = sp(), minA = s0 * s0 * 0.17;
    var shards = [[[0, 0], [W, 0], [W, H], [0, H]]];
    for (var pass = 0; pass < 9; pass++) {
      var next = [];
      for (var e = 0; e < shards.length; e++) {
        var p = shards[e];
        if (aire(p) < minA) { next.push(p); continue; }
        var c = cent(p), lx = 0, ly = 0, best = -1;
        for (var i = 0; i < p.length; i++) for (var j = i + 1; j < p.length; j++) { var dx = p[j][0] - p[i][0], dy = p[j][1] - p[i][1], dd = dx * dx + dy * dy; if (dd > best) { best = dd; lx = dx; ly = dy; } }
        var la = Math.atan2(ly, lx) + (R() - 0.5) * 0.9;
        var jx = c[0] + (R() - 0.5) * s0 * 0.22, jy = c[1] + (R() - 0.5) * s0 * 0.22;
        var A = clip(p, jx, jy, Math.cos(la), Math.sin(la)), B = clip(p, jx, jy, -Math.cos(la), -Math.sin(la));
        if (A.length > 2) next.push(A); if (B.length > 2) next.push(B);
      }
      shards = next;
    }
    for (var k = 0; k < shards.length; k++) {
      var q = shards[k]; if (q.length < 3 || aire(q) < s0 * s0 * 0.008) continue;
      var ct = cent(q), n = near(ct[0], ct[1]);
      g.fillStyle = hexOf(R() < 0.18 ? nu(cOf(n.s, now), -0.18) : cOf(n.s, now));
      path(inset(q, Math.min(s0 * 0.02, Math.sqrt(aire(q)) * 0.09))); g.fill();
    }
  }

  /* Bobinette — le fil enroulé : arcs de Truchet gainés de fond, anneaux épaissis */
  function bobinette(now) {
    _sync();
    var count = seeds.length;
    var cmax = Math.sqrt(0.62 * W * H / Math.max(1, count)), c = Math.min(Math.min(W, H) / 9, cmax);
    var cols = Math.ceil(W / c) + 1, rows = Math.ceil(H / c) + 1, th = c * 0.26, casing = c * 0.44;
    var R = rng(4242), anneau = {}, flips = {};
    function poser(gi, gj) { anneau[gi + '|' + gj] = 1; flips[(gi - 1) + ',' + (gj - 1)] = 1; flips[gi + ',' + (gj - 1)] = 0; flips[(gi - 1) + ',' + gj] = 0; flips[gi + ',' + gj] = 1; }
    for (var i = 0; i < seeds.length; i++) poser(Math.round(seeds[i].x / c), Math.round(seeds[i].y / c));
    var tiles = [];
    for (var a = -1; a < cols; a++) for (var b = -1; b < rows; b++) {
      var x = a * c, y = b * c, f = flips[a + ',' + b];
      if (f === undefined) f = R() < 0.5 ? 1 : 0;
      var arcs = f ? [[x, y, 0, Math.PI / 2], [x + c, y + c, Math.PI, Math.PI * 1.5]] : [[x + c, y, Math.PI / 2, Math.PI], [x, y + c, Math.PI * 1.5, Math.PI * 2]];
      for (var t = 0; t < 2; t++) {
        var A = arcs[t], mx = A[0] + Math.cos((A[2] + A[3]) / 2) * c / 2, my = A[1] + Math.sin((A[2] + A[3]) / 2) * c / 2;
        var n = near(mx, my);
        tiles.push({ a: A, col: hexOf(n.d1 / (n.d1 + n.d2) > 0.42 ? nu(cOf(n.s, now), 0.18) : cOf(n.s, now)), k: ((a * 3 + b * 5) % 7 + 7) % 7, tile: !!anneau[Math.round(A[0] / c) + '|' + Math.round(A[1] / c)] });
      }
    }
    tiles.sort(function (p, q) { return p.k - q.k; });
    g.save(); g.lineCap = 'butt';
    for (var m = 0; m < tiles.length; m++) {
      var T = tiles[m], A2 = T.a, extra = T.tile ? th * 0.55 : 0;
      g.strokeStyle = bg; g.lineWidth = casing + extra;
      g.beginPath(); g.arc(A2[0], A2[1], c / 2 - extra / 2, A2[2] - 0.05, A2[3] + 0.05); g.stroke();
      g.strokeStyle = T.col; g.lineWidth = th + extra;
      g.beginPath(); g.arc(A2[0], A2[1], c / 2 - extra / 2, A2[2] - 0.05, A2[3] + 0.05); g.stroke();
    }
    g.restore();
  }

  /* Ritournelle — la coulée : anneaux emboîtés, QUATRE tons de palette (ce qu'un monde ne peut pas faire) */
  function ritournelle(now) {
    _sync();
    var s0 = sp(), NA = 90, R = rng(99);
    for (var i = 0; i < seeds.length; i++) {
      var s = seeds[i];
      var c0 = cent(shapeOf(s, 16));
      var cell = shapeOf(s, NA, c0[0], c0[1]);
      var h = [[2, R() * 6.283, 0.05 + R() * 0.03], [3, R() * 6.283, 0.022 + R() * 0.018], [5, R() * 6.283, 0.01 + R() * 0.01]];
      var lim = [];
      for (var k = 0; k < NA; k++) {
        var ang = k / NA * 6.283, m = 1;
        for (var q = 0; q < 3; q++) m += Math.sin(ang * h[q][0] + h[q][1]) * h[q][2];
        var cellR = Math.hypot(cell[k][0] - c0[0], cell[k][1] - c0[1]);
        lim.push(cellR * (0.72 + 0.28 * m) - s0 * 0.006);
      }
      for (var pass = 0; pass < 8; pass++) { var nx = []; for (var z = 0; z < NA; z++) nx.push((lim[(z - 1 + NA) % NA] + 2 * lim[z] + lim[(z + 1) % NA]) / 4); lim = nx; }
      var bord = [];
      for (var z2 = 0; z2 < NA; z2++) { var a2 = z2 / NA * 6.283; bord.push([c0[0] + Math.cos(a2) * lim[z2], c0[1] + Math.sin(a2) * lim[z2]]); }
      var base = cOf(s, now), tons = [base, nu(base, 0.34), nu(base, -0.3), nu(base, 0.16)];
      var couches = 4 + (i % 3);
      for (var k2 = 0; k2 < couches; k2++) {
        var fr = 1 - k2 / couches, ring = [];
        for (var z3 = 0; z3 < NA; z3++) ring.push([c0[0] + (bord[z3][0] - c0[0]) * fr, c0[1] + (bord[z3][1] - c0[1]) * fr]);
        g.fillStyle = hexOf(tons[k2 % 4]); smooth(ring); g.fill();
      }
    }
  }

  /* Madrure — l'onde du bois, pixel par pixel (INTERDIT en production, référence seulement) */
  function madrure(now) {
    _sync();
    var s0 = sp(), SS = 1, iw = W * SS, ih = H * SS;
    var img = g.createImageData(iw, ih), d = img.data;
    var R = rng(777), band = s0 * 0.16 * SS;
    var th = R() * 6.283, ct = Math.cos(th), st = Math.sin(th);
    var K = [], bgc = hex(bg);
    for (var i = 0; i < seeds.length; i++) K.push({ s: seeds[i], x: seeds[i].x * SS, y: seeds[i].y * SS, k: band * (2.1 + R() * 0.9), r: s0 * SS * (0.42 + R() * 0.16) });
    // les quatre tons bruts de la palette, répartis comme sur la planche : c, c2, c3 par nœud
    var PAL = env.PAL;
    var cols = [];
    for (var z = 0; z < seeds.length; z++) {
      var s0 = seeds[z], ci = s0.ci | 0;
      var c2 = (ci + 1 + (z % 3)) % 4; if (c2 === ci) c2 = (ci + 2) % 4;
      var rest = [0, 1, 2, 3].filter(function (k) { return k !== ci && k !== c2; });
      var c3 = rest[z % 2];
      cols.push([PAL[ci], PAL[c2], PAL[c3]]);
    }
    for (var y = 0; y < ih; y++) for (var x = 0; x < iw; x++) {
      var phi = x * ct + y * st, own = -1, bd = 1e18;
      for (var k3 = 0; k3 < K.length; k3++) {
        var Kk = K[k3], dx = x - Kk.x, dy = y - Kk.y, dd = dx * dx + dy * dy;
        if (dd < bd) { bd = dd; own = k3; }
        phi += Kk.k / (1 + dd / (Kk.r * Kk.r));
      }
      var v = phi / band, b = Math.floor(v), fr = v - b, m = ((b % 3) + 3) % 3;
      var col = fr < 0.11 ? cols[own][2] : m === 2 ? null : (m === 0 ? cols[own][0] : cols[own][1]);
      var c2 = col || bgc, i4 = (y * iw + x) * 4;
      d[i4] = c2[0]; d[i4 + 1] = c2[1]; d[i4 + 2] = c2[2]; d[i4 + 3] = 255;
    }
    g.putImageData(img, 0, 0);
  }

  return { esquille: esquille, bobinette: bobinette, ritournelle: ritournelle, madrure: madrure };
}
window.creerMondesPDF = creerMondesPDF;
})();
