# LE LOT DU CERCLE, INTÉGRÉ — VÉRIFIÉ À L'ÉCRAN (11 sept. 2026), deux thèmes, AVANT les batteries.
# Chaque contrat nomme ce qu'il vérifie et ce qu'il a trouvé (CLAUDE §8 : un instrument nomme ce qui rate).
# Les portes sont touchées AU POINT (souris) ; l'encart l'est aussi au VRAI DOIGT (événements tactiles CDP).
import json, os, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, 'integration'); os.makedirs(OUT, exist_ok=True)
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
PEAUF = "()=>{const x=document.querySelector('#dpDetails .dpd-tog'); if(x) x.click();}"
ORDRE = ['RÉCURRENCE', 'RAPPEL', "C'EST IMPORTANT ?", 'LA MÉMOIRE']
L2 = "prévenir Rachel la veille, apporter le gâteau et les bougies"
L3 = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
OUTILS = r"""()=>{ window.__V = {
 lignes(c){ const r=c.getBoundingClientRect(), cs=getComputedStyle(c); const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2); const F=[];
   const w=document.createTreeWalker(c,NodeFilter.SHOW_TEXT); let n;
   while((n=w.nextNode())){ if(!n.textContent.trim()) continue; const p=n.parentElement; if(!p.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})||p.closest('textarea')) continue;
     const g=document.createRange(); g.selectNodeContents(n); [...g.getClientRects()].forEach(q=>{ if(q.width>1) F.push({l:q.left,t:q.top,b:q.bottom}); }); }
   c.querySelectorAll('textarea,input:not([type=file])').forEach(e=>{ if(!e.checkVisibility()) return; const k=getComputedStyle(e), er=e.getBoundingClientRect(); const d=document.createElement('div');
     ['fontFamily','fontSize','fontWeight','letterSpacing','lineHeight'].forEach(p=>d.style[p]=k[p]);
     d.style.cssText+=';position:fixed;visibility:hidden;white-space:pre-wrap;word-wrap:break-word;left:'+(er.left+parseFloat(k.paddingLeft))+'px;top:'+(er.top+parseFloat(k.paddingTop))+'px;width:'+(er.width-parseFloat(k.paddingLeft)-parseFloat(k.paddingRight))+'px';
     d.textContent=e.value||e.placeholder||''; document.body.appendChild(d); const g=document.createRange(); g.selectNodeContents(d);
     [...g.getClientRects()].forEach(q=>{ if(q.width>1 && q.top<er.bottom-1) F.push({l:q.left,t:q.top,b:q.bottom}); }); d.remove(); });
   F.sort((a,b)=>a.t-b.t); const L=[]; F.forEach(f=>{ const x=L.find(y=>Math.abs((y.t+y.b)/2-(f.t+f.b)/2)<4); if(x){x.l=Math.min(x.l,f.l);x.t=Math.min(x.t,f.t);x.b=Math.max(x.b,f.b);} else L.push({...f}); });
   L.sort((a,b)=>a.t-b.t); const cy=r.height/2, ri=R-bw;
   const e=(ln)=>{ const t=ln.t-r.top, b=ln.b-r.top, l=ln.l-r.left; const hm=b<cy, bm=t>cy; const py=hm?t:(bm?b:(t+b)/2); const ay=py<R?R:(py>r.height-R?r.height-R:py);
     return l<R?(ri-Math.hypot(l-R,py-ay)):(l-bw); };
   let air=Infinity; for(let i=0;i+1<L.length;i++) air=Math.min(air, L[i+1].t-L[i].b);
   const air_haut = L.length>=3 ? L[1].t-L[0].b : null, air_bas = L.length>=3 ? L[L.length-1].t-L[L.length-2].b : null;
   // le texte du MILIEU (la 2e ligne d'un champ à 3 lignes ; le bloc des lignes de texte sinon) : écarts au haut et au bas du contour
   const mid = L.length>=3 ? {t:L[1].t-r.top, b:L[L.length-2].b-r.top} : null;
   return {lignes:L.length, h:+r.height.toFixed(1), rayon:+R.toFixed(1), premiere:L.length?+e(L[0]).toFixed(1):null, derniere:L.length?+e(L[L.length-1]).toFixed(1):null,
     air_min:isFinite(air)?+air.toFixed(1):null, air_haut: air_haut==null?null:+air_haut.toFixed(1), air_bas: air_bas==null?null:+air_bas.toFixed(1), milieu_haut: mid? +(mid.t-bw).toFixed(1):null, milieu_bas: mid? +((r.height-bw)-mid.b).toFixed(1):null}; },
 mur(hote){ const b=document.querySelector(hote+' .s2-cercle'); if(!b) return null; const enc=b.querySelector('.s2-encart');
   return {ordre:[...b.querySelectorAll(':scope > .s2-reg .s2-lab')].map(x=>x.textContent), encart: enc? enc.textContent.trim():null, encart_vis: !!(enc&&enc.checkVisibility()),
     sous_titre: !!b.querySelector('.s2-enc-s'), flous:[...b.querySelectorAll(':scope > .s2-reg')].map(r=>getComputedStyle(r).filter), doigt:[...b.querySelectorAll(':scope > .s2-reg')].map(r=>getComputedStyle(r).pointerEvents)}; },
 etat(){ const ps=document.getElementById('plusScreen'); return {couches:[...document.querySelectorAll('.show')].map(e=>e.id).filter(i=>i&&i!=='scrim').sort().join(','),
   dessus: ps.classList.contains('cercle-dessus'), ps_show: ps.classList.contains('show'), premium: document.getElementById('device').classList.contains('premium'),
   fiche_peauf: document.getElementById('detailPoster').classList.contains('show') && document.getElementById('detailPoster').classList.contains('s2-ouv'),
   pp_peauf: document.getElementById('createSheet').classList.contains('show') && document.getElementById('createSheet').classList.contains('pp-peauf'),
   titre: (document.getElementById('fTitle')||{}).value, phrase: window._phrase && window._phrase.titre}; },
 /* ⚠ ON NE FAIT DÉFILER QUE CE QUI EST HORS DE L'APPAREIL : un scrollIntoView sur la barre de la page + (déjà en bas, visible)
    déplaçait toute la page — la barre remontait à y 424 — et le toucher tombait ailleurs (sonde du 11 sept. : la barre ouvre
    son Peaufiner dans les 8 cas, souris et doigt, avant et après le lot ; c'était l'instrument). */
 point(sel){ const e=document.querySelector(sel); if(!e) return null; const dv=document.getElementById('device').getBoundingClientRect(); let r=e.getBoundingClientRect();
   if(r.top<dv.top || r.bottom>dv.bottom){ e.scrollIntoView({block:'center'}); r=e.getBoundingClientRect(); } const x=r.left+r.width*0.8, y=r.top+r.height/2;
   const h=document.elementFromPoint(x,y); return {x, y, recoit:(h&&(h===e||e.contains(h)))?'soi':(h?(h.id||String(h.className).split(' ')[0]):null)}; },
 dessusVisible(){ const ps=document.getElementById('plusScreen'), r=ps.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+320); return !!(h&&ps.contains(h)); }
}; }"""
R = {}; KO = []
def ok(nom, cond, detail):
    R.setdefault(TH, []).append((nom, bool(cond), detail))
    print('   %s %s  %s' % ('✓' if cond else '✗', nom, detail))
    if not cond: KO.append('%s · %s · %s' % (TH, nom, detail))
