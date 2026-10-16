#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_trait.py — VALIDER UN TRAIT : AU MOINS 60 pt (v143, Tom, 12 oct. 2026 — C-107).

« Un trait (planter comme tenir) ne compte que si le doigt a avancé d'au moins 60 pt le long du trait. En dessous, c'est un faux contact : le
trait revient à son état d'avant (la moitié plantée reste, rien n'est validé). Un geste court et rapide de plus de 60 pt reste accepté. »

Comme Tom (banc_tom : WebKit, 390 × 844 ×3, doigt, Toile vide, paroles plantées par l'app, fiche ouverte en touchant la dalle). 60 EN DUR.
  TENIR  (sur la fiche)  : 30 pt → refusé, la parole n'est pas tenue, le trait est revenu ; un doigt POSÉ 1,2 s sans avancer → refusé ;
                           70 pt lent (1 s) → tenue ; 70 pt rapide (0,12 s) → tenue ;
  PLANTER (sur la page +) : 30 pt → rien n'est planté, la page + reste ; 70 pt lent → planté ; 70 pt rapide → planté ;
  la règle déclarée vaut 60 ; la main fantôme montre un geste de plus de 60 pt.
Le verdict se lit sur l'ÉTAT RÉEL (le statut de la parole, le nombre de paroles), jamais sur ce que le geste déclare.
Preuve : rouge sur v142 (python3 redteam_trait.py zz-av143.html).
"""
import sys
sys.path.insert(0, '.')
from banc_tom import *
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:260]), flush=True)
OU = open('redteam_deplace.py', encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
ZONE = "(id)=>{ const c=document.getElementById(id); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }"
ST = "()=>({n:promises.length, statuts:promises.map(p=>p.status), fiche:document.getElementById('detailPoster').classList.contains('show'), cs:document.getElementById('createSheet').classList.contains('show'), tr:document.getElementById('detailPoster').classList.contains('tracant'), d:window._traitDernier||null, regle:(window._traitRegle||{}).MIN})"
def ouvre_fiche(pg, pid):
    pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(700)
    G = pg.evaluate(OU)
    if str(pid) not in G: return False
    tap(pg, G[str(pid)][0], G[str(pid)][1]); pg.wait_for_timeout(1800); return pg.evaluate(ST)['fiche']
def trait(pg, zid, x0, dx, pas):
    z = pg.evaluate(ZONE, zid)
    if not z: return None
    y = z[1] + z[3] * 0.45; n = 10
    return glisse(pg, [[x0 + dx * i / n, y] for i in range(n + 1)], pas=pas, tenue=380 if zid == 'tenirZone' else 0)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = contexte(b); pg = ouvre(ctx, F)
    # ── PLANTER ──
    def page_plus(titre):
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("a=>{document.getElementById('fTitle').value=a;document.getElementById('fWho').value='moi';window._csEnLair=true;window._csDueISO=null; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} }", titre); pg.wait_for_timeout(400)
    page_plus('rendre le livre'); n0 = pg.evaluate(ST)['n']
    trait(pg, 'planterZone', 40, 30, 30); pg.wait_for_timeout(1500); s = pg.evaluate(ST)
    juge('PLANTER · 30 pt : rien n\'est planté, la page + reste ouverte', s['n'] == n0 and s['cs'], 'paroles %d → %d · page + %s · geste %s' % (n0, s['n'], s['cs'], s['d']))
    trait(pg, 'planterZone', 40, 70, 100); pg.wait_for_timeout(3200); s = pg.evaluate(ST)
    juge('PLANTER · 70 pt lent (1 s) : la parole est plantée', s['n'] == n0 + 1, 'paroles %d → %d · geste %s' % (n0, s['n'], s['d']))
    page_plus('écrire à Lou'); n1 = pg.evaluate(ST)['n']
    trait(pg, 'planterZone', 40, 70, 12); pg.wait_for_timeout(3200); s = pg.evaluate(ST)
    juge('PLANTER · 70 pt rapide (0,12 s) : la parole est plantée', s['n'] == n1 + 1, 'paroles %d → %d · geste %s' % (n1, s['n'], s['d']))
    plante(pg, 'réparer le vélo'); pg.wait_for_timeout(800)
    ids = pg.evaluate("()=>promises.map(p=>p.id)")
    # ── TENIR ──
    ok = ouvre_fiche(pg, ids[0])
    juge('TENIR · la fiche de la première parole s\'ouvre en touchant sa dalle', ok)
    trait(pg, 'tenirZone', 200, 30, 30); pg.wait_for_timeout(1500); s = pg.evaluate(ST)
    juge('TENIR · 30 pt : la parole n\'est pas tenue, le trait est revenu à son état d\'avant', s['statuts'][0] != 'tenu' and not s['tr'], 'statut %s · en tracé %s · geste %s' % (s['statuts'][0], s['tr'], s['d']))
    z = pg.evaluate(ZONE, 'tenirZone'); y = z[1] + z[3] * 0.45
    glisse(pg, [[200 + (i % 2) * 2, y] for i in range(16)], pas=75, tenue=300); pg.wait_for_timeout(1500); s = pg.evaluate(ST)
    juge('TENIR · un doigt posé 1,5 s sans avancer (2 pt de jeu) : la parole n\'est pas tenue', s['statuts'][0] != 'tenu', 'statut %s · geste %s' % (s['statuts'][0], s['d']))
    trait(pg, 'tenirZone', 200, 70, 100); pg.wait_for_timeout(3500); s = pg.evaluate(ST)
    juge('TENIR · 70 pt lent (1 s) : la parole est tenue', s['statuts'][0] == 'tenu', 'statut %s · geste %s' % (s['statuts'][0], s['d']))
    ok = ouvre_fiche(pg, ids[1])
    trait(pg, 'tenirZone', 200, 70, 12); pg.wait_for_timeout(3500); s = pg.evaluate(ST)
    juge('TENIR · 70 pt rapide (0,12 s) : la parole est tenue', ok and s['statuts'][1] == 'tenu', 'fiche %s · statut %s · geste %s' % (ok, s['statuts'][1], s['d']))
    juge('la règle déclarée vaut 60 pt', s['regle'] == 60, s['regle'])
    # ── la main fantôme montre un geste de plus de 60 pt ──
    ctx2 = contexte(b, gestes_vus=False); pg2 = ouvre(ctx2, F); plante(pg2, 'arroser le figuier'); pg2.wait_for_timeout(800)
    G = pg2.evaluate(OU); a = list(G)[0]; tap(pg2, G[a][0], G[a][1])
    L = []
    for i in range(80):   # v144 (C-110) : la main ne paraît plus qu'à 3 s — on la suit jusqu'à 9,6 s
        pg2.wait_for_timeout(120)
        v = pg2.evaluate("()=>{ const g=document.getElementById('gesteFantome'); if(!g||!g.children.length) return null; const m=g.querySelector('svg > g')||g.firstElementChild;   /* la main est le groupe déplacé dans le calque */ const r=m.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(); return (r.left+r.width/2-d.left)/(d.width/390); }")
        if v is not None: L.append(v)
    juge('la main fantôme paraît sur la fiche à tenir, et son geste couvre plus de 60 pt', len(L) >= 5 and max(L) - min(L) > 60, '%d relevés · de x %.0f à x %.0f' % (len(L), min(L) if L else 0, max(L) if L else 0))
    juge('aucune erreur de page', not pg.__dict__['erreurs'] and not pg2.__dict__['erreurs'], (pg.__dict__['erreurs'] + pg2.__dict__['erreurs'])[:2])
    ctx.close(); ctx2.close(); b.close()
n = sum(1 for _, c in res if c); print('\n%d/%d' % (n, len(res)))
if n < len(res): sys.exit(1)
