import sys, io, os; sys.path.insert(0,'.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image
from playwright.sync_api import sync_playwright
ETAT = """a=>{ const [t, nat, etat, mots]=a; const p=promises.find(x=>x.title===t); if(!p) return null;
  if(nat==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; }
  p.comments=mots.map((x,i)=>({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); p.status='encours'; delete p.parts; delete p.req; if(nat==='chiche') p.who='Adrien';
  if(etat==='moitie'){ p.who='Rachel, Marion'; if(nat==='promi') p.req=true; p.parts={'Rachel':'2026-11-05T09:00:00Z'}; }
  if(etat==='tenu'){ p.status='tenu'; }
  if(etat==='passee'){ p.ech={iso:'2026-10-12', due:-28}; p.due=-28; }
  try{ saveState(true); }catch(e){}
  return p.id; }"""
TITRE = {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}
F=sys.argv[1]; sombre='--sombre' in sys.argv; out=sys.argv[2]
ims=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for nat in ('promi','chiche'):
        for etat in ('plante','moitie','tenu','passee'):
            ctx=B.contexte(b, sombre=sombre); B.toile_pleine(ctx,'cercle'); ctx.add_init_script(BJ.AMORCE); pg=B.ouvre(ctx,F,6000)
            pid=pg.evaluate(ETAT,[TITRE[nat],nat,etat,BJ.MOTS]); pg.evaluate("id=>{ try{closeAll()}catch(e){} openDetail(id); }",pid)
            for _ in range(40): pg.evaluate("()=>window.__horloge(100)"); pg.wait_for_timeout(50)
            pg.evaluate("()=>{document.getElementById('detailPoster').scrollTop=1}"); pg.wait_for_timeout(200)
            J=pg.evaluate("()=>{const j=_v189Jonction(); return j.F?j.F.s0:null}")
            d=B.dev(pg); k=d[4]; row=[]
            for s in (0, (J or 130)+14, (J or 130)+30, (J or 130)+60):
                pg.evaluate("s=>{document.getElementById('detailPoster').scrollTop=s}",s); pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
                full=Image.open(io.BytesIO(pg.screenshot())); q=full.size[0]/pg.evaluate("()=>innerWidth")
                row.append(full.crop((int(d[0]*q),int((d[1]+60*k)*q),int((d[0]+390*k)*q),int((d[1]+340*k)*q))))
            print(nat,etat,J,pg.erreurs[:2]); ims.append(row); ctx.close()
    b.close()
W,H=ims[0][0].size; m=Image.new('RGB',(W*8,H*4),'white')
for r,row in enumerate(ims):
    for c,im in enumerate(row): m.paste(im,((r)*W, c*H))
m=m.resize((m.size[0]//2,m.size[1]//2)); m.save(out)
