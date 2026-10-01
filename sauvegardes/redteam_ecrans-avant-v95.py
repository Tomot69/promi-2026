# -*- coding: utf-8 -*-
"""Batterie 4 — les huit écrans jamais testés.
   Chaque écran : ouverture réelle, éléments clés, géométrie, clair ET sombre."""
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

import sys
# ⚑ LES TROIS TEINTES D'ÉTAT — écrites ici, avec la décision qui les fixe (Tom, 16 septembre 2026 :
#   « l'orange devient #DD4D23 — même fonction d'accent, pastilles et états »). La RÈGLE ne change
#   pas — « la légende nomme trois arcs en trois teintes d'état », « aucune piste vide » ; seule la
#   VALEUR de l'accent bouge. Le juge porte la décision, l'app la respecte — jamais l'inverse (§7).
#   Version d'avant : sauvegardes/redteam_ecrans-avant-PALETTE-16sept.py
# ⚑ REPRIS LE 21 SEPTEMBRE 2026 (§7). LA RÈGLE NE BOUGE PAS — « la légende nomme trois arcs en
#   trois teintes d'état » ; ce sont les VALEURS, et elles BASCULENT désormais avec le thème.
#   Tom : « Ils doivent porter les valeurs d'état v7 : à tenir #DD4D23, en cours #291547,
#   tenu #00341A. En mode clair, ce sont les profondes. » La colonne de l'Aura est posée sur la
#   PAGE : en clair les profondes, en sombre leurs claires (§3, une marque suit son fond).
#   L'amande #8FE08F n'est plus une valeur d'état : elle est réservée à la célébration.
#   Version d'avant : sauvegardes/redteam_ecrans-avant-v8b.py
# ⚑ REPRIS LE 22 SEPTEMBRE 2026 (§7). LA BASCULE DISPARAÎT. Tom : « #DD4D23, #291547, #00341A.
#   Exactement celles-là, partout où un état paraît. Aucune teinte dérivée, aucun calcul, aucune
#   transformation. » Les deux CLAIRES que j'avais construites (#33BA6C, #A77CF7) sortent.
#   Version d'avant : sauvegardes/redteam_ecrans-avant-v8d.py
ETATS3 = ('rgb(0, 52, 26)', 'rgb(41, 21, 71)', 'rgb(221, 77, 35)')
def etats_du_theme(th):
    return list(ETATS3)
TENU_D    = 'rgb(51, 186, 108)'    # #33BA6C — l'amande #8FE08F jusqu'au 21 sept.
                                   #   (planche des correspondances, « bande pleine en pied »).
                                   #   Version d'avant : sauvegardes/redteam_ecrans-avant-IDENTITE.py
# ⚑ REPRIS LE 21 SEPTEMBRE 2026 (§7, la valeur décidée s'écrit EN DUR dans le juge).
#   La RÈGLE ne bouge pas — « la légende nomme trois arcs en trois teintes d'état » ; c'est la
#   VALEUR qui change. Tom, 21 sept. : « Le jaune sort. #FFD447 a été retiré en v6, il ne doit
#   revenir nulle part. » Le clair de l'« en cours » devient le violet #A77CF7, que le jeu
#   portait déjà (--c-mauve63) : ΔE 30 du lilas Nuée, 41 du bleu, 58 du rose.
#   Version d'avant : sauvegardes/redteam_ecrans-avant-v8.py
ENCOURS_D = 'rgb(167, 124, 247)'   # #A77CF7 · jaune #FFD447 du 17 au 21 sept. · périwinkle #8FA0FF avant
ATENIR_D  = 'rgb(221, 77, 35)'     # #DD4D23 — était #F07A2E rgb(240, 122, 46)



R=[]
def t(n,ok,d=''): R.append((n,'OK' if ok else 'KO',d))

GEO = """(sel)=>{const d=document.getElementById('device').getBoundingClientRect();
  const e=document.querySelector(sel); if(!e) return null;
  const r=e.getBoundingClientRect();
  return {x:Math.round(r.left-d.left),y:Math.round(r.top-d.top),
          w:Math.round(r.width),h:Math.round(r.height),
          dw:Math.round(d.width),dh:Math.round(d.height),
          vis:getComputedStyle(e).display!=='none'&&r.width>0};}"""

# ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 10 septembre 2026.
#   Règle intacte : rien ne sort de l'appareil. Décision qui l'amende : une RANGÉE QUI
#   DÉFILE n'est pas un débordement — le disque coupé au bord est l'affordance du
#   défilement (Q128 §3 ; « la septième silhouette », validé par Tom pour l'Aura). Elle
#   n'est exemptée que si elle se DÉCLARE (`data-glisse`) ET SOUS CONDITION : elle tient
#   elle-même dans l'appareil, et elle rogne. Même règle que releve-S3.
#   Original : sauvegardes/redteam_ecrans-avant-aura-orbite.py
DEBORDE = """(sel)=>{const d=document.getElementById('device').getBoundingClientRect();
  const root=document.querySelector(sel); if(!root)return -1;
  let n=0;
  root.querySelectorAll('*').forEach(e=>{
    const r=e.getBoundingClientRect();
    if(r.width<2||r.height<2)return;
    if(getComputedStyle(e).position==='fixed')return;
    if(r.right>d.right+2||r.left<d.left-2){
      const g=e.closest('[data-glisse]');
      if(g&&g!==e){const gr=g.getBoundingClientRect(), ov=getComputedStyle(g).overflowX;
        if(gr.left>=d.left-2&&gr.right<=d.right+2&&(ov==='hidden'||ov==='auto'||ov==='scroll'))return;}
      n++;}
  });
  return n;}"""

