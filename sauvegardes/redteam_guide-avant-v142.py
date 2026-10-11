#!/usr/bin/env python3
"""
redteam_guide.py — LE GUIDE DE FIN DE PARCOURS (v141, Tom, 10 oct. 2026 — C-094). Il remplace E2bis (C-076).

LA DÉCISION, EN DUR (§7) :
  « Une seule fois, à la fin du premier parcours :
    1 · on arrive sur l'accueil, la première dalle est visible ; après environ 0,8 s, un flou couvre l'écran — la matière du flou des murs ;
        il s'installe en zones abstraites qui se remplissent et se rejoignent ; ni orange ni “Ma Parole !” ;
    2 · tout est flou, sauf l'icône du Studio, nette et un peu plus grosse ; au milieu : “Chacun sa matière. La tienne est au Studio.” ;
    3 · la toucher ouvre le Studio ;
    4 · au retour, le flou se reforme, net sur le + et son encart : “Tout le reste part d'ici.” ;
    5 · toucher le + ouvre la page +. Le guidage est fini.
    Garde-fous : toucher le flou ailleurs le dissout et finit le guidage ; un “Plus tard” discret, toujours visible ; une seule fois, sauf par
    “Revoir la présentation” ; avec Réduire les animations, le flou est posé sans mouvement ; phrases dans TEXTES_ENGAGEMENT, sans impératif. »
  La barre du bas est COMPLÈTE dès le départ (le dévoilement de v140 est retiré).

Stockage vierge, parcours complet AU VRAI DOIGT (CDP), clair et sombre. « Flou » et « net » se jugent sur l'IMAGE : l'énergie des contours
(écart moyen entre pixels voisins) d'une zone, avant le guide et pendant. Captures : planche-v141/guide-*.png.

Usage : python3 redteam_guide.py [--fichier=zz-av141.html] [--vite]
"""
import io, os, re, sys, time
from playwright.sync_api import sync_playwright
from PIL import Image
F = 'app.html'
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
VITE = '--vite' in sys.argv
URL = 'http://127.0.0.1:8752/' + F
PH_STUDIO = 'Chacun sa matière. La tienne est au Studio.'      # les mots de Tom, en dur
PH_PLUS = 'Tout le reste part d’ici.'
FLOU = 4.8                                                      # la valeur des murs (v105)
IMP = re.compile(r"(^|[.!?…:;]\s+|\n)(touche|ouvre|trace|plante|va|viens|choisis|essaie|regarde|découvre|commence|appuie|glisse|fais|dis|reviens|clique|tape)\b", re.I)
os.makedirs('planche-v141', exist_ok=True)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('  %s %-112s %s' % ('✅' if cond else '❌', nom, detail))

DEV = "()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}"
ETAT = """()=>{ const g=document.getElementById('guide'), f=document.getElementById('guideFlou'), p=document.getElementById('guidePhrase'), t=document.getElementById('guideTard');
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const B=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k].map(v=>Math.round(v*10)/10); };
  const cs=e=>e?getComputedStyle(e):null; const fl=cs(f);
  const eng=[...document.querySelectorAll('#guide, #guide *')].map(e=>{const c=getComputedStyle(e); return {id:e.id, eng:e.getAttribute('data-eng'), op:+c.opacity, tr:c.transitionDuration, an:c.animationName, col:c.color};});
  const acc=(()=>{ const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.45); return h?(h.closest('.screen')?'ecran:'+h.closest('.screen').id:(h.closest('#guide')?'guide':(h.closest('.sheet,.poster')?'feuille':'accueil'))):null; })();
  const barre=['studioBtn','souffleBtn','createBtn','indexBtn','filBtn'].map(i=>{const e=document.getElementById(i); if(!e) return null; const c=getComputedStyle(e), r=e.getBoundingClientRect(); return (c.display!=='none'&&c.visibility!=='hidden'&&r.width>8)?B(e):null;});
  return {guide:g?g.getAttribute('data-guide'):null, u:f?+f.getAttribute('data-u'):null, flou:fl?(fl.backdropFilter||fl.webkitBackdropFilter):null, masque:f?(f.style.maskImage||f.style.webkitMaskImage||'').length:0,
    phrase:p?p.textContent:null, phraseB:B(p), phraseCol:p?cs(p).color:null, tard:t?t.textContent:null, tardB:B(t), tardDeco:t?cs(t).textDecorationLine:null, tardFs:t?cs(t).fontSize:null,
    eng:eng, devant:acc, barre:barre, e:(window._guide?window._guide.etat():null), vu:localStorage.getItem('promi_guide'),
    studio:(()=>{const s=document.getElementById('studioScreen'); const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.6); return !!(s&&h&&s.contains(h));})(),
    choix:!!(document.getElementById('accChoix')&&document.getElementById('accChoix').classList.contains('ouvert')), cs:!!document.querySelector('#createSheet.show'),
    textes:(window.TEXTES_ENGAGEMENT&&window.TEXTES_ENGAGEMENT.guide)||null, onb:!!(document.getElementById('onbV')) }; }"""

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
    d = pg.evaluate(DEV); pg.screenshot(path='planche-v141/guide-%s.png' % nom, clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})

