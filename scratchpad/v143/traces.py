import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
C=[(0,'moi','à soi'),(0,'Rachel','à quelqu’un'),(0,'Rachel, Marion','à plusieurs'),(1,'moi','à soi'),(1,'Rachel','à quelqu’un'),(1,'Rachel, Marion','à plusieurs')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b); pg=ouvre(ctx,F)
    for nat,qui,cas in C:
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("n=>{const x=[...document.querySelectorAll('#createSheet .tile')][n];x&&x.click()}",nat); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a[0];const w=document.getElementById('fWho'); w.value=a[1]; w.dispatchEvent(new Event('input',{bubbles:true})); w.dispatchEvent(new Event('change',{bubbles:true})); window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a[0]; _phrase.qui=a[1]; } if(window._ppTout) _ppTout(); }catch(e){} }",['rendre le livre',qui]); pg.wait_for_timeout(900)
        pp=pg.evaluate("()=>{const t=document.querySelector('#createSheet .pp-trace'); return t?(t.getAttribute('aria-label')||t.textContent).trim():null}")
        pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2600); pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(500)
        pid=pg.evaluate("()=>promises[promises.length-1].id"); pg.evaluate("(i)=>openDetail(i)",pid); pg.wait_for_timeout(1800)
        fi=pg.evaluate("()=>{const t=document.getElementById('dptTrace'); const p=promises[promises.length-1]; return [t?t.textContent.trim():null, p.who, !!p.chiche, p.status]}")
        print('%-7s %-13s | page + : %-22s | fiche : %-40s | %s'%('Chiche' if nat else 'Promi',cas,(pp or '').upper(),(fi[0] or '').upper(),fi[1:]),flush=True)
    b.close()
