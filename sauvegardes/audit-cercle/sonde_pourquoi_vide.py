# POURQUOI LA SPHÈRE N'A PAS PEINT — on teste les hypothèses, on ne corrige pas à l'aveugle.
#  H1 · `promises` est un `let` : `window.promises` est undefined (faute déjà faite, chantier 69) → faitIles jette → null
#  H2 · _aura.peintSur / faitIles absents (le patch n'a pas pris)
#  H3 · faitIles rend bien des îles mais peintSur refuse (trame, opts, atlas/semis)
#  H4 · la veille ne démarre pas (l'observateur ne voit pas la classe)
import json, os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/scratchpad/app-vend-sphere.html'
Q = r"""()=>{
  const o={};
  o.H1_window_promises = typeof window.promises;
  try{ o.H1_bare_promises = (typeof promises!=='undefined') ? ('tableau de ' + promises.length) : 'introuvable'; }
  catch(e){ o.H1_bare_promises = 'jette : ' + e.message; }
  o.H2_peintSur = typeof (window._aura && window._aura.peintSur);
  o.H2_faitIles = typeof (window._aura && window._aura.faitIles);
  o.H4_go = typeof window._vendSphereGo;
  o.canvas = (()=>{ const c=document.querySelector('#plCadre .plv-sph'); return c?{w:c.width,h:c.height,connecte:c.isConnected}:null; })();
  o.lignes = document.querySelectorAll('#plCadre .plv-li').length;
  /* H3 : on appelle faitIles nous-mêmes et on regarde ce qui sort */
  try{ const r = window._aura.faitIles(14, ['sillons','gravure','terrazzo']);
       o.H3_faitIles = r ? {iles: r.iles ? r.iles.length : '?', avecMatiere: r.iles ? r.iles.filter(i=>i.m).length : '?'} : 'rend null'; }
  catch(e){ o.H3_faitIles = 'jette : ' + e.message; }
  return o; }"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto(URL, timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(3500)
    print(json.dumps(pg.evaluate(Q), ensure_ascii=False, indent=1))
    br.close()
