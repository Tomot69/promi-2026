# -*- coding: utf-8 -*-
"""LE PARTAGE DE LA PELOTE — seule, ou dans Mon Folio (décision Tom, 24 sept. 2026).
Joué AU DOIGT (CDP Input.dispatchTouchEvent, contexte has_touch) — jamais à la souris (§8).
Valeurs décidées EN DUR : appui long 380 ms, tolérance 8 px (§7 : le juge porte la décision).
Usage : python3 redteam_pelote_partage.py [page]   (défaut app.html)"""
import sys, json, time
from playwright.sync_api import sync_playwright
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
LONG, TOL = 380, 8
res = []
PIEGE_DR = """(()=>{ window.__dr=[]; const P=CanvasRenderingContext2D.prototype, f=P.drawImage;
  P.drawImage=function(src){ try{ if(this.canvas&&this.canvas.id==='shCanvas'){ const a=arguments, n=a.length, T=this.getTransform();
      let dx,dy,dw,dh; if(n>=9){dx=a[5];dy=a[6];dw=a[7];dh=a[8];} else if(n>=5){dx=a[1];dy=a[2];dw=a[3];dh=a[4];} else {dx=a[1];dy=a[2];dw=src.width;dh=src.height;}
      window.__dr.push({pel:(src.id==='auBoule'), x:T.a*dx+T.e, y:T.d*dy+T.f, w:T.a*dw, h:T.d*dh}); } }catch(e){} return f.apply(this,arguments); }; })();"""
TRACES = """()=>{ window.__dr=[]; shareRender(); const D=window.__dr.slice(); const P=D.filter(d=>d.pel), C=D.filter(d=>!d.pel);
  const bad=[]; for(const p of P) for(const c of C){ const ix=Math.min(p.x+p.w,c.x+c.w)-Math.max(p.x,c.x), iy=Math.min(p.y+p.h,c.y+c.h)-Math.max(p.y,c.y);
    if(ix>2&&iy>2) bad.push([Math.round(c.x),Math.round(c.y),Math.round(ix),Math.round(iy)]); }
  return {pelote:P.length, dalles:C.length, recouvrements:bad}; }"""
def ok(nom, cond, det=''):
    res.append((nom, bool(cond), det)); print(('✅' if cond else '❌'), nom, det)

