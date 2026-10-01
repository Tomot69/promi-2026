# TOUS LES CHEMINS VERS UNE PERSONNE — au doigt. Sur chaque écran qui montre quelqu'un, chaque NOM et chaque VISAGE
# visibles (touchés au doigt) sont touchés, un par un, sur un écran rouvert à neuf ; on note où ça mène :
# la fiche de CETTE personne (openPerson), autre chose, ou rien.
import json, sys
from playwright.sync_api import sync_playwright
NOMS = ['Rachel','Marion','Adrien','Nico','Léa','Maman','Mimi']
ECRANS = {
 'Aura':                 "()=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('souffleBtn').click(); }",
 'Index':                "()=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); if(window.ouvrirIndex)ouvrirIndex(); else document.getElementById('indexSheet').classList.add('show'); }",
 'Fil':                  "()=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); const s=document.getElementById('feedView'); s.classList.add('show'); if(window._s4Fil) _s4Fil(); }",
 'fiche Promi à Rachel': "()=>{ closeAll(); openDetail(126); }",
 'fiche Chiche à Marion, avec Rachel': "()=>{ closeAll(); openDetail(127); }",
 'fiche Chiche de Marion, avec Adrien (Nuée)': "()=>{ closeAll(); openDetail(133); }",
 'fiche Promi de Rachel → le groupe': "()=>{ closeAll(); openDetail(131); }",
 'fiche de Nuée (le potager)': "()=>{ closeAll(); if(window.openEssaim) openEssaim('potager'); }",
 'fiche de la personne (Rachel)': "()=>{ closeAll(); openPerson('Rachel'); }",
}
CAND = r"""(noms)=>{ const dv=document.getElementById('device').getBoundingClientRect(), re=new RegExp('(^|[^\\wÀ-ÿ])('+noms.join('|')+')([^\\wÀ-ÿ]|$)');
  const touche=(e)=>{ const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return null; const x=r.left+r.width/2, y=r.top+r.height/2;
    if(x<dv.left+1||x>dv.right-1||y<dv.top+1||y>dv.bottom-1) return null; const h=document.elementFromPoint(x,y); return (h&&(h===e||e.contains(h)))?[x,y]:null; };
  const out=[];
  document.querySelectorAll('body *').forEach(e=>{ const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').trim();
    let quoi=null, qui=null;
    const m=txt&&txt.length<70?txt.match(re):null; if(m){ quoi='nom'; qui=m[2]; }
    const c=getComputedStyle(e), bg=c.backgroundImage||'', cls=String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||'');
    const r=e.getBoundingClientRect();
    if(!quoi && /ava|vis|visage|kring|au-nb|photo/i.test(cls+' '+(e.id||'')) && r.width>=18 && r.width<=90 && Math.abs(r.width-r.height)<6){ quoi='visage'; qui=e.getAttribute('data-p')||''; }
    if(!quoi) return; const pt=touche(e); if(!pt) return;
    out.push({quoi:quoi, qui:qui, t:txt.slice(0,40), cls:cls.slice(0,40), id:e.id||'', pt:pt}); });
  const vu=new Set(); return out.filter(o=>{ const k=o.quoi+'|'+o.t+'|'+o.cls; if(vu.has(k)) return false; vu.add(k); return true; }).slice(0,18); }"""
APRES = r"""()=>{ const sh=document.getElementById('personSheet'), c=document.getElementById('psCadre');
  return {personne: sh&&sh.classList.contains('show') ? (c?c.getAttribute('data-fiche'):'(ANCIENNE fiche)') : null,
          ouverts:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).filter(i=>i!=='scrim').slice(0,4)}; }"""
R = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto(sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for nom, js in ECRANS.items():
        pg.evaluate(js); pg.wait_for_timeout(2600 if nom=='Aura' else 1400)
        cands = pg.evaluate(CAND, NOMS); avant = pg.evaluate(APRES)['ouverts']; R[nom] = []
        for i, c in enumerate(cands):
            pg.evaluate(js); pg.wait_for_timeout(2600 if nom=='Aura' else 1300)
            cc = pg.evaluate(CAND, NOMS)
            m = [x for x in cc if x['quoi']==c['quoi'] and x['t']==c['t'] and x['cls']==c['cls']]
            if not m: R[nom].append((c, 'introuvable au second passage')); continue
            pg.mouse.click(m[0]['pt'][0], m[0]['pt'][1]); pg.wait_for_timeout(1300)
            a = pg.evaluate(APRES)
            if a['personne']: issue = 'FICHE DE ' + a['personne']
            elif a['ouverts'] != avant: issue = 'ouvre autre chose : ' + ','.join(a['ouverts'])
            else: issue = 'NE MÈNE NULLE PART'
            R[nom].append((c, issue))
        print('\n=== %s — %d nom(s)/visage(s) visibles' % (nom, len(cands)))
        for c, issue in R[nom]: print('   %-6s %-9s « %s » [%s]  →  %s' % (c['quoi'], c['qui'] or '?', c['t'][:34], c['cls'][:22], issue))
    b.close()
