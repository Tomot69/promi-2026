# -*- coding: utf-8 -*-
"""⚑ v188 (Tom, Q608 tranchée autrement ; C-257 suite) — LES COMMENTAIRES DE LA FICHE ET LEUR NOMBRE.
Banc WebKit (banc_tom), Toile du Cercle (etat-cercle), fiches Promi, Chiche, Cercle, échelles 1 et 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79) :
  A · 0, 1, 3, 12 mots, et un titre de 280 caractères : plus aucune ligne « + X commentaires » ; TOUS les mots, le plus récent d'abord ; Promi et Chiche : l'ordre est
      l'état, « Un mot… » (8 pt au moins sous l'état), puis la liste (sous « Un mot… ») ; aucun chevauchement (état, ligne, chaque mot) ;
  B · Promi et Chiche, titre ordinaire : « Un mot… » entière au-dessus de la barre (760) avec 8 pt de marge au moins, au repos ; titre de 280 : atteinte en défilant ;
  C · stable : dix ouvertures de la même fiche, les mêmes mots aux mêmes cotes (± 0,5 pt) ;
  D · le nombre : 0 mot → rien ; 3 vus → « 3 » à l'encre de la ligne ; 3 dont 1 nouveau → « +1 » en #FB4C0D ; 12 dont 4 nouveaux → « +4 » en #FB4C0D ; le toucher fait
      glisser la fiche jusqu'au premier nouveau ; tous vus (passés à l'écran), la fiche refermée puis rouverte → « 12 » à l'encre ;
  E · le dépliage de v183 n'existe plus (ni `_commDeplie`, ni `.cm5-plus`) ; aucune erreur de page."""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True); return ok
NOMS = ['Marion', 'Rachel', 'Nico', 'Adrien', 'Lou']
def com(n, neufs=0):   # les mots, du plus ancien au plus récent ; les `neufs` plus récents sont nouveaux (d'un autre, pas vus)
    return [{'t': 'Mot numéro %d, à propos de ce qu\'on prévoit' % (i + 1), 'by': NOMS[i % 5], 'd': '2026-11-%02dT%02d:00:00Z' % (1 + i // 4, 8 + i % 4 * 3), 'vu': i < n - neufs} for i in range(n)]
LIT = r"""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, dp=document.getElementById('detailPoster');
  const R=e=>{ if(!e) return null; const c=getComputedStyle(e), r=e.getBoundingClientRect(); if(c.display==='none'||c.visibility==='hidden'||r.height<1) return null; return {y:(r.top-D.top)/k+dp.scrollTop, b:(r.bottom-D.top)/k+dp.scrollTop, x:(r.left-D.left)/k, r:(r.right-D.left)/k}; };
  const uns=[...document.querySelectorAll('#cm5Liste .cm5-un')]; const nb=document.querySelector('#cm5Ligne .cm5-nb');
  return {etat:R(document.getElementById('dptQuand')), ligne:R(document.getElementById('cm5Ligne')), uns:uns.map(u=>Object.assign(R(u)||{}, {t:(u.querySelector('.cm5-t')||{}).textContent||''})),
    plus:document.querySelectorAll('.cm5-plus,.cm5-reste').length, nb:nb&&getComputedStyle(nb).display!=='none'?[nb.textContent, getComputedStyle(nb).webkitTextFillColor||getComputedStyle(nb).color, getComputedStyle(document.getElementById('cm5Ligne')).color]:null,
    cercle:dp.classList.contains('dp-mode-nuee'), sc:dp.scrollTop, dep:typeof window._commDeplie }; }"""
def croise(a, b): return a and b and a.get('y') is not None and b.get('y') is not None and a['y'] < b['b'] - 0.5 and b['y'] < a['b'] - 0.5 and a['x'] < b['r'] - 0.5 and b['x'] < a['r'] - 0.5
def ferme(pg): pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie() }catch(e){} try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(1000)
def ouvre(pg, nat, C, titre=None):
    ferme(pg)
    if nat == 'cercle':
        pg.evaluate("c=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; c.forEach(x=>o.comments.push(x)); _cercleMots.garde(); openEssaim('potager'); }", C)
    else:
        t = {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}[nat]
        pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]||x.__t===a[0]); p.__t=a[0]; p.comments=a[1]; if(a[2]) p.title=a[2]; else p.title=a[0]; try{queueSave()}catch(e){} openDetail(p.id); }", [t, C, titre])
    pg.wait_for_timeout(2000)
    POSE = "()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, f=id=>{ const e=document.getElementById(id); return e?Math.round((e.getBoundingClientRect().top-D.top)/k*2)/2:null; }; const u=[...document.querySelectorAll('#cm5Liste .cm5-un')].map(x=>Math.round(x.getBoundingClientRect().top)); return JSON.stringify([f('dptQuand'), f('cm5Ligne'), f('cm5Liste'), u.slice(0,3), document.getElementById('detailPoster').scrollHeight]); }"
    a = pg.evaluate(POSE)   # la fiche POSÉE : deux relevés identiques à 600 ms d'écart (une pose tardive la change encore ≈ 1 s après l'ouverture)
    for _ in range(10):
        pg.wait_for_timeout(600); b2 = pg.evaluate(POSE)
        if b2 == a: break
        a = b2
