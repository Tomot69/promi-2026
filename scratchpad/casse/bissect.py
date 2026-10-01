# -*- coding: utf-8 -*-
"""Réapplique les sept correctifs UN PAR UN, en mesurant la section 2 après chacun.
   Le premier qui fait passer 0 → 212 est le coupable."""
import io, sys, subprocess, re
sys.path.insert(0,'/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/casse')
from patchs import CORRECTIFS
R="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/"
BASE=io.open(R+'sauvegardes/avant-reparations.html',encoding='utf-8').read()

def mesure(quoi):
    out=subprocess.run(['python3',R+quoi],cwd=R,capture_output=True,text=True,timeout=900).stdout
    m=re.search(r'ÉCARTS DE POSITION \(> 3 px\) : (\d+)', out)
    if m: return int(m.group(1))
    if 'AU VERT' in out: return 0
    m=re.search(r'❌\s+(\d+) ÉCARTS', out)
    return int(m.group(1)) if m else -1

S=BASE
print('%-34s %8s %8s' % ('après le correctif', 'S2', 'S4'))
print('%-34s %8d %8d' % ('(rien — état restauré)', mesure('releve-S2-peaufiner.py'), mesure('releve-S4-index-fil.py')))
for nom, patchs in CORRECTIFS:
    for old,new in patchs:
        n=S.count(old)
        if n!=1:
            print('   ⚠ motif %s fois pour « %s »'%(n,nom[:26])); continue
        S=S.replace(old,new,1)
    io.open(R+'app.html','w',encoding='utf-8').write(S)
    # la syntaxe d'abord
    js=''.join(m.group(1) for m in re.finditer(r'<script[^>]*>(.*?)</script>', S, re.S))
    io.open(R+'check.js','w',encoding='utf-8').write(js)
    ok=subprocess.run(['node','--check',R+'check.js'],capture_output=True).returncode==0
    s2=mesure('releve-S2-peaufiner.py'); s4=mesure('releve-S4-index-fil.py')
    print('%-34s %8d %8d %s' % (nom, s2, s4, '' if ok else '  ⚠ SYNTAXE JS'))
io.open(R+'scratchpad/casse/_cumul.html','w',encoding='utf-8').write(S)
print('\nétat cumulé écrit dans scratchpad/casse/_cumul.html')
