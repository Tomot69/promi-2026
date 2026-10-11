import os,sys
from playwright.sync_api import sync_playwright
src=open('scratchpad/accueil_audit.py').read()
exec('MASK_JS = ' + src.split('MASK_JS = ')[1].split('# D —')[0]); exec('REACH_JS = ' + src.split('REACH_JS = ')[1].split('CMDS = [')[0])
with sync_playwright() as p:
    b=p.chromium.launch()
    for n in range(int(sys.argv[1]) if len(sys.argv)>1 else 3):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=1,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.wait_for_timeout(600)
        m=pg.evaluate(MASK_JS); A=pg.evaluate(REACH_JS,[m['rows'],[1.0]])
        z=A['zooms']['1']; 
        for i in z['inatteignables']:
            print(n,'inatteignable',i,A['titres'].get(str(i)), pg.evaluate("(i)=>{var a=Toile.dalleAbs(i),v=Toile.vue(); var L=Toile_lecture().graines.find(g=>g.pid===i); return [Math.round(a.minx),Math.round(a.miny),Math.round(a.w),Math.round(a.h),v,L&&[Math.round(L.x),Math.round(L.y),L.kind]]}",i))
        print(n,'ok' if not z['inatteignables'] else 'KO', z['n'])
        ctx.close()
    b.close()
