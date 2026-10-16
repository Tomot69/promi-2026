#!/usr/bin/env python3
"""
redteam_guide.py — LE GUIDE D'ACCUEIL : DES FLAQUES (v146, Tom, 14 oct. 2026 — C-094, 2e RÉCIDIVE). RÉÉCRIT ; l'original de v144 :
sauvegardes/redteam_guide-avant-v146.py (six formes à bord doux qui grandissent, une loupe ronde qui glisse du Studio au +).

POURQUOI LES JUGES D'AVANT ÉTAIENT VERTS : ils mesuraient qu'un masque grandissait, qu'une icône était nette, qu'une loupe glissait sans à-coup.
Aucun ne regardait la NATURE du mouvement. Tom demandait une matière vivante, aléatoire et ciblée ; il a reçu une découpe géométrique, trop
large, qui se déplace. Ce juge-ci lit la FORME de l'eau sur le canevas du guide, image par image.

LA DÉCISION, EN DUR (le brief de Tom, §4) :
  4.1 LA COUVERTURE — des flaques naissent au hasard (plusieurs, séparées), grossissent, se rejoignent, couvrent l'écran ; 1,2 à 1,6 s ;
      ce qui est mouillé le reste (rien ne se déplace) ; la surface monte sans saut (rien n'arrive d'un coup) ; aucune flaque n'est un disque
      ni une ellipse ; le bord est une ligne (ni fondu ni dégradé) ; deux lancements ne donnent pas les mêmes flaques ;
  4.2 LA PHRASE — mot pour mot, sans aucun contour, plus grosse (≥ 34 px) ; mots-clés en PromiLate (« monde », « Studio » ; « commence ») ;
      en clair : texte #291547, mots-clés #0E78F2, natures dans leur couleur ; en sombre : la crème ;
  4.3 LE STUDIO — la zone nette s'ouvre EN FLAQUES (à mi-chemin elle n'est ni vide ni pleine, en plusieurs morceaux ou échancrée) ; sa forme
      finale contient l'icône et son mot, ne montre NI l'Aura NI le contour de la barre, et n'est ni un cercle parfait ni une forme déchiquetée ;
  4.4 elle DISPARAÎT SUR ELLE-MÊME (elle rétrécit sur place : son centre ne bouge pas) ;
  4.5 LE + — pareil, sur le + seul ; entre le Studio et le +, il y a un instant SANS zone nette (aucune translation de l'un à l'autre) ;
  4.6 LA FIN — les flaques se vident (plusieurs morceaux à mi-retrait), puis il ne reste rien.
  Les chemins (inchangés) : le moment (0,6 s de calme) ; le Studio touché s'ouvre par-dessus ; refermé → l'étape du + ; toucher ailleurs fait
  avancer ; toucher le + ouvre les trois natures ; une seule fois ; « Réduire les animations » : tout est posé sans mouvement ; aucun
  « Plus tard » ; A2 (ni opacité ni transition) ; aucune image au-delà de 16,7 ms de travail du fil principal.
Le premier chemin part d'un STOCKAGE VIERGE et joue l'onboarding entier au doigt (CDP, Chromium avec le vrai GPU), à 390 × 844 ×3.
Preuve (§7) : sur la version d'avant (`--fichier=zz-avant-v146.html`) le juge rougit dès 4.1 (il n'y a pas d'eau).
Usage : python3 redteam_guide.py [--fichier=…] [--vite] [--cadence : la cadence seule, trois passes par thème]
"""
import io, os, re, sys, time, json, base64
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
F = 'app.html'
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
VITE = '--vite' in sys.argv
URL = 'http://127.0.0.1:8752/' + F
PH_STUDIO = 'Choisis d’abord le monde qui te ressemble, au Studio.'      # les mots de Tom, en dur
PH_PLUS = 'Promi, Chiche ou Cercle : tout commence par ce +.'
CLES = {'studio': ['monde', 'Studio'], 'plus': ['commence']}                   # §11.7, en dur
ATTENTE, COUVRE, OUVRE, FERME, RETIRE = 600, 1400, 700, 700, 1200             # ms — les durées décidées (couverture 1,2 à 1,6 s ; zone 0,6 à 0,8 s)
VIOLET, BLEU, CREME = (41, 21, 71), (14, 120, 242), (247, 240, 222)           # #291547 · #0E78F2 · #F7F0DE
os.makedirs('planche-v146', exist_ok=True)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('  %s %-118s %s' % ('✅' if cond else '❌', nom, str(detail)[:280]), flush=True)
DEV = "()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}"
ETAT = """()=>{ const g=document.getElementById('guide'), p=document.getElementById('guidePhrase'), t=document.getElementById('guideTard')||document.getElementById('onbTard')||document.querySelector('#onbV .onbv-tard');
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const B=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k].map(v=>Math.round(v*10)/10); };
  const cs=e=>e?getComputedStyle(e):null;
  const tous=[...document.querySelectorAll('#guide, #guide *')].map(e=>{const c=getComputedStyle(e); return {id:e.id, cl:(e.className&&e.className.baseVal===undefined)?e.className:'', eng:e.getAttribute('data-eng'), op:+c.opacity, trp:c.transitionProperty, trd:c.transitionDuration, an:c.animationName, bf:(c.backdropFilter||c.webkitBackdropFilter||'none'), sh:c.textShadow, st:c.webkitTextStrokeWidth};});
  const acc=(()=>{ const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.45); return h?(h.closest('.screen')?'ecran:'+h.closest('.screen').id:(h.closest('#guide')?'guide':(h.closest('.sheet,.poster')?'feuille':'accueil'))):null; })();
  function vu(el){ let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9; el.querySelectorAll('svg, .l').forEach(e=>{ const q=e.getBoundingClientRect(); if(q.width<2) return; x0=Math.min(x0,q.left); y0=Math.min(y0,q.top); x1=Math.max(x1,q.right); y1=Math.max(y1,q.bottom); }); return [(x0-D.left)/k,(y0-D.top)/k,(x1-x0)/k,(y1-y0)/k]; }
  const ba=document.querySelector('#device .acc-barre');
  const mots=p?[...p.querySelectorAll('.gd-cle, .gd-nat')].map(e=>{ const c=getComputedStyle(e); return {t:e.textContent, cl:e.className, pol:c.fontFamily.split(',')[0].replace(/["']/g,'').trim(), col:c.color, tt:c.textTransform}; }):[];
  return {guide:g?g.getAttribute('data-guide'):null, entier:!!(g&&g.getAttribute('data-entier')), eau:!!document.getElementById('guideEau'),
    phrase:p?p.textContent:null, phraseVue:p?cs(p).visibility:null, phraseB:B(p), phraseCol:p?cs(p).color:null, phraseFs:p?parseFloat(cs(p).fontSize):null, phrasePol:p?cs(p).fontFamily.split(',')[0].replace(/["']/g,'').trim():null, mots:mots,
    tard:t?t.textContent:null, tous:tous, devant:acc, e:(window._guide?window._guide.etat():null), regle:(window._guide?window._guide.regle:null), vu:localStorage.getItem('promi_guide'),
    studioVu:vu(document.getElementById('studioBtn')), auraVu:vu(document.getElementById('souffleBtn')), indexVu:vu(document.getElementById('indexBtn')), plusB:B(document.getElementById('createBtn')), barre:B(ba),
    studio:(()=>{const s=document.getElementById('studioScreen'); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.6); return !!(s&&h&&s.contains(h));})(),
    choix:!!(document.getElementById('accChoix')&&document.getElementById('accChoix').classList.contains('ouvert')), cs:!!document.querySelector('#createSheet.show'),
    textes:(window.TEXTES_ENGAGEMENT&&window.TEXTES_ENGAGEMENT.guide)||null, voulu:(window.TEXTES_ENGAGEMENT&&window.TEXTES_ENGAGEMENT.imperatifVoulu)||null, onb:!!(document.getElementById('onbV')), monde:(()=>{try{return Toile.getTheme()}catch(e){return null}})(), clair:document.getElementById('device').classList.contains('light')}; }"""
