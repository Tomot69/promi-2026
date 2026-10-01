#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_gens.py — LE CHOIX DES PERSONNES (lot-GENS, 13 sept. 2026), AU DOIGT.

Quatre contrats, joués au VRAI DOIGT (CDP `Input.dispatchTouchEvent`, contexte tactile) — pas à la souris :
le 13 septembre, la tuile « Un Chiche » ouvrait un Promi au doigt et un Chiche à la souris, et aucune batterie
ne le voyait (AUDIT-ACCUEIL § 2).

  1 · TOUCHER UNE PERSONNE L'AJOUTE      — la donnée la contient, sa pastille passe « prise » et porte une croix
  2 · LA CROIX LA RETIRE                 — la donnée ne la contient plus, la pastille n'est plus prise
  3 · « + AJOUTER QUELQU'UN » RESTE VISIBLE — même quand la liste déborde : au doigt, à son centre, c'est LUI
                                           qu'on touche, en haut ET en bas de la liste ; et il ouvre le menu d'ajout
  4 · LA LISTE VIT AU-DESSUS DE PEAUFINER — page + : aucune pastille sous 744 (barre 760 − 16), rien de la liste
                                           au doigt sur la barre, aucune pastille coupée au repos

Contextes : page + — Promi « à qui » (verbe basculé), Chiche « qui tu défies » et « avec qui », Nuée « avec » ;
fiche d'un Promi — Peaufiner, « À QUI » (contrats 1 à 3 : la liste y défile dans sa carte, la borne 744 est celle
de la page +). Deux thèmes.

LES CONTRATS SE PROUVENT (§7) : `--sondes` pose quatre défauts fabriqués dans l'app courante, un par contrat,
et exige que CHACUN soit pris. `APP_GENS=http://…/sauvegardes/app-avant-lot-saisie-personnes.html` passe le
juge sur la VRAIE version fautive.

