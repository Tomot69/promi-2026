# -*- coding: utf-8 -*-
"""Balaye TOUS les éléments qui peignent un état, sur les deux versions, et rend la LISTE
   de ceux qui ont changé de couleur. On lit le RENDU (§8 : on trie les surfaces, pas les
   règles), jamais la feuille de style."""
import json, sys
from playwright.sync_api import sync_playwright

ANCIENS = {'#2BE88C':'menthe','#8FA0FF':'périwinkle','#F07A2E':"orange d'origine",'#FFD447':'jaune',
           '#33BA6C':'vert clair','#A77CF7':'violet clair','#8FE08F':'amande','#DD4D23':'à tenir',
           '#291547':'en cours','#00341A':'tenu','#2E1C13':'corps à tenir'}
ECRANS = [('accueil', "()=>{closeAll();}"),
          ('aura',    "()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
          ('index',   "()=>{closeAll(); document.getElementById('indexBtn').click();}"),
          ('fil',     "()=>{closeAll(); document.getElementById('filBtn').click();}"),
          ('fiche',   "()=>{closeAll(); openDetail(promises.filter(p=>!p.draft&&!p.nuee)[0].id);}"),
          ('fiche tenue', "()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")]

SCAN = r"""()=>{
  const out=[], vu=new Set();
  const hex=(c)=>{const m=/rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(c||''); if(!m) return null;
    return '#'+[1,2,3].map(i=>(+m[i]).toString(16).padStart(2,'0')).join('').toUpperCase();};
  const nom=(e)=>{let p=e,s=[];for(let i=0;i<3&&p;i++,p=p.parentElement) s.unshift((p.tagName||'').toLowerCase()+(p.id?'#'+p.id:'')+(p.className&&typeof p.className==='string'?'.'+p.className.trim().split(/\s+/).slice(0,2).join('.'):''));
    return s.join(' ');};
  const dv=document.getElementById('device'); if(!dv) return out;
  dv.querySelectorAll('*').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return;
    const cs=getComputedStyle(e);
    if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity===0) return;
    [['fond',cs.backgroundColor],['texte',cs.color],['contour',cs.borderTopColor],['trait',e.getAttribute&&e.getAttribute('stroke')],
     ['fill',e.getAttribute&&e.getAttribute('fill')]].forEach(([q,v])=>{
      let h = v && v[0]==='#' ? v.toUpperCase() : hex(v);
      if(!h) return;
      const k=nom(e)+'|'+q+'|'+Math.round(r.top)+'x'+Math.round(r.left);
      if(vu.has(k)) return; vu.add(k);
      out.push({n:nom(e), q:q, c:h, y:Math.round(r.top), x:Math.round(r.left), t:(e.textContent||'').trim().slice(0,22)});
    });
  });
  return out; }"""

def releve(url):
    res={}
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        pg.goto(url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark','light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for nom, js in ECRANS:
                try: pg.evaluate(js)
                except Exception: continue
                pg.wait_for_timeout(1400)
                for o in pg.evaluate(SCAN):
                    if o['c'] in ANCIENS:
                        res[(th,nom,o['n'],o['q'],o['y'],o['x'])]=(o['c'],o['t'])
        b.close()
    return res

av = releve('http://127.0.0.1:8752/_preuve-v8d.html')
ap = releve('http://127.0.0.1:8752/app.html')

from collections import defaultdict
def par_famille(res):
    d=defaultdict(set); txt=defaultdict(set); ecr=defaultdict(set)
    for (th,ec,n,q,y,x),(c,t) in res.items():
        fam=n.split(' ')[-1]
        d[(fam,q)].add(c); ecr[(fam,q)].add(ec)
        if t: txt[(fam,q)].add(t[:20])
    return d, txt, ecr
A,tA,eA = par_famille(av); B,tB,eB = par_famille(ap)
NEUF = {'#DD4D23':'à tenir','#291547':'en cours','#00341A':'tenu'}
lignes=[]
for k in sorted(set(A)|set(B)):
    a,b = A.get(k,set()), B.get(k,set())
    if a==b: continue
    lignes.append((k, sorted(a), sorted(b), sorted(eA.get(k,set())|eB.get(k,set())), sorted(tA.get(k,set())|tB.get(k,set()))[:2]))
f=lambda L:', '.join(ANCIENS.get(c,c) for c in L) or '—'
print()
print('%-32s %-7s %-40s %s' % ('LE NŒUD', 'CE QUI', 'AVANT', 'APRÈS'))
for (fam,q),a,b,ec,t in lignes:
    print('%-32s %-7s %-40s %s' % (fam[:32], q, f(a), f(b)))
    print('%-32s %-7s   %s' % ('', '', ' · '.join(ec) + ('   « ' + ' » « '.join(t) + ' »' if t else '')))
print()
print('%d familles de nœuds corrigées' % len(lignes))
