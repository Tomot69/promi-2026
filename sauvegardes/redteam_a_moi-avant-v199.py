#!/usr/bin/env python3
"""
redteam_a_moi.py — ⚑ v197 (Tom, C-269) : « À : moi » PAR DÉFAUT SUR LA PAGE +, VISIBLE AVANT DE PLANTER.

« Au moment où le texte est validé (Promi, Chiche, Cercle), la ligne des personnes paraît sous le titre : « À : moi », ou « Avec : moi » pour un Cercle.
Un toucher sur la ligne ou sur le + ouvre le menu des membres existant. La liste n'est jamais vide : « moi » revient. Le trait et la naissance de la dalle
ne changent pas. Les mêmes personnes paraissent sur la fiche après la plantation. »

Banc comme Tom (WebKit, ×3, doigt) ; la vraie saisie (toucher le titre, taper, Retour). Pour chaque nature × texte court et de 280 caractères × échelles 1
(430 × 932) et 0,79 (330 × 714) :
  A · la ligne paraît, ses mots EN DUR (« À : moi », « Avec : moi ») ; elle est à 12 pt (± 1) sous l'encre de la phrase ;
  B · le + : orange #FB4C0D, son encre commence 26 pt (± 1) après le texte, son centre au milieu des capitales (± 1 pt) — lus sur l'IMAGE ;
  C · rien ne se recouvre (la phrase, la ligne, le + et sa zone, le rail du pinceau avec 12 pt d'air, « garder de côté », la barre), rien ne sort ;
  D · le trait et la dalle : la géométrie de la page + (`_ppEcran` : base, amplitude, lignes ; la boîte de la dalle) identique à v196 servie à côté
      (`--ref=`), et la bande du trait sur le canevas, au repos, au pixel près hors matière.
Au doigt (court, échelle 1) : E · toucher la ligne ouvre le choix ; « Rachel » ajoutée → « À : Rachel » ; retirée par sa croix → « À : moi » ;
F · Rachel ajoutée puis la parole plantée AU TRAIT : la parole porte Rachel, et sa fiche aussi.
"""
import io, os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
REF = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ref=')), 'zz-v196.html')
NATS = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--natures=')), 'promi,chiche,nuee').split(',')
ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), '1,0.79').split(',')
MOTS = {'promi': 'À : moi', 'chiche': 'À : moi', 'nuee': 'Avec : moi'}      # les mots de Tom, en dur
AIR_PH, ECART_PLUS, AIR_RAIL, OR = 12.0, 26.0, 12.0, (251, 76, 13)          # pt — les décisions (C-269, C-242), en dur ; #FB4C0D
LONG = ('courir le marathon de Paris avec toute la bande des copains du quartier puis fêter cela longtemps au bord du canal sous les lampions jusqu\'au matin et recommencer ' * 3)[:270]
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('  %s %-100s %s' % ('✅' if cond else '❌', nom, str(detail)[:300]), flush=True)
src = open('redteam_phrase_lignes.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0]; ns = {}; exec(compile(src, 'pl', 'exec'), ns)
pose, stable = ns['pose'], ns['stable']

LIGNE = """()=>{ const q=document.getElementById('ppQui'); const D=document.getElementById('device').getBoundingClientRect(), s=D.width/390;
  const R=x=>[(x.left-D.left)/s,(x.top-D.top)/s,(x.right-D.left)/s,(x.bottom-D.top)/s];
  if(!q) return null; const cs=getComputedStyle(q); const t=q.querySelector('.ppq-t'); const sv=q.querySelector('.ppq-p svg'), z=q.querySelector('.ppq-p');
  const rg=document.createRange(); rg.selectNodeContents(t); const r1=document.createRange(); if(t.firstChild){ r1.setStart(t.firstChild,0); r1.setEnd(t.firstChild,1); }
  const c=document.createElement('canvas').getContext('2d'); c.font=cs.fontStyle+' '+cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily; const mA=c.measureText('A');
  return {manque:q.getAttribute('data-manque'), vu:cs.visibility==='visible' && q.getAttribute('data-vu')==='1', txt:t.textContent, fam:cs.fontFamily.split(',')[0].replace(/["']/g,'').trim(), fs:parseFloat(cs.fontSize),
    texte:R(rg.getBoundingClientRect()), g1:t.firstChild?R(r1.getBoundingClientRect()):null, plus:sv?R(sv.getBoundingClientRect()):null, zone:z?R(z.getBoundingClientRect()):null,
    trait:sv?sv.querySelector('path').getAttribute('stroke'):null, cap:mA.actualBoundingBoxAscent/s*s, s:s}; }"""
GEOM = """()=>{ let e=null; try{ e=_ppEcran(); }catch(x){} const c=document.getElementById('csTrameCv');
  return {base:e&&Math.round(e.base*100)/100, amp:e&&Math.round(e.amp*100)/100, nl:e&&e.nl, nat:e&&e.nat, dalle:window._ppDalleT?JSON.stringify(window._ppDalleT):null, trait:c&&c.getAttribute('data-trait')}; }"""

def page(b, f, k, t, vw, vh):
    ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, f)
    pg.evaluate("()=>{ Math.random=(function(){ let s=7; return ()=>{ s=(s*16807)%2147483647; return (s-1)/2147483646; }; })(); }")
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600)
    pose(pg, k, t); stable(pg, k)
    for _ in range(60):   # le trait est né (la saisie de 280 caractères est longue)
        if pg.evaluate("()=>{ try{ return _ppInvite.etat().visible; }catch(e){ return false; } }"): break
        pg.wait_for_timeout(200)
    pg.wait_for_timeout(2200); return ctx, pg