def batterie(theme):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
        pg.goto(_url()); pg.wait_for_timeout(5200)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        # ⚑ 21 sept. — L'INSTRUMENT NE METTAIT JAMAIS L'APP EN SOMBRE. Le défaut par défaut de
        #   l'app est `theme='light'` : la passe étiquetée [sombre] tournait donc EN CLAIR, et
        #   tout ce qu'elle mesurait était mesuré deux fois dans le même thème. Trouvé en voyant
        #   la légende de l'Aura rendre les valeurs PROFONDES en « sombre » — l'app avait raison,
        #   c'est le juge qui se trompait de thème (§7 : avant d'accuser le dessin, on vérifie
        #   l'instrument). Version d'avant : sauvegardes/redteam_ecrans-avant-v8b.py
        if theme=='light':
            pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>{e.classList.add('light');e.classList.remove('dark');})")
        else:
            pg.evaluate("()=>{try{setTheme('dark');}catch(e){} document.querySelectorAll('.frame,.device').forEach(e=>e.classList.remove('light'));}")
            pg.wait_for_timeout(500)
        S=' ['+('clair' if theme=='light' else 'sombre')+']'

        # ---------- 1. TOILE ----------
        cv=pg.evaluate(GEO,'#toileCv')
        t('Toile : canvas présent'+S, bool(cv) and cv['vis'], str(cv))
        t('Toile : remplit l\'écran'+S, cv and cv['w']>=cv['dw']-4 and cv['h']>=cv['dh']-90, str(cv))
        t('Toile : des dalles colorées'+S, pg.evaluate("""()=>{const c=document.getElementById('toileCv');
          const g=c.getContext('2d');const im=g.getImageData(0,0,c.width,c.height).data;
          let n=0;for(let i=0;i<im.length;i+=400){const r=im[i],v=im[i+1],b=im[i+2];
            if(Math.abs(r-v)>18||Math.abs(v-b)>18)n++;}return n>30;}"""))
        v0=pg.evaluate("()=>JSON.stringify(Toile.vue())")
        t('Toile : API vue() lisible'+S, v0 and 's' in v0, v0)
        # ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 20 août 2026.
        #   Règle encodée : « une cellule grise ne désigne aucun Promi ». Le contrôle la
        #   testait par `hit(...) === null`, la forme que l'API rendait quand la Toile était
        #   pleine (23 promesses de l'ancien jeu). Avec le jeu de la planche — 12 plantés
        #   pour ~69 cellules — `hit()` rend un descripteur de cellule VIDE :
        #   `{pid:null, kind:'promi', nuee:null}`. C'est le même renseignement.
        #   Mesuré : la forme rendue oscille selon le semis (null en sombre, descripteur en
        #   clair, sur le MÊME jeu) — le contrôle d'origine était donc aussi un flake.
        #   Le contrat protège la même chose : rien n'ouvre de fiche hors d'une dalle plantée.
        #   Version d'origine : sauvegardes/redteam_ecrans-avant-jeu-planche.py
        t('Toile : hit() ignore les cellules grises'+S,
          pg.evaluate("()=>{const h=Toile.hit(-9999,-9999);return h===null||h.pid==null;}"),
          pg.evaluate("()=>{const h=Toile.hit(-9999,-9999);return h===null?'null':JSON.stringify(h);}"))
        # et il garde ses dents : une dalle PLANTÉE, elle, se désigne bien.
        t('Toile : hit() désigne un Promi planté'+S,
          pg.evaluate("""()=>{const v=Toile.vue&&Toile.vue(); const ids=promises.filter(p=>!p.draft).map(p=>p.id);
            for(let x=8;x<390;x+=7) for(let y=8;y<760;y+=7){
              const h=Toile.hit(x,y); if(h&&h.pid!=null&&ids.indexOf(h.pid)>=0) return true;}
            return false;}"""))
        n0=pg.evaluate("()=>Toile.cells()")
        pg.evaluate("()=>Toile.plantOne()"); pg.wait_for_timeout(600)
        t('Toile : planter garde la densité'+S, pg.evaluate("()=>Toile.cells()")==n0,
          '%s -> %s'%(n0,pg.evaluate("()=>Toile.cells()")))
        pg.evaluate("()=>Toile.unplantOne()"); pg.wait_for_timeout(400)

        # ---------- 2. CRÉER ----------
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1200)
        t('Créer : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')"))
        t('Créer : trois tuiles (promi, chiche, nuée)'+S, pg.evaluate("()=>document.querySelectorAll('#createSheet .tile[data-kind]').length")==3)
        t('Créer : sélecteur de sens'+S, pg.evaluate("()=>document.querySelectorAll('#csSens button').length")==2)
        t('Créer : rien ne déborde'+S, pg.evaluate(DEBORDE,'#createSheet')==0,
          'éléments hors cadre : %s'%pg.evaluate(DEBORDE,'#createSheet'))
        # une forme à la fois
        # Trois natures à l'écran de choix : Promi · Chiche · Nuée (le Brouillon est un
        # ÉTAT via « garder de côté »). Le Chiche réutilise le formulaire du Promi.
        etats=[]
        for k in ['promi','chiche','nuee']:
            pg.evaluate("k=>document.querySelector('.tile[data-kind='+k+']').click()",k); pg.wait_for_timeout(450)
            etats.append(pg.evaluate("""()=>['promiForm','nueeForm']
              .filter(i=>{const e=document.getElementById(i);return e&&getComputedStyle(e).display!=='none';}).length"""))
        t('Créer : une seule forme visible'+S, etats==[1,1,1], str(etats))
        # le brouillon reste atteignable : le contrôle « garder de côté » existe
        t('Créer : « garder de côté » présent'+S,
          pg.evaluate("()=>!!document.querySelector('.garde-cote,[data-gc]')"))
        # champ obligatoire
        pg.evaluate("()=>document.querySelector('.tile[data-kind=promi]').click()"); pg.wait_for_timeout(400)
        n=pg.evaluate("()=>promises.length")
        pg.evaluate("()=>{document.getElementById('fTitle').value='';document.getElementById('addPromi').click();}")
        pg.wait_for_timeout(400)
        t('Créer : champ vide refusé'+S, pg.evaluate("()=>promises.length")==n)
        t('Créer : le refus se voit'+S, pg.evaluate("()=>document.getElementById('fTitle').classList.contains('req-vide')"))
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)

        # ---------- 3. INDEX ----------
        pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();else document.getElementById('indexSheet').classList.add('show');}"); pg.wait_for_timeout(1400)
        t('Index : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('indexSheet').classList.contains('show')"))
        t('Index : des lignes'+S, pg.evaluate("()=>document.querySelectorAll('#indexSheet .row,#indexSheet .irow,#indexList > *').length")>0,
          str(pg.evaluate("()=>document.querySelectorAll('#indexList > *').length")))
        t('Index : miniatures de dalle'+S, pg.evaluate("()=>document.querySelectorAll('#indexSheet canvas').length")>0)
        t('Index : rien ne déborde'+S, pg.evaluate(DEBORDE,'#indexSheet')==0,
          str(pg.evaluate(DEBORDE,'#indexSheet')))
        t('Index : ✕ ferme'+S, (pg.evaluate("()=>{const c=document.querySelector('#indexSheet .closeb');if(c)c.click();return 1;}"),
           pg.wait_for_timeout(700), not pg.evaluate("()=>document.getElementById('indexSheet').classList.contains('show')"))[2])

        # ---------- 4. FIL ----------
        pg.evaluate("()=>{if(window.buildFeed)buildFeed();const e=document.getElementById('feedScreen');if(e)e.classList.add('show');}")
        pg.wait_for_timeout(1200)
        t('Fil : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('feedScreen').classList.contains('show')"))
        t('Fil : rien ne déborde'+S, pg.evaluate(DEBORDE,'#feedScreen')==0, str(pg.evaluate(DEBORDE,'#feedScreen')))
        pg.evaluate("()=>document.getElementById('feedScreen').classList.remove('show')"); pg.wait_for_timeout(400)

        # ---------- 5. AURA ----------
        # ⚑ CONTRATS RÉÉCRITS AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 10 septembre 2026.
        #   L'Aura est RÉÉCRITE EN ENTIER (lot-AURA-ORBITE) : la sphère, les Noyaux du §2.9,
        #   la légende, « Ce que tu as tenu », « Partager mon Noyau ». Les nœuds de l'ancienne
        #   Aura restent dans le DOM, masqués : un contrôle qui les viserait encore passerait
        #   VERT sur une interface morte. D'où la réécriture, règle par règle :
        #     · « anneau peint » visait `.kr-c`, l'anneau de l'ANCIEN Noyau. L'anneau autour de
        #       la sphère est SORTI (« il faisait doublon avec le Noyau toi », 10 sept.) ; celui
        #       qui porte la règle est le Noyau « toi » de la rangée. Même règle, nouveau nœud —
        #       et la sphère elle-même est lue dans ses pixels.
        #     · « Partager mon Noyau » RETIRÉ : décision INVERSE du 10 septembre (« la porte
        #       manquait sur l'Aura alors que l'aide l'annonce en gratuit »). Le contrat vérifie
        #       que la porte existe ET qu'elle mène au partage en mode Noyau.
        #     · « rien ne déborde » : inchangé, avec l'exemption SOUS CONDITION de DEBORDE.
        #   Original : sauvegardes/redteam_ecrans-avant-aura-orbite.py
        pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(1800)
        t('Aura : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('auraScreen').classList.contains('show')"))
        for _ in range(80):
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret&&_aura.etat().frames>3)"): break
            pg.wait_for_timeout(250)
        t('Aura : le Noyau « toi » porte ses arcs'+S, pg.evaluate("""()=>{const n=document.querySelector('#auraScreen .au-moi');
          if(!n)return false;return [...n.querySelectorAll('.au-arc')].filter(c=>c.getBoundingClientRect().width>0).length>0;}"""))
        t('Aura : la sphère est peinte'+S, pg.evaluate("""()=>{const c=document.getElementById('auBoule');
          if(!c||!c.width)return false;const im=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
          let n=0;for(let i=3;i<im.length;i+=160)if(im[i]>200)n++;return n>200;}"""))
        _p = pg.evaluate("()=>{const b=document.getElementById('auPartage');if(!b)return 'absente';b.click();return 'ok';}")
        pg.wait_for_timeout(900)
        _sh = pg.evaluate("""()=>({ouvert:document.getElementById('shareScreen').classList.contains('show'),
          pelote:window.shareMode==='pelote'||document.getElementById('shareScreen').classList.contains('shc-pelote')})""")
        # ⚑ REPRIS LE 23 SEPTEMBRE 2026, second tour (§7). LA RÈGLE QUE CE CONTRÔLE ENCODAIT :
        #   le bouton de l'Aura mène au partage EN MODE NOYAU. LA DÉCISION QUI LA REMPLACE (Tom) :
        #   « On ne partage plus son Noyau. Le Noyau porte des proportions de paroles tenues :
        #   le partager, c'est partager son score. Ce qu'on partage, c'est la Pelote. »
        #   MÊME INTENTION — le bouton ouvre le partage sur SON sujet — nouveau sujet.
        #   Original : sauvegardes/redteam_ecrans-avant-v13.py
        t('Aura : « Partager ma Pelote » mène au partage de la Pelote'+S, _p=='ok' and _sh['ouvert'] and _sh['pelote'], '%s %s'%(_p,_sh))
        pg.evaluate("()=>{document.getElementById('shareScreen').classList.remove('show');}"); pg.wait_for_timeout(500)
        t('Aura : rien ne déborde'+S, pg.evaluate(DEBORDE,'#auraScreen')==0, str(pg.evaluate(DEBORDE,'#auraScreen')))
        pg.evaluate("()=>{const c=document.querySelector('#auraScreen .closeb');if(c)c.click();}"); pg.wait_for_timeout(700)

        # ---------- 6. STUDIO ----------
        pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(1800)
        t('Studio : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('show')"))
        # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7). Il exigeait que les deux
        # bascules forment un groupe centré EN HAUT du Studio. Le Studio est porté à la
        # variante B : le champ occupe le haut, et les réglages qui ne sont ni le monde ni
        # le pinceau vivent derrière la barre Peaufiner (Q109). Le §9 interdisant de perdre
        # une fonction, elles sont DÉPLACÉES — même intention, nouveau nœud.
        # Original : sauvegardes/redteam_ecrans-avant-studio-champ.py
        t('Studio : les deux bascules existent'+S,
          pg.evaluate("()=>!!(document.getElementById('thToggle')&&document.getElementById('txToggle'))"))
        # ⚑ RÉÉCRIT UNE SECONDE FOIS, AU NIVEAU DE LA DÉCISION (CLAUDE.md §7).
        # La règle protégée n'a pas bougé : LES DEUX BASCULES DE VUE SONT ATTEIGNABLES ET
        # LEUR GROUPE EST CENTRÉ. Ce sont les NŒUDS qui ont changé : la variante « le
        # champ » (tiroir `#stcTiroir`, pile `.stc-pile`) est supprimée, remplacée par le
        # Studio à deux plateaux — le pinceau ayant quitté le Studio, l'onde n'avait plus
        # rien à montrer et la Toile prend tout l'écran (CLAUDE.md §5).
        # Les deux bascules sont désormais portées par QUATRE DISQUES sur le plateau du
        # bas (`#stpVue`), qui ne les remplacent pas : ils les CLIQUENT. Le contrôle est
        # donc plus fort qu'avant — il vérifie que le geste arrive vraiment à la bascule.
        # Original : sauvegardes/redteam_ecrans-avant-studio-plateaux.py
        t('Studio : les deux réglages de vue sont sur le plateau'+S,
          pg.evaluate("()=>document.querySelectorAll('#stpVue .stp-d').length")==4,
          str(pg.evaluate("()=>document.querySelectorAll('#stpVue .stp-d').length")))
        _av=pg.evaluate("()=>{const b=document.querySelector('#txToggle [data-tx=\"on\"]');return !!(b&&b.classList.contains('on'));}")
        pg.evaluate("()=>{const d=document.querySelectorAll('#stpVue .stp-d');if(d[2])d[2].click();}"); pg.wait_for_timeout(320)
        pg.evaluate("()=>{const d=document.querySelectorAll('#stpVue .stp-d');if(d[3])d[3].click();}"); pg.wait_for_timeout(320)
        _ap=pg.evaluate("()=>{const b=document.querySelector('#txToggle [data-tx=\"on\"]');return !!(b&&b.classList.contains('on'));}")
        t('Studio : le disque atteint vraiment la bascule'+S, _ap is False,
          'avant %s / apres %s' % (_av, _ap))
        g=pg.evaluate(GEO,'#stpVue')
        t('Studio : rangée de vue centrée'+S, g and abs(g['x']-(g['dw']-g['x']-g['w']))<10, str(g))
        t('Studio : aperçus de monde'+S, pg.evaluate("()=>document.querySelectorAll('#studioScreen canvas').length")>0,
          str(pg.evaluate("()=>document.querySelectorAll('#studioScreen canvas').length")))
        pg.evaluate("()=>{const c=document.querySelector('#studioScreen .closeb');if(c)c.click();}"); pg.wait_for_timeout(700)

        # ---------- 7. RÉGLAGES ----------
        pg.evaluate("()=>{const e=document.getElementById('settingsScreen');if(e)e.classList.add('show');}")
        pg.wait_for_timeout(1000)
        t('Réglages : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('settingsScreen').classList.contains('show')"))
        t('Réglages : ligne Inviter'+S, pg.evaluate("()=>!!document.getElementById('setInvite')"))
        t('Réglages : encart Cercle'+S, pg.evaluate("()=>!!document.querySelector('.set-cercle')"))
        t('Réglages : rien ne déborde'+S, pg.evaluate(DEBORDE,'#settingsScreen')<=1,
          str(pg.evaluate(DEBORDE,'#settingsScreen')))
        pg.evaluate("()=>document.getElementById('settingsScreen').classList.remove('show')"); pg.wait_for_timeout(400)

        # ---------- 8. FICHE ----------
        pg.evaluate("""()=>{const p=promises.find(x=>!x.draft&&!x.req);
          if(p&&window.renderDetail){renderDetail(p.id);}
          const e=document.getElementById('detailPoster');if(e)e.classList.add('show');}""")
        pg.wait_for_timeout(1400)
        t('Fiche : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
        t('Fiche : vignette de dalle'+S, pg.evaluate("()=>{const e=document.getElementById('dForm');return !!e;}"))
        t('Fiche : le + commun'+S, pg.evaluate("()=>document.querySelectorAll('#detailPoster .dpf-plus').length")>0)
        t('Fiche : rien ne déborde'+S, pg.evaluate(DEBORDE,'#detailPoster')==0, str(pg.evaluate(DEBORDE,'#detailPoster')))




        # ---------- AURA : l'Aura sans chiffre, le mot, l'ordre, la légende ----------
        # ⚑ CONTRATS RÉÉCRITS AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 10 septembre 2026.
        #   Ce bloc protégeait le Noyau de l'ANCIENNE Aura : la série dans l'anneau, le mot
        #   d'harmonie dessous, le % en signature, HARMONIE en trois teintes qui suivaient le
        #   Studio, la légende entre le % et les compteurs. Décision de Tom, 10 septembre,
        #   « L'AURA SANS CHIFFRE » : le chiffre d'harmonie et le mot qui qualifie la personne
        #   SORTENT (l'un est une note, l'autre un verdict) ; UN mot revient, il qualifie
        #   L'OBJET. Et le 4 septembre : une dalle est FIGÉE à sa plantation. Règle par règle :
        #     le Noyau ne porte que la série  → les Noyaux ne portent que l'image et le prénom
        #     le mot d'harmonie sous le Noyau → le mot qualifie l'objet (une des phrases de Tom)
        #     le % sous le Noyau              → aucun chiffre, aucun pourcentage sur l'Aura
        #     le % en signature               ┐ FUSIONNÉS : les deux protégeaient la signature
        #     le décalage suit le corps        ┘ du %, qui n'existe plus → aucune signature chiffrée
        #     anneau puis % puis légende      → sphère, Noyaux, légende, ce que tu as tenu, bouton
        #     HARMONIE en trois teintes       → la légende nomme trois arcs en trois teintes d'état
        #     les teintes suivent le Studio   → le Studio ne repeint pas les dalles déjà plantées
        #     légende entre % et compteurs    → légende centrée entre les Noyaux et « Ce que tu as tenu »
        #   Original : sauvegardes/redteam_ecrans-avant-aura-orbite.py
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));document.getElementById('souffleBtn').click();}")
        for _ in range(80):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!(window._aura&&_aura.etat().pret)"): break
        pg.wait_for_timeout(600)
        _nb = pg.evaluate("()=>[...document.querySelectorAll('#auraScreen .au-nb')].map(e=>e.textContent.trim()).filter(Boolean)")
        t('Aura : les Noyaux ne portent que l image et le prénom'+S,
          pg.evaluate("()=>document.querySelectorAll('#auraScreen .au-nb').length")>0 and not _nb, str(_nb[:3]))
        _mot = pg.evaluate("()=>{const e=document.querySelector('#auraScreen .au-mot');return e?e.textContent.trim():null;}")
        t('Aura : le mot qualifie l objet (une des phrases de Tom)'+S, _mot in (
          'Rien de ce qui est ici n’a été dit à la légère.', 'Tout ça, tu l’as dit. Et tu l’as fait.',
          'On ne dirait pas comme ça, mais c’est du solide.', 'Il y en a, des paroles tenues.',
          'Et dire que tout ça, c’est toi.', 'La première parole laissera sa trace ici.'), str(_mot))
        _tx = pg.evaluate("""()=>{const o=[];document.querySelectorAll('#auraScreen *').forEach(e=>{
          const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
          const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').trim();
          if(t&&(t.indexOf('%')>=0||/^[\\d\\s.,]+$/.test(t)))o.push(t);});return o;}""")
        t('Aura : aucun chiffre ni pourcentage'+S, not _tx, str(_tx[:3]))
        _sg = pg.evaluate("""()=>{const o=[];document.querySelectorAll('#auraScreen *').forEach(e=>{
          const r=e.getBoundingClientRect();if(!r.width||!r.height)return;const s=getComputedStyle(e).textShadow||'';
          if(s.indexOf('221, 77, 35')>=0&&s.indexOf('58, 84, 255')>=0)o.push(e.textContent.trim().slice(0,12));});return o;}""")
        t('Aura : aucune signature chiffrée'+S, not _sg, str(_sg[:3]))
        _g = pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
          const R=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();
            return r.height?[Math.round(r.top-d.top),Math.round(r.bottom-d.top)]:null;};
          return {boule:R('#auBoule'), nx:R('#auraScreen .au-nx'), lg:R('#auraScreen .au-lg'),
                  mo:R('#auraScreen .au-mo h3'), bt:R('#auPartage')};}""")
        # ⚑ REPRIS LE 23 SEPTEMBRE 2026, second tour (§7). LA RÈGLE QUE CE CONTRÔLE ENCODAIT :
        #   l'ordre de la colonne était ... légende, ce que tu as tenu, PUIS le bouton, tout en bas.
        #   LA DÉCISION QUI LA REMPLACE (Tom) : « Le bouton de partage remonte sous la légende —
        #   en bas de page, personne n'y va. » Mesuré avant : le bouton tombait à y 1045, soit
        #   201 px sous le pli. MÊME INTENTION — la colonne est ordonnée et sans recouvrement —
        #   nouvel ordre : Pelote, Noyaux, légende, BOUTON, ce que tu as tenu.
        _o = [_g[k] for k in ('boule','nx','lg','bt','mo')]
        t('Aura : Pelote, Noyaux, légende, bouton, ce que tu as tenu'+S,
          all(_o) and all(_o[i][0] < _o[i+1][0] for i in range(4))
          and _g['nx'][1] <= _g['lg'][0] and _g['lg'][1] <= _g['bt'][0]
          and _g['bt'][1] <= _g['mo'][0], str(_g))
        _hc = pg.evaluate("()=>[...document.querySelectorAll('#auraScreen .au-lg span')].map(s=>[s.textContent.trim(),getComputedStyle(s.querySelector('i')).backgroundColor])")
        t('Aura : la légende nomme trois arcs en trois teintes d état'+S,
          [x[0] for x in _hc]==['tenues','en cours','à tenir']
          and [x[1] for x in _hc]==etats_du_theme(theme), str(_hc))
        _m0 = pg.evaluate("()=>JSON.stringify((window._auraComp||{}).iles||null)")
        pg.evaluate("()=>{try{Toile.setPalette('ocean');}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); document.getElementById('souffleBtn').click();}")
        pg.wait_for_timeout(1500)
        _m1 = pg.evaluate("()=>JSON.stringify((window._auraComp||{}).iles||null)")
        t('Aura : le Studio ne repeint pas les dalles déjà plantées'+S,
          _m0 == _m1 and _m0 not in ('null', '[]'), '%s -> %s' % (_m0[:60], _m1[:60]))
        pg.evaluate("()=>{try{Toile.setPalette('signal');}catch(e){}}")
        pg.wait_for_timeout(1000)



        # ---------- Aura : la légende est centrée entre ses deux voisins ----------
        # (réécrit — voir le bloc ci-dessus. Le seuil se RESSERRE : 12 px → 1 px, celui du
        #  juge de l'air, parce que la cote est désormais calculée, plus approchée à l'œil.)
        pg.evaluate("()=>{document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show'));document.getElementById('souffleBtn').click();}")
        pg.wait_for_timeout(1200)
        _c = pg.evaluate("""()=>{const L=document.querySelector('#auraScreen .au-lg');if(!L||!L.getAttribute('data-centre-entre'))return null;
          const p=L.getAttribute('data-centre-entre').split('|'), sc=L.closest('.screen');
          const A=sc.querySelector(p[0]).getBoundingClientRect(), E=L.getBoundingClientRect(), B=sc.querySelector(p[1]).getBoundingClientRect();
          return [+(E.top-A.bottom).toFixed(2), +(B.top-E.bottom).toFixed(2)];}""")
        # ⚑ REPRIS LE 22 SEPTEMBRE 2026 (§7). LA RÈGLE QUE CE CONTRÔLE ENCODAIT : la légende est
        #   centrée AUX BOÎTES. LA DÉCISION QUI LA REMPLACE (Tom) : « L'air au-dessus et en
        #   dessous doit être égal, À L'ENCRE. » Gilbert se pose bas dans sa boîte de ligne : les
        #   deux centrages ne coïncident pas. L'app corrige donc la boîte de `K.lgINK` = −1,25 px,
        #   une cote DÉCLARÉE, relevée une fois police chargée. Le juge vérifie exactement ça :
        #   l'écart aux boîtes vaut −2 × lgINK, ni plus ni moins. L'air à l'encre lui-même se
        #   mesure sur l'image rendue (`scratchpad/air_encre_legende.py` : 29,5 / 29,0).
        # ⚑ 23 SEPT. (Tom) — la légende est repassée à la taille du commentaire (30 → 19,4) :
        #   l'écart d'encre de Gilbert se remesure avec elle. −1,25 → −0,5, valeur DÉCIDÉE,
        #   relevée sur l'image rendue (−1,25 donnait 31,5 / 34,0 ; 0 donnait 33,5 / 32,0).
        # ⚑ REPRIS LE 23 SEPT., SECOND TOUR (§7). LA RÈGLE QUE CE CONTRÔLE ENCODAIT : la légende
        #   est centrée AUX BOÎTES à −lgINK près, entre les Noyaux et un TITRE de moisson.
        #   LA DÉCISION QUI LA REMPLACE (Tom) : le bouton remonte sous la légende — son voisin du
        #   bas est donc un BOUTON, dont le contour commence plus haut dans sa boîte qu'une encre
        #   de titre. Mesuré à l'air de 28 des deux côtés : 36,5 au-dessus, 31,0 en dessous ; on
        #   rend les 5,5 par la boîte (lgINK −6) et l'ENCRE tombe égale (31,5 / 31,0, `releve-aura`).
        #   MÊME INTENTION — l'air se lit à l'encre, pas à la boîte. Original :
        #   sauvegardes/redteam_ecrans-avant-v13.py
        LG_INK = -6
        t('Aura : la légende est centrée à l\'encre (boîtes décalées de lgINK)'+S,
          bool(_c) and abs((_c[0]-_c[1]) - LG_INK) <= 1, str(_c))
        pg.evaluate("()=>{const c=document.querySelector('#auraScreen .closeb');if(c)c.click();}"); pg.wait_for_timeout(600)


        # ---------- ⚑ v21 — CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (Tom, 22 sept. 2026) ----------
        #   « L'ancien sélecteur Toile / Index : supprime-le entièrement, pas masqué — retiré. »
        #   Les cinq contrôles d'avant vérifiaient ses libellés, sa largeur et qu'il ouvrait l'Index.
        #   Même intention (une seule façon claire d'aller à l'Index, pas de doublon), nouvel objet.
        #   Original : sauvegardes/redteam_ecrans-avant-v21.py
        t('le selecteur Toile / Index est retire'+S, pg.evaluate("()=>!document.getElementById('viewSwitch')"))
        t('un seul Fil dans l app'+S, pg.evaluate("""()=>{let n=0;
          document.querySelectorAll('button,.dctrl').forEach(e=>{const q=e.querySelector('.l');
            const tx=(q?q.textContent:e.textContent||'').trim();
            if(/^Fil$/i.test(tx))n++;});return n;}""") == 1)
        pg.evaluate("()=>document.getElementById('indexBtn').click()")
        pg.wait_for_timeout(1500)
        t('l Index s ouvre par sa porte de l accueil'+S,
          pg.evaluate("()=>document.getElementById('indexSheet').classList.contains('show')"))
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(700)
        t('aucun bouton Toile ni Index dans la barre du haut'+S, pg.evaluate("""()=>![...document.querySelectorAll('.topbar button')].some(b=>/^(Toile|Index)$/.test((b.textContent||'').trim()))"""))
        t('aucun reste du selecteur (.viewswitch)'+S, pg.evaluate("()=>document.querySelectorAll('.viewswitch').length===0"))


        # ---------- L'INDEX EN BLOCS ----------
        pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();}"); pg.wait_for_timeout(1800)
        # SECTION 4 · l'Index est porté au moodboard : le bloc plein cadre `.ix-bloc` est
        # devenu la CARTE `.s4-carte` (§3.9). L'intention des contrôles ne change pas —
        # seul le nom du nœud qu'ils désignent change.
        _nb = pg.evaluate("()=>document.querySelectorAll('#indexSheet .s4-carte').length")
        t('Index : les Promi sont des blocs'+S, _nb > 0, '%d blocs' % _nb)
        # « seuls les urgents ont un aplat » : dans la carte du moodboard l'état ne vit plus
        # dans le fond mais dans LA LIGNE (§2.1 bis). Le contrôle devient donc : aucune carte
        # n'est peinte d'une couleur d'état — le fond reste un des trois corps du §1.3.
        _etats = pg.evaluate("""()=>[...document.querySelectorAll('#indexSheet .s4-carte')]
          .map(e=>getComputedStyle(e).backgroundColor)
          .filter(c=>/221, 77, 35|143, 224, 143/.test(c)).length""")
        t('Index : seuls les urgents ont un aplat'+S, _etats == 0, 'fonds d\'état %s / %d' % (_etats, _nb))
        t('Index : le mot du temps est peint'+S,
          all(x for x in pg.evaluate("()=>[...document.querySelectorAll('#indexSheet .s4-carte .s4-et')].map(e=>e.textContent.trim())")))
        t('Index : la vraie dalle est peinte'+S,
          pg.evaluate("""()=>[...document.querySelectorAll('#indexSheet .s4-carte canvas')].filter(c=>{
            try{const g=c.getContext('2d');const d=g.getImageData(0,0,c.width,c.height).data;
            for(let i=3;i<d.length;i+=400)if(d[i]>10)return true;}catch(e){}return false;}).length""") > 0)
        t('Index : « a rattraper » a disparu'+S,
          not pg.evaluate("()=>document.body.innerText.toLowerCase().includes('rattraper')"))
        t('Index : la recherche est conservee'+S, pg.evaluate("()=>!!document.getElementById('ixSearch')"))
        t('Index : le ✕ Fermer est conserve'+S, pg.evaluate("()=>!!document.querySelector('#indexSheet .closeb')"))
        pg.evaluate("()=>{const b=document.querySelector('#indexSheet .s4-carte');if(b)b.click();}")
        pg.wait_for_timeout(1400)
        t('Index : toucher un bloc ouvre la fiche'+S,
          pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
        pg.evaluate("()=>{document.getElementById('detailPoster').classList.remove('show');document.getElementById('indexSheet').classList.remove('show');}")
        pg.wait_for_timeout(700)

        # ---------- CHANTIER 45 : le Fil dans le dock ----------
        # ⚑ renommage de nœud (§7, pas une règle abandonnée) — 13 sept. 2026 : la barre de l'accueil est `#accBarre` (Q212).
        _d = pg.evaluate("()=>[...document.querySelectorAll('.dock .dctrl,.dock .dhero,#accBarre .dctrl,#accBarre .dhero')].map(e=>e.id)")
        t('le Fil a son bouton dans le dock'+S, 'filBtn' in _d, str(_d))
        t('le Fil a sa pastille'+S, pg.evaluate("()=>!!document.getElementById('filDot')"))
        # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (v89, Tom 27 sept. — Q347) : le compteur du Fil porte ce qui ATTEND UN GESTE de moi,
        #   il redescend quand j'agis, JAMAIS parce que j'ai regardé. (Avant : « s'allume sur du non-lu / s'éteint après lecture ».)
        _n0 = pg.evaluate("()=>window._filAttente?window._filAttente():0")
        pg.evaluate("()=>{FEED.push({id:99901,type:'chiche_recu',text:'Test te lance un chiche : « essai »',from:'Test',unread:true});if(window._majFilDot)_majFilDot();}")
        pg.wait_for_timeout(500)
        t('la pastille s allume sur ce qui attend un geste'+S,
          pg.evaluate("()=>document.getElementById('filDot').classList.contains('on')") and pg.evaluate("()=>window._filAttente()") == _n0 + 1)
        pg.evaluate("()=>document.getElementById('filBtn').click()"); pg.wait_for_timeout(1300)
        # le Fil vit dans #feedView (une vue), pas dans #feedScreen (un ecran)
        t('le bouton ouvre le Fil'+S,
          pg.evaluate("()=>{const v=document.getElementById('feedView');return !!v&&getComputedStyle(v).display!=='none';}"))

        _fv = pg.evaluate("""()=>{const v=document.getElementById('feedView');
          if(!v)return null; return {vis:getComputedStyle(v).display!=='none',
            n:v.querySelectorAll('.s4-carte,.fd-item').length};}""")
        t('le Fil affiche ses evenements'+S, bool(_fv and _fv['vis'] and _fv['n'] > 0), str(_fv))
        t('le compteur ne redescend pas a la lecture (Q347)'+S, pg.evaluate("()=>window._filAttente()") == _n0 + 1)
        pg.evaluate("()=>{ if(window.feedReleve) feedReleve(99901); }"); pg.wait_for_timeout(500)
        t('le compteur redescend quand j agis (Q347)'+S, pg.evaluate("()=>window._filAttente()") == _n0,
          str(pg.evaluate("()=>window._filAttente()")) + ' / attendu ' + str(_n0))
        pg.evaluate("()=>{if(window.setView)setView('toile');}"); pg.wait_for_timeout(700)

        # ---------- CHANTIER 8 : l'anneau du bouton + suit la Toile ----------
        _v0 = pg.evaluate("()=>getComputedStyle(document.getElementById('createBtn')).getPropertyValue('--kr-a1').trim()")
        t('l anneau du + porte des proportions'+S, bool(_v0), _v0)
        _c = pg.evaluate("""()=>{let t=0,e=0,r=0;promises.forEach(p=>{if(p.draft||p.req)return;
          if(p.status==='tenu')t++;else if(p.status==='rate')r++;else e++;});return {t,tot:Math.max(1,t+e+r)};}""")
        _att = 360*_c['t']/_c['tot'] - 10.8
        t('elles correspondent aux Promi tenus'+S,
          _v0 and abs(float(_v0.replace('deg','')) - _att) < 1.5,
          '%s attendu %.1f' % (_v0, _att))


        # ⚑ RÉÉCRITS AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 10 septembre 2026.
        #   Ils visaient `.seal-crown`, la couronne de traits de l'ANCIEN Noyau, bâtie dans
        #   #auraSeal (même innerHTML que le % en signature) : elle n'est plus à l'écran. La
        #   règle protégée — un trait fin reste lisible, et la couleur d'un anneau DIT quelque
        #   chose — se lit maintenant sur les Noyaux de la rangée, et le §2.9 a été corrigé
        #   par Tom le 10 septembre : la PISTE est neutre (une personne n'a pas de nature),
        #   seuls les ARCS portent la couleur, celle de l'ÉTAT.
        #   Original : sauvegardes/redteam_ecrans-avant-aura-orbite.py
        # ⚑ 14 sept. 2026 (Q215, §2.9 corrigé) : deux moitiés en chemins, plus de piste. Original : sauvegardes/redteam_ecrans-avant-deux-moities.py
        # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (Tom, 23 sept. 2026) : un anneau posé sur un fond
        #   sombre est CERNÉ D'UN FILET CRÈME de 1,4 px (§3). Ce filet n'est pas un arc — il ne
        #   dit aucun état, il rend l'anneau lisible. Le contrôle vise donc les ARCS, qui se
        #   déclarent (`.au-arc`), et plus « tout ce qui porte un stroke ».
        #   Original : sauvegardes/redteam_ecrans-avant-v11.py
        _tr = pg.evaluate("""()=>[...document.querySelectorAll('#auraScreen .au-n circle, #auraScreen .au-n path')]
          .filter(c=>!/kr-filet/.test(c.getAttribute('class')||'') && c.getAttribute('data-v16-filet')!=='1')   /* ⚑ v18 : le filet crème de 1 px n'est pas un arc (Tom, Q298) */
          .map(c=>({w:+c.getAttribute('stroke-width'), cls:c.getAttribute('class'), c:getComputedStyle(c).stroke}))""")
        t('Aura : les arcs des Noyaux sont lisibles (6 px et plus)'+S,
          bool(_tr) and min(x['w'] for x in _tr) >= 6, 'trait min %s' % (min(x['w'] for x in _tr) if _tr else 'aucun'))
        # ⚠ le thème AFFICHÉ, pas l'étiquette de la passe : cette batterie ne pose jamais le thème
        #   sombre (sa passe « sombre » n'ajoute simplement pas `.light`), et l'app démarre en CLAIR
        #   (relevé : `#device.light`, fond crème, promi_theme = light). La piste est neutre POUR LE
        #   THÈME QU'ON VOIT — c'est ça, la règle.
        _pi = 'rgb(222, 215, 198)' if pg.evaluate("()=>document.getElementById('device').classList.contains('light')") else 'rgb(42, 44, 52)'
        t('Aura : aucune piste vide, les arcs disent l état'+S,
          bool(_tr) and not any(x['cls'] == 'au-piste' for x in _tr)
          and all(x['c'] in etats_du_theme(theme) for x in _tr if x['cls'] == 'au-arc'),
          str(sorted(set(x['c'] for x in _tr))))
        t('bouton + : rotation lente'+S, pg.evaluate("""()=>{const e=document.getElementById('createBtn');
          return parseFloat(getComputedStyle(e,'::before').animationDuration) >= 40;}"""))

        # ---------- la signature est la MEME partout ----------
        # ⚑ RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 10 septembre 2026.
        #   Il comparait la signature de l'app à celle du % de l'Aura (#kPct). L'Aura n'a plus
        #   de chiffre (décision Tom, 10 sept.) : #kPct n'est plus à l'écran. La règle — UNE
        #   signature, la même partout — se lit donc sur tous les porteurs qui restent : les
        #   `.sig` de l'app ont les mêmes proportions de décalage, sans exception.
        #   Original : sauvegardes/redteam_ecrans-avant-aura-orbite.py
        _sig = pg.evaluate("""()=>{
          const r=(e)=>{if(!e)return null;const c=getComputedStyle(e);
            const f=parseFloat(c.fontSize);
            const m=c.textShadow.match(/(-?[\\d.]+)px\\s+(-?[\\d.]+)px/);
            return m? (Math.abs(+m[1])/f).toFixed(3)+'/'+(Math.abs(+m[2])/f).toFixed(3) : null;};
          return [...document.querySelectorAll('.sig')].map(r).filter(Boolean);}""")
        t('la signature est identique partout où elle est portée'+S,
          len(_sig) >= 2 and len(set(_sig)) == 1, str(_sig))

        t('aucune erreur JS'+S, not er, str(er[:2]))
        b.close()

for th in ['dark','light']:
    batterie(th)

for n,s,d in R: print('%-46s %s  %s'%(n,s,d if s=='KO' else ''))
ok=sum(1 for _,s,_ in R if s=='OK')
print('\n%d/%d'%(ok,len(R)))
sys.exit(0 if ok==len(R) else 1)
