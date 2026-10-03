import json
from PIL import Image, ImageDraw, ImageFont
A=json.load(open('scratchpad/v124/cotes-avant.json')); B=json.load(open('scratchpad/v124/cotes-apres.json'))
F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',38); f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',30)
S=3; L=1000; HALO=0.12*232.064   # l'étendue du halo au-delà de la silhouette (0,12 D)
out=Image.new('RGB',(2*(390*S+L),844*S+120),(255,255,255)); d=ImageDraw.Draw(out)
for i,th in enumerate(('clair','sombre')):
    im=Image.open('scratchpad/v124/aura-apres-%s.png'%th).convert('RGB'); x0=i*(390*S+L); out.paste(im,(x0,120))
    d.text((x0+10,30),'Aura · %s · 390 × 844 · après v124'%th,font=F,fill=(20,20,20))
    def C(D):
        s=D['silhouette (rayon 121)']; return {'plateau':D['plateau'][1], 'halo_h':s[0]-HALO+0.0, 'halo_b':s[1], 'ombre_h':D.get('ombre',D.get('flaque'))[0], 'ombre_b':D.get('ombre',D.get('flaque'))[1], 'bt_h':D['« Partager ma Pelote »'][0], 'bt_b':D['« Partager ma Pelote »'][1], 'ph_h':D['la phrase'][0], 'ph_b':D['la phrase'][1], 'nx_h':D['les Noyaux'][0], 'cpt_b':D['les chiffres'][1]}
    av=C(A['clair']); ap=C(B[th])   # avant : le clair de v122 (en sombre l'ombre était la flaque, d'une autre géométrie)
    G=[('bas de la Pelote → ombre','halo_b','ombre_h',-4),('ombre → « PARTAGER MA PELOTE »','ombre_b','bt_h',-4),('« PARTAGER » → la phrase','bt_b','ph_h',-4),('la phrase → ses disques','ph_b','nx_h',-4)]
    for j,(nom,x,y,dem) in enumerate(G):
        y1=120+ap[x]*S; y2=120+ap[y]*S; xx=x0+390*S-50-j*14
        for yy in (y1,y2): d.line([x0,yy,x0+390*S+40,yy],fill=(230,0,120),width=2)
        d.line([xx,y1,xx,y2],fill=(230,0,120),width=6)
        a_=av[y]-av[x]; b_=ap[y]-ap[x]; ty=(y1+y2)/2-40
        d.text((x0+390*S+60,ty),nom,font=F,fill=(20,20,20))
        d.text((x0+390*S+60,ty+46),'%.2f → %.2f pt  (demandé %+d, mesuré %+.2f)'%(a_,b_,dem,b_-a_),font=f,fill=(0,120,40) if abs((b_-a_)-dem)<0.05 else (200,0,0))
    yc=120+ap['cpt_b']*S; d.line([x0,yc,x0+390*S+40,yc],fill=(0,120,255),width=3)
    d.text((x0+390*S+60,yc-60),'bas de la ligne des chiffres : %.2f'%ap['cpt_b'],font=F,fill=(0,90,200))
    d.text((x0+390*S+60,yc-14),'(bas de l\'écran : 844 — il reste %.1f pt)'%(844-ap['cpt_b']),font=f,fill=(0,90,200))
out.save('planche-v124/aura-cotee.png'); print(out.size)
for k,(nom,x,y,dem) in enumerate(G): print('%-34s %7.2f → %7.2f  Δ %+.2f'%(nom, av[y]-av[x], C(B['clair'])[y]-C(B['clair'])[x], (C(B['clair'])[y]-C(B['clair'])[x])-(av[y]-av[x])))
