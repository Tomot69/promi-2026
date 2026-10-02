from playwright.sync_api import sync_playwright
J = r"""()=>{ const out={}; const pals=(Toile.palettes?Toile.palettes():null)||Object.keys(window.PALETTES||{}); out.pals=pals&&pals.slice?pals.slice(0,30):pals;
  out.api=Object.keys(Toile).filter(k=>/pal|col/i.test(k));
  const P=promises.filter(q=>!q.draft&&!q.req&&!q.nuee&&!q.photo&&!q.chiche)[0], C=promises.filter(q=>q.chiche&&!q.draft)[0];
  out.promi={t:P.title, monde:P.monde, dalle:P.dalle, st:P.status}; out.chiche=C?{t:C.title, monde:C.monde, dalle:C.dalle, st:C.status}:null;
  const nat={promi:'#82AEF8', chiche:'#FFB8D2'};
  out.essais=[];
  for(const pal of ['signal','primesautier','irascible','allegre','taciturne','truculent']){ for(const ci of [0,1,2,3]){
    for(const [nm,q] of [['promi',P],['chiche',C]]){ if(!q) continue; const av=[q.monde,q.dalle,q.dalleOrigine];
      q.monde={m:'encre',p:pal,h:0}; q.dalle={ci:ci,lit:(av[1]&&av[1].lit)||0}; q.dalleOrigine=true;
      const r=window._origineBande(q, nat[nm]); out.essais.push([nm,pal,ci,r?+r.dE.toFixed(1):null]);
      q.monde=av[0]; q.dalle=av[1]; q.dalleOrigine=av[2]; } } }
  return out; }"""
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    o = pg.evaluate(J)
    print(o['api']); print(o['pals']); print(o['promi']); print(o['chiche'])
    for e in o['essais']: print(e)
    b.close()
