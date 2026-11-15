"""⚑ v203 (Tom, retours sur 58a4ff9, §3, C-280) — MODIFIER LE TITRE D'UNE FICHE EN LE TOUCHANT.
« Titre entier : le premier toucher passe en modification ; titre long, coupé par « … » : le premier toucher le déplie (C-244), le second, sur le titre déplié, passe
en modification. Sur place, même typographie, curseur à l'endroit touché, clavier, sans ouvrir Peaufiner ; mêmes limites que la page + (280, 40 pour le nom d'un
Cercle) ; validée par Retour ou un toucher hors du titre ; un titre vidé puis validé n'est pas accepté : l'ancien revient en se traçant ; le nouveau titre partout
(Index, Fil, fiche, membres) ; la Toile ne change pas (même dalle, même place, même forme) ; la barre Peaufiner reste en bas, la fiche glisse pour garder le titre
au-dessus du clavier. Juge : trois natures, titre court, titre long (déplier puis modifier), titre vidé, titre à la limite. Toile identique au pixel avant et après. »
WebKit, 390 × 844 ×3, au doigt (banc_tom), l'état d'un Cercle (dix paroles, « Le potager »), clavier simulé (visualViewport, iOS ; il s'ouvre aussi sur un élément
modifiable). Chaque fiche s'ouvre par sa carte de l'Index.
  A · le premier toucher sur un titre entier passe en modification (le titre a le focus, la même police et la même taille qu'avant, Peaufiner fermé) ; le
      curseur à l'endroit touché (toucher la fin : la lettre tapée finit le titre)
  B · Retour valide : la parole (ou le Cercle) porte le titre neuf, la fiche l'affiche, la carte de l'Index aussi, le Fil (ses lignes de cette parole), la sauvegarde
  C · la Toile au pixel avant et après (le texte des dalles coupé pour la mesure : il change, c'est le titre), les graines identiques
  D · un titre long coupé : le premier toucher le déplie sans le modifier, le second le modifie
  E · vidé puis validé : l'ancien titre revient, par un tracé (TraceLettres.trace sur le titre)
  F · à la limite : 280 caractères (40 pour un Cercle), pas un de plus
  G · clavier ouvert : le titre (le curseur) au-dessus du clavier ; la barre Peaufiner en bas
  H · un toucher hors du titre valide
--natures=promi,chiche,nuee · --fichier= (rouge sur 58a4ff9 : A et B, la fonction n'existe pas)"""
import sys, json, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
NAT = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--natures=')), ['promi', 'chiche', 'nuee'])
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
LONG = ('aller voir la mer en hiver avec toute la bande et ne pas oublier les gâteaux de mamie, le thermos, les écharpes, les jumelles, '
        'le carnet pour noter les oiseaux et la vieille radio qui grésille quand on la pose sur le sable mouillé du matin')
CLAV = r"""(()=>{ const K=336, D=280; let h=null; const H=()=>innerHeight; const vv=new EventTarget(); Object.defineProperty(vv,'height',{get:()=>h==null?H():h}); Object.defineProperty(vv,'width',{get:()=>innerWidth});
  Object.defineProperty(vv,'scale',{get:()=>1}); Object.defineProperty(vv,'offsetTop',{get:()=>0}); Object.defineProperty(vv,'pageTop',{get:()=>0});
  try{ Object.defineProperty(window,'visualViewport',{get:()=>vv, configurable:true}); }catch(e){}
  let anim=0; function vers(c){ const h0=(h==null?H():h), t0=performance.now(); cancelAnimationFrame(anim); (function f(){ const u=Math.min(1,(performance.now()-t0)/D); h=Math.round(h0+(c-h0)*(1-Math.pow(1-u,3))); vv.dispatchEvent(new Event('resize')); if(u<1) anim=requestAnimationFrame(f); })(); }
  const cle=t=>t && (/^(INPUT|TEXTAREA)$/.test(t.tagName) || t.isContentEditable);
  document.addEventListener('focusin', e=>{ if(cle(e.target)) setTimeout(()=>vers(H()-K), 40); }, true);
  document.addEventListener('focusout', e=>{ if(cle(e.target)) setTimeout(()=>vers(H()), 30); }, true); })()"""   # le clavier d'iOS (336 pt), lu au moment où il s'ouvre
