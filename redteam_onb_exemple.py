"""⚑ v203 clôture (Tom, C-282) — ONBOARDING : LA PHRASE D'EXEMPLE REVIENT EN SE TRAÇANT, PAR LE CODE DE LA PAGE +.
« Dans l'onboarding, quand on écrit puis efface sa phrase du premier Promi, la phrase d'exemple réapparaît d'un coup. L'onboarding utilise EXACTEMENT le même code
que la page + pour le retour de l'exemple (C-274, avec la veille de 300 ms) et pour le tracé et le détracé (C-279). À la première lettre tapée, l'exemple se détrace,
comme sur la page +, et la lettre apparaît immédiatement (Q620). Juge : dans l'onboarding, taper puis tout effacer 5 fois, à 5 vitesses, clavier ouvert et fermé.
L'exemple se trace entier à chaque fois. Séquence comparée image par image à celle de la page +, identique. »
WebKit, 390 × 844 ×3, au doigt (banc_tom), clavier simulé (iOS). Onboarding (stockage vierge : le prénom, puis la page de la parole) et page + d'un Promi, chacun
clavier ouvert et clavier fermé (le champ quitté après l'effacement), 5 passes (frappe et effacement à 20, 60, 150, 35, 90 ms). Chaque tracé de la place et de la
copie de l'exemple (`TraceLettres.trace`) est relevé dans la page, avec son début, sa fin et son sens :
  A · 3,5 s après l'effacement : la place montre l'exemple entier (son texte), vide, aucune transition en cours, aucune découpe, son encre peinte (lue sur l'image)
  B · il est revenu par un TRACÉ (jamais posé d'un coup)
  C · à la première lettre : la lettre est dans la place à l'image qui suit, et l'exemple se DÉTRACE (une copie, à rebours)
  D · la séquence de l'onboarding est celle de la page + : les mêmes étapes, dans le même ordre (détracé de la copie de l'exemple à la première lettre, détracé de
      ce qu'on a tapé puis tracé de l'exemple à l'effacement), sur les 5 passes
  D2 · le tracé de l'exemple, à la cadence du module (40 car/s, une lettre en 70 à 90 ms : ≤ 45 ms par caractère). La durée de chaque pas (ms par caractère) varie
      avec la préparation des lettres (leur dessin calculé ou repris du cache) et la charge : elle n'est pas comparée d'une page à l'autre au pixel près.
  E · le prénom (la page d'avant) : effacé, « ton prénom » revient par son tracé
--sonde (l'onboarding repeint d'un coup comme avant : B et D rougissent) · --fichier="""
import sys, io, json; sys.path.insert(0, '.')
import banc_tom as B
from collections import Counter
from PIL import Image
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
PLACES = "#onbPh .onbv-pm, #csPhrase [data-ph=titre]"
INIT = r"""(()=>{ window.__X={tr:[]}; (function arme(){ const T=window.TraceLettres; if(!T || !T.trace){ setTimeout(arme, 50); return; } if(T.__x) return; T.__x=1; const o=T.trace;
  T.trace=function(el, c, op){ op=op||{}; if(!op.preparer && el && el.closest){ const pl=el.closest('%s'), ex=el.closest('.v203-ex'); if(pl || ex){ const r={t:performance.now(), inv:!!op.inverse, ex:!!ex, n:(el.textContent||'').trim().length, fin:null}; window.__X.tr.push(r);
      const sf=op.surFin; op=Object.assign({}, op, {surFin:function(){ r.fin=performance.now(); if(sf) return sf.apply(this, arguments); }}); arguments[2]=op; } }
    return o.apply(this, arguments); }; })(); })();""" % PLACES
