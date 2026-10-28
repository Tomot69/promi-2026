import sys, os, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
car=sys.argv[1]; fr=[float(x) for x in sys.argv[2].split(',')]; fz=float(os.environ.get('FZ','29')); ech=float(os.environ.get('ECH','0.7466')); mod=os.environ.get('MOD','')
html=os.environ.get('HTML') or car; zoom=int(os.environ.get('Z','4')); out=os.environ.get('OUT','scratchpad/v170/frames2.png')
JS="""async a=>{ const [html,fz,ech,f]=a; let w=document.getElementById('gW'); if(!w){ w=document.createElement('div'); w.id='gW'; w.style.cssText='position:fixed;left:20px;top:20px;transform-origin:0 0;z-index:60;background:#fff;padding:0'; document.body.appendChild(w); }
 w.style.transform='scale('+ech+')'; w.innerHTML=''; const el=document.createElement('div'); el.id='gEl'; el.style.cssText='width:300px;font:400 '+fz+'px/1.25 PromiLate;color:#291547;padding:6px 10px'; el.innerHTML=html; w.appendChild(el);
 await document.fonts.load('400 '+fz+'px PromiLate'); if(f<0) return w.getBoundingClientRect().toJSON(); const C=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await C.pret; C.va(f); window.__C=C; return w.getBoundingClientRect().toJSON(); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{try{closeAll()}catch(e){} var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';}}"); pg.add_style_tag(content='#device{visibility:hidden!important}')
    if mod: pg.add_script_tag(url='http://127.0.0.1:8752/'+mod); pg.wait_for_timeout(300)
    if os.environ.get('CHEM'): pg.add_script_tag(url='http://127.0.0.1:8752/'+os.environ['CHEM']); pg.wait_for_timeout(300)
    ims=[]
    for f in fr:
        r=pg.evaluate(JS,[html,fz,ech,f]); pg.wait_for_timeout(80)
        clip={'x':r['x'],'y':r['y'],'width':min(r['width'],float(os.environ.get('CW','45'))),'height':r['height']}
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB'))
        pg.evaluate("()=>{ if(window.__C){ window.__C.stop(); window.__C=null; } }")
    W=sum(i.width for i in ims)+4*len(ims); H=max(i.height for i in ims); o=Image.new('RGB',(W,H),(200,60,60)); x=0
    for i in ims: o.paste(i,(x,0)); x+=i.width+4
    o=o.resize((o.width*zoom//3*1, o.height*zoom//3*1), Image.NEAREST) if zoom!=3 else o
    o.save(out); print(o.size)
    b.close()
