# OÙ LA PILULE COMMENCE-T-ELLE À MANGER LE TEXTE ? (Tom, 11 sept. : « mesure le seuil exact — à quelle hauteur la pilule
# commence à manger le texte — et pose la bascule là, pas à un nombre de lignes arbitraire »).
# 1 · LE RELEVÉ (ce fichier) : chaque champ à contour des Peaufiner (fiche d'un Promi, page +, Nuée), texte d'invite puis
#     texte long (le champ s'ouvre) : sa hauteur, son trait, son rayon, et la place de CHAQUE ligne dans le champ (gauche,
#     haut, bas), en cotes d'écran 390. Plus l'écart mesuré AU NAVIGATEUR avec le rayon en place (sert à valider le modèle).
# 2 · L'ANALYSE (seuil_analyse.py) : l'écart début de ligne → courbe intérieure, pour tout rayon, sans rouvrir le navigateur.
#     La place des lignes ne dépend pas du rayon (le rayon ne touche pas la mise en page) : le calcul est exact.
import json, os, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
ET = sys.argv[2] if len(sys.argv) > 2 else 'app'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'lignes'); os.makedirs(OUT, exist_ok=True)
LONG = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
RELEVE = r"""(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, H=document.querySelector(hote); const out=[];
  const frags=(e)=>{ if(e.tagName==='TEXTAREA'||e.tagName==='INPUT'){ const cs=getComputedStyle(e); const d=document.createElement('div');
      ['fontFamily','fontSize','fontWeight','letterSpacing','lineHeight','wordSpacing','textTransform'].forEach(k=>d.style[k]=cs[k]);
      const r=e.getBoundingClientRect(); d.style.cssText+=';position:fixed;visibility:hidden;white-space:pre-wrap;word-wrap:break-word;left:'+(r.left+parseFloat(cs.paddingLeft))+'px;top:'+(r.top+parseFloat(cs.paddingTop))+'px;width:'+(r.width-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight))+'px';
      d.textContent=e.value||e.placeholder||''; document.body.appendChild(d);
      const rg=document.createRange(); rg.selectNodeContents(d); let F=[...rg.getClientRects()].map(q=>({l:q.left,t:q.top,b:q.bottom}));
      d.remove(); F=F.filter(f=>f.t < r.bottom-1); return F; }                       // jusqu'au bord VISIBLE du champ de saisie
    const F=[]; const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); let n;
    while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) continue;
      if(p.closest('textarea')) continue; const rg=document.createRange(); rg.selectNodeContents(n);
      [...rg.getClientRects()].forEach(q=>{ if(q.width>1) F.push({l:q.left,t:q.top,b:q.bottom}); }); }
    e.querySelectorAll('textarea,input:not([type=file])').forEach(x=>{ if(x.checkVisibility()) frags(x).forEach(f=>F.push(f)); });
    return F; };
  H.querySelectorAll('*').forEach(c=>{ if(!c.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return;
    const cs=getComputedStyle(c), r=c.getBoundingClientRect(); const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2);
    if(bw<=0 || r.height<40 || R < 20 || r.width<200) return;                        // tout champ arrondi à contour (le rayon 30 compris)
    if(r.bottom<dv.top+100 || r.top>dv.bottom-90) return;
    let F=frags(c); if(!F.length) return;
    F.sort((a,b)=>a.t-b.t); const L=[]; F.forEach(f=>{ const g=L.find(x=>Math.abs((x.t+x.b)/2-(f.t+f.b)/2)<4); if(g){g.l=Math.min(g.l,f.l);g.t=Math.min(g.t,f.t);g.b=Math.max(g.b,f.b);} else L.push({...f}); });
    L.sort((a,b)=>a.t-b.t);
    const cy=r.top+r.height/2, ri=R-bw;
    const ecart=(ln)=>{ const hm=ln.b<cy, bm=ln.t>cy; const px=ln.l, py=hm?ln.t:(bm?ln.b:(ln.t+ln.b)/2);
      const ax=r.left+R, ay=py<r.top+R?r.top+R:(py>r.bottom-R?r.bottom-R:py);
      return px<ax ? (ri-Math.hypot(px-ax,py-ay))/s : (px-(r.left+bw))/s; };
    const lab=(c.querySelector('.s2-lab,.np-lab')||c).textContent.replace(/\s+/g,' ').trim().slice(0,22);
    out.push({champ:lab, id:c.id||'', cls:String(c.className).split(' ').slice(0,3).join('.'), h:+(r.height/s).toFixed(2), w:+(r.width/s).toFixed(2), bw:+(bw/s).toFixed(2), rayon:+(R/s).toFixed(2),
      lignes:L.map(x=>({l:+((x.l-r.left)/s).toFixed(2), t:+((x.t-r.top)/s).toFixed(2), b:+((x.b-r.top)/s).toFixed(2)})),
      nav_premiere:+ecart(L[0]).toFixed(2), nav_derniere:+ecart(L[L.length-1]).toFixed(2)}); });
  return out; }"""
REMPLIR = r"""(t)=>{ document.querySelectorAll('#detailPoster .s2-zone textarea, #createSheet .s2-zone textarea, #detailPoster .np-carte textarea, #detailPoster textarea.np-txt').forEach(x=>{ if(!/comment/i.test(x.id||'')) { x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); } }); }"""
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
ECRANS = [
  ('fiche', '#detailPoster', [(BASE, 200), ("()=>openDetail(126)", 1400), ("()=>document.querySelector('#dpDetails .dpd-tog').click()", 1700)]),
  ('page+', '#createSheet', [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 600),
     ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
     ("()=>document.getElementById('csBotBar').click()", 1800)]),
  ('Nuée', '#detailPoster', [(BASE, 200), ("()=>openEssaim('potager')", 1500), ("()=>document.querySelector('#dpDetails .dpd-tog').click()", 1700)]),
]
R = {}
with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
    for nom, hote, steps in ECRANS:
        for texte in ('invite', 'long'):
            for js, w in steps: pg.evaluate(js); pg.wait_for_timeout(w)
            if texte == 'long': pg.evaluate(REMPLIR, LONG); pg.wait_for_timeout(700)
            vus = {}
            for k in range(7):
                pg.evaluate("(k)=>{const c=document.querySelector('%s .dpd-corps')||document.querySelector('%s'); if(c) c.scrollTop=k*240;}" % (hote, hote), k); pg.wait_for_timeout(260)
                for m in pg.evaluate(RELEVE, hote): vus[m['champ'] + '|' + m['cls'] + '|' + m['id']] = m
            R['%s · %s' % (nom, texte)] = list(vus.values())
            print('\n== %s · %s' % (nom, texte))
            for m in vus.values():
                print('   %-22s %-26s h %6.2f r %5.2f · %d lignes · nav 1re %5.2f dern %5.2f' % (m['champ'], (m['id'] or m['cls'])[:26], m['h'], m['rayon'], len(m['lignes']), m['nav_premiere'], m['nav_derniere']))
        if nom != 'Nuée':
            pg.evaluate("()=>{ document.querySelectorAll('#dNote, #createSheet .s2-zone textarea').forEach(x=>{ x.value=''; x.dispatchEvent(new Event('input',{bubbles:true})); }); }")
    br.close()
json.dump(R, open(os.path.join(OUT, 'seuil_releve_%s.json' % ET), 'w'), ensure_ascii=False, indent=1)
print('\nécrit : lignes/seuil_releve_%s.json' % ET)
