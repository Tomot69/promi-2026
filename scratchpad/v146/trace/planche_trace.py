# planche_trace.py — LE TRACÉ VU DE PRÈS : pour quelques glyphes, huit instants du tracé (WebKit, échelle 3), côte à côte.
#   python3 planche_trace.py "lhaeostf" [h|b] [sortie.png]      (une ligne par glyphe, une colonne par instant)
import sys, io
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image
chars = sys.argv[1] if len(sys.argv) > 1 else 'lhaeostf'; V = sys.argv[2] if len(sys.argv) > 2 else 'h'; sortie = sys.argv[3] if len(sys.argv) > 3 else 'trace-%s.png' % V
PAS = [0.08, 0.2, 0.33, 0.46, 0.6, 0.74, 0.88, 1.0]; CW, CH, FS = 96, 124, 92
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/scratchpad/v146/trace/essai.html'); pg.wait_for_timeout(900)
    pg.evaluate("""a=>{ document.body.innerHTML='<div id="z" style="position:absolute;left:0;top:0;width:390px"></div>'; const z=document.getElementById('z'); window.C=[];
      [...a[0]].forEach((c,i)=>{ const d=document.createElement('div'); d.style.cssText='position:absolute;left:'+((i%4)*a[2])+'px;top:'+(Math.floor(i/4)*a[3])+'px;width:'+a[2]+'px;height:'+a[3]+'px;font:700 '+a[4]+'px/'+a[3]+'px Gilbert;text-align:center;color:#291547';
        d.textContent=c; z.appendChild(d); }); }""", [chars, V, CW, CH, FS])
    pg.evaluate("async v=>{ for(const d of document.getElementById('z').children){ const c=TraceLettres.trace(d, null, {manuel:true, depart:v, respecteReduire:false}); await c.pret; C.push(c); } }", V)
    n = len(chars); H = ((n + 3) // 4) * CH; ims = []
    for f in PAS:
        pg.evaluate("f=>C.forEach(c=>c.va(f))", f); pg.wait_for_timeout(60)
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': 0, 'y': 0, 'width': 4 * CW, 'height': H}))).convert('RGB'))
    b.close()
k = 3; out = Image.new('RGB', (len(PAS) * CW * k, n * CH * k), '#F7F0DE')
for i in range(n):
    for j, im in enumerate(ims):
        out.paste(im.crop(((i % 4) * CW * k, (i // 4) * CH * k, (i % 4 + 1) * CW * k, (i // 4 + 1) * CH * k)), (j * CW * k, i * CH * k))
out.save(sortie); print(sortie, out.size)
