import io, sys
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL = 'http://127.0.0.1:8752/' + (sys.argv[1] if len(sys.argv) > 1 else 'app.html')
TH = sys.argv[2] if len(sys.argv) > 2 else 'light'
GEO = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, f=document.getElementById('onbFin'); if(!f) return null; const fr=f.getBoundingClientRect();
  const vis=[...f.querySelectorAll('.onbv-titre,.onbv-ton,.onbv-l')].filter(e=>getComputedStyle(e).visibility!=='hidden'); let bas=0; vis.forEach(e=>{ bas=Math.max(bas,(e.getBoundingClientRect().bottom-D.top)/k); });
  /* les dalles lues SUR L'IMAGE du canevas de la Toile : la première ligne (de haut en bas) qui porte un pixel bleu de la parole ou crème des voisines, sous le texte */
  const cv=document.getElementById('toileCv'), g=cv.getContext('2d'), W=cv.width, H=cv.height, d=g.getImageData(0,0,W,H).data, sy=H/844; let haut=null;
  for(let y=Math.round(bas+2); y<844 && haut===null; y+=2){ for(let x=10; x<380; x+=4){ const q=((Math.round(y*sy))*W+Math.round(x*W/390))*4; const r=d[q],gg=d[q+1],b=d[q+2]; if((b>200&&r<170)||(r>235&&gg>225&&b>200)){ haut=y; break; } } }
  return {top:Math.round((fr.top-D.top)/k), basTexte:Math.round(bas), dallesHaut:haut, ecart:haut!=null?haut-Math.round(bas):null, vus:vis.length, pas:(window._onbFinPas&&_onbFinPas())}; }"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True)
    if TH == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
    pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
    prenom(pg, cdp); pg.wait_for_timeout(2500); parole(pg); saisie(pg); pg.wait_for_timeout(600)
    trace(pg, cdp); pg.wait_for_timeout(5200); d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
    ims = []
    print('vue', pg.evaluate("()=>{ const L=Toile_lecture(); const p=promises[promises.length-1]; const g=L.graines.find(x=>x.pid===p.id); return {vue:L.vue, cible:L.cible, W:L.W, H:L.H, graine:g}; }"))
    print('départ', pg.evaluate(GEO)); ims.append(Image.open(io.BytesIO(pg.screenshot())))
    for i in range(3):
        toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(5500)
        print('toucher', i + 1, pg.evaluate(GEO)); print('   vue', pg.evaluate("()=>{ const L=Toile_lecture(); const p=promises[promises.length-1]; const g=L.graines.find(x=>x.pid===p.id); return [L.vue.s, L.vue.oy, L.cible&&L.cible.oy, g.y, g.y*L.vue.s+L.vue.oy]; }")); ims.append(Image.open(io.BytesIO(pg.screenshot())))
    pg.wait_for_timeout(1500); toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(250); ims.append(Image.open(io.BytesIO(pg.screenshot()))); print('apres', pg.evaluate("()=>{ const c=document.getElementById('toileCv'); const s=getComputedStyle(c); const v=document.getElementById('onbV'); return [s.visibility, s.opacity, s.display, document.getElementById('device').className, [...v.children].map(e=>e.className+':'+getComputedStyle(e).display+':'+Math.round(e.getBoundingClientRect().height)).join(' | ').slice(0,600), Toile_lecture().graines.filter(g=>g.kind!=='gray').length, (function(){ const L=Toile_lecture(); const g=L.graines.find(x=>x.kind!=='gray'); return [L.vue, L.cible, g&&g.y, g&&(g.y*L.vue.s+L.vue.oy)]; })()]; }")); pg.wait_for_timeout(1500); ims.append(Image.open(io.BytesIO(pg.screenshot())))
    print('compte', pg.evaluate("()=>{ const c=document.querySelector('.onbv-compte'); if(!c) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=c.getBoundingClientRect(); return [Math.round((r.top-D.top)/k), Math.round(r.height/k), getComputedStyle(c).backgroundColor]; }"))
    w, h = ims[0].size; o = Image.new('RGB', (w * len(ims) + 20 * len(ims), h), (255, 255, 255))
    for i, im in enumerate(ims): o.paste(im, (i * (w + 20), 0))
    o = o.resize((o.width // 3, o.height // 3)); o.save('scratchpad/v148/fin_%s.png' % TH)
    b.close()
