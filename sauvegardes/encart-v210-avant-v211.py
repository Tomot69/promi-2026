"""v210 C-301 — relevé de l'encart du haut sur chaque page (pt de l'écran 390). python3 scratchpad/v210/encart.py [--fichier=] [--vue=1|079] [--json=]"""
import sys, re, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
V = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--vue=')), '1')
CSS = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--css=')), None)
J = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--json=')), None)
PAGES = [('index', "()=>{ ouvrirIndex(); }"), ('fil', "()=>{ document.getElementById('filBtn').click(); }"),
         ('aura', "()=>{ document.getElementById('souffleBtn').click(); }"), ('reglages', "()=>{ document.getElementById('settingsBtn').click(); }"),
         ('partager', "()=>{ document.getElementById('shareBtn').click(); }"), ('studio', "()=>{ document.getElementById('studioBtn').click(); }"),
         ('aide aura', "async ()=>{ document.getElementById('souffleBtn').click(); await new Promise(r=>setTimeout(r,1500)); document.getElementById('auraInfoBtn').click(); }"),
         ('confidentialite', "async ()=>{ document.getElementById('settingsBtn').click(); await new Promise(r=>setTimeout(r,1200)); document.getElementById('privCard').click(); }"),
         ('ma parole', "()=>{ ouvreCercle(); }")]
REL = r"""()=>{ const dev=document.getElementById('device').getBoundingClientRect(), k=dev.width/390;
 const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); if(r.width<1) return null; return [+((r.left-dev.left)/k).toFixed(2), +((r.top-dev.top)/k).toFixed(2), +(r.width/k).toFixed(2), +(r.height/k).toFixed(2)]; };
 const vis=e=>{ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return false; const c=getComputedStyle(e); if(c.visibility=='hidden'||+c.opacity<0.05) return false; const x=r.left+r.width/2,y=r.top+r.height/2; return true; };
 const ink=e=>{ const g=document.createRange(); g.selectNodeContents(e); const r=g.getBoundingClientRect(); return r.width? [+((r.left-dev.left)/k).toFixed(2), +((r.top-dev.top)/k).toFixed(2), +(r.width/k).toFixed(2), +(r.height/k).toFixed(2)] : null; };
 const P=[...document.querySelectorAll('.enh')].filter(e=>{ const r=e.getBoundingClientRect(); return vis(e) && r.top-dev.top<200*k && r.bottom>dev.top && getComputedStyle(e.closest('.screen,.sheet,#indexScreen,[id$=Screen]')||e).visibility!='hidden'; });
 const top=document.elementFromPoint(dev.left+195*k, dev.top+(window.__ENC_DY||0)*k+70*k); const enh=top && (top.closest('.enh')||top.closest('#stpHaut')||top.closest('#shcTitre'));
 const o={enh:enh?R(enh):null, cls:enh?enh.className:null, host:enh&&enh.parentElement?enh.parentElement.id:null, nb:P.length, items:[]};
 if(enh){ const scr=enh.closest('[id]');
  [...enh.querySelectorAll('*')].concat([...(enh.parentElement||document).querySelectorAll('input,button,.ix-recherche,[id*=Tri],[id*=Search],[id*=Rech]')]).forEach(e=>{
   if(!vis(e)) return; const r=R(e); if(!r || r[1]>220) return; o.items.push([e.tagName, e.id, String(e.className).slice(0,40), (e.textContent||e.placeholder||'').trim().slice(0,16), r, getComputedStyle(e).fontSize]); }); }
 const t=enh&&enh.querySelector('.enh-t,.stp-t'); if(t){ const c=getComputedStyle(t); const g=document.createElement('canvas').getContext('2d'); g.font='100px '+c.fontFamily; const h=g.measureText('H'); const fs=parseFloat(c.fontSize), lh=parseFloat(c.lineHeight), fa=h.fontBoundingBoxAscent/100, fd=h.fontBoundingBoxDescent/100, cap=h.actualBoundingBoxAscent/100; const rt=t.getBoundingClientRect(), re=enh.getBoundingClientRect(); const capC=(rt.top-dev.top)/k+parseFloat(c.paddingTop)+(lh-(fa+fd)*fs)/2+fa*fs-cap*fs/2; o.titre={fs:fs, gauche:+((rt.left-dev.left)/k).toFixed(2), capC:+capC.toFixed(2), centre:+(((re.top+re.height/2)-dev.top)/k).toFixed(2), off:t.offsetParent&&t.offsetParent.className}; }
 const x=enh&&enh.querySelector('.x157-g'); if(x){ const r=x.getBoundingClientRect(); o.X=[+((r.left-dev.left)/k).toFixed(2),+((r.top-dev.top)/k).toFixed(2),+(r.width/k).toFixed(2),+(r.height/k).toFixed(2), getComputedStyle(x).fontSize]; }
 return o; }"""
