#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extrait_jeu.py — TOUS LES TEXTES DES CADRES, dans un JSON.

Pour bâtir le jeu de démonstration à partir de la planche : on ne recopie pas de mémoire,
on lit. Sortie : scratchpad/jeu_planche.json
"""
import json
from playwright.sync_api import sync_playwright

MARQUE = """()=>{const isF=e=>{const s=e.getAttribute('style')||'';
  return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
  [...document.querySelectorAll('div')].filter(isF).forEach((f,i)=>f.setAttribute('data-cadre',i));}"""

TXT = """(n)=>{const f=document.querySelector('[data-cadre="'+n+'"]'); if(!f) return null;
  const fr=f.getBoundingClientRect(); const out=[];
  f.querySelectorAll('*').forEach(e=>{
    let t=''; e.childNodes.forEach(k=>{if(k.nodeType===3)t+=k.nodeValue;});
    t=t.replace(/\\s+/g,' ').trim(); if(!t) return;
    const r=e.getBoundingClientRect(); const c=getComputedStyle(e);
    out.push({x:Math.round(r.left-fr.left), y:Math.round(r.top-fr.top),
              fs:parseFloat(c.fontSize), fw:c.fontWeight, col:c.color, t:t});});
  return out;}"""

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for url, tag, rng in (("http://127.0.0.1:8752/promi-moodboard-H.html", 'H', range(0, 102)),
                          ("http://127.0.0.1:8752/promi-nuee-toile.html", 'N', range(0, 20))):
        pg = b.new_page(viewport={'width': 1400, 'height': 1000})
        pg.goto(url); pg.wait_for_timeout(4500); pg.evaluate(MARQUE)
        for n in rng:
            r = pg.evaluate(TXT, n)
            if r:
                res['%s%d' % (tag, n)] = r
        pg.close()
    b.close()
open('scratchpad/jeu_planche.json', 'w').write(json.dumps(res, ensure_ascii=False))
print('cadres lus :', len(res))
