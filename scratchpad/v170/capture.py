import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); i=src.index('ENREG = """'); j=src.index('"""', i+11); ENREG=src[i+11:j].replace('\\\\','\\')
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx,'app.html',attente=7000,q='?tlv=0.05')
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(300)
    pg.evaluate(ENREG); pg.evaluate("()=>_guide.montre('reste')")
    info=None
    for _ in range(900):
        pg.wait_for_timeout(40)
        info=pg.evaluate("""()=>{ const r=(window.__TL||[]).slice(-1)[0]; if(!r) return null; const c=window.__CTL[r.k]; if(!c||c.fini) return null; const e=c.etat(); const a=e.actives||[];
          if(a.length<3) return null; const g=a.map(j=>c.glyphes[j]); if(g.some(x=>x.police!=='PromiLate')) return null; if('LE'.includes(g[0].car) && e.glyphe<4) return null; return {g:g.map(x=>x.car), n:e.glyphe}; }""")
        if info: break
    e=pg.evaluate("()=>{ const q=document.getElementById('guidePhrase').getBoundingClientRect(); return [q.left,q.top,q.width,q.height]; }")
    pg.screenshot(path='scratchpad/v170/trace-promilate-x005.png', clip={'x':max(0,e[0]-10),'y':max(0,e[1]-10),'width':min(390,e[2]+20),'height':e[3]+20})
    print(info); b.close()
