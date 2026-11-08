#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_vol_dalle.py — LA DALLE QUI NAÎT AU DEMI-TRAIT ARRIVE SUR LA TOILE, ET C'EST TOUT (v183b, Tom, 7 nov. 2026 — C-237 suite, C-241 suite).
« À la fin du vol il y a encore un coup : pas de substitution visible, pas de flash, pas de changement de taille, de forme ni de couleur au moment où elle se pose. »
« À tout instant, une seule dalle de la nouvelle parole est visible à l'écran. »
Banc WebKit 430 × 932 ×3, Toile de dix paroles, page + d'un Promi au doigt, la moitié du trait tracée ; mondes : Pochade sous Ingénu (la palette par défaut),
Esquille (une Toile faite de ses paroles), Touffe, Tesselle :
  A · UNE SEULE DALLE, image par image (relevé dans la page) : jamais la dalle qui vole ET la page + qui montre encore la sienne ;
  B · L'ATTERRISSAGE : l'image de la dalle qui vole, gardée au moment où elle est collée dans l'image de la Toile d'avant (sa boîte rendue), puis comparée,
      une fois la Toile d'avant retirée, aux pixels de l'écran à la même place : ≤ 4 % de pixels écartés de plus de 40 niveaux (le titre que la Toile écrit
      sur sa dalle compris) — ni place, ni taille, ni forme, ni couleur ne changent quand elle se pose.
`?onbLent=4` ralentit le retrait (les photographies tombent au début de lui, pas au milieu). Usage : python3 redteam_vol_dalle.py [fichier.html] [mondes…]
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
exec(open('redteam_moitie.py').read().split('REF = None')[0].split('from playwright.sync_api import sync_playwright')[1])
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
MONDES = [a for a in sys.argv[1:] if not a.endswith('.html') and not a.startswith('--')] or ['encre', 'esquille', 'touffe', 'mosaique']
NOMS = {'encre': 'Pochade · Ingénu', 'esquille': 'Esquille', 'touffe': 'Touffe', 'mosaique': 'Tesselle'}
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('%s  %s  %s' % ('OK' if ok else 'KO', nom, str(d)[:220]), flush=True)
REC = r"""()=>{ window.__vol=[]; const t0=performance.now(); (function f(){ const dc=document.querySelector('#ppNait .onbv-dalle'), cs=document.getElementById('createSheet');
   const pageDalle=!!(cs && cs.classList.contains('show') && !cs.classList.contains('cs-coupe') && getComputedStyle(cs).visibility!=='hidden' && !window._ppSansDalle);
   window.__vol.push([Math.round(performance.now()-t0), !!dc, pageDalle]); if(performance.now()-t0<7000) requestAnimationFrame(f); })(); }"""
