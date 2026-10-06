import io
J=io.open('redteam_palettes.py',encoding='utf-8').read()
def rj(a,b):
    global J
    assert J.count(a)==1,(J.count(a),a[:60]); J=J.replace(a,b)
rj("""  return {ouvert:sc.classList.contains('stp-pals')&&cs.display!=='none',""","""  const bt=(e)=>{ if(!e) return null; const q=e.getBoundingClientRect(); return [(q.top-dv.top)/k,(q.bottom-dv.top)/k]; };
  const noms=[...document.querySelectorAll('#st3pn')], nomVu=noms.filter(e=>e.getBoundingClientRect().height>0);
  return {nNoms:noms.length, yNom:bt(nomVu[0]), yGrille:bt(rangs[0]), yJauge:bt([...P.querySelectorAll('.st3-spec')].filter(e=>e.getBoundingClientRect().height>0)[0]), nJauges:P.querySelectorAll('.st3-spec').length,
    ouvert:sc.classList.contains('stp-pals')&&cs.display!=='none',""")
rj("""            if tour==1 and th=='dark': print('     ordre :'""","""            # ⚑ la forme du défaut vu par Tom (v133) : à la DEUXIÈME ouverture, le nom de la palette passait AU-DESSUS de la grille, qui descendait sur la jauge
            ok(tag+' un seul nom de palette dans le document, une seule jauge', e['nNoms']==1 and e['nJauges']==1, (e['nNoms'], e['nJauges']))
            ok(tag+' dans l\\'ordre : la grille, puis le nom, puis la jauge — sans recouvrement', bool(e['yGrille'] and e['yNom'] and e['yJauge']) and e['yGrille'][1]<=e['yNom'][0]+0.5 and e['yNom'][1]<=e['yJauge'][0]+0.5 and max(o['y']+o['h'] for o in e['O'])<=e['yJauge'][0]+0.5, (e['yGrille'], e['yNom'], e['yJauge']))
            if tour==1 and th=='dark': print('     ordre :'""")
io.open('redteam_palettes.py','w',encoding='utf-8').write(J)
