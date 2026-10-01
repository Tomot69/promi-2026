#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capture les cadres §3 du moodboard H, un PNG par cadre (390x844)."""
import os
from playwright.sync_api import sync_playwright
MB="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/promi-moodboard-H.html"
OUT="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/scratchpad/mb"
os.makedirs(OUT, exist_ok=True)

CADRES = {  # nom : (index sombre, index clair)
 'promi_atenir':(44,45),'promi_encours':(46,47),'promi_tenue':(48,49),'promi_titrelong':(50,51),
 'chiche_lance':(52,53),'chiche_releve':(54,55),'chiche_duo':(56,57),
 'nuee_promi':(58,59),'nuee_vide':(60,61),'garde_promi':(62,63),
 'commentaires':(68,69),'sanscomment':(70,71),
 # SECTION 2 — Peaufiner (9 écrans × 2 thèmes)
 'peauf_promi_haut':(78,79),'peauf_promi_suite':(80,81),'peauf_cercle':(82,83),
 'peauf_nuee_haut':(84,85),'peauf_nuee_bas':(86,87),
 'peauf_chiche_haut':(88,89),'peauf_chiche_bas':(90,91),
 'peauf_garde':(92,93),'peauf_reglages':(94,95),
 # SECTION 3 — la page + (17 écrans × 2 thèmes), cadres 0 à 33, dans l'ordre de l'inventaire
 'pp_choix':(0,1),'pp_promi_vide':(2,3),'pp_promi_soi':(4,5),'pp_promi_rachel':(6,7),
 'pp_promets_moi':(8,9),'pp_promettez_moi':(10,11),
 'pp_chiche_vide':(12,13),'pp_chiche_rempli':(14,15),'pp_nuee':(16,17),
 'pp_choix_mot':(18,19),'pp_choix_personne':(20,21),'pp_choix_echeance':(22,23),
 'pp_garder':(24,25),'pp_garde_apres':(26,27),
 'pp_geste_repos':(28,29),'pp_geste_pendant':(30,31),'pp_geste_signe':(32,33),
 # SECTION 4 — Index et Fil (3 écrans × 2 thèmes). Les indices sont RELEVÉS sur le
 # moodboard (scratchpad/liste_cadres.py), jamais déduits de l'ordre du document : les
 # deux ordres diffèrent — 96 est « l'autre moitié arrive », pas l'Index.
 'ix_deux':(72,73),'ix_trois':(74,75),'fil':(76,77),
 # SECTION 5 — L'instant (3 écrans × 2 thèmes)
 'inst_arrive':(96,97),'inst_referme':(98,99),'inst_apres':(100,101),
}

JS=r"""()=>{
  const isFrame=(e)=>{const s=e.getAttribute('style')||'';return /width:\s*390px/.test(s)&&/height:\s*844px/.test(s);};
  const frames=[...document.querySelectorAll('div')].filter(isFrame);
  window.__F=frames; return frames.length;
}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':1200}, device_scale_factor=2)
    pg.goto('file://'+MB); pg.wait_for_timeout(4000)
    n=pg.evaluate(JS); print("cadres:",n)
    for nom,(d,l) in CADRES.items():
        for idx,th in ((d,'dark'),(l,'light')):
            h=pg.evaluate_handle("(i)=>window.__F[i]", idx)
            el=h.as_element()
            el.scroll_into_view_if_needed(); pg.wait_for_timeout(250)
            el.screenshot(path=os.path.join(OUT,'%s_%s.png'%(nom,th)))
    b.close()
print("cadres dans", OUT)
