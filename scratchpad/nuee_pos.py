from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for k in ('le potager','famille'):
        pg.evaluate("(k)=>{closeAll(); const kk=Object.keys(NUE||{}).find(x=>NUE[x]===k||x===k)||Object.keys(NUE||{})[0]; window.openNueeDetail(kk);}", k)
        pg.wait_for_timeout(2800)
        print(k, pg.evaluate(r"""()=>{const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
          const R=sel=>{const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect();
            if(r.width<2) return 'invisible'; return [+((r.top-dv.top)/s).toFixed(1), +((r.bottom-dv.top)/s).toFixed(1)];};
          const cartes=[...document.querySelectorAll('#detailPoster .s4-fdcard, #detailPoster .nf-card, #nueeFil > *')]
            .slice(0,3).map(e=>{const r=e.getBoundingClientRect(); return [String(e.className).slice(0,14), +((r.top-dv.top)/s).toFixed(1)];});
          return {nb:document.querySelectorAll('#detailPoster .au-nb, #detailPoster canvas.kr-c').length,
            anneaux:R('#detailPoster canvas.kr-c'), avec:R('#detailPoster .dpt-qui'), titre:R('#detailPoster .dpt-titre'),
            trame:R('#dpTrameCv'), fil:R('#nueeFil'), cartes:cartes, n:(window.promises||[]).filter(p=>p.nuee).length};}"""))
    b.close()
