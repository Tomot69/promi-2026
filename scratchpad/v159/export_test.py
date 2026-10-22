import sys, glob, os; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
avant=set(glob.glob('etats/tom-*.json'))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=692); B.toile_pleine(ctx,5); pg=B.ouvre(ctx,'app.html',attente=7000,q='?export=1')
    print('fait', pg.evaluate("()=>window._exportFait")); ctx.close()
    neuf=sorted(set(glob.glob('etats/tom-*.json'))-avant); print('fichier', neuf)
    c2,d=B.contexte_tom(b, neuf[-1]); pg=c2.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    print('rejoué', d['ecran']['largeur'], d['ecran']['hauteur'], 'paroles', pg.evaluate("()=>promises.length"), 'toile', d['toile'])
    b.close()
    for f in neuf: os.remove(f)
