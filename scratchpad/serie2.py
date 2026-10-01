#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les batteries que le lot du trait (§2.1 bis) et les juges repris peuvent toucher."""
import subprocess, sys, os, re, time
R=os.path.dirname(os.path.abspath(__file__)).replace('/scratchpad','')
BATS=['redteam_tokens.py','redteam_ecrans.py','redteam_tonsurton.py','redteam_geste.py',
      'redteam_toile.py','redteam_air.py','redteam_champ.py','redteam_reperage.py',
      'redteam_formes.py','redteam_nuee.py','redteam_vide.py','redteam_nuee_dalle.py',
      'redteam_dalle_figee.py','redteam_verbe.py','redteam_filets.py','redteam_aveugle.py']
for f in BATS:
    t=time.time()
    try:
        p=subprocess.run([sys.executable,f],cwd=R,capture_output=True,text=True,timeout=900)
        out=(p.stdout or '')+(p.stderr or '')
    except subprocess.TimeoutExpired: out='(dépassement)'
    L=[l for l in out.strip().split('\n') if l.strip()]
    v=' / '.join(L[-2:]) if L else '(rien)'
    m=re.search(r'(\d+)\s*/\s*(\d+)',v)
    e='?' ;
    if m: e='VERT' if m.group(1)==m.group(2) else 'ROUGE'
    elif 'AUCUN ÉCART' in out or 'INTACT' in out or '0 filet' in out or '0 écart' in out: e='VERT'
    print(f"  {e:6} {int(time.time()-t):>4}s  {f:26} {v[:96]}", flush=True)
