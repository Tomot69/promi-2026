#!/usr/bin/env python3
"""
redteam_onboarding.py — L'ONBOARDING REFAIT : PRÉNOM → PREMIER TRAIT → LA TOILE.

Écrit AVANT l'intégration (21 sept. 2026), et prouvé ROUGE sur la version d'aujourd'hui.

LES DÉCISIONS QU'IL PORTE (Tom, 21 sept. 2026 — écrites ici EN DUR, §7) :
  1 · on plante d'abord UNE PROMESSE À SOI-MÊME : « Je me promets de… » — ni contact, ni compte.
      On trace, la première dalle naît sous le doigt et se pose sur une TOILE VIDE.
  2 · les étapes d'aujourd'hui sont JETÉES : prénom → premier trait → la Toile. Le Chiche, la Nuée,
      le Studio, l'Aura se découvrent à l'usage — ni diapositive, ni tutoriel qui suit.
  3 · les notifications ne se demandent JAMAIS au lancement (iOS ne laisse demander qu'une fois).
  4 · le compte vient APRÈS le premier trait ; les mots : courts, complices, jamais d'exclamation.
  + le point de départ (onboarding-depart/) : rien de l'accueil sous l'onboarding, un écran plein ;
    le geste est celui du §5 (118 px, deux points) ; la dalle est la vraie, sur la vraie Toile ;
    rien ne survit (§8) ; le verrou `promi_onb` ; « Revoir la présentation » relance.

L'INTERFACE QUE L'APP DOIT DÉCLARER (des POIGNÉES pour poser le doigt, jamais des valeurs vérifiées) :
  #promiOnb [data-onb="prenom"]    le champ du prénom
  #promiOnb [data-onb="suite"]     ce qui fait passer du prénom au trait (sinon : Entrée)
  #promiOnb [data-onb="parole"]    le champ qui suit « Je me promets de »
  #promiOnb [data-onb="trait"]     la zone du geste ; elle déclare data-depart="x,y" et
                                   data-arrivee="x,y" (px de la zone) : la demi-courbe qu'elle MONTRE
  #promiOnb [data-onb="plus-tard"] (facultatif) remettre le compte à plus tard, après le trait

Tout geste est joué AU VRAI DOIGT (CDP `Input.dispatchTouchEvent`, contexte tactile, §8) ;
le fenêtrage 430 × 932 donne `#device` exactement 390 × 844 (§8, le comparateur qui redimensionne).

Usage :  python3 redteam_onboarding.py
"""
import io, json, re, sys, time
from playwright.sync_api import sync_playwright
from PIL import Image

import os
URL = os.environ.get("APP_ONB", "http://127.0.0.1:8752/app.html")
SEUIL_LUM = 42                  # §3 — du texte sur un fond
GESTE_H = 118                   # §5 — le geste, 118 px de haut
BANNIS = ['tâche', 'to-do', 'objectif', 'valider', 'urgent', 'score', 'brouillon', 'orbite', 'sphère',
          'échéance']            # §2
DIAPOS = ['deux vues', 'choisis un style', 'signal', 'ton noyau grandit', 'harmonie']   # les étapes jetées
COMPTE = re.compile(r'\b(apple|google|continuer avec|se connecter|créer un compte|conditions|mot de passe)\b', re.I)
PRENOM, PAROLE = 'Camille', 'marcher une heure'

# ⚑ v23 · les deux contrats du panneau de compte (Tom, 22 sept.)
C21 = "O21 au rejeu, le compte revient tant qu'il n'existe pas"
C22 = 'O22 une porte permanente vers le compte'
CENTRE = ("()=>{const r=document.getElementById('device').getBoundingClientRect();"
          "return {x:r.left+r.width/2, y:r.top+r.height*0.45};}")
RANGEE = """()=>{const c=document.getElementById('compteCard'); if(!c) return null;
  const s=getComputedStyle(c); if(s.display==='none'||s.visibility==='hidden'||+s.opacity<0.05) return {cache:true};
  const r=c.getBoundingClientRect(); if(r.width<2||r.height<2) return {cache:true};
  const D=document.getElementById('device').getBoundingClientRect();
  return {x:r.left+r.width/2, y:r.top+r.height/2, t:(c.innerText||'').trim(),
          dansLeCadre:(r.top>=D.top-1 && r.bottom<=D.bottom+1)};}"""
