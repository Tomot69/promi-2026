# C-296 : un rectangle paraît et disparaît sur le « Je » de la phrase de la page +. Chaque image, chaque élément dont la boîte coupe le « Je » et qui
# PEINT quelque chose (fond, bord, contour, ombre, canevas, filtre) est relevé ; on liste ceux qui ne sont pas là au repos.
import sys, os, json; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F=os.environ.get('FICH','app.html')
REC=r"""()=>{ window.__R=[]; const sc=document.getElementById('createSheet');
 function jeRect(){ const b=document.querySelector('#csPhrase [data-ph=sens]'); if(!b) return null; const w=document.createTreeWalker(b,NodeFilter.SHOW_TEXT); let n; while((n=w.nextNode())&&!n.data.trim()); if(!n) return null;
   const i=n.data.search(/\S/); const r=document.createRange(); r.setStart(n,i); r.setEnd(n,Math.min(n.data.length,i+2)); const q=r.getBoundingClientRect(); return [q.left,q.top,q.right,q.bottom]; }
 function peint(e,cs){ const p=[]; if(e.tagName==='CANVAS') p.push('canvas'); const bg=cs.backgroundColor; if(bg&&bg!=='rgba(0, 0, 0, 0)'&&bg!=='transparent') p.push('bg '+bg); if(cs.backgroundImage&&cs.backgroundImage!=='none') p.push('bgi');
   if(parseFloat(cs.borderTopWidth)>0&&cs.borderTopStyle!=='none') p.push('bord '+cs.borderTopWidth+' '+cs.borderTopStyle+' '+cs.borderTopColor); if(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0) p.push('outline '+cs.outlineWidth+' '+cs.outlineColor);
   if(cs.boxShadow&&cs.boxShadow!=='none') p.push('ombre'); if(cs.filter&&cs.filter!=='none') p.push('filtre '+cs.filter); if(cs.backdropFilter&&cs.backdropFilter!=='none') p.push('bdf'); return p; }
 function nom(e){ return e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).join('.'):'')+(e.dataset&&e.dataset.ph?'[ph='+e.dataset.ph+']':''); }
 (function f(t){ const J=jeRect(); if(J){ const L=[]; for(const e of sc.querySelectorAll('*')){ const r=e.getBoundingClientRect(); if(!r.width||!r.height) continue; if(r.right<=J[0]||r.left>=J[2]||r.bottom<=J[1]||r.top>=J[3]) continue;
     const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none') continue; let o=1, a=e; while(a&&a!==document.body){ o*=parseFloat(getComputedStyle(a).opacity); a=a.parentElement; } if(o<0.02) continue;
     const p=peint(e,cs); if(e.classList&&e.classList.contains('v202-part')) p.push('bw '+cs.borderTopWidth); if(p.length) L.push(nom(e)+' {'+p.join(', ')+'} op '+o.toFixed(2)+' r '+cs.borderRadius+' ['+[r.left,r.top,r.width,r.height].map(v=>Math.round(v)).join(',')+']'); }
   window.__R.push([Math.round(t), J.map(v=>Math.round(v)), L]); }
   if(window.__R.length<2000) requestAnimationFrame(f); })(performance.now()); }"""
def rapport(pg, nom, base):
    R=pg.evaluate("()=>{ const r=window.__R; window.__R=[]; return r; }")
    vus={}
    for t,J,L in R:
        for x in L:
            k=x.split(' op ')[0]
            if k in base: continue
            vus.setdefault(k,[]).append(t)
    print('==',nom,'images',len(R))
    for k,v in vus.items(): print('   NEUF %3d images (%d → %d ms) : %s'%(len(v), v[0]-R[0][0], v[-1]-R[0][0], k[:260]))
    if '--detail' in sys.argv:
        for t,J,L in R:
            m=[x for x in L if 'ph-vide' in x]
            if m: print('     %4d Je %s'%(t-R[0][0],J), ' | '.join(x.split('} ',1)[1] for x in m))
    return R
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); B.toile_pleine(ctx,10); pg=B.ouvre(ctx,F,attente=7000)
    B.tap_sel(pg,'#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg,'.acc-pil[data-k=promi]'); pg.wait_for_timeout(3500)
    pg.evaluate(REC); pg.wait_for_timeout(800)
    R=pg.evaluate("()=>{ const r=window.__R; window.__R=[]; return r; }")
    base=set(x.split(' op ')[0] for t,J,L in R for x in L); print('au repos :'); [print('   ',x[:200]) for x in sorted(base)]
    for i in range(3):
        B.tap_sel(pg,'#csPhrase [data-ph=sens]'); pg.wait_for_timeout(2600); rapport(pg,'bascule %d'%(i+1), base)
        R=pg.evaluate("()=>{ const r=window.__R; window.__R=[]; return r; }")
        base|=set(x.split(' op ')[0] for t,J,L in R[-5:] for x in L)
    for i in range(2):
        B.tap_sel(pg,'#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1500); pg.keyboard.type('marcher', delay=60); pg.wait_for_timeout(1500); rapport(pg,'frappe %d'%(i+1), base)
        for _ in range(9): pg.keyboard.press('Backspace'); pg.wait_for_timeout(50)
        pg.wait_for_timeout(2500); rapport(pg,'effacement %d'%(i+1), base)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(2000); rapport(pg,'validation %d'%(i+1), base)
    b.close()
