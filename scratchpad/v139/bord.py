# capture @3x de la Pelote (WebKit) : la boule entière et le bord haut-droit agrandi
import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]; nom=sys.argv[2]; clair=(len(sys.argv)<4 or sys.argv[3]!='sombre')
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('geste_vu_pelote','1');localStorage.setItem('promi_theme','%s');}catch(e){}"%('light' if clair else 'dark'))
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("(c)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}",clair); pg.wait_for_timeout(7000)
    r=pg.evaluate("()=>{var c=document.getElementById('auBouleGL')||document.getElementById('auBoule');var r=c.getBoundingClientRect();return [r.left,r.top,r.width,r.height,!!document.getElementById('auBouleGL')]}")
    print(f,r)
    pg.screenshot(path='planche-v139/'+nom+'.png',clip={'x':r[0]-10,'y':r[1]-10,'width':r[2]+20,'height':r[3]+60})
    cx=r[0]+r[2]/2; cy=r[1]+r[3]/2
    pg.screenshot(path='planche-v139/'+nom+'-bord.png',clip={'x':cx+40,'y':cy-135,'width':80,'height':80})
    b.close()
