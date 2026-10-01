# -*- coding: utf-8 -*-
"""Q30 BORNÉ — AUCUNE DALLE HORS BANDE HAUTE N'EST TEINTÉE.
   La comparaison pixel ne prouve rien ici : les dalles de la Toile sont ANIMÉES et tirées
   au hasard à chaque exécution. On instrumente donc la teinture elle-même — on note CHAQUE
   appel et l'écran qui était à l'affiche — puis on parcourt tout ce qui montre des dalles
   hors bande haute : Toile, Index, Fil, encart de Nuée, Partage, Aura, Studio."""
from playwright.sync_api import sync_playwright
R="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
OK=[]
def t(n,c,d=''): OK.append((n,'OK' if c else 'KO',d))

# 1 · contrôle STATIQUE : un seul site d'appel
import re, io
S=io.open(R+'/app.html',encoding='utf-8').read()
# le site d'appel passe par l'export, avec la locale en secours :
#   (window._ppTeinteDalle || teinteDalle)(src, e.nat)
sites=[m.start() for m in re.finditer(r'\(window\._ppTeinteDalle \|\| teinteDalle\)\(', S)]
defs =[m.start() for m in re.finditer(r'function teinteDalle\(', S)]
# tout autre appel direct « teinteDalle( » serait un second site — il n'en existe aucun
nus  =[m.start() for m in re.finditer(r'(?<![\w.])teinteDalle\(', S)]
nus  =[i for i in nus if i not in [d+len('function ') for d in defs]]
t('un seul site d\'appel dans tout le fichier', len(sites)==1 and len(nus)==0,
  '%d site via l\'export · %d appel nu · %d définition'%(len(sites), len(nus), len(defs)))

INSTR = r"""()=>{
  window.__teint=[];
  const vrai = window._ppTeinteDalle;
  window._ppTeinteDalle = function(src, nat){
    const cs=document.getElementById('createSheet');
    const dp=document.getElementById('detailPoster');
    window.__teint.push({
      pageplus: !!(cs && cs.classList.contains('pp') && cs.classList.contains('show')),
      fiche:    !!(dp && dp.classList.contains('show')),
      nat:nat});
    return vrai.apply(this, arguments);
  };
  return true;}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto('file://'+R+'/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    # la teinture doit être posée AVANT qu'on parcoure les écrans
    t('la teinture est instrumentable', pg.evaluate(INSTR))
    # 2 · on parcourt TOUT ce qui montre des dalles hors bande haute
    for vue in ('toile','index','fil'):
        pg.evaluate("(v)=>{ if(typeof setView==='function') setView(v); }", vue); pg.wait_for_timeout(2400)
    for scr in ('shareScreen','auraScreen','studioScreen','plusScreen','feedScreen'):
        pg.evaluate("(s)=>{var e=document.getElementById(s);if(e){e.classList.add('show');}}", scr); pg.wait_for_timeout(1200)
        pg.evaluate("(s)=>{var e=document.getElementById(s);if(e){e.classList.remove('show');}}", scr)
    pg.evaluate("()=>{ if(window.peintMinis) peintMinis(); if(window.buildIndex) buildIndex(); }")
    pg.wait_for_timeout(2000)
    hors = pg.evaluate("()=>window.__teint.filter(x=>!x.pageplus && !x.fiche).length")
    total_avant = pg.evaluate("()=>window.__teint.length")
    t('aucune teinture hors bande haute', hors==0,
      '%d appel(s) au total en parcourant Toile · Index · Fil · Partage · Aura · Studio, dont %d hors bande haute'%(total_avant,hors))
    # 3 · et elle marche bien DANS la bande haute
    pg.evaluate("()=>{ document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(1500)
    dedans = pg.evaluate("()=>window.__teint.filter(x=>x.pageplus).length")
    t('la teinture agit dans le champ de la page +', dedans>0, '%d appel(s)'%dedans)
    t('aucune erreur JS', not er, str(er[:2]))
    b.close()
for n,s,d in OK: print('%-46s %s  %s'%(n,s,d))
print('\n%d/%d'%(sum(1 for _,s,_ in OK if s=='OK'), len(OK)))
