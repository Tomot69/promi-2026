import sys, json, io, re; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
PROF = open('scratchpad/v143/profil.py', encoding='utf-8').read().split('PROF = r"""')[1].split('"""')[0]
def ferme(pg):
    r = pg.evaluate("()=>{ const e=[...document.querySelectorAll('#auraScreen [data-close], #auraScreen .closeb')].find(x=>x.getBoundingClientRect().width>4); if(!e) return null; const q=e.getBoundingClientRect(); return [q.left+q.width/2,q.top+q.height/2]; }")
    if r: pg.touchscreen.tap(r[0], r[1])
    pg.wait_for_timeout(900)
def attend(pg):
    for _ in range(40):
        if pg.evaluate("()=>_aura.pre().pret"): return
        pg.wait_for_timeout(300)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); ctx.add_init_script(PROF); B.toile_pleine(ctx, 25); pg = B.ouvre(ctx)
    attend(pg); print('avant 1re ouverture', pg.evaluate("()=>_aura.pre()"))
    pg.evaluate("()=>{ window.__t0=0; document.getElementById('souffleBtn').addEventListener('touchstart',()=>{ window.__t0=performance.now(); },true); window.__Pon(true); }")
    B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(2500)
    r = pg.evaluate("()=>({t0:window.__t0, P:window.__P.slice(), pre:_aura.pre()})")
    print('1re ouverture — latence', r['pre']['latence'], 'dansGeste', r['pre']['dansGeste'])
    for e in sorted([e for e in r['P'] if -5 <= e[0] - r['t0'] <= 600], key=lambda e: e[0]): print('   %5d ms  %6.1f ms  %s' % (e[0] - r['t0'], e[1], re.sub(r'\s+', ' ', e[2])[:130]))
    ferme(pg); attend(pg)
    print('avant la tenue', pg.evaluate("()=>_aura.pre()"))
    pg.evaluate("()=>{ const p=promises.find(p=>p.status!=='tenu'); p.status='tenu'; p.keptAt=Date.now(); try{ syncAll(); }catch(e){} }")
    for t in (100, 500, 900, 1300, 1600): pg.wait_for_timeout(400 if t > 100 else 100); print('  +%d ms' % t, pg.evaluate("()=>{ const e=_aura.pre(); return {pret:e.pret, enCours:e.enCours, sol:e.sol, chaud:e.chaud, calme:e.calme, ms:e.ms}; }"))
    pg.evaluate("()=>window.__Pon(true)"); B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(2500)
    r = pg.evaluate("()=>({t0:window.__t0, P:window.__P.slice(), pre:_aura.pre()})"); print('après tenue — latence', r['pre']['latence'], 'dansGeste', r['pre']['dansGeste'], 'chaude', r['pre']['chaude'])
    for e in sorted([e for e in r['P'] if -5 <= e[0] - r['t0'] <= 600], key=lambda e: e[0]): print('   %5d ms  %6.1f ms  %s' % (e[0] - r['t0'], e[1], re.sub(r'\s+', ' ', e[2])[:130]))
    b.close()
