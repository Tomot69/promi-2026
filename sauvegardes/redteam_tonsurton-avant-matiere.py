#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_tonsurton.py — UN TRAIT NE DOIT JAMAIS ÊTRE À MOINS DE 42 DE SON CHAMP.

Le §2.1 bis le dit : le trait posé sur un champ plein porte la TEINTE CLAIRE de la nature,
jamais sa couleur pleine. Les cadres clairs du moodboard qui peignent le trait en couleur
pleine sont une **erreur de dessin** (décision Tom, 18 août 2026) : le trait y prend
exactement la couleur de l'aplat et disparaît.

On ne fait pas confiance aux constantes : **on lit les pixels peints**. Pour chaque trait du
produit — fiche, page +, carte d'Index, bandeau du Fil, l'instant — on relève la couleur du
champ en haut du cadre, puis la couleur de la ligne au centre de son épaisseur, et on
compare en luminosité. Seuil : **42** (§3).

Usage :  python3 redteam_tonsurton.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
SEUIL = 42
ok = [0]; ko = []

def t(nom, d, detail=''):
    if d is None:
        ko.append(nom); print('%-52s KO  %s' % (nom, detail or 'non mesurable')); return
    if d >= SEUIL: ok[0] += 1; print('%-52s OK  Δ%-4d %s' % (nom, d, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-52s KO  Δ%-4d TON SUR TON  %s' % (nom, d, detail))

# la sonde : on longe l'onde, on lit LE CENTRE de la ligne, on compare aux TROIS canaux
SONDE = r"""(a)=>{
  const cv=document.getElementById(a.cv); if(!cv) return null;
  const g=cv.getContext('2d'); const larg=parseFloat(cv.style.width);
  if(!larg) return null;
  const k=cv.width/larg;
  const lire=(x,y)=>{ if(x<0||y<0||x*k>=cv.width||y*k>=cv.height) return null;
    const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
    return d[3]>200 ? [d[0],d[1],d[2]] : null; };
  const lum=c=>0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
  const per=a.per||1.5, amp=a.amp, mont=amp*0.34, aa=amp*0.62, base=a.base, W=a.W||390;
  const y=x=>{const t=Math.min(1,Math.max(0,x/W));return base-mont*t-aa*Math.sin(2*Math.PI*per*t);};
  /* le champ : haut du cadre, loin de la dalle et de la ligne */
  const champ = lire(W*0.06, Math.max(2, base*0.06));
  if(!champ) return {champ:null};
  /* la ligne : on cherche, le long de l'onde, le pixel le plus ÉLOIGNÉ du champ —
     c'est lui, la ligne. On balaie l'épaisseur, pas seulement le centre. */
  let best=null, bd=-1;
  for(let x=W*0.08;x<W*0.92;x+=3){
    for(let dy=-6;dy<=6;dy+=1){
      const p=lire(x, y(x)+dy); if(!p) continue;
      const d=Math.abs(p[0]-champ[0])+Math.abs(p[1]-champ[1])+Math.abs(p[2]-champ[2]);
      if(d>bd){ bd=d; best=p; }
    }
  }
  if(!best) return {champ:champ, trait:null};
  return {champ:champ, trait:best,
          d:Math.round(Math.abs(lum(best)-lum(champ))),
          hexChamp:'#'+champ.map(v=>v.toString(16).padStart(2,'0')).join(''),
          hexTrait:'#'+best.map(v=>v.toString(16).padStart(2,'0')).join('')};}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    def mesure(cv, base, amp, per=1.5, W=390):
        return pg.evaluate(SONDE, {'cv':cv,'base':base,'amp':amp,'per':per,'W':W})

    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        print('\n══ thème %s ══' % th)

        # ── LES FICHES ──
        etats = pg.evaluate("""()=>({
          encours:(promises.filter(p=>!p.draft&&!p.req&&!p.chiche&&p.status==='encours')[0]||{}).id,
          atenir :(promises.filter(p=>!p.draft&&!p.req&&p.status==='rate')[0]||{}).id,
          tenue  :(promises.filter(p=>!p.draft&&p.status==='tenu')[0]||{}).id,
          chiche :(promises.filter(p=>p.chiche)[0]||{}).id})""")
        for nom, pid in etats.items():
            if pid is None: continue
            pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid); pg.wait_for_timeout(1400)
            e = pg.evaluate("""()=>{const dp=document.getElementById('detailPoster');
              const e=window._ficheEcran(dp,cur); return {base:e.base, amp:e.amp};}""")
            r = mesure('dpTrameCv', e['base'], e['amp'])
            t('fiche · %-9s [%s]' % (nom, th), r and r.get('d'),
              '%s sur %s' % (r.get('hexTrait'), r.get('hexChamp')) if r else '')

        # ── LA PAGE + ──
        for i, nat in ((0,'Promi'),(1,'Chiche'),(2,'Nuée')):
            pg.evaluate("()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();}")
            pg.wait_for_timeout(800)
            pg.evaluate("(i)=>{const x=[...document.querySelectorAll('#createSheet .tile')][i];if(x)x.click();}", i)
            pg.wait_for_timeout(1100)
            e = pg.evaluate("()=>{const e=window._ppEcran?window._ppEcran():null;return e?{base:e.base,amp:e.amp}:null;}")
            if not e: continue
            r = mesure('csTrameCv', e['base'], e['amp'])
            t('page + · %-8s [%s]' % (nat, th), r and r.get('d'),
              '%s sur %s' % (r.get('hexTrait'), r.get('hexChamp')) if r else '')

        # ── LES CARTES D'INDEX ──
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}"); pg.wait_for_timeout(1700)
        # ⚠ TOUT EN UNE SEULE PASSE. Poser un id sur un canevas puis le relire dans un
        #   second appel ne marche pas : l'Index se redessine entre les deux et le nœud
        #   n'existe plus. On sonde donc les cartes sans les marquer.
        pires = pg.evaluate("""()=>{const lum=c=>0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
          const out=[];
          [...document.querySelectorAll('#indexList .s4-carte')].slice(0,10).forEach(c=>{
            const cv=c.querySelector('canvas'); if(!cv) return;
            const W=parseFloat(cv.style.width), H=parseFloat(cv.style.height);
            if(!W||!H) return;
            const g=cv.getContext('2d'); const k=cv.width/W;
            const lire=(x,y)=>{ if(x<0||y<0||x*k>=cv.width||y*k>=cv.height) return null;
              const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
              return d[3]>200?[d[0],d[1],d[2]]:null;};
            /* ⚠ ON NE DEVINE PAS OÙ EST L'ONDE. La hauteur du canevas est celle de la CARTE,
               pas celle du champ : calculer `base = H − amp − 20` cherchait la ligne 60 px
               trop bas et ne trouvait rien. On cherche donc LA COULEUR DE LA LIGNE, qui est
               d'un jeu connu (§2.1 bis : terracotta, menthe, ou l'une des trois teintes
               claires), partout dans le canevas. */
            const TRAITS=[[240,122,46],[43,232,140],[203,170,255],[255,192,168],[208,176,255]];
            const champ=lire(W*0.06, 3); if(!champ) return;
            let best=null,bd=1e9;
            for(let x=2;x<W-2;x+=2) for(let yy=2;yy<H-2;yy+=2){
              const p=lire(x,yy); if(!p) continue;
              for(const T of TRAITS){
                const dd=Math.abs(p[0]-T[0])+Math.abs(p[1]-T[1])+Math.abs(p[2]-T[2]);
                if(dd<26 && dd<bd){ bd=dd; best=p; } } }
            if(!best) return;
            out.push([Math.round(Math.abs(lum(best)-lum(champ))), c.getAttribute('data-etat')||'?']);});
          return out;}""")
        t('carte d\'Index · mesurable [%s]' % th, 42 if pires else None,
          '%d cartes sondées' % len(pires))
        if pires:
            pires.sort()
            t('carte d\'Index · le pire des %d [%s]' % (len(pires), th), pires[0][0], pires[0][1])

        # ── LES BANDEAUX DU FIL (trait VERTICAL : sonde dédiée) ──
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1700)
        d = pg.evaluate("""()=>{const lum=c=>0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
          let pire=null;
          [...document.querySelectorAll('#feedList .s4-carte canvas')].forEach(cv=>{
            const g=cv.getContext('2d'); const k=cv.width/parseFloat(cv.style.width);
            const lire=(x,y)=>{const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
              return d[3]>200?[d[0],d[1],d[2]]:null;};
            const champ=lire(12,10); if(!champ) return;
            let best=null,bd=-1;
            for(let y=6;y<122;y+=2) for(let x=100;x<140;x+=1){
              const p=lire(x,y); if(!p) continue;
              const dd=Math.abs(p[0]-champ[0])+Math.abs(p[1]-champ[1])+Math.abs(p[2]-champ[2]);
              if(dd>bd){bd=dd;best=p;}}
            if(!best) return;
            const v=Math.round(Math.abs(lum(best)-lum(champ)));
            if(pire===null||v<pire) pire=v;});
          return pire;}""")
        t('bandeau du Fil · le pire [%s]' % th, d)

        # ── L'INSTANT ──
        pid = pg.evaluate("()=>(promises.filter(p=>!p.draft&&!p.req)[0]||{}).id")
        for nom in ('arrive','referme','apres'):
            pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid); pg.wait_for_timeout(1200)
            pg.evaluate("(k)=>window._instantJoue(k)", nom); pg.wait_for_timeout(900)
            r = mesure('dpTrameCv', 300, 44)
            t('l\'instant · %-8s [%s]' % (nom, th), r and r.get('d'),
              '%s sur %s' % (r.get('hexTrait'), r.get('hexChamp')) if r else '')
        pg.evaluate("()=>{window._instantJoue(null);if(window.closeAll)closeAll();}"); pg.wait_for_timeout(500)

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0]+len(ko)))
if ko:
    print('\nTRAITS SOUS LE SEUIL DE 42 :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
