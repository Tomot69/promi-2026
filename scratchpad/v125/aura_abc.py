# §5 — les trois compositions de l'Aura, 390 × 844, clair et sombre, toutes les cotes annotées (@3x)
import sys, json
sys.path.insert(0,'scratchpad'); from aura_ouvre import ouvre
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
src=open('scratchpad/v123/cotes_aura.py',encoding='utf-8').read(); Q=src[src.index('Q="""')+5:src.index('return o; }"""')]+'return o; }'
F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',34); f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30); FT=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',46)
S=3; L=640; REF=json.load(open('scratchpad/v124/cotes-apres.json'))
NOMS={'A':'A — appliquée (−10 · −8 · −8)','B':'B — plus serrée (−14 · −12 · −12)','C':'C — plus aérée (−6 · −6 · −6)'}
def paires(D):
    return [('plateau → Pelote',D['plateau'][1],D['silhouette (rayon 121)'][0]),('Pelote → ombre',D['silhouette (rayon 121)'][1],D['ombre'][0]),('ombre → bouton',D['ombre'][1],D['« Partager ma Pelote »'][0]),
            ('bouton → phrase',D['« Partager ma Pelote »'][1],D['la phrase'][0]),('phrase → disques',D['la phrase'][1],D['les Noyaux'][0]),('disques → légende',D['les Noyaux'][1],D['la légende'][0]),
            ('légende → chiffres',D['la légende'][1],D['les chiffres'][0]),('air sous les chiffres',D['les chiffres'][1],844.0)]
RES={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for comp in 'ABC':
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3,reduced_motion='reduce')
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?aura='+comp); pg.wait_for_timeout(7000)
        ims=[]
        for th in (0,1):
            ouvre(pg,th); pg.wait_for_timeout(2800); pg.evaluate("()=>{document.getElementById('auraScreen').scrollTop=0; _aura.vue(3.1,0.32)}"); pg.wait_for_timeout(700)
            D=pg.evaluate(Q); nom='sombre' if th else 'clair'; RES[(comp,nom)]=D
            fn='scratchpad/v125/aura-%s-%s.png'%(comp,nom); pg.screenshot(path=fn, clip={'x':20,'y':44,'width':390,'height':844})
            im=Image.open(fn).convert('RGB'); out=Image.new('RGB',(390*S+L,844*S+110),(255,255,255)); out.paste(im,(0,110)); d=ImageDraw.Draw(out)
            d.text((14,26),'Aura · %s · %s'%(NOMS[comp],nom),font=FT,fill=(20,20,20))
            ref=dict((n,b_-a_) for n,a_,b_ in paires(REF['clair']))
            for j,(n,y1,y2) in enumerate(paires(D)):
                Y1=110+y1*S; Y2=110+y2*S; xx=390*S-40-(j%3)*16
                for yy in (Y1,Y2): d.line([0,yy,390*S+30,yy],fill=(230,0,120),width=2)
                d.line([xx,Y1,xx,Y2],fill=(230,0,120),width=6)
                ty=(Y1+Y2)/2-36; dv=(y2-y1)-ref[n]
                d.text((390*S+44,ty),n,font=F,fill=(20,20,20))
                d.text((390*S+44,ty+40),'%.1f pt'%(y2-y1)+('   (v124 : %.1f, %+.1f)'%(ref[n],dv) if abs(dv)>0.05 else '   (inchangé)'),font=f,fill=(0,110,40) if n!='air sous les chiffres' or (y2-y1)>=48 else (200,0,0))
            out.save('planche-v125/aura-%s-%s.png'%(comp,nom)); ims.append(out)
        W=sum(i.size[0] for i in ims)+40; o=Image.new('RGB',(W,ims[0].size[1]),(255,255,255)); x=0
        for i in ims: o.paste(i,(x,0)); x+=i.size[0]+40
        o.save('planche-v125/aura-%s.png'%comp); ctx.close()
    b.close()
for k,D in RES.items(): print(k, ' · '.join('%s %.1f'%(n,b_-a_) for n,a_,b_ in paires(D)))
