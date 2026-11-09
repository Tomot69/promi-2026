# v191 A2 — l'état exporté de Tom (sa fenêtre 390 × 651, son stockage) : Promi et Chiche, défilés aller et retour.
# Avant l'accrochage : la zone de la jonction identique à v190 au pixel ; après : la loi de l'aplatissement ; la zone du geste coupée ; une planche pour l'œil.
import sys, io; sys.path.insert(0,'.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
def ouvre(b, F, quoi):
    ctx, e = B.contexte_tom(b); ctx.add_init_script(BJ.AMORCE); pg = B.ouvre(ctx, F, 7000)
    r = pg.evaluate("""q=>{ closeAll(); const p=promises.find(x=>!x.draft&&!x.nuee&&(q==="chiche"?!!x.chiche:!x.chiche)); if(!p) return null; p.comments=[["Marion","On commence quand ?"],["Rachel","Je m’occupe de la farine."],["Nico","Samedi matin ?"]].map((c,i)=>({t:c[1],by:c[0],d:"2026-11-0"+(i+1)+"T09:00:00Z",vu:true})); openDetail(p.id); return p.title; }""", quoi)
    for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(600); return ctx, pg, r
with sync_playwright() as p:
    b = p.webkit.launch()
    for quoi in ('promi','chiche'):
        ctx, pg, r = ouvre(b, 'app.html', quoi)
        if not r: print(quoi, ': aucune'); ctx.close(); continue
        pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=1; }"); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
        J = pg.evaluate("()=>{ const j=_v189Jonction(); const d=document.getElementById('detailPoster'); return [j.F&&j.F.s0, d.scrollHeight-d.clientHeight]; }")
        s0, smax = J; s0 = s0 if s0 is not None else 9e9; print(quoi, "défilement possible", smax); avant = [s for s in BJ.PAS if s < s0 - 0.5]
        A = BJ.images(pg, avant)
        loi = []; im = []
        for s in [x for x in range(0, int(min(smax, s0 + 60)) + 1, 2)] + [x for x in range(int(min(smax, s0 + 60)), -1, -2)]:
            pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}", s); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
            v = pg.evaluate("()=>{ const c=document.getElementById('v189Jonction'), z=document.getElementById('tenirZone'), d=document.getElementById('detailPoster'); const on=c&&getComputedStyle(c).display!=='none'; return [d.scrollTop, on?+(c.getAttribute('data-jonction')||'').split(',')[1]:null, getComputedStyle(z).pointerEvents]; }")
            att = None if v[0] < s0 else min(1, (v[0] - s0) / 40)
            if (v[1] is None) != (att is None) or (att is not None and abs(v[1] - att) > 0.012) or ((att is not None) != (v[2] == 'none')): loi.append(v)
        d = B.dev(pg); k = d[4]
        for s in ((0, s0 + 10, s0 + 25, s0 + 45) if s0 < 1e8 else (0, smax/3, 2*smax/3, smax)):
            pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}", s); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
            full = Image.open(io.BytesIO(pg.screenshot())); q = full.size[0] / pg.evaluate("()=>innerWidth")
            im.append(full.crop((int(d[0]*q), int(d[1]*q), int((d[0]+390*k)*q), int((d[1]+420*k)*q))))
        er = pg.erreurs[:]; ctx.close()
        c2, p2, _ = ouvre(b, 'zz-v190.html', quoi); Bv = BJ.images(p2, avant); c2.close()
        e = [(x[0], BJ.ecart(x, y)) for x, y in zip(A, Bv)]
        W, H = im[0].size; m = Image.new('RGB', (W*4, H), 'white')
        for i, x in enumerate(im): m.paste(x, (i*W, 0))
        m.save('scratchpad/v191/a2-tom-mots-%s.png' % quoi)
        print(quoi, r, 's0 %.1f smax %.0f' % (s0, smax), '| avant l\'accrochage :', len(e), 'pas,', len([z for z in e if z[1]]), 'différents | loi et geste :', len(loi), 'écarts', loi[:3], '| erreurs', er[:2])
    b.close()
