#!/usr/bin/env python3
"""redteam_index_fil.py — ⚑ v183d (Tom, 7 nov. 2026, C-250) : « Tom pense que c'est bon, mais on n'est jamais sûr. Écris un juge agressif sur l'Index, le Fil et
leurs liens. Pour chaque cas : même ordre dans l'Index et le Fil, aucun doublon, aucune carte perdue, la bonne fiche ouverte, retour au même endroit. Sur l'état
exporté de Tom et sur un état synthétique de 200 paroles. »

Banc WebKit, `banc_tom` (webdriver masqué, l'état relu comme sur un téléphone). L'Index et le Fil sont LUS SUR LEURS CARTES RENDUES (`.s4-carte`, rangées par leur
place dans la grille), jamais sur la composition que l'app publie : une carte de l'Index se reconnaît à son titre (un Cercle à son nom), une carte du Fil à sa
parole (`data-pid`). Après CHAQUE cas, quatre invariants :
  I1 · l'Index porte chaque parole seule (hors d'un Cercle nommé) et chaque Cercle, une fois et une seule — ni doublon, ni carte perdue ;
  I2 · le Fil porte autant de cartes de chaque parole que le journal (`FEED`) d'événements à son nom — ni doublon, ni carte perdue ;
  I3 · le même ordre : les paroles du Fil, rangées à leur première carte et ramenées à leur entrée d'Index (un Cercle pour ses paroles), sont dans l'ordre de l'Index ;
  I4 · aucune erreur de page.
Les cas (dans cet ordre, sur la même page — l'état s'accumule, comme chez Tom) :
  A · un MOT au doigt (« Un mot… », la saisie, Entrée) sur la parole seule la plus basse de l'Index → en tête de l'Index et du Fil ;
  B · TENIR une autre parole ancienne par son sélecteur d'état (le chemin du trait) → en tête ;
  C · Peaufiner : son échéance changée → en tête ;
  D · PLANTER (le +, la nature, le bouton) → la parole neuve en tête ;
  E · EFFACER une parole ancienne (« Supprimer », confirmé) → elle n'est plus nulle part, rien d'autre ne manque ;
  F · un mot sur une parole d'un CERCLE → le Cercle en tête de l'Index, ses cartes en tête du Fil ;
  G · DEUX ACTIONS RAPIDES (120 ms) sur deux paroles différentes → la seconde en tête, la première juste après ;
  H · RECHARGER → les deux ordres identiques ;
  J · un SECOND ONGLET fait une action (par la vraie saisie, 4 s après s'être ouvert) → le premier, revenu au premier plan, la montre en tête ;
  J2 · un onglet DÉPASSÉ (un autre a écrit, il ne peut pas encore se recharger) fait une action → elle est gardée, et celle de l'autre aussi ;
  K · `?jour=+30` → les deux ordres identiques à ceux du jour ;
  L · un TRI actif (Par personne) puis retiré → les deux ordres d'avant ;
  M · le FIL RESTÉ OUVERT SOUS UNE FICHE : une carte du bas touchée, sa fiche (la bonne), un mot, le X → on est sur le Fil, la parole est en tête ;
  N · une carte du Fil → sa fiche (la bonne) → le X → le Fil, au même défilement ; la même chose depuis l'Index.
`--etat=tom|200|tous` (défaut : tous), `--partie=1` (A à H), `2` (J à L) ou `3` (M, N) : trois passes tiennent chacune sous le plafond de 10 min. `--fichier=` pour une autre version.
"""
import sys, collections; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
ARG = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
F = ARG.get('fichier', 'app.html'); PARTIE = ARG.get('partie', 'tous'); ETATS = {'tous': ('tom', '200')}.get(ARG.get('etat', 'tous'), (ARG.get('etat'),))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True); return ok

