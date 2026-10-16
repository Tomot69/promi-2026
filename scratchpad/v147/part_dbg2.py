import sys, importlib.util; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
def etat(pg, t):
    print(t, pg.evaluate("""()=>{ var s=document.getElementById('createSheet');
      return {cls:s&&s.className.slice(0,60), who:(window._phrase||{}).qui||null, sel:(typeof newWhoSel!=='undefined')?JSON.stringify(newWhoSel):'?',
       act:document.activeElement&&(document.activeElement.id||document.activeElement.className), val:(document.getElementById('gnSaisie')||{}).value, n:promises.length,
       top:(function(){var d=document.getElementById('device').getBoundingClientRect(),k=d.width/390;var e=document.querySelector('#createSheet .gn > .ph-add');if(!e)return 'pas de ph-add';var r=e.getBoundingClientRect();var x=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return x&&(x.id||x.className)})(),
       ov:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).join(',')} }"""))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    def plante(titre, gens):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(350); B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(650)
        B.tap_sel(pg,'.acc-pil[data-k=chiche]')
        for _ in range(40):
            pg.wait_for_timeout(120)
            if pg.evaluate("k=>{ var s=document.getElementById('createSheet'); return !!(s && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe')); }", 'chiche'): break
        pg.wait_for_timeout(600)
        B.tap_sel(pg,'#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1000); etat(pg,'qui')
        B.tap_sel(pg,'#createSheet .gn > .ph-add'); pg.wait_for_timeout(250); etat(pg,'add')
        for i,n in enumerate(gens):
            for _ in range(30):
                if pg.evaluate("()=>document.activeElement && document.activeElement.id==='gnSaisie'"): break
                pg.wait_for_timeout(100)
            pg.keyboard.type(n,delay=25); pg.wait_for_timeout(300); etat(pg,'tapé '+n)
            if i%2==0: B.tap_sel(pg,'#createSheet .gn > .ph-add .gn-plus')
            else: pg.keyboard.press('Enter')
            pg.wait_for_timeout(750); etat(pg,'validé '+n)
        pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(400)
        pg.evaluate("a=>{ document.getElementById('fTitle').value=a; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} window._csEnLair=true; window._csDueISO=null; }", titre); pg.wait_for_timeout(300)
        z = pg.evaluate("()=>{ const c=document.getElementById('planterZone'); const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k] }")
        y=z[1]+z[3]*0.45; B.glisse(pg, [[40+80*i/10.0, y] for i in range(11)], pas=60); pg.wait_for_timeout(3400)
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
        return pg.evaluate("()=>{ var p=promises[promises.length-1]; return {id:p.id, who:p.who}; }")
    pr=plante('courir dimanche',['Rachel','Marion','Nico']); print(pr)
    pg.evaluate("id=>openDetail(id)", pr['id']); pg.wait_for_timeout(2600)
    for n in ['Nico','Rachel']:
        pg.evaluate("a=>_parts.arrive(promises.find(p=>p.id===a[0]),a[1])", [pr['id'], n]); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} window.ouvrirIndex(); return 1; }"); pg.wait_for_timeout(2200)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pr['id']); pg.wait_for_timeout(2600)
    pg.evaluate("a=>_parts.arrive(promises.find(p=>p.id===a[0]),a[1])", [pr['id'], 'Marion'])
    pg.wait_for_timeout(3300)
    print('statut', pg.evaluate("id=>promises.find(p=>p.id===id).status", pr['id']))
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }")
    pr=plante('nager en mer',['Rachel','Marion','Nico']); print(pr)
    print(errs)
