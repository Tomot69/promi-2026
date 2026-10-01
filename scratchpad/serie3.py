#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Série complète — lot des CINQ POINTS (18 sept. 2026). En SÉRIE, jamais en parallèle (§7)."""
import subprocess, sys, os, re, time
R=os.path.dirname(os.path.abspath(__file__)).replace('/scratchpad','')
BATS=sorted([f for f in os.listdir(R) if re.match(r'^(redteam_|releve-).*\.py$', f)])
print('%d batteries · une par une\n'%len(BATS), flush=True)
verts=rouges=autres=0; LR=[]
for f in BATS:
    t=time.time()
    try:
        p=subprocess.run([sys.executable,f],cwd=R,capture_output=True,text=True,timeout=1200)
        out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement)'
    L=[l for l in out.strip().split('\n') if l.strip()]
    v=' / '.join(x.strip()[:90] for x in L[-2:]) if L else '(rien)'
    m=re.search(r'(\d+)\s*/\s*(\d+)',v); e='?'
    if '❌' in v or 'ÉCART' in v.upper(): e='ROUGE'
    elif m: e='VERT' if m.group(1)==m.group(2) else 'ROUGE'
    elif '✅' in v: e='VERT'
    if e=='VERT': verts+=1
    elif e=='ROUGE': rouges+=1; LR.append((f,v))
    else: autres+=1
    print('  %-7s %4ds  %-34s %s'%(e,int(time.time()-t),f,v[:110]), flush=True)
print('\nVERT %d · ROUGE %d · à lire %d'%(verts,rouges,autres), flush=True)
print('\nLES ROUGES :', flush=True)
for f,v in LR: print('  %-34s %s'%(f,v[:110]), flush=True)
