import sys
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'; T=sys.argv[2] if len(sys.argv)>2 else 'x'
clip={'x':20,'y':44,'width':390,'height':844}
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','dark')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:120])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); Toile.setTheme('pixel');}"); pg.wait_for_timeout(4000)
    S=[]
    pg.screenshot(path='scratchpad/v130/px-%s-toile.png'%T,clip=clip); S.append('toile')
    pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex();}"); pg.wait_for_timeout(3000); pg.screenshot(path='scratchpad/v130/px-%s-index.png'%T,clip=clip); S.append('index')
    pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}"); pg.wait_for_timeout(3000); pg.screenshot(path='scratchpad/v130/px-%s-fiche.png'%T,clip=clip); S.append('fiche')
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3000); pg.screenshot(path='scratchpad/v130/px-%s-fil.png'%T,clip=clip); S.append('fil')
    b.close()
ims=[Image.open('scratchpad/v130/px-%s-%s.png'%(T,s)).resize((390,844)) for s in S]
Q=Image.new('RGB',(390*4,844)); [Q.paste(a,(390*i,0)) for i,a in enumerate(ims)]; Q.save('scratchpad/v130/px-%s.png'%T)
