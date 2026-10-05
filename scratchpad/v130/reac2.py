import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'app.html'
ETAT=r"""()=>{ const vis=(e)=>{ if(!e) return false; const r=e.getBoundingClientRect(); return r.width>0&&r.top<800&&r.bottom>60; };
  const sc=(id)=>{const e=document.getElementById(id); return !!e&&(e.classList.contains('show')||e.classList.contains('in'));};
  return { ouverts:['indexSheet','feedView','auraScreen','detailPoster','createSheet'].filter(sc).join(','),
    auraVue: vis(document.querySelector('#auraScreen .au-bo')),
    index:[...document.querySelectorAll('#indexList .s4-ti')].map(e=>e.textContent.trim()),
    fil:[...document.querySelectorAll('#feedList [data-pid], #feedList .s4f-ti, #feedList .s5-ti')].map(e=>(e.textContent||'').trim().slice(0,30)),
    filN:document.querySelectorAll('#feedList > *').length,
    moisson:[...document.querySelectorAll('#auraScreen .au-mo *')].filter(e=>e.children.length===0).map(e=>e.textContent.trim()).filter(Boolean),
    nf:[...document.querySelectorAll('.nf-item')].map(e=>e.innerText.replace(/\s+/g,' ').slice(0,40)),
    data:{ n:promises.filter(p=>!p.draft&&!p.req).length, tenus:promises.filter(p=>p.status==='tenu'&&!p.draft&&!p.req&&(!p.from||p.from==='moi')).map(p=>p.title) } }; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:140])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def img(): pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))")
    e=pg.evaluate(ETAT); print('DÉPART index',len(e['index']),'fil',e['filN'],'tenus',e['data']['tenus']); 
    print('promesses :', pg.evaluate("()=>promises.map(p=>p.id+':'+p.title+'/'+p.status+'/'+(p.nuee||p.essaim||'-')+'/'+(p.from||'')+(p.draft?'/gardé':'')+(p.req?'/req':'')).join(' | ')")[:1500])
    # A · AURA ouverte, on ouvre une fiche « en cours » par openDetail (comme la porte d'une dalle), on la tient par segStatus, on revient
    pg.evaluate("()=>{closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(2500)
    e=pg.evaluate(ETAT); print('A0 Aura ouverte :', e['ouverts'], e['auraVue'], e['moisson'])
    cible=pg.evaluate("()=>{const p=promises.find(p=>p.status!=='tenu'&&!p.draft&&!p.req&&(!p.from||p.from==='moi')); return p?[p.id,p.title]:null}"); print('cible',cible)
    pg.evaluate("(id)=>{ const p=promises.find(q=>q.id===id); p.status='tenu'; if(window.syncAll) syncAll(); }", cible[0]); img()
    e=pg.evaluate(ETAT); print('A1 tenue (données + syncAll), Aura restée ouverte :', e['moisson'], '| attendu en tête :', cible[1])
    pg.wait_for_timeout(1500); e=pg.evaluate(ETAT); print('A1 +1,5 s :', e['moisson'])
    pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{document.getElementById('souffleBtn').click();}"); img(); e=pg.evaluate(ETAT); print('A2 Aura rouverte :', e['moisson'])
    # B · INDEX ouvert, on retire une parole par les données + syncAll
    pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); if(x) x.click(); closeAll(); ouvrirIndex();}"); pg.wait_for_timeout(1800)
    e=pg.evaluate(ETAT); print('B0 Index ouvert :', e['ouverts'], len(e['index']))
    pg.evaluate("(id)=>{ promises=promises.filter(q=>q.id!==id); if(window.syncAll) syncAll(); }", cible[0]); img()
    e=pg.evaluate(ETAT); print('B1 retirée, Index resté ouvert :', len(e['index']), cible[1] in e['index'])
    # C · la vraie suppression : fiche ouverte DEPUIS l'Index, Supprimer ×2
    c2=pg.evaluate("()=>{const p=promises.find(p=>!p.draft&&!p.req&&!(p.nuee)&&p.status!=='tenu'); return [p.id,p.title]}"); print('cible 2',c2)
    pg.evaluate("(t)=>{ const c=[...document.querySelectorAll('#indexList .s4-carte')].find(c=>c.innerText.includes(t)); c.click(); }", c2[1]); pg.wait_for_timeout(2200)
    e=pg.evaluate(ETAT); print('C0 fiche ouverte depuis l\'Index :', e['ouverts'])
    pg.evaluate("()=>{ const b=document.getElementById('actDel'); b.click(); b.click(); }"); img()
    e=pg.evaluate(ETAT); print('C1 après Supprimer ×2 :', e['ouverts'], 'cartes', len(e['index']), 'encore là ?', c2[1] in e['index'], '· données', pg.evaluate("(id)=>promises.some(p=>p.id===id)", c2[0]))
    pg.wait_for_timeout(1500); e=pg.evaluate(ETAT); print('C1 +1,5 s :', e['ouverts'], len(e['index']), c2[1] in e['index'])
    b.close()