def ouvre(b, th, reduit=False):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True, reduced_motion=('reduce' if reduit else 'no-preference'))
    ctx.add_init_script("try{ if(!localStorage.getItem('promi_theme')) localStorage.setItem('promi_theme','%s'); }catch(e){}" % th)
    # le relevé se fait DANS la page, à chaque image (§8 : un instrument qui interroge la page depuis Python toutes les 300 ms ne voit pas un mouvement de 1,5 s)
    ctx.add_init_script("""window.__g={us:[],tArr:0,tG:0,vuOnb:false}; (function b(){ try{ var o=document.getElementById('onbV'), f=document.getElementById('guideFlou'), n=performance.now();
      if(o) { window.__g.vuOnb=true; window.__g.tArr=0; } else if(window.__g.vuOnb && !window.__g.tArr) window.__g.tArr=n;
      if(f){ if(!window.__g.tG) window.__g.tG=n; var u=+f.getAttribute('data-u'); var L=window.__g.us; if(!L.length || L[L.length-1]!==u) L.push(u); } }catch(e){} requestAnimationFrame(b); })();""")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500)
    pg.evaluate("(t)=>{ try{ setTheme(t); }catch(e){} }", th); pg.wait_for_timeout(500)
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

def attend_guide(pg, quoi, maxi=6000):
    t0 = time.time(); vus = []
    while (time.time() - t0) * 1000 < maxi:
        e = pg.evaluate(ETAT); vus.append(e)
        if e['guide'] == quoi and e['u'] is not None and e['u'] >= 1: return e, vus
        pg.wait_for_timeout(60)
    return pg.evaluate(ETAT), vus

