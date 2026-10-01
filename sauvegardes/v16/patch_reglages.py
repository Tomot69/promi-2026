# Lot v16 — les Réglages : les réglages d'un Promi en sortent (§5), la Langue sort (aucune
# traduction n'existe : un choix qui ne change rien est un chemin sans issue), « Se déconnecter »
# entre, la Confidentialité rejoint « App », Légal = Conditions · Politique · À propos.
import io
F='app.html'; S=io.open(F,encoding='utf-8').read()
def rep(a,b,n=1):
    global S; c=S.count(a); assert c==n,(c,a[:90]); S=S.replace(a,b)
rep("""<div class="grouplab">App</div><div class="scard" id="langCard"><span class="k">Langue</span><span class="v ac" id="langV">Français ›</span></div><div class="scard" id="notifCard"><span class="k">Notifications</span><span class="v"><span class="toggle off" id="notifTog"></span></span></div>""",
    """<div class="grouplab">App</div><div class="scard" id="langCard" hidden style="display:none"><span class="k">Langue</span><span class="v ac" id="langV">Français ›</span></div><div class="scard" id="notifCard" role="switch" aria-checked="false"><span class="k">Notifications</span><span class="v"><span class="toggle off" id="notifTog"></span></span></div><div class="scard" id="privCard"><span class="k">Confidentialité</span><span class="v ac">privé &amp; partagé ›</span></div>""")
rep("""<div class="grouplab">Légal</div><div class="scard" id="privCard"><span class="k">Confidentialité</span><span class="v ac">privé &amp; partagé ›</span></div><div class="scard" id="cguCard"><span class="k">Conditions d’utilisation</span><span class="v ac">lire ›</span></div><div class="scard" id="delAccount"><span class="k">Supprimer mon compte</span><span class="v ac danger">définitif ›</span></div>""",
    """<div class="grouplab">Compte</div><div class="scard" id="logoutCard" role="button"><span class="k">Se déconnecter</span><span class="v ac">›</span></div><div class="scard v16-danger" id="delAccount" role="button"><span class="k">Supprimer mon compte</span></div>
      <div class="grouplab">Légal</div><div class="scard" id="cguCard" role="button"><span class="k">Conditions d’utilisation</span><span class="v ac">›</span></div><div class="scard" id="polCard" role="button"><span class="k">Politique de confidentialité</span><span class="v ac">›</span></div><div class="scard" id="aboutCard" role="button"><span class="k">À propos</span><span class="v ac">›</span></div>""")
# le bloc du Cercle des Réglages : plus de réglages floutés, l'encart seul (ils vivent dans Peaufiner)
rep("""    [['RÉCURRENCE', 'chaque semaine'], ['RAPPEL', 'la veille à 19:00'],
     ["C'EST IMPORTANT ?", '· ·· ···'], ['LA MÉMOIRE', 'réveille tes « en l’air »'], ['LA COULEUR', 'palette ou code']]
      .forEach(function(p){ c.appendChild(reg(p[0], p[1])); });""",
    """    /* ⚑ v16 (Tom) : « les réglages du Cercle quittent les Réglages — ils appartiennent à un Promi,
       c'est le §5. Ils restent dans Peaufiner. » L'encart reste seul : il ouvre Le Cercle. */
    c.classList.add('v16-seul');""")
# « garder de côté » sur un gardé de côté : il créait un DOUBLON (le brouillon repris restait)
rep("""    if(gcP) gcP.style.display=(k==='promi' && phraseHasContent()) ? 'inline-flex' : 'none';
    if(gcN) gcN.style.display=(k==='nuee' && nueeHasContent()) ? 'inline-flex' : 'none';""",
    """    /* ⚑ v16 : sur un gardé de côté REPRIS, le lien créait un second brouillon (l'ancien restait) — il sort. */
    var _rep = (window._brouillonRepris!=null);
    if(gcP) gcP.style.display=(k==='promi' && phraseHasContent() && !_rep) ? 'inline-flex' : 'none';
    if(gcN) gcN.style.display=(k==='nuee' && nueeHasContent() && !_rep) ? 'inline-flex' : 'none';""")
# « Supprimer ce Promi » : un seul clic sur un bouton caché ne faisait qu'ARMER #actDel — rien ne se voyait
rep("""    liste.appendChild(reg(chiche?'SUPPRIMER CE CHICHE':'SUPPRIMER CE PROMI', '→',
      {act:function(){ var b=document.getElementById('actDel'); if(b) b.click(); }}));""",
    """    var _rs=reg(chiche?'SUPPRIMER CE CHICHE':'SUPPRIMER CE PROMI', '',
      {act:function(){ if(window._v16SupprimerPromi) window._v16SupprimerPromi(p); }});
    _rs.classList.add('v16-danger'); liste.appendChild(_rs);""")
# les deux pages neuves prennent le plateau, comme la confidentialité
rep("""    ['#privScreen',     'h2.scr-t'],
    ['#essaimSheet',""", """    ['#privScreen',     'h2.scr-t'],
    ['#aboutScreen',    'h2.scr-t'],
    ['#legalScreen',    'h2.scr-t'],
    ['#essaimSheet',""")
io.open(F,'w',encoding='utf-8').write(S); print('ok')