PANNEAU = """()=>{const p=document.querySelector('.onbv-compte'); if(!p) return null;
  const r=p.getBoundingClientRect(), s=getComputedStyle(p);
  const D=document.getElementById('device').getBoundingClientRect();
  const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
  return {vu:s.display!=='none'&&+s.opacity>0.5&&r.height>40,
          dans:r.left>=D.left-1&&r.right<=D.right+1&&r.bottom<=D.bottom+1,
          dessus:!!(h&&(p===h||p.contains(h))),
          t:(p.innerText||'').replace(/\\s+/g,' ').trim()};}"""

INIT = r"""(()=>{ window.__nd=0;
  try{ if(window.Notification){ Notification.requestPermission=function(){ window.__nd++; return Promise.resolve('default'); }; } }catch(e){}
})();"""

# ── lectures ─────────────────────────────────────────────────────────────────────────────
VIS = r"""(e)=>{ if(!e) return false; const c=getComputedStyle(e);
  if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false;
  const r=e.getBoundingClientRect(); const D=document.getElementById('device').getBoundingClientRect();
  if(r.width<2||r.height<2) return false;
  if(r.right<D.left+1||r.left>D.right-1||r.bottom<D.top+1||r.top>D.bottom-1) return false;
  let p=e; while(p&&p!==document.body){ const s=getComputedStyle(p); if(+s.opacity<0.05||s.display==='none') return false; p=p.parentElement; }
  return true; }"""

ONB = r"""()=>{ const o=document.getElementById('promiOnb'); const vis=%s;
  if(!o) return {existe:false};
  const txt=[...o.querySelectorAll('*')].filter(e=>vis(e)&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))
     .map(e=>[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').replace(/\s+/g,' ').trim());
  const ph=[...o.querySelectorAll('input,textarea')].filter(vis).map(e=>e.placeholder||'');
  return {existe:true, gone:o.classList.contains('gone'), vu:vis(o), textes:txt, places:ph, tout:(o.innerText||'').replace(/\s+/g,' '),
          points:[...o.querySelectorAll('.ob-dots,.ob-dot')].some(vis)}; }""" % VIS

# le chrome de l'accueil : ni visible, ni touchable sous l'onboarding
CHROME = ['#accPlat', '#accBarre', '#createBtn', '#studioBtn', '#souffleBtn', '#indexBtn', '#filBtn']
ACCUEIL = r"""(sels)=>{ const vis=%s; const o=document.getElementById('promiOnb'); const out=[];
  for(const s of sels){ const e=document.querySelector(s); if(!vis(e)) continue;
    const r=e.getBoundingClientRect(); const x=r.left+r.width/2, y=r.top+r.height/2;
    const h=document.elementFromPoint(x,y);
    /* couvert = le doigt tombe DANS l'onboarding, et ce qui est touché y est opaque (aplat ou canevas) */
    let couvert=false;
    if(h&&o&&o.contains(h)){ let p=h; while(p&&p!==o.parentElement){ const c=getComputedStyle(p);
        if(p.tagName==='CANVAS'||/rgb\(|rgba\(.*, 1\)/.test(c.backgroundColor)&&!/rgba\(.*, 0(\.\d+)?\)/.test(c.backgroundColor)){couvert=true;break;}
        p=p.parentElement; } }
    if(!couvert) out.push(s+(h&&o&&o.contains(h)?' (sous un voile transparent)':' (touchable)'));
  } return out; }""" % VIS

POIGNEE = r"""(q)=>{ const vis=%s; const e=document.querySelector('#promiOnb '+q); if(!vis(e)) return null;
  const r=e.getBoundingClientRect(); const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  return {x:r.left+r.width/2, y:r.top+r.height/2, l:r.left, t:r.top, w:r.width/k, h:r.height/k, k:k,
          dep:e.getAttribute('data-depart'), arr:e.getAttribute('data-arrivee'), tag:e.tagName}; }""" % VIS

ETAT = r"""()=>{ const T=window.Toile; /* ⚠ `promises` est un `let` global : window.promises n'existe pas (22 sept.) */
  const pr=((typeof promises!=='undefined'&&promises)||[]).filter(p=>!p.draft);
  let res=null; try{ res=(T&&T.reserved)?T.reserved.length:0; }catch(e){}
  return {n:pr.length, colorees:(T&&T.colored)?T.colored():null, reserve:res,
          promis:pr.map(p=>({id:p.id,who:p.who,from:p.from,title:p.title,dalle:!!(T&&T.dalleAbs&&T.dalleAbs(p.id))})),
          nom:(window.USER||{}).name||null, verrou:(()=>{try{return localStorage.getItem('promi_onb');}catch(e){return null;}})(),
          notif:window.__nd||0, tuto:!!document.getElementById('tutoOv'),
          theme:document.getElementById('device').classList.contains('light')?'light':'dark'}; }"""

