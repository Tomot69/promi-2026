#!/usr/bin/env python3
"""redteam_clavier_doux.py — v177 (Tom, Q598) : À LA FERMETURE DU CLAVIER, LA PAGE REJOINT SA PLACE PAR UN MOUVEMENT DOUX DE 300 À 400 ms, JAMAIS D'UN COUP.
Trois natures × clair, sombre × échelles 1 et 0,79, parole écrite, lu image par image dans la page : la phrase, le libellé, le rail et la barre vont de leur place de saisie à leur place finale sans aucun
pas au-delà de 35 % de la course (compté à la cote, sous charge : un grand pas d'une image lente n'est jugé qu'au calme) ; l'onde du moment va de la base de saisie à la base finale ; aucune image de la page finale avant
le mouvement ; durée 300 à 400 ms (au calme, charge < 4 ; sinon non jugée) ; à la fin : les cotes finales, aucun calque, aucune transformation restée. Et : parole vide (page « pas prête ») ; « Réduire les animations » : la page se pose.
Rouge sur v176 (`--fichier=zz-v176.html`) : d'un coup."""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html'); VITE = '--vite' in sys.argv; res = []
SEUL = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--seul=')), None)   # --seul=promi-sombre-1 : un seul tour
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', n, str(d)[:200]), flush=True)
ENR = """()=>{ window.__m=[]; (function f(){ const c=document.getElementById('createSheet'), e=_ppEcran(), p=document.getElementById(e.nat==='nuee'?'nueePhrase':'csPhrase'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, h=n=>{const r=n.getBoundingClientRect();return +((r.top-D.top)/k).toFixed(1)};
  window.__m.push({t:performance.now(), ph:h(p), lib:h(c.querySelector('.pp-trace')), rail:h(document.getElementById('csPinceau')), barre:h(document.getElementById('csBotBar')), base:(window._ppMvtEtat&&!window._ppMvtEtat.fini)?window._ppMvtEtat.base:null, ov:!!document.getElementById('ppMvt'), ouv:c.classList.contains('pp-ouvert')}); if(window.__m.length<320) requestAnimationFrame(f); })(); }"""
SL = {'promi': '#csPhrase .ph-m[data-ph="titre"]', 'chiche': '#csPhrase .ph-m[data-ph="titre"]', 'nuee': '#nueePhrase .ph-m[data-np="nom"]'}
def tour(b, nat, sombre, vw, vh, nom, ecrit=True):
    T = '[%s · %s · %s%s]' % (nat, 'sombre' if sombre else 'clair', nom, '' if ecrit else ' · vide'); ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(800); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2800)
    for _ in range(6):
        B.tap_sel(pg, SL[nat]); pg.wait_for_timeout(1000)
        if pg.evaluate("()=>{const a=document.activeElement;return !!a&&(a.id==='phIn'||a.id==='nueeNomIn');}"): break
    if ecrit: pg.keyboard.type('nager', delay=50); pg.wait_for_timeout(1500)
    pg.evaluate(ENR); pg.wait_for_timeout(150); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
    R = pg.evaluate("()=>window.__m"); et = pg.evaluate("()=>window._ppMvtEtat"); ch = B.charge()
    i0 = next((i for i, r in enumerate(R) if not r['ouv'] or r['ov']), None)
    if i0 is None or i0 == 0: juge(T + ' le relevé (fermeture vue image par image)', ch >= 8, 'i0 %s · charge %.0f : non jugé' % (i0, ch)); ctx.close(); return
    a, z = R[i0 - 1], R[-1]; S = R[i0 - 1:]
    for cle in ('ph', 'lib', 'rail') if ecrit else ('ph',):
        c = abs(z[cle] - (S[1][cle] if cle == 'rail' else a[cle])) or 1; v = [r[cle] for r in S]
        juge('%s %s : la première image après la fermeture est encore à sa place de départ, jamais la place finale' % (T, cle), abs(S[1][cle] - z[cle]) >= c * .5 or c < 2, 'départ %.1f · 1re image %.1f · fin %.1f' % (a[cle], S[1][cle], z[cle]))
        if ch < 8:
            pas = max(abs(v[i + 1] - v[i]) for i in range(1, len(v) - 1)); juge('%s %s : d\'un mouvement, aucun pas au-delà de 35 %% de la course' % (T, cle), pas <= c * .35, 'course %.1f · pas %.1f' % (c, pas))
    if nat == 'nuee': juge(T + ' la barre d\'un Cercle, visible pendant la saisie, ne bouge pas', max(r['barre'] for r in S) - min(r['barre'] for r in S) < .5, [S[0]['barre'], z['barre']])
    elif ecrit: juge(T + ' la barre remonte du bas : sous sa place au départ, à sa place à la fin', S[1]['barre'] > z['barre'] + 40 and abs(z['barre'] - 760) < 1, [S[1]['barre'], z['barre']])
    b_ = [r['base'] for r in S if r['base'] is not None]; juge(T + ' l\'onde descend avec eux', len(b_) >= 2 and b_[0] < b_[-1], b_[:4])
    d = (et or {}).get('ms'); juge(T + ' durée 300 à 400 ms (au calme ; sinon non jugée)', et and et.get('fini') and (ch >= 4 or 300 <= d <= 400), '%s ms · charge %.0f' % (d, ch))
    # v178b (C-229) : le trait naît APRÈS la fermeture du clavier (horizon 360 ms, puis 700 ms de flaques) — « la fin » attend la fin de sa naissance, 3 s au plus
    for _ in range(30):
        if not pg.evaluate("()=>document.querySelectorAll('#ppMvt,#ppMvtDeja,#createSheet canvas.passage-flaques').length"): break
        pg.wait_for_timeout(100)
    f = pg.evaluate("()=>{const c=document.getElementById('createSheet');return {cal:document.querySelectorAll('#ppMvt,#ppMvtDeja,#createSheet canvas.passage-flaques').length, tr:[...c.querySelectorAll('.pp-phrase,.pp-trace,#csPinceau,.pp-garder,#csBotBar')].map(n=>(n.style.getPropertyValue('transform')+n.style.getPropertyValue('translate'))).join('')}}")
    juge(T + ' à la fin : aucun calque, aucune transformation restée', f['cal'] == 0 and not f['tr'], f)
    if pg.__dict__['erreurs']: juge(T + ' aucune erreur de page', False, pg.__dict__['erreurs'][:2])
    ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_clavier_doux — %s, charge %.1f' % (F, B.charge()))
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        for sombre in (False, True):
            for nat in ('promi', 'chiche', 'nuee'):
                if VITE and (nom != '1' or sombre): continue
                if SEUL and SEUL != '%s-%s-%s' % (nat, 'sombre' if sombre else 'clair', nom): continue
                tour(b, nat, sombre, vw, vh, nom)
    tour(b, 'promi', False, 430, 932, '1', ecrit=False)
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA, reduced_motion='reduce')
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){} try{ if(!sessionStorage.getItem('__a')){ sessionStorage.setItem('__a','1'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_guide','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}")
    pg = B.ouvre(ctx, F); B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(800); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2800); B.tap_sel(pg, SL['promi']); pg.wait_for_timeout(1000); pg.keyboard.type('nager', delay=50); pg.wait_for_timeout(800)
    pg.evaluate(ENR); pg.wait_for_timeout(150); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200); R = pg.evaluate("()=>window.__m")
    juge('[réduit] la page se pose, aucun calque de mouvement', not any(r['ov'] for r in R), len(R)); ctx.close(); b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
