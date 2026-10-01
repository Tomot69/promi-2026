#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES PLANCHES DU LOT PALETTE — Index, Aura, Fil, fiches × 2 thèmes, AVANT et APRÈS.
   Deux fichiers servis par le même serveur : app.html (avant) et app-palette.html (après)."""
import os, sys
from playwright.sync_api import sync_playwright
R = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OUT = os.path.join(R, 'planche-identite'); os.makedirs(OUT, exist_ok=True)

OUVRE_FICHE = r"""(nom)=>{
  function tr(f){ try{ return promises.filter(function(p){return !p.draft;}).find(f); }catch(e){ return null; } }
  var p=null;
  if(nom==='promi'){ p=tr(function(q){return q.status==='encours';}); if(!p) return null;
    delete p.chiche; delete p.avec; p.who='Rachel'; p.from=null; }
  else if(nom==='chiche'){ p=tr(function(q){return q.status==='encours';}); if(!p) return null;
    p.chiche=true; p.who='Marion'; delete p.avec; delete p.nuee; p.from=null; }
  else if(nom==='tenu'){ p=tr(function(q){return q.status==='tenu';}) || tr(function(q){return true;}); if(!p) return null;
    p.status='tenu'; delete p.chiche; }
  else if(nom==='nuee'){ var k=null; try{ for(var q in NUE){ k=q; break; } }catch(e){}
    if(!k) return null; openNueeDetail(k); return 'nuee'; }
  openDetail(p.id); return p.id; }"""

def serie(pg, tag):
    er = []
    pg.on('pageerror', lambda x: er.append(str(x)))
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{if(window.closeAll)closeAll();if(window.setView)setView('toile');}"); pg.wait_for_timeout(700)
        pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_accueil_{th}.png")
        # INDEX
        pg.evaluate("()=>{window._s4Trois=false;if(window.setView)setView('toile');window.ouvrirIndex();}"); pg.wait_for_timeout(1500)
        pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_index_{th}.png")
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
        # FIL
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1500)
        pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_fil_{th}.png")
        pg.evaluate("()=>{setView('toile');if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
        # AURA
        pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(2600)
        pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_aura_{th}.png")
        # ⚠ closeAll ne ferme que .sheet et .poster : l'Aura est un .screen, elle restait
        #   ouverte par-dessus le Fil suivant (la planche « fil » montrait l'Aura).
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();}")
        pg.wait_for_timeout(600)
        # FICHES
        for nom in ('promi','chiche','nuee','tenu'):
            pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(350)
            r = pg.evaluate(OUVRE_FICHE, nom)
            pg.wait_for_timeout(1700)
            if r: pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_fiche-{nom}_{th}.png")
            else: print(f"   (pas de fiche {nom})")
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
        # STUDIO — les vingt palettes
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();document.getElementById('studioBtn').click();}")
        pg.wait_for_timeout(2200)
        pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_studio_{th}.png")
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();}")
        pg.wait_for_timeout(600)
        # LE CERCLE — l'écran qui vend
        pg.evaluate("()=>{document.getElementById('plusScreen').classList.add('show');try{if(window._pcPeint)_pcPeint();}catch(e){}}")
        pg.wait_for_timeout(2200)
        pg.query_selector('#device').screenshot(path=f"{OUT}/{tag}_cercle_{th}.png")
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(e=>e.classList.remove('show'));if(window.closeAll)closeAll();}")
        pg.wait_for_timeout(500)
    return er

with sync_playwright() as p:
    b = p.chromium.launch()
    for tag, url in (('avant','app.html'), ('apres','app-identite.html')):
        pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/'+url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.wait_for_timeout(500)
        er = serie(pg, tag)
        print(f"{tag} : {len([f for f in os.listdir(OUT) if f.startswith(tag)])} vues · erreurs JS : {er[:3]}")
        pg.close()
    b.close()
print("planches dans", OUT)