# les textes et le fond RÉELLEMENT peint autour d'eux (lu sur l'image, §8 : le fond d'un texte
# n'est pas son background-color)
TEXTES = r"""()=>{ const vis=%s; const o=document.getElementById('promiOnb'); if(!o) return [];
  return [...o.querySelectorAll('*')].filter(e=>vis(e)&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))
    .map(e=>{ const r=e.getBoundingClientRect(); const c=getComputedStyle(e);
      /* un texte posé sur un aplat opaque (un bouton, une pastille) se juge contre CET aplat */
      let bg=null, p=e; const D=document.getElementById('device').getBoundingClientRect();
      while(p&&p!==o.parentElement){ const s=getComputedStyle(p), q=p.getBoundingClientRect();
        if(q.width*q.height>0.5*D.width*D.height) break;
        const m=s.backgroundColor.match(/[\d.]+/g); if(m&&(m.length<4||+m[3]>0.95)){ bg=s.backgroundColor; break; }
        p=p.parentElement; }
      return {t:e.textContent.replace(/\s+/g,' ').trim().slice(0,40), x:r.left,y:r.top,w:r.width,h:r.height, bg:bg,
              c:c.webkitTextFillColor&&c.webkitTextFillColor!=='rgba(0, 0, 0, 0)'?c.webkitTextFillColor:c.color}; }); }""" % VIS


def rgb(s):
    m = re.findall(r'[\d.]+', s or '')
    return tuple(float(v) for v in m[:3]) if len(m) >= 3 else None


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(pg):
    """Δlum entre chaque texte et le fond peint dans un anneau de 3 px autour de sa boîte."""
    img = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
    dpr = img.width / pg.viewport_size['width']
    bas = []
    for t in pg.evaluate(TEXTES):
        c = rgb(t['c'])
        if not c:
            continue
        if t.get('bg'):
            d = abs(lum(c) - lum(rgb(t['bg'])))
            if d < SEUIL_LUM:
                bas.append('« %s » Δlum %.1f (sur son aplat)' % (t['t'], d))
            continue
        L = []
        for i in range(12):
            for (px, py) in ((t['x'] - 3 + (t['w'] + 6) * i / 11, t['y'] - 3), (t['x'] - 3 + (t['w'] + 6) * i / 11, t['y'] + t['h'] + 3),
                             (t['x'] - 3, t['y'] - 3 + (t['h'] + 6) * i / 11), (t['x'] + t['w'] + 3, t['y'] - 3 + (t['h'] + 6) * i / 11)):
                X, Y = int(px * dpr), int(py * dpr)
                if 0 <= X < img.width and 0 <= Y < img.height:
                    L.append(lum(img.getpixel((X, Y))))
        if not L:
            continue
        L.sort()
        d = abs(lum(c) - L[len(L) // 2])
        if d < SEUIL_LUM:
            bas.append('« %s » Δlum %.1f' % (t['t'], d))
    return bas


def toucher(cdp, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})


def tracer(cdp, z, jusqua=1.0):
    """Un trait AU DOIGT, horodaté par le CDP (§8 : l'instrument ne ralentit pas avec la page),
    en courbe quadratique de départ à arrivée — la demi-courbe que la zone montre."""
    def pt(s):
        a, b = [float(v) for v in s.split(',')]
        return z['l'] + a * z['k'], z['t'] + b * z['k']
    (x0, y0), (x1, y1) = pt(z['dep']), pt(z['arr'])
    cx, cy = (x0 + x1) / 2, min(y0, y1) - 18 * z['k']
    t0 = time.time()
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}], 'timestamp': t0})
    N = 24
    for i in range(1, int(N * jusqua) + 1):
        u = i / N
        x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1
        y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}], 'timestamp': t0 + 0.03 * i})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': t0 + 0.03 * (N + 1)})


