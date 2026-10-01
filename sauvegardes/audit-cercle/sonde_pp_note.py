# SONDE : pourquoi la NOTE de la page + ne grandit-elle pas ? On piège les écritures de hauteur sur la zone (§7 : qui d'autre écrit).
from playwright.sync_api import sync_playwright
LONG = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1800)
    print(pg.evaluate("""()=>{ const cs=document.getElementById('createSheet'); const zs=[...document.querySelectorAll('#createSheet .s2-zone')];
      return {pp_peauf: cs.classList.contains('pp-peauf'), zones: zs.map(z=>({cls:z.className, h:z.getBoundingClientRect().height, style:z.getAttribute('style'), ta:(z.querySelector('textarea')||{}).id, taStyle:(z.querySelector('textarea')||{getAttribute:()=>null}).getAttribute('style'), lignes:z.getAttribute('data-cercle-lignes')}))}; }"""))
    pg.evaluate("""()=>{ window.__J=[]; const z=document.querySelector('#createSheet .s2-zone'); const ta=z.querySelector('textarea');
      [z,ta].forEach((el,i)=>{ const sp=el.style.setProperty.bind(el.style); el.style.setProperty=function(k,v,pr){ if(/height/.test(k)) window.__J.push([i?'ta':'z',k,v,pr||'',(new Error()).stack.split('\\n').slice(2,5).join(' | ')]); return sp(k,v,pr); }; });
      const mo=new MutationObserver(ms=>ms.forEach(m=>{ if(m.attributeName==='style') window.__J.push([m.target===z?'z':'ta','attr',String(m.target.getAttribute('style')).slice(0,160)]); })); mo.observe(z,{attributes:true}); mo.observe(ta,{attributes:true});
      }""")
    pg.evaluate("(t)=>{ const ta=document.querySelector('#createSheet .s2-zone textarea'); ta.value=t; ta.dispatchEvent(new Event('input',{bubbles:true})); }", LONG); pg.wait_for_timeout(1500)
    for j in pg.evaluate("()=>window.__J"): print('  ', j)
    print(pg.evaluate("""()=>{ const z=document.querySelector('#createSheet .s2-zone'); const ta=z.querySelector('textarea'); const k=getComputedStyle(ta);
      return {h:z.getBoundingClientRect().height, zstyle:z.getAttribute('style'), taH:ta.getBoundingClientRect().height, taMax:k.maxHeight, taStyle:ta.getAttribute('style'), lignes:z.getAttribute('data-cercle-lignes'), lh:k.lineHeight, w:ta.getBoundingClientRect().width}; }"""))
    br.close()
