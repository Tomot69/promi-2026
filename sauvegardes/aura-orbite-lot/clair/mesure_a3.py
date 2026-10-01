# Q182 — trois voies du thème clair, mesurées côte à côte contre le SOMBRE (Tom : « ta version d'abord ;
# si ça ne tient pas, inverse le poil ; si ça ne tient toujours pas, la 2 »). Cible : l'écart boule ↔ page
# du sombre. Métrique du §3 (0,2126 R + 0,7152 G + 0,0722 B). Vue figée, même angle pour tout.
#   A · ta version      poil = couleur de nature,           peau → teinte claire §1.2 (100 %)
#   B · poil inversé    poil = corps sombre de nature §1.3,  peau → teinte claire §1.2 (100 %)
#   C · la « 2 »        poil = teinte claire §1.2,           peau = celle du peintre (le poil assombri)
# Pour chaque voie : boule ↔ page, contour (limbe ↔ page), dentelle (p90 − p10), et les ÎLES une à une —
# le masque = ce qui change quand on retire les îles (trame vide), découpé en composantes : on rend la
# plus faible et la médiane. L'instrument s'arrête s'il mesure du vide (erreur, boule non peinte).
#   python3 mesure_q182.py URL SORTIE
import sys, os, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
NATURE_CLAIRE = [0xCB, 0xAA, 0xFF]     # Promi, §1.2
NATURE_SOMBRE = [0x12, 0x14, 0x2A]     # Promi, §1.3 (corps sombre de la fiche)
SNAP = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__q_'+nom]=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); return cv.width; }"""
MES = r"""([nom,fond,sans])=>{ const d=window['__q_'+nom], s0=window['__q_'+sans], W=Math.round(Math.sqrt(d.length/4)), c=W/2, R=W*0.392;
  const L=(r,g,b)=>0.2126*r+0.7152*g+0.0722*b, comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255), lum=(D,i)=>L(comp(D,i,0),comp(D,i,1),comp(D,i,2));
  const dedans=[], limbe=[], S=2, G=Math.ceil(W/S), M=new Float32Array(G*G).fill(-1);
  for(let y=0;y<W;y+=S) for(let x=0;x<W;x+=S){ const r=Math.hypot(x-c,y-c)/R; if(r>1) continue; const i=(y*W+x)*4, l=lum(d,i);
    if(r<=0.90){ dedans.push(l); const e=Math.abs(l-lum(s0,i)); if(e>12) M[(y/S)*G+(x/S)]=e; } else if(r>=0.95) limbe.push(l); }
  // les îles une à une : composantes 4-connexes du masque (au moins 40 cellules)
  const vu=new Uint8Array(G*G), iles=[];
  for(let k=0;k<G*G;k++){ if(M[k]<0||vu[k]) continue; let pile=[k], n=0, s=0; vu[k]=1;
    while(pile.length){ const q=pile.pop(); n++; s+=M[q]; const qx=q%G, qy=(q/G)|0;
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const nx=qx+dx, ny=qy+dy; if(nx<0||ny<0||nx>=G||ny>=G) continue; const z=ny*G+nx;
        if(M[z]>=0&&!vu[z]){ vu[z]=1; pile.push(z); } } }
    if(n>=40) iles.push({n:n, ecart:s/n}); }
  iles.sort((a,b)=>a.ecart-b.ecart);
  dedans.sort((a,b)=>a-b); const q=(p)=>dedans[Math.floor(p*(dedans.length-1))], moy=a=>a.reduce((s,v)=>s+v,0)/a.length, pg=L(...fond);
  return {boule_page:Math.abs(moy(dedans)-pg), limbe_page:Math.abs(moy(limbe)-pg), dentelle:q(0.90)-q(0.10),
          iles:iles.map(x=>[x.n, +x.ecart.toFixed(1)]), ile_min:iles.length?iles[0].ecart:null,
          ile_med:iles.length?iles[iles.length>>1].ecart:null}; }"""
SAIN = "()=>{const e=_aura.etat(), cv=document.getElementById('auBoule'), d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; let n=0; for(let i=3;i<d.length;i+=400) if(d[i]>10) n++; return {pret:e.pret, erreur:e.erreur&&e.erreur.slice(0,300), px:n};}"
VOIES = [('A', None, None, 1.0), ('A1_peau_30pc_creme', None, [215, 190, 246], 1.0), ('A2_peau_60pc_creme', None, [228, 211, 237], 1.0), ('A3_poil_15pc_plus_clair', [80, 97, 255], None, 1.0)]
RES = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def peintes(n=8):
        p0 = pg.evaluate("()=>_aura.etat().peints")
        for _ in range(300):
            if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
            pg.wait_for_timeout(50)
    def sain(nom):
        s = pg.evaluate(SAIN)
        if not s['pret'] or s['erreur'] or s['px'] < 500:
            print('❌  MESURE INVALIDE à « %s » : pret %s · boule peinte %d · erreur %s' % (nom, s['pret'], s['px'], s['erreur'])); b.close(); sys.exit(2)
    def une(nom, fond):
        pg.evaluate("()=>_aura.sansIles(false)"); peintes(); sain(nom); pg.evaluate(SNAP, nom)
        pg.query_selector('#auBoule').screenshot(path=os.path.join(OUT, nom + '.png'))
        pg.evaluate("()=>_aura.sansIles(true)"); peintes(); sain(nom + ' (sans îles)'); pg.evaluate(SNAP, nom + '_nu')
        pg.evaluate("()=>_aura.sansIles(false)"); peintes()
        m = pg.evaluate(MES, [nom, fond, nom + '_nu']); RES[nom] = m
        print('%-16s boule↔page %5.1f · contour %5.1f · dentelle %5.1f · îles : la plus faible %s, médiane %s (%d îles %s)' % (
            nom, m['boule_page'], m['limbe_page'], m['dentelle'], m['ile_min'] and round(m['ile_min'], 1), m['ile_med'] and round(m['ile_med'], 1), len(m['iles']), m['iles']))
    def ouvre(th):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(800)
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
    ouvre('dark'); une('sombre', [22, 23, 27])
    ouvre('light')
    for nom, sol, peauc, t in VOIES:
        pg.evaluate("(c)=>_aura.regleSol(c)", sol); pg.evaluate("(c)=>_aura.reglePeauC(c)", peauc); pg.evaluate("(t)=>_aura.reglePeau(t)", t)
        une(nom, [244, 238, 225])
    pg.evaluate("()=>{_aura.regleSol(null); _aura.reglePeauC(null); _aura.reglePeau(null); _aura.fige(false);}")
    b.close()
json.dump(RES, open(os.path.join(OUT, 'a3.json'), 'w'), indent=1)
