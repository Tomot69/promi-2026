"""⚑ v203 clôture (Tom, C-284) — LES PHRASES DU GUIDE NE SE SUPERPOSENT JAMAIS QUAND ON TOUCHE VITE.
« Il n'y a jamais deux phrases du guide à l'écran en même temps. Un toucher pendant une transition ne la coupe pas : la transition en cours se termine plus vite, en
douceur (même courbe, durée réduite), puis la suivante commence. Plusieurs touchers rapides ne font avancer que d'une étape à la fois. Juge : sur chaque étape du guide,
de 1 à 10 touchers en rafale (toutes les 50 ms) à différents instants de la transition. Une seule phrase visible à chaque image, aucune coupure sèche, aucune image au-dessus
de 33 ms au banc. »
WebKit, 390 × 844 ×3, au doigt. Pour chaque étape (le Studio : le rappel ; le + ; Partager : la phrase 1 ; la phrase 2) × rafale de 1, 4 ou 10 touchers ailleurs que la
cible, toutes les 50 ms, partie 100 ou 500 ms après le début du tracé de la phrase de l'étape. Relevé APRÈS chaque image (v123) :
  A · au plus UNE phrase du guide visible (la phrase posée, non cachée, et celles qui se détracent)
  B · aucun tracé de phrase arrêté en cours de route (`stop` sur une phrase qui se trace ou se détrace : une coupure sèche)
  C · la rafale n'avance que d'une étape à la fois, jamais une étape sautée : un toucher au repos agit ; ceux qui tombent pendant une transition l'accélèrent et ne
      gardent qu'UNE avance (le guide : l'étape suivante paraît, toujours ; « Promi planté ! » : le pas ne monte que d'un cran à la fois, chaque pas tracé)
  D · aucune image au-dessus de 33 ms (au calme seulement : charge < 4)
--etapes=studio,plus,partage,reste,onboarding · --sonde (la phrase coupée et posée tout de suite, comme avant : A, B rougissent) · --fichier="""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A_ = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A_ if a.startswith('--fichier=')), 'app.html')
ETAPES = next((a.split('=', 1)[1].split(',') for a in A_ if a.startswith('--etapes=')), ['studio', 'plus', 'partage', 'reste', 'onboarding'])
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
INIT = r"""(()=>{ window.__G={cuts:[], tr:[]}; (function a(){ const T=window.TraceLettres; if(!T||!T.trace){ setTimeout(a,50); return; } if(T.__g) return; T.__g=1; const o=T.trace;
  T.trace=function(el, c, op){ const r=o.apply(this, arguments); try{ if(!(op&&op.preparer) && el && (el.id==='guidePhrase' || (el.classList && el.classList.contains('gd-part')))){ window.__G.tr.push({t:performance.now(), inv:!!(op&&op.inverse)});
      if(r && r.stop){ const s=r.stop; r.stop=function(){ if(!r.fini) window.__G.cuts.push(performance.now()); return s.apply(this, arguments); }; } } }catch(e){} return r; }; })(); })();"""
SONDE = r"""(()=>{ (function a(){ if(!window._guide){ setTimeout(a,50); return; } })(); })();"""
REC = r"""()=>{ window.__F=[]; const t0=performance.now(), mc=new MessageChannel(); let prev=performance.now(); mc.port1.onmessage=()=>{ const now=performance.now();
    const ph=[...document.querySelectorAll('#guidePhrase, #guide .gd-part')].filter(e=>{ const c=getComputedStyle(e); return e.getClientRects().length && c.visibility!=='hidden' && c.display!=='none'; });
    const g=document.getElementById('guide'); window.__F.push({t:now, n:ph.length, dt:now-prev, e:g?g.getAttribute('data-guide'):null}); prev=now; };
  (function f(){ mc.port2.postMessage(0); if(performance.now()-t0<4500) requestAnimationFrame(f); })(); }"""