def etat():
    st = json.load(io.open('banc-etats/etat-cercle.json', encoding='utf-8')); st.pop('promi_theme', None)
    s = json.loads(st['promi_state'])
    for p in s['promises']:
        if p['id'] == 151: p['title'] = LONG
        if p['id'] in (145, 147, 151): p['nuee'] = None   # une parole et un Chiche hors du Cercle : leurs cartes sont dans l'Index
    st['promi_state'] = json.dumps(s); return st
SONDE = "(()=>{ (function a(){ if(!window._titreSortie){ setTimeout(a,50); return; } const o=window._titreSortie; window._titreSortie=o; })(); })()"
TI = r"""()=>{ const t=document.getElementById('dptTitre'), d=document.getElementById('detailPoster'); if(!t) return null; const cs=getComputedStyle(t), r=t.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390;
  const b=document.getElementById('dpDetails'), br=b?b.getBoundingClientRect():null; let cur=null; try{ const s=getSelection(); if(s.rangeCount){ const q=s.getRangeAt(0).getClientRects(); const qq=q.length?q[q.length-1]:s.getRangeAt(0).getBoundingClientRect(); cur={y:(qq.bottom-dv.top)/k}; } }catch(_){ }
  return {txt:t.textContent, focus:document.activeElement===t, edit:t.isContentEditable, fam:cs.fontFamily, fs:cs.fontSize, coupe:!!t.getAttribute('data-coupe'), cle:t.getAttribute('data-cle'), dep:window._titreDeplie||null,
    s2:!!(d&&d.classList.contains('s2-ouv')), bas:(r.bottom-dv.top)/k, haut:(r.top-dv.top)/k, cur:cur, vvh:window.visualViewport?(visualViewport.height-dv.top)/k:null, barre:br?[(br.top-dv.top)/k,(br.bottom-dv.top)/k]:null}; }"""
TOILE = r"""async ()=>{ const T=window.Toile; const lo=T.labelsOn; T.labelsOn=()=>false; T.redraw(); await new Promise(r=>setTimeout(r,900)); const c=document.getElementById('toileCv');
  const g=c.getContext('2d'), d=g.getImageData(0,0,c.width,c.height).data; let h=0; for(let i=0;i<d.length;i+=4){ h=(h*31+d[i]+d[i+1]*7+d[i+2]*13)>>>0; }
  T.labelsOn=lo; T.redraw(); const G=(window.Toile_graines?Toile_graines():[]).map(s=>[Math.round(s.x*10)/10,Math.round(s.y*10)/10,Math.round((s.w||0)*10)/10].join(',')).join(';'); return {h:h, g:G, px:Array.from(d)}; }"""
def toile(pg):
    pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(1500)
    r = pg.evaluate(TOILE); return r
def ecart(a, b):
    n = 0
    for i in range(0, min(len(a['px']), len(b['px'])), 4):
        if abs(a['px'][i] - b['px'][i]) + abs(a['px'][i + 1] - b['px'][i + 1]) + abs(a['px'][i + 2] - b['px'][i + 2]) > 6: n += 1
    return n
def ouvre(pg, nat):
    B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2200)
    sel = {'promi': '#indexList .s4-carte[data-pid="145"]', 'chiche': '#indexList .s4-carte[data-pid="147"]', 'nuee': '#indexList .s4-carte[data-nk="potager"]', 'long': '#indexList .s4-carte[data-pid="151"]'}[nat]
    pg.evaluate("(s)=>{ const c=document.querySelector(s); if(c) c.scrollIntoView({block:'center'}); }", sel); pg.wait_for_timeout(500)
    B.tap_sel(pg, sel); pg.wait_for_timeout(2600)
def tap_fin(pg):
    """un toucher sur la DERNIÈRE lettre du titre (le curseur vient à la fin)"""
    p = pg.evaluate("()=>{ const t=document.getElementById('dptTitre'), R=document.createRange(); R.selectNodeContents(t); const q=[...R.getClientRects()].filter(x=>x.width>0).pop(); return [q.right-3, q.top+q.height/2]; }")
    B.tap(pg, p[0], p[1], appareil=False)
