#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_deplace.py — DÉPLACER UNE DALLE SUR SA TOILE (v142, Tom, 11 oct. 2026, C-101).

La décision : « Un appui de 0,8 s sur une dalle la détache : léger agrandissement, sans ombre ; elle suit le doigt, les voisines se
réorganisent ; au lâcher elle reste où on l'a posée, sa place est gardée ; jamais sous la barre du bas. »

Comme Tom la voit (banc_tom : WebKit, 390 × 844, échelle 3, doigt, Toile de ses seules paroles, plantées par l'app), sous CINQ mondes.
Les valeurs décidées sont EN DUR : 0,8 s (800 ms), barre à 710 pt. `Toile.hit` n'est qu'un POINTEUR (où est la dalle) ; les verdicts se lisent
sur la place de la dalle à l'écran, la fiche ouverte ou non, ce qui est sauvegardé.
  1 · appui de 0,95 s puis glissé : la dalle est attrapée (à mi-geste) et finit sous le doigt (≤ 50 pt du point de lâcher — une demi-dalle) ;
  2 · aucune fiche ne s'ouvre au lâcher ; les autres paroles sont toujours sur la Toile ; la vue (zoom) n'a pas changé ;
  3 · un toucher bref ouvre toujours la fiche ; un glissé sans attendre (0,2 s) ne déplace aucune dalle ;
  4 · après rechargement, la dalle est où on l'a posée DANS LA TOILE (la vue se recadre : le point de l'écran est ramené par la vue) ;
  5 · lâchée sous la barre (y 800), elle reste atteignable au-dessus (centre < 710) ;
  6 · la règle déclarée : 800 ms.
