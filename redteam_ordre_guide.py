#!/usr/bin/env python3
"""redteam_ordre_guide.py — ⚑ v148 (Tom, 16 oct. 2026, C-146) : L'ORDRE DU GUIDE, APRÈS L'ONBOARDING.

« 12.1 Au lancement, le flou du Studio. Tant que le Studio n'a jamais été ouvert, toucher ailleurs montre la phrase de rappel — choisir son monde — et
SEULEMENT elle, autant de fois qu'on touche ailleurs. JAMAIS la phrase du + avant le Studio.
 12.2 Studio ouvert puis refermé (avec ou sans changement) → le flou, et l'invitation vers le +. »

Chromium, 390 × 844 ×3, au vrai doigt (CDP), stockage d'un parcours fini (onboarding fait, guide jamais vu), clair puis sombre. Une sonde relève à chaque
image la phrase affichée et l'étape (`data-guide`).
  A · au lancement : le flou, l'étape du Studio, sa phrase mot pour mot
  B · trois touchers ailleurs (la Toile, le bas de l'écran, la place du + sous le flou) : à chaque fois l'étape reste celle du Studio, la phrase est
      ÉCRITE DE NOUVEAU (un nœud neuf) et c'est la phrase du Studio, mot pour mot ; les natures ne s'ouvrent pas
  C · l'app relancée sans que le Studio ait été ouvert : le flou du Studio revient
  D · le Studio touché : il s'ouvre ; refermé SANS changement → le flou reste, l'étape du + et sa phrase mot pour mot
  E · (autre lancement) le Studio refermé APRÈS un changement de monde → de même
  F · sur tout le parcours, la phrase du + n'a JAMAIS été vue avant que le Studio soit ouvert
  G · le + touché : les natures s'ouvrent ; relancée, l'app ne remontre plus le guide
Preuve : `--fichier=zz-av147.html` rougit (B, C, F : sur v147 toucher ailleurs menait à l'étape du +).
"""
import sys, time, os
from playwright.sync_api import sync_playwright

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
URL = 'http://127.0.0.1:8752/' + F
PH_STUDIO = 'Choisis d’abord le monde qui te ressemble, au Studio.'      # les mots de Tom, en dur
PH_PLUS = 'Promi, Chiche ou Cercle : tout commence par ce +.'
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-116s %s' % ('✅' if c else '❌', nom, str(d)[:240]), flush=True)

SONDE = r"""(function(){ window.__o=[]; var der=''; (function f(){ try{ var g=document.getElementById('guide'), p=document.getElementById('guidePhrase'), s=(g?g.getAttribute('data-guide'):'-')+'|'+(p?p.textContent:'');
      if(s!==der){ der=s; window.__o.push([Math.round(performance.now()), g?g.getAttribute('data-guide'):null, p?p.textContent:null]); } }catch(e){} requestAnimationFrame(f); })(); })();"""
ETAT = """()=>{ const g=document.getElementById('guide'), p=document.getElementById('guidePhrase'), D=document.getElementById('device').getBoundingClientRect();
  const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.6), s=document.getElementById('studioScreen');
  return {guide:g?g.getAttribute('data-guide'):null, entier:!!(g&&g.getAttribute('data-entier')), eau:!!document.getElementById('guideEau'), phrase:p?p.textContent:null, neuf:p?!p.__vieux:null,
    rappels:g?+(g.getAttribute('data-rappels')||0):0, e:(window._guide?window._guide.etat():null), vu:localStorage.getItem('promi_guide'),
    studio:!!(s&&h&&s.contains(h)), choix:!!(document.getElementById('accChoix')&&document.getElementById('accChoix').classList.contains('ouvert')), cs:!!document.querySelector('#createSheet.show'),
    monde:(()=>{try{return Toile.getTheme()}catch(e){return null}})()}; }"""
