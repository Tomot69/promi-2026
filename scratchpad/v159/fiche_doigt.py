import sys, random; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; M=sys.argv[2] if len(sys.argv)>2 else 'terrazzo'; N=int(sys.argv[3]) if len(sys.argv)>3 else 25
random.seed(3)
GEO = "()=>{var c=Toile_cellules();return {v:[+c.view.s.toFixed(3),+c.view.ox.toFixed(1),+c.view.oy.toFixed(1)],n:c.c.length,g:c.c.filter(s=>s.kind!=='gray').map(s=>[s.pid,+s.x.toFixed(1),+s.y.toFixed(1)])}}"
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 692}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{if(!sessionStorage.getItem('__amorce')){sessionStorage.setItem('__amorce','1');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_monde','%s');}}catch(e){}" % M)
    toile_pleine(ctx, N); pg = ouvre(ctx, F)
    pg.evaluate("m=>{if(Toile.getTheme()!==m)Toile.setTheme(m)}", M); pg.wait_for_timeout(3000)
    a = pg.evaluate(GEO); capture(pg,'scratchpad/v159/f_a.png')
    for i in range(8):
        g = random.choice([x for x in a['g'] if 200 < x[2] < 680])
        X = g[1]*a['v'][0]+a['v'][1]; Y = g[2]*a['v'][0]+a['v'][2]
        tap(pg, X, Y); pg.wait_for_timeout(random.choice([900,2500]))
        ouvert = pg.evaluate("()=>{var d=document.getElementById('detailPoster');return !!(d&&d.classList.contains('show'))}")
        tap_sel(pg, '#detailPoster .closeb'); pg.wait_for_timeout(random.choice([400,1500,3000]))
        bb = pg.evaluate(GEO)
        A={x[0]:x for x in a['g']}; d=[x for x in bb['g'] if x[0] in A and (abs(A[x[0]][1]-x[1])>0.5 or abs(A[x[0]][2]-x[2])>0.5)]
        print(i, 'dalle', g[0], 'fiche', ouvert, 'vue', bb['v'], 'déplacées', len(d), d[:2], flush=True)
    capture(pg,'scratchpad/v159/f_b.png'); print(pg.erreurs[:2]); b.close()
