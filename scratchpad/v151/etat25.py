import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx, 25); pg=B.ouvre(ctx, F, attente=1500)
    a=pg.evaluate("()=>promises.map(p=>[p.title,p.status,p.due,p.dueISO||null,(p.ech&&p.ech.iso)||null])")
    pg.wait_for_timeout(5000)
    c=pg.evaluate("()=>promises.map(p=>[p.title,p.status,p.due,p.dueISO||null,(p.ech&&p.ech.iso)||null])")
    print(F, 'datés', sum(1 for x in a if x[2] is not None), 'dueISO', sum(1 for x in a if x[3]))
    for x,y in zip(a,c):
        if x!=y: print(' change', x, '→', y)
    b.close()
