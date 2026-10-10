# -*- coding: utf-8 -*-
"""redteam_fourrure.py — v140 (Tom, 10 oct. 2026, C-083, RÉCIDIVE « la Pelote trop rase »).
« La fourrure telle qu'elle était avant les essais de halo : douce et soyeuse, avec la longueur, la densité et la souplesse d'alors. »
Référence : sauvegardes/app-avant-v114.html. Valeurs décidées EN DUR (celles d'avant v114) :
  densité ×1 (palier haut 110 000), poil ×1, reflet d'origine ; les pointes dépassent le rayon de la boule (116 pt).
Lu sur l'IMAGE rendue (WebKit, @3x, carte graphique), vue figée :
  A  l'app déclare les réglages décidés
  B  le poil se lit : le grain de l'intérieur (écart moyen de clarté à 1 pt) ≥ GRAIN_MIN
  C  la longueur : le contour moyen dépasse la boule d'au moins POINTE_MIN pt, et il est dentelé (écart-type ≥ DENT_MIN pt)
  D  pas d'anneau : entre la bande du bord (R−1 → contour) et l'intérieur voisin, ΔE médian ≤ 6
  E  rien autour : au-delà de R + 9 pt, la page (hors l'ombre, dessous)
Usage : python3 redteam_fourrure.py [fichier.html]   (rouge sur sauvegardes/app-avant-v140.html)"""
import sys, io, math
from playwright.sync_api import sync_playwright
from PIL import Image
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
R_PT=116.0; FACTEUR=1; EPAISSEUR=1; PALIER=110000
GRAIN_MIN=2.2; POINTE_MIN=1.2; DENT_MIN=0.35; DE_MAX=6.0
INIT="try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','%s');['tenir','chiche','planter','pelote','noyau','fil','studio-monde','studio-couleur','bande','dessin','aura-apparait'].forEach(function(k){localStorage.setItem('geste_vu_'+k,'1')});}catch(e){}"
def lab(c):
    def f(u):
        u/=255.0; return u/12.92 if u<=0.04045 else ((u+0.055)/1.055)**2.4
    r,g,b=[f(x) for x in c[:3]]; X=(r*0.4124+g*0.3576+b*0.1805)/0.95047; Y=r*0.2126+g*0.7152+b*0.0722; Z=(r*0.0193+g*0.1192+b*0.9505)/1.08883
    def h(t): return t**(1/3.0) if t>0.008856 else 7.787*t+16/116.0
    return (116*h(Y)-16, 500*(h(X)-h(Y)), 200*(h(Y)-h(Z)))
