# La phrase posée depuis le petit canevas = la phrase écrite directement, au pixel (Chromium et WebKit, k = 3 et 2,8).
from playwright.sync_api import sync_playwright
JS = r"""async (k)=>{ await document.fonts.ready; const mot='Parole tenue !', fs=40, fx=195.37, fy=503.81, police=fs+'px Gilbert, system-ui';
 function cv(){ const c=document.createElement('canvas'); c.width=Math.round(390*k); c.height=Math.round(844*k); document.body.appendChild(c); const g=c.getContext('2d'); g.setTransform(k,0,0,k,0,0); return [c,g]; }
 const clip=()=>{ const p=new Path2D(); p.moveTo(0,0); p.lineTo(390,0); p.lineTo(390,505); p.quadraticCurveTo(200,480,0,507); p.closePath(); return p; };
 const [a,ga]=cv(); ga.save(); ga.clip(clip()); ga.font=police; ga.fillStyle='#201908'; ga.textBaseline='alphabetic'; ga.textAlign='center'; ga.fillText(mot,fx,fy); ga.restore();
 const [b,gb]=cv(); const TX=document.createElement('canvas'); let tg=TX.getContext('2d'); tg.font=police; const lw=tg.measureText(mot).width;
 const TXx=Math.floor((fx-lw/2-8)*k), TXy=Math.floor((fy-fs*1.25)*k); TX.width=Math.ceil((lw+16)*k); TX.height=Math.ceil(fs*1.8*k);
 tg=TX.getContext('2d'); tg.setTransform(k,0,0,k,-TXx,-TXy); tg.font=police; tg.fillStyle='#201908'; tg.textBaseline='alphabetic'; tg.textAlign='center'; tg.fillText(mot,fx,fy);
 gb.save(); gb.clip(clip()); gb.setTransform(1,0,0,1,0,0); gb.drawImage(TX,TXx,TXy); gb.restore();
 const A=ga.getImageData(0,0,a.width,a.height).data, B=gb.getImageData(0,0,b.width,b.height).data, W=a.width;
 function st(D){ let s=0,sx=0,sy=0,x0=1e9,x1=-1,y0=1e9,y1=-1; for(let i=3;i<D.length;i+=4){ const v=D[i]; if(!v) continue; const p=(i-3)/4, x=p%W, y=(p/W)|0; s+=v; sx+=v*x; sy+=v*y; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } return {encreTotale:s, cx:+(sx/s).toFixed(3), cy:+(sy/s).toFixed(3), boite:[x0,y0,x1,y1]}; }
 const r={direct:st(A), calque:st(B)}; a.remove(); b.remove(); return r; }"""
with sync_playwright() as p:
    for nom, L in (('chromium', p.chromium), ('webkit', p.webkit)):
        b = L.launch(); pg = b.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(3000)
        for k in (3, 2.8):
            print(nom, k, pg.evaluate(JS, k))
        b.close()
