import json,sys
from playwright.sync_api import sync_playwright
V={'avant':'sauvegardes/app-avant-lot-nuee-entree.html','app':'app.html'}
J=r"""()=>{const D=document.getElementById('device').getBoundingClientRect(),k=D.width/390;
 const Y=v=>+((v-D.top)/k).toFixed(1);
 const encre=e=>{const rg=document.createRange();rg.selectNodeContents(e);const r=rg.getBoundingClientRect();return r;};
 const vis=e=>{if(!e)return false;const c=getComputedStyle(e);const r=e.getBoundingClientRect();return c.display!=='none'&&c.visibility!=='hidden'&&r.height>2&&+c.opacity>.05;};
 const B=[];
 const cv=document.getElementById('dpTrameCv'); if(cv){const h=parseFloat(cv.style.height)||cv.getBoundingClientRect().height/k; B.push(['trait (bas de la vague)',Y(D.top+(h-40)*k),Y(D.top+(h-40)*k)]);}
 const au=document.getElementById('dAura'); if(vis(au)){const r=au.getBoundingClientRect();B.push(['Noyaux',Y(r.top),Y(r.bottom)]);}
 ['dptQui','dptTitre','dptQuand'].forEach(id=>{const e=document.getElementById(id);if(vis(e)){const r=encre(e);B.push([id,Y(r.top),Y(r.bottom)]);}});
 document.querySelectorAll('#dpNueeFil .nf-item').forEach((e,i)=>{if(vis(e)){const r=e.getBoundingClientRect();B.push(['carte '+(i+1),Y(r.top),Y(r.bottom)]);}});
 const a=document.getElementById('nfAdd'); if(vis(a)&&a.closest('#dpNueeFil')){const r=a.getBoundingClientRect();B.push(['Planter dans la Nuée',Y(r.top),Y(r.bottom)]);}
 const bar=document.getElementById('dpDetails'); const br=bar?bar.getBoundingClientRect():null;
 return {blocs:B, barre:br?Y(br.top):null, etat:(document.getElementById('dptQuand')||{}).textContent};}"""
OUT={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for vn,f in V.items():
        for th in ['light','dark']:
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
            pg.goto('http://127.0.0.1:8752/'+f); pg.wait_for_timeout(6800)
            pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
            pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(900)
            D=pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top,r.width/390];}")
            clip={'x':D[0],'y':D[1],'width':390*D[2],'height':844*D[2]}
            for nk in ['atelier','potager']:
                pg.evaluate("(k)=>{closeAll();openEssaim(k)}",nk); pg.wait_for_timeout(2600)
                r=pg.evaluate(J); OUT['%s|%s|%s'%(vn,th,nk)]=r
                pg.screenshot(path='planche-reperage/nuee_%s_%s_%s.png'%(vn,nk,th),clip=clip)
                if nk=='potager':
                    # au bout du fil : l'entrée est-elle au-dessus de la barre ?
                    pg.evaluate("()=>{const m=document.getElementById('detailPoster');m.scrollTop=m.scrollHeight;const n=document.getElementById('dpMain');if(n)n.scrollTop=n.scrollHeight;}"); pg.wait_for_timeout(1500)
                    OUT['%s|%s|%s|bout'%(vn,th,nk)]=pg.evaluate(J)
                    pg.screenshot(path='planche-reperage/nuee_%s_%s_%s_bout.png'%(vn,nk,th),clip=clip)
            ctx.close()
    b.close()
json.dump(OUT,open('planche-reperage/nuee_ecarts.json','w'),ensure_ascii=False,indent=1)
for k,v in OUT.items():
    bl=sorted(v['blocs'],key=lambda x:x[1])
    airs=['%s→%s %.1f'%(bl[i][0][:10],bl[i+1][0][:10],bl[i+1][1]-bl[i][2]) for i in range(len(bl)-1)]
    last=bl[-1]; print(k,'| état «%s»'%v['etat'],'| barre',v['barre'],'| dernier bas',last[2]); print('   ',' · '.join(airs))
