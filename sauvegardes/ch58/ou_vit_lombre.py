# CHANTIER 58 · OÙ L'OMBRE VIT ENCORE — et bouge-t-elle toujours après la correction ?
# Le `::before` de `.tuto-fond` est masqué écran par écran, PAR DÉCISION (page + et Réglages : « on le
# remplace par un canvas qui porte la VRAIE dalle du monde actif » ; Aura, Fil, page +, fiche personne).
# Il ne reste donc qu'une poignée d'écrans où il se voit. On les nomme, et on mesure qu'il y bouge encore.
import sys, io as _io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
JS = r"""()=>{ const out=[];
  document.querySelectorAll('.tuto-fond, #createSheet, #settingsScreen').forEach(function(e){
    const k=getComffff=null; });
  return out; }"""
ETAT = r"""()=>[...document.querySelectorAll('.tuto-fond, #createSheet, #settingsScreen')].map(e=>{
  const k=getComputedStyle(e,'::before');
  return {id:e.id||('.'+e.className.split(' ')[0]),
          ouvert:e.classList.contains('show')||e.classList.contains('in'),
          visible:k.display!=='none' && k.content!=='none' && +k.opacity>0.02,
          op:+(+k.opacity).toFixed(2)};})"""
PORTES = [('l’Index', "()=>{const b=document.getElementById('indexBtn'); if(b)b.click();}"),
          ('le partage', "()=>{const b=document.getElementById('shareBtn'); if(b)b.click();}"),
          ('le tri', "()=>{const b=document.getElementById('fdSort')||document.getElementById('ixSort'); if(b)b.click();}")]
if __name__ == '__main__':
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=180000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        print('══ où le ::before est encore AFFICHÉ (écran fermé ou non) ══')
        for e in pg.evaluate(ETAT):
            print('   %-16s ::before affiché : %-3s (opacité %s)' % (e['id'], 'oui' if e['visible'] else 'non', e['op']))
        print()
        print('══ et il bouge encore là où il vit : deux captures à 900 ms ══')
        for nom, js in PORTES:
            pg.evaluate("()=>{try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.sheet.show,.poster.show').forEach(s=>s.classList.remove('show'));}")
            pg.wait_for_timeout(300)
            try: pg.evaluate(js)
            except Exception: pass
            pg.wait_for_timeout(2200)
            ouverts = [e for e in pg.evaluate(ETAT) if e['ouvert']]
            clip = pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
            a = Image.open(_io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')
            pg.wait_for_timeout(900)
            b = Image.open(_io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')
            d = np.asarray(ImageChops.difference(a, b)).max(axis=2)
            print('   %-12s ouvert : %-34s · pixels changés %5.2f %% · écart max %d'
                  % (nom, ', '.join('%s(::before %s)' % (e['id'], 'affiché' if e['visible'] else 'masqué') for e in ouverts) or '—',
                     100.0 * (d > 2).mean(), d.max()))
        br.close()
