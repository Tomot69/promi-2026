#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRÔLE — la phrase de la page + affiche TOUJOURS son verbe (pastille menthe
   « Je promets » / « Promets-moi »), et la bascule trait/bouton mène à un VRAI bouton.

   Ce contrôle existe parce que les neuf batteries n'ont PAS vu disparaître la pastille
   « Je promets » : elles mesurent des écarts, pas la présence d'un élément vital. Ici
   on exige que .ph-b soit présent, visible, d'une hauteur réelle (> 24px) et porte un
   verbe — en clair ET sombre, sens « Je promets » ET « Promets-moi ». Et qu'en mode
   bouton un CTA cliquable apparaisse.

       python3 redteam_verbe.py        attendu : tout OK
"""
import os as _os
from playwright.sync_api import sync_playwright

_ICI = _os.path.dirname(_os.path.abspath(__file__))
def _url():
    for p in [_os.path.join(_ICI, 'app.html'), '/home/claude/app.html']:
        if _os.path.exists(p): return 'file://' + p
    return 'file:///home/claude/app.html'

R = []
def t(n, ok, d=''): R.append((n, 'OK' if ok else 'KO', d))

# trois façons de s'engager (lot 22) : « je me promets » quand c'est à soi ;
# « promettez-moi » au pluriel ; « chiche » pour le défi.
VERBES = ('je promets', 'je me promets', 'promets-moi', 'promettez-moi', 'chiche')

with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ['light', 'dark']:
        pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
        pg.goto(_url()); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if theme == 'light':
            pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.add('light'))")
        else:
            pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.remove('light'))")
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const t=document.querySelector('#createSheet .tile[data-kind=promi]');if(t)t.click();}"); pg.wait_for_timeout(1100)

        def verbe(tag):
            r = pg.evaluate(r"""()=>{const pb=document.querySelector('#csPhrase .ph-b');
              if(!pb)return{f:0};const b=pb.getBoundingClientRect();const c=getComputedStyle(pb);
              return {f:1,h:b.height,txt:(pb.textContent||'').trim().toLowerCase(),
                vis:c.visibility!=='hidden'&&c.display!=='none'&&+c.opacity>0.1};}""")
            ok = r.get('f') and r.get('vis') and r.get('h',0) > 24 and any(v in r.get('txt','') for v in VERBES)
            t('%s : la phrase montre son verbe (%s)' % (theme, tag),
              ok, 'h=%s txt=%r' % (round(r.get('h',0),1), r.get('txt')))

        verbe('Je promets')
        # inverser le sens -> Promets-moi
        pg.evaluate("()=>{const s=document.querySelector('#csPhrase [data-ph=sens]');if(s)s.click();}"); pg.wait_for_timeout(350)
        pg.evaluate("()=>{const d=document.querySelector('#csSens [data-sens=demander]');if(d)d.click();}"); pg.wait_for_timeout(350)
        verbe('Promets-moi')

        # bascule trait/bouton -> un vrai CTA visible
        pg.evaluate("()=>{const a=document.getElementById('planterAlt');if(a)a.click();}"); pg.wait_for_timeout(400)
        cta = pg.evaluate(r"""()=>{const b=document.getElementById('addPromi');if(!b)return{f:0};
          const r=b.getBoundingClientRect();const c=getComputedStyle(b);
          return {f:1,h:Math.round(r.height),vis:c.display!=='none'&&c.visibility!=='hidden'};}""")
        t('%s : la bascule mène à un vrai bouton' % theme,
          bool(cta.get('vis')) and cta.get('h',0) > 24, 'bouton=%r' % cta)
        pg.close()
    b.close()

for n, s, d in R: print('%-52s %s  %s' % (n, s, d))
ok = sum(1 for _, s, _ in R if s == 'OK')
print('\n%d/%d' % (ok, len(R)))
