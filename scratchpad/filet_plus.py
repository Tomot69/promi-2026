import base64
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light','dark'):
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e); if(s.animationName&&s.animationName!=='none') e.style.animationPlayState='paused';});}")
        pg.wait_for_timeout(300)
        box=pg.evaluate("""()=>{const dv=document.getElementById('device').getBoundingClientRect();
          const e=document.getElementById('createBtn'); const r=e.getBoundingClientRect();
          return {cx:(r.left-dv.left+r.width/2)*2, cy:(r.top-dv.top+r.height/2)*2, r:(r.width/2+3.5)*2};}""")
        u='data:image/png;base64,'+base64.b64encode(pg.query_selector('#device').screenshot()).decode()
        print(th, pg.evaluate(r"""async ([u,b])=>{ const im=new Image(); im.src=u; await im.decode();
          const c=document.createElement('canvas'); c.width=im.width; c.height=im.height;
          const g=c.getContext('2d'); g.drawImage(im,0,0);
          const d=g.getImageData(0,0,c.width,c.height).data, W=c.width;
          let ok=0, trous=[];
          for(let a=0;a<360;a++){ let hit=false;
            for(let dr=-3;dr<=3;dr+=0.5){
              const x=Math.round(b.cx+(b.r+dr)*Math.cos(a*Math.PI/180)), y=Math.round(b.cy+(b.r+dr)*Math.sin(a*Math.PI/180));
              const k=(y*W+x)*4;
              if(Math.abs(d[k]-247)<30 && Math.abs(d[k+1]-240)<30 && Math.abs(d[k+2]-222)<34){hit=true;break;} }
            if(hit) ok++; else if(trous.length<8) trous.push(a); }
          return {part:+(100*ok/360).toFixed(1), trous:trous};}""",[u,box]))
    br.close()
