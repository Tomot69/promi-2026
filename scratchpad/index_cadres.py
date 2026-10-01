# -*- coding: utf-8 -*-
"""Les 102 cadres du moodboard, avec leur signature de texte : pour retrouver la page +."""
from playwright.sync_api import sync_playwright
MB="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/promi-moodboard-H.html"
JS=r"""()=>{
  const isFrame=(e)=>{const s=e.getAttribute('style')||'';return /width:\s*390px/.test(s)&&/height:\s*844px/.test(s);};
  const frames=[...document.querySelectorAll('div')].filter(isFrame);
  return frames.map((f,i)=>{
    const t=(f.innerText||'').replace(/\s+/g,' ').trim().slice(0,72);
    const bg=getComputedStyle(f).backgroundColor;
    return i+' | '+bg+' | '+t;});}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':1200})
    pg.goto('file://'+MB); pg.wait_for_timeout(4000)
    for r in pg.evaluate(JS): print(r)
    b.close()
