#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captures SECTION 2 — les 7 cadres Peaufiner du moodboard, au défilement qui leur correspond.
   Les neuf cadres du moodboard sont QUATRE pages qui défilent : chaque « bas / suite » se
   retrouve en amenant son premier bloc à la cote que le cadre lui donne.
       promi_suite : COMMENTAIRES est à 592 dans la liste, à 46 dans le cadre → 546
       cercle      : le bloc est à 806, le cadre le pose à 130            → 676
       chiche_bas  : RELANCER est à 712, le cadre le pose à 46            → 666
       nuee_bas    : le bouton est à 538, le cadre le pose à 46           → 492
"""
import os
from playwright.sync_api import sync_playwright
R = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OUT = os.path.join(R, 'scratchpad/s2')
os.makedirs(OUT, exist_ok=True)

SCENE = r"""(nom)=>{
  function tr(pred){ for(var i=0;i<promises.length;i++){ var p=promises[i]; if(pred(p)) return p; } return null; }
  var p=null;
  if(nom==='promi'){ p=tr(function(q){return !q.draft && q.status==='encours';}); if(!p) return null;
    delete p.chiche; delete p.avec; p.who='Rachel'; p.from=null; }
  else if(nom==='chiche'){ p=tr(function(q){return !q.draft && q.status==='encours';}); if(!p) return null;
    p.chiche=true; p.who='Marion'; delete p.avec; delete p.nuee; p.from=null; }
  else if(nom==='nuee'){ var k=null; try{ for(var q in NUE){ k=q; break; } }catch(e){}
    if(!k) return null; openNueeDetail(k); return 'nuee'; }
  openDetail(p.id); return p.id;
}"""

CADRES = [('peauf_promi_haut', 'promi', 0), ('peauf_promi_suite', 'promi', 546),
          ('peauf_cercle', 'promi', 676),
          ('peauf_nuee_haut', 'nuee', 0), ('peauf_nuee_bas', 'nuee', 492),
          ('peauf_chiche_haut', 'chiche', 0), ('peauf_chiche_bas', 'chiche', 666)]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    er = []
    pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto('file://' + os.path.join(R, 'app.html')); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark', 'light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        courant = None
        for nom, scene, y in CADRES:
            if scene != courant:
                # on referme l'écran courant avant d'en ouvrir un autre : sans ça
                # openNueeDetail retombait sur la Toile (constaté en capture).
                pg.evaluate("()=>{ if(window._s2Ouvre) window._s2Ouvre(false);"
                            " var c=document.querySelector('#detailPoster>.closeb'); if(c) c.click(); }")
                pg.wait_for_timeout(700)
                if not pg.evaluate(SCENE, scene):
                    print('  ⚠ absent :', scene); continue
                pg.wait_for_timeout(1200)
                pg.evaluate("()=>{ if(window._s2Ouvre) window._s2Ouvre(true); }")
                pg.wait_for_timeout(700)
                courant = scene
            pg.evaluate("(y)=>{var c=document.getElementById('dpdCorps'); if(c) c.scrollTop=y;}", y)
            pg.wait_for_timeout(450)
            pg.query_selector('#device').screenshot(path=os.path.join(OUT, '%s_%s.png' % (nom, th)))
        print('  %s : %d cadres' % (th, len(CADRES)))
    if er:
        print('  ERREURS JS :', er[:3])
    b.close()
print('captures dans', OUT)
