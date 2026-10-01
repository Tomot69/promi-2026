# PORTE 8 de releve-fiche-personne : le disque de Rachel sur SA fiche ouvre-t-il la fiche de Rachel ? 5 essais par thème, diagnostic.
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        res = []
        for k in range(5):
            pg = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2).new_page()
            pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            fid = pg.evaluate("()=>{ closeAll(); const p=promises.find(q=>q.title==='faire les crêpes' && q.who==='Rachel'); openDetail(p.id); return p.id; }"); pg.wait_for_timeout(1200)
            kr = pg.evaluate("""()=>{ const k=[...document.querySelectorAll('.kring[data-p]')].find(e=>e.getAttribute('data-p')==='Rachel'&&e.getBoundingClientRect().width>0); if(!k) return null;
                const r=k.getBoundingClientRect(), x=r.left+r.width/2, y=r.top+r.height/2, h=document.elementFromPoint(x,y);
                return {x, y, sous:(h&&(h===k||k.contains(h)))?'le disque':((h&&(h.id||String(h.className).split(' ')[0]))||'rien')}; }""")
            if kr: pg.mouse.click(kr['x'], kr['y'])
            pg.wait_for_timeout(1600); a = pg.evaluate("()=>{const c=document.getElementById('psCadre'); return [document.getElementById('personSheet').classList.contains('show'), c&&c.getAttribute('data-fiche')];}")
            pg.wait_for_timeout(1400); b = pg.evaluate("()=>{const c=document.getElementById('psCadre'); return [document.getElementById('personSheet').classList.contains('show'), c&&c.getAttribute('data-fiche')];}")
            res.append((fid, kr and kr['sous'], a, b))
            pg.context.close()
        print(th); [print('   ', r) for r in res]
    br.close()