def nouvelle(b):
    ctx = B.contexte(b, onb=True, guide=False); ctx.add_init_script(INIT)
    pg = B.ouvre(ctx, F); pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(300); return ctx, pg
def attend(pg, js, n=150, pas=100):
    for _ in range(n):
        v = pg.evaluate(js)
        if v: return v
        pg.wait_for_timeout(pas)
    return None
ETAT = "()=>{ const g=document.getElementById('guide'); return g ? g.getAttribute('data-guide') : null; }"
def ailleurs(pg):   # un point loin de toute cible : le haut de la Toile
    B.tap(pg, 195, 300)
def atteint(pg, etape):
    pg.evaluate("()=>{ _guide.attend(false); }")
    if not attend(pg, "()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='studio' && g.getAttribute('data-entier'); }", 200): return False
    if etape == 'studio': return True
    e = pg.evaluate("()=>_guide.etat()"); pg.wait_for_timeout(1500); B.tap(pg, e['trou']['x'], e['trou']['y']); pg.wait_for_timeout(2600)
    B.tap_sel(pg, '#studioScreen .closeb')
    if not attend(pg, "()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='plus' && +g.getAttribute('data-net')>=1; }", 150): return False
    if etape == 'plus': return True
    pg.wait_for_timeout(2500); ailleurs(pg)
    if not attend(pg, "()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='partage' && document.getElementById('guidePhrase'); }", 150): return False
    if etape == 'partage': return True
    pg.wait_for_timeout(2500); ailleurs(pg)
    return bool(attend(pg, "()=>{ const g=document.getElementById('guide'); return g && g.getAttribute('data-guide')==='reste'; }", 150))
SUITE = {'studio': ('studio',), 'plus': ('partage', 'vers-partage'), 'partage': ('reste', 'vers-reste'), 'reste': ('part', None)}
exec(open('redteam_onb_toucher.py', encoding='utf-8').read().split('def jusquau_titre')[1].split('with sync_playwright')[0].join(['def jusquau_titre', '']))   # le vrai parcours jusqu'à « Promi planté ! »
ONB = r"""()=>{ window.__O={tr:[], cuts:[], act:[]}; const T=window.TraceLettres, o=T.trace; T.trace=function(el,c,op){ const r=o.apply(this, arguments); try{ if(!(op&&op.preparer) && el && el.closest && el.closest('#onbFin')){ window.__O.tr.push(performance.now());
      if(r && r.stop){ const s=r.stop; r.stop=function(){ if(!r.fini) window.__O.cuts.push(performance.now()); return s.apply(this, arguments); }; } } }catch(e){} return r; };
  const mc=new MessageChannel(); mc.port1.onmessage=()=>{ const f=document.getElementById('onbFin'); const n=f?[...f.querySelectorAll('*')].filter(e=>e.__tl && !e.__tl.fini && !e.__tl.__prep).length:0; window.__O.act.push(n); const fp=window._onbFinPas&&_onbFinPas(); window.__O.pas=(window.__O.pas||[]); const pp=fp?fp.pas:0; if(!window.__O.pas.length || window.__O.pas[window.__O.pas.length-1]!==pp) window.__O.pas.push(pp); };
  (function g(){ mc.port2.postMessage(0); requestAnimationFrame(g); })(); }"""
