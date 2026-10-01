# Le film du retour de l'empreinte : les 10 dernières images peintes AVANT le retrait et 2 après,
# à vue figée, zone du doigt — une rangée par version. Sort une planche PNG.
#   python3 film_retour.py SORTIE.png NOM1=URL1 NOM2=URL2 ...
import sys, base64
from playwright.sync_api import sync_playwright

OUT = sys.argv[1]
VERS = [a.split('=', 1) for a in sys.argv[2:]]
TX, TY = -0.40, -0.30

REC = r"""([tx,ty])=>new Promise(res=>{
  const cv=document.getElementById('auBoule'), g=cv.getContext('2d'), W=cv.width, c=W/2, R=W*0.392;
  const zx=c+tx*R, zy=c+ty*R, zr=0.35*R;
  const x0=Math.max(0,Math.floor(zx-zr)), y0=Math.max(0,Math.floor(zy-zr));
  const w=Math.min(W,Math.ceil(zx+zr))-x0, h=Math.min(W,Math.ceil(zy+zr))-y0;
  const buf=[]; let lastP=-1, apres=0, prev=null; const t0=performance.now();
  function tick(){
    const e=_aura.etat();
    if(e.peints!==lastP){ lastP=e.peints;
      const im=g.getImageData(x0,y0,w,h); let n=0,ch=0;
      if(prev){ const a=im.data,b=prev.data; for(let i=0;i<a.length;i+=8){ n++;
        ch+=(Math.abs(a[i]-b[i])+Math.abs(a[i+1]-b[i+1])+Math.abs(a[i+2]-b[i+2]))/3; } }
      buf.push({im, p:e.emp?e.emp.p:null, pas:prev?ch/n:null, t:Math.round(performance.now()-t0)}); prev=im;
      if(e.emp && buf.length>12) buf.shift();
      if(!e.emp && ++apres>=2) return fin();
    }
    if(performance.now()-t0>20000) return fin();
    requestAnimationFrame(tick);
  }
  function fin(){
    const k=document.createElement('canvas'); k.width=w*buf.length; k.height=h+44;
    const q=k.getContext('2d'); q.fillStyle='#000'; q.fillRect(0,0,k.width,k.height);
    buf.forEach((f,j)=>{ q.putImageData(f.im,j*w,0); q.fillStyle=f.p===null?'#2BE88C':'#fff';
      q.font='bold 19px sans-serif'; q.fillText(f.p===null?'LISSE':'p '+f.p.toFixed(3), j*w+8, h+20);
      q.fillText(f.pas===null?'':'pas '+f.pas.toFixed(2), j*w+8, h+40); });
    res(k.toDataURL('image/png'));
  }
  requestAnimationFrame(tick);
})"""

imgs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for nom, url in VERS:
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(url); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>{closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(200)
            e = pg.evaluate("()=>window._aura?_aura.etat():null")
            if e and e['pret'] and e['frames'] > 12: break
        pg.wait_for_timeout(800)
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true);}")
        pg.wait_for_timeout(600)
        r = pg.evaluate("()=>{const b=document.getElementById('auBoule').getBoundingClientRect();return [b.left+b.width/2,b.top+b.height/2,b.width*0.392];}")
        pg.mouse.move(r[0] + TX * r[2], r[1] + TY * r[2]); pg.mouse.down(); pg.wait_for_timeout(950); pg.mouse.up()
        u = pg.evaluate(REC, [TX, TY])
        imgs.append((nom, base64.b64decode(u.split(',', 1)[1])))
        pg.close()
    # une planche : les rangées l'une sous l'autre, avec leur nom
    pg = b.new_page()
    html = '<body style="margin:0;background:#111;color:#fff;font:bold 22px sans-serif">' + ''.join(
        '<div style="padding:10px 8px 4px">%s</div><img style="display:block" src="data:image/png;base64,%s">'
        % (n, base64.b64encode(d).decode()) for n, d in imgs) + '</body>'
    pg.set_content(html); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT, full_page=True)
    b.close()
print('planche :', OUT)
