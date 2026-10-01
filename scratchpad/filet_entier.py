# -*- coding: utf-8 -*-
"""UN FILET DOIT CERNER, PAS ÊTRE TRONQUÉ. On parcourt le cercle du filet sur l'IMAGE
   RENDUE, 360 points, et on rend la part du tour où la crème est vraiment là."""
import base64, sys
from playwright.sync_api import sync_playwright
JS = r"""async ([u, box])=>{ const im=new Image(); im.src=u; await im.decode();
  const c=document.createElement('canvas'); c.width=im.width; c.height=im.height;
  const g=c.getContext('2d'); g.drawImage(im,0,0);
  const d=g.getImageData(0,0,c.width,c.height).data, W=c.width;
  const out=[];
  for(const b of box){
    const cx=b.cx, cy=b.cy, R=b.r; let ok=0, n=0, trous=[];
    for(let i=0;i<360;i++){
      const a=i*Math.PI/180;
      let hit=false;
      for(const dr of [-1.5,-0.75,0,0.75,1.5]){
        const x=Math.round(cx+(R+dr)*Math.cos(a)), y=Math.round(cy+(R+dr)*Math.sin(a));
        if(x<0||y<0||x>=W||y>=c.height) continue;
        const k=(y*W+x)*4;
        if(Math.abs(d[k]-247)<26 && Math.abs(d[k+1]-240)<26 && Math.abs(d[k+2]-222)<30){ hit=true; break; }
      }
      n++; if(hit) ok++; else if(trous.length<6) trous.push(i);
    }
    out.push({nom:b.nom, part:+(100*ok/n).toFixed(1), trous:trous});
  }
  return out;}"""
BOX = r"""()=>{const dv=document.getElementById('device').getBoundingClientRect();
  const s=2;   /* device_scale_factor */
  const out=[];
  document.querySelectorAll('canvas.kr-c, .au-nb').forEach((e,i)=>{
    if(!window._fondSombreSous || !window._fondSombreSous(e)) return;
    const r=e.getBoundingClientRect(); if(r.width<8) return;
    out.push({nom:(e.className?String(e.className).split(' ')[0]:'kr')+'#'+i,
      cx:(r.left-dv.left+r.width/2)*s, cy:(r.top-dv.top+r.height/2)*s, r:(r.width/2-0.7)*s});});
  return out;}"""
ECR=[('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}"),
     ('fiche tenue',"()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}"),
     ('fiche à tenir',"()=>{closeAll(); const p=promises.find(p=>p.status!=='tenu'&&!p.nuee&&!p.draft); if(p) openDetail(p.id);}"),
     ('nuée',"()=>{closeAll(); const k=Object.keys(NUE||{})[0]; window.openNueeDetail(k);}")]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(500)
        for nom,js in ECR:
            pg.evaluate(js); pg.wait_for_timeout(2800)
            box=pg.evaluate(BOX)
            if not box: print('%-6s %-14s (aucun filet)'%(th,nom)); continue
            u='data:image/png;base64,'+base64.b64encode(pg.query_selector('#device').screenshot()).decode()
            for o in pg.evaluate(JS,[u,box]):
                flag='' if o['part']>=99 else '   <<<< TRONQUÉ'
                print('%-6s %-14s %-10s %6.1f %% du tour %s%s'%(th,nom,o['nom'],o['part'],o['trous'][:4],flag))
    b.close()
