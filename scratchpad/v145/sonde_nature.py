import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    for i, nat in enumerate([0, 1, 0, 0, 1, 0]):
        r = B.plante_doigt(pg, 'parole %d' % i, 'moi' if i % 2 else 'Rachel', nat, attente=1700); print(i, 'demandée', bool(nat), '→ plantée chiche =', r, flush=True)
    print(pg.evaluate("()=>promises.map(p=>[p.title,!!p.chiche,p.who])"))
    b.close()
