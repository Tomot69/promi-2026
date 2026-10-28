import sys; sys.path.insert(0,'scratchpad/v146/trace')
import numpy as np, squelette as S
from fontTools.ttLib import TTFont
F=TTFont('Polices Promi/PromiLate-Regular.otf'); cm=F.getBestCmap()
def encre(ch):
    cts=S.contours(F, cm[ord(ch)]); img,x0,y1=S.image(cts); return img,x0,y1
def hruns(img,x0,y1,y):
    r=int(round((y1-y)/S.U)); 
    if r<0 or r>=img.shape[0]: return []
    row=img[r]; out=[]; i=0
    while i<len(row):
        if row[i]:
            j=i
            while j<len(row) and row[j]: j+=1
            out.append((round(x0+i*S.U),round(x0+j*S.U))); i=j
        else: i+=1
    return out
def vruns(img,x0,y1,x):
    c=int(round((x-x0)/S.U))
    if c<0 or c>=img.shape[1]: return []
    col=img[:,c]; out=[]; i=0
    while i<len(col):
        if col[i]:
            j=i
            while j<len(col) and col[j]: j+=1
            out.append((round(y1-j*S.U),round(y1-i*S.U))); i=j
        else: i+=1
    return out
if __name__=='__main__':
    for ch in sys.argv[1]:
        img,x0,y1=encre(ch); adv=F['hmtx'][cm[ord(ch)]][0]
        ys,xs=np.nonzero(img); print('==',ch,'adv',adv,'boite x',round(x0+xs.min()*S.U),round(x0+(xs.max()+1)*S.U),'y',round(y1-(ys.max()+1)*S.U),round(y1-ys.min()*S.U))
        for y in range(25,720,50): print('  y%4d'%y, hruns(img,x0,y1,y))
        for x in range(25,adv,50): print('  x%4d'%x, vruns(img,x0,y1,x))
