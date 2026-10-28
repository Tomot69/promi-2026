#!/usr/bin/env python3
"""redteam_guide_cloture.py — ⚑ v165 (Tom, C-203) : LA CLÔTURE DU GUIDE.

« Après l'étape du +, le guide se termine par une clôture qui invite à partager. Elle n'est PAS contrainte comme l'étape du Studio. Phrase 1 : « Étoffe ta
Toile, et partage-la ! » Phrase 2 : « Le reste s'explore à ton rythme. » La phrase 1 arrive dans TOUS ces cas : a. on touche le + et on crée quelque chose —
au retour sur l'accueil ; b. on touche le +, puis ailleurs (le menu se ferme) ; c. on touche ailleurs que le +. Flou en flaques sauf autour du bouton Partager
(zone nette serrée sur l'icône, 4 à 10 pt, aucun voisin découvert) ; mots-clés en PromiLate et en couleur, en clair et en sombre ; lettres tracées ; aucun
contour. Partager touché : il s'ouvre, à sa fermeture la phrase 2. Ailleurs : la phrase 2. Phrase 2 au centre, sans zone nette ; un toucher ou 3 s termine
le guide, le flou se retire en flaques. Le guide ne revient plus. »

Banc comme Tom (WebKit, doigt), le vrai guide (Studio ouvert puis refermé, puis l'étape du +), clair et sombre, 390 × 844 (échelle 0,93) et 330 × 714 (≈ 0,79).
Preuve : `--fichier=zz-v164b.html` rougit (aucune clôture).
⚑ v166 (Tom, C-203 §3) — contrat remis au niveau (original : sauvegardes/redteam_guide_cloture-avant-v166.py) : la phrase 2 ENTIÈREMENT en PromiLate, d'une
seule couleur (v167 : le cobalt #0E78F2 ; v166 : l'encre du mode), à sa place (422 pt) ; pendant elle, trois zones nettes en flaques — Aura, Index, Fil — et aucune autre, ni flèche ;
Partager jamais obligatoire : sur chacun des trois chemins, Partager touché ET non touché (selon la combinaison).
"""
import sys, base64
sys.path.insert(0, '.')
import numpy as np
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
P1 = 'Étoffe ta Toile, et partage-la !'        # les textes de Tom, EN DUR (l'espace insécable devant « ! », la règle du produit)
P2 = 'Le reste s’explore à ton rythme.'
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
def page(b, sombre, vw, vh):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=True)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__ini')){ sessionStorage.setItem('__ini','1'); localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}" % ('dark' if sombre else 'light'))
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    return ctx, pg, er
def attend(pg, js, n=120, pas=120):
    for _ in range(n):
        v = pg.evaluate(js)
        if v: return v
        pg.wait_for_timeout(pas)
    return None
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
def tap_pt(pg, x, y):
    d = dev(pg); B.tap(pg, d[0] + x * d[2], d[1] + y * d[2], appareil=False)
def tap_sel(pg, sel):
    c = pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
    if c: B.tap(pg, c[0], c[1], appareil=False)
    return bool(c)
ETAT = "()=>{ const g=document.getElementById('guide'); return g ? {g:g.getAttribute('data-guide'), entier:!!g.getAttribute('data-entier'), net:+(g.getAttribute('data-net')||0), couv:+(g.getAttribute('data-couv')||0)} : null; }"
def jusqu_au_plus(pg):
    pg.evaluate("()=>{ _guide.attend(false); }")
    e = attend(pg, "()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&g.getAttribute('data-entier') ? _guide.etat() : null;}", 170)
    if not e: return False
    pg.wait_for_timeout(700); tap_pt(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600)
    tap_sel(pg, '#studioScreen .closeb')
    return bool(attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=1);}", 150))
