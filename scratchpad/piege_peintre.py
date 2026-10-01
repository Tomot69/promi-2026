from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate(r"""()=>{ window.__piege=[];
      const sp=CSSStyleDeclaration.prototype.setProperty;
      CSSStyleDeclaration.prototype.setProperty=function(k,v,pr){
        try{ if((k==='color'||k==='-webkit-text-fill-color') && String(v).indexOf('0, 52, 26')>=0 || String(v).toUpperCase().indexOf('00341A')>=0){
          window.__piege.push((new Error()).stack.split('\n').slice(1,5).join(' | ')); } }catch(_){}
        return sp.call(this,k,v,pr); };}""")
    pg.evaluate("()=>{closeAll(); const p=promises.find(p=>p.status==='tenu'&&!p.nuee); if(p) openDetail(p.id);}")
    pg.wait_for_timeout(2600)
    st=pg.evaluate("()=>window.__piege.slice(-6)")
    for s in st: print(s[:260]); print('---')
    b.close()
