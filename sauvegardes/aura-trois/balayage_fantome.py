# LE CLIC FANTÔME DORT-IL AILLEURS ? — balayage AU VRAI DOIGT de chaque élément touchable, écran par écran (Tom, 11 sept.).
# Pour chaque élément : l'écran rouvert à neuf, un TOUCHER (événements tactiles CDP) ; l'écran rouvert à neuf, un CLIC DE
# SOURIS au même point. On compare ce qui est ouvert 1,4 s après (les couches `.show`, et la fiche / personne courante).
# Une porte fantôme est une porte où LE DOIGT ET LA SOURIS NE FINISSENT PAS AU MÊME ENDROIT. En plus, on consigne la
# signature directe : un clic issu du toucher qui tombe sur une couche ouverte PENDANT le geste (ce que le garde avale).
# Usage : balayage_fantome.py URL [étiquette]   — sans garde : il doit retrouver les Noyaux ; finale : zéro écart.
import sys, json
from playwright.sync_api import sync_playwright
APP = sys.argv[1]; ET = sys.argv[2] if len(sys.argv) > 2 else ''
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
BASE = "()=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"
AURA = [(BASE, 200), ("()=>document.getElementById('souffleBtn').click()", 3000)]
ECRANS = [
  ('accueil',               [(BASE, 400)]),
  ('Index',                 [(BASE, 200), ("()=>{ if(window.ouvrirIndex) ouvrirIndex(); else document.getElementById('indexSheet').classList.add('show'); }", 1800)]),
  ('Fil',                   [(BASE, 200), ("()=>setView('fil')", 1800)]),
  ('Aura',                  AURA),
  ('fiche Promi 126',       [(BASE, 200), ("()=>openDetail(126)", 1500)]),
  ('fiche Chiche 127',      [(BASE, 200), ("()=>openDetail(127)", 1500)]),
  ('Peaufiner Promi 126',   [(BASE, 200), ("()=>openDetail(126)", 1200), (PEAUF, 1400)]),
  ('fiche Nuée potager',    [(BASE, 200), ("()=>openEssaim('potager')", 1600)]),
  ('Peaufiner Nuée',        [(BASE, 200), ("()=>openEssaim('potager')", 1400), (PEAUF, 1400)]),
  ('fiche de Rachel',       [(BASE, 200), ("()=>openPerson('Rachel')", 1600)]),
  ('Studio',                [(BASE, 200), ("()=>document.getElementById('studioBtn').click()", 1800)]),
  ('Réglages',              [(BASE, 200), ("()=>document.getElementById('settingsBtn').click()", 1600)]),
]
CAND = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), out=[], vus=new Set();
  const ok=(e)=>{ const r=e.getBoundingClientRect(); if(r.width<8||r.height<8) return null; const x=r.left+r.width/2, y=r.top+r.height/2;
    if(x<dv.left+2||x>dv.right-2||y<dv.top+2||y>dv.bottom-2) return null; const h=document.elementFromPoint(x,y); return (h&&(h===e||e.contains(h)))?[x,y]:null; };
  document.querySelectorAll('body *').forEach(e=>{ const c=getComputedStyle(e);
    const tap = e.onclick || e.tagName==='BUTTON' || e.getAttribute('role')==='button' || (c.cursor==='pointer' && getComputedStyle(e.parentElement||e).cursor!=='pointer');
    if(!tap) return; const pt=ok(e); if(!pt) return;
    const k=Math.round(pt[0]/6)+','+Math.round(pt[1]/6); if(vus.has(k)) return; vus.add(k);
    const cls=String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||'').split(' ')[0];
    out.push({pt, nom:(e.id?'#'+e.id:e.tagName.toLowerCase()+(cls?'.'+cls:''))+' « '+(e.textContent||'').trim().slice(0,22)+' »'}); });
  return out.slice(0,26); }"""
POSE = r"""()=>{ window.__fant=[]; const p={o:null};
  window.addEventListener('pointerdown', e=>{ p.o=[...document.querySelectorAll('.show')]; }, true);
  window.addEventListener('click', e=>{ if(!e.isTrusted||!p.o) return; const c=e.target&&e.target.closest?e.target.closest('.show'):null;
    if(c && p.o.indexOf(c)<0) __fant.push(c.id||c.className); }, true); }"""
FIN = r"""()=>({couches:[...document.querySelectorAll('.show')].map(e=>e.id).filter(i=>i&&i!=='scrim').sort().join(','),
  personne:document.getElementById('personSheet').classList.contains('show')?(document.getElementById('psCadre')||{getAttribute:()=>'?'}).getAttribute('data-fiche'):null,
  promi:(document.getElementById('detailPoster').classList.contains('show')&&typeof cur!=='undefined'&&cur)?cur.id:null, fant:window.__fant||[]})"""
ecarts, fantomes, total = [], [], 0
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate(POSE)
    def ouvre(steps):
        for js, w in steps:
            try: pg.evaluate(js)
            except Exception: pass
            pg.wait_for_timeout(w)
        pg.evaluate("()=>{ window.__fant=[]; }")
    for nom, steps in ECRANS:
        ouvre(steps); C = pg.evaluate(CAND)
        print('\n== %s — %d éléments touchables' % (nom, len(C)))
        for c in C:
            x, y = c['pt']
            ouvre(steps)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(50)
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1400)
            d = pg.evaluate(FIN)
            ouvre(steps); pg.mouse.click(x, y); pg.wait_for_timeout(1400); s = pg.evaluate(FIN)
            total += 1
            same = (d['couches'], d['personne'], d['promi']) == (s['couches'], s['personne'], s['promi'])
            if d['fant']: fantomes.append((nom, c['nom'], d['fant']))
            if not same:
                ecarts.append((nom, c['nom'], d, s))
                print('   ÉCART  %s\n          doigt  : %s · personne %s · Promi %s\n          souris : %s · personne %s · Promi %s' % (c['nom'], d['couches'], d['personne'], d['promi'], s['couches'], s['personne'], s['promi']))
            if d['fant']: print('   (clic issu du toucher tombé sur une couche ouverte pendant le geste : %s — %s)' % (d['fant'], c['nom']))
    b.close()
print('\n═══ %s — %d éléments touchés au doigt ET à la souris · %d écart(s) doigt ≠ souris · %d clic(s) fantôme(s) consigné(s)' % (ET, total, len(ecarts), len(fantomes)))
for e in ecarts: print('   ÉCART  [%s] %s' % (e[0], e[1]))
for f in fantomes: print('   FANTÔME [%s] %s → %s' % f)