PHRASE = """()=>{ const p=document.getElementById('guidePhrase'); if(!p) return null; const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, r=p.getBoundingClientRect();
  const cles=[...p.querySelectorAll('.gd-cle')].map(e=>{ const c=getComputedStyle(e); return {t:e.textContent, f:c.fontFamily.split(',')[0].replace(/["']/g,''), col:c.color}; });
  const corps=getComputedStyle(p), tout=[p,...p.querySelectorAll('*')].map(e=>getComputedStyle(e));
  const contour=tout.some(c=>(c.textShadow&&c.textShadow!=='none') || (c.webkitTextStrokeWidth&&parseFloat(c.webkitTextStrokeWidth)>0));
  const ar=p.querySelector('[aria-label]'); return {t:ar?ar.getAttribute('aria-label'):p.textContent, cles:cles, fams:[...p.querySelectorAll('.gd-reste, .gd-reste *')].map(e=>getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g,'')),
    cols:[...new Set([...p.querySelectorAll('.gd-reste, .gd-reste *')].filter(e=>!e.classList.contains('v35-acc')).map(e=>getComputedStyle(e).color))], fleche:!!document.getElementById('guide')&&document.getElementById('guide').hasAttribute('data-fleche'), col:corps.color, contour:contour, cy:(r.top-d.top)/k+r.height/k/2, trace:!!(window._guide&&_guide.etat().trace) || !!p.querySelector('canvas') }; }"""
EAU = """(a)=>{ const cv=document.getElementById('guideEau'); if(!cv||!cv.width) return null; const [l,h,bx,by,bw,bh]=a, d=cv.width/390;
  const c=document.createElement('canvas'); c.width=l; c.height=h; const x=c.getContext('2d'); x.imageSmoothingEnabled=false;
  x.drawImage(cv, bx*d, by*d, bw*d, bh*d, 0, 0, l, h); const p=x.getImageData(0,0,l,h).data; let bin='';
  for(let i=0;i<l*h;i++){ const al=p[i*4+3]; bin+=String.fromCharCode(al>200?1:(al>40?2:0)); } return btoa(bin); }"""
def eau(pg, l, h, boite):
    s = pg.evaluate(EAU, [l, h] + list(boite))
    if not s: return None
    return np.frombuffer(base64.b64decode(s), dtype=np.uint8).reshape(h, l)
def morceaux(m, mini=6):
    H, W = m.shape; vu = np.zeros_like(m, dtype=bool); out = []
    for y0, x0 in zip(*[v.tolist() for v in np.where(m)]):
        if vu[y0, x0]: continue
        pile = [(y0, x0)]; vu[y0, x0] = True; n = 0; pts = []
        while pile:
            y, x = pile.pop(); pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not vu[yy, xx]: vu[yy, xx] = True; pile.append((yy, xx))
        if len(pts) >= mini:
            c = np.zeros_like(m, dtype=bool); a = np.array(pts); c[a[:, 0], a[:, 1]] = True; out.append(c)
    return sorted(out, key=lambda c: -c.sum())
