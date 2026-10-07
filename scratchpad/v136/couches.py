from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont, ImageChops
import sys
SC='scratchpad/v136/'
LISTE="""()=>{ const D=document.getElementById('device').getBoundingClientRect(); const B=document.getElementById('auBoule').getBoundingClientRect(); const out=[]; const cx=B.left+B.width/2, cy=B.top+B.height/2;
  document.querySelectorAll('#auraScreen *').forEach(e=>{ const r=e.getBoundingClientRect(); if(r.width<20||r.height<20) return; const s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0) return;
    if(r.left>cx+200||r.right<cx-200||r.top>cy+200||r.bottom<cy-200) return;
    const peint=(s.backgroundImage!=='none')||(s.backgroundColor!=='rgba(0, 0, 0, 0)')||s.boxShadow!=='none'||s.filter!=='none'||e.tagName==='CANVAS'||e.tagName==='svg'||(s.borderTopWidth!=='0px');
    if(!peint) return; out.push({id:e.id||'', cls:String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className).slice(0,30), tag:e.tagName, x:Math.round(r.left-D.left), y:Math.round(r.top-D.top), w:Math.round(r.width), h:Math.round(r.height), bg:s.backgroundImage.slice(0,60), bgc:s.backgroundColor, sh:s.boxShadow.slice(0,40), f:s.filter, op:s.opacity, z:s.zIndex, tr:s.transform.slice(0,40)}); });
  return out }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:200])); pg.goto('http://127.0.0.1:8752/app.html'+(sys.argv[1] if len(sys.argv)>1 else '')); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); document.getElementById('souffleBtn').click();}",th); pg.wait_for_timeout(5200)
        pg.evaluate("()=>{ try{ _aura.fige(true); }catch(e){} }"); pg.wait_for_timeout(400)
        L=pg.evaluate(LISTE); print('==',th)
        for e in L: print('  ',e)
        clip={'x':20+35,'y':44+100,'width':320,'height':330}
        pg.screenshot(path=SC+'co-%s-tout.png'%th, clip=clip)
        ids=[e['id'] for e in L if e['id']]
        for i in ids:
            pg.evaluate("(a)=>{ a[0].forEach(x=>{const e=document.getElementById(x); if(e){ e.dataset.v0=e.style.visibility||''; e.style.setProperty('visibility', x===a[1]?'visible':'hidden','important'); }}); }",[ids,i])
            pg.wait_for_timeout(250); pg.screenshot(path=SC+'co-%s-%s.png'%(th,i), clip=clip)
            pg.evaluate("(a)=>{ a.forEach(x=>{const e=document.getElementById(x); if(e){ e.style.removeProperty('visibility'); if(e.dataset.v0) e.style.visibility=e.dataset.v0; }}); }",ids)
        open(SC+'co-%s-ids.txt'%th,'w').write('\n'.join(ids)); ctx.close()
    b.close()
