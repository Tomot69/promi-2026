import re, sys
from playwright.sync_api import sync_playwright
POINTS=re.search(r'POINTS=r"""(.*?)"""', open('redteam_toucher.py',encoding='utf-8').read(), re.S).group(1)
F=sys.argv[2] if len(sys.argv)>2 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch()
    for m in sys.argv[1].split(','):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} Toile.setTheme(m);}", m); pg.wait_for_timeout(4000)
        def essai(lab):
            P=pg.evaluate(POINTS); r=[]
            for q in P['pts']:
                pile=pg.evaluate("([x,y])=>document.elementsFromPoint(x,y).slice(0,3).map(h=>(h.id||String(h.className).split(' ')[0]||h.tagName)).join('>')", [q['x'],q['y']])
                pg.touchscreen.tap(q['x'],q['y']); pg.wait_for_timeout(1400)
                o=pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"); r.append(('OUI' if o else 'NON ['+pile+']'))
                pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(700)
            print(m, lab, r, '· dalles', P['dalles'], flush=True)
        essai('au repos')
        # planter par la page +
        pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3600)
        pg.evaluate("()=>{ const f=document.getElementById('fTitle'); f.value='parole neuve'; f.dispatchEvent(new Event('input',{bubbles:true})); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(6000)
        essai('après une plantation')
        # tenir une parole (segStatus), puis revenir
        pg.evaluate("()=>{ const p=promises.find(q=>q.title==='nager le mardi'); openDetail(p.id); }"); pg.wait_for_timeout(2000)
        pg.evaluate("()=>document.querySelector('#segStatus button[data-st=tenu]').click()"); pg.wait_for_timeout(4000); pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(1500)
        essai('après avoir tenu')
        # attendre la vie au repos (20 s) puis toucher
        pg.wait_for_timeout(20000); essai('après 20 s de repos')
        ctx.close()
    b.close()
