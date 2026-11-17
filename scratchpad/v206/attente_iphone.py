"""v207 §2 — l'attente des lettres avec un ouvrier à la cadence de l'iPhone (relevé du 15 nov. : ≈ 50 ms par carte, en file) : chaque ouvrier rend ses
réponses au plus vite toutes les 50 ms. Parcours : onboarding (prénom, la page de la parole, taper, effacer, retaper). On lit le journal du module :
les lettres « lentes » (attendues > 150 ms, puis calculées sur le fil), l'attente avant le premier trait de chaque texte, et (v207) l'attente par lettre."""
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
CLAV = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
LENT = r"""(()=>{ const W0=window.Worker; window.Worker=function(u,o){ const w=new W0(u,o); let der=0; const px={postMessage:(...a)=>w.postMessage(...a), terminate:()=>w.terminate()};
  Object.defineProperty(px,'onmessage',{set(f){ w.onmessage=f?(e=>{ const t=Math.max(performance.now(), der+50); der=t; setTimeout(()=>f(e), t-performance.now()); }):null; }});
  Object.defineProperty(px,'onerror',{set(f){ w.onerror=f; }}); return px; }; })();"""
EV = r"""()=>{ const T=window.TraceLettres; const jj=T.journal.filter(x=>/prepare|trace-fin/.test(x.quoi)).map(x=>[x.quoi,x.t,String(x.texte||'').slice(0,24),x.attente,x.ms]);
  return {jj:jj, j:T.journal.filter(x=>/ouvrier|trace-fin/.test(x.quoi)), att:(T.mesures.att||[]), calc:(T.mesures.calc||[]), cache:T.mesures.cache, etat:T.ouvrierEtat, file:T._file?T._file():null}; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, onb=False, guide=False); ctx.add_init_script(CLAV); ctx.add_init_script(LENT)
    pg = B.ouvre(ctx, F, attente=7000)
    B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(500); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(6000); B.attend_parole(pg)
    B.tap_sel(pg, '#onbPh [data-onb="parole"]'); pg.wait_for_timeout(800); pg.keyboard.type('lire', delay=60); pg.wait_for_timeout(int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    for _ in range(4): pg.keyboard.press('Backspace'); pg.wait_for_timeout(60)
    pg.wait_for_timeout(3000); pg.keyboard.type('lire un livre', delay=50); pg.wait_for_timeout(4000)
    r = pg.evaluate(EV)
    b.close()
J = r['j']; lents = [x for x in J if x['quoi'] == 'ouvrier-lent']; fins = [x for x in J if x['quoi'] == 'trace-fin']
q = lambda L, f: round(sorted(L)[min(len(L) - 1, int(f * len(L)))], 1) if L else None
[print('   ', x) for x in r['jj'][-14:]]
print(F, '·', r['etat'], '·', r['file'])
print('  lettres lentes (> 150 ms, puis calculées sur le fil) :', len(lents), [x['ms'] for x in lents][:12])
print('  attente avant le premier trait, par texte :', [(x['texte'][:22], x['attente']) for x in fins])
if r['att']: print('  attente par lettre attendue (v207) : n %d · p50 %s · p95 %s · max %s ms' % (len(r['att']), q(r['att'], .5), q(r['att'], .95), q(r['att'], 1)))
print('  [ouvriers]', [x for x in J if 'supplementaire' in x['quoi'] or x['quoi'] == 'ouvrier-prouve'])
