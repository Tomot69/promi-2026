# ce qui se peint autour de la Pelote : capture, puis carte des écarts au fond (amplifiés)
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'; TAG = sys.argv[2] if len(sys.argv)>2 else 'apres'
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('dark','light'):
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t)}", th); pg.wait_for_timeout(500)
        pg.evaluate("""()=>{var b=[...document.querySelectorAll('#device *')].find(e=>e.children.length<4&&/^\\s*AURA\\s*$/i.test(e.textContent)&&e.getBoundingClientRect().height>0); (b.closest('button,[role=button],.acc-b,a')||b).click();}""")
        for i,ms in enumerate((900, 3500)):
            pg.wait_for_timeout(ms)
            f='scratchpad/v125/zone-%s-%s-%d.png' % (TAG, th, i)
            pg.screenshot(path=f, clip={'x':20,'y':44+90,'width':390,'height':400})
            im=Image.open(f).convert('RGB'); px=im.load(); W,H=im.size; fond=px[6,6]
            out=Image.new('RGB',(W,H)); o=out.load()
            for y in range(H):
                for x in range(W):
                    c=px[x,y]; d=max(abs(c[0]-fond[0]),abs(c[1]-fond[1]),abs(c[2]-fond[2]))
                    o[x,y]=(min(255,d*24),)*3 if d<10 else (255,80,40)
            out.save(f.replace('.png','-ecart.png'))
        print(th, pg.evaluate("""()=>{ const sc=document.getElementById('auraScreen'); const bo=document.querySelector('#auraScreen .au-bo').getBoundingClientRect(); const r=[];
          sc.querySelectorAll('*').forEach(e=>{ const q=e.getBoundingClientRect(); if(!q.width||!q.height) return; if(q.bottom<bo.top-60||q.top>bo.bottom+120) return; const s=getComputedStyle(e);
            if(e.tagName==='CANVAS'|| (s.backgroundImage&&s.backgroundImage!=='none') || (s.backgroundColor!=='rgba(0, 0, 0, 0)') || s.boxShadow!=='none' || s.filter!=='none') r.push((e.id||e.className||e.tagName)+' '+e.tagName+' '+Math.round(q.left)+','+Math.round(q.top)+' '+Math.round(q.width)+'×'+Math.round(q.height)+' op '+s.opacity+' vis '+s.visibility+' bg '+s.backgroundColor+' '+(s.backgroundImage||'').slice(0,60)+' sh '+s.boxShadow.slice(0,40)); });
          return r.join('\\n'); }"""))
        ctx.close()
    b.close()
