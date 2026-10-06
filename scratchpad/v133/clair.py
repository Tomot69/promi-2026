from playwright.sync_api import sync_playwright
from PIL import Image
import sys
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
URL=sys.argv[1] if len(sys.argv)>1 else 'app.html'; TAG=sys.argv[2] if len(sys.argv)>2 else 'ap'
OUV=[('promi',"openDetail(promises.filter(q=>q.title==='nager le mardi')[0].id)"),('promi-at',"openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id)"),('chiche',"openDetail(promises.filter(q=>q.chiche&&!q.done&&!q.draft)[0].id)"),('cercle',"openEssaim('potager')"),('promi-tenu',"openDetail(promises.filter(q=>q.done&&!q.chiche&&!q.nuee)[0].id)")]
with sync_playwright() as p:
    b=p.webkit.launch(); ims=[]
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/'+URL); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('light');}"); pg.wait_for_timeout(500)
    for nom,js in OUV:
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(400); pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(3000)
        info=pg.evaluate("""()=>{ const P=document.getElementById('detailPoster'), D=document.getElementById('device').getBoundingClientRect(); const out={cls:P.className.split(' ').filter(c=>/^dp-|etat|tenu|light/.test(c)).join(' ')};
          const pt=(x,y)=>{ let e=document.elementFromPoint(D.left+x,D.top+y); const ch=[]; while(e&&e!==document.body){ const c=getComputedStyle(e).backgroundColor; if(c!=='rgba(0, 0, 0, 0)'){ ch.push((e.id||e.className.toString().slice(0,24))+' '+c); break;} e=e.parentElement;} return ch[0] };
          out.corps500=pt(380,520); out.corps700=pt(380,720); out.barre=pt(200,810);
          const cs=getComputedStyle(P); out.posterBg=cs.backgroundColor;
          out.textes=['dptQui','dptTitre','dptEtat','dptNat'].map(i=>{const e=document.getElementById(i); return e? i+' '+getComputedStyle(e).color : i+' —'});
          out.disques=[...P.querySelectorAll('canvas')].filter(c=>{const r=c.getBoundingClientRect(); return r.width>20&&r.width<110&&Math.abs(r.width-r.height)<2}).slice(0,3).map(c=>[c.id||c.className, Math.round(c.getBoundingClientRect().width), getComputedStyle(c).boxShadow, getComputedStyle(c).outline, c.getAttribute('data-filet')]);
          return out }""")
        print(nom, info)
        f=SC+'cl-%s-%s.png'%(TAG,nom); pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844}); ims.append(f)
    P=Image.new('RGB',(400*len(ims),844),(255,255,255))
    for i,f in enumerate(ims): P.paste(Image.open(f).resize((390,844)),(i*400,0))
    P.save(SC+'clair-%s.png'%TAG); b.close()