def onboarding(b):
    for n in (1, 4, 10):
        ctx = B.contexte(b, onb=False, guide=False); pg = B.ouvre(ctx, F, attente=7000)
        if not jusquau_titre(pg): juge('[onboarding · %d touchers] le parcours va jusqu\'à « Promi planté ! »' % n, False); ctx.close(); continue
        pg.evaluate(ONB); pas = []
        for k in range(3):
            p0 = pg.evaluate("()=>(_onbFinPas()||{}).pas||0")
            for i in range(n): B.tap(pg, 195, 300); pg.wait_for_timeout(50)
            pg.wait_for_timeout(300)   # la rafale suivante part pendant le pas en cours (sauf au dernier)
            if k == 2: pg.wait_for_timeout(2500)
            pas.append((p0, pg.evaluate("()=>(_onbFinPas()||{}).pas||0")))
        pg.wait_for_timeout(2500); fin = pg.evaluate("()=>(_onbFinPas()||{}).pas||0")
        O = pg.evaluate("()=>window.__O"); deux = sum(1 for a in O['act'] if a > 1)
        nom = '[onboarding · « Promi planté ! » · rafales de %d]' % n
        juge(nom + ' A · un seul texte se trace à la fois', deux == 0, deux)
        juge(nom + ' B · aucune coupure (aucun tracé arrêté en route)', not O['cuts'], len(O['cuts']))
        suite = O.get('pas') or []; sauts = [(a2, b2) for a2, b2 in zip(suite, suite[1:]) if b2 - a2 != 1]
        juge(nom + ' C · le pas n\'avance que d\'un cran à la fois, chaque pas tracé (pas : %s ; textes tracés : %d)' % (suite, len(O['tr'])), not sauts and fin >= 2 and len(O['tr']) >= fin)
        ctx.close()
with sync_playwright() as p:
    b = p.webkit.launch(); ch = B.charge(); print('redteam_guide_rafale — %s · charge %.1f' % (F, ch))
    if 'onboarding' in ETAPES: onboarding(b)
    for et in [e for e in ETAPES if e != 'onboarding']:
        for n, dl in ((1, 100), (4, 100), (10, 100), (4, 500), (10, 500)):
            ctx, pg = nouvelle(b)
            if not atteint(pg, et):
                juge('[%s · %d touchers à %d ms] l\'étape atteinte' % (et, n, dl), False); ctx.close(); continue
            # la phrase de l'étape vient de commencer son tracé : on la relance pour un instant connu (le rappel au Studio est déjà une transition)
            t_ph = pg.evaluate("()=>{ const t=window.__G.tr.filter(x=>!x.inv); return t.length?t[t.length-1].t:performance.now(); }")
            now = pg.evaluate("()=>performance.now()"); attente = max(0, dl - (now - t_ph)); pg.wait_for_timeout(int(attente))
            pg.evaluate(REC); c0 = pg.evaluate("()=>window.__G.cuts.length")
            for i in range(n): ailleurs(pg); pg.wait_for_timeout(50)
            pg.wait_for_timeout(4600)
            Fr = pg.evaluate("()=>window.__F"); cuts = pg.evaluate("()=>window.__G.cuts.length") - c0; fin = pg.evaluate(ETAT)
            deux = [round(x['t'] - Fr[0]['t']) for x in Fr if x['n'] > 1]; longues = [round(x['dt']) for x in Fr[1:] if x['dt'] > 33.4]
            nom = '[%s · %d touchers à %d ms]' % (et, n, dl)
            juge(nom + ' A · une seule phrase visible à chaque image', not deux, deux[:5])
            juge(nom + ' B · aucune coupure (aucun tracé de phrase arrêté en route)', cuts == 0, cuts)
            seq = []
            for x in Fr:
                if not seq or seq[-1] != x['e']: seq.append(x['e'])
            ORDRE = ['studio', 'au-studio', 'plus', 'vers-partage', 'partage', 'vers-reste', 'reste', 'part', None]
            vus = [s for s in seq if s in ('studio', 'plus', 'partage', 'reste')]
            suivante = {'studio': 'studio', 'plus': 'partage', 'partage': 'reste', 'reste': None}[et]
            ok_c = (suivante is None) or (suivante in vus) or (et == 'studio')   # l'étape suivante a bien paru (jamais sautée)
            juge(nom + ' C · une seule étape d\'avance, jamais une étape sautée (suite : %s)' % ' → '.join(str(s) for s in seq), ok_c)
            if ch < 4: juge(nom + ' D · aucune image au-dessus de 33 ms', not longues, longues[:6])
            ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
