from playwright.sync_api import sync_playwright
import sys
URL=sys.argv[1]
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}"); pg.goto(URL); pg.wait_for_timeout(7000)
    for th in ('dark','light'):
        pg.evaluate("t=>{setTheme(t);closeAll();openEssaim('potager');setTimeout(()=>{const t=document.querySelector('#dpDetails .dpd-tog');t&&t.click()},1200)}",th); pg.wait_for_timeout(3200)
        print(th, pg.evaluate("""()=>{const o={};for(const id of ['npDesc','npComm']){const c=document.getElementById(id);const lab=c.querySelector('.np-lab'),bas=c.querySelector('.np-bas');
           const mid=c.querySelector('.np-champ')||c.querySelector('.np-ph'); const R=e=>{const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect()};
           const box=mid.tagName==='INPUT'||mid.tagName==='TEXTAREA'?mid.getBoundingClientRect():R(mid);
           o[id]={lab_bas:Math.round(R(lab).bottom*10)/10, milieu:[Math.round(box.top*10)/10,Math.round(box.bottom*10)/10], bas_haut:Math.round(R(bas).top*10)/10, carte:Math.round(c.getBoundingClientRect().height)};}return o}"""))