def de(a,b): A=lab(a);B=lab(b); return math.sqrt(sum((x-y)**2 for x,y in zip(A,B)))
ok=0; tot=0
def juge(nom,cond,det=''):
    global ok,tot; tot+=1; ok+=1 if cond else 0; print(('  ✅ ' if cond else '  ❌ ')+nom+(' — '+det if det else ''))
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3); ctx.add_init_script(INIT%th)
        pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} closeAll(); document.getElementById('souffleBtn').click();}"); pg.wait_for_timeout(7000)
        inf=pg.evaluate("()=>{try{_aura.fige(true);_aura.vue(0.3,0.2);}catch(e){} var c=document.getElementById('auBouleGL')||document.getElementById('auBoule'); var r=c.getBoundingClientRect(); var G=window._peloteReglage||{}; var d=document.getElementById('device').getBoundingClientRect(); return {gl:!!document.getElementById('auBouleGL'),r:[r.left,r.top,r.width,r.height],k:d.width/390,f:G.facteur,e:G.epaisseur,dx:!!G.doux,pal:(_aura.etat?_aura.etat().palier:null)}}")
        pg.wait_for_timeout(1500); r=inf['r']
        pg.screenshot(path='/tmp/_four.png',clip={'x':r[0]-12,'y':r[1]-12,'width':r[2]+24,'height':r[3]+24}); ctx.close()
        im=Image.open('/tmp/_four.png').convert('RGB'); W,H=im.size; px=im.load(); S=3*inf['k']; cx=W/2.0; cy=H/2.0; R=R_PT*S
        fond=px[3,H//2]   # le plateau passe dans le coin haut de la prise : le fond se lit au milieu du bord gauche
        print('—',th,'· carte graphique' if inf['gl'] else '· SECOURS')
        if th=='light': juge('A · les réglages décidés (densité ×1, poil ×1, reflet d’origine, palier 110 000)', inf['f']==FACTEUR and inf['e']==EPAISSEUR and not inf['dx'] and inf['pal']==PALIER, 'facteur %s, épaisseur %s, doux %s, palier %s'%(inf['f'],inf['e'],inf['dx'],inf['pal']))
        # B · le grain
        s=0;n=0
        for y in range(int(cy-0.55*R),int(cy+0.55*R),2):
            for x in range(int(cx-0.55*R),int(cx+0.55*R),2):
                if (x-cx)**2+(y-cy)**2>(0.55*R)**2: continue
                a=px[x,y]; c=px[x+3,y]; d=px[x,y+3]
                la=0.299*a[0]+0.587*a[1]+0.114*a[2]; s+=abs(la-(0.299*c[0]+0.587*c[1]+0.114*c[2]))+abs(la-(0.299*d[0]+0.587*d[1]+0.114*d[2])); n+=2
        g=s/n; juge('B · le poil se lit (grain ≥ %.1f)'%GRAIN_MIN, g>=GRAIN_MIN, 'grain %.2f'%g)
        # C · le contour, par angle (hors le bas, où l'ombre passe)
        rad=[]
        for k in range(360):
            an=math.radians(k); 
            if 55<k<125: continue
            rr=R*1.12
            while rr>R*0.9:
                x=int(cx+rr*math.cos(an)); y=int(cy+rr*math.sin(an))
                if 0<=x<W and 0<=y<H and de(px[x,y],fond)>12: break
                rr-=0.5
            rad.append(rr/S)
        m=sum(rad)/len(rad); sd=math.sqrt(sum((x-m)**2 for x in rad)/len(rad))
        juge('C · la longueur : les pointes dépassent la boule (≥ %.1f pt) et le contour est dentelé (≥ %.2f pt)'%(POINTE_MIN,DENT_MIN), m-R_PT>=POINTE_MIN and sd>=DENT_MIN, 'contour moyen %.2f pt (boule 116), dentelure %.2f pt, max %.1f'%(m,sd,max(rad)))
        # D · pas d'anneau
        D=[]
        for k in range(0,360,6):
            if 50<k<130: continue
            an=math.radians(k); A=[0,0,0];B=[0,0,0];na=nb=0
            for j in range(12):
                for (lo,hi,T) in ((R-3*S, R+1.0*S, 'a'),(R-16*S,R-8*S,'b')):
                    rr=lo+(hi-lo)*j/11.0; x=int(cx+rr*math.cos(an)); y=int(cy+rr*math.sin(an)); c=px[x,y]
                    if de(c,fond)<12: continue
                    if T=='a': A=[A[i]+c[i] for i in range(3)]; na+=1
                    else: B=[B[i]+c[i] for i in range(3)]; nb+=1
            if na and nb: D.append(de([v/na for v in A],[v/nb for v in B]))
        D.sort(); med=D[len(D)//2]
        juge('D · pas d’anneau au bord (ΔE médian ≤ %.0f)'%DE_MAX, med<=DE_MAX, 'ΔE médian %.1f, max %.1f'%(med,D[-1]))
        # E · rien autour
        mx=0
        for k in range(0,360,2):
            if 45<k<135: continue
            an=math.radians(k)
            for rr in (R+9*S,R+11*S):
                x=int(cx+rr*math.cos(an)); y=int(cy+rr*math.sin(an))
                if 0<=x<W and 0<=y<H: mx=max(mx,de(px[x,y],fond))
        juge('E · rien autour (au-delà de 9 pt, la page)', mx<=2.0, 'ΔE max %.1f'%mx)
    b.close()
print('\n%d / %d'%(ok,tot)); sys.exit(0 if ok==tot else 1)
