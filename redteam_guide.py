#!/usr/bin/env python3
"""
redteam_guide.py — LE GUIDE D'ACCUEIL, REFAIT (v143, Tom, 12 oct. 2026 — C-094). Réécrit ; l'original de v142 : sauvegardes/redteam_guide-avant-v143.py
(il jugeait une découpe du flou réécrite à chaque image, 0,8 s après l'arrivée, et une étape du + qui n'arrivait qu'après le Studio vu ouvert).

LA DÉCISION, EN DUR :
  · LE MOMENT : le guide démarre seulement quand l'accueil est entièrement posé et que plus rien ne bouge (onboarding refermé, Toile rendue),
    puis 1,2 s de calme ;
  · LA TECHNIQUE : le rayon du flou n'est JAMAIS animé (4,8 px, constant) ; le flou est révélé à travers des formes à bord doux qui grandissent
    PAR `transform`, courbe douce (ease-in-out), et se rejoignent en 1,6 s ; aucune image au-delà de 16,7 ms de travail ; la page n'écrit rien
    image par image (les formes ne sont pas retouchées pendant qu'elles grandissent) ;
  · le Studio : net, icône et mot agrandis de 15 % ; « Choisis d’abord le monde qui te ressemble, au Studio. » (impératif VOULU : exception de A3) ;
  · l'étape du + vient TOUJOURS ensuite — Studio refermé avec un choix, Studio refermé sans choix, ou toucher ailleurs pendant l'étape du
    Studio ; net sur le + et son encart (+10 %) ; « Promi, Chiche ou Cercle : tout commence par ce +. » ; seul « Plus tard » arrête tout.
Le premier chemin part d'un STOCKAGE VIERGE et joue l'onboarding entier au doigt (CDP) ; les autres rejouent le guide comme « Revoir la
présentation » (`_guide.attend(true)`), à 390 × 844 ×3. « Flou » et « net » se jugent sur l'IMAGE (l'énergie des contours d'une zone).
Captures : planche-v143/guide-<étape>-<thème>-<ms>.png à 0, 0,4, 0,8, 1,2 et 1,6 s.     Usage : python3 redteam_guide.py [--fichier=…] [--vite]
"""
import io, os, re, sys, time, json
from playwright.sync_api import sync_playwright
from PIL import Image
F = 'app.html'
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
VITE = '--vite' in sys.argv
URL = 'http://127.0.0.1:8752/' + F
PH_STUDIO = 'Choisis d\u2019abord le monde qui te ressemble, au Studio.'      # les mots de Tom, en dur
PH_PLUS = 'Promi, Chiche ou Cercle : tout commence par ce +.'
ATTENTE, INSTALLE, FLOU = 1200, 1600, '4.8'
os.makedirs('planche-v143', exist_ok=True)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('  %s %-118s %s' % ('✅' if cond else '❌', nom, str(detail)[:260]), flush=True)
DEV = "()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}"
ETAT = """()=>{ const g=document.getElementById('guide'), f=document.getElementById('guideFlou'), p=document.getElementById('guidePhrase'), t=document.getElementById('guideTard'), n=document.getElementById('guideNet');
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const B=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k].map(v=>Math.round(v*10)/10); };
  const cs=e=>e?getComputedStyle(e):null; const T=[...document.querySelectorAll('#guide .gd-t')];
  const tous=[...document.querySelectorAll('#guide, #guide *')].map(e=>{const c=getComputedStyle(e); return {id:e.id, cl:(e.className&&e.className.baseVal===undefined)?e.className:'', eng:e.getAttribute('data-eng'), op:+c.opacity, trp:c.transitionProperty, trd:c.transitionDuration, an:c.animationName};});
  const acc=(()=>{ const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.45); return h?(h.closest('.screen')?'ecran:'+h.closest('.screen').id:(h.closest('#guide')?'guide':(h.closest('.sheet,.poster')?'feuille':'accueil'))):null; })();
  const orig=i=>{ const e=document.getElementById(i); if(!e) return null; const v=e.style.visibility; e.style.visibility='visible'; const b=B(e); e.style.visibility=v; return b; };
  return {guide:g?g.getAttribute('data-guide'):null, entier:!!(g&&g.getAttribute('data-entier')), flou:f?(cs(f).backdropFilter||cs(f).webkitBackdropFilter):null, clip:f?(f.style.clipPath||''):'',
    formes:T.length, formesFlou:T.map(e=>cs(e).backdropFilter||cs(e).webkitBackdropFilter), formesMasque:T.map(e=>(cs(e).maskImage||cs(e).webkitMaskImage||'').slice(0,40)), formesTr:T.map(e=>[cs(e).transitionProperty, cs(e).transitionTimingFunction, cs(e).transitionDuration]),
    phrase:p?p.textContent:null, phraseVue:p?cs(p).visibility:null, phraseB:B(p), phraseCol:p?cs(p).color:null, tard:t?t.textContent:null, tardB:B(t), tardDeco:t?cs(t).textDecorationLine:null, tardFs:t?cs(t).fontSize:null,
    net:B(n), studioO:orig('studioBtn'), plusO:orig('createBtn'), tous:tous, devant:acc, e:(window._guide?window._guide.etat():null), regle:(window._guide?window._guide.regle:null), vu:localStorage.getItem('promi_guide'),
    studio:(()=>{const s=document.getElementById('studioScreen'); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.6); return !!(s&&h&&s.contains(h));})(),
    choix:!!(document.getElementById('accChoix')&&document.getElementById('accChoix').classList.contains('ouvert')), cs:!!document.querySelector('#createSheet.show'),
    textes:(window.TEXTES_ENGAGEMENT&&window.TEXTES_ENGAGEMENT.guide)||null, voulu:(window.TEXTES_ENGAGEMENT&&window.TEXTES_ENGAGEMENT.imperatifVoulu)||null, onb:!!(document.getElementById('onbV')), monde:(()=>{try{return Toile.getTheme()}catch(e){return null}})() }; }"""
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
def cap(pg, nom):
    d = pg.evaluate(DEV); pg.screenshot(path='planche-v143/guide-%s.png' % nom, clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})