def tap_titre(pg):
    p = pg.evaluate("()=>{ const t=document.getElementById('dptTitre'), R=document.createRange(); R.selectNodeContents(t); const q=[...R.getClientRects()].filter(x=>x.width>0)[0]; return [q.left+q.width*0.4, q.top+q.height/2]; }")
    B.tap(pg, p[0], p[1], appareil=False)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_titre_fiche — %s · charge %.1f' % (F, B.charge()))
    st = etat()
    for nat in NAT:
        ctx = B.contexte(b); ctx.add_init_script("try{ if(!sessionStorage.getItem('__etat')){ sessionStorage.setItem('__etat','1'); var E=%s; for(var k in E) localStorage.setItem(k,E[k]); } }catch(e){}" % json.dumps(st))
        ctx.add_init_script(CLAV); ctx.add_init_script("window._vivantOff=true;")
        pg = B.ouvre(ctx, F)
        n = '[%s]' % nat
        T0 = toile(pg)
        ouvre(pg, nat); a0 = pg.evaluate(TI)
        tap_fin(pg); pg.wait_for_timeout(800); a1 = pg.evaluate(TI)
        if not a0 or not a1:
            juge(n + ' la fiche s\'ouvre et son titre se touche', False, (a0, a1)); ctx.close(); continue
        juge(n + ' A · premier toucher : en modification, même police et même taille, Peaufiner fermé', a1 and a1['focus'] and a1['edit'] and a1['fam'] == a0['fam'] and a1['fs'] == a0['fs'] and not a1['s2'], {k: a1.get(k) for k in ('focus', 'edit', 'fs', 's2')} if a1 else a1)
        pg.keyboard.type('X', delay=40); pg.wait_for_timeout(300); a2 = pg.evaluate(TI)
        juge(n + ' A · le curseur à l\'endroit touché (la fin : la lettre tapée finit le titre)', a2 and a2['txt'].endswith('X'), a2 and a2['txt'][-20:])
        g = a2 or {}
        juge(n + ' G · clavier ouvert : le curseur au-dessus du clavier, la barre Peaufiner en bas', g.get('cur') and g.get('vvh') and g['cur']['y'] <= g['vvh'] - 4 and g.get('barre') and g['barre'][1] >= 800, {'cur': g.get('cur'), 'vvh': g.get('vvh'), 'barre': g.get('barre')})
        neuf = a0['txt'] + 'X' if not a0['coupe'] else None
        pg.keyboard.press('Enter'); pg.wait_for_timeout(1200); a3 = pg.evaluate(TI)
        cle = a0['cle']
        donnees = pg.evaluate("(c)=>{ const id=c.slice(2); if(c[0]==='p'){ const p=promises.find(x=>String(x.id)===id); const s=JSON.parse(localStorage.getItem('promi_state')); const q=s.promises.find(x=>String(x.id)===id); return {mem:p&&p.title, sauve:q&&q.title, fil:FEED.filter(f=>String(f.pid)===id).map(f=>f.text)}; } const s=JSON.parse(localStorage.getItem('promi_state')); return {mem:NUE[id], sauve:s.NUE&&s.NUE[id], fil:FEED.filter(f=>f.nuee===id).map(f=>f.text)}; }", cle)
        ok_b = a3 and not a3['edit'] and not a3['focus'] and donnees['mem'] and donnees['mem'].endswith('X') and donnees['sauve'] == donnees['mem'] and a3['txt'].replace('…', '') and (a3['txt'] == donnees['mem'] or donnees['mem'].startswith(a3['txt'].rstrip('…')))
        vieux = [t for t in donnees['fil'] if '« ' + a0['txt'] + ' »' in t]
        juge(n + ' B · Retour valide : la parole, la fiche, la sauvegarde, le Fil portent le titre neuf', ok_b and not vieux, {'mem': (donnees['mem'] or '')[-24:], 'sauve': (donnees['sauve'] or '')[-24:], 'fiche': (a3 or {}).get('txt', '')[-24:], 'fil_ancien': vieux[:2]})
        pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(900)
        B.tap_sel(pg, '#indexBtn'); pg.wait_for_timeout(2200)
        carte = pg.evaluate("(c)=>{ const id=c.slice(2); const e=document.querySelector(c[0]==='p' ? '#indexList .s4-carte[data-pid=\"'+id+'\"] .s4-ti' : '#indexList .s4-carte[data-nk=\"'+id+'\"] .s4-ti'); return e ? e.textContent : null; }", cle)
        juge(n + ' B · la carte de l\'Index porte le titre neuf', carte and (carte == donnees['mem'] or donnees['mem'].startswith(carte.rstrip('…'))), carte)
        T1 = toile(pg); e = ecart(T0, T1)
        juge(n + ' C · la Toile au pixel avant et après (texte des dalles coupé), les graines identiques', e == 0 and T0['g'] == T1['g'], {'pixels': e, 'graines': T0['g'] == T1['g']})
        # E · vidé puis validé
        ouvre(pg, nat); av = pg.evaluate(TI)['txt']
        pg.evaluate("()=>{ window.__trT=[]; const o=TraceLettres.trace; TraceLettres.trace=function(el,c,op){ if(el && el.id==='dptTitre') window.__trT.push(!!(op&&op.inverse)); return o.apply(this, arguments); }; }")
        tap_titre(pg); pg.wait_for_timeout(700)
        pg.keyboard.press('Meta+A'); pg.keyboard.press('Backspace'); pg.wait_for_timeout(200)
        vid = pg.evaluate(TI)['txt']; pg.keyboard.press('Enter'); pg.wait_for_timeout(2500); ae = pg.evaluate(TI); tr = pg.evaluate("()=>window.__trT")
        juge(n + ' E · vidé puis validé : l\'ancien titre revient, par son tracé', vid.strip() == '' and ae['txt'] == av and (False in tr), {'vide': repr(vid[:10]), 'revenu': ae['txt'][-20:], 'traces': tr})
        # F · à la limite
        lim = 40 if nat == 'nuee' else 280
        tap_fin(pg); pg.wait_for_timeout(700); pg.keyboard.press('Meta+A'); pg.keyboard.press('Backspace')
        pg.keyboard.insert_text('a' * (lim + 25)); pg.wait_for_timeout(300); pg.keyboard.type('bbb', delay=20); pg.wait_for_timeout(300)
        af = pg.evaluate(TI); nf = len(af['txt'])
        # H · un toucher hors du titre valide
        pt = pg.evaluate("()=>{ const t=document.getElementById('dptTitre').getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390; const y=(t.top-dv.top)/k; return y>100 ? 70 : 800; }")
        B.tap(pg, 200, pt); pg.wait_for_timeout(1200); ah = pg.evaluate(TI)   # hors du titre : le milieu du plateau (70 pt), ou plus bas si le titre a glissé sous lui (à 0,79, 280 caractères : il couvrait le point (120, 150) d'avant)
        memo = pg.evaluate("(c)=>{ const id=c.slice(2); return c[0]==='p' ? (promises.find(x=>String(x.id)===id)||{}).title : NUE[id]; }", cle)
        juge(n + ' F · à la limite : %d caractères, pas un de plus' % lim, nf == lim and len(memo or '') == lim, {'affiché': nf, 'parole': len(memo or '')})
        juge(n + ' H · un toucher hors du titre valide', ah and not ah['edit'] and not ah['focus'] and len(memo or '') == lim, {'edit': ah and ah['edit'], 'focus': ah and ah['focus']})
        if nat == 'promi':
            # D · un titre long coupé : déplier, puis modifier
            pg.evaluate("()=>{ try{ closeAll(); }catch(e){} }"); pg.wait_for_timeout(900)
            ouvre(pg, 'long'); d0 = pg.evaluate(TI)
            tap_titre(pg); pg.wait_for_timeout(1200); d1 = pg.evaluate(TI)
            tap_fin(pg); pg.wait_for_timeout(800); d2 = pg.evaluate(TI)
            pg.keyboard.type('Z', delay=40); pg.wait_for_timeout(200); pg.keyboard.press('Enter'); pg.wait_for_timeout(1000)
            mz = pg.evaluate("()=>(promises.find(x=>x.id===151)||{}).title")
            juge('[long] D · coupé : le premier toucher déplie sans modifier, le second modifie', d0['coupe'] and d1['dep'] and not d1['edit'] and d2['edit'] and d2['focus'] and (mz or '').endswith('Z'),
                 {'coupe': d0['coupe'], 'déplié': d1['dep'], 'edit1': d1['edit'], 'edit2': d2['edit'], 'fin': (mz or '')[-12:]})
        errs = pg.__dict__.get('erreurs') or []
        juge(n + ' aucune erreur de page', not errs, errs[:2])
        ctx.close()
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
