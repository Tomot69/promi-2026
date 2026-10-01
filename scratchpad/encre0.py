import base64
from playwright.sync_api import sync_playwright
GAP = open('releve-aura.py',encoding='utf-8').read().split('ENCRE_GAP = r"""')[1].split('"""')[0]
PIX = r"""async ([u,ys])=>{ const im=new Image(); im.src=u; await im.decode();
  const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; const g=c.getContext('2d'); g.drawImage(im,0,0);
  const d=g.getImageData(0,0,c.width,c.height).data, W=c.width, s=W/390;
  return ys.map(y=>{const yy=Math.round(y*s), x=Math.round(200*s), i=(yy*W+x)*4; return [y,d[i],d[i+1],d[i+2]];}); }"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(5000)
    for th,fond in (('dark',[32,25,8]),('light',[247,240,222])):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(600)
        for i in (0,1):
            pg.evaluate("(i)=>window._aura.mot(i)", i); pg.wait_for_timeout(400)
            m=pg.evaluate("""()=>{const dv=document.getElementById('device').getBoundingClientRect(),s=dv.width/390;
              const R=e=>{const r=e.getBoundingClientRect();return {b:(r.bottom-dv.top)/s};};
              return {b:R(document.querySelector('#auraScreen .au-mot')).b};}""")
            u='data:image/png;base64,'+base64.b64encode(pg.query_selector('#device').screenshot()).decode()
            print(th,i,'mot_bas',round(m['b'],1),'gap',pg.evaluate(GAP,[u,fond,m['b']]),
                  'pix',pg.evaluate(PIX,[u,[m['b']-2,m['b']+3,m['b']+10]]))
    b.close()
