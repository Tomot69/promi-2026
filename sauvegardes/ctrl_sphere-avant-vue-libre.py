#!/usr/bin/env python3
"""LE CONTRÔLE DE LA SPHÈRE.

La masse est un CANEVAS qui couvre 352 × 352 : au test boîte-contre-boîte elle
recouvre TOUT, et l'exempter en bloc serait le crible en bloc que le projet
s'interdit. On l'exempte donc du test de BOÎTES — qui ne veut rien dire pour une
surface de points — et on met à la place une mesure de PIXELS, plus dure :

  1 · combien de points la masse pose-t-elle DANS la boîte d'un prénom ?
      (la clairière doit les avoir retirés)
  2 · combien en pose-t-elle DEVANT un anneau ?
      (« toujours nets » : la matière s'allège, elle ne salit pas)

Preuve que la mesure mord : on coupe la clairière et on recompte.
"""
import sys, json
from playwright.sync_api import sync_playwright
CIBLE = sys.argv[1] if len(sys.argv)>1 else 'PLANCHE-AURA-SPHERE.html'

PIX = r"""(fi)=>{
  const f=document.querySelectorAll('.fr')[fi];
  const F=f.getBoundingClientRect();
  const cvs=[...f.querySelectorAll('canvas[data-role=masse]')];
  if(!cvs.length) return null;
  const ctx=cvs.map(c=>c.getContext('2d'));
  const rect=cvs[0].getBoundingClientRect();
  const ox=rect.left-F.left, oy=rect.top-F.top, D=cvs[0].width/rect.width;
  // combien de points opaques dans un rectangle donné en coordonnées de cadre
  const compte=(x,y,w,h,slabs)=>{
    let n=0, tot=0;
    const X=Math.round((x-ox)*D), Y=Math.round((y-oy)*D);
    const W=Math.round(w*D), H=Math.round(h*D);
    if(W<=0||H<=0) return {n:0,tot:0};
    // ⚠ ON MESURE L'ENCRE DÉPOSÉE, PAS UN NOMBRE DE PIXELS ALLUMÉS.
    // La clairière n'efface pas à 100 % (0,88) : un point à 0,94 d'opacité en garde
    // 0,11 — au-dessus de n'importe quel seuil de comptage, alors qu'il ne se voit
    // plus. Compter des pixels donnait « 6,5 % avec clairière » et « 4,9 % sans » :
    // la mesure ne mesurait rien. La SOMME DES ALPHAS, elle, tombe d'un facteur huit.
    for(const k of slabs){
      const d=ctx[k].getImageData(X,Y,W,H).data;
      for(let i=3;i<d.length;i+=4) n += d[i];
      tot += W*H*255;
    }
    return {n:n, tot:W*H*255};
  };
  const tous=[...cvs.keys()];
  const out={noms:[], anneaux:[]};
  f.querySelectorAll('.orb').forEach(w=>{
    if(!w.__pos||!w.__nom) return;
    // LE MOT, pas la boîte : « Léa » n'occupe pas les 62 px de son bloc.
    const lg=w.__nom.__lg||58;
    const c=compte(w.__pos.x+(62-lg)/2, w.__pos.y+1, lg, 16, tous);
    out.noms.push({qui:w.dataset.qui, points:c.n, boite:c.tot});
  });
  f.querySelectorAll('.orb').forEach(w=>{
    if(!w.__pr) return;
    const d=w.__d, x=195+w.__pr.x-d/2, y=272+w.__pr.y-d/2;
    // seulement les tranches VRAIMENT devant la personne
    const devant=[...cvs.keys()].filter(k=>f.__masZ[k] > w.__z);
    const c=compte(x,y,d,d,devant);
    out.anneaux.push({qui:w.dataset.qui, tranches:devant.length,
                      points:c.n, boite:c.tot,
                      part:c.tot? +(100*c.n/c.tot).toFixed(1):0});
  });
  return out;
}"""
HORS = r"""(fi)=>{
  const f=document.querySelectorAll('.fr')[fi], F=f.getBoundingClientRect(), out=[];
  f.querySelectorAll('*').forEach(n=>{const cs=getComputedStyle(n),r=n.getBoundingClientRect();
    if(cs.display==='none'||r.width<1)return;
    if(r.left<F.left-0.5||r.right>F.right+0.5||r.top<F.top-0.5||r.bottom>F.bottom+0.5)
      out.push(fi+' :: '+(n.className||n.tagName)+' « '+(n.textContent||'').trim().slice(0,22)+' » x'
        +Math.round(r.left-F.left)+'→'+Math.round(r.right-F.left)
        +' / y'+Math.round(r.top-F.top)+'→'+Math.round(r.bottom-F.top));});
  return out;}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1800,'height':1400}, device_scale_factor=2)
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:8752/'+CIBLE)
    pg.wait_for_function("()=>window.__pret===true", timeout=120000)
    pg.wait_for_timeout(2500)
    pg.evaluate("()=>{window.__fige=true;}"); pg.wait_for_timeout(250)
    pg.evaluate("()=>{window._nomsALaCible&&window._nomsALaCible();}"); pg.wait_for_timeout(150)
    print('erreurs de page :', errs[:3])
    figs=pg.query_selector_all('figure')
    hors=[]
    for i,fg in enumerate(figs):
        fg.query_selector('.fr').scroll_into_view_if_needed(); pg.wait_for_timeout(140)
        hors += pg.evaluate(HORS, i)
    print('── HORS CADRE :', len(hors))
    for h in hors[:12]: print('   ', h)
    r=pg.evaluate(PIX, 0)
    av={}
    print('\n── L’ENCRE DE LA MASSE SOUS LE MOT (quatre tranches)')
    for n in r['noms']:
        v=100*n['points']/(n['boite']*4)
        print('   %-8s encre %6.3f %%   %s' % (n['qui'], v, 'lisible' if v<=1.0 else '⚠ AU-DESSUS DE 1 %'))
        av[n['qui']]=100*n['points']/(n['boite']*4)
    print('\n── L’ENCRE DE LA MASSE DEVANT UN ANNEAU (seulement les tranches devant lui)')
    for n in r['anneaux']:
        print('   %-8s %d tranche(s) devant · encre %5.2f %% de sa boîte'
              % (n['qui'], n['tranches'], n['part']))
    v=pg.evaluate("()=>window._verifOrbite()")
    print('\n── AUCUN ANNEAU *DEVANT* TON NOYAU (72 positions) :', v['total'], 'écart(s)')
    print('── LES SIX SONT-ILS DEDANS ? silhouette %s · enveloppe %s · sorties %d/432'
          % (v['silhouette'], v['enveloppe'], v['dehors']))
    print('── LA PROFONDEUR : %s → %s px · rapport %s' % (v['petit'], v['gros'], v['rapport']))
    print('   la boîte de l’orbite sur un tour : %s' % v['boite'])
    # ── LA PREUVE QUE LA MESURE MORD : on coupe la clairière et on REJOUE
    #    LA MÊME PHASE. Rejouer une autre phase ne prouverait rien : les prénoms
    #    auraient bougé, et on comparerait deux écrans différents.
    pg.evaluate("()=>{window.__sansClairiere=true;"
                "document.querySelectorAll('.fr').forEach(function(f){ if(f.__masG) orbitePose(f,f.__u); });}")
    pg.wait_for_timeout(250)
    r2=pg.evaluate(PIX, 0)
    print('\n── PREUVE : la MÊME phase, CLAIRIÈRE COUPÉE')
    # LE CRITÈRE EST ABSOLU : sous le mot, l'encre de la masse doit rester ≤ 1 %.
    # Un critère RELATIF (« elle doit tripler ») ne veut rien dire là où la sphère
    # est déjà creuse : « Maman » tombait dans un vide, l'encre locale valait 1,35 %
    # sans clairière — et le contrôle criait au faux négatif.
    pris=0
    for n2 in r2['noms']:
        ap=100*n2['points']/(n2['boite']*4); base=av.get(n2['qui'],0.0)
        d = ap>1.0
        pris += 1 if d else 0
        print('   %-8s %5.2f %%  →  %5.2f %%   %s' % (n2['qui'], base, ap, 'PRIS' if d else '(zone creuse)'))
    print('   la mesure mord : %s — %d prénom(s) sur 6 passent au-dessus de 1 %%'
          % ('OUI' if pris else 'NON', pris))
    b.close()
