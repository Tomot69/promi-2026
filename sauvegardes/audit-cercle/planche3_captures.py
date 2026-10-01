# LE CERCLE, PLANCHE 3 — LES TROIS CORRECTIONS DE TOM (11 sept. 2026). Rien n'est écrit dans app.html : tout se pose
# dans la page, le temps de la prise, et tout ce qui est posé est DÉCLARÉ sur la planche.
#   1 · l'ordre des réglages payants : RÉCURRENCE · RAPPEL · LA MÉMOIRE · C'EST IMPORTANT ?
#   2 · le bandeau du Peaufiner de la page + : la pastille de la page + (.enh, dont le « FERMER » tombe sous le titre) et le
#       rond photo (.ph-photo-btn) sont AU PRODUIT (probe_bandeau.py : chemin utilisateur pur, sans maquette) — masqués
#       sur la planche, notés en chantier ;
#   3 · les champs à trois lignes et plus : deux versions mesurées —
#       T · la consigne : l'interligne resserré, jamais sous l'air du champ à deux lignes (5,8), le texte recentré ;
#       P · le panneau : rayon 30 (le grand panneau de la grammaire), l'interligne intact.
#       + la carte PIÈCES JOINTES de la Nuée alignée sur celle de la fiche (même champ, deux cotes : 6,35 contre 12,9).
# Sections 1, 2, 4 (mur, chemin, abonné) : T appliqué — c'est la consigne. Section 5 : avant / T / P, avec les mesures.
import json, os
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'planche3'); os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
PAGEPLUS = [(BASE, 200), ("()=>document.getElementById('createBtn').click()", 500),
  ("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}", 900),
  ("()=>{window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'}; if(window._phraseRendu)_phraseRendu();}", 700),
  ("()=>document.getElementById('csBotBar').click()", 1500)]
LONG = "prévenir Rachel la veille, apporter le gâteau et les bougies"   # deux lignes de texte → le champ en a quatre
LONG5 = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"   # trois → cinq : il DÉBORDE (chantier)
AIR = 5.8   # l'air entre les deux lignes du champ à deux lignes de la fiche (PIÈCES JOINTES : 45 → 50,8)

