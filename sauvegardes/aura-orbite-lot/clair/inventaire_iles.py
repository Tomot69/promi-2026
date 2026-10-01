# Les îles RÉELLES, pas celles que le masque veut bien voir (Tom : « ton filtre à 300 cellules, dis-moi ce
# qu'il écarte » ; « un plancher absolu »). Pour chaque dalle du jeu de démonstration, sur plusieurs
# chargements (les couleurs sont tirées au hasard) et dans les deux thèmes, à la vue de mesure (2,9 · 0,32) :
#   · son centre projeté (le moteur exporté recalcule les îles ; vérifié contre `_auraComp.derniere`)
#   · si elle est de face (z > 0,35), la composante du masque qui la contient : son AIRE et son CONTRASTE
#   · ou son ABSENCE du masque (contraste < 12 partout : illisible, et jamais mesurée)
#   python3 inventaire_iles.py URL [chargements]
import sys, os
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
SNAP = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__i_'+nom]=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); return cv.width; }"""
INV = r"""([fond])=>{ const cv=document.getElementById('auBoule'), W=cv.width, d=window.__i_avec, s0=window.__i_sans, c=W/2, R=W*0.392;
  const L=(r,g,b)=>0.2126*r+0.7152*g+0.0722*b, comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255), lum=(D,i)=>L(comp(D,i,0),comp(D,i,1),comp(D,i,2));
  const S=2, G=Math.ceil(W/S), M=new Float32Array(G*G).fill(-1);
  for(let y=0;y<W;y+=S) for(let x=0;x<W;x+=S){ if(Math.hypot(x-c,y-c)/R>0.90) continue; const i=(y*W+x)*4, e=Math.abs(lum(d,i)-lum(s0,i)); if(e>12) M[(y/S)*G+(x/S)]=e; }
  const lab=new Int32Array(G*G).fill(-1), comps=[];
  for(let k=0;k<G*G;k++){ if(M[k]<0||lab[k]>=0) continue; const id=comps.length; let pile=[k], n=0, s=0; lab[k]=id;
    while(pile.length){ const q=pile.pop(); n++; s+=M[q]; const qx=q%G, qy=(q/G)|0;
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const nx=qx+dx, ny=qy+dy; if(nx<0||ny<0||nx>=G||ny>=G) continue; const z=ny*G+nx;
        if(M[z]>=0&&lab[z]<0){ lab[z]=id; pile.push(z); } } }
    comps.push({n:n, ecart:s/n}); }
  // les îles du moteur, recalculées, projetées à la vue courante (x à droite, y en bas, z vers nous)
  const e=_aura.etat(), n=_auraComp.n, B=OrbiteMoteur.batIles(n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan), der=_auraComp.derniere;
  const verif = der && B.derniere ? Math.hypot(der[0]-B.derniere[0], der[1]-B.derniere[1], der[2]-B.derniere[2]) : null;
  const iles=B.iles.map((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct;
    const px=c+X*R, py=c+Y*R, g=((py/S)|0)*G+((px/S)|0);
    // la composante sous le centre, ou la plus proche dans un rayon de 12 cellules
    let id=(g>=0&&g<G*G)?lab[g]:-1;
    if(id<0){ let best=1e9; for(let dy=-12;dy<=12;dy++) for(let dx=-12;dx<=12;dx++){ const z=g+dy*G+dx; if(z>=0&&z<G*G&&lab[z]>=0){ const dd=dx*dx+dy*dy; if(dd<best){best=dd; id=lab[z];} } } }
    return {k:k, z:+Z.toFixed(2), face:Z>0.35, aire:id>=0?comps[id].n:0, ecart:id>=0?+comps[id].ecart.toFixed(1):null, comp:id}; });
  const pris=new Set(iles.filter(x=>x.comp>=0).map(x=>x.comp));
  const bruit=comps.map((c0,i)=>({i:i,n:c0.n})).filter(x=>!pris.has(x.i)).map(x=>x.n).sort((a,b)=>b-a).slice(0,6);
  return {verif:verif, iles:iles, bruit:bruit}; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for ch in range(1, K + 1):
        pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        def peintes(n=8):
            p0 = pg.evaluate("()=>_aura.etat().peints")
            for _ in range(300):
                if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
                pg.wait_for_timeout(50)
        for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
            pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
            for _ in range(80):
                pg.wait_for_timeout(250)
                if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
            pg.wait_for_timeout(600)
            pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
            err = pg.evaluate("()=>_aura.etat().erreur")
            if err: print('❌ erreur du peintre', err[:160]); sys.exit(2)
            pg.evaluate(SNAP, 'avec'); pg.evaluate("()=>_aura.sansIles(true)"); peintes(); pg.evaluate(SNAP, 'sans')
            pg.evaluate("()=>_aura.sansIles(false)"); peintes(4)
            r = pg.evaluate(INV, [fond]); pg.evaluate("()=>_aura.fige(false)")
            print('chargement %d · %-5s · positions vérifiées (écart à derniere %s)' % (ch, th, r['verif'] is not None and round(r['verif'], 4)))
            for I in r['iles']:
                etat = ('ABSENTE du masque — illisible, jamais mesurée' if I['face'] and I['aire'] == 0 else
                        ('de dos / au limbe' if not I['face'] else 'aire %4d cellules%s · contraste %5.1f%s' % (
                            I['aire'], ' (SOUS 300 : écartée par le filtre)' if I['aire'] < 300 else '', I['ecart'], '  ⚠ sous 42' if I['ecart'] < 42 else '')))
                print('   île %d  z %5.2f  %s' % (I['k'], I['z'], etat))
            print('   composantes hors îles (bruit), les plus grandes :', r['bruit'])
        pg.close()
    b.close()