# L'EAU, LUE SUR LE CANEVAS : l'opacité de #guideEau ramenée à `l` × `h` cases (1 = mouillé, 2 = entre-deux), sur tout l'écran ou dans une boîte (en points)
EAU = """(a)=>{ const cv=document.getElementById('guideEau'); if(!cv||!cv.width) return null; const [l,h,bx,by,bw,bh]=a, d=cv.width/390;
  const c=document.createElement('canvas'); c.width=l; c.height=h; const x=c.getContext('2d'); x.imageSmoothingEnabled=false;
  x.drawImage(cv, (bx||0)*d, (by||0)*d, (bw||390)*d, (bh||844)*d, 0, 0, l, h); const p=x.getImageData(0,0,l,h).data; let s='';
  const o=new Uint8Array(l*h); for(let i=0;i<l*h;i++){ const al=p[i*4+3]; o[i]=al>200?1:(al>40?2:0); }
  let bin=''; for(let i=0;i<o.length;i++) bin+=String.fromCharCode(o[i]); return btoa(bin); }"""
def eau(pg, l=195, h=422, boite=None):
    """rend (mouillé, entre-deux) : deux tableaux de booléens"""
    a = [l, h] + (list(boite) if boite else [0, 0, 390, 844]); s = pg.evaluate(EAU, a)
    if not s: return None, None
    v = np.frombuffer(base64.b64decode(s), dtype=np.uint8).reshape(h, l); return (v == 1), (v == 2)
def morceaux(m, mini=6):
    """les morceaux d'un masque (4 voisins) : une liste de tableaux de booléens, les plus grands d'abord"""
    H, W = m.shape; vu = np.zeros_like(m, dtype=bool); out = []
    ys, xs = np.where(m)
    for y0, x0 in zip(ys.tolist(), xs.tolist()):
        if vu[y0, x0]: continue
        pile = [(y0, x0)]; vu[y0, x0] = True; pts = []
        while pile:
            y, x = pile.pop(); pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not vu[yy, xx]: vu[yy, xx] = True; pile.append((yy, xx))
        if len(pts) >= mini:
            c = np.zeros_like(m, dtype=bool); a = np.array(pts); c[a[:, 0], a[:, 1]] = True; out.append(c)
    return sorted(out, key=lambda c: -c.sum())
def ellipse(c):
    """le recouvrement d'un morceau avec L'ELLIPSE DE MÊMES MOMENTS (1 = c'est une ellipse) ; et son profil : (écart-type du rayon rapporté à
    cette ellipse, variation moyenne entre deux directions voisines) — un bord à peine irrégulier a un petit écart-type et une petite variation"""
    ys, xs = np.where(c); n = len(xs)
    if n < 30: return 1.0, 0.0, 0.0
    cx, cy = xs.mean(), ys.mean(); dx, dy = xs - cx, ys - cy
    sxx, syy, sxy = (dx * dx).mean(), (dy * dy).mean(), (dx * dy).mean()
    T, Dt = sxx + syy, sxx * syy - sxy * sxy; l1 = T / 2 + max(0, T * T / 4 - Dt) ** 0.5; l2 = T / 2 - max(0, T * T / 4 - Dt) ** 0.5
    th = 0.5 * np.arctan2(2 * sxy, sxx - syy); a, b = 2 * l1 ** 0.5, 2 * max(l2, 1e-6) ** 0.5
    H, W = c.shape; Y, X = np.mgrid[0:H, 0:W]; u = (X - cx) * np.cos(th) + (Y - cy) * np.sin(th); v = -(X - cx) * np.sin(th) + (Y - cy) * np.cos(th)
    E = (u / a) ** 2 + (v / b) ** 2 <= 1.0
    iou = float((E & c).sum()) / float(max(1, (E | c).sum()))
    # le profil du bord : pour 120 directions, le point du morceau le plus loin du centre, rapporté au rayon de l'ellipse dans cette direction
    ang = np.arctan2(v[c], u[c]); r = np.sqrt(u[c] ** 2 + v[c] ** 2); pr = []
    for k in range(120):
        t0 = -np.pi + k * 2 * np.pi / 120; sel = (ang >= t0) & (ang < t0 + 2 * np.pi / 120)
        if not sel.any(): pr.append(np.nan); continue
        tm = t0 + np.pi / 120; re = 1.0 / np.sqrt((np.cos(tm) / a) ** 2 + (np.sin(tm) / b) ** 2); pr.append(r[sel].max() / re)
    pr = np.array(pr); ok = ~np.isnan(pr)
    if ok.sum() < 60: return iou, 1.0, 1.0
    q = pr[ok]; return iou, float(q.std()), float(np.abs(np.diff(np.r_[q, q[0]])).mean())
def proche(col, ref, tol=30):
    m = re.findall(r'[\d.]+', col or ''); return len(m) >= 3 and sum(abs(float(m[i]) - ref[i]) for i in range(3)) <= tol
