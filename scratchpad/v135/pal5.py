from playwright.sync_api import sync_playwright
src=open('scratchpad/v135/pal4.py').read(); E=src.split('E="""')[1].split('"""')[0]
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:150])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); setPremium(false);}"); pg.wait_for_timeout(800)
    pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2600)
    def sw():
        pg.mouse.move(300,300); pg.mouse.down(); [pg.mouse.move(300-i*20,300) for i in range(1,10)]; pg.mouse.up(); pg.wait_for_timeout(2300)
    for k in range(12):
        sw(); cls=pg.evaluate("()=>document.getElementById('studioScreen').className+' | '+((document.querySelector('#studioBody .st3-dot.on')||{getAttribute(){}}).getAttribute('data-w'))")
        # ouvrir le menu par la classe (le toucher d'une teinte est un mur sur un monde payant), puis par le toucher
        pg.evaluate("()=>document.getElementById('studioScreen').classList.add('stp-pals')"); pg.wait_for_timeout(700)
        e=pg.evaluate(E); print(k, cls[-60:], e and (e['orbe'], e['pn'], e['spec'], e['enfants']), flush=True)
        if e and e['orbe'] and float(e['orbe'][0])<20: pg.screenshot(path='scratchpad/v135/vide-%d.png'%k); 
        pg.evaluate("()=>document.getElementById('studioScreen').classList.remove('stp-pals')"); pg.wait_for_timeout(300)
    b.close()
