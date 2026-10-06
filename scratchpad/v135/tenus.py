from playwright.sync_api import sync_playwright
from PIL import Image
import sys
TAG=sys.argv[1]
SC='scratchpad/v135/'
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}",th); pg.wait_for_timeout(500)
        # un Cercle dont toutes les paroles sont tenues : existe-t-il un état « tenu » ?
        for nom,js in (('promi','openDetail(125)'),('chiche','openDetail(129)'),('cercle',"promises.forEach(q=>{if(q.nuee==='potager'){q.status='tenu';q.done=true}}); try{syncAll()}catch(e){} openEssaim('potager')")):
            pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(500); pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(3200)
            info=pg.evaluate("""()=>{ const P=document.getElementById('detailPoster'), D=document.getElementById('device').getBoundingClientRect(); const cs=getComputedStyle(P);
              const pt=(x,y)=>{ let e=document.elementFromPoint(D.left+x,D.top+y); while(e&&e!==document.body){ const c=getComputedStyle(e).backgroundColor; if(c!=='rgba(0, 0, 0, 0)') return (e.id||String(e.className).slice(0,20))+' '+c; e=e.parentElement;} };
              const tx=i=>{const e=document.getElementById(i); return e&&e.getClientRects().length? getComputedStyle(e).color:null};
              return {corps:cs.backgroundColor, bas:pt(380,600), barre:pt(200,810), qui:tx('dptQui'), titre:tx('dptTitre'), etat:tx('dptEtat')||tx('dptMeta'), filetTrait:[...P.querySelectorAll('canvas[data-filet-trait]')].map(c=>c.getAttribute('data-filet-trait')).join('')} }""")
            print(TAG,th,nom,info)
            pg.screenshot(path=SC+'%s-%s-%s.png'%(TAG,nom,th), clip={'x':20,'y':44,'width':390,'height':844})
        ctx.close()
    b.close()