def toucher(cdp, pg, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
def pt(pg, x, y):   # des points de l'appareil vers l'écran
    d = pg.evaluate(DEV); k = d[2] / 390.0; return d[0] + x * k, d[1] + y * k
def centre(pg, sel):
    return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2, r.top+r.height/2]:null;}", sel)
def image(pg):
    d = pg.evaluate(DEV); return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]}))).convert('L').resize((780, 1688))
def energie(im, x0, y0, x1, y1):   # l'énergie des contours d'une zone (points de l'appareil) : écart moyen entre voisins horizontaux et verticaux
    px = im.load(); s = 0; n = 0
    for y in range(int(y0 * 2), int(y1 * 2) - 1):
        for x in range(int(x0 * 2), int(x1 * 2) - 1):
            v = px[x, y]; s += abs(v - px[x + 1, y]) + abs(v - px[x, y + 1]); n += 2
    return s / max(1, n)

# le relevé se fait DANS la page, à chaque image : le dernier instant où quelque chose BOUGEAIT, l'instant où le guide paraît, où l'eau part, où elle
# couvre tout ; l'avancée de la couverture et de la zone nette à chaque image (ce que le guide déclare) ; la présence d'un « Plus tard »
SONDE = """window.__g={bouge:0,tG:0,tDep:0,tEnt:0,tards:0,couv:[],net:[],dt:[]}; (function b(){ try{ var n=performance.now(), g=document.getElementById('guide'), o=document.getElementById('onbV');
    var run=false; try{ var st=window.Toile_state&&Toile_state(); run=!!(st&&st.running); }catch(e){}
    if(!g && (o || run)) window.__g.bouge=n;
    if(g && !window.__g.tG){ window.__g.tG=n; }
    if(g && !window.__g.tDep && g.getAttribute('data-depart')){ window.__g.tDep=n; try{ performance.mark('lever'); }catch(_){} }
    if(g && !window.__g.tEnt && g.getAttribute('data-entier')) window.__g.tEnt=n;
    if(g){ window.__g.couv.push([Math.round(n), +(g.getAttribute('data-couv')||0)]); window.__g.net.push([Math.round(n), +(g.getAttribute('data-net')||0), g.getAttribute('data-guide')||'']); }
    if(document.getElementById('guideTard')||document.getElementById('onbTard')||document.querySelector('#onbV .onbv-tard')) window.__g.tards++;
    if(!g){ window.__g.tG=0; window.__g.tDep=0; window.__g.tEnt=0; window.__g.couv=[]; window.__g.net=[]; }
  }catch(e){} requestAnimationFrame(b); })();
  ['touchstart','touchend','pointerdown'].forEach(function(t){ document.addEventListener(t,function(){ if(!document.getElementById('guide')) window.__g.bouge=performance.now(); },true); });"""

def cap(pg, nom):
    d = pg.evaluate(DEV); pg.screenshot(path='planche-v146/guide-%s.png' % nom, clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})
def a2(e, T):
    fautes = [t for t in e['tous'] if t['eng'] is None or t['op'] != 1 or (t['trd'] not in ('0s', '') and t['trp'] not in ('none', '')) or t['an'] != 'none' or t['bf'] != 'none']
    juge('[%s] A2 : tout nœud du guide porte data-eng, opacité 1, aucune transition, aucune animation, aucun flou CSS' % T, len(e['tous']) >= 3 and not fautes, '%d nœuds · %s' % (len(e['tous']), fautes[:2]))
def phrase(e, T, quoi):
    """4.2 et §11.7 : la phrase, mot pour mot, sans contour, plus grosse ; ses mots-clés en PromiLate ; les couleurs du clair, la crème du sombre"""
    ph = PH_STUDIO if quoi == 'studio' else PH_PLUS; clair = e['clair']
    juge('[%s] %s · la phrase, mot pour mot, visible, au milieu de l\'écran' % (T, quoi), e['phrase'] == ph and e['phraseVue'] == 'visible' and e['phraseB'] and abs((e['phraseB'][1] + e['phraseB'][3] / 2) - 372) <= 40, '« %s » %s' % (e['phrase'], e['phraseB']))
    cont = [t for t in e['tous'] if t['eng'] == 'guide-phrase' and ((t['sh'] not in ('none', '')) or (t['st'] not in ('0px', '', None)))]
    juge('[%s] %s · AUCUN contour ni ombre sur les lettres ; la phrase est plus grosse (≥ 34 px, 30 avant)' % (T, quoi), not cont and (e['phraseFs'] or 0) >= 34, 'taille %s · contours %s' % (e['phraseFs'], cont[:1]))
    cles = [m for m in e['mots'] if 'gd-cle' in m['cl']]; nats = [m for m in e['mots'] if 'gd-nat' in m['cl']]
    juge('[%s] %s · les mots-clés %s sont en PromiLate, en capitales' % (T, quoi, CLES[quoi]), [m['t'] for m in cles] == CLES[quoi] and all(m['pol'] == 'PromiLate' and m['tt'] == 'uppercase' for m in cles), [(m['t'], m['pol']) for m in cles])
    if clair:
        juge('[%s] %s · en clair : le texte en #291547, les mots-clés en #0E78F2' % (T, quoi), proche(e['phraseCol'], VIOLET) and all(proche(m['col'], BLEU) for m in cles), '%s · %s' % (e['phraseCol'], [m['col'] for m in cles]))
        if quoi == 'plus': juge('[%s] plus · en clair : Promi, Chiche, Cercle dans leur couleur (trois teintes, aucune n\'est celle du texte)' % T, [m['t'] for m in nats] == ['Promi', 'Chiche', 'Cercle'] and len(set(m['col'] for m in nats)) == 3 and proche(nats[0]['col'], BLEU) and not any(proche(m['col'], VIOLET, 12) for m in nats), [(m['t'], m['col']) for m in nats])
    else:
        juge('[%s] %s · en sombre : la crème, pour toute la phrase' % (T, quoi), proche(e['phraseCol'], CREME) and all(proche(m['col'], CREME) for m in e['mots']), '%s · %s' % (e['phraseCol'], [m['col'] for m in e['mots']][:3]))