PIEGE = r"""()=>{ /* v187 (§1) : l'atterrissage est `_atterrit` (la Toile vivante pendant le vol, la couche partie dans une image) — contrat remis au niveau (original : sauvegardes/redteam_vol_dalle-avant-v187.py) */ const NOM=window._atterrit?'_atterrit':(window._poseNette?'_poseNette':'_retireFondFlaques'); const o=window[NOM]; window.__fini=false; window.__dc=null; window[NOM]=function(fond, dc, fin, a4, a5){ window[NOM]=o;
   /* v186c (C-237) : après l'atterrissage, chaque image : la part de pixels qui change hors de la dalle d'une image à la suivante (le mouvement de la Toile) */
   try{ const tc0=document.getElementById('toileCv'), dv0=document.getElementById('device'); window.__img=[]; let prev=null; const t1=performance.now();
     const lit=()=>{ const D=dv0.getBoundingClientRect(), s=(D.width/(dv0.offsetWidth||390))||1, E=2, c=document.createElement('canvas'); c.width=390*E; c.height=844*E; const rt=tc0.getBoundingClientRect(); if(!rt.width) return null; c.getContext('2d').drawImage(tc0,(rt.left-D.left)/s*E,(rt.top-D.top)/s*E,rt.width/s*E,rt.height/s*E); return {d:c.getContext('2d').getImageData(0,0,c.width,c.height).data, w:c.width, s:s, D:D, E:E}; };
     (function f(){ const r=dc && dc.getBoundingClientRect && dc.parentNode ? dc.getBoundingClientRect() : (window.__dcR||null); if(r && dc.parentNode) window.__dcR=r; const L=lit();
       if(L && prev && r){ const bx=[((r.left-L.D.left)/L.s-8)*L.E,((r.top-L.D.top)/L.s-8)*L.E,((r.right-L.D.left)/L.s+8)*L.E,((r.bottom-L.D.top)/L.s+8)*L.E]; let n=0,ch=0;
         for(let y=0;y<844*L.E;y+=3) for(let x=0;x<L.w;x+=3){ if(x>=bx[0]&&x<=bx[2]&&y>=bx[1]&&y<=bx[3]) continue; const i=(y*L.w+x)*4; n++; if(Math.max(Math.abs(L.d[i]-prev[i]),Math.abs(L.d[i+1]-prev[i+1]),Math.abs(L.d[i+2]-prev[i+2]))>24) ch++; }
         window.__img.push([Math.round(performance.now()-t1), Math.round(1000*ch/Math.max(1,n))/10]); }
       if(L && !window.__c0done && fond && fond.width){ window.__c0done=true; try{ const A=document.createElement('canvas'); A.width=L.w; A.height=844*L.E; A.getContext('2d').drawImage(fond,0,0,A.width,A.height); const a=A.getContext('2d').getImageData(0,0,A.width,A.height).data; const r2=window.__dcR; const bx=r2?[((r2.left-L.D.left)/L.s-8)*L.E,((r2.top-L.D.top)/L.s-8)*L.E,((r2.right-L.D.left)/L.s+8)*L.E,((r2.bottom-L.D.top)/L.s+8)*L.E]:[0,0,0,0]; let n=0,ch=0; for(let y=0;y<844*L.E;y+=3) for(let x=0;x<L.w;x+=3){ if(x>=bx[0]&&x<=bx[2]&&y>=bx[1]&&y<=bx[3]) continue; const i=(y*L.w+x)*4; n++; if(Math.max(Math.abs(L.d[i]-a[i]),Math.abs(L.d[i+1]-a[i+1]),Math.abs(L.d[i+2]-a[i+2]))>24) ch++; } window.__hors={pc:100*ch/Math.max(1,n), n:n, quand:'première image vivante'}; }catch(e){ window.__hors={err:String(e)}; } }
       if(L) prev=L.d; if(performance.now()-t1<2600) requestAnimationFrame(f); })(); }catch(e){ window.__img=[['err',String(e)]]; }
   try{ if(dc && dc.width){ const r=dc.getBoundingClientRect(); window.__dc={u:dc.toDataURL(), r:[r.left,r.top,r.width,r.height]}; } }catch(_){ }
   /* v186c (C-237 : « aucun pixel ne change à l'extérieur du contour de la dalle ») : à l'atterrissage, l'image figée (ce qu'on voyait) contre la Toile vivante
      (ce qu'on voit ensuite), hors de la boîte de la dalle élargie de 8 pt, à la densité de l'image figée */
   try{ const tc=document.getElementById('toileCv'), dv=document.getElementById('device'), D=dv.getBoundingClientRect(), s=(D.width/(dv.offsetWidth||390))||1, E=fond.width/390;
     const A=document.createElement('canvas'); A.width=fond.width; A.height=fond.height; const ga=A.getContext('2d'); ga.drawImage(fond,0,0);
     const Bc=document.createElement('canvas'); Bc.width=fond.width; Bc.height=fond.height; const gb=Bc.getContext('2d'); const rt=tc.getBoundingClientRect(); gb.drawImage(tc,(rt.left-D.left)/s*E,(rt.top-D.top)/s*E,rt.width/s*E,rt.height/s*E);
     const r=dc && dc.getBoundingClientRect(); const bx=r?[((r.left-D.left)/s-8)*E,((r.top-D.top)/s-8)*E,((r.right-D.left)/s+8)*E,((r.bottom-D.top)/s+8)*E]:[0,0,0,0];
     const a=ga.getImageData(0,0,A.width,A.height).data, b2=gb.getImageData(0,0,A.width,A.height).data; let n=0, ch=0;
     for(let y=0;y<A.height;y+=2) for(let x=0;x<A.width;x+=2){ if(x>=bx[0]&&x<=bx[2]&&y>=bx[1]&&y<=bx[3]) continue; const i=(y*A.width+x)*4; n++; if(Math.max(Math.abs(a[i]-b2[i]),Math.abs(a[i+1]-b2[i+1]),Math.abs(a[i+2]-b2[i+2]))>24) ch++; }
     window.__hors={pc:100*ch/Math.max(1,n), n:n, vue:Toile.vue(), vue0:window.__vue0||null, g:(window.Toile_graines?Toile_graines():[]).filter(z=>z[3]!=='gray').length}; }catch(e){ window.__hors={err:String(e)}; }
   return o(fond, dc, function(){ window.__fini=true; if(fin) fin(); }, a4, a5); }; }"""
