import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True)
    ctx.add_init_script("try{ localStorage.setItem('promi_theme','light'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} _guide.attend(false);}")
    for _ in range(100):
        if pg.evaluate("()=>document.getElementById('guide')&&document.getElementById('guide').getAttribute('data-entier')"): break
        pg.wait_for_timeout(150)
    e=pg.evaluate("()=>_guide.etat()"); x,y=B.pt(pg,e['trou']['x'],e['trou']['y']); B.tap(pg,x,y,appareil=False); pg.wait_for_timeout(2600)
    print(pg.evaluate("()=>JSON.stringify(Toile_state())").__str__()[:300])
    for i in range(5):
        print('A', pg.evaluate("()=>{const s=Toile_state(); return [s.running, document.getElementById('studioScreen').classList.contains('show')]}")); pg.wait_for_timeout(500)
    B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1800)
    print(pg.evaluate("()=>[...document.querySelectorAll('#studioScreen .st3-p')].map(b=>[b.dataset.p,b.classList.contains('on'),Math.round(b.getBoundingClientRect().top),Math.round(b.getBoundingClientRect().width), getComputedStyle(b).visibility]).slice(0,8)"))
    for i in range(12):
        print(pg.evaluate("()=>{const g=document.getElementById('guide'); let st=null; try{st=Toile_state()}catch(e){} return [g.getAttribute('data-guide'), _guideFlou.sig(), g.getAttribute('data-flou-sig'), g.getAttribute('data-flou-refait'), st&&st.running, _guideFlou.attend()]}"))
        pg.wait_for_timeout(400)
    b.close()
