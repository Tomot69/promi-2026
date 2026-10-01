from playwright.sync_api import sync_playwright
from importlib.machinery import SourceFileLoader
R="/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026"
J=SourceFileLoader("j",R+"/releve-S3-page-plus.py").load_module()
OK=[]
def t(n,c,d=''): OK.append((n,'OK' if c else 'KO',d))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda x: er.append(str(x)))
    pg.goto('file://'+R+'/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate(J.SCENE,'pp_promi_rachel'); pg.wait_for_timeout(1400)
    home=pg.evaluate("()=>['fWho','dueChips','nueeChips','fNote','csFiles','impSeg','urgSeg'].map(i=>{var e=document.getElementById(i);return i+':'+(e&&e.parentElement?(e.parentElement.id||e.parentElement.className||'?'):'ABSENT');})")
    # ouverture par le VRAI geste : un clic sur la barre
    pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1500)
    t('la barre ouvre Peaufiner', pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-peauf')"))
    t('sept réglages bâtis', pg.evaluate("()=>document.querySelectorAll('#createSheet .s2-liste .s2-reg').length")==7,
      str(pg.evaluate("()=>document.querySelectorAll('#createSheet .s2-liste .s2-reg').length")))
    t('pas d\'icône Partager (§3.2)', not pg.evaluate("()=>!!document.querySelector('#csBotBar .dpd-part,#csBotBar .cbb-part')"))
    t('la barre est clouée à 760', abs(pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
      const b=document.getElementById('csBotBar').getBoundingClientRect();return (b.top-d.top)/(d.width/390);}""")-760)<2)
    t('rien ne passe AU-DESSUS de la barre', pg.evaluate("""()=>{const bar=document.getElementById('csBotBar');
      const zb=+getComputedStyle(bar).zIndex||0;const c=document.querySelector('#createSheet>.dpd-corps');
      return zb > (+getComputedStyle(c).zIndex||0);}"""))
    t('rien ne déborde du cadre', pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
      let n=[];document.querySelectorAll('#createSheet .s2-liste *').forEach(e=>{const r=e.getBoundingClientRect();
        if(r.width<2||r.height<2)return;if(r.right>d.right+2||r.left<d.left-2)n.push(e.className);});return n.slice(0,3);}""")==[])
    # refermeture
    pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1500)
    t('la barre referme Peaufiner', not pg.evaluate("()=>document.getElementById('createSheet').classList.contains('pp-peauf')"))
    home2=pg.evaluate("()=>['fWho','dueChips','nueeChips','fNote','csFiles','impSeg','urgSeg'].map(i=>{var e=document.getElementById(i);return i+':'+(e&&e.parentElement?(e.parentElement.id||e.parentElement.className||'?'):'ABSENT');})")
    t('tous les contrôles sont rentrés chez eux', home==home2, '\n     avant=%s\n     apres=%s'%(home,home2))
    t('la phrase est revenue', pg.evaluate("()=>{const e=document.querySelector('.pp-phrase');return !!e&&getComputedStyle(e).display!=='none';}"))
    t('le mot de trace est revenu', pg.evaluate("()=>{const e=document.querySelector('.pp-trace');return !!e&&getComputedStyle(e).display!=='none';}"))
    t('aucune erreur JS', not er, str(er[:2]))
    b.close()
for n,s,d in OK: print('%-42s %s  %s'%(n,s,d))
print('\n%d/%d'%(sum(1 for _,s,_ in OK if s=='OK'), len(OK)))
