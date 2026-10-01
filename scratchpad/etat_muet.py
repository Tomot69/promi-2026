#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ÉTAT SE LIT-IL ENCORE ? Le mot est passé à l'encre : la couleur d'état ne vit plus que dans
   le TRAIT. On compte, sur l'image rendue, les pixels que la couleur d'état occupe encore, et on
   mesure son écart au fond qu'elle traverse. Une fiche est MUETTE si le trait n'y est plus, ou
   s'il ne se distingue pas."""
import sys, numpy as np
sys.path.insert(0,'scratchpad'); from couleurs_lab import *
from PIL import Image
from playwright.sync_api import sync_playwright

ETATS={'tenu':'#8FE08F','a-tenir':'#DD4D23','en-cours':'#FFD447'}
OUV={
 'fiche tenue'   : ("()=>{if(window.closeAll)closeAll();var p=promises.filter(q=>!q.draft).find(q=>q.status==='tenu');if(!p)p=promises[0];p.status='tenu';delete p.chiche;openDetail(p.id);return 1;}",'tenu'),
 'fiche à tenir' : ("()=>{if(window.closeAll)closeAll();var p=promises.filter(q=>!q.draft).find(q=>q.status==='rate');if(!p){p=promises.filter(q=>!q.draft)[0];p.status='rate';}delete p.chiche;openDetail(p.id);return 1;}",'a-tenir'),
 'fiche en cours': ("()=>{if(window.closeAll)closeAll();var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(!p)p=promises[0];p.status='encours';delete p.chiche;openDetail(p.id);return 1;}",'en-cours'),
 'Index'         : ("()=>{if(window.closeAll)closeAll();window._s4Trois=false;setView('toile');window.ouvrirIndex();return 1;}",None),
}
def compte(img, cible, seuil=14.0):
    a=np.asarray(img.convert('RGB'),dtype=float)
    lab_c=np.array(rgb2lab(*hex2rgb(cible)))
    h,w,_=a.shape
    ech=a.reshape(-1,3)[::3]
    d=np.array([math_dist(rgb2lab(*p),lab_c) for p in ech])
    return int((d<seuil).sum()*3), h*w
import math
def math_dist(a,b): return math.dist(a,b)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app-identite.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print(f"{'écran':16}{'thème':8}{'couleur d état':16}{'pixels qu elle occupe':>24}{'verdict':>12}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        for nom,(js,et) in OUV.items():
            pg.evaluate(js); pg.wait_for_timeout(1900)
            pg.query_selector('#device').screenshot(path='scratchpad/_et.png')
            im=Image.open('scratchpad/_et.png')
            cibles = [et] if et else list(ETATS)
            for c in cibles:
                n,tot=compte(im,ETATS[c])
                v='muet' if n<400 else ('faible' if n<1200 else 'lisible')
                print(f"  {nom:14}{th:8}{c+' '+ETATS[c]:16}{n:>14} / {tot:<8}{v:>12}")
            pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(400)
    b.close()
