# v40 (Tom, 24 sept.) — Madrure : l'onde n'est plus un plan ; l'aperçu du Studio porte 10 nœuds au lieu de 5.
import io, sys
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
S = io.open(F, encoding='utf-8').read()

o = "    if (n > 5 && P[0].s && P[0].s.apercu) { P = P.slice().sort(function (a, b) { return a.k - b.k; }).slice(0, 5); n = P.length; }"
assert S.count(o) == 1
S = S.replace(o, "    // v40 (Tom, 24 sept.) : « il n'y a plus assez de nœuds, mets-en deux fois plus » — DIX nœuds dans l'aperçu (étaient cinq)\n"
                 "    if (n > 10 && P[0].s && P[0].s.apercu) { P = P.slice().sort(function (a, b) { return a.k - b.k; }).slice(0, 10); n = P.length; }")

o = "    var ct = Math.cos(th) / band, st = Math.sin(th) / band;\n"
assert S.count(o) == 1
S = S.replace(o, o + r'''    /* ⚑ v40 (Tom, 24 sept.) — L'ONDE N'EST PLUS UN PLAN. « Là ça me fait que des lignes parallèles et des nœuds parfois ; on
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
''')

# la grille : séparable (sin(a+b) = sin a cos b + cos a sin b) — deux produits par onde et par point
o = "    var V = new Float64Array(rw * (ny + 1)), vmin = 1e18, vmax = -1e18;\n"
assert S.count(o) == 1
S = S.replace(o, o + "    var WSX = [], WCX = [], WSY = new Float64Array(WV.length), WCY = new Float64Array(WV.length);\n"
                 "    for (var qw = 0; qw < WV.length; qw++) { var sxa = new Float64Array(nx + 1), cxa = new Float64Array(nx + 1);\n"
                 "      for (var aw = 0; aw <= nx; aw++) { var xw = WV[qw].fx * (gx0 + aw * pas); sxa[aw] = Math.sin(xw); cxa[aw] = Math.cos(xw); }\n"
                 "      WSX.push(sxa); WCX.push(cxa); }\n")
o = "      var y = gy0 + j * pas, nr = 0;\n"
assert S.count(o) == 1
S = S.replace(o, o + "      for (var qy = 0; qy < WV.length; qy++) { var yw = WV[qy].fy * y + WV[qy].ph; WSY[qy] = Math.sin(yw); WCY[qy] = Math.cos(yw); }\n")
o = "          var x = gx0 + a * pas; v = x * ct + y * st;\n"
assert S.count(o) == 1
S = S.replace(o, "          var x = gx0 + a * pas; v = x * ct + y * st;\n"
                 "          for (var qv = 0; qv < WV.length; qv++) v += WV[qv].A * (WSX[qv][a] * WCY[qv] + WCX[qv][a] * WSY[qv]);   // v40 : les ondes\n")
o = "      var v = x * ct + y * st;\n"
assert S.count(o) == 1
S = S.replace(o, "      var v = x * ct + y * st + onde(x, y);   // v40 : les mêmes ondes que la grille\n")
io.open(F, 'w', encoding='utf-8').write(S)
print('OK')
