"""duo_vue.py — LE CADRE ET L'APP CÔTE À CÔTE, POUR L'ŒIL.

Pas de sonde, pas de pourcentage : une image, le cadre à gauche, l'app à droite,
à l'échelle 1 (le `#device` fait 390 × 844 exactement au viewport 430 × 932).

Usage :  python3 scratchpad/duo_vue.py <sortie> [écran ...]
"""
import base64, os, sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
MBH = "http://127.0.0.1:8752/promi-moodboard-H.html"
NUT = "http://127.0.0.1:8752/promi-nuee-toile.html"

# nom, planche, (cadre sombre, cadre clair), mise en scène
ECRANS = [
 ('fiche-tenue',   MBH,(48,49), "()=>{closeAll(); const p=promises.filter(q=>q.title==='planter un arbre')[0]; if(p)openDetail(p.id);}"),
 ('fiche-atenir',  MBH,(44,45), "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p)openDetail(p.id);}"),
 ('fiche-encours', MBH,(46,47), "()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; if(p)openDetail(p.id);}"),
 ('fiche-chiche',  MBH,(56,57), "()=>{closeAll(); const p=promises.filter(q=>q.title==='le grand plongeoir')[0]; if(p)openDetail(p.id);}"),
 # ⚠ PAS DE FICHE POUR UN GARDÉ DE CÔTÉ — Q54, tranchée par Tom le 19 août :
 # « un gardé de côté SE REPREND, il ne se regarde pas ». Le toucher rouvre la page +
 # dans son état. Le cadre 62 montre une fiche : il est antérieur à la décision.
 # On compare donc à la page + d'un gardé, cadres 26/27.
 ('garde-reprise', MBH,(26,27), "()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p)openDetail(p.id);}"),
 ('page-plus',     MBH,(2,3),   "()=>{closeAll(); document.getElementById('createBtn').click(); setTimeout(()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0]; if(x)x.click();},300);}"),
 ('peaufiner',     MBH,(78,79), "()=>{closeAll(); const p=promises.filter(q=>q.title==='aller voir la mer')[0]||promises.filter(q=>!q.draft)[0]; openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 ('index-2',       MBH,(72,73), "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"),
 ('index-3',       MBH,(74,75), "()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=true; if(window._s4Index)_s4Index();}"),
 ('fil',           MBH,(76,77), "()=>{closeAll(); setView('fil');}"),
 ('nuee',          NUT,(10,11), "()=>{closeAll(); openEssaim('potager');}"),
 ('nuee-vide',     NUT,(0,1),   "()=>{closeAll(); openEssaim('atelier');}"),
 ('nuee-peauf',    MBH,(84,85), "()=>{closeAll(); openEssaim('potager'); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}"),
 # l'instant se met en scène par `_instantJoue`, comme le fait `releve-S5-instant.py`
 ('instant-arrive', MBH,(96,97), "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('arrive');}catch(e){}},900);}}"),
 ('instant-referme', MBH,(98,99), "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('referme');}catch(e){}},900);}}"),
 ('instant-apres', MBH,(100,101), "()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; if(p){openDetail(p.id); setTimeout(()=>{try{window._instantJoue('apres');}catch(e){}},900);}}"),
]

MARQUE = """()=>{const isF=e=>{const s=e.getAttribute('style')||'';
  return /width:\\s*390px/.test(s)&&/height:\\s*844px/.test(s);};
  [...document.querySelectorAll('div')].filter(isF).forEach((f,i)=>f.setAttribute('data-cadre',i));}"""

COTE = """(a)=>new Promise(res=>{const A=new Image(),B=new Image();let n=0;
 function pret(){ if(++n<2) return; const W=390,H=844,G=14;
  const c=document.createElement('canvas'); c.width=W*2+G; c.height=H;
  const g=c.getContext('2d'); g.fillStyle='#6E6E7A'; g.fillRect(0,0,c.width,c.height);
  g.drawImage(A,0,0,W,H); g.drawImage(B,W+G,0,W,H);
  res(c.toDataURL('image/png'));}
 A.onload=pret;B.onload=pret;A.src=a.a;B.src=a.b;})"""


def main():
    sortie = sys.argv[1]
    voulus = sys.argv[2:]
    os.makedirs(sortie, exist_ok=True)
    liste = [e for e in ECRANS if not voulus or e[0] in voulus]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        cadres = {}
        for url in (MBH, NUT):
            if not any(e[1] == url for e in liste):
                continue
            pg = b.new_page(viewport={'width':1400,'height':1000}, device_scale_factor=2)
            pg.goto(url); pg.wait_for_timeout(4500); pg.evaluate(MARQUE)
            for nom, u, (cs, cl), _ in liste:
                if u != url: continue
                for th, n in (('dark', cs), ('light', cl)):
                    el = pg.query_selector('[data-cadre="%d"]' % n)
                    if el: cadres[(nom, th)] = base64.b64encode(el.screenshot()).decode()
            pg.close()

        app = {}
        pg = b.new_page(viewport={'width':430,'height':932}, device_scale_factor=2)
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');"
                    "if(o){o.classList.add('gone');o.style.display='none';}}")
        for th in ('dark', 'light'):
            pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
            for nom, u, _, js in liste:
                pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(400)
                try: pg.evaluate(js)
                except Exception as e: print('  ⚠ %s : %s' % (nom, e))
                # ⚠ ON ATTEND QUE LA MATIÈRE SOIT PEINTE, pas que les nœuds soient posés.
                #   Le compte de nœuds visibles se stabilise AVANT la peinture : la fiche
                #   sortait sans sa dalle, deux thèmes, alors que `dalleTrame` rendait bien.
                #   Le signal juste est celui que l'app publie quand elle a fini de peindre :
                #   `data-matiere` sur les canevas.
                pg.wait_for_timeout(3000)
                prec, stable = None, 0
                for _ in range(24):
                    pg.wait_for_timeout(250)
                    et = pg.evaluate("""()=>{
                      const n=[...document.querySelectorAll('#device *')]
                        .filter(e=>{const r=e.getBoundingClientRect();return r.width>4&&r.height>4;}).length;
                      const m=document.querySelectorAll('#device canvas[data-matiere]').length;
                      return n+':'+m;}""")
                    stable = stable + 1 if et == prec else 0
                    prec = et
                    if stable >= 2: break
                pg.wait_for_timeout(500)
                app[(nom, th)] = base64.b64encode(
                    pg.query_selector('#device').screenshot()).decode()
        pg.close()

        pg = b.new_page(); pg.goto('about:blank')
        for (nom, th), img in sorted(app.items()):
            ref = cadres.get((nom, th))
            if not ref:
                print('  ⚠ pas de cadre pour %s [%s]' % (nom, th)); continue
            u = pg.evaluate(COTE, {'a':'data:image/png;base64,'+ref,
                                   'b':'data:image/png;base64,'+img})
            p = os.path.join(sortie, '%s_%s.png' % (nom, th))
            open(p,'wb').write(base64.b64decode(u.split(',',1)[1]))
            print(p)
        b.close()

main()
