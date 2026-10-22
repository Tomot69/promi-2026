import sys, random; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from banc_tom import *
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; M=sys.argv[2] if len(sys.argv)>2 else 'terrazzo'; N=int(sys.argv[3]) if len(sys.argv)>3 else 25; TOURS=int(sys.argv[4]) if len(sys.argv)>4 else 20
random.seed(7)
PR="()=>{var p=Toile_probe(); var m=0; p.forEach(function(d){m=Math.max(m,Math.abs(d[0]),Math.abs(d[1]))}); return [m, p.length, Toile_state().running]}"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b, stockage={'promi_monde':M}); toile_pleine(ctx, N); pg = ouvre(ctx, F)
    pg.evaluate("m=>{if(Toile.getTheme()!==m)Toile.setTheme(m)}", M); pg.wait_for_timeout(3000)
    print('départ', pg.evaluate(PR))
    for i in range(TOURS):
        sel=random.choice(['#souffleBtn','#indexBtn','#filBtn','#studioBtn','#createBtn'])
        attente=random.choice([300,800,2000,5000])
        tap_sel(pg, sel); pg.wait_for_timeout(attente)
        if sel=='#studioBtn': tap_sel(pg,'#studioScreen .closeb')
        else: pg.evaluate("()=>{try{const s=[...document.querySelectorAll('.screen.show .closeb, #feedView .closeb, #indexSheet .closeb')];}catch(e){} try{closeAll()}catch(e){}}")
        pg.wait_for_timeout(random.choice([200,1500,4000]))
        r=pg.evaluate(PR); print(i, sel, attente, r, flush=True)
    capture(pg,'scratchpad/v159/d_fin.png')
    b.close()
