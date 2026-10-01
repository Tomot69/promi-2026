# L'ÉCRAN QUI VEND v3 (dense) — CINQ OUVERTURES D'AFFILÉE dans les deux thèmes.
# On compare la COMPOSITION publiée, pas les pixels : la Toile respire avec performance.now(), des pixels
# différents ne prouveraient rien (CLAUDE §7).
import json, os, itertools
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,'toile3')
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile3.html'
MES=r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const q=(sel)=>{const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect();
    return {y:+((r.top-dv.top)/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1),
            x:+((r.left-dv.left)/s).toFixed(1), w:+(r.width/s).toFixed(1), h:+(r.height/s).toFixed(1),
            txt:(e.textContent||'').trim().slice(0,40), police:getComputedStyle(e).fontFamily.split(',')[0], graisse:getComputedStyle(e).fontWeight};};
  const B={fermer:q('#plusScreen .closeb'), toile:q('#pcCadre .pc-toile'), titre:q('#pcCadre .pc-h'), sous:q('#pcCadre .pc-sub'),
    prix:q('#pcCadre .pc-prix b'), permois:q('#pcCadre .pc-prix i'), cta1:q('#pcCadre #buyMonth'), cta2:q('#pcCadre #buyYear'),
    legal:q('#pcCadre .pc-legal')};
  const args=[...document.querySelectorAll('#pcCadre .pc-arg')].map(e=>({y:+((e.getBoundingClientRect().top-dv.top)/s).toFixed(1),
    bas:+(((e.getBoundingClientRect().top-dv.top)+e.getBoundingClientRect().height)/s).toFixed(1),
    police:getComputedStyle(e.querySelector('b')).fontFamily.split(',')[0], graisse:getComputedStyle(e.querySelector('b')).fontWeight}));
  const cv=document.querySelector('#pcCadre .pc-toile canvas'); let encre=null;
  if(cv&&cv.width){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data;
    let n=0, cnt={};
    for(let i=0;i<d.length;i+=24){ if(d[i+3]<10) continue; n++;
      const k=((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4); cnt[k]=(cnt[k]||0)+1; }
    encre={part:+(100*n/(cv.width*cv.height/6)).toFixed(1), teintes:Object.keys(cnt).length}; }
  const sc=document.getElementById('plusScreen');
  return {B, args, encre, vend:window._vendToile||null, defile:sc.scrollHeight>sc.clientHeight,
          air:{ 'ferme→Toile':+(B.toile.y-B.fermer.bas).toFixed(1), 'Toile→titre':+(B.titre.y-B.toile.bas).toFixed(1),
                'arg3→prix':+(B.prix.y-args[2].bas).toFixed(1), 'prix→CTA':+(B.cta1.y-B.prix.bas).toFixed(1),
                'légal→bas':+(844-B.legal.bas).toFixed(1)}}; }"""
def ouvre(pg):
    pg.evaluate("()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }")
    pg.wait_for_timeout(450)
    pg.evaluate("()=>{ const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
    pg.wait_for_timeout(2000)
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        print('══',th); sigs=[]; ids=[]
        for k in range(5):
            ouvre(pg); m=pg.evaluate(MES); v=m['vend']
            pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_o%d.png'%(th,k+1)))
            sigs.append(v['sig']); ids.append(set(int(x) for x in v['sig'].split('|')[1].split(',') if x))
            print('   o%d · fenêtre éch %.3f (%d,%d) %dx%d · %2d dalles colorées (%s fenêtres possibles) · Cercle %s · couv %s · %s groupes · Toile %s teintes'
                  % (k+1, v['fenetre']['s'], v['fenetre']['ox'], v['fenetre']['oy'], v['fenetre']['largeur'], v['fenetre']['hauteur'],
                     v['dallesVues'], v.get('fenetres'), [(c['monde'],c['ecart']) for c in v['cercle']], v['fenetre']['couverture'], v['fenetre']['groupes'], m['encre']['teintes']))
            if k==0:
                print('   ✕ %s « %s » · Toile %s · défile %s' % ([m['B']['fermer']['x'],m['B']['fermer']['y']], m['B']['fermer']['txt'],
                      [m['B']['toile']['x'],m['B']['toile']['y'],m['B']['toile']['w'],m['B']['toile']['h']], m['defile']))
                print('   AIR :', json.dumps(m['air'],ensure_ascii=False))
                print('   POLICES : titre %s/%s · libellé %s/%s · prix %s/%s · CTA %s/%s · option %s/%s'
                      % (m['B']['titre']['police'],m['B']['titre']['graisse'], m['args'][0]['police'],m['args'][0]['graisse'],
                         m['B']['prix']['police'],m['B']['prix']['graisse'], m['B']['cta1']['police'],m['B']['cta1']['graisse'],
                         m['B']['cta2']['police'],m['B']['cta2']['graisse']))
                print('   MOTS : « %s » · « %s » · option « %s »' % (m['B']['prix']['txt'], m['B']['permois']['txt'], m['B']['cta2']['txt']))
        print('   → 5 signatures distinctes : %s (%d/5)' % (len(set(sigs))==5, len(set(sigs))))
        comm=[len(a&b)/max(1,len(a|b)) for a,b in itertools.combinations(ids,2)]
        print('   → recouvrement des dalles entre deux ouvertures : médiane %.0f%%, max %.0f%%'
              % (100*sorted(comm)[len(comm)//2], 100*max(comm)))
        pg.context.close()
    br.close()
