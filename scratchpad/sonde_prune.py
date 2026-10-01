# -*- coding: utf-8 -*-
"""TOUT CE QUI EST PEINT EN VERT PROFOND SUR LE CHAMP PRUNE — on remonte au premier
   fond opaque depuis chaque texte, comme sonde_champ.py."""
from playwright.sync_api import sync_playwright
JS = r"""()=>{
  const hex=c=>{const m=/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/.exec(c||''); if(!m) return null;
    if(m[4]!==undefined && +m[4]===0) return null;
    return '#'+[1,2,3].map(i=>(+m[i]).toString(16).padStart(2,'0')).join('').toUpperCase();};
  const fond=e=>{let p=e; while(p&&p!==document.body){const c=hex(getComputedStyle(p).backgroundColor); if(c) return {c:c,n:p.className||p.id}; p=p.parentElement;} return null;};
  const out=[];
  document.querySelectorAll('#detailPoster *').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return;
    const cs=getComputedStyle(e); if(cs.visibility==='hidden'||+cs.opacity===0) return;
    const t=(e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))?e.textContent.trim().slice(0,28):'';
    if(!t) return;
    const col=hex(cs.color), f=fond(e);
    out.push({t:t, col:col, fond:f&&f.c, ou:String(e.className).slice(0,40), fs:cs.fontSize, fw:cs.fontWeight});});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")
        pg.wait_for_timeout(2400)
        for o in pg.evaluate(JS):
            if o['fond'] in ('#2B1020','#0B4A2A','#00341A') or o['col'] in ('#00341A','#0B4A2A'):
                print(th, o)
    b.close()
