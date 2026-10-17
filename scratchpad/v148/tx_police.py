from playwright.sync_api import sync_playwright
JS = r"""async ()=>{ await document.fonts.ready; const police='40px Gilbert, system-ui', mot='Parole tenue !';
 const a=document.createElement('canvas'); document.body.appendChild(a); const ga=a.getContext('2d'); ga.font=police;
 const b=document.createElement('canvas'); const gb=b.getContext('2d'); gb.font=police;
 const o=new OffscreenCanvas(10,10).getContext('2d'); o.font=police;
 const s=document.createElement('canvas'); const gs=s.getContext('2d'); gs.font='40px system-ui';
 const r={dansDoc:ga.measureText(mot).width, detache:gb.measureText(mot).width, offscreen:o.measureText(mot).width, systeme:gs.measureText(mot).width, gilbertCharge:document.fonts.check('40px Gilbert')}; a.remove(); return r; }"""
with sync_playwright() as p:
    for nom, L in (('chromium', p.chromium), ('webkit', p.webkit)):
        b = L.launch(); pg = b.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(3000)
        print(nom, pg.evaluate(JS)); b.close()
