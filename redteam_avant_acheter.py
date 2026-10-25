#!/usr/bin/env python3
"""redteam_avant_acheter.py — ⚑ v163b (Tom, C-190 ; AUDIT-BOUTONS 27, point 2) : « AVANT D'ACHETER » A UNE SORTIE QUI N'ACHÈTE PAS.

« « Avant d'acheter » reçoit « Plus tard » (même dessin que « Garder ton achat »), et un toucher hors de l'encart le ferme. »
Banc comme Tom (WebKit ×3, doigt), sans compte, le vrai chemin : le Studio, un monde de Ma Parole !, « Adopte ce design » :
  A · l'encart porte Apple, Google, « Acheter sans compte » et « Plus tard », celui-ci au dessin de « Acheter sans compte » (police, taille, couleur) ;
  B · « Plus tard » : l'encart se ferme, rien n'est acheté (le monde reste verrouillé), aucun second encart, le Studio reste ouvert, plus aucune
      couche floutée de l'achat après 1,5 s ;
  C · un toucher hors de l'encart : de même ;
  D · « Acheter sans compte » achète toujours (le monde déverrouillé, puis « Garder ton achat »).
Preuve : `--fichier=zz-v162.html` rougit (A, B, C).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
ETAT = "()=>({membre:!!(window.isPremium?isPremium():window._premium), verrou:document.getElementById('studioScreen').classList.contains('world-locked'), studio:document.getElementById('studioScreen').classList.contains('show'), encart:[...document.querySelectorAll('#accRappelCompte .onbv-compte')].map(p=>p.querySelector('.lab').textContent), vu:document.getElementById('accRappelCompte').classList.contains('vu'), flou:document.querySelectorAll('#achatFond, .passage-flaques[data-flou]').length})"
def vers_achat(b):
    ctx = B.contexte(b); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ try{ localStorage.removeItem('promi_compte'); }catch(e){} closeAll(); }"); pg.wait_for_timeout(400)
    B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(2600)
    for i in range(22):
        if pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('world-locked')"): break
        B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1500)
    pg.wait_for_timeout(600); B.tap_sel(pg, '#stLockBuy'); pg.wait_for_timeout(2200)
    return ctx, pg
def centre(pg, sel):
    return pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", sel)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx, pg = vers_achat(b)
    A = pg.evaluate("""()=>{ const p=document.querySelector('#accRappelCompte .onbv-compte'); if(!p) return null; const st=e=>{ const s=getComputedStyle(e); return [s.fontFamily, s.fontSize, s.color, s.textTransform]; };
       const t=[...p.querySelectorAll('.tard')]; return {lab:p.querySelector('.lab').textContent, tard:t.map(e=>e.textContent.trim()), styles:t.map(st), pil:[...p.querySelectorAll('.pil')].map(e=>e.textContent.trim())}; }""")
    juge('A · « Avant d\'acheter » : Apple, Google, « Acheter sans compte » et « Plus tard », au même dessin', A and 'Avant' in A['lab'] and A['tard'] == ['Acheter sans compte', 'Plus tard'] and len(A['pil']) == 2 and A['styles'][0] == A['styles'][1], A)
    if A and 'Plus tard' in A['tard']:
        c = centre(pg, '#accRappelCompte .tard-non'); B.tap(pg, c[0], c[1]); pg.wait_for_timeout(1800); e = pg.evaluate(ETAT)
        juge('B · « Plus tard » : fermé, rien d\'acheté, le monde reste verrouillé, pas de second encart, plus de flou', not e['membre'] and e['verrou'] and e['studio'] and not e['encart'] and not e['vu'] and not e['flou'], e)
    ctx.close()
    ctx, pg = vers_achat(b)
    B.tap(pg, 195, 120); pg.wait_for_timeout(1800); e = pg.evaluate(ETAT)
    juge('C · un toucher hors de l\'encart : fermé, rien d\'acheté, rien d\'autre ne s\'ouvre', not e['membre'] and e['verrou'] and e['studio'] and not e['encart'] and not e['vu'] and not e['flou'], e)
    ctx.close()
    ctx, pg = vers_achat(b)
    c = centre(pg, '#accRappelCompte .tard'); B.tap(pg, c[0], c[1]); pg.wait_for_timeout(2600); e = pg.evaluate(ETAT)
    juge('D · « Acheter sans compte » achète toujours (le monde déverrouillé, puis « Garder ton achat »)', not e['verrou'] and any('Garder' in x for x in e['encart']), e)
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('aucune erreur de page', False, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
