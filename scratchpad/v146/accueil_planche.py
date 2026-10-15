import sys, json, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
def cr(l): return l
def lum(c):
    def f(v): v/=255.0; return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
def contraste(a,b): la,lb=lum(a),lum(b); return (max(la,lb)+0.05)/(min(la,lb)+0.05)
print('#022140 sur #F7F0DE : %.2f:1 · #022140 sur #050302 : %.2f:1 · #82AEF8 sur #050302 : %.2f:1 · #F7F0DE sur #050302 : %.2f:1 · #FB4C0D sur #82AEF8 : %.2f:1' % (contraste((2,33,64),(247,240,222)), contraste((2,33,64),(5,3,2)), contraste((130,174,248),(5,3,2)), contraste((247,240,222),(5,3,2)), contraste((251,76,13),(130,174,248))))
ims = []
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre, var in ((False, None), (True, None), (True, '#022140'), (True, '#82AEF8')):
        ctx = B.contexte(b, sombre=sombre); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
        if var: pg.add_style_tag(content="#device#device#device#device .acc-barre .dctrl .l{color:%s!important;-webkit-text-fill-color:%s!important}" % (var, var)); pg.wait_for_timeout(300)
        o = pg.evaluate("()=>({enr:!!document.getElementById('enrToile'), plat:[...document.getElementById('accPlat').children].filter(e=>getComputedStyle(e).display!=='none').map(e=>e.id||e.className), croix:getComputedStyle(document.querySelector('#createBtn svg path')).stroke, noms:[...document.querySelectorAll('.acc-barre .dctrl .l')].map(e=>getComputedStyle(e).color)})")
        print('sombre' if sombre else 'clair', var or '', o)
        f = 'planche-v146/accueil-%s%s.png' % ('sombre' if sombre else 'clair', ('-' + var[1:]) if var else ''); B.capture(pg, f); ims.append(Image.open(f).convert('RGB')); ctx.close()
    b.close()
W = sum(i.width for i in ims) + 40 * 3; P = Image.new('RGB', (W, ims[0].height), (60, 60, 60)); x = 0
for i in ims: P.paste(i, (x, 0)); x += i.width + 40
P.save('planche-v146/PLANCHE-5-accueil.png'); P.resize((W // 3, ims[0].height // 3)).save('scratchpad/v146/pl5.png')
# le bas seulement, agrandi
Q = Image.new('RGB', (W, 420), (60, 60, 60)); x = 0
for i in ims: Q.paste(i.crop((0, i.height - 420, i.width, i.height)), (x, 0)); x += i.width + 40
Q.resize((W // 2, 210)).save('scratchpad/v146/pl5-bas.png')
