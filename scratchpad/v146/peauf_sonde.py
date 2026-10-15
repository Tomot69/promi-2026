# §9 C-134 — quels choix du Peaufiner le referment (et ramènent à la Toile) : fiche Promi, puis page +
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ETAT = """()=>{ const sc=document.getElementById('scrim'); const dp=document.getElementById('detailPoster'), cs=document.getElementById('createSheet');
  return {fiche:!!(dp&&dp.classList.contains('show')), s2:!!(dp&&dp.classList.contains('s2-ouv')), dd:!!(document.getElementById('dpDetails')&&document.getElementById('dpDetails').classList.contains('ouvert')),
    page:!!(cs&&cs.classList.contains('show')), scrim:!!(sc&&sc.classList.contains('show')), csP:cs?[...cs.classList].filter(c=>/ouv|peauf|reg/.test(c)).join(' '):'' , ecran:[...document.querySelectorAll('.screen.show,.sheet.show,.poster.show')].map(e=>e.id).join(' ')}; }"""
LISTE = """(racine)=>{ const R=document.querySelector(racine); if(!R) return []; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  return [...R.querySelectorAll('.s2-reg, .s2-reg *, [role=button], button, .chip, .ph-o, .pz-t, [data-pinceau], .s2-c, .s2-opt, label, input')].filter(e=>{ const r=e.getBoundingClientRect(); const c=getComputedStyle(e); return r.width>8&&r.height>8&&c.visibility!=='hidden'&&r.top>D.top&&r.bottom<D.bottom; })
    .map(e=>{ const r=e.getBoundingClientRect(); return {t:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,30), cl:(e.className&&e.className.baseVal===undefined?e.className:'').slice(0,40), tag:e.tagName, x:(r.left+r.width/2-D.left)/k, y:(r.top+r.height/2-D.top)/k}; }); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
    print('promis', pg.evaluate("()=>promises.map(q=>q.title+'|'+q.who+'|'+(q.done?'t':'')).slice(0,10)"))
    pg.evaluate("()=>{ const q=promises.filter(q=>!q.done)[0]; openDetail(q.id); }"); pg.wait_for_timeout(2200)
    print('fiche', pg.evaluate(ETAT)); B.tap_sel(pg, '#dpDetails .dpd-tog'); pg.wait_for_timeout(1200); print('peaufiner', pg.evaluate(ETAT))
    L = pg.evaluate(LISTE, '#detailPoster'); print(len(L)); 
    for e in L: print('   ', json.dumps(e, ensure_ascii=False))
    b.close()

OPTS = """(lab)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=[...document.querySelectorAll('#detailPoster .s2-reg, #createSheet .s2-reg')].find(x=>{const l=x.querySelector('.s2-lab'); return l&&l.textContent.trim()===lab;}); if(!r) return null;
  return {ouv:r.classList.contains('s2-ouv'), opts:[...r.querySelectorAll('*')].filter(e=>{ const q=e.getBoundingClientRect(); return q.width>10&&q.height>10&&getComputedStyle(e).visibility!=='hidden'&&!e.closest('.s2-lab')&&e.children.length===0; }).map(e=>{ const q=e.getBoundingClientRect(); return {t:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,24), cl:(typeof e.className==='string'?e.className:'').slice(0,30), x:(q.left+q.width/2-D.left)/k, y:(q.top+q.height/2-D.top)/k}; }).slice(0,14)}; }"""
def essai(fiche=True):
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
        def rouvre():
            if fiche: pg.evaluate("()=>{ closeAll(); const q=promises.filter(q=>!q.done)[0]; openDetail(q.id); }")
            else: pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); var n=0; (function e(){ var x=[...document.querySelectorAll('#createSheet .tile')][0]; var cs=document.getElementById('createSheet'); if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(e,350); })(); }")
            pg.wait_for_timeout(2600); B.tap_sel(pg, '#dpDetails .dpd-tog' if fiche else '#csBotBar'); pg.wait_for_timeout(1200)
        rouvre(); print('ouvert', pg.evaluate(ETAT)); print('   réglages :', pg.evaluate("()=>[...document.querySelectorAll('#detailPoster .s2-reg .s2-lab, #createSheet .s2-reg .s2-lab')].filter(e=>e.getBoundingClientRect().width>0).map(e=>e.textContent.trim())"))
        for lab in ('LE TRAIT', 'AVANT', 'À QUI', 'DANS UN CERCLE', 'RÉCURRENCE', 'UN RAPPEL'):
            o = pg.evaluate(OPTS, lab)
            if not o: print(lab, 'absent'); continue
            r = pg.evaluate("(lab)=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=[...document.querySelectorAll('#detailPoster .s2-reg, #createSheet .s2-reg')].find(x=>{const l=x.querySelector('.s2-lab'); return l&&l.textContent.trim()===lab;}); const q=r.getBoundingClientRect(); return [(q.left+q.width/2-D.left)/k,(q.top+30-D.top)/k]; }", lab)
            B.tap(pg, r[0], r[1]); pg.wait_for_timeout(900); o = pg.evaluate(OPTS, lab); print(lab, 'après toucher du titre :', pg.evaluate(ETAT), 'ouv', o and o['ouv'])
            for e in (o or {}).get('opts', [])[:14]: print('      ', e)
            cand = [e for e in (o or {}).get('opts', []) if e['y'] > r[1] + 20 and e['t'] and ' on' not in ' ' + e['cl'] and e['cl'] != 's2-val' and e['x'] < 380]
            if cand:
                c = cand[0]; B.tap(pg, c['x'], c['y']); pg.wait_for_timeout(1200); print('   choix «', c['t'], '» →', pg.evaluate(ETAT))
            if not pg.evaluate(ETAT)['s2']: rouvre()
        b.close()
essai(True)
print('==== PAGE +'); essai(False)
