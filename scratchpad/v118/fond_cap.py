# fond_cap.py avant|apres — l'accueil en clair @3x, trois mondes, hasard amorcé et horloge figée (la même composition avant et après)
import sys, io
from playwright.sync_api import sync_playwright
nom = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){} (function(){var s=7;Math.random=function(){s=(s*16807)%2147483647;return s/2147483647;};})();")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll(); setTheme('light'); try{setPremium(true)}catch(e){}}"); pg.wait_for_timeout(800)
    for m in ('encre', 'braille', 'sillons'):
        pg.evaluate("(m)=>{Toile.setTheme(m)}", m); pg.wait_for_timeout(3500)
        pg.screenshot(path='planche-v118/fond-%s-%s.png' % (nom, m), clip={'x':20,'y':44,'width':390,'height':844})
        print(nom, m, pg.evaluate("""()=>{const c=document.getElementById('toileCv'), g=c.getContext('2d'); const a=g.getImageData(6,Math.round(c.height*0.5),1,1).data, z=g.getImageData(c.width-6,c.height-6,1,1).data; return [[a[0],a[1],a[2]],[z[0],z[1],z[2]]]}"""))
    b.close()
