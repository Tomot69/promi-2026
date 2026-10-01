/* LES QUATRE FONCTIONS D'ORIGINE — telles qu'écrites dans « Promi - Toiles iPhone.dc.html »,
 * celles dont la planche PDF est sortie. Rien n'est adapté ici : c'est la source de vérité du portage.
 *
 * Correspondance des noms : faille = Esquille · noeud = Bobinette · coulee = Ritournelle · ecume = Madrure
 *
 * Contexte dont elles dépendent (reproduit plus bas, verbatim) :
 *   C          les QUATRE couleurs brutes de la palette (pas cOf)
 *   F.sites    les graines, chacune portant c, c2, c3 (trois index de palette), ph, w, empty
 *   F.spacing  l'écart moyen entre graines  (= avg())
 *   F.near     le propriétaire d'un point, avec d1 et d2
 *   F.shapeOf  le contour réel d'une cellule, obtenu en marchant du germe vers la lisière
 *   F.R        le hasard : UN SEUL flux, consommé dans l'ordre du tracé
 *   L.*        polygones : area, centroid, clipHalf, inset, pathPoly, smoothPath, relax, blob, hex
 *   bg         la couleur de fond de la Toile (posée en dur par la page)
 */

// ============================== LES QUATRE MONDES ==============================

  worlds = {
    // Esquille — plaque brisée
    faille(ctx, W, H, F, C, L) {
      const sp = F.spacing, minA = sp * sp * 0.17;
      let shards = [[[0, 0], [W, 0], [W, H], [0, H]]];
      for (let pass = 0; pass < 9; pass++) {
        const next = [];
        shards.forEach(p => {
          if (L.area(p) < minA) { next.push(p); return; }
          const c = L.centroid(p);
          let lx = 0, ly = 0, best = -1;
          for (let i = 0; i < p.length; i++) for (let j = i + 1; j < p.length; j++) {
            const dx = p[j][0] - p[i][0], dy = p[j][1] - p[i][1], dd = dx * dx + dy * dy;
            if (dd > best) { best = dd; lx = dx; ly = dy; }
          }
          const la = Math.atan2(ly, lx) + (F.R() - 0.5) * 0.9, nx = Math.cos(la), ny = Math.sin(la);
          const jx = c[0] + (F.R() - 0.5) * sp * 0.22, jy = c[1] + (F.R() - 0.5) * sp * 0.22;
          const A = L.clipHalf(p, jx, jy, nx, ny), B = L.clipHalf(p, jx, jy, -nx, -ny);
          if (A.length > 2) next.push(A); if (B.length > 2) next.push(B);
        });
        shards = next;
      }
      shards.forEach(p => {
        const q = [];
        p.forEach(v => { const l = q[q.length - 1]; if (!l || Math.hypot(l[0] - v[0], l[1] - v[1]) > 0.6) q.push(v); });
        while (q.length > 2 && Math.hypot(q[0][0] - q[q.length - 1][0], q[0][1] - q[q.length - 1][1]) < 0.6) q.pop();
        if (q.length < 3) return;
        const a = L.area(q); if (a < sp * sp * 0.008) return;
        const c = L.centroid(q), n = F.near(c[0], c[1]);
        const ins = L.inset(q, Math.min(sp * 0.02, Math.sqrt(a) * 0.09));
        if (F.showEmpty && n.s.empty) {
          ctx.strokeStyle = C[n.s.c]; ctx.lineWidth = Math.max(1, sp * 0.022);
          L.pathPoly(ctx, L.inset(ins, sp * 0.012)); ctx.stroke();
        } else {
          ctx.fillStyle = C[F.R() < 0.18 ? n.s.c2 : n.s.c];
          L.pathPoly(ctx, ins); ctx.fill();
        }
      });
    },

    // Guipure — fils tissés, anneaux fermés = dalles ; la maille rétrécit quand la toile s'étoffe
    noeud(ctx, W, H, F, C, L, bg) {
      const count = F.count || F.sites.length;
      // maille fixe : la toile ne dézoome pas, elle se peuple d'anneaux
      const cmax = Math.sqrt(0.62 * W * H / (4 * Math.max(1, count)));
      const c = Math.min(Math.min(W, H) / 9, cmax);
      const cols = Math.ceil(W / c) + 1, rows = Math.ceil(H / c) + 1;
      ctx.lineCap = 'butt';
      const th = c * 0.26, casing = c * 0.44;
      const ringAt = {}, flips = {}, ringCore = {};
      const mark = (gi, gj) => {
        ringAt[gi + ':' + gj] = 1;
        ringCore[gi + '|' + gj] = 1;
        flips[(gi - 1) + ',' + (gj - 1)] = true;
        flips[gi + ',' + (gj - 1)] = false;
        flips[(gi - 1) + ',' + gj] = false;
        flips[gi + ',' + gj] = true;
      };
      let placed = 0, guard = 0;
      while (placed < count && guard++ < count * 200) {
        const gi = 1 + Math.floor(F.R() * (cols - 1)), gj = 1 + Math.floor(F.R() * (rows - 1));
        if (ringAt[gi + ':' + gj]) continue;
        let close = false;
        for (let a = gi - 1; a <= gi + 1 && !close; a++) for (let b = gj - 1; b <= gj + 1; b++) if (ringAt[a + ':' + b]) { close = true; break; }
        if (close) continue;
        mark(gi, gj); placed++;
      }
      const tiles = [];
      for (let i = -1; i < cols; i++) for (let j = -1; j < rows; j++) {
        const x = i * c, y = j * c;
        const forced = flips[i + ',' + j];
        const flip = forced === undefined ? F.R() < 0.5 : forced;
        const arcs = flip
          ? [[x, y, 0, Math.PI / 2], [x + c, y + c, Math.PI, Math.PI * 1.5]]
          : [[x + c, y, Math.PI / 2, Math.PI], [x, y + c, Math.PI * 1.5, Math.PI * 2]];
        arcs.forEach(a => {
          const mx = a[0] + Math.cos((a[2] + a[3]) / 2) * c / 2, my = a[1] + Math.sin((a[2] + a[3]) / 2) * c / 2;
          const n = F.near(mx, my);
          // un arc appartient à une dalle si son centre est le coin d'un anneau de promesse
          const gi = Math.round(a[0] / c), gj = Math.round(a[1] / c);
          const isTile = !!ringCore[gi + '|' + gj];
          tiles.push({ a, col: C[(n.d1 / (n.d1 + n.d2)) > 0.42 ? n.s.c2 : n.s.c], k: ((i * 3 + j * 5) % 7 + 7) % 7, thin: F.showEmpty && n.s.empty, tile: isTile });
        });
      }
      tiles.sort((p, q) => p.k - q.k);
      tiles.forEach(t => {
        const a = t.a;
        ctx.strokeStyle = bg; ctx.lineWidth = casing;
        ctx.beginPath(); ctx.arc(a[0], a[1], c / 2, a[2] - 0.05, a[3] + 0.05); ctx.stroke();
        // l'anneau d'une promesse est épaissi vers l'intérieur : on l'identifie sans dénaturer le tissage
        const extra = t.tile && !t.thin ? th * 0.55 : 0;
        ctx.strokeStyle = t.col; ctx.lineWidth = (t.thin ? th * 0.42 : th) + extra;
        ctx.beginPath(); ctx.arc(a[0], a[1], c / 2 - extra / 2, a[2] - 0.05, a[3] + 0.05); ctx.stroke();
      });
    },

    // Empois — puddle pour : des flaques d'anneaux versées sur la toile, qui se touchent et s'aplatissent
    coulee(ctx, W, H, F, C, L, bg) {
      const sp = F.spacing, SS = 3, iw = W * SS, ih = H * SS, NA = 144;
      const off = document.createElement('canvas'); off.width = iw; off.height = ih;
      const octx = off.getContext('2d');
      const img = octx.createImageData(iw, ih), d = img.data;
      const rgb = C.map(L.hex), bgc = L.hex(bg);
      // pour chaque flaque : la limite d'étalement, libre et ronde, rognée là où la voisine touche
      const info = new Map();
      F.sites.forEach(s => {
        const c0 = L.centroid(F.shapeOf(s, 16));
        const cell = F.shapeOf(s, NA, c0[0], c0[1]);
        const h = [];
        // la coulée n'est pas régulière : deux ou trois lobes doux, comme une flaque qui file
        // presque ronde : l'irrégularité vient du contact avec la voisine, pas d'une déformation
        // le bord d'une coulée : un lobe dominant, deux ondulations fines, rien de plus
        h.push([2, F.R() * 6.283, 0.05 + F.R() * 0.03]);
        h.push([3, F.R() * 6.283, 0.022 + F.R() * 0.018]);
        h.push([5, F.R() * 6.283, 0.01 + F.R() * 0.01]);
        const rad = sp;
        const lim = new Float64Array(NA);
        for (let i = 0; i < NA; i++) {
          const a = i / NA * 6.283;
          let m = 1; h.forEach(q => { m += Math.sin(a * q[0] + q[1]) * q[2]; });
          const cellR = Math.hypot(cell[i][0] - c0[0], cell[i][1] - c0[1]);
          // la coulée remplit sa place : le bord ondule un peu, le liseré reste constant
          lim[i] = cellR * (0.72 + 0.28 * m) - sp * 0.006;
        }
        // lissage du rayon limite : le liquide n'a ni angle ni aspérité
        let sm = lim;
        for (let pass = 0; pass < 8; pass++) {
          const nx = new Float64Array(NA);
          for (let i = 0; i < NA; i++) nx[i] = (sm[(i - 2 + NA) % NA] + 2 * sm[(i - 1 + NA) % NA] + 3 * sm[i] + 2 * sm[(i + 1) % NA] + sm[(i + 2) % NA]) / 9;
          sm = nx;
        }
        info.set(s, { cx: c0[0] * SS, cy: c0[1] * SS, lim: sm, rings: 3 + Math.floor(F.R() * 3), off: Math.floor(F.R() * 4), empty: s.empty });
      });
      for (let y = 0; y < ih; y++) for (let x = 0; x < iw; x++) {
        const q = F.near(x / SS, y / SS);
        const P = info.get(q.s);
        const dx = x - P.cx, dy = y - P.cy, dd = Math.sqrt(dx * dx + dy * dy);
        let a = Math.atan2(dy, dx) / 6.283 * NA; if (a < 0) a += NA;
        const i0 = Math.floor(a), fa = a - i0;
        const limit = (P.lim[i0 % NA] * (1 - fa) + P.lim[(i0 + 1) % NA] * fa) * SS;
        const i4 = (y * iw + x) * 4;
        let col = bgc;
        if (dd <= limit) {
          const t = dd / limit;
          if (F.showEmpty && P.empty) {
            // promesse plantée, pas encore tenue : la coulée n'a laissé que son bord
            if (t > 0.84) col = rgb[P.off % 4];
          } else {
            // anneaux concentriques qui épousent le contour de la flaque
            const k = Math.floor(Math.pow(t, 0.8) * P.rings);
            col = rgb[(k + P.off) % 4];        // même ordre de gobelet d'une flaque à l'autre
          }
        }
        d[i4] = col[0]; d[i4 + 1] = col[1]; d[i4 + 2] = col[2]; d[i4 + 3] = 255;
      }
      octx.putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(off, 0, 0, W, H);
    },

    // Madrure — le fil du bois : veines continues, boucles fermées autour de chaque nœud
    ecume(ctx, W, H, F, C, L, bg) {
      const sp = F.spacing, R = F.R, SS = 3, iw = W * SS, ih = H * SS;
      const th = R() * 6.283, ct = Math.cos(th), st = Math.sin(th);
      const band = sp * 0.17 * SS;
      // le bombement est calé sur la largeur de veine : la densité reste la même quand la toile s'étoffe
      const knots = F.sites.map(s => ({ s, x: s.x * SS, y: s.y * SS, k: band * (7.5 + R() * 2), r: sp * SS * (0.36 + R() * 0.12) }));
      const offc = document.createElement('canvas'); offc.width = iw; offc.height = ih;
      const octx = offc.getContext('2d');
      const img = octx.createImageData(iw, ih), d = img.data;
      const rgb = C.map(L.hex), bgc = L.hex(bg);
      for (let y = 0; y < ih; y++) for (let x = 0; x < iw; x++) {
        let phi = x * ct + y * st;
        let own = null, bestD = 1e9;
        for (let i = 0; i < knots.length; i++) {
          const K = knots[i], dx = x - K.x, dy = y - K.y, dd = dx * dx + dy * dy;
          if (dd < bestD) { bestD = dd; own = K; }
          phi += K.k / (1 + dd / (K.r * K.r));
        }
        const v = phi / band, b = Math.floor(v), fr = v - b;
        const m = ((b % 3) + 3) % 3;
        // trois veines qui alternent, un trait fin de séparation, le fond entre deux
        let col = fr < 0.11 ? rgb[0] : m === 2 ? null : rgb[m === 0 ? 1 : 2];
        if (F.showEmpty && own.s.empty && bestD < own.r * own.r * 1.15 && fr >= 0.11) col = null;
        const c = col || bgc;
        const i4 = (y * iw + x) * 4;
        d[i4] = c[0]; d[i4 + 1] = c[1]; d[i4 + 2] = c[2]; d[i4 + 3] = 255;
      }
      octx.putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(offc, 0, 0, W, H);
    }
  };


