import sys, math, re, io
src = io.open('redteam_trace.py', encoding='utf-8').read()
# on reprend les aides du juge (jusqu'à `cx, cy = bo`) et on joue nos essais
tete, _ = src.split("    cx, cy = bo\n", 1)
essai = r'''
    cx, cy = bo
    for r in (5, 10, 20):
        t = geste(cx - 65, cy - 30, cx + 65, cy - 30, r=r)
        print('rayon', r, court(t), 'arcs', len(t.get('geo') or []), 'w', sorted(set(round(a['w'],3) for a in (t.get('geo') or [])))[:4], flush=True)
    c = geste(cx - 20, cy - 30, cx + 20, cy - 30, r=10); print('court 40', court(c), flush=True)
    l = geste(cx - 70, cy - 30, cx + 70, cy - 30, r=10); print('long 140', court(l), flush=True)
    for r in (6, 14):
        e = appui(cx + 20, cy - 10, r, 1.2); print('appui', r, court(e), 'arcs', len(e.get('geo') or []), flush=True)
    pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(400)
    t = geste(cx - 65, cy - 30, cx + 65, cy + 20, r=10); 
    pg.screenshot(path='scratchpad/v142/trace-essai.png', clip={'x': cx-150, 'y': cy-150, 'width': 300, 'height': 300})
    print('err', er)
    b.close()
'''
exec(compile(tete + essai, 't', 'exec'))
