"""⚑ v206 (§1, C-282 « la première fois seulement ») — LA TOUTE PREMIÈRE FRAPPE, À FROID.
Tom : la première fois qu'il commence à taper, l'exemple ne part pas comme il faut ; la seconde fois, c'est bon. `redteam_premiere` ne pouvait pas le voir : il tape
« x » puis l'efface AVANT de mesurer — la sortie de l'exemple était donc déjà jouée une fois (le code compilé, les mesures faites, le module des flaques chaud).
Ici, chaque essai part d'un NAVIGATEUR NEUF (WebKit relancé), d'un stockage vierge et d'un cache vide ; on mesure la toute première lettre, puis on efface tout,
on attend le retour de l'exemple et on mesure la seconde. Critères : ceux de redteam_premiere (A à F), pour le premier essai ET pour le second, puis
  G · le premier essai est identique au second : même nombre d'images visibles de la copie à ± 2, même fin à ± 30 ms, opacités image à image à ± 0,12
      (comparées à l'heure depuis la frappe), et aucune image de plus de 50 ms dans les 200 ms qui suivent la première frappe (une image longue = un « coup »).
Lieux : l'onboarding (le prénom — la toute première frappe de l'app) et la page + d'un Promi (le titre). --n=10 (essais par lieu) · --lieux=onboarding,page · --fichier=
  H · (--lent : l'ouvrier du tracé répond 800 ms en retard — le relevé de l'iPhone du 15 nov. : 600 à 924 ms ; la lettre tapée 250 ms après l'ouverture de la place,
      pendant que l'exemple attend ses lettres ou se trace) la copie qui s'efface ne montre JAMAIS plus que ce qu'on voyait de l'exemple à l'image d'avant la frappe :
      rien de visible → copie entièrement découpée ; à moitié tracé → la même découpe ; pas un éclair de l'exemple entier. Lu sur l'IMAGE : l'encre de la place
      (hors des lettres tapées et du curseur) à la première image après la frappe ≤ celle de l'image d'avant + 2 %.
--sonde-froid (la première sortie bloque 260 ms le fil, comme un premier usage pas prêt) : G rougit. Sur v205 (--fichier=zz-v205.html --lent) : H rougit."""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
N = int(next((a.split('=', 1)[1] for a in A_ if a.startswith('--n=')), '10'))
LIEUX = next((a.split('=', 1)[1].split(',') for a in A_ if a.startswith('--lieux=')), ['onboarding', 'page'])
src = open('redteam_premiere.py', encoding='utf-8').read()
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
REC = src.split('REC = r"""')[1].split('"""')[0]
SONDE_F = r"""(()=>{ let fait=0; document.addEventListener('input', ()=>{ if(fait) return; fait=1; requestAnimationFrame(()=>{ const t=performance.now(); while(performance.now()-t<260); }); }, true); })();"""
LENT = r"""(()=>{ const W0=window.Worker; if(!W0) return; window.Worker=function(u,o){ const w=new W0(u,o), D=800, px={ postMessage:(...a)=>w.postMessage(...a), terminate:()=>w.terminate(),
  addEventListener:(t,f,op)=>w.addEventListener(t, t==='message'?(e=>setTimeout(()=>f(e),D)):f, op), removeEventListener:(...a)=>w.removeEventListener(...a) };
  Object.defineProperty(px,'onmessage',{set(f){ w.onmessage=f?(e=>setTimeout(()=>f(e),D)):null; }, get(){ return w.onmessage; }});
  Object.defineProperty(px,'onerror',{set(f){ w.onerror=f; }, get(){ return w.onerror; }}); return px; }; })();"""
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
def mesure(pg, sel, lettre):
    pg.evaluate("()=>{ window.__sc=(document.getElementById('device').getBoundingClientRect().width/390)||1; }")
    pg.evaluate(REC, sel); pg.keyboard.press(lettre); pg.wait_for_timeout(1200)
    I = pg.evaluate("()=>window.__I"); K = pg.evaluate("()=>window.__K")
    ap = [x for x in I if K and x['t'] >= K]
    vis = [x for x in ap if x['w'] and (x['op'] or 0) > 0.02]; gone = [x for x in ap if not x['w'] or (x['op'] or 0) <= 0.02]
    t_gone = round(gone[0]['t'] - K) if gone else None; t_last = round(vis[-1]['t'] - K) if vis else None
    # les images : leurs écarts dans les 200 ms qui suivent la frappe
    ts = [K] + [x['t'] for x in ap if x['t'] - K <= 220]; longues = [round(ts[i] - ts[i - 1]) for i in range(1, len(ts)) if ts[i] - ts[i - 1] > 50]
    sauts = []; prev = None
    for x in ap:
        if not x['w']: break
        if prev is not None and x['op'] >= prev - 1e-4 and prev > 0.02: sauts.append(round(x['t'] - K))
        prev = x['op']
    return {'a': bool(ap) and ap[0]['txt'][:1] == lettre, 'nvis': len(vis), 'gone': t_gone, 'last': t_last, 'longues': longues, 'sauts': sauts,
            'op': [(round(x['t'] - K), round(x['op'], 3)) for x in vis], 'premiere_image': round(ap[0]['t'] - K) if ap else None}
