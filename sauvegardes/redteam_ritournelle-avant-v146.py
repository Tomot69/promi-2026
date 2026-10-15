#!/usr/bin/env python3
"""
redteam_ritournelle.py — RITOURNELLE : LE CADRAGE D'AVANT C-088, TEL QUEL (v145, Tom, 13 oct. 2026 — C-088, CLOS).

« Toujours ultra dézoomé avec plein de dalles autour, rien ne change. Je préférais presque l'effet arty bien zoomé : remets-le et clôture ce sujet. »
Décision : les cotes de remplissage de v140 à v144 (55 %, 67,5 %, 85 %…) sont ABANDONNÉES. Sous Ritournelle la Toile est faite de ses seules
paroles DÈS LA PREMIÈRE, vue entière : peu de dalles, de grandes coulées — le cadrage de la version E1 (commit c8f4571, la dernière avant v139).
Réécrit au niveau de cette décision ; l'original de v144 : sauvegardes/redteam_ritournelle-avant-v145.py.

Par le banc « comme Tom » (WebKit, 390 × 844 ×3, Toile vide, paroles plantées par le +). À 1, 2, 3, 4 et 6 paroles :
  A · la Toile n'a QUE ses paroles : autant de graines que de paroles, aucune cellule vide (`Toile.semisNeuf()` vrai) ;
  B · la vue est la Toile entière (zoom 1, aucun décalage) — aucun recadrage sur les dalles ;
  C · les graines sont celles d'E1, relevées sur le commit c8f4571 par le même chemin et portées EN DUR (± 3 pt : E1 lui-même varie d'un point
      d'une passe à l'autre, le relâchement ne converge pas au pixel) ;
  D · à partir de deux paroles, la matière couvre la zone visible (y 102 → 708) : de grandes formes, au moins 55 % de la zone hors du fond
      (lu sur la capture ; E1 : 72 à 100 %) ;
  E · toucher une dalle ouvre sa fiche (le correctif de v139 tient : l'heure des deux ÉVÉNEMENTS, pas celle du traitement).
⚠ CONSTAT, affiché et non jugé : À UNE SEULE PAROLE Ritournelle ne peint rien (une cellule couvre tout l'écran) — c'était déjà vrai en E1, c'est
  rendu tel quel, et c'est signalé à Tom (QUESTIONS, v145).
Avec `--ref=8761` (la version E1 servie sur ce port) : les graines sont AUSSI comparées à celles qu'E1 rend dans la même passe.
Rouge sur v144 (semis constant sous neuf paroles, vue cadrée sur la matière).     Usage : python3 redteam_ritournelle.py [fichier.html] [--ref=port] [--port=8752]
"""
import sys, io
sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
PORT, REF = arg('port', '8752'), arg('ref', '')
Y0, Y1 = 102, 708
TITRES = ['rendre le livre', 'écrire à Lou', 'arroser le ficus', 'courir dimanche', 'appeler mamie', 'finir la maquette']
# les graines d'E1 (commit c8f4571), relevées par ce même chemin le 13 oct. 2026 : x, y en points de la Toile (390 × 844)
E1 = {1: [(339, 143)], 2: [(339, 143), (51, 220)], 3: [(339, 143), (51, 145), (51, 600)], 4: [(339, 143), (51, 143), (51, 600), (339, 717)]}
TOL = 3
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
def passe(b, port, fichier, n_max=6):
    """plante de 1 à n_max paroles sous Ritournelle ; rend, par nombre de paroles : graines, vue, semis, capture"""
    ctx = B.contexte(b); pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%s/%s' % (port, fichier)); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{ Toile.setTheme('ritournelle'); }catch(e){} }"); pg.wait_for_timeout(1500); out = {}
    for i in range(n_max):
        B.plante(pg, TITRES[i]); pg.wait_for_timeout(5500)
        e = pg.evaluate("()=>{ var v=Toile.vue(); return {g:Toile_graines(), vue:[v.s,v.ox,v.oy], neuf:(Toile.semisNeuf?Toile.semisNeuf():null), n:promises.filter(p=>!p.draft).length}; }")
        e['im'] = B.image(pg); out[i + 1] = e
    return pg, ctx, out
