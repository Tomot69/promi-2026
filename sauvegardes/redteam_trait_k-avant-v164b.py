#!/usr/bin/env python3
"""redteam_trait_k.py — ⚑ v163 (Tom, C-184, récidive) : LE TRAIT RÉGLABLE `?trait=`, LE MOT QUI GARDE SON AIR.

« Ajoute `?trait=<facteur>` (par rapport à la taille d'AVANT v162), défaut 1,15. Grossissent le trait (pointillé et continu), la flèche et sa pointe, et
rien d'autre : les trois pages +, toutes les fiches, le trait validé ou lancé d'un Cercle ; pas l'onboarding. Si la flèche s'approche trop du mot
(« TRACE POUR PLANTER / LANCER / TENIR »), il descend juste assez pour garder l'espace d'avant ; tout ce qui est dessous descend de la même valeur. Rien ne
se recouvre, rien ne sort de l'écran, aux échelles 1 et 0,79, clavier ouvert et fermé. Juge : le rapport de taille mesuré ; l'espace flèche–mot ≥ celui
de v162 ; aucun recouvrement. »

Contre v162 servie à côté (`--ref=zz-v162.html`, × 1,05), pour `?trait=1.10`, `1.15`, `1.20` et SANS paramètre (le défaut, 1,15) :
  A · les épaisseurs et rayons PIÉGÉS au dessin du trait (page + ×3, fiche Promi et Chiche à tenir, Cercle) = ceux de v162 × K / 1,05 (± 0,5 %) ;
  B · l'air entre l'ENCRE du trait et l'encre du mot (lu sur l'image) ≥ celui de v162 (− 0,3 pt), à 430 × 932 et à 330 × 714 (échelle ≈ 0,79) ;
  C · aucun recouvrement NOUVEAU entre deux textes (rectangles du texte, pas des boîtes) et rien hors de l'écran, page + au repos et choix ouvert
      (le mot du titre touché : la saisie), fiche à tenir ;
  D · l'onboarding : le trait identique au pixel à v162.
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
REF = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ref=')), 'zz-v162.html')
KS = [None, '1.3', '1.5', '1.8']   # ⚑ v164 (Tom : « aucune différence entre 1,10, 1,15 et 1,20 ») — des paliers nettement visibles
if any(a.startswith('--k=') for a in sys.argv[1:]): KS = [next(a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--k='))]
FEN = [(430, 932), (330, 714)]
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
PIEGE = """(()=>{ window.__T={}; const C=CanvasRenderingContext2D.prototype, st=C.stroke, ar=C.arc;
  function cle(g){ const c=g.canvas; return c && (c.id||c.className||'?'); }
  C.stroke=function(){ try{ const k=cle(this); if(window.__on && window.__on.indexOf(k)>=0){ (window.__T[k]=window.__T[k]||[]).push(['L', +this.lineWidth.toFixed(4)]); } }catch(_){ } return st.apply(this, arguments); };
  C.arc=function(x,y,r){ try{ const k=cle(this); if(window.__on && window.__on.indexOf(k)>=0){ (window.__T[k]=window.__T[k]||[]).push(['R', +(+r).toFixed(4)]); } }catch(_){ } return ar.apply(this, arguments); };
})();"""
LAB = """(sel)=>{ const e=document.querySelector(sel); if(!e) return null; const s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden') return null;
  const rg=document.createRange(); rg.selectNodeContents(e); const q=[...rg.getClientRects()].filter(r=>r.width>1); if(!q.length) return null;
  return [Math.min(...q.map(r=>r.left)), Math.min(...q.map(r=>r.top)), Math.max(...q.map(r=>r.right)), Math.max(...q.map(r=>r.bottom))]; }"""
TEXTES = """(hote)=>{ const H=document.querySelector(hote), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, out=[];
  if(!H) return null;
  const w=document.createTreeWalker(H, NodeFilter.SHOW_TEXT); let n;
  while((n=w.nextNode())){ const t=n.textContent.trim(); if(!t) continue; const e=n.parentElement; let a=e, vis=true;
    while(a && a!==document.body){ const s=getComputedStyle(a); if(s.display==='none'||s.visibility==='hidden'||+s.opacity<0.05){ vis=false; break; } a=a.parentElement; }
    if(!vis) continue; const rg=document.createRange(); rg.selectNodeContents(n);
    [...rg.getClientRects()].filter(r=>r.width>1&&r.height>1).forEach(r=>out.push({t:t.slice(0,24), c:(e.id||e.className||e.tagName)+'', x0:(r.left-D.left)/k, y0:(r.top-D.top)/k, x1:(r.right-D.left)/k, y1:(r.bottom-D.top)/k})); }
  return out; }"""
def ecart(pg, sel):
    r = pg.evaluate(LAB, sel)
    if not r: return None
    im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); k = im.size[0] / pg.viewport_size['width']
    x0, x1, yt = int(r[0] * k), int(r[2] * k), int(r[1] * k)
    if not (0 <= x0 < im.size[0] and 2 <= yt < im.size[1]): return None   # le mot hors de l'image : rien à lire
    x1 = min(x1, im.size[0]); fond = im.getpixel((x0, yt - 2)); best = None
    for x in range(x0, x1, 2):
        for y in range(yt - 2, max(0, yt - int(90 * k)), -1):
            p = im.getpixel((x, y))
            if sum(abs(a - b) for a, b in zip(p, fond)) > 90:
                d = (yt - y) / k
                if best is None or d < best: best = d
                break
    D = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return r.width/390}")
    return round(best / D, 2) if best is not None else None
def recouvre(L):
    """les paires de rectangles de texte qui se recouvrent de plus de 0,6 pt dans les deux sens (deux morceaux d'un même nœud exceptés)"""
    out = set()
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            a, b = L[i], L[j]
            if a['c'] == b['c'] and a['t'] == b['t']: continue
            if min(a['x1'], b['x1']) - max(a['x0'], b['x0']) > 0.6 and min(a['y1'], b['y1']) - max(a['y0'], b['y0']) > 0.6:
                out.add(tuple(sorted((a['t'], b['t']))))
    return out
def hors(L):
    return sorted(set(e['t'] for e in L if e['x0'] < -0.5 or e['x1'] > 390.5 or e['y0'] < -0.5 or e['y1'] > 844.5))
def scene(b, fichier, q, vw, vh, quoi):
    ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 5); ctx.add_init_script(PIEGE); pg = B.ouvre(ctx, fichier, q=q)
    if quoi.startswith('plus-'):
        nat = quoi[5:].split(':')[0]
        pg.evaluate("()=>{ window.__on=['csTrameCv','planterCv','csTrait','ppTrait']; window.__T={}; }")
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
        if quoi.endswith(':ouvert'):
            B.tap_sel(pg, '#csPhrase .ph-m, #nueePhrase .ph-m'); pg.wait_for_timeout(1400)
        hote, lab = '#createSheet', '#createSheet .pp-trace'
    else:
        if quoi == 'fiche-cercle':
            pg.evaluate("()=>{ window.__on=['dpTrameCv']; window.__T={}; window.openNueeDetail('famille'); }")
        else:
            pg.evaluate("c=>{ window.__on=['dpTrameCv']; window.__T={}; const L=promises.filter(p=>!p.draft && p.status!=='tenu' && (!!p.chiche)===c); if(L.length) openDetail(L[0].id); }", quoi == 'fiche-chiche')
        pg.wait_for_timeout(2600); hote, lab = '#detailPoster', '#dptTrace'
    T = pg.evaluate("()=>window.__T"); L = []; [L.extend(v) for v in T.values()]
    e = ecart(pg, lab); tx = pg.evaluate(TEXTES, hote) or []
    ctx.close(); return sorted(set(tuple(x) for x in L if x[1] > 0)), e, tx
