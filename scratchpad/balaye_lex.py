import sys,re
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8752/app.html'
DUMP="""()=>{const dv=document.getElementById('device'),D=dv.getBoundingClientRect();const o=new Set();
 const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
 while(n=w.nextNode()){const t=n.textContent.replace(/\\s+/g,' ').trim();if(!t||!/Nu[ée]e|NU[ÉE]E|Cercle|CERCLE|cercle/.test(t))continue;const e=n.parentElement;if(!e||e.closest('script,style'))continue;
  const r=e.getBoundingClientRect();if(!r.width||r.bottom<D.top||r.top>D.bottom||r.right<D.left||r.left>D.right)continue;const s=getComputedStyle(e);if(s.visibility==='hidden'||+s.opacity===0)continue;
  let p=e,ok=true;while(p&&p!==document.body){const q=getComputedStyle(p);if(q.display==='none'||+q.opacity===0){ok=false;break}p=p.parentElement}if(ok)o.add(t.slice(0,140));}
 document.querySelectorAll('[aria-label],[placeholder]').forEach(e=>{const t=(e.getAttribute('aria-label')||'')+' '+(e.getAttribute('placeholder')||'');if(/Nu[ée]e|Cercle/.test(t))o.add('@'+t.trim())});
 return [...o]}"""
def run(pg,nom,js,wait=1400):
    try: pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(300); pg.evaluate(js); pg.wait_for_timeout(wait)
    except Exception as e: print('!!',nom,str(e)[:120]); return
    print('──',nom); [print('   ',t) for t in pg.evaluate(DUMP)]
with sync_playwright() as p:
    b=p.webkit.launch()
    for prem in (False,True):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(7000)
        pg.evaluate("v=>setPremium(v)",prem); print('\n════ premium',prem)
        run(pg,'accueil',"()=>{}")
        run(pg,'+ choix',"()=>{document.getElementById('createBtn').click()}")
        for k in ('promi','chiche','nuee'):
            run(pg,'page + '+k,"k=>{document.getElementById('createBtn').click();setTimeout(()=>{const t=document.querySelector('#createSheet [data-kind=\"'+k+'\"],.acc-pil[data-k=\"'+k+'\"]');t&&t.click()},500)}".replace('k=>','()=>').replace("'+k+'",k),2200)
        run(pg,'Index',"()=>{(window.openIndex||(()=>document.getElementById('indexBtn').click()))()}")
        run(pg,'Fil',"()=>{document.getElementById('filBtn').click()}")
        run(pg,'fiche Promi',"()=>{openDetail(promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0].id)}")
        run(pg,'Peaufiner Promi',"()=>{openDetail(promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0].id);setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog');x&&x.click()},900)}",2600)
        run(pg,'fiche Nuée',"()=>{openNueeDetail(Object.keys(NUE).filter(k=>k!=='soi')[0])}",2000)
        run(pg,'Peaufiner Nuée',"()=>{openNueeDetail(Object.keys(NUE).filter(k=>k!=='soi')[0]);setTimeout(()=>{const x=document.querySelector('#detailPoster .dpd-tog,#dpBarre');x&&x.click()},1200)}",2800)
        run(pg,'Aura',"()=>{document.getElementById('souffleBtn').click();setTimeout(()=>{const s=document.getElementById('auraScreen');s.scrollTop=9999},1500)}",2600)
        run(pg,'aide Aura',"()=>{document.getElementById('souffleBtn').click();setTimeout(()=>{const h=document.getElementById('auraHelp');h&&h.classList.add('show');setTimeout(()=>{h.scrollTop=0},100)},800)}",2000)
        run(pg,'Réglages',"()=>{document.getElementById('settingsBtn').click()}")
        run(pg,'offre',"()=>{ouvreCercle()}",1500)
        run(pg,'Studio',"()=>{document.getElementById('studioBtn')?document.getElementById('studioBtn').click():openStudio()}",2000)
        run(pg,'Partager',"()=>{document.getElementById('shareBtn').click()}",2000)
        print('pageerror:',errs[:3]); ctx.close()
