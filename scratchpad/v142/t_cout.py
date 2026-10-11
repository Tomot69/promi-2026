import sys, io
F = sys.argv[1]; sys.argv = [sys.argv[0], F]
src = io.open('sauvegardes/redteam_trace-avant-v142.py', encoding='utf-8').read()
tete, _ = src.split("    cx, cy = bo\n", 1)
essai = r'''
    cx, cy = bo
    pg.evaluate("()=>{ window.__R=[]; let d=null; (function f(){ const r=_aura.etat().retouche; if(r && r!==d && (!d || r.ms!==d.ms || r.points!==d.points)){ d=r; __R.push([r.points,r.ms]); } requestAnimationFrame(f); })(); }")
    import random
    for k in range(14):
        y = cy - 60 + k * 9; T[0] += 5
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(cx - 80, y, 11), 'timestamp': T[0]})
        for i in range(1, 25):
            T[0] += .016; pg.wait_for_timeout(16)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(cx - 80 + 160 * i / 24, y, 11), 'timestamp': T[0]})
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]}); pg.wait_for_timeout(500)
    R = pg.evaluate("()=>__R"); ms = sorted(r[1] for r in R)
    print(F, 'retouches vues', len(R), 'traces', pg.evaluate("()=>_aura.tracesGeo().length"), 'ms médiane', ms[len(ms)//2] if ms else None, 'p95', ms[int(len(ms)*.95)] if ms else None, 'max', ms[-1] if ms else None, 'points méd', sorted(r[0] for r in R)[len(R)//2] if R else None)
    b.close()
'''
exec(compile(tete + essai, 't', 'exec'))
