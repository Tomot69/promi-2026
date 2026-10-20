import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
SONDE="""()=>{ const v=[]; for(const a of document.getAnimations()){ if(a.playState!=='running') continue; const t=a.effect&&a.effect.getTiming? a.effect.getTiming():{}; const tg=a.effect&&a.effect.target; v.push((tg&&(tg.id||tg.className&&String(tg.className).slice(0,30)))+':'+(a.animationName||a.constructor.name)); }
 const ops=[...document.querySelectorAll('#device *')].filter(e=>{const c=getComputedStyle(e); return c.transitionDuration && c.transitionDuration.split(',').some(x=>parseFloat(x)>0) && e.getBoundingClientRect().width>0 && c.visibility!=='hidden';}).length;
 return {anims:v.slice(0,12), n:v.length, tl:(window.__TLn||0)}; }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=B.contexte(b, onb=False, guide=False); ctx.add_init_script("(()=>{ const T=()=>{ if(window.TraceLettres && !window.TraceLettres.__s){ const o=TraceLettres.trace; TraceLettres.trace=function(el,t,op){ const c=o.apply(this,arguments); window.__TLc=(window.__TLc||[]).concat([c]); return c; }; TraceLettres.__s=1; } }; setInterval(T,20); })()")
    pg=ctx.new_page(); pg.emulate_media(reduced_motion='reduce'); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(5000)
    print('onboarding', pg.evaluate(SONDE), pg.evaluate("()=>({rm:matchMedia('(prefers-reduced-motion: reduce)').matches, tl:(window.__TLc||[]).map(c=>({fini:c.fini, d:Math.round(c.duree||0)}))})"))
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} localStorage.setItem('promi_guide','1'); }"); pg.wait_for_timeout(1500)
    print('accueil', pg.evaluate(SONDE))
    pg.evaluate("()=>{ try{ document.getElementById('setBtn')&&document.getElementById('setBtn').click(); }catch(e){} }"); pg.wait_for_timeout(1500)
    print('pseudos', pg.evaluate("()=>{ const o=[]; document.querySelectorAll('#createBtn, .set-cercle, .pplus-card, .karma-cercle').forEach(e=>{ for(const ps of ['::before','::after']){ const c=getComputedStyle(e, ps); if(c.animationName && c.animationName!=='none') o.push((e.id||e.className)+ps+':'+c.animationName); } }); return o; }"))
    b.close()