# le relevé se fait DANS la page, à chaque image : le dernier instant où quelque chose BOUGEAIT (l'onboarding encore là, la Toile qui tourne, un
# doigt), l'instant où le guide paraît, où ses formes partent, où le flou est entier ; et chaque écriture de style sur une forme pendant qu'elle grandit
SONDE = """window.__g={bouge:0,tG:0,tDep:0,tEnt:0,ecrits:0,flous:{}}; (function b(){ try{ var n=performance.now(), g=document.getElementById('guide'), o=document.getElementById('onbV');
    var run=false; try{ var st=window.Toile_state&&Toile_state(); run=!!(st&&st.running); }catch(e){}
    if(!g && (o || run)) window.__g.bouge=n;
    if(g && !window.__g.tG){ window.__g.tG=n; try{ performance.mark('lever'); }catch(_){}
      try{ new MutationObserver(function(L){ L.forEach(function(m){ if(m.target.classList && m.target.classList.contains('gd-t') && window.__g.tDep && !window.__g.tEnt) window.__g.ecrits++; }); }).observe(g,{attributes:true,subtree:true,attributeFilter:['style']}); }catch(_){} }
    if(g && !window.__g.tDep && g.getAttribute('data-depart')) window.__g.tDep=n;
    if(g && !window.__g.tEnt && g.getAttribute('data-entier')) window.__g.tEnt=n;
    if(g && !window.__g.tEnt){ [].forEach.call(g.querySelectorAll('.gd-t'), function(e){ var f=getComputedStyle(e).backdropFilter||getComputedStyle(e).webkitBackdropFilter; window.__g.flous[f]=1; }); }
    if(!g){ window.__g.tG=0; window.__g.tDep=0; window.__g.tEnt=0; window.__g.ecrits=0; }
  }catch(e){} requestAnimationFrame(b); })();
  ['touchstart','touchend','pointerdown'].forEach(function(t){ document.addEventListener(t,function(){ if(!document.getElementById('guide')) window.__g.bouge=performance.now(); },true); });"""
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
    x, y = pt(pg, 195, 300); toucher(cdp, pg, x, y); pg.wait_for_timeout(900)          # le message de fin : un toucher → le compte
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
def images(trace, debut_nom='lever'):
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
        if a < t0 or a > t0 + 1900000: continue
        out.append(sum(max(0, min(b_, y) - max(a, x)) for x, y in taches if y > a and x < b_) / 1000.0)
    return out


