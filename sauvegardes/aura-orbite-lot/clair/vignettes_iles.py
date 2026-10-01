# Regarder chaque île RÉELLE à la vue de mesure (2,9 · 0,32), avec et sans îles, dans les deux thèmes :
# une vignette par île, côte à côte « avec | sans », composée sur le fond de la page. Et ce qu'est la dalle :
# le Promi, son monde, la part de pixels peints de sa dalle (un monde clairsemé laisse passer le sol).
#   python3 vignettes_iles.py URL DOSSIER
import sys, os, json, base64, io
from PIL import Image
from playwright.sync_api import sync_playwright
URL, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
POS = r"""()=>{ const cv=document.getElementById('auBoule'), W=cv.width, c=W/2, R=W*0.392, e=_aura.etat();
  const B=OrbiteMoteur.batIles(_auraComp.n, Toile.cols(), {palette:Toile.getPalette(), dalle:function(){return null;}});
  const cl=Math.cos(e.lac), sl=Math.sin(e.lac), ct=Math.cos(e.tan), st=Math.sin(e.tan);
  return B.iles.map((I,k)=>{ const o=I.c, X=o[0]*cl+o[2]*sl, zp=-o[0]*sl+o[2]*cl, Y=o[1]*ct-zp*st, Z=o[1]*st+zp*ct;
    return {k:k, x:c+X*R, y:c+Y*R, z:Z, r:I.r*R}; }); }"""
QUI = r"""()=>(_auraComp.iles||[]).map(x=>({pid:x.pid, titre:x.titre, monde:x.monde&&(x.monde.m||JSON.stringify(x.monde))}))"""
DALLE = r"""()=>{ const out=[]; for(const x of (_auraComp.iles||[])){ try{ const cv=document.createElement('canvas'); cv.width=160; cv.height=160;
    Toile.dalleTrame(cv, x.pid, 1, x.monde); const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; let n=0,p=0;
    for(let i=3;i<d.length;i+=4){ n++; if(d[i]>24) p++; } out.push(+(p/n).toFixed(2)); }catch(err){ out.push('err '+err.message); } } return out; }"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def peintes(n=8):
        p0 = pg.evaluate("()=>_aura.etat().peints")
        for _ in range(300):
            if pg.evaluate("()=>_aura.etat().peints") >= p0 + n: return
            pg.wait_for_timeout(50)
    def image():
        u = pg.evaluate("()=>document.getElementById('auBoule').toDataURL('image/png')")
        return Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGBA')
    for th, fond in (('dark', (22, 23, 27)), ('light', (244, 238, 225))):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(600)
        pg.evaluate("()=>{_aura.relisse(); _aura.fige(true); _aura.vue(2.9,0.32);}"); peintes()
        avec = image(); pos = pg.evaluate(POS)
        pg.evaluate("()=>_aura.sansIles(true)"); peintes(); sans = image()
        pg.evaluate("()=>_aura.sansIles(false)"); peintes(4); pg.evaluate("()=>_aura.fige(false)")
        qui = pg.evaluate(QUI); part = pg.evaluate(DALLE)
        def sur_fond(im):
            f = Image.new('RGBA', im.size, fond + (255,)); f.alpha_composite(im); return f.convert('RGB')
        A, S = sur_fond(avec), sur_fond(sans); A.save(os.path.join(OUT, th + '-boule-avec.png'))
        planche = Image.new('RGB', (2 * 260 + 10, len(pos) * 270), fond)
        for i, I in enumerate(pos):
            h = max(70, int(I['r'] * 1.6))
            box = (int(I['x'] - h), int(I['y'] - h), int(I['x'] + h), int(I['y'] + h))
            planche.paste(A.crop(box).resize((260, 260)), (0, i * 270)); planche.paste(S.crop(box).resize((260, 260)), (270, i * 270))
            q = qui[i] if i < len(qui) else {}
            print('%-5s île %d  z %.2f  %-28s monde %-10s part peinte de la dalle %s' % (th, I['k'], I['z'], (q.get('titre') or '')[:28], q.get('monde'), part[i] if i < len(part) else '?'))
        planche.save(os.path.join(OUT, th + '-iles-avec-sans.png'))
    b.close()
print('vignettes dans', OUT)
