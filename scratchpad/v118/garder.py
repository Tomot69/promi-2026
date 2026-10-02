from playwright.sync_api import sync_playwright
J = r"""()=>{ const e=document.querySelector('#createSheet .pp-garder'); if(!e) return 'absent';
  const out={inline:e.getAttribute('style'), cls:e.className, sheetCls:document.getElementById('createSheet').className, regles:[]};
  for(const sh of document.styleSheets){ let rs; try{ rs=sh.cssRules; }catch(_){ continue; }
    for(const r of rs){ if(r.style && r.style.display==='none' && r.selectorText){ let ok=false; try{ ok=e.matches(r.selectorText); }catch(_){}
      if(ok) out.regles.push((sh.ownerNode&&sh.ownerNode.id||'(sans id)')+' :: '+r.selectorText.slice(0,160)); } } }
  return out; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932})
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate('()=>{var o=document.getElementById("promiOnb");if(o){o.classList.add("gone");o.style.display="none";}}')
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"); pg.wait_for_timeout(2500)
    print(pg.evaluate(J)); b.close()
