# SECONDE PASSE — chaque visage touché UN PAR UN (la première dédoublonnait par classe : un seul .au-nb essayé, sans savoir lequel),
# et les écrans que la première n'avait pas ouverts : Fil (setView), Peaufiner d'un Promi / d'un Chiche / d'une Nuée, partage, fiche d'un Promi DE Rachel.
import sys
from playwright.sync_api import sync_playwright
NOMS = ['Rachel','Marion','Adrien','Nico','Léa','Maman','Mimi','Mamie','Toi','toi','Moi','moi']
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
BASE = "()=>{ closeAll(); document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"
ECRANS = [
 ('Aura',                         [(BASE,200), ("()=>document.getElementById('souffleBtn').click()",3200)]),
 ('Fil',                          [(BASE,200), ("()=>setView('fil')",1800)]),
 ('Peaufiner · Promi à Rachel',   [(BASE,200), ("()=>openDetail(126)",1200), (PEAUF,1400)]),
 ('Peaufiner · Chiche à Marion avec Rachel', [(BASE,200), ("()=>openDetail(127)",1200), (PEAUF,1400)]),
 ('fiche · Promi DE Rachel au groupe', [(BASE,200), ("()=>openDetail(131)",1400)]),
 ('fiche · Promi à Rachel (disques)',  [(BASE,200), ("()=>openDetail(126)",1400)]),
 ('Nuée potager',                 [(BASE,200), ("()=>openEssaim('potager')",1600)]),
 ('Peaufiner · Nuée potager',     [(BASE,200), ("()=>openEssaim('potager')",1400), (PEAUF,1400)]),
 ('Partage · Promi à Rachel',     [(BASE,200), ("()=>openDetail(126)",1200), ("()=>openShare()",2000)]),
]
CAND = r"""(noms)=>{ const dv=document.getElementById('device').getBoundingClientRect(), re=new RegExp('(^|[^\\wÀ-ÿ])('+noms.join('|')+')([^\\wÀ-ÿ]|$)');
  const touche=(e)=>{ const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return null; const x=r.left+r.width/2, y=r.top+r.height/2;
    if(x<dv.left+1||x>dv.right-1||y<dv.top+1||y>dv.bottom-1) return null; const h=document.elementFromPoint(x,y); return (h&&(h===e||e.contains(h)))?[x,y]:null; };
  const lbs=[...document.querySelectorAll('.au-lb,.kr-n')].filter(l=>l.getBoundingClientRect().width>0);
  const pres=(r)=>{ let best='', bd=1e9; for(const l of lbs){ const q=l.getBoundingClientRect(), d=Math.abs(q.left+q.width/2-(r.left+r.width/2))+Math.abs(q.top-r.bottom); if(d<bd&&d<60){bd=d; best=l.textContent.trim();} } return best; };
  const out=[], rang={};
  document.querySelectorAll('body *').forEach(e=>{ if(e.closest('#personSheet')&&!document.getElementById('personSheet').classList.contains('show')) return;
    const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ').trim();
    let quoi=null, qui=null;
    const m=txt&&txt.length<70?txt.match(re):null; if(m){ quoi='nom'; qui=m[2]; }
    const cls=String(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||''), r=e.getBoundingClientRect();
    if(!quoi && /(^|[\s-])(ava|au-nb|au-vis|s4-vis|ps-vis|kring|kr-av|vis|visage|photo)([\s-]|$)/i.test(cls) && r.width>=16 && r.width<=96 && Math.abs(r.width-r.height)<8){ quoi='visage'; qui=e.getAttribute('data-p')||pres(r)||''; }
    if(!quoi) return; const pt=touche(e); if(!pt) return;
    const cle=quoi+'|'+txt.slice(0,40)+'|'+cls.slice(0,40); rang[cle]=(rang[cle]||0)+1;
    out.push({quoi, qui, t:txt.slice(0,44), cls:cls.slice(0,40), cle, n:rang[cle]-1, pt}); });
  return out.slice(0,24); }"""
ETAT = r"""()=>{ const sh=document.getElementById('personSheet'), c=document.getElementById('psCadre');
  return {personne: sh&&sh.classList.contains('show') ? (c?c.getAttribute('data-fiche'):'(ANCIENNE fiche)') : null,
          ouverts:[...document.querySelectorAll('.show')].map(e=>e.id).filter(Boolean).filter(i=>i!=='scrim').slice(0,5).join(','),
          texte:(document.body.innerText||'').length}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def ouvrir(steps):
        for js, w in steps: pg.evaluate(js); pg.wait_for_timeout(w)
    for nom, steps in ECRANS:
        ouvrir(steps); cands = pg.evaluate(CAND, NOMS)
        print('\n=== %s — %d nom(s)/visage(s) visibles' % (nom, len(cands)))
        for c in cands:
            ouvrir(steps); avant = pg.evaluate(ETAT)
            m = [x for x in pg.evaluate(CAND, NOMS) if x['cle']==c['cle'] and x['n']==c['n']]
            if not m: print('   %-6s %-8s « %s » [%s] → introuvable au second passage' % (c['quoi'], c['qui'], c['t'][:36], c['cls'][:24])); continue
            pg.mouse.click(m[0]['pt'][0], m[0]['pt'][1]); pg.wait_for_timeout(1300); a = pg.evaluate(ETAT)
            if a['personne'] and not avant['personne']: issue = 'FICHE DE ' + a['personne']
            elif a['personne'] and avant['personne'] and a['personne']!=avant['personne']: issue = 'FICHE DE ' + a['personne']
            elif a['ouverts'] != avant['ouverts']: issue = 'ouvre autre chose : ' + a['ouverts']
            elif abs(a['texte']-avant['texte'])>2: issue = "rien d'ouvert, mais l'écran change (%+d car.)" % (a['texte']-avant['texte'])
            else: issue = 'NE MÈNE NULLE PART'
            print('   %-6s %-8s « %s » [%s]  →  %s' % (c['quoi'], c['qui'] or '?', c['t'][:36], c['cls'][:24], issue))
    b.close()
