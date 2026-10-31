#!/usr/bin/env python3
"""
⚑ v146 (Tom, 14 oct. 2026, 11.4) — CONTRAT REMIS AU NIVEAU (original : sauvegardes/redteam_onb_sorties-avant-v146.py) : « C'est planté. » devient
  « Promi planté ! » ; le message ne montre d'abord que le titre et la phrase de ton, le reste vient au premier toucher, le second mène au compte.
⚑ v144 (Tom, 12 oct. 2026) — « “Plus tard” retiré, du guide comme de l'onboarding, par décision de Tom : le parcours est court, on ne le passe pas.
  Exception nommée dans redteam_engagement (R6) et dans CLAUDE.md. » Et la main fantôme ne paraît plus sur le trait de l'onboarding (C-110).
  Ce juge vérifie donc : les textes d'avant v140 mot pour mot, AUCUN « Plus tard » à aucune étape (le panneau du compte garde le sien : c'est le
  refus du compte, pas une sortie du parcours), aucune main. Original (v141, 27 contrôles) : sauvegardes/redteam_onb_sorties-avant-v144.py.

redteam_onb_sorties.py — L'ONBOARDING D'AVANT v140 EST REVENU EN ENTIER, AVEC UNE SORTIE À CHAQUE ÉTAPE (v141, Tom, 10 oct. 2026 — C-075).

LA DÉCISION, EN DUR (§7) :
  « L'onboarding de v140 est retiré. Remets toutes les étapes et tous les textes d'avant v140, mot pour mot, y compris la dernière diapositive.
    L'étape “principe” et ses textes disparaissent. “Toi, c'est ?” reste, mais sans dalle derrière le texte ; rien d'autre ne change à cette étape.
    Ce que tu gardes de v140 : la main fantôme sur les traits, “TRACE POUR TENIR” plus grand, un “Plus tard” à chaque étape, mais sans
    soulignement, et deux fois plus petit. Juge : chaque texte identique à avant v140, R6 vert. »
  Les textes ci-dessous ont été RELEVÉS sur la version d'avant v140 (sauvegardes/app-avant-v140.html, au doigt) et sont écrits ici EN DUR.
  « Plus tard » : 12 px — le plancher du §6 (la moitié des 14 px de v140 donnerait 7 px) —, sans soulignement.

Usage : python3 redteam_onb_sorties.py [fichier.html] [--r6]     (--r6 : la seule ligne R6, pour redteam_engagement)
"""
import io, sys, time
from playwright.sync_api import sync_playwright
from PIL import Image
R6 = '--r6' in sys.argv
F = ([a for a in sys.argv[1:] if not a.startswith('--')] or ['app.html'])[0]
URL = 'http://127.0.0.1:8752/' + F
TEXTES = {   # relevés sur la version d'avant v140 — mot pour mot
 'prénom': 'PromiToi, c’est ton prénom ?',
 'prénom saisi': 'PromiToi, c’est Camille ?→',
 # ⚑ v147 (Tom, 15 oct. 2026, C-124 §4.2) — « Tom enrichit subtilement cette page » : « [Prénom], donc. Enchanté. » · « Quid d’un Promi à toi-même ? » (mot pour mot ;
 #   original : sauvegardes/redteam_onb_sorties-avant-v147.py)
 # ⚑ v155 (Tom, C-169 §4.4) : « trace pour planter » paraît 1 s après le prénom, avant la parole (original : sauvegardes/redteam_onb_sorties-avant-v155.py)
 'parole': 'PromiCamille, donc.Quid d’un Promi à toi-même ?Je me promets de ne plus dire “je commence lundi”Petite ou grande promesse, elle compte.trace pour planter',
 'trait': 'PromiCamille, donc.Quid d’un Promi à toi-même ?Je me promets de marcher une heurePetite ou grande promesse, elle compte.trace pour planter',
 'fin': 'Promi planté !',   # ⚑ v148 (Tom, C-124 §9.1) : « au départ, le titre seul » ; chaque toucher fait venir un paragraphe (v146 : le titre et le premier paragraphe ensemble)
 # ⚑ v149 (Tom, C-124) : « Le reste se découvre en traçant. » devient « Tout le monde promet. Toi, tu tiens. » (original : sauvegardes/redteam_onb_sorties-avant-v149.py)
 'fin-reste': 'Promi planté !Ton premier Promi, ta première dalle sur ta Toile. Plus qu’à le tenir.Primo, un Promi, c’est ta parole donnée.Deuxio, un Chiche, c’est un coup de culot.Tertio, un Cercle, c’est tout cela à la fois, mais à plusieurs.Tout le monde promet. Toi, tu tiens parole.La suite t’appartient.',
 'compte': 'Garder ta ToilePour la retrouver sur un autre téléphone.Continuer avec AppleContinuer avec GooglePlus tardEn continuant, tu acceptes les Conditions et la Politique de confidentialité.',
}
PRINCIPE = ['Promi garde ta parole', 'Une promesse s’écrit en une phrase', 'd’un trait du doigt', 'un second trait le dit', 'Une toute petite pour commencer', 'C’est parti']   # les textes de l'étape retirée
res = []; sorties = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond)))
    if not R6: print('  %s %-108s %s' % ('✅' if cond else '❌', nom, detail), flush=True)
