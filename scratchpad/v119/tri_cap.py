import io
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{setTheme('dark'); closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);}"); pg.wait_for_timeout(3200)
    print('S5 arrive sombre :', pg.evaluate("""()=>{const e=document.getElementById('dptQui'), c=getComputedStyle(e), r=e.getBoundingClientRect(); const cv=document.getElementById('dpTrameCv'); const k=cv.width/cv.getBoundingClientRect().width, cr=cv.getBoundingClientRect(); const d=cv.getContext('2d').getImageData(Math.round((r.left+4-cr.left)*k), Math.round((r.top-6-cr.top)*k),1,1).data;
       const dp=getComputedStyle(document.getElementById('detailPoster')); return {texte:c.color, sousCanevas:[d[0],d[1],d[2],d[3]], poster:dp.backgroundColor, y:Math.round(r.top-44), classes:document.getElementById('detailPoster').className}}"""))
    pg.screenshot(path='planche-v119/tri-S5-arrive-sombre.png', clip={'x':20,'y':44,'width':390,'height':844})
    # le mur du Peaufiner, sombre : la phrase et « Ma Parole ! »
    pg.evaluate("()=>{closeAll(); try{localStorage.removeItem('promi_murs')}catch(e){} const p=promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.chiche); openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"); pg.wait_for_timeout(2600)
    c = pg.evaluate("()=>{const w=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)'); if(!w) return null; w.scrollIntoView({block:'center'}); const r=w.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}")
    if c:
        pg.wait_for_timeout(500); c = pg.evaluate("()=>{const r=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}")
        pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(900)
        print('mur :', pg.evaluate("()=>{const p=document.getElementById('murPhrase'); if(!p) return null; const m=p.querySelector('.mp'); return {phrase:p.textContent, texte:getComputedStyle(p).color, mp:m?getComputedStyle(m).color:null, corps:getComputedStyle(document.querySelector('#detailPoster .dpd-corps')).backgroundColor}}"))
        pg.screenshot(path='planche-v119/tri-murs-7-sombre.png', clip={'x':20,'y':44,'width':390,'height':844})
    b.close()
