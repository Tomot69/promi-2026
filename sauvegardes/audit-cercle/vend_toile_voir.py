# L'ÉCRAN QUI VEND — VERSION TOILE, sur la COPIE. On MESURE avant de regarder.
import json, os
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'toile')
URL = 'http://127.0.0.1:8752/scratchpad/app-vend-toile.html'
MES = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, o={};
  const q=(sel)=>{ const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect();
    return {x:+((r.left-dv.left)/s).toFixed(1), y:+((r.top-dv.top)/s).toFixed(1), w:+(r.width/s).toFixed(1),
            h:+(r.height/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1), txt:(e.textContent||'').trim().slice(0,54)}; };
  o.fermer=q('#pcCadre .pc-x'); o.toile=q('#pcCadre .pc-toile'); o.titre=q('#pcCadre .pc-h'); o.sous=q('#pcCadre .pc-sub');
  o.args=[...document.querySelectorAll('#pcCadre .pc-arg')].map(e=>{const r=e.getBoundingClientRect();
    return {y:+((r.top-dv.top)/s).toFixed(1), t:e.querySelector('b').textContent, d:e.querySelector('i').textContent};});
  o.prix=q('#pcCadre .pc-prix'); o.cta1=q('#pcCadre #buyMonth'); o.cta2=q('#pcCadre #buyYear'); o.legal=q('#pcCadre .pc-legal');
  const cv=document.querySelector('#pcCadre .pc-toile canvas');
  if(cv&&cv.width){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data; let n=0;
    for(let i=3;i<d.length;i+=4) if(d[i]>10) n++;
    o.encre={cv:[cv.width,cv.height], peints:n, part:+(100*n/(cv.width*cv.height)).toFixed(1)}; }
  o.vend=window._vendToile||null;
  const sc=document.getElementById('plusScreen');
  o.ecran={scrollH:sc.scrollHeight, clientH:sc.clientHeight, defile:sc.scrollHeight>sc.clientHeight};
  o.restes=[...document.querySelectorAll('#plusScreen>.enh,#plusScreen>.pl-eb,#plusScreen>.pl-h,#plusScreen #plCadre,#plusScreen>.closeb')]
            .filter(e=>getComputedStyle(e).display!=='none').length;
  const bas=[o.legal,o.cta2,o.cta1].filter(Boolean).map(e=>e.bas);
  o.plusBas=Math.max(...bas);
  return o; }"""
with sync_playwright() as p:
    br = p.chromium.launch()
    for th in ('light','dark'):
        pg = br.new_context(viewport={'width':430,'height':932}, device_scale_factor=2).new_page()
        pg.goto(URL, timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", th); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
        pg.wait_for_timeout(2200)
        m = pg.evaluate(MES)
        pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_t0.png'%th))
        pg.wait_for_timeout(5200)
        pg.locator('#pcCadre').screenshot(path=os.path.join(OUT,'%s_t5.png'%th))
        print('══', th)
        print('   _vendToile :', json.dumps(m['vend'], ensure_ascii=False))
        print('   encre      :', m['encre'])
        print('   ✕ %s · Toile %s' % (m['fermer'] and [m['fermer']['x'],m['fermer']['y'],m['fermer']['w'],m['fermer']['h']],
                                      m['toile'] and [m['toile']['x'],m['toile']['y'],m['toile']['w'],m['toile']['h']]))
        print('   titre y=%s « %s » · sous y=%s « %s »' % (m['titre']['y'], m['titre']['txt'], m['sous']['y'], m['sous']['txt']))
        for a in m['args']: print('   arg y=%-6s %s — %s' % (a['y'], a['t'], a['d']))
        print('   prix y=%s « %s » · CTA1 %s « %s » · CTA2 y=%s « %s »' % (m['prix']['y'], m['prix']['txt'],
              [m['cta1']['x'],m['cta1']['y'],m['cta1']['w'],m['cta1']['h']], m['cta1']['txt'], m['cta2']['y'], m['cta2']['txt']))
        print('   légal y=%s « %s » · le plus bas : %s (pli 844)' % (m['legal']['y'], m['legal']['txt'], m['plusBas']))
        print('   défile : %s · restes visibles de l’ancien écran : %s' % (m['ecran']['defile'], m['restes']))
        pg.context.close()
    br.close()