# ── la lecture des deux listes, sur leurs cartes rendues ──
LIRE = r"""(quoi)=>{
  const nk=(p)=>(p && p.nuee && typeof NUE!=='undefined' && NUE[p.nuee]) ? p.nuee : null;
  const ent=(p)=>{ const k=nk(p); return k ? 'n:'+k : 'p:'+p.id; };
  const range=(sel)=>[...document.querySelectorAll(sel)].sort((a,b)=>(a.offsetTop-b.offsetTop)||(a.offsetLeft-b.offsetLeft));
  if(quoi==='ix'){
    return range('#indexList .s4-carte').map(c=>{ const t=((c.querySelector('.s4-ti')||{}).textContent||'').replace(/\s+/g,' ').trim(), nat=c.getAttribute('data-nat')||'';
      const ks=Object.keys(NUE||{}).filter(k=>(NUE[k]||k)===t); if(ks.length && (nat==='nuee'||nat==='cercle'||!promises.some(p=>p.title===t))) return 'n:'+ks[0];
      const L=promises.filter(p=>!nk(p) && (p.title||'').replace(/\s+/g,' ').trim()===t);
      if(L.length===1) return 'p:'+L[0].id;
      const L2=promises.filter(p=>!nk(p) && t.length>4 && t.replace(/[…\.]+$/,'')!==t && (p.title||'').startsWith(t.replace(/[…\.]+$/,'').trim()));
      return L2.length===1 ? 'p:'+L2[0].id : ('?'+L.length+':'+t); });
  }
  if(quoi==='fil'){
    return range('#feedList .s4-carte').map(c=>{ const id=c.getAttribute('data-pid'); if(id==null) return 'x:'+(c.getAttribute('data-nuee')||'?');
      const p=promises.find(q=>q.id===+id); return p ? ('f:'+p.id+'>'+ent(p)) : ('f:'+id+'>perdue'); });
  }
  if(quoi==='attendu'){
    const ix=promises.filter(p=>!nk(p)).map(p=>'p:'+p.id).concat(Object.keys(NUE||{}).map(k=>'n:'+k));
    /* un événement d'une parole effacée reste au journal ; le Fil ne le montre pas (C-049) : il n'est pas attendu */
    const vit=(f)=>f.pid==null || promises.some(p=>p.id===f.pid), J=(window.FEED||[]).filter(vit);
    const fil={}; J.forEach(f=>{ if(f.pid==null) return; fil[f.pid]=(fil[f.pid]||0)+1; });
    return {ix:ix, fil:fil, n:J.length};
  }
}"""
OUVRE_IX = "()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); try{ setView('toile'); }catch(e){} window.ixFiltre='tous'; window.ixTri='recent'; openSheet(document.getElementById('indexSheet')); buildIndex(); }"
OUVRE_FIL = "()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); window.fdFiltre='tous'; try{ fdSortMode='recent'; }catch(e){} try{ fdQuery=''; }catch(e){} setView('fil'); buildFeed(); if(window._s4Fil) _s4Fil(); }"
FERME = "()=>{ try{ _peaufSortie(); }catch(e){} closeAll(); try{ setView('toile'); }catch(e){} }"
def lis(pg):
    pg.evaluate(OUVRE_IX); pg.wait_for_timeout(700); ix = pg.evaluate(LIRE, 'ix')
    pg.evaluate(OUVRE_FIL); pg.wait_for_timeout(700); fil = pg.evaluate(LIRE, 'fil')
    att = pg.evaluate(LIRE, 'attendu'); pg.evaluate(FERME); pg.wait_for_timeout(400)
    return ix, fil, att
def err(pg):
    """la vérification de version (v145) recharge une page dont le commit diffère du serveur (arbre modifié pendant un lot) : sa requête annulée remonte en
    « erreur de page » en WebKit — ce n'est pas une faute de la page (CLAUDE.md, v151), on l'écarte nommément"""
    return [e for e in pg.erreurs if 'version.json' not in e]
def ordre_fil(fil):
    vu, o = set(), []
    for c in fil:
        e = c.split('>', 1)[1] if '>' in c else c
        if e not in vu: vu.add(e); o.append(e)
    return o
def invariants(T, pg, ix, fil, att):
    dup = [k for k, n in collections.Counter(ix).items() if n > 1]; manque = sorted(set(att['ix']) - set(ix)); trop = sorted(set(ix) - set(att['ix']))
    ok1 = juge(T + ' I1 · l\'Index : chaque parole et chaque Cercle, une fois', not dup and not manque and not trop, ('doublons', dup[:4], 'perdues', manque[:4], 'en trop', trop[:4], len(ix), len(att['ix'])))
    cf = collections.Counter(int(c[2:].split('>')[0]) for c in fil if c.startswith('f:'))
    ecarts = {k: (cf.get(int(k), 0), n) for k, n in att['fil'].items() if cf.get(int(k), 0) != n}
    ecarts.update({k: (n, att['fil'].get(str(k), 0)) for k, n in cf.items() if str(k) not in att['fil']})
    perdus = [c for c in fil if c.endswith('>perdue') or c.startswith('x:')]
    ok2 = juge(T + ' I2 · le Fil : autant de cartes par parole que le journal', not ecarts and not perdus and len(fil) == att['n'], (len(fil), att['n'], 'écarts (cartes, journal)', dict(list(ecarts.items())[:4]), perdus[:3]))
    of = ordre_fil(fil); pos = {e: i for i, e in enumerate(ix)}; seq = [pos.get(e, -1) for e in of]
    casse = [(of[i - 1], of[i]) for i in range(1, len(seq)) if seq[i] < seq[i - 1]]
    ok3 = juge(T + ' I3 · le même ordre dans l\'Index et le Fil', not casse and -1 not in seq, ('inversions', len(casse), casse[:3], 'absentes de l\'Index', [e for e, s in zip(of, seq) if s < 0][:3]))
    ok4 = juge(T + ' I4 · aucune erreur de page', not err(pg), err(pg)[:2])
    return ok1 and ok2 and ok3 and ok4
