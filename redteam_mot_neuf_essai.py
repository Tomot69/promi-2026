# -*- coding: utf-8 -*-
"""⚑ v189b (Tom, C-257 suite) — « LE +N : TRIPLE VÉRIFICATION, ET TESTABLE PAR TOM ». L'adresse ?mot_neuf=1.
Trois passes (trois contextes neufs, banc WebKit, Toile du Cercle), chacune sur un Promi, un Chiche et un Cercle :
  A · à l'ouverture de la fiche, un mot arrive d'une personne de la parole (pas de moi) : « +1 » en #FB4C0D sur « Un mot… », la pastille sur ce mot (en tête de liste) ;
  B · la fiche fermée sans lire : la pastille sur la carte de l'Index et sur la ligne la plus récente du Fil ;
  C · rouverte : toujours « +1 » (un seul mot, pas deux) ; un toucher sur « +1 » fait glisser la fiche jusqu'au mot neuf (entier entre 112 et 760) ;
  D · lue, fermée, rouverte : le total, à l'encre de la ligne ; plus de pastille ;
  E · rechargée sans le paramètre : aucun mot d'essai ; les données (paroles, mots des Cercles, dernières actions) identiques à celles d'avant l'adresse ; aucune erreur de page."""
import sys, os, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, str(d)[:220]), flush=True); return ok
# hors de la comparaison : la place des graines (la Toile respire, HORS de lot-V181B) et `files: []` (ouvrir une fiche le pose, avec ou sans le paramètre — mesuré)
DONNEES = "()=>{ const g=k=>localStorage.getItem(k); let s=null; try{ s=JSON.parse(g('promi_state')||'null'); }catch(e){} const P=(s&&s.promises||[]).map(q=>{ const o=Object.assign({},q); ['x','y','tx','ty'].forEach(k=>delete o[k]); if(Array.isArray(o.files)&&!o.files.length) delete o.files; return o; }); return JSON.stringify([P, s&&s.NUE, s&&s.NUEEMEM, g('promi_cercle_mots'), g('promi_cercle_act')]); }"
CHOIX = """()=>{ const aFil=new Set((window.FEED||[]).map(f=>f.pid)); const ok=q=>!q.draft && !q.pending && !q.nuee && aFil.has(q.id) && !(q.comments||[]).length;
  const pr=promises.find(q=>ok(q) && !q.chiche), ch=promises.find(q=>ok(q) && q.chiche && q!==pr) || promises.find(q=>ok(q) && q!==pr && !q.chiche && q.id!==(pr&&pr.id));
  return [pr&&pr.id, ch&&ch.id, ch&&!!ch.chiche]; }"""
FICHE = """()=>{ const l=document.getElementById('cm5Ligne'), nb=l&&l.querySelector('.cm5-nb'), u=document.querySelector('#cm5Liste .cm5-un'), c=nb?getComputedStyle(nb):null;
  const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=u?u.getBoundingClientRect():null;
  return {nb:nb&&c.display!=='none'?nb.textContent.trim():'', col:c?(c.webkitTextFillColor||c.color):'', encre:l?getComputedStyle(l).color:'', neuf:u?u.getAttribute('data-neuf'):null, pas:u?!!u.querySelector('.s4-att'):false,
    qui:u?(u.textContent||'').slice(0,40):'', n:document.querySelectorAll('#cm5Liste .cm5-un').length, neufs:document.querySelectorAll('#cm5Liste .cm5-un[data-neuf]').length,
    y:r?(r.top-D.top)/k:null, b:r?(r.bottom-D.top)/k:null }; }"""
def ferme(pg):
    B.tap_sel(pg, '#detailPoster > .enh .closeb'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie() }catch(e){} try{ closeAll() }catch(e){} try{ setView('toile') }catch(e){} }"); pg.wait_for_timeout(700)
def ouvre(pg, nat, ref):
    if nat == 'cercle': pg.evaluate("()=>openEssaim('potager')")
    else: pg.evaluate("id=>openDetail(id)", ref)
    pg.wait_for_timeout(2800)
