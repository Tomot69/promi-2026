# C-156 §7.2 : ma part seule — l'écran 250 ms après le lever (la vague amande sous le trait, aucun rideau), puis 1,5 s après.
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
TIENT = open('scratchpad/v149/vague_vue.py', encoding='utf-8').read().split('TIENT = r"""')[1].split('"""')[0]
CREE = open('redteam_validation.py', encoding='utf-8').read().split('CREE = """')[1].split('"""')[0]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, dsf=2); pg = B.ouvre(ctx)
    pid = pg.evaluate(CREE, ['traverser la baie à la nage', 'Marion', 'Rachel, Nico']); pg.wait_for_timeout(900)
    pg.evaluate("id=>{ closeAll(); openDetail(id); }", pid); pg.wait_for_timeout(3000)
    z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'), r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.top-d.top)/k, r.height/k]; }")
    y = z[0] + z[1] * 0.45
    P = [list(B.pt(pg, 200 + 150 * i / 10, y)) for i in range(11)]
    pg.evaluate(TIENT, [P]); pg.wait_for_timeout(600); B.capture(pg, 'scratchpad/v149/part_pendant.png')
    pg.evaluate("()=>window.__fin()"); pg.wait_for_timeout(250); B.capture(pg, 'scratchpad/v149/part_250.png')
    pg.wait_for_timeout(1300); B.capture(pg, 'scratchpad/v149/part_1550.png'); b.close()
