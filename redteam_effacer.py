# -*- coding: utf-8 -*-
"""⚑ v187 (Tom, §3) — EFFACER JUSTE APRÈS UNE PLANTATION : LA PAROLE NE REVIENT JAMAIS.
Sur l'état exporté de Tom (WebKit, banc_tom), au doigt :
  E · 20 fois DE SUITE : planter (par l'app), puis effacer une parole ancienne par la vraie feuille (« Supprimer », touchée au doigt à un instant tiré de 0 à
      700 ms après l'ouverture de la feuille, son arrivée comprise) → elle n'est plus ni dans `promises`, ni dans le stockage, ni dans l'Index ; la feuille
      n'a jamais laissé passer le doigt (aucun clic sous elle) ;
  R · rechargée : aucune des 20 ne revient ;
  T · un SECOND ONGLET, ouvert par l'app avant l'effacement, qui porte encore la parole, y écrit un mot (sur elle et sur une autre), puis les deux onglets
      rechargent → la parole effacée ne revient dans aucun ; le mot sur l'autre parole est gardé ;
  P · la pierre tombale : la parole effacée, réécrite par un enregistrement tardif (l'objet remis dans `promises`), n'est jamais réécrite au stockage ;
  U · « Annuler » la rend, et elle reste après rechargement.
`--fichier=` pour une autre version. Échelle 0,79 : PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79."""
import sys, json, random; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ARG = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
F = ARG.get('fichier', 'app.html'); N = int(ARG.get('n', '20'))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True); return ok
SOUS = "()=>{ window.__sous=[]; document.addEventListener('click',e=>{ if(!e.target.closest('#v16Conf,#v16Toast')) window.__sous.push(e.target.className||e.target.id||e.target.tagName); },true); }"
DANS = "q=>[promises.some(p=>p.id===q), (JSON.parse(localStorage.getItem('promi_state')).promises||[]).some(p=>p.id===q)]"
def efface(pg, q, att):
    pg.evaluate("id=>{ try{_peaufSortie()}catch(e){} closeAll(); openDetail(id); }", q); pg.wait_for_timeout(1600)
    pg.evaluate("()=>{ window.__sous=[]; window._v16SupprimerPromi(cur); }")
    if att: pg.wait_for_timeout(att)
    # le doigt vise la place FINALE du bouton (relevée une fois, la feuille posée) : un vrai doigt vise ce qu'il voit
    pg.touchscreen.tap(CIBLE[0], CIBLE[1])
    pg.wait_for_timeout(900)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx, d = B.contexte_tom(b)
    pg = B.ouvre(ctx, F, 9000); pg.wait_for_timeout(2500); pg.evaluate(SOUS)
    random.seed(187); morts = []
    q0 = pg.evaluate("()=>promises.filter(p=>!p.draft)[0].id")
    pg.evaluate("id=>{ closeAll(); openDetail(id); }", q0); pg.wait_for_timeout(1600); pg.evaluate("()=>window._v16SupprimerPromi(cur)"); pg.wait_for_timeout(900)
    CIBLE = pg.evaluate("()=>{ const r=document.querySelector('.v16-oui').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }")
    pg.evaluate("()=>{ const v=document.getElementById('v16Conf'); if(v) v.remove(); }")
    print('  le bouton « Supprimer », posé : (%.1f ; %.1f)' % tuple(CIBLE), flush=True)
    for k in range(N):
        B.plante(pg, 'planter %d' % k, attente=1400)
        # la parole effacée : la plantation du tour d'avant (au premier tour, une parole ancienne) — juste après la plantation suivante
        q = pg.evaluate("k=>{ const L=promises.filter(p=>!p.draft && p.title===(k?'planter '+(k-1):'')); if(L.length) return L[L.length-1].id; const A=promises.filter(p=>!p.draft && !/^planter \\d+$/.test(p.title||'')); return A.length?A[0].id:null; }", k)
        if q is None: juge('E · il reste une parole ancienne à effacer (%d)' % k, False); break
        att = random.choice([0, 20, 50, 80, 120, 200, 350, 500, 700])
        pg.evaluate(SOUS); efface(pg, q, att)
        en, st = pg.evaluate(DANS, q); sous = pg.evaluate("()=>window.__sous")
        juge('E%02d · effacée juste après une plantation (doigt à %d ms)' % (k, att), not en and not st and not sous, ('promises', en, 'stockage', st, 'clic sous la feuille', sous))
        morts.append(q)
        pg.evaluate("()=>{ const t=document.getElementById('v16Toast'); if(t) t.remove(); }")
    pg.reload(); pg.wait_for_timeout(5000)
    rev = pg.evaluate("L=>L.filter(q=>promises.some(p=>p.id===q))", morts)
    juge('R · rechargée : aucune des %d ne revient' % len(morts), not rev, rev)
    # T · un second onglet qui porte encore la parole
    q = pg.evaluate("()=>{ const L=promises.filter(p=>!p.draft); return L.length>1?[L[0].id,L[1].id]:null; }")
    with ctx.expect_page() as pi: pg.evaluate("()=>window.open(location.pathname+location.search)")
    g = pi.value; g.wait_for_timeout(6000)
    porte = g.evaluate("q=>promises.some(p=>p.id===q)", q[0])
    efface(pg, q[0], 400); en, st = pg.evaluate(DANS, q[0])
    g.evaluate("a=>{ const L=promises.filter(p=>a.includes(p.id)); L.forEach(p=>{ p.comments=(p.comments||[]).concat([{by:'moi',d:Date.now(),t:'second onglet '+p.id}]); }); saveState(); }", q)
    g.wait_for_timeout(800); g.reload(); g.wait_for_timeout(5000); pg.reload(); pg.wait_for_timeout(5000)
    r1 = pg.evaluate("q=>promises.some(p=>p.id===q)", q[0]); r2 = g.evaluate("q=>promises.some(p=>p.id===q)", q[0])
    mot = pg.evaluate("q=>{ const p=promises.find(x=>x.id===q); return !!(p && (p.comments||[]).some(c=>(c.t||'').indexOf('second onglet')===0)); }", q[1])
    juge('T · le second onglet portait la parole', porte)
    juge('T · effacée dans le premier, écrite par le second : elle ne revient dans aucun', not en and not st and not r1 and not r2, (en, st, r1, r2))
    juge('T · le mot du second onglet sur l\'autre parole est gardé', mot)
    g.close()
    # P · la pierre tombale
    q = pg.evaluate("()=>promises.filter(p=>!p.draft)[0].id"); obj = pg.evaluate("q=>JSON.stringify(promises.find(p=>p.id===q))", q)
    efface(pg, q, 400)
    pg.evaluate("s=>{ promises.push(JSON.parse(s)); saveState(true); }", obj); pg.wait_for_timeout(300)
    st = pg.evaluate("q=>(JSON.parse(localStorage.getItem('promi_state')).promises||[]).some(p=>p.id===q)", q)
    pg.reload(); pg.wait_for_timeout(5000); r = pg.evaluate("q=>promises.some(p=>p.id===q)", q)
    juge('P · une écriture tardive ne la fait pas revenir (stockage, puis rechargée)', not st and not r, (st, r))
    # U · Annuler
    q = pg.evaluate("()=>promises.filter(p=>!p.draft)[0].id"); efface(pg, q, 400)
    B.tap_sel(pg, '#v16Toast button'); pg.wait_for_timeout(700)
    a = pg.evaluate("q=>promises.some(p=>p.id===q)", q); pg.reload(); pg.wait_for_timeout(5000); a2 = pg.evaluate("q=>promises.some(p=>p.id===q)", q)
    juge('U · « Annuler » la rend, et elle reste après rechargement', a and a2, (a, a2))
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
