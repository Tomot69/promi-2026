#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_cadre.py — LA PHOTO D'UNE FICHE SE CADRE AU DOIGT (v139, Tom, 9 oct. 2026, C-085).

« Recadrer au pincement, comme dans Photos sur iPhone, avec la même sensibilité : on écarte ou on rapproche deux doigts pour zoomer, on
glisse pour déplacer. Elle peut remplir tout le haut, être très zoomée ou dézoomée. Le cadrage est mémorisé par fiche. En plein écran, un
petit bouton “Enregistrer la photo”. Partout : fiches Promi, Chiche et page +. »
Au vrai doigt (CDP `Input.dispatchTouchEvent`, un et deux doigts), Chromium. La photo d'essai : quatre quarts de couleur.
  1 · sans geste, la photo garde sa boîte (aucun cadrage posé) ;
  2 · écarter deux doigts du simple au double zoome du simple au double (± 6 %) — la sensibilité de Photos, 1:1 ;
  3 · à l'écran : le quart haut-gauche de la photo couvre maintenant le centre de la bande (pixels) ;
  4 · rapprocher jusqu'au tiers dézoome d'autant ; la photo dézoomée laisse voir le champ de la nature autour (pixels) ;
  5 · glisser d'un doigt de 60 pt déplace la photo de 60 pt (± 3), et n'ouvre ni la vue en entier ni Peaufiner ;
  6 · un pincement n'ouvre pas la vue en entier ; un toucher simple l'ouvre toujours ;
  7 · la vue en entier porte le bouton « Enregistrer la photo » (visible, sous le doigt), le toucher enregistre et ne referme pas ;
  8 · le cadrage est mémorisé : après rechargement de la page, la fiche le retrouve ;
  9 · un Chiche : pareil ; la page + : pareil (pincement), et le cadrage suit la photo ;
 10 · les bornes déclarées (0,3 à 8).
