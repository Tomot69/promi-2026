#!/usr/bin/env python3
"""
redteam_murs_toucher.py — CHAQUE MUR DE L'APP : LA PHRASE DÈS LE PREMIER TOUCHER, VINGT FOIS SUR VINGT (v141, Tom, 10 oct. 2026 — C-100).

« Au Studio, toucher une zone floutée ne réagit qu'une fois sur quatre. Nomme la cause. Chaque mur de l'app : la phrase dès le premier
toucher, vingt fois sur vingt. »

Gratuit, au VRAI DOIGT (CDP). Pour chaque mur, vingt touchers répartis sur toute la zone floutée visible — et un doigt n'est pas un clic de
banc : il GLISSE de quelques points (0 à 7 pt, dans toutes les directions) et reste posé de 50 à 170 ms. Après chaque toucher, la phrase doit
être là ; on la baisse (`_murBaisse`) et l'on recommence. Vingt sur vingt, pour chaque mur.

Les murs : le Studio (panneau fermé, puis palettes ouvertes, sur un monde de Ma Parole !) · le Peaufiner d'une fiche · le Peaufiner de la
page + · l'Aura (« Ce qu'on t'a tenu ») · l'aide de l'Aura · les notifications · les couleurs du dessin.

Usage : python3 redteam_murs_toucher.py [fichier.html] [--seul=studio|palettes|fiche|plus|aura|aide|notifs|dessin]
"""
import sys, math
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if not a.startswith('--')), 'app.html')
SEUL = next((a.split('=')[1] for a in sys.argv[1:] if a.startswith('--seul=')), None)
N = 20
res = []
def juge(nom, cond, detail=''):
    res.append((nom, bool(cond))); print('%s  %s  %s' % ('OK' if cond else 'KO', nom, detail), flush=True)
# la zone floutée VISIBLE d'un mur : la réunion des éléments (de la liste) qui portent un flou, bornée à l'appareil et à ce qui les rogne
ZONE = """(sels)=>{ const D=document.getElementById('device').getBoundingClientRect(); let u=null;
  sels.forEach(s0=>{ const panneau=s0.charAt(0)==='!', s=panneau?s0.slice(1):s0; document.querySelectorAll(s).forEach(e=>{ const c=getComputedStyle(e), r=e.getBoundingClientRect(); if(c.display==='none'||c.visibility==='hidden'||r.width<4||r.height<1) return;
    let fl=panneau;   /* « ! » : un panneau dont le contenu flouté n'est pas un descendant (le Studio) */ for(let q=e;q&&q.id!=='device';q=q.parentElement){ const f=getComputedStyle(q).filter; if(f&&f.indexOf('blur')>=0){ fl=true; break; } } if(!fl){ const k=e.querySelector('*'); fl=[...e.querySelectorAll('*')].some(x=>{const f=getComputedStyle(x).filter; return f&&f.indexOf('blur')>=0;}); } if(!fl) return;
    let x0=Math.max(r.left,D.left), x1=Math.min(r.right,D.right), y0=Math.max(r.top,D.top), y1=Math.min(r.bottom,D.bottom);
    for(let q=e.parentElement;q&&q.id!=='device';q=q.parentElement){ const cq=getComputedStyle(q); if(/(auto|scroll|hidden)/.test(cq.overflowY+cq.overflowX)){ const rq=q.getBoundingClientRect(); x0=Math.max(x0,rq.left); x1=Math.min(x1,rq.right); y0=Math.max(y0,rq.top); y1=Math.min(y1,rq.bottom); } }
    if(x1-x0<4||y1-y0<1) return; u=u?[Math.min(u[0],x0),Math.min(u[1],y0),Math.max(u[2],x1),Math.max(u[3],y1)]:[x0,y0,x1,y1]; }); });
  return u; }"""
