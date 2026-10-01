# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# CHANTIER 58 · LA PREUVE — deux choses, et les deux comptent
#   ① L'OMBRE BOUGE TOUJOURS sur l'écran qu'on regarde. On piège `style.setProperty` et on compte les
#      écritures reçues par l'écran OUVERT sur 1,2 s. Si elle tombe à zéro, la parade a éteint l'animation.
#   ② ELLE N'ÉCRIT PLUS SUR LES ÉCRANS FERMÉS. Même piège, on compte ce que reçoivent les onze autres.
# On mesure les deux sur la version d'avant et sur l'actuelle, écran par écran, dans les deux thèmes.
#   python3 preuve_ombre.py <url>
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
PIEGE = r"""()=>{ window.__ombre={};
  document.querySelectorAll('.tuto-fond, #createSheet, #settingsScreen').forEach(function(e){
    var id=e.id||('.'+e.className.split(' ')[0]);
    var sp=e.style.setProperty.bind(e.style);
    e.style.setProperty=function(p,v,pr){
      if(p==='--gx'||p==='--gy'||p==='--grot'){
        window.__ombre[id]=window.__ombre[id]||{n:0, ouvert:null};
        window.__ombre[id].n++;
        window.__ombre[id].ouvert=e.classList.contains('show')||e.classList.contains('in');
      }
      return sp(p,v,pr); }; }); }"""
LIT = r"""()=>{ const o=window.__ombre||{}, out={ouverts:{}, fermes:0, fermesListe:[]};
  const vus=[...document.querySelectorAll('.tuto-fond, #createSheet, #settingsScreen')];
  vus.forEach(function(e){ const id=e.id||('.'+e.className.split(' ')[0]);
    const ouvert=e.classList.contains('show')||e.classList.contains('in');
    const n=(o[id]&&o[id].n)||0;
    if(ouvert) out.ouverts[id]=n; else if(n){ out.fermes+=n; out.fermesListe.push(id+':'+n); } });
  return out; }"""
PORTES = [('la page +', "()=>document.getElementById('createBtn').click()"),
          ('les Réglages', "()=>document.getElementById('settingsBtn').click()"),
          ('le Fil', "()=>{const b=document.getElementById('feedBtn')||document.getElementById('filBtn'); if(b)b.click();}"),
          ('l’Aura', "()=>document.getElementById('souffleBtn').click()")]

if __name__ == '__main__':
    print('══ %s ══' % URL)
    with sync_playwright() as p:
        br = p.chromium.launch()
        for th in ('dark', 'light'):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto(URL, timeout=180000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(1200)
            for nom, js in PORTES:
                pg.evaluate("()=>{try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.sheet.show,.poster.show').forEach(s=>s.classList.remove('show'));}")
                pg.wait_for_timeout(300)
                try: pg.evaluate(js)
                except Exception: pass
                pg.wait_for_timeout(1500)
                pg.evaluate(PIEGE); pg.wait_for_timeout(1200)
                r = pg.evaluate(LIT)
                ouv = ' · '.join('%s %d' % (k, v) for k, v in r['ouverts'].items()) or '— aucun écran ouvert'
                print('   %-6s %-14s ouvert(s) : %-28s · écritures sur les FERMÉS : %4d %s'
                      % (th, nom, ouv, r['fermes'], ('(' + ', '.join(r['fermesListe'][:3]) + '…)') if r['fermes'] else ''))
            pg.context.close()
        br.close()

# ═══ ③ ET ELLE BOUGE VRAIMENT À L'ÉCRAN — deux captures à 900 ms d'écart, sur l'écran ouvert ══════════════
# Compter des écritures ne prouve pas que l'image change : le `::before` pourrait être masqué. On compare
# donc deux captures du MÊME écran ouvert et on donne la part de pixels qui ont changé.
def bouge(url, tag):
    import io as _io
    from PIL import Image, ImageChops
    import numpy as _np
    with sync_playwright() as p:
        br = p.chromium.launch()
        for nom, js in (('les Réglages', "()=>document.getElementById('settingsBtn').click()"),
                        ('le Fil', "()=>{const b=document.getElementById('feedBtn')||document.getElementById('filBtn'); if(b)b.click();}")):
            pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
            pg.goto(url, timeout=180000); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("()=>{try{closeAll();}catch(e){}}"); pg.wait_for_timeout(300)
            try: pg.evaluate(js)
            except Exception: pass
            pg.wait_for_timeout(2200)
            clip = pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}")
            a = Image.open(_io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')
            pg.wait_for_timeout(900)
            b = Image.open(_io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')
            d = _np.asarray(ImageChops.difference(a, b)).max(axis=2)
            print('   %-6s %-14s pixels changés en 900 ms : %5.2f %% · écart max %d niveaux'
                  % (tag, nom, 100.0 * (d > 2).mean(), d.max()))
            pg.context.close()
        br.close()
