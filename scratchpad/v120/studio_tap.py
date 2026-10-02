# Au vrai doigt (CDP) : toucher chaque disque et chaque ton du Studio, lire l'effet.  usage: studio_tap.py <fichier> [query]
import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]; Q=sys.argv[2] if len(sys.argv)>2 else ''
ETAT = """()=>({clair:document.documentElement.classList.contains('light')||document.body.classList.contains('light'), tx:(()=>{const b=document.querySelector('#txToggle [data-tx="on"]');return !!(b&&b.classList.contains('on'))})(),
  on:[...document.querySelectorAll('#stpVue .stp-d')].map(d=>d.classList.contains('on')?1:0).join(''), pal:(()=>{try{return Toile.mondeCourant().p}catch(e){return '?'}})(), monde:(()=>{try{return Toile.mondeCourant().m}catch(e){return '?'}})(),
  feuilles:[...document.querySelectorAll('.show')].map(e=>e.id).join(','), tons:[...document.querySelectorAll('#studioScreen .stp-ton')].map(e=>getComputedStyle(e).backgroundColor).join(' '),
  orbes:[...document.querySelectorAll('#studioScreen [data-pal], #studioScreen .pal-orb, #studioScreen .orb')].filter(e=>e.getBoundingClientRect().width>4).length})"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false});localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');}catch(e){}")
        pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:200])); cdp=ctx.new_cdp_session(pg)
        def tap(x,y):
            cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]}); pg.wait_for_timeout(60)
            cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(900)
        pg.goto('http://127.0.0.1:8752/'+F+Q); pg.wait_for_timeout(7000)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setTheme(t)}catch(e){}}",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*STUDIO\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}")
        pg.wait_for_timeout(3500)
        print('== %s%s [%s] départ %s' % (F,Q,th,pg.evaluate(ETAT)))
        cibles=pg.evaluate("()=>[...document.querySelectorAll('#stpVue .stp-d, #studioScreen .stp-ton')].map(e=>{const r=e.getBoundingClientRect();return {n:(e.id||e.className).toString().slice(0,24),x:r.left+r.width/2,y:r.top+r.height/2}})")
        for c in cibles:
            av=pg.evaluate(ETAT); tap(c['x'],c['y']); ap=pg.evaluate(ETAT)
            d={k:(av[k],ap[k]) for k in av if av[k]!=ap[k]}
            print('   toucher %-24s (%3d,%3d) → %s' % (c['n'],c['x'],c['y'], d if d else 'RIEN NE CHANGE'))
        pg.screenshot(path='scratchpad/v120/tap-%s-%s.png'%(F.replace('.html',''),th), clip={'x':20,'y':44,'width':390,'height':844})
        print('   erreurs', er[:3]); ctx.close()
    b.close()
