#!/usr/bin/env python3
"""redteam_garder_reprise.py — ⚑ v162 (Tom, C-149, RÉCIDIVE) : « GARDER DE CÔTÉ » NE GARDE RIEN.

« Le toucher enregistre le brouillon, referme la page +, et le brouillon se retrouve dans ce que j'ai gardé de côté ; rouvrir un brouillon rouvre la page +
exactement dans l'état gardé. Juge : garder, fermer l'app, rouvrir, retrouver, rouvrir le brouillon ; pour les 3 natures, avec et sans personnes. »
Banc comme Tom (WebKit, ×3, doigt). Pour chaque cas : la page + ouverte au doigt (le + puis la nature) ; la parole écrite au doigt (Promi, Chiche : la
pastille du titre ; Cercle : son nom) ; les personnes posées dans l'état de la page comme le fait le choix des personnes ; « garder de côté » touché au doigt.
  A · la page + se referme, un brouillon de cette nature existe, enregistré ;
  B · l'app fermée et rouverte (rechargement) : il est toujours là, et l'Index le montre (« GARDÉ DE CÔTÉ ») ;
  C · touché dans l'Index : la page + se rouvre dans SA nature, la phrase porte le titre (ou le nom du Cercle), les personnes sont les mêmes ;
  D · « une personne ajoutée, sans titre » (Promi) : gardé aussi (c'est ce que l'ancien bouton perdait).
Preuve : `--fichier=zz-v161.html` rougit.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
CAS = [('promi', 'ranger la cave', []), ('promi', 'ranger la cave', ['Marion', 'Rachel']), ('chiche', 'sauter en parachute', []),
       ('chiche', 'sauter en parachute', ['Marion']), ('nuee', 'Les jardiniers', []), ('nuee', 'Les jardiniers', ['Marion', 'Rachel']), ('promi', '', ['Marion'])]
BROUILLONS = "()=>promises.filter(p=>p.draft).map(p=>({t:p.title, w:p.who, nat:(p.brouillon&&p.brouillon.nat)||(p.dk==='nuee'?'nuee':(p.chiche?'chiche':'promi')), who:(p.brouillon&&p.brouillon.who)||null}))"
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat, titre, gens in CAS:
        T = '%s · %s · %s' % (nat, titre or 'sans titre', ('avec ' + ', '.join(gens)) if gens else 'sans personne')
        ctx = B.contexte(b); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, F)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
        if titre:
            if nat == 'nuee':
                B.tap_sel(pg, '#nueePhrase .ph-m[data-np="nom"]'); pg.wait_for_timeout(600); pg.keyboard.type(titre, delay=25); pg.keyboard.press('Enter')
            else:
                B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(600); pg.keyboard.type(titre, delay=25); pg.keyboard.press('Enter')
            pg.wait_for_timeout(900)
        if gens:
            if nat == 'nuee': pg.evaluate("g=>{ window.newNueeMembers=g.slice(); if(window._nueePhraseRendu) _nueePhraseRendu(); }", gens)
            else: pg.evaluate("g=>{ window.newWhoSel=g.slice(); window._phrase.qui=g.join(', '); if(window._phraseRendu) _phraseRendu(); if(window._ppTout) _ppTout(); }", gens)
            pg.wait_for_timeout(700)
        pg.evaluate("()=>{ const cs=document.getElementById('createSheet'), g=cs.querySelector('.pp-garder'); if(g && window._garderEtat) _garderEtat(cs, g); }"); pg.wait_for_timeout(300)
        B.tap_sel(pg, '#createSheet .pp-garder'); pg.wait_for_timeout(1500)
        ouverte = pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')"); L = pg.evaluate(BROUILLONS)
        mien = [x for x in L if x['nat'] == nat and (not titre or x['t'] == titre)]
        juge('[%s] A · la page + se referme, un brouillon de cette nature est gardé' % T, not ouverte and len(mien) == 1, 'page ouverte %s · brouillons %s' % (ouverte, L))
        pg.reload(); pg.wait_for_timeout(6500); L2 = pg.evaluate(BROUILLONS)
        B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2500)
        lab = titre or '(sans titre)'
        carte = pg.evaluate("t=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const c=[...document.querySelectorAll('#indexList .s4-carte')].find(c=>(c.innerText||'').indexOf(t)>=0 && /gard/i.test(c.innerText||'')); if(!c) return null; c.scrollIntoView({block:'center'}); const r=c.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }", lab)
        juge('[%s] B · l\'app rouverte : le brouillon est toujours là, et l\'Index le montre (« gardé de côté »)' % T, len([x for x in L2 if x['nat'] == nat]) == len(mien) and carte is not None, 'après rechargement %s · carte %s' % (L2, carte))
        if carte:
            pg.wait_for_timeout(500)
            carte = pg.evaluate("t=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const c=[...document.querySelectorAll('#indexList .s4-carte')].find(c=>(c.innerText||'').indexOf(t)>=0 && /gard/i.test(c.innerText||'')); const r=c.getBoundingClientRect(); return [(r.left-D.left)/k+r.width/k/2, (r.top-D.top)/k+r.height/k/2]; }", lab)
            B.tap(pg, carte[0], carte[1]); pg.wait_for_timeout(3500)
            r = pg.evaluate("()=>{ const cs=document.getElementById('createSheet'); const ph=document.getElementById(cs.getAttribute('data-kind')==='nuee'?'nueePhrase':'csPhrase'); return {ouverte:cs.classList.contains('show'), nat:cs.getAttribute('data-kind'), texte:ph?ph.innerText.replace(/\\s+/g,' '):'', who:window.newWhoSel||[], membres:window.newNueeMembers||[], nom:(document.getElementById('nName')||{}).value||'', titre:(window._phrase||{}).titre||''}; }")
            ok = r['ouverte'] and r['nat'] == nat and ((titre.replace(' ', '') in r['texte'].replace(' ', '')) if titre else True) and ((r['membres'] if nat == 'nuee' else r['who']) == gens)
            juge('[%s] C · rouvert depuis l\'Index : la page + dans sa nature, la phrase porte la parole, les mêmes personnes' % T, ok, r)
        er = [x for x in pg.erreurs if 'version.json' not in x]
        if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
