# §1 — planche @3x : fiches Promi (à tenir, en cours, tenue), Chiche (lancé = en cours, tenu à deux), Cercle, clair et sombre,
# la valeur DÉCIDÉE annotée à côté de chaque zone (décisions = celles de redteam_decisions.py, lues dans le fichier), et la valeur rendue.
import io, re, os, sys, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
ICI = os.getcwd()
src = io.open('redteam_decisions.py', encoding='utf-8').read()
ns = {}; exec(src.split("S = open(")[0].split("from playwright")[0] + src.split("from playwright.sync_api import sync_playwright")[1].split("S = open(")[0], ns)
D = ns['D']
FICHES = [('Promi à tenir', 'faire les crêpes'), ('Promi en cours', 'nager le mardi'), ('Promi tenue', 'planter un arbre'), ('Chiche lancé', 'courir dimanche'), ('Chiche tenu à deux', 'le grand plongeoir'), ('Cercle', None)]
RECTS = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const dp=document.getElementById('detailPoster'); const g=id=>document.getElementById(id);
  const R=(e,txt)=>{ if(!e) return null; let b; if(txt&&(e.textContent||'').trim()){ const r=document.createRange(); r.selectNodeContents(e); b=r.getBoundingClientRect(); } else b=e.getBoundingClientRect(); if(b.width<1) return null; return [b.left-dv.left,b.top-dv.top,b.right-dv.left,b.bottom-dv.top]; };
  const cs=e=>e?getComputedStyle(e):null; const c=e=>{const s=cs(e); return s?(s.webkitTextFillColor||s.color):null;};
  const cv=g('dpTrameCv'); let champ=null; try{const d=cv.getContext('2d').getImageData(6,6,1,1).data; champ='rgb('+d[0]+', '+d[1]+', '+d[2]+')';}catch(e){}
  const pl=dp.querySelector('.enh'); const ring=[...dp.querySelectorAll('canvas.kr-c')][0];
  const cb=cv?cv.getBoundingClientRect():null;
  return {r:{plateau:R(pl), motMarque:R(g('dptNat'),1), champ:cb?[12,cb.top-dv.top+20,40,cb.top-dv.top+48]:null, corps:[12,742,40,770], titre:R(g('dptTitre'),1), aQui:R(g('dptQui'),1), echeance:R(g('dptQuand'),1), trace:R(g('dptTrace'),1), anneau:R(ring)},
          v:{plateau:pl?cs(pl).backgroundColor:null, motMarque:c(g('dptNat')), champ:champ, corps:cs(dp).backgroundColor, titre:c(g('dptTitre')), aQui:c(g('dptQui')), echeance:c(g('dptQuand')), trace:c(g('dptTrace'))}}; }"""
def hexa(v):
    if not v or 'rgb' not in v: return v
    n = [int(x) for x in re.findall(r'\d+', v)[:3]]; return '#%02X%02X%02X' % tuple(n)
F = '/System/Library/Fonts/Supplemental/Arial.ttf'
f1 = ImageFont.truetype(F, 34); f2 = ImageFont.truetype(F, 26); fT = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 48)
S3 = 3; AW = 1500
tuiles = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light', 'dark'):
        pg.evaluate("(t)=>{try{closeAll()}catch(e){} setTheme(t)}", th); pg.wait_for_timeout(700)
        for nom, ti in FICHES:
            if ti: pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}", ti)
            else: pg.evaluate("()=>{closeAll(); openEssaim('potager');}")
            pg.wait_for_timeout(3200)
            z = pg.evaluate(RECTS)
            dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top]}")
            im = Image.open(io.BytesIO(pg.screenshot(clip={'x': dv[0], 'y': dv[1], 'width': 390, 'height': 844}))).convert('RGB')
            T = Image.new('RGB', (390 * S3 + AW, 844 * S3 + 110), (255, 255, 255)); T.paste(im, (0, 110)); d = ImageDraw.Draw(T)
            d.text((10, 20), '%s · %s' % (nom, 'clair' if th == 'light' else 'sombre'), font=fT, fill=(20, 20, 20))
            dec = {zz: (val, s) for (e, t_, zz, val, s) in D if e == nom and t_ == th}
            ys = []
            zs = sorted([zz for zz in ('plateau', 'motMarque', 'anneau', 'champ', 'titre', 'aQui', 'echeance', 'trace', 'corps') if z['r'].get(zz)], key=lambda zz: (z['r'][zz][1] + z['r'][zz][3]) / 2)
            for zone in zs:
                r = z['r'].get(zone)
                cy = 110 + (r[1] + r[3]) / 2 * S3; cx = r[2] * S3
                ly = max(cy, (ys[-1] + 120) if ys else 0); ys.append(ly)
                d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=(230, 0, 120), width=5)
                d.line([cx + 10, cy, 390 * S3 + 30, ly], fill=(230, 0, 120), width=3)
                vu = hexa(z['v'].get(zone)) if zone != 'anneau' else None
                if zone in dec:
                    val, s = dec[zone]; okk = (vu == val)
                    d.rectangle([390 * S3 + 40, ly - 28, 390 * S3 + 96, ly + 28], fill=val, outline=(0, 0, 0), width=2)
                    d.text((390 * S3 + 110, ly - 36), '%s  décidé %s  ·  rendu %s  %s' % (zone, val, vu, 'OK' if okk else 'ÉCART'), font=f1, fill=(0, 120, 40) if okk else (200, 0, 0))
                    d.text((390 * S3 + 110, ly + 4), s[:95], font=f2, fill=(90, 90, 90))
                else:
                    lab = 'trois arcs = les trois états (Q262) : #DD4D23 · #291547 · #00341A' if zone == 'anneau' else '%s  rendu %s  (aucune décision de Tom : valeur de v118)' % (zone, vu)
                    d.text((390 * S3 + 110, ly - 18), lab, font=f1, fill=(60, 60, 60))
            tuiles[(nom, th)] = T
    b.close()
W, H = tuiles[FICHES[0][0], 'light'].size
P = Image.new('RGB', (W * 2, H * len(FICHES)), (255, 255, 255))
for i, (nom, _) in enumerate(FICHES):
    for j, th in enumerate(('light', 'dark')): P.paste(tuiles[(nom, th)], (j * W, i * H))
os.makedirs('planche-v122', exist_ok=True); P.save('planche-v122/fiches-decisions.png')
P.resize((P.width // 3, P.height // 3), Image.LANCZOS).save('planche-v122/fiches-decisions-reduite.png', optimize=True)
print(P.size, os.path.getsize('planche-v122/fiches-decisions.png') // 1e6, 'Mo ;', os.path.getsize('planche-v122/fiches-decisions-reduite.png') // 1e6, 'Mo')
