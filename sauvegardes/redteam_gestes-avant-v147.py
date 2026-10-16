#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_gestes.py — LA MAIN FANTÔME NE PARAÎT QUE SUR UNE FICHE À TENIR (v144, Tom, 12 oct. 2026, C-110). RÉÉCRIT.

« Tom ne veut la main nulle part ailleurs que sur une fiche à tenir (Promi ou Chiche), pour le geste de tenir. Retire-la partout ailleurs,
  définitivement : Studio, Aura, page +, Fil, Partager, mode dessin, bande. Retire aussi ces gestes de l'inventaire. Sur la fiche, elle
  paraît 3 s après l'ouverture. Juge : la main n'apparaît sur aucun autre écran. »
Par banc_tom (WebKit, 390 × 844, @3x, vrai toucher, Toile vide, paroles plantées par l'app), tous les drapeaux `geste_vu_*` ABSENTS :
  A · l'inventaire ne porte que `tenir` et `chiche` ; le délai déclaré vaut 3 000 ms (valeurs décidées, en dur ici) ;
  B · sur la fiche d'un Promi à tenir puis d'un Chiche à tenir, ouvertes en touchant leur dalle : aucune main à 2,5 s du toucher, la main entre
      2,8 et 3,6 s ; elle est opaque, sans fondu (A2), porte `data-eng`, et part au premier toucher ;
  C · sur aucun autre écran, six secondes sans toucher chacun : l'accueil, le Studio, l'Aura, la page + (phrase remplie), le Fil, l'Index,
      Partager, les Réglages, une fiche tenue, le Peaufiner d'une fiche, le mode dessin, une fiche portant un dessin posé (la bande), l'onboarding
      (le trait).
Original (E1, 132 contrôles, dix gestes branchés) : sauvegardes/redteam_gestes-avant-v144.py. Rouge sur v143 (`zz-av144.html` : la main
paraît à 1,5 s, et sur la page +, l'Aura, le Studio…).
"""
import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
FICHIER = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
INVENTAIRE_DECIDE, DELAI_DECIDE = ['tenir', 'chiche'], 3000
OU = open('redteam_deplace.py', encoding='utf-8').read().split('OU = """')[1].split('"""')[0]
MAIN = "()=>{ const c=document.getElementById('gesteFantome'); const m=c&&c.querySelector('[data-main]'); if(!m) return null; const r=m.getBoundingClientRect(); if(r.width<2) return null; let o=1,e=m; while(e&&e.nodeType===1){ o*=parseFloat(getComputedStyle(e).opacity); e=e.parentElement; } const cs=getComputedStyle(m), cc=getComputedStyle(c); return {id:c.getAttribute('data-geste'), eng:!!c.getAttribute('data-eng')||c.hasAttribute('data-eng'), op:o, anim:cs.animationName+'|'+cc.animationName, trans:parseFloat(cs.transitionDuration)||0}; }"
ok = 0; ko = []
def juge(nom, cond, detail=''):
    global ok
    if cond: ok += 1
    else: ko.append(nom)
    print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
def guette(pg, ms):
    """la main, relevée toutes les 100 ms pendant ms : [(instant, état)] des relevés où elle est là"""
    L = []; n = int(ms / 100)
    for i in range(n):
        m = pg.evaluate(MAIN)
        if m: L.append((i * 100, m))
        pg.wait_for_timeout(100)
    return L
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b, gestes_vus=False); pg = B.ouvre(ctx, FICHIER)
    inv = pg.evaluate("()=>GesteFantome.inventaire().map(g=>g.id+(g.branche?'':'(non branché)'))"); regle = pg.evaluate("()=>GesteFantome.regle")
    juge('A · l\'inventaire ne porte que tenir et chiche', inv == INVENTAIRE_DECIDE, str(inv))
    juge('A · le délai déclaré sur une fiche vaut %d ms' % DELAI_DECIDE, regle.get('INACTIF_FICHE') == DELAI_DECIDE, str(regle.get('INACTIF_FICHE')))
    B.plante(pg, 'rendre le livre'); B.plante(pg, 'oser le plongeoir', nature=1); pg.wait_for_timeout(1500)
    ids = pg.evaluate("()=>promises.map(q=>[q.id,!!q.chiche])")
    for pid, chiche in ids:
        nom = 'Chiche' if chiche else 'Promi'
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(900)
        G = pg.evaluate(OU); g = G.get(str(pid))
        if not g: juge('B · [%s] sa dalle est sur la Toile' % nom, False); continue
        B.tap(pg, g[0], g[1])
        import time; t0 = time.time(); vue = None; avant = False
        while time.time() - t0 < 5.2:
            m = pg.evaluate(MAIN); t = time.time() - t0
            if m and vue is None: vue = (t, m)
            if m and t < 2.5: avant = True
            pg.wait_for_timeout(60)
        fiche = pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')")
        juge('B · [%s] la fiche à tenir est ouverte par sa dalle' % nom, fiche)
        juge('B · [%s] aucune main dans les 2,5 s qui suivent le toucher' % nom, not avant)
        juge('B · [%s] la main paraît 3 s après l\'ouverture (2,8 à 3,6 s)' % nom, vue is not None and 2.8 <= vue[0] <= 3.6, 'vue à %.2f s' % vue[0] if vue else 'jamais vue')
        if vue:
            m = vue[1]
            juge('B · [%s] c\'est le geste de tenir (%s)' % (nom, 'chiche' if chiche else 'tenir'), m['id'] == ('chiche' if chiche else 'tenir'), m['id'])
            juge('B · [%s] A2 : opaque, sans fondu ni animation, porte data-eng' % nom, m['op'] >= 0.999 and m['trans'] == 0 and m['anim'].replace('none', '').strip('|') == '' and m['eng'], str(m))
        d = B.dev(pg); pg.touchscreen.tap(d[0] + d[2] * 0.5, d[1] + d[3] * 0.62); pg.wait_for_timeout(250)
        juge('B · [%s] elle part au premier toucher' % nom, pg.evaluate(MAIN) is None)
    # C · aucun autre écran
    def ecran(nom, ouvre, attente=900, dur=6000):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} try{ ['settingsScreen','shareScreen','studioScreen','auraScreen'].forEach(i=>{ const s=document.getElementById(i); if(s&&i==='settingsScreen') s.classList.remove('show'); }); }catch(e){} try{ Object.keys(localStorage).forEach(k=>{ if(k.indexOf('geste_vu_')===0) localStorage.removeItem(k); }); GesteFantome.oublierTout(); }catch(e){} }"); pg.wait_for_timeout(500)
        try: ouvre()
        except Exception as e: juge('C · [%s] ouvert' % nom, False, str(e)[:80]); return
        pg.wait_for_timeout(attente); L = guette(pg, dur)
        juge('C · [%s] aucune main en %d s sans toucher' % (nom, dur // 1000), not L, ('main « %s » à %d ms' % (L[0][1]['id'], L[0][0])) if L else '')
    ev = lambda s: (lambda: pg.evaluate(s))
    pid0 = ids[0][0]
    def fiche_devant():
        if not pg.evaluate("()=>{ const dp=document.getElementById('detailPoster'), d=document.getElementById('device').getBoundingClientRect(), e=document.elementFromPoint(d.left+d.width/2, d.top+d.height*0.55); return dp.classList.contains('show') && !!e && dp.contains(e); }"): raise Exception('la fiche n\'est pas devant')
    def peaufiner():
        G = pg.evaluate(OU); g = G.get(str(pid0)); B.tap(pg, g[0], g[1]); pg.wait_for_timeout(1100); B.tap(pg, 150, 790); pg.wait_for_timeout(1100)
        if not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('s2-ouv')"): raise Exception('Peaufiner non ouvert')
    def dessin():
        pg.evaluate("()=>{ openDetail(%d); setTimeout(()=>{ try{ window._dessin.ouvre(); }catch(e){} },700); }" % pid0); pg.wait_for_timeout(1800)
        if not pg.evaluate("()=>!!document.getElementById('dessinMode')"): raise Exception('mode dessin non ouvert')
    def tenue(): pg.evaluate("()=>{ const q=promises.find(x=>x.id===%d); q.status='tenu'; q.doneAt=Date.now(); try{syncAll()}catch(e){} openDetail(%d); }" % (pid0, pid0)); pg.wait_for_timeout(900); fiche_devant()
    def bande(): pg.evaluate("()=>{ const q=promises.find(x=>x.id===%d); q.dessin={fond:'#82AEF8',traits:[],poses:[{c:'#201908',t:6,g:0,pts:[[60,60,1],[200,160,1]]}],pose:true,masque:false}; try{syncAll()}catch(e){} openDetail(%d); }" % (pid0, pid0)); pg.wait_for_timeout(900); fiche_devant()
    def page_plus():
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(700)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1600)
        pg.evaluate("()=>{ const f=document.getElementById('fTitle'); f.value='courir dimanche'; f.dispatchEvent(new Event('input',{bubbles:true})); try{ window._phrase.titre='courir dimanche'; }catch(e){} }")
    ecran('accueil', ev("()=>0"))
    ecran('Peaufiner d\'une fiche', peaufiner, attente=300)
    ecran('mode dessin', dessin, attente=300)
    ecran('fiche tenue', tenue, attente=300)
    ecran('fiche tenue portant un dessin (la bande)', bande, attente=300)
    ecran('page +, phrase remplie', page_plus)
    ecran('Fil', ev("()=>document.getElementById('filBtn').click()"), attente=1500)
    ecran('Index', ev("()=>document.getElementById('indexBtn').click()"), attente=1500)
    ecran('Réglages', ev("()=>{ const s=document.getElementById('settingsScreen'); if(window.openSettings) openSettings(); else s.classList.add('show'); }"), attente=1200)
    ecran('Aura', ev("()=>document.getElementById('souffleBtn').click()"), attente=3500)
    ecran('Partager', ev("()=>{ const e=document.getElementById('shareBtn')||document.querySelector('#device .acc-plat [aria-label*=\"artager\"]'); if(e) e.click(); else if(window.openShare) openShare(); }"), attente=3500)
    ecran('Studio', ev("()=>document.getElementById('studioBtn').click()"), attente=3500)
    etats = pg.evaluate("()=>({dessin:!!document.getElementById('dessinMode'), err:(window.__err||null)})")
    ctx.close()
    # l'onboarding, jusqu'au trait (stockage vierge)
    ctx = B.contexte(b, gestes_vus=False, onb=False, guide=False); pg = B.ouvre(ctx, FICHIER, attente=5000)
    c = pg.evaluate("()=>{const e=document.getElementById('onbPh'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
    if c:
        pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(400); pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(300); pg.keyboard.press('Enter'); pg.wait_for_timeout(1000)
        pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(1200)
    L = guette(pg, 6000); et = pg.evaluate("()=>({onb:document.getElementById('device').classList.contains('onb-actif'), trait:!!(document.getElementById('onbTrait')&&document.getElementById('onbTrait').getBoundingClientRect().width>10)})")
    juge('C · [onboarding, le trait] aucune main en 6 s sans toucher', not L and et['onb'] and et['trait'], ('main « %s »' % L[0][1]['id']) if L else str(et))
    b.close()
print('\n%d / %d' % (ok, ok + len(ko)))
if ko: print('KO :', ' · '.join(ko[:10]))
sys.exit(1 if ko else 0)