def main(theme):
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=2, has_touch=True)
        # ⚑ ASSAINISSEMENT (30 sept. 2026) — « rien ne se superpose » se juge sur les VRAIS TRACÉS : chaque drawImage sur l'aperçu est
        #   piégé avec son rectangle d'arrivée (transformation comprise) ; la Pelote est celle dont la source est son canevas (#auBoule),
        #   les autres sont les dalles. Avant, le contrôle croisait les cases et le bloc que l'app PUBLIE (`_plancheComp`) : l'app se
        #   notait elle-même. La composition publiée reste un POINTEUR (où toucher), jamais le verdict.
        #   Original : sauvegardes/redteam_pelote_partage-avant-assainissement.py
        ctx.add_init_script(PIEGE_DR)
        pg = ctx.new_page()
        pg.goto('http://127.0.0.1:8752/' + PAGE); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        cdp = ctx.new_cdp_session(pg)
        def touch(t, x, y):
            pts = [] if t == 'touchEnd' else [{'x':x,'y':y,'id':1}]
            cdp.send('Input.dispatchTouchEvent', {'type':t, 'touchPoints':pts})
        pg.evaluate("()=>openShare()"); pg.wait_for_timeout(2500)
        fond = 'Clair' if theme == 'clair' else 'Sombre'
        pg.evaluate("""(f)=>{var row=[...document.querySelectorAll('#shcPile .shc-reg')].find(c=>/FOND DE L/.test((c.querySelector('.l')||{}).textContent||''));
            var b=row&&[...row.querySelectorAll('button')].find(x=>x.textContent.trim()===f); if(b) b.click();}""", fond)
        pg.wait_for_timeout(800)
        ok(theme+' · le fond de l\'image est bien '+fond, pg.evaluate("()=>typeof _sealDark!=='undefined'?_sealDark:null") == (theme != 'clair'))
        # — 1 · Ma Toile : la Pelote ne s'y ajoute plus —
        pg.evaluate("()=>{document.querySelector('#shMode [data-mode=toile]').click(); window.shPelote=true; shareRender();}")
        pg.wait_for_timeout(900)
        r = pg.evaluate("""()=>{var row=[...document.querySelectorAll('#shcPile .shc-reg')].find(c=>c.querySelector('[data-pel]'));
            return {rowVis: row?getComputedStyle(row).display!=='none':null,
                    compo: document.getElementById('shCanvas').getAttribute('data-compo')}}""")
        ok(theme+' · Ma Toile : la rangée « La Pelote » ne paraît pas', r['rowVis'] is False, str(r))
        ok(theme+' · Ma Toile : aucune composition Pelote n\'est peinte', not r['compo'], str(r))
        # — 2 · Mon Folio —
        pg.evaluate("()=>{document.querySelector('#shMode [data-mode=mosaic]').click();}"); pg.wait_for_timeout(800)
        pg.evaluate("()=>{window.shPelote=true; window.shPelBR=1; window.shPelBC=0; shareRender();}"); pg.wait_for_timeout(1500)
        r = pg.evaluate("""()=>{var row=[...document.querySelectorAll('#shcPile .shc-reg')].find(c=>c.querySelector('[data-pel]'));
            var h=document.getElementById('shHint');
            return {rowVis: row?getComputedStyle(row).display!=='none':null, hint: h?getComputedStyle(h).display:null}}""")
        ok(theme+' · Mon Folio : la rangée « La Pelote » paraît', r['rowVis'] is True, str(r))
        ok(theme+' · Mon Folio : l\'invite du doigt ne barre pas la planche', r['hint'] == 'none', str(r))
        def etat():
            return pg.evaluate("""()=>{var C=window._plancheComp||{}; var B=C.bloc||null;
               var c=document.getElementById('shCanvas').getBoundingClientRect(); var G=C.grille||null;
               var sx=G?c.width/G.W:1, sy=G?c.height/G.H:1;
               return {n:C.n, ids:(C.cases||[]).map(q=>q.id).sort(), cases:C.cases, bloc:B, G:G&&{cols:G.cols,maxR:G.maxR},
                 br:window.shPelBR, bc:window.shPelBC, prise:!!window._shPelPrise,
                 centre: B?[c.x+(B.x+B.w/2)*sx, c.y+(B.y+B.h/2)*sy]:null, cv:[c.x,c.y,c.width,c.height], sx:sx, sy:sy}}""")
        e0 = etat()
        ok(theme+' · la géométrie du bloc est publiée', e0['bloc'] is not None and e0['G'] is not None, str(e0['bloc']))
        if not e0['bloc']:
            b.close(); return
        cx, cy = e0['centre']
        def aucun_recouvrement(e):
            B = e['bloc']; bad = []
            for q in e['cases']:
                if q['x'] < B['x']+B['w']-1 and q['x']+q['cw'] > B['x']+1 and q['y'] < B['y']+B['h']-1 and q['y']+q['cw'] > B['y']+1:
                    bad.append(q['id'])
            return bad
        # — 3 · un GLISSEMENT rapide sans appui long ne déplace rien —
        touch('touchStart', cx, cy); pg.wait_for_timeout(60)
        for i in range(1, 8):
            touch('touchMove', cx + i*25, cy - i*30); pg.wait_for_timeout(16)
        touch('touchEnd', 0, 0); pg.wait_for_timeout(400)
        e1 = etat()
        ok(theme+' · glissement rapide : la Pelote reste en place', (e1['br'], e1['bc']) == (e0['br'], e0['bc']) and e1['bloc']['r'] == e0['bloc']['r'] and e1['bloc']['c'] == e0['bloc']['c'], f"{e0['bloc']['r'],e0['bloc']['c']} → {e1['bloc']['r'],e1['bloc']['c']}")
        cx, cy = etat()['centre']
        # — 4 · une dérive lente qui dépasse la tolérance AVANT l'appui long ne prend rien —
        touch('touchStart', cx, cy); pg.wait_for_timeout(150)
        touch('touchMove', cx + TOL + 6, cy); pg.wait_for_timeout(LONG + 200)
        prise = pg.evaluate("()=>!!window._shPelPrise")
        for i in range(1, 6):
            touch('touchMove', cx + TOL + 6 + i*30, cy - i*40); pg.wait_for_timeout(30)
        touch('touchEnd', 0, 0); pg.wait_for_timeout(400)
        e2 = etat()
        ok(theme+' · un doigt qui bouge avant 380 ms ne prend pas la Pelote', not prise and (e2['bloc']['r'], e2['bloc']['c']) == (e0['bloc']['r'], e0['bloc']['c']), f"prise={prise}")
        # — 5 · un appui long immobile la PREND ; on la glisse en haut à droite —
        e0b = etat(); cx, cy = e0b['centre']
        touch('touchStart', cx, cy); pg.wait_for_timeout(LONG + 150)
        prise = pg.evaluate("()=>!!window._shPelPrise && document.getElementById('shareScreen').classList.contains('sh-pel-prise')")
        ok(theme+' · appui long immobile : la Pelote est prise', prise)
        cvx, cvy, cvw, cvh = e0b['cv']
        tx, ty = cvx + cvw*0.80, cvy + cvh*0.14
        N = 14
        for i in range(1, N+1):
            touch('touchMove', cx + (tx-cx)*i/N, cy + (ty-cy)*i/N); pg.wait_for_timeout(40)
        pg.wait_for_timeout(300)
        em = etat()
        ok(theme+' · pendant le geste, la planche se recompose (case visée en haut à droite)', em['bloc']['r'] == 0 and em['bloc']['c'] == e0['G']['cols']-2, f"bloc {em['bloc']['r'],em['bloc']['c']}")
        touch('touchEnd', 0, 0); pg.wait_for_timeout(700)
        e3 = etat()
        ok(theme+' · au lâcher, la Pelote est posée où on l\'a laissée', not e3['prise'] and e3['bloc']['r'] == 0 and e3['bloc']['c'] == e0['G']['cols']-2, f"{e3['bloc']['r'],e3['bloc']['c']}")
        ok(theme+' · rien ne disparaît (mêmes Promi)', e3['ids'] == e0['ids'] and e3['n'] == e0['n'], f"{e0['n']} → {e3['n']}")
        _t3 = pg.evaluate(TRACES)
        ok(theme+' · rien ne se superpose au bloc (au tracé)', _t3['pelote'] == 1 and _t3['dalles'] > 0 and not _t3['recouvrements'], str(_t3))
        # — 6 · tout en bas : pas de rangée vide —
        c3 = e3['centre']
        touch('touchStart', c3[0], c3[1]); pg.wait_for_timeout(LONG + 150)
        for i in range(1, N+1):
            touch('touchMove', c3[0] + (cvx+cvw*0.2-c3[0])*i/N, c3[1] + (cvy+cvh*0.97-c3[1])*i/N); pg.wait_for_timeout(40)
        touch('touchEnd', 0, 0); pg.wait_for_timeout(700)
        e4 = etat()
        rows_items = set((q['y']) for q in e4['cases'])
        ok(theme+' · posée tout en bas : bornée à la dernière rangée utile', e4['bloc']['r'] == e4['G']['maxR'], f"r={e4['bloc']['r']} maxR={e4['G']['maxR']}")
        _t4 = pg.evaluate(TRACES)
        ok(theme+' · posée tout en bas : rien ne disparaît, rien ne se superpose (au tracé)', e4['ids'] == e0['ids'] and _t4['pelote'] == 1 and _t4['dalles'] > 0 and not _t4['recouvrements'], str(_t4))
        # — 7 · l'export est l'aperçu —
        pg.evaluate("()=>{HTMLCanvasElement.prototype.toBlob=function(){};}")
        for mode in ('mosaic', 'pelote', 'toile'):
            pg.evaluate("(m)=>{document.querySelector('#shMode [data-mode='+m+']').click();}", mode); pg.wait_for_timeout(1200)
            ex = pg.evaluate("""()=>{var c=(window._shExporteCanevas||window.shareExport)(); if(!c||!c.width) return null;
                 var t=document.createElement('canvas'); t.width=60; t.height=Math.round(60*c.height/c.width);
                 t.getContext('2d').drawImage(c,0,0,t.width,t.height);
                 var p=document.getElementById('shCanvas'); var u=document.createElement('canvas'); u.width=t.width; u.height=t.height;
                 u.getContext('2d').drawImage(p,0,0,u.width,u.height);
                 var a=t.getContext('2d').getImageData(0,0,t.width,t.height).data, bb=u.getContext('2d').getImageData(0,0,t.width,t.height).data, s=0;
                 for(var i=0;i<a.length;i+=4) s+=Math.abs(a[i]-bb[i])+Math.abs(a[i+1]-bb[i+1])+Math.abs(a[i+2]-bb[i+2]);
                 return {W:c.width, H:c.height, ecart:s/(a.length/4)/3, px:c.width*c.height}}""")
            ok(theme+f' · export {mode} : l\'image est l\'aperçu (écart moyen < 12 niveaux)', ex and ex['ecart'] < 12, str(ex))
            ok(theme+f' · export {mode} : sous le plafond iPhone (16,7 Mpx)', ex and ex['px'] <= 16777216, str(ex and ex['px']))
        b.close()

for th in ('sombre', 'clair'):
    main(th)
n_ok = sum(1 for r in res if r[1])
print(f"\n{n_ok}/{len(res)}")
for r in res:
    if not r[1]: print('RATE :', r[0], r[2])
