from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True); pg = ctx.new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(5000)
    print('onboarding :', pg.evaluate("""()=>{const q=s=>{const e=document.querySelector(s); if(!e) return 'absent'; const c=getComputedStyle(e), r=e.getBoundingClientRect(); return c.display+' '+Math.round(r.width)+'×'+Math.round(r.height)+' op'+c.opacity;}; return {promiOnb:q('#promiOnb'), auth:q('#authScreen'), pseudo:q('#pseudoScreen'), apple:q('#btnApple'), onbV20:[...document.querySelectorAll('[id^=onb]')].map(e=>e.id).slice(0,12)}}"""))
    pg.evaluate('()=>{var o=document.getElementById("promiOnb");if(o){o.classList.add("gone");o.style.display="none";}}')
    pg.evaluate("()=>{const p=promises.filter(q=>!q.draft&&!q.req&&!q.nuee)[0]; openDetail(p.id);}"); pg.wait_for_timeout(1800)
    print('fiche :', pg.evaluate("""()=>{const q=s=>{const e=document.querySelector(s); if(!e) return 'absent'; const c=getComputedStyle(e), r=e.getBoundingClientRect(); return c.display+' '+c.visibility+' '+Math.round(r.width)+'×'+Math.round(r.height)+' @'+Math.round(r.left)+','+Math.round(r.top);}; return {dpBarre:q('#dpBarre'), dpbCom:q('#dpbCom'), dpbJoint:q('#dpbJoint'), dpbPart:q('#dpbPart'), dAura:q('#dAura'), dCommentInput:q('#dCommentInput'), dNote:q('#dNote')}}"""))
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"); pg.wait_for_timeout(2500)
    print('page + :', pg.evaluate("()=>({addwho:document.querySelectorAll('[data-addwho]').length, garder:[...document.querySelectorAll('#createSheet *')].filter(e=>/garder de c/i.test(e.textContent)&&e.children.length==0).map(e=>{const c=getComputedStyle(e),r=e.getBoundingClientRect(); return (e.id||e.className)+' '+c.display+' '+c.visibility+' '+Math.round(r.width)+'×'+Math.round(r.height)})})"))
    b.close()