def zone(pg, e, T, quoi, nette=None):
    """4.3 / 4.5 : la zone nette, lue sur le canevas à 3 cases par point, dans une boîte de 130 pt autour de la cible"""
    tr = (e['e'] or {}).get('trou')
    if not tr: juge('[%s] %s · la zone nette existe' % (T, quoi), False); return None
    bx, by = tr['x'] - 65, tr['y'] - 65; m, _ = eau(pg, 390, 390, (bx, by, 130, 130))
    if m is None: juge('[%s] %s · le canevas de l\'eau se lit' % (T, quoi), False); return None
    trou = ~m; M = morceaux(trou, 20)
    if not M: juge('[%s] %s · la zone nette est ouverte' % (T, quoi), False, 'aucun trou'); return None
    c = M[0]; ys, xs = np.where(c); x0, x1, y0, y1 = bx + xs.min() / 3.0, bx + (xs.max() + 1) / 3.0, by + ys.min() / 3.0, by + (ys.max() + 1) / 3.0
    cb = e['studioVu'] if quoi == 'studio' else e['plusB']
    contient = x0 <= cb[0] + 0.7 and y0 <= cb[1] + 0.7 and x1 >= cb[0] + cb[2] - 0.7 and y1 >= cb[1] + cb[3] - 0.7
    juge('[%s] %s · la zone nette, un seul morceau, contient toute la cible (%s)' % (T, quoi, 'l\'icône et son mot' if quoi == 'studio' else 'le +'), len(M) == 1 and contient, 'zone x %.1f–%.1f, y %.1f–%.1f · cible %s' % (x0, x1, y0, y1, [round(v, 1) for v in cb]))
    ba = e['barre']; voisins = [e['auraVu']] + ([e['indexVu']] if quoi == 'plus' else [])
    hors_voisins = all(x1 <= v[0] - 0.5 or x0 >= v[0] + v[2] + 0.5 for v in voisins)
    dans_barre = x0 >= ba[0] + 3 and x1 <= ba[0] + ba[2] - 3 and y0 >= ba[1] + 3 and y1 <= ba[1] + ba[3] - 3
    juge('[%s] %s · on ne voit NI l\'Aura%s NI le contour de la barre : la zone s\'arrête avant' % (T, quoi, ' ni l\'Index' if quoi == 'plus' else ''), hors_voisins and dans_barre, 'zone x %.1f–%.1f · Aura à %.1f · barre %s' % (x0, x1, e['auraVu'][0], [round(v, 1) for v in ba]))
    iou, sd, var = ellipse(c)
    juge('[%s] %s · sa forme est un entourage LÉGÈREMENT imparfait : ni cercle ni ellipse parfaits (recouvrement avec l\'ellipse de mêmes moments ≤ 0,988 ; une vraie ellipse de cette taille : ≥ 0,995), ni déchiqueté (≥ 0,90, et un bord lisse : ≤ 1,2 %% d\'une direction à la voisine)' % (T, quoi),
         0.90 <= iou <= 0.988 and var <= 0.012 and sd <= 0.09, 'recouvrement %.3f · écart-type du rayon %.3f · variation voisine %.4f' % (iou, sd, var))
    if nette is not None:
        apres = image(pg); ex0, ey0, ex1, ey1 = cb[0] + 2, cb[1] + 2, cb[0] + cb[2] - 2, cb[1] + cb[3] - 2
        en, ea = energie(nette, ex0, ey0, ex1, ey1), energie(apres, ex0, ey0, ex1, ey1); Z = ((30, 44, 360, 96), (30, 110, 360, 280), (30, 470, 360, 690)); f0, f1 = sum(energie(nette, *z) for z in Z), sum(energie(apres, *z) for z in Z)
        juge('[%s] %s · sur l\'image : la cible est NETTE (≥ 85 %% de ses contours), le reste de l\'écran est FLOU (≤ 45 %%)' % (T, quoi), en > 0 and ea >= 0.85 * en and f1 <= 0.45 * f0, 'cible %.2f → %.2f · plateau et Toile hors de la phrase %.2f → %.2f' % (en, ea, f0, f1))
    return {'cx': (x0 + x1) / 2, 'cy': (y0 + y1) / 2, 'aire': float(c.sum()) / 9.0}
def couverture(pg, T):
    """4.1, sur des états arrêtés (`figeA`) : des flaques, pas une forme ; ce qui est mouillé le reste ; le bord est une ligne"""
    etapes = [0.08, 0.2, 0.35, 0.5, 0.65, 0.8, 0.93, 1.0]; M = []; entre = []
    for u in etapes:
        pg.evaluate("(ms)=>{ _guide.figeA(ms); }", u * COUVRE); pg.wait_for_timeout(120); m, e2 = eau(pg); M.append(m); entre.append(e2)
        if u in (0.2, 0.5, 0.8): cap(pg, 'couverture-%s-%02d' % (T, int(u * 100)))
    if any(m is None for m in M): juge('[%s] 4.1 · l\'eau se lit sur le canevas du guide' % T, False); return
    parts = [float(m.mean()) for m in M]
    juge('[%s] 4.1 · la surface mouillée monte d\'un bout à l\'autre : rien à 8 %% du temps ou presque, tout à la fin, sans palier' % T, parts[0] <= 0.12 and parts[-1] >= 0.999 and all(b >= a - 0.002 for a, b in zip(parts, parts[1:])) and max(b - a for a, b in zip(parts, parts[1:])) <= 0.34 and 0.2 <= parts[3] <= 0.75,
         ' · '.join('%d %%' % round(p * 100) for p in parts))
    n = [len(morceaux(m, 12)) for m in M]
    juge('[%s] 4.1 · des FLAQUES : au début plusieurs, séparées (≥ 4 à 20 %% du temps) ; elles se rejoignent (moins de morceaux ensuite) ; une seule nappe à la fin' % T, n[1] >= 4 and n[-1] == 1 and n[4] <= n[1] and max(n[:3]) >= 5, 'morceaux : %s' % n)
    garde = [float((a & b).sum()) / float(max(1, a.sum())) for a, b in zip(M, M[1:])]
    juge('[%s] 4.1 · rien ne se déplace : ce qui est mouillé le reste (≥ 99,5 %% d\'une étape à la suivante)' % T, min(garde) >= 0.995, ' · '.join('%.1f %%' % (g * 100) for g in garde))
    formes = [ellipse(c) for c in morceaux(M[1], 40)[:6]] + [ellipse(c) for c in morceaux(M[2], 60)[:4]]
    io_ = sorted(f[0] for f in formes)
    juge('[%s] 4.1 · aucune flaque n\'est un disque ni une ellipse (recouvrement avec l\'ellipse de mêmes moments < 0,96 pour chacune, ≤ 0,92 en médiane ; une vraie ellipse de cette taille : ≥ 0,97)' % T, len(formes) >= 4 and io_[-1] < 0.96 and io_[len(io_) // 2] <= 0.92, ' · '.join('%.2f' % f for f in io_))
    bord = [float(e2.mean()) / max(1e-6, float(m.mean()) + float(e2.mean())) for m, e2 in zip(M[1:6], entre[1:6])]
    juge('[%s] 4.1 · le bord d\'une flaque est une LIGNE : aucune zone à demi transparente (≤ 2 %% de l\'eau entre-deux, le lissage du trait)' % T, max(bord) <= 0.02, ' · '.join('%.2f %%' % (b * 100) for b in bord))
    return M
def ouvre(b, th, reduit=False, vierge=True):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, reduced_motion=('reduce' if reduit else 'no-preference'))
    ctx.add_init_script("try{ if(!localStorage.getItem('promi_theme')) localStorage.setItem('promi_theme','%s'); %s }catch(e){}" % (th, '' if vierge else "localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_rappel_n','9');"))
    ctx.add_init_script(SONDE)
    pg = ctx.new_page(); pg.__dict__['er'] = []; pg.on('pageerror', lambda e: pg.__dict__['er'].append(str(e)[:160])); pg.goto(URL); pg.wait_for_timeout(6500)
    pg.evaluate("(t)=>{ try{ setTheme(t); }catch(e){} }", th); pg.wait_for_timeout(500)
    if not vierge: pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
    return ctx, pg, ctx.new_cdp_session(pg)
def onboarding(pg, cdp, compte=True):
    """le parcours d'origine, au doigt : prénom → parole → trait → message de fin → compte (« Plus tard ») → l'accueil"""
    c = centre(pg, '#onbPh'); toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
    return trait(pg, cdp, compte)
def trait(pg, cdp, compte=True):
    z = pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(); return {l:r.left,t:r.top,k:r.width/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    if not z or not z['dep']: return False
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]}); pg.wait_for_timeout(90)
    for i in range(1, 25):
        u = i / 24.0; cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * u, 'y': y0 + (y1 - y0) * u - 14 * z['k'] * (1 - abs(2 * u - 1))}]}); pg.wait_for_timeout(22)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    pg.wait_for_timeout(1900 + 4000 + 500)
    x, y = pt(pg, 195, 300); toucher(cdp, pg, x, y)          # v146 (11.4) : le premier toucher fait venir le reste du message…
    for _ in range(60):
        if pg.evaluate("()=>{ const v=document.getElementById('onbV'); return !v || v.getAttribute('data-onb-reste')==='fini' || !document.getElementById('onbReste'); }"): break
        pg.wait_for_timeout(150)
    pg.wait_for_timeout(300); toucher(cdp, pg, x, y); pg.wait_for_timeout(900)          # … le second mène au compte
    if compte:
        c = centre(pg, '.onbv-compte .tard')
        if c: toucher(cdp, pg, c[0], c[1])
    return True

