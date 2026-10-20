import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx)
    B.plante(pg,'rendre le livre'); B.plante(pg,'appeler mamie',qui='Rachel')
    out=[]
    for i,t in enumerate(['rendre le livre','appeler mamie']):
        pg.evaluate("t=>{ closeAll(); const p=promises.find(x=>x.title===t); openDetail(p.id); }", t); pg.wait_for_timeout(2600)
        print(t, pg.evaluate("()=>{ const c=document.getElementById('dpTrameCv'); return c&&c.getAttribute('data-depart'); }"))
        B.capture(pg, 'scratchpad/v155/fiche%d.png'%i)
    pg.evaluate("()=>{ closeAll(); }"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ const x=[...document.querySelectorAll('#createSheet .tile')][0]; x&&x.click(); }"); pg.wait_for_timeout(2500)
    B.capture(pg, 'scratchpad/v155/pageplus.png')
    b.close()
for f in ['fiche0','fiche1','pageplus']:
    im=Image.open('scratchpad/v155/%s.png'%f); w,h=im.size
