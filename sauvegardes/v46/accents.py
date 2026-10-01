# Tout texte VISIBLE, en capitales, en PromiLate, qui porte un É non composé (lot-V35-E-ACCENT), écran par écran.
from playwright.sync_api import sync_playwright
PROBE=r"""()=>{ const out=[]; const dev=document.getElementById('device').getBoundingClientRect();
 const w=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
 while((n=w.nextNode())){ if(!/[éÉ]/.test(n.nodeValue)) continue; const pa=n.parentElement; if(!pa||pa.closest('.v35-e')) continue;
   const cs=getComputedStyle(pa); const up=cs.textTransform==='uppercase'||/É/.test(n.nodeValue); if(!up) continue;
   const fam=(cs.fontFamily||'').split(',')[0].replace(/['"]/g,'').trim(); if(!/PromiLate/i.test(fam)) continue;
   const r=pa.getBoundingClientRect(); if(r.width<1||r.height<1) continue; if(r.bottom<dev.top||r.top>dev.bottom||r.right<dev.left||r.left>dev.right) continue;
   if(cs.visibility==='hidden'||+cs.opacity===0) continue;
   out.push((pa.id?'#'+pa.id:'')+'.'+String(pa.className).split(' ')[0]+' « '+n.nodeValue.trim().slice(0,40)+' » '+Math.round(parseFloat(cs.fontSize))+'px'); }
 return out; }"""
ECR={
 'accueil':"closeAll()",
 'page+ promi':"closeAll(); document.getElementById('createBtn').click()",
 'page+ chiche':"closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const t=[...document.querySelectorAll('[data-kind=chiche]')][0]; t&&t.click();},400)",
 'page+ nuée':"closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const t=[...document.querySelectorAll('[data-kind=nuee]')][0]; t&&t.click();},400)",
 'index':"closeAll(); document.getElementById('indexBtn')&&document.getElementById('indexBtn').click()",
 'fil':"closeAll(); document.getElementById('filBtn')&&document.getElementById('filBtn').click()",
 'partage':"closeAll(); openShare()",
 'studio':"closeAll(); document.getElementById('studioBtn').click()",
 'aura':"closeAll(); (document.getElementById('auraBtn')||{click(){}}).click()",
 'réglages':"closeAll(); (document.getElementById('settingsBtn')||document.querySelector('[data-act=reglages]')||{click(){}}).click()",
 'fiche promi':"closeAll(); openDetail(promises.filter(p=>!p.draft&&!p.nuee)[0].id)",
 'fiche nuée':"closeAll(); typeof openNuee==='function'&&openNuee(Object.keys(NUE).filter(k=>k!=='soi')[0])",
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom,js in ECR.items():
        try: pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(1600); r=pg.evaluate(PROBE)
        except Exception as e: r=['ERREUR '+str(e)[:80]]
        print('%-12s %s'%(nom, r if r else 'ok'))
        if nom=='page+ nuée': pg.locator('#device').screenshot(path='sauvegardes/v46/pageplus_nuee.png')
    b.close()
