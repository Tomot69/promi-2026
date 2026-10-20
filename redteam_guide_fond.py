#!/usr/bin/env python3
"""redteam_guide_fond.py — ⚑ v154 (Tom, C-166) : APRÈS LE STUDIO, LE FOND DU GUIDE MONTRE LE NOUVEAU MONDE.

« Sur la première phrase du guide, la dalle bleue est en fond sous le flou. Tom va au Studio et change le monde et la couleur. Au retour, la phrase du +
paraît sur le flou, mais le fond montre encore l'ANCIEN monde. Au retour du Studio, le fond flouté est recalculé à partir de la Toile réelle ; si rien n'a
changé, le fond reste identique. Aucune saccade : prépare-le pendant la fermeture du Studio. Juge : changer le monde et la palette, fermer le Studio ; le
fond flouté correspond à la Toile réelle. Sans changement : fond identique au pixel. »

Banc comme Tom (WebKit, 390 × 844, échelle 3), le vrai premier guide, clair et sombre :
  A · Studio touché (sa zone nette), refermé SANS changement : l'étape du + ; le fond flouté est le MÊME au pixel (aucun recalcul)
  B · (autre lancement) Studio touché ; le monde changé au doigt (glissé) et la palette (une pastille) ; refermé : l'étape du + ; le fond flouté est
      celui de la Toile RÉELLE d'après le Studio (l'accueil repris et flouté à 4,8 maintenant, comparé au pixel, ± 2 niveaux) ; il diffère de l'ancien ;
      il était posé AVANT que le Studio se referme (sous lui)
  C · la fermeture du Studio, image par image : aucune image au-delà de 50 ms — une cadence : jugée sous une charge de 4 seulement (C-137)
Preuve : `--fichier=zz-av153.html` rougit (B).
"""
import sys, json, hashlib, base64; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-110s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
ETAT = "()=>{ const g=document.getElementById('guide'); return {guide:g?g.getAttribute('data-guide'):null, entier:!!(g&&g.getAttribute('data-entier')), e:(window._guide?window._guide.etat():null), sig:g?g.getAttribute('data-flou-sig'):null, refait:g?(+g.getAttribute('data-flou-refait')||0):0, monde:(window.Toile&&Toile.mondeCourant)?JSON.stringify(Toile.mondeCourant()):null}; }"
EMPREINTE = "()=>{ const g=document.getElementById('guide'); const f=g&&g.__flou; if(!f) return null; const d=f.getContext('2d').getImageData(0,0,f.width,f.height).data; let h=0; for(let i=0;i<d.length;i+=7) h=(h*31+d[i])>>>0; return h; }"
COMPARE = """async ()=>{ const g=document.getElementById('guide'); const f=g&&g.__flou; if(!f||!window._guide) return null; const net=await _guide.image(); const fr=Flaques.floute(net, 4.8);
  const a=f.getContext('2d').getImageData(0,0,f.width,f.height).data, b=fr.getContext('2d').getImageData(0,0,fr.width,fr.height).data; if(a.length!==b.length) return {taille:false};
  let max=0, n=0; for(let i=0;i<a.length;i++){ const e=Math.abs(a[i]-b[i]); if(e>max) max=e; if(e>6) n++; } return {max:max, hors:n, part:n/a.length, taille:true}; }"""