def courbe(m, t):
    """l'opacité de la copie à l'heure t (interpolée ; 0 après sa fin)"""
    P = m['op']
    if not P or t > P[-1][0]: return 0.0
    if t <= P[0][0]: return P[0][1]
    for i in range(1, len(P)):
        if P[i][0] >= t: a, b = P[i - 1], P[i]; return a[1] + (b[1] - a[1]) * (t - a[0]) / max(1, b[0] - a[0])
    return 0.0
HREC = r"""(sel)=>{ window.__H={}; const V='polygon(0px 0px,0px 0px,0px 0px)', cl=e=>e?((e.style.getPropertyValue('clip-path')||'').trim()||'none'):'absent';
  document.addEventListener('keydown', function k(){ document.removeEventListener('keydown', k, true); const pl=document.querySelector(sel), inn=pl&&pl.querySelector(':scope > .v200-mt');
    const c=cl(inn); window.__H.av={clip:c==='none'||c==='absent'?c:(c.replace(/\s+/g,'')===V.replace(/\s+/g,'')?'vide':'partiel'), cv:!!(inn&&inn.__trace&&inn.__trace.canevas&&inn.__trace.canevas.isConnected)};
    requestAnimationFrame(()=>requestAnimationFrame(()=>{ const gh=document.querySelector('.v203-ex'); if(!gh){ window.__H.ap={copie:false}; return; } const sp=gh.querySelector('.v206-vu'), g=cl(gh);
      window.__H.ap={copie:true, gh:g==='none'?'none':(g.replace(/\s+/g,'')===V.replace(/\s+/g,'')?'vide':'autre'), sp:sp?cl(sp):null, op:+getComputedStyle(gh).opacity, txt:(gh.textContent||'').trim().slice(0,30)}; })); }, true); }"""
def h_essai(p, i):
    """H : l'onboarding, la parole ; l'ouvrier lent ; la première lettre pendant que l'exemple attend ses lettres ou se trace"""
    b = p.webkit.launch()
    try:
        ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV); ctx.add_init_script(LENT)
        pg = B.ouvre(ctx, F, attente=7000)
        B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter')
        sel = '#onbPh .onbv-pm[data-onb=parole]'; pg.wait_for_timeout(5000); B.attend_parole(pg)
        for _ in range(4):
            if pg.evaluate("()=>{const a=document.activeElement;return !!a&&a.id==='onbIn';}"): break
            B.tap_sel(pg, sel); pg.wait_for_timeout(900)
        pg.keyboard.press('x'); pg.wait_for_timeout(500); pg.keyboard.press('Backspace')   # l'exemple revient (à froid : ses lettres ne sont pas en cache)
        try: pg.wait_for_function("(s)=>{ const e=document.querySelector(s), i=e&&e.querySelector(':scope > .v200-mt'); const c=i?(i.style.getPropertyValue('clip-path')||'').trim():''; return !!c && c!=='none'; }", arg=sel, timeout=8000, polling=20)
        except Exception: return None
        pg.wait_for_timeout([0, 150, 350, 550, 800, 1100][i % 6])
        pg.evaluate(HREC, sel); pg.keyboard.press('m'); pg.wait_for_timeout(400)
        h = pg.evaluate("()=>window.__H"); ctx.close(); return h
    finally:
        b.close()