LEVE = "()=>{ const m=document.getElementById('murPhrase'); return {leve:!!(m&&m.classList.contains('leve')), offre:!!document.querySelector('#plusScreen.show')}; }"
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    def session():
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now(),der:2,decouvert:1}))}catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(false)}catch(e){} }"); pg.wait_for_timeout(500)
        return ctx, pg, cdp
    def doigt(pg, cdp, x, y, i):
        a = i * 2.39996; d = (i % 4) * 2.3; dx, dy = d * math.cos(a), d * math.sin(a); ms = 50 + (i * 37) % 121     # 0 à 7 pt de glissement, 50 à 170 ms
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]}); pg.wait_for_timeout(ms // 2)
        if d: cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x + dx * 0.5, 'y': y + dy * 0.5}]}); pg.wait_for_timeout(8); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': x + dx, 'y': y + dy}]})
        pg.wait_for_timeout(ms // 2); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
    LIBRE = """([x,y,sels])=>{ if(!sels) return false; for(const q of sels){ const e=document.querySelector(q); if(!e) continue; const r=e.getBoundingClientRect(); if(r.width>2 && x>=r.left-4 && x<=r.right+4 && y>=r.top-4 && y<=r.bottom+4) return true; } return false; }"""
    def vingt(nom, pg, cdp, sels, prepare=None, libres=None):
        # ⚑ v163b (C-198) : sur un monde payant, Sombre/Clair, Avec/Sans texte (et leurs mots) et les barrettes ne sont plus des murs — un toucher
        #    qui tombe sur eux ne fait paraître NI phrase NI offre (ils agissent) ; tout autre toucher du panneau reste exigé, 20 sur 20.
        #    Original : sauvegardes/redteam_murs_toucher-avant-v163b.py
        z = pg.evaluate(ZONE, sels)
        if not z: juge('[%s] la zone floutée est à l\'écran' % nom, False, 'aucune zone floutée trouvée pour %s' % sels); return
        bons = 0; rates = []; nlib = 0; libok = 0; librates = []; nflou = 0
        for i in range(N):
            if prepare: prepare()
            z = pg.evaluate(ZONE, sels) or z
            w, h = z[2] - z[0], z[3] - z[1]; m = 9
            x = z[0] + m + (w - 2 * m) * ((i % 5) + 0.5) / 5.0; y = z[1] + min(m, h * 0.25) + (h - 2 * min(m, h * 0.25)) * ((i // 5) + 0.5) / 4.0
            # un vrai bouton posé sur le mur (« Adopte ce design », sur le haut du panneau des palettes) n'est pas la zone floutée : on descend sous lui
            for _ in range(12):
                # ni à moins de 20 pt de lui : le navigateur rabat un toucher sur le bouton voisin (mesuré : à 5 pt sous « Adopte ce design », le clic part sur lui)
                if not pg.evaluate("([x,y])=>[[0,0],[0,-20],[0,20],[-20,0],[20,0]].some(d=>{const h=document.elementFromPoint(x+d[0],y+d[1]); return !!(h&&h.closest&&h.closest('button,#stLockBuy,#stLockCta'));})", [x, y]): break
                y += 12
            if '--dbg' in sys.argv: print(i, round(x), round(y), pg.evaluate("([x,y])=>document.elementsFromPoint(x,y).slice(0,3).map(e=>e.id||(''+e.className).slice(0,18)||e.tagName).join(' < ')", [x, y]))
            lib = pg.evaluate(LIBRE, [x, y, libres])
            _a = i * 2.39996; _d = (i % 4) * 2.3; xf, yf = x + _d * math.cos(_a), y + _d * math.sin(_a)   # là où le doigt se lève (doigt() glisse de 0 à 7 pt)
            if libres and lib != pg.evaluate(LIBRE, [xf, yf, libres]): nflou += 1; continue   # posé dans une zone, levé dans l'autre : ni l'un ni l'autre ne juge
            doigt(pg, cdp, x, y, i); pg.wait_for_timeout(650)
            e = pg.evaluate(LEVE)
            if lib:
                nlib += 1
                if not e['leve'] and not e['offre']: libok += 1
                else: librates.append('(%d ; %d)%s' % (x, y, ' offre' if e['offre'] else ' phrase'))
            elif e['leve'] and not e['offre']: bons += 1
            else: rates.append('(%d ; %d)%s sous le doigt : %s' % (x, y, ' offre' if e['offre'] else '', pg.evaluate("([x,y])=>document.elementsFromPoint(x,y).slice(0,3).map(e=>e.id||(''+e.className).slice(0,18)||e.tagName).join(' < ')", [x, y])))
            pg.evaluate("()=>{ try{ _murBaisse(); }catch(e){} const c=document.querySelector('#plusScreen.show .closeb'); if(c) c.click(); }"); pg.wait_for_timeout(420)
        juge('[%s] la phrase dès le premier toucher : %d sur %d (zone floutée %d × %d pt)' % (nom, bons, N - nlib - nflou, w, h), bons == N - nlib - nflou and N - nlib - nflou >= 4, ('ratés : ' + ' '.join(rates[:8])) if rates else '')
        if libres: juge('[%s] sur les réglages libres (C-198), ni phrase ni offre : %d sur %d' % (nom, libok, nlib), nlib >= 3 and libok == nlib, ' '.join(librates[:6]))
    def studio(pals):
        ctx, pg, cdp = session(); pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(6000)
        d = pg.evaluate("()=>document.getElementById('device').getBoundingClientRect().toJSON()")
        if pals:
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': d['x'] + 75, 'y': d['y'] + 620}]}); pg.wait_for_timeout(60); cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1500)
        for k in range(14):
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchStart', 'touchPoints': [{'x': d['x'] + 320, 'y': d['y'] + 300}]})
            for i in range(1, 11): pg.wait_for_timeout(16); cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [{'x': d['x'] + 320 - i * 24, 'y': d['y'] + 300}]})
            cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []}); pg.wait_for_timeout(1500)
            if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
        pg.wait_for_timeout(2500)
        vingt('le Studio, palettes ouvertes' if pals else 'le Studio, panneau', pg, cdp, ['#studioScreen #stpPals'] if pals else ['!#studioScreen #stpBas'], libres=None if pals else ['#studioScreen #stpVue', '#studioScreen #stpLab', '#studioScreen #stpDots'])   # le panneau entier : ses bandes floutées ET ce qui les sépare
        ctx.close()
    def fiche():
        ctx, pg, cdp = session()
        pg.evaluate("()=>{closeAll();const p=promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0];openDetail(p.id);}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const x=document.querySelector('#dpDetails .dpd-tog');if(x)x.click();}"); pg.wait_for_timeout(1600)
        pg.evaluate("()=>{const e=document.querySelector('#detailPoster .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(700)
        vingt('le Peaufiner d\'une fiche', pg, cdp, ['#detailPoster .s2-cercle:not(.v16-seul)']); ctx.close()
    def plus():
        ctx, pg, cdp = session()
        pg.evaluate("()=>{ closeAll(); document.getElementById('createBtn').click(); }"); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ const t=document.querySelector('#createSheet .tuile[data-kind=promi], #createSheet [data-kind=promi]'); if(t&&document.getElementById('createSheet').classList.contains('pp-choix')) t.click(); }"); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ const x=document.querySelector('#csBotBar .cbb-peauf, #csBotBar'); if(x) x.click(); }"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{const e=document.querySelector('#createSheet.pp-peauf .s2-cercle:not(.v16-seul)');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(700)
        vingt('le Peaufiner de la page +', pg, cdp, ['#createSheet.pp-peauf .s2-cercle:not(.v16-seul)']); ctx.close()
    def aura():
        ctx, pg, cdp = session(); pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{const e=document.querySelector('#auCadre.au-voile .au-gr2');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(800)
        vingt('l\'Aura', pg, cdp, ['#auCadre.au-voile .au-gr2']); ctx.close()
    def aide():
        ctx, pg, cdp = session(); pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(3000)
        pg.evaluate("()=>{ const a=document.getElementById('auraHelp'); try{ if(typeof openAuraHelp==='function') openAuraHelp(); else { const b=document.querySelector('#auraScreen .au-aide, #auraScreen [data-aide], #auHelpBtn'); if(b) b.click(); else a.classList.add('show'); } }catch(e){ a.classList.add('show'); } }"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const e=document.querySelector('#auraHelp .ah-locked');if(e)e.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(800)
        vingt('l\'aide de l\'Aura', pg, cdp, ['#auraHelp .ah-locked']); ctx.close()
    def notifs():
        ctx, pg, cdp = session(); pg.evaluate("()=>{ try{ window._notifPage(); }catch(e){} }"); pg.wait_for_timeout(1800)
        vingt('les notifications', pg, cdp, ['#notifScreen .nt-mur']); ctx.close()
    def dessin():
        ctx, pg, cdp = session()
        pg.evaluate("()=>{closeAll();const p=promises.filter(p=>!p.draft&&!p.req&&!p.nuee)[0];openDetail(p.id);}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ try{ window._dessin.ouvre(); }catch(e){} }"); pg.wait_for_timeout(1500)
        def prep():
            if not pg.evaluate("()=>!!document.querySelector('#dessinMode.ouv .dz-couleurs.dz-mur')"):
                if not pg.evaluate("()=>!!document.getElementById('dessinMode')"): pg.evaluate("()=>{ try{ window._dessin.ouvre(); }catch(e){} }"); pg.wait_for_timeout(1200)
                pg.evaluate("()=>{ const b=document.querySelector('#dessinMode [data-outil=couleur]'); if(b) b.click(); }"); pg.wait_for_timeout(600)
        prep(); vingt('les couleurs du dessin', pg, cdp, ['#dessinMode.ouv .dz-couleurs.dz-mur'], prep); ctx.close()
    TOUS = [('studio', lambda: studio(False)), ('palettes', lambda: studio(True)), ('fiche', fiche), ('plus', plus), ('aura', aura), ('aide', aide), ('notifs', notifs), ('dessin', dessin)]
    for k, f in TOUS:
        if SEUL and k != SEUL: continue
        try: f()
        except Exception as e: juge('[%s] le mur s\'ouvre et se touche' % k, False, repr(e)[:200])
    b.close()
ok = sum(1 for _, c in res if c)
print('\n%d / %d' % (ok, len(res))); sys.exit(0 if ok == len(res) and res else 1)
