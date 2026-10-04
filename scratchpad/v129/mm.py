from playwright.sync_api import sync_playwright
JS=r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('detailPoster'); const out=[];
 [...document.querySelectorAll('#detailPoster *, .enh *')].forEach(e=>{ const t=(e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))?e.textContent.trim():''; if(!/^(PROMI|CHICHE|CERCLE|Promi|Chiche|Cercle|Promi\s*|P\s*r)/i.test(t)||t.length>8) return; const r=e.getBoundingClientRect(); if(r.top-dv.top>110||r.width<5) return; const cs=getComputedStyle(e); const p=e.parentElement, pr=p.getBoundingClientRect(), pc=getComputedStyle(p);
   out.push(e.tagName+'#'+e.id+'.'+e.className+' «'+t+'» y'+(r.top-dv.top).toFixed(2)+' h'+r.height.toFixed(2)+' fs'+cs.fontSize+' lh'+cs.lineHeight+' '+cs.fontFamily.split(',')[0]+' pos:'+cs.position+' top:'+cs.top+' tt:'+cs.textTransform+' | parent '+p.tagName+'#'+p.id+'.'+p.className+' y'+(pr.top-dv.top).toFixed(2)+' h'+pr.height.toFixed(2)+' disp:'+pc.display+' ai:'+pc.alignItems+' pad:'+pc.paddingTop+'/'+pc.paddingBottom+' style='+(e.getAttribute('style')||'').slice(0,160)); }); return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for n,js in (('promi',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),('cercle',"()=>{closeAll(); openEssaim('potager');}")):
        pg.evaluate(js); pg.wait_for_timeout(3000); print('==',n); [print(' ',x) for x in pg.evaluate(JS)]
    b.close()
