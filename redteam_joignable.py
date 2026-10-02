#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_joignable.py — CE QUI SE TOUCHE EST JOIGNABLE, ET CE QU'UN GESTE APPELLE EXISTE (v118, Tom, 2 oct. 2026).

Né de deux défauts de v117b qu'aucun juge ne voyait, parce que tous ouvraient les portes par `.click()` :
  · le bouton photo d'une fiche, recouvert par `#dpMain` (z-index égal, venu après) — injoignable au doigt depuis sa naissance ;
  · le rond Partager, qui appelait `ouvrirPartage()` — une fonction qui n'existe nulle part.

A · AU RENDU — pour chaque élément interactif de chaque écran atteignable (la liste de `redteam_air`, plus le menu photo) :
    `document.elementFromPoint` AU CENTRE de l'élément doit rendre l'élément ou un de ses descendants.
    Est interactif : bouton, lien, champ, [role=button], ce qui porte un `on…` ou un écouteur de toucher/clic
    (les `addEventListener` sont piégés avant le chargement). Un élément hors du cadre est amené dans son conteneur qui défile.
B · À LA SOURCE — pour chaque gestionnaire (`x.onclick = function…`, `addEventListener('click', …)`) : chaque fonction qu'il
    appelle doit exister (déclarée dans la source, ou connue de la page chargée). Un appel gardé (`if(window.f) f()`) à une
    fonction qui n'existe nulle part est compté : c'est une branche morte, et ce qui suit le `else` est ce qui tourne vraiment.
    (Aucun gestionnaire en attribut `on…=""` ni par `data-*` dans l'app : vérifié, le juge le recompte et rougit s'il en naît.)

Le juge ROUGIT sur tout défaut qui n'est pas NOMMÉ dans `joignable-dette.json` (la dette de naissance : elle se solde, elle ne
grandit jamais). L'inventaire complet — élément, écran, joignable oui/non, cause — est écrit dans `joignable-inventaire.md`.
  --figer   écrit la dette depuis ce passage (à ne faire qu'après lecture de l'inventaire)
