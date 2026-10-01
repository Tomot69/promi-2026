# Trois faits pour l'audit de la fiche de la personne (rien n'est modifié) :
#  a · les mini-dalles de la liste sont-elles peintes ? (pixels opaques à 0,3 · 0,9 · 2,5 s après l'ouverture)
#  c · qui peint la grande forme grise derrière la fiche ? (pseudo-éléments, éléments sous le point)
#  d · de quelle couleur est tracée la courbe « comment ça évolue » ? (traits et remplissages du SVG)
import sys, json
from playwright.sync_api import sync_playwright
MINI = r"""()=>[...document.querySelectorAll('#personSheet canvas.mini-dalle')].map(c=>{ let n=0,t=0; try{ const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
  for(let i=3;i<d.length;i+=4){ t++; if(d[i]>10) n++; } }catch(e){ return 'err '+e.message; } return c.width+'×'+c.height+' opaques '+(t?(100*n/t).toFixed(1):0)+' %'; })"""
FORME = r"""()=>{ const sh=document.getElementById('personSheet'), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const ps=(sel)=>{ const c=getComputedStyle(sh, sel); return {content:c.content, bgi:(c.backgroundImage||'').slice(0,90), bg:c.backgroundColor, w:c.width, h:c.height, pos:c.position, filt:c.filter, op:c.opacity}; };
  const sous=[]; for(const [x,y] of [[300,260],[120,300],[330,420]]){ const els=document.elementsFromPoint(dv.left+x*s, dv.top+y*s).slice(0,6);
    sous.push([x,y].join(',')+' → '+els.map(e=>(e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className.baseVal!==undefined?e.className.baseVal:e.className).split(' ').slice(0,2).join('.'))).join(' ▸ ')); }
  const cvs=[...sh.querySelectorAll('canvas')].map(c=>{ const r=c.getBoundingClientRect(); return (c.id||c.className)+' '+Math.round(r.width/s)+'×'+Math.round(r.height/s)+' @'+Math.round((r.left-dv.left)/s)+','+Math.round((r.top-dv.top)/s); });
  return {avant:ps('::before'), apres:ps('::after'), sous:sous, canevas:cvs, sheetBgi:getComputedStyle(sh).backgroundImage.slice(0,120)}; }"""
SVG = r"""()=>{ const sv=[...document.querySelectorAll('#personSheet svg')]; return sv.map(s=>[...s.querySelectorAll('*')].filter(e=>['path','line','polyline','circle','rect'].includes(e.tagName)).map(e=>{ const c=getComputedStyle(e);
  return e.tagName+' stroke '+c.stroke+' '+c.strokeWidth+' fill '+c.fill+' op '+c.opacity+(e.getAttribute('d')?' d '+e.getAttribute('d').slice(0,50):''); })); }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(sys.argv[1]); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(600)
        pt = pg.evaluate("""()=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()==='Marion'); const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
            for(const n of document.querySelectorAll('#auraScreen .au-nb')){ const r=n.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} } return best; }""")
        pg.mouse.click(pt[0], pt[1])
        mini = []
        for t in (300, 600, 1600):
            pg.wait_for_timeout(t); mini.append(pg.evaluate(MINI))
        print('=== %s' % th)
        print('a · mini-dalles à 0,3 · 0,9 · 2,5 s :', json.dumps(mini, ensure_ascii=False))
        print('c · forme :', json.dumps(pg.evaluate(FORME), ensure_ascii=False, indent=1))
        print('d · courbe :', json.dumps(pg.evaluate(SVG), ensure_ascii=False))
        pg.close()
    b.close()
