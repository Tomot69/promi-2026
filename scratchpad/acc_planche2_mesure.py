# mesure les planches : collisions du chrome, libellés, zone libre, et l'atteinte des dalles avec le VRAI moteur
import json
from playwright.sync_api import sync_playwright
exec(open('scratchpad/accueil_audit.py').read().split('CMDS = [')[0])
MASQ=r"""(id)=>{const f=document.querySelector('[data-cadre="'+id+'"]');f.scrollIntoView({block:'center',inline:'center'});
 const r=f.getBoundingClientRect();const rows=[];
 for(let y=0;y<844;y+=4){let row='';for(let x=0;x<390;x+=4){const px=r.left+x+2,py=r.top+y+2;
   if(px<0||py<0||px>innerWidth||py>innerHeight){row+='?';continue;}
   const e=document.elementFromPoint(px,py);row+=(e&&e.closest('.ch'))?'0':'1';}rows.push(row);}
 return rows;}"""
COLL=r"""(id)=>{const f=document.querySelector('[data-cadre="'+id+'"]');const F=f.getBoundingClientRect();
 const els=[...f.querySelectorAll('.ch.dq,.ch.lb,.ch.plus,.ch.pil,.ch.rec,.plat .ic svg,.plat .mm,.plat .ct,.it .lb,.it svg')];
 const box=e=>{const r=e.getBoundingClientRect();let b={n:(e.className.baseVal!==undefined?'svg':e.className)+(e.textContent?':'+e.textContent.trim().slice(0,12):''),x0:r.left-F.left,y0:r.top-F.top,x1:r.right-F.left,y1:r.bottom-F.top};
   if(e.classList&&(e.classList.contains('lb')||e.classList.contains('mm')||e.classList.contains('ct'))){const rg=document.createRange();rg.selectNodeContents(e);const q=rg.getBoundingClientRect();b.x0=q.left-F.left;b.x1=q.right-F.left;b.y0=q.top-F.top;b.y1=q.bottom-F.top;}
   if(e.classList&&e.classList.contains('plus')){b.cx=(b.x0+b.x1)/2;b.cy=(b.y0+b.y1)/2;b.r=(b.x1-b.x0)/2+7;}
   return b;};
 const B=els.map(box);const out=[];
 const gap=(a,b)=>{ if(a.r||b.r){const c=a.r?a:b,o=a.r?b:a;const nx=Math.max(o.x0,Math.min(c.cx,o.x1)),ny=Math.max(o.y0,Math.min(c.cy,o.y1));return Math.hypot(nx-c.cx,ny-c.cy)-c.r;}
   const dx=Math.max(a.x0-b.x1,b.x0-a.x1,0),dy=Math.max(a.y0-b.y1,b.y0-a.y1,0);return (dx>0||dy>0)?Math.hypot(dx,dy):-Math.min(a.x1-b.x0,b.x1-a.x0,a.y1-b.y0,b.y1-a.y0);};
 for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){const a=B[i],b=B[j];
   const cont=(p,q)=>p.x0<=q.x0&&p.y0<=q.y0&&p.x1>=q.x1&&p.y1>=q.y1; if(cont(a,b)||cont(b,a))continue;
   const g=gap(a,b); if(g<8)out.push([a.n,b.n,+g.toFixed(1)]);}
 return out;}"""
LBL=r"""()=>{const s=document.createElement('span');s.className='lb';s.style.position='absolute';document.querySelector('.f').appendChild(s);
 const w=t=>{s.textContent=t;return +s.getBoundingClientRect().width.toFixed(1);};const o={};['Studio','Aura','Index · Fil','Partager','Fil','Index'].forEach(t=>o[t]=w(t));s.remove();return o;}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pl=b.new_page(viewport={'width':1700,'height':1000}); pl.goto("http://127.0.0.1:8752/PLANCHE-ACCUEIL-2.html"); pl.wait_for_timeout(2500)
    res={'libelles':pl.evaluate(LBL),'cadres':{}}
    ids=pl.evaluate("()=>[...document.querySelectorAll('[data-cadre]')].map(e=>e.dataset.cadre)")
    masques={}
    for i in ids:
        rows=pl.evaluate(MASQ,i); masques[i]=rows
        tot=sum(r.count('1') for r in rows); unk=sum(r.count('?') for r in rows)
        res['cadres'][i]={'libre_pct':round(100*tot/(len(rows)*len(rows[0])),1),'non_confirme':unk,'collisions':pl.evaluate(COLL,i)}
    # atteinte avec le vrai moteur, 3 chargements × 2 thèmes, pour les cadres de repos
    zooms=[0.4,0.48,0.6,0.8,1.0,1.25,1.5,2,3,5]
    att={}
    for th in ['light','dark']:
        for charge in range(3):
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
            pg.goto("http://127.0.0.1:8752/app.html"); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(1500)
            for i in ids:
                if not (i.endswith('-repos') or i.endswith('-zoom')): continue
                rows=[r.replace('?','0') for r in masques[i]]
                A=pg.evaluate(REACH_JS,[rows,zooms])
                for s,z in A['zooms'].items():
                    k=(i.split('-')[-1],s); att.setdefault(k,[0,0]); att[k][0]+=len(z['inatteignables']); att[k][1]+=z['n']
            ctx.close()
    res['atteinte']={'%s @ %s'%k:'%d inatteignables / %d'%tuple(v) for k,v in sorted(att.items())}
    b.close()
json.dump(res,open('scratchpad/acc_planche2_mesure.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))