SONDE_SEC = r"""(()=>{ (function a(){ const D=window._douceur; if(!D || !D.place){ setTimeout(a, 50); return; } D.place=function(){ return false; }; })(); })();"""   # l'onboarding comme avant : repeint d'un coup
ETAT = r"""(sel)=>{ const t=document.querySelector(sel); if(!t) return {absent:true}; const i=t.querySelector(':scope > .v200-mt'); const cp=e=>e?(getComputedStyle(e).clipPath||'none'):'none';
  const r=t.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390;
  return {txt:(t.textContent||'').trim(), vide:t.classList.contains('vide')||t.classList.contains('ph-vide'), tr:!!(t.__v200 && !t.__v200.fini), cp:cp(t), cpi:cp(i), x:(r.left-d.left)/k, y:(r.top-d.top)/k, w:r.width/k, h:r.height/k}; }"""
def encre(pg, e):
    if e.get('absent') or e['w'] < 20: return 0
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.width/390];}"); k = d[2]
    im = Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0] + (e['x'] + 6) * k, 'y': d[1] + (e['y'] + 4) * k, 'width': max(4, (e['w'] - 12) * k), 'height': max(4, (e['h'] - 8) * k)}))).convert('RGB'); px = list(im.getdata())
    fond = Counter(px).most_common(1)[0][0]; return sum(1 for q in px if sum(abs(q[j] - fond[j]) for j in range(3)) > 120)
def norm(s): return ' '.join(s.replace('“', '"').replace('”', '"').split())
VITESSES = (20, 60, 150, 35, 90); MOTS = ('lire', 'nager loin', 'aa', 'courir le matin', 'zut')
def passes(pg, sel, champ, ferme, ouvrir, exemple):
    out = []
    for i, d in enumerate(VITESSES):
        for _ in range(4):
            if pg.evaluate("(id)=>{const a=document.activeElement;return !!a&&a.id===id;}", champ): break
            ouvrir(); pg.wait_for_timeout(900)
        mot = MOTS[i]; t0 = pg.evaluate("()=>performance.now()")
        pg.keyboard.press(mot[0]); pg.wait_for_timeout(34); prem = pg.evaluate("(s)=>{ const t=document.querySelector(s); return t?(t.textContent||''):''; }", sel)
        fondu = pg.evaluate("()=>{ const g=document.querySelector('.v203-exw .v203-ex'); if(!g) return null; const o=parseFloat(getComputedStyle(g).opacity); return o; }")   # v205 (C-282) : la copie de l'exemple, en fondu
        pg.keyboard.type(mot[1:], delay=d); pg.wait_for_timeout(d * 3 + 400)
        t1 = pg.evaluate("()=>performance.now()")
        for _ in range(len(mot)): pg.keyboard.press('Backspace'); pg.wait_for_timeout(d)
        if ferme: pg.evaluate("()=>{ const a=document.activeElement; if(a && a.blur) a.blur(); }")
        pg.wait_for_timeout(3500)
        e = pg.evaluate(ETAT, sel); n = encre(pg, e); tr = pg.evaluate("()=>window.__X.tr")
        out.append({'e': e, 'n': n, 'prem': prem, 'fondu': fondu, 'mot': mot, 'avant': [x for x in tr if t0 <= x['t'] < t1], 'apres': [x for x in tr if x['t'] >= t1], 'ex': exemple})
    return out
def sig(p):
    """les étapes d'une passe : à la première lettre, à l'effacement — leur sens, et leur cadence (ms par caractère)"""
    s = []
    for nom in ('avant', 'apres'):
        for x in p[nom]:
            cad = round((x['fin'] - x['t']) / max(1, x['n']), 1) if x['fin'] else None
            s.append((nom, 'détracé' if x['inv'] else 'tracé', 'copie' if x['ex'] else 'place', cad))
    return s
def onboarding(b, ferme, sonde):
    ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV); ctx.add_init_script(INIT)
    if sonde: ctx.add_init_script(SONDE_SEC)
    pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(700)
    # E · le prénom
    pg.keyboard.type('Ca', delay=60); pg.wait_for_timeout(400); t1 = pg.evaluate("()=>performance.now()")
    for _ in range(2): pg.keyboard.press('Backspace'); pg.wait_for_timeout(60)
    pg.wait_for_timeout(3000); e = pg.evaluate(ETAT, '#onbPh .onbv-pm[data-onb=prenom]'); tr = [x for x in pg.evaluate("()=>window.__X.tr") if x['t'] >= t1 and not x['inv']]
    pn = (e, tr)
    pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(400); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200); B.attend_parole(pg)
    sel = '#onbPh .onbv-pm[data-onb=parole]'
    P = passes(pg, sel, 'onbIn', ferme, lambda: B.tap_sel(pg, '#onbPh [data-onb="parole"]'), 'ne plus dire “je commence lundi”')
    ctx.close(); return P, pn
