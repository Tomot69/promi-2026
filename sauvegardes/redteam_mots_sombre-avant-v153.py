#!/usr/bin/env python3
"""redteam_mots_sombre.py — ⚑ v152 (Tom, C-162) : ONBOARDING ET GUIDE EN SOMBRE, LES MOTS-CLÉS EN COULEUR.

« En sombre, les mots-clés sont blancs comme le reste du texte. Exemple : « … tout COMMENCE par ce + » : en clair, « COMMENCE » est en couleur ; en
sombre, il est blanc. Règle : TOUT mot coloré en clair est coloré aussi en sombre, dans l'onboarding comme dans les phrases du guide. Même rôle, même
famille de couleur. En sombre, chaque couleur prend sa variante claire de la palette, au moins 3:1 sur le fond sombre : bleu → #82AEF8, rose → #FFB8D2,
lilas → #C9A8F5. Les lettres multicolores de « Studio » prennent leurs équivalents clairs. Juge : pour chaque mot coloré en clair, il est coloré en
sombre, à au moins 3:1. »

Banc comme Tom (WebKit, 390 × 844, échelle 3, doigt). L'inventaire est relevé, pas écrit : le vrai parcours de l'onboarding (prénom, parole, trait,
« Promi planté ! » et ses trois touchers) et les deux phrases du guide (Studio, +), dans les deux thèmes ; chaque nœud de texte visible et sa couleur.
  · « coloré en clair » = une autre couleur que l'encre de la page (#291547, #201908) ; les pastilles (le prénom, « Je me promets », la parole, la
    flèche) ne sont pas des mots colorés : leur texte est l'encre inversée sur la pastille.
  · « coloré en sombre » = une autre couleur que la crème #F7F0DE et que la seiche ; contraste ≥ 3:1 sur le fond RÉEL, lu sur l'image autour du mot.
  · en sombre, les natures du guide en dur : Promi #82AEF8, Chiche #FFB8D2, Cercle #C9A8F5 ; « commence » #82AEF8 (la décision de Tom).
  · EXCEPTIONS NOMMÉES, et elles seules : « trace pour planter » crème en sombre (Tom, v151 C-126 §5) ; « La suite t'appartient. » crème en sombre
    (Q548, chef de chantier, v152).
Preuve : `--fichier=zz-av151.html` rougit (la phrase du + du guide : Promi, Chiche, Cercle, commence en crème).
"""
import io, sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
from collections import Counter
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ENCRE_CLAIR = {(41, 21, 71), (32, 25, 8)}
CREME, SEICHE = (247, 240, 222), (5, 3, 2)
PASTILLE = ('onbv-pm', 'onbv-pb', 'onbv-suite')
EXCEPTIONS = {'trace pour planter': 'Tom, v151 C-126 §5', 'La suite t’appartient.': 'Q548, v152'}
EN_DUR = {('guide-plus', 'Promi'): (130, 174, 248), ('guide-plus', 'Chiche'): (255, 184, 210), ('guide-plus', 'Cercle'): (201, 168, 245), ('guide-plus', 'commence'): (130, 174, 248)}
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
def rgb(s):
    import re; m = re.findall(r'[\d.]+', s or ''); return tuple(int(float(x)) for x in m[:3]) if len(m) >= 3 else None
def lum(c):
    f = lambda x: x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0] / 255) + 0.7152 * f(c[1] / 255) + 0.0722 * f(c[2] / 255)
