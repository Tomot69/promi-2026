# PLANCHE C-042 (v130) — la mise en page du mode dessin : rangée A SOUS le trait, déploiements SOUS la rangée, rien dans la bande.
# Posé par-dessus l'app RENDUE (vraies couleurs, lues sur la fiche). Rien n'est construit dans l'app. @3x.
import sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
clip={'x':20,'y':44,'width':390,'height':844}; D='scratchpad/v130/dessin/'; K=3
PEN=open(D+'pen.js',encoding='utf-8').read(); OV=open(D+'ov.js',encoding='utf-8').read()
FICHES={'promi':"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}", 'cercle':"()=>{closeAll(); openEssaim('potager');}"}
ECART=24            # l'écart franc entre le bas du trait et la rangée (proposé)
BAS=r"""()=>{const cv=document.getElementById('dpTrameCv'); const g=cv.getContext('2d'); const W=cv.width,H=cv.height; const d=g.getImageData(0,0,W,H).data; const k=W/cv.getBoundingClientRect().width; let bas=0;
  for(let y=0;y<H;y++){ for(let x=0;x<W;x+=3){ if(d[(y*W+x)*4+3]>200){ bas=y; break; } } } const dv=document.getElementById('device').getBoundingClientRect(); return cv.getBoundingClientRect().top-dv.top+(bas+1)/k; }"""
