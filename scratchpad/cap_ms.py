from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu-vsync','--disable-frame-rate-limit'])
    pg=b.new_page(viewport={'width':1400,'height':1100},device_scale_factor=1)
    e=[]; pg.on('pageerror',lambda x:e.append(str(x)))
    pg.goto('http://127.0.0.1:8752/PLANCHE-PAVAGE.html')
    pg.wait_for_function("()=>window.__pret===true",timeout=300000)
    r=pg.evaluate("""()=>{
      var out={};
      ['hero','m-encre','m-pixel','m-gravure'].forEach(function(id){
        var c=document.querySelector('canvas[data-cad="'+id+'"]');
        if(!c||!c.__opt){ out[id]='absent'; return; }
        var o=c.__opt, T=[];
        for(var i=0;i<26;i++){
          o.rot=(o.rot||0)+0.05;
          var t0=performance.now(); peint(c,o); T.push(performance.now()-t0);
        }
        T.shift(); T.shift();                    /* les deux premieres chauffent */
        T.sort(function(a,b){return a-b;});
        var n=T.length;
        out[id]={css:o.css, med:Math.round(T[n>>1]*10)/10,
                 p90:Math.round(T[Math.floor(n*0.9)]*10)/10};
      });
      return out;
    }""")
    print("ms par image (cadre 620 px, sphere en rotation) :", r)
    print("erreurs:",e[:3])
    b.close()
