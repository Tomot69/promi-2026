import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, timezone_id='Europe/Paris')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er=[]; pg.on('pageerror', lambda e: er.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    print(pg.evaluate("()=>{const e=_zzz.etat(); const f=t=>new Date(t).toLocaleTimeString('fr-FR',{timeZone:'Europe/Paris'}); return {e:e, lever:f(e.lever), coucher:f(e.coucher), fuseaux:_zzz.fuseaux}}"))
    for d in ('2026-06-21T12:00:00+02:00','2026-12-21T12:00:00+01:00'):
        print(d, pg.evaluate("(d)=>{const t=Date.parse(d), f=_zzz.fenetre(t), g=x=>new Date(x).toLocaleTimeString('fr-FR',{timeZone:'Europe/Paris'}); return [g(f.lever), g(f.coucher), f.source]}", d))
    print('neutres :', len(pg.evaluate("()=>_zzz.neutres()")), pg.evaluate("()=>_zzz.neutres().filter(k=>/creme95$|blanc100$|creme92$/.test(k.n))"))
    def cap(nom):
        im = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB'); im.save('scratchpad/v118/zzz-%s.png' % nom); return im
    pg.evaluate("()=>{ setTheme('dark'); _zzz.regle(false); closeAll(); Toile.setTheme('encre'); }"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ const pn=performance.now.bind(performance); const t0=pn(); performance.now=()=>t0; }"); pg.wait_for_timeout(600)
    a = cap('sombre')
    pg.evaluate("()=>{ window._zzzMaintenant=()=>Date.parse('2026-12-21T23:30:00+01:00'); _zzz.regle(true); }"); pg.wait_for_timeout(1500)
    print('nuit :', pg.evaluate("()=>{const e=_zzz.etat(); return [e.theme,e.cran,e.nuit, getComputedStyle(document.documentElement).getPropertyValue('--c-creme95'), document.getElementById('device').className]}"))
    n = cap('nuit')
    bb = ImageChops.difference(a, n).getbbox(); print('différence sombre ↔ nuit :', bb)
    # ce qui reste crème pur (#F7F0DE ± 2) dans l'image de nuit : des neutres clairs peints en canevas, pas en CSS
    px = n.load(); W,Hh = n.size; reste = 0; ys = {}
    for y in range(0,Hh,2):
        for x in range(0,W,2):
            r,g,bl = px[x,y]
            if abs(r-247)<3 and abs(g-240)<3 and abs(bl-222)<3: reste += 1; ys[y//100] = ys.get(y//100,0)+1
    print('pixels restés #F7F0DE dans la nuit :', reste, ys)
    print('pageerror :', er or 'aucune'); b.close()