Preuve (§7) : copier `sauvegardes/app-avant-v117b.html` À LA RACINE, puis
`APP=http://127.0.0.1:8752/<copie>.html SRC=<copie>.html python3 redteam_joignable.py` doit ROUGIR
(bouton photo recouvert ; `ouvrirPartage` appelé à nu par le rond de la barre).
"""
import os, re, io, sys, json
from playwright.sync_api import sync_playwright
import importlib.util

ICI = os.path.dirname(os.path.abspath(__file__))
APP = os.environ.get('APP', 'http://127.0.0.1:8752/app.html')
SRC = os.path.join(ICI, os.environ.get('SRC', 'app.html'))
DETTE = os.path.join(ICI, 'joignable-dette.json')
INV = os.path.join(ICI, os.environ.get('INV', 'joignable-inventaire.md'))

_sp = importlib.util.spec_from_file_location('air', os.path.join(ICI, 'redteam_air.py'))
_air = importlib.util.module_from_spec(_sp)
_argv = sys.argv; sys.argv = ['x', '--liste']          # redteam_air ne s'exécute que sous __main__
try: _sp.loader.exec_module(_air)
finally: sys.argv = _argv
ECRANS = list(_air.ECRANS) + [
 ('menu photo',  "()=>{closeAll(); const p=promises.filter(q=>!q.draft&&!q.req&&!q.nuee&&!q.photo)[0]; openDetail(p.id); setTimeout(()=>{const b=document.querySelector('#detailPoster .ph-photo-btn'); if(b) b.click();},900);}"),
 ('Peaufiner gardé de côté', "()=>{closeAll(); const p=promises.filter(q=>q.draft)[0]; if(p){openDetail(p.id); setTimeout(()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x)x.click();},900);}}"),
]

# ── A · au rendu ──────────────────────────────────────────────────────────────────────────────────────────────────
PIEGE = r"""(()=>{ const A=EventTarget.prototype.addEventListener;
  const T={click:1,pointerup:1,pointerdown:1,touchend:1,touchstart:1,mousedown:1,mouseup:1,change:1,input:1};
  EventTarget.prototype.addEventListener=function(t,f,o){
    try{ if(T[t] && this && this.nodeType===1 && this!==document.body && this!==document.documentElement) this.__ec=(this.__ec||'')+t+' '; }catch(e){}
    return A.call(this,t,f,o); }; })();"""

MESURE = r"""()=>{
  const dv=document.getElementById('device').getBoundingClientRect(), sc=dv.width/390;
  const dans=(x,y)=>x>=dv.left&&x<=dv.right&&y>=dv.top&&y<=dv.bottom;
  const nom=e=>{ if(!e) return 'rien'; const c=(''+(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className)).split(' ').filter(Boolean).slice(0,2).join('.');
    return e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(c?'.'+c:''); };
  const chemin=e=>{ if(e.id) return '#'+e.id; let n=e, p=[]; for(let i=0;i<4&&n&&n.nodeType===1;i++,n=n.parentNode){ p.unshift(nom(n)); if(n.id) break; } return p.join('>'); };
  const DEV=document.getElementById('device'), FR=document.querySelector('.frame');
  const couche=e=>{ let n=e; while(n&&n.parentNode&&n.parentNode!==DEV&&n.parentNode!==FR&&n.parentNode.nodeType===1) n=n.parentNode; return n; };
  const visible=n=>{ for(;n&&n.nodeType===1;n=n.parentNode){ const c=getComputedStyle(n); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; } return true; };
  const flou=n=>{ for(;n&&n.nodeType===1;n=n.parentNode){ if(/blur/.test(getComputedStyle(n).filter)) return true; } return false; };
  const defile=e=>{ let s=e.parentNode; for(;s&&s.nodeType===1;s=s.parentNode){ const c=getComputedStyle(s);
        if((/(auto|scroll)/.test(c.overflowY)&&s.scrollHeight>s.clientHeight+2)||(/(auto|scroll)/.test(c.overflowX)&&s.scrollWidth>s.clientWidth+2)) return s; } return null; };
  const boite=e=>{ const c=getComputedStyle(e); if(c.display==='inline'){ const q=e.getClientRects(); if(q.length) return q[0]; } return e.getBoundingClientRect(); };
  const centre=(e,s)=>{ const r=boite(e), sr=s.getBoundingClientRect(); s.scrollTop+=(r.top+r.height/2)-(sr.top+sr.height/2); s.scrollLeft+=(r.left+r.width/2)-(sr.left+sr.width/2); };
  const NATIF='button,a[href],input,textarea,select,[role=button],[contenteditable=true]';
  const out=[], vus={};
  document.querySelectorAll('.frame *').forEach(e=>{
    const natif=e.matches(NATIF), par=natif?'natif':(e.onclick||e.onpointerup||e.onpointerdown||e.ontouchend||e.ontouchstart||e.onchange)?'on…':e.__ec?'écouteur':'';
    if(!par) return;
    if(e.type==='hidden' || (e.tagName==='INPUT'&&e.type==='file')) return;
    for(let n=e;n&&n.nodeType===1;n=n.parentNode){ const c=getComputedStyle(n); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return; }
    const cs=getComputedStyle(e);
    let r=boite(e), cx=r.left+r.width/2, cy=r.top+r.height/2, deplace=null;
    const amene=()=>{ /* on l'amène au milieu de son conteneur qui défile, si ce conteneur est lui-même à l'écran */
      const s=defile(e); if(!s) return false; const sr=s.getBoundingClientRect(); if(!dans(sr.left+sr.width/2, sr.top+sr.height/2)) return false;
      if(!deplace) deplace=[s,s.scrollTop,s.scrollLeft]; centre(e,s); r=boite(e); cx=r.left+r.width/2; cy=r.top+r.height/2; return true; };
    const rend=()=>{ if(deplace){ deplace[0].scrollTop=deplace[1]; deplace[0].scrollLeft=deplace[2]; } };
    if(!dans(cx,cy)){ if(!amene()||!dans(cx,cy)){ rend(); return; } }
    /* une rangée GLISSANTE qui se déclare (data-glisse, Q128) : ce qu'elle rogne n'est pas à l'écran, on le fait glisser pour l'atteindre */
    { const gl=e.closest('[data-glisse]'); if(gl){ const q=gl.getBoundingClientRect(); if(cx<q.left||cx>q.right||cy<q.top||cy>q.bottom){ rend(); return; } } }
    const txt=((e.getAttribute('aria-label')||e.textContent||e.placeholder||e.value||'')+'').replace(/\s+/g,' ').trim().slice(0,24);
    const cle=chemin(e)+(e.id?'':'«'+txt+'»');
    let ok=true, cause='';
    if(r.width<2||r.height<2){ ok=false; cause='taille nulle ('+Math.round(r.width/sc)+' × '+Math.round(r.height/sc)+')'; }
    else if(cs.pointerEvents==='none'){ ok=false; cause=flou(e)?'mur flouté (pointer-events:none)':'inerte (pointer-events:none)'; }
    else { let h=document.elementFromPoint(cx,cy);
      if(!(h&&(h===e||e.contains(h))) && amene()) h=document.elementFromPoint(cx,cy);      /* sous une barre collante : on le recentre */
      if(!(h&&(h===e||e.contains(h)))){
        /* ⚑ un AUTRE écran, ouvert et VISIBLE par-dessus : l'élément n'est pas sur cet écran-ci, il ne se juge pas ici.
           Un recouvrant de la MÊME couche (le défaut de v117b), ou une couche INVISIBLE, reste pris. */
        if(h && couche(h)!==couche(e) && visible(h)){ rend(); return; }
        ok=false;
        cause = !h ? 'rien sous le doigt' : h.contains(e) ? 'son contenant répond à sa place : '+nom(h) : 'recouvert par '+chemin(h)+' (z '+getComputedStyle(h).zIndex+(visible(h)?'':', INVISIBLE')+')'; } }
    rend();
    if(vus[cle]) return; vus[cle]=1;
    out.push({cle:cle, par:par, mot:txt, ok:ok, cause:cause, x:Math.round((cx-dv.left)/sc), y:Math.round((cy-dv.top)/sc), w:Math.round(r.width/sc), h:Math.round(r.height/sc)});
  });
  return out; }"""


def rendu():
    inv = []; ids = set()
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script(PIEGE)
        pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
        pg.goto(APP); pg.wait_for_timeout(6800)
        pg.evaluate('()=>{var o=document.getElementById("promiOnb");if(o){o.classList.add("gone");o.style.display="none";}}')
        pg.evaluate("()=>{try{setTheme('light')}catch(e){}}"); pg.wait_for_timeout(500)
        connus = pg.evaluate(r"""(noms)=>noms.filter(n=>{ try{ return (0,eval)('typeof '+n)!=='undefined'; }catch(e){ return false; } })""", sorted(APPELS_NOMS))
        for nom, js in ECRANS:
            if os.environ.get('ECRANS') and nom not in os.environ['ECRANS'].split('|'): continue
            pg.evaluate("()=>{ try{ closeAll(); }catch(_){ } document.querySelectorAll('.screen.show,#auraHelp.show,#plusScreen.show,#privScreen.show').forEach(s=>s.classList.remove('show')); }")
            pg.wait_for_timeout(250)
            pg.evaluate(_air.RAZ_EX)
            try: pg.evaluate(js)
            except Exception: pass
            pg.wait_for_timeout(2600)
            for e in pg.evaluate(MESURE): e['ecran'] = nom; inv.append(e)
            ids.update(pg.evaluate("()=>[...document.querySelectorAll('[id]')].map(e=>e.id)"))
        b.close()
    return inv, set(connus), er, ids


# ── B · à la source ───────────────────────────────────────────────────────────────────────────────────────────────
MOTS = set('if for while switch catch function return typeof new delete void in of do else try throw case var let const await async yield super this class extends import export default instanceof with'.split())
EVTS = 'click|pointerup|pointerdown|touchend|touchstart|mousedown|mouseup|change|input|keydown|keyup|submit|dblclick'


def scripts(S):
    js = [m.group(1) for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', S, re.S)]
    for m in re.finditer(r'<script[^>]*\bsrc="([^"]+)"', S):
        f = os.path.join(ICI, m.group(1))
        if os.path.exists(f): js.append(io.open(f, encoding='utf-8').read())
    return '\n;\n'.join(js)


def corps(J, i):
    """de l'accolade ouvrante en i jusqu'à sa fermante — chaînes, gabarits et commentaires sautés."""
    n, k, L = 0, i, len(J)
    while k < L:
        c = J[k]
        if c in '"\'`':
            q = c; k += 1
            while k < L and J[k] != q:
                if J[k] == '\\': k += 1
                k += 1
        elif c == '/' and J[k+1:k+2] == '/':
            k = J.find('\n', k);  k = L if k < 0 else k
        elif c == '/' and J[k+1:k+2] == '*':
            k = J.find('*/', k) + 1;  k = L if k <= 0 else k
        elif c == '{': n += 1
        elif c == '}':
            n -= 1
            if n == 0: return J[i:k+1]
        k += 1
    return J[i:]


def sans_texte(b):
    b = re.sub(r'/\*.*?\*/', ' ', b, flags=re.S)
    b = re.sub(r'(?<![:\\])//[^\n]*', ' ', b)
    return re.sub(r'"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|`(?:\\.|[^`\\])*`', '""', b)


def gestionnaires(J):
    """(porteur, évènement, corps, position) pour chaque gestionnaire écrit en fonction littérale ; et les références nues."""
    out = []
    pats = [r'([\w$.\[\]\'"()#-]{1,60})\.on(' + EVTS + r')\s*=\s*(?:function\s*[\w$]*\s*\([^)]*\)|\([^)]*\)\s*=>|[\w$]+\s*=>)\s*\{',
            r'([\w$.\[\]\'"()#-]{0,60})\.addEventListener\(\s*[\'"](' + EVTS + r')[\'"]\s*,\s*(?:function\s*[\w$]*\s*\([^)]*\)|\([^)]*\)\s*=>|[\w$]+\s*=>)\s*\{']
    for p in pats:
        for m in re.finditer(p, J):
            out.append((m.group(1), m.group(2), corps(J, m.end()-1), m.start()))
    refs = []
    for m in re.finditer(r'\.addEventListener\(\s*[\'"](' + EVTS + r')[\'"]\s*,\s*([A-Za-z_$][\w$]*)\s*[,)]', J): refs.append((m.group(2), m.start()))
    for m in re.finditer(r'\.on(' + EVTS + r')\s*=\s*([A-Za-z_$][\w$]*)\s*;', J): refs.append((m.group(2), m.start()))
    return out, refs


def appels(b):
    b = sans_texte(b)
    nus = set(n for n in re.findall(r'(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(', b) if n not in MOTS)
    nus -= set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', b))
    win = set(re.findall(r'\bwindow\.([A-Za-z_$][\w$]*)\s*\(', b))
    return nus, win


def declare(J, n):
    global JN
    if JN is None: JN = sans_texte(J)
    J = JN
    e = re.escape(n)
    return bool(re.search(r'function\s+' + e + r'\s*\(|(?:var|let|const)\s+(?:[\w$]+\s*(?:=[^,;]*)?,\s*)*' + e + r'\b|(?<![.\w$])' + e + r'\s*=(?!=)|window\.' + e + r'\s*=(?!=)|[(,]\s*' + e + r'\s*(?=[,)])[^;{]{0,80}\)\s*(?:=>|\{)|catch\s*\(\s*' + e + r'\s*\)', J))


S = io.open(SRC, encoding='utf-8').read()
J = scripts(S)
JN = None
GEST, REFS = gestionnaires(J)
APPELS = []                    # (porteur, évènement, nom, forme, contourné)
for porteur, ev, b, pos in GEST:
    nus, win = appels(b)
    for n in sorted(nus | win):
        avant = sans_texte(b)[:max(0, sans_texte(b).find(n + '('))] if (n + '(') in sans_texte(b) else ''
        APPELS.append((porteur.strip()[-40:], ev, n, 'window.' if (n in win and n not in nus) else '', bool(re.search(r'\breturn\b', avant)), pos))
for n, pos in REFS: APPELS.append(('(référence)', '', n, 'réf', False, pos))
APPELS_NOMS = set(a[2] for a in APPELS)
ATTR = len(re.findall(r'<[a-zA-Z][^<>]*\son(?:' + EVTS + r')\s*=', S))


def porteur_lisible(porteur, pos):
    """le nom de variable ne dit rien (`bp2`) : on remonte à l'id qu'elle désigne, dans les 400 caractères d'avant."""
    v = re.sub(r'[^\w$].*$', '', porteur) if re.match(r'[\w$]+$', porteur.split('.')[-1] or '') else porteur
    v = porteur.split('.')[-1]
    m = None
    for m in re.finditer(re.escape(v) + r'\s*=\s*(?:document\.getElementById\(\s*[\'"]([\w-]+)[\'"]|[\w$.]*querySelector\(\s*[\'"]([^\'"]+)[\'"])', J[max(0, pos-900):pos]): pass
    if m: return '#' + m.group(1) if m.group(1) else m.group(2)
    m = re.search(r'getElementById\(\s*[\'"]([\w-]+)[\'"]\s*\)$', porteur) or re.search(r'querySelector\(\s*[\'"]([^\'"]+)[\'"]\s*\)$', porteur)
    return ('#' + m.group(1)) if (m and m.re.pattern.startswith('getElementById')) else (m.group(1) if m else porteur)


