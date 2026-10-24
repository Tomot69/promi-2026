#!/usr/bin/env python3
"""redteam_guide_studio.py — ⚑ v157 (Tom, C-172) : LE + DU GUIDE N'ARRIVE QU'APRÈS LE STUDIO FERMÉ.

« Dans le guide de l'onboarding, première phrase (le flou sur le Studio) : si l'utilisateur CHOISIT un design dans le Studio, le flou et l'icône + apparaissent
par-dessus le Studio encore ouvert. La phrase du + et son flou ne se déclenchent qu'une fois le Studio fermé, de retour sur l'accueil avec sa Toile. Jamais tant
que le Studio est ouvert. Juge : ouvrir le Studio, choisir un design, puis un second ; pas de flou ni de + tant que le Studio est ouvert ; à la fermeture,
le flou et la phrase du + arrivent sur l'accueil. »

Banc comme Tom (WebKit 390 × 844 ×3, doigt), le vrai guide (stockage du premier lancement), image par image :
  A · Studio ouvert par la zone nette du guide ; deux designs choisis au doigt (un monde glissé, puis une palette ; deux fois) : tant que le Studio est ouvert —
      `.show`, ou pas encore sorti de l'écran — le guide reste « au Studio » : ni étape du +, ni phrase, ni + net
  B · le Studio refermé (✕) : l'étape du + arrive, sa phrase et son + ; sa première image vient APRÈS que le Studio a fini de sortir de l'écran
  C · la situation où l'ancien test se trompait, posée exprès sous le Studio ouvert : la Toile déclarée au repos et le point sondé qui traverse le Studio (le
      Studio sans pointeur) pendant 3 s — le guide ne part pas ; puis le Studio fermé, il part
Preuve : `--fichier=zz-av156.html` rougit (C).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-110s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
SONDE = """()=>{ window.__g=[]; const dev=document.getElementById('device');
  (function f(){ const g=document.getElementById('guide'), st=document.getElementById('studioScreen'), r=st.getBoundingClientRect(), D=dev.getBoundingClientRect();
    const ouvert=st.classList.contains('show') || !(r.top>=D.bottom-1 || r.bottom<=D.top+1);
    const ph=document.getElementById('guidePhrase'), ci=document.getElementById('guideCible');
    window.__g.push({t:performance.now(), ouvert:ouvert, etat:g?g.getAttribute('data-guide'):null, plus:!!(ci && /Planter/.test(ci.getAttribute('aria-label')||'')) || !!(ph && /commence/.test(ph.textContent||''))});
    if(window.__g.length<4000) requestAnimationFrame(f); })(); }"""
def centre(pg, sel): return pg.evaluate("s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
def page(b, sombre):
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True)
    ctx.add_init_script("try{ localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); }catch(e){}" % ('dark' if sombre else 'light'))
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160])); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{ _guide.attend(false); }"); e = None
    for _ in range(170):
        e = pg.evaluate("()=>{const g=document.getElementById('guide'); return g&&g.getAttribute('data-guide')==='studio'&&g.getAttribute('data-entier') ? _guide.etat() : null;}")
        if e: break
        pg.wait_for_timeout(120)
    return ctx, pg, er, e
def ouvre_studio(pg, e):
    pg.wait_for_timeout(600); d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width];}"); k = d[2] / 390
    B.tap(pg, d[0] + e['trou']['x'] * k, d[1] + e['trou']['y'] * k, appareil=False); pg.wait_for_timeout(2600)
def choisit(pg):
    m0 = pg.evaluate("()=>JSON.stringify(Toile.mondeCourant())")
    B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1800)
    c = centre(pg, '#studioScreen .stp-ton')
    if c: B.tap(pg, c[0], c[1], appareil=False)
    pg.wait_for_timeout(900)
    c = pg.evaluate("()=>{ const P=[...document.querySelectorAll('#stpPals .st3-p')].filter(b=>!b.classList.contains('on') && b.getBoundingClientRect().width>4); const b=P[Math.min(5,P.length-1)]; if(!b) return null; const r=b.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
    if c: B.tap(pg, c[0], c[1], appareil=False)
    pg.wait_for_timeout(3500)
    return m0, pg.evaluate("()=>JSON.stringify(Toile.mondeCourant())")
def ferme(pg):
    c = centre(pg, '#studioScreen .closeb')
    if c: B.tap(pg, c[0], c[1], appareil=False)
    for _ in range(120):
        pg.wait_for_timeout(120)
        if pg.evaluate("()=>{const g=document.getElementById('guide'); return !!(g && g.getAttribute('data-guide')==='plus' && g.getAttribute('data-entier'));}"): break
    pg.wait_for_timeout(500)
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = 'sombre' if sombre else 'clair'
        ctx, pg, er, e = page(b, sombre)
        if not e: juge('[%s] le guide paraît à l\'étape du Studio' % T, False); ctx.close(); continue
        pg.evaluate(SONDE); ouvre_studio(pg, e)
        a1 = choisit(pg); a2 = choisit(pg)
        L = pg.evaluate("()=>window.__g"); ouv = [x for x in L if x['ouvert']]
        mauvais = [x for x in ouv if x['etat'] in ('vers-plus', 'plus', 'part') or x['plus']]
        juge('[%s] A · deux designs choisis au Studio (%s → %s → %s) : tant que le Studio est ouvert, ni étape du +, ni sa phrase, ni son +' % (T, a1[0][7:30], a1[1][7:30], a2[1][7:30]),
             len(ouv) > 100 and not mauvais and a1[0] != a1[1] and a2[0] != a2[1], '%d images le Studio ouvert, %d avec le + ou sa phrase · états vus : %s' % (len(ouv), len(mauvais), sorted(set(x['etat'] or '-' for x in ouv))))
        ferme(pg); L = pg.evaluate("()=>window.__g")
        p1 = next((x for x in L if x['etat'] in ('vers-plus', 'plus')), None); fin_st = max([x['t'] for x in L if x['ouvert']] or [0])
        dern = L[-1] if L else {}
        juge('[%s] B · Studio refermé : l\'étape du + arrive sur l\'accueil, après que le Studio a fini de sortir de l\'écran' % T,
             p1 is not None and p1['t'] > fin_st and dern.get('etat') == 'plus' and dern.get('plus') and not dern.get('ouvert'),
             'Studio sorti à %s ms · première image du + à %s ms (+%s) · dernier état %s' % (round(fin_st), p1 and round(p1['t']), p1 and round(p1['t'] - fin_st), dern.get('etat')))
        juge('[%s] aucune erreur de page' % T, not [x for x in er if 'version.json' not in x], er[:2]); ctx.close()
    # C · la situation où l'ancien test se trompait
    ctx, pg, er, e = page(b, False)
    if e:
        ouvre_studio(pg, e); pg.evaluate(SONDE)
        pg.evaluate("()=>{ window.__ts=window.Toile_state; window.Toile_state=function(){ const s=window.__ts(); return Object.assign({}, s, {running:false}); }; const s=document.createElement('style'); s.id='__sondeC'; s.textContent='#studioScreen, #studioScreen *{pointer-events:none!important}'; document.head.appendChild(s); }")
        pg.wait_for_timeout(3000)
        L = pg.evaluate("()=>window.__g"); mauvais = [x for x in L if x['ouvert'] and (x['etat'] in ('vers-plus', 'plus', 'part') or x['plus'])]
        pg.evaluate("()=>{ window.Toile_state=window.__ts; const s=document.getElementById('__sondeC'); if(s) s.remove(); }")
        ferme(pg); fin = pg.evaluate("()=>{const g=document.getElementById('guide'); return g && g.getAttribute('data-guide');}")
        juge('[clair] C · la Toile déclarée au repos et le point sondé qui traverse le Studio ouvert (3 s) : le guide ne part pas ; le Studio fermé, il part',
             not mauvais and fin == 'plus', '%d images du + sous le Studio ouvert · après fermeture : %s' % (len(mauvais), fin))
    else: juge('[clair] C · le guide paraît', False)
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
