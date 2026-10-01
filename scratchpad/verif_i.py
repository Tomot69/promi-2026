from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(1800)
    print(pg.evaluate(r"""()=>{
      const i=document.querySelector('.acc-mm i'), cb=document.getElementById('createBtn');
      const cs=i?getComputedStyle(i):null, cc=cb?getComputedStyle(cb):null;
      return {i: cs?{col:cs.color, an:cs.animationName+' '+cs.animationDuration}:null,
        plus: cc?{outline:cc.outlineWidth+' '+cc.outlineStyle+' '+cc.outlineColor, off:cc.outlineOffset, r:cc.borderRadius}:null};}"""))
    b.close()
