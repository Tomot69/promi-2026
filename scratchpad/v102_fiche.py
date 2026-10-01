import sys
from playwright.sync_api import sync_playwright
M=r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390; const Y=v=>+((v-D.top)/k).toFixed(1); const o={};
 const f=(nom,e)=>{ if(!e||e.getBoundingClientRect().height===0) return; const b=e.getBoundingClientRect(); const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); const c=getComputedStyle(e);
   o[nom]={boite:[Y(b.top),Y(b.bottom)], encre:[Y(r.top),Y(r.bottom)], haut:+(Y(r.top)-Y(b.top)).toFixed(1), bas:+(Y(r.bottom)-Y(b.bottom)).toFixed(1), fs:c.fontSize, fam:c.fontFamily.split(',')[0]}; };
 f('kr-n',[...document.querySelectorAll('#dAura .kr-n')].find(x=>x.getBoundingClientRect().height>0)); f('dAura',document.getElementById('dAura'));
 ['dptQui','dptTitre','dptQuand','dptTrace'].forEach(id=>f(id,document.getElementById(id))); return o;}"""
T=sys.argv[2] if len(sys.argv)>2 else 'faire les crêpes'
with sync_playwright() as p:
    b=p.chromium.launch()
    for app in sys.argv[1].split(','):
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2); pg.goto('http://127.0.0.1:8752/'+app); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';};setTheme('dark');}"); pg.wait_for_timeout(400)
        pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; if(p) openDetail(p.id);}", T); pg.wait_for_timeout(2500)
        print('==',app)
        for k,v in pg.evaluate(M).items(): print('   %-9s %s' % (k,v))
        pg.close()
    b.close()
