# Première ouverture du Peaufiner d'une Nuée, au toucher (WebKit) : qu'y a-t-il sous le doigt, et la barre bouge-t-elle encore ?
import sys
from playwright.sync_api import sync_playwright
ATT=int(sys.argv[1]) if len(sys.argv)>1 else 1500
with sync_playwright() as p:
    for k in range(4):
        b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True); pg=ctx.new_page()
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(8000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>{closeAll(); var k=null; for(var q in NUE){k=q;break;} openNueeDetail(k);}"); pg.wait_for_timeout(ATT)
        a=pg.evaluate("()=>{const b=document.querySelector('#dpDetails .dpd-tog'); const r=b.getBoundingClientRect(); const e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return {y:Math.round(r.top), sous:(e&&(e.id||e.className))+''};}")
        pg.wait_for_timeout(400)
        a2=pg.evaluate("()=>Math.round(document.querySelector('#dpDetails .dpd-tog').getBoundingClientRect().top)")
        r=pg.evaluate("()=>{const b=document.querySelector('#dpDetails .dpd-tog').getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2];}")
        pg.touchscreen.tap(*r); pg.wait_for_timeout(1500)
        o=pg.evaluate("()=>document.getElementById('dpDetails').classList.contains('ouvert')")
        print('essai',k+1,'attente',ATT,'ms · barre y',a['y'],'→',a2,'· sous le doigt :',a['sous'][:40],'· ouvert :',o, flush=True)
        b.close()
