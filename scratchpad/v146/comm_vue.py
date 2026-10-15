# §15/§17 — une fiche reçue avec des mots (fermée, puis ouverte), et la fiche d'un Cercle avec sa ligne « Un mot… »
import sys; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); toile_pleine(ctx, 25); pg = ouvre(ctx)
    pg.evaluate("""()=>{ const q=promises.filter(x=>x.from&&!/^moi$/i.test(x.from))[0]||promises[0]; window.__q=q.id; q.comments=[]; const now=Date.now();
      _comm.arrive(q, {t:'Je passe dimanche si tu veux, on fait ça ensemble ?', by:'Christophe', d:new Date(now-86400000*1.2).toISOString()});
      _comm.arrive(q, {t:'Bonne idée !', by:'Christine', d:new Date(now-3*60000).toISOString()});
      _comm.arrive(q, {t:'Parfait, à dimanche.', by:'moi', d:new Date(now-20000).toISOString()}); openDetail(q.id); }""")
    pg.wait_for_timeout(2600); capture(pg, 'scratchpad/v146/comm-1.png')
    tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(1200); capture(pg, 'scratchpad/v146/comm-2.png')
    print(pg.evaluate("()=>[...document.querySelectorAll('#cm5Fil .nom-lien, #cm5Dernier .nom-lien')].map(e=>e.textContent)"))
    k = pg.evaluate("()=>Object.keys(NUE)[0]"); pg.evaluate("(k)=>{ closeAll(); openEssaim(k); }", k); pg.wait_for_timeout(3200); capture(pg, 'scratchpad/v146/comm-3.png')
    print(pg.evaluate("()=>{ const l=document.getElementById('cm5Ligne'), a=document.getElementById('nfAdd'); const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=x=>x?[(x.getBoundingClientRect().top-D.top)/k,(x.getBoundingClientRect().bottom-D.top)/k].map(Math.round):null; return {ligne:r(l), planter:r(a)}; }"))
    print(pg.__dict__['erreurs'][:2]); b.close()
ims = [Image.open('scratchpad/v146/comm-%d.png' % i).resize((300, 649)) for i in (1, 2, 3)]
W = Image.new('RGB', (310 * 3, 649), 'white')
for i, im in enumerate(ims): W.paste(im, (i * 310, 0))
W.save('scratchpad/v146/comm-planche.png')
