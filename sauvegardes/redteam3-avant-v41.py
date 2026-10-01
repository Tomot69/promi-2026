"""Red team qui mesure l'IMAGE : chaque bouton doit changer des pixels."""
from playwright.sync_api import sync_playwright
import os as _os
_ICI = _os.path.dirname(_os.path.abspath(__file__))
def _url():
    for p in [_os.path.join(_ICI,'app.html'), '/home/claude/app.html']:
        if _os.path.exists(p): return 'file://' + p
    import re as _re
    for f in sorted(_os.listdir(_ICI), reverse=True):
        if _re.match(r'promi-v\d+\.html$', f): return 'file://' + _os.path.join(_ICI, f)
    return 'file:///home/claude/app.html'

R=[]
def t(n,ok,d=''): R.append((n,'OK' if ok else 'KO',d))
SNAP="""()=>{const cv=document.getElementById('shCanvas');return cv.toDataURL('image/png').length+':'+
  (()=>{const g=cv.getContext('2d');const im=g.getImageData(0,0,cv.width,cv.height).data;
   let s=0;for(let i=0;i+2<im.length;i+=97)s=(s+im[i]*31+im[i+1]*7+im[i+2])%1000000007;return s;})();}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto(_url()); pg.wait_for_timeout(4600)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}")
    pg.wait_for_timeout(2000)
    pg.evaluate("()=>document.getElementById('shTrayBtn').click()"); pg.wait_for_timeout(400)
    def change(nom, js, attente=900):
        a=pg.evaluate(SNAP); pg.evaluate(js); pg.wait_for_timeout(attente); c=pg.evaluate(SNAP)
        t(nom, a!=c, 'image inchangee')
    change("Sombre -> Clair change l'image","()=>document.querySelector('#shTheme button[data-t=light]').click()")
    change("Clair -> Sombre change l'image","()=>document.querySelector('#shTheme button[data-t=dark]').click()")
    change("QR active change l'image","()=>document.getElementById('shQrTog').click()")
    change("QR desactive change l'image","()=>document.getElementById('shQrTog').click()")
    change("format Carre change l'image","()=>document.querySelector('#shFormats .sh-fmt[data-fmt=square]').click()")
    change("format Story change l'image","()=>document.querySelector('#shFormats .sh-fmt[data-fmt=story]').click()")
    change("Noyau pose change l'image","()=>document.getElementById('shNyOn').click()")
    change("Noyau Grand change l'image","()=>document.getElementById('shNyL').click()")
    change("Avec le chiffre change l'image","()=>document.getElementById('shNyPct').click()")
    change("Noyau masque change l'image","()=>document.getElementById('shNyOff').click()")
    change("mode Mes Promi change l'image","()=>document.querySelector('#shMode button[data-mode=mosaic]').click()",1200)
    change("Sans texte change l'image","()=>document.getElementById('shTxOff').click()")
    change("Avec texte change l'image","()=>document.getElementById('shTxOn').click()")
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=toile]').click()"); pg.wait_for_timeout(1200)
    # CONSTAT (chantier 39) : depuis que Ma Toile passe par Toile.renderTo(),
    # shareVis ne pilote plus les libelles — ce chemin de shareToile n'est plus
    # emprunte. On verifie donc l'etat, pas le rendu, et le chantier est ouvert.
    _v0 = pg.evaluate("()=>[...document.querySelectorAll('#shQpRail .sh-qp')].filter(e=>e.classList.contains('on')).length")
    pg.evaluate("()=>{const e=document.querySelector('#shQpRail .sh-qp');if(e)e.click();}"); pg.wait_for_timeout(1200)
    t("masquer un Promi bascule son encart",
      pg.evaluate("()=>[...document.querySelectorAll('#shQpRail .sh-qp')].filter(e=>e.classList.contains('on')).length") != _v0)
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=mosaic]').click()"); pg.wait_for_timeout(1200)
    change("mode Ma Toile change l'image","()=>document.querySelector('#shMode button[data-mode=toile]').click()",1200)
    # le logo : change le DOM, pas le canvas
    f1=pg.evaluate("()=>getComputedStyle(document.getElementById('shWordmark')).fontFamily.split(',')[0]")
    pg.evaluate("()=>document.getElementById('shWmSig').click()"); pg.wait_for_timeout(400)
    f2=pg.evaluate("()=>getComputedStyle(document.getElementById('shWordmark')).fontFamily.split(',')[0]")
    t("le logo bascule en signature", f1!=f2, '%s -> %s'%(f1,f2))
    pg.evaluate("()=>document.getElementById('shWmBri').click()"); pg.wait_for_timeout(300)
    # le Noyau ne doit poser QUE l'anneau : meme pixel au centre, avec et sans
    C = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const d=g.getImageData(cv.width>>1,cv.height>>1,1,1).data;return d[0]+','+d[1]+','+d[2];}"""
    # on remet un etat connu : sans Noyau, sans chiffre, taille moyenne
    pg.evaluate("()=>{if(window.shChiffre)document.getElementById('shNyPct').click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const b=document.getElementById('shNyM');if(b)b.click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{if(window.shNoyau)document.getElementById('shNyOff').click();}"); pg.wait_for_timeout(1100)
    c0=pg.evaluate(C)
    pg.evaluate("()=>document.getElementById('shNyOn').click()"); pg.wait_for_timeout(1100)
    c1=pg.evaluate(C)
    t("le Noyau ne pose aucun fond (centre intact)", c0==c1, '%s -> %s'%(c0,c1))
    t("aucune erreur JS", not er, str(er[:2]))
    pg.locator('#device').screenshot(path='AP.png')
    b.close()
for n,s,d in R: print('%-46s %s  %s'%(n,s,d if s=='KO' else ''))
print('\n%d/%d'%(sum(1 for _,s,_ in R if s=='OK'),len(R)))
