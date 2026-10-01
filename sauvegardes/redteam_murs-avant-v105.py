#!/usr/bin/env python3
"""
redteam_murs.py — LES MURS DU CERCLE (Tom, 30 sept. 2026). WebKit, au doigt, deux thèmes.

  1 · aucun encart « Le Cercle » sur un mur (Peaufiner d'une fiche, Aura, aide, Studio) — le réglage reste FLOUTÉ à 4,8 px, sans explication
  2 · la toute première fois : la phrase 1 monte, puis la page de l'offre s'ouvre SEULE (≤ 2,5 s)
  3 · ensuite : toucher un mur fait monter la phrase SUIVANTE, qui RESTE (encore là 3 s après) sans ouvrir l'offre ;
      toucher n'importe où ouvre l'offre, et l'écran d'où l'on vient est toujours là dessous
  4 · le compteur est GLOBAL : la phrase suivante vient d'une autre zone (l'Aura) sans repartir de 1
  5 · les 21 phrases dans l'ordre, EN DUR ci-dessous (la 21e à la 21e touche) ; au-delà, au hasard sans jamais répéter la précédente
  6 · une longue absence (plus que ABSENCE_JOURS) remet le compteur à zéro
  7 · la phrase se lit : son texte à la couleur d'accent, « Ma Parole ! » dans une autre couleur, et les deux à Δlum ≥ 42 du fond
  8 · Cercle payé : rien de flouté, rien ne monte
Prouvé contre sauvegardes/app-avant-v104b.html.
"""
import sys, json
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
ABSENCE_JOURS = 14          # à valider (QUESTIONS) — la « longue absence »
FLOU = 'blur(4.8px)'      # Tom, 30 sept. : « deux fois plus flou » (2,4 → 4,8), un seul flou pour tous les murs hors Studio
AUTO_MAX = 2500; RESTE_MS = 3000; DLUM = 42
MP = 'Ma Parole !'
PHRASES = ['Eh non ! Mais avec ' + MP + ', oui.', 'Toujours pas. Avec ' + MP + ', si.', 'Je vois bien que ça te titille. ' + MP + ' lève tout ça.',
    'Tiens tiens, on dirait que ça commence à t’intéresser…', 'Tu connais déjà la solution, me semble-t-il.', 'Tu sais où trouver ' + MP + ' maintenant.',
    'Je commence à connaître tes habitudes.', 'Je crois qu’on commence à bien se connaître.', 'C’est sûr de sûr que tu ne veux pas essayer ?',
    'Allons bon. Nous y voilà à nouveau.', 'Entre nous, tu sais très bien ce qu’il faudrait faire.', 'À ce stade, autant arrêter de négocier, non ?',
    'Tu peux continuer. Je ne dirai rien.', 'Tu sais, je ne vais pas te juger.', MP + ' aussi, ça peut durer longtemps.',
    'Je crois que tu essaies de me faire changer d’avis.', 'On pourrait presque appeler ça une tradition.', 'Tu commencerais presque à connaître le chemin.',
    'On commence à avoir nos petites habitudes.', 'Je vais finir par croire que tu viens juste me voir.', 'On se dit directement à la prochaine ?']
res = []
def t(nom, ok, detail=''):
    res.append(ok); print(('  ✅ ' if ok else '  ❌ ') + nom + ('  — ' + detail if detail else ''))

ETAT = """()=>{const p=document.getElementById('murPhrase');const ps=document.getElementById('plusScreen');
  return {leve:!!(p&&p.classList.contains('leve')),texte:p?p.textContent:null,offre:!!(ps&&ps.classList.contains('show'))}}"""
def ferme_offre(pg):
    pg.evaluate("()=>{const c=document.querySelector('#plusScreen .closeb,#plusScreen [data-close]');if(c)c.click();}"); pg.wait_for_timeout(700)
def peaufiner(pg):
    pg.evaluate("()=>{closeAll();const p=promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0];openDetail(p.id);}"); pg.wait_for_timeout(1300)
    pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
    return pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(!e)return null;const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
