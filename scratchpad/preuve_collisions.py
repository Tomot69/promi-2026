#!/usr/bin/env python3
"""PREUVE — l'outil de collisions mord-il encore ? (CLAUDE.md §7)

Trois sondes posées dans un cadre du BAS de la planche — celui que l'ancienne version
ne regardait jamais :
  1 · deux TEXTES qui se recouvrent        → doit être PRIS
  2 · un texte qui DÉBORDE d'un canevas    → doit être PRIS
  3 · une dalle entièrement DANS la frise  → doit être EXEMPTÉE (marque sur sa surface)
"""
import re, io
from playwright.sync_api import sync_playwright

src = io.open('scratchpad/cap_retenu.py', encoding='utf-8').read()
REGLE = re.search(r'REGLE = r"""(.*?)"""', src, re.S).group(1)

SONDE = """()=>{
  const fs=document.querySelectorAll('.fr'); const I=4; const f=fs[I];   /* « le bas » : la moisson */
  const mk=(css,t)=>{const d=document.createElement('div');
    d.className='bg700'; d.style.cssText='position:absolute;color:#fff;'+css;
    d.textContent=t; f.appendChild(d);};
  mk('left:24px;top:660px;width:200px;font-size:20px','SONDE UN');
  mk('left:60px;top:666px;width:200px;font-size:20px','SONDE DEUX');
  mk('left:20px;top:200px;width:150px;font-size:18px','DEBORDE');   /* chevauche des dalles de la moisson */
  /* 4 · une BOÎTE BORDÉE qui chevauche une dalle — un bouton porte un <span>,
        ce n'est donc pas une feuille : l'outil le manquait. */
  const b=document.createElement('div');
  b.className='btn'; b.style.cssText='position:absolute;left:24px;top:400px;'
    +'width:342px;height:62px;border:2px solid #fff;border-radius:31px';
  const sp=document.createElement('span'); sp.textContent='BOITE BORDEE'; b.appendChild(sp);
  f.appendChild(b);
  return I;}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1800, 'height': 1400}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-RETENU.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=30000)
    pg.wait_for_timeout(2200)
    fi = pg.evaluate(SONDE)
    pg.wait_for_timeout(400)
    pg.query_selector_all('.fr')[fi].scroll_into_view_if_needed()
    pg.wait_for_timeout(250)
    res = pg.evaluate(REGLE, fi)
    print('prises :', len(res))
    for r in res: print('   ', r)
    un   = any('SONDE UN' in r and 'SONDE DEUX' in r for r in res)
    deb  = any('DEBORDE' in r for r in res)
    # 3 · le cas EXEMPTÉ : aucune ligne ne doit être rapportée sans qu'une sonde y figure.
    #     Une dalle peinte sur la frise, un visage dans son anneau : rien ne doit crier.
    SONDES = ('SONDE UN', 'SONDE DEUX', 'DEBORDE', 'BOITE BORDEE')
    surf = any(not any(s in r for s in SONDES) for r in res)
    print()
    print('1 · deux textes qui se recouvrent      →', 'PRIS ✅' if un else 'MANQUÉ ❌')
    print('2 · un texte débordant d’un canevas    →', 'PRIS ✅' if deb else 'MANQUÉ ❌')
    boite = any('BOITE BORDEE' in r for r in res)
    print('3 · une dalle DANS la frise            →', 'exemptée ✅' if not surf else 'CRIÉE À TORT ❌')
    print('4 · une boîte BORDÉE sur une dalle     →', 'PRIS ✅' if boite else 'MANQUÉ ❌')
    b.close()
