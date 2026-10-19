# v151 C-160 : planter « 5 j » ; recharger avec ?jour=+30 ; la parole est « à tenir » ; REPORTER depuis le Fil ; tracer
import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
ETAT = "t=>{ const p=promises.find(x=>x.title===t); return p ? {status:p.status, due:p.due, ech:p.ech||null, iso:p.dueISO||null, mot:(window.motDuTemps?motDuTemps(p).mot:'')} : null; }"
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx, F)
    B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=promi]'); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{ document.getElementById('fTitle').value='rendre le livre'; const c=document.querySelector('#dueChips .chip[data-d=\"5\"]'); c && c.click(); }")
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2800); pg.evaluate("()=>{try{closeAll()}catch(e){}}")
    print('planté     ', pg.evaluate(ETAT, 'rendre le livre'))
    pg.goto('http://127.0.0.1:8752/%s?jour=+30' % F); pg.wait_for_timeout(6500)
    print('jour +30   ', pg.evaluate(ETAT, 'rendre le livre'))
    print('Fil        ', pg.evaluate("()=>FEED.filter(f=>{const p=promises.find(x=>x.id===f.pid);return p&&p.title==='rendre le livre';}).map(f=>[f.id,f.type])"))
    fid = pg.evaluate("()=>{const f=FEED.find(f=>{const p=promises.find(x=>x.id===f.pid);return p&&p.title==='rendre le livre';});return f?f.id:null}")
    if fid is not None:
        pg.evaluate("i=>_fpost(i,3)", fid); pg.wait_for_timeout(500)
        print('reporter +3', pg.evaluate(ETAT, 'rendre le livre'))
    pg.goto('http://127.0.0.1:8752/%s?jour=+30' % F); pg.wait_for_timeout(6500)
    print('recharge   ', pg.evaluate(ETAT, 'rendre le livre'))
    pg.goto('http://127.0.0.1:8752/%s?jour=+40' % F); pg.wait_for_timeout(6500)
    print('jour +40   ', pg.evaluate(ETAT, 'rendre le livre'))
    print('erreurs', pg.erreurs[:3]); b.close()
