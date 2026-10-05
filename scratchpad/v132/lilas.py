from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3600)
    for l in pg.evaluate("""()=>{ const out=[]; const lilas='rgb(196, 162, 245)';
      [...document.querySelectorAll('#createSheet *')].forEach(e=>{ const c=getComputedStyle(e); if(e.getBoundingClientRect().width<2) return; ['color','borderTopColor','webkitTextFillColor','stroke','fill','backgroundColor'].forEach(k=>{ if(c[k]===lilas){ let n=e, d=0, src=''; while(n&&d<6){ if(n.style&&/196, 162, 245|C4A2F5|c4a2f5/.test(n.style.cssText)){ src=(n.id||n.className)+' ⟵ en ligne : '+n.style.cssText.match(/[a-z-]*:[^;]*(196, 162, 245|C4A2F5|c4a2f5)[^;]*/i)[0]; break; } n=n.parentElement; d++; } out.push(e.tagName+'.'+String(e.className).slice(0,18)+'#'+e.id+' '+k+' | '+src); } }); });
      return [...new Set(out)].slice(0,25); }"""): print(l[:200])
    b.close()
