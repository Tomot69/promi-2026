from playwright.sync_api import sync_playwright
import sys
F = sys.argv[1] if len(sys.argv)>1 else 'app.html'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},has_touch=True,is_mobile=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} document.getElementById('studioBtn').click();}"); pg.wait_for_timeout(3000)
    print(pg.evaluate("""()=>{ var d=document.getElementById('device').getBoundingClientRect(); var x=d.left+d.width/2, y=d.top+d.height*0.42; var e=document.elementFromPoint(x,y), r=[];
      while(e && e!==document.documentElement){ var s=getComputedStyle(e); r.push((e.id||e.className||e.tagName)+' : touch-action '+s.touchAction+' · overflow '+s.overflowY+' · user-select '+(s.webkitUserSelect||s.userSelect)+' · callout '+s.webkitTouchCallout+' · défile '+(e.scrollHeight>e.clientHeight+1)); e=e.parentElement; }
      return r.join('\\n'); }"""))
    b.close()
