from playwright.sync_api import sync_playwright
OUVRE = """()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click(); try{_aura.fige(true)}catch(e){} }"""
M = """async ()=>{ const cv=document.getElementById('auBoule'), W=cv.width, out=[]; for(const u of [0,0.1,0.2,0.3,0.5,0.75,1]){ window._peloteU=u; await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))));
   const d=cv.getContext('2d').getImageData(W/2-60,W/2-60,120,120).data; let s=0; for(let i=0;i<d.length;i+=4) s+=d[i]+d[i+1]+d[i+2]; out.push(+(s/(d.length/4)/3).toFixed(2)); } window._peloteU=undefined; return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{closeAll();setTheme('light')}"); pg.wait_for_timeout(800); pg.evaluate(OUVRE); pg.wait_for_timeout(4000); pg.evaluate("()=>{_aura.fige(true)}")
    print('1re ouverture', pg.evaluate(M), pg.evaluate("()=>_peloteLumiere.etat().cle"))
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1500); pg.evaluate(OUVRE); pg.wait_for_timeout(3000)
    print('2e ouverture ', pg.evaluate(M), pg.evaluate("()=>_peloteLumiere.etat().cle"))
    b.close()
