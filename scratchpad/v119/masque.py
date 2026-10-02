from playwright.sync_api import sync_playwright
J = r"""()=>{ const o=[]; document.querySelectorAll('#plusScreen *, #plusScreen').forEach(e=>{ const c=getComputedStyle(e), m=c.webkitMaskImage||c.maskImage||''; const r=e.getBoundingClientRect(); for(const ps of ['', '::before','::after']){ const cc=ps?getComputedStyle(e,ps):c; const mm=cc.webkitMaskImage||cc.maskImage||'none', bg=cc.backgroundImage||'none';
   if((mm!=='none') || /gradient/.test(bg) || (cc.boxShadow!=='none'&&/px [1-9]\d*px/.test(cc.boxShadow.replace(/^[^)]*\)/,''))) || cc.textShadow!=='none' || (cc.filter||'none')!=='none') o.push((e.id||e.className).toString().slice(0,26)+ps+' ['+Math.round(r.width)+'×'+Math.round(r.height)+'] masque:'+mm.slice(0,60)+' fond:'+bg.slice(0,60)+' ombre:'+cc.boxShadow.slice(0,40)+' filtre:'+(cc.filter||'')); } }); return o; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{closeAll(); document.getElementById('settingsBtn').click(); setTimeout(()=>{const b=document.getElementById('openPlusTop'); if(b) b.click();},500);}")
    for ms in (700, 300, 400, 1500):
        pg.wait_for_timeout(ms); print('—', ms); [print('  ', l) for l in pg.evaluate(J)]
    b.close()