Usage :  python3 redteam_gens.py [--sondes] [--verbose]
"""
import os, sys
from playwright.sync_api import sync_playwright

APP = os.environ.get('APP_GENS', "http://127.0.0.1:8752/app.html")
VERBOSE = '--verbose' in sys.argv
BORNE = 744          # barre de Peaufiner à 760 − 16 d'air — décision du lot-GENS, EN DUR (§7)
ok = [0]; ko = []


def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-64s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-64s KO  %s' % (nom, detail))


GN = "#createSheet .gn, #dpdCorps .gn"

# ── lecture : le choix ouvert ────────────────────────────────────────────────────────────
ETAT = r"""(sel)=>{
  const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  const cfg=g._gens; let pris=null; try{ pris=cfg?cfg.choisis():null; }catch(e){}
  const libres=[...g.querySelectorAll(':scope > .ph-o[data-v]:not(.on)')].map(b=>b.getAttribute('data-v'));
  const prises=[...g.querySelectorAll(':scope > .ph-o[data-v].on')].map(b=>({n:b.getAttribute('data-v'),x:!!b.querySelector('.ppo-x')}));
  const r=g.getBoundingClientRect();
  return {pris, libres, prises, haut:(r.top-D.top)/k, bas:(r.bottom-D.top)/k, add:!!g.querySelector('.ph-add'),
          defile:g.scrollHeight>g.clientHeight+2};}"""

CENTRE = r"""(a)=>{ const [sel,q]=a;
  const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
  const e=g.querySelector(q); if(!e) return null;
  const r=e.getBoundingClientRect(); return {x:r.left+r.width/2, y:r.top+r.height/2, w:r.width, h:r.height};}"""


def doigt(cdp, pt):
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pt['x'], 'y': pt['y']}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})


# ── les sondes : un défaut fabriqué par contrat. Posées et mesurées dans la même page (§8). ─────
SONDES = {
    'ajout': r"""()=>{document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('.gn .ph-o[data-v]:not(.on)');
               if(b&&!e.target.closest('.ppo-x')){e.stopPropagation();e.preventDefault();}},true);}""",
    'croix': r"""()=>{document.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('.gn .ppo-x')){e.stopPropagation();e.preventDefault();}},true);}""",
    'ajouter': r"""()=>{const o=window._gensBorne; window._gensBorne=function(){const r=o.apply(this,arguments);
               document.querySelectorAll('.gn > .ph-add').forEach(a=>a.style.setProperty('position','static','important'));return r;};}""",
    'peaufiner': r"""()=>{const o=window._gensBorne; window._gensBorne=function(){const r=o.apply(this,arguments);
               document.querySelectorAll('#createSheet .gn').forEach(g=>{g.style.setProperty('max-height','none','important');g.style.setProperty('overflow-y','visible','important');});return r;};}""",
}
VISE = {'ajout': 'ajoute', 'croix': 'retire', 'ajouter': '« + ajouter » visible', 'peaufiner': 'au-dessus de Peaufiner'}


def ouvre_page(pg, tuile, cle):
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
    # la tuile se choisit ici à la SOURIS : ce contrôle ne juge pas l'écran des choix (défaut noté à part, AUDIT-ACCUEIL)
    pg.evaluate("(i)=>{const t=[...document.querySelectorAll('#createSheet .tile')][i]; if(t) t.click();}", tuile)
    pg.wait_for_timeout(1200)
    if cle == 'bascule-qui':
        pg.evaluate("()=>{const e=document.querySelector('#csPhrase [data-ph=sens]'); if(e) e.click();}"); pg.wait_for_timeout(900)
        cle = 'qui'
    sel = '#csPhrase [data-ph=%s]' % cle if cle in ('qui', 'avec') else '#nueePhrase [data-np=avec]'
    pg.evaluate("(s)=>{const e=document.querySelector(s); if(e) e.click();}", sel); pg.wait_for_timeout(1000)


def ouvre_fiche(pg, pid, lab):
    pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)
    pg.evaluate("(i)=>openDetail(i)", pid); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const t=document.getElementById('dpdTog'); if(t) t.click();}"); pg.wait_for_timeout(1000)
    pg.evaluate("""(l)=>{const r=[...document.querySelectorAll('#dpdCorps .s2-reg')].find(r=>((r.querySelector('.s2-lab')||{}).textContent||'').trim()===l);
                   if(r && !r.classList.contains('s2-ouv')) r.click();}""", lab)
    pg.wait_for_timeout(1000)


def remplis(pg, n=9):
    """fait déborder la liste : n personnes prises, par la donnée du choix (c'est le rendu qu'on juge, pas l'ajout)"""
    pg.evaluate("""(a)=>{const [sel,n]=a; const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10);
        if(!g||!g._gens) return; const c=g._gens;
        ['Anouk','Basile','Céleste','Dimitri','Elsa','Farid','Gaspard','Hortense','Ilyes','Jeanne'].slice(0,n).forEach(x=>{try{c.ajoute(x);}catch(e){}});
        try{ if(c.rendu) c.rendu(); else window._gens(g,c); }catch(e){} }""", [GN, n])
    pg.wait_for_timeout(1400)


def contrats(pg, cdp, nom, ouvrir, page_plus, seuls=None):
    """seuls : le sous-ensemble de contrats à jouer (une sonde ne vise que le sien)"""
    pris = {}
    def veut(c): return seuls is None or c in seuls
    # 1 · ajout
    if veut('ajout') or veut('croix'):
        ouvrir()
        e = pg.evaluate(ETAT, GN)
        if not e:
            t('%s · le choix des personnes s\'ouvre' % nom, False, 'aucune liste .gn ouverte'); return pris
        if not e['libres']:
            pg.evaluate("""(sel)=>{const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10);
               if(g&&g._gens){const c=g._gens;(c.choisis()||[]).forEach(n=>{try{c.retire(n)}catch(_){} }); try{c.rendu?c.rendu():window._gens(g,c)}catch(_){}}}""", GN)
            pg.wait_for_timeout(1000); e = pg.evaluate(ETAT, GN)
        n = e['libres'][0] if e and e['libres'] else None
        if n is None:
            t('%s · une personne à toucher' % nom, False, 'aucune pastille libre'); return pris
        pt = pg.evaluate(CENTRE, [GN, '.ph-o[data-v="%s"]' % n])
        doigt(cdp, pt); pg.wait_for_timeout(1100)
        e2 = pg.evaluate(ETAT, GN) or {}
        dans = n in (e2.get('pris') or [])
        porte = any(p['n'] == n and p['x'] for p in e2.get('prises', []))
        if veut('ajout'):
            pris['ajout'] = not (dans and porte)
            t('%s · toucher « %s » l\'ajoute' % (nom, n), dans and porte, 'donnée %s · pastille prise avec croix %s' % (dans, porte))
        # 2 · croix
        if veut('croix'):
            px = pg.evaluate(CENTRE, [GN, '.ph-o[data-v="%s"] .ppo-x' % n])
            if not px:
                pris['croix'] = True
                t('%s · la croix de « %s » la retire' % (nom, n), False, 'pas de croix à toucher')
            else:
                doigt(cdp, px); pg.wait_for_timeout(1100)
                e3 = pg.evaluate(ETAT, GN) or {}
                parti = n not in (e3.get('pris') or []) and not any(p['n'] == n for p in e3.get('prises', []))
                pris['croix'] = not parti
                t('%s · la croix de « %s » la retire' % (nom, n), parti, 'donnée %s' % e3.get('pris'))
    # 3 · « + ajouter » visible, liste qui déborde
    if veut('ajouter') or (page_plus and veut('peaufiner')):
        ouvrir(); remplis(pg)
        e = pg.evaluate(ETAT, GN) or {}
        if veut('ajouter'):
            vus = []
            for bout in ('haut', 'bas'):
                pg.evaluate("""(a)=>{const [sel,b]=a;const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10);
                    if(g) g.scrollTop = b==='haut' ? 0 : g.scrollHeight;
                    const s=g&&g.closest('#dpdCorps'); if(s){ const a2=g.querySelector('.ph-add'); if(a2) a2.scrollIntoView({block:'nearest'}); } }""", [GN, bout])
                pg.wait_for_timeout(400)
                vu = pg.evaluate("""(sel)=>{const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10); if(!g) return 'pas de liste';
                    const a=g.querySelector(':scope > .ph-add'); if(!a) return 'absent';
                    const r=a.getBoundingClientRect(); const x=r.left+r.width/2, y=r.top+r.height/2;
                    if(y<0||y>innerHeight) return 'hors fenêtre';
                    const h=document.elementFromPoint(x,y); return (h&&(h===a||a.contains(h)))?'ok':('recouvert par '+(h?(h.id||h.className||h.tagName):'rien'));}""", GN)
                vus.append('%s:%s' % (bout, vu))
            bon = all(v.endswith(':ok') for v in vus) if page_plus else any(v.endswith(':ok') for v in vus)
            ouvre = False
            if bon:
                pa = pg.evaluate(CENTRE, [GN, ':scope > .ph-add'])
                if pa: doigt(cdp, pa); pg.wait_for_timeout(700)
                ouvre = pg.evaluate("(sel)=>!!document.querySelector('.gn > .gn-barre input')", GN)
            pris['ajouter'] = not (bon and ouvre)
            t('%s · « + ajouter quelqu\'un » visible et vivant (déborde : %s)' % (nom, e.get('defile')), bon and ouvre,
              '%s · menu d\'ajout %s' % (' '.join(vus), ouvre))
        # 4 · au-dessus de Peaufiner (page + seulement)
        if page_plus and veut('peaufiner'):
            ouvrir(); remplis(pg)
            m = pg.evaluate("""(a)=>{const [sel,B]=a; const g=[...document.querySelectorAll(sel)].find(e=>e.getBoundingClientRect().height>10); if(!g) return null;
                const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
                g.scrollTop=0; const gr=g.getBoundingClientRect();
                /* ⚠ LE BOUTON COLLÉ RECOUVRE ce qui passe dessous (fond du corps + 8 d'ombre de la même couleur) : une rangée
                   derrière lui n'est pas « vue ». Le premier passage comptait ces rangées coupées — l'image montrait l'inverse. */
                const ad=g.querySelector(':scope > .ph-add'); const adSticky=ad&&getComputedStyle(ad).position==='sticky';
                const clipBas=adSticky?Math.min(gr.bottom, ad.getBoundingClientRect().top-8*k):gr.bottom;
                const vis=[...g.querySelectorAll(':scope > .ph-o')].map(b=>{const r=b.getBoundingClientRect();
                   const st=getComputedStyle(b).position==='sticky';
                   const top=Math.max(r.top,gr.top), bot=Math.min(r.bottom, st?gr.bottom:clipBas);
                   return {n:(b.getAttribute('data-v')||b.textContent).trim().slice(0,14), y0:(r.top-D.top)/k, y1:(r.bottom-D.top)/k,
                           vis:Math.max(0,bot-top)/k, h:r.height/k, sticky:getComputedStyle(b).position==='sticky'};}).filter(v=>v.vis>0);
                const plusBas=Math.max(...vis.map(v=>v.y0+v.vis));
                const coupees=vis.filter(v=>!v.sticky && v.vis < v.h-1).map(v=>v.n);
                let surBarre=0; for(let x=40;x<=350;x+=30){ const h=document.elementFromPoint(D.left+x*k, D.top+772*k); if(h&&g.contains(h)) surBarre++; }
                return {plusBas:+plusBas.toFixed(1), coupees, surBarre, n:vis.length};}""", [GN, BORNE])
            bon = bool(m) and m['plusBas'] <= BORNE + 0.5 and not m['coupees'] and m['surBarre'] == 0
            pris['peaufiner'] = not bon
            t('%s · la liste vit au-dessus de Peaufiner' % nom, bon,
              ('bas %.1f (borne %d) · coupées %s · sur la barre %d' % (m['plusBas'], BORNE, m['coupees'], m['surBarre'])) if m else 'pas de liste')
    return pris


def passe(b, th, sonde=None):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(700)
    cdp = ctx.new_cdp_session(pg)
    if sonde: pg.evaluate(SONDES[sonde])
    seuls = [sonde] if sonde else None
    fiche = pg.evaluate("()=>{const p=promises.find(p=>!p.draft&&!p.req&&!p.chiche&&!p.nuee&&p.who&&!/^(moi|le groupe)$/i.test(p.who));return p?p.id:null}")
    CTX = [
        ('Promi · à qui', lambda: ouvre_page(pg, 0, 'bascule-qui'), True),
        ('Chiche · qui tu défies', lambda: ouvre_page(pg, 1, 'qui'), True),
        ('Chiche · avec qui', lambda: ouvre_page(pg, 1, 'avec'), True),
        ('Nuée · avec', lambda: ouvre_page(pg, 2, 'nuee'), True),
        ('Fiche · Peaufiner · À QUI', lambda: ouvre_fiche(pg, fiche, 'À QUI'), False),
    ]
    prises = {}
    for nom, ouvrir, pplus in CTX:
        if sonde == 'peaufiner' and not pplus: continue
        r = contrats(pg, cdp, '[%s] %s' % ('clair' if th == 'light' else 'sombre', nom), ouvrir, pplus, seuls)
        for k, v in r.items(): prises[k] = prises.get(k, False) or v
    if er: print('   erreurs de page :', er[:3])
    ctx.close()
    return prises


with sync_playwright() as p:
    b = p.chromium.launch()
    if '--sondes' in sys.argv:
        print('── PREUVE : chaque contrat sur un défaut fabriqué — il doit ROUGIR ──')
        bilan = {}
        for s in SONDES:
            print('\n· sonde « %s » (contrat : %s)' % (s, VISE[s]))
            pr = passe(b, 'light', s)
            bilan[s] = pr.get(s, False)
        print('\n── BILAN DES SONDES ──')
        for s, v in bilan.items(): print('  %-10s %s' % (s, 'PRISE' if v else '⚠ NON PRISE — le contrat est éteint'))
        b.close()
        sys.exit(0 if all(bilan.values()) else 1)
    for th in ['light', 'dark']:
        print('\n── thème %s ──' % th)
        passe(b, th)
    b.close()

print('\n%d/%d' % (ok[0], ok[0] + len(ko)))
if ko: print('KO :', ' · '.join(ko[:12]))
sys.exit(1 if ko else 0)
