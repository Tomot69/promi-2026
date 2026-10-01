#!/usr/bin/env python3
"""LA PREUVE EN PIXELS DE L'EMPREINTE — on ne mesure QUE les images rendues.

La MEME scene, les DEUX lois, trois pressions. Le temoin « cloche » est
l'ANCIEN modele (la gaussienne) : c'est contre lui que le plateau se prouve.
Sa tache ne grandit pas avec la pression — c'est ce qu'on lui reproche.

⚠ DEUX PIEGES D'INSTRUMENT PAYES ICI.
1 · Ma premiere sonde cherchait de l'ENCRE PERDUE au coeur du contact. Elle
    n'en trouvait pas et annoncait « fond plat : 0 px » sur un plateau
    parfaitement plat. La cause n'etait pas le modele : le plateau, etant PLAN
    et face a la lumiere, en GAGNE. On mesure l'ecart SIGNE.
2 · L'ecart brut entre deux images est domine par LE GRAIN — un fil deplace
    d'un pixel donne un couple +200/-200, quand la forme de l'empreinte vaut
    20 a 50. On lisse sur 13 px avant de profiler. C'est le grain qu'on
    retire, jamais la forme.
"""
import os, math, sys, json
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np

DOSS='scratchpad/empp'; os.makedirs(DOSS,exist_ok=True)
CAS=['plateau14','plateau55','plateau100','cloche14','cloche55','cloche100']

def rendre():
    with sync_playwright() as p:
        b=p.chromium.launch()
        pg=b.new_page(viewport={'width':520,'height':900}, device_scale_factor=1)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:8752/scratchpad/mesure_pav.html')
        pg.wait_for_function("()=>window.__pret===true", timeout=180000)
        pg.wait_for_timeout(400)
        if errs: print("ERREURS PAGE :", errs[:4])
        for cv in pg.query_selector_all('canvas[data-cad]'):
            n=cv.get_attribute('data-cad')
            cv.scroll_into_view_if_needed(); pg.wait_for_timeout(80)
            cv.screenshot(path='%s/%s.png'%(DOSS,n))
        json.dump(pg.evaluate("()=>window.__emp"), open(DOSS+'/_emp.json','w'))
        b.close()

def lum(n): return np.asarray(Image.open('%s/%s.png'%(DOSS,n)).convert('L'),dtype=np.float64)
def flou(a,r):
    c=np.cumsum(np.pad(a,((r+1,r),(0,0))),axis=0); a=(c[2*r+1:]-c[:-(2*r+1)])/(2*r+1)
    c=np.cumsum(np.pad(a,((0,0),(r+1,r))),axis=1); return (c[:,2*r+1:]-c[:,:-(2*r+1)])/(2*r+1)

