import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
def etat(pg, t):
    print(t, pg.evaluate("""()=>{ var s=document.getElementById('createSheet'); var g=document.querySelector('#createSheet .gn');
      return {cls:s&&s.className.slice(0,120), gn:!!g, gnvis:g?getComputedStyle(g).display:'', who:(window._phrase||{}).qui||null, sel:(typeof newWhoSel!=='undefined')?JSON.stringify(newWhoSel):'?',
       act:document.activeElement&&(document.activeElement.id||document.activeElement.className), n:promises.length, ph:(document.getElementById('csPhrase')||{}).textContent} }"""))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    B.plante_doigt(pg,'rendre le livre','moi',0); etat(pg,'après A')
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(350); B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(650); etat(pg,'+')
    B.tap_sel(pg,'.acc-pil[data-k=chiche]'); pg.wait_for_timeout(2500); etat(pg,'chiche')
    B.tap_sel(pg,'#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1000); etat(pg,'qui')
    B.tap_sel(pg,'#createSheet .gn > .ph-add'); pg.wait_for_timeout(250); etat(pg,'add')
    pg.keyboard.type('Rachel',delay=25); pg.wait_for_timeout(300); B.tap_sel(pg,'#createSheet .gn > .ph-add .gn-plus'); pg.wait_for_timeout(750); etat(pg,'rachel')
    pg.keyboard.type('Marion',delay=25); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(750); etat(pg,'marion')
    pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(400)
    pg.evaluate("a=>{ document.getElementById('fTitle').value=a; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} window._csEnLair=true; window._csDueISO=null; }", 'courir dimanche'); pg.wait_for_timeout(300)
    z = pg.evaluate("()=>{ const c=document.getElementById('planterZone'); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k, getComputedStyle(c).display, getComputedStyle(c).pointerEvents] }")
    print('zone', z)
    pg.screenshot(path='scratchpad/v147/part_dbg.png')
    if z and z[2]>20:
        y=z[1]+z[3]*0.45; print('y',y, pg.evaluate("a=>{var d=document.getElementById('device').getBoundingClientRect(),k=d.width/390; var e=document.elementFromPoint(d.left+a[0]*k,d.top+a[1]*k); return e&&(e.id||e.className)}", [60,y]))
        B.glisse(pg, [[40+80*i/10.0, y] for i in range(11)], pas=60)
    pg.wait_for_timeout(3400); etat(pg,'après trait')
    print(errs)
