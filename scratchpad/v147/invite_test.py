import sys, time; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
OUT=sys.argv[1]; V=sys.argv[2] if len(sys.argv)>2 else 'A'; TH=sys.argv[3] if len(sys.argv)>3 else 'clair'; NAT=sys.argv[4] if len(sys.argv)>4 else 'promi'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,has_touch=True,is_mobile=True)
    ctx.add_init_script("try{Object.defineProperty(Navigator.prototype,'webdriver',{get:function(){return false},configurable:true});}catch(e){}")
    pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:8752/promi-invite-variantes.html?v=%s&th=%s&nat=%s'%(V,TH,NAT))
    t0=time.time()
    for i in range(80):
        pg.wait_for_timeout(250)
        e=pg.evaluate("()=>window._invite.etat()")
        if e: break
    print('armé après', round(time.time()-t0,1),'s', e)
    vrai=pg.evaluate("()=>{ try{ return localStorage.getItem('promi_state')===null; }catch(e){ return 'err'; } }")
    print('vrai stockage intact (aucun promi_state):', vrai)
    f=pg.frames[1] if len(pg.frames)>1 else None
    info=pg.evaluate("()=>{ const w=window._invite.cadre().contentWindow, d=w.document, cv=d.getElementById('dpTrameCv'), ov=d.getElementById('invCv'); const r=cv.getBoundingClientRect(), q=ov&&ov.getBoundingClientRect(); return {trait:cv.getAttribute('data-trait'), cv:[r.left,r.top,r.width,r.height], ov:q&&[q.left,q.top,q.width,q.height], dp:d.getElementById('detailPoster').className.slice(0,80), titre:(d.getElementById('dptTitre')||{}).textContent} }")
    print(info)
    pg.wait_for_timeout(3000)
    pg.evaluate("()=>{ window.__lent=1; }")
    # figer : on rejoue l'image B à t=500 ms (le chevron au plus loin) par l'horloge de la page — capture sur une pause de 120 ms
    for k,ms in enumerate([300,560]):
        pg.wait_for_timeout(ms if k==0 else ms-300)
        pg.screenshot(path='%s/%s-%s-%s-%d.png'%(OUT,V,TH,NAT,k), clip={'x':0,'y':200,'width':390,'height':200})
    pg.wait_for_timeout(1500); print('après passe 1', pg.evaluate("()=>window._invite.etat()"), pg.evaluate("()=>document.getElementById('mes').textContent"))
    print('erreurs', errs[:3])
    b.close()
