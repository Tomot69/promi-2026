"""Captures du VRAI moteur pour la planche de l'onboarding (21 sept. 2026).
La Toile vide, la dalle d'un Promi à soi sous Ingénu, l'accueil à une dalle — rendus par app.html."""
import base64, json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
CHROME = "#accPlat,#accBarre,#accChoix,.acc-barre,.acc-plat,#toast,.caption,#captionBar"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for th in ('dark', 'light'):
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        ctx.add_init_script("try{if(!sessionStorage.getItem('x')){sessionStorage.setItem('x','1');localStorage.clear();localStorage.setItem('promi_onb','1');localStorage.setItem('promi_fresh','1');}}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        pg.evaluate("(t)=>{obResetData(); Toile.sync([]); try{render()}catch(e){}; setTheme(t)}", th); pg.wait_for_timeout(2500)
        dev = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return {x:r.left,y:r.top,width:r.width,height:r.height}}")
        info = {'device': dev, 'n0': pg.evaluate("()=>({n:promises.length,col:Toile.colored()})")}
        cache = "(s)=>{document.querySelectorAll(s).forEach(e=>e.style.setProperty('visibility','hidden','important'))}"
        montre = "(s)=>{document.querySelectorAll(s).forEach(e=>e.style.removeProperty('visibility'))}"
        pg.evaluate(cache, CHROME); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(D, 'toile-vide-%s.png' % th), clip=dev)
        pg.evaluate(montre, CHROME)
        # le moteur choisit la cellule ; on retire jusqu'à un tirage entièrement dans l'écran (lisibilité de la planche)
        for essai in range(12):
            pid = pg.evaluate("""()=>{obResetData(); Toile.sync([]); var np=P('marcher une heure','Moi',7,2,'encours',undefined,'moi');
                computeBox();np.x=box.x+box.w/2;np.y=box.y+box.h/2;np.tx=np.x;np.ty=np.y;promises.push(np);
                Toile.sync([np.id]); if(typeof render==='function')render(); return np.id;}""")
            pg.wait_for_timeout(1500)
            bx = pg.evaluate("""(pid)=>{const a=Toile.dalleAbs(pid); if(!a) return null; const cv=document.getElementById('toileCv');
                const R=cv.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect();
                const sx=R.width/cv.clientWidth, k=D.width/390; return [(R.left-D.left+a.minx*sx)/k,(R.top-D.top+a.miny*sx)/k,a.w*sx/k,a.h*sx/k];}""", pid)
            if bx and bx[0] > 40 and bx[0] + bx[2] < 350 and 200 < bx[1] and bx[1] + bx[3] < 470:
                break
        pg.wait_for_timeout(1500)
        pg.screenshot(path=os.path.join(D, 'accueil-une-dalle-%s.png' % th), clip=dev)
        pg.evaluate(cache, CHROME); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(D, 'toile-une-dalle-%s.png' % th), clip=dev)
        pg.evaluate(montre, CHROME)
        r = pg.evaluate("""(pid)=>{const a=Toile.dalleAbs(pid); const cv=document.getElementById('toileCv');
            const R=cv.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect();
            const sx=R.width/cv.clientWidth, sy=R.height/cv.clientHeight, k=D.width/390;
            const c=document.createElement('canvas'); c.width=300; c.height=300; c.style.cssText='position:fixed;left:0;top:0;width:150px;height:150px';
            document.body.appendChild(c);
            const p=promises.find(q=>q.id===pid); const ok=Toile.dalleTrame(c,pid,1,p&&p.monde);
            const url=c.toDataURL('image/png'); c.remove();
            return {ok:ok, url:url, cw:c.width, ch:c.height,
               box:{x:(R.left-D.left+a.minx*sx)/k, y:(R.top-D.top+a.miny*sy)/k, w:a.w*sx/k, h:a.h*sy/k},
               nat:(p&&p.dalle)||null, monde:(p&&p.monde)||null, col:Toile.colored()}; }""", pid)
        open(os.path.join(D, 'dalle-%s.png' % th), 'wb').write(base64.b64decode(r.pop('url').split(',')[1]))
        info.update(r)
        json.dump(info, open(os.path.join(D, 'capture-%s.json' % th), 'w'), indent=1)
        print(th, json.dumps(info))
        ctx.close()
    b.close()
