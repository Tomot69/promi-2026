import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]; nom=sys.argv[2]
JS="""()=>{var dv=document.getElementById('device').getBoundingClientRect(); function R(e){var r=e.getBoundingClientRect(); return [+(r.left-dv.left).toFixed(1),+(r.top-dv.top).toFixed(1),+r.width.toFixed(1),+r.height.toFixed(1)];}
 var b=document.getElementById('createBtn'), o={btn:R(b), barre:R(document.getElementById('accBarre'))};
 var cs=getComputedStyle(b,'::before'); o.before=[cs.inset,cs.width,cs.height,cs.borderTopWidth,cs.outlineOffset, cs.boxShadow.slice(0,60)];
 o.enfants=[].map.call(b.querySelectorAll('*'),function(e){return e.tagName+'.'+(e.className.baseVal||e.className)+' '+R(e).join(',')});
 o.freres=[].map.call(document.getElementById('accBarre').children,function(e){return (e.id||e.className)+' '+R(e).join(',')});
 o.plat=R(document.getElementById('accPlat')); return o;}"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll();}"); pg.wait_for_timeout(1500)
    o=pg.evaluate(JS)
    for k,v in o.items(): print(k,v)
    r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}")
    pg.screenshot(path='planche-v139/%s.png'%nom,clip={'x':r[0],'y':r[1]+640,'width':390,'height':204})
    b.close()
