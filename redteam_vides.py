#!/usr/bin/env python3
"""
redteam_vides.py — v178c (Tom, 4 nov. 2026, E4 étape 2, C-078) : LES ÉCRANS VIDES.
« Chaque écran vide montre exactement ses deux lignes et un seul élément touchable, qui mène à la bonne action ; la recherche ne dit jamais la même chose
qu'un vide de contenu ; clair et sombre, échelles 1 et 0,79. »
Les textes de Tom, EN DUR (mot pour mot). Pour chaque thème × échelle (430 × 932 ; 330 × 714), banc comme Tom (WebKit, au doigt, Toile vide relue) :
  ① la ligne 1 et la ligne 2 à l'écran, exactement (rendu : `innerText`, visibles, chacune prise au doigt à son centre) ;
  ② un seul élément touchable dans le bloc (la ligne 2), sa zone ≥ 44 pt de haut ; rien ne sort de l'écran ;
  ③ toucher la ligne 2 mène à l'action dite (la page + d'un Promi, « à quelqu'un » pour le Fil ; le filtre sur Tout ; le champ vidé ; l'Index ; l'ajout d'une personne) ;
  ④ la recherche dit autre chose que le vide de contenu.
Rouge sur v178b (`--fichier=zz-v178b.html`).
"""
import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
A = '’'
TXT = {   # mot pour mot (brief du 4 nov. 2026) ; l'apostrophe typographique de l'app
  'toile': ('Rien n' + A + 'est planté.', 'Qu' + A + 'as-tu dit aujourd' + A + 'hui que tu comptes tenir ?'),
  'index': ('Pas encore de parole.', 'La première se plante en une phrase.'),
  'ixtri': ('Rien sous ce tri.', 'Revenir à toutes les paroles.'),
  'ixgarde': ('Rien de gardé de côté.', 'Revenir à toutes les paroles.'),
  'ixq': ('Rien pour « zq ».', 'Revenir à tout l' + A + 'Index.'),
  'fil': ('Rien ne bouge encore.', 'Une parole donnée à quelqu' + A + 'un, et le Fil s' + A + 'anime.'),
  'filq': ('Rien pour « zq ».', 'Revenir à tout le Fil.'),
  'filtri': ('Rien sous ce tri.', 'Revenir à tout le Fil.'),
  'cercle': ('Un Cercle, c' + A + 'est des gens.', 'La première personne s' + A + 'ajoute ici.'),
  'aura': ('La première parole laissera sa trace ici.', 'Tout commence par une parole donnée.'),
  'auratenu': ('Rien de tenu pour l' + A + 'instant.', 'Une parole tenue prendra place ici.'),
  'personne': ('Rien entre vous pour l' + A + 'instant.', None),
}
NB = lambda s: s.replace(' ', ' ').replace(' ', ' ')
# le bloc lu à l'écran : ses lignes visibles, les éléments touchables qu'il porte, la place de la ligne 2, et si chaque ligne se prend au doigt
LIT = """(s)=>{ const b=document.querySelector(s); if(!b) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  const vis=e=>{ const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) return false; for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; } return true; };
  const pris=e=>{ const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!h && (h===e || e.contains(h)); };
  const l1=b.querySelector('.e4-l1')||(b.classList.contains('e4-l1')?b:null), l2=b.querySelector('.e4-l2');
  const R=e=>{ const r=e.getBoundingClientRect(); return [(r.left-D.left)/k,(r.top-D.top)/k,(r.right-D.left)/k,(r.bottom-D.top)/k]; };
  const tch=[...b.querySelectorAll('button,a,[role=button],[data-e4],input')].filter(vis);
  return {l1:l1&&vis(l1)?l1.innerText.trim():null, l2:l2&&vis(l2)?l2.innerText.replace(/\\s+/g,' ').trim():null, p1:l1?pris(l1):false, p2:l2?pris(l2):false,
    n:tch.length, r2:l2?R(l2):null, rb:R(b)}; }"""
