from playwright.sync_api import sync_playwright
JS=r"""()=>{ const e=document.getElementById('dptNat'), cs=getComputedStyle(e), p=e.parentElement; const P=['marginTop','marginBottom','paddingTop','paddingBottom','transform','alignSelf','position','top','bottom','height','lineHeight','verticalAlign','display','translate'];
  const kids=[...p.children].map(c=>{const r=c.getBoundingClientRect(); return c.tagName+'.'+String(c.className).slice(0,30)+' h'+r.height.toFixed(1)+' y'+r.top.toFixed(1)+' as:'+getComputedStyle(c).alignSelf+' mt:'+getComputedStyle(c).marginTop}).join(' ; ');
  return {style:e.getAttribute('style'), cs:P.map(k=>k+':'+cs[k]).join(' '), parent:(p.getAttribute('style')||'').slice(0,300), pcs:['alignItems','display','height','paddingTop','flexDirection','flexWrap','alignContent'].map(k=>k+':'+getComputedStyle(p)[k]).join(' '), kids:kids, html:e.innerHTML.slice(0,300)}; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for n,js in (('promi',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),('cercle',"()=>{closeAll(); openEssaim('potager');}")):
        pg.evaluate(js); pg.wait_for_timeout(3000); r=pg.evaluate(JS); print('==',n); [print('  ',k,':',v) for k,v in r.items()]
    b.close()
