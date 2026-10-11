# -*- coding: utf-8 -*-
"""redteam_engagement.py — LA GRILLE DU CHANTIER D'ENGAGEMENT, VÉRIFIABLE PAR MACHINE (E0, C-073).

Source : ENGAGEMENT.md, E0 point 2, et les AMENDEMENTS DU CHEF DE CHANTIER, qui priment (A2, A3, A4). Il passe à la fin de CHAQUE lot E.
Chromium sans tête, sur le serveur du projet (http://127.0.0.1:8752 — la règle du dépôt, à la place du `file://` du document).

  R1  LEXIQUE. Le texte de tous les éléments visibles de chaque écran parcouru, plus toutes les chaînes de `TEXTES_ENGAGEMENT`. Échec si un
      mot de la liste interdite y paraît (insensible à la casse, frontières de mots). ⚑ A4 : la liste s'aligne sur le lexique de CLAUDE.md §2 ;
      « échéance » en est retiré si l'app l'emploie (constaté à l'écran, et dit). ⚑ A3 : aucun texte de `TEXTES_ENGAGEMENT` à l'impératif.
      Liste blanche explicite, une ligne par exception, avec sa justification.
  R2  ABSENCE ET TEMPS. Sur `TEXTES_ENGAGEMENT` : depuis|longtemps|toujours pas|encore rien|tu n'as|oubli|manqu|retard|hier|reviens|revenu|attend.
  R3  AUCUN CHIFFRE SUR LA PELOTE. Aucun nœud de texte visible portant un chiffre dans le cadre de la Pelote (sa boîte, silhouette comprise).
  R4  INVARIANCE DU MOMENT TENIR — INACTIF AVANT E3.
  R5  RIEN NE SE THÉSAURISE. Les clés de `localStorage` avant et après trois « tenir » : aucune clé nouvelle hors liste blanche.
  R6  SORTIE À UN GESTE. À chaque étape de l'onboarding, une sortie visible, activable en un toucher.
  R7  ÂGE INVISIBLE. Sur la Toile et sur une fiche à tenir : aucun texte visible `il y a | depuis N | N j(ours)` (les libellés d'horizon en liste blanche).
  A2  AUCUNE TRANSPARENCE NI FONDU sur les éléments du chantier (ceux qui portent `data-eng`) : opacité 1 sur eux et leurs ancêtres, aucune
      transition ni animation qui touche l'opacité.

Preuve que le juge mord : `--sonde` pose des textes fautifs dans TEXTES_ENGAGEMENT, un élément `data-eng` à demi transparent avec un fondu,
un chiffre sur la Pelote, un âge sur la fiche, une clé de compteur — R1, A3, R2, R3, R5, R7 et A2 doivent ROUGIR.
Usage : python3 redteam_engagement.py [fichier.html] [--sonde]
"""
import io, re, sys, json
from playwright.sync_api import sync_playwright
from redteam_onboarding import POIGNEE, toucher, tracer, PRENOM, PAROLE
F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'
SONDE = '--sonde' in sys.argv
URL = 'http://127.0.0.1:8752/' + F
L = '(?<![a-zàâçéèêëîïôûùüÿœ])'; Rb = '(?![a-zàâçéèêëîïôûùüÿœ])'
# ── LA LISTE INTERDITE (A4) : le lexique de CLAUDE.md §2 (termes bannis), puis les mots de récompense de la règle 4 du chantier.
INTERDITS = [  # (mot affiché, motif)
 ('tâche', 'tâches?'), ('to-do', 'to[- ]?do'), ('objectif', 'objectifs?'), ('valider', 'valid(?:er|e|es|ez|ons|é|ée|és|ées|ation)'), ('urgent', 'urgente?s?|urgence'),
 ('score', 'scores?'), ('brouillon', 'brouillons?'), ('Orbite', 'orbites?'), ('la sphère', 'sphères?'), ('Belle parole', 'belle parole'), ('En replanter un', 'en replanter un'),
 ('Dire un mot', 'dire un mot'),
 ('badge', 'badges?'), ('série', 'séries?'), ('streak', 'streaks?'), ('niveau', 'niveaux?'), ('classement', 'classements?'), ('points (récompense)', 'points?'),
 ('bravo', 'bravos?'), ('félicitations', 'félicitations?'), ('record', 'records?')]
