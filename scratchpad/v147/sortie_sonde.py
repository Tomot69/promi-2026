import sys, json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/app.html'
def toucher(cdp, pg, x, y):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(70); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
def centre(pg, sel): return pg.evaluate("(s)=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return r.width>4?[r.left+r.width/2,r.top+r.height/2]:null;}", sel)
TRACE_FINI = "()=>![...document.querySelectorAll('#onbV .onbv-a')].some(e=>getComputedStyle(e).display!=='none' && (e.style.visibility==='hidden' || (e.style.clipPath && e.style.clipPath!=='none')))"
def attend(pg):
    for _ in range(50):
        if pg.evaluate(TRACE_FINI): break
        pg.wait_for_timeout(150)
def trace(pg, cdp):
    z = pg.evaluate("()=>{const c=document.getElementById('onbTrait'); if(!c) return null; const r=c.getBoundingClientRect(); return {l:r.left,t:r.top,k:r.width/390,dep:c.getAttribute('data-depart'),arr:c.getAttribute('data-arrivee')};}")
    a = [float(v) for v in z['dep'].split(',')]; e = [float(v) for v in z['arr'].split(',')]
    x0, y0, x1, y1 = z['l'] + a[0] * z['k'], z['t'] + a[1] * z['k'], z['l'] + (e[0] + 6) * z['k'], z['t'] + e[1] * z['k']
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x0, 'y': y0}]}); pg.wait_for_timeout(90)
    for i in range(1, 25):
        u = i / 24.0; cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x0 + (x1 - x0) * u, 'y': y0 + (y1 - y0) * u - 14 * z['k'] * (1 - abs(2 * u - 1))}]}); pg.wait_for_timeout(22)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
VIS = """()=>{ const v=document.getElementById('onbV'); if(!v) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  return [...v.querySelectorAll('*')].filter(e=>{ const c=getComputedStyle(e); const r=e.getBoundingClientRect(); return c.display!=='none' && c.visibility!=='hidden' && r.width>2 && r.height>2 && (e.children.length===0 || e.tagName==='CANVAS'); })
    .map(e=>{ const r=e.getBoundingClientRect(); return [e.tagName+'.'+String(e.className).slice(0,24), Math.round((r.top-D.top)/k), Math.round(r.height/k), (e.textContent||'').trim().slice(0,30)]; }); }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True); pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(URL); pg.wait_for_timeout(6500); attend(pg)
    c = centre(pg, '#onbPh'); toucher(cdp, pg, c[0], c[1]); pg.wait_for_timeout(300); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300)
    pg.keyboard.press('Enter'); pg.wait_for_timeout(900); attend(pg)
    pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(900); attend(pg)
    trace(pg, cdp); pg.wait_for_timeout(6400)
    toucher(cdp, pg, 195, 300); pg.wait_for_timeout(2500); attend(pg); toucher(cdp, pg, 195, 300); pg.wait_for_timeout(1500); attend(pg)
    print('AVANT', json.dumps(pg.evaluate(VIS), ensure_ascii=False))
    c = centre(pg, '.onbv-compte .tard'); print('tard', c)
    pg.evaluate("""()=>{ window.__S=[]; const t0=performance.now(); (function f(){ const v=document.getElementById('onbV'); const pl=document.getElementById('accPlat'), br=document.getElementById('accBarre');
       window.__S.push([Math.round(performance.now()-t0), v?[...v.children].filter(e=>getComputedStyle(e).visibility!=='hidden' && getComputedStyle(e).display!=='none').map(e=>String(e.className).slice(0,12)+':'+(e.style.transform||'')).join('|')+' clip '+(v.style.clipPath||''):'(retiré)', pl?pl.style.transform:'', br?br.style.transform:'', document.getElementById('guide')?1:0]);
       if(performance.now()-t0<3500) requestAnimationFrame(f); })(); }""")
    if c: toucher(cdp, pg, c[0], c[1])
    pg.wait_for_timeout(3700)
    S = pg.evaluate("()=>window.__S")
    for s in S[::3]: print(s)
    b.close()
