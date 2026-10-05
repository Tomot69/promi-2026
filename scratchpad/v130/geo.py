from playwright.sync_api import sync_playwright
G=r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('detailPoster'); const out=[];
  const cv=document.getElementById('dpTrameCv'); const r0=cv.getBoundingClientRect(); out.push('canevas '+Math.round(r0.top-dv.top)+'→'+Math.round(r0.bottom-dv.top)+' onde='+(cv.getAttribute('data-onde')||P.getAttribute('data-onde')||'?'));
  const w=document.createTreeWalker(P,NodeFilter.SHOW_TEXT); let t; while(t=w.nextNode()){ const s=t.textContent.trim(); if(!s) continue; const e=t.parentElement; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none') continue; const r=document.createRange(); r.selectNodeContents(t); const b=r.getBoundingClientRect(); if(b.width<2) continue; const y=b.top-dv.top; if(y<0||y>844) continue;
    const top=document.elementFromPoint(b.left+b.width/2,b.top+b.height/2); if(!top||!(top===e||e.contains(top)||top.contains(e))) continue; out.push(s.slice(0,26)+' : '+y.toFixed(1)+'→'+(b.bottom-dv.top).toFixed(1)+' x'+Math.round(b.left-dv.left)+' '+(e.id||e.className)); }
  [...P.querySelectorAll('canvas.kr-c, .nq-noy, #dpDetails, .dpd-tog')].forEach(e=>{ const b=e.getBoundingClientRect(); if(b.width>2) out.push((e.id||e.className)+' : '+(b.top-dv.top).toFixed(1)+'→'+(b.bottom-dv.top).toFixed(1)); });
  return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in (('PROMI',"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"),('CERCLE',"()=>{closeAll(); openEssaim('potager');}")):
        pg.evaluate(js); pg.wait_for_timeout(3000); print(nom); [print('   ',l) for l in pg.evaluate(G)]
        # bas de l'onde : dernière rangée du canevas où le champ (couleur du pixel 6,6) paraît encore
        print('   bas du trait (px écran) :', pg.evaluate("()=>{const cv=document.getElementById('dpTrameCv'); const g=cv.getContext('2d'); const W=cv.width,H=cv.height; const d=g.getImageData(0,0,W,H).data; const k=W/cv.getBoundingClientRect().width; let bas=0, haut=H; for(let y=0;y<H;y+=2){ for(let x=0;x<W;x+=4){ const i=(y*W+x)*4; if(d[i+3]>200){ if(y>bas) bas=y; } } } const dv=document.getElementById('device').getBoundingClientRect(); return (cv.getBoundingClientRect().top-dv.top+bas/k).toFixed(1); }"))
    b.close()
