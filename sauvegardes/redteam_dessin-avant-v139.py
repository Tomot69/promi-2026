#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_dessin.py — v132 (C-042) : LE DESSIN, CONSTRUIT DANS L'APP.
Décisions Tom (5 oct. 2026), en dur dans ce juge :
  A · COULEURS FIGÉES trait par trait — « trois traits sous trois palettes, chacun garde la sienne » ; le dessin en cours est gardé si l'on
      sort ; après le premier POSER le fond est fixé (plus d'onglet FOND) et les nouveaux traits ne prennent que les couleurs déjà présentes ;
  B · MASQUAGE pour soi seul, mémorisé par fiche — « un dessin masqué n'est jamais emporté dans un partage » ;
  C · AUCUNE SUPERPOSITION d'outil sur la surface de dessin : la surface va du haut de l'écran à la rangée, posée EN BAS ; tailles et couleurs
      se déploient juste AU-DESSUS de la rangée et se replient dès le choix fait ;
  D · RETOUR EXACT de la fiche après POSER (jugé sur le rendu de chaque nœud), le dessin REMPLACE la dalle dans la bande, « Retirer le
      dessin » rend la dalle ; toucher la bande ouvre le dessin entier (C-051) ;
  E · JOIGNABILITÉ de chaque outil (ce qui est sous le doigt, puis un vrai toucher) et VoiceOver sur chaque outil ;
  F · les entrées : « Dessiner » en tête du menu du bouton photo (fiche, page +, fiche d'un Cercle) ; le dessin de la page + suit la parole.
Épaisseurs : 2,5 · 4,5 · 8 pt ; rangée A : PLUME · GOMME · ANNULER · COULEUR · POSER.
⚑ v133 (Tom, 6 oct. 2026) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_dessin-avant-v133.py) :
  G · SORTIR SANS POSER : un ✕ dans le contour de l'encart, à l'emplacement de « ✕ FERMER » ; le dessin en cours est gardé ; VoiceOver
      « Quitter le dessin ». C'est le SEUL nœud admis sur la surface de dessin (l'ancien contrôle C n'en admettait aucun) ;
  H · tailles et couleurs déployées à 16 pt au-dessus de la rangée (8 avant) ; la rangée CENTRÉE dans sa zone basse, entre le bas de la
      surface et le bord bas utile (844 − 34 de zone de sécurité) : écarts haut et bas égaux à 0,5 pt près ;
  I · LES COULEURS DU DESSIN SONT DANS MA PAROLE ! : sans elle, on dessine à l'encre du mode sur le champ de la nature, la zone des teintes
      est floutée (4,8 px), rien ne s'y choisit, la phrase des murs monte ; avec elle, tout se choisit (familles A et C, jouées payant).
Usage : python3 redteam_dessin.py [fichier.html] [--sonde=couleurs|partage|superpose|retour|joignable|quitter|centre|mur]
Chaque sonde fabrique la version FAUTIVE dans la page (§7) : le juge doit y rougir sur sa famille."""
import sys, io, math
from playwright.sync_api import sync_playwright
from PIL import Image
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
SONDE=next((a.split('=')[1] for a in sys.argv if a.startswith('--sonde=')), None)
TAILLES=[2.5, 4.5, 8]; OUTILS=['plume','gomme','annuler','couleur','poser']
R=[]
def ok(nom, cond, detail=''):
    R.append((nom,bool(cond))); print(('  ✅ ' if cond else '  ❌ ')+nom+((' — '+str(detail)[:300]) if (detail!='' and not cond) else ''))
EMP=r"""()=>{ const dp=document.getElementById('detailPoster'); const L=[dp].concat([...dp.querySelectorAll('*')]).filter(e=>!(e.classList&&(e.classList.contains('dz-bande')||e.classList.contains('dz-oeil')))&&!(e.closest&&e.closest('.dz-oeil'))&&!(e.closest&&e.closest('.ph-photo-nid'))).map(e=>{ const r=e.getBoundingClientRect(), c=getComputedStyle(e);
    return e.tagName+'#'+e.id+'|'+(e===dp?'':(e.getAttribute('class')||''))+'|'+[r.left,r.top,r.width,r.height].map(v=>Math.round(v*2)/2).join(',')+'|'+c.color+'|'+c.backgroundColor+'|'+c.fontFamily.split(',')[0]+'|'+c.fontSize+'|'+c.display+'|'+c.visibility+'|'+(e.id==='tenirCv'?'~':c.opacity)+'|'+(e.children.length?'':(e.textContent||'').slice(0,30)); });
  return L; }"""
PIX=r"""(q)=>{ const d=window._dessin.lit(); if(!d) return null; const k=2; const cv=window._dessin.entier({fond:d.fond, poses:q.cours?d.traits:d.poses, h:d.h}, k); const p=cv.getContext('2d').getImageData(Math.round(q.x*k), Math.round(q.y*k), 1, 1).data;
  return '#'+[p[0],p[1],p[2]].map(v=>(v<16?'0':'')+v.toString(16)).join('').toUpperCase(); }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    def page(th):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); pg.errs=[]; pg.on('pageerror', lambda e: pg.errs.append(str(e)[:160]))
        pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); try{setPremium(true)}catch(e){} try{Toile.setPalette('signal')}catch(e){}}", th); pg.wait_for_timeout(700)
        return ctx, pg
    def centre(pg, sel):
        return pg.evaluate("(s)=>{const e=[...document.querySelectorAll(s)].filter(x=>x.getBoundingClientRect().width>0)[0]; if(!e) return null; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", sel)
    def tape(pg, sel, attente=300):
        c=centre(pg, sel)
        if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(attente)
        return bool(c)
    def trait(pg, x0, y0, x1, y1, n=14):
        pg.mouse.move(20+x0,44+y0); pg.mouse.down()
        for i in range(1,n+1): pg.mouse.move(20+x0+(x1-x0)*i/n, 44+y0+(y1-y0)*i/n); pg.wait_for_timeout(9)
        pg.mouse.up(); pg.wait_for_timeout(120)
    def ouvrir_mode(pg):
        tape(pg, '#detailPoster .ph-photo-btn, #createSheet .ph-photo-btn'); r=tape(pg, '.ph-photo-menu [data-dessiner]', 450); return r and pg.evaluate("()=>!!(window._dessin&&_dessin.ouvert())")
    def etat(pg): return pg.evaluate("()=>window._dessin.etat()")
    def choisir_ton(pg, hexa):
        if not pg.evaluate("()=>!!document.querySelector('#dessinMode .dz-couleurs')"): tape(pg, '#dessinMode [data-outil=couleur]')
        return tape(pg, '#dessinMode .dz-ton[data-ton="%s"]'%hexa)

    # ═════════ fiche Promi, sombre ═════════
    ctx,pg=page('dark')
    if not pg.evaluate("()=>!!window._dessin"):
        ok("l'app porte l'outil de dessin", False, 'window._dessin absent'); b.close(); print('\nredteam_dessin : 0/1'); sys.exit(1)
    pg.evaluate("()=>{closeAll(); openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id);}"); pg.wait_for_timeout(3200)
    avant=pg.evaluate(EMP)
    # F · l'entrée
    tape(pg, '#detailPoster .ph-photo-btn')
    menu=pg.evaluate("()=>[...document.querySelectorAll('.ph-photo-menu button')].map(b=>({t:b.textContent, h:Math.round(b.getBoundingClientRect().height*2)/2, y:b.getBoundingClientRect().top}))")
    ok('F · « Dessiner » est en tête du menu du bouton photo (fiche)', bool(menu) and menu[0]['t']=='Dessiner' and all(m['y']>=menu[0]['y'] for m in menu), menu)
    ok('F · le menu est compact (33 pt de haut, 4 pt entre deux)', bool(menu) and all(abs(m['h']-33)<=1 for m in menu) and (len(menu)<2 or abs((menu[1]['y']-menu[0]['y'])-37)<=1.5), menu)
    tape(pg, '.ph-photo-menu [data-dessiner]', 450)
    ok('F · toucher « Dessiner » ouvre le mode dessin', pg.evaluate("()=>window._dessin.ouvert()"))
    if SONDE=='quitter': pg.evaluate("()=>{ const e=document.querySelector('#dessinMode .dz-quitter'); if(e) e.remove(); }")
    if SONDE=='centre': pg.evaluate("()=>{ const z=document.querySelector('#dessinMode .dz-rangee'); z.style.top=(parseFloat(z.style.top)+4)+'px'; }")
    if SONDE=='superpose': pg.evaluate("()=>{ document.querySelector('#dessinMode .dz-rangee').style.top='420px'; }")
    if SONDE=='joignable': pg.evaluate("()=>{ const v=document.createElement('div'); v.style.cssText='position:absolute;left:0;top:740px;width:390px;height:104px;z-index:5'; document.getElementById('dessinMode').appendChild(v); }")
    # C · la mise en page
    G=pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, m=document.getElementById('dessinMode'), s=m.querySelector('.dz-surface').getBoundingClientRect();
      const O=[...m.querySelectorAll('.dz-rangee button')].map(e=>{const r=e.getBoundingClientRect(); return {o:e.getAttribute('data-outil'), x:(r.left-dv.left)/k, y:(r.top-dv.top)/k, w:r.width/k, h:r.height/k, label:e.getAttribute('aria-label')}});
      let autres=0, nq=0; for(let y=4;y<(s.height/k)-2;y+=22) for(let x=6;x<390;x+=24){ const h=document.elementFromPoint(dv.left+x*k, dv.top+y*k); if(h&&h.closest('.dz-quitter')){ nq++; continue; } if(!h||h.tagName!=='CANVAS'||!h.closest('.dz-surface')) autres++; }
      const cs=getComputedStyle(m); return {couvre:Math.abs(m.getBoundingClientRect().height-dv.height)<1&&Math.abs(m.getBoundingClientRect().width-dv.width)<1, fond:cs.backgroundColor, opac:cs.opacity, surf:[(s.top-dv.top)/k,(s.bottom-dv.top)/k,(s.width)/k], O:O, autres:autres, nq:nq,
        quit:(()=>{const e=m.querySelector('.dz-quitter'); if(!e) return null; const r=e.getBoundingClientRect(), g=e.querySelector('svg').getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
          return {label:e.getAttribute('aria-label'), w:r.width/k, h:r.height/k, cx:(g.left+g.width/2-dv.left)/k, cy:(g.top+g.height/2-dv.top)/k, droite:(g.right-dv.left)/k, sous:!!(h&&h.closest('.dz-quitter')), bg:getComputedStyle(e).backgroundColor, b:getComputedStyle(e).borderTopWidth}})(), P:window._dessinParams,
        plateau:(()=>{const e=m.querySelector('.dz-plateau'), c=getComputedStyle(e), r=e.getBoundingClientRect(); return {bg:c.backgroundColor, b:c.borderTopWidth, txt:e.textContent, pe:c.pointerEvents, r:[(r.left-dv.left)/k,(r.top-dv.top)/k,r.width/k,r.height/k]}})(),
        fiche:(()=>{const h=document.elementFromPoint(dv.left+195*k, dv.top+560*k); return !!(h&&h.closest('#dessinMode'))})() }; }""")
    ok('C · le mode couvre tout l\'appareil, plein (aucune transparence)', G['couvre'] and G['opac']=='1' and 'rgba' not in G['fond'], (G['couvre'],G['fond'],G['opac']))
    ok('C · la surface de dessin part du haut de l\'écran et occupe toute la largeur', abs(G['surf'][0])<0.6 and abs(G['surf'][2]-390)<0.6, G['surf'])
    ok('C · la rangée porte PLUME · GOMME · ANNULER · COULEUR · POSER, dans cet ordre', [o['o'] for o in G['O']]==OUTILS and all(G['O'][i]['x']<G['O'][i+1]['x'] for i in range(4)), [o['o'] for o in G['O']])
    haut=min(o['y'] for o in G['O']) if G['O'] else 0; bas=max(o['y']+o['h'] for o in G['O']) if G['O'] else 0
    ok('C · la rangée est EN BAS de l\'écran, sous la surface : aucun outil sur la surface de dessin', bool(G['O']) and haut>=G['surf'][1]-0.5 and bas<=844 and haut>844-140, 'rangée %.1f → %.1f · surface jusqu\'à %.1f'%(haut,bas,G['surf'][1]))
    ok('C · la surface va jusqu\'à la rangée (la marge déclarée, pas un vide)', bool(G['O']) and abs((haut-G['surf'][1])-12)<=0.5, 'écart %.1f'%(haut-G['surf'][1]))
    UTILE=844-34   # le bord bas utile : la zone de sécurité de l'iPhone (34 pt) retirée — en dur
    eh, eb = haut-G['surf'][1], UTILE-bas
    ok('H · la rangée est CENTRÉE dans sa zone basse : écarts haut et bas égaux à 0,5 pt près', bool(G['O']) and abs(eh-eb)<=0.5 and eh>=8, 'haut %.1f · bas %.1f (bord bas utile %d)'%(eh,eb,UTILE))
    Q=G['quit']
    ok('G · un ✕ dans le contour de l\'encart, à l\'emplacement de « ✕ FERMER » (dans le plateau, calé à droite comme lui)', bool(Q) and abs(Q['cy']-70)<=1 and abs(Q['droite']-338)<=1.5 and Q['bg']=='rgba(0, 0, 0, 0)' and Q['b']=='0px', Q)
    ok('G · le ✕ est sous le doigt, 44 pt au moins, nommé « Quitter le dessin »', bool(Q) and Q['sous'] and Q['w']>=43.5 and Q['h']>=43.5 and Q['label']=='Quitter le dessin', Q)
    ok('C · rien d\'autre que la surface sous le doigt, sur toute sa hauteur — le ✕ de sortie excepté (44 pt)', G['autres']==0 and G['nq']<=6, '%d points couverts, %d sur le ✕'%(G['autres'],G['nq']))
    ok('C · l\'encart du haut ne garde que son contour : trait fin, ni fond ni texte', G['plateau']['bg']=='rgba(0, 0, 0, 0)' and G['plateau']['b']=='1px' and G['plateau']['txt']=='' and G['plateau']['pe']=='none' and [round(v) for v in G['plateau']['r']]==[24,40,342,60], G['plateau'])
    ok('C · tout le reste de la fiche s\'est retiré (le mode est devant)', G['fiche'])
    # E · joignabilité et VoiceOver
    J=pg.evaluate("""()=>[...document.querySelectorAll('#dessinMode .dz-rangee button')].map(e=>{const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return {o:e.getAttribute('data-outil'), sous:!!(h&&(h===e||e.contains(h))), label:e.getAttribute('aria-label'), w:r.width, hh:r.height}})""")
    ok('E · chaque outil de la rangée est sous le doigt, à son centre', len(J)==5 and all(j['sous'] for j in J), [(j['o'],j['sous']) for j in J])
    ok('E · chaque outil fait au moins 44 pt', len(J)==5 and all(j['w']>=43.5 and j['hh']>=43.5 for j in J), [(j['o'],j['w'],j['hh']) for j in J])
    ok('E · VoiceOver : chaque outil a son nom', len(J)==5 and all(j['label'] for j in J) and J[0]['label'].startswith('Plume') and J[1]['label'].startswith('Gomme') and J[2]['label'].startswith('Annuler') and J[3]['label']=='Couleur' and J[4]['label']=='Poser le dessin', [j['label'] for j in J])
    # le trait
    trait(pg, 60, 250, 300, 250); e=etat(pg)
    ok('le geste trace un trait (il est gardé dans le dessin)', e['traits']==1, e)
    ep=pg.evaluate("()=>{const d=window._dessin.lit(); return d.traits[0].t}")
    ok('l\'épaisseur de base est le moyen : 4,5 pt', ep==TAILLES[1], ep)
    tape(pg, '#dessinMode [data-outil=plume]')     # second toucher : les tailles
    T=pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, p=document.querySelector('#dessinMode .dz-tailles'); if(!p) return null; const r=p.getBoundingClientRect(), rg=document.querySelector('#dessinMode .dz-rangee').getBoundingClientRect();
      return {bas:(r.bottom-dv.top)/k, rangee:(rg.top-dv.top)/k, n:p.querySelectorAll('button').length, labels:[...p.querySelectorAll('button')].map(b=>b.getAttribute('aria-label')), pts:[...p.querySelectorAll('button i')].map(i=>i.getBoundingClientRect().width/k), sous:[...p.querySelectorAll('button')].every(b=>{const q=b.getBoundingClientRect(), h=document.elementFromPoint(q.left+q.width/2,q.top+q.height/2); return h===b||b.contains(h)})}; }""")
    ok('second toucher sur la plume : trois petits points, de taille croissante', bool(T) and T['n']==3 and T['pts'][0]<T['pts'][1]<T['pts'][2], T)
    ok('C · les tailles se déploient juste AU-DESSUS de la rangée', bool(T) and T['bas']<=T['rangee']+0.5 and abs((T['rangee']-T['bas'])-16)<=0.5, T)
    ok('E · les trois tailles sont sous le doigt et nommées (Fin, Moyen, Gros)', bool(T) and T['sous'] and T['labels']==['Fin','Moyen','Gros'], T)
    tape(pg, '#dessinMode [data-taille="2"]')
    ok('C · le choix fait, les tailles se replient', not pg.evaluate("()=>!!document.querySelector('#dessinMode .dz-deploi')") and etat(pg)['taille']['plume']==2)
    trait(pg, 60, 330, 300, 330)
    ok('le gros trait fait 8 pt', pg.evaluate("()=>window._dessin.lit().traits[1].t")==TAILLES[2])
    tape(pg, '#dessinMode [data-outil=annuler]'); ok('ANNULER retire le dernier trait', etat(pg)['traits']==1)
    tape(pg, '#dessinMode [data-outil=annuler]'); ok('ANNULER, à volonté : le dessin est vide', etat(pg)['traits']==0)
    ok('ANNULER n\'a plus rien à annuler : il se déclare inactif', pg.evaluate("()=>document.querySelector('#dessinMode [data-outil=annuler]').disabled"))
    # A · trois traits sous trois palettes
    PAL=['signal']+[k for k in pg.evaluate("()=>Object.keys(Toile.palettes())") if k!='signal'][:8]
    posés=[]; ys=[230,330,430]; utilises=[]
    for i in range(3):
        if i>0:
            if i==1:
                tape(pg, '#dessinMode .dz-quitter', 300)                                # v133 : on SORT par le ✕, au doigt — le dessin en cours est gardé
                ok('G · toucher le ✕ quitte le mode dessin', not pg.evaluate("()=>window._dessin.ouvert()"))
            else: pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
            # une palette dont AUCUNE teinte n'a déjà servi
            for cand in PAL[1:]:
                tn=pg.evaluate("(k)=>{ const t=Toile.palettes()[k].cols; return t.map(c=>'#'+c.slice(0,3).map(v=>(v<16?'0':'')+Math.round(v).toString(16)).join('').toUpperCase()); }", cand)
                if cand not in utilises and not any(t in [x[1] for x in posés] for t in tn): break
            pg.evaluate("(k)=>Toile.setPalette(k)", cand); utilises.append(cand); pg.wait_for_timeout(500)
            ouvrir_mode(pg)
            if i==1: ok('A · le dessin en cours est gardé si l\'on sort', etat(pg)['traits']==1, etat(pg))
        ch=pg.evaluate("()=>window._dessin.choix()"); e=etat(pg)
        ton=[t for t in ch['trait'][:4] if t!=e['fond'] and t not in [x[1] for x in posés]][0]
        choisir_ton(pg, ton)
        ok('C · la couleur choisie, le panneau se replie (trait %d)'%(i+1), not pg.evaluate("()=>!!document.querySelector('#dessinMode .dz-deploi')") and etat(pg)['couleur']==ton, etat(pg))
        trait(pg, 60, ys[i], 300, ys[i]); posés.append((ys[i], ton))
    ok('A · trois traits, sous trois palettes, de trois teintes différentes', len(set(t for _,t in posés))==3, posés)
    if SONDE=='couleurs': pg.evaluate("()=>{ const d=window._dessin.lit(), m=Toile.mondeCourant(), t=Toile.tonsDe(m.p,m.h)[1], h='#'+t.map(v=>(v<16?'0':'')+Math.round(v).toString(16)).join('').toUpperCase(); d.traits.forEach(x=>{ x.c=h; }); }")
    data=pg.evaluate("()=>window._dessin.lit().traits.map(t=>t.c)")
    ok('A · chaque trait garde SA couleur dans le dessin (les données)', data==[t for _,t in posés], (data, posés))
    lus=[pg.evaluate(PIX, {'x':180,'y':y,'cours':True}) for y,_ in posés]
    ok('A · chaque trait garde SA couleur à l\'image (lue sur le rendu)', lus==[t for _,t in posés], (lus, posés))
    # le panneau des couleurs, avant le premier POSER
    tape(pg, '#dessinMode [data-outil=couleur]')
    C=pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, p=document.querySelector('#dessinMode .dz-couleurs'); if(!p) return null; const r=p.getBoundingClientRect(), rg=document.querySelector('#dessinMode .dz-rangee').getBoundingClientRect();
      const m=Toile.mondeCourant(), pal=Toile.tonsDe(m.p,m.h).map(t=>'#'+t.map(v=>(v<16?'0':'')+Math.round(v).toString(16)).join('').toUpperCase());
      return {bas:(r.bottom-dv.top)/k, rangee:(rg.top-dv.top)/k, onglets:[...p.querySelectorAll('.dz-onglet')].map(e=>e.textContent+'|'+e.getAttribute('aria-selected')), tons:[...p.querySelectorAll('.dz-ton')].map(e=>({t:e.getAttribute('data-ton'), off:e.disabled, label:e.getAttribute('aria-label')})), pal:pal, fond:window._dessin.etat().fond,
        sous:[...p.querySelectorAll('button')].every(b=>{const q=b.getBoundingClientRect(), h=document.elementFromPoint(q.left+q.width/2,q.top+q.height/2); return h===b||b.contains(h)}), sym:!!document.querySelector('#dessinMode [data-outil=couleur] svg')}; }""")
    ok('COULEUR : les onglets TRAIT et FOND, tant que le dessin n\'a jamais été posé', bool(C) and [o.split('|')[0] for o in C['onglets']]==['Trait','Fond'], C and C['onglets'])
    ok('COULEUR : les teintes sont celles de la palette du Studio EN COURS', bool(C) and all(t in [x['t'] for x in C['tons']] for t in C['pal']), C and (C['pal'],[x['t'] for x in C['tons']]))
    ok('COULEUR : la teinte du fond est grisée pour le trait', bool(C) and all((x['off']==(x['t']==C['fond'])) for x in C['tons']), C and C['tons'])
    ok('C · les couleurs se déploient juste AU-DESSUS de la rangée', bool(C) and C['bas']<=C['rangee']+0.5 and abs((C['rangee']-C['bas'])-16)<=0.5, C and (C['bas'],C['rangee']))
    ok('E · onglets et teintes sont sous le doigt, nommés pour VoiceOver', bool(C) and C['sous'] and all(x['label'] for x in C['tons']), C and C['tons'])
    tape(pg, '#dessinMode [data-onglet=FOND]'); fonds=pg.evaluate("()=>[...document.querySelectorAll('#dessinMode .dz-ton')].map(e=>e.getAttribute('data-ton'))")
    nouveau=[t for t in fonds if t not in [x[1] for x in posés] and t!=C['fond']][0] if C else None
    tape(pg, '#dessinMode .dz-ton[data-ton="%s"]'%nouveau)
    ok('COULEUR · FOND : la teinte choisie devient le fond du dessin', etat(pg)['fond']==nouveau and pg.evaluate(PIX, {'x':20,'y':600,'cours':True})==nouveau, (etat(pg)['fond'], nouveau))
    # la gomme
    tape(pg, '#dessinMode [data-outil=gomme]'); trait(pg, 180, 200, 180, 260, 8)
    ok('la gomme efface le trait là où elle passe, et rend le fond', pg.evaluate(PIX, {'x':180,'y':230,'cours':True})==nouveau and pg.evaluate(PIX, {'x':90,'y':230,'cours':True})==posés[0][1], (pg.evaluate(PIX, {'x':180,'y':230,'cours':True}), nouveau))
    tape(pg, '#dessinMode [data-outil=annuler]')       # on rend le trait
    # D · POSER
    if SONDE=='retour': pg.evaluate("()=>{ const s=window._dessin.sort; }")
    tape(pg, '#dessinMode [data-outil=poser]', 900)
    if SONDE=='retour': pg.evaluate("()=>{ document.getElementById('dptTitre').style.setProperty('transform','translateY(9px)','important'); }")
    pg.wait_for_timeout(900)
    ok('D · POSER referme le mode, sans rien laisser (ni panneau, ni outil)', not pg.evaluate("()=>window._dessin.ouvert()") and pg.evaluate("()=>{const m=document.getElementById('dessinMode'); return getComputedStyle(m).display==='none' && !m.querySelector('.dz-deploi') && !m.querySelector('.dz-rangee button')}"))
    apres=pg.evaluate(EMP); diff=[(a,c) for a,c in zip(avant,apres) if a!=c]
    ok('D · retour exact de la fiche après POSER (place, couleur, police, texte de chaque nœud ; %d nœuds)'%len(avant), len(avant)==len(apres) and not diff, diff[:2])
    B=pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, c=document.querySelector('#detailPoster > canvas.dz-bande'), cv=document.getElementById('dpTrameCv'); if(!c) return null; const r=c.getBoundingClientRect(), cs=getComputedStyle(c);
      return {haut:(r.top-dv.top)/k, larg:r.width/k, h:r.height/k, disp:cs.display, op:cs.opacity, pe:cs.pointerEvents, apres:c.previousElementSibling===cv, sous:(()=>{const h=document.elementFromPoint(dv.left+195*k, dv.top+220*k); return h&&(h.id||h.tagName)})()}; }""")
    ok('D · le dessin est dans la bande : une couche pleine, calée en haut, sur toute la largeur', bool(B) and abs(B['haut'])<0.6 and abs(B['larg']-390)<0.6 and B['disp']=='block' and B['op']=='1' and B['h']>150, B)
    im=Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); px=im.getpixel((int((20+180)*2), int((44+230)*2))); px2=im.getpixel((int((20+30)*2), int((44+140)*2)))
    def h3(c): return '#%02X%02X%02X'%c
    ok('D · à l\'écran, la bande montre le dessin — son trait et son fond — à la place de la dalle (capture)', h3(px)==posés[0][1] and h3(px2)==nouveau, (h3(px),posés[0][1],h3(px2),nouveau))
    lus=[pg.evaluate(PIX, {'x':180,'y':y}) for y,_ in posés]
    ok('A · posé, chaque trait a toujours SA couleur', lus==[t for _,t in posés], (lus,posés))
    # C-051 : la vue entière
    lab=pg.evaluate("()=>document.getElementById('dpTrameCv').getAttribute('aria-label')")
    pg.touchscreen.tap(20+195, 44+215); pg.wait_for_timeout(500)
    V=pg.evaluate("()=>{const v=document.getElementById('entierVue'); if(!v||!v.classList.contains('ouv')) return null; const im=v.querySelector('img'); return {label:v.getAttribute('aria-label'), nat:[im.naturalWidth, im.naturalHeight]}}")
    ok('D · toucher la bande ouvre le dessin ENTIER (C-051), plus haut que la bande', bool(V) and V['label']=='Le dessin en entier' and V['nat'][1]/max(1,V['nat'][0])>1.5 and lab=='Voir le dessin en entier', (V,lab))
    pg.evaluate("()=>window._entier&&_entier.ferme()"); pg.wait_for_timeout(300)
    # après le premier POSER : fond fixé, couleurs présentes seulement
    ouvrir_mode(pg); tape(pg, '#dessinMode [data-outil=couleur]')
    A2=pg.evaluate("()=>({onglets:[...document.querySelectorAll('#dessinMode .dz-onglet')].map(e=>e.textContent), tons:[...document.querySelectorAll('#dessinMode .dz-ton')].map(e=>e.getAttribute('data-ton'))})")
    ok('A · après le premier POSER, le fond est fixé : plus d\'onglet FOND', A2['onglets']==['Trait'], A2)
    ok('A · après le premier POSER, les nouveaux traits ne prennent que les couleurs déjà présentes dans le dessin', sorted(A2['tons'])==sorted(set(t for _,t in posés)), (A2['tons'],posés))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    # B · le masquage
    pid=pg.evaluate("()=>cur.id")
    O=pg.evaluate("()=>{const e=document.querySelector('#detailPoster > .dz-oeil'); if(!e) return null; const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2); return {label:e.getAttribute('aria-label'), sous:h===e||e.contains(h), w:r.width}}")
    ok('B · un petit bouton discret, dans un coin de la bande : « Masquer le dessin »', bool(O) and O['label']=='Masquer le dessin' and O['sous'] and O['w']<=36, O)
    ok('B · non masqué, le dessin part dans le partage', pg.evaluate("(id)=>!!window._dessinCase(id)", pid))
    tape(pg, '#detailPoster > .dz-oeil', 500)
    if SONDE=='partage': pg.evaluate("()=>{ window._dessinCase=function(pid){ const p=promises.filter(x=>x.id===pid)[0]; return (p&&p.dessin&&p.dessin.poses&&p.dessin.poses.length)?window._dessin.entier(p.dessin,2):null; }; }")
    Mq=pg.evaluate("(id)=>({masque:promises.find(p=>p.id===id).dessin.masque, bande:!!document.querySelector('#detailPoster > canvas.dz-bande'), label:(document.querySelector('#detailPoster > .dz-oeil')||{getAttribute(){return null}}).getAttribute('aria-label'), cas:!!window._dessinCase(id)})", pid)
    ok('B · masqué : la bande rend la dalle, le bouton propose « Afficher le dessin »', Mq['masque'] and not Mq['bande'] and Mq['label']=='Afficher le dessin', Mq)
    ok('B · un dessin masqué n\'est JAMAIS emporté dans un partage (la case rend la dalle)', not Mq['cas'], Mq)
    # … et à l'image du partage : la planche de cette parole ne porte pas le fond du dessin
    def partage_porte(couleur):
        pg.evaluate("()=>{ try{ window.ouvrirPartage(); }catch(e){} }"); pg.wait_for_timeout(2600)
        n=pg.evaluate("""(c)=>{ const cvs=[...document.querySelectorAll('#shareScreen canvas')].filter(x=>x.getBoundingClientRect().width>60); let n=0; const R=parseInt(c.slice(1,3),16),G=parseInt(c.slice(3,5),16),B=parseInt(c.slice(5,7),16);
          cvs.forEach(cv=>{ try{ const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data; for(let i=0;i<d.length;i+=16){ if(d[i+3]>250&&Math.abs(d[i]-R)+Math.abs(d[i+1]-G)+Math.abs(d[i+2]-B)<5) n++; } }catch(e){} }); return n; }""", couleur)
        pg.evaluate("()=>{ const x=document.querySelector('#shareScreen .closeb'); if(x) x.click(); }"); pg.wait_for_timeout(700)
        if not pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"): pg.evaluate("(id)=>{closeAll(); openDetail(id)}", pid); pg.wait_for_timeout(2500)
        return n
    pg.evaluate("(id)=>{ const d=promises.find(p=>p.id===id).dessin; d.fond='#12FF34'; }", pid)      # un fond qu'aucune palette ne porte : on le cherche à l'image
    n_masque=partage_porte('#12FF34')
    ok('B · à l\'image du partage, rien du dessin masqué (0 pixel de son fond)', n_masque==0, '%d pixels'%n_masque)
    tape(pg, '#detailPoster > .dz-oeil', 500)
    n_montre=partage_porte('#12FF34')
    ok('B · affiché de nouveau, le dessin est dans l\'image du partage', n_montre>50, '%d pixels'%n_montre)
    ok('B · le masquage est mémorisé avec la fiche (sauvegardé)', pg.evaluate("(id)=>{ const s=JSON.parse(localStorage.getItem('promi_state')||'{}'); const p=(s.promises||[]).find(p=>p.id===id); return !!(p&&p.dessin&&p.dessin.masque===false&&p.dessin.poses.length) }", pid))
    # « Retirer le dessin » rend la dalle
    tape(pg, '#detailPoster .ph-photo-btn'); items=pg.evaluate("()=>[...document.querySelectorAll('.ph-photo-menu button')].map(b=>b.textContent)")
    pg.evaluate("()=>{ const b=[...document.querySelectorAll('.ph-photo-menu button')].find(x=>x.textContent==='Retirer le dessin'); if(b){ const r=b.getBoundingClientRect(); window.__c=[r.left+r.width/2,r.top+r.height/2]; } else window.__c=null; }")
    c=pg.evaluate("()=>window.__c")
    if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(700)
    ok('D · « Retirer le dessin » rend la dalle (plus de couche, plus de bouton de masquage, plus de dessin)', 'Retirer le dessin' in items and items[0]=='Dessiner' and pg.evaluate("(id)=>!promises.find(p=>p.id===id).dessin && !document.querySelector('#detailPoster > .dz-bande') && !document.querySelector('#detailPoster > .dz-oeil')", pid), items)
    ok('aucune erreur de page (fiche Promi)', not pg.errs, pg.errs[:2]); ctx.close()

    # ═════════ I · sans Ma Parole ! (v133, C-061) : deux thèmes ═════════
    for th in ('dark','light'):
        ctx,pg=page(th); pg.evaluate("()=>{ setPremium(false); try{localStorage.setItem('promi_murs',JSON.stringify({n:0,t:Date.now(),der:null,decouvert:1}))}catch(e){} closeAll(); openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id);}"); pg.wait_for_timeout(3000)
        ouvrir_mode(pg); e=etat(pg)
        ENC={'dark':'#F7F0DE','light':'#201908'}[th]
        ok('I · [%s] sans Ma Parole ! : on dessine à l\'encre du mode, sur le champ de la nature'%th, e['couleur']==ENC and e['fond']=='#82AEF8', (e['couleur'],e['fond']))
        tape(pg, '#dessinMode [data-outil=couleur]')
        if SONDE=='mur': pg.evaluate("()=>{ const s=document.createElement('style'); s.textContent='#device #dessinMode .dz-couleurs.dz-mur > *{filter:none!important;-webkit-filter:none!important;pointer-events:auto!important}'; document.head.appendChild(s); const q=document.querySelector('#dessinMode .dz-couleurs'); q.classList.remove('dz-mur'); }")
        Mu=pg.evaluate("""()=>{ const q=document.querySelector('#dessinMode .dz-couleurs'); if(!q) return null; const k=[...q.children];
          return {mur:q.classList.contains('dz-mur'), flous:k.map(e=>getComputedStyle(e).filter||getComputedStyle(e).webkitFilter), pe:k.map(e=>getComputedStyle(e).pointerEvents), n:k.length, label:q.getAttribute('aria-label')}; }""")
        ok('I · [%s] la zone des teintes est floutée (4,8 px), en entier'%th, bool(Mu) and Mu['n']>=4 and all(f=='blur(4.8px)' for f in Mu['flous']), Mu)
        t0=pg.evaluate("()=>{ const e=[...document.querySelectorAll('#dessinMode .dz-ton')].filter(x=>x.getAttribute('data-ton')!=='#82AEF8')[0]; const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, e.getAttribute('data-ton')] }")
        pg.touchscreen.tap(t0[0], t0[1]); pg.wait_for_timeout(800); e2=etat(pg) if pg.evaluate("()=>window._dessin.ouvert()") else {'couleur':None,'fond':None}
        ok('I · [%s] toucher une teinte ne choisit rien'%th, e2['couleur']==ENC and e2['fond']=='#82AEF8', (e2['couleur'],e2['fond'],t0[2]))
        Ph=pg.evaluate("""()=>{ const p=document.getElementById('murPhrase'); if(!p) return null; const m=p.querySelector('.mp'), q=document.querySelector('#dessinMode .dz-couleurs'); const r=p.getBoundingClientRect(), w=q?q.getBoundingClientRect():r;
          const h=document.elementFromPoint(r.left+8, r.top+r.height/2);
          return {leve:p.classList.contains('leve'), texte:p.textContent, mp:m?getComputedStyle(m).color:null, coul:getComputedStyle(p).color, dans:r.top>=w.top-1&&r.bottom<=w.bottom+1, z:+getComputedStyle(p).zIndex} }""")
        MPC={'dark':'rgb(254, 208, 195)','light':'rgb(251, 76, 13)'}[th]   # v134 : #FED0C3 sur le bleu définitif #0E78F2
        ok('I · [%s] la phrase des murs monte sur la zone, devant le mode, « Ma Parole ! » dans son orange'%th, bool(Ph) and Ph['leve'] and 'Ma Parole' in Ph['texte'] and Ph['mp']==MPC and Ph['dans'] and Ph['z']>390, Ph)
        pg.evaluate("()=>{window._murBaisse&&_murBaisse()}"); pg.wait_for_timeout(200)
        # avec Ma Parole ! : la même zone, nette, et la teinte se choisit
        pg.evaluate("()=>{ window._dessin.sort&&0; }"); pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
        pg.evaluate("()=>setPremium(true)"); pg.wait_for_timeout(300); ouvrir_mode(pg); tape(pg, '#dessinMode [data-outil=couleur]')
        Av=pg.evaluate("()=>{ const q=document.querySelector('#dessinMode .dz-couleurs'); return q?{mur:q.classList.contains('dz-mur'), flous:[...q.children].map(e=>getComputedStyle(e).filter)}:null }")
        ch=pg.evaluate("()=>window._dessin.choix()"); ton=[t for t in ch['trait'] if t not in (ENC, '#82AEF8')][0]; choisir_ton(pg, ton)
        ok('I · [%s] avec Ma Parole ! : rien de flouté, la teinte touchée est choisie'%th, bool(Av) and not Av['mur'] and all(f=='none' for f in Av['flous']) and etat(pg)['couleur']==ton, (Av, etat(pg)['couleur'], ton))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200); pg.evaluate("()=>{ try{ window._dessin.retire&&window._dessin.retire(); }catch(e){} }")
        ok('aucune erreur de page (sans Ma Parole !, %s)'%th, not pg.errs, pg.errs[:2]); ctx.close()

    # ═════════ fiche d'un Cercle et page +, clair ═════════
    ctx,pg=page('light')
    pg.evaluate("()=>{closeAll(); openEssaim('potager');}"); pg.wait_for_timeout(3200)
    tape(pg, '#detailPoster .ph-photo-btn'); menu=pg.evaluate("()=>[...document.querySelectorAll('.ph-photo-menu button')].map(b=>b.textContent)")
    ok('F · la fiche d\'un Cercle a son bouton photo : il propose « Dessiner »', menu[:1]==['Dessiner'], menu)
    tape(pg, '.ph-photo-menu [data-dessiner]', 450); trait(pg, 60, 130, 300, 130); tape(pg, '#dessinMode [data-outil=poser]', 900)
    ok('F · un Cercle garde son dessin, sa bande le montre', pg.evaluate("()=>!!document.querySelector('#detailPoster > canvas.dz-bande') && !!JSON.parse(localStorage.getItem('promi_dessins_cercle')||'{}').potager"))
    for nat,idx in (('un Promi',0),('un Chiche',1),('un Cercle',2)):
        pg.evaluate("(i)=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][i]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}", idx); pg.wait_for_timeout(3600)
        tape(pg, '#createSheet .ph-photo-btn'); menu=pg.evaluate("()=>[...document.querySelectorAll('.ph-photo-menu button')].map(b=>b.textContent)")
        ok('F · page + (%s) : « Dessiner » en tête du menu du bouton photo'%nat, menu[:1]==['Dessiner'], menu)
        pg.evaluate("()=>window._photoMenuFerme&&_photoMenuFerme()")
    # le dessin de la page + suit la parole plantée
    pg.evaluate("()=>{closeAll(); document.getElementById('createBtn').click(); var n=0; (function essai(){ var cs=document.getElementById('createSheet'); var x=[...document.querySelectorAll('#createSheet .tile')][0]; if(cs&&cs.classList.contains('pp-choix')&&x){ x.click(); } if(++n<6) setTimeout(essai,350); })();}"); pg.wait_for_timeout(3600)
    tape(pg, '#createSheet .ph-photo-btn'); tape(pg, '.ph-photo-menu [data-dessiner]', 450); trait(pg, 60, 160, 300, 160); tape(pg, '#dessinMode [data-outil=poser]', 900)
    ok('F · page + : le dessin posé paraît dans la bande de la page +', pg.evaluate("()=>!!document.querySelector('#createSheet > canvas.dz-bande')"))
    pg.evaluate("()=>{ const f=document.getElementById('fTitle'); f.value='parole dessinée'; f.dispatchEvent(new Event('input',{bubbles:true})); document.getElementById('addPromi').click(); }"); pg.wait_for_timeout(3200)
    ok('F · à la plantation, le dessin de la page + suit la parole', pg.evaluate("()=>{ const p=promises.filter(q=>q.title==='parole dessinée')[0]; return !!(p&&p.dessin&&p.dessin.poses&&p.dessin.poses.length===1) && !(window._phrase||{}).dessin }"))
    ok('aucune erreur de page (Cercle, page +)', not pg.errs, pg.errs[:2]); ctx.close()
    b.close()
n=sum(1 for _,c in R if c); print('\nredteam_dessin%s : %d/%d'%((' [sonde %s]'%SONDE) if SONDE else '', n, len(R)))
for nom,c in R:
    if not c: print('   ROUGE :', nom)
sys.exit(0 if n==len(R) else 1)
