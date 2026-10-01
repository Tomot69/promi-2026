#!/usr/bin/env python3
"""redteam_ajouter.py — « + AJOUTER QUELQU'UN » GARDE SA LIGNE (v116, Tom) : la liste des profils défile dans son propre espace,
aucun profil ne passe sous le bouton — page + (Chiche, « qui ose ? ») et fiche (Peaufiner, À QUI), 9 personnes, deux thèmes.
Rougi : python3 redteam_ajouter.py sauvegardes/app-avant-v116.html"""
import sys, os, shutil
from playwright.sync_api import sync_playwright
ARG=next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); tmp=None
if '/' in ARG: shutil.copy(ARG,'zz-ajouter.html'); ARG=tmp='zz-ajouter.html'
tag='juge'; ok=True
GN="#createSheet .gn, #dpdCorps .gn"
REMP="""(a)=>{const [sel,n]=a; const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10);
 if(!g||!g._gens) return 'pas de liste'; const c=g._gens; ['Anouk','Basile','Céleste','Dimitri','Elsa','Farid','Gaspard','Hortense','Ilyes'].slice(0,n).forEach(x=>{try{c.ajoute(x);}catch(e){}});
 try{ if(c.rendu) c.rendu(); else window._gens(g,c); }catch(e){} return 'ok'; }"""
GEO="""()=>{const dv=document.getElementById('device').getBoundingClientRect(),s=dv.width/390;const g=[...document.querySelectorAll('#createSheet .gn, #dpdCorps .gn')].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
 const Y=v=>Math.round((v-dv.top)/s*10)/10; const a=g.querySelector('.ph-add'); const L=g.querySelector('.gn-liste')||g; const pills=[...g.querySelectorAll('.ph-o:not(.ph-add)')];
 const ra=a?a.getBoundingClientRect():null, rl=L.getBoundingClientRect();
 const sous = ra ? pills.filter(p=>{const r=p.getBoundingClientRect(); return r.bottom>ra.top+1 && r.top<ra.bottom-1 && r.bottom>rl.top && r.top<rl.bottom;}).length : null;
 const tr=document.querySelector('#createSheet.show canvas#csTrameCv'); const pl=document.querySelector('#createSheet.show .enh, #createSheet.show .cs-top');
 const bar=g.closest('#dpdCorps')?document.getElementById('dpdTog'):null; const barre=bar?Y(bar.getBoundingClientRect().top):760;
 return {barre:barre, liste:[Y(rl.top),Y(rl.bottom)], ajouter:ra?[Y(ra.top),Y(ra.bottom)]:null, pastilles_sous_le_bouton:sous, trait:window._ppTrait||null}}"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('dark','light'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
        pg.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg.goto('http://127.0.0.1:8752/'+ARG); pg.wait_for_timeout(7000); pg.evaluate("t=>setTheme(t)",th)
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(500)
        pg.wait_for_timeout(600); pg.evaluate("()=>{document.querySelector('#createSheet .tile[data-kind=\"chiche\"]').click()}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{const e=document.querySelector('#csPhrase [data-ph=qui]'); e&&e.click()}"); pg.wait_for_timeout(1200)
        pg.evaluate(REMP,[GN,9]); pg.wait_for_timeout(1500)
        r=pg.evaluate(GEO); bon=bool(r) and r['pastilles_sous_le_bouton']==0 and r['ajouter'] is not None and r['ajouter'][1]<=r['barre']-1; ok=ok and bon
        print('%s page+ [%s] %s'%('OK' if bon else '✗',th,r))
        fid=pg.evaluate("()=>{const p=promises.find(p=>!p.draft&&!p.req&&!p.chiche&&!p.nuee&&p.who&&!/^(moi|le groupe)$/i.test(p.who));return p?p.id:null}")
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(500); pg.evaluate("(i)=>openDetail(i)",fid); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const t=document.getElementById('dpdTog'); if(t) t.click();}"); pg.wait_for_timeout(1000)
        pg.evaluate("""()=>{const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>((r.querySelector('.s2-lab')||{}).textContent||'').trim()==='À QUI'); if(r && !r.classList.contains('s2-ouv')) r.click();}"""); pg.wait_for_timeout(1000)
        pg.evaluate(REMP,[GN,9]); pg.wait_for_timeout(1500)
        r=pg.evaluate(GEO); bon=bool(r) and r['pastilles_sous_le_bouton']==0 and r['ajouter'] is not None and r['ajouter'][1]<=r['barre']-1; ok=ok and bon
        print('%s fiche [%s] %s'%('OK' if bon else '✗',th,r))
        ctx.close()
    b.close()

if tmp: os.remove(tmp)
print('✅ la liste défile dans son espace, le bouton garde sa ligne' if ok else '❌ des profils passent sous « + ajouter quelqu\'un »'); sys.exit(0 if ok else 1)
