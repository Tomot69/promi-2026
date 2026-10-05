from playwright.sync_api import sync_playwright
P=r"""()=>{ window.__r=[]; const f=Toile.dalleTrame; Toile.dalleTrame=function(dcv,pid,k,monde,opts){ if(opts&&opts.rampe&&window.__e==='Index'){ const p=promises.find(x=>x.id===pid); window.__r.push((p?p.title:pid)+' ← '+(new Error().stack||'').split('\n').slice(1,7).map(l=>l.trim().replace(/http:\/\/127.0.0.1:8752\//,'').slice(0,60)).join(' < ')); } return f.apply(this,arguments); }; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); vus=0
    for essai in range(8):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','light')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} Toile.setTheme('mosaique');}"); pg.wait_for_timeout(2500); pg.evaluate(P)
        pg.evaluate("()=>{window.__e='fiche'; closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(2600)
        pg.evaluate("()=>{window.__e='Index'; closeAll(); setView('toile'); ouvrirIndex();}"); pg.wait_for_timeout(2600)
        R=pg.evaluate("()=>window.__r"); 
        if R: vus+=1; print('essai',essai); [print('   ',x[:420]) for x in R[:2]]
        ctx.close()
    print('passages avec une rampe pendant l\'Index :',vus,'/ 8'); b.close()
