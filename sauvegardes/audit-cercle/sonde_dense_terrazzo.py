# DEUX MESURES avant d'écrire :
#  1 · Toile.renderTo rend-elle la Toile ENTIÈRE (cellules neutres comprises) hors de son écran, et à quelles cotes ?
#  2 · LE TERRAZZO SE LIT-IL ? Le bon test : l'écart entre la cellule peinte en matière Cercle et la MÊME peinte dans
#      le monde de base. Si Terrazzo s'écarte bien moins que Sillons et Gravure, la matière ne dit rien.
import json
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8752/app.html'
Q = r"""()=>{
  const o={};
  /* 1 · renderTo */
  const b=document.createElement('canvas');
  let ok=false; try{ ok=window.Toile.renderTo(b,2); }catch(e){ o.renderErr=String(e); }
  o.renderTo={ok:!!ok, px:[b.width,b.height], css:[b.width/2,b.height/2]};
  if(ok&&b.width){ const g=b.getContext('2d'), d=g.getImageData(0,0,b.width,b.height).data;
    let n=0, cnt={};
    for(let i=0;i<d.length;i+=40){ if(d[i+3]<10) continue; n++;
      const k=((d[i]>>4)<<8)|((d[i+1]>>4)<<4)|(d[i+2]>>4); cnt[k]=(cnt[k]||0)+1; }
    o.renderTo.echantillons=n; o.renderTo.teintes=Object.keys(cnt).length; }
  /* 2 · le Terrazzo se lit-il ? */
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=(window.Toile.mondeCourant()||{});
  function rend(id,m){ const c=document.createElement('canvas');
    let k=false; try{ k=window.Toile.dalleTrame(c,id,1,m?{m:m,p:base.p,h:base.h}:undefined); }catch(e){}
    return (k&&c.width)?c:null; }
  function diff(a,b2){ /* écart moyen en niveaux, sur les pixels peints de l'une OU l'autre */
    const W=Math.min(a.width,b2.width), H=Math.min(a.height,b2.height);
    const da=a.getContext('2d').getImageData(0,0,W,H).data, db=b2.getContext('2d').getImageData(0,0,W,H).data;
    let s=0,n=0;
    for(let i=0;i<da.length;i+=4){ const aa=da[i+3],ab=db[i+3]; if(aa<24&&ab<24) continue;
      s+=(Math.abs(da[i]-db[i])+Math.abs(da[i+1]-db[i+1])+Math.abs(da[i+2]-db[i+2]))/3; n++; }
    return n?+(s/n).toFixed(1):0; }
  const cibles=ids.slice(0,6), res=[];
  for(const id of cibles){
    const bb=rend(id,base.m); if(!bb) continue;
    const r={id:id, base:base.m, aire:bb.width*bb.height};
    for(const m of ['sillons','gravure','terrazzo']){ const c=rend(id,m); r[m]=c?diff(bb,c):null; }
    res.push(r);
  }
  o.terrazzo=res;
  o.monde=base;
  return o; }"""
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
        pg.wait_for_timeout(2200)
        R=pg.evaluate(Q)
        print('══',th)
        print('   renderTo :', json.dumps(R['renderTo'], ensure_ascii=False), '· monde', R['monde'])
        print('   écart d’une cellule entre son monde de base et la matière Cercle (niveaux) :')
        for r in R['terrazzo']:
            print('     dalle %-4s  sillons %-6s gravure %-6s terrazzo %-6s' % (r['id'], r['sillons'], r['gravure'], r['terrazzo']))
        vals={m:[r[m] for r in R['terrazzo'] if r[m] is not None] for m in ('sillons','gravure','terrazzo')}
        for m,v in vals.items():
            if v: print('     %-9s médiane %.1f  (min %.1f, max %.1f)' % (m, sorted(v)[len(v)//2], min(v), max(v)))
        pg.context.close()
    br.close()