ECHEANCE = ('échéance', 'échéances?')            # A4 : retiré de la liste si l'app l'emploie — on le CONSTATE, on ne le suppose pas
# ── LA LISTE BLANCHE DE R1 : (mot, ce que le texte doit contenir, justification) — une ligne par exception
BLANCHE_R1 = []
R2_MOTIF = r"depuis|longtemps|toujours pas|encore rien|tu n['’]as|oubli|manqu|retard|hier|reviens|revenu|attend"
# ── A3 : l'impératif. Un verbe en tête de phrase (ou après une virgule, « puis », « et ») à la 2e personne ou à la 1re du pluriel, ou un
#    verbe suivi d'un pronom à trait d'union (« fais-le », « dis-la », « allons-y »).
IMPERATIFS = ('fais faites faisons reviens revenez dis dites ajoute ajoutez lance lancez commence commencez change changez plante plantez trace tracez touche touchez '
              'écris écrivez essaie essaye essayez viens venez va allez allons regarde regardez tiens tenez choisis choisissez prends prenez pose posez garde gardez ouvre ouvrez '
              'appuie appuyez glisse glissez continue continuez promets promettez raconte racontez envoie envoyez invite invitez partage partagez découvre découvrez pense pensez '
              'laisse laissez mets mettez donne donnez montre montrez reprends reprenez relève relevez tente tentez ose osez').split()
IMP_TETE = re.compile(r"(?:^|[.!?…:;]\s+|,\s+|\b(?:puis|et)\s+)(%s)%s" % ('|'.join(IMPERATIFS), Rb), re.I)
IMP_TRAIT = re.compile(r"%s[a-zàâçéèêëîïôûùüÿœ]+(?:e|s|ons|ez|a)-(?:le|la|les|lui|leur|toi|moi|nous|y|en)%s" % (L, Rb), re.I)
BLANCHE_CLES = [  # R5 : ce qui peut naître dans le stockage pendant trois « tenir » — aucun compteur
 ('promi_state', "la sauvegarde des paroles elles-mêmes (leur état), pas un compte"),
 ('promi_fil_vu', "le dernier passage au Fil"), ('promi_pelote_vue', "le tirage de couleur de la Pelote à la dernière ouverture"),
 ('promi_pelote_palier', "le palier de densité appliqué"), ('promi_debut', "la date de première ouverture"),
 ('promi_graine', "la graine du visage"), ('promi_theme', "le thème choisi"), ('promi_sig', "la signature de partage"), ('promi_sigdemo', "idem, jeu de démonstration"),
 ('geste_vu_', "les drapeaux de E1 (un geste déjà montré)"), ('promi_devoile', "E2bis (v140) : ce qui est déjà apparu dans la barre — des drapeaux de PREMIÈRE FOIS (index, aura, studio, fil), jamais un compte"), ('promi_e2', "E2 (v140) : l'étape en cours du premier parcours, retirée à sa fin"), ('ob_fini', "le drapeau de fin de E2"), ('promi_onb', "le verrou de l'onboarding")]
HORIZONS = r"^(?:demain|aujourd['’]hui|ce soir|un jour|cette semaine|\d+ ?jours?|dans \d+ ?j(?:ours)?|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)(?: \d+)?$"   # R7 : un horizon, pas un âge
R7_MOTIF = r"il y a|depuis \d|\d+ ?j(?:ours)?%s" % Rb
HORIZON_DANS = re.compile(r"(?:dans|d['’]ici|sous) \d+ ?j(?:ours?)?%s" % Rb, re.I)   # liste blanche de R7 : « dans N jours » regarde devant, ce n'est pas un âge
ok = [0]; ko = []; inactifs = []
def t(nom, c, d=''):
    if c: ok[0] += 1
    else: ko.append(nom)
    print('%s  %-66s %s' % ('OK' if c else 'KO', nom, str(d)[:330]))
