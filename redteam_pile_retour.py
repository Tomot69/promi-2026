#!/usr/bin/env python3
"""redteam_pile_retour.py — ⚑ v163b (Tom, C-193 ; AUDIT-BOUTONS, point 5) : FERMER RAMÈNE D'OÙ L'ON VIENT.

(« redteam_retour » est déjà le juge du retour exact de la vie au repos, C-028 : celui-ci s'appelle « pile_retour ».)
« Une seule pile d'écrans, hors du moteur. Le X de Peaufiner ferme seulement Peaufiner (C-134). Un gardé de côté rouvert depuis l'Index revient à l'Index
au X, et ses drapeaux de reprise sont remis à zéro à la fermeture. Juge : chaque chemin du point 5 de l'audit. »
Banc comme Tom (WebKit ×3, doigt), Toile de 10 paroles, un Cercle ; chaque chemin joué au DOIGT, le X touché, puis on lit l'écran qu'on voit (sous le centre) :
  1 · Index → fiche → X → l'Index (à son défilement) ;   2 · Fil → fiche → X → le Fil ;   3 · fiche d'une personne → fiche → X → la personne ;
  4 · fiche d'un Cercle → une carte de son fil → X → le Cercle ;   5 · Réglages → Vie privée → X → les Réglages ;   6 · Réglages → Ma Parole ! → X → les Réglages ;
  7 · Aura → « Partager ma Pelote » → X → l'Aura ;   8 · le X de Peaufiner : Peaufiner se ferme, la fiche reste ;
  9 · Index → un gardé de côté → X → l'Index, et ses drapeaux de reprise à zéro ;   10 · depuis l'accueil, une fiche → X → l'accueil (rien à rendre).
Preuve : `--fichier=zz-v162.html` rougit (1 à 9).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-92s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)
VU = """()=>{ const d=document.getElementById('device'), r=d.getBoundingClientRect(), k=r.width/390, e=document.elementFromPoint(r.left+195*k, r.top+422*k);
  const s=e && e.closest ? e.closest('#personSheet, #detailPoster, #createSheet, #indexSheet, #feedView, #settingsScreen, #auraScreen, #shareScreen, #plusScreen, #privScreen, .screen, .sheet, .poster') : null;
  return s ? s.id : 'accueil'; }"""
def c_(pg, sel, scroll=True):
    # le point du doigt : l'élément amené à l'écran, la page laissée se poser (un fil qui défile change de géométrie), puis un point où il est VRAIMENT sous le doigt
    if scroll: pg.evaluate("s=>{ const e=document.querySelector(s); if(e) e.scrollIntoView({block:'center'}); }", sel); pg.wait_for_timeout(900)
    return pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!r.width) return null; const cx=r.left+r.width/2; for(let y=r.top+r.height/2, i=0; i<40; i++, y+=(i%2?-1:1)*i*3){ if(y<r.top||y>r.bottom) continue; const h=document.elementFromPoint(cx, y); if(h && (h===e || e.contains(h))) return [(cx-D.left)/k, (y-D.top)/k]; } return null; }", sel)
def touche(pg, sel, attente=2400, scroll=True):
    c = c_(pg, sel, scroll)
    if c: B.tap(pg, c[0], c[1]); pg.wait_for_timeout(attente)
    return c is not None
def x_de(pg, ecran):
    return touche(pg, '#%s > .closeb, #%s .closeb[data-close], #%s [data-close]' % (ecran, ecran, ecran), 2600, False)
def accueil(pg):
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); try{ quitteVues(); }catch(e){} ['settingsScreen','auraScreen','shareScreen','plusScreen','privScreen','studioScreen'].forEach(i=>{ const e=document.getElementById(i); if(e) e.classList.remove('show'); }); }"); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    pg.evaluate("()=>{ const k='jardin'; NUE[k]='Les jardiniers'; NUEEMEM[k]=['Marion','Rachel']; NUECREATOR[k]='moi'; promises.filter(q=>!q.draft && !q.chiche).slice(0,2).forEach(q=>{ q.nuee=k; }); const d=promises.filter(q=>!q.draft)[5]; d.draft=true; d.brouillon={nat:'promi'}; saveState(); syncAll(); }")
    pg.wait_for_timeout(800)
    # 1 · Index → fiche → X
    B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2500)
    touche(pg, '#indexList .s4-carte[data-etat=encours]'); v1 = pg.evaluate(VU); x_de(pg, 'detailPoster'); v2 = pg.evaluate(VU)
    juge('1 · Index → fiche → X → l\'Index', v1 == 'detailPoster' and v2 == 'indexSheet', '%s → %s' % (v1, v2))
    # 9 · Index → gardé de côté → X
    touche(pg, '#indexList .s4-carte[data-etat=garde]', 3000); v1 = pg.evaluate(VU); fl1 = pg.evaluate("()=>[window._brouillonRepris, window._ppGarde]")
    x_de(pg, 'createSheet'); v2 = pg.evaluate(VU); fl2 = pg.evaluate("()=>[window._brouillonRepris, window._ppGarde]")
    juge('9 · Index → un gardé de côté → X → l\'Index, ses drapeaux à zéro', v1 == 'createSheet' and v2 == 'indexSheet' and fl1[0] is not None and fl2[0] is None and not fl2[1], '%s → %s · drapeaux %s → %s' % (v1, v2, fl1, fl2))
    accueil(pg)
    # 2 · Fil → fiche → X
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600)
    touche(pg, '#feedView .s4-carte'); v1 = pg.evaluate(VU); x_de(pg, 'detailPoster'); v2 = pg.evaluate(VU)
    juge('2 · Fil → fiche → X → le Fil', v1 == 'detailPoster' and v2 == 'feedView', '%s → %s' % (v1, v2))
    accueil(pg)
    # 3 · personne → fiche → X
    nom = pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.who && q.who!=='moi' && q.who!=='le groupe'); return p.who; }")
    pg.evaluate("n=>openPerson(n)", nom); pg.wait_for_timeout(2400); pg.evaluate("n=>{ window.__pileNom=n; }", nom)
    touche(pg, '#personSheet .ps-c'); v1 = pg.evaluate(VU); x_de(pg, 'detailPoster'); v2 = pg.evaluate(VU)
    juge('3 · fiche d\'une personne → fiche → X → la personne', v1 == 'detailPoster' and v2 == 'personSheet', '%s → %s (%s)' % (v1, v2, nom))
    accueil(pg)
    # 4 · Cercle → carte du fil → X
    pg.evaluate("()=>openNueeDetail('jardin')"); pg.wait_for_timeout(2600)
    NU = "()=>{ const dp=document.getElementById('detailPoster'); return [dp.classList.contains('show'), dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'), cur?cur.title:null, typeof curNuee!=='undefined'?curNuee:null]; }"
    touche(pg, '#dpNueeFil .nf-item'); v1 = pg.evaluate(NU); x_de(pg, 'detailPoster'); v2 = pg.evaluate(NU)
    juge('4 · Cercle → une carte de son fil → X → le Cercle', v1[0] and not v1[1] and v1[2] and v2[0] and v2[1] and v2[3] == 'jardin', 'fiche (montrée, Cercle, parole, clé) %s → %s' % (v1, v2))
    accueil(pg)
    # 5 · Réglages → Vie privée → X ; 6 · Réglages → Ma Parole ! → X
    for n_, sel, ecran in (('5 · Réglages → Vie privée → X → les Réglages', '#privCard', 'privScreen'), ('6 · Réglages → Ma Parole ! → X → les Réglages', '#openPlusTop', 'plusScreen')):
        B.tap_sel(pg, '#settingsBtn'); pg.wait_for_timeout(1800)
        touche(pg, sel, 2200); v1 = pg.evaluate(VU); x_de(pg, ecran); v2 = pg.evaluate(VU)
        juge(n_, v1 == ecran and v2 == 'settingsScreen', '%s → %s' % (v1, v2)); accueil(pg)
    # 7 · Aura → Partager ma Pelote → X
    B.tap_sel(pg, '#souffleBtn'); pg.wait_for_timeout(2800)
    touche(pg, '#auPartage', 2800); v1 = pg.evaluate(VU); x_de(pg, 'shareScreen'); v2 = pg.evaluate(VU)
    juge('7 · Aura → « Partager ma Pelote » → X → l\'Aura', v1 == 'shareScreen' and v2 == 'auraScreen', '%s → %s' % (v1, v2))
    accueil(pg)
    # 8 · le X de Peaufiner
    pid = pg.evaluate("()=>promises.find(q=>!q.draft && !q.nuee && q.status!=='tenu').id")
    pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2400); B.tap_sel(pg, '#dpdTog'); pg.wait_for_timeout(1300)
    o1 = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('s2-ouv')")
    touche(pg, '#detailPoster .s2-fermer', 1500, False)
    o2 = pg.evaluate("()=>[document.getElementById('detailPoster').classList.contains('s2-ouv'), document.getElementById('detailPoster').classList.contains('show')]")
    juge('8 · le X de Peaufiner : Peaufiner se ferme, la fiche reste', o1 and not o2[0] and o2[1], '%s → %s' % (o1, o2))
    accueil(pg)
    # 10 · depuis l'accueil
    cel = pg.evaluate("i=>{ const a=Toile.dalleAbs&&Toile.dalleAbs(i); return a; }", pid)
    pg.evaluate("i=>openDetail(i)", pid); pg.wait_for_timeout(2400); x_de(pg, 'detailPoster'); v2 = pg.evaluate(VU)
    juge('10 · une fiche ouverte sans origine → X → l\'accueil', v2 == 'accueil', v2)
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('aucune erreur de page', False, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
