import sys, os, re; sys.path.insert(0,'.'); sys.argv=sys.argv[:1]
src=open('redteam_trace_lettres.py',encoding='utf-8').read(); src=src[:src.index('with sync_playwright() as p:')]; exec(src)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }")
    pg.evaluate(GEO_ECRAN,['R',42,0.7466,'pose']); pg.evaluate(GEO_ECRAN,['R',42,0.7466,'arme']); pg.evaluate(GEO_ECRAN,['R',42,0.7466,1/3])
    r=pg.evaluate("()=>{const e=document.getElementById('gEl'); const q=e.getBoundingClientRect(); return {cp:getComputedStyle(e).clipPath.slice(0,600), top:q.top, left:q.left, k:q.width/e.offsetWidth}}")
    print(r['top'], r['left'], r['k']); print(r['cp'])
    ys=[float(v) for v in re.findall(r'L[-\d.]+ ([-\d.]+)', r['cp'])]; print(sorted(set(round(y,2) for y in ys))[-8:])
    for y in sorted(set(ys))[-4:]: print(y, (r['top']+y*r['k'])*3)
    b.close()
