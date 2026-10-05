# tous les textes visibles SOUS la bande d'une fiche / de la page +, en sombre : couleur, fond effectif, contraste
import sys, json
from playwright.sync_api import sync_playwright
SCAN=r"""(rootId)=>{ const root=document.getElementById(rootId); const dv=document.getElementById('device').getBoundingClientRect();
  const lin=c=>{c/=255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4)}; const Y=a=>0.2126*lin(a[0])+0.7152*lin(a[1])+0.0722*lin(a[2]);
  const rgb=s=>{const m=(s||'').match(/[\d.]+/g); return m?m.map(Number):null}; const hx=a=>'#'+a.slice(0,3).map(v=>Math.round(v).toString(16).padStart(2,'0')).join('').toUpperCase();
  const fond=(e)=>{ let n=e; while(n&&n!==document.documentElement){ const c=rgb(getComputedStyle(n).backgroundColor); if(c&&(c.length<4||c[3]>0.9)) return c; n=n.parentElement; } return null; };
  const out=[]; const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT); let t;
  while(t=w.nextNode()){ const s=t.textContent.trim(); if(!s) continue; const e=t.parentElement; const cs=getComputedStyle(e); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.05) continue;
    const r=document.createRange(); r.selectNodeContents(t); const b=r.getBoundingClientRect(); if(b.width<2||b.height<2) continue;
    const cx=b.left+b.width/2, cy=b.top+b.height/2; if(cx<dv.left||cx>dv.right||cy<dv.top||cy>dv.bottom) continue;
    const top=document.elementFromPoint(cx,cy); if(!top||!(top===e||e.contains(top)||top.contains(e))) continue;
    const c=rgb(cs.webkitTextFillColor)||rgb(cs.color), f=fond(e); if(!c||!f) continue;
    const a=Y(c), bb=Y(f); const k=(Math.max(a,bb)+0.05)/(Math.min(a,bb)+0.05);
    out.push({t:s.slice(0,28), c:hx(c), a:(c[3]==null?1:c[3]), f:hx(f), k:+k.toFixed(2), y:Math.round(b.top-dv.top), el:(e.id?'#'+e.id:'.'+(e.className||'').toString().split(' ')[0])}); }
  return out; }"""
CORPS='#273CEB'
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme('dark');}"); pg.wait_for_timeout(600)
    def montre(lab, root):
        L=[x for x in pg.evaluate(SCAN, root) if x['f']==CORPS]
        print('──', lab, ':', len(L), 'textes sur le corps')
        for x in L: print('   %s y%-4d %-28s %s (α %.2f) %5.2f:1  %s'%('OK ' if x['k']>=4.5 else 'KO ', x['y'], x['t'], x['c'], x['a'], x['k'], x['el']))
    for nom,ti in (('Promi à tenir','faire les crêpes'),('Promi en cours','nager le mardi')):
        pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}",ti); pg.wait_for_timeout(2600); montre(nom,'detailPoster')
        if nom=='Promi en cours':
            pg.evaluate("()=>{ const b=document.querySelector('#detailPoster .dp-peauf, #detailPoster #dpdBarre, #detailPoster [class*=peauf]'); }")
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3600); montre('page + Promi','createSheet')
    b.close()
