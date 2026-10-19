import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ENREG=open('redteam_trace_lettres.py',encoding='utf-8').read().split('ENREG = """')[1].split('"""')[0].replace('\\\\','\\')
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, onb=False, guide=False); pg=B.ouvre(ctx,'app.html',attente=7000,q='?tlv=0.05')
    pg.wait_for_function("()=>!document.querySelector('canvas[data-trace]') && !!document.getElementById('onbPh') && getComputedStyle(document.getElementById('onbPh')).visibility==='visible'", timeout=90000); pg.wait_for_timeout(300)
    pg.evaluate(ENREG); B.tap_sel(pg,'#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille',delay=30); pg.keyboard.press('Enter')
    for _ in range(600):
        pg.wait_for_timeout(50)
        e=pg.evaluate("()=>{ const r=window.__TL.find(x=>x.id==='onbDit'); if(!r) return null; const c=window.__CTL[r.k]; return c?c.etat():null; }")
        if e and e['glyphe']==9: break
    pg.wait_for_timeout(450)
    r=pg.evaluate("()=>{ const e=document.getElementById('onbDit'); const g=document.createRange(); g.selectNodeContents(e); const q=g.getBoundingClientRect(); return [q.left,q.top,q.width,q.height]; }")
    print(r, e)
    pg.screenshot(path='scratchpad/v153/trace-o-x005.png', clip={'x':r[0]+r[2]*0.55,'y':r[1]-2,'width':r[2]*0.3,'height':r[3]+4}); b.close()
