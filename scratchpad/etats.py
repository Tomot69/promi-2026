# -*- coding: utf-8 -*-
"""LES ÉLÉMENTS D'ÉTAT, ÉCRAN PAR ÉCRAN, DANS LES DEUX THÈMES — et ce qu'ils portent.
   Les valeurs justes (v7/v8) :
     à tenir  #DD4D23 partout
     en cours #291547 sur fond clair · #A77CF7 sur fond sombre
     tenu     #00341A sur fond clair · #33BA6C sur fond sombre
   L'amande #8FE08F n'est PLUS une valeur d'état : elle est réservée à la célébration."""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
JUSTES={'#DD4D23','#291547','#A77CF7','#00341A','#33BA6C'}
VIEILLES={'#8FE08F':"l'amande (réservée à la célébration)", '#2BE88C':'la menthe d\'avant le 16 sept.',
          '#8FA0FF':'le périwinkle', '#FFD447':'le jaune', '#F07A2E':"l'orange d'origine"}
def hx(c):
    try:
        v=[int(x) for x in c.replace('rgba(','').replace('rgb(','').replace(')','').split(',')[:3]]
        return '#%02X%02X%02X'%tuple(v)
    except Exception: return c
JS=r"""()=>{var out=[];
 function pousse(zone, sel, prop){
   document.querySelectorAll(sel).forEach(function(e){
     var r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return;
     var cs=getComputedStyle(e);
     var v = prop==='bg'?cs.backgroundColor : (prop==='stroke'? (e.getAttribute('stroke')||cs.stroke) : cs.color);
     if(!v||v==='rgba(0, 0, 0, 0)'||v==='none') return;
     out.push([zone,(e.textContent||'').trim().slice(0,22)||sel,v]);});
 }
 pousse('Aura · légende','#auraScreen .au-lg i','bg');
 pousse('Aura · arcs','#auraScreen .au-nb path','stroke');
 pousse('Aura · aide','.ah-legend i','bg');
 pousse('Index · état','#indexSheet .s4-et','col');
 pousse('Fil · état','#feedView .s4-et','col');
 pousse('accueil · anneau','#device .acc-barre #createBtn','bg');
 pousse('fiche · état','#detailPoster .dpt-quand','col');
 pousse('fiche personne','#psCadre .ps-lg i','bg');
 return out;}"""
ECR=[('accueil',''),('aura',"document.getElementById('souffleBtn').click()"),
     ('index',"document.getElementById('indexBtn').click()"),('fil',"document.getElementById('filBtn').click()"),
     ('aide de l’Aura',"document.getElementById('souffleBtn').click();setTimeout(function(){var b=document.getElementById('auraInfoBtn');b&&b.click();},800)"),
     ('fiche personne',"openPerson('Adrien')")]
mauvais=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    for theme in ('sombre','clair'):
        vu=set()
        print('══ %s ══'%theme)
        for nom,js in ECR:
            pg.goto(URL); pg.wait_for_timeout(6100)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>{setTheme(t==='clair'?'light':'dark');}",theme); pg.wait_for_timeout(500)
            if js:
                try: pg.evaluate("()=>{%s}"%js)
                except Exception: pass
                pg.wait_for_timeout(2600)
            for z,t,v in pg.evaluate(JS):
                h=hx(v); k=(z,t,h)
                if k in vu: continue
                vu.add(k)
                mal = h in VIEILLES
                if mal: mauvais.append((theme,z,t,h))
                print('   %-18s %-24s %-9s %s'%(z,t,h,('✗ '+VIEILLES[h]) if mal else ('' if h in JUSTES else '(hors table)')))
        print()
    b.close()
print('%d élément(s) d\'état aux anciennes valeurs.'%len(mauvais))
for m in mauvais: print('   ', m)
