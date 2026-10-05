import sys, json
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
LIT=r"""async (q)=>{ const T=q.t; const out={}; const lire=()=>({
   index:[...document.querySelectorAll('#indexList .s4-ti')].map(e=>e.textContent.trim()).filter(t=>t===T).length,
   indexN:document.querySelectorAll('#indexList .s4-carte').length,
   fil:(document.getElementById('feedList')||{innerText:''}).innerText.includes(T), 
   aura:(document.getElementById('auraScreen')||{innerText:''}).innerText.replace(/\s+/g,' ').slice(0,0),
   moisson:[...document.querySelectorAll('#auraScreen .au-mo *')].filter(e=>e.children.length===0).map(e=>e.textContent.trim()).filter(Boolean).join(' | ').slice(0,300),
   chiffres:[...document.querySelectorAll('#auraScreen .au-lg *, #auraScreen [class*=chif] *')].filter(e=>e.children.length===0&&/^\d+$/.test(e.textContent.trim())).map(e=>e.textContent.trim()).join(' '),
   cercle:(document.getElementById('detailPoster')||{innerText:''}).innerText.includes(T) });
  await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); out.image=lire(); await new Promise(r=>setTimeout(r,1500)); out.tard=lire(); return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    T='parole du juge'
    # on ouvre chaque écran une fois (ils sont bâtis), puis on revient
    for js in ("()=>{closeAll(); ouvrirIndex();}","()=>{closeAll(); document.getElementById('filBtn').click();}","()=>{closeAll(); document.getElementById('souffleBtn').click();}","()=>{closeAll(); openEssaim('potager');}","()=>{closeAll(); const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"):
        pg.evaluate(js); pg.wait_for_timeout(1800)
    n0=pg.evaluate("()=>promises.length")
    # planter par la vraie page + (dans le Cercle « potager »)
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3200)
    pg.evaluate("(t)=>{ const f=document.getElementById('fTitle'); f.value=t; f.dispatchEvent(new Event('input',{bubbles:true})); document.getElementById('addPromi').click(); }", T); pg.wait_for_timeout(2500)
    print('plantée :', pg.evaluate("(t)=>[promises.length, promises.filter(p=>p.title===t).map(p=>p.status+'/'+(p.nuee||'-')+'/'+p.draft)]", T), 'avant', n0)
    def tour(lab):
        for nom,js in (('Index',"()=>{closeAll(); ouvrirIndex();}"),('Fil',"()=>{closeAll(); document.getElementById('filBtn').click();}"),('Aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}")):
            pg.evaluate(js); r=pg.evaluate(LIT,{'t':T}); k={'Index':['index','indexN'],'Fil':['fil'],'Aura':['chiffres','moisson']}[nom]
            print('  %s · %s : image suivante %s · 1,5 s après %s' % (lab, nom, {x:r['image'][x] for x in k}, {x:r['tard'][x] for x in k}))
            pg.evaluate("()=>{closeAll(); const x=document.querySelector('#auraScreen .closeb'); if(x&&document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click();}"); pg.wait_for_timeout(700)
    tour('après planter')
    pg.evaluate("(t)=>{ const p=promises.find(q=>q.title===t); closeAll(); openDetail(p.id); }", T); pg.wait_for_timeout(2500)
    print('tenir :', pg.evaluate("(t)=>{ const p=promises.find(q=>q.title===t); try{ if(window._tenirParole){ _tenirParole(p.id); return 'par _tenirParole'; } }catch(e){} return Object.keys(window).filter(k=>/tenir|keep/i.test(k)).slice(0,30).join(' '); }", T))
    b.close()
