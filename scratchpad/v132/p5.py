import io
def patch(f, reps):
    S=io.open(f,encoding='utf-8').read()
    for a,b in reps:
        assert S.count(a)==1,(f,S.count(a),a[:70]); S=S.replace(a,b)
    io.open(f,'w',encoding='utf-8').write(S)
# ── réactivité : la plus récente en premier
patch('redteam_reactif.py',[
("""            if etat=='tenu' and present: ok('%s · Aura : la parole tenue est la dernière de la liste (ordre chronologique)'%lab, e['moisson'][-1:]==[T], 'fin %s'%e['moisson'][-1:])""",
 """            # ⚑ v132 (Tom, 5 oct. 2026) : « la plus récente en premier. La parole qu'on vient de tenir doit se voir sans défiler. » (v131 la posait en dernier.)
            if etat=='tenu' and present: ok('%s · Aura : la parole tenue est la PREMIÈRE de la liste, visible sans défiler'%lab, e['moisson'][:1]==[T] and e.get('moissonY') is not None and e['moissonY']<844, 'tête %s · y %s'%(e['moisson'][:1], e.get('moissonY')))"""),
("""    moisson:[...document.querySelectorAll('#auraScreen .au-mo .au-c span')].map(e=>e.textContent.trim()),""",
 """    moisson:[...document.querySelectorAll('#auraScreen .au-mo .au-c span')].map(e=>e.textContent.trim()),
    moissonY:(()=>{ const e=document.querySelector('#auraScreen .au-mo .au-c'), dv=document.getElementById('device').getBoundingClientRect(); return e?Math.round((e.getBoundingClientRect().top-dv.top)/(dv.width/390)):null; })(),"""),
])
# ── menu photo : « Dessiner » en tête, sur la fiche et sur la page +
patch('redteam_photo_menu.py',[
("""    t(tag + ' A · le bouton photo d\\'une fiche ouvre un menu de deux choix', bool(m) and m['vis'] and m['mots'] == MOTS, str(m))""",
 """    # ⚑ v132 (Tom, C-042) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_photo_menu-avant-v132.py) : « Dessiner » est en tête du menu, sur la
    #   fiche ET sur la page + (v128 ③, construit en v132) ; les deux choix de v117 suivent, dans le même ordre.
    t(tag + ' A · le bouton photo d\\'une fiche ouvre son menu : « Dessiner » en tête, puis les deux choix', bool(m) and m['vis'] and m['mots'] == ['Dessiner'] + MOTS, str(m))"""),
("""                tape(pg, '.ph-photo-menu button:nth-child(1)')
            t(tag + ' B · « Importer une image » ouvre le sélecteur du système', fc.value is not None)""",
 """                tape(pg, '.ph-photo-menu button:nth-child(2)')
            t(tag + ' B · « Importer une image » ouvre le sélecteur du système', fc.value is not None)"""),
("""        tape(pg, '#detailPoster .ph-photo-btn')
        tape(pg, '.ph-photo-menu button:nth-child(2)')
        pg.wait_for_timeout(1500)""","""        tape(pg, '#detailPoster .ph-photo-btn')
        tape(pg, '.ph-photo-menu button:nth-child(3)')
        pg.wait_for_timeout(1500)"""),
("""    try:
        with pg.expect_file_chooser(timeout=2500) as fc:
            tape(pg, '#createSheet .ph-photo-btn')
        t(tag + ' F · page + : le bouton ouvre le sélecteur, sans menu', fc.value is not None and not menu(pg))
    except Exception as e:
        t(tag + ' F · page + : le bouton ouvre le sélecteur, sans menu', False, str(e)[:120])""",
 """    # v132 : la page + ouvre le même menu — « Dessiner », puis « Importer une image », qui ouvre le sélecteur
    tape(pg, '#createSheet .ph-photo-btn'); mp = menu(pg)
    t(tag + ' F · page + : le bouton ouvre le menu, « Dessiner » en tête puis « Importer une image »', bool(mp) and mp['mots'][:2] == ['Dessiner', 'Importer une image'], str(mp))
    try:
        with pg.expect_file_chooser(timeout=2500) as fc:
            tape(pg, '.ph-photo-menu button:nth-child(2)')
        t(tag + ' F · page + : « Importer une image » ouvre le sélecteur', fc.value is not None)
    except Exception as e:
        t(tag + ' F · page + : « Importer une image » ouvre le sélecteur', False, str(e)[:120])"""),
])
# ── décisions : le lilas éclairci et le libellé de suppression
patch('redteam_decisions.py',[
("""print('\\n%d / %d' % (ok[0], ok[0] + len(ko)))""",
 """# ⚑ v132 (Tom, 5 oct. 2026) — deux décisions de plus, lues à l'écran :
#   C-054 · « la phrase lilas de la page + garde sa teinte, éclaircie jusqu'à 4,5:1 » → #DAC3FF sur le cobalt (4,51:1), en sombre ;
#   C-053 · « SUPPRIMER CE PROMI passe en crème #F7F0DE : le #DD4D23 est une couleur d'état et ne sert à rien d'autre » (encre en clair).
for cle, val, src in V132:
    cond = cle[1] == val
    if cond: ok[0] += 1
    else: ko.append(cle[0])
    print('%-44s décidé %-8s rendu %-8s %s   (%s)' % (cle[0], val, cle[1], 'OK' if cond else 'KO', src))
print('\\n%d / %d' % (ok[0], ok[0] + len(ko)))"""),
("""        # l'anneau : ses arcs ne portent que les trois états""",
 """        if th == 'dark':
            pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3500)
            for sel, nom in (('#csPhrase .ph-li', 'page + [dark] phrase'), ('#csPhrase .ph-hint', 'page + [dark] consigne')):
                V132.append(((nom, hexa(pg.evaluate("(s)=>{const e=document.querySelector(s); return e?getComputedStyle(e).color:null}", sel))), '#DAC3FF', 'v132 (C-054) : le lilas éclairci à 4,5:1'))
        pg.evaluate("()=>{closeAll(); const p=promises.filter(q=>q.title==='nager le mardi')[0]; openDetail(p.id);}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
        V132.append((('Peaufiner [%s] « Supprimer ce Promi »' % th, hexa(pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-reg.v16-danger .s2-lab'); return e?getComputedStyle(e).color:null}"))), CREME if th == 'dark' else ENCRE, 'v132 (C-053) : jamais l\\'orange d\\'état'))
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(400)
        # l'anneau : ses arcs ne portent que les trois états"""),
("""FICHES = [('Promi à tenir', 'faire les crêpes'),""","""V132 = []
FICHES = [('Promi à tenir', 'faire les crêpes'),"""),
])
# ── couleurs de référence : E9
patch('redteam_couleurs_ref.py',[
("""                    ecarts.append((cle, k, pr_, va, vr))
            for k, c in a['c'].items():""",
 """                    # E9 (v132) : le lilas éclairci de la page + d'un Promi en sombre ; le libellé « Supprimer ce Promi / ce Chiche » et sa corbeille
                    if cle[1] == 'dark' and cle[0] == 'page +' and va and vr and '196, 162, 245' in vr and va == vr.replace('196, 162, 245', '218, 195, 255'): exceptions['E9'] += 1; continue
                    if cle[0].startswith('Peaufiner') and 'Nuée' not in cle[0] and va and vr and '221, 77, 35' in vr and va == vr.replace('221, 77, 35', '247, 240, 222' if cle[1] == 'dark' else '32, 25, 8') and re.search(r'danger|s2-lab|s2-reg', k): exceptions['E9'] += 1; continue
                    ecarts.append((cle, k, pr_, va, vr))
            for k, c in a['c'].items():"""),
("""exceptions = {'E1': 0, 'E3': 0, 'E4': 0, 'E5': 0, 'E6': 0, 'E7': 0, 'E8': 0}""","""exceptions = {'E1': 0, 'E3': 0, 'E4': 0, 'E5': 0, 'E6': 0, 'E7': 0, 'E8': 0, 'E9': 0}"""),
("""  E7  v123 §2 : en sombre, l'ombre de la Pelote""","""  E9  v132 (Tom, 5 oct. 2026) : ① la phrase lilas de la page + d'un Promi, en sombre : #C4A2F5 → #DAC3FF (éclaircie à 4,5:1 sur le cobalt) ;
      ② « SUPPRIMER CE PROMI / CE CHICHE » et sa corbeille, dans le Peaufiner d'une fiche : #DD4D23 → crème en sombre, encre en clair.
  E7  v123 §2 : en sombre, l'ombre de la Pelote"""),
])
print('ok')
