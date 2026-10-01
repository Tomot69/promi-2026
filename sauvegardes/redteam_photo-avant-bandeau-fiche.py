#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_photo.py — LA PHOTO DE FICHE.

Dans la bande haute, au-dessus du trait, la photo REMPLACE la visualisation en dalles.
Ce contrôle vérifie les six choses que Tom a demandées, et il MESURE la lisibilité de
l'entête au lieu de la supposer.

Usage :  python3 redteam_photo.py [--verbose]
"""
import sys, base64
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
ok = [0]; ko = []

def t(nom, cond, detail=''):
    if cond: ok[0] += 1; print('%-56s OK  %s' % (nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-56s KO  %s' % (nom, detail))

# deux photos d'essai : une TRÈS CLAIRE et une TRÈS SOMBRE — c'est là que l'entête souffre
def png(rgb):
    import zlib, struct
    w=h=64
    raw=b''.join(b'\x00'+bytes(rgb)*w for _ in range(h))
    def ch(t,d):
        c=struct.pack('>I',len(d))+t+d
        return c+struct.pack('>I', zlib.crc32(t+d)&0xffffffff)
    return (b'\x89PNG\r\n\x1a\n'
            + ch(b'IHDR', struct.pack('>IIBBBBB',w,h,8,2,0,0,0))
            + ch(b'IDAT', zlib.compress(raw)) + ch(b'IEND', b''))

CLAIRE = 'data:image/png;base64,' + base64.b64encode(png((250,248,240))).decode()
SOMBRE = 'data:image/png;base64,' + base64.b64encode(png((8,8,12))).decode()

LIS = r"""()=>{
  /* la lisibilité de l'entête : on lit LE PIXEL PEINT sous le mot-marque et sous ✕ FERMER,
     et on le compare à leur encre. Seuil du §3 : 42 de luminosité. */
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const cv=document.getElementById('dpTrameCv'); if(!cv) return null;
  const g=cv.getContext('2d'); const k=cv.width/parseFloat(cv.style.width);
  const lum=c=>0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
  const rgb=s=>{const m=(s||'').match(/[\d.]+/g);return m?m.slice(0,3).map(Number):null;};
  const out={};
  [['marque','#dptNat'],['fermer','#detailPoster>.closeb']].forEach(([n,s])=>{
    const e=document.querySelector(s); if(!e){out[n]=null;return;}
    const r=e.getBoundingClientRect();
    const x=(r.left+r.width/2-dev.left)/sc, y=(r.top+r.height/2-dev.top)/sc;
    const d=g.getImageData(Math.round(x*k),Math.round(y*k),1,1).data;
    const enc=rgb(getComputedStyle(e).webkitTextFillColor||getComputedStyle(e).color);
    out[n]=Math.round(Math.abs(lum(enc)-lum([d[0],d[1],d[2]])));});
  return out;}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':390,'height':844}, device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    for nat, mise in (('Promi',   "()=>promises.filter(p=>!p.draft&&!p.req&&!p.chiche)[0].id"),
                      ('Chiche',  "()=>{const p=promises.filter(x=>x.chiche)[0]; return p?p.id:null;}")):
        pid = pg.evaluate(mise)
        if pid is None: continue
        print('\n── la fiche · %s ──' % nat)
        pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid); pg.wait_for_timeout(1500)

        # 1 · le bouton existe, discret, et il SUIT LE TRAIT
        g1 = pg.evaluate("""()=>{const b=document.querySelector('#detailPoster .ph-photo-btn');
          if(!b) return null; const c=getComputedStyle(b);
          const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
          const r=b.getBoundingClientRect();
          return {x:(r.left-dev.left)/sc, y:(r.top-dev.top)/sc, w:r.width/sc, h:r.height/sc,
                  op:parseFloat(c.opacity), texte:(b.textContent||'').trim()};}""")
        t('%s · le bouton est là' % nat, bool(g1), str(g1))
        if not g1: continue
        t('%s · il est petit' % nat, g1['w'] <= 40 and g1['h'] <= 40, '%.0f×%.0f' % (g1['w'], g1['h']))
        t('%s · il est discret' % nat, g1['op'] < 0.8 and not g1['texte'],
          'opacité %.2f, sans libellé' % g1['op'])
        t('%s · il est en bas à droite' % nat, g1['x'] + g1['w'] > 330, 'droite à %.0f' % (g1['x']+g1['w']))

        # 2 · il suit le trait : on change la base, l'écart doit rester le même
        e1 = pg.evaluate("""()=>{const dp=document.getElementById('detailPoster');
          const e=window._ficheEcran(dp,cur); const y=window._onde.onde(e.base,e.amp);
          const b=document.querySelector('#detailPoster .ph-photo-btn');
          const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
          const r=b.getBoundingClientRect();
          return Math.round(y(349) - (r.top-dev.top)/sc);}""")
        pg.evaluate("""()=>{const p=cur; p.__b=1; const dp=document.getElementById('detailPoster');
          dp.classList.add('f-tenue');}"""); pg.wait_for_timeout(200)
        pg.evaluate("()=>{if(window._ficheTrait)_ficheTrait();}"); pg.wait_for_timeout(500)
        e2 = pg.evaluate("""()=>{const dp=document.getElementById('detailPoster');
          const e=window._ficheEcran(dp,cur); const y=window._onde.onde(e.base,e.amp);
          const b=document.querySelector('#detailPoster .ph-photo-btn');
          const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
          const r=b.getBoundingClientRect();
          return Math.round(y(349) - (r.top-dev.top)/sc);}""")
        t('%s · l\'écart au trait ne bouge pas' % nat, abs(e1-e2) <= 2, '%s px puis %s px' % (e1, e2))

        # 3 · la photo remplace la dalle
        for nom, src in (('claire', CLAIRE), ('sombre', SOMBRE)):
            pg.evaluate("(s)=>{cur.photo=s; if(window._ficheTrait)_ficheTrait();}", src)
            pg.wait_for_timeout(900)
            pg.evaluate("()=>{if(window._ficheTrait)_ficheTrait();}"); pg.wait_for_timeout(700)
            peint = pg.evaluate("""(attendu)=>{const dp=document.getElementById('detailPoster');
              const e=window._ficheEcran(dp,cur); const b=e.dalle;
              const cv=document.getElementById('dpTrameCv'); const g=cv.getContext('2d');
              const k=cv.width/parseFloat(cv.style.width);
              const d=g.getImageData(Math.round((b.x+b.w/2)*k),Math.round((b.y+b.h*0.7)*k),1,1).data;
              return [d[0],d[1],d[2]];}""", src)
            proche = abs(peint[0]-(250 if nom=='claire' else 8)) < 30
            t('%s · la photo %s occupe la boîte de la dalle' % (nat, nom), proche, 'rgb%s' % peint)

            # 4 · l'entête reste lisible — MESURÉ
            L = pg.evaluate(LIS)
            t('%s · entête lisible sur photo %s' % (nat, nom),
              L and L.get('marque',0) >= 42 and L.get('fermer',0) >= 42,
              'Δ mot-marque %s · Δ ✕ FERMER %s (seuil 42)' % (L.get('marque'), L.get('fermer')))

            # 5 · rien ne dépasse sous l'onde
            sous = pg.evaluate("""()=>{const dp=document.getElementById('detailPoster');
              const e=window._ficheEcran(dp,cur);
              const y=window._onde.onde(e.base,e.amp);
              const cv=document.getElementById('dpTrameCv'); const g=cv.getContext('2d');
              const k=cv.width/parseFloat(cv.style.width);
              let n=0;
              for(let x=40;x<350;x+=14){ const yy=Math.round((y(x)+22)*k);
                if(yy>=cv.height) continue;
                const d=g.getImageData(Math.round(x*k),yy,1,1).data;
                if(d[3]>200) n++; }
              return n;}""")
            t('%s · la photo %s ne passe pas sous l\'onde' % (nat, nom), sous == 0,
              '%d points peints sous le trait' % sous)

        # 6 · le même bouton rend la dalle
        pg.evaluate("""()=>{const b=document.querySelector('#detailPoster .ph-photo-btn'); if(b)b.click();}""")
        pg.wait_for_timeout(900)
        t('%s · le même bouton revient à la dalle' % nat,
          pg.evaluate("()=>!cur.photo"), 'photo = %s' % pg.evaluate("()=>!!cur.photo"))

    # ── Q53 · LA PHOTO PARTOUT OÙ LA MATIÈRE S'AFFICHE ──────────────────────────────
    print('\n── la photo dans les listes (Q53) ──')
    # on pose la photo sur une promesse qui est À LA FOIS dans l'Index ET dans le Fil :
    # sinon le bandeau qu'on cherche n'existe pas, et le contrôle ment.
    pid = pg.evaluate("""()=>{const dansFil=FEED.map(f=>f.pid).filter(Boolean);
      const p=promises.filter(x=>!x.draft&&!x.req&&dansFil.indexOf(x.id)>=0)[0]
             || promises.filter(x=>!x.draft&&!x.req)[0];
      return p?p.id:null;}""")
    pg.evaluate("(a)=>{const p=promises.find(x=>x.id===a.id); p.photo=a.src;}",
                {'id': pid, 'src': CLAIRE})
    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}")
    pg.wait_for_timeout(1900)
    pg.evaluate("()=>{if(window.buildIndex)buildIndex();}"); pg.wait_for_timeout(1200)
    vu = pg.evaluate("""(id)=>{const c=[...document.querySelectorAll('#indexList .s4-carte')]
      .filter(x=>x.getAttribute('data-etat')!==null);
      for(const x of c){ const cv=x.querySelector('canvas'); if(!cv) continue;
        const g=cv.getContext('2d'); const k=cv.width/parseFloat(cv.style.width);
        const d=g.getImageData(Math.round(80*k),Math.round(40*k),1,1).data;
        if(Math.abs(d[0]-250)<26 && Math.abs(d[1]-248)<26) return true; }
      return false;}""", pid)
    t('Q53 · une carte d\'Index montre la photo', vu, 'photo très claire cherchée dans les cartes')

    pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1900)
    pg.evaluate("()=>{if(window.buildFeed)buildFeed();}"); pg.wait_for_timeout(1200)
    vu2 = pg.evaluate("""()=>{for(const cv of document.querySelectorAll('#feedList .s4-carte canvas')){
        const g=cv.getContext('2d'); const k=cv.width/parseFloat(cv.style.width);
        const d=g.getImageData(Math.round(60*k),Math.round(60*k),1,1).data;
        if(Math.abs(d[0]-250)<26 && Math.abs(d[1]-248)<26) return true; }
      return false;}""")
    t('Q53 · un bandeau du Fil montre la photo', vu2)
    pg.evaluate("(id)=>{const p=promises.find(x=>x.id===id); if(p)p.photo=null;}", pid)

    print('\n── la page + ──')
    pg.evaluate("()=>{if(window.closeAll)closeAll();document.getElementById('createBtn').click();}")
    pg.wait_for_timeout(900)
    pg.evaluate("()=>{const t=[...document.querySelectorAll('#createSheet .tile')][0];if(t)t.click();}")
    pg.wait_for_timeout(1200)
    t('la page + porte le bouton',
      pg.evaluate("()=>!!document.querySelector('#createSheet .ph-photo-btn')"))

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0]+len(ko)))
if ko:
    print('\nCE QUI NE MARCHE PAS :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
