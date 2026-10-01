# 1 · LE DÉMARRAGE EST-IL RETARDÉ ? On compare app.html (sans le lot) et la copie (avec), même protocole.
# 2 · SUR MACHINE LENTE : processeur ralenti ×1, ×4, ×6 (substitut de Lighthouse, PAS un appareil — déclaré tel quel).
# 3 · L'OUVERTURE DU CERCLE : tout de suite après le chargement (collection incomplète) et après 22 s (prête).
import json, time
from playwright.sync_api import sync_playwright
CIBLES = [('app d’origine','http://127.0.0.1:8752/app.html'),
          ('avec le lot','http://127.0.0.1:8752/scratchpad/app-vend-toileA.html')]
PRET = "()=>{ try{ return !!(window.Toile && window.Toile.count && window.Toile.count()>0) && !!document.querySelector('#stage'); }catch(e){ return false; } }"
def mesure(pg, url, ralenti, attendre=None):
    cdp = pg.context.new_cdp_session(pg)
    cdp.send('Emulation.setCPUThrottlingRate', {'rate': ralenti})
    t0=time.time(); pg.goto(url, timeout=180000)
    pg.wait_for_function(PRET, timeout=120000)
    pret=round((time.time()-t0)*1000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setPremium(false)")
    if attendre: pg.wait_for_timeout(attendre)
    t1=time.time()
    pg.evaluate("()=>{ try{closeAll();}catch(e){} const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
    try: pg.wait_for_function("()=>{const s=document.getElementById('plusScreen');return s&&s.classList.contains('show');}", timeout=60000)
    except Exception: pass
    pg.wait_for_timeout(200)
    ouvre=round((time.time()-t1)*1000)
    v=pg.evaluate("()=>window._vendToile||null")
    f=pg.evaluate("()=>window._vendFond||null")
    cdp.send('Emulation.setCPUThrottlingRate', {'rate': 1})
    return {'pret_ms':pret, 'ouverture_ms':ouvre, 'vend':v, 'fond':f}
with sync_playwright() as p:
    br=p.chromium.launch()
    print('=== 1 · LE DÉMARRAGE (jusqu’à Toile vivante + scène présente) ===')
    for nom,url in CIBLES:
        for ral in (1,4):
            pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
            r=mesure(pg,url,ral)
            print('   %-16s processeur ×%d → prêt en %5d ms · ouverture du Cercle %5d ms%s'
                  % (nom, ral, r['pret_ms'], r['ouverture_ms'],
                     ('  (collection %d/%d bâtie en fond)'%(r['fond']['faites'],r['fond']['total'])) if r['fond'] else ''))
            pg.context.close()
    print()
    print('=== 2 · L’OUVERTURE APRÈS 22 s (le fond a eu le temps) ===')
    for ral in (1,4,6):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        r=mesure(pg,CIBLES[1][1],ral,attendre=22000)
        v=r['vend'] or {}
        print('   processeur ×%d → ouverture %5d ms · collection %s dalles (%s ms) · %s poses (%s ms) · fond bâti %s'
              % (ral, r['ouverture_ms'], v.get('collection'), v.get('collectionMs'), v.get('poses'), v.get('posesMs'),
                 ('%d/%d'%(r['fond']['faites'],r['fond']['total'])) if r['fond'] else '—'))
        pg.context.close()
    br.close()
