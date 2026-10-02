# planche @3x — §1 : v118 sans l'écho | la nouvelle Pelote, clair et sombre, deux palettes ; recadrages à 100 % (bord éclairé, ombre)
import sys, io, math
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S = 3; PALS = [('candide', 'Candide (claire)'), ('irascible', 'Irascible (soutenue)')]
caps = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for ver, url in (('v118', 'http://127.0.0.1:8752/zz-v118.html'), ('v119', 'http://127.0.0.1:8752/app.html')):
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S, reduced_motion='reduce')
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto(url); pg.wait_for_timeout(7000)
        for pal, _ in PALS:
            for d in (0, 1):
                pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); if(x && document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click();}"); pg.wait_for_timeout(900)
                pg.evaluate("(p)=>{try{_aura.fige(false)}catch(e){} Toile.setPalette(p); window.__R=Math.random; Math.random=function(){return 0.125;};}", pal)
                ouvre(pg, d); pg.evaluate("()=>{Math.random=window.__R}"); pg.wait_for_timeout(4500); pg.evaluate("()=>{_aura.fige(true); _aura.vue(2.9,0.35); const e=document.getElementById('auPeloteEcho'); if(e) e.style.visibility='hidden';}"); pg.wait_for_timeout(900)
                caps[(ver, pal, d)] = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44+104,'width':390,'height':396}))).convert('RGB')
        ctx.close()
    b.close()
try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 44); f1 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 34)
except Exception: f = f1 = ImageFont.load_default()
w, h = caps[('v119', 'candide', 0)].size; G = 50; T = 70
LUM = math.atan2(-0.72, -0.58); cx, cy = 195, 122.532 + 148 - 104
bx, by = cx + 124*math.cos(LUM), cy + 124*math.sin(LUM)
def rec(im, x, y, lw, lh): return im.crop((int((x-lw/2)*S), int((y-lh/2)*S), int((x+lw/2)*S), int((y+lh/2)*S)))
cw, ch = int(110*S), int(110*S); ow, oh = int(230*S), int(56*S)
rangs = [(pal, nom, d) for pal, nom in PALS for d in (0, 1)]
Wt = 2*w + cw*2 + 5*G + 0; Ht = G + len(rangs)*(h + T + G)
pl = Image.new('RGB', (Wt + 2*G + ow*0, Ht), (150, 146, 138)); dr = ImageDraw.Draw(pl); y = G
for pal, nom, d in rangs:
    a, c = caps[('v118', pal, d)], caps[('v119', pal, d)]
    dr.text((G, y), '%s, %s — v118 sans l’écho · v119 · le bord éclairé (100 %%) · l’ombre (100 %%)' % (nom, 'sombre' if d else 'clair'), fill=(20, 16, 6), font=f)
    pl.paste(a, (G, y + T)); pl.paste(c, (2*G + w, y + T))
    x0 = 3*G + 2*w
    pl.paste(rec(a, bx, by, 110, 110), (x0, y + T)); pl.paste(rec(c, bx, by, 110, 110), (x0 + cw + G, y + T))
    dr.text((x0, y + T + ch + 8), 'v118', fill=(20, 16, 6), font=f1); dr.text((x0 + cw + G, y + T + ch + 8), 'v119', fill=(20, 16, 6), font=f1)
    oy = 461.35 - 104
    o1, o2 = rec(a, 195, oy, 230, 56), rec(c, 195, oy, 230, 56)
    pl.paste(o1.resize((cw*2 + G, int(oh*(cw*2+G)/ow))), (x0, y + T + ch + 60)); pl.paste(o2.resize((cw*2 + G, int(oh*(cw*2+G)/ow))), (x0, y + T + ch + 60 + int(oh*(cw*2+G)/ow) + 50))
    dr.text((x0, y + T + ch + 60 + int(oh*(cw*2+G)/ow) + 6), 'l’ombre, v118 (dessus) · v119 (dessous)', fill=(20, 16, 6), font=f1)
    y += h + T + G
pl.save('planche-v119/planche-pelote-halo.png'); print(pl.size)
k = 1700/pl.width; pl.resize((1700, int(pl.height*k))).save('scratchpad/v119/pelote-vue.png')