def coupe(d, cx, cy, ux, uy, demi, pas=1.0, larg=9):
    """profil EN LIGNE DROITE, signe, moyenne sur une bande de `larg` px."""
    H,W=d.shape; xs=[]; vs=[]
    vx,vy=-uy,ux
    n=int(demi/pas)
    for i in range(-n,n+1):
        t=i*pas; acc=[]
        for j in range(-(larg//2),larg//2+1):
            X=cx+ux*t+vx*j; Y=cy+uy*t+vy*j
            xi,yi=int(round(X)),int(round(Y))
            if 0<=xi<W and 0<=yi<H: acc.append(d[yi,xi])
        if acc: xs.append(t); vs.append(sum(acc)/len(acc))
    return np.array(xs), np.array(vs)

def lire(x,v,fen=None):
    """Les marqueurs, lus SUR LA COUPE, normalises par l'AMPLITUDE du profil.

    ⚠ Ma version precedente normalisait par la valeur AU CENTRE. Sur un
    plateau cette valeur vaut zero — c'est exactement ce qu'on cherche a
    prouver — et toutes les mesures partaient a 300 %. Le bon repere est
    l'amplitude, pas le coeur.

    Le marqueur qui separe vraiment les deux lois : LE RAYON DU COEUR INTACT.
    Une pulpe a une zone de contact ou RIEN ne bouge (elle adhere, elle
    translate) : ce rayon existe et il GRANDIT avec la pression. Une cloche
    n'en a pas : elle creuse des le centre, a toutes les pressions."""
    amp=np.max(np.abs(v)); i0=int(np.argmin(np.abs(x)))
    # 1 · LE FOND PLAT : le plus grand r ou le profil ne s'ECARTE PAS DE SA
    #     PROPRE VALEUR AU CENTRE de plus de 15 % de l'amplitude.
    #     ⚠ Ma version precedente exigeait un coeur A ZERO. C'etait vrai a
    #     faible enfoncement ; a 24,5 % du rayon, la PERSPECTIVE decale tout le
    #     plateau EN BLOC (le contact recule, donc son image se contracte de
    #     4 %) — le fond reste parfaitement plat, mais il n'est plus a zero.
    #     Ce qu'on veut mesurer est la PLATITUDE, pas le niveau.
    v0=float(np.mean(v[max(i0-2,0):i0+3]))
    r=0
    for k in range(0,min(i0,len(x)-i0)):
        if abs(v[i0-k]-v0)>0.15*amp or abs(v[i0+k]-v0)>0.15*amp: break
        r=abs(x[i0+k])
    # 2 · LA PLATITUDE dans une fenetre donnee (la meme pour les deux lois)
    f=fen if fen is not None else r
    sel=np.abs(x)<=max(f,1.0)
    plat=np.std(v[sel])/amp*100
    moy =np.mean(v[sel])/amp*100
    if fen is not None: r=r
    # 3 · LE BORD FRANC : la retombee du creux, mesuree DEPUIS SON EXTREMUM
    #     vers l'exterieur — 85 % -> 15 % de l'amplitude, en pixels.
    #     ⚠ Mesuree depuis le centre, elle donnait 0 px pour la cloche : son
    #     extremum EST au centre, donc a et b tombaient au meme endroit. On
    #     part de l'extremum, quel qu'il soit, dans les deux cas.
    ie=int(np.argmax(np.abs(v))); se=1.0 if v[ie]>0 else -1.0
    pas=+1 if x[ie]>=0 else -1
    a=b=None; k=ie
    while 0<=k<len(x):
        q=v[k]*se
        if a is None and q<0.85*amp: a=abs(x[k]-x[ie])
        if a is not None and q<0.15*amp: b=abs(x[k]-x[ie]); break
        k+=pas
    bord=(b-a) if (a is not None and b is not None) else float('nan')
    # 4 · LE BOURRELET : le lobe de signe oppose au creux, au-dela du bord
    hors=np.abs(x)>max(r,1.0)
    sgn=-1.0 if np.min(v[hors])<-np.max(v[hors]) else 1.0
    lobe=(np.max(v[hors]) if sgn<0 else np.min(v[hors]))/amp*100
    rl=abs(x[hors][int(np.argmax(v[hors]) if sgn<0 else np.argmin(v[hors]))])
    # symetrie : le profil est-il centre la ou le modele pose le contact ?
    w=np.abs(v); dec=float((x*w).sum()/max(w.sum(),1e-9))
    return dict(amp=amp,rcoeur=r,plat=plat,moy=moy,bord=bord,lobe=lobe,rlobe=rl,dec=dec)

def trace(C):
    Wp,Hp=1020,620
    img=Image.new('RGB',(Wp,Hp),(12,13,16)); px=img.load()
    COL={'plateau':(244,238,225),'cloche':(250,34,88)}
    ymax=max(np.max(np.abs(v)) for x,v in C.values())*1.14
    ox,oy,sw,sh=Wp//2,Hp//2,Wp-70,Hp//2-30
    for x in range(35,Wp-35): px[x,oy]=(58,56,50)
    for y in range(oy-sh,oy+sh): px[ox,y]=(58,56,50)
    for nom,(x,v) in C.items():
        fam='cloche' if nom.startswith('cloche') else 'plateau'
        ep={'14':0,'55':1,'100':2}[nom.replace(fam,'')]
        c=tuple(int(z*(0.36,0.64,1.0)[ep]) for z in COL[fam])
        prev=None
        for xx,vv in zip(x,v):
            X=ox+xx/120.0*(sw/2); Y=oy-vv/ymax*sh
            if prev:
                n=int(max(abs(X-prev[0]),abs(Y-prev[1])))+1
                for q in range(n+1):
                    a=int(prev[0]+(X-prev[0])*q/n); b=int(prev[1]+(Y-prev[1])*q/n)
                    if 0<=a<Wp and 0<=b<Hp:
                        for e in (-1,0,1):
                            if 0<=b+e<Hp: px[a,b+e]=c
            prev=(X,Y)
    img.save(DOSS+'/_profils.png')

if __name__=='__main__':
    if '--garde' not in sys.argv: rendre()
    EMP=json.load(open(DOSS+'/_emp.json'))
    rep=lum('repos'); C={}
    for n in CAS:
        e=EMP[n]; d=flou(lum(n)-rep,6)
        ux,uy=-e['uy'],e['ux']; nn=math.hypot(ux,uy); ux/=nn; uy/=nn
        C[n]=coupe(d,e['x'],e['y'],ux,uy,120)
    trace(C)
    L={n:lire(*C[n]) for n in CAS}
    # la platitude se compare DANS LA MEME FENETRE : celle du plateau
    for s in ('14','55','100'):
        f=L['plateau'+s]['rcoeur']
        L['cloche'+s+'_f']=lire(*C['cloche'+s],fen=f)
        L['plateau'+s+'_f']=L['plateau'+s]
    print()
    print("  MESURE SUR LES IMAGES RENDUES. Cadre 392 px, sphere 159 px de rayon,")
    print("  ECLAIRAGE PLAT (l'image est la densite projetee du semis, donc la")
    print("  geometrie). Coupe en travers du doigt, lissee sur 13 px.")
    print()
    print("  Le profil est-il centre la ou le modele pose le contact ?")
    print("     "+" · ".join("%s %+.1f px"%(n.replace('plateau','P').replace('cloche','C'),L[n]['dec']) for n in CAS))
    print()
    print("  1 · UN FOND PLAT, ET IL GRANDIT         rayon ou le profil ne bouge plus (<15 % de l'amplitude)")
    for f in ('plateau','cloche'):
        v=[L[f+s]['rcoeur'] for s in ('14','55','100')]
        x=("  ->  x%.2f"%(v[-1]/v[0])) if v[0]>0 else "   (aucun fond plat : elle creuse des le centre)"
        print("        %-8s  %s%s"%(f," -> ".join("%5.1f px"%z for z in v),x))
    print()
    print("  2 · LE FOND EST-IL PLAT ?               dans LA MEME fenetre, ecart-type / amplitude")
    for f in ('plateau','cloche'):
        print("        %-8s  %s"%(f," -> ".join("%5.1f %%"%L[f+s+'_f']['plat'] for s in ('14','55','100'))))
    print("        (et la moyenne)")
    for f in ('plateau','cloche'):
        print("        %-8s  %s"%(f," -> ".join("%+5.1f %%"%L[f+s+'_f']['moy'] for s in ('14','55','100'))))
    print()
    print("  3 · LE BORD EST-IL FRANC ?              largeur de la montee 15 % -> 85 %")
    for f in ('plateau','cloche'):
        print("        %-8s  %s"%(f," -> ".join("%5.1f px"%L[f+s]['bord'] for s in ('14','55','100'))))
    print()
    print("  4 · Y A-T-IL UN BOURRELET ?             lobe de signe oppose, au-dela du bord")
    for f in ('plateau','cloche'):
        print("        %-8s  %s"%(f," -> ".join("%+5.0f %% a %2.0f px"%(L[f+s]['lobe'],L[f+s]['rlobe']) for s in ('14','55','100'))))
    print()
    print("  profils traces dans %s/_profils.png"%DOSS)
