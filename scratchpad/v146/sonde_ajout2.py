import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
R = """()=>{ const d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; const out={};
  const g=[...document.querySelectorAll('#createSheet .gn, #dpdCorps .gn')].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
  const r=e=>{ if(!e) return null; const q=e.getBoundingClientRect(); return [Math.round((q.left-d.left)/k*10)/10,Math.round((q.top-d.top)/k*10)/10,Math.round(q.width/k*10)/10,Math.round(q.height/k*10)/10]; };
  const z=g.querySelector(':scope > .ph-add');
  out.zone=r(z); out.cls=z&&z.className; out.bord=z&&getComputedStyle(z).borderTopStyle; out.txt=z&&z.textContent; out.plus=r(z&&z.querySelector('.gn-plus')); out.plusVu=z&&z.querySelector('.gn-plus')&&z.querySelector('.gn-plus').style.display;
  out.ligne=r(z&&z.querySelector('.gn-ligne')); out.barre=!!g.querySelector('.gn-barre');
  out.actif=document.activeElement&&(document.activeElement.id||document.activeElement.className||document.activeElement.tagName);
  out.pris=g._gens&&g._gens.choisis(); out.sa=window._gensSaisie&&window._gensSaisie.etat(); return out; }"""
KB = """h=>{ const vv=window.visualViewport; Object.defineProperty(vv,'height',{get(){return h},configurable:true}); vv.dispatchEvent(new Event('resize')); }"""
nom = sys.argv[1] if len(sys.argv) > 1 else 'apres'
sombre = '--sombre' in sys.argv
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre=sombre); pg = B.ouvre(ctx)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2200)
    B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(1100)
    B.tap_sel(pg, '#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1200)
    print('page + repos   :', json.dumps(pg.evaluate(R), ensure_ascii=False))
    B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(500)
    pg.evaluate(KB, 844 - 336); pg.wait_for_timeout(500)
    print('  touché        :', json.dumps(pg.evaluate(R), ensure_ascii=False))
    B.capture(pg, 'planche-v146/ajout-%s-1-touche.png' % nom)
    pg.keyboard.type('Rachel', delay=60); pg.wait_for_timeout(500)
    print('  saisi         :', json.dumps(pg.evaluate(R), ensure_ascii=False))
    B.capture(pg, 'planche-v146/ajout-%s-2-saisie.png' % nom)
    B.tap_sel(pg, '#createSheet .gn > .ph-add .gn-plus'); pg.wait_for_timeout(900)
    print('  validé au +   :', json.dumps(pg.evaluate(R), ensure_ascii=False), pg.evaluate("()=>window._phrase&&window._phrase.qui"))
    B.capture(pg, 'planche-v146/ajout-%s-3-valide.png' % nom)
    pg.keyboard.type('Marion', delay=60); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
    print('  validé Retour :', json.dumps(pg.evaluate(R), ensure_ascii=False), pg.evaluate("()=>window._phrase&&window._phrase.qui"))
    B.capture(pg, 'planche-v146/ajout-%s-4-deux.png' % nom)
    print('erreurs', pg.__dict__['erreurs'][:3]); b.close()
