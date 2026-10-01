# Lot v16 — « tutoiement partout, vous et Vos sortent ». Même le « vous » pluriel (toi + l'autre) se lisait comme un
# vouvoiement : on le tourne autrement, sans changer le sens.
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
def rep(a,b,n=1):
    global S; c=S.count(a); assert c==n,(c,a[:90]); S=S.replace(a,b)
rep("var h2=el('div','ps-h','Ce que vous partagez');", "var h2=el('div','ps-h','Ce que tu partages avec '+nom);")
rep("'votre harmonie : '+harmonyWord(allTrust)", "'harmonie à deux : '+harmonyWord(allTrust)", 2)
rep("<span class=\"lbl-prem\">votre harmonie, des deux côtés</span>", "<span class=\"lbl-prem\">l’harmonie, des deux côtés</span>")
rep("en douceur · et ce qui circule entre vous", "en douceur · et ce qui circule entre toi et les autres")
rep("l’harmonie que vous construisez ensemble", "l’harmonie qu’on construit ensemble")
rep("<b>Les promesses tenues qui vous lient</b> : les paroles honorées <b>ensemble</b> — la trace vivante de votre harmonie",
    "<b>Les promesses tenues qui te lient à eux</b> : les paroles honorées <b>ensemble</b> — la trace vivante de cette harmonie")
rep("<b>promesses tenues</b> qui vous lient<br>", "<b>promesses tenues</b> qui te lient<br>")
io.open(F,'w',encoding='utf-8').write(S); print('ok')
