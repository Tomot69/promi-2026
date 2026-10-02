from playwright.sync_api import sync_playwright
ETAT = r"""()=>{ const cs=document.getElementById('createSheet'), g=cs.querySelector('.pp-garder'); const r=g?g.getBoundingClientRect():null;
  const h=r&&r.width?document.elementFromPoint(r.left+r.width/2,r.top+r.height/2):null;
  return {lien:g?getComputedStyle(g).display+' '+Math.round(r.width)+'×'+Math.round(r.height)+' @'+Math.round(r.left)+','+Math.round(r.top):'absent', sous:h?(h.className||h.id):'—',
          cibles:[...document.querySelectorAll('#addDraft,#csDraft,#csGarder,[data-garder],.cs-draft')].map(e=>(e.id||e.className)+':'+getComputedStyle(e).display),
          drafts:promises.filter(p=>p.draft).length, cls:cs.className, titre:(document.getElementById('fTitle')||{}).value, feuilles:[...document.querySelectorAll('.sheet.show,.screen.show,.poster.show')].map(e=>e.id)} }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, has_touch=True); pg = ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate('()=>{var o=document.getElementById("promiOnb");if(o){o.classList.add("gone");o.style.display="none";}}')
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"); pg.wait_for_timeout(2500)
    print('vide   ', pg.evaluate(ETAT)); print('avant :', pg.evaluate("()=>promises.length"))
    r = pg.evaluate("()=>{const m=document.querySelector('#csPhrase [data-ph=titre]'); const q=m.getClientRects()[0]; return {x:q.left+q.width/2,y:q.top+q.height/2}}")
    pg.touchscreen.tap(r['x'], r['y']); pg.wait_for_timeout(900); pg.keyboard.type('aller voir la mer'); pg.wait_for_timeout(400); pg.keyboard.press('Enter'); pg.wait_for_timeout(1500)
    e = pg.evaluate(ETAT); print('écrit  ', e)
    pg.screenshot(path='scratchpad/v118/garder-ecrit.png')
    g = pg.evaluate("()=>{const g=document.querySelector('#createSheet .pp-garder'); const r=g.getBoundingClientRect(); return r.width?{x:r.left+r.width/2,y:r.top+r.height/2}:null}")
    if g:
        pg.touchscreen.tap(g['x'], g['y']); pg.wait_for_timeout(4000); print('touché ', pg.evaluate(ETAT)); print('gardés :', pg.evaluate("()=>promises.filter(p=>p.draft).map(p=>p.title)"), '| tous :', pg.evaluate("()=>promises.length"), pg.evaluate("()=>promises.some(p=>p.title==='aller voir la mer')")); pg.screenshot(path='scratchpad/v118/garder-touche.png')
    b.close()
