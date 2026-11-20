# -*- coding: utf-8 -*-
"""L0 (vraie app, 20 nov. 2026) — L'ÉTAT DU BANC DE RENDU, pour la vraie app.
banc_rendu.py (le banc de référence du portage) rend le jeu de démonstration du prototype, sous un hasard amorcé. Cet outil charge le
prototype EXACTEMENT comme le banc (même amorce, même attente) et relève l'état que le banc rend : les paroles, les Cercles, la graine.
Il l'écrit au format d'un export du prototype (`{ls: …}`) : promi/tests/rendu/etat-banc-rendu.json — la vraie app l'importe, rend les
vingt mondes par le même protocole, et se compare aux images figées de banc-rendu/ref/ (tests/rendu/banc-rendu.spec.ts).
python3 outils/banc_rendu_etat.py   (le serveur du prototype sur 8752)"""
import json, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, '.')
import banc_rendu as B
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2); ctx.add_init_script(B.AMORCE)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
    ls = pg.evaluate("""()=>{ const st={v:1, promises:JSON.parse(JSON.stringify(promises)), NUE:JSON.parse(JSON.stringify(NUE)),
        NUEEMEM:JSON.parse(JSON.stringify(NUEEMEM)), NUEDALLE:JSON.parse(JSON.stringify(window.NUEDALLE||{})), PEOPLE:[], FEED:[], feedReacted:{}, shareHidden:{},
        state:{mood:state.mood, structure:state.structure, sort:state.sort, labels:!!state.labels}, nid:nid, fid:1, notifOn:false};
      const r={promi_state:JSON.stringify(st), promi_onb:'1'}; const g=localStorage.getItem('promi_graine'); if(g!=null) r.promi_graine=g;
      const th=localStorage.getItem('promi_theme'); if(th!=null) r.promi_theme=th; return r; }""")
    b.close()
json.dump({'quand': 'banc_rendu', 'ls': ls}, open('promi/tests/rendu/etat-banc-rendu.json', 'w'), ensure_ascii=False, indent=1)
print('paroles :', len(json.loads(ls['promi_state'])['promises']), '· graine :', ls.get('promi_graine'))
