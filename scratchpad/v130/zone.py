import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
clip={'x':20,'y':44+90,'width':390,'height':340}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','dark')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:120])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def aura(n):
        pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{try{_aura.fige(true); _aura.vue(0.6,0.2)}catch(e){}}"); pg.wait_for_timeout(700)
        pg.screenshot(path='scratchpad/v130/zone-%s.png'%n, clip=clip)
        print(n, pg.evaluate("()=>[...document.querySelectorAll('#auraScreen canvas, #auraScreen [id^=auPelote]')].map(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e); return e.id+' '+Math.round(r.left)+','+Math.round(r.top)+' '+Math.round(r.width)+'x'+Math.round(r.height)+' op'+c.opacity+' '+c.display+(e.style.backgroundImage?' bg':'')}).join(' | ')"))
    def studio():
        pg.evaluate("()=>{closeAll(); const x=document.querySelector('#auraScreen .closeb'); if(x&&document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click();}"); pg.wait_for_timeout(600); pg.evaluate("()=>{document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(2500); pg.evaluate("()=>{const x=document.querySelector('#studioScreen .closeb')||document.querySelector('#stcCadre .closeb'); if(x) x.click(); else closeAll();}"); pg.wait_for_timeout(1200)
    aura('1'); studio(); aura('2'); studio(); studio(); aura('3')
    b.close()
ims=[Image.open('scratchpad/v130/zone-%s.png'%n).convert('RGB') for n in '123']
for i in (1,2):
    d=ImageChops.difference(ims[0],ims[i]).convert('L'); print('écart 1 vs',i+1, sum(1 for v in d.getdata() if v>6))
Q=Image.new('RGB',(ims[0].width*3,ims[0].height)); [Q.paste(a.point(lambda v:min(255,v*4)),(ims[0].width*i,0)) for i,a in enumerate(ims)]; Q.resize((Q.width//3,Q.height//3)).save('scratchpad/v130/zone.png')
