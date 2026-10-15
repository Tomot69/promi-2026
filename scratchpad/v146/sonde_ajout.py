import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
R = """()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; const out={};
  const g=[...document.querySelectorAll('#createSheet .gn, #dpdCorps .gn')].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
  const r=e=>{ if(!e) return null; const q=e.getBoundingClientRect(); return [Math.round((q.left-d.left)/k),Math.round((q.top-d.top)/k),Math.round(q.width/k),Math.round(q.height/k)]; };
  out.gn=r(g); out.liste=r(g.querySelector('.gn-liste')); out.add=r(g.querySelector('.ph-add')); out.barre=r(g.querySelector('.gn-barre')); out.inp=r(g.querySelector('.gn-in'));
  out.hote=(g.closest('#createSheet')?'page +':'fiche'); out.actif=document.activeElement&&(document.activeElement.className||document.activeElement.tagName);
  let p=g, sc=[]; while(p&&p!==document.body){ const cs=getComputedStyle(p); if(/auto|scroll/.test(cs.overflowY)&&p.scrollHeight>p.clientHeight+2) sc.push((p.id||p.className)+':'+p.scrollTop+'/'+(p.scrollHeight-p.clientHeight)); p=p.parentElement; } out.defile=sc; return out; }"""
nom = sys.argv[1] if len(sys.argv) > 1 else 'avant'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    # page + · Promi · à qui
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2200)
    B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(1100)
    B.tap_sel(pg, '#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1200)
    print('page + · à qui :', json.dumps(pg.evaluate(R)))
    B.capture(pg, 'planche-v146/ajout-%s-1-page-plus.png' % nom)
    B.tap_sel(pg, '#createSheet .gn .ph-add'); pg.wait_for_timeout(900)
    print('  après toucher  :', json.dumps(pg.evaluate(R)))
    pg.keyboard.type('Rachel', delay=40); pg.wait_for_timeout(400)
    B.capture(pg, 'planche-v146/ajout-%s-2-page-plus-saisie.png' % nom)
    print('  après saisie   :', json.dumps(pg.evaluate(R)), pg.evaluate("()=>window._phrase&&window._phrase.qui"))
    # fiche · Peaufiner · À QUI
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600)
    pid = pg.evaluate("()=>{ const p=promises.find(p=>p.who&&p.who!=='moi'&&p.status!=='tenu'&&!p.nuee); return p?p.id:null; }")
    if pid is None:
        B.plante(pg, 'venir au concert', 'Rachel') if hasattr(B,'plante') else None
        pid = pg.evaluate("()=>promises[promises.length-1].id")
    print('  parole', pg.evaluate("i=>{const p=promises.find(p=>p.id===i); return p&&[p.title,p.who,p.kind,p.sens];}", pid))
    pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2500)
    B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1300)
    print('  réglages :', pg.evaluate("()=>[...document.querySelectorAll('#dpdCorps .s2-reg')].map(r=>((r.querySelector('.s2-lab')||{}).textContent||'').trim())"))
    pg.evaluate("""()=>{const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>/QUI/i.test(((r.querySelector('.s2-lab')||{}).textContent||''))); if(r) r.scrollIntoView({block:'center'});}"""); pg.wait_for_timeout(400)
    c = pg.evaluate("""()=>{const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>/QUI/i.test(((r.querySelector('.s2-lab')||{}).textContent||''))); if(!r) return null; const q=r.getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2];}""")
    if c: pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(1200)
    print('fiche · À QUI  :', json.dumps(pg.evaluate(R)))
    B.capture(pg, 'planche-v146/ajout-%s-3-fiche.png' % nom)
    r = B.tap_sel(pg, '#dpdCorps .gn .ph-add'); pg.wait_for_timeout(900)
    print('  après toucher  :', json.dumps(pg.evaluate(R)))
    B.capture(pg, 'planche-v146/ajout-%s-4-fiche-saisie.png' % nom)
    print('erreurs', pg.__dict__['erreurs'][:3]); b.close()
