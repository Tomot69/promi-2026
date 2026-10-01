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
      // ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 2 septembre 2026.
      //    LA RÈGLE QU'IL ENCODAIT : « hors du tiroir, seul le sujet reste dehors ».
      //    LA DÉCISION QUI LA REMPLACE : Tom, 2 septembre — « L'IMAGE EST L'ÉCRAN,
      //    ENTIÈRE. Une ligne posée dessus dit où l'on en est. » L'aperçu occupe désormais
      //    390 × 844 : son badge et son mot-marque (`shBadge`, `shWordmark`) s'étendent
      //    avec lui. Ils ne « traînent » pas — ILS SONT L'IMAGE, et l'image est le sujet
      //    de l'écran. Ce que la règle protège, ce sont les COMMANDES : aucune ne doit
      //    vivre hors du tiroir, le sujet mis à part. On exclut donc ce qui vit DANS
      //    l'aperçu, et rien d'autre.
      //    Version d'origine : sauvegardes/redteam-avant-partage-plein.py
      const ap=document.getElementById('shPreviewArea');
      return [...sc.querySelectorAll('[id]')].filter(n=>{
        if(dur.includes(n.id)) return false;
        if(ap&&ap.contains(n)) return false;
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
    # ⚑ v41 — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (§7). Il attendait qu'un toucher fasse ALTERNER la police du
    #   mot-marque (le style « signature »). Décisions : 18 sept. — le mot-marque est en PromiLate (lot-TITRES-POLICE) ;
    #   22 sept. — il ne reste que trois polices, la seconde (Fraunces) est retirée. Il n'y a plus de second style.
    #   Ce que le contrat protège désormais : le mot-marque est en PromiLate AVANT ET APRÈS le toucher, et son « i »
    #   garde le bleu d'accent (#82AEF8 sur une image sombre, #022140 sur une claire — jamais une couleur d'état).
    #   Version d'avant : sauvegardes/redteam-avant-v41.py
    I_ACC = ('rgb(130, 174, 248)', 'rgb(2, 33, 64)')   # #82AEF8 · #022140 — décidés, en dur
    lit = "()=>{const w=document.getElementById('shWordmark'), i=w.querySelector('.uvi'); return [getComputedStyle(w).fontFamily.split(',')[0].replace(/[\"']/g,''), i?getComputedStyle(i).color:'']}"
    f1=pg.evaluate(lit)
    pg.evaluate("()=>{const e=document.getElementById('shWordmark'); if(e) e.click();}"); pg.wait_for_timeout(400)
    f2=pg.evaluate(lit)
    t('le mot-marque reste en PromiLate, son i en accent', f1[0]=='PromiLate' and f2[0]=='PromiLate' and f1[1] in I_ACC and f2[1] in I_ACC, '%s -> %s' % (f1, f2))

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
    # ⚑ CONTRÔLE MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — 2 septembre 2026.
    #   LA RÈGLE QU'IL ENCODAIT : « chaque bloc commence après la fin du précédent »,
    #   l'aperçu compris — c'était l'empilement de la version « feuille ».
    #   LA DÉCISION QUI LA REMPLACE : Tom, 2 septembre — « L'IMAGE EST L'ÉCRAN, ENTIÈRE.
    #   Une ligne posée dessus dit où l'on en est. » L'aperçu passe DESSOUS, par décision :
    #   le plateau, la ligne et les deux boutons sont POSÉS SUR LUI, et c'est le parti.
    #   L'intention ne bouge pas d'un iota : LES COMMANDES ne se recouvrent pas entre
    #   elles, et la dernière reste dans le cadre. On retire l'aperçu de la pile — et on
    #   VÉRIFIE EN PLUS qu'il tient bien l'écran entier, ce que la décision demande.
    #   Version d'origine : sauvegardes/redteam-avant-partage-plein.py
    pile=[g['plateau'],g['peaufiner'],g['barre']]
    ok=all(b is not None for b in pile) and g['apercu'] is not None
    if ok:
        ok=all(pile[i+1][0] >= pile[i][1]-3 for i in range(len(pile)-1)) and pile[-1][1] <= g['dev']
        # l'image est bien l'écran : elle part du haut et descend jusqu'en bas
        ok=ok and g['apercu'][0] <= 2 and g['apercu'][1] >= g['dev']-2
    t('aucun recouvrement', ok, str(g))

    # ✕ ferme
    pg.evaluate("()=>document.querySelector('#shareScreen .closeb').click()"); pg.wait_for_timeout(700)
    t('le ✕ ferme', not pg.evaluate("()=>document.getElementById('shareScreen').classList.contains('show')"))

    t('aucune erreur JS', not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-42s %s  %s'%(n,s,d if s=='KO' else ''))
print('\n%d/%d'%(sum(1 for _,s,_ in R if s=='OK'),len(R)))
