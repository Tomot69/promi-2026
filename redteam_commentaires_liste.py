#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
redteam_commentaires_liste.py — LES COMMENTAIRES SUR LA VUE PRINCIPALE D'UNE FICHE (v183a, Tom, 7 nov. 2026 — C-248).

« Les commentaires sont visibles sur la vue principale de la fiche, les uns sous les autres, sans aucun chevauchement. S'il y en a trop, les plus récents
sont affichés, suivis d'une ligne « + X commentaires ». Un toucher sur cette ligne déplie le reste en douceur (hauteur animée, sans saut), et le contenu
défile au-dessus de la barre Peaufiner. Rien ne passe sous l'en-tête. Rien ne disparaît. »
Par banc_tom (WebKit, 390 × 844 @3x), fiches Promi, Chiche, Cercle × 0, 1, 3, 12 mots (dont un de 280 caractères) ; puis l'état exporté de Tom (mots ajoutés) :
  A · le compte : min(n, 3) mots affichés, du plus récent au plus ancien ; « + X commentaires » si n > 3, avec le bon X ; 0 mot : aucune liste ;
  B · aucun rectangle de mot ne chevauche un autre mot, la ligne d'état, « Un mot… », ni « + X » (lus sur les nœuds rendus) ;
  C · rien sous l'en-tête : aucun mot à l'écran entre le haut de l'appareil et le bas du plateau quand la fiche est au repos, et la liste commence sous l'état ;
  D · rien ne disparaît : 2,5 s après l'ouverture, les mêmes mots, aux mêmes cotes (à 1 pt) qu'à 0,8 s ;
  E · (12 mots) toucher « + X » : à chaque image le haut de la liste ne bouge pas, sa hauteur croît sans saut (pas ≤ 1/4 de la course), fin : 12 mots, plus de « + X » ;
  F · (12 mots) défilée jusqu'en bas : la barre Peaufiner est au bas de l'écran (760 pt), « Un mot… » entier au-dessus d'elle ;
  G · (Cercle) la liste ferme le fil, sous la dernière carte, dans les marges des cartes ; rien ne passe sous l'encart (le fil est coupé).
