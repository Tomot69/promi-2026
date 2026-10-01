"""Deux captures du MÊME écran, sans rien changer entre les deux : ce qui bouge est
l'instabilité de l'app, et aucun comparateur ne peut descendre en dessous."""
import base64
from playwright.sync_api import sync_playwright
APP="http://127.0.0.1:8752/app.html"
DIFF="""(a)=>new Promise(res=>{const A=new Image(),B=new Image();let n=0;
 function pret(){ if(++n<2) return; const W=390,H=844;
  const c1=document.createElement('canvas');c1.width=W;c1.height=H;
  const c2=document.createElement('canvas');c2.width=W;c2.height=H;
  c1.getContext('2d').drawImage(A,0,0,W,H); c2.getContext('2d').drawImage(B,0,0,W,H);
  const d1=c1.getContext('2d').getImageData(0,0,W,H).data, d2=c2.getContext('2d').getImageData(0,0,W,H).data;
  const Z=a.zones||[]; let diff=0,tot=0;
  const dans=(x,y)=>{for(const q of Z) if(x>=q[0]&&x<q[0]+q[2]&&y>=q[1]&&y<q[1]+q[3]) return true; return false;};
  for(let i=0;i<d1.length;i+=4){const p=i/4,y=Math.floor(p/W),x=p%W; if(dans(x,y)) continue;
    tot++; if(Math.abs(d1[i]-d2[i])+Math.abs(d1[i+1]-d2[i+1])+Math.abs(d1[i+2]-d2[i+2])>60) diff++;}
  res(tot?Math.round(1000*diff/tot)/10:0);}
 A.onload=pret;B.onload=pret;A.src=a.a;B.src=a.b;})"""
SC=[('fiche-tenue',"()=>{if(window.closeAll)closeAll(); const p=promises.filter(q=>!q.draft&&q.status==='tenu')[0]; if(p)openDetail(p.id);}"),
    ('index-2',"()=>{if(window.closeAll)closeAll(); setView('toile'); ouvrirIndex();}"),
    ('fil',"()=>{if(window.closeAll)closeAll(); setView('fil');}"),
    ('nuee',"()=>{if(window.closeAll)closeAll(); openEssaim('potager');}"),
    ('page-plus',"()=>{if(window.closeAll)closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}")]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    calc=b.new_page(); calc.goto('about:blank')
    print("%-14s %10s %10s"%("écran","même vue","ré-ouvert"))
    for nom,js in SC:
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
        pg.evaluate(js); pg.wait_for_timeout(3000)
        z=pg.evaluate("()=>window._zonesMatiere?window._zonesMatiere().zones:[]")
        a1=base64.b64encode(pg.query_selector('#device').screenshot()).decode()
        pg.wait_for_timeout(1500)
        a2=base64.b64encode(pg.query_selector('#device').screenshot()).decode()
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
        pg.evaluate(js); pg.wait_for_timeout(3000)
        a3=base64.b64encode(pg.query_selector('#device').screenshot()).decode()
        d12=calc.evaluate(DIFF,{'a':'data:image/png;base64,'+a1,'b':'data:image/png;base64,'+a2,'zones':z})
        d13=calc.evaluate(DIFF,{'a':'data:image/png;base64,'+a1,'b':'data:image/png;base64,'+a3,'zones':z})
        print("%-14s %9.1f%% %9.1f%%"%(nom,d12,d13))
    b.close()
