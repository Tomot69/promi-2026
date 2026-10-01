from playwright.sync_api import sync_playwright
import sys
LISTE="""()=>{const o=[];document.querySelectorAll('input,textarea,[contenteditable=true]').forEach(e=>{const q=e.getBoundingClientRect();const s=getComputedStyle(e);
  if(q.width<20||q.height<10||s.display==='none'||s.visibility==='hidden')return; if(q.bottom<0||q.top>932)return;
  o.push({sel:e.id?'#'+e.id:null, tag:e.tagName, ph:(e.placeholder||'').slice(0,30), x:q.x+q.width/2, y:q.y+q.height/2});});return o;}"""
def essai(pg, e, nom):
    pg.evaluate("s=>{const e=document.querySelector(s); if(e) e.scrollIntoView({block:'center'});}", e['sel']); pg.wait_for_timeout(300)
    r=pg.evaluate("s=>{const e=document.querySelector(s); const q=e.getBoundingClientRect(); const h=document.elementFromPoint(q.x+q.width/2,q.y+q.height/2); return [q.x+q.width/2,q.y+q.height/2, h?(h.id||String(h.className).slice(0,30)||h.tagName):'-', h===e||e.contains(h), getComputedStyle(e).pointerEvents, getComputedStyle(e).webkitUserSelect||getComputedStyle(e).userSelect]}", e['sel'])
    pg.evaluate("()=>{if(document.activeElement)document.activeElement.blur();}")
    pg.touchscreen.tap(r[0],r[1]); pg.wait_for_timeout(600)
    act=pg.evaluate("()=>{const a=document.activeElement;return a?(a.id||a.tagName):null}")
    pg.keyboard.type('abc'); pg.wait_for_timeout(300)
    v=pg.evaluate("s=>{const e=document.querySelector(s);return e.value!=null?e.value:e.textContent}", e['sel'])
    print('  %-24s %-28s dessus=%s(lui:%s) pe=%s sel=%s · focus=%s · valeur=%r' % (nom, e['sel'], r[2], r[3], r[4], r[5], act, (v or '')[-10:]))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
    for nom,js in (('fiche Cercle',"()=>{closeAll();openEssaim('potager')}"),
                   ('Peaufiner Cercle',"()=>{closeAll();openEssaim('potager');setTimeout(()=>{const t=document.querySelector('#dpDetails .dpd-tog')||document.getElementById('dpdTog');t&&t.click()},1200)}"),
                   ('page + Cercle',"()=>{closeAll();document.getElementById('createBtn').click();setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()},400)}"),
                   ('Peaufiner Promi (témoin)',"()=>{closeAll();openDetail(promises.find(p=>p.title==='nager le mardi').id);setTimeout(()=>{const t=document.querySelector('#dpDetails .dpd-tog');t&&t.click()},1200)}")):
        pg.evaluate(js); pg.wait_for_timeout(3200)
        L=[e for e in pg.evaluate(LISTE) if e['sel']]
        print('==',nom,[e['sel'] for e in L])
        for e in L[:6]:
            pg.evaluate(js); pg.wait_for_timeout(3000); essai(pg,e,nom)
