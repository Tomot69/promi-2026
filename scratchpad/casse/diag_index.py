import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{if(window.closeAll)closeAll();ouvrirIndex();}"); pg.wait_for_timeout(1600)
    print('handler oninput :', pg.evaluate("()=>{const e=document.getElementById('ixSearch');return e? (typeof e.oninput):'ABSENT';}"))
    print('parent de #ixSearch :', pg.evaluate("()=>{const e=document.getElementById('ixSearch');return e&&e.parentNode?(e.parentNode.className||e.parentNode.id):'?';}"))
    pg.evaluate("""()=>{window.__bi=0; const o=window.buildIndex;
      window.buildIndex=function(){window.__bi++; return o.apply(this,arguments);};
      try{buildIndex=window.buildIndex;}catch(e){}}""")
    pg.evaluate("""()=>{const e=document.getElementById('ixSearch');e.focus();e.value='zzzz';
      e.dispatchEvent(new Event('input',{bubbles:true}));}"""); pg.wait_for_timeout(1300)
    print('buildIndex appelé :', pg.evaluate("()=>window.__bi"), ' ixQuery =', pg.evaluate("()=>(typeof ixQuery!=='undefined')?ixQuery:'INDÉFINI'"))
    print('.ix-bloc après filtre :', pg.evaluate("()=>document.querySelectorAll('#indexList .ix-bloc').length"))
    print('.s4-carte après filtre :', pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte').length"))
    print('_s4Entrees :', pg.evaluate("()=>((window._s4Entrees||[]).length)"))
    b.close()