def complet(b, th):
    T = 'clair' if th == 'light' else 'sombre'
    print('\n── le parcours complet, %s' % T)
    ctx, pg, cdp = ouvre(b, th)
    onboarding(pg, cdp)
    # l'arrivée sur l'accueil : pas de flou tout de suite — on prend là l'image NETTE et la barre
    arr = None; e0 = None; nette = None
    for _ in range(40):
        if pg.evaluate("()=>!document.getElementById('onbV')"): arr = True; pg.wait_for_timeout(120); e0 = pg.evaluate(ETAT); nette = image(pg); break
        pg.wait_for_timeout(50)
    if e0 is None: e0 = pg.evaluate(ETAT)
    juge('[%s] la barre du bas est complète dès l\'arrivée sur l\'accueil (cinq entrées), et rien n\'est encore flou' % T, all(e0['barre']) and not e0['guide'], '%s · guide %s' % (e0['barre'], e0['guide']))
    attend_guide(pg, 'studio', 6000)
    g = pg.evaluate("()=>window.__g"); us = g['us']
    delai = ((g['tG'] - g['tArr']) / 1000.0) if (g['tArr'] and g['tG']) else None
    juge('[%s] 1 · le flou paraît environ 0,8 s après l\'arrivée sur l\'accueil (entre 0,6 et 1,6 s)' % T, delai is not None and 0.6 <= delai <= 1.6, 'délai %s s' % (None if delai is None else round(delai, 2)))
    crois = len(set(us)) >= 12 and all(us[i] <= us[i + 1] + 1e-6 for i in range(len(us) - 1))
    juge('[%s] 1 · il s\'installe peu à peu (le masque grandit, sans à-coup de retour)' % T, crois, '%d valeurs relevées, de %s à %s' % (len(set(us)), us[:1], us[-1:]))
    pg.wait_for_timeout(250); e = pg.evaluate(ETAT); im = image(pg); cap(pg, '1-studio-%s' % T)
    juge('[%s] 1 · la matière est le flou des murs : %s px, par un flou de l\'arrière-plan' % (T, FLOU), bool(e['flou']) and ('blur(%spx)' % FLOU) in e['flou'], '%s' % e['flou'])
    if arr:
        zones = {'le mot-marque': (30, 48, 150, 92), 'les icônes du plateau': (210, 48, 360, 92), 'AURA': (104, 730, 146, 792), 'le +': (160, 725, 230, 795), 'INDEX': (246, 730, 288, 792), 'FIL': (300, 730, 342, 792)}
        r = {n: (energie(nette, *z), energie(im, *z)) for n, z in zones.items()}
        flous = all(ap <= av * 0.62 for av, ap in r.values())
        juge('[%s] 2 · tout est flou : le plateau et les autres entrées de la barre perdent leurs contours (≤ 62 %% de l\'énergie d\'avant)' % T, flous, ' · '.join('%s %.1f→%.1f' % (n, a, p) for n, (a, p) in r.items()))
        sb = e['barre'][0]; zs = (sb[0] + 4, sb[1] + 4, sb[0] + sb[2] - 4, sb[1] + sb[3] - 4) if sb else (48, 732, 92, 790)
        av, ap = energie(nette, 46, 730, 94, 792), energie(im, 40, 724, 100, 796)
        juge('[%s] 2 · seule l\'icône du Studio est nette (ses contours gardent ≥ 80 %% de leur énergie), et un peu plus grosse' % T, ap >= av * 0.80 and bool(sb) and bool(e0['barre'][0]) and sb[2] > e0['barre'][0][2] * 1.1, 'énergie %.1f → %.1f · largeur %s → %s' % (av, ap, e0['barre'][0][2], sb and sb[2]))
    juge('[%s] 2 · la phrase, mot pour mot, au milieu de l\'écran' % T, e['phrase'] == PH_STUDIO and e['phraseB'] and abs((e['phraseB'][1] + e['phraseB'][3] / 2) - 392) <= 30 and abs((e['phraseB'][0] + e['phraseB'][2] / 2) - 195) <= 2, '« %s » %s' % (e['phrase'], e['phraseB']))
    cols = [c for c in [e['phraseCol']] if c]
    attendue = 'rgb(32, 25, 8)' if th == 'light' else 'rgb(247, 240, 222)'
    juge('[%s] 2 · ni orange ni « Ma Parole ! » : la phrase est à l\'encre du mode' % T, e['phraseCol'] == attendue and 'Ma Parole' not in (e['phrase'] or ''), '%s' % e['phraseCol'])
    juge('[%s] un « Plus tard » discret, visible : 12 px, sans soulignement' % T, e['tard'] == 'Plus tard' and e['tardB'] and e['tardFs'] == '12px' and e['tardDeco'] == 'none', '%s %s %s %s' % (e['tard'], e['tardB'], e['tardFs'], e['tardDeco']))
    a2 = [x for x in e['eng'] if x['op'] < 1 or (x['tr'] not in ('0s', '') and any(float(v.replace('s', '').replace('m', '')) > 0 for v in x['tr'].split(', '))) or x['an'] not in ('none', '')]
    juge('[%s] A2 : aucun nœud du guide n\'a d\'opacité, de transition ni d\'animation ; tous portent `data-eng`' % T, not a2 and all(x['eng'] for x in e['eng']), '%s' % (a2[:2] or [x['id'] for x in e['eng'] if not x['eng']]))
    # 3 · toucher le Studio
    x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2600)
    e3 = pg.evaluate(ETAT); cap(pg, '2-au-studio-%s' % T)
    juge('[%s] 3 · toucher l\'icône ouvre le Studio ; le flou n\'est plus là' % T, e3['studio'] and not e3['guide'], 'Studio %s · guide %s' % (e3['studio'], e3['guide']))
    # 4 · le retour
    c = centre(pg, '#studioScreen .closeb')                        # le vrai « ✕ Fermer » du Studio, au doigt (`closeAll()` ne ferme pas le Studio, §8)
    if c: toucher(cdp, pg, c[0], c[1])
    e4, _ = attend_guide(pg, 'plus', 7000); pg.wait_for_timeout(250); im4 = image(pg); e4 = pg.evaluate(ETAT); cap(pg, '3-plus-%s' % T)
    juge('[%s] 4 · au retour, le flou se reforme ; la phrase, mot pour mot' % T, e4['guide'] == 'plus' and e4['phrase'] == PH_PLUS, 'guide %s · « %s »' % (e4['guide'], e4['phrase']))
    if arr and e4['guide'] == 'plus':
        r = {n: (energie(nette, *z), energie(im4, *z)) for n, z in {'le mot-marque': (30, 48, 150, 92), 'STUDIO': (48, 730, 92, 792), 'FIL': (300, 730, 342, 792)}.items()}
        av, ap = energie(nette, 163, 728, 227, 792), energie(im4, 157, 722, 233, 798)
        pb = e4['barre'][2]
        juge('[%s] 4 · tout est flou, sauf le + et son encart, nets et un peu grossis' % T, all(p <= a * 0.62 for a, p in r.values()) and ap >= av * 0.75 and pb and pb[2] > e0['barre'][2][2] * 1.05,
             ' · '.join('%s %.1f→%.1f' % (n, a, p) for n, (a, p) in r.items()) + ' · le + %.1f→%.1f, largeur %s → %s' % (av, ap, e0['barre'][2][2], pb and pb[2]))
    # 5 · toucher le +
    if e4['e'] and e4['e']['trou']:
        x, y = pt(pg, e4['e']['trou']['x'], e4['e']['trou']['y']); toucher(cdp, pg, x, y)
    pg.wait_for_timeout(900); e5 = pg.evaluate(ETAT); cap(pg, '4-apres-plus-%s' % T)
    juge('[%s] 5 · toucher le + ouvre la création (les trois natures du +, ou la page +) ; le guidage est fini' % T, (e5['choix'] or e5['cs']) and not e5['guide'] and e5['vu'] == '1', 'natures %s · page + %s · guide %s · promi_guide %s' % (e5['choix'], e5['cs'], e5['guide'], e5['vu']))
    juge('[%s] après le guide, la barre est complète et à sa taille' % T, all(e5['barre']) and abs(e5['barre'][0][2] - e0['barre'][0][2]) < 0.6 and abs(e5['barre'][2][2] - e0['barre'][2][2]) < 0.6, '%s' % e5['barre'])
    # le rechargement : il ne revient pas
    pg.reload(); pg.wait_for_timeout(8500); e6 = pg.evaluate(ETAT)
    juge('[%s] une seule fois : après un rechargement, ni onboarding ni guide (8,5 s sur l\'accueil)' % T, not e6['guide'] and not e6['onb'] and e6['devant'] == 'accueil', 'guide %s · devant : %s' % (e6['guide'], e6['devant']))
    tx = e['textes'] or {}
    juge('[%s] les phrases vivent dans TEXTES_ENGAGEMENT, sans impératif (A3)' % T, tx.get('studio') == PH_STUDIO and tx.get('plus') == PH_PLUS and not any(IMP.search(v) for v in tx.values()), '%s' % tx)
    ctx.close()

