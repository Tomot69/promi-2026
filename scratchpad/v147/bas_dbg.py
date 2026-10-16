import sys, json; from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':160,'height':110}, device_scale_factor=3)
    pg.goto('http://127.0.0.1:8752/scratchpad/v147/essai_trace34.html'); pg.wait_for_function('window.pret'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{ TraceLettres._debug=true; return Promise.all([C.a.pret,C.b.pret]); }"); pg.evaluate("()=>{C.a.va(0.35);}")
    r=pg.evaluate("()=>{ const g=TraceLettres._bas[0]; return {car:g.car,w:g.w,h:g.h,D:g.D,sup:g.sup,T0:Array.from(g.T0),T1:Array.from(g.T1),A:Array.from(g.A)}; }")
    b.close()
w,h=r['w'],r['h']; im=Image.new('RGB',(w,h),'white'); px=im.load()
for y in range(h):
    for x in range(w):
        i=y*w+x
        if r['A'][i]: s=(int(r['T0'][i]/20)%2); px[x,y]=(200,40,40) if s else (60,60,200)
im=im.resize((w*6,h*6),Image.NEAREST); im.save(sys.argv[1]); print(r['car'],w,h,r['D'],r['sup'])
