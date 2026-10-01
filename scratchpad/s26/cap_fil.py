from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    pg.evaluate("()=>{closeAll(); document.getElementById('filBtn').click();}"); pg.wait_for_timeout(3200)
    info=pg.evaluate(r"""()=>{
      var l=document.querySelector('#feedList')||document.getElementById('feedView');
      var out={list:l?l.id:null, n:0, cards:[]};
      var cards=document.querySelectorAll('#feedView .s4-ligne, #feedView .fd-card, #feedList > *');
      out.n=cards.length;
      [].forEach.call(document.querySelectorAll('#feedView canvas, #feedList canvas'),function(c){
        var b=c.getBoundingClientRect();
        var g=c.getContext('2d'); var d=null;
        try{ var im=g.getImageData(0,0,c.width,c.height).data; var n=0; for(var i=3;i<im.length;i+=400) if(im[i]>10)n++; d=n; }catch(e){d='err';}
        out.cards.push({cls:c.parentElement&&c.parentElement.className, w:c.width,h:c.height, bw:+b.width.toFixed(1), bh:+b.height.toFixed(1), peint:d, decl:c.getAttribute('data-matiere')});
      });
      return out;
    }""")
    print(json.dumps(info,indent=1,ensure_ascii=False)[:4000])
    for i,y in enumerate((0,600,1200,1800)):
        pg.evaluate("(y)=>{var l=document.getElementById('feedList')||document.getElementById('feedView'); l.scrollTop=y;}",y)
        pg.wait_for_timeout(1400)
        open('scratchpad/s26/fil-scroll%d.png'%i,'wb').write(pg.query_selector('#device').screenshot())
    b.close()