def toucher(cdp, pg, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
def pt(pg, x, y):
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width];}"); k = d[2] / 390.0; return d[0] + x * k, d[1] + y * k
def centre(pg, sel):
    return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2, r.top+r.height/2]:null;}", sel)
def attend(pg, quoi, maxi=12000):
    t0 = time.time(); e = None
    while (time.time() - t0) * 1000 < maxi:
        e = pg.evaluate(ETAT)
        if e['guide'] == quoi and e['entier'] and (e['e'] or {}).get('net', 0) >= 1: return e
        pg.wait_for_timeout(80)
    return e or pg.evaluate(ETAT)
def ouvre(b, th):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True)
    ctx.add_init_script("try{ localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); }catch(e){}" % th)
    ctx.add_init_script(SONDE)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto(URL); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    return ctx, pg, ctx.new_cdp_session(pg), er
def lancement(pg):
    """le moment où l'onboarding se referme : l'app demande le guide (comme `terminer` de l'onboarding)"""
    pg.evaluate("()=>{ if(window._guide) _guide.attend(false); }")
def studio_puis_ferme(pg, cdp, e, change):
    x, y = pt(pg, e['e']['trou']['x'], e['e']['trou']['y']); t_st = pg.evaluate("()=>Math.round(performance.now())"); toucher(cdp, pg, x, y); pg.wait_for_timeout(2600)
    e1 = pg.evaluate(ETAT); m0 = e1['monde']
    if change:
        x0, y0 = pt(pg, 300, 330); x1, y1 = pt(pg, 80, 330)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]})
        for i in range(1, 11): pg.wait_for_timeout(18); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * i / 10, 'y': y0}]})
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1800)
    m1 = pg.evaluate("()=>{try{return Toile.getTheme()}catch(e){return null}}")
    c = centre(pg, '#studioScreen .closeb')
    if c: toucher(cdp, pg, c[0], c[1])
    e2 = attend(pg, 'plus', 12000)
    return t_st, e1, m0, m1, e2