def zone(im, r, S=3, m=24): return im.crop((int(r[0]*S)-m, int(r[1]*S)-m, int((r[0]+r[2])*S)+m, int((r[1]+r[3])*S)+m))
def change(a, c): d = ImageChops.difference(a, c).convert('L'); h = d.histogram(); return 100 * sum(h[40:]) / max(1, sum(h))
with sync_playwright() as p:
    b = p.webkit.launch()
    for m in MONDES:
        ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, 7000, q='?onbLent=4')
        pg.evaluate("m=>{ Toile.setTheme(m); window._vivantOff=true; }", m); pg.wait_for_timeout(9000)
        ouvre_nature(pg, 'promi'); remplit(pg, 'promi', 'arroser les tomates')
        pg.evaluate(REC); pg.evaluate(PIEGE); pg.evaluate("()=>{ window.__vue0=Toile.vue(); window.__g0=Toile_graines(); }")
        B.glisse(pg, points(pg, list(range(44, 212, 12))), pas=18, tenue=40)
        for _ in range(120):
            pg.wait_for_timeout(100)
            if pg.evaluate("()=>window.__fini"): break
        pg.wait_for_timeout(1200)
        c = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        d = pg.evaluate("()=>window.__dc")
        V = pg.evaluate("()=>window.__vol"); deux = [v[0] for v in V if v[1] and v[2]]
        juge('A · [%s] une seule dalle à chaque image (%d images, %d avec la dalle qui vole)' % (NOMS.get(m, m), len(V), sum(1 for v in V if v[1])), not deux and any(v[1] for v in V), ('images doubles à', deux[:6]))
        if not d: juge('B · [%s] la dalle arrive' % NOMS.get(m, m), False, 'aucune dalle au collage'); ctx.close(); continue
        r = d['r']; im = Image.open(io.BytesIO(__import__('base64').b64decode(d['u'].split(',')[1]))).convert('RGBA')
        S = 3; W, H = max(1, round(r[2] * S)), max(1, round(r[3] * S)); X, Y = round(r[0] * S), round(r[1] * S); im = im.resize((W, H))
        n = tot = fort = 0
        for j in range(0, H, 2):
            for i in range(0, W, 2):
                q = im.getpixel((i, j))
                if q[3] < 250: continue
                s = c.getpixel((min(c.width - 1, X + i), min(c.height - 1, Y + j))); dd = max(abs(q[k] - s[k]) for k in range(3)); n += 1; fort += dd > 40
        pc = 100 * fort / max(1, n)
        juge('B · [%s] la dalle qui vole, au collage, est la dalle de la Toile vivante : même place, taille, forme, couleur (%.1f %% de pixels écartés de plus de 40)' % (NOMS.get(m, m), pc), pc <= 4.0, ([round(x) for x in r], n))
        pl = Image.new('RGB', (W * 2 + 10, H), 'white'); bg = Image.new('RGBA', (W, H), (230, 220, 200, 255)); bg.alpha_composite(im); pl.paste(bg.convert('RGB'), (0, 0)); pl.paste(c.crop((X, Y, X + W, Y + H)), (W + 10, 0)); pl.save('scratchpad/v183/vol-%s.png' % m)
        h = pg.evaluate("()=>window.__hors") or {}
        juge('C · [%s] à l\'atterrissage, hors de la dalle (8 pt), les pixels qui changent entre ce qu\'on voyait et la Toile vivante : %.2f %%' % (NOMS.get(m, m), h.get('pc', 99)), h.get('pc', 99) <= 0.5, h)
        im2 = pg.evaluate("()=>window.__img") or []; vals = [z[1] for z in im2 if isinstance(z[1], (int, float))]
        juge('D · [%s] après l\'atterrissage, hors de la dalle, aucune image ne change plus de 6 %% des pixels d\'un coup (plus grand : %.1f %% sur %d images)' % (NOMS.get(m, m), max(vals or [0]), len(vals)), vals and max(vals) <= 6, im2[:14])
        juge('Z · [%s] aucune erreur de page' % NOMS.get(m, m), not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
        ctx.close()
    b.close()
print('\n%d / %d' % (sum(res), len(res)))
