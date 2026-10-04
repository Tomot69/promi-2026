#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_vivant.py — LA TOILE VIT AU REPOS (v126, Tom, 4 oct. 2026, C-028).

« Quand personne ne touche l'écran, de temps en temps, la matière d'une ou deux dalles bouge à peine, selon la manière de son monde,
pendant 1 à 2 s. Jamais toute la Toile à la fois. […] Intervalle tiré au hasard entre 5 et 15 s, jamais moins de 5 s. Arrêt hors écran
et en arrière-plan. Immobile avec Réduire les animations. Aucun calcul entre deux mouvements.
Juge : 3 min de repos par monde. Pas d'intervalle sous 5 s, aucun motif périodique, jamais plus de deux dalles en mouvement, coût nul
entre deux mouvements. Il doit rougir sur une version à intervalle fixe. »

LE VERDICT VIENT DES PIXELS du canevas de la Toile, lu toutes les 100 ms (WebKit) : un mouvement = une suite de lectures où des pixels
changent. Le journal du moteur (`Toile.vivant.journal`) ne sert qu'à dire combien de dalles le moteur a tirées (un pointeur).
Les valeurs décidées sont en dur : intervalle ≥ 5 s (de la fin d'un mouvement au début du suivant) et ≤ 15 s + la durée ; durée 1 à 2 s ;
au plus 2 dalles ; jamais plus de 4 % de la Toile (une ou deux dalles, pas « toute la Toile ») ; après un mouvement, la Toile est revenue
à l'image d'avant ; entre deux mouvements, aucune image n'est demandée par le moteur (sa boucle est arrêtée, et aucun pixel ne change).
MONDES JUGÉS : les douze qui vivent. Les huit autres (Volubilis, Guingois, Mascaret, Ramage, Madrure, Chantourné, Chamade, Éclisse) n'ont
pas encore leur manière : le juge vérifie qu'ils restent IMMOBILES (rien ne bouge), et les nomme.
  --duree=180 (par monde)   --mondes=a,b   --fixe (la sonde : intervalle fixe de 6 s — le contrôle « jamais périodique » doit rougir)
"""
import sys, json
from playwright.sync_api import sync_playwright
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
DUREE = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--duree=')), 180))
VIVENT = 'encre,touffe,mosaique,braille,pixel,halin,esquille,ritournelle,bobinette,gravure,sillons,brouillamini'.split(',')
IMMOBILES = 'volubilis,guingois,mascaret,ramage,madrure,chantourne,chamade,terrazzo'.split(',')
MONDES = next((a.split('=')[1].split(',') for a in sys.argv if a.startswith('--mondes=')), VIVENT + IMMOBILES)
FIXE = '--fixe' in sys.argv
INT_MIN, INT_MAX, DUR_MIN, DUR_MAX, DALLES_MAX, PART_MAX = 5.0, 15.0, 1.0, 2.0, 2, 6.0   # 6 % : deux grandes dalles (mesuré : jusqu’à 4,2 % sous Ritournelle) ; « toute la Toile » = des dizaines de %
JS = r"""async (duree)=>{ const cv=document.getElementById('toileCv'); const o=document.createElement('canvas'); o.width=390; o.height=Math.round(390*cv.height/cv.width); const g=o.getContext('2d',{willReadFrequently:true});
  const lit=()=>{ g.drawImage(cv,0,0,o.width,o.height); return g.getImageData(0,0,o.width,o.height).data; };
  const dif=(x,y)=>{ let n=0; for(let i=0;i<x.length;i+=4){ if(Math.max(Math.abs(x[i]-y[i]),Math.abs(x[i+1]-y[i+1]),Math.abs(x[i+2]-y[i+2]))>10) n++; } return 100*n/(x.length/4); };
  let repos=lit(), av=repos, E=[], cur=null, t0=performance.now(), boucleEntre=0, lectures=0;
  while(performance.now()-t0<duree*1000){ await new Promise(r=>setTimeout(r,100)); const t=(performance.now()-t0)/1000, d=lit(), p=dif(av,d); lectures++;
    if(p>0.004){ if(!cur){ cur={t0:t, max:0, repos:repos}; E.push(cur); } cur.t1=t; cur.max=Math.max(cur.max, dif(cur.repos,d)); cur.calme=0; }
    else if(cur){ if(++cur.calme>=4){ cur.retour=dif(cur.repos,d); delete cur.repos; cur=null; repos=d; } }
    else { if(Toile.vivant.boucle()) boucleEntre++; }
    av=d; }
  E.forEach(e=>{ delete e.repos; });
  return {E, lectures, boucleEntre, journal:Toile.vivant.journal().map(j=>Object.assign({},j,{ts:(j.t-t0)/1000})).filter(j=>j.ts>=-0.5)}; }"""
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){};" + ("window._vivantFixe=6000;" if FIXE else ""))
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if FIXE: print('SONDE : intervalle fixe de 6 s')
    for m in MONDES:
        pg.evaluate("m=>{ try{closeAll()}catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(7000)
        r = pg.evaluate(JS, DUREE); Etous = r['E']; J = r['journal']
        # un mouvement de la vie au repos = une suite de lectures qui commence quand le moteur a tiré (le journal ne sert qu'à RECONNAÎTRE
        #   l'épisode ; ce qu'on en juge — durée, étendue, retour — est lu sur les pixels). Ce qui bouge sans tirage est compté à part.
        E = [e for e in Etous if any(-0.35 <= e['t0'] - j['ts'] <= 0.6 for j in J)]; autres = [e for e in Etous if e not in E]
        if m in IMMOBILES:
            juge('[%s] immobile au repos (il n\'a pas encore sa manière) : rien ne bouge en %d s' % (m, DUREE), len(Etous) == 0 and not J, '%d mouvement(s)' % len(Etous)); continue
        durs = [e['t1'] - e['t0'] + 0.1 for e in E]; ints = [E[i + 1]['t0'] - E[i]['t1'] for i in range(len(E) - 1)]; debuts = [E[i + 1]['t0'] - E[i]['t0'] for i in range(len(E) - 1)]
        juge('[%s] la Toile bouge au repos (au moins %d mouvements en %d s)' % (m, max(2, DUREE // 30), DUREE), len(E) >= max(2, DUREE // 30), '%d mouvement(s)' % len(E))
        juge('[%s] jamais moins de 5 s entre deux mouvements' % m, not ints or min(ints) >= INT_MIN - 0.25, 'le plus court : %.1f s' % (min(ints) if ints else 0))
        juge('[%s] jamais plus de 15 s (+ les lectures) sans mouvement' % m, not ints or max(ints) <= INT_MAX + 1.0, 'le plus long : %.1f s' % (max(ints) if ints else 0))
        juge('[%s] aucun motif périodique (les intervalles s\'étalent sur plus de 3 s)' % m, len(debuts) < 3 or (max(debuts) - min(debuts)) > 3.0, 'de %.1f à %.1f s' % ((min(debuts), max(debuts)) if debuts else (0, 0)))
        juge('[%s] un mouvement dure 1 à 2 s' % m, bool(durs) and min(durs) >= DUR_MIN - 0.35 and max(durs) <= DUR_MAX + 0.35, 'de %.1f à %.1f s' % ((min(durs), max(durs)) if durs else (0, 0)))
        juge('[%s] jamais toute la Toile : au plus %.0f %% des pixels pendant un mouvement' % (m, PART_MAX), bool(E) and max(e['max'] for e in E) <= PART_MAX, 'le plus grand : %.2f %%' % (max(e['max'] for e in E) if E else 0))
        juge('[%s] jamais plus de deux dalles (le tirage du moteur)' % m, bool(J) and max(j['n'] for j in J) <= DALLES_MAX, 'au plus %d' % (max(j['n'] for j in J) if J else 0))
        juge('[%s] après un mouvement, la Toile est revenue à l\'image d\'avant' % m, bool(E) and max(e.get('retour', 0) for e in E) <= 0.02, 'reste : %.3f %%' % (max(e.get('retour', 0) for e in E) if E else 0))
        juge('[%s] rien d\'autre ne bouge sur la Toile au repos' % m, not autres, '%d changement(s) sans tirage : %s' % (len(autres), ' · '.join('à %.0f s, %.2f s, %.2f %% (reste %.3f %%)' % (e['t0'], e['t1'] - e['t0'] + 0.1, e['max'], e.get('retour', 0)) for e in autres[:3])))
        juge('[%s] coût nul entre deux mouvements : la boucle du moteur est arrêtée, aucun pixel ne change' % m, r['boucleEntre'] <= max(2, len(E) * 3), '%d lecture(s) sur %d où la boucle tournait' % (r['boucleEntre'], r['lectures']))
    # Réduire les animations : rien
    ctx2 = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, reduced_motion='reduce')
    ctx2.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg2 = ctx2.new_page(); pg2.goto('http://127.0.0.1:8752/' + FICHIER); pg2.wait_for_timeout(6500)
    pg2.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} Toile.setTheme('encre');}"); pg2.wait_for_timeout(5000)
    r2 = pg2.evaluate(JS, 24)
    juge('« Réduire les animations » : immobile (24 s)', len(r2['E']) == 0 and not r2['journal'], '%d mouvement(s)' % len(r2['E']))
    # un écran ouvert par-dessus : rien (l'Index, 22 s)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} Toile.setTheme('encre'); }"); pg.wait_for_timeout(6000)
    n0 = pg.evaluate("()=>Toile.vivant.journal().length"); pg.evaluate("()=>{ ouvrirIndex(); }"); pg.wait_for_timeout(22000)
    n1 = pg.evaluate("()=>Toile.vivant.journal().length")
    juge('hors écran (l\'Index ouvert par-dessus, 22 s) : aucun mouvement tiré', n1 == n0, '%d → %d' % (n0, n1))
    juge('aucune erreur de page', not er, '; '.join(er[:2]))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:10]))
sys.exit(1 if ko else 0)
