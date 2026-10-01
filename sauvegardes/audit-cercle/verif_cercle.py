# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# LE JUGE DE L'ÉCRAN QUI VEND — version « Toile de démonstration en dalles superposées » (12 septembre 2026).
# Il REMPLACE la famille D de `verif_seuil.py`, qui mesurait l'écran d'avant (rangée de trois dalles, « 29 € ») :
# cet écran n'existe plus, `lot-CERCLE-VEND` est retiré. Un contrôle qui passe au vert sur du vide est pire
# qu'aucun contrôle — c'est pour ça que celui-ci est écrit.
#
# ⚑ LES VALEURS DÉCIDÉES SONT EN DUR ICI (CLAUDE §7 : un juge qui lit la valeur qu'il vérifie ne vérifie rien).
#   Le prix, le titre, le mauve, le plancher de fond, le nombre de mondes, la part de Touffe : le juge porte la
#   décision, l'app la respecte — jamais l'inverse.
# ⚑ ET IL EST PROUVÉ CONTRE DE VRAIS DÉFAUTS par `preuve_vend.py` (l'écran) et `preuve_vide.py` (sans Promi).
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
import io, json, os, re, sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(D, '..', '..', 'app.html')

# ── LES DÉCISIONS, EN DUR ──────────────────────────────────────────────────────────────────────────────────
TITRE   = 'Rejoins le Cercle !'
PRIX    = '39 €'
MOIS    = 'soit 3,25 €/mois'
# ⚑ 14 sept. 2026, Tom : l'annuel en avant (39 €, soit 3,25 €/mois) ; « le mensuel à 5,99 € est une option, pas le prix de l'écran ».
#    L'option répétait 39 € : elle porte maintenant le mois. Original : verif_cercle-avant-prix-5-99.py
OPTION  = 'ou le mois — 5,99 €'
LEGAL   = 'Sans engagement · résiliable à tout moment'
MAUVE   = (138, 92, 240)          # #8A5CF0, §3 — « Cercle » dans le titre
FRAMB   = (250, 34, 88)           # #FA2258 — le CTA
PLI     = 844                     # rien ne descend en dessous, et l'écran ne défile pas
FOND_MAX = 8.0                    # % de pixels transparents tolérés dans la Toile (recouvrement)
MONDES  = ['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo']
TOUFFE  = (18.0, 42.0)            # part des poses : dominante, sans tout manger
COTE_MIN = 40                     # une dalle de la collection ne descend pas sous 40 px : sinon c'est du confetti

BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"

