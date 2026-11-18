# C-299 : chaque écran sur trois formes de téléphone, l'app comme dans « Promi preuve » (la coquille : échelle qui couvre, zones sûres déclarées).
import sys, os, re; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import banc_tom as B
src=open('redteam_app.py', encoding='utf-8').read(); ns={'VITE': False}; exec(re.search(r'(def ecrans\(pg\):.*?return L\n)', src, re.S).group(1), ns); ecrans=ns['ecrans']
SONDE=eval(open('scratchpad/v207/haut_ecrans.py').read().split('SONDE=',1)[1].split('\nwith ')[0])
COQ=open('../promi-preuve-capacitor/capacitor/coquille.js',encoding='utf-8').read()
i=COQ.index("  (function () { var st = document.createElement('style'); st.id = 'coquille-plein-ecran';"); j=COQ.index("})();\n",i)+6; FIT=COQ[i:j]
FORMES=[('16e',390,844,[47,0,34,0]),('16 Pro',402,874,[62,0,34,0]),('SE',375,667,[20,0,0,0])]
OUT='scratchpad/v207/formes'; os.makedirs(OUT,exist_ok=True)
QUELS=set((sys.argv[1] if len(sys.argv)>1 else 'accueil,page+ promi,fiche promi,fiche cercle,index,fil,aura,reglages,partager,studio encre').split(','))
bilan=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for nomF,W,H,ins in FORMES:
        ctx=B.contexte(b,vw=W,vh=H); B.toile_pleine(ctx,10)
        ctx.add_init_script("window.__zsInsets=%s; document.addEventListener('DOMContentLoaded',function(){ %s });" % (ins, FIT))
        pg=B.ouvre(ctx,'app.html'); faits=[]
        for nom,js in ecrans(pg):
            if nom not in QUELS: continue
            pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); }catch(e){} try{ closeAll(); }catch(e){} document.querySelectorAll('#auraScreen.show .closeb, #studioScreen.show .closeb').forEach(x=>{ try{x.click()}catch(e){} }); }"); pg.wait_for_timeout(700)
            try: pg.evaluate(js)
            except Exception as e: print('  !', nom, str(e)[:80])
            pg.wait_for_timeout(2600)
            dev=pg.evaluate("()=>{ const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.right,r.bottom]; }")
            couvre = dev[0]<=0.5 and dev[1]<=0.5 and dev[2]>=W-0.5 and dev[3]>=H-0.5
            # contenus au-dessus de la zone sûre (en px d'écran)
            haut=pg.evaluate("""()=>{ const out=[]; for(const e of document.querySelectorAll('#device *, .frame *')){ const r=e.getBoundingClientRect(); if(r.width<2||r.height<2||r.top>=%f||r.bottom<=0) continue; const c=getComputedStyle(e); if(c.visibility==='hidden'||c.display==='none') continue;
               let op=1,a=e; while(a&&a!==document.body){ op*=parseFloat(getComputedStyle(a).opacity); a=a.parentElement; } if(op<0.05) continue; const texte=[...e.childNodes].some(n=>n.nodeType===3&&n.data.trim()); const bord=parseFloat(c.borderTopWidth)>0&&c.borderTopStyle!=='none';
               if((texte||bord) && !(r.width>%f*0.9&&r.height>300)) out.push((e.id||e.className.toString().slice(0,20))+' '+Math.round(r.top)); } return out; }""" % (ins[0], W))
            haut=[x for x in haut if 'v187Bande' not in x]
            ch=os.path.join(OUT,'%s-%s.png'%(nomF.replace(' ',''),nom.replace(' ','_').replace('+','plus'))); pg.screenshot(path=ch); faits.append((nom,ch))
            bilan.append((nomF,nom,couvre,haut)); print(nomF, nom, 'couvre' if couvre else 'NE COUVRE PAS %s'%[round(v) for v in dev], 'contenus sous la zone non sûre :', haut[:4], flush=True)
        ctx.close()
        ims=[Image.open(c).convert('RGB') for _,c in faits]; w=200; h=int(ims[0].height*w/ims[0].width)
        P=Image.new('RGB',(len(ims)*(w+8)+8,h+30),(240,236,228)); d=ImageDraw.Draw(P)
        for k,(im,(nom,_)) in enumerate(zip(ims,faits)): P.paste(im.resize((w,h)),(8+k*(w+8),24)); d.text((8+k*(w+8),6),nom,fill=(0,0,0))
        P.save(os.path.join(OUT,'PLANCHE-%s.png'%nomF.replace(' ','')))
    b.close()
print('bilan :', sum(1 for x in bilan if x[2] and not x[3]), '/', len(bilan), 'écrans couverts et sans contenu hors zone sûre')
