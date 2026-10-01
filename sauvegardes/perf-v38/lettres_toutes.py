# Toute lettre isolée (élément de 1 à 2 caractères) posée dans un titre, dont la couleur diffère de son titre ou qui clignote.
from playwright.sync_api import sync_playwright
J=r"""()=>{ const out=[]; const T=[...document.querySelectorAll('h1,h2,h3,.scr-ti,.scr-t,.acc-mm,.cs-mark,#shcTitre .t,[class*=titre],[class*=-ti],[class*=mark]')];
 for(const t of T){ const ct=getComputedStyle(t).color;
  for(const k of t.querySelectorAll('*')){ const x=k.textContent.trim(); if(!x||x.length>2) continue; const s=getComputedStyle(k);
   const blink=s.animationName.indexOf('promiBlink')>=0; if(s.color!==ct||blink){ let h=t; let id=''; while(h&&!id){id=h.id;h=h.parentElement;}
     out.push([id, t.tagName+'.'+String(t.className).slice(0,30), (t.textContent||'').trim().slice(0,22), x, k.className, s.color, 'titre '+ct, blink?'CLIGNOTE':'']); } } }
 return out; }"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ('dark','light'):
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("t=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", th); pg.wait_for_timeout(600)
        seen=set()
        for r in pg.evaluate(J):
            k=tuple(r[:5]); 
            if k in seen: continue
            seen.add(k); print(th, r)
        pg.close()
    b.close()
