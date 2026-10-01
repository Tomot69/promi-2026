# Lot v16 — décision 1 : les phrases du trait en PromiLate CAPITALES. PromiLate n'a AUCUNE
# capitale accentuée : on reformule plutôt que de mêler deux polices dans un mot.
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
R=[
 ("e.trace=(p&&p.who?p.who:'elle')+' complètera si elle relève';", "e.trace=(p&&p.who?p.who:'elle')+' tracera sa part si elle ose';"),
 ("? (e.ouvert ? 'trace pour planter' : 'trace ta moitié')", "? (e.ouvert ? 'trace pour planter' : 'trace ta part')"),
 ("trace:{y:388, mot:'l’autre moitié arrive', col:MENTHE},", "trace:{y:388, mot:'l’autre part arrive', col:MENTHE},"),
 ('<div class="tenir-lab" id="planterLabD">glisse pour garder de côté →</div>', '<div class="tenir-lab" id="planterLabD">glisse pour le garder →</div>'),
]
for a,b in R:
    n=S.count(a); assert n==1,(n,a[:70]); S=S.replace(a,b)
io.open(F,'w',encoding='utf-8').write(S); print('ok',len(R))