def zone(pg):
    """la zone nette, lue sur le canevas de l'eau (3 cases par point) : sa marge autour de l'icône de Partager, le voisin, le contour du plateau ; et aucun
    autre trou sur tout l'écran"""
    g = pg.evaluate("""()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390;
      const R=s=>{ const n=document.querySelector(s); if(!n) return null; const q=n.getBoundingClientRect(); return [(q.left-d.left)/k,(q.top-d.top)/k,q.width/k,q.height/k]; };
      const pa=document.getElementById('accPlat'); return {sh:R('#shareBtn svg')||R('#shareBtn'), rg:R('#settingsBtn svg')||R('#settingsBtn'), pl:R('#accPlat'), plr:pa?parseFloat(getComputedStyle(pa).borderTopLeftRadius)||30:30}; }""")
    sh, rg, pl = g['sh'], g['rg'], g['pl']; bx, by = sh[0] + sh[2] / 2 - 40, sh[1] + sh[3] / 2 - 40
    v = eau(pg, 240, 240, (bx, by, 80, 80)); tout = eau(pg, 390, 844, (0, 0, 390, 844))
    if v is None or tout is None: return None
    M = morceaux(v != 1, 20); T = morceaux(tout != 1, 6)
    if not M: return {'trous': len(T), 'zone': None}
    c = M[0]; bord = c & ~(np.roll(c, 1, 0) & np.roll(c, -1, 0) & np.roll(c, 1, 1) & np.roll(c, -1, 1)); yy, xx = np.where(bord)
    px, py = bx + (xx + 0.5) / 3.0, by + (yy + 0.5) / 3.0
    dx = np.maximum(0, np.maximum(sh[0] - px, px - (sh[0] + sh[2]))); dy = np.maximum(0, np.maximum(sh[1] - py, py - (sh[1] + sh[3]))); mg = np.sqrt(dx * dx + dy * dy)
    ys, xs = np.where(c); x0, x1, y0, y1 = bx + xs.min() / 3.0, bx + (xs.max() + 1) / 3.0, by + ys.min() / 3.0, by + (ys.max() + 1) / 3.0
    contient = x0 <= sh[0] + 0.7 and y0 <= sh[1] + 0.7 and x1 >= sh[0] + sh[2] - 0.7 and y1 >= sh[1] + sh[3] - 0.7
    voisin = bool(rg) and not (x1 <= rg[0] + 0.5 or x0 >= rg[0] + rg[2] - 0.5)
    r = min(g['plr'], pl[3] / 2)
    qx = np.abs(px - (pl[0] + pl[2] / 2)) - (pl[2] / 2 - r); qy = np.abs(py - (pl[1] + pl[3] / 2)) - (pl[3] / 2 - r)
    sd = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r
    libre = sd < -6.0; mgl = mg[libre] if libre.any() else mg
    return {'trous': len(T), 'un': len(M) == 1, 'contient': contient, 'voisin': voisin, 'plateau': round(-float(sd.max()), 1), 'marge': [round(float(mgl.min()), 1), round(float(mg.max()), 1)]}
ICONES = """()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390;
  const R=s=>{ const n=document.querySelector(s); if(!n) return null; let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9; [...n.querySelectorAll('svg, .l')].forEach(e=>{ const q=e.getBoundingClientRect(); if(q.width<2) return; x0=Math.min(x0,q.left); y0=Math.min(y0,q.top); x1=Math.max(x1,q.right); y1=Math.max(y1,q.bottom); });
    if(!(x1>x0)){ const q=n.getBoundingClientRect(); x0=q.left; y0=q.top; x1=q.right; y1=q.bottom; } return [(x0-d.left)/k,(y0-d.top)/k,(x1-x0)/k,(y1-y0)/k]; };
  return {studio:R('#studioBtn'), aura:R('#souffleBtn'), plus:R('#createBtn'), index:R('#indexBtn'), fil:R('#filBtn'), partage:R('#shareBtn')}; }"""
def zones_reste(pg):
    """les trous de l'eau, lus sur tout l'écran (3 cases par point) : lesquelles des icônes ils découvrent, et leur marge autour de leur icône"""
    I = pg.evaluate(ICONES); tout = eau(pg, 1170, 2532, (0, 0, 390, 844))
    if tout is None: return None
    T = morceaux(tout != 1, 30); out = {'trous': len(T), 'zones': {}}
    for c in T:
        ys, xs = np.where(c); x0, x1, y0, y1 = xs.min() / 3.0, (xs.max() + 1) / 3.0, ys.min() / 3.0, (ys.max() + 1) / 3.0
        dedans = [n for n, b in I.items() if b and x0 <= b[0] + 0.7 and y0 <= b[1] + 0.7 and x1 >= b[0] + b[2] - 0.7 and y1 >= b[1] + b[3] - 0.7]
        touche = [n for n, b in I.items() if b and not (x1 <= b[0] + 0.5 or x0 >= b[0] + b[2] - 0.5 or y1 <= b[1] + 0.5 or y0 >= b[1] + b[3] - 0.5) and n not in dedans]
        nom = dedans[0] if len(dedans) == 1 else '?' + '+'.join(dedans)
        b = I.get(nom) if nom in I else None; mg = None
        if b: mg = [round(min(b[0] - x0, b[1] - y0, x1 - b[0] - b[2], y1 - b[1] - b[3]), 1), round(max(b[0] - x0, b[1] - y0, x1 - b[0] - b[2], y1 - b[1] - b[3]), 1)]
        out['zones'][nom] = {'marge': mg, 'decouvre': touche}
    return out
