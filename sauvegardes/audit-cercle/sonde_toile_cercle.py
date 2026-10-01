# SONDE — la vraie Toile est-elle exploitable depuis l'écran qui vend ?
#  · Toile.dalleAbs(pid) répond-elle hors de l'écran Toile (liaison germes↔Promi) ?
#  · quelles cotes fait la Toile vivante (pour caler le cadre 346×276) ?
#  · combien de dalles réelles, et leur emprise
import json
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
Q = r"""()=>{
  const o={};
  try{ o.count = window.Toile.count(); }catch(e){ o.count='?'; }
  try{ o.vue = window.Toile.vue(); }catch(e){ o.vue='?'; }
  try{ o.monde = window.Toile.mondeCourant(); }catch(e){ o.monde='?'; }
  const ids = (typeof promises!=='undefined' ? promises : []).filter(p=>!p.draft && !p.req).map(p=>p.id);
  o.promi = ids.length;
  /* la liaison germes↔Promi : elle doit exister, sinon dalleAbs rend null */
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){ o.syncErr=String(e); }
  const abs = [];
  for(const id of ids){ let d=null; try{ d=window.Toile.dalleAbs(id); }catch(e){}
    if(d) abs.push({id, x:+d.minx.toFixed(1), y:+d.miny.toFixed(1), w:+d.w.toFixed(1), h:+d.h.toFixed(1), pts:d.poly.length}); }
  o.dallesAvecCellule = abs.length;
  o.exemples = abs.slice(0,4);
  if(abs.length){
    o.emprise = {x0:Math.min(...abs.map(a=>a.x)), y0:Math.min(...abs.map(a=>a.y)),
                 x1:Math.max(...abs.map(a=>a.x+a.w)), y1:Math.max(...abs.map(a=>a.y+a.h))};
    o.emprise.w = +(o.emprise.x1-o.emprise.x0).toFixed(1); o.emprise.h = +(o.emprise.y1-o.emprise.y0).toFixed(1);
    o.emprise.ratio = +(o.emprise.w/o.emprise.h).toFixed(3);
  }
  /* une dalle peinte dans un monde Cercle sort-elle ? */
  try{ const c=document.createElement('canvas');
       const base = window.Toile.mondeCourant()||{};
       const ok = window.Toile.dalleTrame(c, abs.length?abs[0].id:ids[0], 1, {m:'sillons', p:base.p, h:base.h});
       o.dalleSillons = {ok:!!ok, w:c.width, h:c.height}; }catch(e){ o.dalleSillons='jette : '+e.message; }
  const cb = document.querySelector('#plusScreen .closeb');
  if(cb){ const r=cb.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
    o.fermer = {x:+((r.left-dv.left)/s).toFixed(1), y:+((r.top-dv.top)/s).toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1), txt:cb.textContent.trim()}; }
  return o; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto(URL, timeout=90000); pg.wait_for_timeout=getattr(pg,'wait_for_timeout'); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(2500)
    print(json.dumps(pg.evaluate(Q), ensure_ascii=False, indent=1))
    br.close()
