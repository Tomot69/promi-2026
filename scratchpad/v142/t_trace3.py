import sys, io
FICHIER = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
sys.argv = [sys.argv[0], FICHIER]
src = io.open('redteam_trace.py', encoding='utf-8').read()
tete, _ = src.split("    cx, cy = bo\n", 1)
essai = r'''
    cx, cy = bo
    BOITE = r"""()=>{ const a=window.__i1, b=window.__i2, c=document.getElementById('auBoule'), W=c.width, k=W/296; const col={}, lig={}; let n=0;
      for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const i=(y*W+x)*4; if(!a[i+3]||!b[i+3]) continue; const e=Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]); if(e>36){ col[x]=(col[x]||0)+1; lig[y]=(lig[y]||0)+1; n++; } }
      const et=(o,seuil)=>{ const K=Object.keys(o).map(Number).filter(v=>o[v]>=seuil).sort((p,q)=>p-q); return K.length? [K[0]/k, K[K.length-1]/k, (K[K.length-1]-K[0])/k] : null; };
      const mx=Math.max(1,...Object.values(lig)), my=Math.max(1,...Object.values(col));
      return {n:n, aire:n/(k*k), x:et(col, my*0.35), y:et(lig, mx*0.35)}; }"""
    def essaie(x0, x1, r, y=None):
        y = cy - 10 if y is None else y
        pg.evaluate("()=>{ _aura.relisse(); _aura.fige(true); _aura.vue(3.1,0.2); }"); pg.wait_for_timeout(500)
        T[0] += 5; cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': tp(x0, y, r), 'timestamp': T[0]})
        n = 18
        for i in range(1, n + 1):
            T[0] += .45 / n; pg.wait_for_timeout(25)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': tp(x0 + (x1 - x0) * i / n, y, r), 'timestamp': T[0]})
        pg.wait_for_timeout(350); T[0] += .35
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': [], 'timestamp': T[0]})
        pg.wait_for_function("()=>{const e=_aura.etat(); return !e.emp && !e.attente && !e.vlac && !e.vtan}", timeout=25000); pg.wait_for_timeout(500)
        v = pg.evaluate("()=>{const e=_aura.etat(); return [e.lac,e.tan]}")
        geo = pg.evaluate("()=>_aura.tracesGeo()")
        pg.evaluate(GARDE, 1); pg.evaluate("([l,t])=>{ _aura.relisse(); _aura.vue(l,t); }", v); pg.wait_for_timeout(500); pg.evaluate(GARDE, 2)
        t = pg.evaluate(BOITE); t['arcs'] = len(geo); t['Ltot'] = round(sum(a['L'] for a in geo) * 116, 1); t['w'] = round(max([a['w'] for a in geo] or [0]) * 116, 1); return t
    for r in (6, 12, 18):
        print('rayon', r, essaie(cx - 110, cx, r), flush=True)
    for L in (30, 60, 120):
        print('trajet', L, essaie(cx - L, cx, 10), flush=True)
    b.close()
'''
exec(compile(tete + essai, 't', 'exec'))
