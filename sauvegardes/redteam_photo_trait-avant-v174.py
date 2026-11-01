#!/usr/bin/env python3
"""redteam_photo_trait.py — ⚑ v164 (Tom, C-201) : LE BOUTON PHOTO NE TOUCHE JAMAIS LE TRAIT.

« Sur la page + (et vérifie aussi les fiches), l'icône pour changer la photo ou le dessin est maintenant posée SUR les pointillés du trait. Remonte-la
juste assez pour qu'aucune partie de l'icône ni de sa zone de toucher ne touche le trait, quel que soit le facteur choisi (vérifie à 1,8), aux
échelles 1 et 0,79. »

Banc comme Tom (WebKit, doigt), Toile de 5 paroles et un Cercle ; les 3 pages + (Promi, Chiche, Cercle) et les fiches (Promi à tenir, Chiche à tenir,
une parole tenue, un Cercle) ; ?trait=1.15 (défaut), 1.3, 1.5, 1.8 ; fenêtres 430 × 932 (échelle 1) et 330 × 714 (≈ 0,79).
Sur chaque écran : la zone de toucher du bouton (sa boîte, ou plus grande si un pseudo-élément l'étend), et l'ENCRE du trait lue sur les pixels du
canevas, colonne par colonne sous le bouton (± 2 pt) : la plus haute. L'écart doit être ≥ 1 pt.
`--tom` : l'état exporté de Tom (A2). Preuve : `--fichier=zz-v163b.html` rougit (la page + d'un Promi à 0,79 : 23 pt dans les pointillés).
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
KS = ['1.3']   # ⚑ v164b : ×1,3 figé, `?trait=` retiré — le défaut seul
FEN = [('1', 430, 932), ('0,79', 330, 714)]
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-78s %s' % ('✅' if ok else '❌', nom, str(d)[:200]), flush=True)
MESURE = """(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, H=document.querySelector(hote);
 if(!H || !H.classList.contains('show')) return {err:'écran fermé'};
 const b=[...H.querySelectorAll('.ph-photo-btn')].find(e=>{ const r=e.getBoundingClientRect(); return r.width>4 && e.offsetParent!==null && getComputedStyle(e).visibility!=='hidden' && r.bottom>dv.top && r.top<dv.bottom; });
 if(!b) return {err:'pas de bouton'};
 let R=b.getBoundingClientRect(); const a=getComputedStyle(b,'::after');
 let bx0=(R.left-dv.left)/k, bx1=(R.right-dv.left)/k, by1=(R.bottom-dv.top)/k;
 if(a && a.content && a.content!=='none'){ const h=parseFloat(a.height)||0, w=parseFloat(a.width)||0; if(h>R.height/k){ by1=(R.top-dv.top)/k + R.height/k/2 + h/2; } if(w>R.width/k){ const cx=(bx0+bx1)/2; bx0=cx-w/2; bx1=cx+w/2; } }
 const cv=H.querySelector('#csTrameCv, #dpTrameCv'); if(!cv) return {err:'pas de canevas'};
 let base, amp; if(cv.id==='csTrameCv' && window._ppEcran){ const e=_ppEcran(); base=e.base; amp=e.amp; } else { const t=(cv.getAttribute('data-trait')||'').split(','); base=+t[0]; amp=+t[1]; }
 if(!isFinite(base)) return {err:'onde inconnue'};
 const C=cv.getBoundingClientRect(), sx=cv.width/C.width, sy=cv.height/C.height, g=cv.getContext('2d'), yc=window._onde.onde(base,amp);
 let haut=1e9;
 for(let x=Math.max(0,bx0-2); x<=Math.min(389,bx1+2); x+=1){ const y=yc(x), px=Math.round((x*k+dv.left-C.left)*sx);
   const y0=Math.max(0, Math.round(((y-34)*k+dv.top-C.top)*sy)), y1=Math.round(((y+34)*k+dv.top-C.top)*sy); if(y1<=y0) continue;
   const d=g.getImageData(px, y0, 1, y1-y0).data, n=d.length/4, c=Math.round((y*k+dv.top-C.top)*sy)-y0;
   if(c<0||c>=n||d[c*4+3]<200) continue; const ref=[d[c*4],d[c*4+1],d[c*4+2]], top=[d[0],d[1],d[2]];
   if(Math.abs(ref[0]-top[0])+Math.abs(ref[1]-top[1])+Math.abs(ref[2]-top[2])<60) continue;   // sous ce point de l'onde, rien n'est tracé (entre deux points)
   for(let i=c;i>=0;i--){ const q=[d[i*4],d[i*4+1],d[i*4+2]]; if(!(d[i*4+3]>100 && Math.abs(q[0]-ref[0])+Math.abs(q[1]-ref[1])+Math.abs(q[2]-ref[2])<90)){ const yy=((y0+i+1)/sy+C.top-dv.top)/k; if(yy<haut) haut=yy; break; } } }
 return {bas:Math.round(by1*10)/10, encre:haut<1e8?Math.round(haut*10)/10:null, ecart:haut<1e8?Math.round((haut-by1)*10)/10:null}; }"""
def ecrans(pg, etiq):
    for nat in ('promi', 'chiche', 'nuee'):
        for essai in range(3):   # une page + qui ne s'est pas ouverte, ou pas encore posée : on attend, puis on la rouvre
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2800)
            m = pg.evaluate(MESURE, '#createSheet')
            if m.get('err') or m.get('encre') is None: pg.wait_for_timeout(1500); m = pg.evaluate(MESURE, '#createSheet')   # le trait pas encore peint : on attend
            if not m.get('err') and m.get('encre') is not None: break
            pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(900)
        juge('[%s] page + %s : le bouton photo au-dessus du trait' % (etiq, nat), m.get('ecart') is not None and m['ecart'] >= 1, m)
        pg.evaluate("()=>{try{closeAll()}catch(e){}}"); pg.wait_for_timeout(700)
    cercle = pg.evaluate("()=>Object.keys(NUE||{}).filter(k=>NUE[k])[0]||null")
    for nom, js in (('fiche Promi à tenir', "promises.find(q=>!q.draft&&!q.chiche&&!q.nuee&&q.status!=='tenu')"), ('fiche Chiche', "promises.find(q=>!q.draft&&q.chiche&&q.status!=='tenu')"),
                    ('fiche tenue', "promises.find(q=>!q.draft&&q.status==='tenu')"), ("fiche d'un Cercle", None)):
        if js and not pg.evaluate("()=>!!(%s)" % js): print('  ·  [%s] %s : aucune dans cet état' % (etiq, nom)); continue
        if not js and not cercle: print('  ·  [%s] aucun Cercle dans cet état' % etiq); continue
        for essai in range(3):
            if js: pg.evaluate("()=>{ const p=%s; if(p) openDetail(p.id); }" % js)
            else: pg.evaluate("(k)=>openNueeDetail(k)", cercle)
            pg.wait_for_timeout(2800)
            m = pg.evaluate(MESURE, '#detailPoster')
            if m.get('err') or m.get('encre') is None: pg.wait_for_timeout(1500); m = pg.evaluate(MESURE, '#detailPoster')   # le trait pas encore peint : on attend
            if not m.get('err') and m.get('encre') is not None: break
            pg.evaluate("()=>{try{window._peaufSortie&&_peaufSortie();closeAll()}catch(e){}}"); pg.wait_for_timeout(900)
        juge('[%s] %s : le bouton photo au-dessus du trait' % (etiq, nom), m.get('ecart') is not None and m['ecart'] >= 1, m)
        pg.evaluate("()=>{try{window._peaufSortie&&_peaufSortie();closeAll()}catch(e){}}"); pg.wait_for_timeout(700)
    er = [x for x in pg.erreurs if 'version.json' not in x] if hasattr(pg, 'erreurs') else []
    if er: juge('[%s] aucune erreur de page' % etiq, False, er[:2])
TOM = '--tom' in sys.argv
with sync_playwright() as p:
    b = p.webkit.launch()
    if TOM:   # A2 · l'état exporté de Tom (le dernier qui porte des paroles), sa fenêtre réelle puis l'échelle 1
        import glob, json, io as _io
        L = [f for f in sorted(glob.glob('etats/tom-*.json')) if json.loads(json.load(_io.open(f, encoding='utf-8')).get('ls', {}).get('promi_state', '{}') or '{}').get('promises')]
        if not L: juge("l'état exporté de Tom existe", False, 'aucun')
        for ech in ((None, 1) if L else ()):
            for K in KS:
                ctx, d = B.contexte_tom(b, L[-1], echelle=ech); pg = ctx.new_page()
                pg.goto('http://127.0.0.1:8752/' + F, timeout=180000); pg.wait_for_timeout(7000)
                ecrans(pg, 'Tom %s · %s · ×%s' % (L[-1].split('/')[-1], ('%s × %s' % (d['ecran'].get('largeur'), d['ecran'].get('hauteur'))) if ech is None else 'échelle 1', K))
                ctx.close()
    else:
      for ech, vw, vh in FEN:
        for K in KS:
            ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 5); pg = B.ouvre(ctx, F, q='')
            pg.evaluate("()=>{ const k='jardin'; NUE[k]='Les jardiniers'; NUEEMEM[k]=['Marion']; NUECREATOR[k]='moi'; promises.filter(q=>!q.draft&&!q.chiche).slice(0,2).forEach(q=>{ q.nuee=k; }); saveState(); syncAll(); }"); pg.wait_for_timeout(500)
            ecrans(pg, '%s · ×%s' % (ech, K))
            ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
