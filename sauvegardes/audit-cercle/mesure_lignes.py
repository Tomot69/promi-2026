# UN CHAMP À TROIS LIGNES SERRE SON CADRE (Tom, 11 sept.) — la mesure.
# Pour chaque champ à contour arrondi (rayon ≥ un tiers de la hauteur, trait > 0) des Peaufiner — fiche d'un Promi,
# page +, Nuée — on relève ses LIGNES DE TEXTE (fragments de ligne réels ; pour un textarea, un double invisible, même
# police, même largeur, même texte) et, pour la PREMIÈRE et la DERNIÈRE, la distance entre le DÉBUT de la ligne et la
# courbe INTÉRIEURE du contour (le trait déduit) :
#   · coin haut-gauche pour une ligne de la moitié haute, coin bas-gauche pour la moitié basse, milieu-gauche sinon ;
#   · distance au cercle de l'arrondi si le point est dans l'arrondi, sinon au bord droit du trait.
# Deux passages : le texte tel quel (invite), puis un texte LONG posé dans les champs qui s'écrivent (le champ passe
# alors à ses lignes maximales). Usage : mesure_lignes.py [etiquette] [js_a_appliquer_avant]
import json, os, sys
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'lignes'); os.makedirs(OUT, exist_ok=True)
ET = sys.argv[1] if len(sys.argv) > 1 else 'avant'
PATCH = sys.argv[2] if len(sys.argv) > 2 else ''
LONG = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
MESURE = r"""(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, H=document.querySelector(hote);
  const out=[];
  const frags=(e)=>{ // fragments de ligne du texte visible d'un nœud (textarea : un double)
    if(e.tagName==='TEXTAREA'||e.tagName==='INPUT'){ const cs=getComputedStyle(e); const d=document.createElement('div');
      ['fontFamily','fontSize','fontWeight','letterSpacing','lineHeight','wordSpacing','textTransform'].forEach(k=>d.style[k]=cs[k]);
      const r=e.getBoundingClientRect(); d.style.cssText+=';position:fixed;visibility:hidden;white-space:pre-wrap;word-wrap:break-word;left:'+(r.left+parseFloat(cs.paddingLeft))+'px;top:'+(r.top+parseFloat(cs.paddingTop))+'px;width:'+(r.width-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight))+'px';
      d.textContent=e.value||e.placeholder||''; document.body.appendChild(d);
      const rg=document.createRange(); rg.selectNodeContents(d); let F=[...rg.getClientRects()].map(q=>({l:q.left,t:q.top,b:q.bottom,r:q.right}));
      d.remove(); const maxH=parseFloat(cs.maxHeight); if(isFinite(maxH)) F=F.filter(f=>f.t < r.top+parseFloat(cs.paddingTop)+maxH-1); return F; }
    const F=[]; const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); let n;
    while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) continue;
      if(p.closest('textarea')) continue; const rg=document.createRange(); rg.selectNodeContents(n);
      [...rg.getClientRects()].forEach(q=>{ if(q.width>1) F.push({l:q.left,t:q.top,b:q.bottom,r:q.right}); }); }
    e.querySelectorAll('textarea,input').forEach(x=>{ if(x.checkVisibility()) frags(x).forEach(f=>F.push(f)); });
    return F; };
  H.querySelectorAll('*').forEach(c=>{ if(!c.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return;
    const cs=getComputedStyle(c), r=c.getBoundingClientRect(); const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2);
    if(bw<=0 || r.height<40 || R < r.height/3 || r.width<200) return;
    if(r.bottom<dv.top+100 || r.top>dv.bottom-90) return;           // hors de la zone lisible (sous le plateau / la barre)
    let F=frags(c); if(!F.length) return;
    // regrouper les fragments par ligne (même bande verticale)
    F.sort((a,b)=>a.t-b.t); const L=[]; F.forEach(f=>{ const g=L.find(x=>Math.abs((x.t+x.b)/2-(f.t+f.b)/2)<4); if(g){g.l=Math.min(g.l,f.l);g.t=Math.min(g.t,f.t);g.b=Math.max(g.b,f.b);} else L.push({...f}); });
    L.sort((a,b)=>a.t-b.t);
    const cy=r.top+r.height/2, ri=R-bw;
    const ecart=(ln)=>{ const hautMoitie=ln.b<cy, basMoitie=ln.t>cy; const px=ln.l, py=hautMoitie?ln.t:(basMoitie?ln.b:(ln.t+ln.b)/2);
      const ax=r.left+R, ay=py<r.top+R?r.top+R:(py>r.bottom-R?r.bottom-R:py);
      return px<ax ? (ri-Math.hypot(px-ax,py-ay))/s : (px-(r.left+bw))/s; };
    const lab=(c.querySelector('.s2-lab,.np-lab')||c).textContent.replace(/\s+/g,' ').trim().slice(0,22);
    out.push({champ:lab, cls:String(c.className).split(' ').slice(0,3).join('.'), h:+(r.height/s).toFixed(1), rayon:+(R/s).toFixed(1), lignes:L.length,
      premiere:+ecart(L[0]).toFixed(1), derniere:+ecart(L[L.length-1]).toFixed(1),
      ys:L.map(x=>+(((x.t-r.top)/s)).toFixed(1)), min:+Math.min(...L.map(ecart)).toFixed(1)}); });
  return out; }"""
