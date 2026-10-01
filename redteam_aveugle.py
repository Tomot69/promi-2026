#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_aveugle.py — LES TROIS ZONES QUE PERSONNE NE REGARDE.

1 · LE CERCLE PAYÉ — `isPremium` forcé : ce que voit un abonné.
2 · LA NUÉE EN PROFONDEUR — sa fiche, ses membres, son fil.
3 · UN PARCOURS ENTIER — planter → fiche → tenir → Index → Fil, dans les deux thèmes.

Usage :  python3 redteam_aveugle.py [--verbose]
"""
import sys
from playwright.sync_api import sync_playwright

APP = "http://127.0.0.1:8752/app.html"
VERBOSE = '--verbose' in sys.argv
ok=[0]; ko=[]
def t(nom, cond, detail=''):
    if cond: ok[0]+=1; print('%-56s OK  %s'%(nom, detail if VERBOSE else ''))
    else: ko.append(nom); print('%-56s KO  %s'%(nom, detail))

SUP = r"""(racine)=>{
  const dev=document.getElementById('device').getBoundingClientRect(); const sc=dev.width/390;
  const h=racine?document.querySelector(racine):document.body; if(!h) return [];
  const vis=e=>{const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)<0.35) return false;
    const r=e.getBoundingClientRect(); return r.width>6&&r.height>6;};
  const f=[...h.querySelectorAll('*')].filter(e=>{ if(!vis(e)) return false;
    if(['CANVAS','IMG','SVG'].includes(e.tagName)) return false;
    const t=(e.textContent||'').trim(); if(!t) return false;
    return [...e.children].every(c=>['B','I','EM','STRONG','SPAN','SMALL','BR','U'].includes(c.tagName));});
  const box=e=>{const r=e.getBoundingClientRect();
    return {x:(r.left-dev.left)/sc,y:(r.top-dev.top)/sc,w:r.width/sc,h:r.height/sc};};
  const out=[];
  for(let i=0;i<f.length;i++) for(let j=i+1;j<f.length;j++){
    const a=f[i],b=f[j]; if(a.contains(b)||b.contains(a)) continue;
    const A=box(a),B=box(b);
    const ix=Math.max(0,Math.min(A.x+A.w,B.x+B.w)-Math.max(A.x,B.x));
    const iy=Math.max(0,Math.min(A.y+A.h,B.y+B.h)-Math.max(A.y,B.y));
    if(ix<3||iy<3) continue;
    if(ix*iy/Math.min(A.w*A.h,B.w*B.h) < 0.4) continue;
    /* ⚑ CONFIRMÉ AU DOIGT (§8, réécrit le 14 sept. 2026 au niveau de la règle : « un recouvrement se confirme au doigt,
       jamais au rectangle seul »). Au centre de l'intersection, un texte n'est VU que si aucun aplat opaque qui n'est pas
       son ancêtre ne passe devant lui. Vécu : la carte « vider le composteur » du fil d'une Nuée défile SOUS la barre
       Peaufiner, opaque — le rectangle la comptait. Original : sauvegardes/redteam_aveugle-avant-au-doigt.py */
    const cx=dev.left+(Math.max(A.x,B.x)+ix/2)*sc, cy=dev.top+(Math.max(A.y,B.y)+iy/2)*sc;
    if(cx>=0&&cy>=0&&cx<=innerWidth&&cy<=innerHeight){
      const pile=document.elementsFromPoint(cx,cy);
      const vu=el=>{ for(const s of pile){ if(s===el||el.contains(s)) return true; if(s.contains(el)) continue;
        const bg=getComputedStyle(s).backgroundColor, m=bg.match(/rgba?\(([^)]+)\)/); const al=m?(m[1].split(',')[3]===undefined?1:parseFloat(m[1].split(',')[3])):0;
        if(al>0.9) return false; } return true; };   /* absent de la pile (pointer-events:none) et rien d'opaque devant : vu */
      if(!(vu(a)&&vu(b))) continue;
    }
    out.push(((a.textContent||'').trim().slice(0,18))+' ⨯ '+((b.textContent||'').trim().slice(0,18)));}
  return [...new Set(out)].slice(0,6);}"""

with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror', lambda e: er.append(str(e)))
    pg.goto(APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    for th in ('dark','light'):
        pg.evaluate("(t)=>setTheme(t)", th); pg.wait_for_timeout(500)
        print('\n══ thème %s ══' % th)

        # ── 1 · LE CERCLE PAYÉ ───────────────────────────────────────────────────────
        for prem in (False, True):
            pg.evaluate("(v)=>{if(typeof setPremium==='function')setPremium(v);}", prem)
            pg.evaluate("""()=>{if(window.closeAll)closeAll();
              openDetail(promises.filter(p=>!p.draft&&!p.req)[0].id);}"""); pg.wait_for_timeout(1300)
            pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}")
            pg.wait_for_timeout(1200)
            e = pg.evaluate("""()=>{const r=document.querySelector('#detailPoster .s2-cercle .s2-reg');
              if(!r) return null; const c=getComputedStyle(r);
              const enc=document.querySelector('#detailPoster .s2-cercle .s2-encart,#detailPoster .s2-cercle .set-cercle');
              return {flou:c.filter, pe:c.pointerEvents,
                      encart:enc?getComputedStyle(enc).display:'-'};}""")
            mot = 'payé' if prem else 'non payé'
            if prem:
                t('Cercle %-9s [%s] · les réglages sont NETS' % (mot, th),
                  e and e['flou']=='none' and e['pe']!='none', str(e))
                t('Cercle %-9s [%s] · l\'encart s\'efface' % (mot, th),
                  e and e['encart']=='none', 'encart : %s' % (e or {}).get('encart'))
            else:
                t('Cercle %-9s [%s] · les réglages sont floutés' % (mot, th),
                  e and 'blur' in (e['flou'] or '') and e['pe']=='none', str(e))
        pg.evaluate("()=>{if(typeof setPremium==='function')setPremium(false);}")

        # ── 2 · LA NUÉE EN PROFONDEUR ────────────────────────────────────────────────
        pg.evaluate("()=>{if(window.closeAll)closeAll();const k=Object.keys(NUE)[0];if(k)openEssaim(k);}")
        pg.wait_for_timeout(1800)
        n = pg.evaluate("""()=>{const dp=document.getElementById('detailPoster');
          const v=id=>{const e=document.getElementById(id); if(!e) return 'ABSENT';
            const c=getComputedStyle(e); return (c.display==='none'||c.visibility==='hidden')?'masqué':'VU';};
          return {mode:dp.classList.contains('dp-mode-nuee')||dp.classList.contains('dp-nuee'),
                  trace:v('dptTrace'), geste:v('tenirCv'),
                  titre:(document.getElementById('dptTitre')||{}).textContent,
                  deuxEcrans:(document.getElementById('essaimSheet')||{classList:{contains:()=>false}}).classList.contains('show')};}""")
        t('Nuée [%s] · un seul écran' % th, n and not n['deuxEcrans'], 'essaimSheet montré : %s' % (n or {}).get('deuxEcrans'))
        t('Nuée [%s] · ni trait à tracer, ni geste' % th,
          n and n['trace'] in ('ABSENT','masqué') and n['geste'] in ('ABSENT','masqué'),
          'trace=%s geste=%s' % ((n or {}).get('trace'), (n or {}).get('geste')))
        s = pg.evaluate(SUP, '#detailPoster')
        t('Nuée [%s] · rien ne se superpose' % th, not s, ' · '.join(s))

        # ── 3 · UN PARCOURS ENTIER ───────────────────────────────────────────────────
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(600)
        n0 = pg.evaluate("()=>promises.length")
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];if(x)x.click();}")
        pg.wait_for_timeout(1100)
        pg.evaluate("""()=>{const f=document.getElementById('fTitle');
          if(f){f.value='aller voir la mer'; f.dispatchEvent(new Event('input',{bubbles:true}));}
          if(window._phrase){window._phrase.titre='aller voir la mer'; if(window._phraseRendu)_phraseRendu();}}""")
        pg.wait_for_timeout(700)
        r = pg.evaluate("""()=>{const e=document.querySelector('#planterCv');if(!e)return null;
          const b=e.getBoundingClientRect();return {x:b.left,y:b.top,w:b.width,h:b.height};}""")
        if r:
            yy=r['y']+r['h']/2
            pg.mouse.move(r['x']+12, yy); pg.mouse.down()
            for i in range(1,26):
                pg.mouse.move(r['x']+12+(r['w']-24)*i/25, yy+(6 if i%2 else -6)); pg.wait_for_timeout(12)
            pg.mouse.up(); pg.wait_for_timeout(1400)
        t('parcours [%s] · planter' % th, pg.evaluate("()=>promises.length") > n0,
          '%d → %d' % (n0, pg.evaluate("()=>promises.length")))
        pid = pg.evaluate("""()=>{const p=promises[promises.length-1]; if(p){p.status='rate';} return p?p.id:null;}""")
        pg.evaluate("(i)=>{if(window.closeAll)closeAll();openDetail(i);}", pid); pg.wait_for_timeout(1400)
        pg.evaluate("()=>{if(typeof renderDetail==='function')renderDetail();}"); pg.wait_for_timeout(800)
        t('parcours [%s] · la fiche s\'ouvre' % th,
          pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
        r = pg.evaluate("""()=>{const e=document.querySelector('#tenirCv');if(!e)return null;
          const b=e.getBoundingClientRect(); if(b.width<10) return null;
          return {x:b.left,y:b.top,w:b.width,h:b.height};}""")
        if r:
            yy=r['y']+r['h']/2
            pg.mouse.move(r['x']+12, yy); pg.mouse.down()
            for i in range(1,26):
                pg.mouse.move(r['x']+12+(r['w']-24)*i/25, yy+(6 if i%2 else -6)); pg.wait_for_timeout(12)
            pg.mouse.up(); pg.wait_for_timeout(1400)
        t('parcours [%s] · tenir au geste' % th,
          pg.evaluate("(i)=>{const p=promises.find(x=>x.id===i);return p&&p.status==='tenu';}", pid))
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');ouvrirIndex();}"); pg.wait_for_timeout(1700)
        t('parcours [%s] · l\'Index le montre' % th,
          pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte').length") > 0,
          '%d cartes' % pg.evaluate("()=>document.querySelectorAll('#indexList .s4-carte').length"))
        s = pg.evaluate(SUP, '#indexSheet')
        t('parcours [%s] · l\'Index ne se superpose pas' % th, not s, ' · '.join(s))
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('fil');}"); pg.wait_for_timeout(1700)
        t('parcours [%s] · le Fil le montre' % th,
          pg.evaluate("()=>document.querySelectorAll('#feedList .s4-carte').length") > 0,
          '%d bandeaux' % pg.evaluate("()=>document.querySelectorAll('#feedList .s4-carte').length"))
        s = pg.evaluate(SUP, '#feedView')
        t('parcours [%s] · le Fil ne se superpose pas' % th, not s, ' · '.join(s))
        pg.evaluate("()=>{if(window.closeAll)closeAll();setView('toile');}"); pg.wait_for_timeout(700)

    if er: print('\nERREURS JS :', er[:3])
    b.close()

print('\n%d/%d' % (ok[0], ok[0]+len(ko)))
if ko:
    print('\nCE QUI NE MARCHE PAS :')
    for k in ko: print('   ·', k)
sys.exit(0 if not ko else 1)
