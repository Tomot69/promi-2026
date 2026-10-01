import sys
from playwright.sync_api import sync_playwright
M=r"""(sels)=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390; const Y=v=>+((v-D.top)/k).toFixed(1);
 const out={}; sels.forEach(s=>{ const e=[...document.querySelectorAll(s)].find(x=>x.getBoundingClientRect().height>0); if(!e){out[s]=null;return;}
   const b=e.getBoundingClientRect(); const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); const c=getComputedStyle(e);
   out[s]={boite:[Y(b.top),Y(b.bottom)], encre:[Y(r.top),Y(r.bottom)], fs:c.fontSize, lh:c.lineHeight, top:e.style.top||''}; }); return out;}"""
SELS=sys.argv[2].split(',')
OUV=sys.argv[3] if len(sys.argv)>3 else "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"
with sync_playwright() as p:
    b=p.chromium.launch()
    for app in sys.argv[1].split(','):
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/'+app); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme('dark');}"); pg.wait_for_timeout(500)
        pg.evaluate(OUV); pg.wait_for_timeout(2500)
        print('==',app)
        for k,v in pg.evaluate(M,SELS).items(): print('   %-24s %s' % (k,v))
        pg.close()
    b.close()
