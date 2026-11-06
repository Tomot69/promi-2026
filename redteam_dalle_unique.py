#!/usr/bin/env python3
"""redteam_dalle_unique.py — ⚑ v181a (Tom, 6 nov. 2026, C-241) : « la dalle du fond, en haut de la page +, doit être EXACTEMENT la même que celle qui naît
à la moitié du trait, qui est elle-même la même que celle qui arrive sur la Toile : même monde, même palette, même couleur, même forme. Juge : les trois
rendus sont identiques (forme et couleurs), dans 3 mondes différents. »

Banc WebKit ×3, Toile de dix paroles, page + d'un Promi au doigt, la moitié du trait tracée ; trois rendus lus sur leurs canevas : le HAUT de la page +
(celui que pose `_poseDalle` sur #csTrameCv), la dalle qui NAÎT (.onbv-dalle, sa première image), la dalle sur la TOILE une fois posée (`dalleTrame`).
Couleur : la moyenne de ses pixels opaques, ΔE CIELAB ≤ 5. Forme : le masque d'opacité ramené à 48 × 48, recouvrement (IoU) ≥ 0,9.
Mondes : Pochade (encre), Touffe (anciens, semis constant), Esquille (neuf, la Toile grandit).
⚠ v181a : NAÎT = TOILE en couleur partout ; en forme dans les anciens mondes ; le HAUT reste une autre parole (rouge, voir CHANTIERS C-241).
"""
import sys, json, io, base64; sys.path.insert(0,'.')
import banc_tom as B
from PIL import Image
from playwright.sync_api import sync_playwright
exec(open('redteam_moitie.py').read().split('REF = None')[0].split('from playwright.sync_api import sync_playwright')[1])
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
PIEGE = """()=>{ if(window.__pp) return; window.__pp=[]; const u=window._poseUn; window._poseUn=function(g,cv,x,y){ const r=u.apply(this,arguments); try{ if(g.canvas&&g.canvas.id==='csTrameCv'&&g.canvas.getAttribute('data-avenir')!=null||(g.canvas&&g.canvas.id==='csTrameCv'&&cv&&cv.width>40)) window.__pp.push({id:'avenir', o:null, cv:cv.toDataURL(), info:null}); }catch(e){} return r; }; const f=window._poseDalle; window._poseDalle=function(g,id,x,y,w,h,o){ const r=f.apply(this,arguments); try{ if(g.canvas&&g.canvas.id==='csTrameCv') window.__pp.push({id:id, o:o?JSON.stringify(o).slice(0,80):null, cv:r&&r.cv?r.cv.toDataURL():null, info:r&&r.cv&&r.cv.__dalleInfo?{c:r.cv.__dalleInfo.c||r.cv.__dalleInfo.sat, lum:r.cv.__dalleInfo.lum, monde:r.cv.__dalleInfo.monde}:null}); }catch(e){} return r; }; }"""
NAIT = """()=>{ const e=document.querySelector('.onbv-dalle'); if(e && !window.__nait) window.__nait=e.toDataURL(); requestAnimationFrame(()=>{}); return !!e; }"""
def img(u): return Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
def masque(im, n=48):
    im=im.resize((n,n)); return [im.getpixel((x,y))[3]>128 for y in range(n) for x in range(n)]
def iou(a,b): i=sum(1 for x,y in zip(a,b) if x and y); u=sum(1 for x,y in zip(a,b) if x or y); return round(i/max(1,u),3)
def lab(c):
    def f(u):
        u/=255; return ((u+.055)/1.055)**2.4 if u>.04045 else u/12.92
    r,g,b=[f(x) for x in c]; X=(r*.4124+g*.3576+b*.1805)/.95047; Y=r*.2126+g*.7152+b*.0722; Z=(r*.0193+g*.1192+b*.9505)/1.08883
    h=lambda t: t**(1/3) if t>.008856 else 7.787*t+16/116
    return (116*h(Y)-16, 500*(h(X)-h(Y)), 200*(h(Y)-h(Z)))
def de(a,b): A,B=lab(a),lab(b); return round(sum((x-y)**2 for x,y in zip(A,B))**.5,1)
def moy(im):
    px=[p for p in im.getdata() if p[3]>200]; return tuple(round(sum(p[i] for p in px)/max(1,len(px))) for i in range(3))
with sync_playwright() as p:
    b=p.webkit.launch()
    res=[]
    def juge(nom, ok, d=''):
        res.append(bool(ok)); print('  %s %-80s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
    for monde in ('encre','touffe','esquille'):
        ctx=B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 10); pg=B.ouvre(ctx, F, 7000)
        pg.evaluate("m=>{ Toile.setTheme(m); }", monde); pg.wait_for_timeout(9000)   # la Toile posée dans son monde (un changement de famille la ressème)
        pg.evaluate(PIEGE); ouvre_nature(pg,'promi'); remplit(pg,'promi','arroser les tomates')
        haut = pg.evaluate("()=>window.__pp.slice(-1)[0]")
        pg.evaluate("()=>{ window.__nait=null; (function f(){ const e=document.querySelector('.onbv-dalle'); if(e&&!window.__nait&&e.width) window.__nait=e.toDataURL(); if(!window.__nait) requestAnimationFrame(f); })(); }")
        B.glisse(pg, points(pg, list(range(44,212,12))), pas=18, tenue=40); pg.wait_for_timeout(3500)
        np_ = pg.evaluate("()=>{ const q=promises[promises.length-1]; return {id:q.id, monde:q.monde, dalle:q.dalle}; }")
        fin = pg.evaluate("id=>{ const c=document.createElement('canvas'); Toile.dalleTrame(c,id,1); return c.toDataURL(); }", np_['id'])
        nait = pg.evaluate("()=>window.__nait")
        H, N, T = img(haut['cv']), img(nait), img(fin)
        print(monde, '· haut id', haut['id'], 'opts', haut['o'], '| nouvelle', np_)
        print('   couleur moyenne  haut', moy(H), ' naît', moy(N), ' Toile', moy(T))
        print('   forme (IoU)  haut/naît', iou(masque(H),masque(N)), ' naît/Toile', iou(masque(N),masque(T)), ' haut/Toile', iou(masque(H),masque(T)), ' tailles', H.size, N.size, T.size)
        juge('[%s] naît = Toile : couleur (ΔE ≤ 5)' % monde, de(moy(N), moy(T)) <= 5, (moy(N), moy(T)))
        juge('[%s] naît = Toile : forme (IoU ≥ 0,9)' % monde, iou(masque(N), masque(T)) >= .9, iou(masque(N), masque(T)))
        juge('[%s] haut = naît : couleur (ΔE ≤ 5)' % monde, de(moy(H), moy(N)) <= 5, (moy(H), moy(N), 'haut : parole', haut['id'], 'nouvelle', np_['id']))
        juge('[%s] haut = naît : forme (IoU ≥ 0,9)' % monde, iou(masque(H), masque(N)) >= .9, iou(masque(H), masque(N)))
        pl=Image.new('RGBA',(600,200),(235,225,200,255))
        for i,im in enumerate((H,N,T)):
            t=im.copy(); t.thumbnail((190,190)); pl.alpha_composite(t,(i*200+5,5))
        pl.save('scratchpad/v181/c241-%s.png'%monde)   # haut · naît · Toile, côte à côte
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