def attend(pg, quoi, maxi=9000, entier=True):
    t0 = time.time(); e = None
    while (time.time() - t0) * 1000 < maxi:
        e = pg.evaluate(ETAT)
        if e['guide'] == quoi and (e['entier'] or not entier): return e
        pg.wait_for_timeout(80)
    return e or pg.evaluate(ETAT)
def images(trace, debut_nom='lever', duree=2000000):
    """le travail du fil principal par image, lu dans la trace (la méthode de redteam_fluide)"""
    ev = trace.get('traceEvents', trace) if isinstance(trace, dict) else trace
    m = [e for e in ev if e.get('name') == debut_nom and 'ts' in e]
    if not m: return None
    pid, tid, t0 = m[0]['pid'], m[0]['tid'], m[0]['ts']
    taches = sorted((e['ts'], e['ts'] + e.get('dur', 0)) for e in ev if e.get('name') == 'RunTask' and e.get('ph') == 'X' and e.get('pid') == pid and e.get('tid') == tid and e.get('dur', 0) > 0)
    debuts = sorted(set(e['ts'] for e in ev if e.get('name') == 'AnimationFrame::Render' and e.get('pid') == pid and 'ts' in e))
    if len(debuts) < 10: debuts = sorted(set(e['ts'] for e in ev if e.get('name') in ('Commit', 'BeginMainThreadFrame') and e.get('pid') == pid and 'ts' in e))
    out = []
    for a, b_ in zip(debuts, debuts[1:]):
        if a < t0 or a > t0 + duree: continue
        out.append(sum(max(0, min(b_, y) - max(a, x)) for x, y in taches if y > a and x < b_) / 1000.0)
    return out


def longues(tr, marque, duree):
    """les appels de plus de 12 ms dans la fenêtre : leur nom, leur fichier, leur ligne — pour NOMMER ce qui dépasse"""
    ev = tr.get('traceEvents', tr); m = [e for e in ev if e.get('name') == marque and 'ts' in e]
    if not m: return []
    pid, tid, t0 = m[0]['pid'], m[0]['tid'], m[0]['ts']; out = []
    for e in ev:
        if e.get('pid') == pid and e.get('tid') == tid and e.get('ph') == 'X' and e.get('dur', 0) > 12000 and 0 <= e['ts'] - t0 <= duree and e.get('name') not in ('RunTask', 'v8.callFunction', 'ThreadControllerImpl::RunTask'):
            d = (e.get('args') or {}).get('data') or {}; out.append('%d ms : %s %.0f ms %s' % ((e['ts'] - t0) / 1000, e['name'], e['dur'] / 1000.0, ((d.get('functionName') or '') + '@' + str(d.get('url', '')).split('/')[-1][:20] + ':' + str(d.get('lineNumber', ''))) if d else ''))
    return out[:6]