OUTILS = r"""()=>{
 const P=(e,k,v)=>e&&e.style.setProperty(k,v,'important');
 const L_ = function(c){ const cs=getComputedStyle(c), r=c.getBoundingClientRect(); const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2);
   const F=[];
   const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT); let n;
   while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})||p.closest('textarea')) continue;
     const rg=document.createRange(); rg.selectNodeContents(n); [...rg.getClientRects()].forEach(q=>{ if(q.width>1) F.push({l:q.left,t:q.top,b:q.bottom}); }); }
   c.querySelectorAll('textarea,input:not([type=file])').forEach(e=>{ if(!e.checkVisibility()) return; const k=getComputedStyle(e), er=e.getBoundingClientRect(); const d=document.createElement('div');
     ['fontFamily','fontSize','fontWeight','letterSpacing','lineHeight'].forEach(p=>d.style[p]=k[p]);
     d.style.cssText+=';position:fixed;visibility:hidden;white-space:pre-wrap;word-wrap:break-word;left:'+er.left+'px;top:'+er.top+'px;width:'+er.width+'px';
     d.textContent=e.value||e.placeholder||''; document.body.appendChild(d); const rg=document.createRange(); rg.selectNodeContents(d);
     /* ⚠ la limite est le bord VISIBLE du champ (son rectangle), pas sa max-height déclarée : un premier filtre sur la
      max-height a caché une troisième ligne bel et bien PEINTE sur la ligne de visibilité */
     [...rg.getClientRects()].forEach(q=>{ if(q.width>1 && q.top<er.bottom-1) F.push({l:q.left,t:q.top,b:q.bottom}); }); d.remove(); });
   F.sort((a,b)=>a.t-b.t); const L=[]; F.forEach(f=>{ const g=L.find(x=>Math.abs((x.t+x.b)/2-(f.t+f.b)/2)<4); if(g){g.l=Math.min(g.l,f.l);g.t=Math.min(g.t,f.t);g.b=Math.max(g.b,f.b);} else L.push({...f}); });
   L.sort((a,b)=>a.t-b.t);
   return {L:L.map(x=>({l:x.l-r.left,t:x.t-r.top,b:x.b-r.top})), H:r.height, R, bw}; };
 const mesure = function(c){ const g=L_(c), L=g.L, cy=g.H/2, ri=g.R-g.bw;
   const e=(ln)=>{ const hm=ln.b<cy, bm=ln.t>cy; const px=ln.l, py=hm?ln.t:(bm?ln.b:(ln.t+ln.b)/2); const ax=g.R, ay=py<g.R?g.R:(py>g.H-g.R?g.H-g.R:py);
     return px<ax?(ri-Math.hypot(px-ax,py-ay)):(px-g.bw); };
   let air=Infinity; for(let i=0;i+1<L.length;i++) air=Math.min(air, L[i+1].t-L[i].b);
   return {lignes:L.length, premiere:L.length?+e(L[0]).toFixed(1):null, derniere:L.length?+e(L[L.length-1]).toFixed(1):null,
           air_min: isFinite(air)?+air.toFixed(1):null, h:+g.H.toFixed(1), rayon:+g.R.toFixed(1), ys:L.map(x=>+x.t.toFixed(1))}; };
 const parts = (c)=>({lab:c.querySelector('.s2-lab,.np-lab'), mid:c.querySelector('textarea,input:not([type=file]),.np-ph'), bas:c.querySelector('.s2-vis,.np-bas')});
 /* T · la consigne : à trois lignes et plus, l'air entre les lignes descend à celui du champ à deux lignes, et le bloc
    se recentre dans sa boîte. La boîte et son rayon ne bougent pas. */
 const T = function(c, air){ const {lab,mid,bas}=parts(c); if(!lab||!mid||!bas) return mesure(c);
   let g=L_(c); if(g.L.length<3) return mesure(c);
   const L=g.L, H=g.H, hl=L[0].b-L[0].t, hv=L[L.length-1].b-L[L.length-1].t, hm=L[L.length-2].b-L[1].t;
   /* ⚠ QUAND LA BOÎTE EST PLEINE, T NE TOUCHE RIEN. Première écriture : à quatre lignes, le bloc ne tient plus en
      recentrant (il faudrait remonter le libellé au-dessus de sa place), et le calage du bas poussait la dernière ligne
      PLUS BAS qu'aujourd'hui — mesuré −1,1 contre 2,5 : T aggravait le cas qu'il devait soulager. */
   const topT=(H-(hl+hm+hv+2*air))/2;
   if(topT<=L[0].t+0.1){ c.setAttribute('data-planche','T-sans-effet'); return Object.assign(mesure(c),{sans_effet:true}); }
   const top=topT;
   for(let k=0;k<3;k++){
     g=L_(c); P(c,'padding-top',(parseFloat(getComputedStyle(c).paddingTop)+top-g.L[0].t)+'px');
     g=L_(c); P(mid,'margin-top',(parseFloat(getComputedStyle(mid).marginTop)+(top+hl+air)-g.L[1].t)+'px');
     g=L_(c); const Ln=g.L; P(bas,'bottom',(parseFloat(getComputedStyle(bas).bottom)+(Ln[Ln.length-1].b-(top+hl+hm+hv+2*air)))+'px'); }
   c.setAttribute('data-planche','T'); return mesure(c); };
 /* P · le panneau : à trois lignes et plus, rayon 30 (le grand panneau de la grammaire) ; l'interligne ne bouge pas. */
 const Pn = function(c){ if(L_(c).L.length<3) return mesure(c); P(c,'border-radius','30px'); c.setAttribute('data-planche','P'); return mesure(c); };
 /* la carte PIÈCES JOINTES de la Nuée prend les places de celle de la fiche (libellé à 23, bas à 50,8 du haut) */
 const alignePJ = function(c, t1, t2){ const bas=c.querySelector('.np-bas'); if(!bas) return mesure(c); P(c,'align-content','flex-start');
   for(let k=0;k<3;k++){ let g=L_(c); P(c,'padding-top',(parseFloat(getComputedStyle(c).paddingTop)+t1-g.L[0].t)+'px');
     g=L_(c); P(bas,'margin-top',(parseFloat(getComputedStyle(bas).marginTop)+t2-g.L[g.L.length-1].t)+'px'); }
   c.setAttribute('data-planche','PJ'); return mesure(c); };
 const ordre = function(hote){ document.querySelectorAll(hote+' .s2-cercle').forEach(b=>{ const regs=[...b.querySelectorAll(':scope > .s2-reg')];
   const k=r=>{const t=(r.querySelector('.s2-lab')||r).textContent; return /RÉCURRENCE/.test(t)?0:/RAPPEL/.test(t)?1:/MÉMOIRE/.test(t)?2:3;};
   const enc=b.querySelector(':scope > .s2-encart'); regs.sort((a,z)=>k(a)-k(z)).forEach(r=>b.insertBefore(r, enc||null)); }); };
 const bandeau = function(){ const cs=document.getElementById('createSheet'); if(!cs||!cs.classList.contains('pp-peauf')) return 0; let n=0;
   cs.querySelectorAll('.enh, .ph-photo-btn').forEach(e=>{ if(!e.checkVisibility()) return; e.setAttribute('data-planche-masque','1'); P(e,'visibility','hidden'); n++; }); return n; };
 const encartSeul = function(hote){ document.querySelectorAll(hote+' .s2-encart .s2-enc-s').forEach(s=>P(s,'display','none')); };
 const champs = function(hote){ return [...document.querySelectorAll(hote+' .s2-zone, '+hote+' .np-carte')].filter(c=>c.checkVisibility()); };
 window.__P3 = {L_, mesure, T, Pn, alignePJ, ordre, bandeau, encartSeul, champs};
 /* le mur de la page + : la brique de l'app, remise par un observateur quand la liste est rebâtie (planche 2) */
 const cs=document.getElementById('createSheet');
 const pose=()=>{ const l=cs.querySelector(':scope > .dpd-corps .s2-liste')||cs.querySelector('.s2-liste');
   if(!l || !cs.classList.contains('pp-peauf')) return; if(l.querySelector('.s2-cercle')) return;
   l.appendChild(window._s2Briques.cercle()); encartSeul('#createSheet'); ordre('#createSheet');
   try{ if(window._cerclePaye) window._cerclePaye(); }catch(e){} };
 if(!window.__murPP){ window.__murPP=new MutationObserver(()=>pose()); window.__murPP.observe(cs,{childList:true,subtree:true}); }
 window.__P3.pose=pose; }"""