def rgb(s): import re; m = re.findall(r'[\d.]+', s or ''); return tuple(int(float(x)) for x in m[:3])
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ var v=promises.find(x=>x.title==='réparer le vélo'); v.chiche=true; v.chicheEtat='lance'; v.phraseSens='chiche'; }")
    long280 = ('ranger enfin le garage avec toute la famille, trier les cartons de papa, donner les vélos trop petits, repeindre les étagères, ' * 3)[:280]
    for nat in ('promi', 'chiche', 'cercle'):
        for n in (0, 1, 3, 12):
            C = com(n); ouvre(pg, nat, C); e = pg.evaluate(LIT); att = [c['t'] for c in reversed(C)]
            T = '[%s · %d mot%s]' % (nat, n, 's' if n > 1 else '')
            txt = [u['t'] for u in e['uns']]
            ordre = e['cercle'] or not e['uns'] or (e['ligne'] and e['uns'][0]['y'] >= e['ligne']['b'] - 0.5)
            air = e['cercle'] or not e['etat'] or not e['ligne'] or e['ligne']['y'] - e['etat']['b'] >= 7.5
            boites = [x for x in [e['etat'], e['ligne']] + e['uns'] if x]
            cr = [(i, j) for i in range(len(boites)) for j in range(i + 1, len(boites)) if croise(boites[i], boites[j])]
            juge(T + ' A · tous les mots, le plus récent d\'abord, aucun « + X », l\'ordre état · « Un mot… » · liste, 8 pt sous l\'état, aucun chevauchement',
                 txt == att and e['plus'] == 0 and ordre and air and not cr, (len(txt), e['plus'], ordre, air, cr[:2], e['ligne'] and round(e['ligne']['y'], 1), e['etat'] and round(e['etat']['b'], 1)))
            if nat != 'cercle':
                juge(T + ' B · « Un mot… » entière au-dessus de la barre, 8 pt de marge au moins (au repos)', e['ligne'] and e['ligne']['b'] <= 752.5 and e['sc'] == 0, (e['ligne'] and round(e['ligne']['b'], 1), e['sc']))
                coupe = [round(u['y'], 1) for u in e['uns'] if u.get('y') is not None and u['y'] < 760 - 0.5 and u['b'] > 760 + 0.5]
                juge(T + ' B · aucun mot coupé par la barre au repos (entier au-dessus, ou sous elle)', not coupe, coupe)
            if n == 3:
                P = [];
                for i in range(10):
                    ouvre(pg, nat, C); x = pg.evaluate(LIT); P.append([(round(u.get('y', -1), 1), u['t'][:10]) for u in x['uns']] + [round((x['ligne'] or {}).get('y', -1), 1)])
                juge(T + ' C · dix ouvertures : les mêmes mots aux mêmes cotes', all(len(q) == len(P[0]) and all((a == b2) or (isinstance(a, float) and abs(a - b2) <= 0.5) or (isinstance(a, tuple) and a[1] == b2[1] and abs(a[0] - b2[0]) <= 0.5) for a, b2 in zip(q, P[0])) for q in P), P[0][:2])
        if nat != 'cercle':
            ouvre(pg, nat, com(3), long280); e = pg.evaluate(LIT)
            pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.scrollTop=d.scrollHeight; }"); pg.wait_for_timeout(1500)
            v = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=document.getElementById('cm5Ligne').getBoundingClientRect(); return [(r.top-D.top)/k, (r.bottom-D.top)/k]; }")
            boites = [x for x in [e['etat'], e['ligne']] + e['uns'] if x]
            cr = [(i, j) for i in range(len(boites)) for j in range(i + 1, len(boites)) if croise(boites[i], boites[j])]
            juge('[%s · titre de 280] B · « Un mot… » atteinte en défilant, au-dessus de la barre ; aucun chevauchement' % nat, v[1] <= 760.5 and v[0] >= 100 and not cr, ([round(z, 1) for z in v], cr[:2]))
            pg.evaluate("t=>{ var p=promises.find(x=>x.__t===t); p.title=t; }", {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}[nat])
    # B2 · tous les états de fiche, sans mot et avec un mot, titre ordinaire
    CAS = [('promi en cours', {'status': 'encours'}), ('promi tenue', {'status': 'tenu'}), ('promi reçue', {'status': 'encours', 'from': 'Marion', 'who': 'moi'}),
           ('chiche lancé', {'chiche': True, 'chicheEtat': 'lance', 'status': 'encours', 'phraseSens': 'chiche'}), ('chiche tenu', {'chiche': True, 'status': 'tenu', 'phraseSens': 'chiche'}),
           ('chiche tenu à deux', {'chiche': True, 'status': 'tenu', 'avec': 'Rachel', 'phraseSens': 'chiche'}), ('chiche reçu', {'chiche': True, 'status': 'encours', 'from': 'Marion', 'who': 'moi', 'phraseSens': 'chiche'})]
    for nom, o in CAS:
        for n in (0, 1):
            pg.evaluate("a=>{ var p=promises.find(x=>x.__t==='faire les crêpes'||x.title==='faire les crêpes'); ['chiche','chicheEtat','from','avec','phraseSens'].forEach(k=>delete p[k]); p.who='Nico'; Object.assign(p,a); }", o)
            ouvre(pg, 'promi', com(n)); e = pg.evaluate(LIT)
            juge('[%s · %d mot] B · « Un mot… » entière au-dessus de la barre (8 pt de marge), 8 pt sous l\'état' % (nom, n), e['ligne'] and e['ligne']['b'] <= 752.5 and e['etat'] and e['ligne']['y'] - e['etat']['b'] >= 7.5, (e['etat'] and round(e['etat']['b'], 1), e['ligne'] and round(e['ligne']['b'], 1)))
    pg.evaluate("()=>{ var p=promises.find(x=>x.__t==='faire les crêpes'||x.title==='faire les crêpes'); ['chiche','chicheEtat','from','avec','phraseSens'].forEach(k=>delete p[k]); p.status='encours'; p.who='Nico'; }")
    # D · le nombre
    for nat in ('promi', 'cercle'):
        for n, neufs, txt, orange in ((0, 0, None, False), (3, 0, '3', False), (3, 1, '+1', True), (12, 4, '+4', True)):
            C = com(n, neufs); ouvre(pg, nat, C); e = pg.evaluate(LIT)
            T = '[%s · %d mots dont %d nouveaux]' % (nat, n, neufs)
            if txt is None: juge(T + ' D · aucun nombre', e['nb'] is None, e['nb']); continue
            ok = e['nb'] and e['nb'][0] == txt and ((rgb(e['nb'][1]) == (251, 76, 13)) if orange else (rgb(e['nb'][1]) == rgb(e['nb'][2])))
            juge(T + ' D · « %s »%s' % (txt, ' en #FB4C0D' if orange else ' à l\'encre de la ligne'), ok, e['nb'])
            if neufs:
                pg.evaluate("()=>{ const nb=document.querySelector('#cm5Ligne .cm5-nb'); nb.click(); }"); pg.wait_for_timeout(1800)
                g = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, u=document.querySelector('#cm5Liste .cm5-un[data-neuf]'); const r=u.getBoundingClientRect(); return [(r.top-D.top)/k, (u.querySelector('.cm5-t')||{}).textContent]; }")
                juge(T + ' D · le toucher fait glisser la fiche jusqu\'au premier nouveau (sous l\'en-tête, à l\'écran)', 110 <= g[0] <= 700, [round(g[0], 1), g[1][:20]])
                pg.evaluate("()=>new Promise(async r=>{ const d=document.getElementById('detailPoster'); for(let y=0;y<=d.scrollHeight;y+=200){ d.scrollTop=y; await new Promise(q=>setTimeout(q,120)); } r(); })"); pg.wait_for_timeout(500)
                ferme(pg)
                if nat == 'cercle': pg.evaluate("()=>openEssaim('potager')")
                else: pg.evaluate("()=>openDetail(promises.find(x=>x.__t==='faire les crêpes'||x.title==='faire les crêpes').id)")
                pg.wait_for_timeout(2600); e = pg.evaluate(LIT)
                juge(T + ' D · tous lus (passés à l\'écran), refermée puis rouverte : « %d » à l\'encre de la ligne' % n, e['nb'] and e['nb'][0] == str(n) and rgb(e['nb'][1]) == rgb(e['nb'][2]), e['nb'])
    juge('E · plus de dépliage (ni `_commDeplie`, ni « + X ») ; aucune erreur de page', pg.evaluate("()=>typeof window._commDeplie") == 'undefined' and not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
