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

    # ⚑ TROIS CONTRATS RÉÉCRITS AU NIVEAU DE LA DÉCISION (§7 de CLAUDE.md).
    #   La règle qu'ils encodaient : les réglages du partage s'ouvrent par un bouton « ⋯ »
    #   (#shTrayBtn) OU par le libellé du format (#shFmtTxt), dans un tiroir #shTrayWrap.
    #   La décision qui l'a remplacée — Tom, 1er septembre 2026 : « page partager c'est
    #   moche ça donne pas envie. Faut un bandeau Peaufiner et Inviter/Partager, pas de
    #   trait, et JUSTE le sélecteur Ma Toile / Mes Promi visible, sinon faut Peaufiner. »
    #   Il n'y a donc plus qu'UNE porte, et c'est voulu : le libellé du format vit
    #   désormais À L'INTÉRIEUR du tiroir, il ne peut plus l'ouvrir.
    #   L'intention protégée ne bouge pas : les réglages s'atteignent, se referment, et
    #   rien d'autre qu'eux ne traîne dehors. Version d'origine :
    #   sauvegardes/redteam-avant-partage-sans-trait.py

    def ouvert():
        return pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('shc-ouvert')")

    pg.evaluate("()=>document.getElementById('shcPeaufiner').click()"); pg.wait_for_timeout(450)
    o1=ouvert()
    pg.evaluate("()=>document.getElementById('shcPeaufiner').click()"); pg.wait_for_timeout(450)
    o2=ouvert()
    t('la barre Peaufiner ouvre et referme', o1 and not o2, '%s / %s'%(o1,o2))

    # seul le sujet reste dehors — c'est la décision, mot pour mot
    pg.evaluate("()=>document.getElementById('shcPeaufiner').click()"); pg.wait_for_timeout(450)
    deh=pg.evaluate("""()=>{const sc=document.getElementById('shareScreen');
      const pile=document.getElementById('shcPile');
      const d=document.getElementById('device').getBoundingClientRect();
      const dur=['shcTitre','shcPeaufiner','shcBarre','shcSujet','shcCadre','shcChamp',
                 'shPreviewArea','shWrap','shCanvas','shMode','shInviteBtn','shShareBtn'];
      return [...sc.querySelectorAll('[id]')].filter(n=>{
        if(dur.includes(n.id)) return false;
        if(pile&&pile.contains(n)) return false;
        const c=getComputedStyle(n), r=n.getBoundingClientRect();
        if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.05) return false;
        if(r.width<20||r.height<12) return false;
        if(r.bottom<d.top||r.top>d.bottom) return false;
        return true;}).map(n=>n.id);}""")
    t('rien ne traine hors du tiroir', len(deh)==0, str(deh))

    # un tap ailleurs referme — la fonction existait sur l'ancien écran, elle est gardée
    pg.evaluate("()=>document.getElementById('shPreviewArea').click()"); pg.wait_for_timeout(450)
    t('un tap ailleurs referme', not ouvert())

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
    # ⚑ CONTRAT RÉÉCRIT (§7). Il visait `.sh-top` et `.sh-foot`, l'entête et le pied de
    #   l'ancien partage, que la décision du 1er septembre a remplacés. La pile est
    #   désormais : plateau · aperçu · sujet · Peaufiner · Inviter-Partager. L'intention
    #   ne change pas d'un iota — chaque bloc commence après la fin du précédent, et le
    #   dernier reste dans le cadre.
    g=pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
      const R=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();
        return [Math.round(r.top-d.top),Math.round(r.bottom-d.top)];};
      return {dev:Math.round(d.height),plateau:R('#shcTitre'),apercu:R('#shPreviewArea'),
              sujet:R('#shcSujet'),peaufiner:R('#shcPeaufiner'),barre:R('#shcBarre')};}""")
    pile=[g['plateau'],g['apercu'],g['sujet'],g['peaufiner'],g['barre']]
    ok=all(b is not None for b in pile)
    if ok:
        ok=all(pile[i+1][0] >= pile[i][1]-3 for i in range(len(pile)-1)) and pile[-1][1] <= g['dev']
    t('aucun recouvrement', ok, str(g))

    # ✕ ferme
    pg.evaluate("()=>document.querySelector('#shareScreen .closeb').click()"); pg.wait_for_timeout(700)
    t('le ✕ ferme', not pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('show')"))

    t('aucune erreur JS', not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-42s %s  %s'%(n,s,d if s=='KO' else ''))
print('\n%d/%d'%(sum(1 for _,s,_ in R if s=='OK'),len(R)))
