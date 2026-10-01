# LE CERCLE — LE JUGE DE LA PLANCHE (PLANCHE-CERCLE.html, les quatre cadres composés de la page du Cercle).
# Chaque cadre est amené dans la fenêtre avant d'être interrogé (CLAUDE §8 : elementsFromPoint travaille en coordonnées
# de fenêtre). Contrôles, tous en cotes du cadre 390 × 844 :
#   1 · rien hors cadre (latéral ; et en vertical, ce qui dépasse doit être rogné par le conteneur qui défile)
#   2 · aucun texte sous 12 px, aucune opacité effective sous 0,72, aucune face hors des six
#   3 · aucun recouvrement entre deux blocs visibles, SAUF l'encart du §3.8 sur ses réglages (la seule superposition)
#   4 · contraste WCAG ≥ 4,5 pour tout texte NET (les réglages floutés sont exclus : ils ne se lisent pas, c'est voulu)
#   5 · l'air entre deux blocs consécutifs de la colonne (bas de A → haut de B), listé
# Captures de chaque cadre sur disque : planche/verif_<cadre>.png.
import json, os, sys
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'planche')
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/PLANCHE-CERCLE.html'
J = r"""(sel)=>{
 const F=document.querySelector(sel), fr=F.getBoundingClientRect(); const out={blocs:[],hors:[],petits:[],contraste:[],faces:[]};
 const lum=(c)=>{const m=c.match(/[\d.]+/g).map(Number); const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}; return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]);};
 const fondDe=(e)=>{for(let p=e;p&&p!==document.body;p=p.parentElement){const b=getComputedStyle(p).backgroundColor; const a=(b.match(/[\d.]+/g)||[]).map(Number); if(a.length>=3&&(a.length<4||a[3]>.6)) return b;} return 'rgb(14,15,18)';};
 const clip=F.querySelector('.defil'), cr=clip?clip.getBoundingClientRect():null;
 F.querySelectorAll('*').forEach(e=>{
   let own=''; for(const n of e.childNodes) if(n.nodeType===3) own+=n.textContent; own=own.trim();
   const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return;
   const x=r.left-fr.left, y=r.top-fr.top;
   const dansDefil = clip && clip.contains(e);
   // ce qui est rogné par le conteneur qui défile ne compte pas, comme sur l'appareil
   const vis = !dansDefil || (r.bottom>cr.top+1 && r.top<cr.bottom-1);
   if(!vis) return;
   const cs=getComputedStyle(e); const blur=/blur/.test(cs.filter)||(e.closest('.reg')!==null);
   const nom=(e.className||e.tagName).toString().split(' ')[0]+(own?' « '+own.slice(0,30)+' »':'');
   if(x<-0.5||x+r.width>390.5) out.hors.push(nom+' x '+x.toFixed(0)+'→'+(x+r.width).toFixed(0));
   if(!dansDefil && (y<-0.5||y+r.height>844.5)) out.hors.push(nom+' y '+y.toFixed(0));
   if(['reg','enc','dal','nom','prix','sous','btn','note','plat'].some(k=>e.classList.contains(k))){
     const yy=dansDefil?Math.max(y,cr.top-fr.top):y, hh=dansDefil?Math.min(r.bottom,cr.bottom)-Math.max(r.top,cr.top):r.height;
     out.blocs.push({k:[...e.classList].join('.'), t:(e.textContent||'').trim().slice(0,28), x:+x.toFixed(1), y:+yy.toFixed(1), w:+r.width.toFixed(1), h:+hh.toFixed(1)});
   }
   if(own){
     const fs=parseFloat(cs.fontSize); if(fs<12) out.petits.push(nom+' '+fs+'px');
     let op=1; for(let p=e;p&&p!==F;p=p.parentElement) op*=parseFloat(getComputedStyle(p).opacity); if(op<.72) out.petits.push(nom+' opacité '+op.toFixed(2));
     const ff=cs.fontFamily.split(',')[0].replace(/["']/g,''); if(!['Fraunces','Bricolage','Apfel','ApfelMid'].includes(ff)) out.faces.push(nom+' '+ff);
     if(!blur){ const a=lum(cs.color), b=lum(fondDe(e)); const k=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
       out.contraste.push({t:own.slice(0,34), k:+k.toFixed(2)}); }
   }
 });
 return out;}"""
res = {}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1600, 'height': 1000}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(1500); pg.evaluate("()=>document.fonts.ready")
    cadres = pg.evaluate("()=>[...document.querySelectorAll('.fr[data-cadre]')].map(f=>f.dataset.cadre)")
    for c in cadres:
        sel = '.fr[data-cadre="%s"]' % c
        pg.locator(sel).scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        r = pg.evaluate(J, sel)
        pg.locator(sel).screenshot(path=os.path.join(OUT, 'verif_%s.png' % c))
        # recouvrements : deux blocs dont les boîtes se coupent, hors encart ↔ réglage
        B = r['blocs']; rec = []
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                a, b = B[i], B[j]
                if a['x'] < b['x'] + b['w'] and b['x'] < a['x'] + a['w'] and a['y'] < b['y'] + b['h'] and b['y'] < a['y'] + a['h']:
                    ks = {a['k'].split('.')[0], b['k'].split('.')[0]}
                    if ks == {'enc', 'reg'}: continue
                    rec.append('%s « %s » ↔ %s « %s »' % (a['k'], a['t'], b['k'], b['t']))
        col = sorted([b for b in B if b['k'] != 'plat'], key=lambda b: b['y'])
        air = []
        for a, b in zip(col, col[1:]):
            if b['y'] >= a['y'] + a['h'] - 0.5 and not (a['k'].startswith('dal') and b['k'].startswith('dal')):
                air.append('%s → %s : %.1f' % (a['t'] or a['k'], b['t'] or b['k'], b['y'] - a['y'] - a['h']))
        faibles = [x for x in r['contraste'] if x['k'] < 4.5]
        res[c] = {'hors': r['hors'], 'petits': r['petits'], 'faces': r['faces'], 'recouvrements': rec, 'contraste_faible': faibles,
                  'contraste_min': min([x['k'] for x in r['contraste']] or [0]), 'air': air}
        print('\n== %s\n   hors cadre %d · <12px/opacité %d · faces %d · recouvrements %d · contraste < 4,5 : %d (min %.2f)'
              % (c, len(r['hors']), len(r['petits']), len(r['faces']), len(rec), len(faibles), res[c]['contraste_min']))
        for k in ('hors', 'petits', 'faces', 'recouvrements', 'contraste_faible'):
            for x in res[c][k]: print('     %s : %s' % (k, x))
        print('   air : ' + ' | '.join(air))
    br.close()
json.dump(res, open(os.path.join(OUT, 'verif.json'), 'w'), ensure_ascii=False, indent=1)
