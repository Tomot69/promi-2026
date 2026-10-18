# Q536 : pendant le tracé, quels nœuds de la fiche ont un filtre, une opacité < 1, un text-shadow flou ? (WebKit, doigt posé)
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
TIENT = open('scratchpad/v149/vague_vue.py', encoding='utf-8').read().split('TIENT = r"""')[1].split('"""')[0]
LIT = """()=>[...document.querySelectorAll('#detailPoster, #detailPoster *')].map(e=>{ const c=getComputedStyle(e); const r=e.getBoundingClientRect(); return {id:e.id, cl:(typeof e.className==='string'?e.className:'').slice(0,40), f:c.filter, o:c.opacity, ts:c.textShadow, bf:c.backdropFilter||c.webkitBackdropFilter, w:r.width}; }).filter(x=>x.w>0 && ((x.f&&x.f!=='none') || +x.o<1 || (x.ts&&x.ts!=='none') || (x.bf&&x.bf!=='none')))"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    B.plante(pg, 'rendre le livre', qui='Marion'); pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3000)
    av = pg.evaluate(LIT)
    z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'), r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.top-d.top)/k, r.height/k]; }")
    P = [list(B.pt(pg, 200 + 50 * i / 10, z[0] + z[1] * 0.45)) for i in range(11)]
    pg.evaluate(TIENT, [P]); pg.wait_for_timeout(700)
    pe = pg.evaluate(LIT); cls = pg.evaluate("()=>[document.getElementById('detailPoster').className, document.getElementById('tenirZone').className]")
    print('classes pendant :', cls)
    ka = {(x['id'], x['cl']): x for x in av}
    for x in pe:
        k = (x['id'], x['cl'])
        if k not in ka or ka[k] != x: print('  CHANGÉ', x)
    pg.evaluate("()=>window.__fin()"); b.close()
