import sys, re
from playwright.sync_api import sync_playwright
POINTS=re.search(r'POINTS=r"""(.*?)"""', open('redteam_toucher.py',encoding='utf-8').read(), re.S).group(1)
with sync_playwright() as p:
    b=p.webkit.launch()
    for prem in (True, False):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(p)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(p)}catch(e){} }", prem)
        pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2500)
        for k in range(12):
            if pg.evaluate("()=>Toile.getTheme()")=='ramage': break
            pg.mouse.move(20+300,44+300); pg.mouse.down()
            for i in range(1,13): pg.mouse.move(20+300-i*18,44+300); pg.wait_for_timeout(16)
            pg.mouse.up(); pg.wait_for_timeout(2200)
        print('premium',prem,'· Studio sur', pg.evaluate("()=>[Toile.getTheme(), document.getElementById('studioScreen').className]"))
        c=pg.evaluate("()=>{const x=[...document.querySelectorAll('#studioScreen .closeb')].filter(e=>e.getBoundingClientRect().width>0)[0]; const r=x.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
        pg.touchscreen.tap(*c); pg.wait_for_timeout(3500)
        print('   de retour :', pg.evaluate("()=>[Toile.getTheme(), document.getElementById('studioScreen').className, getComputedStyle(document.getElementById('studioScreen')).transform, [...document.querySelectorAll('.show,.in')].map(e=>e.id).join(',')]"))
        P=pg.evaluate(POINTS)
        for q in P['pts']:
            pile=pg.evaluate("([x,y])=>document.elementsFromPoint(x,y).slice(0,5).map(h=>(h.id||String(h.className).split(' ')[0]||h.tagName)+'['+getComputedStyle(h).pointerEvents+']')", [q['x'],q['y']])
            pg.touchscreen.tap(q['x'],q['y']); pg.wait_for_timeout(1500)
            e=pg.evaluate("()=>{const dp=document.getElementById('detailPoster'); return [dp.classList.contains('show'), (typeof cur!=='undefined'&&cur)?cur.title:null, !!document.querySelector('#murPhrase.leve'), [...document.querySelectorAll('.show')].map(e=>e.id).join(',')]}")
            print('   touche', q['titre'], '→', e, '| pile', pile); pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(600)
        ctx.close()
    b.close()
