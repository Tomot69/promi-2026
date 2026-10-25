#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_part.py — À PLUSIEURS : LA RÈGLE DE LA PART (v145, Tom et chef de chantier, 13 oct. 2026 — C-115).

« La fiche ne doit pas paraître tenue tant que les personnes n'ont pas tenu. Il faut savoir qui a tenu dès la fiche. »
La règle, portée EN DUR ici :
  · une parole qui engage plusieurs personnes est UNE parole (une fiche, une dalle) — plus une par personne ;
  · la seconde moitié du trait est divisée en autant de parts que de personnes qui doivent tenir ;
  · une part tracée est PLEINE (l'épaisseur du trait, 10 pt) à la couleur de l'état tenu #0B4A2A ; une part non tracée est un trait FIN (2,5 pt)
    dans la teinte de la nature, CONTINU (aucun point : la loi des points) ;
  · la fiche et la dalle restent EN COURS tant que toutes les parts ne sont pas tracées ; la dernière part tracée rend la parole tenue ;
  · jusqu'à 4 personnes : les initiales sous les parts TRACÉES seulement (v146, Q487) ; au-delà : un compte « k SUR n » ;
  · toucher le trait ouvre la liste des noms, avec la date de ceux qui ont tracé ;
  · une parole à une seule personne ne change pas (chevron et points, « TRACE POUR TENIR », pas de parts).
Par banc_tom (WebKit, 390 × 844 @3x, Toile vide). ⚑ v146 : les paroles à plusieurs sont plantées PAR LE VRAI CHEMIN — le +, la pilule, « à qui »,
chaque prénom ÉCRIT dans la zone en pointillés et validé (le « + », puis Retour), puis le trait. 2, 3 et 6 personnes, deux ordres de tracé. Le verdict vient du CANEVAS de la fiche (l'épaisseur et la couleur du trait, colonne par
colonne) ; `data-parts` ne sert qu'à savoir où regarder. La part d'une autre personne arrive par `_parts.arrive` (le prototype n'a pas de réseau).
`--sonde` coupe le peintre des parts : le juge rougit.     Usage : python3 redteam_part.py [fichier.html] [--port=8752] [--sonde]
"""
import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
arg = lambda k, d: next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--' + k + '=')), d)
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); PORT = arg('port', '8752'); SONDE = '--sonde' in sys.argv
EP, FIN, TENU = 10.0, 2.5, (11, 74, 42)          # l'épaisseur du trait, celle d'une part non tracée, la couleur de l'état tenu (#0B4A2A)
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:330]), flush=True)
# pour chaque part : son épaisseur peinte et sa couleur, lues sur le canevas à cinq abscisses ; et s'il y a de l'encre sous elle (les initiales)
LIT = r"""()=>{ const cv=document.getElementById('dpTrameCv'); if(!cv) return null; const t=(cv.getAttribute('data-trait')||'').split(','), dp=cv.getAttribute('data-parts');
  const k=cv.width/390, g=cv.getContext('2d'), f=window._onde.onde(parseFloat(t[0]), parseFloat(t[1])), P=dp?JSON.parse(dp):null;
  /* sous l'onde le canevas est TRANSPARENT : le trait est ce qui est opaque et n'a pas la couleur du champ, dans une fenêtre de ± 7,5 pt autour de l'onde
     (les initiales, posées dessous, n'y entrent pas). Une première écriture prenait pour référence « le pixel 16 pt sous l'onde » : il tombait dans
     l'initiale d'une part tracée, verte comme elle — le trait vert n'était plus compté, et la part sortait « noire ». */
  function col(x){ const xi=Math.round(x*k), y0=Math.round((f(x)-7.5)*k), h=Math.round(15*k), d=g.getImageData(xi, y0, 1, h).data, hh=g.getImageData(xi, Math.round((f(x)-15)*k), 1, 1).data; let n=0, r=0, v=0, b=0;
    for(let i=0;i<h;i++){ if(d[i*4+3]<200) continue; const dh=Math.abs(d[i*4]-hh[0])+Math.abs(d[i*4+1]-hh[1])+Math.abs(d[i*4+2]-hh[2]); if(dh>60){ n++; r+=d[i*4]; v+=d[i*4+1]; b+=d[i*4+2]; } }
    return {ep:n/k, c:n?[Math.round(r/n),Math.round(v/n),Math.round(b/n)]:null}; }
  function encreSous(xa, xb){ let n=0; for(let x=xa;x<=xb;x+=0.5){ const xi=Math.round(x*k), y0=Math.round((f(x)+7.5)*k), h=Math.round(18*k), d=g.getImageData(xi,y0,1,h).data; for(let i=0;i<h;i++){ if(d[i*4+3]>128) n++; } } return n; }
  const out={trait:t, parts:P, mesures:[], seconde:[]};
  if(P){ P.x.forEach(function(q,i){ const L=q[1]-q[0], M=[0.2,0.35,0.5,0.65,0.8].map(u=>col(q[0]+L*u)); const xc=(q[0]+q[1])/2; out.mesures.push({ep:M.map(m=>+m.ep.toFixed(1)), c:M[2].c, encre:encreSous(xc-9, xc+9)}); });
    out.centre=encreSous((195+14+390)/2-26, (195+14+390)/2+26); }
  for(let x=215;x<=380;x+=3) out.seconde.push(+col(x).ep.toFixed(1));
  const dq=document.getElementById('dptQuand'), tr=document.getElementById('dptTrace'), dpo=document.getElementById('detailPoster');
  out.quand=dq?dq.textContent.trim():''; out.consigne=tr&&getComputedStyle(tr).display!=='none'?tr.textContent.trim().toUpperCase():''; out.cls=dpo.className; out.aria=cv.getAttribute('aria-label')||'';
  return out; }"""
def ouvre_fiche(pg, pid):
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600)
def proche(c, ref, tol=70): return bool(c) and abs(c[0] - ref[0]) + abs(c[1] - ref[1]) + abs(c[2] - ref[2]) <= tol
def plante_a(pg, titre, gens, nature=1):
    """⚑ v146 (Tom, C-122 : « Rejoue ensuite redteam_part sur ce vrai chemin ») — planter à plusieurs PAR LE VRAI CHEMIN, AU DOIGT : le +, la
    pilule de la nature, le mot « à qui » de la phrase, la zone en pointillés où l'on ÉCRIT chaque prénom (validé au « + », puis à Retour, en
    alternance), puis le TRAIT (80 pt ; la règle en demande 60). Avant v146 les personnes étaient posées par `newWhoSel` et la parole plantée
    par un clic scripté : l'ajout d'une personne, cassé sur l'iPhone, n'était jamais joué. Original : sauvegardes/redteam_part-avant-v146.py"""
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(350); B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(650)
    k = ['promi', 'chiche'][nature]; B.tap_sel(pg, '.acc-pil[data-k=%s]' % k)
    for _ in range(40):
        pg.wait_for_timeout(120)
        if pg.evaluate("k=>{ var s=document.getElementById('createSheet'); return !!(s && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix') && !s.classList.contains('acc-passe')); }", k): break
    pg.wait_for_timeout(600)
    if nature == 0: B.tap_sel(pg, '#csPhrase [data-ph=sens]'); pg.wait_for_timeout(900)
    B.tap_sel(pg, '#csPhrase [data-ph=qui]'); pg.wait_for_timeout(1000)
    B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(250)
    # ⚑ v147 — L'INSTRUMENT ATTEND LE CLAVIER, COMME UN DOIGT (§8, « un instrument qui ralentit avec la machine ») : machine chargée (charge 11 à 20,
    #   une autre session), le clavier partait avant que la zone ait pris le focus, et les lettres tombaient dans le vide (« à Nico » seul, au
    #   second passage C). Sur l'iPhone on tape quand le clavier est là. On attend donc le focus avant d'écrire, et le nom dans la liste après
    #   l'avoir validé — aucune reprise : si le nom n'y est pas, le juge le dira.
    for i, n in enumerate(gens):
        for _ in range(30):
            if pg.evaluate("()=>document.activeElement && document.activeElement.id==='gnSaisie'"): break
            pg.wait_for_timeout(100)
        pg.keyboard.type(n, delay=25); pg.wait_for_timeout(300)
        if i % 2 == 0:
            # le doigt touche le « + » qu'il VOIT : on attend qu'il soit posé (deux relevés identiques à 120 ms) — sous charge il glissait encore
            # quand le juge touchait, et le toucher tombait sur « Moi » (qui vide la liste)
            q = None
            for _ in range(25):
                r = pg.evaluate("()=>{ var e=document.querySelector('#createSheet .gn > .ph-add .gn-plus'); if(!e) return null; var b=e.getBoundingClientRect(); return b.width>2?[Math.round(b.left),Math.round(b.top)]:null; }")
                if r and r == q: break
                q = r; pg.wait_for_timeout(120)
            B.tap_sel(pg, '#createSheet .gn > .ph-add .gn-plus')
        else: pg.keyboard.press('Enter')
        for _ in range(20):
            pg.wait_for_timeout(100)
            if pg.evaluate("n=>{ try{ return newWhoSel.indexOf(n)>=0; }catch(e){ return true; } }", n): break
        pg.wait_for_timeout(400)
        if '--dbg' in sys.argv: print('   dbg', n, pg.evaluate("()=>({sel:JSON.stringify(newWhoSel), act:document.activeElement&&document.activeElement.id, ph:(document.getElementById('csPhrase')||{}).textContent.slice(0,80)})"))
    pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(400)
    pg.evaluate("a=>{ document.getElementById('fTitle').value=a; try{ if(window._phrase){ _phrase.titre=a; } }catch(e){} window._csEnLair=true; window._csDueISO=null; }", titre); pg.wait_for_timeout(300)
    n0 = pg.evaluate("()=>promises.length")
    z = pg.evaluate("()=>{ const c=document.getElementById('planterZone'); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return r.width>20?[(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]:null }")
    if z:
        y = z[1] + z[3] * 0.45; B.glisse(pg, [[40 + 80 * i / 10.0, y] for i in range(11)], pas=60)
    pg.wait_for_timeout(3400)
    pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(500)
    return n0, pg.evaluate("()=>promises.length"), pg.evaluate("()=>{ var p=promises[promises.length-1]; return {id:p.id, who:p.who, chiche:!!p.chiche, status:p.status}; }")
def etat_fiche(pg, nom, n, faites, natcol, initiales=None):
    """la fiche ouverte : n parts, celles de `faites` pleines et vertes, les autres fines et à la teinte de la nature ; en cours tant qu'il en reste"""
    L = pg.evaluate(LIT); P = (L or {}).get('parts')
    if not P or len(L['mesures']) != n:
        juge('%s : le trait porte %d parts' % (nom, n), False, 'data-parts %s' % (P,)); return L
    bons = True; det = []
    for i, m in enumerate(L['mesures']):
        ep = sorted(m['ep'])[2]; tr = i in faites
        ok = (abs(ep - EP) <= 2.0 and proche(m['c'], TENU)) if tr else (1.0 <= ep <= FIN + 2.0 and proche(m['c'], natcol, 90) and min(m['ep']) >= 1.0)
        bons = bons and ok; det.append('%s %.1f pt %s' % ('TRACÉE' if tr else 'fine', ep, m['c']))
    juge('%s : %d part(s) tracée(s) pleines et vertes, les autres fines, continues, à la teinte de la nature' % (nom, len(faites)), bons, ' · '.join(det))
    tenue = 'f-tenue' in L['cls'] or 'TENU' in L['quand'].upper()
    juge('%s : la fiche reste en cours' % nom, not tenue, 'état « %s »' % L['quand'])
    if n <= 4:
        # ⚑ v146 (chef de chantier, Q487) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_part-avant-v146b.py) : « sur la fiche, initiales seulement sous les
        #   parts TRACÉES ; les parts non tracées restent anonymes (grille, question 3) ». Sous une part tracée : son initiale, de l'encre ; sous une part non tracée : rien.
        att = [(initiales[i] if initiales is not None else None) if i in faites else '' for i in range(n)]
        juge('%s : les initiales sous les parts TRACÉES seulement, rien sous les autres (Q487)' % nom, all((P['textes'][i] == att[i] if att[i] is not None else P['textes'][i] != '') for i in range(n)) and all((m['encre'] > 12) if i in faites else (m['encre'] <= 4) for i, m in enumerate(L['mesures'])),
             'déclarées %s · encre sous les parts %s' % (P['textes'], [m['encre'] for m in L['mesures']]))
    else:
        juge('%s : le compte « %d SUR %d »' % (nom, len(faites), n), P['textes'] == ['%d SUR %d' % (len(faites), n)] and L['centre'] > 40, 'déclaré %s · encre au centre %s' % (P['textes'], L['centre']))
    return L
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); pg.__dict__['erreurs'] = []; pg.on('pageerror', lambda e: pg.__dict__['erreurs'].append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%s/%s' % (PORT, F)); pg.wait_for_timeout(6500)
    if SONDE: pg.evaluate("()=>{ window._partsPeint=null; }")
    juge('la règle existe dans l\'app (`_parts`)', pg.evaluate("()=>!!(window._parts && window._parts.tenants && window._partsPeint)") or SONDE)
    try:
        CHICHE = (61, 15, 35)          # la teinte du trait d'un Chiche (#3D0F23)
        # ── A · une parole à une seule personne ne change pas
        B.plante_doigt(pg, 'rendre le livre', 'moi', 0); p1 = pg.evaluate("()=>promises[promises.length-1].id"); ouvre_fiche(pg, p1); L = pg.evaluate(LIT)
        pts = [e for e in L['seconde']]; creux = sum(1 for i in range(1, len(pts)) if pts[i] < 1 <= pts[i - 1])
        juge('A · une parole à une seule personne ne change pas : pas de parts, des points, « TRACE POUR TENIR »', L['parts'] is None and creux >= 4 and L['consigne'] == 'TRACE POUR TENIR', 'parts %s · %d intervalles entre des points · consigne « %s »' % (L['parts'], creux, L['consigne']))
        # ── B · deux personnes : un Chiche lancé à Rachel et Marion
        n0, n1, pr = plante_a(pg, 'le grand plongeoir', ['Rachel', 'Marion'])
        juge('B · planter à deux personnes fait UNE parole', n1 == n0 + 1 and pr['chiche'] and 'Rachel' in pr['who'] and 'Marion' in pr['who'], '%d → %d paroles · à « %s »' % (n0, n1, pr['who']))
        T = pg.evaluate("id=>window._parts?_parts.tenants(promises.find(p=>p.id===id)):null", pr['id'])
        juge('B · ceux qui doivent tenir : Rachel et Marion', T == ['Rachel', 'Marion'], T)
        ouvre_fiche(pg, pr['id']); L = etat_fiche(pg, 'B · 2 personnes, aucune part', 2, [], CHICHE, ['R', 'M'])
        juge('B · la consigne : « À CHACUN DE TRACER SA PART »', (L or {}).get('consigne') == 'À CHACUN DE TRACER SA PART', (L or {}).get('consigne'))
        pg.evaluate("id=>_parts.arrive(promises.find(p=>p.id===id),'Marion','2026-10-12T10:00:00.000Z')", pr['id']); pg.wait_for_timeout(900)
        L = etat_fiche(pg, 'B · 2 personnes, Marion a tracé', 2, [1], CHICHE, ['R', 'M'])
        juge('B · la consigne nomme celle qui reste : « À RACHEL DE TRACER SA PART »', (L or {}).get('consigne') == 'À RACHEL DE TRACER SA PART', (L or {}).get('consigne'))
        st = pg.evaluate("id=>promises.find(p=>p.id===id).status", pr['id'])
        juge('B · la parole (et donc sa dalle) reste en cours', st == 'encours', st)
        # toucher le trait : la liste des noms, avec la date de ceux qui ont tracé
        r = pg.evaluate("()=>{ const cv=document.getElementById('dpTrameCv'), q=cv.getBoundingClientRect(), k=q.width/390, P=JSON.parse(cv.getAttribute('data-parts')), t=cv.getAttribute('data-trait').split(','), f=window._onde.onde(+t[0],+t[1]); const x=(P.x[0][0]+P.x[0][1])/2; return [q.left+x*k, q.top+f(x)*k]; }")
        pg.touchscreen.tap(r[0], r[1]); pg.wait_for_timeout(700)
        li = pg.evaluate("()=>{ const l=document.getElementById('partsListe'); if(!l) return null; return [...l.querySelectorAll('.pl-rang')].map(e=>[e.children[0].textContent, e.children[1].textContent]); }")
        juge('B · toucher le trait ouvre la liste des noms, la date pour qui a tracé', li == [['Rachel', ''], ['Marion', '12 oct.']], li)
        pg.touchscreen.tap(195, 120); pg.wait_for_timeout(600)
        juge('B · un toucher referme la liste, la fiche est toujours là', pg.evaluate("()=>!document.getElementById('partsListe') && document.getElementById('detailPoster').classList.contains('show')"))
        pg.evaluate("id=>_parts.arrive(promises.find(p=>p.id===id),'Rachel')", pr['id']); pg.wait_for_timeout(4200)
        fin = pg.evaluate("id=>{ const p=promises.find(p=>p.id===id); return [p.status, document.getElementById('detailPoster').classList.contains('f-tenue')]; }", pr['id'])
        juge('B · la dernière part tracée rend la parole tenue', fin == ['tenu', True], fin)
        # ── C · trois personnes, deux ordres de tracé
        for ordre in ([2, 0, 1], [1, 2, 0]):
            titre = 'courir dimanche' if ordre[0] == 2 else 'nager en mer'
            n0, n1, pr = plante_a(pg, titre, ['Rachel', 'Marion', 'Nico'])
            ouvre_fiche(pg, pr['id']); noms = ['Rachel', 'Marion', 'Nico']; faites = []
            etat_fiche(pg, 'C · 3 personnes, ordre %s, aucune part' % ordre, 3, [], CHICHE, ['R', 'M', 'N'])
            for k, i in enumerate(ordre[:2]):
                pg.evaluate("a=>_parts.arrive(promises.find(p=>p.id===a[0]),a[1])", [pr['id'], noms[i]]); pg.wait_for_timeout(900); faites.append(i)
                etat_fiche(pg, 'C · 3 personnes, ordre %s, après %s' % (ordre, noms[i]), 3, faites, CHICHE, ['R', 'M', 'N'])
            # la dalle : l'Index, ouvert maintenant, ne dit pas « tenu »
            idx = pg.evaluate("id=>{ try{closeAll()}catch(e){} window.ouvrirIndex(); return 1; }", pr['id']); pg.wait_for_timeout(2200)
            et = pg.evaluate("t=>{ const c=[...document.querySelectorAll('#indexList .s4-carte')].find(e=>e.textContent.toLowerCase().indexOf(t)>=0); return c?c.textContent.replace(/\\s+/g,' ').slice(0,90):null; }", titre)
            juge('C · ordre %s : dans l\'Index, la parole n\'est pas tenue' % ordre, bool(et) and 'TENU' not in et.upper(), et)
            ouvre_fiche(pg, pr['id']); pg.evaluate("a=>_parts.arrive(promises.find(p=>p.id===a[0]),a[1])", [pr['id'], noms[ordre[2]]]); pg.wait_for_timeout(4200)
            juge('C · ordre %s : la troisième part rend la parole tenue' % ordre, pg.evaluate("id=>promises.find(p=>p.id===id).status", pr['id']) == 'tenu')
            pg.evaluate("id=>{ try{closeAll()}catch(e){} window._v16SupprimerPromi && 0; }", pr['id'])
        # ── D · six personnes : un compte, pas d'initiales
        n0, n1, pr = plante_a(pg, 'traverser le lac', ['Rachel', 'Marion', 'Nico', 'Adrien', 'Lou', 'Sam'])
        juge('D · planter à six personnes fait UNE parole', n1 == n0 + 1, '%d → %d' % (n0, n1))
        ouvre_fiche(pg, pr['id']); etat_fiche(pg, 'D · 6 personnes, aucune part', 6, [], CHICHE)
        for nom in ('Nico', 'Sam', 'Rachel'): pg.evaluate("a=>_parts.arrive(promises.find(p=>p.id===a[0]),a[1])", [pr['id'], nom]); pg.wait_for_timeout(700)
        etat_fiche(pg, 'D · 6 personnes, trois parts', 6, [0, 2, 5], CHICHE)
        # ── E · quand c'est à moi : un Chiche reçu, avec deux autres — mon geste trace MA part, et seulement elle
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); B.plante_doigt(pg, 'chanter en public', 'moi', 1)
        pe = pg.evaluate("()=>{ var p=promises[promises.length-1]; p.from='Marion'; p.who='moi'; p.avec='Rachel, Nico'; try{queueSave()}catch(e){} return p.id; }")
        T = pg.evaluate("id=>_parts.tenants(promises.find(p=>p.id===id))", pe)
        juge('E · un Chiche reçu avec deux autres : moi, Rachel et Nico doivent tenir', T == ['moi', 'Rachel', 'Nico'], T)
        ouvre_fiche(pg, pe); L = etat_fiche(pg, 'E · à moi de tracer, aucune part', 3, [], CHICHE, ['T', 'R', 'N'])
        juge('E · la consigne reste « TRACE POUR TENIR »', (L or {}).get('consigne') == 'TRACE POUR TENIR', (L or {}).get('consigne'))
        # le geste de tenir, au doigt, comme redteam_trait : un appui (380 ms) dans la zone du geste, puis 100 pt d'avancée (la règle : 60 pt)
        z = pg.evaluate("()=>{ const r=document.getElementById('tenirZone').getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k]; }")
        yz = z[1] + z[3] * 0.45; B.glisse(pg, [[200 + 100 * i / 12.0, yz] for i in range(13)], pas=40, tenue=380); pg.wait_for_timeout(1500)
        apres = pg.evaluate("id=>{ const p=promises.find(p=>p.id===id), d=document.getElementById('detailPoster'); return {parts:Object.keys(p.parts||{}), status:p.status, instant:d.classList.contains('inst-referme')||d.classList.contains('inst-apres'), tenue:d.classList.contains('f-tenue')}; }", pe)
        juge('E · mon geste trace MA part, et la parole reste en cours (aucun instant « tenu »)', apres['parts'] == ['moi'] and apres['status'] == 'encours' and not apres['instant'] and not apres['tenue'], apres)
        etat_fiche(pg, 'E · ma part tracée', 3, [0], CHICHE, ['T', 'R', 'N'])
    except Exception as ex:
        juge('le juge va au bout (la règle de la part répond partout)', False, str(ex).replace('\n', ' ')[:260])
    juge('aucune erreur de page', not pg.erreurs, pg.erreurs[:2])
    B.capture(pg, 'scratchpad/v146/part-derniere.png')
    b.close()
ok = sum(1 for r in res if r[1]); print('\n%d / %d' % (ok, len(res)))
if ok < len(res): print('KO :', ' · '.join(r[0] for r in res if not r[1])[:1200])
sys.exit(0 if ok == len(res) else 1)