def tete_fil(fil, e):
    """les cartes de l'entrée e sont toutes en tête du Fil (s'il en a)"""
    n = sum(1 for c in fil if c.endswith('>' + e))
    return n == 0 or all(c.endswith('>' + e) for c in fil[:n]), n
def ancienne(ix, sauf=()):
    for e in reversed(ix):
        if e.startswith('p:') and e not in sauf: return int(e[2:])
def fiche(pg, pid):
    pg.evaluate("id=>{ try{ _peaufSortie(); }catch(e){} closeAll(); openDetail(id); }", pid); pg.wait_for_timeout(2200)
def mot(pg, texte):
    B.tap_sel(pg, '#cm5Ligne'); pg.wait_for_timeout(800); pg.keyboard.type(texte, delay=15); pg.keyboard.press('Enter'); pg.wait_for_timeout(900)
def x_fiche(pg):
    for _ in range(3):   # « Un mot… » encore ouvert : le premier toucher du X le referme
        c = pg.evaluate("()=>{ const e=document.querySelector('#detailPoster .closeb'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]; }"); pg.mouse.click(c[0], c[1]); pg.wait_for_timeout(1700)
        if not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"): break
CARTE = """([liste, rang])=>{ const L=[...document.querySelectorAll(liste+' .s4-carte')].sort((a,b)=>(a.offsetTop-b.offsetTop)||(a.offsetLeft-b.offsetLeft)); const c=L[rang]; if(!c) return null;
  const r=c.getBoundingClientRect(), s=document.querySelector(liste).getBoundingClientRect(); if(r.top<s.top+8||r.bottom>s.bottom-8) c.scrollIntoView({block:'center'}); return true; }"""
POINT = """([liste, rang])=>{ const L=[...document.querySelectorAll(liste+' .s4-carte')].sort((a,b)=>(a.offsetTop-b.offsetTop)||(a.offsetLeft-b.offsetLeft)); const c=L[rang]; const r=c.getBoundingClientRect();
  return [r.left+r.width*0.62, r.top+r.height*0.55, document.querySelector(liste).scrollTop]; }"""
def touche(pg, liste, rang):
    """la souris : elle porte des évènements de pointeur, que la pile de C-193 lit à `pointerdown` (un toucher du banc WebKit n'en porte pas)"""
    if not pg.evaluate(CARTE, [liste, rang]): return None, None
    pg.wait_for_timeout(500); x, y, st = pg.evaluate(POINT, [liste, rang]); pg.mouse.click(x, y); pg.wait_for_timeout(2600)
    return pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); if(!d.classList.contains('show')) return null; return (typeof curNuee!=='undefined' && curNuee && (!cur || d.classList.contains('dp-mode-nuee'))) ? 'n:'+curNuee : (cur ? cur.id : null); }"), st

def onglet(pg, q):
    """un second onglet ouvert PAR l'app (`window.open`) : il hérite du `sessionStorage` de la page — sans cela le script d'amorce du banc réécrirait le stockage
    avec l'état de départ, et le second onglet jugerait un autre état que le premier"""
    with pg.context.expect_page() as pi: pg.evaluate("q=>window.open(location.pathname+q)", q)
    g = pi.value; g.__dict__['erreurs'] = []; g.on('pageerror', lambda e: g.__dict__['erreurs'].append(str(e)[:200])); return g
