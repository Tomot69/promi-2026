from playwright.sync_api import sync_playwright
J = r"""(sels)=>sels.map(s=>{ const e=document.querySelector(s); if(!e) return s+' : absent'; const c=getComputedStyle(e); return s+' : color '+c.color+' · inline « '+(e.getAttribute('style')||'').slice(0,160)+' » · fill '+c.fill+' · bg '+c.backgroundColor; })"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, timezone_id='Europe/Paris')
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){} window._zzzMaintenant=function(){return Date.parse('2026-12-21T23:30:00+01:00')};")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{ setTheme('dark'); _zzz.regle(true); closeAll(); }"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex()}"); pg.wait_for_timeout(2500)
    for l in pg.evaluate(J, ['#indexList .s4-ti', '#indexList .s4-natlab', '#indexList .s4-eb', '#indexList .s4-et']): print(l)
    pg.evaluate("()=>{closeAll(); const p=promises.find(q=>q.chiche&&!q.draft); openDetail(p.id)}"); pg.wait_for_timeout(2500)
    for l in pg.evaluate(J, ['#dptTitre', '#dptNat', '#dptQui', '#dpMsg', '#detailPoster .dpm-rep']): print(l)
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300)}"); pg.wait_for_timeout(2500)
    for l in pg.evaluate(J, ['#createSheet .enh', '#createSheet .closeb', '#csPinceauRail .pc-t', '#csPinceauRail .pc-n']): print(l)
    b.close()
