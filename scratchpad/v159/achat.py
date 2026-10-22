import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; SAUT=int(sys.argv[2]) if len(sys.argv)>2 else 0; N=int(sys.argv[3]) if len(sys.argv)>3 else 25
GEO = "()=>{var c=Toile_cellules();return {v:[+c.view.s.toFixed(3),+c.view.ox.toFixed(1),+c.view.oy.toFixed(1)],n:c.c.length,g:c.c.filter(s=>s.kind!=='gray').map(s=>[s.pid,+s.x.toFixed(1),+s.y.toFixed(1)]),th:Toile.getTheme(),cv:document.getElementById('toileCv').width}}"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 692}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{if(!sessionStorage.getItem('__amorce')){sessionStorage.setItem('__amorce','1');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');}}catch(e){}")
    B.toile_pleine(ctx, N); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} closeAll(); }"); pg.wait_for_timeout(1500)
    a = pg.evaluate(GEO); B.capture(pg, 'scratchpad/v159/h_a.png')
    pg.evaluate("()=>{ document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    vus = 0
    for i in range(30):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"):
            if vus >= SAUT: break
            vus += 1
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500)
    w = pg.evaluate("()=>window._lockedWorld"); print('monde', w, 'thème avant achat', pg.evaluate("()=>Toile.getTheme()"))
    c = pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(2000)
    t = pg.evaluate("()=>{ const e=document.querySelector('#accRappelCompte .tard'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
    pg.touchscreen.tap(t[0], t[1]); pg.wait_for_timeout(3000)
    t = pg.evaluate("()=>{ const e=document.querySelector('#accRappelCompte .tard'); if(!e) return null; const r=e.getBoundingClientRect(); return r.width?[r.left+r.width/2, r.top+r.height/2]:null; }")
    if t: pg.touchscreen.tap(t[0], t[1]); pg.wait_for_timeout(2500)
    B.capture(pg, 'scratchpad/v159/h_s.png')
    B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(3000)
    bb = pg.evaluate(GEO); B.capture(pg, 'scratchpad/v159/h_b.png')
    print('thème', a['th'], '→', bb['th'], 'vue', a['v'], bb['v'], 'cellules', a['n'], bb['n'], 'cv', a['cv'], bb['cv'])
    A={x[0]:x for x in a['g']}; Bb={x[0]:x for x in bb['g']}
    d=[(k,A[k][1:],Bb.get(k)) for k in A if k not in Bb or abs(A[k][1]-Bb[k][1])>0.5 or abs(A[k][2]-Bb[k][2])>0.5]
    print('déplacées', len(d), d[:3]); print(pg.erreurs[:3])
    # puis ouvrir/fermer les pages
    for sel in ['#souffleBtn','#indexBtn','#filBtn']:
        B.tap_sel(pg, sel); pg.wait_for_timeout(1800); pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(1800)
        cc = pg.evaluate(GEO); print(sel, 'vue', cc['v'], 'n', cc['n'], 'déplacées', sum(1 for x in cc['g'] if x[0] in Bb and (abs(Bb[x[0]][1]-x[1])>0.5 or abs(Bb[x[0]][2]-x[2])>0.5)))
    B.capture(pg, 'scratchpad/v159/h_c.png')
    b.close()
