# Premier passage au doigt de la fiche intégrée (pas encore le juge) — ce qui s'affiche vraiment.
import sys, json, os
from playwright.sync_api import sync_playwright
O='sauvegardes/audit-fiche-personne/apres/'
def page(b):
    pg=b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2); err=[]; pg.on('pageerror', lambda e: err.append(str(e)))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); return pg, err
def aura_tap(pg, nom):
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}"); pg.wait_for_timeout(250)
    pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    pg.wait_for_timeout(600)
    pt=pg.evaluate("""(n)=>{ const lb=[...document.querySelectorAll('#auraScreen .au-lb')].find(e=>e.textContent.trim()===n); const l=lb.getBoundingClientRect(), cx=l.left+l.width/2; let best=null, bd=1e9;
        for(const x of document.querySelectorAll('#auraScreen .au-nb')){ const r=x.getBoundingClientRect(), d=Math.abs(r.left+r.width/2-cx)+Math.abs(r.bottom-l.top); if(d<bd){bd=d; best=[r.left+r.width/2, r.top+r.height/2];} } return best; }""", nom)
    pg.mouse.click(pt[0], pt[1]); pg.wait_for_timeout(1600)
ETAT=r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, c=document.getElementById('psCadre'); if(!c) return {cadre:null};
  const R=(e)=>{const r=e.getBoundingClientRect(); return [Math.round((r.left-dv.left)/s),Math.round((r.top-dv.top)/s),Math.round(r.width/s),Math.round(r.height/s)];};
  const cartes=[...c.querySelectorAll('.s4-carte')].map(k=>{ const cv=k.querySelector('canvas'); let n=0,t=0; try{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; for(let i=3;i<d.length;i+=64){t++; if(d[i]>10)n++;} }catch(e){}
    return {ti:(k.querySelector('.s4-ti')||{}).textContent, eb:(k.querySelector('.s4-eb')||{}).textContent, et:(k.querySelector('.s4-et')||{}).textContent, box:R(k), peint:t?+(n/t).toFixed(2):null}; });
  const dal=[...c.querySelectorAll('.ps-c canvas')].map(cv=>{ let n=0,t=0; const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; for(let i=3;i<d.length;i+=16){t++; if(d[i]>10)n++;} return +(n/t).toFixed(2); });
  const vieux=['.ps-head','#psMirror','#psList','.grip'].map(q=>{ const e=document.querySelector('#personSheet '+q); return q+':'+(e?getComputedStyle(e).display:'absent'); });
  return {cadre:R(c), fiche:document.getElementById('personSheet').classList.contains('show'), nom:document.getElementById('psName').textContent,
    nomPolice:getComputedStyle(document.getElementById('psName')).fontWeight, noyau:R(c.querySelector('.ps-ny')), titres:[...c.querySelectorAll('.ps-h')].map(e=>e.textContent+' '+R(e)),
    cartes:cartes, dalles:dal, gestes:[...c.querySelectorAll('.ps-bt')].map(e=>e.textContent+' '+R(e)), vieux:vieux, avant:getComputedStyle(document.getElementById('personSheet'),'::before').display, comp:window._ficheComp}; }"""
def shot(pg, nom):
    dv=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
    pg.screenshot(path=O+nom+'.png', clip={'x':dv[0],'y':dv[1],'width':dv[2],'height':dv[3]})
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ('dark','light'):
        pg,err=page(b); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        aura_tap(pg,'Rachel'); r=pg.evaluate(ETAT); print('=== %s · Rachel (au doigt, depuis l\'Aura)' % th); print(json.dumps(r, ensure_ascii=False)); shot(pg,'essai-rachel-'+th)
        pg.evaluate("()=>{ const c=document.querySelector('#psCadre .ps-col'); c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(400); shot(pg,'essai-rachel-bas-'+th)
        pg.evaluate("()=>{ openPerson('Nico'); }"); pg.wait_for_timeout(1200); print('   Nico :', json.dumps(pg.evaluate(ETAT), ensure_ascii=False)[:400]); shot(pg,'essai-nico-'+th)
        print('   erreurs de page :', err[:3]); pg.close()
    # LES DEUX GESTES, au doigt, jusqu'au Promi planté
    for geste, chiche in (('promi',False),('chiche',True)):
        pg,err=page(b); aura_tap(pg,'Rachel')
        pg.evaluate("()=>{ const c=document.querySelector('#psCadre .ps-col'); c.scrollTop=c.scrollHeight; }"); pg.wait_for_timeout(400)
        bx=pg.evaluate("(g)=>{ const e=document.querySelector('#psCadre .ps-bt[data-geste='+g+']'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }", geste)
        pg.mouse.click(bx[0], bx[1]); pg.wait_for_timeout(1400)
        st=pg.evaluate("""()=>({page:document.getElementById('createSheet').classList.contains('show'), fiche:document.getElementById('personSheet').classList.contains('show'),
            qui:window._phrase&&window._phrase.qui, sens:window.csSens&&window.csSens(), kind:window.createKind, fWho:(document.getElementById('fWho')||{}).value, sel:window.newWhoSel,
            phrase:((document.getElementById('csPhrase')||{}).textContent||'').replace(/\\s+/g,' ').trim().slice(0,90)})""")
        print('=== geste %s : %s' % (geste, json.dumps(st, ensure_ascii=False)))
        shot(pg,'essai-geste-'+geste)
        n0=pg.evaluate("()=>promises.length")
        fentes=pg.evaluate("()=>[...document.querySelectorAll('#csPhrase [data-ph]')].map(e=>{const r=e.getBoundingClientRect(); return {ph:e.getAttribute('data-ph'), t:(e.textContent||'').trim().slice(0,30), vis:r.width>0, xy:[r.left+r.width/2,r.top+r.height/2]};})")
        print('   fentes de la phrase :', json.dumps(fentes, ensure_ascii=False))
        ti=[x for x in fentes if x['ph'] in ('titre','quoi','de') and x['vis']]
        if ti: pg.mouse.click(ti[0]['xy'][0], ti[0]['xy'][1]); pg.wait_for_timeout(400)
        print('   focus après le toucher :', pg.evaluate("()=>{const a=document.activeElement; return a?(a.id||a.tagName)+' '+(a.getAttribute('contenteditable')||''):null;}"))
        pg.keyboard.type('essai du geste '+geste, delay=20); pg.wait_for_timeout(300)
        print('   #fTitle après la frappe :', pg.evaluate("()=>(document.getElementById('fTitle')||{}).value"))
        pa=pg.evaluate("()=>{const a=document.getElementById('planterAlt'); if(!a) return null; const r=a.getBoundingClientRect(); return r.width?[r.left+r.width/2,r.top+r.height/2]:null;}")
        if pa: pg.mouse.click(pa[0],pa[1]); pg.wait_for_timeout(400)
        ap=pg.evaluate("()=>{const a=document.getElementById('addPromi'); if(!a) return null; const r=a.getBoundingClientRect(); return r.width?[r.left+r.width/2,r.top+r.height/2]:null;}")
        if ap: pg.mouse.click(ap[0],ap[1]); pg.wait_for_timeout(1200)
        nouv=pg.evaluate("(n0)=>promises.slice(n0).map(p=>({t:p.title, who:p.who, from:p.from||null, chiche:!!p.chiche, etat:p.chicheEtat||null}))", n0)
        print('   bascule %s · bouton %s · planté : %s · erreurs %s' % (bool(pa), bool(ap), json.dumps(nouv, ensure_ascii=False), err[:2])); pg.close()
    b.close()
