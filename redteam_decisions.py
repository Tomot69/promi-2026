#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_decisions.py — CHAQUE DÉCISION DE COULEUR DE TOM, CONFRONTÉE À L'ÉCRAN RENDU (v122, Tom, 3 oct. 2026).

« Un second contrôle compare chaque décision du tableau b à l'écran rendu. » Les décisions sont écrites EN DUR ci-dessous (§7), chacune
avec sa source ; le juge ouvre les fiches Promi (à tenir, en cours, tenue), Chiche (lancé, tenu à deux), Cercle, la page + et l'Index,
dans les deux thèmes, et lit les couleurs RENDUES (styles calculés, pixels du canevas pour le champ et l'anneau).
Là où une zone n'a AUCUNE décision de Tom, elle n'est pas jugée ici : c'est `redteam_couleurs_ref.py` qui la tient à sa valeur de v118.
Preuve (§7) : sur `sauvegardes/app-avant-v122.html`, « trace pour tenir » d'une fiche à tenir sombre est #F3E7D1 au lieu de la crème
#F7F0DE (Q290) → il ROUGIT.
"""
import os, sys, re, math
from playwright.sync_api import sync_playwright

FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
ok = [0]; ko = []
ETATS = {'atenir': '#DD4D23', 'encours': '#291547', 'tenu': '#00341A'}      # Q262 (22 sept.) : « une fois pour toutes »
CREME, ENCRE, SEICHE, TERRE, AMANDE = '#F7F0DE', '#201908', '#050302', '#2B1020', '#8FE08F'
CHAMP = {'promi': '#82AEF8', 'chiche': '#FFB8D2', 'nuee': '#C9A8F5'}           # 17 sept. (planche des correspondances)
CORPS_SOMBRE = {'promi': '#273CEB', 'chiche': '#7C3F58', 'nuee': '#5D4978'}     # v113 (Q358) ; ⚠ le Cercle : ajout de v113, pas une citation de Tom
# ⚑ v130 (Tom, 5 oct. 2026) : le corps sombre d'un Promi #335382 est REMPLACÉ par le Pantone 13-4307 TPG « Tropical Breeze », #8ACBE8
#   (relevé par Tom sur son échantillon) — fiche Promi et page + d'un Promi ; le texte posé dessus passe à l'encre #201908.
# ⚑ v131 (Tom, 5 oct. 2026) : « Tropical Breeze est écarté (trop proche du bleu du champ) » — le corps sombre d'un Promi devient le
#   COBALT ÉLECTRIQUE #273CEB (fiche Promi et page + d'un Promi) ; « le texte posé sur ce corps redevient crème #F7F0DE, comme avant ».
SRC_TROPICAL = 'v131 (Tom, 5 oct. 2026) : cobalt électrique #273CEB ; remplace Tropical Breeze #8ACBE8 (v130, écarté) et #335382 (v113, Q358)'

# (écran, thème, zone, valeur décidée, source)
D = []
for th in ('light', 'dark'):
    for nom, nat in (('Promi à tenir', 'promi'), ('Promi en cours', 'promi'), ('Promi tenue', 'promi'), ('Chiche lancé', 'chiche'), ('Chiche tenu à deux', 'chiche'), ('Cercle', 'nuee')):
        D.append((nom, th, 'champ', CHAMP[nat], '17 sept., planche des correspondances ; Q101 (29 août) : jamais blanc'))
        D.append((nom, th, 'plateau', SEICHE if th == 'dark' else CREME, 'v116 + v121 (seiche dans les pages) · 16 sept. (fond clair)'))
        D.append((nom, th, 'motMarque', CREME if th == 'dark' else ENCRE, '17 sept. : le texte du plateau à l\'encre en clair'))
    for nom in ('Promi tenue', 'Chiche tenu à deux'):
        D.append((nom, th, 'corps', TERRE, 'v8 (21 sept.) : la terre, dans les deux thèmes'))
        D.append((nom, th, 'echeance', AMANDE, 'Q269 (23 sept.) · Q299 : « TENUE » en amande'))
        D.append((nom, th, 'titre', CREME, 'v8 (21 sept.) : sur la terre, le texte passe crème'))
    if th == 'dark':
        for nom, nat in (('Promi à tenir', 'promi'), ('Promi en cours', 'promi'), ('Chiche lancé', 'chiche'), ('Cercle', 'nuee')):
            D.append((nom, th, 'corps', CORPS_SOMBRE[nat], SRC_TROPICAL if nat == 'promi' else 'v113 (30 sept., Q358) : « option 2 »'))
        for z in ('aQui', 'echeance', 'trace'):
            D.append(('Chiche lancé', th, z, CREME, 'v16 (Q290) : les textes d\'état sur fond sombre passent crème'))
        for nom in ('Promi à tenir', 'Promi en cours'):
            for z in ('titre', 'aQui', 'echeance', 'trace'):
                D.append((nom, th, z, CREME, 'v131 (Tom, 5 oct. 2026) : « le texte posé sur ce corps redevient crème #F7F0DE, comme avant Tropical : titre, à-qui, échéance, mentions »'))
    else:
        for z in ('aQui', 'echeance', 'trace'):
            D.append(('Promi à tenir', th, z, ETATS['atenir'], 'Q262 (22 sept.) : l\'état, partout où il paraît'))
            D.append(('Promi en cours', th, z, ETATS['encours'], 'Q262 (22 sept.)'))
            D.append(('Chiche lancé', th, z, ETATS['encours'], 'v29 (Q310) : « LANCÉ » suit la règle des états'))
    D.append(('page +', th, 'champ', CHAMP['promi'], 'Q101 (29 août) : la couleur de la nature'))
    if th == 'dark': D.append(('page +', th, 'corps', CORPS_SOMBRE['promi'], SRC_TROPICAL))
    D.append(('Index', th, 'fond', SEICHE if th == 'dark' else None, 'v116 + v121 : la seiche dans les pages'))
    if th == 'light': D.append(('Index', th, 'carte_libelle', '#022140', 'Q221 (17 sept.) : le compagnon sombre, mode clair'))
    D.append(('Index', th, 'carte_etat', CREME if th == 'dark' else None, 'v16 (Q290) : état sur fond sombre en crème'))
    D.append(('Index', th, 'cartes_etats', CREME if th == 'dark' else None, 'v16 (Q290) : les libellés des cartes À TENIR, EN COURS, LANCÉ, sur le corps sombre, en crème — « à tenir » compris'))
D = [d for d in D if d[3]]

S = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scratchpad', 'v122', 'zones.py'), encoding='utf-8').read()
Z = re.search(r'Z=r"""(.*?)"""', S, re.S).group(1)
FICHES = [('Promi à tenir', 'faire les crêpes'), ('Promi en cours', 'nager le mardi'), ('Promi tenue', 'planter un arbre'), ('Chiche tenu à deux', 'le grand plongeoir'), ('Chiche lancé', 'courir dimanche')]


def hexa(v):
    if not v or 'rgb' not in v: return v
    n = [int(x) for x in re.findall(r'\d+', v)[:3]]; return '#%02X%02X%02X' % tuple(n)


def pose(pg):
    # l'état POSÉ : deux relevés identiques à 700 ms d'écart (la première image d'une fiche montre encore la couleur de la fiche
    # d'avant — mesuré : « EN COURS » vert #00341A de 0 à ~200 ms sur un Chiche lancé ouvert après un Chiche tenu, en v118 aussi)
    a = None
    for _ in range(6):
        b_ = {k: hexa(v) for k, v in pg.evaluate(Z).items()}
        if b_ == a: return b_
        a = b_; pg.wait_for_timeout(700)
    return a


R = {}
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    pg.goto('http://127.0.0.1:8752/' + FICHIER); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    for th in ('light', 'dark'):
        pg.evaluate("(t)=>{try{closeAll()}catch(e){} setTheme(t)}", th); pg.wait_for_timeout(600)
        for nom, ti in FICHES:
            pg.evaluate("(t)=>{closeAll(); const p=promises.filter(q=>q.title===t)[0]; openDetail(p.id);}", ti); pg.wait_for_timeout(2600)
            R[(nom, th)] = pose(pg)
        pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(2800)
        R[('Cercle', th)] = pose(pg)
        pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3500)
        R[('page +', th)] = {k: hexa(v) for k, v in pg.evaluate("()=>{const s=document.getElementById('createSheet'); const cv=document.getElementById('csTrameCv'); let ch=null; try{const d=cv.getContext('2d').getImageData(6,6,1,1).data; ch='rgb('+d[0]+', '+d[1]+', '+d[2]+')';}catch(e){} return {corps:getComputedStyle(s).backgroundColor, champ:ch};}").items()}
        pg.evaluate("()=>{closeAll(); setView('toile'); ouvrirIndex(); window._s4Trois=false; if(window._s4Index)_s4Index();}"); pg.wait_for_timeout(3000)
        R[('Index', th)] = {k: hexa(v) for k, v in pg.evaluate("()=>{const s=document.getElementById('indexSheet'); const c=document.querySelector('#indexList .s4-carte'); const et=c&&c.querySelector('.s4-et'); const nl=c&&c.querySelector('.s4-natlab'); const H=v=>{const n=(v.match(/\\d+/g)||[]).slice(0,3).map(x=>(+x).toString(16).padStart(2,'0')).join('').toUpperCase(); return '#'+n;}; const toutes=[...new Set([...document.querySelectorAll('#indexList .s4-carte')].filter(c=>{const t=c.querySelector('.s4-et'); return t&&/^(À TENIR|EN COURS|LANCÉ)/.test(t.textContent.trim());}).flatMap(c=>[...c.querySelectorAll('.s4-et,.s4-eb')]).map(e=>H(getComputedStyle(e).color)))].join(' ');   /* les cartes À TENIR, EN COURS, LANCÉ — les états ; une Nuée, un gardé de côté portent leur nature, une tenue l'amande ou la crème panneau */ return {fond:getComputedStyle(s).backgroundColor, carte_etat:et?getComputedStyle(et).color:null, carte_libelle:nl?getComputedStyle(nl).color:null, cartes_etats:toutes};}").items()}
        # l'anneau : ses arcs ne portent que les trois états (Q262, v8c « trois arcs ») — les couleurs franches, à ΔE près
        a = (R[('Promi à tenir', th)].get('anneau') or '').split()
        R[('Promi à tenir', th)]['anneau_ok'] = all(min(sum((int(x[i:i + 2], 16) - int(e[i:i + 2], 16)) ** 2 for i in (1, 3, 5)) ** .5 for e in list(ETATS.values()) + ['#2A1548', '#00351A']) < 12 for x in a) and bool(a)
    b.close()

for ecran, th, zone, val, src in D:
    vu = (R.get((ecran, th)) or {}).get(zone)
    if ko is not None:
        cond = vu == val
        if cond: ok[0] += 1
        else: ko.append('%s [%s] %s' % (ecran, th, zone))
        print('%-20s %-5s %-14s décidé %-8s rendu %-8s %s   (%s)' % (ecran, th, zone, val, vu, 'OK' if cond else 'KO', src))
for th in ('light', 'dark'):
    c = R[('Promi à tenir', th)].get('anneau_ok')
    if c: ok[0] += 1
    else: ko.append('anneau [%s]' % th)
    print('%-20s %-5s %-14s décidé 3 états  rendu %-24s %s   (Q262, v8c)' % ('Promi à tenir', th, 'anneau', R[('Promi à tenir', th)].get('anneau'), 'OK' if c else 'KO'))
print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko))
sys.exit(1 if ko else 0)