def phrase1(pg, T, ch):
    st = attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='partage' && +g.getAttribute('data-net')>=1);}", 120)
    juge('[%s · %s] la phrase 1 arrive, sa zone nette ouverte' % (T, ch), bool(st), pg.evaluate(ETAT))
    if not st: return False
    ph = pg.evaluate(PHRASE) or {}
    juge('[%s · %s] phrase 1, mot pour mot' % (T, ch), ph.get('t') == P1, repr(ph.get('t')))
    cl = ph.get('cles') or []
    juge('[%s · %s] « Toile » et « partage-la » en PromiLate, en couleur (≠ le texte), aucun contour' % (T, ch),
         sorted(c['t'] for c in cl) == ['Toile', 'partage-la'] and all(c['f'] == 'PromiLate' and c['col'] != ph.get('col') for c in cl) and not ph.get('contour'), cl)
    juge('[%s · %s] les lettres se tracent' % (T, ch), ph.get('trace'), ph.get('trace'))
    z = zone(pg)
    juge('[%s · %s] zone nette sur Partager seulement : un seul trou à l\'écran, l\'icône dedans, 4 à 10 pt de marge, l\'icône des Réglages non découverte, 2,5 pt au moins en deçà du plateau' % (T, ch),
         bool(z) and z.get('trous') == 1 and z.get('un') and z.get('contient') and not z.get('voisin') and z.get('plateau', 0) >= 2.5 and z['marge'][0] >= 3.3 and z['marge'][1] <= 10.7, z)
    return True
def phrase2(pg, T, ch, attendre_seul):
    st = attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='reste');}", 120)
    t0 = pg.evaluate("()=>performance.now()")   # v166 : la phrase arrivée — la lecture des zones prend du temps
    ph = pg.evaluate(PHRASE) or {}; e = pg.evaluate("()=>_guide.etat()")
    juge('[%s · %s] la phrase 2, mot pour mot, au centre (± 6 pt), sans flèche' % (T, ch), bool(st) and ph.get('t') == P2 and abs(ph.get('cy', 0) - 422) <= 6 and not e.get('trou') and not ph.get('fleche'),
         {'t': ph.get('t'), 'cy': round(ph.get('cy', 0), 1), 'trou': e.get('trou'), 'fleche': ph.get('fleche')})
    ink = 'rgb(14, 120, 242)'   # ⚑ v167 (Tom, C-203 §2) : le cobalt #0E78F2, la couleur des mots-clés du guide, dans les deux thèmes (v166 : l'encre du mode)
    juge('[%s · %s] v167 · la phrase 2 ENTIÈREMENT en PromiLate, d\'une seule couleur : le cobalt #0E78F2' % (T, ch), bool(ph.get('fams')) and all(f == 'PromiLate' for f in ph['fams']) and ph.get('cols') == [ink],
         {'polices': sorted(set(ph.get('fams') or [])), 'couleurs': ph.get('cols')})
    op = attend(pg, "()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='reste' && +g.getAttribute('data-net')>=1);}", 40, 60)
    z = zones_reste(pg) if op else None
    Zs = (z or {}).get('zones') or {}
    juge('[%s · %s] v166 · pendant la phrase 2, trois zones nettes — Aura, Index, Fil — et aucune autre ; chacune contient son icône, 3,3 à 10,7 pt de marge, aucun voisin découvert' % (T, ch),
         bool(z) and z['trous'] == 3 and sorted(Zs) == ['aura', 'fil', 'index'] and all(v['marge'] and v['marge'][0] >= 3.3 and v['marge'][1] <= 10.7 and not v['decouvre'] for v in Zs.values()), z)
    if attendre_seul:
        fin = attend(pg, "()=>!document.getElementById('guide')", 60, 100); t1 = pg.evaluate("()=>performance.now()")
        juge('[%s · %s] 3 s sans toucher : le guide se termine, les flaques se vident' % (T, ch), bool(fin) and 2800 <= t1 - t0 <= 5600, '%.0f ms' % (t1 - t0))
    else:
        pg.wait_for_timeout(600); tap_pt(pg, 200, 560)
        fin = attend(pg, "()=>!document.getElementById('guide')", 40, 100)
        juge('[%s · %s] un toucher : le guide se termine' % (T, ch), bool(fin))
    juge('[%s · %s] l\'accueil reste net (rien du guide), promi_guide « 1 »' % (T, ch), pg.evaluate("()=>!document.getElementById('guide') && localStorage.getItem('promi_guide')==='1' && !document.getElementById('device').className.match(/guide-/)"))
