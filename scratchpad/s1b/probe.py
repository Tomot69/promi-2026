import os,sys
from playwright.sync_api import sync_playwright
V='file://'+os.path.abspath('app.html')

DUMP=r"""()=>{
  const dp=document.getElementById('detailPoster'); if(!dp) return {err:'no dp'};
  const R=dp.getBoundingClientRect();
  const out={cls:dp.className, scrollTop:dp.scrollTop, h:R.height};
  const sel={dpTrameCv:'#dpTrameCv', type:'#dpType', close:'.closeb', main:'#dpMain',
    tete:'#dpTete', qui:'#dpTete .dpt-qui', titre:'#dpTete .dpt-titre', quand:'#dptQuand',
    aura:'#dAura', corps:'#dpCorps', geste:'.geste-env', tenir:'#tenirZone',
    details:'#dpDetails', tog:'#dpdTog', nuee:'#dpNuee', fil:'#dpNueeFil'};
  out.el={};
  for(const k in sel){ const e=dp.querySelector(sel[k]);
    if(!e){ out.el[k]=null; continue; }
    const b=e.getBoundingClientRect(), cs=getComputedStyle(e);
    out.el[k]={x:+(b.x-R.x).toFixed(1), y:+(b.y-R.y+dp.scrollTop).toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1),
      font:cs.fontFamily.split(',')[0].replace(/"/g,''), size:cs.fontSize, weight:cs.fontWeight,
      color:cs.color, bg:cs.backgroundColor, disp:cs.display};
  }
  // enfants de dpMain dans l'ordre visuel
  const m=dp.querySelector('#dpMain');
  out.mainKids=m?[...m.children].map(c=>c.id||c.className):[];
  out.dpKids=[...dp.children].map(c=>c.id||c.className);
  return out;
}"""

def run(pick,arg,tag,light=False):
  with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto(V); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(l)=>{var d=document.querySelector('.device');if(d){l?d.classList.add('light'):d.classList.remove('light');}}",light)
    pg.evaluate(pick,arg)
    pg.wait_for_timeout(1500)
    r=pg.evaluate(DUMP)
    print('=== '+tag)
    print('cls:',r.get('cls'))
    print('dpKids:',r.get('dpKids'))
    print('mainKids:',r.get('mainKids'))
    for k,v in (r.get('el') or {}).items():
      if v is None: print('  %-10s —'%k)
      else: print('  %-10s x=%-6s y=%-6s w=%-6s h=%-6s %s %s/%s %s bg=%s'%(k,v['x'],v['y'],v['w'],v['h'],v['font'],v['weight'],v['size'],v['color'],v['bg']))
    pg.screenshot(path='scratchpad/s1b/probe_%s.png'%tag)
    pg.close(); b.close()

PICK_STATUS="""(want)=>{ try{var pr=promises.filter(p=>!p.draft&&!p.nuee); var at=pr.filter(p=>p.status===want)[0]||pr[0]; openDetail(at.id);}catch(e){} }"""
PICK_NUEE="""()=>{ try{ var k=Object.keys(NUE)[0]; ouvrirNuee ? ouvrirNuee(k) : openNuee(k); }catch(e){ try{ var b=document.querySelector('[data-nuee]'); if(b) b.click(); }catch(_){} } }"""
if __name__=='__main__':
  for want,tag in [('rate','atenir'),('encours','encours'),('tenu','tenue')]:
    run(PICK_STATUS,want,tag)
