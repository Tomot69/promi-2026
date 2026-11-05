#!/usr/bin/env python3
"""redteam_cercle_membres.py — ⚑ v180b (Tom, C-230 suite) : « quand « + Planter dans le Cercle » ouvre un Promi ou un Chiche, les membres du Cercle sont déjà
choisis comme destinataires (« à qui » pour le Promi, « qui ose ? » pour le Chiche). On peut ensuite en retirer. »

Banc WebKit ×3, au doigt, le Cercle « Le potager » (membres Rachel et Marion, banc-etats/etat-cercle.json), clair :
  A · « Un Promi » / « Un Chiche » : la phrase nomme Rachel ET Marion, les deux sont choisies dans la liste (« à qui », « qui ose ? ») ;
  B · Marion retirée au doigt (sa croix dans la liste) : la phrase ne la nomme plus, et 2 s plus tard elle n'est pas revenue ;
  C · la parole plantée : à Rachel seule, dans le Cercle.
Rouge sur v180a (`--fichier=zz-v180a.html`) : « tout le monde ».
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
ETAT = """()=>{ const P=window._phrase||{}, ph=document.getElementById('csPhrase'); return {qui:P.qui||'', sel:(typeof selNuee!=='undefined'?selNuee:null), sens:P.sens,
  txt:ph?(ph.querySelector('.ph-txt')||ph).textContent.replace(/\\s+/g,' ').trim():'', liste:[...document.querySelectorAll('#createSheet .gn .ph-o[data-v].on')].map(b=>b.getAttribute('data-v'))}; }"""
def centre(pg, sel):
    return pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width?[r.left+r.width/2, r.top+r.height/2]:null; }", sel)
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in ('promi', 'chiche'):
        T = '[%s]' % nat
        ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
        mem = pg.evaluate("()=>(NUEEMEM['potager']||[]).filter(n=>!/^moi$/i.test(n))")
        pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(2600)
        c = centre(pg, '#nfAdd')
        if c: pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(500)
        r = centre(pg, '#cpChoix.ouvert .cp-pil[data-k=%s]' % nat)
        if r: pg.touchscreen.tap(r[0], r[1])
        pg.wait_for_timeout(2800); e = pg.evaluate(ETAT)
        cle = 'qui'
        okA = bool(mem) and set(B_ for B_ in mem) == set(x.strip() for x in e['qui'].split(',')) and all(m in e['txt'] for m in mem) and e['sel'] == 'potager'
        juge(T + ' A · les membres du Cercle sont choisis d\'avance : la phrase les nomme', okA, (mem, e))
        q = centre(pg, '#csPhrase .ph-m[data-ph="%s"]' % cle)
        if q: pg.touchscreen.tap(q[0], q[1]); pg.wait_for_timeout(900)
        e1 = pg.evaluate(ETAT)
        juge(T + ' A · dans la liste, les deux sont choisis', set(mem) <= set(e1['liste']), e1['liste'])
        x = centre(pg, '#createSheet .gn .ph-o[data-v="Marion"].on .ppo-x')
        if x: pg.touchscreen.tap(x[0], x[1])
        pg.wait_for_timeout(2200); e2 = pg.evaluate(ETAT)
        juge(T + ' B · Marion retirée au doigt : la phrase ne la nomme plus, elle ne revient pas (2 s)', x and 'Marion' not in e2['qui'] and 'Marion' not in e2['txt'] and 'Rachel' in e2['qui'], e2)
        pg.evaluate("()=>{ const i=document.getElementById('fTitle'); i.value='arroser les tomates'; i.dispatchEvent(new Event('input',{bubbles:true})); }"); pg.wait_for_timeout(300)
        pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2600)
        np = pg.evaluate("()=>{ const q=promises.find(x=>x.title==='arroser les tomates'); return q?{who:q.who, nuee:q.nuee||null, chiche:!!q.chiche}:null; }")
        juge(T + ' C · la parole plantée : à Rachel seule, dans le Cercle', np and np['who'] == 'Rachel' and np['nuee'] == 'potager' and np['chiche'] == (nat == 'chiche'), np)
        juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
