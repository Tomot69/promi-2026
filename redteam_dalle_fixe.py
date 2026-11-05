#!/usr/bin/env python3
"""redteam_dalle_fixe.py — ⚑ v179b (Tom, C-234) : PAGE + — LA DALLE NE ZOOME JAMAIS.

« La dalle garde TOUJOURS la même taille, du début à la fin, pendant la frappe comme à la validation. Elle se contente de DESCENDRE et de REMONTER avec
l'horizon : 12 à 18 pt au plus, un mouvement doux. »
Banc WebKit ×3, état exporté de Tom, trois natures, échelles 1 et 0,79 (`--echelle=`). Chaque dessin de la dalle sur le champ de la page + est PIÉGÉ
(`_poseDalle` sur #csTrameCv : la taille et la place réellement peintes), page montrée seulement, de l'ouverture à 3 s après la validation (Retour) :
  A · une seule taille de dalle à toutes les étapes (± 0,05 pt) — ouverture, champ ouvert, frappe longue (la phrase change de lignes), validation ;
  B · le déplacement total ≤ 18 pt ; C · aucun saut : ≤ 3 pt par image de 16,7 ms ; D · le mouvement a lieu (≥ 8 pt) ; aucune erreur de page.
Rouge sur v178 (`--fichier=zz-v178.html`) : 147 × 167, puis 390 × 191 pendant la frappe, puis 176 × 200.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), '1,0.79')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:230]), flush=True)
PIEGE = """()=>{ if(window.__pdP) return; window.__pdP=1; window.__pd=[]; const f=window._poseDalle;
  window._poseDalle=function(g,id,x,y,w,h,o){ const r=f.apply(this, arguments); try{ const cs=document.getElementById('createSheet');
    if(g && g.canvas && g.canvas.id==='csTrameCv' && cs.classList.contains('show') && !cs.classList.contains('acc-passe') && getComputedStyle(cs).visibility==='visible' && r)
      window.__pd.push([Math.round(performance.now()), +r.w.toFixed(2), +r.h.toFixed(2), +r.x.toFixed(2), +r.y.toFixed(2)]); }catch(_){ } return r; }; }"""
SEL = {'promi': '#csPhrase .ph-m[data-ph="titre"]', 'chiche': '#csPhrase .ph-m[data-ph="titre"]', 'nuee': '#nueePhrase .ph-m[data-np="nom"]'}
with sync_playwright() as p:
    b = p.webkit.launch()
    for ech in ECH.split(','):
        for nat in ('promi', 'chiche', 'nuee'):
            T = '[%s · ×%s]' % (nat, ech)
            ctx, d = B.contexte_tom(b, echelle=1 if ech == '1' else None)
            if ech != '1': ctx.close(); ctx, d = B.contexte_tom(b); 
            pg = B.ouvre(ctx, F); pg.evaluate(PIEGE)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
            B.tap_sel(pg, SEL[nat]); pg.wait_for_timeout(900)
            pg.keyboard.type('apprendre le violoncelle avec mes enfants le dimanche matin', delay=35); pg.wait_for_timeout(900)
            pg.keyboard.press('Enter'); pg.wait_for_timeout(3200)
            L = pg.evaluate("()=>window.__pd")
            tailles = sorted(set((w, h) for _, w, h, x, y in L)); ys = [y for _, w, h, x, y in L]
            juge(T + ' A · une seule taille de dalle, de l\'ouverture à la validation (%d dessins)' % len(L), len(L) >= 10 and max(w for w, h in tailles) - min(w for w, h in tailles) <= 0.05 and max(h for w, h in tailles) - min(h for w, h in tailles) <= 0.05, tailles[:4])
            if ys:
                # un saut se juge à la VITESSE : au plus 3 pt par image de 16,7 ms (deux dessins espacés de plusieurs images, sous charge, ne sont pas un saut)
                v = [abs(L[i + 1][4] - L[i][4]) / max(1.0, (L[i + 1][0] - L[i][0]) / 16.7) for i in range(len(L) - 1)]
                pas = max(v or [0])
                juge(T + ' B · le déplacement total ≤ 18 pt', max(ys) - min(ys) <= 18, 'de %.2f à %.2f' % (min(ys), max(ys)))
                juge(T + ' C · aucun saut : ≤ 3 pt par image (16,7 ms)', pas <= 3, 'pas max %.2f pt / image' % pas)
                juge(T + ' D · elle descend et remonte avec l\'horizon (≥ 8 pt)', max(ys) - min(ys) >= 8, '%.2f pt' % (max(ys) - min(ys)))
            juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