def passe(b, th):
    T = 'clair' if th == 'light' else 'sombre'; print('\n── %s' % T)
    ctx, pg, cdp, er = ouvre(b, th); lancement(pg)
    e = attend(pg, 'studio')
    juge('[%s] A · au lancement : le flou, l\'étape du Studio, sa phrase mot pour mot' % T, e['guide'] == 'studio' and e['eau'] and e['entier'] and e['phrase'] == PH_STUDIO, 'étape %s · « %s »' % (e['guide'], e['phrase']))
    if e['guide'] != 'studio':
        ctx.close(); return
    pg.wait_for_timeout(1500)
    lieux = [(195, 250, 'la Toile'), (300, 560, 'le bas de la Toile'), (195, 760, 'la place du + sous le flou')]
    for i, (x_, y_, nom) in enumerate(lieux, 1):
        pg.evaluate("()=>{ const p=document.getElementById('guidePhrase'); if(p) p.__vieux=1; }")
        x, y = pt(pg, x_, y_); toucher(cdp, pg, x, y); pg.wait_for_timeout(900); e = pg.evaluate(ETAT)
        juge('[%s] B · toucher ailleurs n°%d (%s) : l\'étape reste celle du Studio, la phrase du Studio est écrite DE NOUVEAU, mot pour mot ; rien ne s\'ouvre' % (T, i, nom),
             e['guide'] == 'studio' and e['phrase'] == PH_STUDIO and e['neuf'] is True and e['rappels'] == i and not e['choix'] and not e['cs'] and e['eau'],
             'étape %s · nœud neuf %s · rappels %s · « %s » · natures %s' % (e['guide'], e['neuf'], e['rappels'], e['phrase'], e['choix'] or e['cs']))
    pg.wait_for_timeout(1200); e = pg.evaluate(ETAT)
    juge('[%s] B · après les trois touchers, toujours l\'étape du Studio et sa phrase (le guide ne s\'en va pas)' % T, e['guide'] == 'studio' and e['phrase'] == PH_STUDIO, 'étape %s' % e['guide'])
    O = pg.evaluate("()=>window.__o"); vus = [o for o in O if o[2] == PH_PLUS]
    juge('[%s] F · pendant les trois touchers, la phrase du + n\'a jamais paru, pas une image' % T, not vus, '%d image(s)' % len(vus))
    # C · relancée sans que le Studio ait été ouvert
    pg.reload(); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} }")
    e = attend(pg, 'studio', 9000)
    juge('[%s] C · l\'app relancée sans que le Studio ait été ouvert : le flou du Studio revient, sa phrase' % T, e['guide'] == 'studio' and e['phrase'] == PH_STUDIO, 'étape %s · mémoire « %s »' % (e['guide'], e['vu']))
    if e['guide'] == 'studio':
        t_st, e1, m0, m1, e2 = studio_puis_ferme(pg, cdp, e, False)
        juge('[%s] D · le Studio touché s\'ouvre ; refermé SANS changement : le flou reste, l\'étape du + et sa phrase mot pour mot' % T,
             e1['studio'] and e2['guide'] == 'plus' and e2['phrase'] == PH_PLUS and e2['eau'] and e2['entier'] and m0 == m1, 'Studio ouvert %s · monde %s → %s · étape %s · « %s »' % (e1['studio'], m0, m1, e2['guide'], e2['phrase']))
        O = pg.evaluate("()=>window.__o")
        avant = [o for o in O if o[0] < t_st and o[2] == PH_PLUS]
        juge('[%s] F · la phrase du + n\'a JAMAIS été vue avant que le Studio soit ouvert (depuis la relance)' % T, not avant, '%d image(s)' % len(avant))
        if e2['guide'] == 'plus':
            x, y = pt(pg, e2['e']['trou']['x'], e2['e']['trou']['y']); toucher(cdp, pg, x, y); pg.wait_for_timeout(2600); e3 = pg.evaluate(ETAT)
            pg.reload(); pg.wait_for_timeout(8500); e4 = pg.evaluate(ETAT)
            juge('[%s] G · le + touché ouvre les natures ; relancée, l\'app ne remontre plus le guide' % T, (e3['choix'] or e3['cs']) and not e4['guide'] and e4['vu'] == '1', 'natures %s · guide après relance %s · mémoire « %s »' % (e3['choix'] or e3['cs'], e4['guide'], e4['vu']))
    juge('[%s] aucune erreur de page' % T, not er, er[:2]); ctx.close()
    # E · un autre lancement : le Studio refermé APRÈS un changement de monde
    ctx, pg, cdp, er = ouvre(b, th); lancement(pg); e = attend(pg, 'studio')
    if e['guide'] == 'studio':
        pg.wait_for_timeout(800); x, y = pt(pg, 195, 250); toucher(cdp, pg, x, y); pg.wait_for_timeout(900)
        t_st, e1, m0, m1, e2 = studio_puis_ferme(pg, cdp, pg.evaluate(ETAT), True)
        juge('[%s] E · le Studio refermé APRÈS un changement de monde (%s → %s) : le flou reste, l\'étape du + et sa phrase' % (T, m0, m1), e1['studio'] and m1 != m0 and e2['guide'] == 'plus' and e2['phrase'] == PH_PLUS and e2['eau'], 'étape %s · « %s »' % (e2['guide'], e2['phrase']))
        O = pg.evaluate("()=>window.__o"); avant = [o for o in O if o[0] < t_st and o[2] == PH_PLUS]
        juge('[%s] F · (ce lancement) la phrase du + n\'a jamais été vue avant le Studio' % T, not avant, '%d image(s)' % len(avant))
    else: juge('[%s] E · le guide paraît au second lancement' % T, False, e['guide'])
    ctx.close()

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ('light', 'dark'): passe(b, th)
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
