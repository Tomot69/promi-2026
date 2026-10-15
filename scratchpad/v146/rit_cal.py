# §10 — étalonnage du cadre : 15 paroles plantées une fois au doigt, puis chaque sous-ensemble 1…15 par Toile.sync (places gardées), plusieurs cadres
import sys, json; sys.path.insert(0, '.'); sys.argv += ['--n=15']
exec(open('scratchpad/v146/rit_mesure.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0])
CADRES = [(None, None)]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    pg.evaluate("()=>{ try{ Toile.setTheme('ritournelle'); }catch(e){} }"); pg.wait_for_timeout(1500)
    for i in range(15): B.plante(pg, TITRES[i], attente=1800)
    pg.wait_for_timeout(4000); ids = pg.evaluate("()=>promises.filter(p=>!p.draft).map(p=>p.id)")
    for C in CADRES:
        pg.evaluate("(c)=>{ window._ritCadre=c[0]; window._ritPartMin=c[1]; }", C); ligne = []
        for k in range(1, 16):
            pg.evaluate("(ids)=>{ Toile.sync(ids); }", ids[:k]); pg.wait_for_timeout(2600)
            e = pg.evaluate("()=>{ var v=Toile.vue(); return {vue:[v.s,v.ox,v.oy], formes:(window._ritFormes||[]).slice(), n:Toile_graines().length}; }")
            vis, cov = mesure(e) if e['formes'] else ([0], 0)
            ligne.append('%d:%2.0f/%2.0f' % (k, 100 * min(vis), 100 * cov))
            if k in (1, 3, 6, 9, 12, 15): B.capture(pg, 'scratchpad/v146/rit-cadre-%02d.png' % k)
        print(C, ' '.join(ligne), flush=True)
    b.close()
