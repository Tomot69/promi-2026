import sys; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
quoi=sys.argv[1] if len(sys.argv)>1 else 'reste'; ts=[int(x) for x in (sys.argv[2] if len(sys.argv)>2 else '2000,6000,12000,20000').split(',')]
theme=sys.argv[3] if len(sys.argv)>3 else 'light'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True,is_mobile=True)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__ini')){ sessionStorage.setItem('__ini','1'); localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}"%theme)
    pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html?tlv=0.05',timeout=180000); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(300)
    pg.evaluate("q=>{ _guide.montre(q); }", quoi); t0=0
    for t in ts:
        pg.wait_for_timeout(t-t0); t0=t
        r=pg.evaluate("()=>{const p=document.getElementById('guidePhrase'); const r=p.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        pg.screenshot(path='scratchpad/v170/ral-%s-%d.png'%(quoi,t), clip={'x':0,'y':max(0,r[1]-20),'width':390,'height':min(844-max(0,r[1]-20), r[3]+40)})
    print(er)
    b.close()
