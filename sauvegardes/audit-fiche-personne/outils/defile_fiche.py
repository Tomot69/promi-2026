# Qu'est-ce qui défile DANS la fiche de la personne ? (descendants dont scrollHeight > clientHeight, et leur overflow)
import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(sys.argv[1]); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(600)
    pt = pg.evaluate("""()=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()==='Marion'); const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
        for(const n of document.querySelectorAll('#auraScreen .au-nb')){ const r=n.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} } return best; }""")
    pg.mouse.click(pt[0], pt[1]); pg.wait_for_timeout(1800)
    print(pg.evaluate("""()=>{ const sh=document.getElementById('personSheet'), out=[];
      for(const e of [sh, ...sh.querySelectorAll('*')]){ const c=getComputedStyle(e); if(e.scrollHeight>e.clientHeight+2 && c.display!=='none')
        out.push((e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className).split(' ')[0])+' '+e.scrollHeight+'/'+e.clientHeight+' overflow-y:'+c.overflowY); }
      const par=[]; for(let x=sh.parentElement; x; x=x.parentElement){ if(x.scrollHeight>x.clientHeight+2) par.push((x.id||x.tagName)+' '+x.scrollHeight+'/'+x.clientHeight+' '+getComputedStyle(x).overflowY); }
      return JSON.stringify({dedans:out, ancetres:par, sheetBox:(()=>{const r=sh.getBoundingClientRect(); return [r.top,r.height];})()}); }"""))
    b.close()
