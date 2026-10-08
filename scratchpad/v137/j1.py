import io
S=io.open('redteam_phrase_fiche.py',encoding='utf-8').read()
def r(a,b):
    global S
    assert S.count(a)==1,(a[:70],S.count(a)); S=S.replace(a,b)
r("""     ('Chiche lancé',"p=promises.find(q=>q.title==='courir dimanche')", 'À Marion · avec Rachel · chiche de', 'courir dimanche'),
     ('Chiche reçu',"p=promises.find(q=>q.title==='courir dimanche'); p.from='Marion'; p.who='moi'; p.avec=''", 'Marion me lance'+NB+': chiche de', 'courir dimanche'),""",
"""     # ⚑ v137 (Tom, 8 oct. 2026, Q412) — CONTRAT RÉÉCRIT (original : sauvegardes/redteam_phrase_fiche-avant-v137.py) : « Pour les Chiche,
     #   remplace par l'expression courante : à soi "T'es pas chiche de" ; lancé "Marion, t'es pas chiche de" ("Marion et Rachel, vous êtes
     #   pas chiches de", et "… + x personnes" au-delà de trois) ; reçu "Marion me dit : t'es pas chiche de". »
     ('Chiche à soi',"p=promises.find(q=>q.title==='courir dimanche'); p.who='moi'; p.avec=''", 'T’es pas chiche de', 'courir dimanche'),
     ('Chiche lancé à une personne',"p=promises.find(q=>q.title==='courir dimanche'); p.who='Marion'; p.avec=''", 'Marion, t’es pas chiche de', 'courir dimanche'),
     ('Chiche lancé à deux',"p=promises.find(q=>q.title==='courir dimanche'); p.who='Marion'; p.avec='Rachel'", 'Marion et Rachel, vous êtes pas chiches de', 'courir dimanche'),
     ('Chiche lancé à six',"p=promises.find(q=>q.title==='courir dimanche'); p.who='Marion, Rachel, Nico, Adrien, Léa, Jo'; p.avec=''", 'Marion, Rachel +'+NB+'4'+NB+'personnes, vous êtes pas chiches de', 'courir dimanche'),
     ('Chiche reçu',"p=promises.find(q=>q.title==='courir dimanche'); p.from='Marion'; p.who='moi'; p.avec=''", 'Marion me dit'+NB+': t’es pas chiche de', 'courir dimanche'),""")
r("VERBES=['Je me promets','Je promets à','me promet de','me promet d’','chiche de','promets-moi de','me lance']","VERBES=['Je me promets','Je promets à','me promet de','me promet d’','chiche de','chiches de','promets-moi de','me dit']")
io.open('redteam_phrase_fiche.py','w',encoding='utf-8').write(S)