def essai(p, lieu, i):
    b = p.webkit.launch()   # un navigateur neuf : aucun cache, aucun code compilé
    try:
        if lieu == 'onboarding': ctx = B.contexte(b, onb=False, guide=False)
        else: ctx = B.contexte(b); B.toile_pleine(ctx, 10)
        ctx.add_init_script(CLAV)
        if '--sonde-froid' in A_: ctx.add_init_script(SONDE_F)
        pg = B.ouvre(ctx, F, attente=7000)
        if lieu == 'onboarding':
            sel, champ = '#onbPh .onbv-pm', 'onbIn'; ouvrir = lambda: B.tap_sel(pg, '#onbPh')
        else:
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2600)
            sel, champ = '#csPhrase [data-ph=titre]', 'phIn'; ouvrir = lambda: B.tap_sel(pg, '#csPhrase [data-ph=titre]')
        for _ in range(4):
            if pg.evaluate("(id)=>{const a=document.activeElement;return !!a&&a.id===id;}", champ): break
            ouvrir(); pg.wait_for_timeout(900)
        pg.wait_for_timeout(1500)   # le tracé de l'exemple fini (comme redteam_premiere : 0 ms après sa fin, au plus tôt)
        m1 = mesure(pg, sel, 'm')
        for _ in range(3): pg.keyboard.press('Backspace'); pg.wait_for_timeout(60)
        pg.wait_for_timeout(3200)   # l'exemple revient par son tracé
        m2 = mesure(pg, sel, 'm')
        ctx.close()
    finally:
        b.close()
    return m1, m2
with sync_playwright() as p:
    print('redteam_premiere_froid — %s · charge %.1f · %d essais par lieu%s' % (F, B.charge(), N, ' · SONDE' if '--sonde-froid' in A_ else ''))
    if '--lent' in A_:
        for i in range(N):
            h = h_essai(p, i)
            if not h or 'av' not in h: juge('[H #%d] la parole en transition, la frappe prise' % (i + 1), False, h); continue
            av, ap = h['av'], h.get('ap') or {}
            if av['clip'] == 'vide' and not av['cv']: ok = (not ap.get('copie')) or ap.get('gh') == 'vide'
            elif av['clip'] in ('vide', 'partiel'): ok = (not ap.get('copie')) or ap.get('gh') == 'vide' or (ap.get('sp') not in (None, 'none'))
            else: ok = True
            juge('[H #%d] avant la frappe : %s%s → la copie : %s' % (i + 1, av['clip'], ' + lettres en cours' if av['cv'] else '', ap), ok)
        LIEUX = []
    for lieu in LIEUX:
        for i in range(N):
            m1, m2 = essai(p, lieu, i)
            for k, m in (('1re', m1), ('2e', m2)):
                ok = m['a'] and m['gone'] is not None and m['gone'] >= 130 and (m['last'] is None or m['last'] <= 170) and not m['sauts']
                juge('[%s #%d · %s frappe] A-C · lettre à l’image, l’exemple parti en %s ms, opacité qui baisse' % (lieu, i + 1, k, m['gone']), ok, '' if ok else m)
            dops = [abs(courbe(m1, t) - courbe(m2, t)) for t in range(0, 160, 8)]
            g = abs(m1['nvis'] - m2['nvis']) <= 2 and m1['gone'] is not None and m2['gone'] is not None and abs(m1['gone'] - m2['gone']) <= 30 and max(dops) <= 0.12 and not m1['longues']
            juge('[%s #%d] G · la 1re frappe identique à la 2e (images %d/%d, fin %s/%s ms, Δopacité max %.2f, images > 50 ms après la 1re : %s)' % (lieu, i + 1, m1['nvis'], m2['nvis'], m1['gone'], m2['gone'], max(dops), m1['longues'] or 'aucune'), g)
print('%d/%d' % (sum(RES), len(RES)))
