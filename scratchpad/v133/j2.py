import io, ast
S=io.open('redteam_dessin.py',encoding='utf-8').read()
def r(a,b,n=1):
    global S
    assert S.count(a)==n,(a[:70],S.count(a)); S=S.replace(a,b)
r("""Usage : python3 redteam_dessin.py [fichier.html] [--sonde=couleurs|partage|superpose|retour|joignable]""",
"""⚑ v133 (Tom, 6 oct. 2026) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_dessin-avant-v133.py) :
  G · SORTIR SANS POSER : un ✕ dans le contour de l'encart, à l'emplacement de « ✕ FERMER » ; le dessin en cours est gardé ; VoiceOver
      « Quitter le dessin ». C'est le SEUL nœud admis sur la surface de dessin (l'ancien contrôle C n'en admettait aucun) ;
  H · tailles et couleurs déployées à 16 pt au-dessus de la rangée (8 avant) ; la rangée CENTRÉE dans sa zone basse, entre le bas de la
      surface et le bord bas utile (844 − 34 de zone de sécurité) : écarts haut et bas égaux à 0,5 pt près ;
  I · LES COULEURS DU DESSIN SONT DANS MA PAROLE ! : sans elle, on dessine à l'encre du mode sur le champ de la nature, la zone des teintes
      est floutée (4,8 px), rien ne s'y choisit, la phrase des murs monte ; avec elle, tout se choisit (familles A et C, jouées payant).
Usage : python3 redteam_dessin.py [fichier.html] [--sonde=couleurs|partage|superpose|retour|joignable|quitter|centre|mur]""")
r("""setTheme(t); try{Toile.setPalette('signal')}catch(e){}}", th)""","""setTheme(t); try{setPremium(true)}catch(e){} try{Toile.setPalette('signal')}catch(e){}}", th)""")
# la surface : seul le ✕ y est admis
r("""if(!h||h.tagName!=='CANVAS'||!h.closest('.dz-surface')) autres++; }""","""if(h&&h.closest('.dz-quitter')){ nq++; continue; } if(!h||h.tagName!=='CANVAS'||!h.closest('.dz-surface')) autres++; }""")
r("""let autres=0; for(let y=4;""","""let autres=0, nq=0; for(let y=4;""")
r("""surf:[(s.top-dv.top)/k,(s.bottom-dv.top)/k,(s.width)/k], O:O, autres:autres,""","""surf:[(s.top-dv.top)/k,(s.bottom-dv.top)/k,(s.width)/k], O:O, autres:autres, nq:nq,
        quit:(()=>{const e=m.querySelector('.dz-quitter'); if(!e) return null; const r=e.getBoundingClientRect(), g=e.querySelector('svg').getBoundingClientRect(), h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
          return {label:e.getAttribute('aria-label'), w:r.width/k, h:r.height/k, cx:(g.left+g.width/2-dv.left)/k, cy:(g.top+g.height/2-dv.top)/k, droite:(g.right-dv.left)/k, sous:!!(h&&h.closest('.dz-quitter')), bg:getComputedStyle(e).backgroundColor, b:getComputedStyle(e).borderTopWidth}})(),""")
r("""0<=haut-G['surf'][1]<=G['P']['MARGE_HAUT']+0.6, 'écart %.1f'%(haut-G['surf'][1]))""","""abs((haut-G['surf'][1])-12)<=0.5, 'écart %.1f'%(haut-G['surf'][1]))
    UTILE=844-34   # le bord bas utile : la zone de sécurité de l'iPhone (34 pt) retirée — en dur
    eh, eb = haut-G['surf'][1], UTILE-bas
    ok('H · la rangée est CENTRÉE dans sa zone basse : écarts haut et bas égaux à 0,5 pt près', bool(G['O']) and abs(eh-eb)<=0.5 and eh>=8, 'haut %.1f · bas %.1f (bord bas utile %d)'%(eh,eb,UTILE))
    Q=G['quit']
    ok('G · un ✕ dans le contour de l\\'encart, à l\\'emplacement de « ✕ FERMER » (dans le plateau, calé à droite comme lui)', bool(Q) and abs(Q['cy']-70)<=1 and abs(Q['droite']-338)<=1.5 and Q['bg']=='rgba(0, 0, 0, 0)' and Q['b']=='0px', Q)
    ok('G · le ✕ est sous le doigt, 44 pt au moins, nommé « Quitter le dessin »', bool(Q) and Q['sous'] and Q['w']>=43.5 and Q['h']>=43.5 and Q['label']=='Quitter le dessin', Q)""")
r("""ok('C · rien d\\'autre que la surface sous le doigt, sur toute sa hauteur', G['autres']==0, '%d points couverts'%G['autres'])""",
"""ok('C · rien d\\'autre que la surface sous le doigt, sur toute sa hauteur — le ✕ de sortie excepté (44 pt)', G['autres']==0 and G['nq']<=6, '%d points couverts, %d sur le ✕'%(G['autres'],G['nq']))""")
r("""T['rangee']-T['bas']<=G['P']['ECART_DEPLOI']+0.6, T)""","""abs((T['rangee']-T['bas'])-16)<=0.5, T)""")
r("""C['rangee']-C['bas']<=G['P']['ECART_DEPLOI']+0.6, C and (C['bas'],C['rangee']))""","""abs((C['rangee']-C['bas'])-16)<=0.5, C and (C['bas'],C['rangee']))""")
# la sortie par le ✕ (au doigt) au lieu d'Échap, une fois
r("""            pg.keyboard.press('Escape'); pg.wait_for_timeout(250)                       # on SORT : le dessin en cours est gardé""",
"""            if i==1:
                tape(pg, '#dessinMode .dz-quitter', 300)                                # v133 : on SORT par le ✕, au doigt — le dessin en cours est gardé
                ok('G · toucher le ✕ quitte le mode dessin', not pg.evaluate("()=>window._dessin.ouvert()"))
            else: pg.keyboard.press('Escape'); pg.wait_for_timeout(250)""")