def net_et_flou(pg, e, nette, quoi, T):
    """l'image : tout est flou sauf l'entrée, nette et agrandie"""
    im = image(pg)
    zones = {'le mot-marque': (30, 48, 150, 92), 'les icônes du plateau': (210, 48, 360, 92), 'INDEX': (246, 730, 288, 792), 'FIL': (300, 730, 342, 792)}
    zones.update({'AURA': (112, 736, 146, 792), 'le +': (160, 725, 230, 795)} if quoi == 'studio' else {'STUDIO': (48, 730, 92, 792), 'AURA': (112, 736, 146, 792)})
    r = {n: (energie(nette, *z), energie(im, *z)) for n, z in zones.items()}
    juge('[%s] %s · tout est flou : le plateau et les autres entrées perdent leurs contours (≤ 62 %% de l\'énergie d\'avant)' % (T, quoi), all(ap <= av * 0.62 for av, ap in r.values()), ' · '.join('%s %.1f→%.1f' % (n, a, p) for n, (a, p) in r.items()))
    o = e['studioO'] if quoi == 'studio' else e['plusO']; n = e['net']; gr = 1.15 if quoi == 'studio' else 1.10
    rap = (n[2] / o[2]) if (n and o and o[2]) else 0
    if quoi == 'studio':
        # les zones suivent les boîtes réelles : l'entrée d'origine (o) dans l'image nette, sa copie agrandie (n) dans l'image du guide ; le haut = l'icône,
        # le bas = le mot. Agrandie de 15 %, la même encre s'étale sur 32 % de surface en plus : sa densité de contours baisse d'autant (≈ 87 %) — le seuil est 70 %.
        ic0, ic = energie(nette, o[0], o[1], o[0] + o[2], o[1] + o[3] * 0.62), energie(im, n[0], n[1], n[0] + n[2], n[1] + n[3] * 0.62)
        mot0, mot = energie(nette, o[0], o[1] + o[3] * 0.62, o[0] + o[2], o[1] + o[3] + 3), energie(im, n[0], n[1] + n[3] * 0.62, n[0] + n[2], n[1] + n[3] + 3)
        juge('[%s] studio · l\'icône ET le mot STUDIO sont nets (≥ 70 %% de leur densité de contours), agrandis de 15 %% (13 à 17)' % T, ic >= ic0 * 0.70 and mot >= mot0 * 0.70 and gr - 0.02 <= rap <= gr + 0.02, 'icône %.1f → %.1f · mot %.1f → %.1f · largeur %s → %s (× %.3f)' % (ic0, ic, mot0, mot, o and o[2], n and n[2], rap))
    else:
        # comme pour le Studio : les zones suivent les boîtes réelles (l'original dans l'image nette, sa copie agrandie dans l'image du guide) ; agrandie
        # de 10 %, la même encre s'étale sur 21 % de surface en plus — le seuil est 70 % de la densité de contours
        # … et le CŒUR des boîtes (72 %) : aux coins de la boîte du + passent le bord et le fond de la barre, qui, eux, sont floutés (en sombre ils pesaient
        # plus que le + lui-même : 3,4 → 2,4 alors que le + est net sur la capture)
        ce = lambda b: (b[0] + b[2] * 0.14, b[1] + b[3] * 0.14, b[0] + b[2] * 0.86, b[1] + b[3] * 0.86)
        av, ap = energie(nette, *ce(o)), energie(im, *ce(n))
        juge('[%s] plus · le + et son encart sont nets (≥ 70 %% de leur densité de contours), agrandis de 10 %% (8 à 12)' % T, ap >= av * 0.70 and gr - 0.02 <= rap <= gr + 0.02, 'le + %.1f → %.1f · largeur %s → %s (× %.3f)' % (av, ap, o and o[2], n and n[2], rap))