with sync_playwright() as p:
    br = p.chromium.launch()
    for TH in ('dark', 'light'):
        print('\n════ %s' % TH)
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg); pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", TH); pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS)
        def cap(n): pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s.png' % (TH, n)))
        def clic(sel):
            pt = pg.evaluate("(s)=>window.__V.point(s)", sel); pg.wait_for_timeout(250)
            pt = pg.evaluate("(s)=>window.__V.point(s)", sel)
            if pt: pg.mouse.click(pt['x'], pt['y'])
            return pt
        def fiche(pid=126):
            # ⚠ plus d'id en dur : les numéros du jeu changent d'un chargement à l'autre (126 une fois sur quatre, 142 sinon —
            #   chantier 71 ; ma première note disait « passée ratée dans la soirée » : faux). On prend le premier Promi en cours adressé à quelqu'un, comme releve-S2.
            #   (Une première écriture avait collé ce commentaire AU MILIEU de la ligne : le toucher sur la barre Peaufiner était
            #   passé en commentaire, et le mur « manquait » — c'était l'instrument.)
            pg.evaluate(BASE); pg.wait_for_timeout(200)
            pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee) || promises.find(q=>!q.draft && !q.nuee); openDetail(p.id); return p.id; }")
            pg.wait_for_timeout(1400); pg.evaluate(PEAUF); pg.wait_for_timeout(1700)
        # A · le mur d'une fiche
        fiche(); m = pg.evaluate("()=>window.__V.mur('#detailPoster')")
        ok('fiche · ordre', m and m['ordre'] == ORDRE, m and m['ordre'])
        ok('fiche · encart « ✦ Le Cercle » seul', m and m['encart'] == '✦ Le Cercle' and not m['sous_titre'], m and (m['encart'], m['sous_titre']))
        ok('fiche · floutés et intouchables', m and all('blur(2.4px)' in f for f in m['flous']) and all(d == 'none' for d in m['doigt']), m and (m['flous'][:1], m['doigt']))
        pg.evaluate("()=>document.querySelector('#detailPoster .s2-cercle').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); cap('A_fiche_mur')
        # B · les champs : rayon 30, texte centré, écart constant
        for i, nom in ((0, 'NOTE'), (1, 'COMMENTAIRES')):
            z = pg.evaluate("(i)=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[i]; z.scrollIntoView({block:'center'}); return window.__V.lignes(z); }", i)
            ok('fiche · %s · rayon 30' % nom, abs(z['rayon'] - 30) < 0.6, z['rayon'])
            ok('fiche · %s · texte du milieu centré (écarts égaux)' % nom, z['milieu_haut'] is not None and abs(z['milieu_haut'] - z['milieu_bas']) <= 1.0, (z['milieu_haut'], z['milieu_bas']))
            ok('fiche · %s · début des lignes extrêmes ≥ 12,9' % nom, z['premiere'] >= 12.4 and z['derniere'] >= 12.4, (z['premiere'], z['derniere']))
        cap('B_fiche_champs')
        for cas, t in (('deux lignes', L2), ('trois lignes', L3)):
            fiche()
            z = pg.evaluate("(t)=>{ const z=document.querySelectorAll('#detailPoster .s2-zone')[0]; const x=z.querySelector('textarea'); x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); z.scrollIntoView({block:'center'}); return null; }", t)
            pg.wait_for_timeout(500)
            z = pg.evaluate("()=>window.__V.lignes(document.querySelectorAll('#detailPoster .s2-zone')[0])")
            # ⚑ CONTRAT RÉÉCRIT AVANT TOUTE SÉRIE : il comparait l'air entre TOUTES les lignes voisines, interligne du paragraphe
            #    compris (0,5 = 22 px de dessin dans une ligne de 22,5 : l'interligne normal du texte). Le défaut vu par Tom est
            #    ENTRE BLOCS : le texte contre « visible par Rachel ». On mesure donc libellé → texte et texte → visibilité.
            ok('NOTE %s · le texte ne touche ni le libellé ni la visibilité (air ≥ 10)' % cas, z['air_haut'] is not None and z['air_haut'] >= 10 and z['air_bas'] >= 10,
               (z['lignes'], z['h'], 'libellé→texte', z['air_haut'], 'texte→visibilité', z['air_bas'], 'dans le paragraphe', z['air_min']))
            ok('NOTE %s · écart constant (≥ 12,9)' % cas, z['premiere'] >= 12.4 and z['derniere'] >= 12.4, (z['premiere'], z['derniere']))
            ok('NOTE %s · centré' % cas, abs(z['milieu_haut'] - z['milieu_bas']) <= 1.0, (z['milieu_haut'], z['milieu_bas']))
            cap('B_note_%s' % cas.replace(' ', '_'))
        # remettre la note vide (ne rien laisser dans les données du jeu)
        pg.evaluate("()=>{ const x=document.getElementById('dNote'); x.value=''; x.dispatchEvent(new Event('input',{bubbles:true})); }")
        # C · le mur de la page +, D · le gardé de côté
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
        pg.evaluate("()=>{window._phrase={sens:'faire',qui:'Moi',titre:'aller voir la mer',quand:'un jour'}; if(window._phraseRendu)_phraseRendu(); document.getElementById('fTitle').value='aller voir la mer';}"); pg.wait_for_timeout(500)
        clic('#csBotBar'); pg.wait_for_timeout(1800)
        m = pg.evaluate("()=>window.__V.mur('#createSheet')")
        ok('page + · le mur est posé', m is not None and len(m['ordre']) == 4, m and m['ordre'])
        ok('page + · ordre, encart, floutés, intouchables', m and m['ordre'] == ORDRE and m['encart'] == '✦ Le Cercle' and all('blur(2.4px)' in f for f in m['flous']) and all(d == 'none' for d in m['doigt']), m)
        z = pg.evaluate("()=>{ const z=document.querySelector('#createSheet .s2-zone'); return z ? window.__V.lignes(z) : null; }")
        ok('page + · NOTE rayon 30, centrée', z is not None and abs(z['rayon'] - 30) < 0.6 and abs(z['milieu_haut'] - z['milieu_bas']) <= 1.0, z or 'aucun champ : le Peaufiner de la page + ne s’est pas ouvert')
        pg.wait_for_timeout(1200)   # laisser passer les rebâtisseurs de la liste (90/280/650 ms)
        ok('page + · le mur tient après les rebâtisseurs', pg.evaluate("()=>!!document.querySelector('#createSheet .s2-cercle')"), '')
        pg.evaluate("()=>{const b=document.querySelector('#createSheet .s2-cercle'); if(b) b.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(300); cap('C_pageplus_mur')
        # E · le chemin depuis la page + : encart → par-dessus → ✕ → retour, phrase intacte ; puis encart → achat → retour, nets
        pt = clic('#createSheet .s2-encart'); pg.wait_for_timeout(1000); e = pg.evaluate("()=>window.__V.etat()")
        ok('page + · l’encart ouvre le Cercle PAR-DESSUS', e['ps_show'] and e['dessus'] and e['pp_peauf'] and pg.evaluate("()=>window.__V.dessusVisible()"), (pt and pt['recoit'], e['couches']))
        cap('E_pageplus_dessus')
        clic('#plusScreen .closeb'); pg.wait_for_timeout(800); e = pg.evaluate("()=>window.__V.etat()")
        ok('page + · ✕ ramène au même Peaufiner, phrase intacte', (not e['ps_show']) and e['pp_peauf'] and e['phrase'] == 'aller voir la mer' and e['titre'] == 'aller voir la mer', e)
        clic('#createSheet .s2-encart'); pg.wait_for_timeout(900)
        pg.evaluate("()=>{const s=document.getElementById('plusScreen'); s.scrollTop=s.scrollHeight;}"); pg.wait_for_timeout(400)
        clic('#buyYear'); pg.wait_for_timeout(1300); e = pg.evaluate("()=>window.__V.etat()")
        m = pg.evaluate("()=>window.__V.mur('#createSheet')")
        ok('page + · l’achat ramène au même Peaufiner (pas l’Aura), phrase intacte', e['premium'] and (not e['ps_show']) and e['pp_peauf'] and 'auraScreen' not in e['couches'] and e['phrase'] == 'aller voir la mer', e)
        ok('page + · abonné : nets et touchables, encart effacé', bool(m) and all(f == 'none' for f in m['flous']) and all(d == 'auto' for d in m['doigt']) and not m['encart_vis'], m)
        pg.evaluate("()=>{const b=document.querySelector('#createSheet .s2-cercle'); if(b) b.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(300); cap('E_pageplus_apres_achat')
        pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(400)
        # D · le gardé de côté
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>{const d=promises.find(p=>p.draft); if(d) openDetail(d.id);}"); pg.wait_for_timeout(1800)
        clic('#csBotBar'); pg.wait_for_timeout(1800)
        m = pg.evaluate("()=>window.__V.mur('#createSheet')")
        ok('gardé de côté · le mur est posé', m is not None and m['ordre'] == ORDRE, m and m['ordre'])
        pg.evaluate("()=>{const b=document.querySelector('#createSheet .s2-cercle'); if(b) b.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(300); cap('D_garde_mur')
        # F · le chemin depuis une fiche, AU VRAI DOIGT sur l'encart
        fiche(); pt = pg.evaluate("()=>window.__V.point('#detailPoster .s2-encart')"); pg.wait_for_timeout(300)
        pt = pg.evaluate("()=>window.__V.point('#detailPoster .s2-encart')")
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': pt['x'], 'y': pt['y']}]}); pg.wait_for_timeout(60)
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1400)
        e = pg.evaluate("()=>window.__V.etat()")
        ok('fiche · au doigt, l’encart ouvre le Cercle par-dessus, et il RESTE ouvert', e['ps_show'] and e['dessus'] and e['fiche_peauf'] and pg.evaluate("()=>window.__V.dessusVisible()"), (pt['recoit'], e['couches']))
        cap('F_fiche_dessus')
        pg.evaluate("()=>{const s=document.getElementById('plusScreen'); s.scrollTop=s.scrollHeight;}"); pg.wait_for_timeout(400)
        clic('#buyMonth'); pg.wait_for_timeout(1300); e = pg.evaluate("()=>window.__V.etat()"); m = pg.evaluate("()=>window.__V.mur('#detailPoster')")
        ok('fiche · l’achat ramène au même Peaufiner, réglages nets et touchables', e['premium'] and (not e['ps_show']) and e['fiche_peauf'] and 'auraScreen' not in e['couches'] and m and all(f == 'none' for f in m['flous']) and all(d == 'auto' for d in m['doigt']), (e['couches'], m and m['flous'][:1]))
        pg.evaluate("()=>document.querySelector('#detailPoster .s2-cercle').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); cap('F_fiche_apres_achat')
        # G · l'encart des Réglages après une fin d'abonnement
        pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('settingsBtn').click()"); pg.wait_for_timeout(1700)
        g = pg.evaluate("()=>{ const op=document.getElementById('openPlusTop'); op.scrollIntoView({block:'center'}); const s=op.querySelector('.sc-s'); return {t:op.querySelector('.sc-t').textContent, sous_titre_visible: !!(s&&s.checkVisibility()), vis: op.checkVisibility(), ordre:[...document.querySelectorAll('#settingsScreen .s2-cercle > .s2-reg .s2-lab')].map(x=>x.textContent)}; }")
        ok('Réglages · après fin d’abonnement : « ✦ Le Cercle », sans sous-titre, visible', g['t'] == '✦ Le Cercle' and not g['sous_titre_visible'] and g['vis'], g)
        ok('Réglages · ordre', g['ordre'] == ORDRE, g['ordre'])
        pg.wait_for_timeout(300); cap('G_reglages')
        # H · la Nuée
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(1500); pg.evaluate(PEAUF); pg.wait_for_timeout(1700)
        for cid in ('npDesc', 'npComm'):
            z = pg.evaluate("(i)=>{ const z=document.getElementById(i); z.scrollIntoView({block:'center'}); return window.__V.lignes(z); }", cid)
            ok('Nuée · %s · rayon 30, centré, écart ≥ 12,9' % cid, abs(z['rayon'] - 30) < 0.6 and abs(z['milieu_haut'] - z['milieu_bas']) <= 1.0 and z['premiere'] >= 12.4 and z['derniere'] >= 12.4, z)
        pj = pg.evaluate("""()=>{ const c=document.getElementById('npFich'), r=c.getBoundingClientRect(); const rg=(e)=>{const g=document.createRange(); g.selectNodeContents(e); return +(g.getClientRects()[0].top-r.top).toFixed(1);};
            return {lab:rg(c.querySelector('.np-lab')), bas:rg(c.querySelector('.np-bas'))}; }""")
        ok('Nuée · PIÈCES JOINTES aux places de la fiche (23 / 50,8)', abs(pj['lab'] - 23) <= 0.6 and abs(pj['bas'] - 50.8) <= 0.6, pj)
        pg.evaluate("()=>{const c=document.querySelector('#detailPoster .dpd-corps'); if(c) c.scrollTop=0;}"); pg.wait_for_timeout(300); cap('H_nuee')
        # I · les autres portes gardent leur chemin
        pg.evaluate(BASE); pg.wait_for_timeout(300); clic('#cercleTopBtn'); pg.wait_for_timeout(1000); e = pg.evaluate("()=>window.__V.etat()")
        ok('accueil · la porte du haut ouvre le Cercle sans « par-dessus »', e['ps_show'] and not e['dessus'], e['couches'])
        ctx.close()
    br.close()
json.dump(R, open(os.path.join(OUT, 'verif.json'), 'w'), ensure_ascii=False, indent=1)
print('\n══ %d contrat(s) raté(s)' % len(KO))
for k in KO: print('   ✗ ' + k)
