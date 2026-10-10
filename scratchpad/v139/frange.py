# largeur de la frange du bord : par secteur, rayon où l'opacité tombe sous 90 % puis sous 10 %
import sys,json
from playwright.sync_api import sync_playwright
JS="""()=>{ _aura.fige&&_aura.fige(true); var c=_aura.pelote?_aura.pelote():document.getElementById('auBoule'); c=document.getElementById('auBoule');
 var W=c.width,g=c.getContext('2d'),d=g.getImageData(0,0,W,W).data,k=W/296,cx=W/2,out=[];
 for(var s=0;s<72;s++){var a=s*Math.PI/36,r90=0,r10=0; for(var r=100*k;r<140*k;r+=0.5){var x=Math.round(cx+r*Math.cos(a)),y=Math.round(cx+r*Math.sin(a)); if(x<0||y<0||x>=W||y>=W)break; var al=d[(y*W+x)*4+3]; if(al>=230)r90=r; if(al>=25)r10=r;} out.push([r90/k,r10/k]);}
 return out;}"""
for f in sys.argv[1:]:
  with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('geste_vu_pelote','1');}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(7000)
    o=pg.evaluate(JS); fr=sorted(x[1]-x[0] for x in o); r90=sorted(x[0] for x in o); r10=sorted(x[1] for x in o)
    print(f,'frange médiane %.2f pt, max %.2f | plein jusqu\'à %.1f (méd) | fin %.1f (méd) %.1f (max)'%(fr[36],fr[-1],r90[36],r10[36],r10[-1]))
    b.close()