def bloc(pg, s, cle, T, tap=True):
    pg.wait_for_timeout(700); v = pg.evaluate(LIT, s); a, b = TXT[cle]
    ok = v is not None and v['l1'] is not None and NB(v['l1']) == a and (NB(v['l2'] or '') == b if b else v['l2'] is None) and v['p1'] and (v['p2'] if b else True)
    juge(T + ' ① %s : ses deux lignes, exactement, visibles' % cle, ok, v and (v['l1'], v['l2'], v['p1'], v['p2']))
    if not v: return None
    r = v['rb']; dans = r[0] >= -0.5 and r[2] <= 390.5 and r[1] >= 0 and r[3] <= 844
    juge(T + ' ② %s : un seul élément touchable (la ligne 2), zone ≥ 44 pt, rien hors de l\'écran' % cle, (v['n'] == (1 if b else 0)) and (not b or (v['r2'][3] - v['r2'][1]) >= 43.5) and dans, 'touchables %d · ligne 2 %s · bloc %s' % (v['n'], v['r2'] and round(v['r2'][3] - v['r2'][1], 1), [round(x) for x in r]))
    if b and tap: B.tap_sel(pg, s + ' .e4-l2')
    return v
def ferme(pg): pg.evaluate("()=>{ try{ if(window._peaufSortie) _peaufSortie(); }catch(e){} try{ const a=document.getElementById('auraScreen'), x=document.querySelector('#auraScreen .closeb'); if(a&&a.classList.contains('show')&&x) x.click(); }catch(e){} try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(900)
def plus_ouverte(pg): return pg.evaluate("()=>{ const c=document.getElementById('createSheet'); return !!c && c.classList.contains('show') && c.classList.contains('pp-promi') ? (document.getElementById('csPhrase')||{}).textContent : null; }")

def tour(b, sombre, vw, vh, nom):
    T = '[%s · %s]' % ('sombre' if sombre else 'clair', nom)
    ctx = B.contexte(b, sombre, vw=vw, vh=vh); pg = B.ouvre(ctx, F); pg.wait_for_timeout(1200)
    # la Toile vide
    bloc(pg, '#e4Toile', 'toile', T); pg.wait_for_timeout(2600); ph = plus_ouverte(pg)
    juge(T + ' ③ toile : la ligne 2 ouvre la page + d\'un Promi', ph is not None, ph)
    ferme(pg)
    # l'Index : vide, recherche, gardés de côté, tri
    B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(1400)
    v0 = bloc(pg, '#indexList .e4v', 'index', T, tap=False)
    pg.evaluate("()=>{ const i=document.getElementById('ixSearch'); i.value='zq'; i.dispatchEvent(new Event('input',{bubbles:true})); }")
    vq = bloc(pg, '#indexList .e4v', 'ixq', T); pg.wait_for_timeout(700)
    q = pg.evaluate("()=>({v:document.getElementById('ixSearch').value, t:(document.querySelector('#indexList .e4v .e4-l1')||{}).innerText})")
    juge(T + ' ③ ④ index : la recherche dit autre chose que le vide, sa ligne 2 vide le champ', vq and v0 and vq['l1'] != v0['l1'] and q['v'] == '' and NB(q['t'] or '') == TXT['index'][0], q)
    for f, cle in (('brouillons', 'ixgarde'), ('demandes', 'ixtri')):
        pg.evaluate("(f)=>{ window.ixFiltre=f; buildIndex(); }", f); bloc(pg, '#indexList .e4v', cle, T); pg.wait_for_timeout(700)
        juge(T + ' ③ index %s : la ligne 2 remet le filtre sur Tout' % f, pg.evaluate("()=>window.ixFiltre") == 'tous' and NB(pg.evaluate("()=>(document.querySelector('#indexList .e4v .e4-l1')||{}).innerText") or '') == TXT['index'][0], pg.evaluate("()=>window.ixFiltre"))
    B.tap_sel(pg, '#indexList .e4v .e4-l2'); pg.wait_for_timeout(2600); ph = plus_ouverte(pg)
    juge(T + ' ③ index : la ligne 2 ouvre la page + d\'un Promi', ph is not None, ph)
    ferme(pg)
    # le Fil : vide, recherche
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(1400)
    f0 = bloc(pg, '#feedList .e4v', 'fil', T, tap=False)
    pg.evaluate("()=>{ const i=document.getElementById('fdSearch'); i.value='zq'; i.dispatchEvent(new Event('input',{bubbles:true})); }")
    fq = bloc(pg, '#feedList .e4v', 'filq', T); pg.wait_for_timeout(700)
    q = pg.evaluate("()=>({v:document.getElementById('fdSearch').value, t:(document.querySelector('#feedList .e4v .e4-l1')||{}).innerText})")
    juge(T + ' ③ ④ fil : la recherche dit autre chose que le vide, sa ligne 2 vide le champ', fq and f0 and fq['l1'] != f0['l1'] and q['v'] == '' and NB(q['t'] or '') == TXT['fil'][0], q)
    B.tap_sel(pg, '#feedList .e4v .e4-l2'); pg.wait_for_timeout(3200); ph = plus_ouverte(pg)
    juge(T + ' ③ fil : la ligne 2 ouvre la page + d\'un Promi, « à quelqu\'un »', ph is not None and 'Je promets' in ph and 'me promets' not in ph, ph)
    ferme(pg)
    # l'Aura sans parole
    B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(2600)
    va = pg.evaluate("""()=>{ const m=[...document.querySelectorAll('#auraScreen .e4-l2')].filter(e=>e.getBoundingClientRect().height>0); const e=m[0]; if(!e) return null;
        const p=e.parentElement; return {l1:(p.firstChild&&p.firstChild.nodeType===3)?p.firstChild.textContent.trim():null, l2:e.innerText.trim(), n:m.length}; }""")
    juge(T + ' ① aura : ses deux lignes, une seule touchable', va and NB(va['l1'] or '') == TXT['aura'][0] and NB(va['l2']) == TXT['aura'][1] and va['n'] == 1, va)
    B.tap_sel(pg, '#auraScreen .e4-l2'); pg.wait_for_timeout(2600); ph = plus_ouverte(pg)
    juge(T + ' ③ aura : la ligne 2 ouvre la page + d\'un Promi', ph is not None, ph)
    ferme(pg)
    # une personne, rien en commun
    pg.evaluate("()=>openPerson('Zoé')"); pg.wait_for_timeout(1500)
    vp = pg.evaluate("""()=>{ const e=document.querySelector('#personSheet .e4-ps'); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
        return {t:e.innerText.trim(), bt:document.querySelectorAll('#personSheet .ps-bt').length, x:[(r.left-D.left)/k,(r.right-D.left)/k], pris:(()=>{ const h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return !!h&&(h===e||e.contains(h)); })()}; }""")
    juge(T + ' ① personne : « Rien entre vous pour l\'instant. », sans ligne 2, les deux boutons restent', vp and NB(vp['t']) == TXT['personne'][0] and vp['bt'] == 2 and vp['pris'] and vp['x'][1] <= 390.5, vp)
    ferme(pg)
    if not VITE or (nom == '1' and not sombre):
        # avec une parole : l'Aura « rien de tenu », le Fil trié sans résultat, les pièces jointes vides
        B.plante_doigt(pg, 'écrire à Lou', 'moi', 0); ferme(pg)
        B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(2600)
        vt = pg.evaluate("""()=>{ const e=[...document.querySelectorAll('#auraScreen .e4-l2')].filter(e=>e.getBoundingClientRect().height>0)[0]; if(!e) return null; const p=e.parentElement;
            return {l1:(p.firstChild&&p.firstChild.nodeType===3)?p.firstChild.textContent.trim():null, l2:e.innerText.trim()}; }""")
        juge(T + ' ① aura, rien de tenu : ses deux lignes', vt and NB(vt['l1'] or '') == TXT['auratenu'][0] and NB(vt['l2']) == TXT['auratenu'][1], vt)
        B.tap_sel(pg, '#auraScreen .e4-l2'); pg.wait_for_timeout(2400)
        juge(T + ' ③ aura, rien de tenu : la ligne 2 ouvre l\'Index', pg.evaluate("()=>{ const s=document.getElementById('indexSheet')||document.getElementById('indexScreen'); return !!s && s.classList.contains('show'); }"))
        ferme(pg)
        for _ in range(3):
            B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(1400)
            if pg.evaluate("()=>{ const f=document.getElementById('feedView'); return !!f && getComputedStyle(f).display!=='none' && f.getBoundingClientRect().height>0; }"): break
        print('      fil ouvert :', pg.evaluate("()=>{ const f=document.getElementById('feedView'); return [getComputedStyle(f).display, Math.round(f.getBoundingClientRect().height), document.querySelectorAll('#feedList .fd-item, #feedList .s4-carte').length]; }"))
        pg.evaluate("()=>{ document.getElementById('fdTriBtn').click(); document.querySelector('#fdMenu [data-fdfilt=demandes]').click(); }"); pg.wait_for_timeout(1200); bloc(pg, '#feedList .e4v', 'filtri', T); pg.wait_for_timeout(900)
        juge(T + ' ③ fil trié sans résultat : la ligne 2 remet le filtre sur Tout', pg.evaluate("()=>window.fdFiltre") == 'tous' and pg.evaluate("()=>document.querySelectorAll('#feedList .e4v').length") == 0, pg.evaluate("()=>window.fdFiltre"))
        ferme(pg)
        pid = pg.evaluate("()=>promises.slice(-1)[0].id"); pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2200)
        pj = pg.evaluate("()=>[...document.querySelectorAll('.dpf-empty')].map(e=>e.textContent.trim())")
        juge(T + ' ① pièces jointes vides : « Aucun fichier. », sans phrase', pj and all(t == 'Aucun fichier.' for t in pj), pj)
        ferme(pg)
        # un Cercle sans membre
        pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][2];x&&x.click()}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{ const n=document.getElementById('nName'), b=document.getElementById('addNuee'); n.value='les voisins'; b.click(); }"); pg.wait_for_timeout(3200); ferme(pg)
        cle = pg.evaluate("()=>Object.keys(NUE).find(k=>NUE[k]==='les voisins')"); pg.evaluate("(k)=>{closeAll();openNueeDetail(k)}", cle); pg.wait_for_timeout(2600)
        # ⚑ v179b (Tom, C-235) : « Un Cercle, c'est des gens. » est SUPPRIMÉ partout, avec son code — un Cercle sans membre ne porte aucune phrase
        cz = pg.evaluate("()=>({noeud:!!document.querySelector('.e4-cercle'), texte:/c.est des gens|premi.re personne s.ajoute/i.test(document.body.innerText||''), code:typeof window._e4Cercle})")
        juge(T + ' ③ cercle sans membre : aucune phrase, aucun nœud, plus de code (C-235)', not cz['noeud'] and not cz['texte'] and cz['code'] == 'undefined', cz)
        ferme(pg)
    if pg.__dict__.get('erreurs'): juge(T + ' aucune erreur de page', False, pg.__dict__['erreurs'][:2])
    ctx.close()

with sync_playwright() as p:
    b = p.webkit.launch()
    print('redteam_vides — %s, charge %.1f' % (F, B.charge()))
    ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), None)   # un juge ≤ 10 min (C-227) : une échelle par passe
    for vw, vh, nom in ((430, 932, '1'), (330, 714, '0,79')):
        if ECH and ECH != nom: continue
        for sombre in (False, True):
            if VITE and (nom != '1') and sombre: continue
            tour(b, sombre, vw, vh, nom)
    b.close()
print('\n  %s %d / %d' % ('✅' if all(res) else '❌', sum(res), len(res)))
sys.exit(0 if all(res) else 1)
