# SONDE À L'EXÉCUTION — avant de monter une seconde sphère sur l'écran qui vend.
# On VÉRIFIE (on ne suppose pas) : la boîte de #plHeroCv et de son PARENT (le canevas qui rend du vide en silence),
# ce que OrbiteMoteur et _aura exposent vraiment, K/G/PALIERS, et que la Toile est vivante sur cet écran.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
Q = r"""()=>{
  const o={};
  o.OrbiteMoteur = (typeof window.OrbiteMoteur==='object' && window.OrbiteMoteur) ? Object.keys(window.OrbiteMoteur) : String(typeof window.OrbiteMoteur);
  o._aura = (typeof window._aura==='object' && window._aura) ? Object.keys(window._aura) : String(typeof window._aura);
  o.a_opts = !!(window._aura && window._aura.opts);
  try{ o.K = window._aura.K; }catch(e){ o.K='?'; }
  try{ o.G = window._aura.G; }catch(e){ o.G='?'; }
  try{ o.PALIERS = window._aura.PALIERS; }catch(e){ o.PALIERS='?'; }
  try{ o.toileCount = window.Toile.count(); }catch(e){ o.toileCount='?'; }
  try{ o.monde = window.Toile.mondeCourant(); }catch(e){ o.monde='?'; }
  const s=document.getElementById('plusScreen'), h=document.getElementById('plHeroCv');
  o.plusScreen = s ? {show:s.classList.contains('show'), clientW:s.clientWidth, clientH:s.clientHeight, scrollH:s.scrollHeight,
                      overflowY:getComputedStyle(s).overflowY} : null;
  if(h){ const cs=getComputedStyle(h);
    o.hero_avant = {display:cs.display, w:h.width, h:h.height, parent:h.parentElement.id||h.parentElement.className};
    h.style.setProperty('display','block','important');
    const r=h.getBoundingClientRect(), p=h.parentElement;
    o.hero_apres = {rect:[+r.width.toFixed(1), +r.height.toFixed(1)], parentClient:[p.clientWidth, p.clientHeight]};
    h.style.removeProperty('display');
  } else o.hero_avant='absent';
  return o; }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
    pg.goto('http://127.0.0.1:8752/app.html', timeout=90000); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(2400)
    R = pg.evaluate(Q)
    json.dump(R, open(os.path.join(D, 'sonde_sphere.json'), 'w'), ensure_ascii=False, indent=1)
    print('OrbiteMoteur expose :', R['OrbiteMoteur'])
    print('_aura expose        :', R['_aura'])
    print('_aura.opts existe ? :', R['a_opts'])
    print('K                   :', json.dumps(R['K'], ensure_ascii=False))
    print('G.AUTO              :', R['G'].get('AUTO') if isinstance(R['G'], dict) else R['G'])
    # et une fois l'Aura ouverte : la sphère est-elle vivante ?
    pg.evaluate("()=>{ try{closeAll();}catch(e){} const a=document.getElementById('auraScreen'); if(a) a.classList.add('show'); }")
    pg.wait_for_timeout(3000)
    e = pg.evaluate("()=>{ try{ const s=window._aura.etat(); return {pret:s.pret, palier:s.palier, vise:s.vise, ms:s.ms, lac:s.lac, tan:s.tan, tour:s.tour}; }catch(err){ return String(err); } }")
    print('\n_aura.etat() une fois l’Aura ouverte :', json.dumps(e, ensure_ascii=False))
    br.close()
