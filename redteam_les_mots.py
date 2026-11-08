# -*- coding: utf-8 -*-
"""⚑ v189b (Tom, C-261) — « LES MOTS » SUR LA FICHE DU CERCLE.
Banc WebKit, Toile du Cercle (échelle 0,79 : PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79) :
  A · Cercle à 1 et 3 mots : le titre « Les Mots » (ce texte), Gilbert 700, 13 pt, interligne 16, chasse 0,10 em, capitales, --c-beige67 (le style des titres de section de l'Aura) ;
  B · ses cotes : 32 pt de la dernière carte du fil au haut du titre (le double des 16 d'avant), 36 pt du bas du titre au premier mot (± 0,5) ; il ne recouvre rien ;
  C · seulement sur le Cercle : absent d'une fiche Promi et Chiche (avec mots), absent d'un Cercle sans mot ; aucune erreur de page."""
import sys, os; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-104s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True); return ok
MOTS = [['Marion', 'On sème samedi ?'], ['Rachel', 'Je prends les graines.'], ['Nico', 'Je passe arroser mardi.']]
LIT = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, dp=document.getElementById('detailPoster'), t=document.getElementById('cm5Titre');
  const vis=t && getComputedStyle(t).display!=='none' && t.getBoundingClientRect().height>0; if(!vis) return {vis:false};
  const R=e=>{ const r=e.getBoundingClientRect(); return [(r.top-D.top)/k+dp.scrollTop, (r.bottom-D.top)/k+dp.scrollTop, (r.left-D.left)/k, (r.right-D.left)/k]; };
  const it=[...document.querySelectorAll('#dpNueeFil .nf-item')], u=document.querySelector('#cm5Liste .cm5-un'), c=getComputedStyle(t);
  const voisins=[...document.querySelectorAll('#dpNueeFil .nf-item, #cm5Liste .cm5-un, #cm5Ligne')].map(R);
  return {vis:true, txt:t.textContent, font:c.font, ls:c.letterSpacing, tt:c.textTransform, col:c.webkitTextFillColor, ref:getComputedStyle(document.documentElement).getPropertyValue('--c-beige67').trim(),
    carte:R(it[it.length-1]), titre:R(t), mot:u?R(u):null, voisins}; }"""
def hexrgb(h): h = h.lstrip('#'); return 'rgb(%d, %d, %d)' % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 7000)
    for n in (1, 3, 0):
        pg.evaluate("()=>{ try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(700)
        pg.evaluate("a=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; a.forEach((x,i)=>o.comments.push({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); _cercleMots.garde(); openEssaim('potager'); }", MOTS[:n]); pg.wait_for_timeout(3000)
        e = pg.evaluate(LIT); T = '[Cercle · %d mot%s]' % (n, 's' if n > 1 else '')
        if n == 0: juge(T + ' C · un Cercle sans mot n\'a pas le titre', not e['vis']); continue
        juge(T + ' A · « Les Mots », Gilbert 700 13/16, chasse 0,10 em, capitales, --c-beige67', e['vis'] and e['txt'] == 'Les Mots' and e['font'].startswith('700 13px / 16px Gilbert') and e['ls'] == '1.3px' and e['tt'] == 'uppercase' and e['col'] == hexrgb(e['ref']), (e.get('txt'), e.get('font'), e.get('ls'), e.get('col'), e.get('ref')))
        if not e['vis']: juge(T + ' B · les cotes (pas de titre)', False); continue
        av = e['titre'][0] - e['carte'][1]; so = e['mot'][0] - e['titre'][1] if e['mot'] else None
        cr = [v for v in e['voisins'] if v[0] < e['titre'][1] - 0.5 and e['titre'][0] < v[1] - 0.5 and v[2] < e['titre'][3] and e['titre'][2] < v[3]]
        juge(T + ' B · 32 pt sous la dernière carte, 36 pt au-dessus du premier mot (± 0,5), aucun recouvrement', abs(av - 32) <= 0.5 and so is not None and abs(so - 36) <= 0.5 and not cr, (round(av, 2), so and round(so, 2), cr[:2]))
    for nat, t in (('promi', 'faire les crêpes'), ('chiche', 'réparer le vélo')):
        pg.evaluate("()=>{ try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(700)
        pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); if(a[1]){ p.chiche=true; p.phraseSens='chiche'; } p.comments=[{t:'Un mot', by:'Marion', d:'2026-11-01T09:00:00Z', vu:true}]; openDetail(p.id); }", [t, nat == 'chiche']); pg.wait_for_timeout(3000)
        e = pg.evaluate(LIT); juge('[%s] C · pas de titre « Les Mots » hors du Cercle' % nat, not e['vis'])
    juge('aucune erreur de page', not [x for x in pg.erreurs if 'Load failed' not in x and 'cancelled' not in x], pg.erreurs[:2])
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
