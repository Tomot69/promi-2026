"""redteam_onb_rejeu.py — ⚑ v151 (Tom, C-159) : REJOUER L'ONBOARDING, LE TEXTE S'ADAPTE.

« Quand on rejoue l'onboarding et que la Toile a déjà des dalles, la parole plantée n'est plus la première. Dès que la Toile compte au moins une dalle
avant cette plantation, le texte devient, mot pour mot : « PROMI planté ! » « Une nouvelle dalle sur ta Toile, félicitations. Plus qu'à le tenir. »
Le reste de la chorégraphie ne change pas. Juge : Toile vide → texte d'origine ; Toile avec 1 et 10 dalles → texte de Tom. »

Banc comme Tom (WebKit, 390 × 844, échelle 3, doigt, webdriver masqué) :
  A · premier lancement, Toile vide : « Ton premier Promi, ta première dalle sur ta Toile. Plus qu'à le tenir. »
  B · rejeu (Réglages → « Revoir la présentation », au doigt), Toile d'une dalle : le texte de Tom
  C · rejeu, Toile de dix paroles relue de la sauvegarde (banc-etats/etat-10.json) : le texte de Tom
  D · dans les trois cas, le reste ne change pas : le titre « PROMI planté ! », Primo · Deuxio · Tertio, « Tout le monde promet. Toi, tu tiens
      parole. », « La suite t'appartient. » — mot pour mot, trois touchers
Textes en dur. Preuve : `--fichier=zz-av150.html` rougit (B, C).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright

F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
PREMIER = 'Ton premier Promi, ta première dalle sur ta Toile. Plus qu’à le tenir.'
NOUVELLE = 'Une nouvelle dalle sur ta Toile, félicitations. Plus qu’à le tenir.'   # le texte de Tom, mot pour mot
TITRE = 'Promi planté !'   # l'espace insécable est lue comme une espace (\s)
RESTE = ['Primo, un Promi, c’est ta parole donnée.', 'Deuxio, un Chiche, c’est un coup de culot.',
         'Tertio, un Cercle, c’est tout cela à la fois, mais à plusieurs.', 'Tout le monde promet. Toi, tu tiens parole.', 'La suite t’appartient.']
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, d))
LIT = """()=>{ const f=document.getElementById('onbFin'); if(!f) return null; const T=e=>e?(e.textContent||'').replace(/\\s+/g,' ').trim():null;
  return {titre:T(f.querySelector('.onbv-titre')), ton:T(f.querySelector('.onbv-ton')), reste:[...f.querySelectorAll('#onbReste .onbv-l')].map(T),
    vus:[...f.querySelectorAll('.onbv-ton,#onbReste .onbv-l')].filter(e=>getComputedStyle(e).visibility!=='hidden').length, pas:(window._onbFinPas&&_onbFinPas()||{}).pas||0}; }"""
def parcours(pg, prenom=None):
    if prenom is None:   # le rejeu passe la page du prénom quand un prénom est gardé
        prenom = bool(pg.evaluate("()=>{ const e=document.getElementById('onbPh'); return !!e && /Toi, c/.test(e.textContent||''); }"))
    if prenom:
        B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1600)
    elif pg.evaluate("()=>{ const a=document.activeElement; return !(a && a.id==='onbIn'); }"):   # au rejeu le champ a déjà la main (le clavier est ouvert)
        B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(4500)
    z = pg.evaluate("()=>{ const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {l:(r.left-D.left)/k, t:(r.top-D.top)/k, k:r.width/390/k, dep:c.getAttribute('data-depart'), arr:c.getAttribute('data-arrivee')}; }")
    if not z or not z['dep'] or not z['arr']: return False
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    B.glisse(pg, [[x0 + (x1 - x0) * i / 24, y0 + (y1 - y0) * i / 24 - 14 * (1 - abs(2 * i / 24 - 1))] for i in range(25)], pas=24, tenue=90)
    pg.wait_for_timeout(5600)
    for _ in range(3): B.tap(pg, 195, 300); pg.wait_for_timeout(3800)
    return True
def termine(pg):
    """le quatrième toucher mène au compte ; « Plus tard » referme l'onboarding (le parcours est fait)"""
    B.tap(pg, 195, 300); pg.wait_for_timeout(2600)
    B.tap_sel(pg, '.onbv-compte .tard'); pg.wait_for_timeout(3500)
def verdict(cas, r, attendu):
    juge('%s · le texte de « Promi planté ! »' % cas, r and r['ton'] == attendu, (r or {}).get('ton'))
    juge('%s · le reste ne change pas : le titre, Primo · Deuxio · Tertio, la fin — trois touchers' % cas,
         r and r['titre'] == TITRE and r['reste'] == RESTE and r['vus'] == 6, '%s · %s visibles · pas %s%s' % ((r or {}).get('titre'), (r or {}).get('vus'), (r or {}).get('pas'),
         '' if (r and r['reste'] == RESTE) else ' · lu : %s' % ((r or {}).get('reste'),)))
def rejeu(pg):
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{ const b=document.getElementById('settingsBtn')||document.querySelector('[data-open=settings]'); if(b) b.click(); else if(window.ouvrirReglages) ouvrirReglages(); }"); pg.wait_for_timeout(1500)
    vu = pg.evaluate("()=>{ const e=document.getElementById('replayOnb'); if(!e) return false; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(); return r.width>4 && r.height>4; }")
    pg.wait_for_timeout(400)
    if vu: B.tap_sel(pg, '#replayOnb')
    else: pg.evaluate("()=>replayIntro()")
    pg.wait_for_timeout(4200); return vu

with sync_playwright() as p:
    b = p.webkit.launch()
    # A — premier lancement, Toile vide
    ctx = B.contexte(b, onb=False, guide=False); pg = B.ouvre(ctx, F, attente=7000)
    ok = parcours(pg, True); r = pg.evaluate(LIT)
    juge('A · premier lancement : le parcours va jusqu\'à « Promi planté ! »', ok and r is not None)
    verdict('A · Toile vide', r, PREMIER)
    termine(pg)
    # B — le rejeu sur une Toile d'une dalle (la parole qu'on vient de planter)
    pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(7000)
    n = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
    vu = rejeu(pg); ok = parcours(pg); r = pg.evaluate(LIT)
    juge('B · le rejeu part des Réglages (« Revoir la présentation », au doigt) sur une Toile de %d dalle' % n, vu and ok and n == 1, 'rangée vue : %s' % vu)
    verdict('B · Toile d\'une dalle', r, NOUVELLE)
    err = list(pg.erreurs); ctx.close()
    # C — le rejeu sur une Toile de dix paroles relue de la sauvegarde
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F, attente=7000)
    n = pg.evaluate("()=>promises.filter(p=>!p.draft).length")
    vu = rejeu(pg); ok = parcours(pg); r = pg.evaluate(LIT)
    juge('C · le rejeu sur une Toile de %d paroles' % n, ok and n >= 10)
    verdict('C · Toile de dix dalles', r, NOUVELLE)
    err += list(pg.erreurs); ctx.close()
    err = [x for x in err if 'version.json' not in x]
    juge('aucune erreur de page', not err, str(err[:2]))
    b.close()

ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
