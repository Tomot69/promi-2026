#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA SÉRIE COMPLÈTE, EN SÉRIE — jamais en parallèle (§7 : douze Playwright d'un coup font ramer
   la machine, et les rouges qu'on lit alors sont FAUX)."""
import subprocess, sys, os, re, time
R='/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026'
BATS=[f for f in sorted(os.listdir(R)) if re.match(r'^(redteam|releve)[-_].*\.py$', f)]
print(f"{len(BATS)} batteries · une par une\n", flush=True)
res=[]
for f in BATS:
    t=time.time()
    try:
        p=subprocess.run([sys.executable, f], cwd=R, capture_output=True, text=True, timeout=900)
        out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired:
        out='(dépassement de 15 min)'
    d=int(time.time()-t)
    lignes=[l for l in out.strip().split('\n') if l.strip()]
    verdict=' / '.join(lignes[-2:]) if lignes else '(rien)'
    m=re.search(r'(\d+)\s*/\s*(\d+)', verdict)
    etat='?'
    if m: etat='VERT' if m.group(1)==m.group(2) else 'ROUGE'
    elif 'AUCUN ÉCART' in out or 'aucun écart' in out.lower(): etat='VERT'
    elif 'ÉCART' in out or 'ERREUR' in out.upper(): etat='ROUGE'
    res.append((f,etat,d,verdict[:110]))
    print(f"  {etat:6} {d:>4}s  {f:34} {verdict[:100]}", flush=True)
print()
v=[r for r in res if r[1]=='VERT']; rg=[r for r in res if r[1]=='ROUGE']; q=[r for r in res if r[1]=='?']
print(f"VERT {len(v)} · ROUGE {len(rg)} · à lire {len(q)}")
if rg:
    print("\nLES ROUGES :")
    for f,e,d,x in rg: print(f"  {f:34} {x}")
if q:
    print("\nÀ LIRE À LA MAIN :")
    for f,e,d,x in q: print(f"  {f:34} {x}")
