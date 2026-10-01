from playwright.sync_api import sync_playwright
import sys, json
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1800,'height':1200}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/PLANCHE-AURA-TROIS-PARTIS.html')
    pg.wait_for_function("()=>window.__pret===true", timeout=30000)
    pg.wait_for_timeout(2500)
    figs = pg.query_selector_all('figure')
    names=[]
    for i,fg in enumerate(figs):
        cap = fg.query_selector('figcaption').inner_text().replace(' ','_').replace('·','-').replace('/','-')[:38]
        fr = fg.query_selector('.fr')
        path=f'scratchpad/partis/{i:02d}.png'
        fr.screenshot(path=path)
        names.append((path,cap))
    print(json.dumps(names, ensure_ascii=False, indent=1))
    # controle de recouvrement : au DOIGT, dans chaque cadre
    res = pg.evaluate("""()=>{
      const out=[];
      document.querySelectorAll('.fr').forEach((f,fi)=>{
        const ns=[...f.querySelectorAll('*')].filter(n=>{
          const cs=getComputedStyle(n), r=n.getBoundingClientRect();
          if(cs.display==='none'||cs.visibility==='hidden'||r.width<1||r.height<1) return false;
          // on ne compare que les FEUILLES porteuses de contenu
          return n.children.length===0;
        });
        for(let i=0;i<ns.length;i++)for(let j=i+1;j<ns.length;j++){
          const a=ns[i].getBoundingClientRect(), b=ns[j].getBoundingClientRect();
          if(ns[i].contains(ns[j])||ns[j].contains(ns[i]))continue;
          const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left);
          const oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
          if(ox>2&&oy>2){
            // confirme AU DOIGT au centre du recouvrement
            const cx=(Math.max(a.left,b.left)+Math.min(a.right,b.right))/2;
            const cy=(Math.max(a.top,b.top)+Math.min(a.bottom,b.bottom))/2;
            const els=document.elementsFromPoint(cx,cy);
            if(els.indexOf(ns[i])>=0 && els.indexOf(ns[j])>=0)
              out.push(fi+' :: '+(ns[i].className||ns[i].tagName)+' « '+(ns[i].textContent||'').trim().slice(0,20)+' »'
                       +'  ⨯  '+(ns[j].className||ns[j].tagName)+' « '+(ns[j].textContent||'').trim().slice(0,20)+' »'
                       +'  ('+Math.round(ox)+'x'+Math.round(oy)+')');
          }
        }
      });
      return out;
    }""")
    print('\n── RECOUVREMENTS CONFIRMÉS AU DOIGT :', len(res))
    for r in res[:40]: print('   ', r)
    # debordements
    ded = pg.evaluate("""()=>{const out=[];
      document.querySelectorAll('.fr').forEach((f,fi)=>{const F=f.getBoundingClientRect();
        f.querySelectorAll('*').forEach(n=>{const cs=getComputedStyle(n),r=n.getBoundingClientRect();
          if(cs.display==='none'||r.width<1)return;
          if(r.left<F.left-0.5||r.right>F.right+0.5||r.top<F.top-0.5||r.bottom>F.bottom+0.5)
            out.push(fi+' :: '+(n.className||n.tagName)+' « '+(n.textContent||'').trim().slice(0,22)+' » x'
              +Math.round(r.left-F.left)+' → '+Math.round(r.right-F.left)+' / y'+Math.round(r.top-F.top)+' → '+Math.round(r.bottom-F.top));});});
      return out;}""")
    print('\n── HORS CADRE :', len(ded))
    for r in ded[:30]: print('   ', r)
    b.close()
