import json, re, sys
from playwright.sync_api import sync_playwright
OCC=json.load(open('scratchpad/v114/dette-occ.json'))
SELS=sorted(set(o['sel'] for o in OCC if o['type']=='css' and o['sel']))
TRAP="""(()=>{window.__cvtrap={}; const P=CanvasRenderingContext2D.prototype;
 function note(k){ try{ const st=(new Error()).stack.split('\\n').slice(1,4).join(' | '); const m=st.match(/(app\\.html|promi-moteur\\.js)[^:]*:(\\d+):/); const key=k+'@'+(m?m[1]+':'+m[2]:'?'); window.__cvtrap[key]=(window.__cvtrap[key]||0)+1; }catch(_){} }
 ['createLinearGradient','createRadialGradient','createConicGradient'].forEach(function(f){ const o=P[f]; if(o) P[f]=function(){ note(f); return o.apply(this,arguments); }; });
 const d=Object.getOwnPropertyDescriptor(P,'shadowBlur'); if(d&&d.set) Object.defineProperty(P,'shadowBlur',{set:function(v){ if(v>0) note('shadowBlur'); d.set.call(this,v); }, get:d.get, configurable:true});
})();"""
SCAN="""(sels)=>{ const dv=document.getElementById('device').getBoundingClientRect(); const out={};
 function vis(e){ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return false; if(r.bottom<dv.top||r.top>dv.bottom||r.right<dv.left||r.left>dv.right) return false;
   const c=getComputedStyle(e); return c.visibility!=='hidden' && c.display!=='none' && +c.opacity>0.02; }
 function feat(c){ const f=[]; if(/gradient/.test(c.backgroundImage)) f.push('bg'); if(c.maskImage&&/gradient/.test(c.maskImage)||c.webkitMaskImage&&/gradient/.test(c.webkitMaskImage)) f.push('mask');
   if(c.boxShadow&&c.boxShadow!=='none') f.push('bs'); if(c.textShadow&&c.textShadow!=='none') f.push('ts'); if(/drop-shadow/.test(c.filter)) f.push('ds'); return f; }
 for(const s of sels){ let q=s.replace(/::?(before|after)/g,''); let pseudo=/::?before/.test(s)?'::before':(/::?after/.test(s)?'::after':null);
   let els=[]; try{ for(const part of q.split(',')){ try{ els=els.concat([...document.querySelectorAll(part.trim()||'*:not(*)')]); }catch(_){} } }catch(_){}
   for(const e of els){ if(!vis(e)) continue; const c=getComputedStyle(e,pseudo); if(pseudo && (c.content==='none'||c.content==='normal')) continue; const f=feat(c); if(f.length){ out[s]=(out[s]||[]).concat([f.join('+')+'|'+(c.backgroundImage||'').slice(0,160)]); break; } } }
 return out; }"""
ECRANS=[('accueil',"()=>{closeAll()}"),('index',"()=>{closeAll();document.getElementById('indexBtn').click()}"),('fil',"()=>{closeAll();document.getElementById('filBtn').click()}"),
 ('fiche promi',"()=>{closeAll();openDetail(promises.find(p=>p.title==='nager le mardi').id)}"),('fiche chiche',"()=>{closeAll();openDetail(promises.find(p=>p.title==='courir dimanche').id)}"),
 ('fiche tenue',"()=>{closeAll();openDetail(promises.find(p=>p.title==='planter un arbre').id)}"),('fiche cercle',"()=>{closeAll();openEssaim('potager')}"),
 ('peaufiner',"()=>{closeAll();openDetail(promises.find(p=>p.title==='nager le mardi').id);setTimeout(()=>{const d=document.getElementById('dpDetails');d&&d.classList.add('ouvert')},600)}"),
 ('page+ promi',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=document.querySelector('#createSheet .tile[data-kind=\\\"promi\\\"]');x&&x.click()},400)}"),
 ('page+ chiche',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=document.querySelector('#createSheet .tile[data-kind=\\\"chiche\\\"]');x&&x.click()},400)}"),
 ('page+ cercle',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=document.querySelector('#createSheet .tile[data-kind=\\\"nuee\\\"]');x&&x.click()},400)}"),
 ('studio',"()=>{closeAll();document.getElementById('studioBtn').click()}"),('aura',"()=>{closeAll();document.getElementById('souffleBtn').click()}"),
 ('partager',"()=>{closeAll();openShare()}"),('ma parole',"()=>{closeAll();ouvreCercle()}"),('reglages',"()=>{closeAll();const b=document.querySelector('#accPlat [aria-label*=églage], #setBtn, .acc-reglages');b&&b.click()}")]
vus={}; cv={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932}); ctx.add_init_script(TRAP+"try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        for nom,js in ECRANS:
            try:
                pg.evaluate("t=>setTheme(t)",th); pg.evaluate(js); pg.wait_for_timeout(1800)
                r=pg.evaluate(SCAN,SELS)
                for s,v in r.items(): vus.setdefault(s,set()).add('%s/%s'%(nom,th))
            except Exception as e: print('écran',nom,th,'✗',str(e)[:80])
        for k,v in pg.evaluate("()=>window.__cvtrap").items(): cv[k]=cv.get(k,0)+v
        ctx.close()
    b.close()
json.dump({'css':{k:sorted(v) for k,v in vus.items()},'canvas':cv},open('scratchpad/v114/dette-vus.json','w'),ensure_ascii=False,indent=0)
print('sélecteurs rendus :',len(vus),'/',len(SELS)); print('canevas :',cv)
