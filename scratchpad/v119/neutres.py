# en sombre de nuit : où reste-t-il des neutres clairs à leur valeur de JOUR ? (pixels exacts, puis l'élément sous le pixel)
import io, sys
from playwright.sync_api import sync_playwright
from PIL import Image
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
JOUR = {(247,240,222):'#F7F0DE', (243,231,209):'#F3E7D1', (255,255,255):'#FFFFFF', (228,215,187):'#E4D7BB', (244,231,209):'#F4E7D1'}
ECRANS = [('accueil', "()=>{closeAll()}"),
 ('fiche à tenir', "()=>{closeAll(); const p=promises.find(q=>!q.draft&&!q.req&&!q.nuee&&!q.chiche&&q.status!=='tenu'); openDetail(p.id)}"),
 ('fiche tenue', "()=>{closeAll(); const p=promises.find(q=>q.status==='tenu'&&!q.nuee); openDetail(p.id)}"),
 ('fiche chiche', "()=>{closeAll(); const p=promises.find(q=>q.chiche&&!q.draft); openDetail(p.id)}"),
 ('Cercle', "()=>{closeAll(); openEssaim('potager')}"),
 ('Peaufiner', "()=>{closeAll(); const p=promises.find(q=>!q.draft&&!q.req&&!q.nuee); openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900)}"),
 ('page +', "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300)}"),
 ('Index', "()=>{closeAll(); setView('toile'); ouvrirIndex()}"), ('Fil', "()=>{closeAll(); setView('fil')}"),
 ('Aura', "()=>{closeAll(); setView('toile'); document.getElementById('souffleBtn').click()}"),
 ('Studio', "()=>{const x=document.querySelector('#auraScreen .closeb'); if(x) x.click(); closeAll(); document.getElementById('openStudio2').click()}"),
 ('Réglages', "()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('settingsBtn').click()}"),
 ('Partager', "()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('shareBtn').click()}"),
 ('Ma Parole !', "()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('settingsBtn').click(); setTimeout(()=>{const b=document.getElementById('openPlusTop'); if(b) b.click();},500)}"),
 ('personne', "()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); openPerson('Rachel')}")]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, timezone_id='Europe/Paris')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){} window._zzzMaintenant=function(){return Date.parse('2026-12-21T23:30:00+01:00')};")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{ setTheme('dark'); _zzz.regle(true); closeAll(); }"); pg.wait_for_timeout(1200)
    print('nuit :', pg.evaluate("()=>document.getElementById('device').className"))
    total = 0
    for nom, js in ECRANS:
        pg.evaluate(js); pg.wait_for_timeout(2600)
        im = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB'); px = im.load(); pts = {}
        for y in range(0, im.height, 2):
            for x in range(0, im.width, 2):
                c = px[x, y]
                for k in JOUR:
                    if abs(c[0]-k[0]) <= 1 and abs(c[1]-k[1]) <= 1 and abs(c[2]-k[2]) <= 1: pts.setdefault(JOUR[k], []).append((x//2, y//2)); break
        n = sum(len(v) for v in pts.values()); total += n
        if not n: print('%-14s 0' % nom); continue
        qui = {}
        for hx, L in pts.items():
            for (x, y) in L[::max(1, len(L)//25)]:
                e = pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x+20,y+44); if(!e) return '?'; return (e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+(''+(e.className.baseVal!==undefined?e.className.baseVal:e.className)).split(' ').slice(0,2).join('.'))+' < '+(e.parentNode.id?'#'+e.parentNode.id:(''+e.parentNode.className).split(' ')[0])}", [x, y])
                qui[(hx, e)] = qui.get((hx, e), 0) + 1
        print('%-14s %d pixels :' % (nom, n), '; '.join('%s %s' % (k[0], k[1]) for k in sorted(qui, key=lambda k: -qui[k])[:7]))
    print('TOTAL', total); b.close()
