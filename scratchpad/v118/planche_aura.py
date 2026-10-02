# planche @3x — §5 (le bouton sous l'ombre, coté, 390 × 844) et §6 (l'écho décalé), deux thèmes
import sys, io
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S = 3
J = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, o={};
  const q={plateau:'#auraScreen .enh', ombre:'#auPeloteOmbre', echo:'#auPeloteEcho', boule:'#auBoule', bouton:'#auPartage', phrase:'.au-mot'};
  for(const n in q){ const e=document.querySelector((n==='plateau'?'':'#auraScreen ')+q[n]); const r=e.getBoundingClientRect(); o[n]=[(r.left-dv.left)/k,(r.top-dv.top)/k,(r.right-dv.left)/k,(r.bottom-dv.top)/k]; }
  o.ton=getComputedStyle(document.getElementById('auPeloteEcho')).backgroundColor; return o; }"""
caps = []
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for d in (0, 1):
        pg.evaluate("()=>{Toile.setPalette('signal'); window.__R=Math.random; Math.random=function(){return 0.125;};}")
        ouvre(pg, d); pg.evaluate("()=>{Math.random=window.__R}"); pg.wait_for_timeout(4000); pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(500)
        o = pg.evaluate(J); im = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
        caps.append((d, o, im))
        pg.evaluate("()=>{_aura.fige(false); const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    b.close()
try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 34); f2 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 46)
except Exception: f = f2 = ImageFont.load_default()
W, H = caps[0][2].size; M = 620; G = 60; T = 130
pl = Image.new('RGB', (2*(W + M) + 3*G, H + T + 2*G), (247, 240, 222)); dr = ImageDraw.Draw(pl)
for i, (d, o, im) in enumerate(caps):
    x0 = G + i*(W + M + G); y0 = T + G; pl.paste(im, (x0, y0))
    dr.text((x0, G), ('SOMBRE' if d else 'CLAIR') + ' — 390 × 844, @3x · écho : ' + o['ton'], fill=(32, 25, 8), font=f2)
    silBas = o['boule'][1] + 148 + 121.532          # centre de la boule + silhouette (boule 116,032 + poil 5,5)
    cotes = [(o['plateau'][3], 'bas du plateau %.1f' % o['plateau'][3]), (o['boule'][1] + 148 - 120.532, 'haut de la silhouette %.1f (G1 = 50)' % (o['boule'][1] + 148 - 120.532)),
             (silBas, 'bas de la silhouette %.1f' % silBas), (o['echo'][3], 'bas de l’écho %.1f (décalé de 11)' % o['echo'][3]),
             (o['ombre'][3], 'bas de l’ombre %.1f' % o['ombre'][3]), (o['bouton'][1], 'haut du bouton %.1f  ← G2 = %.1f' % (o['bouton'][1], o['bouton'][1] - o['ombre'][3])),
             (o['bouton'][3], 'bas du bouton %.1f (pli : 844)' % o['bouton'][3]), (o['phrase'][1] + 1.87, 'encre de la phrase %.1f  ← %.1f sous le bouton' % (o['phrase'][1] + 1.87, o['phrase'][1] + 1.87 - o['bouton'][3])),
             (844, 'le pli 844')]
    for y, txt in cotes:
        Y = y0 + int(y*S); dr.line([(x0, Y), (x0 + W + 24, Y)], fill=(221, 77, 35), width=3); dr.text((x0 + W + 34, Y - 20), txt, fill=(32, 25, 8), font=f)
pl.save('planche-v118/planche-aura-bouton-echo.png'); print(pl.size, [c[1]['bouton'] for c in caps], [c[1]['ton'] for c in caps])
k = 1700/pl.size[0]; pl.resize((1700, int(pl.size[1]*k))).save('scratchpad/v118/aura-planche-vue.png')