ETAT = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390;
  const C=document.getElementById('pcCadre'); if(!C) return {absent:true};
  const rgb=t=>{const m=String(t).match(/\d+/g); return m?m.slice(0,3).map(Number):null;};
  const q=sel=>{const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect(), k=getComputedStyle(e);
    return {y:+((r.top-dv.top)/s).toFixed(1), x:+((r.left-dv.left)/s).toFixed(1), w:+(r.width/s).toFixed(1),
            h:+(r.height/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1),
            txt:(e.textContent||'').replace(/ /g,' ').trim(), col:rgb(k.color), fond:rgb(k.backgroundColor),
            ff:k.fontFamily.split(',')[0].replace(/["']/g,''), fw:k.fontWeight, fs:parseFloat(k.fontSize), vis:e.checkVisibility()};};
  const o={sans:C.classList.contains('pc-sans'), vend:window._vendToile||null, fond:window._vendFond||null};
  o.fermer=q('#plusScreen .closeb'); o.toile=q('#pcCadre .pc-toile'); o.titre=q('#pcCadre .pc-h');
  o.h1=q('#pcCadre .pc-h1'); o.h2=q('#pcCadre .pc-h2'); o.h3=q('#pcCadre .pc-h3');
  o.sous=q('#pcCadre .pc-sub'); o.prix=q('#pcCadre .pc-prix b'); o.mois=q('#pcCadre .pc-prix i');
  o.cta=q('#pcCadre #buyMonth'); o.option=q('#pcCadre #buyYear'); o.legal=q('#pcCadre .pc-legal');
  o.args=[...document.querySelectorAll('#pcCadre .pc-arg')].map(e=>{const r=e.getBoundingClientRect();
    return {y:+((r.top-dv.top)/s).toFixed(1), bas:+(((r.top-dv.top)+r.height)/s).toFixed(1),
            t:e.querySelector('b').textContent, d:e.querySelector('i').textContent.replace(/\s+/g,' ').trim(),
            ff:getComputedStyle(e.querySelector('b')).fontFamily.split(',')[0].replace(/["']/g,''),
            fw:getComputedStyle(e.querySelector('b')).fontWeight};});
  /* les pastilles : de vraies dalles, rendues à leur taille — le canevas et l'affichage doivent coïncider */
  const dpr=Math.min(2,window.devicePixelRatio||1);
  o.pastilles=[...document.querySelectorAll('#pcCadre .pc-ch')].map(c=>{const k=getComputedStyle(c);
    return {m:c.getAttribute('data-m'), dalle:c.getAttribute('data-dalle'), ech:c.getAttribute('data-echelle'),
            px:[c.width,c.height], css:[parseFloat(k.width),parseFloat(k.height)], vis:c.checkVisibility()};});
  /* la Toile : part de pixels transparents */
  const cv=document.querySelector('#pcCadre .pc-toile canvas');
  if(cv && cv.width>4){ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
    let n=0,vide=0; for(let i=3;i<d.length;i+=16){ n++; if(d[i+3]<20) vide++; }
    o.canevas={px:[cv.width,cv.height], vide:+(100*vide/n).toFixed(2)}; } else o.canevas=null;
  const sc=document.getElementById('plusScreen');
  o.ecran={defile:sc.scrollHeight>sc.clientHeight, show:sc.classList.contains('show')};
  o.promi=(typeof promises!=='undefined'?promises.filter(p=>!p.draft&&!p.req).length:null);
  return o; }"""

def blocs(e):
    """les blocs de texte, de haut en bas — pour chercher un chevauchement"""
    b = [e['titre'], e['sous']] + e['args'] + [e['prix'], e['cta'], e['option'], e['legal']]
    return [x for x in b if x]

def contrats(e, th):
    """rend la liste des (nom, ok, ce qu'on a trouvé). Chaque contrat NOMME ce qu'il a vu."""
    C = []
    def c(nom, ok, dit): C.append((nom, bool(ok), dit))
    if e.get('absent'):
        c('le cadre existe', False, 'aucun #pcCadre'); return C
    v = e['vend'] or {}
    # ⚑ LE JUGE BRANCHE SUR LA DONNÉE, JAMAIS SUR LA CLASSE QU'IL VÉRIFIE (§7). Il lisait `pc-sans` — la classe
    #   que l'app POSE : la retirer ne faisait pas rougir « la Toile est cachée », ça faisait basculer le juge
    #   dans l'autre famille. C'est le piège « un juge qui lit la valeur qu'il vérifie ». Le nombre de Promi est
    #   la cause ; la classe est l'effet, et elle devient un contrat à part entière.
    sans = (e['promi'] == 0) if e['promi'] is not None else e['sans']

    # ── les mots et le prix : le juge porte la décision
    c('le titre est celui décidé', e['titre'] and e['titre']['txt'] == TITRE,
      '« %s » (décidé « %s »)' % (e['titre']['txt'] if e['titre'] else '—', TITRE))
    c('« Cercle » est en mauve', e['h2'] and tuple(e['h2']['col'] or ()) == MAUVE,
      '%s (décidé %s)' % (e['h2']['col'] if e['h2'] else '—', list(MAUVE)))
    c('« Rejoins le » et « ! » sont en encre',
      e['h1'] and e['h3'] and tuple(e['h1']['col'] or ()) != MAUVE and tuple(e['h3']['col'] or ()) != MAUVE,
      'le « ! » %s' % (e['h3']['col'] if e['h3'] else '—'))
    c('le prix est celui décidé', e['prix'] and e['prix']['txt'] == PRIX and e['mois'] and e['mois']['txt'] == MOIS,
      '« %s » · « %s »' % (e['prix']['txt'] if e['prix'] else '—', e['mois']['txt'] if e['mois'] else '—'))
    c('l’option porte le prix', e['option'] and e['option']['txt'] == OPTION,
      '« %s » (décidé « %s »)' % (e['option']['txt'] if e['option'] else '—', OPTION))
    c('le légal est celui décidé', e['legal'] and e['legal']['txt'] == LEGAL, '« %s »' % (e['legal']['txt'] if e['legal'] else '—'))
    c('le CTA est en framboise', e['cta'] and tuple(e['cta']['fond'] or ()) == FRAMB,
      '%s (décidé %s)' % (e['cta']['fond'] if e['cta'] else '—', list(FRAMB)))
    c('le ✕ FERMER est celui du produit', e['fermer'] and e['fermer']['vis'] and 'FERMER' in e['fermer']['txt'].upper(),
      '« %s » à %s' % (e['fermer']['txt'] if e['fermer'] else '—', [e['fermer']['x'], e['fermer']['y']] if e['fermer'] else '—'))

    # ── la mise en page
    B = blocs(e)
    chev = [(B[i]['bas'], B[i+1]['y']) for i in range(len(B)-1) if B[i+1]['y'] < B[i]['bas'] - 0.5]
    c('aucun bloc n’en chevauche un autre', not chev, '%d chevauchement(s) %s' % (len(chev), chev[:2]))
    bas = max(x['bas'] for x in B) if B else 0
    c('rien ne descend sous le pli', bas <= PLI, 'le plus bas %s (pli %d)' % (bas, PLI))
    c('l’écran ne défile pas', not e['ecran']['defile'], 'défile=%s' % e['ecran']['defile'])
    c('l’essai est visible sans défiler', e['cta'] and e['cta']['bas'] <= PLI,
      'bas de l’essai %s' % (e['cta']['bas'] if e['cta'] else '—'))

    # ── les polices du produit
    c('les libellés sont en Bricolage 600',
      all(a['ff'] == 'Bricolage' and a['fw'] == '600' for a in e['args']) if e['args'] else False,
      ' · '.join('%s %s' % (a['ff'], a['fw']) for a in e['args']))
    c('le titre et le prix sont en Fraunces 600',
      e['titre'] and e['titre']['ff'] == 'Fraunces' and e['titre']['fw'] == '600'
      and e['prix'] and e['prix']['ff'] == 'Fraunces',
      'titre %s %s · prix %s' % (e['titre']['ff'], e['titre']['fw'], e['prix']['ff'] if e['prix'] else '—'))

    # ── SANS AUCUN PROMI : le cadre s'efface et tout remonte
    if sans:
        c('sans Promi · le cadre porte pc-sans', e['sans'], 'pc-sans=%s (0 Promi)' % e['sans'])
        c('sans Promi · la collection est vide', (v.get('collection') or 0) == 0,
          'collection %s' % v.get('collection'))
        c('sans Promi · la Toile est cachée', e['toile'] and not e['toile']['vis'], 'Toile visible=%s' % (e['toile']['vis'] if e['toile'] else '—'))
        c('sans Promi · les pastilles sont cachées', all(not p['vis'] for p in e['pastilles']),
          '%d pastille(s) visible(s)' % sum(1 for p in e['pastilles'] if p['vis']))
        c('sans Promi · tout est remonté', e['titre'] and e['titre']['y'] < 200, 'titre à y=%s' % (e['titre']['y'] if e['titre'] else '—'))
        return C

    # ── LA TOILE — de vraies dalles, superposées
    c('la Toile est faite de vraies dalles', v.get('collection', 0) > 0 and v.get('poses', 0) > 0,
      'collection %s · %s poses' % (v.get('collection'), v.get('poses')))
    c('le fond ne paraît pas', e['canevas'] and e['canevas']['vide'] <= FOND_MAX,
      'vide %s %% (plancher %s)' % (e['canevas']['vide'] if e['canevas'] else '—', FOND_MAX))
    mats = v.get('matieres') or {}
    c('les huit mondes sont présents', len(mats) == len(MONDES), '%d monde(s) : %s' % (len(mats), sorted(mats)))
    tot = sum(mats.values()) or 1
    part = 100.0 * mats.get('touffe', 0) / tot
    c('la Touffe domine sans tout manger', TOUFFE[0] <= part <= TOUFFE[1], 'Touffe %.1f %% (fenêtre %s)' % (part, list(TOUFFE)))
    cotes = v.get('cotes') or []
    # la grandeur juste est la MOYENNE GÉOMÉTRIQUE : le plus petit côté condamnait une cellule allongée (31 × 61)
    # qui n'est pas du confetti — son aire vaut celle d'une dalle de 44.
    petites = [x for x in cotes
               if (lambda a, b: (a * b) ** 0.5 < COTE_MIN)(*[int(n) for n in x.split('×')])]
    c('les dalles ne sont pas du confetti', not petites, 'cotes %s (plancher %d)' % (cotes[:4], COTE_MIN))

    # ── les pastilles : de vraies dalles, peintes À LEUR TAILLE
    # ⚑ LE CONTRAT DÉPEND DES DONNÉES, PAS D'UN VŒU : s'il n'y a aucun Promi, il n'y a AUCUNE dalle à peindre,
    #    et le bon résultat est ZÉRO pastille — jamais un canevas vide redimensionné. Avec des Promi : exactement
    #    trois, chacune déclarant sa dalle et son échelle. (La première écriture exigeait trois dans tous les cas :
    #    elle condamnait le comportement juste et couvrait le mauvais.)
    P = [p for p in e['pastilles'] if p['vis']]
    n_att = 3 if (e.get('promi') or 0) > 0 else 0
    c('les pastilles suivent les données (%d attendue(s))' % n_att,
      len(P) == n_att and all(p['dalle'] and p['ech'] for p in P),
      '%d pastille(s) · %s' % (len(P), [(p['m'], p['dalle'], p['ech']) for p in P]))
    mal = [p for p in P if not p['px'][0] or abs(p['px'][0] / 2.0 - p['css'][0]) > 1.1]
    c('aucune pastille n’est redimensionnée', not mal,
      '%d écart(s) canevas/affichage %s' % (len(mal), [(p['px'], p['css']) for p in mal[:2]]))

    # ── le bâti de fond
    f = e['fond'] or {}
    c('la collection se bâtit en fond', f.get('total', 0) > 0, 'fond %s/%s' % (f.get('faites'), f.get('total')))
    return C

STATIQUE = None
def statique():
    """⚑ AUCUNE DÉCOUPE D'IMAGE — se lit dans le FICHIER, pas à l'écran (Tom, quatre fois)."""
    global STATIQUE
    if STATIQUE is not None: return STATIQUE
    S = io.open(APP, encoding='utf-8').read()
    a = S.find('<style id="lot-CERCLE-TOILE-css">')
    b = S.find('</script>', S.find('<script id="lot-CERCLE-TOILE">'))
    lot = S[a:b] if a > 0 and b > a else ''
    draws = re.findall(r'drawImage\s*\(([^;]{0,200})', lot)
    neuf = [d for d in draws if d.count(',') >= 8]       # 9 arguments = un rectangle SOURCE = une découpe
    out = [
      ('le lot existe', bool(lot), '%d caractères' % len(lot)),
      ('aucune découpe d’image (drawImage à 9 arguments)', not neuf, '%d sur %d appels' % (len(neuf), len(draws))),
      ('aucun choix de pixels (getImageData)', 'getImageData' not in lot, '%d' % lot.count('getImageData')),
      ('aucun report de pixels (putImageData)', 'putImageData' not in lot, '%d' % lot.count('putImageData')),
      ('le moteur peint à la taille finale (dalleTrame avec k)',
       lot.count('dalleTrame(cv, id, k') + lot.count('dalleTrame(ch, id, k') >= 2,
       '%d appel(s) avec échelle' % (lot.count('dalleTrame(cv, id, k') + lot.count('dalleTrame(ch, id, k'))),
      ('l’ancien lot est retiré, pas neutralisé', 'lot-CERCLE-VEND' not in S and 'plCadre' not in S,
       'lot-CERCLE-VEND %d · plCadre %d' % (S.count('lot-CERCLE-VEND'), S.count('plCadre'))),
    ]
    STATIQUE = out
    return out

def ouvre(pg, th, vider=False, attendre=True):
    pg.goto(URL, timeout=180000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setPremium(false)")
    if vider: pg.evaluate("()=>{ promises.length=0; }")
    pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(2200)
    if attendre and not vider:
        try:
            pg.wait_for_function("(t)=>{const f=window._vendFond; return f && f.total>0 && f.faites>=f.total && f.cle && f.cle.indexOf(t)>=0;}",
                                 arg=('clair' if th == 'light' else 'sombre'), timeout=150000)
        except Exception: pass
    pg.evaluate(BASE); pg.wait_for_timeout(300)
    pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
    pg.wait_for_timeout(2600)

def passe(sonde=None, vise=None):
    """une passe complète. `sonde` = du JS posé avant la mesure (pour les preuves). Rend (verts, rouges, journal)."""
    verts, rouges, journal = 0, [], []
    for nom, ok, dit in statique():
        journal.append(('statique', nom, ok, dit))
        if ok: verts += 1
        else: rouges.append(('statique', nom, dit))
    with sync_playwright() as p:
        br = p.chromium.launch()
        for th in ('light', 'dark'):
            for cas, vider in (('avec Promi', False), ('sans Promi', True)):
                pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
                ouvre(pg, th, vider)
                if sonde:
                    try: pg.evaluate(sonde)
                    except Exception as ex: journal.append((th, 'la sonde s’applique', False, str(ex)[:80]))
                    pg.wait_for_timeout(400)
                e = pg.evaluate(ETAT)
                for nom, ok, dit in contrats(e, th):
                    journal.append(('%s · %s' % (th, cas), nom, ok, dit))
                    if ok: verts += 1
                    else: rouges.append(('%s · %s' % (th, cas), nom, dit))
                pg.context.close()
        # la Toile change-t-elle d'une ouverture à l'autre ?
        pg = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2).new_page()
        ouvre(pg, 'dark')
        sigs = []
        for _ in range(3):
            sigs.append(pg.evaluate("()=>{const v=window._vendToile; return v?v.sig:null;}"))
            pg.evaluate(BASE); pg.wait_for_timeout(400)
            pg.evaluate("()=>{ const x=document.querySelector('.set-cercle'); if(x) x.click(); }")
            pg.wait_for_timeout(2400)
        ok = len(set(s for s in sigs if s)) == len([s for s in sigs if s]) and len([s for s in sigs if s]) == 3
        journal.append(('dark', 'la Toile change à chaque ouverture', ok, '%d signature(s) distincte(s) sur 3' % len(set(sigs))))
        if ok: verts += 1
        else: rouges.append(('dark', 'la Toile change à chaque ouverture', '%d sur 3' % len(set(sigs))))
        pg.context.close(); br.close()
    return verts, rouges, journal

if __name__ == '__main__':
    v, r, j = passe()
    for ou, nom, ok, dit in j:
        print('%-22s %-46s %s  %s' % (ou, nom, 'OK ' if ok else 'KO ', dit))
    print()
    if r:
        print('❌  %d ÉCART(S)' % len(r))
        for ou, nom, dit in r: print('   · %s · %s — %s' % (ou, nom, dit))
    else:
        print('✅  %d CONTRATS TENUS — l’écran qui vend, deux thèmes, avec et sans Promi.' % v)
