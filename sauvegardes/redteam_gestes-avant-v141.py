# -*- coding: utf-8 -*-
"""redteam_gestes.py — E1 (C-074) : LES GESTES APPRIS EN SITUATION. La main fantôme, geste par geste.

Source : ENGAGEMENT.md, E1, corrigé par les amendements (A1, A2, A3). Les règles, EN DUR :
  · la main paraît après 600 ms sans toucher, joue le geste DEUX fois au plus (900 ms de pause), disparaît au premier toucher ;
  · le drapeau `geste_vu_<id>` est posé dès la première apparition ; après rechargement, la main ne revient pas ;
  · « Revoir les gestes » (l'ancienne entrée « Revoir la présentation » des Réglages, au doigt) efface les drapeaux : elle revient ;
  · A2 : la couche porte `data-eng`, opacité 1 (elle et ses ancêtres), aucune transition, aucune animation CSS ; trait plein à l'encre du mode ;
  · A1 : la couche ne prend aucun toucher, et pendant qu'elle joue la Toile ne change pas d'un pixel ;
  · « Réduire les animations » : la main est immobile au départ du geste (deux relevés à 700 ms d'écart, même place) et une flèche trace le trajet.
Pour chaque geste BRANCHÉ de l'inventaire : mise en situation, trois captures dans planche-e1/ (apparition, après rechargement, après rejeu).
Usage : python3 redteam_gestes.py [fichier.html] [--sonde]    (--sonde : la couche à demi transparente avec un fondu → A2 doit rougir)
"""
import sys, json
from playwright.sync_api import sync_playwright
F = [a for a in sys.argv[1:] if not a.startswith('--')]; F = F[0] if F else 'app.html'
SONDE = '--sonde' in sys.argv
SEUL = next((a.split('=')[1] for a in sys.argv if a.startswith('--seul=')), None)
LENT = {'studio-monde': 7500, 'studio-couleur': 7500, 'noyau': 6000}   # le Studio et le partage mettent plusieurs secondes à se bâtir à leur première ouverture
URL = 'http://127.0.0.1:8752/' + F
INACTIF, PAUSE, TOURS = 600, 900, 3   # ⚑ v139 (Tom, 9 oct. 2026, C-074, Q429) : « trois passages au plus » (deux en E1) ; original : sauvegardes/redteam_gestes-avant-v139.py
GRAND, TRAJET = 1.5, 1600               # « plus grande, et plus lente (environ 1,6 s pour le trajet) »
ok = [0]; ko = []
def t(nom, c, d=''):
    if c: ok[0] += 1
    else: ko.append(nom)
    print('%s  %-76s %s' % ('OK' if c else 'KO', nom, str(d)[:260]))
