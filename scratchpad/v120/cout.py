# coût de la peinture par densité et par palier, et le palier que vise le régulateur — @3x, WebKit et Chromium GPU
import sys
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for moteur in ('webkit','chromium'):
        b = p.webkit.launch() if moteur=='webkit' else p.chromium.launch(args=['--use-angle=metal','--enable-gpu','--ignore-gpu-blocklist'])
        for dn in (1,2,3):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?densite=%d'%dn); pg.wait_for_timeout(7000)
            ouvre(pg,1)
            for _ in range(40):
                if pg.evaluate("()=>{const c=document.getElementById('auBoule'); try{ return !!(c && c.width>400 && _aura.etat().pret); }catch(e){ return false; }}"): break
                pg.wait_for_timeout(500)
            pg.wait_for_timeout(9000); e=pg.evaluate("()=>{const e=_aura.etat(); return [e.palier,e.vise,+(+e.ms).toFixed(1)]}")
            L=[]
            for i in range(3):
                pg.evaluate("(i)=>_aura.palier(i)",i); pg.wait_for_timeout(5000); r=pg.evaluate("()=>{const e=_aura.etat(); return [e.palier,+(+e.ms).toFixed(1)]}"); L.append('%d poils : %s ms'%(r[0],r[1]))
            print('%-8s ?densite=%d · après 9 s : palier %s, le régulateur vise %s (médiane %s ms) · '%(moteur,dn,e[0],e[1],e[2]) + ' · '.join(L)); ctx.close()
        b.close()
