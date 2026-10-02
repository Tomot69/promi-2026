# Ouvre le panneau des palettes au doigt et capture ; puis, panneau fermé, touche chaque disque.  usage: studio_pal.py <fichier> <tag> [query]
import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]; TAG=sys.argv[2]; Q=sys.argv[3] if len(sys.argv)>3 else ''
ETAT = """()=>({clair:document.documentElement.classList.contains('light')||document.body.classList.contains('light'), tx:(()=>{const b=document.querySelector('#txToggle [data-tx="on"]');return !!(b&&b.classList.contains('on'))})(),
  on:[...document.querySelectorAll('#stpVue .stp-d')].map(d=>d.classList.contains('on')?1:0).join(''), pal:(()=>{try{return Toile.mondeCourant().p}catch(e){return '?'}})()})"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
        ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false});localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');}catch(e){}")
        pg=ctx.new_page(); er=[]; pg.on('pageerror',lambda e:er.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/'+F+Q); pg.wait_for_timeout(7000)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setTheme(t)}catch(e){}}",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*STUDIO\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}")
        pg.wait_for_timeout(3500)
        print('== %s [%s] départ %s' % (F,th,pg.evaluate(ETAT)))
        ds=pg.evaluate("()=>[...document.querySelectorAll('#stpVue .stp-d')].map(e=>{const r=e.getBoundingClientRect();return {n:(e.id||e.className).toString().slice(0,24),x:r.left+r.width/2,y:r.top+r.height/2}})")
        for c in ds:
            av=pg.evaluate(ETAT); pg.touchscreen.tap(c['x'],c['y']); pg.wait_for_timeout(1100); ap=pg.evaluate(ETAT)
            d={k:(av[k],ap[k]) for k in av if av[k]!=ap[k]}
            print('   disque %-14s (%3d) → %s' % (c['n'],c['x'], d if d else 'RIEN NE CHANGE'))
        t=pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
        pg.touchscreen.tap(t[0],t[1]); pg.wait_for_timeout(1500)
        info=pg.evaluate("""()=>{const dv=document.getElementById('device').getBoundingClientRect(); const n=[...document.querySelectorAll('#studioScreen *')].filter(e=>{const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); return r.width>=20&&r.width<=60&&Math.abs(r.width-r.height)<2&&cs.borderRadius.indexOf('50%')>=0||(parseFloat(cs.borderRadius)>=r.width/2-1&&r.width>=20&&r.width<=60&&Math.abs(r.width-r.height)<2)});
          return {ronds:n.length, vides:n.filter(e=>{const cs=getComputedStyle(e);return (cs.backgroundColor==='rgba(0, 0, 0, 0)')&&cs.backgroundImage==='none'&&!e.querySelector('canvas,svg,*')}).length, ex:n.slice(0,6).map(e=>(e.className||'').toString().slice(0,20)+':'+getComputedStyle(e).backgroundColor+'/'+getComputedStyle(e).backgroundImage.slice(0,30))}}""")
        print('   panneau des palettes :', info)
        pg.screenshot(path='scratchpad/v120/pal-%s-%s.png'%(TAG,th), clip={'x':20,'y':44,'width':390,'height':844})
        print('   erreurs', er[:3]); ctx.close()
    b.close()
