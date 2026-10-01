# La couleur brute d'une dalle est-elle STABLE dans une page ? (deux rendus du même Promi, dans son monde)
import sys
from playwright.sync_api import sync_playwright
JS = r"""()=>(_auraComp.iles||[]).map(x=>{ const r=[]; for(let t=0;t<3;t++){ const cv=document.createElement('canvas'); cv.width=160; cv.height=160;
  Toile.dalleTrame(cv, x.pid, 1, x.monde); const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data, cnt={}; let n=0; const m=[0,0,0];
  for(let i=0;i<d.length;i+=4){ if(d[i+3]<24) continue; n++; m[0]+=d[i]; m[1]+=d[i+1]; m[2]+=d[i+2]; const q=((d[i]>>3)<<10)|((d[i+1]>>3)<<5)|(d[i+2]>>3); cnt[q]=(cnt[q]||0)+1; }
  const top=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a])[0]|0; r.push({moy:m.map(v=>Math.round(v/n)), dom:[((top>>10)&31)*8+4,((top>>5)&31)*8+4,(top&31)*8+4], part:+(cnt[top]/n).toFixed(2)}); }
  return {titre:x.titre, r:r}; })"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    pg.goto(sys.argv[1]); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{closeAll();document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));}")
    pg.wait_for_timeout(250); pg.evaluate("()=>document.getElementById('souffleBtn').click()")
    for _ in range(80):
        pg.wait_for_timeout(250)
        if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>20)"): break
    for x in pg.evaluate(JS): print('%-28s' % x['titre'][:28], ' | '.join('moy %s dom %s (%.0f%%)' % (tuple(r['moy']), tuple(r['dom']), r['part'] * 100) for r in x['r']))
    b.close()