def ratio(a, b): la, lb = lum(a), lum(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
COL = """(root)=>{ const R=document.querySelector(root); if(!R) return []; const out=[]; const w=document.createTreeWalker(R,NodeFilter.SHOW_TEXT);
  while(w.nextNode()){ const n=w.currentNode; const t=n.nodeValue.trim(); if(!t) continue; const e=n.parentElement; let v=e,vis=true; while(v&&v!==document.body){ const c=getComputedStyle(v); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05){vis=false;break;} v=v.parentElement; }
    if(!vis) continue; const c=getComputedStyle(e); const rg=document.createRange(); rg.selectNodeContents(n); const r=rg.getBoundingClientRect();
    out.push([t, c.webkitTextFillColor||c.color, (e.className&&e.className.baseVal===undefined?e.className:e.tagName)+'', [r.left,r.top,r.width,r.height]]); }
  return out; }"""
def fond(pg, b, m=5):
    if b[2] < 1: return None
    im = Image.open(io.BytesIO(pg.screenshot(clip={'x': max(0, b[0] - m), 'y': max(0, b[1] - m), 'width': b[2] + 2 * m, 'height': b[3] + 2 * m}, scale='css'))).convert('RGB')
    C = Counter(); W, H = im.size
    for x in range(W):
        for y in (0, 1, H - 2, H - 1): C[im.getpixel((x, y))] += 1
    for y in range(H):
        for x in (0, 1, W - 2, W - 1): C[im.getpixel((x, y))] += 1
    return C.most_common(1)[0][0]
def onboarding(pg):
    pages = {}
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300)
    pages['prénom'] = pg.evaluate(COL, '#onbV')
    pg.keyboard.press('Enter'); pg.wait_for_timeout(5000); pages['parole'] = pg.evaluate(COL, '#onbV')
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000); pages['trait'] = pg.evaluate(COL, '#onbV')
    z = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {l:(r.left-D.left)/k, t:(r.top-D.top)/k, k:r.width/390/k, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee')}; }")
    if z and z['dep']:
        a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
        x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
        B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
        pg.wait_for_timeout(5600)
        for _ in range(3): B.tap(pg, 195, 300); pg.wait_for_timeout(4000)
        pages['fin'] = pg.evaluate(COL, '#onbV')
    return pages
def guide(pg, et):
    pg.evaluate("e=>_guide.montre(e,true)", et)
    for _ in range(10):
        pg.wait_for_timeout(1000)
        if pg.evaluate("()=>!!document.getElementById('guidePhrase')"): break
    pg.wait_for_timeout(3500); return pg.evaluate(COL, '#guidePhrase')
REL = {}; FONDS = {}
with sync_playwright() as p:
    b = p.webkit.launch(); err = []
    for th in ('clair', 'sombre'):
        ctx = B.contexte(b, sombre=(th == 'sombre'), onb=False, guide=False); pg = B.ouvre(ctx, F, attente=7000)
        REL[th] = onboarding(pg)
        if th == 'sombre':
            for k, L in REL[th].items():
                if k == 'fin': FONDS[k] = [fond(pg, x[3]) for x in L]
        err += pg.erreurs; ctx.close()
        if th == 'sombre':   # les fonds des pages d'avant « Promi planté ! » : relus sur un second passage, page par page
            pass
        for et in ('studio', 'plus'):
            ctx = B.contexte(b, sombre=(th == 'sombre')); pg = B.ouvre(ctx, F, attente=6500)
            REL[th]['guide-' + et] = L = guide(pg, et)
            if th == 'sombre': FONDS['guide-' + et] = [fond(pg, x[3]) for x in L]
            err += pg.erreurs; ctx.close()
    b.close()
FOND_ONB = (11, 9, 8)   # le fond réel de l'onboarding en sombre (#0B0908, mesuré en v151) — pour les pages lues avant la fin
for page in REL['clair']:
    C, S = REL['clair'][page], REL['sombre'].get(page, [])
    juge('%s · les deux thèmes portent les mêmes mots, dans le même ordre' % page, [x[0] for x in C] == [x[0] for x in S], '%d / %d' % (len(C), len(S)))
    for i, (t, c, k, bx) in enumerate(C):
        c = rgb(c)
        if c in ENCRE_CLAIR or any(x in k.split() for x in PASTILLE): continue
        s = S[i] if i < len(S) and S[i][0] == t else next((x for x in S if x[0] == t), None)
        if not s: juge('%s · « %s » existe en sombre' % (page, t), False); continue
        sc = rgb(s[1]); f = (FONDS.get(page) or [None] * len(S))[S.index(s)] if page in FONDS else FOND_ONB
        if t in EXCEPTIONS:
            juge('%s · « %s » : exception nommée (%s), crème en sombre' % (page, t, EXCEPTIONS[t]), sc == CREME, 'clair %s · sombre %s' % (c, sc)); continue
        r = ratio(sc, f) if f else 0
        att = EN_DUR.get((page, t))
        ok = sc not in (CREME, SEICHE) and r >= 3 and (att is None or sc == att)
        juge('%s · « %s » coloré en clair %s → coloré en sombre%s, ≥ 3:1' % (page, t, c, ' %s (en dur)' % (att,) if att else ''), ok, 'sombre %s · fond %s · %.2f:1' % (sc, f, r))
juge('aucune erreur de page', not [x for x in err if 'version.json' not in x], str(err[:2]))
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