// ============================== LE CONTEXTE ==============================

  lib = (function () {
    function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
    function pathPoly(ctx, p) { ctx.beginPath(); ctx.moveTo(p[0][0], p[0][1]); for (let i = 1; i < p.length; i++) ctx.lineTo(p[i][0], p[i][1]); ctx.closePath(); }
    function smoothPath(ctx, p) {
      const n = p.length;
      ctx.beginPath();
      ctx.moveTo((p[n - 1][0] + p[0][0]) / 2, (p[n - 1][1] + p[0][1]) / 2);
      for (let i = 0; i < n; i++) {
        const a = p[i], b = p[(i + 1) % n];
        ctx.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
      }
      ctx.closePath();
    }
    function centroid(p) { let x = 0, y = 0; p.forEach(q => { x += q[0]; y += q[1]; }); return [x / p.length, y / p.length]; }
    function area(p) { let a = 0; for (let i = 0, j = p.length - 1; i < p.length; j = i++) a += p[j][0] * p[i][1] - p[i][0] * p[j][1]; return Math.abs(a / 2); }
    function clipHalf(p, px, py, nx, ny) {
      const out = [], d = q => (q[0] - px) * nx + (q[1] - py) * ny;
      for (let i = 0, j = p.length - 1; i < p.length; j = i++) {
        const A = p[j], B = p[i], da = d(A), db = d(B);
        if (db <= 0) { if (da > 0) { const t = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]); } out.push(B); }
        else if (da <= 0) { const t = da / (da - db); out.push([A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]); }
      }
      return out;
    }
    function inset(p, d) {
      const c = centroid(p);
      return p.map(q => { const dx = c[0] - q[0], dy = c[1] - q[1], l = Math.hypot(dx, dy) || 1; return [q[0] + dx / l * Math.min(d, l * 0.5), q[1] + dy / l * Math.min(d, l * 0.5)]; });
    }
    // contour libre : harmoniques basses, aucune arête
    function blob(cx, cy, rad, R, N) {
      const h = [];
      for (let i = 0; i < 3; i++) h.push([(0.085 + R() * 0.075) / (i + 1), R() * 6.283]);
      const pts = [];
      for (let i = 0; i < (N || 90); i++) {
        const a = i / (N || 90) * 6.283;
        let m = 1;
        h.forEach((q, k) => { m += Math.sin(a * (k + 2) + q[1]) * q[0]; });
        pts.push([cx + Math.cos(a) * rad * m, cy + Math.sin(a) * rad * m]);
      }
      return pts;
    }
    // relâche un contour : moyenne avec ses voisins, les fripures disparaissent
    function relax(p, iter) {
      let q = p.map(v => v.slice());
      for (let t = 0; t < (iter || 2); t++) {
        const n = q.length, r = [];
        for (let i = 0; i < n; i++) {
          const a = q[(i - 1 + n) % n], b = q[i], c = q[(i + 1) % n];
          r.push([(a[0] + 2 * b[0] + c[0]) / 4, (a[1] + 2 * b[1] + c[1]) / 4]);
        }
        q = r;
      }
      return q;
    }
    const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
    return { rng, pathPoly, smoothPath, centroid, area, clipHalf, inset, blob, relax, hex };
  })();


  makeField(W, H, cell, seed, limit) {
    const L = this.lib, R = L.rng(seed * 7919 + 13);
    const cols = Math.max(2, Math.round(W / cell)), rows = Math.max(2, Math.round(H / cell));
    const sx = W / cols, sy = H / rows;
    let sites = [];
    for (let j = -1; j <= rows; j++) for (let i = -1; i <= cols; i++)
      sites.push({ x: (i + 0.5 + (R() - 0.5) * 0.62) * sx, y: (j + 0.5 + (R() - 0.5) * 0.62) * sy, w: 0.84 + R() * 0.32, i: sites.length, ord: 0 });
    // ordre d'arrivée des promesses : la toile grandit toujours dans le même ordre
    sites.forEach(s => { s.ord = R(); });
    if (limit) {
      const inside = sites.filter(s => s.x > 0 && s.x < W && s.y > 0 && s.y < H).sort((a, b) => a.ord - b.ord).slice(0, limit);
      const out = sites.filter(s => !(s.x > 0 && s.x < W && s.y > 0 && s.y < H));
      sites = inside;
      sites.forEach((s, k) => { s.i = k; });
    }
    const spacing = (sx + sy) / 2;
    const a = spacing * 0.3, ph = [R() * 6.283, R() * 6.283, R() * 6.283, R() * 6.283];
    const l1 = spacing * 0.95, l2 = spacing * 1.4;
    const warp = (x, y, o) => {
      o[0] = x + a * Math.sin(y / l1 + ph[0]) + a * 0.45 * Math.sin(y / l2 + ph[2]);
      o[1] = y + a * Math.sin(x / l1 + ph[1]) + a * 0.45 * Math.sin(x / l2 + ph[3]);
    };
    const bw = Math.ceil(W / spacing) + 3, bh = Math.ceil(H / spacing) + 3, buckets = [];
    for (let i = 0; i < bw * bh; i++) buckets.push([]);
    sites.forEach(s => {
      const bx = Math.max(0, Math.min(bw - 1, Math.floor(s.x / spacing) + 1)), by = Math.max(0, Math.min(bh - 1, Math.floor(s.y / spacing) + 1));
      buckets[by * bw + bx].push(s);
    });
    const tmp = [0, 0];
    const near = (x, y, raw) => {
      let wx = x, wy = y;
      if (!raw) { warp(x, y, tmp); wx = tmp[0]; wy = tmp[1]; }
      const bx = Math.max(0, Math.min(bw - 1, Math.floor(wx / spacing) + 1)), by = Math.max(0, Math.min(bh - 1, Math.floor(wy / spacing) + 1));
      let d1 = 1e9, d2 = 1e9, s1 = null;
      for (let j = by - 1; j <= by + 1; j++) for (let i = bx - 1; i <= bx + 1; i++) {
        if (i < 0 || j < 0 || i >= bw || j >= bh) continue;
        const b = buckets[j * bw + i];
        for (let k = 0; k < b.length; k++) {
          const s = b[k], dx = s.x - wx, dy = s.y - wy, d = Math.sqrt(dx * dx + dy * dy) / s.w;
          if (d < d1) { d2 = d1; d1 = d; s1 = s; } else if (d < d2) d2 = d;
        }
      }
      if (!s1) {
        for (let k = 0; k < sites.length; k++) {
          const s = sites[k], dx = s.x - wx, dy = s.y - wy, d = Math.sqrt(dx * dx + dy * dy) / s.w;
          if (d < d1) { d2 = d1; d1 = d; s1 = s; } else if (d < d2) d2 = d;
        }
      }
      if (d2 > 1e8) d2 = d1 * 3;
      return { s: s1, d1, d2 };
    };
    sites.forEach(s => {
      const used = {};
      sites.forEach(o => { if (o !== s && o.c !== undefined && Math.hypot(o.x - s.x, o.y - s.y) < spacing * 1.45) used[o.c] = 1; });
      let c = 0; while (used[c] && c < 3) c++;
      s.c = c;
      s.c2 = (c + 1 + Math.floor(R() * 3)) % 4; if (s.c2 === c) s.c2 = (c + 2) % 4;
      s.c3 = [0, 1, 2, 3].filter(k => k !== c && k !== s.c2)[Math.floor(R() * 2)];
      s.ph = R() * 6.283;
      s.empty = R() < 0.32;      // promesse plantée mais pas encore tenue
    });
    // contour réel d'une promesse : on marche du germe vers la lisière, dans toutes les directions
    const shapeOf = (s, N, ox, oy) => {
      const n = N || 56, pts = [], step = spacing * 0.05;
      const cx = ox === undefined ? s.x : ox, cy = oy === undefined ? s.y : oy;
      for (let i = 0; i < n; i++) {
        const ang = i / n * 6.283, cs = Math.cos(ang), sn = Math.sin(ang);
        let r = step;
        while (r < spacing * 2.4) {
          const q = near(cx + cs * (r + step), cy + sn * (r + step));
          if (q.s !== s) break;
          r += step;
        }
        pts.push([cx + cs * r, cy + sn * r]);
      }
      return pts;
    };
    return { sites, spacing, near, shapeOf, R };
  }

