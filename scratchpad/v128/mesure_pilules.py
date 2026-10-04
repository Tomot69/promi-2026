# le plus compact des composants de menu ou de pilule de l'app : hauteur, écart, corps
from playwright.sync_api import sync_playwright
JS=r"""(sel)=>{ const dv=document.getElementById('device').getBoundingClientRect(); const E=[...document.querySelectorAll(sel)].filter(e=>{const r=e.getBoundingClientRect(); return r.width>20&&r.height>10&&r.left>=dv.left-4&&r.top>=dv.top&&r.bottom<=dv.bottom;}); const R=E.map(e=>e.getBoundingClientRect());
  const gaps=[]; for(let i=1;i<R.length;i++){ const dy=R[i].top-R[i-1].bottom, dx=R[i].left-R[i-1].right; gaps.push(Math.abs(R[i].top-R[i-1].top)<4?+dx.toFixed(1):+dy.toFixed(1)); }
  return E.slice(0,4).map((e,i)=>{const cs=getComputedStyle(e); return (e.textContent||'').trim().slice(0,18)+' h'+R[i].height.toFixed(1)+' w'+R[i].width.toFixed(0)+' fs'+cs.fontSize+' '+cs.fontFamily.split(',')[0]+' pad'+cs.paddingLeft+' br'+cs.borderRadius+' bw'+cs.borderTopWidth}).join(' | ')+'  écarts '+gaps.slice(0,4).join(' '); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{document.querySelector('.ph-photo-btn').click()}"); pg.wait_for_timeout(800)
    print('menu photo :', pg.evaluate(JS,'.ph-photo-nid button:not(.ph-photo-btn)'))
    print(pg.evaluate("()=>{const e=[...document.querySelectorAll('.ph-photo-nid button:not(.ph-photo-btn)')][0]; return e?e.className+' / parent '+e.parentElement.className:''}"))
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3600)
    print('rail du pinceau :', pg.evaluate(JS,'#createSheet [data-glisse] > *, #createSheet .pin-rail > *, #createSheet [class*=pinc] button, #createSheet [class*=pinc] > *'))
    print(pg.evaluate("()=>{const e=[...document.querySelectorAll('#createSheet *')].filter(x=>x.children.length<=2&&/^Plein$/.test((x.textContent||'').trim()))[0]; if(!e) return ''; let n=e; const o=[]; for(let i=0;i<3&&n;i++){ const r=n.getBoundingClientRect(); o.push(n.tagName+'.'+n.className+' '+r.width.toFixed(0)+'×'+r.height.toFixed(0)); n=n.parentElement;} return o.join(' < ')}"))
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(2500)
    print(pg.evaluate("()=>{const dv=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('.pill,.chip,[class*=pastille],[class*=chip]')].map(e=>{const r=e.getBoundingClientRect(); return r.height>8&&r.width>20?e.className.split(' ')[0]+' '+r.height.toFixed(0):null}).filter(Boolean).slice(0,12).join(' | ')}"))
    b.close()