`--sonde=chevauche` pose la liste sur la ligne d'état : B rougit.     Usage : python3 redteam_commentaires_liste.py [fichier.html] [--tom-seul] [--sonde=…]
"""
import sys, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html'); SONDE = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--sonde=')), '')
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, str(detail)[:260]), flush=True)
L280 = ("Je viens, mais seulement si on part tôt : il faut passer prendre les chaises chez Nico, puis le pain à la boulangerie du coin, "
        "et je voudrais qu'on garde un moment pour la photo de groupe avant que tout le monde reparte, parce que la dernière fois on l'a oubliée et c'était dommage")[:280]
NOMS = ['Marion', 'Rachel', 'moi', 'Nico', 'Adrien', 'Lou']
def com(n):
    return [{'t': L280 if (n > 3 and i == n - 2) else 'Mot numéro %d, à propos de ce qu\'on prévoit' % (i + 1), 'by': NOMS[i % 6], 'd': '2026-11-%02dT%02d:00:00Z' % (1 + i // 4, 8 + i % 4 * 3)} for i in range(n)]
ET = r"""()=>{ var dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  function R(e){ if(!e) return null; var q=e.getBoundingClientRect(), cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||q.height<1||q.width<1) return null; return {x:(q.left-dv.left)/k, y:(q.top-dv.top)/k, b:(q.bottom-dv.top)/k, r:(q.right-dv.left)/k}; }
  var l=document.getElementById('cm5Liste'), uns=l?[...l.querySelectorAll('.cm5-un')]:[];
  var vis=uns.map(u=>{ var q=R(u); if(!q) return null; var a=u.parentNode, cl=null; while(a&&a!==l){ var cs=getComputedStyle(a); if(cs.overflow!=='visible'||cs.overflowY!=='visible'){ var r=a.getBoundingClientRect(); cl=[(r.top-dv.top)/k,(r.bottom-dv.top)/k]; } a=a.parentNode; }
     if(cl){ q.y=Math.max(q.y,cl[0]); q.b=Math.min(q.b,cl[1]); }
     var fl=u.closest('.nf-liste'); if(fl){ var cp=(fl.style.clipPath||'').match(/inset\(([\d.]+)px/); if(cp){ var fr=fl.getBoundingClientRect(), kl=fr.width/(fl.offsetWidth||1); q.y=Math.max(q.y,(fr.top-dv.top)/k+parseFloat(cp[1])*kl/k); } }   /* le fil d'un Cercle est rogné sous l'encart (C-243, v181a) : on lit ce qui reste visible */
     var nt=document.querySelector('#dpNueeFil .nf-tete'); if(nt && u.closest('#dpNueeFil')){ var tr=nt.getBoundingClientRect(); if(tr.height){ q.b=Math.min(q.b,(tr.top-dv.top)/k-12); } }   /* le bloc collant du bas d'un Cercle (« Un mot… », « + Planter ») a son fond, 12 pt au-dessus de lui : le fil passe dessous, comme ses cartes */
     if(q.b-q.y<1) return null; q.t=(u.querySelector('.cm5-t')||{}).textContent||''; return q; }).filter(Boolean);
  var pl=l?l.querySelector('.cm5-plus'):null, ent=document.querySelector('#detailPoster .enh'), fil=document.getElementById('dpNueeFil'), nt=document.querySelector('#dpNueeFil .nf-tete');
  var cartes=[...document.querySelectorAll('#dpNueeFil .nf-item')].map(R).filter(Boolean);
  var plv=R(pl); if(plv){ var nt2=document.querySelector('#dpNueeFil .nf-tete'); if(nt2 && pl.closest('#dpNueeFil')){ var t2=nt2.getBoundingClientRect(); if(t2.height) plv.b=Math.min(plv.b,(t2.top-dv.top)/k-12); }
    var fl2=pl.closest('.nf-liste'); if(fl2){ var cp2=(fl2.style.clipPath||'').match(/inset\(([\d.]+)px/); if(cp2){ var fr2=fl2.getBoundingClientRect(), kl2=fr2.width/(fl2.offsetWidth||1); plv.y=Math.max(plv.y,(fr2.top-dv.top)/k+parseFloat(cp2[1])*kl2/k); } } if(plv.b-plv.y<1) plv=null; }
  var poses=uns.filter(u=>{ var a=u; while(a&&a!==document.body){ var cs=getComputedStyle(a); if(cs.display==='none'||cs.visibility==='hidden') return false; a=a.parentElement; } var r=u.getBoundingClientRect(); if(!r.height) return false;
     var c=u.parentElement; if(c&&c.classList.contains('cm5-reste')&&c.getBoundingClientRect().height<1) return false; return true; }).map(u=>(u.querySelector('.cm5-t')||{}).textContent||'');
  return {liste:R(l), uns:vis, poses:poses, plusPose:!!(pl&&pl.getBoundingClientRect().height>1), plusT2:pl&&pl.getBoundingClientRect().height>1?pl.textContent.trim():'', plus:plv, plusT:pl&&R(pl)?pl.textContent.trim():'', ligne:R(document.getElementById('cm5Ligne')), etat:R(document.getElementById('dptQuand')), barre:R(document.getElementById('dpDetails')),
    ent:R(ent), nfTete:R(nt), cartes:cartes, sc:document.getElementById('detailPoster').scrollTop, cercle:document.getElementById('detailPoster').classList.contains('dp-mode-nuee')}; }"""
def croise(a, b, m=0.5): return a and b and a['y'] < b['b'] - m and b['y'] < a['b'] - m and a['x'] < b['r'] - m and b['x'] < a['r'] - m
def ferme(pg):
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie() }catch(e){} try{ closeAll() }catch(e){} }"); pg.wait_for_timeout(900)
def cas(pg, tag, ouvrir, n, attendus):
    ouvrir(); pg.wait_for_timeout(800); e1 = pg.evaluate(ET); pg.wait_for_timeout(1700); e = pg.evaluate(ET)
    if SONDE == 'chevauche' and e['liste']: pg.evaluate("()=>{ var l=document.getElementById('cm5Liste'); l.style.setProperty('top', (parseFloat(l.style.top)||640)-30+'px','important'); }"); e = pg.evaluate(ET)
    # ⚑ v188 (Tom, Q608 tranchée autrement) — CONTRAT REMIS AU NIVEAU (original : sauvegardes/redteam_commentaires_liste-avant-v188.py) : plus de « + X commentaires » ;
    #   TOUS les mots, le plus récent d'abord, sous « Un mot… » (Promi, Chiche) ou au bout du fil (Cercle) ; plus de dépliage (E) ; défilée jusqu'en bas, le dernier mot
    #   entier au-dessus de la barre (F) ; rien sous l'en-tête au doigt (la bande de v187 couvre ce qui y passe, G).
    nv = n; txt = e['poses']   # les mots POSÉS dans la fiche (sur un Cercle, au bout du fil : on les voit en défilant ; B et C jugent ce qui est à l'écran)
    juge('A · [%s] %d mot(s) : tous affichés, le plus récent d\'abord, aucun « + X »' % (tag, n),
         len(txt) == nv and txt == attendus[:nv] and not e['plusPose'] and (n > 0 or not e['liste']),
         (len(txt), [t[:18] for t in txt], e['plusT2']))
    boites = e['uns'] + [x for x in (e['etat'], e['ligne'], e['plus']) if x]
    cr = [(i, j) for i in range(len(boites)) for j in range(i + 1, len(boites)) if croise(boites[i], boites[j])]
    juge('B · [%s] %d mot(s) : aucun chevauchement (mots, état, « Un mot… », « + X »)' % (tag, n), not cr, cr[:4])
    haut = e['ent']['b'] if e['ent'] else 100   # le bas du plateau (CERCLE / PROMI et X)
    sous = [u for u in e['uns'] if u['y'] < haut - 0.5 and u['b'] > 0]
    juge('C · [%s] %d mot(s) : rien sous l\'en-tête (%.0f), la liste sous l\'état' % (tag, n, haut), not sous and (not e['uns'] or e['cercle'] or not e['etat'] or e['uns'][0]['y'] >= e['etat']['b'] - 0.5), (sous[:2], e['etat'] and e['etat']['b'], e['uns'][0]['y'] if e['uns'] else None))
    # D : relevé RELATIF à la ligne d'état (la fiche glisse encore à l'ouverture : tout bouge d'un bloc) ; un mot présent à 0,8 s l'est encore à 2,5 s
    o1 = (e1['etat'] or {'b': 0})['b'] if not e1['cercle'] else (e1['cartes'][0]['y'] if e1['cartes'] else 0); o2 = (e['etat'] or {'b': 0})['b'] if not e['cercle'] else (e['cartes'][0]['y'] if e['cartes'] else 0)
    c1 = [(u['t'][:20], round(u['y'] - o1)) for u in e1['uns']]; c2 = [(u['t'][:20], round(u['y'] - o2)) for u in e['uns']]
    juge('D · [%s] %d mot(s) : rien ne disparaît ni ne saute (0,8 s → 2,5 s, relatif à l\'état)' % (tag, n), len(c1) <= len(c2) and all(a[0] == b[0] and abs(a[1] - b[1]) <= 1 for a, b in zip(c1, c2)), (c1[:3], c2[:3]))
    return e
def depliage(pg, tag):
    e0 = pg.evaluate(ET)
    juge('E · [%s] plus de « + X » ni de dépliage (v188) : les 12 mots posés' % tag, not e0['plusPose'] and pg.evaluate("()=>typeof window._commDeplie") == 'undefined' and pg.evaluate("()=>document.querySelectorAll('#cm5Liste .cm5-un').length") == 12)
    pg.evaluate("()=>{ var dp=document.getElementById('detailPoster'); dp.scrollTop=dp.scrollHeight; }"); pg.wait_for_timeout(1800)
    e = pg.evaluate(ET)
    der = e['uns'][-1] if e['uns'] else None
    juge('F · [%s] défilée jusqu\'en bas : la barre au bas de l\'écran (760), le dernier mot entier au-dessus' % tag,
         e['barre'] and abs(e['barre']['y'] - 760) <= 1.5 and der and der['b'] <= e['barre']['y'] + 0.5 and der['y'] >= 100, (e['barre'], der and (round(der['y'], 1), round(der['b'], 1)), round(e['sc'])))
def ouvre_par(pg, titre): return lambda: pg.evaluate("t=>openDetail(promises.find(x=>x.title===t).id)", titre)
with sync_playwright() as p:
    b = p.webkit.launch()
    if '--tom-seul' not in sys.argv:
        ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F)
        pg.evaluate("()=>{ var v=promises.find(x=>x.title==='réparer le vélo'); v.chiche=true; v.chicheEtat='lance'; v.phraseSens='chiche'; try{queueSave()}catch(e){} }")
        for n in [int(x) for x in next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--n=')), '0,1,3,12').split(',')]:
            C = com(n); att = [c['t'] for c in reversed(C)]
            for tag, titre in (('Promi', 'faire les crêpes'), ('Chiche', 'réparer le vélo')):
                ferme(pg); pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); p.comments=a[1]; try{queueSave()}catch(e){} }", [titre, C])
                cas(pg, tag, ouvre_par(pg, titre), n, att)
                if n == 12: depliage(pg, tag)
            ferme(pg); pg.evaluate("c=>{ var o=window._cercleMots.de('potager'); o.comments.length=0; c.forEach(x=>o.comments.push(x)); _cercleMots.garde(); }", C)
            e = cas(pg, 'Cercle', lambda: (pg.evaluate("()=>openEssaim('potager')"), pg.wait_for_timeout(2400)), n, att)
            if n:
                pg.evaluate("()=>{ var dp=document.getElementById('detailPoster'); dp.scrollTop=dp.scrollHeight; }"); pg.wait_for_timeout(1500); e = pg.evaluate(ET)
                der = e['cartes'][-1] if e['cartes'] else None
                sous = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; let n=0; document.querySelectorAll('#cm5Liste .cm5-un').forEach(u=>{ const r=u.getBoundingClientRect(); for(let y=Math.max(r.top,D.top+2*k); y<Math.min(r.bottom, D.top+100*k); y+=4*k){ const e=document.elementFromPoint(r.left+r.width/2, y); if(e && u.contains(e)){ n++; break; } } }); return Array(n).fill(0); }")   # au doigt
                juge('G · [Cercle] %d mot(s), défilé : la liste sous la dernière carte, dans ses marges, rien sous l\'encart' % n,
                     e['uns'] and der and pg.evaluate("()=>{ const L=document.getElementById('cm5Liste'), c=[...document.querySelectorAll('#dpNueeFil .nf-item')].pop(); return L && c && L.getBoundingClientRect().top >= c.getBoundingClientRect().bottom - 0.5; }") and all(abs(u['x'] - der['x']) <= 1.5 and u['r'] <= der['x'] + 342.5 for u in e['uns']) and not sous,
                     (der and round(der['b']), [(round(u['x']), round(u['y'])) for u in e['uns'][:2]], len(sous)))
                if n == 12:
                    pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(1200); depliage(pg, 'Cercle')
        print('erreurs de page :', pg.__dict__['erreurs'][:3]); juge('Z · aucune erreur de page', not pg.__dict__['erreurs'])
        ctx.close()
    # l'état exporté de Tom, mots ajoutés
    ctx, d = B.contexte_tom(b)
    if ctx:
        pg = B.ouvre(ctx, F); ps = pg.evaluate("()=>promises.filter(p=>!p.draft).map(p=>p.title)")
        for n, ti in ((3, ps[0]), (12, ps[-1])):
            C = com(n); ferme(pg); pg.evaluate("a=>{ var p=promises.find(x=>x.title===a[0]); p.comments=a[1]; try{queueSave()}catch(e){} }", [ti, C])
            cas(pg, 'Tom · ' + ti[:10], ouvre_par(pg, ti), n, [c['t'] for c in reversed(C)])
            if n == 12: depliage(pg, 'Tom')
        ctx.close()
    b.close()
ok = sum(1 for _, v in res if v); print('\n%d / %d' % (ok, len(res)))