def ailleurs(b, comment):
    print('\n── %s' % comment)
    ctx, pg, cdp = ouvre(b, 'light'); onboarding(pg, cdp); e, _ = attend_guide(pg, 'studio', 8000)
    if comment.startswith('toucher'):
        x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y)
    else:
        c = centre(pg, '#guideTard'); toucher(cdp, pg, c[0], c[1]) if c else None
    pg.wait_for_timeout(1100); e2 = pg.evaluate(ETAT)
    juge('%s : le flou se dissout, le guidage est fini (rien d\'ouvert, l\'accueil est là)' % comment, e['guide'] == 'studio' and not e2['guide'] and e2['devant'] == 'accueil' and not e2['studio'] and e2['e']['etat'] is None, 'avant %s · après %s · devant %s' % (e['guide'], e2['guide'], e2['devant']))
    pg.wait_for_timeout(2500); e3 = pg.evaluate(ETAT)
    juge('%s : il ne se reforme pas' % comment, not e3['guide'], 'guide %s' % e3['guide'])
    pg.reload(); pg.wait_for_timeout(8000); e4 = pg.evaluate(ETAT)
    juge('%s : après un rechargement, il ne revient pas' % comment, not e4['guide'] and not e4['onb'], 'guide %s' % e4['guide'])
    ctx.close()

