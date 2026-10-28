import sys, os; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B, numpy as np, io
from PIL import Image
GRAVE='<span class="v35-e">A<span class="v35-acc" aria-hidden="true" style="top:-.06em;transform:translateX(-70%) scaleX(-1)">’</span></span>'
AIGU='<span class="v35-e">E<span class="v35-acc" aria-hidden="true">’</span></span>'
CAS=[('KDEUXIO',25,'<span style="display:inline-block;transform:skewX(-3deg)">DEUXIO</span>'),('À',29,GRAVE),('É',42,AIGU),('SEXP',29,'S’EXPLORE')]
JS="""async a=>{ const [html,fz,f]=a; document.querySelectorAll('#gEl,canvas[data-trace]').forEach(e=>e.remove()); const el=document.createElement('div'); el.id='gEl';
 el.style.cssText='position:fixed;left:40px;top:60px;width:340px;font:400 '+fz+'px/1.3 PromiLate;color:#291547;z-index:60;text-transform:uppercase'; el.innerHTML=html; document.body.appendChild(el);
 await document.fonts.load('400 '+fz+'px PromiLate'); window.__C=null; if(f<0) return 1; const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret; C.va(f); window.__C=C; return 1; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} document.body.style.background='#fff'}")
    pg.add_style_tag(content='#device{visibility:hidden!important}')
    clip={'x':30,'y':40,'width':360,'height':110}
    for nom,fz,h in CAS:
        h=h or nom
        pg.evaluate(JS,[h,fz,-1]); pg.wait_for_timeout(150); a=np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(int)
        res=[]
        for f in (0.9,0.97,0.995,0.99999):
            pg.evaluate(JS,[h,fz,f]); pg.wait_for_timeout(120); c=np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(int)
            res.append((f,int((np.abs(a-c)>40).sum())))
            if f==0.99999: Image.fromarray(np.concatenate([a,c],1).astype('uint8')).save('scratchpad/v170/fin-%s.png'%nom[:2].replace('’',''))
        pg.evaluate("()=>{ if(window.__C) window.__C.finir(); }"); pg.wait_for_timeout(120); d=np.asarray(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('L')).astype(int)
        print(nom[:12],fz,res,'après finir',int((np.abs(a-d)>40).sum()))
    b.close()
from PIL import Image as _I
for f in ('KD','À','É','SE'):
    im=np.asarray(_I.open('scratchpad/v170/fin-%s.png'%f)).astype(int); w=im.shape[1]//2; a=im[:,:w]; c=im[:,w:]
    print('grossiers',f, int(((a<100)&(c>200)|(a>200)&(c<100)).sum()))
