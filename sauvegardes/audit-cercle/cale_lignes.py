# UN CHAMP À TROIS LIGNES SERRE SON CADRE — LE CALAGE (Tom, 11 sept. : « Réduis un peu l'interligne dans ce cas précis —
# exceptionnellement, seulement à trois lignes et plus. Mesure l'écart entre le texte et le contour, il doit rester constant
# quel que soit le nombre de lignes. »)
# CIBLE : l'écart du champ à DEUX lignes de la fiche (PIÈCES JOINTES, mesuré 12,9 / 13,7) — la norme que le produit tient.
# Même mesure que mesure_lignes.py : distance du DÉBUT de la ligne (coin haut-gauche pour la moitié haute, bas-gauche pour
# la moitié basse) à la courbe INTÉRIEURE du contour.
# On cherche, dans la page (rien dans app.html), le plus petit resserrement qui porte la 1re et la dernière ligne à la cible,
# puis on recentre la ligne du milieu. À 4 lignes (NOTE longue) : (a) le mieux possible DANS la boîte de 118 ;
# (b) la boîte s'allonge d'une ligne, rayon gardé à celui de trois lignes. Sortie : lignes/calage.json + journal.
import json, os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'lignes'); os.makedirs(OUT, exist_ok=True)
GAPS = r"""
window.__gaps = function(c){ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const cs=getComputedStyle(c), r=c.getBoundingClientRect(); const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2);
  const F=[];
  const txt=(e)=>{ const w=document.createTreeWalker(e,NodeFilter.SHOW_TEXT); let n;
    while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})||p.closest('textarea')) continue;
      const rg=document.createRange(); rg.selectNodeContents(n); [...rg.getClientRects()].forEach(q=>{ if(q.width>1) F.push({l:q.left,t:q.top,b:q.bottom}); }); } };
  txt(c);
  c.querySelectorAll('textarea,input:not([type=file])').forEach(e=>{ if(!e.checkVisibility()) return; const k=getComputedStyle(e), er=e.getBoundingClientRect(); const d=document.createElement('div');
    ['fontFamily','fontSize','fontWeight','letterSpacing','lineHeight'].forEach(p=>d.style[p]=k[p]);
    d.style.cssText+=';position:fixed;visibility:hidden;white-space:pre-wrap;word-wrap:break-word;left:'+er.left+'px;top:'+er.top+'px;width:'+er.width+'px';
    d.textContent=e.value||e.placeholder||''; document.body.appendChild(d); const rg=document.createRange(); rg.selectNodeContents(d);
    const mh=parseFloat(k.maxHeight); [...rg.getClientRects()].forEach(q=>{ if(q.width>1 && (!isFinite(mh)||q.top<er.top+mh-1)) F.push({l:q.left,t:q.top,b:q.bottom}); }); d.remove(); });
  F.sort((a,b)=>a.t-b.t); const L=[]; F.forEach(f=>{ const g=L.find(x=>Math.abs((x.t+x.b)/2-(f.t+f.b)/2)<4); if(g){g.l=Math.min(g.l,f.l);g.t=Math.min(g.t,f.t);g.b=Math.max(g.b,f.b);} else L.push({...f}); });
  L.sort((a,b)=>a.t-b.t); const cy=r.top+r.height/2, ri=R-bw;
  const e=(ln)=>{ const hm=ln.b<cy, bm=ln.t>cy; const px=ln.l, py=hm?ln.t:(bm?ln.b:(ln.t+ln.b)/2); const ax=r.left+R, ay=py<r.top+R?r.top+R:(py>r.bottom-R?r.bottom-R:py);
    return px<ax?(ri-Math.hypot(px-ax,py-ay))/s:(px-(r.left+bw))/s; };
  return {lignes:L.length, premiere:L.length?+e(L[0]).toFixed(2):null, derniere:L.length?+e(L[L.length-1]).toFixed(2):null,
          ys:L.map(x=>+((x.t-r.top)/s).toFixed(1)), yb:L.map(x=>+((x.b-r.top)/s).toFixed(1)), h:+(r.height/s).toFixed(1), rayon:+(R/s).toFixed(1)}; };
"""
# le calage d'un champ : haut (padding du flux), bas (ancre du texte cloué en bas), marge du texte du milieu, interligne.
CALE = r"""(a)=>{ const [sel, cible, mode] = a; const c=document.querySelector(sel); if(!c) return {absent:sel};
  const lab=c.querySelector('.s2-lab,.np-lab'), mid=c.querySelector('textarea,input:not([type=file]),.np-ph'), bas=c.querySelector('.s2-vis,.np-bas');
  const P=(e,k,v)=>e&&e.style.setProperty(k,v,'important');
  const avant=window.__gaps(c);
  const csP=getComputedStyle(c); const padG=csP.paddingLeft, padD=csP.paddingRight;
  const b0=parseFloat(getComputedStyle(bas).bottom);
  // 1 · le haut : le plus petit padding-top qui porte la 1re ligne à la cible
  let pt=parseFloat(csP.paddingTop); for(; pt<60; pt+=0.25){ P(c,'padding',pt+'px '+padD+' 0 '+padG); if(window.__gaps(c).premiere>=cible) break; }
  // 2 · le bas : la plus petite ancre qui porte la dernière ligne à la cible
  let bb=b0; for(; bb<60; bb+=0.25){ P(bas,'bottom',bb+'px'); if(window.__gaps(c).derniere>=cible) break; }
  // 3 · la ligne du milieu, recentrée entre le libellé et le bas ; interligne réduit s'il le faut
  const lr=lab.getBoundingClientRect(), br=bas.getBoundingClientRect(), s=document.getElementById('device').getBoundingClientRect().width/390;
  const fs=parseFloat(getComputedStyle(mid).fontSize);
  // ⚠ le nombre de lignes du MILIEU se COMPTE (lignes mesurées − le libellé − le bas), il ne se déduit pas de la
  // hauteur du textarea : sa hauteur plancher (44) faisait compter 2 lignes pour une, et réduisait l'interligne à tort.
  const n=Math.max(1, avant.lignes - 2);
  let lh=1.25; const place=(br.top-lr.bottom)/s;              // l'espace entre le libellé et le bas, en cotes écran
  while(lh>1.0 && n*fs*lh > place-6) lh-=0.01;                // on ne réduit l'interligne que si le texte ne tient pas
  const m=Math.max(2,(place - n*fs*lh)/2);
  P(mid,'line-height',lh.toFixed(2)); P(mid,'margin-top',m.toFixed(1)+'px'); if(mid.tagName==='TEXTAREA') P(mid,'max-height',(n*fs*lh+1).toFixed(1)+'px');
  const apres=window.__gaps(c);
  return {sel, avant, apres, reglage:{padding_top:pt, bas:bb, bas_avant:b0, milieu_marge:+m.toFixed(1), interligne:+lh.toFixed(2), lignes_milieu:n,
          tient: n*fs*lh <= place-6}}; }"""
