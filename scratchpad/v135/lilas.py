from playwright.sync_api import sync_playwright
J="""()=>{ const D=document.getElementById('device').getBoundingClientRect(); const lin=v=>{v/=255; return v<=0.04045?v/12.92:Math.pow((v+0.055)/1.055,2.4)}, L=c=>0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);
  const rgb=s=>(s.match(/[\\d.]+/g)||[]).map(Number); const out={};
  const fond=e=>{ while(e&&e.nodeType===1){ const c=rgb(getComputedStyle(e).backgroundColor); if(c.length>=3&&(c.length<4||c[3]>0.85)) return c; e=e.parentElement;} return null };
  document.querySelectorAll('#detailPoster *, #createSheet *').forEach(e=>{ if(!e.getClientRects().length) return; const t=[...e.childNodes].filter(n=>n.nodeType===3&&n.nodeValue.trim()).map(n=>n.nodeValue.trim()).join(' '); const ph=e.placeholder; if(!t&&!ph) return;
    const s=getComputedStyle(e); if(s.visibility==='hidden'||s.display==='none'||+s.opacity<0.1) return; const r=e.getBoundingClientRect(); if(r.bottom<D.top||r.top>D.bottom) return;
    const f=fond(e); if(!f||Math.abs(f[0]-14)+Math.abs(f[1]-120)+Math.abs(f[2]-242)>6) return;
    const col=rgb(ph&&!t? getComputedStyle(e,'::placeholder').color : (s.webkitTextFillColor||s.color)); const a=L(col),b=L(f); const k=((Math.max(a,b)+0.05)/(Math.min(a,b)+0.05));
    const cle=col.slice(0,3).join(','); (out[cle]=out[cle]||{k:k.toFixed(2),ex:[]}).ex.push((e.id||String(e.className).split(' ')[0])+':'+(t||ph).slice(0,22)); });
  return out }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark'); setPremium(true)}"); pg.wait_for_timeout(500)
    for nom,js,peauf in (('fiche à tenir','openDetail(126)',0),('fiche en cours','openDetail(128)',0),('Peaufiner','openDetail(128)',1),('Peaufiner bas','openDetail(128)',2),('page +',None,0),('page + Peaufiner',None,1)):
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(400)
        if js: pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(2500)
        else:
            pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
            for k in range(3): pg.evaluate("()=>{const t=document.querySelectorAll('#createSheet .tile')[0]; if(t) t.click();}"); pg.wait_for_timeout(500)
            pg.wait_for_timeout(1500)
        if peauf:
            pg.evaluate("()=>{const x=document.querySelector(document.getElementById('createSheet').classList.contains('show')?'#createSheet .cbb, #csBotBar':'#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1600)
            if peauf==2: pg.evaluate("()=>{const c=document.getElementById('dpdCorps'); if(c) c.scrollTop=9999;}"); pg.wait_for_timeout(500)
        r=pg.evaluate(J); print('==',nom)
        for c,v in sorted(r.items(), key=lambda x: float(x[1]['k'])): print('   rgb(%s)  %s:1  ×%d  %s'%(c,v['k'],len(v['ex']),' | '.join(v['ex'][:5])))
    b.close()
