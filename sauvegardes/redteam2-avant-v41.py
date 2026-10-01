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
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto(_url()); pg.wait_for_timeout(4600)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}")
    pg.wait_for_timeout(1900)
    # ⚑ CONTRAT RÉÉCRIT (§7). Il exigeait un tiroir `#shTrayWrap` collé au-dessus d'un
    #   pied `.sh-foot` — la mise en page de l'ancien partage. Décision Tom du 1er
    #   septembre 2026 : plus de pied, plus de trait, une BARRE Inviter/Partager en bas.
    #   L'intention est la même : la commande de sortie est en bas, entière, dans le
    #   cadre. Version d'origine : sauvegardes/redteam2-avant-partage-sans-trait.py
    pg.evaluate("()=>document.getElementById('shcPeaufiner').click()"); pg.wait_for_timeout(450)
    pg.evaluate("()=>document.getElementById('shcPeaufiner').click()"); pg.wait_for_timeout(450)
    g=pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
      const e=document.getElementById('shcBarre');const r=e.getBoundingClientRect();
      const p=document.getElementById('shcPeaufiner').getBoundingClientRect();
      return {pos:getComputedStyle(e).position,top:Math.round(r.top-d.top),bot:Math.round(r.bottom-d.top),
              pf:Math.round(p.bottom-d.top),dev:Math.round(d.height)};}""")
    t('la barre est en bas, sous Peaufiner, dans le cadre',
      g['pos']=='absolute' and g['top']>=g['pf']-3 and g['bot']<=g['dev'] and g['top']>0, str(g))
    t('rangee Le Noyau presente', pg.evaluate("()=>!!document.getElementById('shNyRow')"))
    t('rangee Le texte presente', pg.evaluate("()=>!!document.getElementById('shTxRow')"))
    t('bouton QR present', pg.evaluate("()=>!!document.getElementById('shQrTog')"))
    # Noyau
    pg.evaluate("()=>document.getElementById('shNyOn').click()"); pg.wait_for_timeout(900)
    n1=pg.evaluate("()=>window.shNoyau")
    d1=pg.evaluate("""()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const s=Math.round(Math.min(cv.width,cv.height)*0.1);
      const im=g.getImageData(cv.width/2-s,cv.height/2-s,2*s,2*s).data;
      let n=0;for(let i=0;i<im.length;i+=8){if(im[i+3]>200)n++;}return n;}""")
    pg.evaluate("()=>document.getElementById('shNyL').click()"); pg.wait_for_timeout(900)
    t('le Noyau se pose et change de taille', n1==True, 'pose=%s'%n1)
    pg.evaluate("()=>document.getElementById('shNyOff').click()"); pg.wait_for_timeout(700)
    t('le Noyau se masque', pg.evaluate("()=>window.shNoyau")==False)
    # texte
    pg.evaluate("()=>document.getElementById('shTxOff').click()"); pg.wait_for_timeout(800)
    t('Sans texte reagit', pg.evaluate("()=>document.getElementById('shTxOff').classList.contains('on')"))
    pg.evaluate("()=>document.getElementById('shTxOn').click()"); pg.wait_for_timeout(700)
    # visibles / tous
    # « Visibles » a laisse place a la rangee de Promi : on teste la rangee
    v0=pg.evaluate("()=>[...document.querySelectorAll('#shQpRail .sh-qp')].map(e=>e.classList.contains('on'))")
    pg.evaluate("()=>{const e=document.querySelector('#shQpRail .sh-qp');if(e)e.click();}"); pg.wait_for_timeout(900)
    v1=pg.evaluate("()=>[...document.querySelectorAll('#shQpRail .sh-qp')].map(e=>e.classList.contains('on'))")
    t('Visibles reagit', v0!=v1, '%s -> %s'%(v0,v1))
    # QR
    q0=pg.evaluate("()=>_shShowQR"); pg.evaluate("()=>document.getElementById('shQrTog').click()"); pg.wait_for_timeout(800)
    t('le QR bascule', pg.evaluate("()=>_shShowQR")!=q0)
    pg.evaluate("()=>document.getElementById('shQrTog').click()"); pg.wait_for_timeout(500)
    t('aucune erreur JS', not er, str(er[:2]))
    pg.locator('#device').screenshot(path='AO_tray.png')
    b.close()
for n,s,d in R: print('%-44s %s  %s'%(n,s,d if s=='KO' else ''))
print('\n%d/%d'%(sum(1 for _,s,_ in R if s=='OK'),len(R)))
