#!/usr/bin/env python3
"""redteam_tri_menus.py — ⚑ v163b (Tom, C-191 ; AUDIT-BOUTONS 14, 15, point 3) : LES MENUS ⇅ FONT CE QU'ILS AFFICHENT.

« Fil : TRIER et NE MONTRER QUE agissent sur les cartes d'aujourd'hui, retire les pastilles cachées #fdSort après la fusion. Index : retire QUADRILLAGE (le
pincement reste). « Manquées » devient « À tenir » partout. Le repère « • » de l'option choisie est remplacé par un signe qui n'est pas un point. »
Banc comme Tom (WebKit ×3, doigt), Toile de 10 paroles (dont une à tenir et une dans un Cercle) ; chaque option touchée au doigt :
  A · Fil, NE MONTRER QUE « À tenir » : seules les cartes à tenir ; « Cercles » : seules celles d'un Cercle ; « Tout » : toutes de nouveau ;
  B · Fil, TRIER « Par personne » : les cartes rangées par personne (l'ordre lu sur les cartes est trié) ; « Récents » : l'ordre d'origine ;
  C · #fdSort n'existe plus ; l'Index n'a plus de QUADRILLAGE ; « Manquées » n'est écrit nulle part, « À tenir » est dans les deux menus ;
  D · le repère de l'option choisie : aucun « • », une barrette pleine (largeur > 2 × hauteur), seulement sur l'option choisie.
Preuve : `--fichier=zz-v162.html` rougit.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
CARTES = "()=>[...document.querySelectorAll('#feedView .s4-carte')].map(c=>{ const p=promises.find(q=>q.id===+c.getAttribute('data-pid')); const et=((c.querySelector('.s4-et')||{}).textContent||'').toUpperCase(); return {pid:+c.getAttribute('data-pid')||null, etat:/À TENIR/.test(et)?'atenir':(/TENU/.test(et)?'tenue':(c.getAttribute('data-nuee')?'nuee':'autre')), et:et, nuee:!!(c.getAttribute('data-nuee')||(p&&p.nuee)), who:(p&&p.who)||'', eb:(c.querySelector('.s4-eb')||{}).textContent||''}; })"
def option(pg, menu, btn, attr, val):
    B.tap_sel(pg, btn); pg.wait_for_timeout(700)
    c = pg.evaluate("a=>{ const e=document.querySelector(a[0]+' .ix-mi['+a[1]+'=\"'+a[2]+'\"]'); if(!e) return null; e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", [menu, attr, val])
    pg.wait_for_timeout(400)   # le panneau défile encore : la position se relit après
    c = pg.evaluate("a=>{ const e=document.querySelector(a[0]+' .ix-mi['+a[1]+'=\"'+a[2]+'\"]'); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", [menu, attr, val])
    if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(1400)
    return c is not None
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ const L=promises.filter(q=>!q.draft && !q.nuee && q.status!=='tenu'); const p=L[0]; p.status='rate'; p.due=-1; if(typeof feedAdd==='function') feedAdd('added','Ton Promi « '+p.title+' » est à tenir',{pid:p.id}); saveState&&saveState(); syncAll&&syncAll(); }")
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600)
    tous = pg.evaluate(CARTES)
    option(pg, '#fdMenu', '#fdTriBtn', 'data-fdfilt', 'atenir'); at = pg.evaluate(CARTES)
    juge('A · Fil, « À tenir » : seules les cartes à tenir', at and all(c['etat'] == 'atenir' for c in at) and len(at) < len(tous), 'avant %d · après %s' % (len(tous), [c['etat'] for c in at]))
    option(pg, '#fdMenu', '#fdTriBtn', 'data-fdfilt', 'nuees'); nu = pg.evaluate(CARTES)
    juge('A · Fil, « Cercles » : seules les cartes d\'un Cercle (aucune ici : la Toile du banc n\'a pas d\'événement de Cercle)', all(c['nuee'] or c['etat'] == 'nuee' for c in nu) and len(nu) < len(tous), [(c['etat'], c['nuee']) for c in nu])
    option(pg, '#fdMenu', '#fdTriBtn', 'data-fdfilt', 'tous'); t2 = pg.evaluate(CARTES)
    juge('A · Fil, « Tout » : toutes les cartes reviennent', len(t2) == len(tous), '%d / %d' % (len(t2), len(tous)))
    option(pg, '#fdMenu', '#fdTriBtn', 'data-fdtri', 'personne'); pe = pg.evaluate(CARTES)
    cles = [(c['who'] or 'zz').lower() if (c['who'] or '').lower() != 'moi' else '￿' for c in pe if c['pid']]
    juge('B · Fil, « Par personne » : les cartes rangées par personne', cles == sorted(cles) and [c['pid'] for c in pe] != [c['pid'] for c in tous], cles)
    option(pg, '#fdMenu', '#fdTriBtn', 'data-fdtri', 'recent'); re_ = pg.evaluate(CARTES)
    juge('B · Fil, « Récents » : l\'ordre d\'origine', [c['pid'] for c in re_] == [c['pid'] for c in tous], [c['pid'] for c in re_][:6])
    D = pg.evaluate("""()=>{ const out={}; ['#ixMenu','#fdMenu'].forEach(m=>{ const M=document.querySelector(m); M.classList.add('on'); const on=[...M.querySelectorAll('.ix-mi.on')];
        out[m]={point:/•/.test(M.textContent), barres:on.map(e=>{ const i=e.querySelector('i'); const r=i?i.getBoundingClientRect():null; return r?[Math.round(r.width*10)/10, Math.round(r.height*10)/10, getComputedStyle(i).visibility]:null; }),
          autres:[...M.querySelectorAll('.ix-mi:not(.on) i')].filter(i=>getComputedStyle(i).visibility!=='hidden').length}; M.classList.remove('on'); }); return out; }""")
    okD = all(not v['point'] and v['barres'] and all(x and x[0] > 2 * x[1] and x[1] > 0 and x[2] == 'visible' for x in v['barres']) and v['autres'] == 0 for v in D.values())
    juge('D · le repère de l\'option choisie : une barrette, aucun « • », seulement sur l\'option choisie', okD, D)
    C = pg.evaluate("()=>({fdSort:!!document.getElementById('fdSort'), quad:!!document.querySelector('#ixMenu [data-cols]') || /QUADRILLAGE/.test(document.getElementById('ixMenu').textContent), manq:/Manqu/.test(document.getElementById('ixMenu').textContent+document.getElementById('fdMenu').textContent), atenir:[/À tenir/.test(document.getElementById('ixMenu').textContent), /À tenir/.test(document.getElementById('fdMenu').textContent)]})")
    juge('C · #fdSort retiré, plus de QUADRILLAGE, plus de « Manquées », « À tenir » dans les deux menus', not C['fdSort'] and not C['quad'] and not C['manq'] and all(C['atenir']), C)
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('aucune erreur de page', False, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
