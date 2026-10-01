from playwright.sync_api import sync_playwright
JS=r"""()=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const out=[];
  document.querySelectorAll('#detailPoster .s2-reg,#detailPoster .s2-cercle,#detailPoster .s2-encart').forEach(e=>{
    const c=getComputedStyle(e), r=e.getBoundingClientRect();
    if(c.display==='none'||r.height<6) return;
    const p=e.closest('.s2-cercle');
    out.push(Math.round((r.top-dev.top)/sc)+'  '+(e.className||'').slice(0,22)
      +'  «'+(e.textContent||'').trim().replace(/\s+/g,' ').slice(0,36)+'»'
      +'  flou='+(c.filter!=='none'?c.filter:(p?getComputedStyle(p).filter:'-'))
      +(p?'  [DANS LE CERCLE]':'  [GRATUIT]'));});
  return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{if(window.closeAll)closeAll();openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}")
    pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1400)
    for l in pg.evaluate(JS): print('  ',l)
    print('\nisPremium :', pg.evaluate("()=>(typeof isPremium!=='undefined')?isPremium:'?'"))
    b.close()
