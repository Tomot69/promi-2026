#!/usr/bin/env python3
"""redteam_achat_net.py — ⚑ v158 (Tom, C-170 RÉCIDIVE) : « GARDER TON ACHAT » — PLUS AUCUN FLOU.

« Après l'achat, sur l'encart “Garder ton achat — il est sur ce téléphone…”, Tom voit ENCORE la Toile floutée en fond. À ce stade le design est débloqué :
la Toile se voit NETTE, partout sur cet écran, derrière l'encart comme à travers lui. Aucun flou, aucun voile, sur aucune couche. Les étapes d'avant l'achat
gardent leur flou en flaques. Refais le vrai chemin : Studio → monde payant → acheter SANS compte → “Garder ton achat”. Juge : sur toute la surface de
l'écran, encart compris, aucun pixel flouté, mesuré par la netteté locale comparée au Studio net ; il doit rougir sur v157. »

Banc comme Tom (WebKit, la fenêtre de Safari : 390 × 692, l'appareil réduit à ≈ 0,79, ×3, doigt, Toile de 25 paroles, AUCUN compte), deux mondes payants :
  A · image par image, du moment où le second encart est demandé à 2,5 s après : aucune couche floutée à l'écran — ni le fond du premier encart
      (`#achatFond`), ni un passage en flaques qui porte une image floutée, ni un élément à filtre ou à flou d'arrière-plan, ni voile sur l'hôte ;
  B · l'image dont l'encart naît (« à travers lui ») est aussi nette que le Studio (netteté ≥ 0,9 × celle du Studio à cet instant) ;
  C · la netteté locale de tout l'écran hors du panneau (72 carreaux) à 0,3 s, 1 s et 2,5 s : aucun carreau sous 0,6 × le même carreau du Studio net
      (l'écran repris l'encart parti, la Toile figée entre les deux) ;
  D · LA SITUATION OÙ LE SECOND ENCART REPRENAIT LE FLOU, posée exprès : le point que v157 sondait (40 % de la hauteur) couvert par une couche transparente
      pendant l'achat — A, B, C doivent tenir quand même ;
  E · les étapes d'avant l'achat gardent leur flou en flaques : le premier encart pose bien son fond flouté.
Preuve : `--fichier=zz-av157.html` rougit (D).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter, ImageStat
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
ESPION = """()=>{ window.__F=[]; window.__IM=[]; const t0=performance.now(); window.__t0=t0;
  const pf=window._passageFlaques; window._passageFlaques=function(h,o){ const r=pf.apply(this,arguments); try{ if(window.__deux && o && o.image){ const c=o.image, w=c.width, hh=c.height, d=c.getContext('2d').getImageData(0,0,w,hh).data; let s=0,n=0; for(let y=4;y<hh-4;y+=3) for(let x=4;x<w-4;x+=3){ const i=(y*w+x)*4, j=(y*w+x+2)*4, l=((y+2)*w+x)*4; s+=Math.abs(d[i]-d[j])+Math.abs(d[i]-d[l]); n++; } window.__IM.push(s/n); } }catch(e){} return r; };
  const oc=window._onbCompte; window._onbCompte=function(h,a,o){ if(o && /Garder/.test(o.lab||'')){ window.__deux=performance.now(); const bg=document.getElementById('stBg'); try{ const c=document.createElement('canvas'); c.width=390; c.height=844; c.getContext('2d').drawImage(bg,0,0,390,844); const d=c.getContext('2d').getImageData(0,0,390,844).data; let s=0,n=0; for(let y=4;y<840;y+=3) for(let x=4;x<386;x+=3){ const i=(y*390+x)*4, j=(y*390+x+2)*4, l=((y+2)*390+x)*4; s+=Math.abs(d[i]-d[j])+Math.abs(d[i]-d[l]); n++; } window.__studioNet=s/n; }catch(e){} } return oc.apply(this,arguments); };
  (function f(){ if(window.__deux && performance.now()-window.__deux<2500){ const D=document.getElementById('device').getBoundingClientRect(); const fl=[];
      document.querySelectorAll('#achatFond, canvas.passage-flaques').forEach(c=>{ const r=c.getBoundingClientRect(); if(!c.isConnected||r.width<2||r.bottom<D.top||r.top>D.bottom) return; if(c.id==='achatFond'||c.hasAttribute('data-flou')) fl.push(c.id||'passage flouté'); });
      document.querySelectorAll('#device *').forEach(e=>{ const s=getComputedStyle(e); const bf=s.backdropFilter||s.webkitBackdropFilter; if((bf&&bf!=='none')||(s.filter&&/blur/.test(s.filter))){ const r=e.getBoundingClientRect(); let vu=r.width>2&&r.height>2&&r.right>D.left&&r.left<D.right&&r.bottom>D.top&&r.top<D.bottom; for(let q=e;vu&&q&&q.nodeType===1;q=q.parentElement){ const z=getComputedStyle(q); if(z.display==='none'||z.visibility==='hidden'||+z.opacity<0.02) vu=false; } if(vu) fl.push((e.id||e.className||e.tagName).toString().slice(0,30)+' '+(bf!=='none'?bf:s.filter)); } });
      const h=document.getElementById('accRappelCompte'); if(h){ const v=getComputedStyle(h).backgroundColor; if(v!=='rgba(0, 0, 0, 0)' && v!=='transparent') fl.push('voile '+v); }
      window.__F.push([Math.round(performance.now()-window.__deux), fl.join(' ; ')]); }
    if(performance.now()-t0<20000) requestAnimationFrame(f); })(); }"""
def aretes(png):
    return Image.open(io.BytesIO(png)).convert('L').filter(ImageFilter.FIND_EDGES)
def passe(b, saut, sonde):
    ctx = b.new_context(viewport={'width': 390, 'height': 692}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{if(!sessionStorage.getItem('__amorce')){sessionStorage.setItem('__amorce','1');localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','light');}}catch(e){}")
    B.toile_pleine(ctx, 25); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} closeAll(); }"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{ document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    vus = 0
    for i in range(30):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"):
            if vus >= saut: break
            vus += 1
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500)
    w = pg.evaluate("()=>window._lockedWorld"); T = '%s%s' % (w, ' · sonde' if sonde else '')
    pg.evaluate(ESPION)
    c = pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(2000)
    prem = pg.evaluate("()=>!!document.getElementById('achatFond')")
    if sonde:   # le point que v157 sondait (40 % de la hauteur de l'appareil), couvert par une couche transparente qui n'est pas le Studio
        pg.evaluate("()=>{ const d=document.createElement('div'); d.id='__sondeD'; d.style.cssText='position:absolute;left:150px;top:300px;width:90px;height:90px;z-index:200;background:transparent'; document.getElementById('device').appendChild(d); }")
    t = pg.evaluate("()=>{ const e=document.querySelector('#accRappelCompte .tard'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
    pg.touchscreen.tap(t[0], t[1])
    for _ in range(80):
        pg.wait_for_timeout(100)
        if pg.evaluate("()=>{ const h=document.getElementById('accRappelCompte'); return !!(h&&h.classList.contains('vu')&&h.textContent.indexOf('Garder')>=0); }"): break
    D = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
    shots = []
    for ms in (300, 700, 1500):
        pg.wait_for_timeout(ms); shots.append(pg.screenshot(clip=D))
    pr = pg.evaluate("()=>{ const p=document.querySelector('#accRappelCompte .onbv-compte'), D=document.getElementById('device').getBoundingClientRect(); return p?(p.getBoundingClientRect().top-D.top)/(D.width/390):844; }")
    Fr = pg.evaluate("()=>window.__F"); IM = pg.evaluate("()=>[window.__IM, window.__studioNet]")
    # le Studio net de référence : l'encart retiré, la Toile figée
    pg.evaluate("()=>{ window.__raf=window.requestAnimationFrame; window.requestAnimationFrame=function(){return 0;}; const h=document.getElementById('accRappelCompte'); if(h) h.style.setProperty('display','none','important'); const s=document.getElementById('__sondeD'); if(s) s.remove(); const t=document.getElementById('_toast'); if(t) t.remove(); }")
    pg.wait_for_timeout(300); ref = aretes(pg.screenshot(clip=D))
    pg.evaluate("()=>{ window.requestAnimationFrame=window.__raf; }")
    floues = [f for f in Fr if f[1]]
    juge('[%s] A · image par image, aucune couche floutée ni voile pendant le second encart (%d images)' % (T, len(Fr)), Fr and not floues, floues[:3])
    nets = IM[0]; sn = IM[1] or 1
    juge('[%s] B · l\'image dont l\'encart naît est aussi nette que le Studio' % T, nets and min(nets) >= 0.9 * sn, 'netteté de l\'entrée %s · Studio %.1f' % ([round(x, 1) for x in nets], sn))
    W, H = ref.size; s = W / 390.0; bas = int(min(pr - 8, 844) * s); pire = 9
    for png in shots:
        e = aretes(png)
        for gx in range(6):
            for gy in range(12):
                x0, y0 = int(gx * W / 6), int(gy * bas / 12); x1, y1 = int((gx + 1) * W / 6), int((gy + 1) * bas / 12)
                if y1 - y0 < 10: continue
                rm = ImageStat.Stat(ref.crop((x0, y0, x1, y1))).mean[0]
                if rm < 6: continue
                pire = min(pire, ImageStat.Stat(e.crop((x0, y0, x1, y1))).mean[0] / rm)
    juge('[%s] C · la netteté locale de tout l\'écran hors du panneau, à 0,3, 1 et 2,5 s : aucun carreau sous 0,6 × le Studio net' % T, pire >= 0.6, 'le carreau le plus flou : %.2f × le Studio net' % pire)
    juge('[%s] E · avant l\'achat, le premier encart pose bien son flou en flaques' % T, prem, '#achatFond %s' % prem)
    er = [x for x in pg.erreurs if 'version.json' not in x]; juge('[%s] aucune erreur de page' % T, not er, er[:2]); ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for saut, sonde in ((0, False), (1, False), (0, True)):
        passe(b, saut, sonde)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