REMPLIR = r"""(t)=>{ document.querySelectorAll('#detailPoster .s2-zone textarea, #createSheet .s2-zone textarea, #detailPoster .np-carte textarea, #detailPoster textarea.np-txt').forEach(x=>{ if(!/comment/i.test(x.id||'')) { x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); } });
  document.querySelectorAll('#detailPoster .np-carte').forEach(c=>{ const d=c.querySelector('.np-val,.np-txt'); if(d && d.tagName!=='TEXTAREA' && /présente/.test(d.textContent)) d.textContent=t; }); }"""
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ECRANS = [
  ('fiche Promi 126', '#detailPoster', [(BASE, 200), ("()=>openDetail(126)", 1400), ("()=>document.querySelector('#dpDetails .dpd-tog').click()", 1600)]),
  ('page +', '#createSheet', [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 600),
     ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
     ("()=>document.getElementById('csBotBar').click()", 1600)]),
  ('Nuée potager', '#detailPoster', [(BASE, 200), ("()=>openEssaim('potager')", 1500), ("()=>document.querySelector('#dpDetails .dpd-tog').click()", 1600)]),
]
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('dark')"); pg.wait_for_timeout(300)
    if PATCH: pg.evaluate(PATCH)
    for nom, hote, steps in ECRANS:
        for texte in ('invite', 'long'):
            for js, w in steps: pg.evaluate(js); pg.wait_for_timeout(w)
            if texte == 'long': pg.evaluate(REMPLIR, LONG); pg.wait_for_timeout(600)
            # défiler par pas pour voir TOUS les champs de la liste
            vus = {}
            for k in range(6):
                pg.evaluate("(k)=>{const c=document.querySelector('%s .dpd-corps')||document.querySelector('%s'); if(c) c.scrollTop=k*260;}" % (hote, hote), k); pg.wait_for_timeout(250)
                for m in pg.evaluate(MESURE, hote): vus[m['champ'] + '|' + m['cls']] = m
            R['%s · %s' % (nom, texte)] = list(vus.values())
            pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s_%s.png' % (ET, nom.split()[0], texte)))
            print('\n== %s · %s' % (nom, texte))
            for m in vus.values():
                print('   %-22s %-24s h %5.1f r %5.1f · %d lignes · 1re %5.1f · dernière %5.1f · min %5.1f · y %s' % (m['champ'], m['cls'], m['h'], m['rayon'], m['lignes'], m['premiere'], m['derniere'], m['min'], m['ys']))
    br.close()
json.dump(R, open(os.path.join(OUT, 'lignes_%s.json' % ET), 'w'), ensure_ascii=False, indent=1)
