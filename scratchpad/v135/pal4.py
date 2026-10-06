from playwright.sync_api import sync_playwright
import sys
E="""()=>{ const P=document.getElementById('stpPals'); if(!P) return null; const pals=[...P.querySelectorAll('.st3-pals > *')]; const o=pals[0]&&pals[0].querySelector('.st3-orb'); const cs=o?getComputedStyle(o):null; const pn=document.getElementById('st3pn'); const sp=P.querySelector('.st3-spec');
  return {dev:Math.round(document.getElementById('device').getBoundingClientRect().width), n:pals.length, orbe:o?[o.getBoundingClientRect().width.toFixed(1), cs.width, cs.display, o.getAttribute('style')]:null, p:pals[0]?[getComputedStyle(pals[0]).width, pals[0].getAttribute('style')]:null,
    pn:pn?[getComputedStyle(pn).fontFamily.slice(0,20), getComputedStyle(pn).textAlign, pn.parentNode.id]:null, spec:sp?[getComputedStyle(sp).height, getComputedStyle(sp).position]:null, enfants:[...P.children].map(c=>c.id||c.className)} }"""
with sync_playwright() as p:
    for nav in ('chromium','webkit'):
        b=getattr(p,nav).launch()
        for vp in ((300,650),(430,932),(360,560)):
            for prem,nb in ((True,'0'),(False,'0'),(True,'1')):
                ctx=b.new_context(viewport={'width':vp[0],'height':vp[1]},device_scale_factor=2,has_touch=True)
                ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_nb','%s')}catch(e){}"%nb)
                pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:150])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
                pg.evaluate("(v)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); setPremium(v); try{Toile.setTheme('ramage')}catch(e){}}",prem); pg.wait_for_timeout(1500)
                pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2600)
                pg.evaluate("()=>{const e=[...document.querySelectorAll('#studioScreen .stp-ton')].filter(x=>x.getBoundingClientRect().width>0)[0]; if(e) e.click();}"); pg.wait_for_timeout(1300)
                e=pg.evaluate(E); print(nav,vp,'payé' if prem else 'gratuit','nb'+nb, e and (e['dev'],e['n'],e['orbe'],e['pn'],e['spec'],e['enfants']), errs[:1], flush=True)
                if e and e['orbe'] and float(e['orbe'][0])<20: pg.screenshot(path='scratchpad/v135/vide-%s-%d.png'%(nav,vp[0]))
                ctx.close()
        b.close()
