import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    B.plante_doigt(pg, 'venir au concert', 'moi', 0)
    pid = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.from='Marion'; p.who='moi'; return p.id; }")
    pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600)
    pg.evaluate("""()=>{ window.__j=[]; ['pointerdown','pointerup','touchstart','touchend','click','focusin','focusout'].forEach(function(n){ document.addEventListener(n,function(e){ window.__j.push(n+'@'+((e.target&&(e.target.id||e.target.className))||'?')+' ouvert='+_comm.etat().ouvert); },true); });
      var o=_comm.ouvre, f=_comm.ferme; }""")
    r = B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(900)
    print(r, pg.evaluate("()=>window.__j"), pg.evaluate("()=>_comm.etat()"))
    print('au point :', pg.evaluate("p=>{ var e=document.elementFromPoint(p[0],p[1]); return e&&(e.id||e.className||e.tagName); }", r))
    b.close()
