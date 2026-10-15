#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_commentaires.py — LA LIGNE DE COMMENTAIRE DES FICHES (v145, Tom, 13 oct. 2026 — C-116).

« Quand on reçoit un Promi ou un Chiche de quelqu'un, on a tout de suite envie de commenter : il faut la ligne de commentaire. »
Sur toute fiche Promi ou Chiche REÇUE : une ligne en bas de la fiche, toujours visible, qui ouvre la saisie au toucher ; les commentaires
s'affichent sous le trait, du plus ancien au plus récent, avec le nom et la date. Texte de la ligne, provisoire : « Un mot… ». Ni compteur, ni
pastille, ni relance (CLAUDE.md §12).
Par banc_tom (WebKit, 390 × 844 @3x), au vrai toucher, en clair et en sombre :
  A · la ligne est là sur une parole reçue — à tenir, en cours, tenue ; Promi et Chiche — à 12 pt au-dessus de la barre Peaufiner (692, 342 × 56),
      au doigt (c'est elle que le doigt atteint), avec son texte ;
  B · RÉCEPTION : un commentaire qui arrive paraît au-dessus de la ligne (auteur, date, début), sans chiffre ni pastille, et le Fil ne gagne aucun non-lu ;
  C · toucher la ligne ouvre la SAISIE (le champ a le curseur) et le fil des commentaires sous le trait ;
  D · ENVOI : le texte tapé puis Entrée (et par la flèche) est ajouté, signé, daté, en dernier ; le champ est vidé ; la parole le garde ;
  E · ORDRE : du plus ancien au plus récent, quel que soit l'ordre d'arrivée ; chaque commentaire porte nom et date (v146 : la date sobre — « à l'instant »,
      « il y a 5 min », « hier », « 12 oct. ») ;
  F · (v146, C-116, C-128) le texte à la taille des noms ; le visage petit, rond, sans cerclage ; le nom se touche (il mène à la fiche de la personne) ;
  F · rien ne se superpose : l'ancien champ « écris un mot » est retiré, la ligne, le dernier mot et la ligne d'état ne se recouvrent pas ;
  G · toucher la bande referme la saisie, la fiche reste ;
  H · ce qui ne change pas : une parole à soi « à tenir », sans commentaire, n'a pas de ligne.
`--sonde` retire la zone : le juge rougit. Rouge sur v144 (--port=8762).     Usage : python3 redteam_commentaires.py [fichier.html] [--port=8752] [--sonde]
"""
import re, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); PORT = arg('port', '8752'); SONDE = '--sonde' in sys.argv
TEXTE = 'Un mot…'      # provisoire — texte à écrire par Tom (QUESTIONS)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:300]), flush=True)
ET = r"""()=>{ var dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  function r(id){ var e=document.getElementById(id); if(!e) return null; var q=e.getBoundingClientRect(), cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||q.width<2) return null; return {x:+((q.left-dv.left)/k).toFixed(1), y:+((q.top-dv.top)/k).toFixed(1), w:+(q.width/k).toFixed(1), h:+(q.height/k).toFixed(1), t:(e.textContent||'').replace(/\s+/g,' ').trim()}; }
  var l=document.getElementById('cm5Ligne'), a=document.activeElement, s=l?l.querySelector('.cm5-saisie'):null, au=null;
  if(l){ var q=l.getBoundingClientRect(), e=document.elementFromPoint(q.left+60, q.top+q.height/2); au=!!(e && l.contains(e)); }
  var dq=document.getElementById('dptQuand'), qq=dq?dq.getBoundingClientRect():null, co=document.getElementById('dpCorps');
  return {ligne:r('cm5Ligne'), dernier:r('cm5Dernier'), fil:r('cm5Fil'), auDoigt:au, saisie:!!(s && a===s), valeur:s?s.value:null, motVu:l?(function(){ var m=l.querySelector('.cm5-mot'); return m&&getComputedStyle(m).display!=='none'?m.textContent:''; })():null,
    uns:[...document.querySelectorAll('#cm5Fil .cm5-un')].map(e=>{ const c=e.querySelector(':scope > div'); return [c?c.children[0].textContent:'', c?c.children[1].textContent:'']; }), etatBas:qq?+((qq.bottom-dv.top)/k).toFixed(1):null, ancien:co?getComputedStyle(co).display:null,
    comm:(typeof cur!=='undefined'&&cur&&cur.comments||[]).map(c=>[c.by,c.t]), fiche:document.getElementById('detailPoster').classList.contains('show'), nonlus:(typeof FEED!=='undefined')?FEED.filter(f=>f.unread).length:null}; }"""
def fiche(pg, pid):
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600)
def recue(pg, titre, nature, de, statut=None):
    B.plante_doigt(pg, titre, 'moi', nature)
    return pg.evaluate("a=>{ var p=promises[promises.length-1]; p.from=a[0]; p.who='moi'; if(a[1]) p.status=a[1]; try{queueSave()}catch(e){} return p.id; }", [de, statut])
def ligne_ok(e): l = e.get('ligne'); return bool(l) and abs(l['x'] - 24) <= 1 and abs(l['y'] - 692) <= 1 and abs(l['w'] - 342) <= 1 and abs(l['h'] - 56) <= 1 and e.get('motVu') == TEXTE and e.get('auDoigt')
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        th = 'sombre' if sombre else 'clair'
        ctx = B.contexte(b, sombre=sombre); pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%s/%s' % (PORT, F)); pg.wait_for_timeout(6500)
        if SONDE: pg.evaluate("()=>{ if(window._comm){ window._comm.actif=function(){ return false; }; } }")
        try:
            # A · la ligne, sur une parole reçue, dans les trois états
            p1 = recue(pg, 'venir au concert', 0, 'Marion', 'rate'); fiche(pg, p1); e = pg.evaluate(ET)
            juge('A · [%s] Promi reçu, à tenir : la ligne est là, à sa place, au doigt, « %s »' % (th, TEXTE), ligne_ok(e), e.get('ligne'))
            juge('F · [%s] l\'ancien champ est retiré, la ligne ne touche ni la ligne d\'état ni la barre' % th, e.get('ancien') == 'none' and bool(e.get('ligne')) and e['etatBas'] is not None and e['etatBas'] + 8 <= e['ligne']['y'] and e['ligne']['y'] + e['ligne']['h'] + 11 <= 760, 'ancien champ : %s · état jusqu\'à %s · ligne %s' % (e.get('ancien'), e.get('etatBas'), e.get('ligne')))
            # B · réception
            nl0 = e.get('nonlus')
            pg.evaluate("id=>_comm.arrive(promises.find(p=>p.id===id),{t:'Promis, j’y serai. Tu gardes une place ?',by:'Marion',d:'2026-10-11T18:00:00.000Z'})", p1); pg.wait_for_timeout(700); e = pg.evaluate(ET)
            d = e.get('dernier') or {}
            juge('B · [%s] RÉCEPTION : le commentaire reçu paraît au-dessus de la ligne (auteur, date, début)' % th, bool(d) and 'MARION' in d.get('t', '').upper() and '11 oct.' in d.get('t', '') and 'Promis' in d.get('t', '') and d['y'] + d['h'] <= e['ligne']['y'] and e['etatBas'] <= d['y'], d)
            juge('B · [%s] ni compteur ni pastille : la ligne ne porte aucun chiffre, le Fil ne gagne aucun non-lu' % th, not any(ch.isdigit() for ch in (e['ligne'] or {}).get('t', '')) and e.get('nonlus') == nl0, 'ligne « %s » · non-lus du Fil %s → %s' % ((e['ligne'] or {}).get('t'), nl0, e.get('nonlus')))
            # C · toucher la ligne ouvre la saisie
            B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(900); e = pg.evaluate(ET)
            juge('C · [%s] toucher la ligne ouvre la saisie (le champ a le curseur) et le fil des commentaires sous le trait' % th, e.get('saisie') and bool(e.get('fil')) and e['fil']['y'] > 300 and len(e.get('uns', [])) == 1, 'saisie %s · fil %s · %d commentaire(s)' % (e.get('saisie'), e.get('fil'), len(e.get('uns', []))))
            # D · envoi, par Entrée puis par la flèche
            pg.keyboard.type('Oui, au premier rang'); pg.keyboard.press('Enter'); pg.wait_for_timeout(700); e = pg.evaluate(ET)
            juge('D · [%s] ENVOI par Entrée : ajouté en dernier, signé, daté ; le champ est vidé ; la parole le garde' % th, len(e.get('uns', [])) == 2 and 'Oui, au premier rang' in e['uns'][-1][1] and 'TOM' in e['uns'][-1][0].upper() and ('instant' in e['uns'][-1][0].lower() or 'il y a' in e['uns'][-1][0].lower()) and e.get('valeur') == '' and e['comm'][-1][1] == 'Oui, au premier rang', e.get('uns'))
            pg.keyboard.type('À samedi'); B.tap_sel(pg, '#cm5Ligne .cm5-va'); pg.wait_for_timeout(700); e = pg.evaluate(ET)
            juge('D · [%s] ENVOI par la flèche' % th, len(e.get('uns', [])) == 3 and e['uns'][-1][1] == 'À samedi', e.get('uns', [])[-1:])
            # E · l'ordre : un commentaire plus ancien arrive après coup
            pg.evaluate("id=>_comm.arrive(promises.find(p=>p.id===id),{t:'Je prends les billets',by:'Marion',d:'2026-10-09T08:00:00.000Z'})", p1); pg.wait_for_timeout(600); e = pg.evaluate(ET)
            juge('E · [%s] ORDRE : du plus ancien au plus récent, chacun avec son nom et sa date' % th, [u[1] for u in e.get('uns', [])] == ['Je prends les billets', 'Promis, j’y serai. Tu gardes une place ?', 'Oui, au premier rang', 'À samedi'] and all(re.search(r'(instant|il y a|hier|\d+ \w+\.)', u[0]) for u in e['uns']), [u[0] + ' — ' + u[1][:24] for u in e.get('uns', [])])
            st = pg.evaluate("()=>{ const u=document.querySelector('#cm5Fil .cm5-un'); if(!u) return null; const c=u.querySelector(':scope > div'), nm=c.children[0].querySelector('.nom-lien'), tx=c.children[1], v=u.querySelector('.cm5-vis'); const S=x=>getComputedStyle(x); return {fsNom:nm?parseFloat(S(nm).fontSize):0, fsTxt:parseFloat(S(tx).fontSize), r:v?S(v).borderRadius:'', bord:v?S(v).borderTopWidth:'', ombre:v?S(v).boxShadow:'', contour:v?S(v).outlineStyle:'', w:v?v.getBoundingClientRect().width:0, lien:!!nm}; }")
            juge('F · [%s] v146 (C-116) : le texte d\'un mot a la taille des noms ; (C-128) le visage est petit, rond, à gauche, SANS cerclage ni bord ni ombre ; le nom se touche' % th,
                 bool(st) and st['fsNom'] == st['fsTxt'] >= 16 and (st['r'] in ('50%', '9999px') or ('px' in st['r'] and float(st['r'].replace('px', '')) >= st['w'] / 2 - 0.5)) and st['bord'] in ('0px', '') and st['ombre'] in ('none', '') and st['lien'], st)
            B.capture(pg, 'scratchpad/v145/comm-ouvert-%s.png' % th)
            # G · toucher la bande referme la saisie, la fiche reste
            B.tap(pg, 195, 170); pg.wait_for_timeout(900); e = pg.evaluate(ET)
            juge('G · [%s] toucher la bande referme la saisie, la fiche reste, le dernier mot est au-dessus de la ligne' % th, e.get('fiche') and not e.get('saisie') and not e.get('fil') and e.get('motVu') == TEXTE and 'samedi' in (e.get('dernier') or {}).get('t', ''), 'fiche %s · saisie %s · dernier %s' % (e.get('fiche'), e.get('saisie'), e.get('dernier')))
            B.capture(pg, 'scratchpad/v145/comm-ferme-%s.png' % th)
            # A · les autres états reçus
            p2 = recue(pg, 'le grand plongeoir', 1, 'Rachel'); fiche(pg, p2); e = pg.evaluate(ET)
            juge('A · [%s] Chiche reçu, lancé : la ligne est là' % th, ligne_ok(e), e.get('ligne'))
            p3 = recue(pg, 'rendre le livre', 0, 'Nico', 'tenu'); fiche(pg, p3); e = pg.evaluate(ET)
            juge('A · [%s] Promi reçu, tenu : la ligne est là' % th, ligne_ok(e), e.get('ligne'))
            # H · ce qui ne change pas
            B.plante_doigt(pg, 'arroser le ficus', 'moi', 0); p4 = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.status='rate'; return p.id; }"); fiche(pg, p4); e = pg.evaluate(ET)
            juge('H · [%s] une parole à soi, à tenir, sans commentaire : pas de ligne (inchangé)' % th, not e.get('ligne'), e.get('ligne'))
        except Exception as ex:
            juge('le juge va au bout [%s]' % th, False, str(ex).replace('\n', ' ')[:260])
        juge('aucune erreur de page [%s]' % th, not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:1000])
sys.exit(0 if ok == len(res) else 1)
