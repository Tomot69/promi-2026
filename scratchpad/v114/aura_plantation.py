import sys, json
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
TRAP="""(()=>{ const t=setInterval(()=>{ if(!window.Toile||!Toile.dalleTrame||Toile.dalleTrame.__p) return; const o=Toile.dalleTrame;
  Toile.dalleTrame=function(cv,id,k,monde,opts){ try{ const sc=cv&&cv.closest&&cv.closest('#auraScreen'); const pile=(new Error()).stack||'';
    (window.__dt=window.__dt||[]).push({id:id, monde:monde?JSON.stringify(monde):null, plant:!!(opts&&opts.plantation), aura:!!sc||/aura|Aura|pelote|iles/.test(pile)}); }catch(_){}
    return o.apply(this,arguments); }; Toile.dalleTrame.__p=1; clearInterval(t); },20); })();"""
MO="""()=>[...document.querySelectorAll('#auraScreen .au-mo canvas')].filter(c=>c.width>0).map(c=>{const g=c.getContext('2d');const d=g.getImageData(0,0,c.width,c.height).data;let r=0,gg=0,b=0,n=0;for(let i=0;i<d.length;i+=16){if(d[i+3]>200){r+=d[i];gg+=d[i+1];b+=d[i+2];n++;}}return n?[Math.round(r/n),Math.round(gg/n),Math.round(b/n)]:null;})"""
with sync_playwright() as p:
    b=p.webkit.launch(); pg=b.new_page(viewport={'width':430,'height':932})
    pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}"+TRAP)
    pg.goto('http://127.0.0.1:8752/'+(sys.argv[1] if len(sys.argv)>1 else 'app.html')); pg.wait_for_timeout(7000)
    for studio in (('encre','signal'),('touffe','irascible')):
        pg.evaluate("(s)=>{const x=document.querySelector('#auraScreen [data-close]'); if(x&&document.getElementById('auraScreen').getBoundingClientRect().top<200) x.click(); Toile.setTheme(s[0]); Toile.setPalette(s[1]); window.__dt=[];}", list(studio)); pg.wait_for_timeout(1500)
        ouvre(pg,0); pg.wait_for_timeout(3000)
        calls=pg.evaluate("()=>window.__dt||[]"); mo=pg.evaluate(MO)
        tenus=pg.evaluate("()=>promises.filter(x=>x.status==='tenu').map(x=>x.id)")
        a=[c for c in calls if c['id'] in tenus]
        print('Studio %-18s appels dalleTrame (paroles tenues) : %d · avec le monde de plantation : %d · sans : %d'%('/'.join(studio),len(a),sum(1 for c in a if c['monde'] or c['plant']),sum(1 for c in a if not (c['monde'] or c['plant']))))
        print('   couleurs moyennes des dalles de « Ce que tu as tenu » :', mo)
    b.close()
