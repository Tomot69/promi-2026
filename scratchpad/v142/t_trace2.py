import sys, io
FICHIER = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
sys.argv = [sys.argv[0], FICHIER]
src = io.open('redteam_trace.py', encoding='utf-8').read()
tete, _ = src.split("    cx, cy = bo\n", 1)
essai = r'''
    cx, cy = bo
    def brut(x0, y0, x1, y1, r, duree=0.45, n=18):
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x0, y0, r), 'timestamp': T[0]})
        for i in range(1, n + 1):
            T[0] += duree / n; pg.wait_for_timeout(int(1000 * duree / n))
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, r), 'timestamp': T[0]})
        pg.wait_for_timeout(350); T[0] += .35
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]})
        pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente && !e.vlac && !e.vtan}", timeout=25000); pg.wait_for_timeout(500)
    nom = FICHIER.replace('.html','')
    for i, r in enumerate((5, 10, 20)):
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        brut(cx - 65, cy - 20, cx + 65, cy - 20, r)
        v = pg.evaluate("()=>{const e=_aura.etat(); return [e.lac,e.tan, (_aura.tracesGeo()||[]).length]}"); print(r, v)
        pg.screenshot(path='scratchpad/v142/trace-%s-r%d.png' % (nom, r), clip={'x': cx-150, 'y': cy-150, 'width': 300, 'height': 300})
    for i, (r, L) in enumerate(((10, 20), (10, 70))):
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        brut(cx - L, cy - 20, cx + L, cy - 20, r)
        pg.screenshot(path='scratchpad/v142/trace-%s-L%d.png' % (nom, L), clip={'x': cx-150, 'y': cy-150, 'width': 300, 'height': 300})
    pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
    T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx+10, 'y': cy-10, 'radiusX': 16, 'radiusY': 9, 'rotationAngle': 30, 'force': 1}], 'timestamp': T[0]})
    pg.wait_for_timeout(1200); T[0] += 1.2
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]}); pg.wait_for_timeout(3500)
    pg.screenshot(path='scratchpad/v142/trace-%s-appui.png' % nom, clip={'x': cx-150, 'y': cy-150, 'width': 300, 'height': 300})
    b.close()
'''
exec(compile(tete + essai, 't', 'exec'))
