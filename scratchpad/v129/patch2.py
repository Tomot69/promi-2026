import io
S=io.open('app.html',encoding='utf-8').read()
i=S.index("""<b>Ça y est.</b><span>Ton premier '+nat('Promi')+',"""); j=S.index("</div>'", i)
N=u"""<b>C’est planté.</b><span>Ton premier '+nat('Promi')+', ta première dalle sur ta Toile. Plus qu’à le tenir.</span><span class="onbv-cpt">Primo, un '+nat('Promi')+', c’est ta parole donnée. <i class="onbv-deux">Deuxio</i>, un '+nat('Chiche')+', c’est un coup de culot. Tertio, un '+nat('Cercle')+', c’est tout cela à la fois, mais à plusieurs.</span><span>Le reste se découvre en traçant. La suite t’appartient.</span>"""
S=S[:i]+N+S[j:]
a="#onbV .onbv-fin .onbv-cpt{margin-top:20px}"
assert S.count(a)==1
S=S.replace(a,a+"""
/* ⚑ v129 (Tom, C-006) — « Deuxio » : le seul mot « Deuxio » est penché de 3° (oblique, bien moins qu'un italique) — un clin d'œil à la faute
   volontaire, qui ne se remarque qu'en regardant de près. Même police, même graisse, même couleur ; aucun autre mot penché. */
#onbV .onbv-fin .onbv-deux{display:inline-block;font-style:normal;font-weight:inherit;color:inherit;-webkit-text-fill-color:inherit;transform:skewX(-3deg)}""")
io.open('app.html','w',encoding='utf-8').write(S)
J=io.open('redteam_onboarding.py',encoding='utf-8').read()
a="""            elif 'Le reste se trace' not in (fin['t'] or '').replace('\\u00a0', ' '):
                ko('O20 le message reste (4 s, puis le toucher)', 'le message ne dit pas « Le reste se trace. » (v128, Tom)')"""
assert J.count(a)==1
J=J.replace(a,"""            elif any(m not in (fin['t'] or '').replace('\\u00a0', ' ') for m in TEXTE_FIN):
                ko('O20 le message reste (4 s, puis le toucher)', 'le message ne dit pas le texte figé en v129 : ' + ' / '.join(m for m in TEXTE_FIN if m not in (fin['t'] or '').replace('\\u00a0', ' ')))""")
a="""            ok('O20 le message reste (4 s, puis le toucher)')"""
assert J.count(a)==1
J=J.replace(a,a+"""
            # ⚑ v129 (Tom) — « Deuxio » : le seul mot penché, de 3° (± 0,5) ; aucune autre inclinaison sur la diapositive (ni transformation, ni italique)
            dx = pg.evaluate(\"\"\"()=>{ const f=document.getElementById('onbFin'); if(!f) return null; const out={deux:null, autres:[]};
              [...f.querySelectorAll('*')].forEach(e=>{ const cs=getComputedStyle(e), tr=cs.transform, it=cs.fontStyle; let ang=0;
                if(tr&&tr!=='none'){ const m=tr.match(/matrix\\\\(([^)]+)\\\\)/); if(m){ const v=m[1].split(',').map(parseFloat); ang=Math.atan2(v[2], v[3])*180/Math.PI; if(Math.abs(v[1])>1e-4||Math.abs(v[0]-1)>1e-4||Math.abs(v[3]-1)>1e-4) ang=999; } else ang=999; }
                if(e.classList.contains('onbv-deux')) out.deux={mot:e.textContent, ang:ang, it:it, police:cs.fontFamily.split(',')[0], poids:cs.fontWeight, couleur:cs.color, pPolice:getComputedStyle(e.parentElement).fontFamily.split(',')[0], pPoids:getComputedStyle(e.parentElement).fontWeight, pCouleur:getComputedStyle(e.parentElement).color};
                else if(ang!==0 || (it!=='normal')) out.autres.push((e.textContent||'').slice(0,14)+' '+ang.toFixed(1)+'° '+it); }); return out; }\"\"\")
            d2 = (dx or {}).get('deux')
            if not d2 or d2['mot'] != 'Deuxio': ko('O21 « Deuxio » est penché de 3°, et lui seul', 'le mot penché est introuvable : %s' % d2)
            elif abs(abs(d2['ang']) - DEUXIO_ANGLE) > 0.5 or d2['ang'] > 0: ko('O21 « Deuxio » est penché de 3°, et lui seul', 'angle %.2f° (décidé : %.0f° ± 0,5, vers la droite)' % (d2['ang'], DEUXIO_ANGLE))
            elif d2['it'] != 'normal' or d2['police'] != d2['pPolice'] or d2['poids'] != d2['pPoids'] or d2['couleur'] != d2['pCouleur']: ko('O21 « Deuxio » est penché de 3°, et lui seul', 'police, graisse ou couleur différentes du texte : %s' % d2)
            elif dx['autres']: ko('O21 « Deuxio » est penché de 3°, et lui seul', 'autre inclinaison : %s' % dx['autres'][:3])
            else: ok('O21 « Deuxio » est penché de 3°, et lui seul')""")
a="import "
i=J.index("\nimport ")
J=J[:i]+"""
# ⚑ v129 (Tom, C-006) — LE TEXTE DE LA DERNIÈRE DIAPOSITIVE EST FIGÉ, EN DUR (original du juge : sauvegardes/redteam_onboarding-avant-v129.py)
TEXTE_FIN = ['C’est planté.', 'Ton premier Promi, ta première dalle sur ta Toile. Plus qu’à le tenir.',
             'Primo, un Promi, c’est ta parole donnée. Deuxio, un Chiche, c’est un coup de culot. Tertio, un Cercle, c’est tout cela à la fois, mais à plusieurs.',
             'Le reste se découvre en traçant. La suite t’appartient.']
DEUXIO_ANGLE = 3.0
"""+J[i:]
io.open('redteam_onboarding.py','w',encoding='utf-8').write(J)
