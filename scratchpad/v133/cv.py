from playwright.sync_api import sync_playwright
import json, sys
NS=[int(x) for x in __import__('os').environ.get('NS','3,5,7,9,12,15,20,30,40,60').split(',')]; MONDES=sys.argv[1:] or ['encre','madrure','esquille']
PEUPLE="""([n,dec])=>{ const base=promises.filter(p=>!p.draft&&!p.nuee&&!p.chiche)[0]; const B=JSON.parse(JSON.stringify(base)); promises.length=0;
  const mots=['planter un arbre','faire les crêpes','nager le mardi','rapporter le livre','appeler Mamie','venir dimanche','courir au parc','écrire à Léa','ranger le garage','apprendre le piano','goûter chez Jo','réparer le vélo'];
  const gens=['Rachel','Marion','Adrien','Nico','moi','Léa','Jo'];
  for(let i=0;i<n;i++){ const p=JSON.parse(JSON.stringify(B)); p.id=9000+dec*100+i; p.title=mots[(i+dec*5)%mots.length]+((i>=mots.length||dec)?' '+(1+dec*7+Math.floor(i/mots.length)):''); p.who=gens[(i*3)%gens.length]; delete p.dalle; delete p.monde; delete p.dessin; promises.push(p); }
  window.Toile.sync(promises.map(p=>p.id)); try{ window.Toile.cadre&&window.Toile.cadre(); }catch(e){} }"""
MES="""()=>{ const cv=document.getElementById('toileCv'); const w=cv.clientWidth,h=cv.clientHeight; const A={}; let tot=0, vide=0;
  for(let y=1;y<h;y+=3) for(let x=1;x<w;x+=3){ tot++; const t=window.Toile.hit(x,y); if(t&&t.pid!=null){ A[t.pid]=(A[t.pid]||0)+1; } else vide++; }
  const v=Object.values(A).map(a=>a*9); const m=v.reduce((a,b)=>a+b,0)/Math.max(1,v.length); const sd=Math.sqrt(v.reduce((a,b)=>a+(b-m)*(b-m),0)/Math.max(1,v.length));
  return {n:v.length, cv:m?sd/m:0, min:Math.min.apply(null,v), max:Math.max.apply(null,v), moy:m, vide:vide/tot, aires:v.sort((a,b)=>b-a).map(Math.round)} }"""
out={}; ESSAIS=int(__import__('os').environ.get('ESSAIS','4'))
with sync_playwright() as p:
    b=p.webkit.launch()
    for mo in MONDES:
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:160])); pg.goto('http://127.0.0.1:8752/'+__import__('os').environ.get('PAGE','app.html')); pg.wait_for_timeout(6500)
        pg.evaluate("(m)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setPremium(true); Toile.setTheme(m);}",mo); pg.wait_for_timeout(2500)
        out[mo]={}
        for n in NS:
            L=[]
            for dec in range(ESSAIS):
                pg.evaluate(PEUPLE,[n,dec]); pg.wait_for_timeout(3200); L.append(pg.evaluate(MES))
            cvs=[r['cv'] for r in L]; out[mo][n]={'cv':sum(cvs)/len(cvs),'cvs':cvs,'ratio':sum(r['max']/max(1,r['min']) for r in L)/len(L)}
            print('%-10s N=%2d  CV moyen %.2f  (%s)  max/min %4.1f'%(mo,n,out[mo][n]['cv'],' '.join('%.2f'%c for c in cvs),out[mo][n]['ratio']), flush=True)
        ctx.close()
    b.close()
json.dump(out,open('scratchpad/v133/cv-%s.json'%'-'.join(MONDES),'w'))