Preuve : rouge sur v141 (python3 redteam_deplace.py zz-av142.html --mondes=pochade).
"""
import sys, math
from playwright.sync_api import sync_playwright
from banc_tom import contexte, ouvre, dev, tap, glisse, droite, plante, capture
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
MONDES = next((a.split('=')[1].split(',') for a in sys.argv[1:] if a.startswith('--mondes=')), ['pochade', 'touffe', 'mosaique', 'ritournelle', 'bobinette'])
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:260]), flush=True)
OU = """()=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390, kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height, G={};
  for(let y=110;y<706;y+=6) for(let x=8;x<384;x+=6){ let h=null; try{ h=Toile.hit((d.left+x*k-r.left)*kx,(d.top+y*k-r.top)*ky); }catch(e){} if(h&&h.pid!=null){ const g=G[h.pid]=G[h.pid]||{n:0,x:0,y:0}; g.n++; g.x+=x; g.y+=y; } }
  let v=null; try{ v=Toile_vueLue(); }catch(e){} const o={}; for(const p in G){ const X=G[p].x/G[p].n, Y=G[p].y/G[p].n, cx=(d.left+X*k-r.left)*kx, cy=(d.top+Y*k-r.top)*ky; o[p]=[X, Y, G[p].n, v?(cx-v.ox)/v.s:X, v?(cy-v.oy)/v.s:Y]; } return o; }"""
ETAT = "()=>{const dp=document.getElementById('detailPoster'); let v=null; try{v=Toile.view&&Toile.view()}catch(e){} return {fiche:!!(dp&&dp.classList.contains('show')), tire:(window.Toile_tire?Toile_tire():null), regle:window.Toile_tireRegle||null}}"
with sync_playwright() as p:
    b = p.webkit.launch()
    for m in MONDES:
        ctx = contexte(b); pg = ouvre(ctx, F)
        pg.evaluate("(m)=>{try{setPremium(true)}catch(e){} Toile.setTheme(m)}", m); pg.wait_for_timeout(1500)
        for t in ('arroser le figuier', 'écrire à Lou', 'réparer le vélo'): plante(pg, t)
        pg.wait_for_timeout(1200)
        G = pg.evaluate(OU); pids = sorted(G, key=lambda k: -G[k][2])
        if len(pids) < 3: juge('%s · trois paroles plantées et visibles' % m, False, G); ctx.close(); continue
        a = pids[0]; x0, y0 = G[a][0], G[a][1]
        # la cible : à 110 pt de là, vers le milieu de la zone libre
        cx, cy = 195, 400; d = math.hypot(cx - x0, cy - y0) or 1; x1, y1 = x0 + (cx - x0) / d * 110, y0 + (cy - y0) / d * 110
        if d < 60: x1, y1 = x0 + 90, y0 + 90
        # 3 · un glissé SANS attendre ne déplace rien
        pg.evaluate("()=>{window.__tire=0; window.__it=setInterval(()=>{ if(window.Toile_tire&&Toile_tire()) window.__tire++; },30)}")
        glisse(pg, droite((x0, y0), (x0 + 40, y0 + 50), 8), pas=20, tenue=200); pg.wait_for_timeout(900)
        n0 = pg.evaluate("()=>window.__tire"); pg.evaluate("()=>{try{Toile.recadre&&0}catch(e){}}")
        juge('%s · 3 · un glissé sans attendre 0,8 s ne détache aucune dalle' % m, n0 == 0, 'images « attrapée » : %s' % n0)
        pg.reload(); pg.wait_for_timeout(6500); G = pg.evaluate(OU)
        if a not in G: juge('%s · la parole est toujours là après rechargement' % m, False, G); ctx.close(); continue
        x0, y0 = G[a][0], G[a][1]; d = math.hypot(cx - x0, cy - y0) or 1; x1, y1 = (x0 + (cx - x0) / d * 110, y0 + (cy - y0) / d * 110) if d >= 60 else (x0 + 90, y0 + 90)
        pg.evaluate("()=>{window.__tire=0; window.__it=setInterval(()=>{ if(window.Toile_tire&&Toile_tire()) window.__tire++; },30)}")
        capture(pg, 'planche-v142/deplace-%s-%s-1avant.png' % (F.replace('.html', ''), m))
        glisse(pg, droite((x0, y0), (x1, y1), 14), pas=40, tenue=950)
        e = pg.evaluate(ETAT); n1 = pg.evaluate("()=>window.__tire"); pg.wait_for_timeout(1600)
        capture(pg, 'planche-v142/deplace-%s-%s-2apres.png' % (F.replace('.html', ''), m))
        G2 = pg.evaluate(OU); e2 = pg.evaluate(ETAT)
        ou = G2.get(a); dist = math.hypot(ou[0] - x1, ou[1] - y1) if ou else 999
        if m == 'ritournelle':
            # ⚑ v146 (chef de chantier, Q496) — CONTRAT RÉÉCRIT pour Ritournelle (original : sauvegardes/redteam_deplace-avant-v146.py) : « on garde le cadrage
            #   de Ritournelle et on répare le déplacement sans y toucher ; si c'est impossible, le déplacement est désactivé dans ce cas, sans message ».
            #   Une coulée se centre sur sa cellule, pas sur sa graine : impossible sans toucher au cadrage — l'appui long n'attrape rien, la dalle reste.
            reste = ou and math.hypot(ou[0] - x0, ou[1] - y0) <= 20
            msg = pg.evaluate("()=>[...document.querySelectorAll('.toast,[role=alert],[role=status]')].filter(e=>e.getBoundingClientRect().width>0&&e.textContent.trim()).length")
            juge('%s · Q496 · l\'appui long n\'attrape rien, la dalle reste à sa place, aucune fiche, aucun message (déplacement désactivé sous Ritournelle)' % m, n1 == 0 and reste and not e2['fiche'] and msg == 0 and pg.evaluate("()=>!!(window.Toile_tireNon&&Toile_tireNon.ritournelle)"),
                  'attrapée %s · départ (%.0f, %.0f) → %s · fiche %s · messages %s' % (n1, x0, y0, ou and [round(v) for v in ou[:2]], e2['fiche'], msg))
            tap(pg, ou[0], ou[1]); pg.wait_for_timeout(1500); e5 = pg.evaluate(ETAT)
            juge('%s · Q496 · un toucher bref ouvre toujours la fiche' % m, e5['fiche'])
            juge('%s · aucune erreur de page' % m, not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close(); continue
        juge('%s · 1 · appui 0,95 s puis glissé : la dalle est attrapée pendant le geste' % m, n1 >= 3, 'images « attrapée » : %s' % n1)
        juge('%s · 1 · elle finit sous le doigt (≤ 50 pt du lâcher), à plus de 60 pt de son départ' % m, dist <= 50 and ou and math.hypot(ou[0] - x0, ou[1] - y0) >= 60, 'départ (%.0f, %.0f) · lâcher (%.0f, %.0f) · dalle %s' % (x0, y0, x1, y1, ou and [round(v) for v in ou[:2]]))
        juge('%s · 2 · aucune fiche ne s\'ouvre ; les deux autres paroles sont toujours là' % m, not e2['fiche'] and all(q in G2 for q in pids[:3]), 'fiche %s · paroles %d' % (e2['fiche'], len(G2)))
        # 4 · après rechargement
        pg.reload(); pg.wait_for_timeout(6500); G3 = pg.evaluate(OU); o3 = G3.get(a)
        # au rechargement la vue se recadre (c'est la règle) : la place se compare DANS LA TOILE (le point de l'écran ramené par la vue, qui n'est qu'un pointeur)
        juge('%s · 4 · après rechargement, elle est où on l\'a posée dans la Toile (≤ 30 pt de Toile), plus à sa place de départ (≥ 15)' % m,
             o3 and ou and math.hypot(o3[3] - ou[3], o3[4] - ou[4]) <= 30 and math.hypot(o3[3] - G[a][3], o3[4] - G[a][4]) >= 15, 'départ %s · posée %s · relue %s' % tuple(x and [round(v) for v in x[3:5]] for x in (G[a], ou, o3)))
        if o3:
            # 5 · lâchée sous la barre
            glisse(pg, droite((o3[0], o3[1]), (195, 800), 16), pas=40, tenue=950); pg.wait_for_timeout(1600); G4 = pg.evaluate(OU); o4 = G4.get(a)
            capture(pg, 'planche-v142/deplace-%s-%s-3barre.png' % (F.replace('.html', ''), m))
            juge('%s · 5 · lâchée sous la barre (y 800) : elle reste atteignable au-dessus (centre < 710)' % m, o4 and o4[1] < 710 and o4[2] >= 12, 'dalle %s' % (o4 and [round(v) for v in o4]))
            # 3 · un toucher bref ouvre toujours la fiche
            if o4:
                tap(pg, o4[0], o4[1]); pg.wait_for_timeout(1500); e5 = pg.evaluate(ETAT)
                juge('%s · 3 · un toucher bref ouvre toujours la fiche' % m, e5['fiche'], e5['fiche'])
        juge('%s · 6 · la règle déclarée : 800 ms' % m, (e.get('regle') or {}).get('MS') == 800, e.get('regle'))
        juge('%s · aucune erreur de page' % m, not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2])
        ctx.close()
    b.close()
n = sum(1 for _, c in res if c); print('\n%d/%d' % (n, len(res)))
if n < len(res): sys.exit(1)
