#!/usr/bin/env python3
"""
redteam_titres_cartes.py — v149 (C-151) : sur les cartes de l'Index, un titre de deux lignes était ROGNÉ par la ligne d'état (« planter un / arbre »,
« le grand plongeoir » : 48 pt de texte pour 20 à 45 pt de place). Règle (CLAUDE.md, la carte d'Index) : « le titre ne touche jamais l'état » et un texte ne
sort pas de sa boîte — un titre trop long RÉTRÉCIT jusqu'à tenir (plancher 11 px, §6) ; un titre qui tient garde la taille décidée (24 px, l'échelle des
titres de carte). Lu au rendu (WebKit, 390 × 844), deux thèmes : chaque titre tient dans sa boîte, le bas de ses lignes reste au-dessus du mot d'état, et
aucun titre qui tenait à 24 px n'a été rétréci. `--page=` : une autre page servie (rouge sur v148 : zz-av148.html).
"""
import sys
from playwright.sync_api import sync_playwright
PAGE = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
DECIDE = 24.0      # px — `#device .s4-ti{font-size:24px!important}` (les titres de carte, d'Index et du Fil), en dur
ok = [0]; ko = []
def t(nom, cond, detail=''):
    if cond: ok[0] += 1
    else: ko.append(nom)
    print('  %s %-92s %s' % ('✅' if cond else '❌', nom, detail), flush=True)
J = """()=>[...document.querySelectorAll('#indexList .s4-carte')].map(c=>{ const t=c.querySelector('.s4-ti'), e=c.querySelector('.s4-et'); if(!t) return null;
  const R=document.createRange(), k=(t.getBoundingClientRect().width/(t.offsetWidth||1))||1;
  const mes=()=>{ R.selectNodeContents(t); const tr=R.getBoundingClientRect(), b=e?e.getBoundingClientRect():null; return {sh:t.scrollHeight, ch:t.clientHeight, bas:tr.bottom, etat:b?b.top:null}; };
  const deborde=m=>m.sh>m.ch+1 || (m.etat!=null && m.bas>m.etat-2*k);
  const fs=parseFloat(getComputedStyle(t).fontSize), m=mes();
  /* un point plus grand (dans la même tâche, puis rendu tel quel) : le rétrécissement était-il nécessaire ? */
  let plus=null; if(fs<24-0.01){ const av=t.style.getPropertyValue('font-size'), pr=t.style.getPropertyPriority('font-size'); t.style.setProperty('font-size',(fs+1)+'px','important'); plus=deborde(mes()); t.style.setProperty('font-size',av,pr); }
  return {t:t.textContent, fs:fs, sh:m.sh, ch:m.ch, bas:m.bas, etat:m.etat, plusDeborde:plus}; }).filter(Boolean)"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        T = 'clair' if th == 'light' else 'sombre'
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
        pg.add_init_script("localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_theme','%s')" % th)
        pg.goto('http://127.0.0.1:8752/' + PAGE); pg.wait_for_timeout(6000)
        pg.evaluate("()=>{ closeAll(); setView('toile'); ouvrirIndex(); }"); pg.wait_for_timeout(4500)
        L = pg.evaluate(J)
        t('[%s] l\'Index montre des cartes' % T, len(L) >= 8, '%d cartes' % len(L))
        rog = [(x['t'], x['sh'], x['ch']) for x in L if x['sh'] > x['ch'] + 1]
        t('[%s] aucun titre ne sort de sa boîte (rogné)' % T, not rog, rog[:4])
        tou = [(x['t'], round(x['bas'], 1), round(x['etat'], 1)) for x in L if x['etat'] is not None and x['bas'] > x['etat'] - 1]
        t('[%s] le bas des lignes d\'un titre reste au-dessus du mot d\'état' % T, not tou, tou[:4])
        ret = [(x['t'], x['fs']) for x in L if x['fs'] < DECIDE - 0.01 and not x['plusDeborde']]
        gro = [(x['t'], x['fs']) for x in L if x['fs'] > DECIDE + 0.01]
        t('[%s] un titre n\'est rétréci que s\'il le faut (un point plus grand, il déborderait ou toucherait l\'état) ; jamais au-dessus de %d px' % (T, DECIDE), not ret and not gro, (ret + gro)[:4])
        pti = [(x['t'], x['fs']) for x in L if x['fs'] < 11 - 0.01]
        t('[%s] aucun titre sous le plancher de 11 px (§6)' % T, not pti, pti[:4])
        pg.close()
    b.close()
print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
sys.exit(1 if ko else 0)
