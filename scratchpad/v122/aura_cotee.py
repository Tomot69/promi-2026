# §3 — capture cotée de l'Aura à 390 × 844 (@3x), clair et sombre côte à côte, chaque écart annoté (avant → après, en pt)
import json
from PIL import Image, ImageDraw, ImageFont
A=json.load(open('scratchpad/v122/cotes-avant.json')); B=json.load(open('scratchpad/v122/cotes-apres.json'))
F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',38); f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
S=3; L=900
out=Image.new('RGB',(2*(390*S+L),844*S+120),(255,255,255)); d=ImageDraw.Draw(out)
for i,th in enumerate(('clair','sombre')):
    im=Image.open('scratchpad/v122/aura-apres-%s.png'%th).convert('RGB'); x0=i*(390*S+L); out.paste(im,(x0,120))
    d.text((x0+10,30),'Aura · %s · 390 × 844 · halo 3 · après v122'%th,font=F,fill=(20,20,20))
    a,b=A[th],B[th]; om='ombre' if th=='clair' else 'flaque'
    G=[('plateau → silhouette','plateau',1,'silhouette (rayon 121)',0,-11),('Pelote → %s'%om,'silhouette (rayon 121)',1,om,0,-15),('%s → « Partager ma Pelote »'%om,om,0 if th=='sombre' else 1,'« Partager ma Pelote »',0,-12),('« Partager » → la phrase','« Partager ma Pelote »',1,'la phrase',0,-12)]
    for j,(nom,x,ix,y,iy,dem) in enumerate(G):
        y1=120+b[x][ix]*S; y2=120+b[y][iy]*S; xx=x0+390*S-60-j*14
        for yy in (y1,y2): d.line([x0,yy,x0+390*S+40,yy],fill=(230,0,120),width=2)
        d.line([xx,y1,xx,y2],fill=(230,0,120),width=6)
        av=a[y][iy]-a[x][ix]; ap=b[y][iy]-b[x][ix]
        ty=(y1+y2)/2-40
        d.text((x0+390*S+60,ty),nom,font=F,fill=(20,20,20))
        d.text((x0+390*S+60,ty+46),'%.2f → %.2f pt  (demandé %+d, mesuré %+.2f)'%(av,ap,dem,ap-av),font=f,fill=(0,120,40) if abs((ap-av)-dem)<0.05 else (200,0,0))
    d.line([x0,120+b['halo (canevas)'][0]*S,x0+390*S,120+b['halo (canevas)'][0]*S],fill=(0,120,255),width=2)
    d.text((x0+390*S+60,120+b['plateau'][1]*S-10),'bas du plateau 100,00 · haut du canevas du halo %.2f (le halo peint commence à 110,7)'%b['halo (canevas)'][0],font=f,fill=(0,90,200))
out.save('planche-v122/aura-cotee.png'); print(out.size)
