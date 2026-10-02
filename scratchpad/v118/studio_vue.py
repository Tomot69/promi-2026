import sys
from playwright.sync_api import sync_playwright
J = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390; const out=[];
  document.querySelectorAll('#studioScreen *').forEach(e=>{ const t=(e.textContent||'').trim(); if(!/^(◐|◑)?\s*(SOMBRE|CLAIR|AVEC TEXTE|SANS TEXTE|Zzz)$/i.test(t)) return; const r=e.getBoundingClientRect(); if(!r.width) return; const c=getComputedStyle(e);
    out.push({tag:e.tagName, id:e.id, cls:(''+e.className).slice(0,50), txt:t, x:+((r.left-dv.left)/k).toFixed(1), y:+((r.top-dv.top)/k).toFixed(1), w:+(r.width/k).toFixed(1), h:+(r.height/k).toFixed(1), font:c.fontFamily.split(',')[0]+' '+c.fontSize+' '+c.fontWeight, ls:c.letterSpacing, tt:c.textTransform, col:c.color, bg:c.backgroundColor, bd:c.border, rad:c.borderRadius, pad:c.padding, parent:(e.parentNode.id||e.parentNode.className).toString().slice(0,40), aria:e.getAttribute('aria-pressed')+'/'+e.getAttribute('aria-label')}); });
  return out; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for W in (430, 375):
        ctx = b.new_context(viewport={'width':W,'height':932 if W==430 else 812}, device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + (sys.argv[1] if len(sys.argv)>1 else 'app.html')); pg.wait_for_timeout(6500)
        for th in ('light','dark'):
            pg.evaluate("(t)=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); setTheme(t); document.getElementById('openStudio2').click();}", th); pg.wait_for_timeout(2500)
            if W==430: pg.screenshot(path='scratchpad/v118/studio-%s.png' % th, clip={'x':20,'y':44,'width':390,'height':844})
            print(W, th, 'device', pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return Math.round(r.width)+'×'+Math.round(r.height)}"))
            for e in pg.evaluate(J): print('  ', e)
        ctx.close()
    b.close()
