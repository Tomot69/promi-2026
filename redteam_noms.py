#!/usr/bin/env python3
"""
redteam_noms.py — LES NOMS, LES VISAGES, LES DATES (v146, Tom, 14 oct. 2026 — C-128, C-116 ; §17 : la ligne « Un mot… » d'un Cercle).
LA DÉCISION, EN DUR :
  · le pseudo en entier s'il tient ; sinon coupé à 6 lettres et suivi d'un « . » ;
  · si deux personnes ou plus partagent le même début, on ajoute TOUJOURS les caractères suivants jusqu'au premier qui les distingue (Christo. / Christi.) ;
  · toucher un nom mène à la fiche de la personne ; le SÉLECTEUR des personnes reste tel quel (les noms entiers) ;
  · la date : « à l'instant », « il y a 5 min », « hier », puis « 12 oct. » ; au-delà d'un an, l'année ;
  · la fiche d'un Cercle : la ligne « Un mot… » juste au-dessus de « + Planter dans le Cercle ».
Le verdict se lit sur l'écran (le texte rendu, le doigt) ; la fonction de l'app n'est appelée que pour les cas d'école (doublons, dates), avec des valeurs en dur.
Preuve (§7) : `--fichier=zz-avant-v146.html` — il rougit (aucune règle, aucun lien, l'ancienne date « aujourd'hui »).
"""
import sys; sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-110s %s' % ('✅' if c else '❌', nom, str(d)[:230]), flush=True)
CAS = [  # (nom, autres présents, place en pt ou None, attendu)
    ('Rachel', ['Marion'], 120, 'Rachel'), ('Bartholomew', ['Rachel'], 40, 'Bartho.'), ('Christophe', ['Christine', 'Rachel'], 40, 'Christo.'), ('Christine', ['Christophe'], 40, 'Christi.'),
    ('Alexandra', ['Alexandre'], 40, 'Alexandra'), ('Maximilien', ['Maxime'], 40, 'Maximi.'), ('Jean-Baptiste', ['Jean-Marc'], 40, 'Jean-B.'), ('Léonard', [], 40, 'Léonar.')]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); toile_pleine(ctx, 10); pg = ouvre(ctx, F)
    ok = pg.evaluate("()=>!!window._noms")
    juge('la règle existe dans l\'app (`window._noms`)', ok)
    if ok:
        for nom, autres, place, att in CAS:
            v = pg.evaluate("([n,a,l])=>window._noms.court(n, {tous:a.concat([n]), largeur:l, police:'700 15px Gilbert'})", [nom, autres, place])
            juge('« %s » (avec %s, %s pt de place) → « %s »' % (nom, ', '.join(autres) or 'personne', place, att), v == att, 'rendu « %s »' % v)
        D = pg.evaluate("""()=>{ const n=new Date('2026-10-14T15:00:00'); const f=(ms)=>window._noms.date(new Date(n.getTime()-ms).toISOString(), n);
          return [f(20e3), f(5*60e3), f(3*3600e3), f(24*3600e3), window._noms.date('2026-10-02T10:00:00', n), window._noms.date('2025-06-02T10:00:00', n)]; }""")
        att = ['à l’instant', 'il y a 5 min', 'il y a 3 h', 'hier', '2 oct.', '2 juin 2025']
        juge('les dates : « à l’instant », « il y a 5 min », « il y a 3 h », « hier », « 2 oct. », et l\'année au-delà d\'un an', D == att, D)
    # sur l'écran : une fiche avec des mots de Christophe et de Christine, un nom long
    pg.evaluate("""()=>{ const q=promises.filter(x=>!x.draft)[0]; window.__q=q.id; q.comments=[]; const now=Date.now();
      q.comments.push({t:'On fait ça ensemble ?', by:'Christophe', d:new Date(now-86400000).toISOString()});   /* v148 : 24 h, toujours « hier » — 36 h ne l'était qu'après midi */ q.comments.push({t:'Avec plaisir', by:'Christine', d:new Date(now-4*60000).toISOString()});
      q.comments.push({t:'Je réserve.', by:'Bartholomew', d:new Date(now-40000).toISOString()}); openDetail(q.id); }""")
    pg.wait_for_timeout(2600); tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(1200)
    E = pg.evaluate("()=>[...document.querySelectorAll('#cm5Fil .cm5-un')].map(u=>{ const n=u.querySelector('.nom-lien'); const c=u.querySelector(':scope > div'); return {nom:n?n.textContent:null, data:n?n.getAttribute('data-nom'):null, tete:c?c.children[0].textContent:''}; })")
    juge('les mots : le nom s\'affiche selon la règle et porte la personne (Christophe, Christine, Bartholomew)', [e['data'] for e in E] == ['Christophe', 'Christine', 'Bartholomew'] and all(e['nom'] for e in E), [(e['nom'], e['data']) for e in E])
    juge('les mots : la date sobre (« hier », « il y a 4 min », « à l’instant »)', len(E) == 3 and 'hier' in E[0]['tete'] and 'il y a 4 min' in E[1]['tete'] and 'instant' in E[2]['tete'], [e['tete'] for e in E])
    c = pg.evaluate("()=>{ const n=[...document.querySelectorAll('#cm5Fil .nom-lien')].find(x=>x.getAttribute('data-nom')==='Christine'); if(!n) return null; const r=n.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }")
    if c: tap(pg, c[0], c[1]); pg.wait_for_timeout(1500)
    ps = pg.evaluate("()=>{ const s=document.getElementById('personSheet'), c=document.getElementById('psCadre'), n=document.getElementById('psName'); return {vu:!!(s&&s.classList.contains('show')), fiche:c?c.getAttribute('data-fiche'):null, nom:n?n.textContent:null}; }")
    juge('toucher un nom (Christine) mène à la fiche de la personne', bool(c) and ps['vu'] and ps['fiche'] == 'Christine', ps)
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(600)
    # le sélecteur des personnes reste tel quel : le nom entier
    pg.evaluate("()=>{ const q=promises.filter(x=>!x.draft)[0]; q.who='Bartholomew'; openDetail(q.id); }"); pg.wait_for_timeout(2400)
    sel = pg.evaluate("()=>[...document.querySelectorAll('#detailPoster .ph-o, #detailPoster .ppo-nom')].map(e=>e.textContent.trim()).filter(Boolean)")
    kr = pg.evaluate("()=>[...document.querySelectorAll('#detailPoster .kr-n')].map(e=>e.textContent.trim())")
    juge('le Noyau de la fiche suit la règle (Bartholomew → « Bartho. ») ; le sélecteur garde le nom entier', any(x == 'Bartho.' for x in kr) and (not sel or any('Bartholomew' in x for x in sel)), 'Noyaux %s · sélecteur %s' % (kr, sel[:4]))
    # PARTOUT où un nom apparaît : la phrase de la fiche (le nom tient : entier, et il se touche), le sur-titre d'une carte d'Index et la ligne du Fil
    # (ils ne tiennent pas : chaque nom coupé selon la règle). Les noms des cartes ne se touchent pas : toute la carte ouvre la fiche (Q512).
    ph = pg.evaluate("()=>{ const n=document.querySelector('#dptQui .nom-lien'); if(!n) return null; const r=n.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return {t:n.textContent, d:n.getAttribute('data-nom'), x:(r.left+r.width/2-D.left)/k, y:(r.top+r.height/2-D.top)/k}; }")
    juge('la phrase de la fiche : « Bartholomew » y tient — le nom est entier, et c\'est un lien', bool(ph) and ph['t'] == 'Bartholomew' and ph['d'] == 'Bartholomew', ph)
    if ph: tap(pg, ph['x'], ph['y']); pg.wait_for_timeout(1500)
    ps = pg.evaluate("()=>{ const s=document.getElementById('personSheet'), c=document.getElementById('psCadre'); return {vu:!!(s&&s.classList.contains('show')), fiche:c?c.getAttribute('data-fiche'):null}; }")
    juge('toucher le nom dans la phrase de la fiche mène à la fiche de la personne', bool(ph) and ps['vu'] and ps['fiche'] == 'Bartholomew', ps)
    pg.evaluate("""()=>{ try{ closeAll(); }catch(e){} const q=promises.filter(x=>!x.draft)[0]; q.who='Bartholomew, Christophe, Maximilien'; try{ queueSave(); }catch(e){}
      feedAdd('chiche','Bartholomew te lance un chiche : « '+q.title+' »',{pid:q.id, from:'Bartholomew'}); }"""); pg.wait_for_timeout(600)
    tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2600)
    ix = pg.evaluate("()=>{ const q=promises.filter(x=>!x.draft)[0]; const c=[...document.querySelectorAll('#indexList .s4-carte')].find(c=>{ const t=c.querySelector('.s4-ti'); return t && t.textContent.trim()===q.title; }); const e=c&&c.querySelector('.s4-eb'); return e?e.textContent.trim():null; }")
    juge('l\'Index : le sur-titre qui ne tient pas coupe chaque nom selon la règle (« Bartho. », « Christo. », « Maximi. »)', bool(ix) and 'Bartho.' in ix and 'Christo.' in ix and 'Maximi.' in ix and 'Bartholomew' not in ix, ix)
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(500); tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600)
    fl = pg.evaluate("()=>[...document.querySelectorAll('.s4-carte .s4-nom')].map(e=>e.textContent.trim()).filter(t=>/Bartho/.test(t))")
    juge('le Fil : la ligne qui ne tient pas coupe le nom (« Bartho. te lance un chiche »)', bool(fl) and all('Bartholomew' not in t for t in fl) and any('Bartho.' in t for t in fl), fl)
    ctx.close()
    # la fiche d'un Cercle (le jeu de démonstration) : « Un mot… » juste au-dessus de « + Planter dans le Cercle »
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); openEssaim('potager'); }"); pg.wait_for_timeout(3600)
    g = pg.evaluate("()=>{ const l=document.getElementById('cm5Ligne'), a=document.getElementById('nfAdd'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=x=>x?[(x.getBoundingClientRect().top-D.top)/k,(x.getBoundingClientRect().bottom-D.top)/k]:null; const h=l?document.elementFromPoint(l.getBoundingClientRect().left+60, l.getBoundingClientRect().top+20):null; return {ligne:r(l), planter:r(a), mot:l?l.textContent.trim():null, doigt:!!(h&&l&&l.contains(h))}; }")
    juge('§17 · la fiche d\'un Cercle : « Un mot… » juste au-dessus de « + Planter dans le Cercle » (4 à 16 pt d\'air), joignable au doigt', bool(g['ligne'] and g['planter']) and 4 <= g['planter'][0] - g['ligne'][1] <= 16 and g['doigt'] and (g['mot'] or '').startswith('Un mot'), g)
    # le nom d'un CERCLE n'est pas un pseudo : il reste entier (« l'atelier du samedi » sortait « l'atel. ») ; un Cercle SANS parole n'a pas la ligne
    # (16 pt seulement entre « encore aucune parole » et « + Planter » : sa cale poussait l'entrée sous le bandeau, 750 → 812)
    pg.evaluate("()=>{ closeAll(); openEssaim('atelier'); }"); pg.wait_for_timeout(3600)
    v = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, a=document.getElementById('nfAdd'), r=a?a.getBoundingClientRect():null; return {kr:[...document.querySelectorAll('#detailPoster .kr-n')].filter(e=>e.getBoundingClientRect().height>0).map(e=>e.textContent.trim()), ligne:!!(document.getElementById('cm5Ligne')&&document.getElementById('cm5Ligne').getBoundingClientRect().height), planter:r?[(r.top-D.top)/k,(r.bottom-D.top)/k]:null, sous:r?(()=>{const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return !!(h&&a.contains(h));})():null}; }")
    juge('le nom d\'un Cercle n\'est pas abrégé (Noyau de sa fiche : « l\'atelier du samedi »)', "l'atelier du samedi" in v['kr'], v['kr'])
    juge('un Cercle sans parole : pas de ligne « Un mot… », « + Planter » reste 12 pt au-dessus du bandeau (686 → 748), au doigt', not v['ligne'] and v['planter'] and abs(v['planter'][1] - 748) <= 1 and v['sous'], v)
    b.close()
print('\n  %s  %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res))); sys.exit(0 if all(res) else 1)