with sync_playwright() as p:
    b = p.webkit.launch()
    for passe in (1, 2, 3):
        ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 7000)
        avant = pg.evaluate(DONNEES); ids = pg.evaluate(CHOIX)
        pg.goto('http://127.0.0.1:8752/' + F + '?mot_neuf=1'); pg.wait_for_timeout(7500)
        for nat, ref in (('promi', ids[0]), ('chiche', ids[1]), ('cercle', 'potager')):
            T = '[passe %d · %s%s]' % (passe, nat, '' if nat != 'chiche' or ids[2] else ' (sans Chiche au Fil : une autre parole)')
            if ref is None: juge(T + ' une parole au Fil, sans mot', False); continue
            pg.evaluate("()=>{ try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(500)
            ouvre(pg, nat, ref); f = pg.evaluate(FICHE)
            moi = pg.evaluate("()=>[(typeof USER!=='undefined'&&USER&&USER.name)||'', localStorage.getItem('promi_prenom')||'']")
            juge(T + ' A · un mot arrive d\'une personne de la parole : « +1 » en #FB4C0D, la pastille sur ce mot, en tête', f['nb'] == '+1' and f['col'] in ('rgb(251, 76, 13)',) and f['neuf'] == '1' and f['pas'] and f['neufs'] == 1 and not any(m and f['qui'].startswith(m) for m in moi), f)
            ferme(pg)
            B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2600)
            sel = '#indexList .s4-carte[data-nk="potager"], #indexList .s4-carte[data-nuee="potager"]' if nat == 'cercle' else '#indexList .s4-carte[data-pid="%s"]' % ref
            ix = pg.evaluate("s=>{ const c=document.querySelector(s); return c ? !!c.querySelector(':scope > .s4-att') : null; }", sel)
            juge(T + ' B · l\'Index : la carte porte la pastille', ix is True, ix)
            pg.evaluate("()=>{ closeAll(); try{ setView('toile'); }catch(e){} }"); pg.wait_for_timeout(800); B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2800)
            sel = '#feedView .s4-carte[data-nk="potager"], #feedView .s4-carte[data-nuee="potager"]' if nat == 'cercle' else '#feedView .s4-carte[data-pid="%s"]' % ref
            if nat == 'cercle':   # les lignes du Fil d'un Cercle sont celles de ses paroles (`data-pid`)
                fl = pg.evaluate("()=>{ const ids=new Set(promises.filter(q=>q.nuee==='potager').map(q=>String(q.id))); return [...document.querySelectorAll('#feedView .s4-carte')].filter(c=>ids.has(c.getAttribute('data-pid'))).map(c=>!!c.querySelector(':scope > .s4-att')); }")
            else: fl = pg.evaluate("s=>[...document.querySelectorAll(s)].map(c=>!!c.querySelector(':scope > .s4-att'))", sel)
            juge(T + ' B · le Fil : la ligne la plus récente porte la pastille, et elle seule', bool(fl) and fl[0] and not any(fl[1:]), fl[:6])
            pg.evaluate("()=>{ closeAll(); try{ setView('toile'); }catch(e){} }"); pg.wait_for_timeout(700)
            ouvre(pg, nat, ref); f = pg.evaluate(FICHE)
            juge(T + ' C · rouverte : toujours « +1 », un seul mot neuf', f['nb'] == '+1' and f['neufs'] == 1, (f['nb'], f['neufs'], f['n']))
            B.tap_sel(pg, '#cm5Ligne .cm5-nb'); pg.wait_for_timeout(2400); g = pg.evaluate(FICHE)
            juge(T + ' C · le toucher sur « +1 » glisse jusqu\'au mot neuf (entier entre 112 et 760)', g['y'] is not None and g['y'] >= 111.5 and g['b'] <= 760.5, (g['y'] and round(g['y'], 1), g['b'] and round(g['b'], 1)))
            ferme(pg); ouvre(pg, nat, ref); h = pg.evaluate(FICHE)
            juge(T + ' D · lue puis rouverte : le total, à l\'encre de la ligne, plus de pastille', h['nb'] == str(h['n']) and h['col'] == h['encre'] and not h['neufs'], (h['nb'], h['n'], h['col'], h['encre'], h['neufs']))
            pg.evaluate("()=>{ try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(400)
        pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(7500)
        ess = pg.evaluate("()=>{ let n=0; (promises||[]).forEach(p=>(p.comments||[]).forEach(c=>{ if(c.essai) n++; })); try{ const M=JSON.parse(localStorage.getItem('promi_cercle_mots')||'{}'); Object.values(M).forEach(L=>L.forEach(c=>{ if(c.essai) n++; })); }catch(e){} return n; }")
        apres = pg.evaluate(DONNEES)
        diff = '' if apres == avant else next((i for i, (x, y) in enumerate(zip(json.loads(avant), json.loads(apres))) if x != y), '?')
        juge('[passe %d] E · rechargée sans le paramètre : aucun mot d\'essai, les données identiques à celles d\'avant' % passe, ess == 0 and apres == avant, (ess, diff))
        juge('[passe %d] E · aucune erreur de page' % passe, not [e for e in pg.erreurs if 'Load failed' not in e and 'cancelled' not in e], pg.erreurs[:2])
        ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