def encre_plus(pg, L):
    """l'encre ORANGE du + et la ligne de base du premier glyphe, lues sur l'image (points de l'appareil)"""
    im = Image.open(io.BytesIO(B.capture(pg))).convert('RGB'); s = im.width / 390.0
    x0, y0, x1, y1 = [int(round(v * s)) for v in L['zone']]
    px = im.load(); o = [(x, y) for y in range(max(0, y0), min(im.height, y1)) for x in range(max(0, x0), min(im.width, x1)) if sum(abs(a - b_) for a, b_ in zip(px[x, y][:3], OR)) < 70]
    if not o: return None
    ox0, ox1 = min(p[0] for p in o) / s, max(p[0] for p in o) / s; oy0, oy1 = min(p[1] for p in o) / s, max(p[1] for p in o) / s
    g = L['g1']; fond = px[int(g[0] * s) - 3, int((g[1] + g[3]) / 2 * s)][:3]
    gx0, gx1 = int(g[0] * s), int(g[2] * s); bas = None
    for y in range(int(g[3] * s), int(g[1] * s), -1):
        if any(sum(abs(a - b_) for a, b_ in zip(px[x, y][:3], fond)) > 120 for x in range(gx0, gx1)): bas = y / s; break
    return {'x0': ox0, 'x1': ox1, 'y0': oy0, 'y1': oy1, 'base': bas}