# sondes
r("""    if SONDE=='superpose':""","""    if SONDE=='quitter': pg.evaluate("()=>{ const e=document.querySelector('#dessinMode .dz-quitter'); if(e) e.remove(); }")
    if SONDE=='centre': pg.evaluate("()=>{ const z=document.querySelector('#dessinMode .dz-rangee'); z.style.top=(parseFloat(z.style.top)+4)+'px'; }")
    if SONDE=='superpose':""")
# la famille I, avant le Cercle
a="""    ok('aucune erreur de page (fiche Promi)', not pg.errs, pg.errs[:2]); ctx.close()
"""
I='''
    # ═════════ I · sans Ma Parole ! (v133, C-061) : deux thèmes ═════════
    for th in ('dark','light'):
        ctx,pg=page(th); pg.evaluate("()=>{ setPremium(false); try{localStorage.setItem('promi_murs',JSON.stringify({n:0,t:Date.now(),der:null,decouvert:1}))}catch(e){} closeAll(); openDetail(promises.filter(q=>q.title==='faire les crêpes')[0].id);}"); pg.wait_for_timeout(3000)
        ouvrir_mode(pg); e=etat(pg)
        ENC={'dark':'#F7F0DE','light':'#201908'}[th]
        ok('I · [%s] sans Ma Parole ! : on dessine à l\\'encre du mode, sur le champ de la nature'%th, e['couleur']==ENC and e['fond']=='#82AEF8', (e['couleur'],e['fond']))
        tape(pg, '#dessinMode [data-outil=couleur]')
        if SONDE=='mur': pg.evaluate("()=>{ const s=document.createElement('style'); s.textContent='#device #dessinMode .dz-couleurs.dz-mur > *{filter:none!important;-webkit-filter:none!important;pointer-events:auto!important}'; document.head.appendChild(s); const q=document.querySelector('#dessinMode .dz-couleurs'); q.classList.remove('dz-mur'); }")
        Mu=pg.evaluate("""()=>{ const q=document.querySelector('#dessinMode .dz-couleurs'); if(!q) return null; const k=[...q.children];
          return {mur:q.classList.contains('dz-mur'), flous:k.map(e=>getComputedStyle(e).filter||getComputedStyle(e).webkitFilter), pe:k.map(e=>getComputedStyle(e).pointerEvents), n:k.length, label:q.getAttribute('aria-label')}; }""")
        ok('I · [%s] la zone des teintes est floutée (4,8 px), en entier'%th, bool(Mu) and Mu['n']>=4 and all(f=='blur(4.8px)' for f in Mu['flous']), Mu)
        t0=pg.evaluate("()=>{ const e=document.querySelector('#dessinMode .dz-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2, e.getAttribute('data-ton')] }")
        pg.touchscreen.tap(t0[0], t0[1]); pg.wait_for_timeout(800); e2=etat(pg) if pg.evaluate("()=>window._dessin.ouvert()") else {'couleur':None,'fond':None}
        ok('I · [%s] toucher une teinte ne choisit rien'%th, e2['couleur']==ENC and e2['fond']=='#82AEF8', (e2['couleur'],e2['fond'],t0[2]))
        Ph=pg.evaluate("""()=>{ const p=document.getElementById('murPhrase'); if(!p) return null; const m=p.querySelector('.mp'), q=document.querySelector('#dessinMode .dz-couleurs'); const r=p.getBoundingClientRect(), w=q?q.getBoundingClientRect():r;
          const h=document.elementFromPoint(r.left+8, r.top+r.height/2);
          return {leve:p.classList.contains('leve'), texte:p.textContent, mp:m?getComputedStyle(m).color:null, coul:getComputedStyle(p).color, dans:r.top>=w.top-1&&r.bottom<=w.bottom+1, z:+getComputedStyle(p).zIndex} }""")
        MPC={'dark':'rgb(255, 159, 132)','light':'rgb(251, 76, 13)'}[th]
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
'''
assert S.count(a)==1; S=S.replace(a,a+I)
ast.parse(S); io.open('redteam_dessin.py','w',encoding='utf-8').write(S)

M=io.open('redteam_photo_menu.py',encoding='utf-8').read()
n=M.count('Importer une image'); M=M.replace('Importer une image','Importer une photo')
M=M.replace("MOTS = ['Importer une photo',","# ⚑ v133 (Tom, 6 oct. 2026) — contrat réécrit (original : sauvegardes/redteam_photo_menu-avant-v133.py) : « Importer une image » devient « Importer une photo »\nMOTS = ['Importer une photo',")
ast.parse(M); io.open('redteam_photo_menu.py','w',encoding='utf-8').write(M); print(n)
