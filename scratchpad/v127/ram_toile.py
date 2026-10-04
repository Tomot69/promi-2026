# la VRAIE Toile sous Ramage : planter une parole et relever, image par image, la part des pixels qui changent et la boîte du changement
import sys, re
from playwright.sync_api import sync_playwright
S=open('redteam_ramage_onde.py',encoding='utf-8').read(); JS=re.search(r'JS = r"""(.*?)"""',S,re.S).group(1).replace("document.querySelector('#stBg')","document.getElementById('toileCv')")
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); er=[]; pg.on('pageerror', lambda e: er.append(str(e)[:140])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('ramage');}"); pg.wait_for_timeout(5000)
    pg.evaluate("()=>{ window._vivantOff=true; setTimeout(function(){ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'essai v127',nuee:null})); Toile.addPromi(97001); }, 600); }")
    r=pg.evaluate(JS); ev=r['ev']
    print('images', len(ev['im']) if ev else 0, [[round(a,1),round(c)] for a,c in (ev['im'] if ev else [])][:80], er[:2])
    b.close()
