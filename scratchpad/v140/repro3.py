import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
SRC="""()=>{ const c=document.createElement('canvas'); c.width=600; c.height=800; const g=c.getContext('2d'); g.fillStyle='#E03020'; g.fillRect(0,0,600,800); g.fillStyle='#20C040'; g.fillRect(0,0,600,200); g.fillStyle='#FFE000'; g.beginPath(); g.arc(300,400,150,0,7); g.fill(); return c.toDataURL('image/png'); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    src=pg.evaluate(SRC)
    d=pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
    def cap(n): pg.screenshot(path='scratchpad/v140/r3-%s.png'%n,clip={'x':d['x'],'y':d['y'],'width':390,'height':420})
    # une fiche à tenir, un dessin posé par l'outil
    pg.evaluate("()=>{ const q=promises.find(p=>!p.done&&p.kind!=='chiche'&&!p.nuee); window.__id=q.id; q.photo=null; q.dessin=null; openDetail(q.id); }"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ _dessin.ouvre(); }"); pg.wait_for_timeout(900)
    r=pg.evaluate("()=>{const s=document.querySelector('#dessinMode canvas'); const r=s.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
    pg.mouse.move(r[0]+60,r[1]+80); pg.mouse.down()
    for i in range(20): pg.mouse.move(r[0]+60+i*12, r[1]+80+ (i%5)*14); pg.wait_for_timeout(15)
    pg.mouse.up(); pg.wait_for_timeout(300)
    pg.evaluate("()=>_dessin.sort(true)"); pg.wait_for_timeout(1200); cap('1-dessin')
    # on importe une photo (comme le fait le sélecteur)
    pg.evaluate("(s)=>{ const b=document.querySelector('#detailPoster .ph-photo-btn'); const q=b._p; q.photo=s; b._rejoue&&b._rejoue(); }", src); pg.wait_for_timeout(1800); cap('2-photo')
    print(pg.evaluate("()=>{const q=promises.find(p=>p.id===window.__id); return {photo:!!q.photo, dessin:!!(q.dessin&&q.dessin.poses&&q.dessin.poses.length), dz:!!document.querySelector('#detailPoster > canvas.dz-bande')}}"))
    b.close()
