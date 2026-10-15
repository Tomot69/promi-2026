# §9 — des choix précis, au doigt, et l'état suivi pendant 4 s (une fermeture peut venir après coup)
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
exec(open('scratchpad/v146/peauf_sonde2.py', encoding='utf-8').read().split('def tous')[0].split('from playwright.sync_api import sync_playwright')[1])
SUIT = """()=>{ window.__suit=[]; const t0=performance.now(); (function f(){ const dp=document.getElementById('detailPoster'), cs=document.getElementById('createSheet'); const s=(dp&&dp.classList.contains('show')?'F':'-')+(dp&&dp.classList.contains('s2-ouv')?'P':'-')+(cs&&cs.classList.contains('show')?'+':'-')+(cs&&cs.classList.contains('pp-peauf')?'p':'-');
  const L=window.__suit; if(!L.length||L[L.length-1][1]!==s) L.push([Math.round(performance.now()-t0), s]); if(performance.now()-t0<4500) requestAnimationFrame(f); })(); }"""
CAS = [(True, None, 'RÉCURRENCE', None), (True, None, 'RAPPEL', None), (True, None, "C'EST IMPORTANT ?", None), (True, None, 'LA COULEUR', None), (True, None, 'LA MÉMOIRE', None),
       (False, None, 'RÉCURRENCE', None), (False, None, "C'EST IMPORTANT ?", None), (False, None, 'LA COULEUR', None), (False, None, 'AVANT', '2 j'), (False, None, 'AVANT', '+ tard')]
with sync_playwright() as p:
    b = p.webkit.launch()
    for fiche, titre, lab, choix in CAS:
        rac = '#detailPoster' if fiche else '#createSheet'
        ctx = B.contexte(b); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx)
        if fiche: pg.evaluate("(t)=>{ closeAll(); const q=promises.filter(q=>t?q.title===t:(!q.done&&q.who&&q.who!=='moi'&&!q.nuee))[0]; openDetail(q.id); }", titre)
        else: pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); var n=0; (function e(){ var x=[...document.querySelectorAll('#createSheet .tile')][0]; var cs=document.getElementById('createSheet'); if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(e,350); })(); }")
        pg.evaluate('()=>setPremium(true)'); pg.wait_for_timeout(2600); B.tap_sel(pg, '#dpDetails .dpd-tog' if fiche else '#csBotBar'); pg.wait_for_timeout(1100)
        o = pg.evaluate(OPTS, [rac, lab]); pg.wait_for_timeout(300); o = pg.evaluate(OPTS, [rac, lab])
        if not o: print(lab, 'absent'); ctx.close(); continue
        B.tap(pg, *o['titre']); pg.wait_for_timeout(900); o = pg.evaluate(OPTS, [rac, lab])
        print('   options', [(x['t'], x['cl']) for x in o['opts']][:10]); opts = [x for x in o['opts'] if x['t'] and ' on' not in ' ' + x['cl'] and x['tag'] not in ('INPUT', 'TEXTAREA')]
        c = next((x for x in opts if choix and x['t'] == choix), opts[0] if opts else None)
        if not c: print('%-6s %-16s aucun choix : %s' % ('fiche' if fiche else 'page+', lab, [x['t'] for x in o['opts']][:8])); ctx.close(); continue
        pg.evaluate(SUIT); B.tap(pg, c['x'], c['y']); pg.wait_for_timeout(4800)
        print('%-6s %-16s « %s » → %s' % ('fiche' if fiche else 'page+', lab, c['t'], pg.evaluate("()=>window.__suit")), pg.evaluate("()=>[...document.querySelectorAll('.screen.show,.sheet.show,.poster.show,.show[id]')].map(e=>e.id).join(' ')"))
        B.capture(pg, 'scratchpad/v146/peauf-%s-%s.png' % ('fiche' if fiche else 'plus', lab.replace(' ', '')[:8]))
        ctx.close()
    b.close()
