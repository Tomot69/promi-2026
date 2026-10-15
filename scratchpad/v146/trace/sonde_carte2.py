# sonde : la carte de temps d'un glyphe, peinte (un ton par propriétaire, la clarté = le temps) — pour voir qui possède quoi
import sys, json, numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image
car = sys.argv[1]; V = sys.argv[2] if len(sys.argv) > 2 else 'h'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/scratchpad/v146/trace/essai.html'); pg.wait_for_timeout(900)
    r = pg.evaluate("""async a=>{ document.body.innerHTML='<div id="z" style="position:absolute;left:0;top:0;width:160px;height:200px;font:700 150px/200px Gilbert;text-align:center;color:#291547"></div>'; const z=document.getElementById('z'); z.textContent=a[0];
      TraceLettres._debug=true; const c=TraceLettres.trace(z, null, {manuel:true, depart:a[1], respecteReduire:false}); await c.pret; c.va(0.5); const d=TraceLettres._derniere;
      return {w:d.w, h:d.h, T:Array.from(d.T).map(v=>Math.round(v*10)/10), own:Array.from(d.own), dep:d.dep, mins:d.mins, maxs:d.maxs, droits:d.droits}; }""", [car, V])
    b.close()
w, h = r['w'], r['h']; T = np.array(r['T']).reshape(h, w); own = np.array(r['own']).reshape(h, w)
print('dep', [round(x, 1) for x in r['dep']], 'mins', [round(x, 1) if x is not None else None for x in r['mins']], 'maxs', [round(x, 1) if x is not None else None for x in r['maxs']], 'droits', r['droits'])
D = T.max(); COL = {0: (220, 60, 60), 1: (60, 110, 230), 2: (40, 160, 90), 3: (220, 140, 0), -2: (150, 150, 150), -1: (255, 255, 255)}
im = np.full((h, w, 3), 255, np.uint8)
for k, c in COL.items():
    m = own == k
    if k == -1: continue
    f = (0.35 + 0.65 * (T / max(D, 1)))[m][:, None]; im[m] = (np.array(c)[None, :] * f).astype(np.uint8)
Image.fromarray(im).resize((w * 2, h * 2), Image.NEAREST).save('carte-%s.png' % car); print('carte-%s.png' % car, w, h, 'pixels tôt (T<3) :', int(((T < 3) & (own != -1)).sum()), {int(k): int(((own == k) & (T < 3)).sum()) for k in np.unique(own)})