def technique(pg, e_mi, g, T, quoi):
    juge('[%s] %s · six formes portent le flou des murs, CONSTANT (4,8 px — jamais un autre rayon pendant la révélation)' % (T, quoi), e_mi['formes'] == 6 and list(g['flous'].keys()) == ['blur(%spx)' % FLOU], 'formes %s · rayons vus pendant la révélation : %s' % (e_mi['formes'], list(g['flous'].keys())))
    juge('[%s] %s · bord doux (un dégradé radial en masque) ; elles grandissent par `transform` seul, courbe douce (ease-in-out)' % (T, quoi),
         e_mi['formes'] == 6 and all('radial-gradient' in m for m in e_mi['formesMasque']) and all(t[0] == 'transform' and 'cubic-bezier(0.65, 0, 0.35, 1)' in t[1] for t in e_mi['formesTr']) and not e_mi['clip'],
         'masque %s · transition %s' % (e_mi['formesMasque'][:1], e_mi['formesTr'][:1]))
    juge('[%s] %s · la page n\'écrit rien image par image : aucune forme retouchée pendant qu\'elle grandit' % (T, quoi), g['ecrits'] == 0, '%d écriture(s) de style sur les formes entre le départ et le flou entier' % g['ecrits'])
    d = (g['tEnt'] - g['tDep']) / 1000.0 if (g['tEnt'] and g['tDep']) else None
    juge('[%s] %s · elles se rejoignent en 1,6 s : le flou est entier 1,6 à 2,0 s après leur départ' % (T, quoi), d is not None and 1.6 <= d <= 2.0, 'durée %s s · relevé %s' % (None if d is None else round(d, 2), {k: (round(v) if isinstance(v, (int, float)) else v) for k, v in g.items() if k != 'flous'}))

def a2(e, T):
    tr = lambda x: x['trd'] not in ('0s', '') and any(float(v.replace('ms', 'e-3').replace('s', '')) > 0 for v in x['trd'].split(', '))
    fautifs = [x for x in e['tous'] if x['op'] < 1 or x['an'] not in ('none', '') or (tr(x) and 'gd-t' not in (x['cl'] or ''))]
    juge('[%s] A2, avec son exception nommée : aucune opacité, aucune animation ; une transition sur les six formes du flou SEULES ; tout porte `data-eng`' % T, not fautifs and all(x['eng'] for x in e['tous']), '%s' % (fautifs[:2] or [x['id'] or x['cl'] for x in e['tous'] if not x['eng']][:3]))