def premier_lancement(b, th):
    """stockage vierge, onboarding entier au doigt, puis : la couverture, la phrase, le Studio, un CHOIX au Studio, le Studio refermé → l'étape du + → le +"""
    T = 'clair' if th == 'light' else 'sombre'; print('\n── premier lancement, %s : onboarding entier, choix au Studio' % T)
    ctx, pg, cdp = ouvre(b, th); onboarding(pg, cdp)
    nette = None
    for _ in range(60):
        if pg.evaluate("()=>!document.getElementById('onbV')"): pg.wait_for_timeout(200); e0 = pg.evaluate(ETAT); nette = image(pg); break
        pg.wait_for_timeout(50)
    else: e0 = pg.evaluate(ETAT)
    juge('[%s] à l\'arrivée sur l\'accueil rien n\'est flou, la barre est complète' % T, not e0['guide'] and e0['plusB'] and e0['studioVu'][2] > 10, 'guide %s' % e0['guide'])
    # pendant la couverture : l'eau est là, en plusieurs morceaux, et ce qu'on lit à deux instants s'emboîte
    vus = []; t0 = time.time()
    while time.time() - t0 < 12:
        e = pg.evaluate(ETAT)
        if e['eau'] and not e['entier'] and (e['e'] or {}).get('couv', 0) > 0.12:
            m, _ = eau(pg, 98, 211)
            if m is not None: vus.append((e['e']['couv'], m))
        if e['entier']: break
        pg.wait_for_timeout(20)
    e = attend(pg, 'studio', 9000); pg.wait_for_timeout(OUVRE + 250); g = pg.evaluate("()=>window.__g"); e = pg.evaluate(ETAT)
    calme = (g['tG'] - g['bouge']) / 1000.0 if g['tG'] else None
    juge('[%s] LE MOMENT : l\'eau commence 0,6 s après que l\'accueil est posé (0,55 à 1,2 s : onboarding refermé, Toile au repos, aucun doigt)' % T, calme is not None and 0.55 <= calme <= 1.2, 'calme avant le guide : %s s' % (None if calme is None else round(calme, 2)))
    duree = (g['tEnt'] - g['tDep']) / 1000.0 if g['tEnt'] and g['tDep'] else None
    juge('[%s] 4.1 · la couverture dure 1,2 à 1,6 s (réglée à 1,4)' % T, duree is not None and 1.2 <= duree <= 1.75 and (e['regle'] or {}).get('COUVRE') == COUVRE, 'mesurée %s s · réglée %s ms' % (None if duree is None else round(duree, 2), (e['regle'] or {}).get('COUVRE')))
    C = [c for c in g['couv'] if 0 < c[1] < 1]; pas = [b_[1] - a_[1] for a_, b_ in zip(C, C[1:])]
    juge('[%s] 4.1 · rien n\'arrive d\'un coup : d\'une image à la suivante la couverture avance de 9 %% au plus, jamais en arrière' % T, len(C) >= 25 and max(pas) <= 0.09 and min(pas) >= -1e-6, '%d images · plus grand pas %.1f %% · plus petit %.2f %%' % (len(C), max(pas or [0]) * 100, min(pas or [0]) * 100))
    juge('[%s] 4.1 · en direct : l\'eau est vue en plusieurs flaques, et ce qui est mouillé le reste d\'un relevé au suivant' % T, len(vus) >= 3 and max(len(morceaux(m, 6)) for _, m in vus[:4]) >= 3 and all(float((a & b_).sum()) / max(1, float(a.sum())) >= 0.99 for (_, a), (_, b_) in zip(vus, vus[1:])),
         '%d relevés · morceaux %s' % (len(vus), [len(morceaux(m, 6)) for _, m in vus[:6]]))
    cap(pg, '1-studio-%s' % T)
    phrase(e, T, 'studio')
    juge('[%s] A3 : l\'impératif de la phrase du Studio est une exception NOMMÉE (TEXTES_ENGAGEMENT.imperatifVoulu) ; l\'autre phrase n\'en a pas' % T, PH_STUDIO in (e['voulu'] or []) and (e['textes'] or {}).get('plus') == PH_PLUS and not re.search(r'\b(Choisis|Touche|Trace|Plante|Tiens|Va|Ouvre)\b', PH_PLUS), '%s' % e['voulu'])
    juge('[%s] « Plus tard » n\'existe pas : ni dans le guide, ni à aucune image de l\'onboarding (exception nommée de R6)' % T, e['tard'] is None and g['tards'] == 0 and pg.evaluate("()=>!!(window.TEXTES_ENGAGEMENT&&TEXTES_ENGAGEMENT.sansPlusTard)&&!TEXTES_ENGAGEMENT.guide.plusTard"), 'vu à %s image(s)' % g['tards'])
    a2(e, T); z1 = zone(pg, e, T, 'studio', nette)
    # toucher le Studio → le Studio ; y faire un CHOIX (un autre monde) ; le refermer
    x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2800); e3 = pg.evaluate(ETAT)
    juge('[%s] toucher le Studio net ouvre le Studio PAR-DESSUS le guide : l\'eau reste posée dessous, sans phrase' % T, e3['studio'] and e3['eau'] and e3['phrase'] is None and e3['e']['etat'] == 'au-studio', 'Studio %s · état %s · phrase %s' % (e3['studio'], e3['e']['etat'], e3['phrase']))
    m0 = e3['monde']; x0, y0 = pt(pg, 300, 330); x1, y1 = pt(pg, 80, 330)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]})
    for i in range(1, 11): pg.wait_for_timeout(18); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * i / 10, 'y': y0}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1800)
    m1 = pg.evaluate("()=>{try{return Toile.getTheme()}catch(e){return null}}")
    c = centre(pg, '#studioScreen .closeb')
    if c: toucher(cdp, pg, c[0], c[1])
    e4 = attend(pg, 'plus', 12000); pg.wait_for_timeout(OUVRE + 250); e4 = pg.evaluate(ETAT); cap(pg, '2-plus-%s' % T)
    juge('[%s] CHEMIN 1 — un choix au Studio (monde %s → %s), Studio refermé : l\'étape du + arrive, sa phrase mot pour mot' % (T, m0, m1), e4['guide'] == 'plus' and e4['phrase'] == PH_PLUS and m1 != m0, 'guide %s · « %s »' % (e4['guide'], e4['phrase']))
    if e4['guide'] == 'plus':
        phrase(e4, T, 'plus'); zone(pg, e4, T, 'plus')
        x, y = pt(pg, e4['e']['trou']['x'], e4['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(380); e5 = pg.evaluate(ETAT); mi, _ = eau(pg, 98, 211)
        juge('[%s] toucher le + ouvre les trois natures TOUT DE SUITE ; l\'eau se retire en flaques pendant ce temps (elle n\'a pas disparu d\'un coup)' % T, (e5['choix'] or e5['cs']) and mi is not None and 0.05 < float(mi.mean()) < 0.99, 'natures %s · eau encore %s %%' % (e5['choix'], None if mi is None else round(float(mi.mean()) * 100)))
        pg.wait_for_timeout(RETIRE + 500); e6 = pg.evaluate(ETAT)
        juge('[%s] puis il ne reste rien : le guide est retiré, vu une fois' % T, not e6['guide'] and not e6['eau'] and e6['vu'] == '1', 'guide %s' % e6['guide'])
    pg.reload(); pg.wait_for_timeout(8500); e7 = pg.evaluate(ETAT)
    juge('[%s] une seule fois : après un rechargement, ni onboarding ni guide' % T, not e7['guide'] and not e7['onb'], 'guide %s · devant %s' % (e7['guide'], e7['devant']))
    juge('[%s] aucune erreur de page' % T, not pg.__dict__['er'], pg.__dict__['er'][:2]); ctx.close()

def rejoue(b, th, reduit=False):
    ctx, pg, cdp = ouvre(b, th, reduit, vierge=False); pg.evaluate("()=>{ localStorage.removeItem('promi_guide'); _guide.attend(true); }"); return ctx, pg, cdp
def pret(pg, quoi, maxi=12000):
    e = attend(pg, quoi, maxi); pg.wait_for_timeout(OUVRE + 250); return pg.evaluate(ETAT)
def chemins(b):
    print('\n── les autres chemins (le guide rejoué)')
    # 2 · Studio refermé SANS choix
    ctx, pg, cdp = rejoue(b, 'light'); e = pret(pg, 'studio'); x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2800)
    c = centre(pg, '#studioScreen .closeb'); toucher(cdp, pg, c[0], c[1]) if c else None; e2 = attend(pg, 'plus', 12000)
    juge('CHEMIN 2 — Studio refermé sans choix : l\'étape du + arrive', e['guide'] == 'studio' and e2['guide'] == 'plus' and e2['phrase'] == PH_PLUS, 'guide %s → %s' % (e['guide'], e2['guide'])); ctx.close()
    # 3 · toucher ailleurs pendant l'étape du Studio : 4.4 la zone se referme SUR ELLE-MÊME, puis celle du + s'ouvre — rien ne glisse
    ctx, pg, cdp = rejoue(b, 'light'); e = pret(pg, 'studio'); tr = e['e']['trou']
    pg.evaluate("""(a)=>{ window.__z=[]; const [l,h]=a; const cv=document.getElementById('guideEau'), d=cv.width/390, c=document.createElement('canvas'); c.width=l; c.height=h; const x=c.getContext('2d',{willReadFrequently:true});
        (function f(){ const g=document.getElementById('guide'); if(!g) return; try{ x.clearRect(0,0,l,h); x.drawImage(cv, 24*d, 700*d, 342*d, 120*d, 0, 0, l, h); const p=x.getImageData(0,0,l,h).data; let n=0, sx=0, x0=1e9, x1=-1, y0=1e9, y1=-1; for(let i=0;i<l*h;i++){ if(p[i*4+3]<128){ const X=i%l, Y=(i/l)|0; n++; sx+=X; if(X<x0)x0=X; if(X>x1)x1=X; if(Y<y0)y0=Y; if(Y>y1)y1=Y; } }
          const kx=342/l, ky=120/h; window.__z.push([Math.round(performance.now()), n, n?24+sx/n*kx:0, n?24+x0*kx:0, n?24+(x1+1)*kx:0, n?700+y0*ky:0, n?700+(y1+1)*ky:0, g.getAttribute('data-guide')||'']); }catch(e){} requestAnimationFrame(f); })(); }""", [342, 120])
    x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y); pg.wait_for_timeout(300); em = pg.evaluate(ETAT); e2 = pret(pg, 'plus', 5000); Z = pg.evaluate("()=>window.__z")
    juge('CHEMIN 3 — toucher ailleurs pendant l\'étape du Studio : sa zone se referme (aucune phrase pendant), puis l\'étape du + arrive ; l\'eau reste', e['guide'] == 'studio' and em['guide'] == 'vers-plus' and em['phrase'] is None and e2['guide'] == 'plus' and e2['phrase'] == PH_PLUS and e2['eau'], 'guide %s → %s → %s' % (e['guide'], em['guide'], e2['guide']))
    A = [z for z in Z if z[1] > 0]; i_vide = [k for k, z in enumerate(Z) if z[1] == 0]
    S = [z for z in (Z[:i_vide[0]] if i_vide else Z) if z[1] > 0]; P = [z for z in (Z[i_vide[-1]:] if i_vide else []) if z[1] > 0]
    deux = [z for z in A if z[3] < 120 and z[4] > 150]                                 # une zone à cheval sur le Studio et le + : une translation, ou deux zones à la fois
    b0 = S[0] if S else None
    dedans = bool(S) and all(z[3] >= b0[3] - 1.5 and z[4] <= b0[4] + 1.5 and z[5] >= b0[5] - 1.5 and z[6] <= b0[6] + 1.5 for z in S)
    retrecit = bool(S) and all(b_[1] <= a_[1] * 1.02 + 4 for a_, b_ in zip(S, S[1:])) and S[-1][1] <= 0.25 * S[0][1]
    juge('4.4 · la zone du Studio DISPARAÎT SUR ELLE-MÊME : elle rétrécit sans jamais regrossir et ne sort jamais de sa propre empreinte (± 1,5 pt), jusqu\'à rien', len(S) >= 8 and dedans and retrecit and bool(i_vide),
         '%d images · empreinte x %.1f–%.1f · la plus à droite ensuite %.1f · surface %d → %d cases' % (len(S), b0[3] if b0 else 0, b0[4] if b0 else 0, max([z[4] for z in S] or [0]), S[0][1] if S else 0, S[-1][1] if S else 0))
    juge('4.5 · AUCUNE TRANSLATION du Studio au + : jamais une zone nette à cheval entre les deux ni deux zones à la fois ; la zone du Studio est entièrement refermée (une image sans aucune zone) avant que celle du + ne s\'ouvre, à sa place',
         not deux and len(i_vide) >= 1 and len(P) >= 8 and all(z[4] <= 120 for z in S) and all(z[3] >= 150 for z in P), 'images à cheval : %d · sans zone : %d · Studio %d · + %d (x %.1f–%.1f)' % (len(deux), len(i_vide), len(S), len(P), min([z[3] for z in P] or [0]), max([z[4] for z in P] or [0])))
    aires = [z[1] for z in P]
    juge('4.5 · la zone du + s\'ouvre EN FLAQUES : elle grandit d\'image en image (elle ne paraît pas d\'un coup : premier relevé ≤ 35 % de sa taille finale)', len(aires) >= 8 and aires[0] <= 0.35 * max(aires) and all(b_ >= a_ * 0.97 for a_, b_ in zip(aires, aires[1:])), 'premier %d · final %d cases' % (aires[0] if aires else 0, max(aires or [0])))
    # 4.3 à mi-ouverture : ni vide ni pleine, et pas un disque qui enfle (plusieurs morceaux, ou une forme échancrée)
    pg.evaluate("()=>_guide.figeNet('plus', %d)" % int(OUVRE * 0.45)); pg.wait_for_timeout(200); m, _ = eau(pg, 390, 390, (130, 695, 130, 130)); t = ~m; Mx = morceaux(t, 8); cap(pg, 'zone-plus-mi')
    pg.evaluate("()=>_guide.figeNet('plus', %d)" % OUVRE); pg.wait_for_timeout(200); mf, _ = eau(pg, 390, 390, (130, 695, 130, 130)); plein = float((~mf).sum())
    io_mi = ellipse(Mx[0])[0] if Mx else 1
    juge('4.3 · à mi-ouverture la zone nette est faite de FLAQUES : ni vide ni pleine (15 à 85 %), en plusieurs morceaux ou échancrée (recouvrement avec une ellipse ≤ 0,9)', bool(Mx) and 0.15 <= float(t.sum()) / max(1.0, plein) <= 0.85 and (len(Mx) >= 2 or io_mi <= 0.9), 'part %.0f %% · %d morceau(x) · ellipse %.2f' % (100 * float(t.sum()) / max(1.0, plein), len(Mx), io_mi))
    pg.evaluate("()=>{ _guide.finir(); }"); pg.wait_for_timeout(200); ctx.close()
    # 4.6 · à l'étape du +, toucher ailleurs : la zone se referme, puis les flaques se vident
    ctx, pg, cdp = rejoue(b, 'light'); e = pret(pg, 'studio'); x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y); e2 = pret(pg, 'plus', 6000); toucher(cdp, pg, x, y)
    R = []; t0 = time.time()
    while time.time() - t0 < (FERME + RETIRE) / 1000.0 + 1.2:
        m, _ = eau(pg, 98, 211)
        if m is None: break
        R.append((float(m.mean()), len(morceaux(m, 6)))); pg.wait_for_timeout(60)
    e3 = pg.evaluate(ETAT); pg.wait_for_timeout(2500); e4 = pg.evaluate(ETAT); k0 = max(range(len(R)), key=lambda k: R[k][0]) if R else 0; R = R[k0:]; parts = [r[0] for r in R]; mi = [r for r in R if 0.2 < r[0] < 0.8]
    juge('4.6 · LA FIN : les flaques se VIDENT — l\'eau baisse sans jamais remonter, en plusieurs morceaux à mi-retrait (≥ 3), puis il ne reste rien et le guide ne se reforme pas', len(R) >= 6 and parts[0] >= 0.995 and all(b_ <= a_ + 0.004 for a_, b_ in zip(parts, parts[1:])) and bool(mi) and max(r[1] for r in mi) >= 3 and not e3['guide'] and not e4['guide'] and e4['devant'] == 'accueil',
         '%d relevés · eau %s %% · morceaux à mi-retrait %s · guide %s' % (len(R), [round(p_ * 100) for p_ in parts[::3]], [r[1] for r in mi][:6], e4['guide'])); ctx.close()
    # deux lancements : pas les mêmes flaques
    ctx, pg, cdp = ouvre(b, 'light', vierge=False); L = []
    for _ in range(2):
        pg.evaluate("()=>{ _guide.montre('studio', true); }"); pg.wait_for_timeout(1300); pg.evaluate("(ms)=>{ _guide.figeA(ms); }", 0.3 * COUVRE); pg.wait_for_timeout(150); m, _ = eau(pg, 98, 211); L.append(m); pg.evaluate("()=>{ _guide.finir(); }"); pg.wait_for_timeout(300)
    rec = float((L[0] & L[1]).sum()) / float(max(1, (L[0] | L[1]).sum())) if L[0] is not None and L[1] is not None else 1
    juge('4.1 · AU HASARD : deux lancements ne donnent pas les mêmes flaques (recouvrement ≤ 0,6 à 30 % du temps)', rec <= 0.6, 'recouvrement %.2f' % rec)
    M = couverture(pg, 'clair'); ctx.close()
    # Réduire les animations
    ctx, pg, cdp = rejoue(b, 'light', True); t0 = time.time(); L = []
    while time.time() - t0 < 8:
        e = pg.evaluate(ETAT)
        if e['guide'] and e['eau']: L.append((e['entier'], (e['e'] or {}).get('couv'), (e['e'] or {}).get('net')))
        if len(L) >= 6: break
        pg.wait_for_timeout(40)
    juge('Réduire les animations : l\'eau est posée sans mouvement (couverture entière et zone ouverte dès le premier relevé)', len(L) >= 6 and all(a and c == 1 and n == 1 for a, c, n in L), '%s' % L[:3]); ctx.close()

