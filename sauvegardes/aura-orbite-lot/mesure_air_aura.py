# L'AIR DE LA COLONNE DE L'AURA, mesuré deux fois : aux BOÎTES (getBoundingClientRect, en pt d'écran
# 390) et à l'ENCRE sur l'image rendue à 2× (les lignes de pixels qui portent autre chose que le fond).
# Pour chacune des cinq phrases (une ou deux lignes) et l'état vide, deux thèmes.
#   python3 mesure_air_aura.py URL [SORTIE_DIR]
import sys, os, json, base64
from playwright.sync_api import sync_playwright
URL = sys.argv[1]; OUT = sys.argv[2] if len(sys.argv) > 2 else None
if OUT: os.makedirs(OUT, exist_ok=True)

BOITES = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const Y=(v)=>+((v-dv.top)/s).toFixed(1);
  const q=(sel)=>document.querySelector('#auraScreen '+sel);
  const r=(el)=>el?el.getBoundingClientRect():null;
  const mot=q('.au-mot'), vide=q('.au-cadre').classList.contains('au-vide');
  const out={vide:vide};
  if(!vide){
    const rg=document.createRange(); rg.selectNodeContents(mot); const L=[...rg.getClientRects()];
    const lignes=new Set(L.map(x=>Math.round(x.top))).size;
    out.mot={haut:Y(r(mot).top), bas_texte:Y(Math.max(...L.map(x=>x.bottom))), lignes:lignes, texte:mot.textContent};
    const nb=[...document.querySelectorAll('#auraScreen .au-nb')].map(e=>r(e));
    out.disques={haut:Y(Math.min(...nb.map(x=>x.top))), bas:Y(Math.max(...nb.map(x=>x.bottom)))};
    out.prenoms={bas:Y(Math.max(...[...document.querySelectorAll('#auraScreen .au-lb')].map(e=>r(e).bottom)))};
    out.legende={haut:Y(r(q('.au-lg')).top), bas:Y(r(q('.au-lg')).bottom)};
    const h3=q('.au-mo h3'); if(h3 && r(h3).height) out.tenu={haut:Y(r(h3).top), bas:Y(r(h3).bottom)};
    const bx=[...document.querySelectorAll('#auraScreen .au-bx')].map(e=>r(e)).filter(x=>x.height);
    if(bx.length) out.dalles={haut:Y(Math.min(...bx.map(x=>x.top))), bas:Y(Math.max(...bx.map(x=>x.bottom)))};
    const sp=[...document.querySelectorAll('#auraScreen .au-c span')].map(e=>r(e)).filter(x=>x.height);
    if(sp.length) out.libelles={bas:Y(Math.max(...sp.map(x=>x.bottom)))};
  } else {
    const iv=q('.au-inv'); out.inv={haut:Y(r(iv).top), bas:Y(r(iv).bottom)};
  }
  out.bouton={haut:Y(r(q('.au-bt')).top), bas:Y(r(q('.au-bt')).bottom)};
  const K=_aura.K; out.sphere_bas=+(K.bo.y+K.bo.d/2+K.bo.d*K.R).toFixed(1);
  out.ecran=844; out.defile=(()=>{const sc=document.getElementById('auraScreen'); return sc.scrollHeight>sc.clientHeight+1;})();
  return out; }"""
# l'encre : lignes de pixels (x de 24 à 366 pt) où au moins 2 pixels s'écartent du fond de plus de 14
ENCRE = r"""async ([u,fond])=>{ const im=new Image(); im.src=u; await im.decode();
  const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; const g=c.getContext('2d'); g.drawImage(im,0,0);
  const d=g.getImageData(0,0,c.width,c.height).data, W=c.width, s=W/390, x0=Math.round(24*s), x1=Math.round(366*s);
  const rows=[]; for(let y=0;y<c.height;y++){ let n=0; for(let x=x0;x<x1;x+=1){ const i=(y*W+x)*4;
      if(Math.abs(d[i]-fond[0])+Math.abs(d[i+1]-fond[1])+Math.abs(d[i+2]-fond[2])>42){ if(++n>=2) break; } } rows.push(n>=2); }
  const runs=[]; let a=-1; for(let y=0;y<=rows.length;y++){ const v=y<rows.length&&rows[y];
    if(v&&a<0) a=y; if(!v&&a>=0){ runs.push([+(a/s).toFixed(1), +(y/s).toFixed(1)]); a=-1; } }
  return runs; }"""

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(URL); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th, fond in (('dark', [22, 23, 27]), ('light', [244, 238, 225])):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(400)
        pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
        pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
        pg.wait_for_timeout(600)
        mots = pg.evaluate("()=>window._aura&&_aura.MOTS?_aura.MOTS.length:5")
        for i in list(range(mots)) + ['vide']:
            if i == 'vide':
                pg.evaluate("()=>{window.__d=promises.map(p=>[p,p.draft]);promises.forEach(p=>{p.draft=true;});}")
                pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
                pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(2500)
            else:
                # la phrase i : par l'API du juge si elle existe (elle recompose), sinon posée dans le nœud
                pg.evaluate("""(i)=>{ if(_aura.mot) _aura.mot(i); else { const L=['Rien de ce qui est ici n’a été dit à la légère.',
                  'Tout ça, tu l’as dit. Et tu l’as fait.','On ne dirait pas comme ça, mais c’est du solide.',
                  'Il y en a, des paroles tenues.','Et dire que tout ça, c’est toi.'];
                  document.querySelector('#auraScreen .au-mot').textContent=L[i]; } }""", i)
                pg.wait_for_timeout(400)
            bx = pg.evaluate(BOITES)
            png = pg.query_selector('#device').screenshot()
            if OUT: open(os.path.join(OUT, 'air_%s_%s.png' % (th, i)), 'wb').write(png)
            runs = pg.evaluate(ENCRE, ['data:image/png;base64,' + base64.b64encode(png).decode(), fond])
            res['%s %s' % (th, i)] = dict(boites=bx, encre=runs)
            if i == 'vide':
                pg.evaluate("()=>{(window.__d||[]).forEach(x=>{x[0].draft=x[1];});}")
    b.close()

def gaps(bx):
    if bx['vide']:
        return [('sphère → invitation', bx['inv']['haut'] - bx['sphere_bas']), ('invitation → bouton', bx['bouton']['haut'] - bx['inv']['bas']),
                ('bouton → bas de l\'écran', 844 - bx['bouton']['bas'])]
    G = [('sphère → phrase', bx['mot']['haut'] - bx['sphere_bas']),
         ('PHRASE → DISQUES', bx['disques']['haut'] - bx['mot']['bas_texte']),
         ('prénoms → légende', bx['legende']['haut'] - bx['prenoms']['bas'])]
    if 'tenu' in bx: G.append(('légende → « ce que tu as tenu »', bx['tenu']['haut'] - bx['legende']['bas']))
    if 'libelles' in bx: G.append(('LIBELLÉS DES DALLES → BOUTON', bx['bouton']['haut'] - bx['libelles']['bas']))
    G.append(('bouton → bas de l\'écran', 844 - bx['bouton']['bas']))
    return G
for k, v in res.items():
    bx = v['boites']
    print('\n%s%s' % (k, '' if bx['vide'] else ' · « %s » · %d ligne(s)' % (bx['mot']['texte'], bx['mot']['lignes'])) + (' · DÉFILE' if bx['defile'] else ''))
    for n, g in gaps(bx): print('   %-34s %6.1f pt' % (n, g))
    print('   encre (pt, haut → bas) :', ' '.join('%s–%s' % tuple(r) for r in v['encre'] if r[0] > 330))
json.dump(res, open((OUT or '.') + '/air_aura.json', 'w'), indent=1, ensure_ascii=False)