DESSIN = "{fond:'#12FF34', traits:[], pose:true, masque:false, poses:[{c:'#FF00AA', t:8, g:false, pts:[60,200,0,0.5, 200,330,32,0.5, 330,220,64,0.5]}]}"
# la mise en situation de chaque geste branché (ce que ferait la personne pour arriver là)
SITU = {
 'tenir':   "openDetail(promises.find(q=>q.title==='faire les crêpes').id)",
 'chiche':  "openDetail(promises.find(q=>q.title==='courir dimanche').id)",
 # v140 (E2) : la main ne montre le trait de plantation que lorsque la phrase porte ses mots — la mise en situation écrit un titre
 'planter': "document.getElementById('createBtn').click(); setTimeout(()=>{const x=document.querySelectorAll('.tile')[0]; if(x) x.click(); setTimeout(()=>{ try{ window._phrase.titre='venir dimanche'; const t=document.getElementById('fTitle'); t.value='venir dimanche'; t.dispatchEvent(new Event('input',{bubbles:true})); window._phraseRendu(); if(window._ppTrait) window._ppTrait(); }catch(e){} },700); },600)",
 'pelote':  "document.getElementById('souffleBtn').click()",
 'noyau':   "window.shNoyau=true; document.getElementById('shareBtn').click(); setTimeout(()=>{ try{ const b=document.querySelector('#shMode button[data-mode=\"toile\"]'); if(b) b.click(); window.shNoyau=true; if(window.shareRender) shareRender(); }catch(e){} },700)",
 'fil':     "setView('fil')",
 'studio-monde': "document.getElementById('studioBtn').click()",
 'studio-couleur': "localStorage.setItem('geste_vu_studio-monde','1'); document.getElementById('studioBtn').click()",
 'bande':   "const p=promises.find(q=>q.title==='planter un arbre'); p.dessin=%s; openDetail(p.id)" % DESSIN,
 # v140 (E2bis) : l'Aura vient de paraître dans la barre — le dévoilement en est à l'Index, une parole est tenue : l'Aura paraît, la main la désigne
 'aura-apparait': "try{ closeAll(); }catch(e){} localStorage.setItem('promi_devoile', JSON.stringify({index:1})); try{ window._devoile.peint(); }catch(e){}",
 'dessin':  "localStorage.setItem('geste_vu_tenir','1'); const p=promises.find(q=>q.title==='nager le mardi'); openDetail(p.id); setTimeout(()=>{ try{ window._dessin.ouvre(); }catch(e){} },900)",   # le trait de la fiche est déjà vu : on arrive au mode dessin
}
ETAT = r"""()=>{ const c=document.getElementById('gesteFantome'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
  if(!c) return {la:false, drapeaux:Object.keys(localStorage).filter(x=>x.indexOf('geste_vu_')===0).sort()};
  const m=c.querySelector('[data-main]'), r=m?m.getBoundingClientRect():null, cs=getComputedStyle(c), f=[];
  for(let q=c;q&&q.nodeType===1&&q!==document.documentElement;q=q.parentElement){ if(+getComputedStyle(q).opacity<1){ f.push('opacité '+getComputedStyle(q).opacity+(q===c?'':' (ancêtre '+(q.id||q.className)+')')); break; } }
  [c].concat([...c.querySelectorAll('*')]).forEach(e=>{ const s=getComputedStyle(e); if((s.transitionDuration||'0s').split(',').some(x=>parseFloat(x)>0)) f.push('transition '+s.transitionProperty); if(s.animationName&&s.animationName!=='none') f.push('animation '+s.animationName);
    ['fill','stroke'].forEach(a=>{ const v=e.getAttribute&&e.getAttribute(a); if(v&&/rgba\(|transparent/.test(v)) f.push(a+' '+v); const o=e.getAttribute&&(e.getAttribute('opacity')||e.getAttribute(a+'-opacity')); if(o&&+o<1) f.push(a+'-opacity '+o); }); });
  return {la:true, id:c.getAttribute('data-geste'), mode:c.getAttribute('data-mode'), eng:c.getAttribute('data-eng'), pe:cs.pointerEvents, fautes:f,
    main:r?[Math.round((r.left-D.left)/k), Math.round((r.top-D.top)/k)]:null, vis:m?m.getAttribute('visibility'):null, trait:m?m.getAttribute('stroke'):null, fond:m?m.getAttribute('fill'):null,
    fleche:!!c.querySelector('[data-fleche]'), clair:document.getElementById('device').classList.contains('light'),
    drapeaux:Object.keys(localStorage).filter(x=>x.indexOf('geste_vu_')===0).sort()}; }"""
def ouvre(b, reduit=False, th='light', vide=True):
    ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True, reduced_motion=('reduce' if reduit else 'no-preference'))
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__pose')){ localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_theme','%s'); sessionStorage.setItem('__pose','1'); } }catch(e){}" % th)
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:140]))
    return ctx, pg, er
def charge(pg, th):
    pg.goto(URL) if pg.url == 'about:blank' else pg.reload(); pg.wait_for_timeout(6500)
    pg.evaluate("t=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} var d=document.getElementById('device'); if(d.classList.contains('light')!==(t==='light')){ try{ setLight(t==='light'); }catch(e){ d.classList.toggle('light',t==='light'); } } }", th)
    pg.wait_for_timeout(300)
def situe(pg, gid):
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); try{ if(window._dessin&&_dessin.ouvert()) _dessin.sort(); }catch(e){} }"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{ %s }" % SITU[gid])
def attend_main(pg, ms=4200, gid=None):
    ms = max(ms, LENT.get(gid, 0)); t0 = 0
    while t0 < ms:
        pg.wait_for_timeout(300); t0 += 300; e = pg.evaluate(ETAT)
        if e['la'] and (gid is None or e.get('id') == gid): return e
    return pg.evaluate(ETAT)
def cap(pg, nom):
    d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height}}")
    pg.screenshot(path='planche-e1/%s.png' % nom, clip=d)
def rejeu(pg):
    pg.evaluate("()=>{ try{closeAll()}catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); try{ if(window._dessin&&_dessin.ouvert()) _dessin.sort(); }catch(e){} }"); pg.wait_for_timeout(500)   # le Studio garde `.show` (§8) : on repart de l'accueil
    pg.evaluate("()=>document.getElementById('settingsBtn').click()"); pg.wait_for_timeout(1300)
    pg.evaluate("()=>{ const e=document.getElementById('replayOnb'); if(e) e.scrollIntoView({block:'center'}); }"); pg.wait_for_timeout(900)
    bb = pg.evaluate("()=>{ const e=document.getElementById('replayOnb'); if(!e) return null; const r=e.getBoundingClientRect(), h=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2); return {x:r.x+r.width/2, y:r.y+r.height/2, ok:!!(h&&(h===e||e.contains(h))), txt:e.textContent}; }")
    if bb: pg.touchscreen.tap(bb['x'], bb['y'])
    pg.wait_for_timeout(700)
    return bb