res = {}
with sync_playwright() as p:
    b = p.webkit.launch()
    vw, vh = (430, 932) if V == '1' else (330, 714)
    ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 10)
    if CSS: ctx.add_init_script("document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent=%r;document.head.appendChild(s);});" % open(CSS).read())
    pg = B.ouvre(ctx, F)
    for nom, js in PAGES:
        pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); }catch(e){} try{ closeAll(); }catch(e){} document.querySelectorAll('#auraScreen.show .closeb, #studioScreen.show .closeb, #settingsScreen.show .closeb, #shareScreen.show .closeb, #auraHelp.show .closeb, #privScreen.show .closeb, #plusScreen.show .closeb').forEach(x=>{ if(x.getBoundingClientRect().top<300) x.click(); }); }")
        pg.wait_for_timeout(700); pg.evaluate(js); pg.wait_for_timeout(2600)
        r = pg.evaluate(REL); res[nom] = r
        if False: print('==', nom, r['enh'], 'titre', r.get('titre'), 'X', r.get('X'))

    b.close()
if J: json.dump(res, open(J, 'w'), ensure_ascii=False, indent=1)

# ── le verdict (C-301) : au demi-point près ; les cotes du composant, EN DUR (Tom : « même hauteur, mêmes marges, même place du titre et du X »)
DY = 3 if CSS else 0     # la coquille de l'app descend l'encart de 3 pt, partout (C-299)
BOITE = [24, 40 + DY, 342, 60]; T = 34; ok = 0; n = 0; ref = res['index']
def ch(c, msg):
    global ok, n; n += 1; ok += bool(c); print(('  ✅ ' if c else '  ❌ ') + msg)
def pr(a, b, tol=0.5): return a is not None and b is not None and all(abs(x - y) <= tol for x, y in zip(a[:4], b[:4]))
for nom, r in res.items():
    t = r.get('titre') or {}
    ch(pr(r['enh'], BOITE), '%-16s l\'encart %s (attendu %s)' % (nom, r['enh'], BOITE))
    ch(abs(t.get('gauche', -9) - 52) <= 0.5 and abs(t.get('capC', -9) - (70 + DY)) <= 0.5, '%-16s le titre : gauche %s, centre des capitales %s (attendus 52, %s)' % (nom, t.get('gauche'), t.get('capC'), 70 + DY))
    # exceptions nommées (v210) : deux titres trop longs pour 34 px avant le X — « VIE PRIVÉE » (249 pt pour 244) et « MA PAROLE ! » (281 : le « ! » est en Gilbert) ;
    # le titre s'ajuste, il ne se rogne pas (lot-HARMONIE) : ils prennent la plus grande taille qui tient. Tout autre titre : 34.
    EXC = {'confidentialite': 33, 'ma parole': 29}
    ch(t.get('fs') == EXC.get(nom, T), '%-16s la taille du titre %s px (attendue %d%s)' % (nom, t.get('fs'), EXC.get(nom, T), ', exception nommée' if nom in EXC else ''))
    ch(pr(r.get('X'), ref.get('X')), '%-16s le X %s (celui de l\'Index : %s)' % (nom, r.get('X'), ref.get('X')))
def item(r, ident): return next((it[4] for it in r['items'] if it[1] == ident), None)
ch(pr(item(res['index'], 'ixSearch'), item(res['fil'], 'fdSearch')), 'la recherche : Index %s, Fil %s' % (item(res['index'], 'ixSearch'), item(res['fil'], 'fdSearch')))
ch(pr(item(res['index'], 'ixTriBtn'), item(res['fil'], 'fdTriBtn')), 'le tri ⇅ : Index %s, Fil %s' % (item(res['index'], 'ixTriBtn'), item(res['fil'], 'fdTriBtn')))
ch(not any(it[1] == 'ixCount' for it in res['index']['items']), 'l\'Index n\'a pas de compteur')
ia = item(res['aura'], 'auraInfoBtn'); ch(ia is not None and abs(ia[1] + ia[3] / 2 - (70 + DY)) <= 0.5, 'le « i » de l\'Aura centré : %s (centre attendu %s)' % (ia and round(ia[1] + ia[3] / 2, 2), 70 + DY))
print('  %s  %d / %d' % ('✅' if ok == n else '❌', ok, n))
