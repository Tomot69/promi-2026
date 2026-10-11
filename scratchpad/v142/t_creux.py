import sys, io
sys.argv = [sys.argv[0], 'app.html']
src = io.open('sauvegardes/redteam_trace-avant-v142.py', encoding='utf-8').read()
tete, _ = src.split("    cx, cy = bo\n", 1)
essai = r'''
    cx, cy = bo
    from PIL import Image
    W = Image.new('RGB', (900, 300), 'white')
    for i, r in enumerate((7, 11, 16)):
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(cx, cy - 10, r), 'timestamp': T[0]})
        pg.wait_for_timeout(1500); T[0] += 1.5
        print(r, pg.evaluate("()=>{const e=_aura.etat(); return JSON.stringify(e.emp||e).slice(0,300)}"))
        pg.screenshot(path='scratchpad/v142/creux-%d.png' % r, clip={'x': cx-150, 'y': cy-150, 'width': 300, 'height': 300})
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]}); pg.wait_for_timeout(3000)
        W.paste(Image.open('scratchpad/v142/creux-%d.png' % r).resize((300, 300)), (300 * i, 0))
    W.save('scratchpad/v142/creux-vue.png'); b.close()
'''
exec(compile(tete + essai, 't', 'exec'))
