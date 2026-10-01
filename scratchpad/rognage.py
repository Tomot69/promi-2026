#!/usr/bin/env python3
"""Les dalles d'ENCRE sortent-elles rognées, et la taille de la boîte y change-t-elle ?
On mesure la part du BORD du canevas qui est opaque : une forme bien cadrée le touche
tangentiellement (quelques %), une forme coupée le sature."""
from playwright.sync_api import sync_playwright
JS = r"""([id,px,monde])=>{
  window.Toile.setTheme(monde);
  const c=document.createElement('canvas'); c.width=px*2; c.height=px*2;
  document.body.appendChild(c);
  window.Toile.dalleTrame(c,id,1);
  const W=c.width,H=c.height,d=c.getContext('2d').getImageData(0,0,W,H).data;
  let bord=0, tot=0;
  const op=(x,y)=>d[(y*W+x)*4+3]>10;
  for(let x=0;x<W;x++){ if(op(x,0))bord++; if(op(x,H-1))bord++; tot+=2; }
  for(let y=0;y<H;y++){ if(op(0,y))bord++; if(op(W-1,y))bord++; tot+=2; }
  c.remove();
  return Math.round(100*bord/tot);
}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    ids = pg.evaluate("()=>promises.filter(p=>!p.draft&&!p.req).slice(0,4).map(p=>p.id)")
    print('%-11s %s' % ('monde', '  '.join('%5dpx' % s for s in (44,88,176))))
    for monde in ('encre','terrazzo','mosaique','braille','pixel'):
        vals=[]
        for px in (44,88,176):
            v=[pg.evaluate(JS,[i,px,monde]) for i in ids]
            vals.append(sum(v)//len(v))
        print('%-11s %s   %% du bord opaque' % (monde, '  '.join('%6d' % v for v in vals)))
    b.close()
