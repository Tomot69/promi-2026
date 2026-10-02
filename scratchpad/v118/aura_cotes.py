# aura_cotes.py [fichier] — l'Aura, deux thèmes : les cotes de la colonne (points d'appareil) et l'air À L'ENCRE sur l'image rendue
import sys, io, os
sys.path.insert(0, 'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'; S = 2
J = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, o={};
  const q={ombre:'#auPeloteOmbre', echo:'#auPeloteEcho', boule:'#auBoule', bouton:'#auPartage', phrase:'.au-mot', noyaux:'.au-nx', legende:'.au-lg', chiffres:'.au-cpt', tenu:'.au-mo', tenuTitre:'.au-mo h3', invite:'.au-inv'};
  for(const n in q){ const e=document.querySelector('#auraScreen '+q[n]); if(!e||getComputedStyle(e).display==='none'){ o[n]=null; continue; } const r=e.getBoundingClientRect();
    o[n]={x:+((r.left-dv.left)/k).toFixed(2), y:+((r.top-dv.top)/k).toFixed(2), w:+(r.width/k).toFixed(2), h:+(r.height/k).toFixed(2), b:+((r.bottom-dv.top)/k).toFixed(2)}; }
  const e=document.getElementById('auPeloteEcho'); o.echoTon=e?getComputedStyle(e).backgroundColor:null; o.pal=Toile.getPalette(); o.sol=_aura.sol().idx; return o; }"""
def encre(im, y0, y1, x0=40, x1=350):
    """première et dernière rangée (points) qui portent autre chose que le fond, entre y0 et y1"""
    px = im.load(); fond = px[int(8*S), int(((y0+y1)/2)*S)]; rows = []
    for y in range(int(y0*S), int(y1*S)):
        if any(sum(abs(px[x, y][c]-fond[c]) for c in range(3)) > 60 for x in range(int(x0*S), int(x1*S), 2)): rows.append(y/S)
    return (rows[0], rows[-1] + 1/S) if rows else (None, None)
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=S)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(7000)
    for d in (0, 1):
        ouvre(pg, d); pg.evaluate("()=>{_aura.fige(true)}"); pg.wait_for_timeout(600)
        o = pg.evaluate(J); nom = 'sombre' if d else 'clair'
        im = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB')
        im.save('scratchpad/v118/aura-%s.png' % nom)
        print('──', nom, '· palette', o['pal'], '· sol', o['sol'], '· écho', o['echoTon'])
        for n in ('boule','echo','ombre','bouton','phrase','noyaux','legende','chiffres','tenuTitre'):
            v = o[n]; print('  %-10s %s' % (n, 'absent' if not v else 'y %.2f → %.2f   x %.2f l %.2f h %.2f' % (v['y'], v['b'], v['x'], v['w'], v['h'])))
        if o['ombre'] and o['bouton']:
            print('  G2 ombre → bouton : %.2f' % (o['bouton']['y'] - o['ombre']['b']), '· bas du bouton %.2f (pli 844)' % o['bouton']['b'])
        if o['phrase']:
            a, z = encre(im, o['phrase']['y']-12, o['phrase']['b']+6)
            print('  encre de la phrase : %.1f → %.1f · bouton → encre : %.2f' % (a, z, a - o['bouton']['b']))
        # sous le pli : on fait défiler la colonne de 300 et on mesure l'air À L'ENCRE autour du groupe « légende + chiffres »
        pg.evaluate("()=>{document.getElementById('auCadre').scrollTop=300}"); pg.wait_for_timeout(500)
        dy = pg.evaluate("()=>document.getElementById('auCadre').scrollTop")
        im2 = Image.open(io.BytesIO(pg.screenshot(clip={'x':20,'y':44,'width':390,'height':844}))).convert('RGB'); im2.save('scratchpad/v118/aura-%s-bas.png' % nom)
        if o['noyaux'] and o['tenuTitre']:
            n0, n1 = encre(im2, o['noyaux']['y']-dy, o['noyaux']['b']-dy+4); l0, l1 = encre(im2, o['legende']['y']-dy-4, o['legende']['b']-dy+4)
            c0, c1 = encre(im2, o['chiffres']['y']-dy-2, o['chiffres']['b']-dy+2); t0, t1 = encre(im2, o['tenuTitre']['y']-dy-6, o['tenuTitre']['b']-dy+4)
            print('  à l\'encre (défilé de %d) : noyaux → légende %.1f · légende → chiffres %.1f · chiffres → « Ce que tu as tenu » %.1f' % (dy, l0-n1, c0-l1, t0-c1))
        pg.evaluate("()=>{document.getElementById('auCadre').scrollTop=0}")
        pg.evaluate("()=>{_aura.fige(false)}")
        pg.evaluate("()=>{const x=document.querySelector('#auraScreen .closeb'); if(x) x.click();}"); pg.wait_for_timeout(900)
    print('pageerror :', er or 'aucune'); b.close()
