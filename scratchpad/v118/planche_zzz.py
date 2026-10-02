# planche @3x — §10 : l'accueil en sombre et en sombre de nuit, côte à côte ; et la ligne SOMBRE / AVEC TEXTE du Studio, COTÉE
import io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S = 3
def cap(pg, clip=None): return Image.open(io.BytesIO(pg.screenshot(clip=clip or {'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S, timezone_id='Europe/Paris')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){} (function(){var s=7;Math.random=function(){s=(s*16807)%2147483647;return s/2147483647;};})();")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{ setTheme('dark'); _zzz.regle(false); closeAll(); }"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ const t0=performance.now(); performance.now=()=>t0; }"); pg.wait_for_timeout(500)
    a = cap(pg)
    pg.evaluate("()=>{ window._zzzMaintenant=()=>Date.parse('2026-12-21T23:30:00+01:00'); _zzz.regle(true); }"); pg.wait_for_timeout(1500)
    n = cap(pg); etat = pg.evaluate("()=>_zzz.neutres().filter(k=>/creme95$/.test(k.n))[0]")
    # la ligne du Studio, telle qu'elle est (le bouton Zzz n'y est pas posé)
    rows = []
    for th in ('light', 'dark'):
        pg.evaluate("(t)=>{ _zzz.regle(false); setTheme(t); closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('openStudio2').click(); }", th); pg.wait_for_timeout(2600)
        g = pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('#stpVue .stp-d')].map(d=>{const r=d.getBoundingClientRect(); return [r.left-dv.left, r.top-dv.top, r.width, d.classList.contains('on')]})}")
        rows.append((th, g, cap(pg, {'x':20,'y':44+620,'width':390,'height':130})))
    b.close()
try: f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 44); f1 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
except Exception: f = f1 = ImageFont.load_default()
W, H = a.size; G = 60; T = 130
rw, rh = rows[0][2].size
pl = Image.new('RGB', (2*W + 3*G, T + H + G + 2*(rh + 330) + 2*G), (247, 240, 222)); d = ImageDraw.Draw(pl)
d.text((G, G), 'SOMBRE ordinaire — crème #F7F0DE', fill=(32, 25, 8), font=f); d.text((2*G + W, G), 'SOMBRE DE NUIT — crème %s (OKLCH L −0,06)' % etat['a'], fill=(32, 25, 8), font=f)
pl.paste(a, (G, T)); pl.paste(n, (2*G + W, T))
y = T + H + G
for th, g, im in rows:
    d.text((G, y), 'Le Studio, %s — la ligne telle qu’elle est : deux paires de disques de 44, écart 20 dans la paire, 56 entre les paires' % ('clair' if th == 'light' else 'sombre'), fill=(32, 25, 8), font=f1)
    pl.paste(im, (G, y + 60))
    yy = y + 60 + rh + 14
    for (x, t, w, on) in g:
        X0 = G + int(x*S); X1 = G + int((x + w)*S); d.line([(X0, yy), (X1, yy)], fill=(221, 77, 35), width=4); d.text((X0, yy + 8), '%.0f→%.0f%s' % (x, x + w, ' +9,7' if on else ''), fill=(32, 25, 8), font=f1)
    X0 = G + int(173*S); X1 = G + int(217*S); d.line([(X0, yy + 70), (X1, yy + 70)], fill=(41, 21, 71), width=4)
    d.text((G, yy + 84), 'un troisième disque de 44, centré : 173→217 — 6 de jeu contre les disques voisins (167 et 223) ; l’anneau du disque pris (9,7) le recouvre de 3,7,', fill=(32, 25, 8), font=f1)
    d.text((G, yy + 124), 'et le sien (163,3→226,7) recouvrirait ses deux voisins de 3,7. Il ne tient pas sans déplacer les paires (il faudrait 84 entre elles au lieu de 56).', fill=(32, 25, 8), font=f1)
    y += rh + 330
pl.save('planche-v118/planche-zzz.png'); print(pl.size, rows[0][1])
k = 1500/pl.size[0]; pl.resize((1500, int(pl.size[1]*k))).save('scratchpad/v118/zzz-planche-vue.png')
