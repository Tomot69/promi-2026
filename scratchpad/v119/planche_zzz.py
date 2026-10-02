# planche @3x — le bouton Zzz : la ligne en clair et en sombre, activé et désactivé, à 100 % ; et le Studio avant/après, hors de cette ligne
import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S = 3
GEO = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, o=[]; document.querySelectorAll('#studioScreen *').forEach(e=>{ if(e.closest('#stpVue,#stpLab')) return; const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return; const c=getComputedStyle(e); if(c.visibility==='hidden'||c.display==='none') return;
   o.push((e.id||e.tagName+'.'+(''+e.className).split(' ')[0])+' '+[(r.left-dv.left)/k,(r.top-dv.top)/k,r.width/k,r.height/k].map(v=>v.toFixed(1)).join(',')+' '+c.color+' '+c.fontSize); }); return o; }"""
def ouvre(pg, th, zzz):
    pg.evaluate("([t,z])=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); setTheme(t); try{ _zzz.regle(z); }catch(e){} document.getElementById('openStudio2').click(); }", [th, zzz]); pg.wait_for_timeout(2600)
with sync_playwright() as p:
    b = p.webkit.launch(); caps = {}; geo = {}
    for nom, url in (('v118', 'http://127.0.0.1:8752/zz-v118.html'), ('v119', 'http://127.0.0.1:8752/app.html')):
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S, timezone_id='Europe/Paris')
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){} window._zzzMaintenant=function(){return Date.parse('2026-12-21T12:00:00+01:00')};")
        pg = ctx.new_page(); pg.goto(url); pg.wait_for_timeout(7000)
        for th in ('light', 'dark'):
            for z in ((True, False) if nom == 'v119' else (False,)):
                ouvre(pg, th, z); geo[(nom, th, z)] = pg.evaluate(GEO)
                caps[(nom, th, z)] = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44+636,'width':390,'height':134}))).convert('RGB')
        ctx.close()
    b.close()
for th in ('light', 'dark'):
    a, c = geo[('v118', th, False)], geo[('v119', th, False)]
    print('Studio %s — hors de la ligne : %d éléments avant, %d après, %d différents' % (th, len(a), len(c), len(set(a) ^ set(c))), sorted(set(a) ^ set(c))[:4])
try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 40)
except Exception: f = ImageFont.load_default()
w, h = caps[('v119', 'light', True)].size; G = 50; T = 70
ordre = [('v118', 'light', False, 'AVANT (v118) — clair'), ('v119', 'light', True, 'v119 — clair, Zzz activé'), ('v119', 'light', False, 'v119 — clair, Zzz désactivé'),
         ('v118', 'dark', False, 'AVANT (v118) — sombre'), ('v119', 'dark', True, 'v119 — sombre, Zzz activé'), ('v119', 'dark', False, 'v119 — sombre, Zzz désactivé')]
pl = Image.new('RGB', (w + 2*G, len(ordre)*(h + T + G) + G), (247, 240, 222)); d = ImageDraw.Draw(pl); y = G
for k in ordre:
    d.text((G, y), k[3] + '   (100 %, @3x)', fill=(32, 25, 8), font=f); pl.paste(caps[k[:3]], (G, y + T)); y += h + T + G
pl.save('planche-v119/planche-zzz-bouton.png'); print(pl.size)
