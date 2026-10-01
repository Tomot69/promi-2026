from playwright.sync_api import sync_playwright
JS=r"""()=>{
  const out={};
  const info=(id)=>{const e=document.getElementById(id); if(!e) return 'ABSENT';
    const c=getComputedStyle(e), r=e.getBoundingClientRect();
    return {disp:c.display,pos:c.position,w:Math.round(r.width),h:Math.round(r.height),
      left:c.left,top:c.top,maxw:c.maxWidth,maxh:c.maxHeight,ov:c.overflow,
      vis:c.visibility,op:c.opacity,parent:(e.parentNode.id||e.parentNode.className||'').slice(0,30),
      pdisp:getComputedStyle(e.parentNode).display,
      ph:Math.round(e.parentNode.getBoundingClientRect().height)};};
  ['csChoix','phIn','fTitle','fWho','promiForm','csPhrase','createSheet'].forEach(i=>out[i]=info(i));
  /* qui impose quoi à #csChoix et à #fTitle ? */
  const regles=(sel)=>{const e=document.querySelector(sel); if(!e) return [];
    const r=[]; for(const sh of document.styleSheets){ let rules; try{rules=sh.cssRules;}catch(x){continue;}
      for(const ru of rules){ if(!ru.selectorText) continue;
        let m=false; try{m=e.matches(ru.selectorText);}catch(x){}
        if(m && /height|display|max-width|width/.test(ru.style.cssText))
          r.push(ru.selectorText.slice(0,90)+' { '+ru.style.cssText.slice(0,120)+' }'); } }
    return r.slice(-8);};
  out._reglesCsChoix=regles('#csChoix');
  out._reglesFTitle=regles('#fTitle');
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1100)
    pg.evaluate("()=>{const e=document.querySelector('[data-ph=titre]');if(e)e.click();}"); pg.wait_for_timeout(1000)
    o=pg.evaluate(JS)
    for k in ('csChoix','phIn','fTitle','fWho','promiForm','csPhrase'):
        print('%-11s %s'%(k,o[k]))
    print('\n--- règles sur #csChoix ---')
    for r in o['_reglesCsChoix']: print('   ',r)
    print('\n--- règles sur #fTitle ---')
    for r in o['_reglesFTitle']: print('   ',r)
    b.close()
