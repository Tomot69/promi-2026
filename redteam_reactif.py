#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_reactif.py — v130 (C-049) : LES ÉCRANS REFLÈTENT L'ÉTAT RÉEL, TOUT DE SUITE.
Décision Tom (5 oct. 2026) : « Quand on plante ou qu'on retire une parole, l'Index, le Fil et la liste des dalles en bas de
l'Aura [se mettent] à jour tout de suite […]. Chaque écran doit refléter l'état réel immédiatement, sans recharger la page. »
Le juge plante, tient puis retire une parole PAR LES VRAIS BOUTONS, sans jamais recharger ; après chaque action il lit
l'Index, le Fil, la liste de l'Aura et le fil du Cercle concerné, À L'IMAGE SUIVANTE, dans deux situations :
  · l'écran est RESTÉ AFFICHÉ pendant l'action (on a ouvert la fiche depuis lui, on y revient) ;
  · l'écran est OUVERT juste après.
Le verdict vient du DOM rendu, comparé aux données (`promises`) ; la liste de l'Aura est jugée COMPLÈTE contre la règle
décidée EN DUR (v131 : TOUTES les paroles tenues, dans l'ordre chronologique — plus de limite à 3 ou 6).
Usage : python3 redteam_reactif.py [fichier.html]"""
import sys
from playwright.sync_api import sync_playwright
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
T='parole du juge'; CERCLE='potager'
# ⚑ v131 (Tom, 5 oct. 2026, C-052) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_reactif-avant-v131.py). La règle d'avant (Q187) : trois
#   dalles, six dès cinq tenues, les plus récentes d'abord. La décision qui la remplace : « la liste montre TOUTES les paroles tenues, dans
#   l'ordre chronologique, l'Aura défilant. Plus de limite à 3 ou 6. » La parole qu'on vient de tenir est donc la DERNIÈRE.
ANIME_MAX = 3000                                       # l'amande (1 000 ms, v124) puis « juste après » : la fiche couvre l'Aura ; borne en dur
LIRE=r"""()=>{ const moi=p=>p&&!p.draft&&!p.req&&(!p.from||p.from==='moi');
  const sc=(id)=>{const e=document.getElementById(id); return !!e&&(e.classList.contains('show')||e.classList.contains('in'));};
  let ordre=[]; try{ ordre=JSON.parse(localStorage.getItem('promi_pelote_ordre')||'[]'); }catch(e){}
  return { ouverts:['indexSheet','feedView','auraScreen','detailPoster','createSheet'].filter(sc),
    index:[...document.querySelectorAll('#indexList .s4-ti')].map(e=>e.textContent.trim()),
    filTxt:(document.getElementById('feedList')||{innerText:''}).innerText.replace(/\s+/g,' '),
    filCartes:[...document.querySelectorAll('#feedList .s4-grille > *')].map(e=>e.innerText.replace(/\s+/g,' ')),
    moisson:[...document.querySelectorAll('#auraScreen .au-mo .au-c span')].map(e=>e.textContent.trim()),
    nf:[...document.querySelectorAll('#detailPoster .nf-item')].map(e=>e.innerText.replace(/\s+/g,' ').trim()),
    tenus:promises.filter(p=>moi(p)&&p.status==='tenu').map(p=>p.title),
    horsCercle:promises.filter(p=>!p.req&&!p.nuee).map(p=>p.title),
    duCercle:promises.filter(p=>!p.draft&&!p.req&&p.nuee==='potager').map(p=>p.title+'|'+p.status) }; }"""
R=[]
def ok(nom, cond, detail=''):
    R.append((nom, bool(cond))); print(('  ✅ ' if cond else '  ❌ ')+nom+((' — '+detail) if (detail and not cond) else ''))
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    def img(): pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r,0))))")
    def lire(): img(); return pg.evaluate(LIRE)
    def accueil():
        pg.evaluate("()=>{ const a=document.getElementById('auraScreen'); const x=document.querySelector('#auraScreen .closeb'); if(a&&a.classList.contains('show')&&x) x.click(); closeAll(); try{ if(typeof setView==='function') setView('toile'); }catch(e){} }"); pg.wait_for_timeout(500)
    OUVRE={'Index':"()=>ouvrirIndex()", 'Fil':"()=>document.getElementById('filBtn').click()", 'Aura':"()=>document.getElementById('souffleBtn').click()", 'Cercle':"()=>openEssaim('potager')"}
    def attendu_moisson(e):
        return len(e['tenus'])
    def juge(lab, e, ecran, present, etat=None):
        """present : la parole du juge doit-elle paraître sur cet écran ?"""
        if ecran=='Index':
            # un Promi d'un Cercle vit dans la carte de son Cercle : l'Index est jugé COMPLET sur les paroles hors Cercle
            manq=[t for t in e['horsCercle'] if t not in e['index']]
            ok('%s · Index complet (%d cartes, aucune parole hors Cercle absente)'%(lab,len(e['index'])), not manq and len(e['index'])>0, 'absentes : %s'%manq)
            fant=[t for t in e['index'] if t==T and T not in e['horsCercle']]
            ok('%s · Index sans parole retirée'%lab, not fant)
        elif ecran=='Fil':
            a=T in e['filTxt']
            ok('%s · Fil : la parole %s'%(lab,'y est' if present else "n'y est plus"), a==present, 'trouvée=%s'%a)
            if present and etat=='tenu':
                c=[x for x in e['filCartes'] if T in x]; ok('%s · Fil : elle y est dite tenue'%lab, any('TENU' in x.upper() for x in c), str(c)[:160])
        elif ecran=='Aura':
            n=attendu_moisson(e); recents=list(reversed(e['tenus']))
            ok('%s · Aura : la liste est complète — TOUTES les paroles tenues (%d)'%(lab,n), len(e['moisson'])==n and sorted(e['moisson'])==sorted(e['tenus']), 'rendu %s'%e['moisson'])
            if etat=='tenu' and present: ok('%s · Aura : la parole tenue est la dernière de la liste (ordre chronologique)'%lab, e['moisson'][-1:]==[T], 'fin %s'%e['moisson'][-1:])
            if not present: ok("%s · Aura : la parole n'y est pas"%lab, T not in e['moisson'], str(e['moisson']))
        elif ecran=='Cercle':
            att=sorted(x.split('|')[0] for x in e['duCercle']); rendu=sorted([t for t in att if any(t in y for y in e['nf'])])
            ok('%s · fil du Cercle complet (%d paroles)'%(lab,len(att)), rendu==att and len(e['nf'])==len(att), 'rendu %d lignes'%len(e['nf']))
            a=any(T in y for y in e['nf']); ok('%s · fil du Cercle : la parole %s'%(lab,'y est' if present else "n'y est plus"), a==present)
            if present and etat=='tenu': ok('%s · fil du Cercle : elle y est dite tenue'%lab, any(T in y and 'TENU' in y.upper() for y in e['nf']), str([y for y in e['nf'] if T in y]))
    def tour(lab, present, etat=None):
        for ecran in ('Index','Fil','Aura','Cercle'):
            accueil(); pg.evaluate(OUVRE[ecran]); juge(lab+' · ouvert ensuite', lire(), ecran, present, etat)
        accueil()
    # ── chaque écran est ouvert une première fois : c'est après qu'un écran « construit une fois » se trahit ──
    for ecran in ('Index','Fil','Aura','Cercle'):
        accueil(); pg.evaluate(OUVRE[ecran]); pg.wait_for_timeout(1600)
    # ── 0 · on dépasse l'ancienne borne (6) : deux paroles de plus sont tenues par le vrai bouton, AVANT le reste
    for ti in ('nager le mardi','tailler la vigne'):
        accueil(); pg.evaluate("(t)=>openDetail(promises.find(p=>p.title===t).id)", ti); pg.wait_for_timeout(2000)
        pg.evaluate("()=>document.querySelector('#segStatus button[data-st=tenu]').click()"); pg.wait_for_function("()=>!window._tenirAnime", timeout=ANIME_MAX); pg.wait_for_timeout(600)
    accueil(); pg.evaluate(OUVRE['Aura']); e0=lire()
    ok("Aura : sept paroles tenues, sept dalles (l'ancienne borne était six)", len(e0['tenus'])==7 and len(e0['moisson'])==7, '%d tenues · %d dalles'%(len(e0['tenus']),len(e0['moisson'])))
    # ── 1 · PLANTER dans le Cercle, par « Planter dans le Cercle », le fil du Cercle étant AFFICHÉ ──
    print('1 · PLANTER'); accueil(); pg.evaluate(OUVRE['Cercle']); pg.wait_for_timeout(1800)
    pg.evaluate("()=>document.getElementById('nfAdd').click()"); pg.wait_for_timeout(2600)
    pg.evaluate("(t)=>{ const f=document.getElementById('fTitle'); f.value=t; f.dispatchEvent(new Event('input',{bubbles:true})); document.getElementById('addPromi').click(); }", T)
    pg.wait_for_timeout(700)
    pid=pg.evaluate("(t)=>{const q=promises.filter(p=>p.title===t); return q.length===1?[q[0].id,q[0].nuee||null,q[0].status]:null}", T)
    ok('la parole est plantée dans le Cercle (données)', pid and pid[1]==CERCLE, str(pid))
    pg.wait_for_timeout(2600); tour('planter', True)
    # ── 2 · TENIR, la fiche ouverte DEPUIS la liste de l'Aura n'existant pas encore : on tient depuis le fil du Cercle ──
    print('2 · TENIR'); accueil(); pg.evaluate(OUVRE['Aura']); pg.wait_for_timeout(1500)       # l'Aura reste AFFICHÉE dessous
    pg.evaluate("(id)=>openDetail(id)", pid[0]); pg.wait_for_timeout(2200)
    pg.evaluate("()=>document.querySelector('#segStatus button[data-st=tenu]').click()")
    # l'Aura est SOUS la fiche pendant l'animation de « tenir » (décidé v124 : aucun travail pendant elle) :
    # elle doit être juste à l'image qui suit la fin de l'animation — donc avant qu'on puisse la revoir.
    t0=pg.evaluate("()=>performance.now()")
    pg.wait_for_function("()=>!window._tenirAnime", timeout=ANIME_MAX); dt=pg.evaluate("(t)=>performance.now()-t", t0)
    ok("tenir · l'animation rend la main en moins de %d ms"%ANIME_MAX, dt<ANIME_MAX, '%d ms'%dt)
    e=lire(); juge('tenir · Aura restée affichée', e, 'Aura', True, 'tenu')
    pg.wait_for_timeout(2500); tour('tenir', True, 'tenu')
    # ── 3 · RETIRER, par « Supprimer » et sa confirmation, la fiche ouverte depuis la liste de l'Aura ──
    print('3 · RETIRER'); accueil(); pg.evaluate(OUVRE['Aura']); pg.wait_for_timeout(1500)
    pg.evaluate("(id)=>openDetail(id)", pid[0]); pg.wait_for_timeout(2200)
    pg.evaluate("(id)=>window._v16SupprimerPromi(promises.find(p=>p.id===id))", pid[0]); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.querySelector('#v16Conf .v16-oui').click()")
    e=lire(); ok('la parole est retirée (données)', not pg.evaluate("(id)=>promises.some(p=>p.id===id)", pid[0]))
    juge('retirer · Aura restée affichée', e, 'Aura', False)
    pg.wait_for_timeout(1200); tour('retirer', False)
    ok('aucune erreur de page', not errs, str(errs[:2]))
    b.close()
n=sum(1 for _,c in R if c); print('\nredteam_reactif : %d/%d'%(n,len(R)))
for nom,c in R:
    if not c: print('   ROUGE :', nom)
sys.exit(0 if n==len(R) else 1)
