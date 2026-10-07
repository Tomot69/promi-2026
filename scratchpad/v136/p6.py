import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
r("""    HCV=el('canvas','au-halo'); HCV.id='auPeloteHalo'; CAD.appendChild(HCV);   /* v121 : le halo, sous la boule */
    OMBRE=el('div','au-ombre'); OMBRE.id='auPeloteOmbre'; CAD.appendChild(OMBRE);
    OMBRE.style.setProperty('top', K.ombre.y+'px', 'important');   /* v125 : la cote de l'ombre vient de K (la feuille porte encore celle de v124) */""",
"""    /* ⚑ v136 (Tom, 7 oct. 2026, C-071) — « Le halo c'est une mauvaise idée en fait. […] Enlève tout ce qu'il y a comme effet autour de la
       Pelote pour le moment, ne masque pas, supprime. » NI HALO NI OMBRE : leurs deux nœuds (`#auPeloteHalo`, `#auPeloteOmbre`) ne sont
       plus créés. Autour de la Pelote il n'y a plus que la page. La place de l'ombre reste dans la colonne (cotes B, inchangées). */""")
i=S.index('<script id="lot-V136-HALO0">'); j=S.index('</script>',i)+10
S=S[:i]+S[j:]
io.open('app.html','w',encoding='utf-8').write(S)