def premier_lancement(b, th):
    """stockage vierge, onboarding entier au doigt, puis : le Studio, un CHOIX au Studio, le Studio refermé → l'étape du + → le +"""
    T = 'clair' if th == 'light' else 'sombre'; print('\n── premier lancement, %s : onboarding entier, choix au Studio' % T)
    ctx, pg, cdp = ouvre(b, th); onboarding(pg, cdp)
    nette = None
    for _ in range(60):
        if pg.evaluate("()=>!document.getElementById('onbV')"): pg.wait_for_timeout(200); e0 = pg.evaluate(ETAT); nette = image(pg); break   # l'état d'abord (une capture ×3 dure plusieurs dixièmes de seconde : le guide part 1,2 s après l'arrivée)
        pg.wait_for_timeout(50)
    else: e0 = pg.evaluate(ETAT)
    juge('[%s] à l\'arrivée sur l\'accueil rien n\'est flou, la barre est complète' % T, not e0['guide'] and e0['studioO'] and e0['plusO'], 'guide %s' % e0['guide'])
    mi = None; t0 = time.time()
    while time.time() - t0 < 12:
        e = pg.evaluate(ETAT)
        if e['guide'] and e['formes'] == 6 and not e['entier'] and e['formesTr'] and e['formesTr'][0][0] == 'transform': mi = e; break
        if e['guide'] and e['entier']: break
        pg.wait_for_timeout(40)
    e = attend(pg, 'studio', 9000); g = pg.evaluate("()=>window.__g")
    calme = (g['tG'] - g['bouge']) / 1000.0 if g['tG'] else None
    juge('[%s] LE MOMENT : le guide paraît après 1,2 s de calme — plus rien ne bougeait depuis 1,15 à 2,5 s (onboarding refermé, Toile au repos, aucun doigt)' % T, calme is not None and 1.15 <= calme <= 2.5, 'calme avant le guide : %s s' % (None if calme is None else round(calme, 2)))
    if mi: technique(pg, mi, g, T, 'studio')
    else: juge('[%s] studio · les formes ont été vues pendant la révélation' % T, False, 'aucun relevé à mi-chemin')
    pg.wait_for_timeout(200); e = pg.evaluate(ETAT); cap(pg, '1-studio-%s' % T)
    juge('[%s] le flou entier est UNE couche, à 4,8 px, sans découpe' % T, e['entier'] and e['formes'] == 0 and ('blur(%spx)' % FLOU) in (e['flou'] or '') and not e['clip'], '%s · formes restantes %s' % (e['flou'], e['formes']))
    if nette: net_et_flou(pg, e, nette, 'studio', T)
    juge('[%s] la phrase du Studio, mot pour mot, visible, au milieu de l\'écran' % T, e['phrase'] == PH_STUDIO and e['phraseVue'] == 'visible' and e['phraseB'] and abs((e['phraseB'][1] + e['phraseB'][3] / 2) - 392) <= 30, '« %s » %s' % (e['phrase'], e['phraseB']))
    juge('[%s] A3 : l\'impératif de cette phrase est une exception NOMMÉE (TEXTES_ENGAGEMENT.imperatifVoulu) ; l\'autre phrase n\'en a pas' % T, PH_STUDIO in (e['voulu'] or []) and (e['textes'] or {}).get('plus') == PH_PLUS and not re.search(r'\b(Choisis|Touche|Trace|Plante|Tiens|Va|Ouvre)\b', PH_PLUS), '%s' % e['voulu'])
    juge('[%s] « Plus tard » : visible, 12 px, sans soulignement' % T, e['tard'] == 'Plus tard' and e['tardB'] and e['tardFs'] == '12px' and e['tardDeco'] == 'none', '%s %s' % (e['tard'], e['tardB']))
    a2(e, T)
    # toucher le Studio → le Studio ; y faire un CHOIX (un autre monde) ; le refermer
    x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2800); e3 = pg.evaluate(ETAT)
    juge('[%s] toucher le Studio net ouvre le Studio ; le flou n\'est plus là, l\'entrée de la barre est rendue' % T, e3['studio'] and not e3['guide'] and pg.evaluate("()=>getComputedStyle(document.getElementById('studioBtn')).visibility")=='visible', 'Studio %s · guide %s' % (e3['studio'], e3['guide']))
    m0 = e3['monde']; x0, y0 = pt(pg, 300, 330); x1, y1 = pt(pg, 80, 330)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]})
    for i in range(1, 11): pg.wait_for_timeout(18); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * i / 10, 'y': y0}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1800)
    m1 = pg.evaluate("()=>{try{return Toile.getTheme()}catch(e){return null}}")
    c = centre(pg, '#studioScreen .closeb')
    if c: toucher(cdp, pg, c[0], c[1])
    e4 = attend(pg, 'plus', 12000); g4 = pg.evaluate("()=>window.__g"); pg.wait_for_timeout(200); e4 = pg.evaluate(ETAT); cap(pg, '2-plus-%s' % T)
    juge('[%s] CHEMIN 1 — un choix au Studio (monde %s → %s), Studio refermé : l\'étape du + arrive, sa phrase mot pour mot' % (T, m0, m1), e4['guide'] == 'plus' and e4['phrase'] == PH_PLUS and m1 != m0, 'guide %s · « %s »' % (e4['guide'], e4['phrase']))
    if e4['guide'] == 'plus':
        d = (g4['tEnt'] - g4['tDep']) / 1000.0 if (g4['tEnt'] and g4['tDep']) else None
        juge('[%s] plus · la même révélation (six formes, 1,6 à 2,0 s)' % T, d is not None and 1.6 <= d <= 2.0 and g4['ecrits'] == 0, 'durée %s s · écritures %s' % (d and round(d, 2), g4['ecrits']))
        nette2 = None
        if e4['e'] and e4['e']['trou']:
            pg.evaluate("()=>{ window.__gg=document.getElementById('guide'); window.__gg.style.display='none'; var o=document.getElementById('createBtn'); window.__v=o.style.visibility; o.style.visibility='visible'; }"); pg.wait_for_timeout(120); nette2 = image(pg)
            pg.evaluate("()=>{ window.__gg.style.display=''; document.getElementById('createBtn').style.setProperty('visibility','hidden','important'); }"); pg.wait_for_timeout(150)
        if nette2: net_et_flou(pg, e4, nette2, 'plus', T)
        x, y = pt(pg, e4['e']['trou']['x'], e4['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(900); e5 = pg.evaluate(ETAT)
        juge('[%s] toucher le + ouvre les trois natures ; le guidage est fini, le + de la barre est rendu' % T, (e5['choix'] or e5['cs']) and not e5['guide'] and e5['vu'] == '1' and pg.evaluate("()=>getComputedStyle(document.getElementById('createBtn')).visibility")=='visible', 'natures %s · guide %s' % (e5['choix'], e5['guide']))
    pg.reload(); pg.wait_for_timeout(8500); e6 = pg.evaluate(ETAT)
    juge('[%s] une seule fois : après un rechargement, ni onboarding ni guide' % T, not e6['guide'] and not e6['onb'], 'guide %s · devant %s' % (e6['guide'], e6['devant']))
    juge('[%s] aucune erreur de page' % T, not pg.__dict__['er'], pg.__dict__['er'][:2]); ctx.close()

def rejoue(b, th):
    ctx, pg, cdp = ouvre(b, th, vierge=False); pg.evaluate("()=>{ localStorage.removeItem('promi_guide'); _guide.attend(true); }"); return ctx, pg, cdp
def chemins(b):
    print('\n── les autres chemins (le guide rejoué)')
    # 2 · Studio refermé SANS choix
    ctx, pg, cdp = rejoue(b, 'light'); e = attend(pg, 'studio', 12000); x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2800)
    c = centre(pg, '#studioScreen .closeb'); toucher(cdp, pg, c[0], c[1]) if c else None; e2 = attend(pg, 'plus', 12000)
    juge('CHEMIN 2 — Studio refermé sans choix : l\'étape du + arrive', e['guide'] == 'studio' and e2['guide'] == 'plus' and e2['phrase'] == PH_PLUS, 'guide %s → %s' % (e['guide'], e2['guide'])); ctx.close()
    # 3 · toucher ailleurs pendant l'étape du Studio
    ctx, pg, cdp = rejoue(b, 'light'); e = attend(pg, 'studio', 12000); x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y); pg.wait_for_timeout(500); e2 = pg.evaluate(ETAT)
    juge('CHEMIN 3 — toucher ailleurs pendant l\'étape du Studio : l\'étape du + vient ensuite, le flou reste', e['guide'] == 'studio' and e2['guide'] == 'plus' and e2['phrase'] == PH_PLUS and e2['entier'] and not e2['studio'], 'guide %s → %s · flou entier %s' % (e['guide'], e2['guide'], e2['entier']))
    x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y); pg.wait_for_timeout(1100); e3 = pg.evaluate(ETAT); pg.wait_for_timeout(3500); e4 = pg.evaluate(ETAT)
    juge('à l\'étape du +, toucher ailleurs retire le flou et finit le guidage (il ne se reforme pas)', not e3['guide'] and not e4['guide'] and e4['devant'] == 'accueil', 'guide %s puis %s · devant %s' % (e3['guide'], e4['guide'], e4['devant'])); ctx.close()
    # 4 · « Plus tard » arrête tout
    ctx, pg, cdp = rejoue(b, 'light'); e = attend(pg, 'studio', 12000); c = centre(pg, '#guideTard'); toucher(cdp, pg, c[0], c[1]) if c else None
    pg.wait_for_timeout(1100); e2 = pg.evaluate(ETAT); pg.wait_for_timeout(5000); e3 = pg.evaluate(ETAT)
    juge('« Plus tard » arrête tout : le flou se retire, aucune étape du + ne vient (6 s), l\'accueil est là', e['guide'] == 'studio' and not e2['guide'] and not e3['guide'] and e3['devant'] == 'accueil' and e3['e']['etat'] is None, 'guide %s → %s → %s · état %s' % (e['guide'], e2['guide'], e3['guide'], e3['e']['etat']))
    pg.reload(); pg.wait_for_timeout(8000); e4 = pg.evaluate(ETAT)
    juge('« Plus tard » : après un rechargement, il ne revient pas', not e4['guide'], 'guide %s' % e4['guide']); ctx.close()
    # 5 · Réduire les animations
    ctx, pg, cdp = ouvre(b, 'light', True, vierge=False); pg.evaluate("()=>{ localStorage.removeItem('promi_guide'); _guide.attend(true); }"); t0 = time.time(); L = []
    while time.time() - t0 < 8:
        e = pg.evaluate(ETAT)
        if e['guide']: L.append((e['entier'], e['formes']))
        if len(L) >= 6: break
        pg.wait_for_timeout(40)
    juge('Réduire les animations : le flou est posé sans mouvement (entier dès la première image, aucune forme)', len(L) >= 6 and all(a and f == 0 for a, f in L), '%s' % L[:6]); ctx.close()

