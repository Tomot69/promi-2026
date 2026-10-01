#!/usr/bin/env python3
"""PREUVE — le juge releve-S2 réécrit MORD-IL ENCORE ?

CLAUDE.md §7 : « un contrat réécrit se prouve contre un VRAI défaut, sinon il ne
mesure plus rien. » On fabrique le défaut, on le pose dans une copie de l'app, on
relance le juge dessus, on vérifie qu'il est PRIS, puis on retire tout.

Résultat attendu : ❌ style ≥ 6 (un libellé fautif × 3 écrans × 2 thèmes).
"""
import io, os, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONDE = """
<script>/* SONDE DE PREUVE */
(function(){function p(){document.querySelectorAll('#dpdCorps .s2-liste .s2-lab').forEach(function(l,i){
  if(i===1){l.style.setProperty('font-size','9px','important');
            l.style.setProperty('margin-left','40px','important');}});}
setInterval(p,200);})();</script>
</body>"""
app = io.open(os.path.join(R, 'app.html'), encoding='utf-8').read()
assert app.count('</body>') == 1
tmp_app = os.path.join(R, 'scratchpad', 'app-sonde.html')
tmp_jug = os.path.join(R, 'scratchpad', 'releve-S2-sonde.py')
io.open(tmp_app, 'w', encoding='utf-8').write(app.replace('</body>', SONDE))
j = io.open(os.path.join(R, 'releve-S2-peaufiner.py'), encoding='utf-8').read()
j = j.replace('APP = "%s/app.html"' % R, 'APP = "%s"' % tmp_app)
io.open(tmp_jug, 'w', encoding='utf-8').write(j)
out = subprocess.run([sys.executable, tmp_jug], capture_output=True, text=True).stdout
print(out.strip().splitlines()[-1])
for f in (tmp_app, tmp_jug):
    os.remove(f)
