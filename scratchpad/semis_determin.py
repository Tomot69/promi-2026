#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""semis_determin.py — LE SEMIS D'UNE NUÉE NE CHANGE JAMAIS.

Même Nuée, même semis : à chaque ouverture, dans les deux thèmes, et d'un appareil à
l'autre. Une Toile qui change de composition entre deux ouvertures ne serait plus la Toile
de CETTE Nuée. On compare les pixels, pas le code : `toDataURL` du champ, ouverture après
ouverture. On vérifie aussi qu'un autre appareil (autre densité de pixels) donne le MÊME
semis — le placement ne doit dépendre que des ids, jamais de la taille du canevas.
"""
import sys
from playwright.sync_api import sync_playwright
APP = "http://127.0.0.1:8752/app.html"
ok = [0]; ko = []
REF = {}

def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-56s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-56s KO  %s' % (nom, detail))

OUVRE = """(n)=>{ const k=Object.keys(NUE)[0];
  promises.forEach(q=>{ if(q.nuee===k) q.nuee=null; });
  promises.filter(q=>!q.draft&&!q.nuee).slice(0,n).forEach(q=>{ q.nuee=k; });
  openEssaim(k); return k; }"""
# ⚠ ON COMPARE LE SEMIS, PAS LES PIXELS. `Toile.dalleTrame` rend la matière du monde avec
# `performance.now()` : les mondes animés ne redonnent jamais deux fois exactement les mêmes
# pixels, partout dans le produit. Comparer `toDataURL` mesure donc LA RESPIRATION DU MONDE
# — mesuré : 3 empreintes distinctes sur 3, sur douze configurations — et pas du tout la
# composition. Ce qui doit être identique, c'est QUELLE dalle occupe QUELLE case et OÙ :
# c'est `window._nueeSemis`, publié par `_ficheNuee` en coordonnées d'écran 390.
# ⚠ ON COMPARE LA CASE, PAS LE RECT PEINT. Le rect peint est la case ajustée au format de la
# dalle, et ce format respire lui aussi : `dalleTrame` recadre au plus juste sur l'alpha, que
# la matière animée déplace. Mesuré : en comparant le rect peint, 3 semis distincts sur 3.
# La CASE — quelle dalle, quelle ligne, quelle colonne, quelle boîte — ne bouge jamais.
EMPREINTE = """()=>{ const s=window._nueeSemis; if(!s) return null;
  return JSON.stringify({n:s.n, base:s.base, amp:s.amp, cols:s.cols, rows:s.rows, sp:s.sp,
    cases:s.cases.map(c=>[c.id,c.r,c.c,c.bx,c.by,c.bw,c.bh])}); }"""

def empreintes(pg, n, tours=3):
    out = []
    for i in range(tours):
        pg.evaluate(OUVRE, n); pg.wait_for_timeout(1700)
        out.append(pg.evaluate(EMPREINTE))
        pg.evaluate("()=>{ if(window.closeAll)closeAll(); }"); pg.wait_for_timeout(500)
    return out

with sync_playwright() as p:
    b = p.chromium.launch()
    for dsf in (2, 3):
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=dsf)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for n in (1, 3, 7):
                e = empreintes(pg, n)
                bon = all(x and x == e[0] for x in e)
                t('semis · %d Promi [%s · dpr %d] · 3 ouvertures' % (n, th, dsf), bon,
                  '%d empreintes, %d distincte(s)' % (len(e), len(set(e))))
                REF.setdefault((th, n), []).append((dsf, e[0]))
        pg.close()
    b.close()

# ── LE MÊME SEMIS D'UN APPAREIL À L'AUTRE ────────────────────────────────────────────────
# Le placement est en coordonnées d'écran 390 : il ne doit RIEN devoir à la densité de
# pixels de l'appareil. On compare dpr 2 et dpr 3, à thème et à n égaux.
for (th, n), vals in sorted(REF.items()):
    if len(vals) < 2: continue
    t('semis · %d Promi [%s] · dpr 2 == dpr 3' % (n, th),
      vals[0][1] is not None and vals[0][1] == vals[1][1],
      'deux appareils' if vals[0][1] == vals[1][1] else 'le semis dépend de l\'appareil')

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko:
    print('\nCE QUI CHANGE ENTRE DEUX OUVERTURES :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
