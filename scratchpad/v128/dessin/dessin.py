# PLANCHE C-042 (v128) — LE PARCOURS de l'outil de dessin, posé par-dessus l'app rendue. Rien n'est construit dans l'app. @3x.
import sys, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
clip={'x':20,'y':44,'width':390,'height':844}; D='scratchpad/v128/dessin/'
PEN=open(D+'pen.js',encoding='utf-8').read(); OV=open(D+'ov.js',encoding='utf-8').read()
FICHES={'promi':"()=>{closeAll(); const p=promises.filter(q=>q.title==='faire les crêpes')[0]; openDetail(p.id);}", 'cercle':"()=>{closeAll(); openEssaim('potager');}"}
GEO={'promi':dict(yRow=316,yBande=186,yDessin=150,cacheBas=[311,368]), 'cercle':dict(yRow=200,yBande=104,yDessin=128,petit=1,descend=['#detailPoster .ov-bas',56])}
OEIL={'promi':[24,204],'cercle':[24,106]}
MARQUE = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); const P=document.getElementById('detailPoster'); let n=0;
  [...P.querySelectorAll('*')].forEach(e=>{ if(e.closest('.ov-bas')||e.tagName==='CANVAS') return; const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); if(r.height<8||r.width<8||cs.position==='static') return; const y=r.top-dv.top;
    if(y>=205 && y<760 && r.bottom-dv.top<=765 && !/peauf|dpd|barre/i.test(e.className+' '+e.id)){ e.classList.add('ov-bas'); n++; } }); return n; }"""
BOUTON = "()=>{const dv=document.getElementById('device').getBoundingClientRect(); const e=[...document.querySelectorAll('.ph-photo-btn')].filter(x=>{const r=x.getBoundingClientRect(); return r.width>0&&r.top>dv.top&&r.bottom<dv.bottom&&getComputedStyle(x).visibility!=='hidden';}).pop(); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left-dv.left, r.top-dv.top, r.width]}"
def prise(pg, nom):
    pg.wait_for_timeout(350); f=D+nom+'.png'; pg.screenshot(path=f, clip=clip); return f
def planche(titre, cases, cols, sortie, sombre=False):
    ims=[(t,Image.open(f).convert('RGB')) for t,f in cases]; w,h=ims[0][1].size; M=54; T=100; H0=160
    rows=(len(ims)+cols-1)//cols; bg=(240,236,226) if not sombre else (28,24,20); enc=(32,25,8) if not sombre else (247,240,222)
    P=Image.new('RGB',(M+cols*(w+M), H0+rows*(h+T+M)), bg); d=ImageDraw.Draw(P)
    try: ft=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',52); fg=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',70)
    except Exception: ft=fg=None
    d.text((M,46),titre,fill=enc,font=fg)
    for i,(t,im) in enumerate(ims):
        x=M+(i%cols)*(w+M); y=H0+(i//cols)*(h+T+M); d.text((x,y+24),t,fill=enc,font=ft); P.paste(im,(x,y+T))
    P.save(sortie); print(sortie, P.size)
def parcours(pg, nat, th, seulement=None):
    pg.evaluate("()=>OV.nettoie()"); pg.evaluate(FICHES[nat]); pg.wait_for_timeout(3000)
    if nat=='cercle': pg.evaluate(MARQUE)
    L=(th=='light'); bt=pg.evaluate(BOUTON); mock=None
    if not bt: mock=[332, OEIL[nat][1]]; bt=[332, OEIL[nat][1], 34]; print(nat, ': aucun bouton photo sur cette fiche aujourd\'hui — il est posé par la planche (élément à créer)')
    C=[]; base=dict(nat=nat, light=L)
    if mock: base['photoMock']=mock
    mode=dict(base); mode.update(GEO[nat]); mode.update(sansDalle=1, cachePhoto=1, dessin='simple', sel='plume'); mode.pop('photoMock',None)
    def e(lab, nom, c):
        if seulement and nom not in seulement: return
        pg.evaluate("(c)=>{OV.montre(c)}", c); C.append((lab, prise(pg,'%s-%s-%s'%(nat,nom,th))))
    def sansB(c): c=dict(c); c.pop('cacheBas',None); c.pop('descend',None); return c
    e('1 · la fiche, avant — le bouton photo','1', dict(base, fleche=[bt[0]+bt[2]/2, bt[1]+bt[2]/2]))
    e('2 · le menu, compact — « Dessiner » en tête','2', dict(base, menu=dict(x=366, y=max(106,bt[1]-115), items=['Dessiner','Importer une image','La dalle d’origine'])))
    e('3 · le mode dessin — rangée A (sous la bande)','3A', dict(mode, compo='A'))
    e('3 · rangée B (au bas de la bande)','3B', sansB(dict(mode, compo='B')))
    e('3 · rangée C (icônes + mots, glisse)','3C', dict(mode, compo='C'))
    e('4 · la taille déployée','4', dict(mode, compo='A', etat='tailles', taille=1))
    e('5 · la couleur déployée — S1','5S1', dict(mode, compo='A', sel='couleur', symbole='S1', etat='couleur', onglet='TRAIT', tonChoisi=4))
    e('5 · la couleur déployée — S2','5S2', dict(mode, compo='A', sel='couleur', symbole='S2', etat='couleur', onglet='TRAIT', tonChoisi=4))
    e('6 · un mot et un dessin — effilé E1','6E1', dict(mode, compo='A', effile='E1'))
    e('6 · un mot et un dessin — effilé E2','6E2', dict(mode, compo='A', effile='E2'))
    e('7 · après POSER : le dessin à la place de la dalle','7', dict(base, sansDalle=1, dessin='simple', yDessin=GEO[nat]['yDessin'], petit=GEO[nat].get('petit',0), oeil=OEIL[nat]+[0]))
    e('8 · dessin masqué : la dalle revient','8', dict(base, oeil=OEIL[nat]+[1]))
    pg.evaluate("()=>OV.nettoie()"); return C
with sync_playwright() as p:
    b=p.webkit.launch(); NOM={'promi':'fiche Promi','cercle':'fiche Cercle'}; SOMBRE=[]
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s')}catch(e){}"%th)
        pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR',str(e)[:160])); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{ if(document.documentElement.classList.contains('light')!==(t==='light')) setTheme(t) }catch(e){} }", th); pg.wait_for_timeout(900)
        pg.evaluate(PEN); pg.evaluate(OV)
        if th=='light':
            for nat in ('promi','cercle'):
                C=parcours(pg, nat, th)
                planche('C-042 · le parcours du dessin — %s (clair)'%NOM[nat], C, 4, 'planche-v128/dessin-parcours-%s.png'%nat)
                for k in range(4): planche('C-042 · %s · %d/4'%(NOM[nat],k+1), C[k*3:k*3+3], 3, 'planche-v128/dessin-parcours-%s-tel-%d.png'%(nat,k+1))
            print('pilule compacte reprise :', json.dumps(pg.evaluate("()=>window._ovChip"), ensure_ascii=False))
            pg.evaluate("()=>{OV.nettoie(); closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3800)
            q=pg.evaluate(BOUTON) or [332,154,34]
            pg.evaluate("(c)=>{OV.montre(c)}", dict(nat='promi', light=True, menu=dict(x=q[0]+q[2], y=max(56,q[1]-78), items=['Dessiner','Importer une image'])))
            PLUS=('la page + — « Dessiner » en tête', prise(pg,'plus-light'))
        else:
            for nat in ('promi','cercle'): SOMBRE += [('7 · %s, après POSER (sombre)'%NOM[nat], parcours(pg, nat, th, seulement=['7'])[0][1])]
        ctx.close()
    planche('C-042 · la page + et l\'écran 7 en sombre', [PLUS]+SOMBRE, 3, 'planche-v128/dessin-plus-et-sombre.png')
    b.close()