def partager(pg, T, ch):
    z = pg.evaluate("()=>(window._guide && _guide.etat().trou) || null")
    if not z: juge('[%s · %s] Partager touché : la zone nette de Partager existe' % (T, ch), False, 'aucune zone'); return False
    tap_pt(pg, z['x'], z['y'])
    ouv = attend(pg, "()=>{ const s=document.getElementById('shareScreen'); if(!s||!s.classList.contains('show')) return false; const r=s.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return r.top<d.top+60 && r.bottom>d.bottom-60; }", 40)
    juge('[%s · %s] Partager touché : Partager s\'ouvre' % (T, ch), bool(ouv))
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ const c=document.querySelector('#shareScreen .closeb')||document.querySelector('#shcTitre .f'); if(c) c.click(); }")
    return ouv
with sync_playwright() as p:
    b = p.webkit.launch()
    COMBOS = ((False, 390, 844, '1'), (True, 390, 844, '1'), (False, 330, 714, '0,79'), (True, 330, 714, '0,79'))
    _c = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--combo=')), None)
    for sombre, vw, vh, ech in ([COMBOS[int(_c)]] if _c is not None else COMBOS):
        T = '%s %s' % ('sombre' if sombre else 'clair', ech)
        ci = COMBOS.index((sombre, vw, vh, ech))
        for ich, ch in enumerate(('c', 'a', 'b')):
            ctx, pg, er = page(b, sombre, vw, vh)
            if not jusqu_au_plus(pg):
                juge('[%s · %s] le guide atteint l\'étape du +' % (T, ch), False, pg.evaluate(ETAT)); ctx.close(); continue
            pg.wait_for_timeout(700)
            if ch == 'c':
                tap_pt(pg, 200, 520)                                       # ailleurs que le +
            else:
                z = pg.evaluate("()=>_guide.etat().trou"); tap_pt(pg, z['x'], z['y'])   # le +
                ouv = attend(pg, "()=>{const c=document.getElementById('accChoix'); return !!(c&&c.classList.contains('ouvert'));}", 30)
                juge('[%s · %s] le + touché : le menu des natures s\'ouvre, le guide se retire' % (T, ch), bool(ouv))
                pg.wait_for_timeout(1600)
                if ch == 'a':
                    tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2500)
                    cs = pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')")
                    juge('[%s · %s] une page + ouverte : pas de clôture par-dessus' % (T, ch), cs and not pg.evaluate("()=>!!document.getElementById('guide')"))
                    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }")   # la page + fermée
                else:
                    tap_pt(pg, 200, 330)                                   # ailleurs : le menu se ferme
            phrase1(pg, T, ch)
            touche = (ci + ich) % 2 == 0   # v166 (§3.3) : sur chaque chemin, Partager touché dans deux combinaisons, pas touché dans les deux autres
            if touche:
                if partager(pg, T, ch): phrase2(pg, T, ch + ' · après Partager', attendre_seul=(ech == '1'))
            else:
                tap_pt(pg, 120, 560); phrase2(pg, T, ch + ' · ailleurs', attendre_seul=(ech != '1'))
            if ch == 'c':
                pg.reload(); pg.wait_for_timeout(9000)
                juge('[%s · %s] au lancement suivant, le guide ne revient pas' % (T, ch), not pg.evaluate("()=>!!document.getElementById('guide')") and pg.evaluate("()=>localStorage.getItem('promi_guide')") == '1')
            juge('[%s · %s] aucune erreur de page' % (T, ch), not [x for x in er if 'version.json' not in x], er[:2])
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
