#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES HUIT MOTS DE LA PLANCHE DU LEXIQUE, EN VECTORIEL.
   Ce ne sont PAS des glyphes de police : ce sont huit DESSINS, assumés comme tels (Tom,
   17 septembre 2026). Un seul `<path>` par mot, `fill:currentColor`, aucun bitmap.

   La chaîne, et pourquoi chaque étape :
   1 · on prend la moitié CLAIRE de la planche — encre sombre sur crème, meilleur rapport
       signal/bruit que l'inverse ;
   2 · on suréchantillonne le NIVEAU DE GRIS (bicubique ×6) avant de seuiller : l'anticrénelage
       de la source porte une information SOUS-PIXEL, et la jeter d'abord donne un escalier ;
   3 · marching squares à l'iso-niveau 0,5, avec interpolation linéaire sur l'arête : le contour
       sort en coordonnées réelles, pas en coins de pixel ;
   4 · Douglas-Peucker, puis détection d'angle : un sommet dont le virage dépasse le seuil reste
       un COIN, le reste devient une courbe ;
   5 · Catmull-Rom → cubiques, un `C` par segment lisse, un `L` par coin.
"""
import numpy as np, math, json
from PIL import Image

SRC='/Users/macbookpro/Downloads/promi-lexique.png'
MOTS=['Promi','Le studio',"L'aura",'Fil','Index','Partager','Toile','Noyau']
CLE =['promi','studio','aura','fil','index','partager','toile','noyau']
SUR = 6           # facteur de suréchantillonnage
EPS = 0.55        # Douglas-Peucker, en pixels SOURCE
ANGLE = 62.0      # au-delà, c'est un coin

# ── marching squares, iso 0.5, ORIENTÉ : l'encre est TOUJOURS à GAUCHE du sens de marche ──
#    (repère écran, y vers le bas : la gauche d'un cap (dx,dy) est (dy,−dx))
#    Sans cette orientation, le chaînage fabrique des fragments : 50 contours pour « Promi »
#    au premier essai, là où le mot en a neuf.
def contours(g):
    H,W=g.shape
    def ip(pa,pb,va,vb):
        t=(0.5-va)/(vb-va) if vb!=va else 0.5
        return (pa[0]+(pb[0]-pa[0])*t, pa[1]+(pb[1]-pa[1])*t)
    TAB={1:[('L','T')],2:[('T','R')],4:[('R','B')],8:[('B','L')],
         3:[('L','R')],6:[('T','B')],12:[('R','L')],9:[('B','T')],
         7:[('L','B')],14:[('T','L')],13:[('R','T')],11:[('B','R')]}
    seg=[]
    for y in range(H-1):
        for x in range(W-1):
            va,vb,vc,vd=g[y,x],g[y,x+1],g[y+1,x+1],g[y+1,x]
            c=(va>0.5)*1+(vb>0.5)*2+(vc>0.5)*4+(vd>0.5)*8
            if c in (0,15): continue
            A,B,C,D=(x,y),(x+1,y),(x+1,y+1),(x,y+1)
            E={'T':ip(A,B,va,vb),'R':ip(B,C,vb,vc),'B':ip(C,D,vc,vd),'L':ip(D,A,vd,va)}
            if c==5:   par=[('T','R'),('B','L')] if (va+vb+vc+vd)/4>0.5 else [('L','T'),('R','B')]
            elif c==10:par=[('T','L'),('B','R')] if (va+vb+vc+vd)/4>0.5 else [('L','B'),('R','T')]
            else:      par=TAB[c]
            for u,v in par: seg.append((E[u],E[v]))
    K=lambda p:(round(p[0],4),round(p[1],4))
    depart={}
    for s,e in seg: depart.setdefault(K(s),[]).append((K(e),s,e))
    loops=[]; pris=set()
    for s,e in seg:
        ks=K(s)
        if ks in pris: continue
        boucle=[s]; cur=K(e); pris.add(ks); dep=ks
        garde=0
        while cur!=dep and garde<400000:
            garde+=1
            cand=[t for t in depart.get(cur,[]) if t[0] not in pris or t[0]==dep]
            if not cand: break
            nk,ps,pe=cand[0]
            boucle.append(ps); pris.add(cur); cur=nk
        if cur==dep and len(boucle)>=6:
            boucle.append(boucle[0]); loops.append(boucle)
    return loops

def rdp(pts,eps):
    if len(pts)<3: return pts
    def d(p,a,b):
        dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy)
        if L<1e-9: return math.hypot(p[0]-a[0],p[1]-a[1])
        return abs(dy*(p[0]-a[0])-dx*(p[1]-a[1]))/L
    dm,im=0,0
    for i in range(1,len(pts)-1):
        dd=d(pts[i],pts[0],pts[-1])
        if dd>dm: dm,im=dd,i
    if dm>eps:
        return rdp(pts[:im+1],eps)[:-1]+rdp(pts[im:],eps)
    return [pts[0],pts[-1]]

def chemin(loop, ech, eps, angle):
    p=[(x/ech,y/ech) for x,y in loop]
    if p[0]!=p[-1]: p.append(p[0])
    p=rdp(p,eps)
    if len(p)<4: return ''
    if p[0]==p[-1]: p=p[:-1]
    n=len(p)
    coin=[False]*n
    for i in range(n):
        a,b,c=p[(i-1)%n],p[i],p[(i+1)%n]
        v1=(b[0]-a[0],b[1]-a[1]); v2=(c[0]-b[0],c[1]-b[1])
        n1=math.hypot(*v1); n2=math.hypot(*v2)
        if n1<1e-9 or n2<1e-9: continue
        cs=max(-1,min(1,(v1[0]*v2[0]+v1[1]*v2[1])/(n1*n2)))
        if math.degrees(math.acos(cs))>angle: coin[i]=True
    f=lambda v:('%.2f'%v).rstrip('0').rstrip('.')
    d=['M%s %s'%(f(p[0][0]),f(p[0][1]))]
    for i in range(n):
        a,b=p[i],p[(i+1)%n]
        if coin[i] or coin[(i+1)%n]:
            d.append('L%s %s'%(f(b[0]),f(b[1]))); continue
        p0,p3=p[(i-1)%n],p[(i+2)%n]
        c1=(a[0]+(b[0]-p0[0])/6.0, a[1]+(b[1]-p0[1])/6.0)
        c2=(b[0]-(p3[0]-a[0])/6.0, b[1]-(p3[1]-a[1])/6.0)
        d.append('C%s %s %s %s %s %s'%(f(c1[0]),f(c1[1]),f(c2[0]),f(c2[1]),f(b[0]),f(b[1])))
    d.append('Z')
    return ''.join(d)

def aire(loop):
    s=0.0
    for i in range(len(loop)-1):
        s+=loop[i][0]*loop[i+1][1]-loop[i+1][0]*loop[i][1]
    return abs(s)/2

if __name__=='__main__':
    im=Image.open(SRC).convert('L'); a=np.asarray(im,dtype=float)
    clair=a[:709]
    encre=(clair<128)
    rows=encre.sum(axis=1); bandes=[]; d0=None
    for y,v in enumerate(rows):
        if v>0 and d0 is None: d0=y
        elif v==0 and d0 is not None:
            if y-d0>12: bandes.append((d0,y))
            d0=None
    assert len(bandes)==8, len(bandes)
    jeu={}
    for (mot,cle,(y0,y1)) in zip(MOTS,CLE,bandes):
        seg=encre[y0:y1]; nz=np.nonzero(seg.sum(axis=0))[0]
        x0,x1=nz[0],nz[-1]+1
        M=3
        sub=clair[max(0,y0-M):y1+M, max(0,x0-M):x1+M]
        g=1.0-np.clip((sub-60.0)/(200.0-60.0),0,1)      # 1 = encre
        h,w=g.shape
        gi=np.asarray(Image.fromarray((g*255).astype(np.uint8)).resize((w*SUR,h*SUR),Image.BICUBIC),dtype=float)/255.0
        lps=[l for l in contours(gi) if aire(l)/(SUR*SUR) > 1.2]
        lps.sort(key=lambda l:-aire(l))
        if cle=='promi':
            # ⚑ LE « i » DE PROMI GARDE SA COULEUR D'ACCENT (Tom, comme sur la planche).
            #    C'est la SEULE exception au « un seul chemin par mot » : deux chemins, et le
            #    second est le i — sa hampe à queue et son point. On le reconnaît à sa place,
            #    pas à un indice : tout contour dont le bord gauche passe 0,82 × la largeur.
            seuil = w*0.82
            estI = lambda l: min(pt[0] for pt in l)/SUR >= seuil
            di = ''.join(chemin(l,SUR,EPS,ANGLE) for l in lps if estI(l))
            dd = ''.join(chemin(l,SUR,EPS,ANGLE) for l in lps if not estI(l))
            jeu[cle]={'mot':mot,'w':round(w,2),'h':round(h,2),'d':dd,'d_i':di,
                      'contours':len(lps),'pts':(dd+di).count('C')+(dd+di).count('L')}
        else:
            dd=''.join(chemin(l,SUR,EPS,ANGLE) for l in lps)
            jeu[cle]={'mot':mot,'w':round(w,2),'h':round(h,2),'d':dd,
                      'contours':len(lps),'pts':dd.count('C')+dd.count('L')}
        e_=jeu[cle]; print(f"  {mot:12} {w:4}×{h:3} px source · {len(lps):3} contours · {e_['pts']:4} segments · {len(e_['d'])+len(e_.get('d_i','')):6} car." + ('   (+ le i, à part)' if 'd_i' in e_ else ''))
    json.dump(jeu,open('scratchpad/lexique_svg.json','w'),ensure_ascii=False)
    print('\n→ scratchpad/lexique_svg.json')
