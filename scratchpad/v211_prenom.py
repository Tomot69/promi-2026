"""v211 C-309 — sonde : la suite des prénoms et la transition image par image."""
import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
REC = r"""()=>{ window.__pr=[]; let on=true; window.__prStop=()=>{on=false;}; const f=()=>{ if(!on) return; const e=document.querySelector('#csPhrase .ph-m[data-ph="qui"]');
  if(e){ const c=getComputedStyle(e); const w=e.querySelector('.v200-mt')||e; const cw=getComputedStyle(w); window.__pr.push([Math.round(performance.now()), e.textContent, cw.clipPath.slice(0,40), cw.visibility, +cw.opacity, (window.TraceLettres&&TraceLettres.actif&&TraceLettres.actif())?1:0, e.getBoundingClientRect().width|0]); }
  else window.__pr.push([Math.round(performance.now()), null]);
  requestAnimationFrame(f); }; requestAnimationFrame(f); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, vw=430, vh=932); pg = B.ouvre(ctx, 'app.html')
    def ouvre():
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{ document.getElementById('createBtn').click(); setTimeout(()=>document.querySelector('#accChoix .acc-pil[data-k=promi]').click(),600); }"); pg.wait_for_timeout(3800)
    def sens(): return pg.evaluate("()=>window._phrase&&window._phrase.sens")
    def qui(): return pg.evaluate("()=>{ const e=document.querySelector('#csPhrase .ph-m[data-ph=\"qui\"]'); return e&&e.textContent; }")
    def bascule(log=False):
        if log: pg.evaluate(REC)
        B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(2600)
        if log: pg.evaluate("()=>__prStop()"); return pg.evaluate("()=>__pr")
    suite = []; ouvre()
    for tour in range(4):
        for _ in range(4):
            fr = bascule(log=True); s = sens()
            if s == 'demander':
                suite.append(qui()); json.dump(fr, open('scratchpad/v211_prenom_fr%d.json' % len(suite), 'w'))
                break
        bascule()   # en sortir
        if tour == 1: ouvre()
    print('suite', suite)
    b.close()
