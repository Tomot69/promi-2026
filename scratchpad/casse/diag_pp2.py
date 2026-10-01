from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1100)
    pg.evaluate("()=>{const e=document.querySelector('[data-ph=titre]');if(e)e.click();}"); pg.wait_for_timeout(1000)
    print('AVANT _ppTout :')
    print('  classes    :', pg.evaluate("()=>document.getElementById('createSheet').className"))
    print('  choixOuvert:', pg.evaluate("()=>window._ppEcran?window._ppEcran().ouvert:'?'"))
    print('  csChoix    :', pg.evaluate("""()=>{const z=document.getElementById('csChoix');const c=getComputedStyle(z);
      return {cls:z.className,h:Math.round(z.getBoundingClientRect().height),mh:c.maxHeight,pt:c.paddingTop,
              enfants:z.children.length};}"""))
    pg.evaluate("()=>{if(window._ppTout)_ppTout();}"); pg.wait_for_timeout(900)
    print('\nAPRÈS _ppTout :')
    print('  classes    :', pg.evaluate("()=>document.getElementById('createSheet').className"))
    print('  csChoix    :', pg.evaluate("""()=>{const z=document.getElementById('csChoix');const c=getComputedStyle(z);
      return {h:Math.round(z.getBoundingClientRect().height),mh:c.maxHeight,pt:c.paddingTop};}"""))
    print('  #phIn      :', pg.evaluate("""()=>{const e=document.getElementById('phIn');const c=getComputedStyle(e);
      const r=e.getBoundingClientRect();return {w:Math.round(r.width),h:Math.round(r.height),op:c.opacity,pos:c.position};}"""))
    print('\n=== qui masque le .field de #fTitle ? ===')
    print(pg.evaluate("""()=>{const e=document.getElementById('fTitle'); const f=e.parentNode;
      const out=[];
      for(const sh of document.styleSheets){ let rules; try{rules=sh.cssRules;}catch(x){continue;}
        for(const ru of rules){ if(!ru.selectorText) continue;
          let m=false; try{m=f.matches(ru.selectorText);}catch(x){}
          if(m && /display/.test(ru.style.cssText)) out.push(ru.selectorText.slice(0,110)+' { '+ru.style.display+' }'); } }
      return out;}"""))
    b.close()
