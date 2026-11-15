#!/usr/bin/env python3
"""
redteam_moi_phrase.py — ⚑ v199 (Tom, C-269 REFAITE) : « moi » EN POINTILLÉS DANS LA PHRASE, PLUS DE LIGNE « À : MOI ».

« Le choix des personnes existe déjà, DANS LA PHRASE. Quand le texte est validé et qu'aucune personne n'a été choisie, la place du destinataire affiche
« moi » entre pointillés. Les pointillés restent tant que personne n'est ajouté ; ils disparaissent dès qu'une personne est ajoutée. Le toucher sur cette
place ouvre le choix existant, « moi » y figure comme une personne choisie (sa petite croix). » Tom (13 nov.) : Promi « Je promets … à qui ? » → « à moi » (« Je me
promets » ne change pas) ; Chiche « à qui ose ? » → « à moi » ; Cercle « avec tout le monde » → « avec moi » ; le mot paraît proprement, jamais d'un coup.

Banc comme Tom (WebKit, ×3, doigt), la vraie saisie. Natures : promi (« Je promets … à qui ? »), chiche, nuee ; et promi-soi (« Je me promets », inchangé).
Par nature × texte court et de 280 caractères × échelles 1 et 0,79 :
  A · avant la validation, la place porte son mot d'attente (« qui ? », « qui ose ? », « tout le monde ») ; validée (le trait né) : « moi », en pointillés ;
      plus aucune ligne « À : moi » (#ppQui absent) ; « Je me promets » : aucune place « moi » ;
  A · « moi » paraît par son TRACÉ (TraceLettres sur la place), jamais d'un coup ;
  B · la phrase de 280 caractères est entière (aucun « … ») ;
  C · le trait et la dalle : la géométrie de la page + (`_ppEcran` : base, amplitude, lignes ; la boîte de la dalle ; le trait déclaré) = v196 (`--ref=`).
Au doigt (court, ×1) : D · toucher la place ouvre le choix ; « Moi » y est choisi, avec sa croix ; E · Rachel ajoutée → « Rachel », sans pointillés, « Moi »
plus choisi ; retirée par sa croix → « moi » en pointillés ; F · plantée au trait avec Rachel → la parole (le Cercle) porte Rachel, sa fiche aussi ;
G · plantée sans personne → sur sa fiche, le choix des personnes montre « Moi » choisi, avec sa croix.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
REF = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ref=')), 'zz-v196.html')
NATS = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--natures=')), 'promi,chiche,nuee,promi-soi').split(',')
ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), '1,0.79').split(',')
SANS_DOIGT = '--sans-doigt' in sys.argv
ATT = {'promi': 'qui ?', 'chiche': 'qui ose ?', 'nuee': 'tout le monde'}          # les mots d'attente, en dur
LONG = ('courir le marathon de Paris avec toute la bande des copains du quartier puis fêter cela longtemps au bord du canal sous les lampions jusqu\'au matin et recommencer ' * 3)[:270]
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('  %s %-100s %s' % ('✅' if cond else '❌', nom, str(detail)[:300]), flush=True)
src = open('redteam_phrase_lignes.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0]; ns = {}; exec(compile(src, 'pl', 'exec'), ns)
pose, stable = ns['pose'], ns['stable']
PLACE = """k=>{ const e=document.querySelector(k==='nuee'?'#nueePhrase .ph-m[data-np="avec"]':'#csPhrase .ph-m[data-ph="qui"]'); return e?{txt:e.textContent, vide:e.classList.contains('ph-vide'), trace:!!e.__trace||!!e.__tl}:null; }"""
GEOM = """()=>{ let e=null; try{ e=_ppEcran(); }catch(x){} const c=document.getElementById('csTrameCv');
  return {base:e&&Math.round(e.base*100)/100, amp:e&&Math.round(e.amp*100)/100, nl:e&&e.nl, nat:e&&e.nat, dalle:window._ppDalleT?JSON.stringify(window._ppDalleT):null, trait:c&&c.getAttribute('data-trait')}; }"""
SUIT = """()=>{ window.__mt=[]; const T=window.TraceLettres; if(T && !T.__m){ T.__m=1; const t=T.trace; T.trace=function(c,x,o){ const pl=c && c.matches && (c.matches('#csPhrase .ph-m[data-ph="qui"], #nueePhrase .ph-m[data-np="avec"]') || (c.matches('.v200-mt') && c.parentElement && c.parentElement.matches('#csPhrase .ph-m[data-ph="qui"], #nueePhrase .ph-m[data-np="avec"]'))); if(!(o&&o.preparer) && !(o&&o.inverse) && pl) window.__mt.push(c.textContent);   /* ⚑ v200 (C-271) : le tracé se fait sur l'enveloppe du mot (.v200-mt), jamais sur l'encart et ses pointillés */ return t.apply(this, arguments); }; } }"""
def page(b, f, k, t, vw, vh, valide=True):
    ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, f)
    pg.evaluate("()=>{ Math.random=(function(){ let s=7; return ()=>{ s=(s*16807)%2147483647; return (s-1)/2147483646; }; })(); }")
    kk = 'promi' if k.startswith('promi') else k
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % kk); pg.wait_for_timeout(2600)
    if k == 'promi': B.tap_sel(pg, '#csPhrase .ph-b[data-ph="sens"]'); pg.wait_for_timeout(900)   # « Je me promets » → « Je promets … à qui ? »
    pg.evaluate(SUIT); avant = pg.evaluate(PLACE, kk)
    if not valide: return ctx, pg, avant
    pose(pg, kk, t); stable(pg, kk)
    for _ in range(60):
        if pg.evaluate("()=>{ try{ return _ppInvite.etat().visible; }catch(e){ return false; } }"): break
        pg.wait_for_timeout(200)
    pg.wait_for_timeout(2200); return ctx, pg, avant
with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_moi_phrase — %s (réf. %s), charge %.1f' % (F, REF, B.charge()))
    for vw, vh, nom in [x for x in ((430, 932, '1'), (330, 714, '0,79')) if (x[2] == '1' and '1' in ECH) or (x[2] != '1' and '0.79' in ECH)]:
        for k in NATS:
            kk = 'promi' if k.startswith('promi') else k
            for t in ('lire un livre', LONG):
                T = '[%s · ×%s · %s]' % (k, nom, 'court' if len(t) < 20 else '280 car.')
                ctx, pg, avant = page(b, F, k, t, vw, vh)
                apres = pg.evaluate(PLACE, kk); mt = pg.evaluate("()=>window.__mt||[]"); qui = pg.evaluate("()=>!!document.getElementById('ppQui')")
                if k == 'promi-soi':
                    juge(T + ' A · « Je me promets » : aucune place « moi » (inchangé)', apres is None and not qui, apres)
                else:
                    juge(T + ' A · avant la validation : « %s » ; validée : « moi », en pointillés ; plus de ligne « À : moi »' % ATT[k], avant and avant['txt'] == ATT[k] and apres and apres['txt'] == 'moi' and apres['vide'] and not qui, '%s → %s · ligne %s' % (avant, apres, qui))
                    juge(T + ' A · « moi » paraît par son TRACÉ (jamais d\'un coup)', 'moi' in mt, mt)
                coupe = pg.evaluate("k=>{ const ph=document.querySelector(k==='nuee'?'#nueePhrase .ph-txt':'#csPhrase .ph-txt'); return ph ? /…/.test(ph.textContent||'') : null; }", kk)
                juge(T + ' B · la phrase est entière (aucun « … »)', coupe is False, 'coupée' if coupe else coupe)
                geo = pg.evaluate(GEOM); err = [e for e in pg.erreurs if 'version.json' not in e]; ctx.close()
                ctx2, pg2, _ = page(b, REF, k, t, vw, vh); geo2 = pg2.evaluate(GEOM); ctx2.close(); vus = [geo2]
                if geo != geo2:   # la boîte de la dalle est fixée à l'ouverture et y prend l'une de deux tailles selon l'instant, en v196 aussi : v196 reprise une fois
                    ctx2, pg2, _ = page(b, REF, k, t, vw, vh); vus.append(pg2.evaluate(GEOM)); ctx2.close()
                juge(T + ' C · le trait et la dalle : la géométrie de la page + = v196 (base, amplitude, lignes, boîte de la dalle, trait)', geo in vus, '%s · v196 %s' % (geo, vus) if geo not in vus else geo)
                juge(T + ' aucune erreur de page', not err, err[:2])
    if '1' in ECH and not SANS_DOIGT:
        ST = """k=>{ const e=document.querySelector(k==='nuee'?'#nueePhrase .ph-m[data-np="avec"]':'#csPhrase .ph-m[data-ph="qui"]'); const m=document.querySelector('#createSheet .gn [data-gn-tete]');
          return {txt:e&&e.textContent, vide:e&&e.classList.contains('ph-vide'), choix:!!document.querySelector('#csChoix.ouvert')||!!((document.getElementById('nueeChoix')||{}).children||[]).length,
            moi:m?{on:m.classList.contains('on'), x:!!m.querySelector('.ppo-x'), nom:(m.querySelector('.ppo-nom')||{}).textContent}:null}; }"""
        for k in [n for n in NATS if n != 'promi-soi']:
            T = '[%s · au doigt]' % k; sel = '#nueePhrase .ph-m[data-np="avec"]' if k == 'nuee' else '#csPhrase .ph-m[data-ph="qui"]'
            ctx, pg, _ = page(b, F, k, 'lire un livre', 430, 932)
            B.tap_sel(pg, sel); pg.wait_for_timeout(1300); e = pg.evaluate(ST, k)
            juge(T + ' D · toucher la place ouvre le choix ; « Moi » y est choisi, avec sa croix', e['choix'] and e['moi'] and e['moi']['on'] and e['moi']['x'], e)
            B.tap_sel(pg, '#createSheet .gn [data-gn-tete] .ppo-x'); pg.wait_for_timeout(900); e = pg.evaluate(ST, k)
            juge(T + ' D · sa croix touchée seul : « Moi » reste choisi (la liste n\'est jamais vide)', e['moi'] and e['moi']['on'], e)
            B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
            pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(1200); e1 = pg.evaluate(ST, k)
            B.tap(pg, 195, 200); pg.wait_for_timeout(2600); e = pg.evaluate(ST, k)
            juge(T + ' E · Rachel ajoutée : « Rachel », sans pointillés ; « Moi » plus choisi', e['txt'].strip(', ') == 'Rachel' and not e['vide'] and e1['moi'] and not e1['moi']['on'], '%s · choix %s' % (e, e1['moi']))
            B.tap_sel(pg, sel); pg.wait_for_timeout(1300)
            B.tap_sel(pg, '#createSheet .gn .gn-liste .ph-o.on[data-v="Rachel"] .ppo-x'); pg.wait_for_timeout(900); B.tap(pg, 195, 200); pg.wait_for_timeout(2600); e = pg.evaluate(ST, k)
            juge(T + ' E · Rachel retirée par sa croix : « moi », en pointillés', e['txt'] == 'moi' and e['vide'], e)
            # F · Rachel de nouveau, planter au trait
            B.tap_sel(pg, sel); pg.wait_for_timeout(1300); B.tap_sel(pg, '#createSheet .gn > .ph-add'); pg.wait_for_timeout(400); pg.keyboard.type('Rachel', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
            pg.evaluate("()=>{ try{ document.activeElement && document.activeElement.blur(); }catch(e){} }"); pg.wait_for_timeout(1200); B.tap(pg, 195, 200); pg.wait_for_timeout(2600)
            def plante(pg):
                zid = 'planterZoneN' if k == 'nuee' else 'planterZone'
                z = pg.evaluate("(i)=>{ const c=document.getElementById(i); if(!c) return null; const r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), s=d.width/390; return [(r.left-d.left)/s,(r.top-d.top)/s,r.width/s,r.height/s]; }", zid)
                y = (z[1] + z[3] * 0.45) if z else 300; x1 = 375 if k == 'nuee' else 215
                B.glisse(pg, [[30 + (x1 - 30) * i / 16.0, y] for i in range(17)], pas=40); pg.wait_for_timeout(4500)
                return pg.evaluate("(k)=>{ if(k==='nuee'){ const n=Object.keys(NUE||{}).pop(); return {n:Object.keys(NUE||{}).length, mem:(NUEEMEM&&NUEEMEM[n])||[], cle:n}; } const p=promises[promises.length-1]; return {n:promises.length, id:p&&p.id, who:p&&p.who}; }", k)
            n0 = pg.evaluate("()=>promises.length"); r = plante(pg)
            if k == 'nuee':
                juge(T + ' F · le Cercle planté porte Rachel', 'Rachel' in (r.get('mem') or []), r); pg.evaluate("(c)=>{ try{ closeAll(); openEssaim(c); }catch(e){} }", r.get('cle'))
            else:
                juge(T + ' F · la parole plantée porte Rachel', r['n'] == n0 + 1 and 'Rachel' in str(r.get('who')), r); pg.evaluate("(i)=>{ try{ closeAll(); openDetail(i); }catch(e){} }", r.get('id'))
            pg.wait_for_timeout(2500); fq = pg.evaluate("()=>{ const q=document.getElementById('dptQui'); return q?q.textContent:null; }")
            juge(T + ' F · sa fiche montre Rachel', bool(fq) and 'Rachel' in fq, '« %s »' % fq)
            err = [x for x in pg.erreurs if 'version.json' not in x]; ctx.close()
            # G · planter sans personne : sur la fiche, « Moi » choisi avec sa croix
            ctx, pg, _ = page(b, F, k, 'lire un livre', 430, 932); r = plante(pg)
            if k == 'nuee': pg.evaluate("(c)=>{ try{ closeAll(); openEssaim(c); }catch(e){} }", r.get('cle'))
            else: pg.evaluate("(i)=>{ try{ closeAll(); openDetail(i); }catch(e){} }", r.get('id'))
            pg.wait_for_timeout(2500)
            g = pg.evaluate("(k)=>{ const h=window._gensFiche(k==='nuee'?'nuee':'qui'); document.body.appendChild(h); const m=h.querySelector('[data-gn-tete]'); const r={on:!!(m&&m.classList.contains('on')), x:!!(m&&m.querySelector('.ppo-x')), nom:m&&(m.querySelector('.ppo-nom')||{}).textContent}; h.remove(); return r; }", k)
            juge(T + ' G · plantée sans personne : sur la fiche, le choix montre « Moi » choisi, avec sa croix', g['on'] and g['x'] and g['nom'] == 'Moi', g)
            err += [x for x in pg.erreurs if 'version.json' not in x]
            juge(T + ' aucune erreur de page', not err, err[:2]); ctx.close()
    b.close()
ok = sum(1 for _, c in res if c); print('\n  %s %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