DIFF_AV = "(h)=>{ return null; }"
def attend(pg, quoi, ms=15000):
    for _ in range(ms // 120):
        e = pg.evaluate(ETAT)
        if e['guide'] == quoi and e['entier']: return e
        pg.wait_for_timeout(120)
    return pg.evaluate(ETAT)
def toucher(cdp, pg, x, y): B.tap(pg, x, y, appareil=False)
def pt(pg, x, y):
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width];}"); k = d[2] / 390.0; return d[0] + x * k, d[1] + y * k
def centre(pg, sel): return pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
def passe(b, sombre, change):
    T = 'sombre' if sombre else 'clair'
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True)
    ctx.add_init_script("try{ localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); }catch(e){}" % ('dark' if sombre else 'light'))
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{ if(window._guide) _guide.attend(false); }"); cdp = None
    e = attend(pg, 'studio', 20000)
    if e['guide'] != 'studio': juge('[%s] le guide paraît à l\'étape du Studio' % T, False, e); ctx.close(); return
    pg.wait_for_timeout(600); e = pg.evaluate(ETAT)
    h0 = pg.evaluate(EMPREINTE); s0 = e['sig']; m0 = e['monde']; pg.evaluate("()=>{ window.__flouAv=document.getElementById('guide').__flou; }")
    x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2600)
    ok = pg.evaluate("()=>{ const s=document.getElementById('studioScreen'), D=document.getElementById('device').getBoundingClientRect(), h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.6); return !!(s&&h&&s.contains(h)); }")
    if change:
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1800)
        c = centre(pg, '#studioScreen .stp-ton')   # un ton du panneau : les palettes se déplient
        if c: toucher(cdp, pg, c[0], c[1])
        pg.wait_for_timeout(900)
        c = pg.evaluate("()=>{ const P=[...document.querySelectorAll('#stpPals .st3-p')].filter(b=>!b.classList.contains('on') && b.getBoundingClientRect().width>4); const b=P[Math.min(5,P.length-1)]; if(!b) return null; const r=b.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
        if c: toucher(cdp, pg, c[0], c[1])
        pg.wait_for_timeout(2400)
    avant = pg.evaluate(ETAT)
    pg.evaluate("()=>{ window.__img=[]; let p=performance.now(); (function f(t){ window.__img.push(t-p); p=t; if(window.__img.length<200) requestAnimationFrame(f); })(performance.now()); }")
    c = centre(pg, '#studioScreen .closeb')
    if c: toucher(cdp, pg, c[0], c[1])
    e2 = attend(pg, 'plus', 15000); pg.wait_for_timeout(400); e2 = pg.evaluate(ETAT)
    h1 = pg.evaluate(EMPREINTE); imgs = pg.evaluate("()=>window.__img||[]")
    if not change:
        juge('[%s] A · Studio ouvert puis refermé SANS changement : l\'étape du + ; le fond flouté est le même au pixel, aucun recalcul' % T,
             ok and e2['guide'] == 'plus' and h1 == h0 and e2['refait'] == 0 and e2['monde'] == m0, 'Studio %s · étape %s · empreinte %s → %s · recalculs %d' % (ok, e2['guide'], h0, h1, e2['refait']))
    else:
        cmp = pg.evaluate(COMPARE); cmpAv = pg.evaluate(COMPARE.replace("const f=g&&g.__flou;", "const f=window.__flouAv;"))
        juge('[%s] B · monde et palette changés au Studio, refermé : l\'étape du + ; le fond flouté est celui de la Toile RÉELLE (≤ 0,2 %% des valeurs à plus de 6 niveaux ; l\'ancien fond : 50 fois plus), il a changé' % T,
             ok and e2['guide'] == 'plus' and json.loads(e2['monde'])['m'] != json.loads(m0)['m'] and json.loads(e2['monde'])['p'] != json.loads(m0)['p'] and cmp and cmp.get('taille') and cmp['part'] <= 0.002 and cmp['part'] < cmpAv['part'] / 50 and h1 != h0,
             'monde %s → %s · comparé à l\'accueil flouté maintenant : %s · l\'ancien fond : %s' % (m0, e2['monde'], cmp, cmpAv))
        juge('[%s] B · le fond neuf était posé SOUS le Studio, avant sa fermeture' % T, avant['refait'] >= 1 and avant['sig'] == e2['sig'], 'recalculs avant la fermeture : %d · signature %s' % (avant['refait'], avant['sig']))
        lent = [round(x) for x in imgs[1:60] if x > 50]; calme = B.charge() < 4
        juge('[%s] C · la fermeture du Studio, image par image : aucune image au-delà de 50 ms%s' % (T, '' if calme else ' — NON JUGÉ (charge ≥ 4)'), (not calme) or not lent, 'images > 50 ms : %s ; charge %.1f' % (lent, B.charge()))
    juge('[%s] aucune erreur de page' % T, not [x for x in er if 'version.json' not in x], er[:2]); ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        passe(b, sombre, False); passe(b, sombre, True)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