YTOP="(s)=>{const dv=document.getElementById('device').getBoundingClientRect(); const e=document.querySelector(s); const r=document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect().top-dv.top;}"
def police(t, gras=True):
    for f in (('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if gras else '/System/Library/Fonts/Supplemental/Arial.ttf'),'/System/Library/Fonts/Helvetica.ttc'):
        try: return ImageFont.truetype(f,t)
        except Exception: pass
    return ImageFont.load_default()
def planche(titre, sous, cases, cols, sortie, sombre):
    ims=[(t,c,Image.open(f).convert('RGB'),m) for t,c,f,m in cases]; w,h=ims[0][2].size; M=70; G=250; T=190; H0=250
    rows=(len(ims)+cols-1)//cols; bg=(240,236,226) if not sombre else (30,26,22); enc=(32,25,8) if not sombre else (247,240,222); gris=(110,99,80) if not sombre else (190,180,160); rouge=(221,77,35)
    P=Image.new('RGB',(M+cols*(w+G+M), H0+rows*(h+T+M)), bg); d=ImageDraw.Draw(P)
    d.text((M,50),titre,fill=enc,font=police(64)); d.text((M,150),sous,fill=gris,font=police(40,False))
    for i,(t,c,im,m) in enumerate(ims):
        x=M+(i%cols)*(w+G+M); y=H0+(i//cols)*(h+T+M); d.text((x,y+20),t,fill=enc,font=police(50)); d.text((x,y+92),c,fill=gris,font=police(34,False)); P.paste(im,(x,y+T))
        # les cotes, dans la marge : le bas du trait, le haut de la rangée, l'écart ; puis le bas du dernier outil
        yt=y+T+m['trait']*K; yr=y+T+m['haut']*K; xb=x+w+26
        d.line([(x+w+6,yt),(xb+60,yt)],fill=rouge,width=4); d.line([(x+w+6,yr),(xb+60,yr)],fill=rouge,width=4); d.line([(xb+30,yt),(xb+30,yr)],fill=rouge,width=4)
        d.text((xb+72,yt-52),'trait %d'%round(m['trait']),fill=rouge,font=police(32)); d.text((xb+72,(yt+yr)//2-18),'%d pt'%round(m['haut']-m['trait']),fill=rouge,font=police(38)); d.text((xb+72,yr+10),'rangée %d'%round(m['haut']),fill=rouge,font=police(32))
        yb=y+T+m['bas']*K; d.line([(x+w+6,yb),(xb+60,yb)],fill=gris,width=3); d.text((xb+72,yb-18),'outils ↑ %d'%round(m['bas']),fill=gris,font=police(30))
        if m.get('texte') is not None:
            yx=y+T+m['texte']*K; d.line([(x+w+6,yx),(xb+60,yx)],fill=gris,width=3); d.text((xb+72,yx-2),'texte %d'%round(m['texte']),fill=gris,font=police(30))
    P.save(sortie); print(sortie, P.size)
TOUT={}
with sync_playwright() as p:
    b=p.webkit.launch(); NOM={'promi':'fiche Promi','cercle':'fiche Cercle'}
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=K)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}"%th)
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:160])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{ setTheme(t) }catch(e){} }", th); pg.wait_for_timeout(900)
        pg.evaluate(PEN); pg.evaluate(OV)
        for nat in ('promi','cercle'):
            pg.evaluate("()=>OV.nettoie()"); pg.evaluate(FICHES[nat]); pg.wait_for_timeout(3200)
            trait=pg.evaluate(BAS); yRow=round(trait)+ECART; sousDeploi=yRow+54+128+18
            base=dict(nat=nat, light=(th=='light'), yRow=yRow, yBande=104, sansDalle=1, epure=1, cachePhoto=1, dessin='simple', sel='plume', compo='A')
            if nat=='promi':
                yq=pg.evaluate(YTOP,'#dptQui'); dy=round(sousDeploi-yq)
                base.update(yDessin=150, cacheSel=['#detailPoster #dptTrace'], descendSel=[['#detailPoster #dptQui','#detailPoster #dptTitre','#detailPoster #dptQuand'], dy]); texte=yq+dy
            else:
                yti=pg.evaluate(YTOP,'#dptTitre'); dy=round(sousDeploi-yti)
                base.update(yDessin=108, petit=1, seulTitre=[round(trait)+2, dy], cacheSel=['#detailPoster #dptQuand','#detailPoster #dptQui']); texte=yti+dy
            C=[]
            def e(lab, nom, c):
                pg.evaluate("(c)=>{OV.montre(c)}", c); pg.wait_for_timeout(400); f=D+'%s-%s-%s.png'%(nat,nom,th); pg.screenshot(path=f, clip=clip)
                pr=pg.evaluate("()=>OV.preuve()"); dans=pr['haut']<trait
                m=dict(trait=trait, haut=pr['haut'], bas=pr['bas'], texte=texte)
                cap='%d outils, de y %d à %d · bas du trait %d · %s · premier texte à %d'%(pr['n'], round(pr['haut']), round(pr['bas']), round(trait), ('AUCUN OUTIL DANS LA BANDE' if not dans else '⚠ UN OUTIL DANS LA BANDE'), round(texte))
                print('  ',nat,th,nom,cap, '| recouvre le texte :', pr['bas']>texte); C.append((lab,cap,f,m))
            e('1 · mode dessin — trait E1','1E1', dict(base, effile='E1'))
            e('1 · mode dessin — trait E2','1E2', dict(base, effile='E2'))
            e('2 · les tailles déployées','2', dict(base, effile='E2', etat='tailles', taille=1))
            e('3 · les couleurs déployées — S1','3S1', dict(base, effile='E2', sel='couleur', symbole='S1', etat='couleur', onglet='TRAIT', tonChoisi=4))
            e('3 · les couleurs déployées — S2','3S2', dict(base, effile='E2', sel='couleur', symbole='S2', etat='couleur', onglet='TRAIT', tonChoisi=4))
            pg.evaluate("()=>OV.nettoie()"); TOUT[(nat,th)]=C
            tn='clair' if th=='light' else 'sombre'
            sous='rangée A sous le trait, à %d pt · tailles et couleurs sous la rangée · %s · tout revient à POSER ou à la sortie'%(ECART, ('les trois lignes descendent de %d pt, espacements gardés'%dy) if nat=='promi' else ('tout est masqué sous la bande sauf le titre (descendu de %d pt)'%dy))
            planche('C-042 · le mode dessin — %s, %s'%(NOM[nat],tn), sous, C, 5, 'planche-v130/dessin-%s-%s.png'%(nat,tn), th=='dark')
            planche('C-042 · %s, %s'%(NOM[nat],tn), sous[:92], C, 2, 'planche-v130/dessin-%s-%s-telephone.png'%(nat,tn), th=='dark')
        ctx.close()
    b.close()
