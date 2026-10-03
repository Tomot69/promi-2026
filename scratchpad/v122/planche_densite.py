# §5 — la Pelote de l'Aura aux trois densités, côte à côte, même taille, même palette (Ingénu, ton du sol n° 0), clair et sombre, halo 3.
# Sous chaque Pelote, un recadrage à 100 % (1 px d'image = 1 px d'écran @3x) sur la pelure, au même endroit pour les trois.
# Vue figée au même angle (_aura.fige / _aura.vue), « Réduire les animations » (souffle immobile à mi-cycle), palier haut forcé.
import io, os, sys, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
COUT = json.load(open('scratchpad/v122/cout_densite.json')) if os.path.exists('scratchpad/v122/cout_densite.json') else {}
S3 = 3; BOX = (20, 88, 370, 446)            # en pt dans l'appareil : la Pelote, son halo, son ombre
CROP = (120, 190, 220, 290)                 # en pt : 100 × 100 sur la pelure, à gauche du centre, au-dessus de l'équateur
F = '/System/Library/Fonts/Supplemental/Arial.ttf'; FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
f1 = ImageFont.truetype(FB, 44); f2 = ImageFont.truetype(F, 34)
col = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        for dn in (1, 2, 3):
            ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S3, reduced_motion='reduce')
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_pelote_palier','0');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
            pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?densite=%d&halo=3' % dn); pg.wait_for_timeout(6800)
            pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('souffleBtn').click();}", th)
            pg.wait_for_timeout(4000)
            info = pg.evaluate("""()=>{ for(let i=0;i<60 && _aura.sol().idx!==0;i++) _aura.nouveauSol(); _aura.fige(true); _aura.vue(0.6, 0.35); return {sol:_aura.sol().idx, reg:window._peloteReglage}; }""")
            pg.wait_for_timeout(1500)
            for _ in range(40):     # la Pelote peinte : le centre du canevas opaque (WebKit met plusieurs secondes à 165 000 et 220 000 poils)
                pg.evaluate("()=>{ try{ _aura.vue(0.6, 0.35); _aura.pelote(); }catch(e){} }")
                ok = pg.evaluate("()=>{ const c=document.getElementById('auBoule'); if(!c||!c.width) return false; const d=c.getContext('2d').getImageData((c.width/2)|0,(c.height/2)|0,1,1).data; return d[3]>250; }")
                if ok: break
                pg.wait_for_timeout(1500)
            print('   peinte :', ok, flush=True)
            pg.wait_for_timeout(2500)
            n = pg.evaluate("()=>{ try{ const S=_aura.verifie&&null; }catch(e){} return (window._peloteReglage.facteur*110000)|0; }")
            dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top]}")
            im = Image.open(io.BytesIO(pg.screenshot(clip={'x': dv[0] + BOX[0], 'y': dv[1] + BOX[1], 'width': BOX[2] - BOX[0], 'height': BOX[3] - BOX[1]}))).convert('RGB')
            cr = Image.open(io.BytesIO(pg.screenshot(clip={'x': dv[0] + CROP[0], 'y': dv[1] + CROP[1], 'width': CROP[2] - CROP[0], 'height': CROP[3] - CROP[1]}))).convert('RGB')
            col[(th, dn)] = (im, cr, n, info)
            print(th, dn, info['sol'], n, flush=True)
            ctx.close()
    b.close()
W = (BOX[2] - BOX[0]) * S3; H = (BOX[3] - BOX[1]) * S3; CW = (CROP[2] - CROP[0]) * S3
M = 60; HEAD = 215
P = Image.new('RGB', (3 * W + 4 * M, 2 * (HEAD + H + M + CW + M)), (255, 255, 255)); d = ImageDraw.Draw(P)
for r, th in enumerate(('light', 'dark')):
    y0 = r * (HEAD + H + M + CW + M)
    for c, dn in enumerate((1, 2, 3)):
        im, cr, n, info = col[(th, dn)]; x0 = M + c * (W + M)
        k = COUT.get(str(dn), {})
        d.text((x0, y0 + 20), 'densité %d · %s' % (dn, 'clair' if th == 'light' else 'sombre'), font=f1, fill=(20, 20, 20))
        d.text((x0, y0 + 80), '%s poils (palier haut) · poil ×%s' % (format(n, ',').replace(',', ' '), {1: '1', 2: '0,8', 3: '0,7'}[dn]), font=f2, fill=(60, 60, 60))
        t_ = k.get('txt', '—').split(' · image ')
        d.text((x0, y0 + 120), 'coût au banc : ' + t_[0], font=f2, fill=(60, 60, 60))
        if len(t_) > 1: d.text((x0, y0 + 158), 'image ' + t_[1], font=f2, fill=(60, 60, 60))
        P.paste(im, (x0, y0 + HEAD))
        # le cadre du recadrage, sur la Pelote
        cx0 = x0 + (CROP[0] - BOX[0]) * S3; cy0 = y0 + HEAD + (CROP[1] - BOX[1]) * S3
        d.rectangle([cx0, cy0, cx0 + CW, cy0 + CW], outline=(230, 0, 120), width=4)
        P.paste(cr, (x0 + (W - CW) // 2, y0 + HEAD + H + M))
        d.rectangle([x0 + (W - CW) // 2 - 2, y0 + HEAD + H + M - 2, x0 + (W + CW) // 2 + 2, y0 + HEAD + H + M + CW + 2], outline=(230, 0, 120), width=3)
os.makedirs('planche-v122', exist_ok=True)
P.save('planche-v122/densite-pelote.png')
R = P.resize((P.width * 2 // 3, P.height * 2 // 3), Image.LANCZOS)
R.save('planche-v122/densite-pelote-telephone.jpg', quality=88)
print(P.size, os.path.getsize('planche-v122/densite-pelote.png') / 1e6, 'Mo ·', R.size, os.path.getsize('planche-v122/densite-pelote-telephone.jpg') / 1e6, 'Mo')
