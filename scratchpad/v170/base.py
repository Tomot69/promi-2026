import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
JS="""async fz=>{ const el=document.createElement('div'); el.style.cssText='position:fixed;left:40.3px;top:60.37px;width:340px;font:400 '+fz+'px/1.3 PromiLate;color:#291547;z-index:60'; el.innerHTML='<span class="v35-e">A<span class="v35-acc">\\u2019</span></span>'; document.body.appendChild(el);
 await document.fonts.ready; const e=el.querySelector('.v35-e'), t=e.firstChild, r=document.createRange(); r.setStart(t,0); r.setEnd(t,1); const rc=r.getClientRects()[0], er=e.getBoundingClientRect();
 const c=document.createElement('canvas').getContext('2d'); c.font='400 '+fz+'px PromiLate'; const m=c.measureText('A'); const cs=getComputedStyle(e);
 el.remove(); return {rc:[rc.left,rc.top,rc.height], er:[er.left,er.top,er.height], lh:cs.lineHeight, fa:m.fontBoundingBoxAscent, fd:m.fontBoundingBoxDescent}; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    for fz in (29,42): print(fz, pg.evaluate(JS,fz))
    b.close()
