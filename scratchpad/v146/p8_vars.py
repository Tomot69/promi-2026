# -*- coding: utf-8 -*-
"""v146 (C-132) — les propriétés personnalisées dont la valeur diffère entre le sombre et le clair, lues à la racine de l'appareil dans chaque thème.
   Écrit scratchpad/v146/vars_sombre.json : {nom: valeur du sombre}."""
import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
S = io.open('app.html', encoding='utf-8').read()
css = ''.join(m.group(1) for m in re.finditer(r'<style[^>]*>(.*?)</style>', S, re.S))
noms = sorted(set(re.findall(r'(--[A-Za-z][\w-]*)\s*:', css)))
print('propriétés personnalisées déclarées :', len(noms))
LIT = "(noms)=>{ const o={}; for(const sel of ['#device', '.frame']){ const e=document.querySelector(sel), c=getComputedStyle(e); o[sel]={}; for(const n of noms) o[sel][n]=c.getPropertyValue(n).trim(); } return o; }"
with sync_playwright() as p:
    b = p.webkit.launch(); V = {}
    for sombre in (True, False):
        ctx = B.contexte(b, sombre=sombre); pg = B.ouvre(ctx, attente=5000); V[sombre] = pg.evaluate(LIT, noms); ctx.close()
    b.close()
out = {}
for n in noms:
    s, c = V[True]['#device'][n], V[False]['#device'][n]
    if s != c: out[n] = s
    elif V[True]['.frame'][n] != V[False]['.frame'][n]: out[n] = V[True]['.frame'][n]
json.dump(out, io.open('scratchpad/v146/vars_sombre.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('diffèrent entre sombre et clair :', len(out)); print({k: out[k] for k in list(out)[:12]})
print('vides en sombre :', [k for k, v in out.items() if not v])