def trait_onb(b, fichier, q):
    ctx = B.contexte(b, onb=False, guide=False); pg = B.ouvre(ctx, fichier, q=q, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200)
    B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(500); pg.keyboard.type('marcher une heure', delay=15); pg.evaluate("()=>document.getElementById('onbIn').blur()"); pg.wait_for_timeout(2500)
    d = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); const g=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let h=2166136261; for(let i=0;i<g.length;i+=1){ h^=g[i]; h=Math.imul(h,16777619)>>>0; } return [c.width,c.height,h]; }")
    ctx.close(); return d
SCENES = ['plus-promi', 'plus-chiche', 'plus-nuee', 'plus-promi:ouvert', 'fiche-promi', 'fiche-chiche', 'fiche-cercle']
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in FEN:
        refs = {s: scene(b, REF, '', vw, vh, s) for s in SCENES}
        for K in KS:
            q = '' if K is None else '?trait=' + K; kf = 1.15 if K is None else float(K); nom = 'défaut' if K is None else K
            for s in SCENES:
                va, ea, ta = refs[s]; vn, en, tn = scene(b, F, q, vw, vh, s)
                if vw == FEN[0][0] and not s.endswith(':ouvert'):
                    # ⚑ v164 : les POINTS (les arcs, R) ne grossissent plus — ils restent à × 1,15 (Tom : « déjà limite un poil trop gros ») ; le plein, le
                    #   ruban, la pointe et la flèche (les épaisseurs, L) suivent K. Original : sauvegardes/redteam_trait_k-avant-v164.py
                    att = sorted(set((t, round(v * (kf if t == 'L' else 1.15) / 1.05, 4)) for t, v in va))
                    ok = bool(va) and len(vn) == len(att) and all(x[0] == y[0] and abs(x[1] - y[1]) <= 0.005 * x[1] for x, y in zip(att, vn))
                    juge('[%s %s] A · épaisseurs du trait = v162 × %.3f, les points à × 1,15 fixes' % (nom, s, kf / 1.05), ok, 'v162 %s · ici %s' % (va, vn))
                if s != 'fiche-cercle':
                    juge('[%s %s %d×%d] B · air trait → mot ≥ v162' % (nom, s, vw, vh), ea is not None and en is not None and en >= ea - 0.3, 'v162 %s · ici %s pt' % (ea, en))
                nv = recouvre(tn) - recouvre(ta); hn = sorted(set(hors(tn)) - set(hors(ta)))
                juge('[%s %s %d×%d] C · aucun recouvrement neuf, rien hors de l\'écran' % (nom, s, vw, vh), not nv and not hn, 'recouvre %s · hors %s' % (sorted(nv), hn))
    oa = trait_onb(b, REF, ''); on = trait_onb(b, F, '')
    juge('D · l\'onboarding : le trait identique au pixel à v162 (défaut)', oa == on, 'v162 %s · ici %s' % (oa, on))
    on2 = trait_onb(b, F, '?trait=1.8')
    juge('D · l\'onboarding : identique aussi sous ?trait=1.8', oa == on2, 'v162 %s · ici %s' % (oa, on2))
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
