# L'ÉCRAN QUI VEND, VERSION SPHÈRE — sur la COPIE. On MESURE avant de regarder :
#   · la sphère peint-elle vraiment (pixels peints, pas « l'image a l'air bonne ») ?
#   · tourne-t-elle (lac à 3 s d'écart + deux captures comparées) ?
#   · les cotes : les trois lignes, et le BAS DE L'ESSAI qui doit rester au-dessus de 844
#   · l'Aura tient-elle à la nouvelle vitesse (2π/100) ?
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'sphere')
URL = 'http://127.0.0.1:8752/scratchpad/app-vend-sphere.html'
MES = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, o={};
  const q=(sel)=>{ const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect();
    return {x:+((r.left-dv.left)/s).toFixed(1), y:+((r.top-dv.top)/s).toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1),
            bas:+(((r.top-dv.top)+r.height)/s).toFixed(1), txt:(e.textContent||'').trim().slice(0,60)}; };
  o.sphere=q('#plCadre .plv-sph'); o.prix=q('#plCadre .plv-prix'); o.sous=q('#plCadre .plv-sous');
  o.annee=q('#plCadre #buyYear'); o.essai=q('#plCadre #buyMonth'); o.n1=q('#plCadre .pl-note.plv-n1'); o.n2=q('#plCadre .pl-note.plv-n2');
  o.lignes=[...document.querySelectorAll('#plCadre .plv-li')].map(e=>{ const r=e.getBoundingClientRect();
    return {top:+((r.top-dv.top)/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1),
            tete:e.querySelector('b').textContent, queue:e.querySelector('i').textContent}; });
  o.dallesCachees=[...document.querySelectorAll('#plCadre .plv-dal,#plCadre .plv-nom')].every(e=>getComputedStyle(e).display==='none');
  /* la sphère peint-elle VRAIMENT ? on compte les pixels non transparents */
  const cv=document.querySelector('#plCadre .plv-sph');
  if(cv && cv.width){ const g=cv.getContext('2d'); const d=g.getImageData(0,0,cv.width,cv.height).data; let n=0;
    for(let i=3;i<d.length;i+=4) if(d[i]>10) n++;
    o.encre={cv:[cv.width,cv.height], peints:n, part:+(100*n/(cv.width*cv.height)).toFixed(1)}; } else o.encre=null;
  o.vend=window._vendSphere||null;
  const sc=document.getElementById('plusScreen');
  o.ecran={scrollH:sc.scrollHeight, clientH:sc.clientHeight, defile:sc.scrollHeight>sc.clientHeight};
  try{ o.toile=window.Toile.count(); }catch(e){ o.toile='?'; }
  return o; }"""
R = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('dark', 'light'):
        pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=90000); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
        pg.wait_for_timeout(4500)
        m1 = pg.evaluate(MES)
        pg.locator('#plCadre').screenshot(path=os.path.join(OUT, '%s_vend_t0.png' % th))
        lac0 = pg.evaluate("()=>window._vendSphere?window._vendSphere.lac:null")
        pg.wait_for_timeout(3000)
        lac1 = pg.evaluate("()=>window._vendSphere?window._vendSphere.lac:null")
        pg.locator('#plCadre').screenshot(path=os.path.join(OUT, '%s_vend_t3.png' % th))
        tour = None
        if lac0 is not None and lac1 is not None:
            d = lac1 - lac0; tour = {'lac0': round(lac0,4), 'lac1': round(lac1,4), 'avance_rad': round(d,4),
                                     'vitesse_rad_s': round(d/3.0,5), 'tour_s': round(6.283185307/(d/3.0),1) if d>1e-6 else None}
        R[th] = {'mesures': m1, 'rotation': tour}
        print('══', th)
        print('   sphère      :', m1['sphere'], '| encre :', m1['encre'])
        print('   _vendSphere :', json.dumps(m1['vend'], ensure_ascii=False))
        print('   rotation    :', json.dumps(tour, ensure_ascii=False))
        print('   essai bas   :', m1['essai'] and m1['essai']['bas'], '(pli 844) · notes', m1['n1'] and m1['n1']['y'], m1['n2'] and m1['n2']['y'])
        print('   lignes      :', json.dumps(m1['lignes'], ensure_ascii=False))
        print('   dalles cachées :', m1['dallesCachees'], '· écran défile :', m1['ecran']['defile'], '· Toile.count :', m1['toile'])
        # l'Aura tient-elle à la nouvelle vitesse ?
        pg.evaluate("()=>{ try{closeAll();}catch(e){} const a=document.getElementById('auraScreen'); if(a) a.classList.add('show'); }")
        pg.wait_for_timeout(3200)
        a = pg.evaluate("()=>{ try{ return {AUTO:window._aura.G.AUTO, tour_s:+(6.283185307/window._aura.G.AUTO).toFixed(1), etat:window._aura.etat().pret, ms:window._aura.etat().ms}; }catch(e){ return String(e); } }")
        print('   Aura        :', json.dumps(a, ensure_ascii=False))
        R[th]['aura'] = a
        pg.context.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'mesures.json'), 'w'), ensure_ascii=False, indent=1)
