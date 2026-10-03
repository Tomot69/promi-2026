# §1 — planche : la Pelote aux densités 1, 2 et 3, avec le NOUVEAU CORPS et ses dalles (les îles du jeu de démonstration : plusieurs
# natures et couleurs), clair et sombre, deux palettes (Ingénu, Irascible), recadrage à 100 % (1 px d'image = 1 px d'écran @3x) au même
# endroit. Les paramètres ?densite et ?halo sont retirés du produit (v123) : la planche règle la densité par un crochet de banc
# (elle intercepte `window._peloteReglage` au chargement) — jamais lu par le produit. Même sol et même corps pour les trois densités
# (on retire jusqu'à tomber sur les mêmes indices), même vue (rotation figée dès l'ouverture), palier haut.
import io, os, sys, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
S3 = 3; BOX = (20, 82, 370, 436); CROP = (200, 176, 300, 276)
DENS = {1: (1, 1, False), 2: (1.5, 0.8, True), 3: (2, 0.7, True)}
PALS = [('signal', 'Ingénu'), ('irascible', 'Irascible')]
COUT = json.load(open('scratchpad/v123/cout_densite.json')) if os.path.exists('scratchpad/v123/cout_densite.json') else {}
F = '/System/Library/Fonts/Supplemental/Arial.ttf'; FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
f1 = ImageFont.truetype(FB, 44); f2 = ImageFont.truetype(F, 32)
tu = {}; cible = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    for pal, _ in PALS:
        for th in ('light', 'dark'):
            for dn in (1, 2, 3):
                fa, ep, dx = DENS[dn]
                ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=S3, reduced_motion='reduce')
                ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_pelote_palier','0')}catch(e){}"
                                    "(function(){ var v; Object.defineProperty(window,'_peloteReglage',{configurable:true, get:function(){return v}, set:function(o){ try{ o.densite=%d; o.facteur=%s; o.epaisseur=%s; o.doux=%s; }catch(e){} v=o; }}); })();" % (dn, fa, ep, 'true' if dx else 'false'))
                pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
                pg.evaluate("([t,p])=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); try{Toile.setPalette(p)}catch(e){} closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('souffleBtn').click();}", [th, pal])
                pg.wait_for_timeout(1500)
                pg.evaluate("()=>{ try{ _aura.fige(true); _aura.vue(3.1, 0.32); }catch(e){} }")
                k = (pal, th)
                if k not in cible:
                    c = pg.evaluate("()=>{ const c=_aura.corps(); return [c.solIdx, c.idx]; }"); cible[k] = c
                else:
                    pg.evaluate("([s,c])=>{ for(let i=0;i<4000;i++){ const q=_aura.corps(); if(q.solIdx===s && q.idx===c) break; _aura.nouveauSol(); } }", cible[k])
                ok = False
                for _ in range(50):
                    pg.evaluate("()=>{ try{ _aura.fige(true); _aura.vue(3.1, 0.32); _aura.pelote(); }catch(e){} }")
                    ok = pg.evaluate("()=>{ const c=document.getElementById('auBoule'); if(!c||!c.width) return false; const d=c.getContext('2d').getImageData((c.width/2)|0,(c.height/2)|0,1,1).data; return d[3]>250; }")
                    if ok: break
                    pg.wait_for_timeout(1500)
                pg.wait_for_timeout(2500)
                info = pg.evaluate("()=>({c:_aura.corps(), p:_aura.etat().palier, r:window._peloteReglage, iles:(()=>{try{return _aura.etat().iles||null}catch(e){return null}})()})")
                dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top]}")
                im = Image.open(io.BytesIO(pg.screenshot(clip={'x': dv[0] + BOX[0], 'y': dv[1] + BOX[1], 'width': BOX[2] - BOX[0], 'height': BOX[3] - BOX[1]}))).convert('RGB')
                cr = Image.open(io.BytesIO(pg.screenshot(clip={'x': dv[0] + CROP[0], 'y': dv[1] + CROP[1], 'width': CROP[2] - CROP[0], 'height': CROP[3] - CROP[1]}))).convert('RGB')
                tu[(pal, th, dn)] = (im, cr, info)
                print(pal, th, dn, ok, info['p'], info['c']['solIdx'], info['c']['idx'], info['c']['rgb'], flush=True)
                ctx.close()
    b.close()
W = (BOX[2] - BOX[0]) * S3; H = (BOX[3] - BOX[1]) * S3; CW = (CROP[2] - CROP[0]) * S3; M = 60; HEAD = 215
RH = HEAD + H + M + CW + M
P = Image.new('RGB', (3 * W + 4 * M, len(PALS) * 2 * RH), (255, 255, 255)); d = ImageDraw.Draw(P); r = 0
for pal, nom in PALS:
    for th in ('light', 'dark'):
        y0 = r * RH; r += 1
        for c, dn in enumerate((1, 2, 3)):
            im, cr, info = tu[(pal, th, dn)]; x0 = M + c * (W + M); k = COUT.get(str(dn), {})
            hx = '#%02X%02X%02X' % tuple(int(v) for v in info['c']['rgb'])
            d.text((x0, y0 + 20), 'densité %d%s · %s · %s' % (dn, ' (retenue)' if dn == 3 else '', nom, 'clair' if th == 'light' else 'sombre'), font=f1, fill=(20, 20, 20))
            d.text((x0, y0 + 80), '%s poils · poil ×%s · corps %s' % (format(int(info['p']), ',').replace(',', ' '), {1: '1', 2: '0,8', 3: '0,7'}[dn], hx), font=f2, fill=(60, 60, 60))
            d.rectangle([x0 + W - 70, y0 + 78, x0 + W - 20, y0 + 118], fill=hx, outline=(0, 0, 0))
            d.text((x0, y0 + 124), 'coût au banc : %s' % k.get('txt', '—'), font=f2, fill=(60, 60, 60))
            P.paste(im, (x0, y0 + HEAD))
            cx0 = x0 + (CROP[0] - BOX[0]) * S3; cy0 = y0 + HEAD + (CROP[1] - BOX[1]) * S3
            d.rectangle([cx0, cy0, cx0 + CW, cy0 + CW], outline=(230, 0, 120), width=4)
            P.paste(cr, (x0 + (W - CW) // 2, y0 + HEAD + H + M))
            d.rectangle([x0 + (W - CW) // 2 - 2, y0 + HEAD + H + M - 2, x0 + (W + CW) // 2 + 2, y0 + HEAD + H + M + CW + 2], outline=(230, 0, 120), width=3)
os.makedirs('planche-v123', exist_ok=True)
P.save('planche-v123/pelote-densites-corps.png')
P.convert('RGB').save('planche-v123/pelote-densites-corps-telephone.jpg', quality=92)
print(P.size, os.path.getsize('planche-v123/pelote-densites-corps.png') / 1e6, 'Mo ·', os.path.getsize('planche-v123/pelote-densites-corps-telephone.jpg') / 1e6, 'Mo')
