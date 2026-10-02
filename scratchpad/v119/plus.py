from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>setTheme('dark')"); pg.wait_for_timeout(800)
    print(pg.evaluate("""()=>{const b=document.getElementById('createBtn'); const cs=getComputedStyle(b), bf=getComputedStyle(b,'::before'), af=getComputedStyle(b,'::after');
      return {html:b.outerHTML.slice(0,500), bg:cs.backgroundImage.slice(0,200), bord:cs.border, sh:cs.boxShadow, ol:cs.outline, avant:[bf.backgroundImage.slice(0,300), bf.border, bf.outline, bf.boxShadow], apres:[af.backgroundImage.slice(0,200), af.border, af.outline]}; }"""))
    print(pg.evaluate("""()=>{const b=document.getElementById('indexBtn'); return b.outerHTML.slice(0,400)}"""))
    b.close()
