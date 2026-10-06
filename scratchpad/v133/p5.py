import io
S=io.open('app.html',encoding='utf-8').read()
def r(a,b,n=1):
    global S
    assert S.count(a)==n,(a[:70],S.count(a)); S=S.replace(a,b)
# ── CSS
r("""#device #dessinMode .dz-rangee{position:absolute;left:0;width:390px;margin:0;padding:0}""",
"""#device #dessinMode .dz-rangee{position:absolute;left:0;width:390px;margin:0;padding:0}
/* ⚑ v133 (Tom, C-056) — sortir sans poser : un ✕ dans le contour de l'encart, à l'emplacement de « ✕ FERMER ». Le dessin en cours est gardé. */
#device #dessinMode .dz-quitter{left:314px;top:48px;width:44px;height:44px;border:0;border-radius:22px;background:none;color:var(--dz-trait-fin);display:flex;align-items:center;justify-content:center}
#device #dessinMode .dz-quitter svg{width:18px;height:18px;display:block;flex:none}
/* ⚑ v133 (Tom, C-061) — sans Ma Parole !, la zone des teintes est un mur : floutée comme les autres (4,8 px), la phrase monte dessus */
#device #dessinMode .dz-couleurs.dz-mur > *{filter:blur(4.8px);-webkit-filter:blur(4.8px);pointer-events:none}
#device #murPhrase.sur-dessin{z-index:400}""")
# ── paramètres
r("""    MARGE_BAS: 34,         /* sous la rangée, jusqu'au bas de l'écran */
    MARGE_HAUT: 12,        /* entre le bas de la surface de dessin et la rangée */""",
"""    SECU_BAS: 34,          /* v133 : la zone de sécurité du bas de l'écran (l'indicateur d'accueil) — le bord bas UTILE est à H − SECU_BAS */
    MARGE_BAS: 12,         /* v133 : sous la rangée, jusqu'au bord bas utile — ÉGALE à MARGE_HAUT : la rangée est centrée dans sa zone basse */
    MARGE_HAUT: 12,        /* entre le bas de la surface de dessin et la rangée */""")
r("""    ECART_DEPLOI: 8,       /* entre la rangée et ce qui se déploie au-dessus d'elle */""","""    ECART_DEPLOI: 16,      /* v133 (Tom) : 16 pt entre la rangée et ce qui se déploie au-dessus d'elle (8 collait) */""")
r("""function surfH(){ return H - P.MARGE_BAS - P.RANGEE_H - P.MARGE_HAUT; }""","""function surfH(){ return H - P.SECU_BAS - P.MARGE_BAS - P.RANGEE_H - P.MARGE_HAUT; }
  function paye(){ try{ return !!(isPremium || dev().classList.contains('premium')); }catch(_){ return false; } }""")
r("""var yR=H-P.MARGE_BAS-P.RANGEE_H; z.style.top=yR+'px'; z.style.height=P.RANGEE_H+'px';""",
"""var yR=H-P.SECU_BAS-P.MARGE_BAS-P.RANGEE_H; z.style.top=yR+'px'; z.style.height=P.RANGEE_H+'px';
    if(!r.querySelector('.dz-quitter')){ var qx=document.createElement('button'); qx.type='button'; qx.className='dz-quitter'; qx.setAttribute('aria-label','Quitter le dessin');
      qx.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>';
      qx.addEventListener('click', function(ev){ ev.stopPropagation(); sort(false); }); r.appendChild(qx); }""")
# une surface plus haute que la place (dessin d'avant v133 : 754) est ramenée à la place
r("""if(!d.traits) d.traits=(d.poses||[]).slice();""","""if(!d.traits) d.traits=(d.poses||[]).slice();
    if(d.h>surfH()) d.h=surfH();   /* v133 : la surface a perdu 12 pt (la rangée est centrée) — un dessin d'avant garde tous ses traits, sa surface est ramenée à la place */""")
# sans Ma Parole ! : l'encre du mode
r("""var ch=choixTrait(); M.couleur=(ch.indexOf(enc)>=0 && enc!==d.fond) ? enc : (ch.filter(function(t){ return t!==d.fond; })[0]||ch[0]);""",
"""var ch=choixTrait(); M.couleur=(ch.indexOf(enc)>=0 && enc!==d.fond) ? enc : (ch.filter(function(t){ return t!==d.fond; })[0]||ch[0]);
    if(!paye() && !d.pose){ var encM=clair()?ENCRE:CREME; M.couleur=(encM!==d.fond)?encM:enc; }   /* v133 (C-061) : sans Ma Parole !, on dessine à l'encre du mode */""")
r("""q.setAttribute('aria-label','Les couleurs du dessin'); q.style.top=(yD-114)+'px';""",
"""q.setAttribute('aria-label','Les couleurs du dessin'); q.style.top=(yD-114)+'px';
      if(!paye()){ q.classList.add('dz-mur'); q.setAttribute('aria-label','Les couleurs du dessin, avec Ma Parole\\u00a0!'); }   /* v133 (C-061) : le mur — rien ne s'y choisit, la phrase monte au toucher */""")
# l'offre s'ouvre : on sort du mode dessin (le dessin en cours est gardé), sinon elle s'ouvrirait dessous
r("""  document.addEventListener('keydown', function(e){ if(M && e.key==='Escape'){ sort(false); e.preventDefault(); } }, true);""",
"""  document.addEventListener('keydown', function(e){ if(M && e.key==='Escape'){ sort(false); e.preventDefault(); } }, true);
  (function(){ var f=window._cercleDessus; if(typeof f==='function' && !f.__dz){ var g=function(){ try{ if(M) sort(false); }catch(_){ } return f.apply(this, arguments); }; g.__dz=true; window._cercleDessus=g; } })();""")
# ── les murs
r("""    add('#notifScreen .nt-mur');   /* v109 : la mémoire des paroles en l'air et le choix de l'heure */""",
"""    add('#notifScreen .nt-mur');   /* v109 : la mémoire des paroles en l'air et le choix de l'heure */
    add('#dessinMode.ouv .dz-couleurs.dz-mur');   /* v133 (C-061) : les teintes du dessin */""")
r("""p.classList.toggle('sur-corps', !_trop && !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet')));""",
"""p.classList.toggle('sur-corps', !_trop && !!(mur && mur.closest && mur.closest('#detailPoster, #createSheet, #dessinMode')));
      p.classList.toggle('sur-dessin', !!(mur && mur.closest && mur.closest('#dessinMode')));""")
# la phrase sur le mur du dessin : sa couleur suit le fond du panneau (le corps), pas le thème
r("""#device #murPhrase.sur-dessin{z-index:400}""","""#device #murPhrase.sur-dessin{z-index:400;color:var(--dz-mur-encre);-webkit-text-fill-color:var(--dz-mur-encre)}""")
r("""      p.classList.toggle('sur-cobalt', _cb); }catch(_){}""","""      p.classList.toggle('sur-cobalt', _cb);
      if(mur && mur.closest && mur.closest('#dessinMode')){ var _dm=document.getElementById('dessinMode'); p.style.setProperty('--dz-mur-encre', getComputedStyle(_dm).getPropertyValue('--dz-encre')); } }catch(_){}""")
# ── la liste des avantages
r("""['Chaque parole se peaufine','récurrence, rappel, importance, mémoire'],""","""['Chaque parole se peaufine','récurrence, rappel, mémoire, couleurs du dessin'],""")
# ── le menu
print(S.count('Importer une image'))
io.open('app.html','w',encoding='utf-8').write(S)
