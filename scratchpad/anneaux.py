# -*- coding: utf-8 -*-
"""LES ANNEAUX DES NOYAUX — combien d'arcs, sur quelle donnée, et de quelle couleur RENDUE.
   La règle (Tom, 22 sept.) : un anneau ne peut avoir que TROIS arcs — à tenir, en cours, tenu."""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
JS=r"""()=>{var out=[];
 document.querySelectorAll('#auraScreen .au-ny,#auraScreen .au-nb').forEach(function(w){
   var box=w.closest('[class*=ny]')||w;
   var nom=(box.parentElement&&box.parentElement.querySelector('.au-lb'))?box.parentElement.querySelector('.au-lb').textContent.trim():
           ((w.parentElement&&w.parentElement.querySelector('.au-lb'))?w.parentElement.querySelector('.au-lb').textContent.trim():'?');
   var arcs=[].map.call(w.querySelectorAll('path.au-arc'),function(p){
     var cs=getComputedStyle(p); var g=p.closest('.au-recu');
     var op=1; var e=p; while(e&&e!==document.body){ var o=parseFloat(getComputedStyle(e).opacity); if(!isNaN(o)) op*=o; e=e.parentElement; }
     return {c:p.getAttribute('stroke'), moitie:g?'reçu (droite)':'tenu par toi (gauche)', op:+op.toFixed(2), z:p.getAttribute('data-z')};});
   if(arcs.length) out.push({qui:nom, n:arcs.length, arcs:arcs});});
 return out;}"""
DONNEES = r"""()=>{try{ return (window._auraComp||{}).gens ? 'gens publié' : Object.keys(window._auraComp||{}).join(','); }catch(e){ return String(e); }}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    for theme in ('sombre','clair'):
        pg.goto(URL); pg.wait_for_timeout(6200)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", 'light' if theme=='clair' else 'dark'); pg.wait_for_timeout(500)
        pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(3600)
        print('══ %s ══'%theme)
        for o in pg.evaluate(JS):
            drapeau = 'OK ' if o['n']<=3 else '✗ %d ARCS'%o['n']
            print('   %-10s %d arc(s)  %s'%(o['qui'],o['n'],drapeau))
            for a in o['arcs']:
                print('        %-24s %-9s opacité %.2f  →  rendu %s'%(a['moitie'],a['c'],a['op'],
                      a['c'] if a['op']>=0.999 else '(délavé par l\'opacité)'))
        print()
    print('la donnée :', pg.evaluate(DONNEES))
    b.close()
