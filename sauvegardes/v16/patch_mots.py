# Lot v16 — les mots. Chaque remplacement sous assert (un motif, une fois).
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
R=[
 # la sphère → la Pelote (aide de l'Aura)
 ("+carte('sphere','La sphère',", "+carte('sphere','La Pelote',"),
 ("'Sous la sphère, une phrase dit où en est ta parole.'", "'Sous la Pelote, une phrase dit où en est ta parole.'"),
 # le titre de l'aide
 ('<h2 class="scr-t ah-head">Ton Aura</h2>', '<h2 class="scr-t ah-head">L’aura</h2>'),
 # THE STUDIO
 ('<span class="k">The Studio</span>', '<span class="k">Le Studio</span>'),
 ('<h2>The <span class="it sig">Studio</span></h2>', '<h2>Le <span class="it sig">Studio</span></h2>'),
 # « tuto »
 ("<span class=\"k\">Revoir l'intro & le tuto</span>", "<span class=\"k\">Revoir la présentation</span>"),
 # un reste de la version web
 ("rien d'autre ne sort.<br>Effacer les données de ce navigateur efface tes Promi : exporte-les avant si tu y tiens.", "rien d'autre ne sort."),
 # tutoiement
 ("'visible par '+qui+' · vous pouvez répondre'", "'visible par '+qui+', qui peut y répondre'"),
 ('<div class="tag">Vos promesses, tenues.</div>', '<div class="tag">Tes promesses, tenues.</div>'),
 # l'accent
 ("g.fillText('ta premiere promesse t\\u2019attend'", "g.fillText('ta première promesse t\\u2019attend'"),
 # AVANT · résolue → une date, quel que soit l'état ; « 2 j » → des mots
 ("   if(p.status!=='encours'){_dueTxt='résolue';}\n   else if(p.enLair){_dueTxt='en l’air';}",
  "   /* ⚑ v16 (Tom) : « AVANT » dit une DATE, quel que soit l'état — « résolue » n'était pas une échéance */\n   if(p.enLair){_dueTxt='en l’air';}"),
 ("catch(_dz){_dueTxt=(p.due<=1?'demain':'dans '+p.due+' j');}}",
  "catch(_dz){_dueTxt=(p.due<=1?'demain':'dans '+p.due+' jours');}}"),
 ("   else{_dueTxt=(p.due==null?'un jour':(p.due<=1?'demain':'dans '+p.due+' j'));}",
  "   else if(p.due==null){_dueTxt='un jour';}\n   else{try{var _dd=new Date();_dd.setHours(0,0,0,0);_dd.setDate(_dd.getDate()+Math.round(+p.due));_dueTxt='avant '+window._dateQuand(_dd);}catch(_de){_dueTxt='un jour';}}"),
]
for a,b in R:
    n=S.count(a); assert n==1,(n,a[:70]); S=S.replace(a,b)
io.open(F,'w',encoding='utf-8').write(S); print('ok',len(R))
