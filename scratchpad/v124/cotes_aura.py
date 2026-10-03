# les cotes de la colonne de l'Aura, en points 390 × 844 (appareil), sombre, Aura PLEINE (le jeu de démonstration) et Aura VIDE
import sys, json, io
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
URL=sys.argv[1]; TAG=sys.argv[2]
Q="""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, sc=document.getElementById('auraScreen'); const o={};
  function r(nom,e){ if(!e) return; const b=e.getBoundingClientRect(); if(!b.height) return; o[nom]=[+((b.top-dv.top)/k).toFixed(2), +((b.bottom-dv.top)/k).toFixed(2)]; }
  r('plateau', sc.querySelector('.enh')||sc.querySelector('.au-plat')); { const c=document.getElementById('auBoule').getBoundingClientRect(); const cy=(c.top+c.height/2-dv.top)/k; o['silhouette (rayon 121)']=[+(cy-121).toFixed(2), +(cy+121).toFixed(2)]; } r('halo (canevas)', document.getElementById('auPeloteHalo')); r('ombre', document.getElementById('auPeloteOmbre')); r('flaque', document.getElementById('auPeloteFlaque'));
  const C=sc.querySelector('.au-cad')||sc;
  [['« Partager ma Pelote »','.au-bt'],['la phrase','.au-mot'],['les Noyaux','.au-nx'],['la légende','.au-lg'],['les chiffres','.au-cpt'],['ce que tu as tenu','.au-mo'],['ce qu’on t’a tenu','.au-mo2'],['l’invite (Aura vide)','.au-inv'],['la fin','.au-fin']].forEach(a=>r(a[0], sc.querySelector(a[1])));
  return o; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(7000); RR={}
    for th in (0,1):
        ouvre(pg,th); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{const s=document.getElementById('auraScreen'); s.scrollTop=0;}"); pg.wait_for_timeout(600)
        R=pg.evaluate(Q); RR['sombre' if th else 'clair']=R; print('sombre' if th else 'clair', json.dumps(R,ensure_ascii=False))
        pg.screenshot(path='scratchpad/v124/aura-%s-%s.png'%(TAG,'sombre' if th else 'clair'), clip={'x':20,'y':44,'width':390,'height':844})
    json.dump(RR,open('scratchpad/v124/cotes-%s.json'%TAG,'w'),ensure_ascii=False)
    b.close()
