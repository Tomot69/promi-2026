"""⚑ v203 (Tom, retours sur 58a4ff9, §1) — L'EXEMPLE REVIENT À CHAQUE EFFACEMENT COMPLET, EN SE TRAÇANT (C-279, C-274).
« Sur la page +, quand on tape puis qu'on efface tout, l'encart en pointillés reste VIDE : la phrase d'exemple ne revient pas. Corrige : l'exemple revient en se traçant,
à chaque effacement complet, sur les trois natures, clavier ouvert et clavier fermé. Juge : taper, tout effacer, 5 fois de suite, à des vitesses différentes. L'exemple est
présent et entier à la fin de chaque effacement. »
Le relevé de l'iPhone de Tom (2026-11-15-1011) : une transition de mot ouverte 30 s, sans tracé ni détracé, née pendant le mouvement du clavier — la transition attendait
pour toujours la fin d'une étape. Non reproduit au banc tel quel : `--panne` fabrique cette panne (le détracé ne rend jamais la main, une fois sur deux) ; la transition
doit s'en relever (v203 : la veille de `lot-V200-DOUCEUR`).
WebKit, 390 × 844 ×3, au doigt (banc_tom), clavier simulé (visualViewport, iOS). Pour chaque nature (Promi, Chiche, Cercle) × clavier ouvert / fermé (Retour après
l'effacement) × 5 passes (frappe à 20, 60, 150, 35, 90 ms ; effacement à la même cadence) :
  A · 3,5 s après l'effacement : la place montre un exemple (non vide), en pointillés (`ph-vide`), aucune transition en cours, aucune découpe (clip-path) sur elle ni
      sur son texte, et l'encre du texte est peinte (lue sur l'image : des pixels d'encre dans la place)
  B · l'exemple est arrivé par un TRACÉ (`TraceLettres.trace` sans `inverse`, sur la place) — jamais posé d'un coup
--natures=promi,chiche,nuee · --panne · --sonde (l'exemple laissé découpé : A rougit) · --fichier="""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
NAT = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--natures=')), ['promi', 'chiche', 'nuee'])
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
INIT = r"""(()=>{ window.__X={traces:[]}; (function arme(){ const T=window.TraceLettres; if(!T || !T.trace){ setTimeout(arme, 50); return; } if(T.__x) return; T.__x=1; const o=T.trace; let n=0;
  T.trace=function(el, c, op){ op=op||{}; if(!op.preparer){ const pl=el && el.closest && el.closest('#csPhrase [data-ph=titre], #nueePhrase [data-np=nom]'); if(pl) window.__X.traces.push({t:performance.now(), inv:!!op.inverse, txt:(el.textContent||'').trim().slice(0,30)});
      if(window.__PANNE && op.inverse && pl && (n++)%2===0){ const sf=op.surFin; op=Object.assign({}, op, {surFin:function(){}}); arguments[2]=op; } }   /* la panne de l'iPhone : le détracé ne rend jamais la main */
    return o.apply(this, arguments); }; })(); })();"""
ETAT = r"""(sel)=>{ const t=document.querySelector(sel); if(!t) return {absent:true}; const i=t.querySelector(':scope > .v200-mt');
  const cp=e=>{ if(!e) return 'none'; const c=getComputedStyle(e).clipPath; return c||'none'; }; const r=t.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390;
  return {txt:(t.textContent||'').trim(), vide:t.classList.contains('ph-vide'), tr:!!(t.__v200 && !t.__v200.fini), cp:cp(t), cpi:cp(i), x:(r.left-d.left)/k, y:(r.top-d.top)/k, w:r.width/k, h:r.height/k}; }"""
def encre(pg, e):
    """des pixels d'encre dans la place : la couleur du texte lue sur l'image (le texte de l'exemple est clair sur le corps)"""
    if e.get('absent') or e['w'] < 20: return 0
    import io
    from PIL import Image
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left, r.top, r.width/390];}")
    k = d[2]; png = pg.screenshot(clip={'x': d[0] + (e['x'] + 14) * k, 'y': d[1] + (e['y'] + 6) * k, 'width': max(4, (e['w'] - 28) * k), 'height': max(4, (e['h'] - 12) * k)})
    im = Image.open(io.BytesIO(png)).convert('RGB'); px = list(im.getdata())
    from collections import Counter
    fond = Counter(px).most_common(1)[0][0]
    return sum(1 for q in px if sum(abs(q[j] - fond[j]) for j in range(3)) > 120)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_exemple_retour — %s · charge %.1f%s' % (F, B.charge(), ' · PANNE' if '--panne' in A else ''))
    for nat in NAT:
        for ferme in (False, True):
            ctx = B.contexte(b); B.toile_pleine(ctx, 10); ctx.add_init_script(CLAV); ctx.add_init_script(INIT)
            if '--panne' in A: ctx.add_init_script("window.__PANNE=1;")
            pg = B.ouvre(ctx, F)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
            sel = '#nueePhrase [data-np=nom]' if nat == 'nuee' else '#csPhrase [data-ph=titre]'
            champ = 'nueeNomIn' if nat == 'nuee' else 'phIn'
            mauvais = []; sans_trace = []
            for i, d in enumerate((20, 60, 150, 35, 90)):
                for _ in range(4):
                    if pg.evaluate("(id)=>{const a=document.activeElement;return !!a&&a.id===id;}", champ): break
                    B.tap_sel(pg, sel); pg.wait_for_timeout(900)
                mot = ('lire', 'nager loin', 'aa', 'courir le matin', 'zut')[i]
                pg.keyboard.type(mot, delay=d); pg.wait_for_timeout(d * 3)
                t0 = pg.evaluate("()=>performance.now()")
                for _ in range(len(mot)): pg.keyboard.press('Backspace'); pg.wait_for_timeout(d)
                if ferme: pg.keyboard.press('Enter')
                pg.wait_for_timeout(3500)
                if '--sonde' in A and i == 2: pg.evaluate("(s)=>{ const t=document.querySelector(s); t.style.setProperty('clip-path','polygon(0px 0px, 0px 0px, 0px 0px)'); }", sel)
                e = pg.evaluate(ETAT, sel); n = encre(pg, e)
                tr = [x for x in pg.evaluate("()=>window.__X.traces") if x['t'] > t0 and not x['inv']]
                ok = (not e.get('absent')) and e['txt'] and e['vide'] and not e['tr'] and e['cp'] == 'none' and e['cpi'] == 'none' and n > 30
                if not ok: mauvais.append((i, mot, {k: e.get(k) for k in ('txt', 'vide', 'tr', 'cp', 'cpi')}, n))
                if not tr: sans_trace.append((i, mot))
            ctx.close()
            nom = '[%s · clavier %s]' % (nat, 'fermé' if ferme else 'ouvert')
            juge(nom + ' A · après chaque effacement (5 passes), l\'exemple est là, entier, en pointillés, peint', not mauvais, mauvais[:3])
            juge(nom + ' B · il est arrivé par son tracé (C-279), jamais d\'un coup', not sans_trace, sans_trace[:3])
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
