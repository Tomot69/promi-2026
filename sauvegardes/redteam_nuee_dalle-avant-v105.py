#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_nuee_dalle.py — UNE NUÉE A SA DALLE SUR LA TOILE, ET SON BLOC DU CERCLE (Tom, 13 sept. 2026).

  « Une Nuée a sa propre dalle sur la Toile. […] sa couleur du Cercle colore sa dalle, pas celles de ses Promi. Chaque Promi
    garde la sienne. […] Une Nuée sans dalle est invisible sur la Toile, alors qu'elle porte parfois neuf paroles. Et donne-lui
    son bloc du Cercle, avec la rangée LA COULEUR comme les deux autres natures. »

  1 · CHAQUE NUÉE EST SUR LA TOILE — « le potager » (9 paroles) ET « l'atelier du samedi » (vide) répondent au doigt
  2 · SA DALLE TIENT — après une plantation (sync de l'app), les deux dalles de Nuée sont toujours là
  3 · UN TOUCHER SUR SA DALLE OUVRE SA FICHE — au doigt (CDP), la fiche de CETTE Nuée
  4 · SA COULEUR EST FIGÉE — même couleur après une plantation
  5 · LE BLOC DU CERCLE — Peaufiner d'une Nuée, page 2 : cinq rangées (LA COULEUR en dernier), 384, encart à 147, sous
      « Planter dans la Nuée » ; DISSOUDRE à 104 sous le bloc ; rien ne se superpose
  6 · LA COULEUR COLORE SA DALLE, PAS CELLES DE SES PROMI — code #C0FFEE : la dalle du potager est rgb(192,255,238), les
      neuf dalles de ses Promi n'ont pas bougé
  7 · OUVERTE, DISSOUDRE DESCEND — rien ne se superpose
  8 · À LA PAGE + D'UNE NUÉE — le code choisi va à la dalle de la Nuée créée, jamais à un Promi planté ensuite
  9 · RIEN NE SURVIT — fermer, ouvrir un Promi : aucun bloc de Nuée ne reste
 10 · UN PROMI PLANTÉ DANS UNE NUÉE A SA DALLE RELIÉE (Tom, 14 sept. : « corrige aussi le Promi dans une Nuée sans lien ») —
      au vrai chemin (« Planter dans la Nuée » → page + → #addPromi) : UNE dalle de plus, reliée, couleur figée ; au doigt elle
      ouvre SA fiche ; sa couleur tient après une plantation
 11 · UNE NUÉE NEUVE (#addNuee) — sa dalle au doigt, et son premier Promi a sa dalle reliée

Cotes et codes EN DUR (§7). Preuve : `APP_ND=http://127.0.0.1:8752/sauvegardes/app-avant-lot-nuee-dalle.html` doit ROUGIR.
"""
import os, sys
from importlib.machinery import SourceFileLoader
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_ND', "http://127.0.0.1:8752/app.html")
R = os.path.dirname(os.path.abspath(__file__))
J = SourceFileLoader("j", R + "/releve-S3-page-plus.py").load_module()
ORDRE = ['RÉCURRENCE', 'RAPPEL', "C'EST IMPORTANT ?", 'LA MÉMOIRE', 'LA COULEUR']
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-66s OK  %s' % (nom, detail))
    else: ko.append(nom); print('%-66s KO  %s' % (nom, detail))


HITS = """()=>{const v={}; for(let y=0;y<844;y+=5)for(let x=0;x<390;x+=5){const h=Toile.hit(x,y); if(h&&h.kind==='nuee'&&h.nuee){ v[h.nuee]=v[h.nuee]||[x,y,0]; v[h.nuee][2]++; }} return v;}"""
COUL = "(k)=>Toile.colorOfNuee?Toile.colorOfNuee(k):null"
GEO = """()=>{const k=document.getElementById('device').getBoundingClientRect().width/390; const c=document.getElementById('dpdCorps'); const C=c.getBoundingClientRect();
  const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return {y:(r.top-C.top)/k+c.scrollTop, h:r.height/k, b:(r.bottom-C.top)/k+c.scrollTop, vis:getComputedStyle(e).display!=='none'&&r.height>0}; };
  const bloc=document.querySelector('#dpdCorps .s2-cercle'); const enc=bloc&&bloc.querySelector('.s2-encart');
  return {bloc:R(bloc), mots: bloc?[...bloc.querySelectorAll(':scope > .s2-reg')].map(r=>(r.querySelector('.s2-lab')||{}).textContent):[],
          enc: enc&&getComputedStyle(enc).display!=='none'?R(enc):null, plant:R(document.getElementById('nfAdd')), diss:R(document.getElementById('npDiss')),
          ouv:R(bloc&&bloc.querySelector('.s2-couleur.s2-ouv'))};}"""

TROUVE_PID = """(i)=>{const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
  for(let y=0;y<844;y+=4)for(let x=0;x<390;x+=4){const h=Toile.hit(x,y); if(h&&h.pid===i){ const X=r.left+x*k,Y=r.top+y*k; const e=document.elementFromPoint(X,Y); if(e&&e.id==='toileCv') return [X,Y]; }} return null;}"""
NUEE_NEUVE = """()=>{ closeAll(); const n=document.getElementById('nName'), f=document.getElementById('nFirst'), b=document.getElementById('addNuee');
  if(!n||!f||!b) return 'champs absents'; n.value='la Nuée neuve du juge'; f.value='premier de la neuve'; b.click(); return 'ok'; }"""
NUEE_NEUVE_LIT = """()=>{ const k=Object.keys(NUE).find(x=>NUE[x]==='la Nuée neuve du juge'); const q=promises.find(x=>x.title==='premier de la neuve');
  const v={}; for(let y=0;y<844;y+=4)for(let x=0;x<390;x+=4){const h=Toile.hit(x,y); if(h&&h.kind==='nuee'&&h.nuee===k) v.n=(v.n||0)+1;}
  return {k:k||null, q:!!q, abs:q?!!Toile.dalleAbs(q.id):false, nuee:v.n||0}; }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ['dark', 'light']:
        T = 'sombre' if th == 'dark' else 'clair'
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)))
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme(t);setPremium(false);}", th)
        pg.wait_for_timeout(1200)
        cdp = ctx.new_cdp_session(pg)
        h1 = pg.evaluate(HITS)
        t('[%s] 1 · « le potager » et « l\'atelier » répondent au doigt sur la Toile' % T, 'potager' in h1 and 'atelier' in h1, str({k: v[2] for k, v in h1.items()}))
        c_av = pg.evaluate(COUL, 'potager')
        # 2 · une plantation (le chemin de l'app : sync des ids réels)
        pg.evaluate("()=>{const q=P('juge nuée dalle','moi',5,2,'encours',null); promises.push(q); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id));}")
        pg.wait_for_timeout(1500)
        h2 = pg.evaluate(HITS)
        t('[%s] 2 · après une plantation, les deux dalles de Nuée sont là' % T, 'potager' in h2 and 'atelier' in h2, str({k: v[2] for k, v in h2.items()}))
        c_ap = pg.evaluate(COUL, 'potager')
        t('[%s] 4 · la couleur de la dalle du potager est figée' % T, c_av is not None and c_av == c_ap, '%s → %s' % (c_av, c_ap))
        # 3 · au doigt
        pt = None
        if 'potager' in h2:
            pt = pg.evaluate("""(a)=>{const cv=document.getElementById('toileCv');const r=cv.getBoundingClientRect();const k=r.width/cv.clientWidth;
              for(let y=0;y<844;y+=5)for(let x=0;x<390;x+=5){const h=Toile.hit(x,y); if(h&&h.nuee==='potager'){ const X=r.left+x*k,Y=r.top+y*k; const e=document.elementFromPoint(X,Y); if(e&&e.id==='toileCv') return [X,Y]; }} return null;}""", None)
        if pt:
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pt[0], 'y': pt[1]}]})
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            pg.wait_for_timeout(1800)
        f = pg.evaluate("()=>{const d=document.getElementById('detailPoster');return {show:d.classList.contains('show'), nuee:(d.classList.contains('dp-nuee')||d.classList.contains('dp-mode-nuee')), cle:(typeof curNuee!=='undefined'?curNuee:null)};}")
        t('[%s] 3 · au doigt, sa dalle ouvre la fiche du potager' % T, bool(pt) and f['show'] and f['nuee'] and f['cle'] == 'potager', '%s · %s' % (pt, f))
        # 5 · le bloc du Cercle
        pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=760;}"); pg.wait_for_timeout(600)
        g = pg.evaluate(GEO)
        bl = g['bloc']
        t('[%s] 5 · Peaufiner d\'une Nuée : cinq réglages, LA COULEUR en dernier' % T, g['mots'] == ORDRE, str(g['mots']))
        t('[%s] 5 · bloc 384 en page 2, encart à 147' % T, bool(bl) and bl['vis'] and abs(bl['h'] - 384) < 1 and 760 < bl['y'] < 1520 and g['enc'] and abs(g['enc']['y'] - bl['y'] - 147) < 1,
          bl and 'y %.0f h %.0f encart %s' % (bl['y'], bl['h'], g['enc'] and round(g['enc']['y'] - bl['y'])))
        t('[%s] 5 · sous « Planter », DISSOUDRE à 104 sous le bloc, rien ne se superpose' % T,
          bool(bl) and g['plant'] and g['diss'] and g['plant']['b'] <= bl['y'] - 0.5 and abs(g['diss']['y'] - bl['b'] - 104) < 1,
          bl and 'planter bas %.0f · bloc %.0f–%.0f · dissoudre %.0f' % (g['plant']['b'] if g['plant'] else -1, bl['y'], bl['b'], g['diss']['y'] if g['diss'] else -1))
        # 6 · payé : la couleur
        membres = pg.evaluate("()=>promises.filter(q=>q.nuee==='potager'&&!q.draft).map(q=>q.id)")
        avant = pg.evaluate("(ids)=>ids.map(i=>Toile.colorOf(i))", membres)
        pg.evaluate("()=>{setPremium(true); if(window._cerclePaye) _cerclePaye(); if(window._nueePeaufiner) _nueePeaufiner();}"); pg.wait_for_timeout(800)
        try:
            pg.evaluate("()=>{const r=document.querySelector('#dpdCorps .s2-couleur'); if(r) r.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(400)
            pg.locator('#dpdCorps .s2-couleur .s2-lab').click(timeout=3000); pg.wait_for_timeout(700)
            pg.locator('#dpdCorps .s2-couleur .cc-code').fill('#C0FFEE', timeout=3000)
        except Exception:
            pass
        pg.wait_for_timeout(1300)
        cn = pg.evaluate(COUL, 'potager')
        apres = pg.evaluate("(ids)=>ids.map(i=>Toile.colorOf(i))", membres)
        t('[%s] 6 · code #C0FFEE : la dalle du potager est rgb(192,255,238)' % T, cn == 'rgb(192,255,238)', str(cn))
        t('[%s] 6 · les dalles de ses %d Promi n\'ont pas bougé' % (T, len(membres)), len(membres) == 9 and avant == apres, '%d changées' % sum(1 for a, c in zip(avant, apres) if a != c))
        g2 = pg.evaluate(GEO); b2 = g2['bloc']
        t('[%s] 7 · LA COULEUR ouverte : DISSOUDRE descend, rien ne se superpose' % T,
          bool(b2) and g2['ouv'] and g2['diss'] and g2['ouv']['b'] <= b2['b'] + 0.5 and g2['diss']['y'] >= b2['b'] + 103,
          b2 and 'ouverte bas %s · bloc bas %.0f · dissoudre %s' % (g2['ouv'] and round(g2['ouv']['b']), b2['b'], g2['diss'] and round(g2['diss']['y'])))
        # 9 · rien ne survit
        pg.evaluate("()=>{closeAll(); openDetail(promises.filter(q=>!q.draft&&!q.req&&!q.nuee)[0].id);}"); pg.wait_for_timeout(1400)
        t('[%s] 9 · fermée, aucun bloc de Nuée ne reste sur une fiche de Promi' % T, pg.evaluate("()=>!document.getElementById('npCercle')"), '')
        # 8 · page + d'une Nuée
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(500)
        pg.evaluate(J.SCENE, 'pp_nuee'); pg.wait_for_timeout(1400)
        kind = pg.evaluate("()=>document.getElementById('createSheet').getAttribute('data-kind')")
        pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1600)
        try:
            pg.evaluate("()=>{const r=document.querySelector('#createSheet .s2-couleur'); if(r) r.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(300)
            pg.locator('#createSheet .s2-couleur .s2-lab').click(timeout=3000); pg.wait_for_timeout(400)
            pg.locator('#createSheet .s2-couleur .cc-code').fill('#7F3B12', timeout=3000)
        except Exception:
            pass
        pg.wait_for_timeout(500)
        r8 = pg.evaluate("""()=>{closeAll(); const q=P('juge après nuée','moi',5,2,'encours',null); promises.push(q); Toile.addPromi(q.id);
          NUE.njuge='la Nuée du juge'; const q2=P('premier du juge','le groupe',5,2,'encours','njuge','moi'); promises.push(q2);
          Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id)); return q.id;}""")
        pg.wait_for_timeout(1500)
        c8 = pg.evaluate(COUL, 'njuge'); cp = pg.evaluate("(i)=>Toile.colorOf(i)", r8)
        t('[%s] 8 · page + d\'une Nuée : le code va à la dalle de la Nuée créée' % T, kind == 'nuee' and c8 == 'rgb(127,59,18)', '%s · %s' % (kind, c8))
        t('[%s] 8 · … et jamais au Promi planté entre-temps' % T, cp != 'rgb(127,59,18)', str(cp))
        # 10 · un Promi planté dans une Nuée existante, au vrai chemin
        pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const b=document.getElementById('nfAdd'); if(b) b.click();}"); pg.wait_for_timeout(1500)
        n0 = pg.evaluate("()=>Toile.count()")
        pg.evaluate("()=>{const f=document.getElementById('fTitle'); if(f){ f.value='juge membre'; f.dispatchEvent(new Event('input',{bubbles:true})); } document.getElementById('addPromi').click();}")
        pg.wait_for_timeout(3500)
        m = pg.evaluate("()=>{const q=promises.find(x=>x.title==='juge membre'); return q?{id:q.id, nuee:q.nuee, abs:!!Toile.dalleAbs(q.id), c:Toile.colorOf(q.id), n:Toile.count(), fig:!!q.dalle}:null;}")
        t('[%s] 10 · planté dans le potager : une dalle de plus, reliée, couleur figée' % T, bool(m) and m['nuee'] == 'potager' and m['abs'] and bool(m['c']) and m['fig'] and m['n'] == n0 + 1, '%s · avant %s' % (m, n0))
        h10 = pg.evaluate(HITS)
        t('[%s] 10 · le potager garde sa dalle, toujours au doigt' % T, 'potager' in h10, str({k: v[2] for k, v in h10.items()}))
        pm = None
        if m:
            pm = pg.evaluate(TROUVE_PID, m['id'])
        if pm:
            pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pm[0], 'y': pm[1]}]})
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
            pg.wait_for_timeout(1600)
        o10 = pg.evaluate("(i)=>{const d=document.getElementById('detailPoster'); return d.classList.contains('show') && typeof cur!=='undefined' && !!cur && cur.id===i;}", m['id'] if m else -1)
        t('[%s] 10 · au doigt, sa dalle ouvre SA fiche' % T, bool(pm) and o10, '%s · %s' % (pm, o10))
        c10 = m and m['c']
        pg.evaluate("()=>{closeAll(); const q=P('juge après membre','moi',5,2,'encours',null); promises.push(q); Toile.sync(promises.filter(p=>!p.draft).map(p=>p.id));}"); pg.wait_for_timeout(1500)
        c10b = pg.evaluate("(i)=>Toile.colorOf(i)", m['id'] if m else -1)
        t('[%s] 10 · sa couleur tient après une plantation' % T, bool(c10) and c10 == c10b, '%s → %s' % (c10, c10b))
        # 11 · une Nuée neuve
        ok11 = pg.evaluate(NUEE_NEUVE)
        pg.wait_for_timeout(3500)
        r11 = pg.evaluate(NUEE_NEUVE_LIT)
        t('[%s] 11 · Nuée neuve : sa dalle au doigt, et son premier Promi relié' % T, ok11 == 'ok' and bool(r11['k']) and r11['q'] and r11['abs'] and r11['nuee'] > 0, '%s · %s' % (ok11, r11))
        t('[%s] aucune erreur JS' % T, not er, str(er[:2]))
        ctx.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