with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in [x for x in ((430, 932, '1'), (330, 714, '0,79')) if (x[2] == '1' and '1' in ECH) or (x[2] != '1' and '0.79' in ECH)]:
        for k in NATS:
            for t in ('lire un livre', LONG):
                T = '[%s · ×%s · %s]' % (k, nom, 'court' if len(t) < 20 else '280 car.')
                ctx, pg = page(b, F, k, t, vw, vh)
                L = pg.evaluate(LIGNE); g = stable(pg, k); geo = pg.evaluate(GEOM)
                ok = bool(L and L['vu'])
                juge(T + ' A · la ligne paraît : « %s »' % MOTS[k], ok and L['txt'] == MOTS[k], L and ('« %s » · vue %s' % (L['txt'], L['vu']) + (' · LA PLACE MANQUE de %s pt (la ligne, 12 pt, le rail, 12 pt au-dessus de « garder de côté »)' % L['manque'] if L.get('manque') else '')))
                coupe = pg.evaluate("k=>{ const ph=document.querySelector(k==='nuee'?'#nueePhrase .ph-txt':'#csPhrase .ph-txt'); return ph ? /\u2026/.test(ph.textContent||'') : null; }", k)
                juge(T + ' A · la phrase n\'est jamais coupée (aucun « … » ; v198, C-269)', coupe is False, 'coupée' if coupe else coupe)   # ⚑ v198 (Tom) : la ligne toujours visible, la phrase jamais coupée
                if not ok: ctx.close(); continue
                bas = max(l[3] for l in g['lignes'])
                juge(T + ' A · sous l\'encre de la phrase, 12 pt (± 1), à la marge (24 pt), Gilbert 19 pt', abs(L['texte'][1] + (L['texte'][3] - L['texte'][1] - 20.9) / 2 - bas - AIR_PH) <= 1.0 and abs(L['texte'][0] - 24) <= 0.6 and L['fam'] == 'Gilbert' and abs(L['fs'] - 19) < 0.1,
                     'phrase %.1f · ligne %.1f · gauche %.1f · %s %s' % (bas, L['texte'][1], L['texte'][0], L['fam'], L['fs']))
                m = encre_plus(pg, L)
                juge(T + ' B · le + est orange #FB4C0D (lu sur l\'image), son encre 26 pt (± 1) après le texte', bool(m) and abs(m['x0'] - L['texte'][2] - ECART_PLUS) <= 1.0 and (L['trait'] or '').upper() == '#FB4C0D',
                     m and 'écart %.2f pt · trait %s' % (m['x0'] - L['texte'][2], L['trait']))
                if m and m['base']:
                    cc = m['base'] - L['cap'] / 2
                    juge(T + ' B · le + est centré sur les capitales (± 1 pt) et a leur hauteur (± 1)', abs((m['y0'] + m['y1']) / 2 - cc) <= 1.0 and abs((m['y1'] - m['y0']) - L['cap']) <= 1.0,
                         'centre du + %.2f · des capitales %.2f · hauteur %.2f / %.2f' % ((m['y0'] + m['y1']) / 2, cc, m['y1'] - m['y0'], L['cap']))
                blocs = [('ligne ' + str(i + 1), l) for i, l in enumerate(g['lignes'])] + [('À : moi', L['texte']), ('+', L['plus'])] + list(g['B'].items())
                pb = []
                for i in range(len(blocs)):
                    for j in range(i + 1, len(blocs)):
                        a_, b_ = blocs[i], blocs[j]
                        if a_[0].startswith('ligne') and b_[0].startswith('ligne'): continue
                        if {a_[0], b_[0]} == {'À : moi', '+'}: continue
                        air = AIR_RAIL if 'rail' in (a_[0], b_[0]) and ('À : moi' in (a_[0], b_[0]) or '+' in (a_[0], b_[0])) else 2
                        if ns['recouvre'](a_[1], b_[1], air): pb.append('%s × %s' % (a_[0], b_[0]))
                    r = blocs[i][1]
                    if r[0] < -0.5 or r[2] > 390.5 or r[3] > 844.5 or r[1] < -0.5: pb.append('%s hors de l\'écran' % blocs[i][0])
                juge(T + ' C · rien ne se recouvre (12 pt entre la ligne et le rail), rien ne sort', not pb, pb or 'ligne %s · rail %s' % ([round(v, 1) for v in L['texte']], [round(v, 1) for v in g['B'].get('rail', [])]))
                ctx.close()
                ctx2, pg2 = page(b, REF, k, t, vw, vh); geo2 = pg2.evaluate(GEOM); ctx2.close()
                juge(T + ' D · le trait et la dalle : la géométrie de la page + = v196 (base, amplitude, lignes, boîte de la dalle, trait déclaré)', geo == geo2, '%s · v196 %s' % (geo, geo2) if geo != geo2 else geo)
    # E, F : au doigt, court, échelle 1
    if '1' in ECH:
        ST = "()=>{ const q=document.getElementById('ppQui'); return {vu:q&&q.getAttribute('data-vu'), txt:q&&q.querySelector('.ppq-t').textContent, choix:!!document.querySelector('#csChoix.ouvert')||!!((document.getElementById('nueeChoix')||{}).children||[]).length}; }"
        for k in NATS:
            T = '[%s · au doigt]' % k
            ctx, pg = page(b, F, k, 'lire un livre', 430, 932)
            B.tap_sel(pg, '#ppQui .ppq-t'); pg.wait_for_timeout(1300); e = pg.evaluate(ST)
            juge(T + ' E · toucher la ligne ouvre le choix des personnes (la ligne se retire)', e['choix'] and e['vu'] == '0', e)
            B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
            pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(1200); B.tap(pg, 195, 200); pg.wait_for_timeout(2600); e = pg.evaluate(ST)
            juge(T + ' E · « Rachel » ajoutée, le choix refermé : « %s Rachel »' % MOTS[k].split(':')[0].strip(), e['vu'] == '1' and e['txt'] == MOTS[k].replace('moi', 'Rachel'), e)
            B.tap_sel(pg, '#ppQui .ppq-p'); pg.wait_for_timeout(1300); e = pg.evaluate(ST)
            juge(T + ' E · toucher le + ouvre le même choix', e['choix'], e)
            B.tap_sel(pg, '#createSheet .gn .gn-liste .ph-o.on[data-v="Rachel"] .ppo-x'); pg.wait_for_timeout(900); B.tap(pg, 195, 200); pg.wait_for_timeout(2600); e = pg.evaluate(ST)
            juge(T + ' E · Rachel retirée : « moi » revient — la liste n\'est jamais vide', e['vu'] == '1' and e['txt'] == MOTS[k], e)
            # F · Rachel de nouveau, puis planter au trait
            B.tap_sel(pg, '#ppQui .ppq-t'); pg.wait_for_timeout(1300); B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
            pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(1200); B.tap(pg, 195, 200); pg.wait_for_timeout(2600)
            n0 = pg.evaluate("()=>promises.length"); zid = 'planterZoneN' if k == 'nuee' else 'planterZone'
            z = pg.evaluate("(i)=>{ const c=document.getElementById(i); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), s=d.width/390; return [(r.left-d.left)/s,(r.top-d.top)/s,r.width/s,r.height/s]; }", zid)
            y = (z[1] + z[3] * 0.45) if z else 300
            x1 = 375 if k == 'nuee' else 215
            B.glisse(pg, [[30 + (x1 - 30) * i / 16.0, y] for i in range(17)], pas=40); pg.wait_for_timeout(4500)
            r = pg.evaluate("(k)=>{ if(k==='nuee'){ const n=Object.keys(NUE||{}).pop(); return {n:Object.keys(NUE||{}).length, mem:(NUEEMEM&&NUEEMEM[n])||[], cle:n}; } const p=promises[promises.length-1]; return {n:promises.length, id:p&&p.id, who:p&&p.who}; }", k)
            if k == 'nuee':
                juge(T + ' F · le Cercle planté au trait porte Rachel', 'Rachel' in (r.get('mem') or []), r)
                pg.evaluate("(c)=>{ try{ closeAll(); openEssaim(c); }catch(e){} }", r.get('cle')); pg.wait_for_timeout(2500)
            else:
                juge(T + ' F · la parole plantée au trait porte Rachel', r['n'] == n0 + 1 and 'Rachel' in str(r.get('who')), '%s (avant %d)' % (r, n0))
                pg.evaluate("(i)=>{ try{ closeAll(); openDetail(i); }catch(e){} }", r.get('id')); pg.wait_for_timeout(2500)
            fq = pg.evaluate("()=>{ const q=document.getElementById('dptQui'); return q?q.textContent:null; }")
            juge(T + ' F · sa fiche montre les mêmes personnes', bool(fq) and 'Rachel' in fq, '« %s »' % fq)
            juge(T + ' aucune erreur de page', not pg.__dict__['erreurs'], pg.__dict__['erreurs'][:2]); ctx.close()
    b.close()
ok = sum(1 for _, c in res if c); print('\n%d/%d' % (ok, len(res))); sys.exit(0 if ok == len(res) else 1)