def main():
    ok = [0]; ko = []
    def t(nom, cond, detail=''):
        if cond: ok[0] += 1; print('%-58s OK  %s' % (nom, detail))
        else: ko.append(nom); print('%-58s KO  %s' % (nom, detail))

    inv, connus, er, ids = rendu()
    dette = json.load(io.open(DETTE, encoding='utf-8')) if os.path.exists(DETTE) else {'rendu': {}, 'source': {}}

    # B
    manquantes = {}
    for porteur, ev, n, forme, contourne, pos in APPELS:
        if n in connus or declare(J, n): continue
        cle = '%s · on%s → %s()%s' % (porteur_lisible(porteur, pos), ev, n, ' [après un return]' if contourne else '')
        manquantes[cle] = 'la fonction `%s` n\'existe nulle part' % n
    # B bis · un gestionnaire posé sur un nœud qui n'existe plus : du code mort (Q363)
    orphelins = {}
    for porteur, ev, b, pos in GEST:
        pl = porteur_lisible(porteur, pos)
        if not re.match(r'#[\w-]+$', pl): continue
        i = pl[1:]
        if i in ids or re.search(r'''\bid\s*[=:]\s*\\?["']''' + re.escape(i) + r'''\\?["']''', S): continue
        orphelins['%s · on%s' % (pl, ev)] = 'le nœud `%s` n\'existe plus : aucun `id` de ce nom, ni à la source ni au rendu' % pl
    manquantes.update(orphelins)
    # A
    injoignables = {}
    for e in inv:
        if not e['ok']: injoignables.setdefault(e['cle'], {'cause': e['cause'], 'ecrans': []})['ecrans'].append(e['ecran'])

    print('\n── A · au rendu : %d éléments interactifs relevés sur %d écrans, %d injoignables (distincts)' % (len(inv), len(set(e['ecran'] for e in inv)), len(injoignables)))
    neufs_a = sorted(k for k in injoignables if k not in dette.get('rendu', {}))
    for k in neufs_a: print('   NEUF  %-60s %s   [%s]' % (k[:60], injoignables[k]['cause'], ', '.join(sorted(set(injoignables[k]['ecrans']))[:3])))
    print('── B · à la source : %d gestionnaires, %d appels, %d défauts (fonction absente ou nœud disparu)' % (len(GEST), len(APPELS), len(manquantes)))
    neufs_b = sorted(k for k in manquantes if k not in dette.get('source', {}))
    for k in neufs_b: print('   NEUF  %s' % k)
    print()
    t('la page se charge sans erreur', not er, '; '.join(er[:2]))
    t('des éléments ont été relevés sur chaque écran', len(set(e['ecran'] for e in inv)) >= len(ECRANS) - 1 or bool(os.environ.get('ECRANS')), '%d écrans' % len(set(e['ecran'] for e in inv)))
    t('aucun élément interactif injoignable hors dette', not neufs_a, '%d neufs, %d en dette' % (len(neufs_a), len(injoignables) - len(neufs_a)))
    t('aucun gestionnaire n\'appelle une fonction absente hors dette', not neufs_b, '%d neufs, %d en dette' % (len(neufs_b), len(manquantes) - len(neufs_b)))
    t('aucun gestionnaire en attribut on…=""', ATTR == 0, '%d' % ATTR)
    soldes = [k for k in dette.get('rendu', {}) if k not in injoignables] + [k for k in dette.get('source', {}) if k not in manquantes]
    if soldes and not os.environ.get('ECRANS'): print('   (dette soldée, à retirer de joignable-dette.json : %s)' % '; '.join(soldes[:8]))

    # l'inventaire
    L = ['# Inventaire de joignabilité — engendré par `redteam_joignable.py`', '',
         'Source : `%s`. %d éléments interactifs relevés sur %d écrans (mode clair, 390 × 844), %d injoignables distincts ; %d gestionnaires lus, %d fonctions absentes.' % (os.path.basename(SRC), len(inv), len(set(e['ecran'] for e in inv)), len(injoignables), len(GEST), len(manquantes)), '',
         '## A · Injoignables au rendu', '', '| Élément | Écrans | Cause | Dette |', '|---|---|---|---|']
    for k in sorted(injoignables): L.append('| `%s` | %s | %s | %s |' % (k.replace('|', '/'), ', '.join(sorted(set(injoignables[k]['ecrans']))), injoignables[k]['cause'].replace('|', '/'), dette.get('rendu', {}).get(k, 'NEUF')))
    L += ['', '## B · Fonctions absentes appelées par un gestionnaire, et gestionnaires posés sur un nœud disparu', '', '| Gestionnaire | Cause | Dette |', '|---|---|---|']
    for k in sorted(manquantes): L.append('| `%s` | %s | %s |' % (k, manquantes[k], dette.get('source', {}).get(k, 'NEUF')))
    L += ['', '## C · Tous les éléments relevés', '', '| Écran | Élément | Par | x, y | l × h | Joignable | Cause |', '|---|---|---|---|---|---|---|']
    for e in sorted(inv, key=lambda e: (e['ecran'], e['y'], e['x'])):
        L.append('| %s | `%s` | %s | %d, %d | %d × %d | %s | %s |' % (e['ecran'], e['cle'].replace('|', '/'), e['par'], e['x'], e['y'], e['w'], e['h'], 'oui' if e['ok'] else 'NON', e['cause'].replace('|', '/')))
    if not os.environ.get('ECRANS'): io.open(INV, 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    if '--figer' in sys.argv:
        d = {'rendu': {k: dette.get('rendu', {}).get(k, 'à classer') for k in sorted(injoignables)},
             'source': {k: dette.get('source', {}).get(k, 'à classer') for k in sorted(manquantes)}}
        io.open(DETTE, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n'); print('dette figée : %d + %d' % (len(d['rendu']), len(d['source'])))
    print('\n%d / %d' % (ok[0], ok[0] + len(ko)))
    sys.exit(1 if ko else 0)


if __name__ == '__main__':
    main()
