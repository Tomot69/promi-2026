import sys,re,io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
src=io.open('redteam_toucher.py',encoding='utf-8').read(); F=sys.argv[1]
POINTS=re.search(r'POINTS\s*=\s*r?"""(.*?)"""',src,re.S).group(1)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} }")
    for m in ['braille','pixel','esquille','chantourne','volubilis','encre']:
        pg.evaluate("(m)=>{ try{closeAll()}catch(e){} try{ if(typeof setView==='function') setView('toile'); }catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(3200)
        P=pg.evaluate(POINTS)
        for q in P['pts']:
            d=pg.evaluate("([x,y])=>{const E=document.elementsFromPoint(x,y).slice(0,4).map(h=>(h.id||h.className||h.tagName)+''); const h=document.elementFromPoint(x,y), s=h&&h.closest('.screen,.sheet,.poster,#feedView'); return [E, s?(s.id+' '+s.className):null, Math.round(y)]}", [q['x'],q['y']])
            pg.touchscreen.tap(q['x'], q['y']); pg.wait_for_timeout(1500)
            e=pg.evaluate("()=>{const dp=document.getElementById('detailPoster'); return [dp.classList.contains('show'), (typeof cur!=='undefined'&&cur)?cur.title:null]}")
            print(m, q['titre'], '| dessus avant :', d, '| après :', e, '' if (e[0] and e[1]==q['titre']) else '  <<<<<')
            pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(700)
    b.close()