with sync_playwright() as p:
    b = p.webkit.launch()
    # ══ l'inventaire ══
    ctx, pg, er = ouvre(b); charge(pg, 'light')
    INV = pg.evaluate("()=>window.GesteFantome ? GesteFantome.inventaire() : null") or []
    regle = pg.evaluate("()=>window.GesteFantome ? GesteFantome.regle : null")
    t('0 · le composant existe, un seul : `GesteFantome.montrer` et `.oublier`', pg.evaluate("()=>!!(window.GesteFantome && typeof GesteFantome.montrer==='function' && typeof GesteFantome.oublier==='function')"))
    t('0 · les valeurs décidées : 600 ms, 900 ms, trois fois, × 1,5, 1,6 s', regle == {'INACTIF': INACTIF, 'PAUSE': PAUSE, 'TOURS': TOURS, 'GRAND': GRAND, 'TRAJET': TRAJET}, regle)
    BR = [g['id'] for g in INV if g['branche']]
    t('0 · l\'inventaire porte au moins : tenir, chiche, noyau, pelote, dessin — et l\'Aura qui paraît, branchée depuis E2bis (v140)', all(x in BR for x in ('tenir', 'chiche', 'noyau', 'pelote', 'dessin', 'aura-apparait')), BR)
    t('0 · chaque geste branché a sa mise en situation dans ce juge', all(x in SITU for x in BR), [x for x in BR if x not in SITU])
    print('\n     INVENTAIRE DES GESTES')
    for g in INV: print('     %-18s %-34s %-9s %s\n     %18s geste : %s%s' % (g['id'], g['ecran'], 'BRANCHÉ' if g['branche'] else 'non', g['condition'], '', g['geste'], ('\n     %18s raison : %s' % ('', g['raison'])) if g['raison'] else ''))
    print()
    json.dump(INV, open('planche-e1/inventaire.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ctx.close()
    # ══ chaque geste branché : première apparition · rechargement · rejeu ══
    for gid in (BR if not SEUL else [SEUL]):
        ctx, pg, er = ouvre(b); charge(pg, 'light')
        toile0 = None
        situe(pg, gid)
        e = attend_main(pg, gid=gid)
        t('%-15s paraît en situation (après 600 ms sans toucher)' % gid, e['la'] and e.get('id') == gid, {k: e.get(k) for k in ('la', 'id', 'mode')})
        if SONDE and e['la']: pg.evaluate("()=>{ const c=document.getElementById('gesteFantome'); c.style.opacity='.6'; c.style.transition='opacity .3s'; }"); e = pg.evaluate(ETAT)
        t('%-15s A2 : `data-eng`, opaque, sans fondu, trait plein à l\'encre du mode' % gid, e['la'] and bool(e.get('eng')) and not e.get('fautes') and (e.get('trait') or '').upper() == '#201908' and (e.get('fond') or '').upper() == '#F7F0DE', '%s · trait %s · fond %s' % (e.get('fautes'), e.get('trait'), e.get('fond')))
        t('%-15s A1 : la couche ne prend aucun toucher' % gid, e.get('pe') == 'none', e.get('pe'))
        t('%-15s le drapeau est posé dès l\'apparition' % gid, ('geste_vu_' + gid) in e['drapeaux'], e['drapeaux'])
        if e['la']: cap(pg, '%s-1-apparition' % gid)
        # elle bouge (hors appui pur) puis s'arrête d'elle-même après deux passages
        p1 = e.get('main'); pg.wait_for_timeout(450); p2 = pg.evaluate(ETAT).get('main')
        pg.wait_for_timeout(13500); fin = pg.evaluate(ETAT)
        t('%-15s elle joue, puis part d\'elle-même (trois passages au plus)' % gid, not fin['la'], 'main %s → %s · encore là : %s' % (p1, p2, fin['la']))
        # un toucher la fait partir : on rejoue le geste par l'API, puis on touche
        pg.evaluate("()=>{ try{ GesteFantome.oublierTout(); }catch(e){} }"); situe(pg, gid); e2 = attend_main(pg, 3600, gid)
        dv = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left+r.width-6, r.top+r.height-6]}")
        if e2['la']: pg.touchscreen.tap(dv[0], dv[1]); pg.wait_for_timeout(120)
        t('%-15s disparaît au premier toucher, sans fondu' % gid, e2['la'] and not pg.evaluate(ETAT)['la'])
        # rechargement : absente
        charge(pg, 'light'); situe(pg, gid); pg.wait_for_timeout(max(4200, LENT.get(gid, 0))); e3 = pg.evaluate(ETAT)
        t('%-15s après rechargement : absente' % gid, not (e3['la'] and e3.get('id') == gid) and ('geste_vu_' + gid) in e3['drapeaux'], {k: e3.get(k) for k in ('la', 'id', 'drapeaux')})
        cap(pg, '%s-2-rechargement' % gid)
        # rejeu : « Revoir les gestes », au doigt, dans les Réglages
        bb = rejeu(pg); dr = pg.evaluate(ETAT)['drapeaux']
        t('%-15s « Revoir les gestes » (Réglages, au doigt) efface les drapeaux' % gid, bool(bb and bb['ok'] and 'Revoir les gestes' in bb['txt']) and not dr, '%s · drapeaux %s' % (bb and bb['txt'], dr))
        situe(pg, gid); e4 = attend_main(pg, gid=gid)
        if not e4['la']: e4['devant'] = pg.evaluate("()=>{ const d=document.getElementById('device').getBoundingClientRect(), h=document.elementFromPoint(d.left+d.width/2, d.top+d.height*0.6); const ch=[]; for(let q=h;q&&q!==document.body;q=q.parentElement) if(q.id) ch.push(q.id); return ch.slice(0,4).join(' < ')+' · inventaire vu : '+JSON.stringify(GesteFantome.inventaire().filter(g=>g.vu).map(g=>g.id)); }")
        t('%-15s après le rejeu : de retour' % gid, e4['la'] and e4.get('id') == gid, {k: e4.get(k) for k in ('la', 'id', 'devant')})
        if e4['la']: cap(pg, '%s-3-rejeu' % gid)
        t('%-15s aucune erreur de page' % gid, not er, er[:2])
        ctx.close()
    # ══ « Réduire les animations » : immobile, avec la flèche du trajet ══
    for gid in (BR if not SEUL else [SEUL]):
        ctx, pg, er = ouvre(b, reduit=True); charge(pg, 'light'); situe(pg, gid); e = attend_main(pg, 3600, gid)
        pg.wait_for_timeout(700); e_ = pg.evaluate(ETAT)
        trajet = gid not in ('fil', 'bande', 'aura-apparait')      # un appui seul n'a pas de trajet : la main, sans flèche
        t('%-15s mouvement réduit : la main immobile%s' % (gid, ', la flèche du trajet' if trajet else ' (un appui : pas de trajet)'), e['la'] and e.get('mode') == 'immobile' and e.get('main') == e_.get('main') and e.get('fleche') == trajet and not e.get('fautes'), {k: e.get(k) for k in ('la', 'mode', 'main', 'fleche')})
        if e['la']: cap(pg, '%s-4-immobile' % gid)
        ctx.close()
    # ══ v139 (C-074, Q429) — « tenir » : LA MAIN TRACE. Suivie image par image dans la page, pendant un passage. ══
    if not SEUL or SEUL == 'tenir':
        ctx, pg, er = ouvre(b); charge(pg, 'light'); situe(pg, 'tenir'); e = attend_main(pg, gid='tenir')
        S_ = pg.evaluate("""()=>new Promise(res=>{ const L=[], t0=performance.now(), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390; (function f(){ const c=document.getElementById('gesteFantome'); const m=c&&c.querySelector('[data-main]'), tr=c&&c.querySelector('[data-trace]');
            if(m){ const r=m.getBoundingClientRect(); let o={t:performance.now()-t0, x:(r.left-dv.left)/k, w:r.width/k, h:r.height/k, vis:m.getAttribute('visibility')!=='hidden'};
              if(tr){ const q=tr.getBoundingClientRect(), cs=getComputedStyle(tr); o.tv=tr.getAttribute('visibility')!=='hidden'; o.tx0=(q.left-dv.left)/k; o.tx1=(q.right-dv.left)/k; o.col=tr.getAttribute('stroke'); o.op=cs.opacity; o.tra=cs.transitionDuration; o.ani=cs.animationName; o.ep=+tr.getAttribute('stroke-width'); } L.push(o); }
            if(performance.now()-t0<3600) requestAnimationFrame(f); else res(L); })(); })""")
        vis = [s for s in S_ if s.get('vis')]; tr = [s for s in S_ if s.get('tv')]
        t('tenir · la main est plus grande (× 1,5 : 49 pt de large, 33 en E1)', bool(vis) and 47.0 <= vis[0]['w'] <= 51.5, 'largeur %.1f pt' % (vis[0]['w'] if vis else -1))
        xs = [s['x'] for s in vis]
        t('tenir · elle va jusqu\'au bout du trait (au-delà de 330 pt ; elle s\'arrêtait à 195 en E1)', bool(xs) and max(xs) + 17 * GRAND >= 330, 'bout du doigt de %.0f à %.0f pt' % (min(xs) + 17 * GRAND if xs else -1, max(xs) + 17 * GRAND if xs else -1))
        # le premier passage seul : du dernier relevé au départ jusqu'au premier relevé à l'arrivée
        i1 = next((i for i, s in enumerate(vis) if s['x'] >= max(xs) - 1), None) if xs else None
        i0 = max([i for i, s in enumerate(vis[:i1 or 0]) if s['x'] <= xs[0] + 1] or [0])
        dur = (vis[i1]['t'] - vis[i0]['t']) if i1 else 0
        t('tenir · le trajet dure environ 1,6 s (± 20 %)', 0.8 * TRAJET <= dur <= 1.2 * TRAJET, '%.0f ms' % dur)
        t('tenir · la seconde moitié se trace sous le doigt : un trait plein, opaque, sans fondu, à la couleur de l\'état', bool(tr) and all((s['col'] or '').upper() == '#DD4D23' and s['op'] == '1' and s['tra'] in ('0s', '') and s['ani'] in ('none', '') and s['ep'] >= 6 for s in tr), str(tr[:1]))
        t('tenir · il part du milieu du trait (195 pt) et grandit avec le doigt', bool(tr) and abs(min(s['tx0'] for s in tr) + tr[0]['ep'] / 2 - 195) <= 12 and tr[-1]['tx1'] - tr[0]['tx1'] > 100 and all(tr[i + 1]['tx1'] >= tr[i]['tx1'] - 0.6 for i in range(len(tr) - 1)), 'de %.0f à %.0f pt' % (tr[0]['tx1'], tr[-1]['tx1']) if tr else '')
        cache = [s for s in S_ if not s.get('vis')]
        t('tenir · le tracé s\'efface quand la main part', bool(cache) and all(not s.get('tv') for s in cache), '%d image(s) sans la main' % len(cache))
        ctx.close()
    # ══ en sombre, et la Toile intacte (A1) ══
    ctx, pg, er = ouvre(b, th='dark'); charge(pg, 'dark'); situe(pg, 'tenir'); e = attend_main(pg)
    t('sombre · la main est à la crème, pleine, sur le fond du mode', e['la'] and (e.get('trait') or '').upper() == '#F7F0DE' and (e.get('fond') or '').upper() == '#050302' and not e.get('fautes'), '%s %s' % (e.get('trait'), e.get('fond')))
    if e['la']: cap(pg, 'tenir-5-sombre')
    ctx.close()
    ctx, pg, er = ouvre(b, reduit=True); charge(pg, 'light')   # « Réduire les animations » : la Toile ne vit pas au repos (v126) — sans quoi elle bouge d'elle-même et la comparaison ne prouve rien
    H = "()=>{ const c=document.getElementById('toileCv'); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let h=0; for(let i=0;i<d.length;i+=97) h=(h*31+d[i])>>>0; return h; }"
    pg.wait_for_timeout(2500)
    h0 = pg.evaluate(H); pg.wait_for_timeout(1200); h1 = pg.evaluate(H)
    r = pg.evaluate("()=>{ const d=document.getElementById('device').getBoundingClientRect(); return GesteFantome.montrer('essai-toile', document.getElementById('toileCv'), [{x:d.left+80,y:d.top+300},{x:d.left+300,y:d.top+420}]); }")
    pg.wait_for_timeout(900); h2 = pg.evaluate(H); la = pg.evaluate("()=>!!document.getElementById('gesteFantome')")
    t('A1 · la main jouée au-dessus de la Toile : aucune dalle ne bouge, le canevas est le même', r and la and h0 == h1 == h2 and pg.evaluate("()=>!document.getElementById('toileCv').contains(document.getElementById('gesteFantome'))"), '%s %s %s%s' % (h0, h1, h2, '' if h0 == h1 else ' (la Toile bougeait déjà sans la main : non concluant)'))
    ctx.close()
    b.close()
print('\nredteam_gestes : %d/%d' % (ok[0], ok[0] + len(ko)))
if ko: print('ROUGE : ' + ' · '.join(ko)); sys.exit(1)
