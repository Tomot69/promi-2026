from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(5000)
    print(pg.evaluate("""()=>{ const T=window._teinte, f=[14,120,242]; const hx=c=>'#'+c.map(v=>(Math.round(v)<16?'0':'')+Math.round(v).toString(16)).join('').toUpperCase();
      const lin=v=>{v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4)}, L=c=>0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]), K=(a,b)=>{const x=L(a),y=L(b); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)};
      const o=T.ajuste([251,76,13],f,3), l=T.ajuste([196,162,245],f,4.5), l2=T.ajuste([196,162,245],f,4.2), l1=T.ajuste([196,162,245],f,4.0);
      return {orange:hx(o), ko:K(o,f).toFixed(2), lilas45:hx(l), kl:K(l,f).toFixed(2), lilas42:hx(l2), k42:K(l2,f).toFixed(2), lilas40:hx(l1), k40:K(l1,f).toFixed(2), blanc:K([255,255,255],f).toFixed(2), creme:K([247,240,222],f).toFixed(2), src:String(T.ajuste).slice(0,900)} }"""))
    b.close()