def reduit(b):
    print('\n── Réduire les animations')
    ctx, pg, cdp = ouvre(b, 'light', True); onboarding(pg, cdp)
    t0 = time.time(); us = []
    while time.time() - t0 < 6:
        e = pg.evaluate(ETAT)
        if e['guide']: us.append(e['u'])
        if len(us) >= 8: break
        pg.wait_for_timeout(40)
    juge('Réduire les animations : le flou est posé sans mouvement (entier dès la première image)', len(us) >= 8 and all(u == 1 for u in us), '%s' % us[:8])
    ctx.close()

def tard_onboarding(b):
    print('\n── « Plus tard » dans l\'onboarding : pas de guide')
    ctx, pg, cdp = ouvre(b, 'light'); c = centre(pg, '#onbTard')
    if c: toucher(cdp, pg, c[0], c[1])
    pg.wait_for_timeout(4000); e = pg.evaluate(ETAT)
    juge('« Plus tard » à la première étape : on est sur l\'accueil, sans guide', bool(c) and not e['onb'] and not e['guide'] and e['devant'] == 'accueil', 'onb %s · guide %s · devant %s' % (e['onb'], e['guide'], e['devant']))
    ctx.close()

def rejeu(b):
    print('\n── « Revoir la présentation » rejoue le guide')
    ctx, pg, cdp = ouvre(b, 'light'); onboarding(pg, cdp); e, _ = attend_guide(pg, 'studio', 8000)
    x, y = pt(pg, 195, 230); toucher(cdp, pg, x, y); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{ try{ obReplay(); }catch(e){} }"); pg.wait_for_timeout(1500)
    pg.keyboard.type('nager le mardi', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
    if not pg.evaluate("()=>!!document.getElementById('onbTrait') && document.getElementById('onbTrait').style.display!=='none'"):
        c = centre(pg, '#onbPh'); toucher(cdp, pg, c[0], c[1]) if c else None; pg.wait_for_timeout(300); pg.keyboard.type('nager le mardi', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(700)
    trait(pg, cdp); e2, _ = attend_guide(pg, 'studio', 9000)
    juge('après « Revoir la présentation » menée au bout, le guide se rejoue', e2['guide'] == 'studio', 'guide %s · promi_guide %s' % (e2['guide'], e2['vu']))
    ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    complet(b, 'light')
    if not VITE:
        complet(b, 'dark'); ailleurs(b, 'toucher le flou ailleurs'); ailleurs(b, '« Plus tard »'); reduit(b); tard_onboarding(b); rejeu(b)
    b.close()
ok = sum(1 for _, c in res if c)
print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
