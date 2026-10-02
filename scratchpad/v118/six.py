from playwright.sync_api import sync_playwright
Q = r"""(sels)=>sels.map(s=>{ const out=[]; document.querySelectorAll(s).forEach(e=>{ const r=e.getBoundingClientRect(); if(!r.width) return; const c=getComputedStyle(e), b=getComputedStyle(e,'::before'), a=getComputedStyle(e,'::after');
   out.push({el:(e.id||e.className).toString().slice(0,30), ts:c.textShadow, bs:c.boxShadow, bg:c.backgroundImage.slice(0,90), mask:(c.webkitMaskImage||c.maskImage||'').slice(0,80), av:b.backgroundImage.slice(0,70), ap:a.backgroundImage.slice(0,70), anim:a.animationName+'/'+b.animationName}); }); return [s,out.slice(0,2)]; })"""
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    for th in ('light','dark'):
        pg.evaluate("(t)=>{closeAll(); setTheme(t); const p=promises.filter(q=>!q.draft&&!q.req&&!q.nuee)[0]; openDetail(p.id);}", th); pg.wait_for_timeout(1600)
        print(th, 'fiche', pg.evaluate(Q, ['#detailPoster .closeb', '#detailPoster .closeb *']))
    pg.evaluate("()=>{closeAll(); document.getElementById('shareBtn').click();}"); pg.wait_for_timeout(2000)
    print('partager', pg.evaluate(Q, ['#shareScreen .sh-badge', '#shareScreen [class*=badge]', '#shareScreen [class*=mm]']))
    pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('settingsBtn').click(); setTimeout(()=>{const b=document.getElementById('openPlusTop'); if(b) b.click();},500);}"); pg.wait_for_timeout(2500)
    print('ma parole', pg.evaluate(Q, ['#plusScreen .pc-achat', '#plusScreen button', '#plusScreen #pcCadre > *']))
    b.close()
