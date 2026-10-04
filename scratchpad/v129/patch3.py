import io
S=io.open('app.html',encoding='utf-8').read()
a=u"""ta première dalle sur ta Toile. Plus qu’à le tenir.</span>"""
assert S.count(a)==1
S=S.replace(a,u"""ta première dalle sur ta Toile. Plus qu’à le tenir.</span>""")
a=u"""<span>Le reste se découvre en traçant. La suite t’appartient.</span>"""
assert S.count(a)==1
S=S.replace(a,u"""<span>Le reste se découvre en traçant. La suite t’appartient.</span>""")
io.open('app.html','w',encoding='utf-8').write(S)
O=io.open('scratchpad/v128/dessin/ov.js',encoding='utf-8').read()
def rep(a,b):
    global O
    assert O.count(a)==1,a[:60]; O=O.replace(a,b)
rep("    var sx=W/r.width, ox=","    if(!c.epure){ var sx=W/r.width, ox=")
rep("g.closePath(); g.fill(); g.globalCompositeOperation='source-over';\n    o.appendChild(k); }","g.closePath(); g.fill(); g.globalCompositeOperation='source-over'; }\n    o.appendChild(k); }")
rep("  function montre(c){","""  /* v129 — LE MODE DESSIN LIBÈRE L'ÉCRAN : les disques et leurs noms disparaissent ; l'encart du haut ne garde que son contour, au trait fin */
  function epure(o, c){ var P=document.getElementById('detailPoster'), dv=document.getElementById('device').getBoundingClientRect();
    function cache(e){ if(!e) return; e.setAttribute('data-ov-cache','1'); e.style.visibility='hidden'; }
    var toi=[].filter.call(P.querySelectorAll('*'), function(e){ return e.children.length===0 && (e.textContent||'').trim()==='Toi'; })[0];
    if(toi){ var n=toi; while(n.parentElement && n.parentElement!==P && n.getBoundingClientRect().width<200) n=n.parentElement; cache(n); }
    [].forEach.call(P.querySelectorAll('.enh'), function(e){ var r=e.getBoundingClientRect(); if(r.top-dv.top<110) cache(e); });
    o.appendChild(el('left:24px;top:40px;width:342px;height:60px;border-radius:30px;border:1px solid #201908;background:transparent')); }
  function montre(c){""")
rep("    if(c.sansDalle) sansDalle(o, c);","    if(c.sansDalle) sansDalle(o, c);\n    if(c.epure) epure(o, c);")
io.open('scratchpad/v129/dessin/ov.js','w',encoding='utf-8').write(O)
D=io.open('scratchpad/v128/dessin/dessin.py',encoding='utf-8').read()
i=D.index("def parcours(pg, nat, th, seulement=None):"); j=D.index("with sync_playwright() as p:")
D=D[:i]+'''def parcours(pg, nat, th, seulement=None):
    pg.evaluate("()=>OV.nettoie()"); pg.evaluate(FICHES[nat]); pg.wait_for_timeout(3000)
    L=(th=='light'); C=[]
    mode=dict(nat=nat, light=L); mode.update(GEO[nat]); mode.pop('descend',None); mode.update(sansDalle=1, epure=1, cachePhoto=1, dessin='simple', sel='plume')
    def e(lab, nom, c):
        if seulement and nom not in seulement: return
        pg.evaluate("(c)=>{OV.montre(c)}", c); C.append((lab, prise(pg,'%s-%s-%s'%(nat,nom,th))))
    def sansB(c): c=dict(c); c.pop('cacheBas',None); return c
    e('3 · mode dessin épuré — rangée A','3A', dict(mode, compo='A'))
    e('3 · rangée B (au bas de la bande)','3B', sansB(dict(mode, compo='B')))
    e('3 · rangée C (icônes + mots)','3C', dict(mode, compo='C'))
    e('4 · la taille déployée','4', dict(mode, compo='A', etat='tailles', taille=1))
    e('5 · la couleur déployée — S1','5S1', dict(mode, compo='A', sel='couleur', symbole='S1', etat='couleur', onglet='TRAIT', tonChoisi=4))
    e('5 · la couleur déployée — S2','5S2', dict(mode, compo='A', sel='couleur', symbole='S2', etat='couleur', onglet='TRAIT', tonChoisi=4))
    e('6 · un mot et un dessin — E1','6E1', dict(mode, compo='A', effile='E1'))
    e('6 · un mot et un dessin — E2','6E2', dict(mode, compo='A', effile='E2'))
    pg.evaluate("()=>OV.nettoie()"); return C
'''+D[j:]
i=D.index("        if th=='light':"); j=D.index("        ctx.close()")
D=D[:i]+'''        if th=='light':
            for nat in ('promi','cercle'):
                C=parcours(pg, nat, th)
                planche('C-042 · le mode dessin libère l\\'écran — %s (clair)'%NOM[nat], C, 4, 'planche-v129/dessin-epure-%s.png'%nat)
                planche('C-042 · %s · rangées A, B, C'%NOM[nat], C[:3], 3, 'planche-v129/dessin-epure-%s-tel-1.png'%nat)
                planche('C-042 · %s · taille, couleur'%NOM[nat], C[3:6], 3, 'planche-v129/dessin-epure-%s-tel-2.png'%nat)
                planche('C-042 · %s · un mot et un dessin'%NOM[nat], C[6:], 2, 'planche-v129/dessin-epure-%s-tel-3.png'%nat)
        else:
            SOMBRE += [('6 · %s · E1 (sombre)'%NOM['promi'], parcours(pg,'promi',th,seulement=['6E1'])[0][1]), ('6 · %s · E2 (sombre)'%NOM['promi'], parcours(pg,'promi',th,seulement=['6E2'])[0][1]), ('6 · %s · E2 (sombre)'%NOM['cercle'], parcours(pg,'cercle',th,seulement=['6E2'])[0][1])]
'''+D[j:]
D=D.replace("    planche('C-042 · la page + et l\\'écran 7 en sombre', [PLUS]+SOMBRE, 3, 'planche-v128/dessin-plus-et-sombre.png')","    planche('C-042 · l\\'étape 6 en sombre', SOMBRE, 3, 'planche-v129/dessin-epure-sombre.png')")
D=D.replace("D='scratchpad/v128/dessin/'","D='scratchpad/v129/dessin/'")
assert 'planche-v128' not in D, [l for l in D.split('\n') if 'planche-v128' in l]
io.open('scratchpad/v129/dessin/dessin.py','w',encoding='utf-8').write(D)