def installation(b, th):
    """le travail du fil principal par image pendant la révélation (trace), puis les captures à 0 / 0,4 / 0,8 / 1,2 / 1,6 s, les deux étapes"""
    T = 'clair' if th == 'light' else 'sombre'; print('\n── la révélation, %s : mesure des images et captures' % T)
    for etape in ('studio', 'plus'):
        ctx, pg, cdp = ouvre(b, th, vierge=False)
        if not pg.evaluate("()=>!!(window._guide&&_guide.montre)"): juge('[%s] %s · le guide se rejoue' % (T, etape), False); ctx.close(); continue
        b.start_tracing(page=pg, categories=['toplevel', 'devtools.timeline', 'disabled-by-default-devtools.timeline', 'blink.user_timing'])
        pg.evaluate("(q)=>{ _guide.montre(q); }", etape); pg.wait_for_timeout(2300)
        tr = json.loads(b.stop_tracing().decode('utf-8')); W = images(tr) or []; pire = max(W) if W else None; W2 = sorted(W)
        juge('[%s] %s · pendant la révélation, aucune image au-delà de 16,7 ms de travail du fil principal' % (T, etape), bool(W) and len(W) >= 40 and sum(W) > 2 and pire <= 16.7, '%d images · travail total %.0f ms · pire %s ms · p95 %s ms' % (len(W), sum(W), None if pire is None else round(pire, 1), round(W2[int(len(W2) * .95)], 1) if W2 else None))
        pg.evaluate("()=>{ _guide.finir(); }"); pg.wait_for_timeout(900); pg.evaluate("(q)=>{ _guide.montre(q); }", etape); pg.wait_for_timeout(120)
        for ms in (0, 400, 800, 1200, 1600):
            pg.evaluate("(ms)=>{ _guide.figeA(ms); }", ms); pg.wait_for_timeout(160); cap(pg, '%s-%s-%04d' % (etape, T, ms))
        ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    premier_lancement(b, 'light'); installation(b, 'light')
    if not VITE:
        chemins(b); premier_lancement(b, 'dark'); installation(b, 'dark')
    b.close()
ok = sum(1 for _, c in res if c)
print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