def matiere(im):
    """la part de la zone visible qui n'est pas le fond de la Toile (la couleur la plus fréquente de la capture d'une Toile nue : #DFCAA4)"""
    px = im.load(); n = t = 0
    for y in range(Y0, Y1, 3):
        for x in range(0, 390, 3):
            c = px[x, y]; t += 1
            if abs(c[0] - 223) + abs(c[1] - 202) + abs(c[2] - 164) > 30: n += 1
    return n / float(t)
with sync_playwright() as p:
    b = p.webkit.launch()
    pg, ctx, R = passe(b, PORT, F)
    ref = None
    if REF:
        pr, cr, ref = passe(b, REF, 'app.html', 4); cr.close()
    for n in (1, 2, 3, 4, 6):
        e = R[n]; G = [(g[1], g[2]) for g in e['g']]; kinds = [g[3] for g in e['g']]
        juge('A · %d parole(s) : la Toile n\'a que ses paroles (autant de graines que de paroles, aucune cellule vide)' % n, e['n'] == n and len(G) == n and e['neuf'] is True and all(k != 'gray' for k in kinds), '%d graine(s) pour %d parole(s) · semis de la famille : %s' % (len(G), e['n'], e['neuf']))
        juge('B · %d parole(s) : la vue est la Toile entière (zoom 1, sans décalage)' % n, abs(e['vue'][0] - 1) < 0.01 and abs(e['vue'][1]) < 1 and abs(e['vue'][2]) < 1, 'vue %s' % [round(v, 2) for v in e['vue']])
        if n in E1:
            ec = max(max(abs(G[i][0] - E1[n][i][0]), abs(G[i][1] - E1[n][i][1])) for i in range(n)) if len(G) == n else 999
            juge('C · %d parole(s) : les graines sont celles d\'E1 (± %d pt)' % (n, TOL), ec <= TOL, 'graines %s · E1 %s · écart %s pt' % (G, E1[n], ec))
            if ref:
                Gr = [(g[1], g[2]) for g in ref[n]['g']]; ec2 = max(max(abs(G[i][0] - Gr[i][0]), abs(G[i][1] - Gr[i][1])) for i in range(n)) if len(G) == len(Gr) == n else 999
                juge('C bis · %d parole(s) : mêmes graines que la version E1 servie à côté, dans la même passe (± %d pt)' % (n, TOL), ec2 <= TOL, 'E1 servie %s · écart %s pt' % (Gr, ec2))
        m = matiere(e['im'])
        if n >= 2: juge('D · %d paroles : de grandes formes — la matière couvre au moins 55 %% de la zone visible' % n, m >= 0.55, '%.0f %% de la zone hors du fond' % (m * 100))
        else: print('··  CONSTAT (non jugé) · 1 parole : %.0f %% de la zone porte de la matière — comme en E1, Ritournelle ne peint rien à une seule parole' % (m * 100), flush=True)
    # E · toucher une dalle ouvre sa fiche : au point de la graine de chaque parole (hors du plateau et de la barre)
    ouvertes = 0; essais = 0
    for g in R[6]['g']:
        x, y = g[1], g[2]
        if not (120 < y < 690 and 12 < x < 378): continue
        essais += 1; pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500); B.tap(pg, x, y); pg.wait_for_timeout(1400)
        if pg.evaluate("()=>{ var d=document.getElementById('detailPoster'); return !!(d && d.classList.contains('show')); }"): ouvertes += 1
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }")
    juge('E · toucher une dalle ouvre sa fiche (au point de chaque graine visible)', essais >= 2 and ouvertes == essais, '%d fiche(s) ouverte(s) sur %d toucher(s)' % (ouvertes, essais))
    juge('aucune erreur de page', not pg.erreurs, str(pg.erreurs[:2]))
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:900])
sys.exit(0 if ok == len(res) else 1)
