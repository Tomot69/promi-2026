#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_phrase_fiche.py — v136 (Tom, 7 oct. 2026, C-069) : LA PHRASE COMPLÈTE DANS LES FICHES PROMI ET CHICHE.
« Dans les fiches seulement, jamais dans le Fil ni l'Index, et pour les Promi et les Chiche (pas les Cercles) : on remet la phrase entière.
La ligne « À moi » / « À Rachel » disparaît, la phrase la remplace. Le titre reste l'élément le plus visible. Au-delà de quelques
personnes : « … + x personnes ». Toucher cette mention déroule la liste complète dans la phrase, qui s'allonge vers le bas. »
Juge demandé : « chaque cas produit sa phrase, le titre est le plus grand texte de la fiche, et le Fil et l'Index sont inchangés ».
Les phrases attendues sont EN DUR (les formes de la page +). Au vrai doigt pour « + x personnes ». Usage : python3 redteam_phrase_fiche.py [fichier.html]"""
import sys
from playwright.sync_api import sync_playwright
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
NB=' '
CAS=[('à soi',"p=promises.find(q=>q.title==='nager le mardi')", 'Je me promets de', 'nager le mardi'),
     ('à une personne',"p=promises.find(q=>q.title==='faire les crêpes')", 'Je promets à Rachel de', 'faire les crêpes'),
     ('à trois personnes',"p=promises.find(q=>q.title==='faire les crêpes'); p.who='Rachel, Marion, Nico'", 'Je promets à Rachel, Marion et Nico de', 'faire les crêpes'),
     ('à six personnes',"p=promises.find(q=>q.title==='faire les crêpes'); p.who='Rachel, Marion, Nico, Adrien, Léa, Jo'", 'Je promets à Rachel, Marion +'+NB+'4'+NB+'personnes de', 'faire les crêpes'),
     ('Promi reçu',"p=promises.find(q=>q.title==='nager le mardi'); p.from='Rachel'; p.who='moi'", 'Rachel me promet de', 'nager le mardi'),
     ('Chiche lancé',"p=promises.find(q=>q.title==='courir dimanche')", 'À Marion · avec Rachel · chiche de', 'courir dimanche'),
     ('Chiche reçu',"p=promises.find(q=>q.title==='courir dimanche'); p.from='Marion'; p.who='moi'; p.avec=''", 'Marion me lance'+NB+': chiche de', 'courir dimanche'),
     ('élision',"p=promises.find(q=>q.title==='nager le mardi'); p.title='aller voir la mer'", 'Je me promets d’', 'aller voir la mer')]
VERBES=['Je me promets','Je promets à','me promet de','me promet d’','chiche de','promets-moi de','me lance']
R=[]
def ok(n,c,d=''): R.append((n,bool(c))); print(('  ✅ ' if c else '  ❌ ')+n+((' — '+str(d)[:260]) if d!='' else ''))
LU="""()=>{const D=document.getElementById('device').getBoundingClientRect(), dp=document.getElementById('detailPoster'), q=document.getElementById('dptQui'), t=document.getElementById('dptTitre');
  let max=0, qui=''; dp.querySelectorAll('*').forEach(e=>{ if(!e.getClientRects().length) return; const tx=[...e.childNodes].filter(n=>n.nodeType===3&&n.nodeValue.trim()).length; if(!tx) return; const s=getComputedStyle(e); if(s.visibility==='hidden'||+s.opacity<0.1) return; const r=e.getBoundingClientRect(); if(r.bottom<D.top||r.top>D.bottom) return; const fs=parseFloat(s.fontSize); if(fs>max){max=fs; qui=e.id||e.className;} });
  const rq=q.getBoundingClientRect(), rt=t.getBoundingClientRect(); return {phrase:q.textContent, titre:t.textContent, plusGrand:qui, fsT:parseFloat(getComputedStyle(t).fontSize), fsQ:parseFloat(getComputedStyle(q).fontSize), qBas:rq.bottom, tHaut:rt.top, voix:q.getAttribute('aria-label')} }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('light','dark'):
        for nom,js,phrase,titre in CAS:
            ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
            ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
            pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:140])); pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6200)
            pg.evaluate("(a)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(a[0]); let p; eval(a[1]); closeAll(); openDetail(p.id);}",[th,js]); pg.wait_for_timeout(2800)
            r=pg.evaluate(LU)
            ok('[%s] %s : la phrase « %s », le titre « %s » seul dans son nœud'%(th,nom,phrase,titre), r['phrase']==phrase and r['titre']==titre, (r['phrase'],r['titre']))
            ok('[%s] %s : le titre est le plus grand texte de la fiche, la phrase est au-dessus de lui sans le toucher'%(th,nom), r['plusGrand']=='dptTitre' and r['fsT']>r['fsQ']*1.4 and r['qBas']<=r['tHaut']+1, (r['plusGrand'],r['fsT'],r['fsQ'],round(r['tHaut']-r['qBas'],1)))
            if nom=='à six personnes':
                c=pg.evaluate("()=>{const e=document.querySelector('#dptQui .dpt-plus'); if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
                if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(1500)
                r2=pg.evaluate(LU)
                ok('[%s] toucher « + 4 personnes » déroule la liste dans la phrase, le titre reste dessous'%th, r2['phrase']=='Je promets à Rachel, Marion, Nico, Adrien, Léa et Jo de' and r2['qBas']<=r2['tHaut']+1 and r2['titre']==titre, (r2['phrase'], round(r2['tHaut']-r2['qBas'],1)))
            if nom=='à soi':
                # le Fil, l'Index et une fiche de Cercle ne portent aucune phrase
                pg.evaluate("()=>{closeAll(); ouvrirIndex();}"); pg.wait_for_timeout(1800); ti=pg.evaluate("()=>document.getElementById('indexList').textContent")
                pg.evaluate("()=>{closeAll(); setView('fil');}"); pg.wait_for_timeout(1800); tf=pg.evaluate("()=>['feedList','feedView','feedScreen'].map(i=>{const e=document.getElementById(i); return e?e.textContent:''}).join(' ')")
                pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(2400); tc=pg.evaluate("()=>document.getElementById('dptQui').textContent+' | '+(document.getElementById('dptQui').getAttribute('data-phrase')||'')")
                ok('[%s] l\'Index ne porte aucune phrase (ses cartes gardent « à … »)'%th, len(ti)>40 and not any(v in ti for v in VERBES), [v for v in VERBES if v in ti])
                ok('[%s] le Fil ne porte aucune phrase'%th, len(tf)>40 and not any(v in tf for v in VERBES[:6]), [v for v in VERBES[:6] if v in tf])
                ok('[%s] la fiche d\'un Cercle garde sa ligne « avec … », sans phrase'%th, tc.lower().startswith('avec') and tc.endswith('| '), tc)
            ok('[%s] %s : aucune erreur de page'%(th,nom), not errs, errs[:1]); ctx.close()
    b.close()
n=sum(1 for _,c in R if c); print('\nredteam_phrase_fiche : %d/%d'%(n,len(R)))
for nom,c in R:
    if not c: print('   ROUGE :', nom)
sys.exit(0 if n==len(R) else 1)