Preuve : sur l'état d'avant (`zz-av139.html`) il rougit (aucun cadrage, aucun bouton).
"""
import sys
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
PHOTO = r"""()=>{ const c=document.createElement('canvas'); c.width=600; c.height=400; const g=c.getContext('2d'); [['#E00000',0,0],['#00B000',300,0],['#0000E0',0,200],['#E0E000',300,200]].forEach(q=>{ g.fillStyle=q[0]; g.fillRect(q[1],q[2],300,200); }); return c.toDataURL('image/png'); }"""
ETAT = "()=>{ try{ return window._photoCadre ? window._photoCadre.etat() : null; }catch(e){ return null; } }"
PIX = r"""([x,y])=>{ const cv=document.getElementById(document.getElementById('createSheet').classList.contains('show')?'csTrameCv':'dpTrameCv'), r=cv.getBoundingClientRect(); const d=cv.getContext('2d').getImageData(Math.round((x-r.left)*cv.width/r.width), Math.round((y-r.top)*cv.height/r.height),1,1).data; return [d[0],d[1],d[2]]; }"""
def couleur(c):
    r, g, b = c
    if r > 180 and g < 90 and b < 90: return 'rouge'
    if g > 130 and r < 90 and b < 90: return 'vert'
    if b > 180 and r < 90 and g < 90: return 'bleu'
    if r > 180 and g > 180 and b < 90: return 'jaune'
    return 'autre'
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, has_touch=True)
    ctx.add_init_script("try{ if(!localStorage.getItem('promi_onb')){ localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9'); ['tenir','chiche','planter','bande'].forEach(g=>localStorage.setItem('geste_vu_'+g,'1')); } }catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    src = pg.evaluate(PHOTO)
    def T(typ, pts): cdp.send('Input.dispatchTouchEvent', {'type': typ, 'touchPoints': [{'x': x, 'y': y, 'id': i} for i, (x, y) in enumerate(pts)]})
    def pince(cx, cy, d0, d1, n=12):
        T('touchStart', [(cx - d0 / 2, cy)]); T('touchStart', [(cx - d0 / 2, cy), (cx + d0 / 2, cy)])
        for i in range(1, n + 1):
            d = d0 + (d1 - d0) * i / n; T('touchMove', [(cx - d / 2, cy), (cx + d / 2, cy)]); pg.wait_for_timeout(18)
        T('touchEnd', []); pg.wait_for_timeout(500)
    def glisse(x, y, dx, dy, n=10):
        T('touchStart', [(x, y)])
        for i in range(1, n + 1): T('touchMove', [(x + dx * i / n, y + dy * i / n)]); pg.wait_for_timeout(18)
        T('touchEnd', []); pg.wait_for_timeout(500)
    def tape(x, y): T('touchStart', [(x, y)]); pg.wait_for_timeout(60); T('touchEnd', []); pg.wait_for_timeout(700)
    def bande():
        return pg.evaluate("()=>{ const c=window._photoCentre||{x:195,y:150}; const cv=document.getElementById(document.getElementById('createSheet').classList.contains('show')?'csTrameCv':'dpTrameCv'), r=cv.getBoundingClientRect(), k=r.width/390; return [r.left+c.x*k, r.top+c.y*k, k]; }")
    entier = "()=>!!(window._entier&&window._entier.ouverte())"
    peauf = "()=>document.getElementById('detailPoster').classList.contains('s2-ouv')"
    for nom, titre in (('Promi', 'faire les crêpes'), ('Chiche', 'courir dimanche')):
        pg.evaluate("([t,s])=>{ try{closeAll()}catch(e){} const q=promises.find(p=>p.title===t); q.photo=s; delete q.photoCadre; openDetail(q.id); }", [titre, src]); pg.wait_for_timeout(3200)
        cx, cy, k = bande(); e0 = pg.evaluate(ETAT)
        juge('1 · [%s] sans geste, aucun cadrage posé' % nom, e0 is not None and not e0['pose'] and e0['z'] == 1, str(e0))
        pince(cx, cy, 60, 120); e1 = pg.evaluate(ETAT) or {'z': 0, 'dx': 0, 'dy': 0}
        juge('2 · [%s] écarter du simple au double zoome du simple au double (± 6 %%)' % nom, abs(e1['z'] - 2.0) <= 0.12, 'z = %.3f' % e1['z'])
        juge('6 · [%s] un pincement n\'ouvre pas la vue en entier' % nom, not pg.evaluate(entier))
        if nom == 'Promi':
            c1 = pg.evaluate(PIX, [cx - 40 * k, cy - 20 * k]); c2 = pg.evaluate(PIX, [cx + 40 * k, cy + 20 * k])
            juge('3 · à l\'écran, zoomée ×2 autour du centre : les quatre quarts restent autour du centre', couleur(c1) == 'rouge' and couleur(c2) == 'jaune', '%s / %s' % (couleur(c1), couleur(c2)))
            pince(cx, cy, 180, 30); e2 = pg.evaluate(ETAT) or {'z': 0}
            juge('4 · rapprocher jusqu\'au sixième dézoome d\'autant (2 → 0,33)', abs(e2['z'] - 2.0 / 6) <= 0.04, 'z = %.3f' % e2['z'])
            c3 = pg.evaluate(PIX, [cx - 150 * k, cy]); juge('4 · dézoomée, la photo laisse voir le champ de la nature autour', couleur(c3) == 'autre' and c3[2] > 200, str(c3))
            pince(cx, cy, 40, 120); pg.wait_for_timeout(200)
        av = pg.evaluate(ETAT) or {'dx': 0, 'dy': 0}; glisse(cx, cy, 60 * k, -20 * k); ap = pg.evaluate(ETAT) or {'dx': 0, 'dy': 0}
        juge('5 · [%s] glisser de (60 ; −20) pt déplace la photo d\'autant (± 3 pt après le seuil)' % nom, abs(ap['dx'] - av['dx'] - 60) <= 13 and abs(ap['dy'] - av['dy'] + 20) <= 6 and ap['dx'] - av['dx'] > 40, 'Δ = (%.1f ; %.1f)' % (ap['dx'] - av['dx'], ap['dy'] - av['dy']))
        juge('5 · [%s] … sans ouvrir ni la vue en entier ni Peaufiner' % nom, not pg.evaluate(entier) and not pg.evaluate(peauf))
        tape(cx, cy); ouv = pg.evaluate(entier)
        juge('6 · [%s] un toucher simple ouvre toujours la photo en entier' % nom, ouv)
        if nom == 'Promi':
            g = pg.evaluate("()=>{ const e=document.querySelector('#entierVue .ev-garde'); if(!e) return null; const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2), c=getComputedStyle(e); return {x:r.left+r.width/2, y:r.top+r.height/2, w:r.width, h:r.height, txt:e.textContent.trim(), voix:e.getAttribute('aria-label'), ico:!!e.querySelector('svg[data-symbole=enregistrer]'), dessus:(h===e||e.contains(h)), vis:c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity===1}; }")
            # ⚑ v140 (Tom, C-091) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_cadre-avant-v140.py) : « Un seul bouton Enregistrer, partout. Une icône seule, sans texte […]. Elle remplace le texte “Enregistrer la photo”. VoiceOver : “Enregistrer”. »
            juge('7 · en plein écran, l\'icône « Enregistrer » est là (sans texte, VoiceOver « Enregistrer »), visible, sous le doigt, 44 pt', bool(g) and g['txt'] == '' and g['voix'] == 'Enregistrer' and g['ico'] and g['dessus'] and g['vis'] and g['h'] >= 44 and g['w'] >= 44, str(g))
            if g:
                n0 = pg.evaluate("()=>window._entierEnregistre||0"); tape(g['x'], g['y'])
                juge('7 · le toucher enregistre, et ne referme pas la vue', pg.evaluate("()=>window._entierEnregistre||0") == n0 + 1 and pg.evaluate(entier))
        pg.evaluate("()=>{ try{ window._entier.ferme(); }catch(e){} }"); pg.wait_for_timeout(300)
    # 8 · mémorisé
    pg.evaluate("()=>{ try{ saveState(); }catch(e){} }"); m0 = pg.evaluate("()=>{ const q=promises.find(p=>p.title==='faire les crêpes'); return q.photoCadre||null; }")
    pg.reload(); pg.wait_for_timeout(6500); pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    m1 = pg.evaluate("()=>{ const q=promises.find(p=>p.title==='faire les crêpes'); return (q&&q.photoCadre)||null; }")
    juge('8 · le cadrage est mémorisé avec la fiche : il revient après rechargement', bool(m0) and bool(m1) and abs(m0['z'] - m1['z']) < 1e-6 and abs(m0['dx'] - m1['dx']) < 1e-6, '%s → %s' % (m0 and {k: round(v, 2) for k, v in m0.items()}, m1 and {k: round(v, 2) for k, v in m1.items()}))
    # 9 · la page +
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })(); }"); pg.wait_for_timeout(3200)
    pg.evaluate("(s)=>{ window._phrase.photo=s; delete window._phrase.photoCadre; try{ if(window._ppTout)_ppTout(); else _ppTrait(); }catch(e){} }", src); pg.wait_for_timeout(1500)
    cx, cy, k = bande(); pince(cx, cy, 60, 120); e9 = pg.evaluate(ETAT) or {'z': 0, 'pose': False}
    juge('9 · la page + : le pincement cadre la photo (du simple au double)', abs(e9['z'] - 2.0) <= 0.12 and e9['pose'], 'z = %.3f' % e9['z'])
    juge('9 · la page + : le cadrage vit avec la photo du brouillon', pg.evaluate("()=>!!(window._phrase.photoCadre && window._phrase.photoCadre.n===window._phrase.photo.length)"))
    bz = pg.evaluate("()=>window._photoCadre ? [_photoCadre.bornes.ZMIN,_photoCadre.bornes.ZMAX] : null")
    juge('10 · les bornes déclarées du zoom : 0,3 à 8', bz == [0.3, 8], str(bz))
    juge('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:12]))
sys.exit(1 if ko else 0)
