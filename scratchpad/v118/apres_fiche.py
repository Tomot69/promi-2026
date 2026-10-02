from playwright.sync_api import sync_playwright
J = """()=>{ const o={}; for(const id of ['createBtn','souffleBtn','settingsBtn','shareBtn','toileCv']){ const e=document.getElementById(id), r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); o[id]=h?(h.id||h.className):'rien'; }
  const dp=document.getElementById('detailPoster'), c=getComputedStyle(dp), r=dp.getBoundingClientRect(); o.poster={cls:dp.className, disp:c.display, vis:c.visibility, op:c.opacity, pe:c.pointerEvents, tr:c.transform, y:Math.round(r.top), h:Math.round(r.height)};
  const t=document.getElementById('dpdTog'); if(t){ const c2=getComputedStyle(t), r2=t.getBoundingClientRect(); o.tog={pe:c2.pointerEvents, vis:c2.visibility, op:c2.opacity, y:Math.round(r2.top), h:Math.round(r2.height)}; } return o; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate('()=>{var o=document.getElementById("promiOnb");if(o){o.classList.add("gone");o.style.display="none";}}')
    print('frais      ', pg.evaluate(J))
    pg.evaluate("()=>{const p=promises.filter(q=>!q.draft&&!q.req)[0]; openDetail(p.id);}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(2500)
    print('après fiche', pg.evaluate(J))
    pg.screenshot(path='scratchpad/v118/apres_fiche.png')
    # au doigt : le + répond-il ?
    r = pg.evaluate("()=>{const r=document.getElementById('souffleBtn').getBoundingClientRect(); return {x:r.left+r.width/2,y:r.top+r.height/2}}")
    pg.touchscreen.tap(r['x'], r['y']); pg.wait_for_timeout(1500)
    print('toucher AURA après une fiche → aura ouverte :', pg.evaluate("()=>{const a=document.getElementById('auraScreen'); const r=a.getBoundingClientRect(); return a.classList.contains('show')+' y='+Math.round(r.top)}"))
    b.close()