def cadence(b, th):
    """le travail du fil principal par image pendant la couverture et pendant l'ouverture d'une zone (trace)"""
    T = 'clair' if th == 'light' else 'sombre'; print('\n── la cadence, %s' % T)
    ctx, pg, cdp = ouvre(b, th, vierge=False)
    if not pg.evaluate("()=>!!(window._guide&&_guide.montre&&_guide.figeNet)"): juge('[%s] le guide se rejoue' % T, False); ctx.close(); return
    b.start_tracing(page=pg, categories=['toplevel', 'devtools.timeline', 'disabled-by-default-devtools.timeline', 'blink.user_timing'])
    pg.evaluate("()=>{ _guide.montre('studio'); }"); pg.wait_for_timeout(COUVRE + OUVRE + 900)
    tr = json.loads(b.stop_tracing().decode('utf-8')); W = images(tr, 'lever', (COUVRE + OUVRE + 200) * 1000) or []; pire = max(W) if W else None; W2 = sorted(W)
    juge('[%s] pendant la couverture et l\'ouverture de la zone, aucune image au-delà de 16,7 ms de travail du fil principal' % T, bool(W) and len(W) >= 40 and pire <= 16.7, '%d images · pire %s ms · p95 %s ms · flou d\'avance %s ms' % (len(W), None if pire is None else round(pire, 1), round(W2[int(len(W2) * .95)], 1) if W2 else None, pg.evaluate("()=>_guide.etat().flouMs")))
    if pire and pire > 16.7: print('      ce qui dépasse :', longues(tr, 'lever', (COUVRE + OUVRE + 200) * 1000))
    if th == 'dark':
        e = pret(pg, 'studio'); phrase(e, T, 'studio'); zone(pg, e, T, 'studio'); x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y); e2 = pret(pg, 'plus', 6000); phrase(e2, T, 'plus'); zone(pg, e2, T, 'plus'); cap(pg, 'plus-sombre')
    ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    if '--cadence' in sys.argv:
        for _ in range(3): cadence(b, 'light'); cadence(b, 'dark')
    else:
        premier_lancement(b, 'light'); cadence(b, 'light')
        if not VITE:
            chemins(b); cadence(b, 'dark')
    b.close()
ok = sum(1 for _, c in res if c)
print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
