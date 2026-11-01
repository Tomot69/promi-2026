#!/usr/bin/env python3
"""redteam_prix.py — ⚑ v174 (Tom, 31 oct. 2026, C-216) : LE PRIX SANS TIRET.

« “Adopte ce design - 2 €” peut se lire “moins 2 €”. Nouveau libellé : “Adopte ce design pour 4 €” / “… pour 6 €”. 4 € pour Houle, Taille-douce et Éclisse ; 6 € pour les autres
mondes payants. » Le juge traverse le Studio au doigt : les douze mondes payants, le libellé lu à l'écran, le prix en dur ; le bouton d'achat dans l'appareil, le texte sur une
ligne ; aucun tiret ni « 2 € » nulle part dans ce qui s'affiche. Rouge sur v173.
"""
import sys, re, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
QUATRE = {'sillons', 'gravure', 'terrazzo'}
PAYANTS = 12
res = []
def juge(n, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', n, str(d)[:200]), flush=True)
with sync_playwright() as p:
    b = p.webkit.launch(); print('fichier :', F, '· charge %.1f' % B.charge())
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F); pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2600); vus = {}
        for i in range(24):
            q = pg.evaluate("()=>{ const s=document.getElementById('studioScreen'); if(!s.classList.contains('world-locked')) return null; const b=document.getElementById('stLockBuy').getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), t=document.getElementById('stBuyTx'), r=document.createRange(); r.selectNodeContents(t); return {w:window._lockedWorld, tx:t.textContent, lignes:new Set([...r.getClientRects()].map(q=>Math.round(q.top))).size, dans:b.left>=D.left&&b.right<=D.right}; }")
            if q and q['w'] not in vus: vus[q['w']] = q
            if len(vus) >= PAYANTS: break
            B.glisse(pg, B.droite([300, 330], [80, 330], 10), pas=18); pg.wait_for_timeout(1300)
        faux = {w: q['tx'] for w, q in vus.items() if q['tx'].replace(' ', ' ') != 'Adopte ce design pour %d €' % (4 if w in QUATRE else 6) or q['lignes'] != 1 or not q['dans']}
        juge('[%s] les douze mondes payants : « Adopte ce design pour 4 € » (Houle, Taille-douce, Éclisse) ou « … pour 6 € », sur une ligne' % nom, len(vus) == PAYANTS and not faux, '%d vus · %s' % (len(vus), faux or {w: q['tx'][-5:] for w, q in list(vus.items())[:4]}))
        ctx.close()
    b.close()
S = io.open(F, encoding='utf-8').read(); C = re.sub(r'/\*.*?\*/', '', S, flags=re.S)
juge('source : plus aucun « — 2 € » hors commentaires, le tarif en une seule table', not re.search(r'[—–-]\s*2(\s|&nbsp;|\\u00a0)€', C) and C.count('_prixDesign=') == 1)
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
