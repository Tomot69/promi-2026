# §9 C-134 — chaque réglage du Peaufiner, chaque choix, au doigt : lequel referme Peaufiner / la fiche / ramène à la Toile ?
import sys, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ETAT = """()=>{ const sc=document.getElementById('scrim'), dp=document.getElementById('detailPoster'), cs=document.getElementById('createSheet');
  return {fiche:!!(dp&&dp.classList.contains('show')), s2:!!(dp&&dp.classList.contains('s2-ouv')), page:!!(cs&&cs.classList.contains('show')), ppP:!!(cs&&cs.classList.contains('pp-peauf')), scrim:!!(sc&&sc.classList.contains('show')),
    ecrans:[...document.querySelectorAll('.screen.show,.sheet.show,.poster.show')].map(e=>e.id).join(' ')}; }"""
RANGS = """(rac)=>[...document.querySelectorAll(rac+' .s2-reg')].filter(e=>e.getBoundingClientRect().width>0).map(e=>{ const l=e.querySelector('.s2-lab'); return l?l.textContent.trim():''; })"""
OPTS = """([rac, lab])=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=[...document.querySelectorAll(rac+' .s2-reg')].find(x=>{const l=x.querySelector('.s2-lab'); return l&&l.textContent.trim()===lab;}); if(!r) return null;
  r.scrollIntoView({block:'start'}); const q0=r.getBoundingClientRect();
  return {titre:[(q0.left+q0.width/2-D.left)/k, (q0.top+26-D.top)/k], ouv:r.classList.contains('s2-ouv'), opts:[...r.querySelectorAll('*')].filter(e=>{ const q=e.getBoundingClientRect(); return q.width>10&&q.height>10&&getComputedStyle(e).visibility!=='hidden'&&!e.closest('.s2-lab')&&!e.closest('.s2-val')&&(e.children.length===0||e.matches('.chip,.s2-ech,.pc-n,[role=button],button'))&&q.top>D.top+60&&q.bottom<D.bottom-90&&q.left>D.left&&q.right<D.right; })
    .map(e=>{ const q=e.getBoundingClientRect(); return {t:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,24), cl:(typeof e.className==='string'?e.className:'').slice(0,30), tag:e.tagName, x:(q.left+q.width/2-D.left)/k, y:(q.top+q.height/2-D.top)/k}; })}; }"""
def tous(fiche, titre=None):
    rac = '#detailPoster' if fiche else '#createSheet'
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
        def rouvre():
            if fiche: pg.evaluate("(t)=>{ closeAll(); const q=promises.filter(q=>t?q.title===t:!q.done)[0]; openDetail(q.id); }", titre)
            else: pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); var n=0; (function e(){ var x=[...document.querySelectorAll('#createSheet .tile')][0]; var cs=document.getElementById('createSheet'); if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(e,350); })(); }")
            pg.wait_for_timeout(2600); B.tap_sel(pg, '#dpDetails .dpd-tog' if fiche else '#csBotBar'); pg.wait_for_timeout(1100)
        rouvre(); rangs = pg.evaluate(RANGS, rac); print('réglages', rangs)
        for lab in rangs:
            o = pg.evaluate(OPTS, [rac, lab])
            if not o: continue
            pg.wait_for_timeout(300); o = pg.evaluate(OPTS, [rac, lab]); B.tap(pg, *o['titre']); pg.wait_for_timeout(900)
            e1 = pg.evaluate(ETAT)
            if not (e1['s2'] or e1['ppP']): print('  %-18s TITRE TOUCHÉ → %s' % (lab, e1)); rouvre(); continue
            o = pg.evaluate(OPTS, [rac, lab]); vus = 0
            for c in (o or {}).get('opts', []):
                if not c['t'] or c['tag'] in ('TEXTAREA', 'INPUT') or vus >= 3: continue
                o2 = pg.evaluate(OPTS, [rac, lab]); c2 = next((x for x in (o2 or {}).get('opts', []) if x['t'] == c['t']), None)
                if not c2: continue
                B.tap(pg, c2['x'], c2['y']); pg.wait_for_timeout(1300); e2 = pg.evaluate(ETAT); vus += 1
                ferme = not (e2['s2'] or e2['ppP'])
                print('  %-18s « %-22s » %s %s' % (lab, c['t'], 'FERME → ' if ferme else 'reste', e2 if ferme else ''))
                if ferme: rouvre(); pg.evaluate(OPTS, [rac, lab]); pg.wait_for_timeout(300); o3 = pg.evaluate(OPTS, [rac, lab]); B.tap(pg, *o3['titre']); pg.wait_for_timeout(900)
        b.close()
print('==== FICHE (à tenir, à quelqu\'un)'); tous(True, 'arroser le ficus')
print('==== PAGE +'); tous(False)
