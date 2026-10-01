import sys
from playwright.sync_api import sync_playwright
tag=sys.argv[1]
GN="#createSheet .gn, #dpdCorps .gn"
REMP="""(a)=>{const [sel,n]=a; const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10);
 if(!g||!g._gens) return 'pas de liste'; const c=g._gens; ['Anouk','Basile','Céleste','Dimitri','Elsa','Farid','Gaspard','Hortense','Ilyes'].slice(0,n).forEach(x=>{try{c.ajoute(x);}catch(e){}});
 try{ if(c.rendu) c.rendu(); else window._gens(g,c); }catch(e){} return 'ok'; }"""
GEO="""()=>{const dv=document.getElementById('device').getBoundingClientRect(),s=dv.width/390;const g=[...document.querySelectorAll('#createSheet .gn, #dpdCorps .gn')].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
 const Y=v=>Math.round((v-dv.top)/s*10)/10; const a=g.querySelector('.ph-add'); const L=g.querySelector('.gn-liste')||g; const pills=[...g.querySelectorAll('.ph-o:not(.ph-add)')];
 const ra=a?a.getBoundingClientRect():null, rl=L.getBoundingClientRect();
 const sous = ra ? pills.filter(p=>{const r=p.getBoundingClientRect(); return r.bottom>ra.top+1 && r.top<ra.bottom-1 && r.bottom>rl.top && r.top<rl.bottom;}).length : null;
 const tr=document.querySelector('#createSheet.show canvas#csTrameCv'); const pl=document.querySelector('#createSheet.show .enh, #createSheet.show .cs-top');
 return {liste:[Y(rl.top),Y(rl.bottom)], ajouter:ra?[Y(ra.top),Y(ra.bottom)]:null, pastilles_sous_le_bouton:sous, trait:window._ppTrait||null}}"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('dark','light'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
        pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000); pg.evaluate("t=>setTheme(t)",th)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(500)
        pg.wait_for_timeout(600); pg.evaluate("()=>{document.querySelector('#createSheet .tile[data-kind=\"chiche\"]').click()}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{const e=document.querySelector('#csPhrase [data-ph=qui]'); e&&e.click()}"); pg.wait_for_timeout(1200)
        pg.evaluate(REMP,[GN,9]); pg.wait_for_timeout(1500)
        print(tag,th,'page+', pg.evaluate(GEO)); pg.screenshot(path='preuves-v116/gens-%s-pageplus-%s.png'%(tag,th),clip={'x':20,'y':44,'width':390,'height':844})
        fid=pg.evaluate("()=>{const p=promises.find(p=>!p.draft&&!p.req&&!p.chiche&&!p.nuee&&p.who&&!/^(moi|le groupe)$/i.test(p.who));return p?p.id:null}")
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(500); pg.evaluate("(i)=>openDetail(i)",fid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const t=document.getElementById('dpdTog'); if(t) t.click();}"); pg.wait_for_timeout(1000)
        pg.evaluate("""()=>{const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>((r.querySelector('.s2-lab')||{}).textContent||'').trim()==='À QUI'); if(r && !r.classList.contains('s2-ouv')) r.click();}"""); pg.wait_for_timeout(1000)
        pg.evaluate(REMP,[GN,9]); pg.wait_for_timeout(1500)
        print(tag,th,'fiche', pg.evaluate(GEO)); pg.screenshot(path='preuves-v116/gens-%s-fiche-%s.png'%(tag,th),clip={'x':20,'y':44,'width':390,'height':844})
        ctx.close()
    b.close()
