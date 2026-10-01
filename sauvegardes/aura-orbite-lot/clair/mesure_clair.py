# Q182 — le thème clair de l'Orbite, mesuré contre le thème SOMBRE (la référence validée).
# Métrique du §3 : lum = 0,2126 R + 0,7152 G + 0,0722 B. Vue figée, même vue pour tout.
#   · boule ↔ page       écart de la luminance moyenne de la boule (composée sur la page) à la page
#   · limbe ↔ page       l'anneau 0,95–1,00 R contre la page — le CONTOUR (≥ 42, seuil du §3)
#   · poil ↔ peau        p90 − p10 à l'intérieur (0,90 R) — la « dentelle »
#   · îles ↔ sol         les pixels qui changent quand on RETIRE les îles (masque) : écart moyen entre
#                        l'île et le sol qu'elle remplace — ni noyée (trop faible) ni tache (trop fort)
# Sombre : une fois. Clair : à plusieurs parts de teinte de la peau. Images sur disque.
#   python3 mesure_clair.py URL SORTIE [t1 t2 ...]
import sys, os, json
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
ILES = '--iles' in sys.argv
TS = [float(x) for x in sys.argv[3:] if x != '--iles'] or [0.0, 0.5, 0.7, 0.85, 1.0]
SNAP = r"""(nom)=>{ const cv=document.getElementById('auBoule'); window['__q_'+nom]=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data.slice(); return cv.width; }"""
MES = r"""([nom,fond,sans])=>{ const d=window['__q_'+nom], s0=sans?window['__q_'+sans]:null, W=Math.round(Math.sqrt(d.length/4)), c=W/2, R=W*0.392;
  const L=(r,g,b)=>0.2126*r+0.7152*g+0.0722*b, comp=(D,i,k)=>D[i+k]*(D[i+3]/255)+fond[k]*(1-D[i+3]/255), lum=(D,i)=>L(comp(D,i,0),comp(D,i,1),comp(D,i,2));
  const dedans=[], limbe=[]; let ni=0, di=0;
  for(let y=0;y<W;y+=2) for(let x=0;x<W;x+=2){ const r=Math.hypot(x-c,y-c)/R; if(r>1) continue; const i=(y*W+x)*4, l=lum(d,i);
    if(r<=0.90){ dedans.push(l); if(s0){ const l0=lum(s0,i); if(Math.abs(l-l0)>12){ ni++; di+=Math.abs(l-l0); } } } else if(r>=0.95) limbe.push(l); }
  dedans.sort((a,b)=>a-b); const q=(p)=>dedans[Math.floor(p*(dedans.length-1))], moy=a=>a.reduce((s,v)=>s+v,0)/a.length, pg=L(...fond);
  return {page:pg, boule:moy(dedans), limbe:moy(limbe), p10:q(0.10), p90:q(0.90), iles_px:ni, iles_ecart:ni?di/ni:null,
          boule_page:Math.abs(moy(dedans)-pg), limbe_page:Math.abs(moy(limbe)-pg), dentelle:q(0.90)-q(0.10)}; }"""
RES = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def peintes(n=6):
        p0 = pg.evaluate("()=>_aura.etat().peints")
        for _ in range(200):
            if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
            pg.wait_for_timeout(50)
    SAIN = "()=>{const e=_aura.etat(), cv=document.getElementById('auBoule'), d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; let n=0; for(let i=3;i<d.length;i+=400) if(d[i]>10) n++; return {pret:e.pret, erreur:e.erreur&&e.erreur.slice(0,300), px:n};}"
    def sain(nom):
        s = pg.evaluate(SAIN)
        if not s['pret'] or s['erreur'] or s['px'] < 500:
            print('❌  MESURE INVALIDE à « %s » : pret %s · boule peinte %d · erreur %s' % (nom, s['pret'], s['px'], s['erreur']))
            b.close(); sys.exit(2)
    def une(th, fond, t, nom, iles=False):
        if t is not None: pg.evaluate("(t)=>_aura.reglePeau(t)", t)
        peintes(); sain(nom); pg.evaluate(SNAP, nom)
        pg.query_selector('#auBoule').screenshot(path=os.path.join(OUT, '%s.png' % nom))
        if iles:     # le masque des îles EN DERNIER : il peut arrêter le peintre
            pg.evaluate("()=>_aura.sansIles(true)"); peintes(); sain(nom + ' (sans îles)'); pg.evaluate(SNAP, nom + '_nu')
            pg.evaluate("()=>_aura.sansIles(false)"); peintes()
        m = pg.evaluate(MES, [nom, fond, (nom + '_nu') if iles else None]); RES[nom] = m
        print('%-12s boule↔page %5.1f · limbe↔page %5.1f · dentelle %5.1f · îles ↔ sol %s (%d px)' % (
            nom, m['boule_page'], m['limbe_page'], m['dentelle'], m['iles_ecart'] is not None and round(m['iles_ecart'], 1), m['iles_px']))
    for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(800)
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
        if th == 'dark': une(th, fond, None, 'sombre', iles=ILES)
        else:
            for t in TS: une(th, fond, t, 'clair_%02d' % round(t * 100), iles=ILES)
            pg.evaluate("()=>_aura.reglePeau(null)")
        pg.evaluate("()=>_aura.fige(false)")
    print('ERREURS JS', er[:3]); b.close()
json.dump(RES, open(os.path.join(OUT, 'clair.json'), 'w'), indent=1)
