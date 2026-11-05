#!/usr/bin/env python3
"""redteam_cercle_plus.py — ⚑ v179b (Tom, C-230) : « + PLANTER DANS LE CERCLE » : CHOISIR PROMI OU CHICHE.

« Un toucher sur « + Planter dans le Cercle » ouvre un petit menu à DEUX choix : Promi et Chiche, aux codes des encarts du + de l'accueil, sans les
textes de droite. Chaque choix ouvre la page + de cette nature, déjà rattachée au Cercle. Toucher à côté referme le menu. »
Banc WebKit ×3, au doigt, un Cercle de six paroles (banc-etats/etat-cercle.json), clair et sombre :
  A · le bouton touché : le menu paraît, deux encarts (Chiche, Promi), à l'aplat de leur nature, la nature en PromiLate capitales, aucun texte de droite,
      au-dessus du bouton, dans l'appareil ;
  B · toucher à côté : le menu se ferme, rien ne s'ouvre, la fiche reste ;
  C · « Un Promi » : la page + d'un Promi, rattachée au Cercle (`selNuee`) ; une parole plantée par elle est dans le Cercle ;
  D · « Un Chiche » : la page + d'un Chiche, rattachée au Cercle ; la parole plantée est un Chiche, dans le Cercle.
`--capture` : planche-v179b/cercle-menu.png. Rouge sur v178 (`--fichier=zz-v178.html`) : pas de menu, le Promi seul.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
def ouvre_cercle(pg):
    pg.evaluate("()=>{ closeAll(); openNueeDetail('potager'); }"); pg.wait_for_timeout(2600)
def touche_bouton(pg):
    c = pg.evaluate("()=>{ const b=document.getElementById('nfAdd'); if(!b) return null; const r=b.getBoundingClientRect(); return [r.left+r.width*0.7, r.top+r.height/2]; }")
    if c: pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(500)
    return c
MENU = """()=>{ const m=document.getElementById('cpChoix'); if(!m || !m.classList.contains('ouvert')) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, b=document.getElementById('nfAdd').getBoundingClientRect();
  return {pils:[...m.querySelectorAll('.cp-pil')].map(p=>{ const r=p.getBoundingClientRect(), s=getComputedStyle(p), n=p.querySelector('.acc-nat'), ns=n?getComputedStyle(n):null;
    return {k:p.getAttribute('data-k'), txt:p.textContent.trim(), fond:s.backgroundColor, nat:ns?ns.fontFamily:null, maj:ns?ns.textTransform:null, small:!!p.querySelector('small'), x:(r.left-D.left)/k, y:(r.top-D.top)/k, w:r.width/k, h:r.height/k}; }),
    bouton:(b.top-D.top)/k }; }"""
def plante(pg, titre):
    pg.evaluate("t=>{ const i=document.getElementById('fTitle'); i.value=t; i.dispatchEvent(new Event('input',{bubbles:true})); }", titre); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(1800)
    return pg.evaluate("t=>{ const q=promises.find(x=>x.title===t); return q?{nuee:q.nuee||null, chiche:!!q.chiche}:null; }", titre)
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        T = '[%s]' % ('sombre' if sombre else 'clair')
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
        ouvre_cercle(pg); c = touche_bouton(pg); m = pg.evaluate(MENU)
        ok = bool(m) and [x['k'] for x in m['pils']] == ['chiche', 'promi'] and all(x['nat'] and 'PromiLate' in x['nat'] and x['maj'] == 'uppercase' and not x['small'] for x in m['pils'])
        ok = ok and m['pils'][0]['fond'] == 'rgb(255, 184, 210)' and m['pils'][1]['fond'] == 'rgb(130, 174, 248)' and m['pils'][0]['txt'] == 'Un Chiche' and m['pils'][1]['txt'] == 'Un Promi'
        ok = ok and all(x['x'] >= 0 and x['x'] + x['w'] <= 390 and x['y'] >= 0 for x in m['pils']) and m['pils'][1]['y'] + m['pils'][1]['h'] <= m['bouton'] - 4
        juge(T + ' A · le menu : Chiche, Promi, l\'aplat de leur nature, PromiLate capitales, sans texte de droite, au-dessus du bouton', ok, m)
        if '--capture' in sys.argv and not sombre:
            import os; os.makedirs('planche-v179b', exist_ok=True); B.capture(pg, 'planche-v179b/cercle-menu.png')
        pg.touchscreen.tap(60, 300); pg.wait_for_timeout(700)
        st = pg.evaluate("()=>({menu:!!document.querySelector('#cpChoix.ouvert'), fiche:document.getElementById('detailPoster').classList.contains('show'), plus:document.getElementById('createSheet').classList.contains('show'), peauf:document.getElementById('detailPoster').classList.contains('s2-ouv')})")
        juge(T + ' B · toucher à côté : le menu se ferme, rien ne s\'ouvre, la fiche reste', m and not st['menu'] and st['fiche'] and not st['plus'] and not st['peauf'], st)
        for nat in ('promi', 'chiche'):
            ouvre_cercle(pg); touche_bouton(pg)
            r = pg.evaluate("k=>{ const p=document.querySelector('#cpChoix.ouvert .cp-pil[data-k='+k+']'); if(!p) return null; const r=p.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }", nat)
            if r: pg.touchscreen.tap(r[0], r[1])
            pg.wait_for_timeout(2800)
            s = pg.evaluate("()=>{ const c=document.getElementById('createSheet'); return {show:c.classList.contains('show'), cls:c.className, kind:c.getAttribute('data-kind'), sel:(typeof selNuee!=='undefined'?selNuee:null), sens:(window._phrase||{}).sens, phrase:(document.getElementById('csPhrase')||{}).textContent}; }")
            okp = r and s['show'] and s['kind'] == nat and ('pp-' + nat) in s['cls'] and s['sel'] == 'potager' and ((s['sens'] == 'chiche') == (nat == 'chiche'))
            q = plante(pg, 'essai %s %s' % (nat, T)) if okp else None
            L = 'C' if nat == 'promi' else 'D'
            juge(T + ' %s · « Un %s » : sa page +, rattachée au Cercle ; la parole plantée est dans le Cercle' % (L, nat.capitalize()), okp and q and q['nuee'] == 'potager' and q['chiche'] == (nat == 'chiche'), [s and {k: (v[:60] if isinstance(v, str) else v) for k, v in s.items()}, q])
        juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
