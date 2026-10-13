import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
ET = """()=>{ var dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390; function r(id){ var e=document.getElementById(id); if(!e) return null; var q=e.getBoundingClientRect(), cs=getComputedStyle(e); return [Math.round((q.left-dv.left)/k),Math.round((q.top-dv.top)/k),Math.round(q.width/k),Math.round(q.height/k),cs.display,cs.visibility,(e.textContent||'').trim().slice(0,70)]; }
  var a=document.activeElement; return {ligne:r('cm5Ligne'), dernier:r('cm5Dernier'), fil:r('cm5Fil'), corps:r('dpCorps'), actif:a&&(a.className||a.id||a.tagName), etat:window._comm&&_comm.etat(), comm:(cur&&cur.comments||[]).map(c=>c.by+': '+c.t)}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for sombre in (False, True):
        ctx = B.contexte(b, sombre=sombre); pg = B.ouvre(ctx); s = '-sombre' if sombre else ''
        B.plante_doigt(pg, 'venir au concert', 'moi', 0)
        pid = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.from='Marion'; p.who='moi'; p.status='rate'; return p.id; }")
        pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600); print('1 reçue, à tenir, sans commentaire', pg.evaluate(ET)); B.capture(pg, 'scratchpad/v145/cm-1%s.png' % s)
        pg.evaluate("id=>_comm.arrive(promises.find(p=>p.id===id),{t:'Promis, j\\u2019y serai. Tu gardes une place ?',by:'Marion',d:'2026-10-11T18:00:00.000Z'})", pid); pg.wait_for_timeout(700)
        print('2 un commentaire reçu', pg.evaluate(ET)); B.capture(pg, 'scratchpad/v145/cm-2%s.png' % s)
        r = B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(900); print('3 ligne touchée', pg.evaluate(ET)); B.capture(pg, 'scratchpad/v145/cm-3%s.png' % s)
        pg.keyboard.type('Oui, au premier rang'); pg.keyboard.press('Enter'); pg.wait_for_timeout(700); print('4 envoyé', pg.evaluate(ET)); B.capture(pg, 'scratchpad/v145/cm-4%s.png' % s)
        B.tap(pg, 195, 180); pg.wait_for_timeout(900); print('5 refermé', pg.evaluate(ET)); B.capture(pg, 'scratchpad/v145/cm-5%s.png' % s)
        print('erreurs', pg.erreurs[:3]); ctx.close()
    b.close()
