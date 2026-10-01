# Arrivée scriptée contre arrivée réelle (Madrure) : la fin du mouvement, image par image.
import sys
from playwright.sync_api import sync_playwright
M=sys.argv[1] if len(sys.argv)>1 else 'madrure'
src=open('../../redteam_rythme.py').read(); ENREG=src.split('ENREG = r"""')[1].split('"""')[0]
SEQ=r"""()=>{ const W=window; W.__fin=true; const T0=W.__T0; return W.__R.filter(r=>r[0]>=T0).map(r=>[Math.round(r[0]-T0), +r[1].toFixed(1)]); }"""
def c(pg,s): return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}",s)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
    pg.evaluate("m=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); Toile.setTheme(m);}",M); pg.wait_for_timeout(3000)
    for cond in ['script','reel']:
        pg.evaluate(ENREG)
        if cond=='script': pg.evaluate("()=>{ const P=window.eval('promises'); P.push(Object.assign({},P[0],{id:97001,title:'mesure du rythme',nuee:null})); Toile.addPromi(97001); }")
        else:
            pg.mouse.click(*c(pg,'#createBtn')); pg.wait_for_timeout(600); pg.mouse.click(*c(pg,'#accChoix .acc-pil[data-k=promi]')); pg.wait_for_timeout(1800)
            pg.evaluate("()=>{ const t=document.getElementById('fTitle'); t.value='mesure du rythme 2'; t.dispatchEvent(new Event('input',{bubbles:true})); }"); pg.evaluate(ENREG)
            z=pg.evaluate("()=>{ const r=document.getElementById('planterZone').getBoundingClientRect(); return [r.left, r.top+r.height/2, r.width]; }")
            pg.mouse.move(z[0]+12,z[1]); pg.mouse.down()
            for i in range(1,26): pg.mouse.move(z[0]+12+(z[2]-24)*i/25, z[1]); pg.wait_for_timeout(12)
            pg.mouse.up()
        pg.wait_for_timeout(3500); s=pg.evaluate(SEQ)
        mv=[x for x in s if x[1]>0.5]
        print(cond, 'images qui bougent', len(mv), 'début', mv[:4], 'fin', mv[-6:])
        print('   cible :', pg.evaluate("()=>{ const s=Toile_probe? null:null; return window._trans_en_cours? 'ok':''; }"))
        pg.wait_for_timeout(1500)
    b.close()
