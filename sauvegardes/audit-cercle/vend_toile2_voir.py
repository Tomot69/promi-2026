# L'ÉCRAN QUI VEND v2 — on mesure l'AIR en entier, le nombre de dalles, l'écart de couleur,
# et surtout : LA TOILE EST-ELLE AUTRE À CHAQUE OUVERTURE (on ouvre trois fois) ?
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'toile2')
URL = 'http://127.0.0.1:8752/scratchpad/app-vend-toile2.html'
MES = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const q=(sel)=>{ const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect();
    return {y:+((r.top-dv.top)/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1),
            x:+((r.left-dv.left)/s).toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1),
            txt:(e.textContent||'').trim().slice(0,44)}; };
  const B={fermer:q('#plusScreen .closeb'), toile:q('#pcCadre .pc-toile'), titre:q('#pcCadre .pc-h'), sous:q('#pcCadre .pc-sub'),
    a1:q('#pcCadre .pc-arg:nth-of-type(1)'), prix:q('#pcCadre .pc-prix'), cta1:q('#pcCadre #buyMonth'),
    cta2:q('#pcCadre #buyYear'), legal:q('#pcCadre .pc-legal')};
  const args=[...document.querySelectorAll('#pcCadre .pc-arg')].map(e=>{const r=e.getBoundingClientRect();
    return {y:+((r.top-dv.top)/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1)};});
  const air={};
  air['Toile→titre']=+(B.titre.y-B.toile.bas).toFixed(1);
  air['titre→sous']=+(B.sous.y-B.titre.bas).toFixed(1);
  air['sous→arg1']=+(args[0].y-B.sous.bas).toFixed(1);
  air['arg1→arg2']=+(args[1].y-args[0].bas).toFixed(1);
  air['arg2→arg3']=+(args[2].y-args[1].bas).toFixed(1);
  air['arg3→prix']=+(B.prix.y-args[2].bas).toFixed(1);
  air['prix→CTA']=+(B.cta1.y-B.prix.bas).toFixed(1);
  air['CTA→option']=+(B.cta2.y-B.cta1.bas).toFixed(1);
  air['option→légal']=+(B.legal.y-B.cta2.bas).toFixed(1);
  air['légal→bas']=+(844-B.legal.bas).toFixed(1);
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let encre=null;
  if(cv&&cv.width){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data; let n=0;
    for(let i=3;i<d.length;i+=4) if(d[i]>10) n++;
    encre={peints:n, part:+(100*n/(cv.width*cv.height)).toFixed(1)}; }
  const sc=document.getElementById('plusScreen');
  const cs=getComputedStyle(document.querySelector('#pcCadre .pc-toile'));
  return {boites:B, air, encre, vend:window._vendToile||null,
          fondCadre:cs.backgroundColor, fondPage:getComputedStyle(sc).backgroundColor,
          defile:sc.scrollHeight>sc.clientHeight, plusBas:B.legal.bas}; }"""
def ouvre(pg):
    pg.evaluate("()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }")
    pg.wait_for_timeout(500)
    pg.evaluate("()=>{ const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(2200)
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('light','dark'):
        pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══', th)
        vus=[]
        for k in range(3):
            ouvre(pg); m = pg.evaluate(MES)
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_o%d.png'%(th,k+1)))
            v=m['vend']; vus.append(v)
            print('   ouverture %d : %d dalles · Cercle %s · fenêtre y=%s éch. %s (%d bandes) · ratés %s · écart couleur max %s · tailles %s'
                  % (k+1, v['dalles'], v['cercle'], v['fenetre']['y'], v['fenetre']['echelle'], v['fenetre']['bandes'],
                     v.get('rates'), v['ecartCouleurMax'], v['tailles'][:6]))
            if k==0:
                print('   ✕ FERMER : %s « %s »' % ([m['boites']['fermer']['x'],m['boites']['fermer']['y'],m['boites']['fermer']['w'],m['boites']['fermer']['h']], m['boites']['fermer']['txt']))
                print('   fond cadre %s · fond page %s' % (m['fondCadre'], m['fondPage']))
                print('   AIR :', json.dumps(m['air'], ensure_ascii=False))
                print('   encre Toile %s · défile %s · le plus bas %s' % (m['encre'], m['defile'], m['plusBas']))
        # différente à chaque ouverture ?
        cles=[(v['fenetre']['y'], tuple(v['cercle']), tuple(v['tailles'])) for v in vus]
        print('   → trois ouvertures distinctes : %s' % (len(set(cles))==3))
        pg.context.close()
    br.close()
