import sys
from playwright.sync_api import sync_playwright
src=open('redteam_nuee_entree.py').read(); J=src.split('J = r"""')[1].split('"""')[0]
X=r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390; const o={};
 ['dptNat','dptQui','dptTitre','dptQuand','dAura'].forEach(id=>{const e=document.getElementById(id); if(!e) return; const r=e.getBoundingClientRect(); const c=getComputedStyle(e);
   o[id]={y:+((r.top-D.top)/k).toFixed(1), h:+(r.height/k).toFixed(1), fs:c.fontSize, lh:c.lineHeight, tr:c.translate, top:e.style.top};}); return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for app in sys.argv[1:]:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/'+app); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme('dark');}"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{closeAll();openEssaim('potager');}"); pg.wait_for_timeout(2800)
        r=pg.evaluate(J); bl=sorted(r['blocs'],key=lambda x:x[1])
        print(app, 'blocs', [(x[0],round(x[1],1),round(x[2],1)) for x in bl])
        for k,v in pg.evaluate(X).items(): print('   ',k,v)
        pg.close()
    b.close()