TX = """()=>{ const o=document.getElementById('promiOnb'); const out=[]; const w=document.createTreeWalker(o,NodeFilter.SHOW_TEXT); const D=document.getElementById('device').getBoundingClientRect();
  while(w.nextNode()){ const n=w.currentNode; const e=n.parentElement; let v=e, vis=true; while(v&&v!==o.parentElement){ const c=getComputedStyle(v); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05){vis=false;break;} v=v.parentElement; } if(!vis) continue;
    const rg=document.createRange(); rg.selectNodeContents(n); const r=rg.getBoundingClientRect(); if(r.width<1||r.top>D.bottom||r.bottom<D.top) continue; out.push(n.nodeValue); }
  return out.join('').replace(/\\u00a0/g,' ').replace(/\\s+/g,' ').trim(); }"""
SORTIE = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const vu=e=>{ if(!e) return null; const c=getComputedStyle(e), r=e.getBoundingClientRect(); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.9||r.width<8) return null;
    const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); if(!h||!(h===e||e.contains(h))) return null; const rg=document.createRange(); rg.selectNodeContents(e); const q=rg.getBoundingClientRect();
    return {t:(e.textContent||'').trim(), fs:c.fontSize, deco:c.textDecorationLine, op:+c.opacity, tr:c.transitionDuration, an:c.animationName, eng:e.getAttribute('data-eng'), b:[(r.left-D.left)/k,(r.top-D.top)/k,r.width/k,r.height/k].map(v=>Math.round(v)), encreL:Math.round(q.width/k), c:[r.left+r.width/2, r.top+r.height/2]}; };
  const a=vu(document.getElementById('onbTard')), b=vu(document.querySelector('.onbv-compte .tard'));
  const gf=document.getElementById('gesteFantome'); const tr=document.getElementById('onbTrace');
  return {tard:a, compte:b, principe:!!document.querySelector('.e2-principe, .e2-bouton'), e2:(typeof window._e2), main:gf?gf.getAttribute('data-geste'):null, mainNoeud:!!(gf&&gf.querySelector('[data-main]')), trace:tr?getComputedStyle(tr).fontSize:null,
    onb:!!document.getElementById('onbV'), verrou:localStorage.getItem('promi_onb'), guide:!!document.getElementById('guide'), n:(typeof promises!=='undefined'?promises.filter(p=>!p.draft).length:-1),
    panneau:!!document.querySelector('.onbv-compte'), colorees:(window.Toile&&Toile.colored)?Toile.colored():-1,
    devant:(()=>{const h=document.elementFromPoint(D.left+D.width/2, D.top+D.height*0.45); return h?(h.closest('#promiOnb')?'onboarding':(h.closest('.screen,.sheet,.poster')?'ecran':'accueil')):null;})() }; }"""
def toucher(cdp, pg, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
def centre(pg, sel): return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
def ouvre(b):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); return ctx, pg, ctx.new_cdp_session(pg)
def prenom(pg, cdp):
    c = centre(pg, '#onbPh'); toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300)
def parole(pg): pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
def saisie(pg, cdp=None):
    # ⚑ v153 (Tom, C-164) : le prénom validé ferme le clavier — on touche la phrase pour saisir la parole, comme sur l'iPhone
    if not pg.evaluate("()=>{ const a=document.activeElement; return !!(a && a.id==='onbIn'); }"):
        c = centre(pg, '[data-onb="parole"]') or centre(pg, '#onbPh')
        if c: pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(350)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
def trace(pg, cdp):
    z = pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(); return {l:r.left,t:r.top,k:r.width/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    if not z or not z['dep']: return False
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]}); pg.wait_for_timeout(90)
    for i in range(1, 25):
        u = i / 24.0; cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * u, 'y': y0 + (y1 - y0) * u - 14 * z['k'] * (1 - abs(2 * u - 1))}]}); pg.wait_for_timeout(22)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); return True
TRACE_FINI = "()=>![...document.querySelectorAll('#onbV .onbv-a')].some(e=>getComputedStyle(e).display!=='none' && (e.style.visibility==='hidden' || (e.style.clipPath && e.style.clipPath!=='none')))"
def etape(pg, nom, textes=True):
    # v147 (C-125) : les textes s'écrivent par le tracé des lettres — on lit la page quand ils sont écrits (6 s au plus)
    for _ in range(40):
        if pg.evaluate(TRACE_FINI): break
        pg.wait_for_timeout(150)
    t = pg.evaluate(TX); s = pg.evaluate(SORTIE); so = s['compte'] if nom == 'compte' else s['tard']
    sorties.append((nom, bool(so), so and so['t']))
    if textes:
        attendu = TEXTES[nom]
        juge('« %s » : le texte est celui d\'avant v140, mot pour mot' % nom, t == attendu, '' if t == attendu else 'lu : %s' % t[:200])
    if nom != 'compte':
        juge('« %s » : aucun « Plus tard » (décision de Tom, v144)' % nom, not so, '%s' % (so and so.get('t')))
    else:
        juge('« compte » : le panneau du compte garde son « Plus tard » (le refus du compte)', bool(so) and so['t'] == 'Plus tard', '%s' % (so and so.get('t')))
    juge('« %s » : l\'étape « principe » n\'existe plus' % nom, not s['principe'] and not any(p in t for p in PRINCIPE) and s['e2'] == 'undefined', 'principe %s · _e2 %s' % (s['principe'], s['e2']))
    return s

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    # ── le parcours, étape par étape
    ctx, pg, cdp = ouvre(b)
    s0 = etape(pg, 'prénom')
    if not R6:
        # « Toi, c'est ? » : aucune dalle derrière le texte — aucun pixel PLUS CLAIR que le fond de la Toile vide (#DFCAA4) dans la boîte de la phrase
        r = pg.evaluate("()=>{var e=document.getElementById('onbPh'); var rg=document.createRange(); rg.selectNodeContents(e); var r=rg.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        im = Image.open(io.BytesIO(pg.screenshot(clip={'x': r[0], 'y': r[1], 'width': r[2], 'height': r[3]}))).convert('RGB'); px = im.load(); c = 0; n = 0
        for y in range(0, im.height, 2):
            for x in range(0, im.width, 2):
                q = px[x, y]; n += 1
                if q[0] + q[1] + q[2] > 223 + 202 + 164 + 12: c += 1
        juge('« prénom » : aucune dalle derrière le texte (aucun pixel plus clair que le fond dans la boîte de la phrase)', n > 500 and c * 100.0 / n < 0.5, '%.2f %% de pixels de cellule sur %d' % (c * 100.0 / max(1, n), n))
    prenom(pg, cdp); etape(pg, 'prénom saisi'); parole(pg); etape(pg, 'parole'); saisie(pg); s = etape(pg, 'trait')
    if not R6:
        juge('le mot de trace de l\'onboarding est à 19 px (gardé de v140 : « plus grand »)', s['trace'] == '19px', '%s' % s['trace'])
        pg.wait_for_timeout(1500); s = pg.evaluate(SORTIE)
        pg.wait_for_timeout(2500); s = pg.evaluate(SORTIE)
        juge('aucune main fantôme sur le trait de l\'onboarding, 4 s sans toucher (C-110 : elle ne paraît que sur une fiche à tenir)', not s['main'] and not s['mainNoeud'], 'main : %s' % s['main'])
    trace(pg, cdp); pg.wait_for_timeout(6400); etape(pg, 'fin')
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height*0.36];}")
    for _f in range(5):   # ⚑ v148 (C-124 §9) : « Promi planté ! » pas à pas — un toucher par paragraphe (trois), puis le compte
        if pg.evaluate("()=>{ const v=document.getElementById('onbV'); return !v || v.getAttribute('data-onb-reste')==='fini' || !document.getElementById('onbReste'); }"): break
        toucher(cdp, pg, d[0], d[1])
        for _ in range(80):
            if pg.evaluate("()=>{ const v=document.getElementById('onbV'); if(!v) return true; const r=v.getAttribute('data-onb-reste'); if(r==='fini'||!document.getElementById('onbReste')) return true; const f=window._onbFinPas&&_onbFinPas(); return !f || (!f.enCours && r!==null && String(f.pas)===r); }"): break
            pg.wait_for_timeout(150)
    pg.wait_for_timeout(300); etape(pg, 'fin-reste'); toucher(cdp, pg, d[0], d[1]); pg.wait_for_timeout(1000)
    etape(pg, 'compte'); decl = bool(pg.evaluate("()=>!!(window.TEXTES_ENGAGEMENT&&TEXTES_ENGAGEMENT.sansPlusTard)")); ctx.close()
    avec = [n for n, c, _ in sorties if c and n != 'compte']; compte_ok = any(n == 'compte' and c for n, c, _ in sorties)
    juge('R6, EXCEPTION NOMMÉE (Tom, v144) — aucun « Plus tard » à aucune des %d étapes du parcours ; le compte garde le sien' % (len(sorties) - 1), len(sorties) >= 6 and not avec and compte_ok and decl, 'avec « Plus tard » : %s · exception déclarée par l\'app : %s' % (avec or 'aucune', decl))
    if R6:
        print('R6 %s · exception nommée (Tom, v144 : « le parcours est court, on ne le passe pas ») · %s · %d étapes · avec « Plus tard » : %s' % ('OK' if (len(sorties) >= 6 and not avec and compte_ok and decl) else 'KO', 'exception déclarée' if decl else 'exception NON déclarée', len(sorties), avec or 'aucune'))
        for n, c, t in sorties: print('     R6 · %-14s %s' % (n, ('« %s »' % t) if c else 'aucun « Plus tard »'))
        b.close(); sys.exit(0 if (len(sorties) >= 6 and not avec and compte_ok and decl) else 1)
    b.close()
ok = sum(1 for _, c in res if c)
print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
for n, c, t in sorties: print('     R6 · %-14s %s' % (n, ('« %s »' % t) if c else 'aucun « Plus tard »'))
sys.exit(0 if ok == len(res) else 1)
