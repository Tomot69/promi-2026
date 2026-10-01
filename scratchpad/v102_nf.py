import sys
from playwright.sync_api import sync_playwright
M=r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390; const Y=v=>+((v-D.top)/k).toFixed(1);
 const it=[...document.querySelectorAll('#dpNueeFil .nf-item')].filter(e=>e.getBoundingClientRect().height>0).slice(0,2);
 return it.map(c=>{ const cb=c.getBoundingClientRect(); const o={carte:[Y(cb.top),Y(cb.bottom)]};
   c.querySelectorAll('*').forEach(e=>{ const t=(e.textContent||'').trim(); if(!t||[...e.children].some(k=>(k.textContent||'').trim())) return; const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); const b=e.getBoundingClientRect(); const cs=getComputedStyle(e);
     o[(e.className||e.tagName)+'«'+t.slice(0,10)]={boite:[Y(b.top),Y(b.bottom)],encre:[Y(r.top),Y(r.bottom)],fs:cs.fontSize,lh:cs.lineHeight,fam:cs.fontFamily.split(',')[0],pos:cs.position,top:cs.top,mt:cs.marginTop}; }); return o; });}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for app in sys.argv[1].split(','):
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/'+app); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme('dark');}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();openEssaim('potager');}"); pg.wait_for_timeout(2800)
        if len(sys.argv)>2: pg.evaluate("()=>{ if(window._nueeDefile) window._nueeDefile(true); }"); pg.wait_for_timeout(1200)
        print('==',app)
        for c in pg.evaluate(M):
            for k,v in c.items(): print('   ',k,v)
        pg.close()
    b.close()
