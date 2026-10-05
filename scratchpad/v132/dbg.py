from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932})
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; p.dessin={v:1,w:390,h:754,fond:'#FFB8D2',pose:true,masque:false,traits:[],poses:[{c:'#201908',t:8,g:0,pts:[60,200,0,-1,200,260,200,-1,330,180,400,-1]}]}; p.dessin.traits=p.dessin.poses.slice(); openDetail(p.id);}"); pg.wait_for_timeout(3000)
    print(pg.evaluate("()=>{const c=document.querySelector('.dz-bande'); if(!c) return 'absent'; const s=getComputedStyle(c), r=c.getBoundingClientRect(); const d=c.getContext('2d').getImageData(200,200,1,1).data; return {vis:s.visibility, disp:s.display, op:s.opacity, z:s.zIndex, pos:s.position, r:[r.left,r.top,r.width,r.height], px:[...d], parent:c.parentElement.id, avant:c.previousElementSibling&&c.previousElementSibling.id, top:document.elementsFromPoint(215,200).slice(0,4).map(e=>e.tagName+'#'+e.id+'.'+String(e.className).slice(0,14))}}"))
    b.close()