GRANDIT = r"""(a)=>{ const [sel, cible, rayon] = a; const c=document.querySelector(sel); const P=(e,k,v)=>e&&e.style.setProperty(k,v,'important');
  // (b) la boîte s'allonge d'UNE ligne de texte, le rayon garde sa valeur de trois lignes
  const mid=c.querySelector('textarea'); const lh=parseFloat(getComputedStyle(mid).lineHeight);
  const h0=c.getBoundingClientRect().height/(document.getElementById('device').getBoundingClientRect().width/390);
  P(c,'height',(118+lh)+'px'); P(c,'border-radius',rayon+'px'); P(mid,'max-height',(2*lh+1)+'px'); P(mid,'line-height','1.25');
  return window.__gaps(c); }"""
LONG = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    # ⚠ une chaîne dont la VALEUR est une fonction est APPELÉE par Playwright (sans argument) : on l'enveloppe
    pg.evaluate("()=>setTheme('dark')"); pg.evaluate("()=>{" + GAPS + "}")
    def fiche():
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>openDetail(126)"); pg.wait_for_timeout(1400)
        pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
    # la référence : le champ à deux lignes de la fiche
    fiche()
    ref = pg.evaluate("()=>window.__gaps([...document.querySelectorAll('#detailPoster .s2-reg.s2-vis2')][0])")
    cible = round(min(ref['premiere'], ref['derniere']), 1)
    print('RÉFÉRENCE · PIÈCES JOINTES de la fiche (2 lignes) : %s  → cible %.1f' % (ref, cible)); R['reference'] = ref; R['cible'] = cible
    # NOTE et COMMENTAIRES (3 lignes)
    for i, nom in ((0, 'NOTE'), (1, 'COMMENTAIRES')):
        fiche()
        pg.evaluate("(i)=>{ document.querySelectorAll('#detailPoster .s2-zone').forEach(z=>z.removeAttribute('data-cale')); const z=document.querySelectorAll('#detailPoster .s2-zone')[i]; z.setAttribute('data-cale','1'); z.scrollIntoView({block:'center'}); }", i)
        pg.wait_for_timeout(300)
        r = pg.evaluate(CALE, ['#detailPoster .s2-zone[data-cale]', cible, ''])
        R['fiche · ' + nom] = r
        print('\n%s (fiche) avant %s\n   après %s\n   réglage %s' % (nom, r['avant'], r['apres'], r['reglage']))
        pg.locator('#device').screenshot(path=os.path.join(OUT, 'cale_fiche_%s.png' % nom))
    # NOTE longue (4 lignes) : (a) dans la boîte, (b) la boîte s'allonge
    fiche()
    pg.evaluate("(t)=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[0]; z.setAttribute('data-cale','1'); const x=z.querySelector('textarea'); x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); z.scrollIntoView({block:'center'}); }", LONG)
    pg.wait_for_timeout(400)
    r = pg.evaluate(CALE, ['#detailPoster .s2-zone[data-cale]', cible, '']); R['fiche · NOTE longue · dans la boîte'] = r
    print('\nNOTE longue (a · dans la boîte de 118) avant %s\n   après %s\n   réglage %s' % (r['avant'], r['apres'], r['reglage']))
    pg.locator('#device').screenshot(path=os.path.join(OUT, 'cale_fiche_NOTE_longue_a.png'))
    fiche()
    pg.evaluate("(t)=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[0]; z.setAttribute('data-cale','1'); const x=z.querySelector('textarea'); x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); z.scrollIntoView({block:'center'}); }", LONG)
    pg.wait_for_timeout(300)
    rc = R['fiche · NOTE']['reglage']
    pg.evaluate("(a)=>{ const z=document.querySelector('#detailPoster .s2-zone[data-cale]'); const P=(e,k,v)=>e.style.setProperty(k,v,'important');"
                "P(z,'padding',a[0]+'px 23px 0 23px'); P(z.querySelector('.s2-vis'),'bottom',a[1]+'px'); P(z.querySelector('textarea'),'margin-top',a[2]+'px'); }",
                [rc['padding_top'], rc['bas'], rc['milieu_marge']])
    g = pg.evaluate(GRANDIT, ['#detailPoster .s2-zone[data-cale]', cible, 59]); R['fiche · NOTE longue · la boîte s’allonge'] = g
    print('\nNOTE longue (b · la boîte s’allonge d’une ligne, rayon 59) %s' % g)
    pg.locator('#device').screenshot(path=os.path.join(OUT, 'cale_fiche_NOTE_longue_b.png'))
    # la page + : NOTE
    pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1600)
    pg.evaluate("()=>{ const z=document.querySelector('#createSheet .s2-zone'); z.setAttribute('data-cale','1'); z.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(300)
    r = pg.evaluate(CALE, ['#createSheet .s2-zone[data-cale]', cible, '']); R['page + · NOTE'] = r
    print('\nNOTE (page +) avant %s\n   après %s\n   réglage %s' % (r['avant'], r['apres'], r['reglage']))
    # la Nuée : DESCRIPTION et COMMENTAIRES (104), et PIÈCES JOINTES (92) comparée à la fiche
    for cid in ('npDesc', 'npComm'):
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700)
        pg.evaluate("(id)=>document.getElementById(id).scrollIntoView({block:'center'})", cid); pg.wait_for_timeout(300)
        r = pg.evaluate(CALE, ['#' + cid, cible, '']); R['Nuée · ' + cid] = r
        print('\n%s (Nuée) avant %s\n   après %s\n   réglage %s' % (cid, r['avant'], r['apres'], r['reglage']))
        pg.locator('#device').screenshot(path=os.path.join(OUT, 'cale_nuee_%s.png' % cid))
    pj = pg.evaluate("()=>window.__gaps(document.getElementById('npFich'))"); R['Nuée · npFich (2 lignes)'] = pj
    print('\nPIÈCES JOINTES (Nuée, 2 lignes) %s   · la même sur la fiche : %s' % (pj, ref))
    br.close()
json.dump(R, open(os.path.join(OUT, 'calage.json'), 'w'), ensure_ascii=False, indent=1)
