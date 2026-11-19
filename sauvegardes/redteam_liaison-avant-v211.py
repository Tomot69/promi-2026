"""⚑ v210 (Tom, 18 nov. 2026, §6) — « de » et « d’ » : « de » devient « d’ » discrètement et en direct quand le mot tapé commence par une voyelle (accentuée ou non)
ou un h muet, et redevient « de » quand on efface ou qu'on change de mot, avec la transition tracée (détracé puis tracé : `_retour.liaison`). Les h aspirés gardent « de »
(haïr, hurler, hausser, honte…). Page + d'un Promi et d'un Chiche (un Cercle n'a pas de « de » : vérifié), et l'onboarding. Une série de mots tapés puis effacés, la
liaison attendue à chaque étape ; chaque changement passe par le tracé (`_douceur.texte`), jamais réécrit d'un coup. WebKit, au doigt, clavier simulé."""
import os, re, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
src = open('redteam_onb_exemple.py', encoding='utf-8').read(); ns = {}
for nom in ('CLAV', 'INIT'):
    m = re.search(r'^%s\s*=\s*(""".*?"""|\'\'\'.*?\'\'\'|"[^\n]*"|\'[^\n]*\')' % nom, src, re.S | re.M)
    if m: ns[nom] = eval(m.group(1))
CLAV = ns.get('CLAV', ''); 
SERIE = [('aller', 'd’'), ('écrire', 'd’'), ('Être', 'd’'), ('ôter', 'd’'), ('habiter', 'd’'), ('hiverner', 'd’'), ('haïr', 'de'), ('hurler', 'de'), ('hausser', 'de'),
         ('honte', 'de'), ('lire', 'de'), ('y aller', 'd’'), ('oui', 'de'), ('11 km', 'de')]
ok = tot = 0
def juge(m, c, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print('  %s %s %s' % ('✅' if c else '❌', m, '' if c else str(d)[:260]), flush=True)
SUIT = """()=>{ window.__lt=[]; const D=window._douceur; if(D && D.texte && !D.__lt){ D.__lt=1; const f=D.texte; D.texte=function(el,a,b){ if(el && el.matches && el.matches('.ph-li, .onbv-de, em')) window.__lt.push([String(a).replace(/<[^>]*>/g,''), String(b).replace(/<[^>]*>/g,'')]); return f.apply(this, arguments); }; } }"""
def norm(s): return (s or '').replace(' ', ' ').strip()
def serie(pg, LI, T):
    for mot, att in SERIE:
        pg.evaluate("()=>{ window.__lt=[]; }")
        pg.keyboard.type(mot, delay=45); pg.wait_for_timeout(1500)
        li = norm(pg.evaluate("(s)=>{ const e=document.querySelector(s); return e?e.textContent:null; }", LI)); lt = pg.evaluate("()=>window.__lt")
        chg = att != 'de'
        juge('%s « %s » → « %s »' % (T, mot, att), li == att and (not chg or any(norm(b) == att for a, b in lt)), [li, lt])
        for _ in range(len(mot)): pg.keyboard.press('Backspace'); pg.wait_for_timeout(40)
        pg.wait_for_timeout(1500); li = norm(pg.evaluate("(s)=>{ const e=document.querySelector(s); return e?e.textContent:null; }", LI)); lt = pg.evaluate("()=>window.__lt")
        juge('%s « %s » effacé → « de »%s' % (T, mot, ', tracé' if chg else ''), li == 'de' and (not chg or any(norm(b) == 'de' for a, b in lt)), [li, lt])
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_liaison — %s · charge %.1f' % (F, B.charge()))
    for k in ('promi', 'chiche', 'nuee'):
        ctx = B.contexte(b, vw=430, vh=932)
        if CLAV: ctx.add_init_script(CLAV)
        pg = B.ouvre(ctx, F)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600); pg.evaluate(SUIT)
        if k == 'nuee':
            t = pg.evaluate("()=>{ const p=document.getElementById('nueePhrase'); return p?p.textContent:''; }")
            juge('[Cercle] la phrase n\'a pas de « de »', not re.search(r"(^|\s)(de|d’)(\s|$)", t.replace(' ', ' ')), t); ctx.close(); continue
        B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1500)
        serie(pg, '#csPhrase .ph-li', '[page + %s]' % k); ctx.close()
    # l'onboarding : la page de la parole
    ctx = B.contexte(b, onb=False, guide=False)
    if CLAV: ctx.add_init_script(CLAV)
    pg = B.ouvre(ctx, F, attente=7000); B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(700)
    pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(400); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200); B.attend_parole(pg); pg.evaluate(SUIT)
    B.tap_sel(pg, '#onbPh [data-onb="parole"]'); pg.wait_for_timeout(1500)
    serie(pg, '#onbPh .onbv-de', '[onboarding]'); ctx.close()
    b.close()
print('\nredteam_liaison : %d/%d' % (ok, tot)); sys.exit(0 if ok == tot else 1)
