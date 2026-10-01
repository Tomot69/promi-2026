# -*- coding: utf-8 -*-
"""LA FRONTIÈRE STUDIO / ÉTAT — mesurée, pas lue.
   On rend l'app sous DEUX palettes très éloignées et on regarde CE QUI BOUGE.
   · ce qui doit bouger  : le sol de la sphère (et la Toile, témoin)
   · ce qui ne doit PAS  : la légende, les arcs des Noyaux, les traits et libellés d'état,
                           et LES DALLES (figées à leur plantation, partout où elles paraissent)"""
import sys, json
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
A, B = 'signal', 'irascible'      # bleu/rose/lilas/crème  contre  rouges et noir

LIRE = r"""()=>{
  var o={};
  function col(cle, sel, prop){
    var e=document.querySelector(sel); if(!e){ o[cle]='(absent)'; return; }
    var cs=getComputedStyle(e); o[cle]=prop==='bg'?cs.backgroundColor:cs.color;
  }
  /* — LES ÉTATS, sur l'Aura — */
  var lg=document.querySelectorAll('#auraScreen .au-lg i');
  o['légende · pastille tenues']  = lg[0]?getComputedStyle(lg[0]).backgroundColor:'(absent)';
  o['légende · pastille en cours']= lg[1]?getComputedStyle(lg[1]).backgroundColor:'(absent)';
  o['légende · pastille à tenir'] = lg[2]?getComputedStyle(lg[2]).backgroundColor:'(absent)';
  var arcs=document.querySelectorAll('#auraScreen .au-nb path, #auraScreen .au-nb circle');
  var A=[]; arcs.forEach(function(p){ var s=p.getAttribute('stroke')||getComputedStyle(p).stroke; if(s&&s!=='none') A.push(s); });
  o["arcs des Noyaux"]=A.slice(0,10).join(' ');
  /* — LE SOL DE LA SPHÈRE, tel que l'app le publie — */
  try{ o['sol de la sphère']=JSON.stringify(window._aura.etat().sol); }catch(e){ o['sol de la sphère']='(?)'; }
  /* — LES DALLES : on hache les pixels de chaque canevas de « Ce que tu as tenu » — */
  var D=[];
  document.querySelectorAll('#auraScreen .au-c canvas, #auraScreen .au-c2 canvas').forEach(function(c,i){
    try{ var g=c.getContext('2d'); var d=g.getImageData(0,0,c.width,c.height).data;
         var h=2166136261; for(var k=0;k<d.length;k+=331){ h^=d[k]; h=Math.imul(h,16777619); }
         D.push((h>>>0).toString(16)); }catch(e){ D.push('x'); }
  });
  o['dalles « Ce que tu as tenu » (empreintes)']=D.join(' ');
  return o;}"""

LIRE2 = r"""()=>{
  var o={};
  function c(cle, sel){ var e=document.querySelector(sel); o[cle]=e?getComputedStyle(e).color:'(absent)'; }
  function b(cle, sel){ var e=document.querySelector(sel); o[cle]=e?getComputedStyle(e).backgroundColor:'(absent)'; }
  /* les libellés d'état des cartes d'Index */
  var et=document.querySelectorAll('#indexSheet .s4-et');
  o['Index · libellé d’état (1)']=et[0]?getComputedStyle(et[0]).color:'(absent)';
  o['Index · libellé d’état (2)']=et[1]?getComputedStyle(et[1]).color:'(absent)';
  o['Index · libellé d’état (3)']=et[2]?getComputedStyle(et[2]).color:'(absent)';
  /* le trait d'état d'une carte : on lit la ligne dans le canevas de la carte */
  return o;}"""

def sous(pg, pal, fn, ouvre):
    pg.evaluate("(p)=>{window.Toile.setPalette(p);}", pal)
    pg.wait_for_timeout(2600)
    pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{%s}"%ouvre); pg.wait_for_timeout(3800)
    return pg.evaluate(fn)

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto(URL); pg.wait_for_timeout(6300)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ra=sous(pg,A,LIRE,"document.getElementById('souffleBtn').click();")
    rb=sous(pg,B,LIRE,"document.getElementById('souffleBtn').click();")
    ia=sous(pg,A,LIRE2,"document.getElementById('indexBtn').click();")
    ib=sous(pg,B,LIRE2,"document.getElementById('indexBtn').click();")
    b.close()

print('PALETTE A = %s   ·   PALETTE B = %s\n'%(A,B))
print('%-44s %-9s %s'%('','SUIT ?','valeurs'))
print('-'*104)
for d1,d2 in ((ra,rb),(ia,ib)):
    for k in d1:
        bouge = d1[k]!=d2.get(k)
        v = ('%s  →  %s'%(str(d1[k])[:34], str(d2.get(k))[:34]))
        print('%-44s %-9s %s'%(k[:44], 'BOUGE' if bouge else 'fixe', v))