def peint(pg, z):
    """Les deux points de la zone sont-ils peints ? On lit le canevas du geste sous chacun."""
    return pg.evaluate(r"""(a)=>{ const z=document.querySelector('#promiOnb [data-onb="trait"]');
      const cv=z&&(z.tagName==='CANVAS'?z:z.querySelector('canvas')); if(!cv||!cv.width) return [false,false];
      const g=cv.getContext('2d'); const r=cv.getBoundingClientRect(), zr=z.getBoundingClientRect();
      const k=cv.width/r.width;
      const lit=(s)=>{ const [x,y]=s.split(',').map(Number); const D=document.getElementById('device').getBoundingClientRect(), s2=D.width/390;
        const X=(zr.left+x*s2-r.left)*k, Y=(zr.top+y*s2-r.top)*k; let n=0;
        for(let dx=-6;dx<=6;dx+=3) for(let dy=-6;dy<=6;dy+=3){ const d=g.getImageData(Math.round(X+dx*k),Math.round(Y+dy*k),1,1).data; if(d[3]>40) n++; }
        return n>0; };
      return [lit(a[0]), lit(a[1])]; }""", [z['dep'], z['arr']])


def un_theme(pw, theme):
    R = {}          # contrat -> [échecs]  (liste vide = tenu ; None = non joué)

    def ko(c, m):
        R.setdefault(c, []).append(m)

    def ok(c):
        R.setdefault(c, [])

    def non_joue(*cs):
        for c in cs:
            if c not in R:
                R[c] = None

    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    ctx.add_init_script(INIT)
    pg = ctx.new_page()
    cdp = ctx.new_cdp_session(pg)
    pg.goto(URL)
    pg.wait_for_timeout(6800)
    pg.evaluate("(t)=>{try{setTheme(t)}catch(e){}}", theme)
    pg.wait_for_timeout(600)
    vus = []

    def releve(etape):
        o = pg.evaluate(ONB)
        vus.append((etape, o))
        return o

    # O1 · il s'ouvre au premier lancement
    o = releve('ouverture')
    if not o['existe'] or o['gone'] or not o['vu']:
        ko('O1 s\'ouvre au premier lancement', 'onboarding absent ou fermé')
        b.close()
        return R
    ok('O1 s\'ouvre au premier lancement')

    def chrome(etape):
        for s in pg.evaluate(ACCUEIL, CHROME):
            ko('O2 rien de l\'accueil dessous', '%s · %s' % (etape, s))
        ok('O2 rien de l\'accueil dessous')

    def pas_de_compte(etape):
        o = pg.evaluate(ONB)
        for t in o['textes']:
            if COMPTE.search(t):
                ko('O4 pas de compte avant le premier trait', '%s · « %s »' % (etape, t[:50]))
        ok('O4 pas de compte avant le premier trait')

    def lisible(etape):
        for m in contraste(pg):
            ko('O17 les textes se lisent (Δlum ≥ 42)', '%s · %s' % (etape, m))
        ok('O17 les textes se lisent (Δlum ≥ 42)')

    chrome('ouverture'); pas_de_compte('ouverture'); lisible('ouverture')

    # O5 · le prénom, au doigt
    p = pg.evaluate(POIGNEE, '[data-onb="prenom"]')
    if not p:
        ko('O5 le prénom se saisit', 'aucun champ [data-onb="prenom"] visible')
        non_joue('O6 « Je me promets de » et la parole', 'O7 la zone du trait (§5)', 'O8 la Toile est vide avant le trait',
                 'O9 un trait interrompu ne plante rien', 'O10 le trait plante UN Promi à soi',
                 'O11 sa dalle est la seule de la Toile', 'O12 il se referme sur la Toile, sans reste',
                 'O13 aucun tutoriel ne suit', 'O15 la réserve de la Toile est vide', 'O16 le verrou est posé',
                 'O18 un rechargement ne relance pas, le Promi reste', 'O19 « Revoir la présentation » relance',
                 C21, C22)
    else:
        toucher(cdp, p['x'], p['y']); pg.wait_for_timeout(250)
        pg.keyboard.type(PRENOM, delay=40); pg.wait_for_timeout(200)
        s = pg.evaluate(POIGNEE, '[data-onb="suite"]')
        if s:
            toucher(cdp, s['x'], s['y'])
        else:
            pg.keyboard.press('Enter')
        pg.wait_for_timeout(1200)
        e = pg.evaluate(ETAT)
        if e['nom'] != PRENOM:
            ko('O5 le prénom se saisit', 'USER.name = %r' % e['nom'])
        ok('O5 le prénom se saisit')
        releve('après le prénom'); chrome('après le prénom'); pas_de_compte('après le prénom'); lisible('après le prénom')

        # O6 · « Je me promets de » et la parole
        o = pg.evaluate(ONB)
        # ⚠ instrument (22 sept.) : la phrase est répartie en plusieurs nœuds (pastille-verbe, « de »,
        #   pastille) — on lit son texte RENDU entier ; « d’ » est l'élision décidée par Tom.
        if not re.search(r'je me promets d(e|’)', o.get('tout', ''), re.I) and \
           not any(re.search(r'je me promets d(e|’)', t, re.I) for t in o['textes'] + o['places']):
            ko('O6 « Je me promets de » et la parole', '« Je me promets de » n\'est écrit nulle part')
        q = pg.evaluate(POIGNEE, '[data-onb="parole"]')
        if not q:
            ko('O6 « Je me promets de » et la parole', 'aucun champ [data-onb="parole"] visible')
        else:
            toucher(cdp, q['x'], q['y']); pg.wait_for_timeout(250)
            pg.keyboard.type(PAROLE, delay=30); pg.wait_for_timeout(400)
        ok('O6 « Je me promets de » et la parole')

        # O7 · la zone du trait
        z = pg.evaluate(POIGNEE, '[data-onb="trait"]')
        if not z or not z['dep'] or not z['arr']:
            ko('O7 la zone du trait (§5)', 'aucune zone [data-onb="trait"] visible, ou sans data-depart / data-arrivee')
            non_joue('O8 la Toile est vide avant le trait', 'O9 un trait interrompu ne plante rien', 'O10 le trait plante UN Promi à soi',
                     'O11 sa dalle est la seule de la Toile', 'O12 il se referme sur la Toile, sans reste', 'O13 aucun tutoriel ne suit',
                     'O15 la réserve de la Toile est vide', 'O16 le verrou est posé',
                     'O18 un rechargement ne relance pas, le Promi reste', 'O19 « Revoir la présentation » relance',
                     C21, C22)
        else:
            if abs(z['h'] - GESTE_H) > 3:
                ko('O7 la zone du trait (§5)', 'hauteur %.1f au lieu de %d' % (z['h'], GESTE_H))
            a, bb = peint(pg, z)
            if not a or not bb:
                ko('O7 la zone du trait (§5)', 'point de départ peint : %s · point d\'arrivée peint : %s' % (a, bb))
            ok('O7 la zone du trait (§5)')
            releve('le trait'); chrome('le trait'); pas_de_compte('le trait'); lisible('le trait')

            e = pg.evaluate(ETAT)
            if e['colorees'] != 0:
                ko('O8 la Toile est vide avant le trait', '%s dalles colorées' % e['colorees'])
            if e['n'] and any(p_['title'] != PAROLE for p_ in e['promis']):
                ko('O8 la Toile est vide avant le trait', '%d Promi déjà là (le jeu de démonstration ?)' % e['n'])
            ok('O8 la Toile est vide avant le trait')

            # O9 · un trait interrompu ne plante rien
            tracer(cdp, z, jusqua=0.35); pg.wait_for_timeout(1200)
            e = pg.evaluate(ETAT)
            if any(p_['title'] == PAROLE for p_ in e['promis']):
                ko('O9 un trait interrompu ne plante rien', 'un tiers de trait a planté')
            ok('O9 un trait interrompu ne plante rien')

            # O10 · le trait entier plante UN Promi, à soi
            z = pg.evaluate(POIGNEE, '[data-onb="trait"]') or z
            tracer(cdp, z); pg.wait_for_timeout(2600)
            e = pg.evaluate(ETAT)
            miens = [p_ for p_ in e['promis'] if p_['title'] == PAROLE]
            if e['n'] != 1 or len(miens) != 1:
                ko('O10 le trait plante UN Promi à soi', '%d Promi, dont %d avec la parole écrite' % (e['n'], len(miens)))
            elif miens[0]['who'] != 'Moi':
                ko('O10 le trait plante UN Promi à soi', 'destinataire %r au lieu de « Moi »' % miens[0]['who'])
            ok('O10 le trait plante UN Promi à soi')

            # ⚑ v21 (Tom, 22 sept.) — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION : « le message après le premier
            #   Promi reste jusqu'au toucher, ou au moins quatre secondes, et il dit : Le reste se découvre à ton
            #   rythme. » Ce juge attendait le panneau du compte SANS toucher. Original : sauvegardes/redteam_onboarding-avant-v21.py
            pg.wait_for_timeout(2800)          # 2,6 s déjà passées depuis le trait : on est à 5,4 s
            fin = pg.evaluate("()=>{const f=document.getElementById('onbFin');return f?{vu:getComputedStyle(f).display!=='none'&&+getComputedStyle(f).opacity>0.5,t:f.innerText}:null}")
            if not fin or not fin['vu']:
                ko('O20 le message reste (4 s, puis le toucher)', 'le message n\'est plus là 5,4 s après le trait')
            elif 'Le reste se découvre à ton rythme' not in (fin['t'] or '').replace('\u00a0', ' '):
                ko('O20 le message reste (4 s, puis le toucher)', 'le message ne dit pas « Le reste se découvre à ton rythme. »')
            if pg.evaluate(POIGNEE, '[data-onb="plus-tard"]'):
                ko('O20 le message reste (4 s, puis le toucher)', 'le panneau du compte est venu sans toucher')
            ok('O20 le message reste (4 s, puis le toucher)')
            pg.wait_for_timeout(1200)
            dd = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return {x:r.left+r.width/2,y:r.top+r.height*0.45}}")
            toucher(cdp, dd['x'], dd['y']); pg.wait_for_timeout(900)
            # le compte, s'il est proposé, se remet à plus tard
            for _ in range(10):
                pt = pg.evaluate(POIGNEE, '[data-onb="plus-tard"]')
                if pt:
                    lisible('le compte'); chrome('le compte')
                    toucher(cdp, pt['x'], pt['y']); pg.wait_for_timeout(1200)
                    break
                if pg.evaluate("()=>{const o=document.getElementById('promiOnb');return !o||o.classList.contains('gone');}"):
                    break
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(2500)

            # O11 · la dalle
            e = pg.evaluate(ETAT)
            miens = [p_ for p_ in e['promis'] if p_['title'] == PAROLE]
            if not miens or not miens[0]['dalle']:
                ko('O11 sa dalle est la seule de la Toile', 'le Promi planté n\'a pas de dalle sur la Toile')
            if e['colorees'] != 1:
                ko('O11 sa dalle est la seule de la Toile', '%s dalles colorées au lieu de 1' % e['colorees'])
            ok('O11 sa dalle est la seule de la Toile')

            # O12 · il se referme sur la Toile, sans reste
            restes = pg.evaluate(r"""()=>{ const vis=%s; const o=document.getElementById('promiOnb'); if(!o) return [];
                return [...o.querySelectorAll('*')].filter(vis).map(e=>e.id?'#'+e.id:(e.tagName+'.'+(e.className+'').split(' ')[0])).slice(0,6); }""" % VIS)
            if restes:
                ko('O12 il se referme sur la Toile, sans reste', 'encore visibles : ' + ', '.join(restes))
            if not pg.evaluate("(s)=>(%s)(document.querySelector(s))" % VIS, '#accPlat'):
                ko('O12 il se referme sur la Toile, sans reste', 'l\'accueil ne revient pas')
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(400)
            if pg.evaluate(r"""()=>{ const vis=%s; const o=document.getElementById('promiOnb'); return !!o&&[...o.querySelectorAll('*')].some(vis); }""" % VIS):
                ko('O12 il se referme sur la Toile, sans reste', 'un nœud de l\'onboarding reparaît après closeAll')
            ok('O12 il se referme sur la Toile, sans reste')

            e = pg.evaluate(ETAT)
            if e['tuto']:
                ko('O13 aucun tutoriel ne suit', '#tutoOv est ouvert')
            ok('O13 aucun tutoriel ne suit')
            if e['reserve']:
                ko('O15 la réserve de la Toile est vide', '%d zones réservées restent (elles éclaircissent les dalles, §8)' % e['reserve'])
            ok('O15 la réserve de la Toile est vide')
            if e['verrou'] != '1':
                ko('O16 le verrou est posé', 'promi_onb = %r' % e['verrou'])
            ok('O16 le verrou est posé')

            # O18 · rechargement
            pg.wait_for_timeout(1500)
            pg.reload(); pg.wait_for_timeout(6800)
            o = pg.evaluate(ONB); e = pg.evaluate(ETAT)
            if o.get('vu') and not o.get('gone'):
                ko('O18 un rechargement ne relance pas, le Promi reste', 'l\'onboarding revient au rechargement')
            if not any(p_['title'] == PAROLE for p_ in e['promis']):
                ko('O18 un rechargement ne relance pas, le Promi reste', 'le Promi planté a disparu')
            ok('O18 un rechargement ne relance pas, le Promi reste')

            # O19 · « Revoir la présentation », au doigt
            pg.evaluate("()=>{try{closeAll()}catch(e){}; document.getElementById('settingsScreen').classList.add('show');}")
            pg.wait_for_timeout(700)
            pg.evaluate("()=>{const r=document.getElementById('replayOnb'); if(r) r.scrollIntoView({block:'center'});}")
            pg.wait_for_timeout(500)
            r = pg.evaluate("()=>{const e=document.getElementById('replayOnb'); if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.left+r.width/2,y:r.top+r.height/2};}")
            if not r:
                ko('O19 « Revoir la présentation » relance', '#replayOnb absent des Réglages')
            else:
                toucher(cdp, r['x'], r['y']); pg.wait_for_timeout(1500)
                o = pg.evaluate(ONB); e = pg.evaluate(ETAT)
                if not o.get('vu') or o.get('gone'):
                    ko('O19 « Revoir la présentation » relance', 'l\'onboarding ne revient pas')
                else:
                    for s in pg.evaluate(ACCUEIL, CHROME):
                        ko('O19 « Revoir la présentation » relance', 'accueil dessous · ' + s)
                if not any(p_['title'] == PAROLE for p_ in e['promis']):
                    ko('O19 « Revoir la présentation » relance', 'le rejeu a effacé le Promi planté')
                # ⚑ v22 (Tom) : « la Toile doit être vide avant le premier trait » — au rejeu aussi
                if e['colorees'] != 0:
                    ko('O19 « Revoir la présentation » relance', 'au rejeu, la Toile n\'est pas vide : %s dalles colorées' % e['colorees'])
            ok('O19 « Revoir la présentation » relance')

            # ⚑ v23 (Tom, 22 sept.) — « Le panneau du compte doit apparaître à la fin de l'onboarding,
            #   ET TANT QU'AUCUN COMPTE N'EXISTE — pas seulement à la première ouverture. Quelqu'un qui a
            #   fait “Plus tard” doit pouvoir le retrouver. » On vient JUSTEMENT de faire « Plus tard »
            #   (O20) : le rejeu doit donc le reproposer, et les Réglages en garder la porte.
            # O21 · au rejeu, on rejoue jusqu'au bout, et le panneau revient
            # ⚠ instrument : AU REJEU le prénom est déjà connu — `demarrer(true)` va droit
            #   à la parole (`if(rejeu && nom) allerParole(false)`). On ne le redemande pas.
            pr = pg.evaluate(POIGNEE, '[data-onb="prenom"]')
            if pr:
                toucher(cdp, pr['x'], pr['y']); pg.wait_for_timeout(250)
                pg.keyboard.type(PRENOM, delay=20); pg.wait_for_timeout(200)
                s2 = pg.evaluate(POIGNEE, '[data-onb="suite"]')
                if s2:
                    toucher(cdp, s2['x'], s2['y'])
                else:
                    pg.keyboard.press('Enter')
                pg.wait_for_timeout(1100)
            if True:
                q2 = pg.evaluate(POIGNEE, '[data-onb="parole"]')
                if not q2:
                    ko(C21, "le rejeu n'offre pas le champ de la parole")
                else:
                    toucher(cdp, q2['x'], q2['y']); pg.wait_for_timeout(250)
                    pg.keyboard.type(PAROLE, delay=20); pg.wait_for_timeout(600)
                z2 = pg.evaluate(POIGNEE, '[data-onb="trait"]')
                if not z2:
                    ko(C21, 'pas de zone de trait au rejeu')
                else:
                    tracer(cdp, z2); pg.wait_for_timeout(6800)   # 1,9 s de message + 4 s d'attente
                    dd2 = pg.evaluate(CENTRE)
                    toucher(cdp, dd2['x'], dd2['y']); pg.wait_for_timeout(1500)
                    pt2 = pg.evaluate(POIGNEE, '[data-onb="plus-tard"]')
                    if not pt2:
                        ko(C21, "le rejeu passe le panneau alors qu'aucun compte n'existe")
                    else:
                        toucher(cdp, pt2['x'], pt2['y']); pg.wait_for_timeout(1400)
            ok(C21)

            # O22 · la porte permanente : la rangée « Garder ta Toile » des Réglages
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(500)
            pg.evaluate("()=>{const st=document.getElementById('settingsScreen'); if(st) st.classList.add('show');}")
            pg.wait_for_timeout(900)
            # ⚠ instrument : les Réglages sont LEUR PROPRE conteneur de défilement (§8) et la
            #   rangée vit à y ≈ 1174 — hors de l'appareil. On l'amène dans le cadre AVANT de
            #   poser le doigt, et on vérifie qu'elle y est (§8, « un balayage annonce 0 sur des
            #   cadres qu'il n'a pas regardés »).
            for _ in range(4):
                pg.evaluate("()=>{const c=document.getElementById('compteCard'); if(c) c.scrollIntoView({block:'center'});}")
                pg.wait_for_timeout(500)
                cc = pg.evaluate(RANGEE)
                if cc and not cc.get('cache') and cc.get('dansLeCadre'):
                    break
            if cc and not cc.get('cache') and not cc.get('dansLeCadre'):
                ko(C22, "la rangée ne peut pas être amenée dans l'appareil")
            if not cc:
                ko(C22, 'aucune rangée #compteCard aux Réglages')
            elif cc.get('cache'):
                ko(C22, "la rangée est masquée alors qu'aucun compte n'existe")
            elif 'garder ta toile' not in (cc.get('t') or '').lower():
                ko(C22, 'la rangée dit %r' % cc.get('t'))
            else:
                toucher(cdp, cc['x'], cc['y']); pg.wait_for_timeout(1600)
                pan = pg.evaluate(PANNEAU)
                if not pan or not pan['vu']:
                    ko(C22, "la rangée n'ouvre pas le panneau")
                elif not pan['dans']:
                    ko(C22, "le panneau sort de l'appareil")
                elif not pan['dessus']:
                    ko(C22, 'le panneau est ouvert mais recouvert (les Réglages passent devant)')
                elif 'garder ta toile' not in pan['t'].lower() or 'plus tard' not in pan['t'].lower():
                    ko(C22, 'le panneau dit %r' % pan['t'][:90])
            ok(C22)

    # O3 · ni diapositive ni mot banni, sur tout ce qui a été vu ; jamais d'exclamation
    for etape, o in vus:
        for t in o.get('textes', []) + o.get('places', []):
            tl = t.lower()
            for m in DIAPOS + BANNIS:
                if re.search(r'(^|[^a-zà-ÿ])' + re.escape(m) + r'($|[^a-zà-ÿ])', tl):
                    ko('O3 ni diapositive ni mot banni', '%s · « %s » (%s)' % (etape, t[:40], m))
            if '!' in t:
                ko('O3 ni diapositive ni mot banni', '%s · exclamation « %s »' % (etape, t[:40]))
        if o.get('points'):
            ko('O3 ni diapositive ni mot banni', '%s · des points de pagination' % etape)
    ok('O3 ni diapositive ni mot banni')

    # O14 · aucune demande de notifications
    try:
        n = pg.evaluate("()=>window.__nd||0")
    except Exception:
        n = 0
    if n:
        ko('O14 aucune demande de notifications', '%d demande(s)' % n)
    ok('O14 aucune demande de notifications')
    b.close()
    return R


def main():
    tout = {}
    with sync_playwright() as pw:
        for th in ('dark', 'light'):
            tout[th] = un_theme(pw, th)
    noms = sorted({c for R in tout.values() for c in R}, key=lambda c: int(re.match(r'O(\d+)', c).group(1)))
    tenus = 0
    total = 0
    print('=' * 86)
    print('  L\'ONBOARDING — prénom → premier trait → la Toile · au doigt · deux thèmes')
    print('=' * 86)
    for c in noms:
        for th in ('dark', 'light'):
            total += 1
            v = tout[th].get(c, None)
            if v == []:
                tenus += 1
                print('  ✅ %-50s %s' % (c, th))
            elif v is None:
                print('  ⬜ %-50s %s   non joué (une étape d\'avant manque)' % (c, th))
            else:
                print('  ❌ %-50s %s' % (c, th))
                for m in v[:4]:
                    print('       · ' + m)
                if len(v) > 4:
                    print('       · … et %d autres' % (len(v) - 4))
    print('=' * 86)
    print('\n  %s  %d / %d contrats tenus' % ('✅' if tenus == total else '❌', tenus, total))
    sys.exit(0 if tenus == total else 1)


if __name__ == '__main__':
    main()
