import re, sys
from playwright.sync_api import sync_playwright
POINTS=re.search(r'POINTS=r"""(.*?)"""', open('redteam_toucher.py',encoding='utf-8').read(), re.S).group(1)
M=sys.argv[1].split(',') if len(sys.argv)>1 else ['encre','ramage','volubilis','madrure','guingois','touffe','chamade','mascaret']
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} window.__L=[]; const st=document.getElementById('stage')||document.querySelector('.stage'); ['pointerdown','pointerup','pointercancel'].forEach(t=>document.addEventListener(t,e=>{ window.__L.push([t, Math.round(e.timeStamp), Math.round(performance.now())]); },true)); }")
    for m in M:
        pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m);}", m); pg.wait_for_timeout(6000 if m=='ramage' else 3500)
        P=pg.evaluate(POINTS); res=[]
        for q in P['pts']:
            pg.evaluate("()=>{window.__L.length=0}")
            pg.mouse.move(q['x'],q['y']); pg.mouse.down(); pg.wait_for_timeout(110); pg.mouse.up(); pg.wait_for_timeout(1600)
            L=pg.evaluate("()=>window.__L"); ouv=pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
            d=[x for x in L if x[0]=='pointerdown'][:1]; u=[x for x in L if x[0]=='pointerup'][:1]
            res.append('%s appui %s ms (événements) · traité %s ms après · fiche %s'%(q['titre'][:14], (u[0][1]-d[0][1]) if d and u else '?', (u[0][2]-d[0][2]) if d and u else '?', 'OUVERTE' if ouv else 'NON'))
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(900)
        print(m, ' | '.join(res))
    b.close()
