# -*- coding: utf-8 -*-
"""redteam_plus_disque.py — ⚑ v186b (Tom, C-254 suite, Q606) : LE + DES MEMBRES À CÔTÉ DU PETIT DISQUE.
« Le + se place à hauteur du milieu du PETIT disque (pas du gros, qui est le tien), juste à côté de lui, verticalement centré sur ce petit disque, à la même
distance de l'élément qu'aujourd'hui (26 pt) ; plusieurs petits disques : après le dernier ; même dessin, même taille ; il ne chevauche plus jamais rien ;
Promi, Chiche et Cercle. » Juge : centre vertical de l'ENCRE du + = centre du petit disque à 0,5 pt ; l'encre commence 26 pt (± 0,5) après le bord droit du
disque ; aucun recouvrement avec un autre élément du haut de la fiche ; titres courts, pleins, 280 caractères (le nom d'un Cercle : 40) ; échelles 1 et 0,79.
Valeurs EN DUR. Usage : python3 redteam_plus_disque.py [fichier.html]"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
ECART, TOL = 26.0, 0.5
ok = ko = 0
def juge(nom, cond, det=''):
    global ok, ko
    if cond: ok += 1
    else: ko += 1
    print(('  ✅ ' if cond else '  ❌ ') + nom.ljust(88) + ' ' + str(det)[:150], flush=True)
TITRES = {'court': 'lire', 'plein': 'appeler le plombier pour la fuite sous l’évier de la cuisine',
          'long': ('ranger ' + 'le grenier, trier les cartons, descendre les vieux meubles, ' * 6)[:280]}
NOMS = {'court': 'Jardin', 'plein': 'Le potager partagé de la rue des Lilas', 'long': 'Le potager partagé de la rue des Lilas ok'[:40]}
MESURE = r"""()=>{ const d=document.getElementById('detailPoster'), k=(window._echDp?window._echDp(d):1), R=d.getBoundingClientRect();
  const b=document.getElementById('cerclePlusMembres'); if(!b || getComputedStyle(b).display==='none') return {plus:false};
  const s=b.querySelector('svg'), q=(s||b).getBoundingClientRect();
  let KR=[...document.querySelectorAll('#dAura .kring:not(.kring-moi) .kr-c')].filter(c=>c.getBoundingClientRect().width>4); const petit=KR.length>0;
  if(!KR.length) KR=[...document.querySelectorAll('#dAura .kring .kr-c')].filter(c=>c.getBoundingClientRect().width>4); if(!KR.length) return {plus:true, disque:false};
  const c=KR[KR.length-1].getBoundingClientRect();
  const y=v=>(v-R.top)/k, x=v=>(v-R.left)/k;
  const enc={l:x(q.left), r:x(q.right), t:y(q.top), b:y(q.bottom)};
  const autres=['dptQui','dptTitre','dptQuand','dAura','cm5Liste','cm5Ligne'].map(id=>document.getElementById(id)).filter(e=>e && getComputedStyle(e).display!=='none');
  const rec=[]; autres.forEach(e=>{ const rg=document.createRange(); rg.selectNodeContents(e); [...(e.id==='dAura'? [...e.querySelectorAll('.kring')].map(z=>z.getBoundingClientRect()) : rg.getClientRects())].forEach(r=>{ if(r.width<1||r.height<1) return;
      const o={l:x(r.left), r:x(r.right), t:y(r.top), b:y(r.bottom)}; if(o.l<enc.r-0.5 && o.r>enc.l+0.5 && o.t<enc.b-0.5 && o.b>enc.t+0.5) rec.push(e.id+':'+[o.l,o.t,o.r-o.l,o.b-o.t].map(v=>Math.round(v)).join(',')); }); });
  return {plus:true, disque:true, cyP:(enc.t+enc.b)/2, cyD:(y(c.top)+y(c.bottom))/2, ecart:enc.l-x(c.right), taille:enc.b-enc.t, droite:enc.r, rec:rec, n:KR.length, petit:petit}; }"""
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, ech in ((430, 932, '1'), (330, 714, '0,79')):
        ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 9000); pg.wait_for_timeout(1500)
        for nat in ('cercle', 'promi', 'chiche', 'soi'):
            for tl in ('court', 'plein', 'long'):
                if nat == 'cercle':
                    pg.evaluate("n=>{ const old=Object.keys(NUE).find(k=>k==='potager'); NUE.potager=n; }", NOMS[tl])
                    ouv = "openEssaim('potager')"
                elif nat == 'soi':   # v186b : un Promi à soi, sans Cercle — aucun petit disque, le + suit le tien
                    pg.evaluate("t=>{ const p=promises.find(q=>!q.draft && !q.chiche && !q.nuee); p.who='moi'; p.nuee=null; p.title=t; window.__pid=p.id; }", TITRES[tl])
                    ouv = "openDetail(window.__pid)"
                else:
                    pg.evaluate("([n,t])=>{ const p=promises.find(q=>!q.draft && (n==='chiche'?q.chiche:!q.chiche) && !q.nuee && (!q.from||q.from==='moi'||q.from===USER.name)); p.title=t; window.__pid=p.id; }", [nat, TITRES[tl]])
                    ouv = "openDetail(window.__pid)"
                pg.evaluate("()=>{ try{_peaufSortie()}catch(e){} closeAll(); }"); pg.wait_for_timeout(600)
                pg.evaluate("()=>" + ouv); pg.wait_for_timeout(2600)
                m = pg.evaluate(MESURE); T = '[%s · %s · %s]' % (ech, nat, tl)
                if not m.get('plus') or not m.get('disque'): juge(T + ' le + et un petit disque sont là', False, m); continue
                juge(T + ' centre du + = centre du petit disque (± 0,5 pt)', abs(m['cyP'] - m['cyD']) <= TOL, (round(m['cyP'], 2), round(m['cyD'], 2)))
                juge(T + ' 26 pt après le bord droit du disque (± 0,5)', abs(m['ecart'] - ECART) <= TOL, round(m['ecart'], 2))
                juge(T + ' ne chevauche rien, reste dans l\'écran (≤ 366)', not m['rec'] and m['droite'] <= 366.5, (m['rec'][:3], round(m['droite'], 1)))
        ctx.close()
    b.close()
print('\n  %s  %d / %d' % ('✅' if ko == 0 else '❌', ok, ok + ko))