def un_etat(nom, b):
    T = '[%s]' % nom
    if nom == 'tom':
        ctx, d = B.contexte_tom(b)
        if not ctx: juge(T + ' un état exporté existe', False); return
        print('  %s %s' % (T, d.get('_fichier')), flush=True)
    else:
        ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, nom)
    pg = B.ouvre(ctx, F, 9000); pg.wait_for_timeout(2000)
    ix, fil, att = lis(pg); print('  %s Index %d · Fil %d · journal %d' % (T, len(ix), len(fil), att['n']), flush=True)
    invariants(T + ' 0 ·', pg, ix, fil, att)
    def apres(lettre, nomcas, e_tete, second=None):
        ix, fil, att = lis(pg); ok_ix = ix and ix[0] == e_tete and (second is None or (len(ix) > 1 and ix[1] == second)); ok_f, n = tete_fil(fil, e_tete)
        juge('%s %s · %s : en tête de l\'Index%s' % (T, lettre, nomcas, ' (puis la première)' if second else ''), ok_ix, (e_tete, second, ix[:3]))
        juge('%s %s · … et ses cartes en tête du Fil (%d)' % (T, lettre, n), ok_f, fil[:3])
        invariants('%s %s ·' % (T, lettre), pg, ix, fil, att); return ix, fil
    if PARTIE in ('1', 'tous'):
        # A · un mot
        q = ancienne(ix); fiche(pg, q); mot(pg, "j'y pense"); pg.evaluate(FERME); pg.wait_for_timeout(500)
        ix, fil = apres('A', 'un mot sur la parole la plus basse', 'p:%d' % q)
        # B · tenir (le sélecteur d'état : le seul chemin du trait)
        q = ancienne(ix); fiche(pg, q)
        t = pg.evaluate("()=>{ const b=document.querySelector('#segStatus button[data-st=\"tenu\"]'); if(!b||!cur) return false; if(cur.status==='tenu') return 'deja'; b.click(); return cur.status; }")
        pg.wait_for_timeout(1500); pg.evaluate(FERME); pg.wait_for_timeout(500)
        if t == 'deja':
            pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); p.status='encours'; saveState(true); }", q); fiche(pg, q); pg.evaluate("()=>document.querySelector('#segStatus button[data-st=\"tenu\"]').click()"); pg.wait_for_timeout(1500); pg.evaluate(FERME)
        ix, fil = apres('B', 'tenir', 'p:%d' % q)
        # C · Peaufiner : l'échéance
        q = ancienne(ix); pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); p.dueISO='2026-12-24'; p.due=47; saveState(true); }", q); pg.wait_for_timeout(600)
        ix, fil = apres('C', 'Peaufiner (l\'échéance)', 'p:%d' % q)
        # D · planter
        B.plante(pg, 'vider la cave 183'); pg.wait_for_timeout(1200)
        nid = pg.evaluate("()=>{ const l=promises.filter(p=>p.title==='vider la cave 183'); return l.length?l[l.length-1].id:null; }")
        ix, fil = apres('D', 'planter', 'p:%s' % nid)
        # E · effacer
        q = ancienne(ix); fiche(pg, q)
        pg.evaluate("()=>window._v16SupprimerPromi(cur)"); pg.wait_for_timeout(700); B.tap_sel(pg, '.v16-oui'); pg.wait_for_timeout(1800)   # la vraie suppression : la feuille, « Supprimer »
        ix, fil, att = lis(pg)
        juge(T + ' E · effacer : la parole n\'est plus ni dans l\'Index ni dans le Fil', 'p:%d' % q not in ix and not any(c.startswith('f:%d>' % q) for c in fil), (q, [c for c in fil if c.startswith('f:%d>' % q)][:2]))
        invariants(T + ' E ·', pg, ix, fil, att)
        # F · une parole d'un Cercle
        k = next((e[2:] for e in reversed(ix) if e.startswith('n:')), None)
        qc = pg.evaluate("k=>{ const l=promises.filter(p=>p.nuee===k && !p.draft); return l.length?l[0].id:null; }", k) if k else None
        if qc:
            fiche(pg, qc); mot(pg, 'on s\'y met samedi'); pg.evaluate(FERME); pg.wait_for_timeout(500)
            ix, fil = apres('F', 'un mot sur une parole du Cercle « %s »' % k, 'n:' + k)
        else: print('  ·  %s F · sans objet : cet état ne porte aucun Cercle' % T, flush=True)
        # G · deux actions rapides
        q1 = ancienne(ix); q2 = ancienne(ix, ('p:%d' % q1,))
        pg.evaluate("""([a,b])=>new Promise(r=>{ const pa=promises.find(x=>x.id===a), pb=promises.find(x=>x.id===b);
          (pa.comments=pa.comments||[]).push({by:'moi', t:'vite', d:new Date().toISOString()}); saveState(true);
          setTimeout(()=>{ (pb.comments=pb.comments||[]).push({by:'moi', t:'vite aussi', d:new Date().toISOString()}); saveState(true); r(); }, 120); })""", [q1, q2]); pg.wait_for_timeout(700)
        ix, fil = apres('G', 'deux actions à 120 ms', 'p:%d' % q2, 'p:%d' % q1)
        # H · recharger
        pg.evaluate("()=>saveState(true)"); pg.wait_for_timeout(400); avant = (ix, ordre_fil(fil))
        pg.reload(); pg.wait_for_timeout(9000); ix, fil, att = lis(pg)
        juge(T + ' H · recharger : l\'Index dans le même ordre', ix == avant[0], (ix[:4], avant[0][:4]))
        juge(T + ' H · … et le Fil', ordre_fil(fil) == avant[1], (ordre_fil(fil)[:4], avant[1][:4]))
        invariants(T + ' H ·', pg, ix, fil, att)
    if PARTIE in ('2', 'tous'):
        # J · un second onglet
        pg2 = onglet(pg, ''); pg2.wait_for_timeout(4000)   # une action rapide : 4 s après l'ouverture de l'onglet, par la vraie saisie
        q = ancienne(ix); fiche(pg2, q); mot(pg2, "depuis l'autre onglet")
        pg2.wait_for_timeout(800); pg2.close(); pg.bring_to_front()
        pg.evaluate("()=>{ document.dispatchEvent(new Event('visibilitychange')); window.dispatchEvent(new Event('pageshow')); }"); pg.wait_for_timeout(9000)
        ix, fil = apres('J', 'une action dans un second onglet', 'p:%d' % q)
        # J2 · un onglet DÉPASSÉ qui agit (il vient de se recharger : il ne peut pas se recharger de nouveau avant 5 s) — rien n'est perdu
        pg2 = onglet(pg, ''); pg2.wait_for_timeout(5000); ix, fil, att = lis(pg)
        qa = ancienne(ix); qb = ancienne(ix, ('p:%d' % qa,))
        pg.evaluate("()=>sessionStorage.setItem('promi_relu', Date.now())")
        pg2.evaluate("id=>{ const p=promises.find(x=>x.id===id); (p.comments=p.comments||[]).push({by:'moi', t:'onglet deux', d:new Date().toISOString()}); saveState(true); }", qa); pg2.wait_for_timeout(600)
        pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); (p.comments=p.comments||[]).push({by:'moi', t:'onglet un', d:new Date(Date.now()+5).toISOString()}); saveState(true); }", qb); pg.wait_for_timeout(600)
        lu = pg2.evaluate("([a,b])=>{ const S=JSON.parse(localStorage.getItem('promi_state')); const c=id=>((S.promises.find(x=>x.id===id)||{}).comments||[]).map(z=>z.t); return [c(a), c(b)]; }", [qa, qb])
        juge(T + ' J2 · un onglet dépassé qui agit : son mot ET celui de l\'autre onglet sont gardés', 'onglet deux' in lu[0] and 'onglet un' in lu[1], (qa, qb, lu))
        pg2.close(); pg.bring_to_front(); pg.reload(); pg.wait_for_timeout(9000); ix, fil, att = lis(pg)
        juge(T + ' J2 · … rechargé, la dernière action (onglet un) est en tête', ix and ix[0] == 'p:%d' % qb and ix[1] == 'p:%d' % qa, (qb, qa, ix[:3]))
        invariants(T + ' J2 ·', pg, ix, fil, att)
        # K · ?jour=+30
        ref = (ix, ordre_fil(fil)); pg3 = pg; ad = pg.url; pg.goto(ad.split('?')[0] + '?jour=+30'); pg.wait_for_timeout(9000); ix3, fil3, att3 = lis(pg3)   # le même onglet (un second fausserait la mesure : il se recharge sur l'écriture de l'autre)
        juge(T + ' K · ?jour=+30 : l\'Index dans le même ordre', ix3 == ref[0], (ix3[:4], ref[0][:4]))
        juge(T + ' K · … et le Fil', ordre_fil(fil3) == ref[1], (ordre_fil(fil3)[:4], ref[1][:4]))
        invariants(T + ' K ·', pg3, ix3, fil3, att3)
        pg.goto(ad.split('?')[0]); pg.wait_for_timeout(9000)   # l'onglet `?jour=+30` a écrit ses jours recomptés : l'onglet un est dépassé ; on repart d'un seul onglet, comme sur l'iPhone
        # L · un tri, puis retiré
        ix, fil, att = lis(pg); ref = (ix, ordre_fil(fil))
        pg.evaluate("()=>{ window.ixTri='personne'; openSheet(document.getElementById('indexSheet')); buildIndex(); }"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{ try{ fdSortMode='personne'; }catch(e){} setView('fil'); buildFeed(); _s4Fil(); }"); pg.wait_for_timeout(600)
        ix, fil, att = lis(pg)
        juge(T + ' L · un tri actif puis retiré : l\'Index d\'avant', ix == ref[0], (ix[:4], ref[0][:4]))
        juge(T + ' L · … et le Fil d\'avant', ordre_fil(fil) == ref[1], (ordre_fil(fil)[:4], ref[1][:4]))
    if PARTIE in ('3', 'tous'):
        # M · le Fil resté ouvert sous une fiche
        pg.evaluate(FERME); pg.wait_for_timeout(500); B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2400)
        fil = pg.evaluate(LIRE, 'fil'); rang = next((i for i in range(len(fil) - 1, -1, -1) if fil[i].startswith('f:') and '>p:' in fil[i]), None)
        pid = int(fil[rang][2:].split('>')[0]); ouv, _ = touche(pg, '#feedList', rang)
        juge(T + ' M · une carte du bas du Fil ouvre SA fiche', ouv == pid, (pid, ouv))
        mot(pg, 'je reviens dessus'); x_fiche(pg); pg.wait_for_timeout(1800)
        vu = pg.evaluate("()=>document.getElementById('feedView').classList.contains('in')"); fil = pg.evaluate(LIRE, 'fil')
        ok_f, n = tete_fil(fil, 'p:%d' % pid)
        juge(T + ' M · le X ramène au Fil, la parole en tête, sans doublon', vu and ok_f and fil and fil[0].endswith('>p:%d' % pid) and len(fil) == pg.evaluate(LIRE, 'attendu')['n'], (vu, fil[:3]))
        # N · carte → fiche → retour, au même défilement (le Fil, puis l'Index)
        for liste, porte, vue in (('#feedList', '#filBtn', "document.getElementById('feedView').classList.contains('in')"), ('#indexList', '#indexBtn', "document.getElementById('indexSheet').classList.contains('show')")):
            pg.evaluate(FERME); pg.wait_for_timeout(500); B.tap_sel(pg, porte); pg.wait_for_timeout(2400)
            lu = pg.evaluate(LIRE, 'fil' if liste == '#feedList' else 'ix'); avant_o = list(lu)
            rang = min(len(lu) - 1, max(2, len(lu) // 2))
            pg.evaluate("s=>{ const e=document.querySelector(s); e.scrollTop=Math.min(e.scrollHeight-e.clientHeight, e.scrollHeight*0.4); e.dispatchEvent(new Event('scroll')); }", liste); pg.wait_for_timeout(500)
            attendu = lu[rang].split('>', 1)[1] if liste == '#feedList' else lu[rang]
            ouv, st0 = touche(pg, liste, rang)
            ouv_e = ouv if isinstance(ouv, str) else ('p:%s' % ouv)
            if liste == '#feedList' and attendu.startswith('n:'): ok_o = ouv_e == 'p:' + lu[rang][2:].split('>')[0] or ouv_e == attendu   # une carte du Fil d'une parole d'un Cercle ouvre la parole
            else: ok_o = ouv_e == attendu
            juge('%s N · %s : la carte touchée ouvre SA fiche' % (T, 'le Fil' if liste == '#feedList' else 'l\'Index'), ok_o, (rang, lu[rang], ouv))
            x_fiche(pg); pg.wait_for_timeout(1200)
            r = pg.evaluate("([s,v])=>[eval(v), document.querySelector(s).scrollTop]", [liste, vue]); apres_o = pg.evaluate(LIRE, 'fil' if liste == '#feedList' else 'ix')
            juge('%s N · … le X ramène %s, au même défilement, dans le même ordre' % (T, 'au Fil' if liste == '#feedList' else 'à l\'Index'), r[0] and abs(r[1] - st0) <= 4 and apres_o == avant_o, (r, round(st0, 1), apres_o == avant_o))
    juge(T + ' aucune erreur de page sur tout le parcours', not err(pg), err(pg)[:2])
    ctx.close()

if __name__ == '__main__':
  with sync_playwright() as p:
    b = p.webkit.launch()
    for e in ETATS: un_etat(e, b)
    b.close()
  print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
