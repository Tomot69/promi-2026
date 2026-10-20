#!/usr/bin/env python3
"""redteam_tenir_presse.py — ⚑ v154 (Tom, C-167) : LE VERT DE « PAROLE TENUE ! » RESTE 400 ms DE PLUS ; UN TOUCHER LE FAIT REMONTER.

« Après validation, le vert avec "Parole tenue !" reste 400 ms de plus avant de remonter. Même chose pour toutes les phrases de validation. » Décision du
chef de chantier : un toucher n'importe où pendant ce temps fait remonter le vert tout de suite et mène à la fiche tenue (sans toucher, le retour se fait
seul). Banc comme Tom (WebKit 390 × 844 ×3, le trait tracé au doigt), lu sur les PIXELS du rideau (le front, image par image) :
  D · l'app déclare 2 400 ms (`_tenirRegle.AMANDE`)
  A · Promi (« Parole tenue ! ») et Chiche (« Défi relevé ! »), sans toucher : le vert commence de remonter 2 250 à 2 700 ms après le lever (v153 : ≈ 2 000)
  B · un toucher sur la barre Peaufiner 1 300 ms après le lever : le vert commence de remonter dans les 150 ms ; la parole est tenue ; le rideau parti au
      moins 700 ms plus tôt que sans toucher ; le toucher est AVALÉ (Peaufiner ne s'ouvre pas, la fiche reste ouverte)
  C · un toucher 100 ms après le lever (le geste qui finit) ne presse rien : la remontée garde son heure
R4 (l'invariance) reste jugé par redteam_tenir_e3 --r4. Preuve : `--fichier=zz-av153.html` rougit (D, A, B).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
# la sonde de redteam_tenir_e3 (le front du rideau, image par image, lu sur ses pixels)
SONDE = """()=>{ window.__lever=0; window.__img=[]; window.__hap=[];
  const hp=window.promiHaptique; window.promiHaptique=function(n){ window.__hap.push([performance.now(), n, !!document.getElementById('tenirMaree')]); if(hp) return hp.apply(this, arguments); };
  document.addEventListener('touchend', function(){ if(!window.__lever) window.__lever=performance.now(); }, {capture:true, once:true});
  window._mareeReleve=function(g, cv, t, u, T){ const k=cv.width/390, W=cv.width, H=cv.height; const fr=[];
    for(const x of [40,100,160,220,280,340]){ const col=g.getImageData(Math.round(x*k),0,1,H).data; let bas=-1; for(let y=H-1;y>=0;y--){ if(col[4*y+3]>200){ bas=y/k; break; } } if(bas>T.y(x)+9) fr.push(bas); }
    fr.sort((a,b)=>a-b); window.__img.push([performance.now(), fr.length>=3?fr[fr.length>>1]:null]); };
  (function f(){ const m=!!document.getElementById('tenirMaree'); (window.__pres=window.__pres||[]).push([performance.now(), m]); if(window.__pres.length<600) requestAnimationFrame(f); })(); }"""
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
def tenir(b, chiche, touche=None):
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    B.plante(pg, 'rendre le livre', nature=1 if chiche else 0); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
    pg.evaluate(SONDE)
    z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
    y = z[1] + z[3] * 0.45
    B.glisse(pg, [[200 + 150 * i / 10, y] for i in range(11)], pas=30, tenue=380)
    tt = None
    if touche is not None:
        for _ in range(200):
            l = pg.evaluate("()=>window.__lever? performance.now()-window.__lever : -1")
            if l >= touche - 15: break
            pg.wait_for_timeout(10)
        pg.evaluate("()=>{ window.__tt=performance.now(); }"); B.tap(pg, 195, 790); tt = pg.evaluate("()=>window.__tt-window.__lever")
    for _ in range(40):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>{ const P=window.__pres||[]; const vu=P.findIndex(x=>x[1]); return vu>=0 && P.slice(vu).some(x=>!x[1]); }"): break
    pg.wait_for_timeout(500)
    d = pg.evaluate("()=>{ const dp=document.getElementById('detailPoster'); return {lev:window.__lever, img:window.__img, pres:window.__pres, st:promises[promises.length-1].status, ouvert:dp.classList.contains('show'), peauf:dp.classList.contains('s2-ouv'), txt:(document.getElementById('instTenue')||{}).textContent||null}; }")
    L = d['lev'] or 0; img = [(t - L, f) for t, f in d['img'] if f is not None]
    fr = [f for t, f in img]; mx = max(fr) if fr else 0
    i_max = next((i for i, f in enumerate(fr) if f >= mx - 1), 0)
    monte = next((t for t, f in img[i_max:] if f < mx - 2), None)
    vu = next((i for i, x in enumerate(d['pres']) if x[1]), None)
    repos = next((x[0] - L for x in d['pres'][vu:] if not x[1]), None) if vu is not None else None
    er = [x for x in pg.erreurs if 'version.json' not in x]; ctx.close()
    return {'er': er, 'monte': monte, 'repos': repos, 'st': d['st'], 'tt': tt, 'ouvert': d['ouvert'], 'peauf': d['peauf'], 'bas': mx}
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); pg = B.ouvre(ctx, F)
    am = pg.evaluate("()=>(window._tenirRegle||{}).AMANDE"); ctx.close(); ER = []
    juge('D · l\'app déclare 2 400 ms pour le vert posé (`_tenirRegle.AMANDE`)', am == 2400, am)
    seul = {}
    for chiche in (False, True):
        nom = 'Chiche' if chiche else 'Promi'
        m = tenir(b, chiche); seul[nom] = m; ER += m['er']
        juge('A · %s sans toucher : le vert commence de remonter 2 250 à 2 700 ms après le lever ; la parole est tenue' % nom,
             m['monte'] is not None and 2250 <= m['monte'] <= 2700 and m['st'] == 'tenu', 'remontée à %s ms · rideau parti à %s ms · statut %s · front au plus bas %s' % (m['monte'] and round(m['monte']), m['repos'] and round(m['repos']), m['st'], m['bas'] and round(m['bas'])))
    m = tenir(b, False, touche=1300); ER += m['er']
    juge('B · un toucher (sur la barre Peaufiner) à 1,3 s : le vert remonte dans les 250 ms, la parole est tenue, la remontée et le rideau parti ≥ 700 ms plus tôt',
         m['monte'] is not None and m['tt'] is not None and 0 <= m['monte'] - m['tt'] <= 250 and m['st'] == 'tenu' and m['repos'] is not None and seul['Promi']['repos'] and seul['Promi']['repos'] - m['repos'] >= 700 and seul['Promi']['monte'] and seul['Promi']['monte'] - m['monte'] >= 700,
         'toucher à %s ms · remontée à %s ms · rideau parti à %s ms (sans toucher : %s)' % (m['tt'] and round(m['tt']), m['monte'] and round(m['monte']), m['repos'] and round(m['repos']), seul['Promi']['repos'] and round(seul['Promi']['repos'])))
    juge('B · le toucher est avalé : Peaufiner ne s\'ouvre pas, la fiche tenue reste ouverte', m['ouvert'] and not m['peauf'], 'fiche ouverte %s · Peaufiner %s' % (m['ouvert'], m['peauf']))
    m = tenir(b, False, touche=100); ER += m['er']
    juge('C · un toucher 100 ms après le lever ne presse rien : la remontée garde son heure (2 250 à 2 700 ms)', m['monte'] is not None and 2250 <= m['monte'] <= 2700, 'toucher à %s ms · remontée à %s ms' % (m['tt'] and round(m['tt']), m['monte'] and round(m['monte'])))
    juge('aucune erreur de page', not ER, ER[:2])
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