def inactif(nom, d): inactifs.append(nom); print('--  %-66s %s' % (nom, d))
TEXTES = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), out=[];
  const vu=e=>{ const r=e.getBoundingClientRect(); if(r.width<1||r.height<1) return false; if(r.right<dv.left||r.left>dv.right||r.bottom<dv.top||r.top>dv.bottom) return false;
    for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; } return true; };
  const T=document.createTreeWalker(document.getElementById('device').parentElement||document.body, NodeFilter.SHOW_ELEMENT); let e;
  while((e=T.nextNode())){ if(e.tagName==='SCRIPT'||e.tagName==='STYLE'||!vu(e)) continue;
    const txt=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join(' ').replace(/\s+/g,' ').trim();
    [txt, e.getAttribute('aria-label')||'', e.getAttribute('placeholder')||''].forEach(d=>{ if(d) out.push(d); }); }
  return [...new Set(out)]; }"""
def plat(o, pre=''):
    out = []
    if isinstance(o, str): out.append((pre, o))
    elif isinstance(o, list):
        for i, v in enumerate(o): out += plat(v, '%s[%d]' % (pre, i))
    elif isinstance(o, dict):
        for k, v in o.items(): out += plat(v, (pre + '.' if pre else '') + str(k))
    return out
air = io.open('redteam_air.py', encoding='utf-8').read()
ECRANS = [(m.group(1), m.group(2)) for m in re.finditer(r"^ \((?:'|\")(.+?)(?:'|\"),\s*\"(\(\)=>\{.*\})\"\),?\s*$", air, re.M)]
with sync_playwright() as p:
    b = p.chromium.launch()
    # ══ écrans parcourus (l'app après l'onboarding, jeu de démonstration) ══
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=1, has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto(URL); pg.wait_for_timeout(2200); pg.wait_for_timeout(4600)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if SONDE:
        pg.evaluate("""()=>{ window.TEXTES_ENGAGEMENT={a:'Fais-le. Puis reviens le tenir.', b:['La prochaine, dis-la à quelqu’un.', 'Bravo, trois points de plus.'], c:{d:'Tu n’as rien planté depuis longtemps.', e:'Allons-y'}}; }""")
    T_ENG = plat(pg.evaluate("()=>{ try{ return JSON.parse(JSON.stringify(window.TEXTES_ENGAGEMENT)); }catch(e){ return null; } }") or {})
    existe = pg.evaluate("()=>typeof window.TEXTES_ENGAGEMENT==='object' && window.TEXTES_ENGAGEMENT!==null")
    vus = {}
    for nom, js in ECRANS:
        try:
            pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(250)
            pg.evaluate(js); pg.wait_for_timeout(1500)
            vus[nom] = pg.evaluate(TEXTES)
        except Exception as ex: er.append('%s : %s' % (nom, str(ex)[:80]))
    # ── R1
    tous = [(n, d) for n, ds in vus.items() for d in ds]
    emploi_ech = sorted({n for n, d in tous if re.search(L + '(?:' + ECHEANCE[1] + ')' + Rb, d, re.I)})
    liste = list(INTERDITS) + ([] if emploi_ech else [ECHEANCE])
    print('     R1 · liste interdite : %s' % ' · '.join(m for m, _ in liste))
    print('     R1 · « échéance » : %s' % ("l'app l'emploie à l'écran (%s) → RETIRÉ de la liste (A4)" % ', '.join(emploi_ech[:4]) if emploi_ech else "l'app ne l'affiche sur aucun écran parcouru → il RESTE dans la liste (A4)"))
    def blanc(mot, d): return next((j for (m, c, j) in BLANCHE_R1 if m == mot and c.lower() in d.lower()), None)
    hits = []; exemptes = []
    for n, d in tous + [('TEXTES_ENGAGEMENT.' + k, v) for k, v in T_ENG]:
        for mot, mo in liste:
            if re.search(L + '(?:' + mo + ')' + Rb, d, re.I):
                j = blanc(mot, d)
                (exemptes if j else hits).append('%s ← %s : « %s »%s' % (mot, n, d[:50], (' [liste blanche : %s]' % j) if j else ''))
    hits = sorted(set(hits))
    t('R1 · lexique : aucun mot interdit (%d écrans, %d textes, %d chaîne(s) du chantier)' % (len(vus), len(tous), len(T_ENG)), len(vus) >= 30 and not hits, ' | '.join(hits[:8]) + (' … (%d)' % len(hits) if len(hits) > 8 else ''))
    for x in sorted(set(exemptes)): print('     R1 · exempté : ' + x)
    t('R1 · `TEXTES_ENGAGEMENT` existe (un seul objet, règle 6)', existe, '%d chaîne(s)' % len(T_ENG))
    imp = sorted({'%s : « %s »' % (k, v[:60]) for k, v in T_ENG if IMP_TETE.search(v) or IMP_TRAIT.search(v)})
    t('R1 · A3 : aucun texte du chantier à l\'impératif (%d chaîne(s))' % len(T_ENG), not imp, ' | '.join(imp[:6]))
    # ── R2
    r2 = sorted({'%s : « %s »' % (k, v[:60]) for k, v in T_ENG if re.search(R2_MOTIF, v, re.I)})
    t('R2 · absence et temps : rien dans `TEXTES_ENGAGEMENT` (%d chaîne(s))' % len(T_ENG), not r2, ' | '.join(r2[:6]))
    # ── R3
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.getElementById('souffleBtn').click(); }"); pg.wait_for_timeout(3200)
    if SONDE: pg.evaluate("()=>{ const d=document.createElement('div'); d.textContent='12'; d.style.cssText='position:absolute;left:50%;top:50%;z-index:9'; document.getElementById('auBoule').parentElement.appendChild(d); }")
    r3 = pg.evaluate(r"""()=>{ const bo=document.getElementById('auBoule'); if(!bo) return null; const R=bo.getBoundingClientRect(), out=[], hors=[];
      const sc=document.getElementById('auraScreen'); const W=document.createTreeWalker(sc, NodeFilter.SHOW_TEXT); let n;
      while((n=W.nextNode())){ const s=n.nodeValue.replace(/\s+/g,' ').trim(); if(!/\d/.test(s)) continue; const e=n.parentElement, c=getComputedStyle(e), r=e.getBoundingClientRect();
        if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05||r.width<1) continue;
        const dedans=!(r.right<=R.left||r.left>=R.right||r.bottom<=R.top||r.top>=R.bottom); (dedans?out:hors).push(s.slice(0,24)); }
      return {dedans:out, hors:hors.slice(0,8), boite:[Math.round(R.width),Math.round(R.height)]}; }""")
    t('R3 · aucun chiffre sur la Pelote (dans son cadre)', bool(r3) and not r3['dedans'], 'dans le cadre : %s · cadre %s' % (r3 and r3['dedans'], r3 and r3['boite']))
    print('     R3 · à savoir : ailleurs sur l\'écran de l\'Aura, des textes portent un chiffre → %s' % (r3 and r3['hors']))
    # ── R4
    inactif('R4 · invariance du moment « tenir »', 'INACTIF AVANT E3')
    # ── R7
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); }"); pg.wait_for_timeout(900)
    toile = pg.evaluate(TEXTES)
    pg.evaluate("()=>{ try{ GesteFantome.oublierTout(); }catch(e){} openDetail(promises.find(q=>q.title==='faire les crêpes').id); }"); pg.wait_for_timeout(600)   # les drapeaux remis : la main reviendra sur cette fiche (A2)
    pg.wait_for_timeout(300)
    if SONDE: pg.evaluate("()=>{ document.getElementById('dptQuand').textContent='il y a 3 jours'; }")
    fiche = pg.evaluate(TEXTES)
    # ── A2 — ⚑ E1 : ARMÉ SUR LA MAIN FANTÔME. La fiche à tenir est ouverte (R7 vient de la lire) et personne ne touche : la main paraît après 600 ms.
    #   On la juge PENDANT qu'elle est à l'écran — elle, ses ancêtres, et chacun de ses tracés.
    for _i in range(12):
        if pg.evaluate("()=>!!document.getElementById('gesteFantome')"): break
        pg.wait_for_timeout(250)
    main_la = pg.evaluate("()=>{ const c=document.getElementById('gesteFantome'); return !!(c && c.getAttribute('data-eng') && c.querySelector('[data-main]')); }")
    if SONDE: pg.evaluate("()=>{ const d=document.createElement('div'); d.setAttribute('data-eng','sonde'); d.textContent='sonde'; d.style.cssText='position:absolute;left:20px;top:300px;opacity:.6;transition:opacity .3s'; document.getElementById('device').appendChild(d); }")
    a2 = pg.evaluate(r"""()=>{ const E=[...document.querySelectorAll('[data-eng]')], f=[];
      E.forEach(e=>{ const nom=e.getAttribute('data-eng')||e.tagName;
        for(let q=e;q&&q.nodeType===1&&q!==document.documentElement;q=q.parentElement){ if(+getComputedStyle(q).opacity<1){ f.push(nom+' : opacité '+getComputedStyle(q).opacity+(q===e?'':' (ancêtre)')); break; } }
        const c=getComputedStyle(e), tp=(c.transitionProperty||''), td=(c.transitionDuration||'0s').split(',').some(x=>parseFloat(x)>0);
        if(td && /opacity|all/.test(tp)) f.push(nom+' : fondu ('+tp+' '+c.transitionDuration+')');
        if(c.animationName && c.animationName!=='none') f.push(nom+' : animation '+c.animationName);
        const col=(c.color.match(/[\d.]+/g)||[]); if(col.length===4 && +col[3]<1) f.push(nom+' : texte à demi transparent '+c.color);
        [...e.querySelectorAll('*')].forEach(d=>{ const s=getComputedStyle(d); if(+s.opacity<1) f.push(nom+' : un tracé à opacité '+s.opacity); if((s.transitionDuration||'0s').split(',').some(x=>parseFloat(x)>0)) f.push(nom+' : un tracé en fondu'); if(s.animationName&&s.animationName!=='none') f.push(nom+' : un tracé animé en CSS');
          ['fill','stroke'].forEach(a=>{ const v=d.getAttribute(a); if(v&&/rgba\(|transparent/.test(v)) f.push(nom+' : '+a+' '+v); const o=d.getAttribute('opacity')||d.getAttribute(a+'-opacity'); if(o&&+o<1) f.push(nom+' : '+a+'-opacity '+o); }); }); });
      return {n:E.length, f:f}; }""")
    r7 = []
    for ou, ds in (('Toile', toile), ('fiche à tenir', fiche)):
        for d in ds:
            if re.match(HORIZONS, d.strip(), re.I): continue
            sans_horizon = re.sub(HORIZON_DANS, ' ', d)          # « À TENIR · DANS 2 JOURS » dit un horizon : on le retire, puis on juge ce qui reste
            if re.search(R7_MOTIF, sans_horizon, re.I): r7.append('%s : « %s »' % (ou, d[:50]))
    t('R7 · âge invisible (Toile : %d textes ; fiche à tenir : %d)' % (len(toile), len(fiche)), len(fiche) > 3 and not r7, ' | '.join(r7[:6]))
    # ── R5
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(600)
    avant = set(pg.evaluate("()=>Object.keys(localStorage)"))
    tenus = 0
    for titre in ('faire les crêpes', 'nager le mardi', 'courir dimanche'):
        pg.evaluate("(t)=>{ try{closeAll()}catch(e){} openDetail(promises.find(q=>q.title===t).id); }", titre); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ const b=document.querySelector('#segStatus button[data-st=tenu]'); if(b) b.click(); }")
        try: pg.wait_for_function("()=>!window._tenirAnime", timeout=9000)
        except Exception: pass
        pg.wait_for_timeout(1200)
        tenus += 1 if pg.evaluate("(t)=>promises.find(q=>q.title===t).status==='tenu'", titre) else 0
    if SONDE: pg.evaluate("()=>localStorage.setItem('promi_nb_tenus','3')")
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900)
    apres = set(pg.evaluate("()=>Object.keys(localStorage)"))
    neuves = sorted(apres - avant); hors = [k for k in neuves if not any(k == c or (c.endswith('_') and k.startswith(c)) for c, _ in BLANCHE_CLES)]
    t('R5 · rien ne se thésaurise : trois « tenir », aucune clé nouvelle hors liste blanche', tenus == 3 and not hors, 'tenus %d/3 · clés nouvelles : %s · hors liste : %s' % (tenus, neuves, hors))
    t('A2 · armé : la main fantôme est à l\'écran sur la fiche à tenir, elle porte `data-eng`', main_la or SONDE, 'main %s · %d élément(s) `data-eng`' % (main_la, a2['n']))
    t('A2 · aucune transparence ni fondu (%d élément(s) `data-eng`, tracés compris)' % a2['n'], a2['n'] > 0 and not a2['f'], ' | '.join(a2['f'][:6]))
    t('aucune erreur de page (écrans parcourus)', not er, er[:3])
    ctx.close()
    # ══ R6 : l'onboarding, stockage vierge, étape par étape ══
    # ⚑ E2 (v140, C-075) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_engagement-avant-v140.py). L'onboarding n'est plus « le prénom, la parole
    # et le trait, le message de fin » : c'est le prénom, le principe, la vraie page +, la fiche, la dernière ligne, le compte. Le parcours est
    # joué au vrai doigt par `redteam_e2.py --r6`, qui rend la sortie visible de chaque étape ; R6 garde sa règle : une sortie à CHAQUE étape.
    import subprocess
    r6 = subprocess.run([sys.executable, 'redteam_e2.py', '--r6'] + ([URL.rsplit('/', 1)[-1]] if not URL.endswith('/app.html') else []), capture_output=True, text=True, timeout=600)
    lignes = [l for l in r6.stdout.splitlines() if l.strip().startswith('R6')]
    t('R6 · sortie à un geste, à chaque étape de l\'onboarding (E2 : prénom, principe, page +, fiche, dernière ligne, compte)', r6.returncode == 0 and len(lignes) >= 7, (lignes[0] if lignes else r6.stdout[-200:]))
    for l in lignes[1:]: print('     ' + l.strip())
    b.close()
print('\nredteam_engagement : %d/%d au vert · %d inactif(s) : %s' % (ok[0], ok[0] + len(ko), len(inactifs), ' ; '.join(inactifs)))
if ko: print('ROUGE : ' + ' · '.join(ko)); sys.exit(1)
