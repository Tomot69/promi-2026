import sys
from playwright.sync_api import sync_playwright
Q=r"""()=>{var out=[];
 function dec(el){var p=[];var n=el;while(n&&n!==document.body){p.unshift(n.tagName.toLowerCase()+(n.id?'#'+n.id:'')+(n.className&&typeof n.className==='string'?'.'+n.className.trim().split(/\s+/).join('.'):''));n=n.parentElement;}
  return {chemin:p.slice(-4).join(' > '), inline:el.getAttribute('style')||'', couleur:getComputedStyle(el).color};}
 document.querySelectorAll('i,.pc-lb,.pc-go,#pvApply').forEach(function(el){
   var t=(el.textContent||'').trim();
   if(t==='▾'||el.classList.contains('pc-lb')||el.classList.contains('pc-go')||el.id==='pvApply'){
     var r=el.getBoundingClientRect(); if(r.width<2)return; out.push(dec(el));}});
 return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app-identite.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate(r"""()=>{var p=promises.filter(q=>!q.draft).find(q=>q.status==='encours');if(p){delete p.chiche;openDetail(p.id);}}""")
    pg.wait_for_timeout(1800)
    for o in pg.evaluate(Q): print(o['couleur'],'|',o['chemin'],'| inline:',o['inline'][:90])
    b.close()