COTES = r"""(hote)=>{ const b=document.querySelector(hote+' .s2-cercle'); if(!b) return null; b.scrollIntoView({block:'center'});
  const dv=document.getElementById('device').getBoundingClientRect(); const q=(e)=>{ if(!e) return null; const r=e.getBoundingClientRect(); return {x:r.left-dv.left, y:r.top-dv.top, w:r.width, h:r.height, vis:e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})}; };
  return {bloc:q(b), encart:q(b.querySelector('.s2-encart')), ordre:[...b.querySelectorAll(':scope > .s2-reg .s2-lab')].map(x=>x.textContent),
          flous:[...b.querySelectorAll('.s2-reg')].map(r=>getComputedStyle(r).filter), touchable:[...b.querySelectorAll('.s2-reg')].map(r=>getComputedStyle(r).pointerEvents)}; }"""
T_TOUS = "(a)=>{ return window.__P3.champs(a[0]).map(c=>({champ:(c.querySelector('.s2-lab,.np-lab')||c).textContent.trim(), ...window.__P3.T(c, a[1])})); }"
C = {}; M = {}
def joue(pg, steps):
    for js, w in steps: pg.evaluate(js); pg.wait_for_timeout(w)
def prise(pg, nom): pg.locator('#device').screenshot(path=os.path.join(OUT, nom + '.png'))
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("()=>document.fonts.ready"); pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(300)
        pg.evaluate(OUTILS)
        # ── sections 1, 2, 4 : le mur, le chemin, l'abonné (T appliqué) ──
        for mode in ('gratuit', 'abonne'):
            pg.evaluate("(v)=>setPremium(v)", mode == 'abonne'); pg.wait_for_timeout(400)
            for nom, pid in (('fiche_promi', 126), ('fiche_chiche', 127)):
                if mode == 'abonne' and nom == 'fiche_chiche': continue
                joue(pg, [(BASE, 200), ("()=>openDetail(%d)" % pid, 1400)])
                if mode == 'gratuit' and nom == 'fiche_promi': prise(pg, 'fiche_promi_repos_%s' % th)
                joue(pg, [(PEAUF, 1700)])
                pg.evaluate("()=>{ window.__P3.encartSeul('#detailPoster'); window.__P3.ordre('#detailPoster'); }")
                t = pg.evaluate(T_TOUS, ['#detailPoster', AIR])
                c = pg.evaluate(COTES, '#detailPoster'); pg.wait_for_timeout(500)
                prise(pg, '%s_%s_%s' % (mode, nom, th)); C['%s_%s_%s' % (mode, nom, th)] = c
                print(th, mode, nom, c and c['ordre'], [(x['champ'], x['premiere'], x['derniere'], x['air_min']) for x in t if x['lignes'] >= 3])
            for nom, steps in (('pageplus', PAGEPLUS), ('garde', [(BASE, 200), ("()=>{const d=promises.find(p=>p.draft); if(d) openDetail(d.id);}", 1800),
                                                                  ("()=>document.getElementById('csBotBar').click()", 1500)])):
                joue(pg, steps); pg.evaluate("()=>window.__P3.pose()"); pg.wait_for_timeout(900)
                n = pg.evaluate("()=>window.__P3.bandeau()")
                t = pg.evaluate(T_TOUS, ['#createSheet', AIR])
                c = pg.evaluate(COTES, '#createSheet'); pg.wait_for_timeout(500)
                prise(pg, '%s_%s_%s' % (mode, nom, th)); C['%s_%s_%s' % (mode, nom, th)] = dict(c or {}, bandeau_masques=n)
                print(th, mode, nom, 'bandeau masqué :', n, c and c['ordre'], [(x['champ'], x['premiere'], x['derniere'], x['air_min']) for x in t if x['lignes'] >= 3])
        pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        # ── section 5 : les champs à trois lignes — avant / T / P ──
        def fiche_note(long_):
            joue(pg, [(BASE, 200), ("()=>openDetail(126)", 1400), (PEAUF, 1700)])
            pg.evaluate("(t)=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[0]; if(t){ const x=z.querySelector('textarea'); x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); } z.scrollIntoView({block:'center'}); }", LONG if long_ else '')
            pg.wait_for_timeout(400)
        for cas, long_ in (('note3', False), ('note4', True)):
            for version in ('avant', 'T', 'P'):
                fiche_note(long_)
                m = pg.evaluate("(a)=>{ const c=document.querySelectorAll('#detailPoster .s2-zone')[0]; return a[0]==='T' ? window.__P3.T(c,a[1]) : a[0]==='P' ? window.__P3.Pn(c) : window.__P3.mesure(c); }", [version, AIR])
                pg.evaluate("()=>document.querySelectorAll('#detailPoster .s2-zone')[0].scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
                prise(pg, 'lignes_%s_%s_%s' % (cas, version, th)); M['%s · %s · %s' % (cas, version, th)] = m
                print(th, cas, version, m)
        for version in ('avant', 'T', 'P'):
            joue(pg, [(BASE, 200), ("()=>openEssaim('potager')", 1500), (PEAUF, 1700)])
            m = pg.evaluate("""(a)=>{ const f=(id)=>document.getElementById(id); const out={};
                ['npDesc','npComm'].forEach(id=>{ const c=f(id); out[id]= a[0]==='T' ? window.__P3.T(c,a[1]) : a[0]==='P' ? window.__P3.Pn(c) : window.__P3.mesure(c); });
                out.npFich = a[0]==='avant' ? window.__P3.mesure(f('npFich')) : window.__P3.alignePJ(f('npFich'), 23, 50.8);
                f('npDesc').scrollIntoView({block:'start'}); return out; }""", [version, AIR])
            pg.evaluate("()=>{const c=document.querySelector('#detailPoster .dpd-corps'); if(c) c.scrollTop=0;}"); pg.wait_for_timeout(300)
            prise(pg, 'lignes_nuee_%s_%s' % (version, th)); M['nuee · %s · %s' % (version, th)] = m
            print(th, 'Nuée', version, m)
        # le cas qui DÉBORDE (texte de trois lignes) : mesuré, capturé sur disque pour le chantier, pas sur la planche
        joue(pg, [(BASE, 200), ("()=>openDetail(126)", 1400), (PEAUF, 1700)])
        pg.evaluate("(t)=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[0]; const x=z.querySelector('textarea'); x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); z.scrollIntoView({block:'center'}); }", LONG5)
        pg.wait_for_timeout(400)
        M['note5 · avant · %s' % th] = m5 = pg.evaluate("()=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[0], x=z.querySelector('textarea'), r=x.getBoundingClientRect(), k=getComputedStyle(x); return Object.assign(window.__P3.mesure(z), {textarea_h:+r.height.toFixed(1), max_height:k.maxHeight, scrollH:x.scrollHeight}); }")
        prise(pg, 'deborde_note5_%s' % th); print(th, 'note5 (déborde ?)', m5)
        # la référence : le champ à deux lignes de la fiche
        joue(pg, [(BASE, 200), ("()=>openDetail(126)", 1400), (PEAUF, 1700)])
        M['reference · %s' % th] = pg.evaluate("()=>window.__P3.mesure(document.querySelector('#detailPoster .s2-reg.s2-vis2'))")
        ctx.close()
    br.close()
json.dump(C, open(os.path.join(OUT, 'cotes.json'), 'w'), ensure_ascii=False, indent=1)
json.dump(M, open(os.path.join(OUT, 'mesures.json'), 'w'), ensure_ascii=False, indent=1)
print('écrit', OUT)