def lum(c):
    import re; v = [float(x) for x in re.findall(r'[\d.]+', c)[:3]]; return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]

with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('dark', 'light'):
        print('\n══ %s' % th)
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}")
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(7000)
        pg.evaluate("t=>{setTheme(t);setPremium(false);try{localStorage.removeItem('promi_murs')}catch(e){}}", th); pg.wait_for_timeout(500)

        # 1 · plus d'encart, le flou reste
        c = peaufiner(pg)
        enc = pg.evaluate("""()=>{const v=e=>e&&e.getClientRects().length&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden';
          const blk=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)'); const reg=blk&&blk.querySelector('.s2-reg');
          return {encart:!!v(blk&&blk.querySelector('.s2-encart')), flou:reg?getComputedStyle(reg).filter:null}}""")
        t('1a · Peaufiner : plus d\'encart « Le Cercle », les réglages restent floutés', enc['encart'] is False and (enc['flou'] or '')==FLOU, str(enc))

        # 2 · la toute première fois
        e0 = None
        if c:
            pg.touchscreen.tap(*c); pg.wait_for_timeout(400); e0 = pg.evaluate(ETAT)
            pg.wait_for_timeout(AUTO_MAX); e1 = pg.evaluate(ETAT)
        t('2 · première fois : la phrase 1 monte, puis l\'offre s\'ouvre seule', bool(e0 and e0['leve'] and e0['texte'] == PHRASES[0] and e1['offre']),
          'phrase %r · offre %s' % ((e0 or {}).get('texte'), (e1 or {}).get('offre') if e0 else None))
        ferme_offre(pg)

        # 3 · ensuite : la phrase reste, puis un toucher n'importe où ouvre l'offre
        pg.touchscreen.tap(*c); pg.wait_for_timeout(RESTE_MS); e2 = pg.evaluate(ETAT)
        t('3a · deuxième toucher : la phrase 2, qui RESTE, sans ouvrir l\'offre', e2['leve'] and e2['texte'] == PHRASES[1] and not e2['offre'], '%r · offre %s' % (e2['texte'], e2['offre']))
        pg.touchscreen.tap(215, 200); pg.wait_for_timeout(900); e3 = pg.evaluate(ETAT)
        dessous = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
        t('3b · toucher ailleurs : l\'offre s\'ouvre, la fiche est toujours là dessous', e3['offre'] and not e3['leve'] and dessous, 'offre %s · fiche %s' % (e3['offre'], dessous))
        ferme_offre(pg)

        # 7 · la phrase se lit (mesurée sur la phrase 3, qui porte « Ma Parole ! »)
        pg.touchscreen.tap(*c); pg.wait_for_timeout(700)
        col = pg.evaluate("""()=>{const p=document.getElementById('murPhrase');if(!p)return {fond:'rgb(0,0,0)',texte:'rgb(0,0,0)',mp:null};const m=p.querySelector('.mp');const s=getComputedStyle(p);
          return {fond:s.backgroundColor,texte:s.webkitTextFillColor||s.color,mp:m?(getComputedStyle(m).webkitTextFillColor||getComputedStyle(m).color):null,
            accent:getComputedStyle(document.getElementById('device')).getPropertyValue('--c-bleu45-txt').trim()}}""")
        e4 = pg.evaluate(ETAT)
        ok7 = col['mp'] and col['mp'] != col['texte'] and abs(lum(col['texte']) - lum(col['fond'])) >= DLUM and abs(lum(col['mp']) - lum(col['fond'])) >= DLUM
        t('7 · phrase à l\'accent, « Ma Parole ! » d\'une autre couleur, les deux lisibles (Δlum ≥ %d)' % DLUM, bool(ok7 and e4['texte'] == PHRASES[2]),
          'texte %s · Ma Parole %s · fond %s · Δ %.0f / %.0f' % (col['texte'], col['mp'], col['fond'], abs(lum(col['texte']) - lum(col['fond'])), abs(lum(col['mp']) - lum(col['fond'])) if col['mp'] else -1))
        pg.evaluate("()=>{window._murBaisse&&_murBaisse();closeAll();}"); pg.wait_for_timeout(700)

        # 4 · le compteur est global : l'Aura prend la suite (phrase 4)
        pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(600)
        a = pg.evaluate("""()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2');if(!e)return null;const q=e.getBoundingClientRect();
          const enc=document.querySelector('#auraScreen .au-enc2');return {c:[q.left+q.width/2,q.top+q.height/2],flou:getComputedStyle(e).filter,encart:!!(enc&&enc.getClientRects().length)}}""")
        e5 = None
        if a: pg.touchscreen.tap(*a['c']); pg.wait_for_timeout(700); e5 = pg.evaluate(ETAT)
        t('1b · Aura : plus d\'encart, « Ce qu\'on t\'a tenu » flouté', bool(a and not a['encart'] and a['flou']==FLOU), str(a and {k: a[k] for k in ('flou', 'encart')}))
        t('4 · compteur global : l\'Aura fait monter la phrase 4', bool(e5 and e5['leve'] and e5['texte'] == PHRASES[3]), repr(e5 and e5['texte']))
        pg.evaluate("()=>{window._murBaisse&&_murBaisse();}")

        # 5 · l'ordre jusqu'à 21, puis le hasard sans répétition
        pg.evaluate("()=>localStorage.setItem('promi_murs',JSON.stringify({n:20,t:Date.now(),der:19,decouvert:1}))")
        pg.evaluate("()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(400)
        a = pg.evaluate("()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2')||document.querySelector('#auraScreen .au-gr2');const q=e.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
        pg.touchscreen.tap(*a); pg.wait_for_timeout(600); e6 = pg.evaluate(ETAT); pg.evaluate("()=>{window._murBaisse&&_murBaisse()}"); pg.wait_for_timeout(300)
        t('5a · la 21e touche fait monter la 21e phrase', e6['texte'] == PHRASES[20], repr(e6['texte']))
        suite = []
        for k in range(24):
            pg.touchscreen.tap(*a); pg.wait_for_timeout(250); suite.append(pg.evaluate(ETAT)['texte']); pg.evaluate("()=>{window._murBaisse&&_murBaisse()}"); pg.wait_for_timeout(120)
        rep = sum(1 for i in range(1, len(suite)) if suite[i] == suite[i - 1]) + (1 if suite and suite[0] == PHRASES[20] else 0)
        distinct = len(set(suite)); horsliste = [s for s in suite if s not in PHRASES]
        t('5b · au-delà : au hasard, jamais deux fois la même de suite', rep == 0 and distinct >= 8 and not horsliste, '%d tirages, %d distinctes, %d répétitions, %d hors liste' % (len(suite), distinct, rep, len(horsliste)))

        # 6 · longue absence
        pg.evaluate("j=>localStorage.setItem('promi_murs',JSON.stringify({n:9,t:Date.now()-(j+1)*86400000,der:8,decouvert:1}))", ABSENCE_JOURS)
        pg.touchscreen.tap(*a); pg.wait_for_timeout(600); e7 = pg.evaluate(ETAT); pg.evaluate("()=>{window._murBaisse&&_murBaisse()}")
        auto = pg.evaluate(ETAT)
        t('6 · après une longue absence le compteur repart à la phrase 1 (sans rouvrir l\'offre seule)', e7['texte'] == PHRASES[0], repr(e7['texte']))

        # 8 · Cercle payé
        pg.evaluate("()=>{closeAll();setPremium(true);}"); pg.wait_for_timeout(600)
        c = peaufiner(pg)
        if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(700)
        e8 = pg.evaluate(ETAT); fl = pg.evaluate("()=>{const r=document.querySelector('#detailPoster .s2-cercle .s2-reg');return r?getComputedStyle(r).filter:null}")
        t('8 · Cercle payé : rien de flouté, rien ne monte', not e8['leve'] and not e8['offre'] and (fl in (None, 'none')), 'phrase %s · offre %s · filtre %s' % (e8['leve'], e8['offre'], fl))
        ctx.close()
    b.close()

n = len(res); k = sum(res)
print('\n%d/%d' % (k, n))
sys.exit(0 if k == n else 1)
