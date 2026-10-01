from playwright.sync_api import sync_playwright
R="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
JS=r"""()=>{const o=[];['stage','toile','indexSheet','feedView','feedScreen','viewSwitch','dock'].forEach(id=>{
 const e=document.getElementById(id); if(!e){o.push(id+' ABSENT');return;}
 const c=getComputedStyle(e), r=e.getBoundingClientRect();
 o.push(id+' disp='+c.display+' vis='+c.visibility+' op='+c.opacity+' cls='+(e.className||'')+' box='+Math.round(r.left)+','+Math.round(r.top)+' '+Math.round(r.width)+'x'+Math.round(r.height));});
 return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    print('--- AU REPOS ---')
    for l in pg.evaluate(JS): print('  ',l)
    print('--- ouvrirIndex() ---')
    print(pg.evaluate("()=>{try{window.ouvrirIndex();return 'ok';}catch(e){return 'ERR '+e;}}"))
    pg.wait_for_timeout(1200)
    for l in pg.evaluate(JS): print('  ',l)
    pg.query_selector('#device').screenshot(path=R+'/scratchpad/_probe_ix.png')
    print('--- setView fil ---')
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1200)
    for l in pg.evaluate(JS): print('  ',l)
    pg.query_selector('#device').screenshot(path=R+'/scratchpad/_probe_fil.png')
    print('ERR', er[:3]); b.close()