def pageplus(b, ferme):
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); ctx.add_init_script(CLAV); ctx.add_init_script(INIT); pg = B.ouvre(ctx, F)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
    sel = '#csPhrase [data-ph=titre]'; ex = pg.evaluate("(s)=>{ const t=document.querySelector(s); return (t.textContent||'').trim(); }", sel)
    P = passes(pg, sel, 'phIn', ferme, lambda: B.tap_sel(pg, sel), ex)
    ctx.close(); return P
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_onb_exemple — %s · charge %.1f%s' % (F, B.charge(), ' · SONDE' if '--sonde' in A_ else ''))
    for ferme in (False, True):
        nom = 'clavier %s' % ('fermé' if ferme else 'ouvert')
        O, pn = onboarding(b, ferme, '--sonde' in A_)
        if not ferme:
            juge('[onboarding · prénom] E · effacé, « ton prénom » revient par son tracé', norm(pn[0].get('txt', '')) == 'ton prénom' and pn[0].get('vide') and pn[1], {'txt': pn[0].get('txt'), 'tracés': len(pn[1])})
        PP = pageplus(b, ferme)
        mauvais = [(i, o['mot'], {k: o['e'].get(k) for k in ('txt', 'vide', 'tr', 'cp', 'cpi')}, o['n']) for i, o in enumerate(O)
                   if not (norm(o['e'].get('txt', '')) == norm(o['ex']) and o['e'].get('vide') and not o['e'].get('tr') and o['e'].get('cp') == 'none' and o['e'].get('cpi') == 'none' and o['n'] > 30)]
        juge('[onboarding · %s] A · après chaque effacement (5 passes), l\'exemple entier, vide, peint' % nom, not mauvais, mauvais[:2])
        sans = [(i, o['mot']) for i, o in enumerate(O) if not any(not x['inv'] and not x['ex'] for x in o['apres'])]
        juge('[onboarding · %s] B · il revient par son tracé, jamais d\'un coup' % nom, not sans, sans)
        # ⚑ v205 (Tom, C-282) : à la première lettre l'exemple part en entier en 150 ms, en fondu — plus de détracé (contrat de v203 : sauvegardes/redteam_onb_exemple-avant-v205.py)
        c = [(i, o['mot'], o['prem'][:12], o['fondu']) for i, o in enumerate(O) if not (o['prem'].strip().startswith(o['mot'][0]) and o['fondu'] is not None and 0 < o['fondu'] < 1 and not any(x['inv'] and x['ex'] for x in o['avant']))]
        juge('[onboarding · %s] C · la première lettre paraît tout de suite, l\'exemple part en fondu (aucun détracé)' % nom, not c, c)
        ec = []
        for i, (o, q) in enumerate(zip(O, PP)):
            so, sq = sig(o), sig(q); eo, eq = [x[:3] for x in so], [x[:3] for x in sq]
            if eo != eq: ec.append({'passe': i, 'onboarding': so, 'page +': sq})
        juge('[%s] D · la séquence de l\'onboarding est celle de la page + : les mêmes étapes, dans le même ordre, sur les 5 passes' % nom, not ec, ec[:1])
        cad = [(i, x[3]) for i, o in enumerate(O) for x in sig(o) if x[0] == 'apres' and x[1] == 'tracé' and (x[3] is None or x[3] > 45)]
        juge('[%s] D2 · l\'exemple de l\'onboarding se trace à la cadence du module (40 car/s : ≤ 45 ms par caractère) — page + : %s' % (nom, [x[3] for o in PP for x in sig(o) if x[0] == 'apres' and x[1] == 'tracé']), not cad, cad)
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
