#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_onboarding.py — REMPLACÉ PAR redteam_e2.py (v140, Tom, 10 oct. 2026, C-075).

⚑ CONTRAT REMPLACÉ (original : sauvegardes/redteam_onboarding-avant-v140.py, 42 contrôles de l'onboarding de v20 à v129 : le prénom, « la parole
et le trait » dans un écran propre à l'onboarding, la plantation simulée, le message de fin « Primo… Deuxio… Tertio… »).
La décision qui le remplace : ENGAGEMENT.md, E2 — « Remplacer le tutoriel par une boucle complète vécue une fois : écrire → planter → faire →
tracer → sentir » — et le lot v140 §8 (« applique E2 et E2bis »). L'onboarding est maintenant : le prénom (gardé), le principe, la VRAIE page +,
la fiche, la dernière ligne, le compte. Ce que l'ancien juge protégeait et qui vaut encore est porté par redteam_e2 (le prénom et sa sortie,
la plantation, le verrou, le compte) et par redteam_verrou_onboarding. Ce fichier passe la main, pour que les séries qui l'appellent
jugent le parcours d'aujourd'hui.
"""
import sys, subprocess
# les aides que d'autres juges importent (redteam_engagement, redteam_verrou_onboarding) : gardées telles quelles
PRENOM, PAROLE = 'Camille', 'marcher une heure'
VIS = r"""(e)=>{ if(!e) return false; const c=getComputedStyle(e);
  if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false;
  const r=e.getBoundingClientRect(); const D=document.getElementById('device').getBoundingClientRect();
  if(r.width<2||r.height<2) return false;
  if(r.right<D.left+1||r.left>D.right-1||r.bottom<D.top+1||r.top>D.bottom-1) return false;
  let p=e; while(p&&p!==document.body){ const s=getComputedStyle(p); if(+s.opacity<0.05||s.display==='none') return false; p=p.parentElement; }
  return true; }"""
POIGNEE = r"""(q)=>{ const vis=%s; const e=document.querySelector('#promiOnb '+q); if(!vis(e)) return null;
  const r=e.getBoundingClientRect(); const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  return {x:r.left+r.width/2, y:r.top+r.height/2, l:r.left, t:r.top, w:r.width/k, h:r.height/k, k:k,
          dep:e.getAttribute('data-depart'), arr:e.getAttribute('data-arrivee'), tag:e.tagName}; }""" % VIS
def toucher(cdp, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})

def tracer(cdp, z, jusqua=1.0):
    """Un trait AU DOIGT, horodaté par le CDP (§8 : l'instrument ne ralentit pas avec la page),
    en courbe quadratique de départ à arrivée — la demi-courbe que la zone montre."""
    def pt(s):
        a, b = [float(v) for v in s.split(',')]
        return z['l'] + a * z['k'], z['t'] + b * z['k']
    (x0, y0), (x1, y1) = pt(z['dep']), pt(z['arr'])
    cx, cy = (x0 + x1) / 2, min(y0, y1) - 18 * z['k']
    t0 = time.time()
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}], 'timestamp': t0})
    N = 24
    for i in range(1, int(N * jusqua) + 1):
        u = i / N
        x = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1
        y = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x, 'y': y}], 'timestamp': t0 + 0.03 * i})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': t0 + 0.03 * (N + 1)})

if __name__ == '__main__':
    sys.exit(subprocess.call([sys.executable, 'redteam_e2.py'] + sys.argv[1:]))
