# Qui salit les styles pendant « tenir » ? Mutations (attributs style/class, nœuds) du lever à +2,5 s, v148 contre v147.
import sys, json
from playwright.sync_api import sync_playwright
FICHIERS = sys.argv[1:] or ['app.html', 'zz-av147.html']
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for F in FICHIERS:
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        tot = {}
        for k in range(3):
            pid = pg.evaluate("()=>{ try{closeAll()}catch(e){} const L=promises.filter(x=>!x.draft&&!x.req&&!x.chiche&&!x.nuee); const p=L[%d %% Math.min(3,L.length)]; p.status='rate'; return p.id; }" % k)
            pg.wait_for_timeout(500); pg.evaluate("(i)=>{openDetail(i)}", pid); pg.wait_for_timeout(1500)
            pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(1700)
            r = pg.evaluate("()=>{const e=document.getElementById('tenirCv'); const q=e.getBoundingClientRect(); return {x:q.left,y:q.top,w:q.width,h:q.height}}")
            y = r['y'] + r['h'] / 2
            pg.mouse.move(r['x'] + 12, y); pg.mouse.down()
            for i in range(1, 26):
                pg.mouse.move(r['x'] + 12 + (r['w'] - 24) * i / 25, y + (6 if i % 2 else -6)); pg.wait_for_timeout(12)
            pg.evaluate("""()=>{ window.__mut={}; const nom=n=>{ if(!n||!n.tagName) return '#text'; return n.tagName.toLowerCase()+(n.id?'#'+n.id:'')+(typeof n.className==='string'&&n.className?'.'+n.className.trim().split(/\\s+/).slice(0,2).join('.'):''); };
              window.__mo=new MutationObserver(L=>{ const t=performance.now()-(window.__t0||performance.now()); if(t>2500) return; L.forEach(m=>{ const k=m.type+' '+(m.attributeName||'')+' '+nom(m.target); window.__mut[k]=(window.__mut[k]||0)+1; }); });
              window.__mo.observe(document.documentElement,{attributes:true,subtree:true,childList:true,characterData:true});
              window.addEventListener('mouseup', ()=>{ window.__t0=performance.now(); }, {capture:true, once:true}); }""")
            pg.mouse.up(); pg.wait_for_timeout(2800)
            m = pg.evaluate("()=>{ window.__mo.disconnect(); return window.__mut; }")
            for kk, v in m.items(): tot[kk] = tot.get(kk, 0) + v
        print('===', F, 'mutations en 3 « tenir » (lever → +2,5 s), les plus fréquentes :')
        for kk, v in sorted(tot.items(), key=lambda a: -a[1])[:25]: print('  %5d  %s' % (v, kk[:150]))
        ctx.close()
    b.close()
