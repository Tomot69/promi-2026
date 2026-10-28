import io
F='variantes/trace-lettres.js'; S=io.open(F,encoding='utf-8').read()
o="""        for (y = 0; y < H2; y++) for (x = 0; x < W2; x++) { p = (y * W2 + x) * 4 + 3; if (a1[p] < 8 || a2[p] >= 255) continue;
          var bt = Infinity, dy2, dx2;
          for (dy2 = -2; dy2 <= 2; dy2++) for (dx2 = -2; dx2 <= 2; dx2++) { var xx = x + dx2, yy = y + dy2; if (xx < 0 || yy < 0 || xx >= W2 || yy >= H2) continue; if (a2[(yy * W2 + xx) * 4 + 3] < 255) continue; var tq = tCouvert(xx, yy); if (tq < bt) bt = tq; }
          if (bt === Infinity) { var lx = lx0 + (x + 0.5) / s0, ly = ly0 + (y + 0.5) / s0, bd = Infinity; for (var k = 0; k < segs.length; k++) { var pr = proj(lx, ly, k); if (pr[0] < bd) { bd = pr[0]; bt = pr[1]; } } }
          L.push([bt, lx0 + x / s0, ly0 + y / s0]); }
"""
n="""        var TR = {}, reste = [];
        for (y = 0; y < H2; y++) for (x = 0; x < W2; x++) { p = (y * W2 + x) * 4 + 3; if (a1[p] < 8 || a2[p] >= 255) continue;
          var bt = Infinity, dy2, dx2;
          for (dy2 = -2; dy2 <= 2; dy2++) for (dx2 = -2; dx2 <= 2; dx2++) { var xx = x + dx2, yy = y + dy2; if (xx < 0 || yy < 0 || xx >= W2 || yy >= H2) continue; if (a2[(yy * W2 + xx) * 4 + 3] < 255) continue; var tq = tCouvert(xx, yy); if (tq < bt) bt = tq; }
          TR[x + ',' + y] = bt; reste.push([x, y]); }
        /* une grappe de restes loin de toute bande : l'instant se propage de proche en proche depuis ses voisins datés, au pas du front (un pixel = sa
           longueur de chemin) — jamais le point de chemin le plus proche, qui pouvait être un autre trait : un point isolé paraissait devant le front */
        for (var tour = 0, change = true; change && tour < 40; tour++) { change = false;
          reste.forEach(function (q) { var key = q[0] + ',' + q[1], b0 = TR[key];
            for (var dy3 = -1; dy3 <= 1; dy3++) for (var dx3 = -1; dx3 <= 1; dx3++) { var v3 = TR[(q[0] + dx3) + ',' + (q[1] + dy3)]; if (v3 === undefined) continue; v3 += Math.hypot(dx3, dy3) / (s0 * g.sc); if (v3 < b0) b0 = v3; }
            if (b0 < TR[key]) { TR[key] = b0; change = true; } }); }
        reste.forEach(function (q) { var bt = TR[q[0] + ',' + q[1]];
          if (bt === Infinity) { var lx = lx0 + (q[0] + 0.5) / s0, ly = ly0 + (q[1] + 0.5) / s0, bd = Infinity; for (var k = 0; k < segs.length; k++) { var pr = proj(lx, ly, k); if (pr[0] < bd) { bd = pr[0]; bt = pr[1]; } } }
          L.push([bt, lx0 + q[0] / s0, ly0 + q[1] / s0]); });
"""
assert S.count(o)==1; S=S.replace(o,n); io.open(F,'w',encoding='utf-8').write(S)
