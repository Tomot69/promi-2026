# cap6.py avant|apres — les trois éléments du §6, @3x
import sys, io
from playwright.sync_api import sync_playwright
nom = sys.argv[1]
def clip(pg, sel, m=14):
    r = pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width?{x:r.left,y:r.top,w:r.width,h:r.height}:null}", sel)
    return None if not r else {'x':max(0,r['x']-m),'y':max(0,r['y']-m),'width':r['w']+2*m,'height':r['h']+2*m}
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for th in ('light', 'dark'):
        pg.evaluate("(t)=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); setTheme(t); const p=promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.chiche&&q.status!=='tenu'); openDetail(p.id)}", th); pg.wait_for_timeout(2200)
        c = clip(pg, '#detailPoster .enh', 10); pg.screenshot(path='planche-v119/s6-%s-fermer-%s.png' % (nom, th), clip=c)
        pg.evaluate("()=>{closeAll(); openEssaim('potager')}"); pg.wait_for_timeout(2200)
        c = clip(pg, '#detailPoster .enh', 10); pg.screenshot(path='planche-v119/s6-%s-fermer-cercle-%s.png' % (nom, th), clip=c)
        pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('settingsBtn').click(); setTimeout(()=>{const b=document.getElementById('openPlusTop'); if(b) b.click();},500);}"); pg.wait_for_timeout(2600)
        pg.screenshot(path='planche-v119/s6-%s-achat-%s.png' % (nom, th), clip={'x':20+10,'y':44+664,'width':370,'height':150})
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); setTheme('dark'); document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(2600)
    c = clip(pg, '#shBadge', 16) or {'x':20,'y':44,'width':390,'height':300}
    pg.screenshot(path='planche-v119/s6-%s-badge.png' % nom, clip=c); print(nom, 'badge', c)
    b.close()
