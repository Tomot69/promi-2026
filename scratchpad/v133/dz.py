from playwright.sync_api import sync_playwright
import sys
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); setPremium(false); closeAll(); openDetail(promises.filter(q=>q.title==='nager le mardi')[0].id);}",th); pg.wait_for_timeout(2400)
        print(th,'fermer', pg.evaluate("()=>{const c=[...document.querySelectorAll('#detailPoster .closeb, #detailPoster [class*=ferm]')].filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect();return [e.className, Math.round(r.left-20), Math.round(r.top-44), Math.round(r.width), Math.round(r.height), e.textContent.trim().slice(0,12)]}); return c}"))
        pg.evaluate("()=>window._dessin.ouvre()"); pg.wait_for_timeout(500)
        # deux traits
        pg.mouse.move(120,300); pg.mouse.down(); [pg.mouse.move(120+i*8,300+(i%5)*9) for i in range(20)]; pg.mouse.up(); pg.wait_for_timeout(200)
        g=pg.evaluate("""()=>{const D=document.getElementById('device').getBoundingClientRect(); const q=s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left-D.left, r.top-D.top, r.width, r.height].map(v=>Math.round(v*10)/10)};
          return {surf:q('#dessinMode .dz-surface'), rangee:q('#dessinMode .dz-rangee'), quit:q('#dessinMode .dz-quitter'), plat:q('#dessinMode .dz-plateau')}}""")
        print(th,g)
        pg.screenshot(path=SC+'dz-%s-1.png'%th, clip={'x':20,'y':44,'width':390,'height':844})
        # couleur, sans Ma Parole
        pg.touchscreen.tap(20+24+3*58+22, 44+754+22); pg.wait_for_timeout(400)
        print(th,'panneau', pg.evaluate("()=>{const D=document.getElementById('device').getBoundingClientRect(); const e=document.querySelector('#dessinMode .dz-couleurs'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.top-D.top, r.bottom-D.top, e.className, getComputedStyle(e.children[0]).filter]}"))
        pg.touchscreen.tap(20+195, 44+680); pg.wait_for_timeout(900)
        print(th,'phrase', pg.evaluate("()=>{const p=document.getElementById('murPhrase'); const s=getComputedStyle(p); const m=p.querySelector('.mp'); const D=document.getElementById('device').getBoundingClientRect(), r=p.getBoundingClientRect(); return [p.className, p.textContent, s.color, m&&getComputedStyle(m).color, s.fontSize, Math.round(r.top-D.top), Math.round(r.bottom-D.top), getComputedStyle(document.getElementById('dessinMode')).getPropertyValue('--dz-corps')]}"))
        pg.screenshot(path=SC+'dz-%s-2.png'%th, clip={'x':20,'y':44,'width':390,'height':844})
        pg.wait_for_timeout(6000)
        print(th,'après lecture', pg.evaluate("()=>[document.getElementById('plusScreen').classList.contains('show'), document.getElementById('dessinMode').classList.contains('ouv'), !!window._dessin.lit]"))
        pg.screenshot(path=SC+'dz-%s-3.png'%th, clip={'x':20,'y':44,'width':390,'height':844})
        ctx.close()
    b.close()
