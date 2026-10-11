import sys, io
F = sys.argv[1]; sys.argv = [sys.argv[0], F]
src = io.open('sauvegardes/redteam_trace-avant-v142.py', encoding='utf-8').read().replace("device_scale_factor=2", "device_scale_factor=3")
tete, _ = src.split("    cx, cy = bo\n", 1)
essai = r'''
    cx, cy = bo; nom = F.replace('.html', '')
    def g(L, r, k):
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        y = cy - 10; x0 = cx - L; T[0] += 5
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x0, y, r), 'timestamp': T[0]})
        for i in range(1, 19):
            T[0] += .025; pg.wait_for_timeout(25); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x0 + L * i / 18, y, r), 'timestamp': T[0]})
        pg.wait_for_timeout(350); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]})
        pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente && !e.vlac && !e.vtan}", timeout=25000); pg.wait_for_timeout(600)
        pg.screenshot(path='scratchpad/v142/pt-%s-%s.png' % (nom, k), clip={'x': cx-130, 'y': cy-130, 'width': 260, 'height': 260})
    g(110, 6, 'r06'); g(110, 12, 'r12'); g(110, 18, 'r18'); g(30, 10, 'L030'); g(100, 10, 'L100')
    pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': cx, 'y': cy - 10, 'radiusX': 16, 'radiusY': 9, 'rotationAngle': 0, 'force': 1}]}); pg.wait_for_timeout(1200)
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(4500)
    pg.screenshot(path='scratchpad/v142/pt-%s-appui.png' % nom, clip={'x': cx-130, 'y': cy-130, 'width': 260, 'height': 260}); b.close()
'''
exec(compile(tete + essai, 't', 'exec'))
