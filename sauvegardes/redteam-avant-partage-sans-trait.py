"""Red team complet de la page Partager : chaque bouton, chaque flux."""
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
def t(nom,ok,det=''): R.append((nom,'OK' if ok else 'KO',det))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto(_url()); pg.wait_for_timeout(4500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    O="()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}"
    pg.evaluate(O); pg.wait_for_timeout(1800)

    # alignements a gauche
    al=pg.evaluate("""()=>{const g=s=>{const e=document.querySelector(s);if(!e)return null;
      return Math.round(e.getBoundingClientRect().left);};
      return {titre:g('#shareScreen .scr-t'),tiroir:g('#shTray'),pied:g('#shareScreen .sh-fmtx'),
              image:g('#shPreviewArea')};}""")
    t('titres et blocs alignes a gauche', len(set(v for v in al.values() if v))<=2, str(al))

    # ⋯ ouvre / referme
    pg.evaluate("()=>document.getElementById('shTrayBtn').click()"); pg.wait_for_timeout(350)
    o1=pg.evaluate("()=>getComputedStyle(document.getElementById('shTrayWrap')).display")
    pg.evaluate("()=>document.getElementById('shTrayBtn').click()"); pg.wait_for_timeout(350)
    o2=pg.evaluate("()=>getComputedStyle(document.getElementById('shTrayWrap')).display")
    t('le ⋯ ouvre et referme', o1=='block' and o2=='none', o1+' / '+o2)

    # le libelle du format ouvre
    pg.evaluate("()=>document.getElementById('shFmtTxt').click()"); pg.wait_for_timeout(350)
    t('le libelle du format ouvre', pg.evaluate("()=>getComputedStyle(document.getElementById('shTrayWrap')).display")=='block')

    # un tap ailleurs referme
    pg.evaluate("()=>document.querySelector('#shareScreen .scr-t').click()"); pg.wait_for_timeout(350)
    t('un tap ailleurs referme', pg.evaluate("()=>getComputedStyle(document.getElementById('shTrayWrap')).display")=='none')

    # les modes
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=mosaic]').click()"); pg.wait_for_timeout(900)
    m1=pg.evaluate("()=>[shareMode,document.querySelector('#shMode button.on').dataset.mode]")
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=toile]').click()"); pg.wait_for_timeout(900)
    m2=pg.evaluate("()=>[shareMode,document.querySelector('#shMode button.on').dataset.mode]")
    t('les deux modes basculent et restent accordes', m1==['mosaic','mosaic'] and m2==['toile','toile'], str(m1)+' '+str(m2))

    # ouvrir le tiroir pour tester son contenu
    pg.evaluate("()=>document.getElementById('shTrayBtn').click()"); pg.wait_for_timeout(400)
    # theme de l'epreuve
    pg.evaluate("()=>document.querySelector('#shTheme button[data-t=light]').click()"); pg.wait_for_timeout(800)
    th=pg.evaluate("()=>document.querySelector('#shTheme button.on').dataset.t")
    t('Sombre / Clair de l epreuve', th=='light', th)
    pg.evaluate("()=>document.querySelector('#shTheme button[data-t=dark]').click()"); pg.wait_for_timeout(700)

    # QR
    q0=pg.evaluate("()=>_shShowQR")
    pg.evaluate("()=>document.getElementById('shQrTog').click()"); pg.wait_for_timeout(800)
    q1=pg.evaluate("()=>_shShowQR")
    t('le QR s active depuis le tiroir', q0==False and q1==True, '%s -> %s'%(q0,q1))
    pg.evaluate("()=>document.getElementById('shQrTog').click()"); pg.wait_for_timeout(600)

    # formats
    pg.evaluate("()=>document.querySelector('#shFormats .sh-fmt[data-fmt=square]').click()"); pg.wait_for_timeout(900)
    f=pg.evaluate("()=>[shareFmt,document.getElementById('shFmtTxt').textContent]")
    t('les formats changent et le pied suit', f[0]=='square' and 'Post' in f[1], str(f))
    pg.evaluate("()=>document.querySelector('#shFormats .sh-fmt[data-fmt=story]').click()"); pg.wait_for_timeout(800)

    # visibles / tous
    v0=pg.evaluate("()=>document.getElementById('shOptScope').classList.contains('on')")
    pg.evaluate("()=>document.getElementById('shOptScope').click()"); pg.wait_for_timeout(700)
    v1=pg.evaluate("()=>document.getElementById('shOptScope').classList.contains('on')")
    t('Visibles / Tous reagit', v0!=v1, '%s -> %s'%(v0,v1))

    # inviter et partager presents et cliquables
    t('Inviter present dans le tiroir', pg.evaluate("()=>{const e=document.getElementById('shInviteBtn');return !!e&&getComputedStyle(e).display!=='none';}"))
    t('le bouton rond relaie Partager', pg.evaluate("()=>{let n=0;const b=document.getElementById('shShareBtn');const o=b.onclick;b.onclick=function(){n++;};document.getElementById('shGo').click();b.onclick=o;return n>0;}"))

    # le mot-marque alterne
    f1=pg.evaluate("()=>getComputedStyle(document.getElementById('shWordmark')).fontFamily.split(',')[0]")
    pg.evaluate("()=>document.getElementById('shWordmark').click()"); pg.wait_for_timeout(400)
    f2=pg.evaluate("()=>getComputedStyle(document.getElementById('shWordmark')).fontFamily.split(',')[0]")
    t('le mot-marque alterne', f1!=f2, '%s -> %s'%(f1,f2))

    # geometrie : rien ne se recouvre
    g=pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
      const R=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();
        return [Math.round(r.top-d.top),Math.round(r.bottom-d.top)];};
      return {dev:Math.round(d.height),top:R('#shareScreen>.sh-top'),cv:R('#shCanvas'),foot:R('#shareScreen .sh-foot')};}""")
    t('aucun recouvrement', g['cv'][0]>=g['top'][1]-3 and g['cv'][1]<=g['foot'][0]+3 and g['foot'][1]<=g['dev'], str(g))

    # ✕ ferme
    pg.evaluate("()=>document.querySelector('#shareScreen .closeb').click()"); pg.wait_for_timeout(700)
    t('le ✕ ferme', not pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('show')"))

    t('aucune erreur JS', not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-42s %s  %s'%(n,s,d if s=='KO' else ''))
print('\n%d/%d'%(sum(1 for _,s,_ in R if s=='OK'),len(R)))
