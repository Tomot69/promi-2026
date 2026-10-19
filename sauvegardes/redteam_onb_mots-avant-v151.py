#!/usr/bin/env python3
"""
redteam_onb_mots.py — v149 (Tom, 18 oct. 2026) : LE I DE PROMI, LES MOTS DES NATURES, LA PHRASE DE FIN — dans tout l'onboarding, clair et sombre.

  C-153 · « Le I de PROMI (le mot-marque, en haut à gauche) clignote sur TOUTES les pages de l'onboarding, dès « Toi, c'est … ? » — même bleu, même
          rythme, même code que l'accueil. » Sur chaque page : l'animation du I est `promiBlink 1.15s steps(1, end)`, la même que celle du I de l'accueil
          (lue sur l'accueil, à la fin) ; sa couleur est celle du I de l'accueil dans le même thème ; ses opacités lues sur 2,4 s passent par 1 et 0,6 ;
          il est à l'écran (rien ne le recouvre). « Promi planté ! » et le panneau du compte n'ont pas de mot-marque en haut à gauche (le titre PROMI le
          remplace, v146) : le juge le dit et passe (question posée à Tom, QUESTIONS). La période mesurée (1,15 s ± 0,1) n'est jugée qu'au calme (charge < 4, C-137).
  C-124 · « Promi, Chiche, Cercle prennent la couleur de leur nature : en sombre exactement #82AEF8, #FFB8D2, #C9A8F5 ; en clair la même teinte foncée
          jusqu'à 3:1 sur le fond ; les trois en GRAS ; même règle partout où ces mots paraissent dans l'onboarding. » Chaque occurrence, sur chaque page :
          sa couleur (EN DUR en sombre ; en clair : la teinte OKLCH de la nature à 3,0–3,3:1 sur #DFCAA4), sa graisse (700).
  C-124 · « Remplacer « Le reste se découvre en traçant. » par « Tout le monde promet. Toi, tu tiens. » (mot pour mot), même place, même rôle, tracé des
          lettres, l'échelle de C-138. » La ligne, son texte EN DUR, juste avant « La suite t'appartient. », à la taille des autres lignes, tracée.
⚑ v150 (Tom, C-124) : la phrase devient « Tout le monde promet. Toi, tu tiens parole. », alignée à DROITE (son encre finit au bord droit du bloc
          de texte, ± 1,5 pt) ; « La suite t'appartient. » est CENTRÉE (le milieu de son encre au milieu du bloc, ± 1,5 pt). Original : *-avant-v150.py.
Preuve : `--page=zz-av148.html` rougit (couleurs à 5:1, graisse 500 hors de la fin, l'ancienne phrase, le I fixe).
"""
import io, os, re, sys
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL = 'http://127.0.0.1:8752/' + next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
CHARGE = float(os.popen('sysctl -n vm.loadavg').read().split()[1])
SOMBRE = {'promi': (130, 174, 248), 'chiche': (255, 184, 210), 'cercle': (201, 168, 245)}   # décision de Tom, en dur
FOND_CLAIR = (223, 202, 164)
FIN_LIGNE = 'Tout le monde promet. Toi, tu tiens parole.'
res = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('  %s %-112s %s' % ('✅' if c else '❌', nom, str(d)[:240]), flush=True)
def lum(c):
    f = lambda x: x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0] / 255) + 0.7152 * f(c[1] / 255) + 0.0722 * f(c[2] / 255)
def ratio(a, b): la, lb = lum(a), lum(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
def rgb(s): m = re.findall(r'[\d.]+', s or ''); return tuple(int(float(x)) for x in m[:3]) if len(m) >= 3 else None
def oklch_h(c):
    l_ = [((x / 255) / 12.92 if (x / 255) <= 0.04045 else (((x / 255) + 0.055) / 1.055) ** 2.4) for x in c]
    L = 0.4122214708 * l_[0] + 0.5363325363 * l_[1] + 0.0514459929 * l_[2]; M = 0.2119034982 * l_[0] + 0.6806995451 * l_[1] + 0.1073969566 * l_[2]; S = 0.0883024619 * l_[0] + 0.2817188376 * l_[1] + 0.6299787005 * l_[2]
    L, M, S = L ** (1 / 3), M ** (1 / 3), S ** (1 / 3)
    a = 1.9779984951 * L - 2.4285922050 * M + 0.4505937099 * S; b = 0.0259040371 * L + 0.7827717662 * M - 0.8086757660 * S
    import math; return math.degrees(math.atan2(b, a)) % 360
LIT_I = """async ()=>{ const v=document.getElementById('onbV'); const mm=v&&v.querySelector('.onbv-mm'), i=mm&&mm.querySelector('i'); if(!i) return {absent:true};
  const hh=document.getElementById('onbHaut'); if(hh && getComputedStyle(hh).display==='none') return {sansMarque:true};
  const s=getComputedStyle(i), r=i.getBoundingClientRect(); let vu=true, e=i; while(e&&e!==document.body){ const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.5){ vu=false; break; } e=e.parentElement; }
  const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); const dessus=!!h && (h===i || i.contains(h) || h===mm);
  const op=[], tr=[]; let av=null; const t0=performance.now();
  for(let k=0;k<60;k++){ const o=+getComputedStyle(i).opacity; op.push(o); if(av!==null && o!==av && o===0.6) tr.push(performance.now()-t0); av=o; await new Promise(z=>setTimeout(z,40)); }
  return {anim:s.animationName, dur:s.animationDuration, tf:s.animationTimingFunction, it:s.animationIterationCount, col:s.color, vu:vu, dessus:dessus, h:h?(h.id||h.className||h.tagName):null, op:[...new Set(op)], tr:tr}; }"""
LIT_NAT = """()=>[...document.querySelectorAll('#onbV .onbv-nat')].filter(e=>{ let v=e; while(v&&v!==document.body){ const c=getComputedStyle(v); if(c.display==='none'||c.visibility==='hidden') return false; v=v.parentElement; } return e.getBoundingClientRect().width>2; })
  .map(e=>{ const c=getComputedStyle(e); return {n:e.getAttribute('data-n'), t:e.textContent, col:c.color, fill:c.webkitTextFillColor, w:+c.fontWeight, f:c.fontFamily.split(',')[0].replace(/["']/g,'').trim(), ou:(e.closest('[id]')||{}).id||''}; })"""
LIT_FIN = """()=>{ const f=document.getElementById('onbFin'); if(!f) return null; const L=[...f.querySelectorAll('.onbv-l')]; const fin=f.querySelector('.onbv-l-fin'), der=f.querySelector('.onbv-l-der');
  const fs=e=>parseFloat(getComputedStyle(e).fontSize);
  const A=e=>{ if(!e) return null; const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, rg=document.createRange(); rg.selectNodeContents(e); const q=rg.getBoundingClientRect(), b=e.getBoundingClientRect(); return {g:+((q.left-b.left)/k).toFixed(1), d:+((b.right-q.right)/k).toFixed(1), c:+((((q.left+q.right)/2)-((b.left+b.right)/2))/k).toFixed(1)}; };
  return {texte:fin?fin.textContent:null, suivant:fin&&fin.nextElementSibling?fin.nextElementSibling.className:null, der:der?der.textContent:null,
    fs:fin?fs(fin):0, alFin:A(fin), alDer:A(der),  ff:fin?getComputedStyle(fin).fontFamily.split(',')[0].replace(/["']/g,'').trim():null, autres:L.filter(l=>l!==fin&&l!==der).map(fs), trace:!!(fin&&fin.__tl), vu:fin?getComputedStyle(fin).visibility:null}; }"""
RECOUVRE = r"""()=>{ const p=document.getElementById('guidePhrase'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; if(!p) return null; const rg=document.createRange(); rg.selectNodeContents(p);
  const L=[...rg.getClientRects()].filter(q=>q.width>1).map(q=>[(q.left-D.left)/k,(q.top-D.top)/k,(q.right-D.left)/k,(q.bottom-D.top)/k]); const pb=p.getBoundingClientRect();
  const tc=document.getElementById('toileCv'), r=tc.getBoundingClientRect(), s=tc.width/r.width, d=tc.getContext('2d').getImageData(0,0,tc.width,tc.height).data, W=tc.width, H=tc.height;
  const lin=x=>{x/=255; return x<=0.04045?x/12.92:Math.pow((x+0.055)/1.055,2.4);};
  const C=(R,G,B)=>{ const l=[lin(R),lin(G),lin(B)]; let a1=Math.cbrt(0.4122214708*l[0]+0.5363325363*l[1]+0.0514459929*l[2]), a2=Math.cbrt(0.2119034982*l[0]+0.6806995451*l[1]+0.1073969566*l[2]), a3=Math.cbrt(0.0883024619*l[0]+0.2817188376*l[1]+0.6299787005*l[2]);
    return Math.hypot(1.9779984951*a1-2.4285922050*a2+0.4505937099*a3, 0.0259040371*a1+0.7827717662*a2-0.8086757660*a3); };
  let dalle=0, tot=0; for(let y=0;y<844;y+=3) for(let x=0;x<390;x+=3){ if(!L.some(l=>x>=l[0]-2&&x<=l[2]+2&&y>=l[1]-2&&y<=l[3]+2)) continue; const X=Math.round(((D.left+x*k)-r.left)*s), Y=Math.round(((D.top+y*k)-r.top)*s); if(X<0||Y<0||X>=W||Y>=H) continue; tot++; const i=(Y*W+X)*4; if(C(d[i],d[i+1],d[i+2])>0.06) dalle++; }
  const ico=[...document.querySelectorAll('.acc-plat svg, .acc-plat button, .acc-plat .acc-mm, #device .acc-barre svg, #device .acc-barre .l, #createBtn')].map(e=>{const q=e.getBoundingClientRect(); return [(q.left-D.left)/k,(q.top-D.top)/k,(q.right-D.left)/k,(q.bottom-D.top)/k,(e.id||(e.className&&e.className.baseVal)||e.className||e.tagName)+''];}).filter(q=>q[2]-q[0]>2);
  const X=(a,b)=>!(a[2]+2<=b[0]||b[2]+2<=a[0]||a[3]+2<=b[1]||b[3]+2<=a[1]);
  const t=(window._guide&&_guide.etat().trou)||null, tz=t?[t.x-t.w/2,t.y-t.h/2,t.x+t.w/2,t.y+t.h/2]:null;
  return {centre:+(((pb.top+pb.bottom)/2-D.top)/k).toFixed(1), dalle:dalle, tot:tot, ico:ico.filter(i=>L.some(l=>X(l,i))).map(i=>i[4]), trou:!!tz && L.some(l=>X(l,tz)), lignes:L.length}; }"""
ACC = """()=>{ const i=document.querySelector('.acc-plat .acc-mm i'); if(!i) return null; const s=getComputedStyle(i); return {anim:s.animationName, dur:s.animationDuration, tf:s.animationTimingFunction, it:s.animationIterationCount, col:s.color}; }"""

with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ('light', 'dark'):
        T = 'clair' if th == 'light' else 'sombre'
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, color_scheme='dark' if th == 'dark' else 'light')
        if th == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        I, NAT = [], []
        def attend_trace():
            for _ in range(50):
                if pg.evaluate(TRACE_FINI): break
                pg.wait_for_timeout(150)
        def releve(page):
            attend_trace(); r = pg.evaluate(LIT_I); r['page'] = page; I.append(r)
            for n in pg.evaluate(LIT_NAT): n['page'] = page; NAT.append(n)
        releve('prénom'); prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); releve('parole'); saisie(pg); pg.wait_for_timeout(600); releve('trait')
        trace(pg, cdp); pg.wait_for_timeout(5200); releve('fin · titre')
        d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
        x, y = d[0] + 195 * d[2], d[1] + 260 * d[2]
        for pas in range(1, 4):
            toucher(cdp, pg, x, y)
            for _ in range(80):
                if pg.evaluate("()=>{ const f=window._onbFinPas&&_onbFinPas(); return !f || (!f.enCours && f.pas>=%d); }" % pas): break
                pg.wait_for_timeout(150)
            pg.wait_for_timeout(500); releve('fin · pas %d' % pas)
        F = pg.evaluate(LIT_FIN)
        toucher(cdp, pg, x, y); pg.wait_for_timeout(1800)
        if pg.evaluate("()=>!!document.querySelector('.onbv-compte')"): releve('compte')
        pg.evaluate("()=>{ const t=document.querySelector('.onbv-compte .tard'); if(t) t.click(); }"); pg.wait_for_timeout(3500)
        for _ in range(60):
            if pg.evaluate("()=>{ const g=document.getElementById('guide'); return !!(g && window._guide && _guide.etat().net>=1); }"): break
            pg.wait_for_timeout(150)
        pg.wait_for_timeout(1200); GR = pg.evaluate(RECOUVRE)
        A = pg.evaluate(ACC)
        # ── C-153
        print('[%s] C-153 — le I de PROMI, %d pages' % (T, len(I)))
        portes = [r for r in I if not r.get('sansMarque')]
        juge('[%s] le mot-marque est en haut à gauche sur les pages du prénom, de la parole et du trait (%s)' % (T, ', '.join(r['page'] for r in portes)), len(portes) >= 3 and [r['page'] for r in portes][:3] == ['prénom', 'parole', 'trait'])
        for r in I:
            if r.get('sansMarque'): print('  ·  « %s » : pas de mot-marque en haut à gauche sur cette page (le titre PROMI le remplace, v146) — question à Tom' % r['page']); continue
            if r.get('absent'): juge('[%s] « %s » : le mot-marque et son I sont là' % (T, r['page']), False, 'absent'); continue
            meme = bool(A) and (r['anim'], r['dur'], r['tf'], r['it']) == (A['anim'], A['dur'], A['tf'], A['it']) and r['anim'] == 'promiBlink' and r['dur'] == '1.15s'
            juge('[%s] « %s » : le I clignote du même code que l\'accueil (%s %s %s)' % (T, r['page'], r['anim'], r['dur'], r['tf']), meme, 'accueil : %s' % A)
            juge('[%s] « %s » : même bleu que le I de l\'accueil, à l\'écran, opacités 1 et 0,6' % (T, r['page']), bool(A) and r['col'] == A['col'] and r['vu'] and r['dessus'] and 1 in r['op'] and 0.6 in r['op'], '%s (accueil %s) · vu %s · dessus %s (%s) · %s' % (r['col'], A and A['col'], r['vu'], r['dessus'], r['h'], r['op']))
        tr = [t for r in I if not r.get('absent') and not r.get('sansMarque') for t in [b_ - a_ for a_, b_ in zip(r['tr'], r['tr'][1:])]]
        if CHARGE < 4 and tr:
            juge('[%s] le rythme mesuré : 1,15 s ± 0,1 entre deux battements (charge %.1f)' % (T, CHARGE), all(abs(t - 1150) <= 100 for t in tr), [round(t) for t in tr][:8])
        else:
            print('  ·  rythme mesuré : non jugé (charge %.1f, C-137) — %s' % (CHARGE, [round(t) for t in tr][:6]))
        # ── C-124 · les natures
        print('[%s] C-124 — Promi, Chiche, Cercle : %d occurrences' % (T, len(NAT)))
        pages = sorted(set(n['page'] for n in NAT))
        juge('[%s] les mots des natures paraissent sur plusieurs pages (%s)' % (T, ', '.join(pages)), len(pages) >= 3 and len(set(n['n'] for n in NAT)) == 3, len(NAT))
        for n in NAT:
            c = rgb(n['col']); fl = rgb(n['fill'])
            if th == 'dark': ok_c = c == SOMBRE[n['n']] and fl == c; d_ = 'exactement %s' % (SOMBRE[n['n']],)
            else:
                r_ = ratio(c, FOND_CLAIR); dh = abs(((oklch_h(c) - oklch_h(SOMBRE[n['n']])) + 180) % 360 - 180)
                ok_c = 3.0 <= r_ <= 3.3 and dh <= 6 and fl == c; d_ = '%.2f:1 sur #DFCAA4, teinte à %.1f° de la nature' % (r_, dh)
            juge('[%s] « %s » · %s (%s) : sa couleur (%s), en GRAS' % (T, n['page'], n['t'], n['ou'], d_), ok_c and n['w'] >= 700, '%s · %s · %s %d' % (n['col'], n['t'], n['f'], n['w']))
        # ── C-124 · la phrase de fin
        print('[%s] C-124 — la ligne de fin' % T)
        juge('[%s] la ligne est « %s », mot pour mot, juste avant « La suite t\'appartient. »' % (T, FIN_LIGNE), bool(F) and F['texte'] == FIN_LIGNE and 'onbv-l-der' in (F['suivant'] or '') and 'appartient' in (F['der'] or ''), F and (F['texte'], F['suivant']))
        juge('[%s] v150 · « … tu tiens parole. » alignée à DROITE (son encre finit au bord droit du bloc, ± 1,5 pt) ; « La suite t\'appartient. » CENTRÉE (± 1,5 pt)' % T,
             bool(F) and F['alFin'] and F['alDer'] and abs(F['alFin']['d']) <= 1.5 and F['alFin']['g'] > 5 and abs(F['alDer']['c']) <= 1.5, F and (F['alFin'], F['alDer']))
        juge('[%s] même rôle : Atkinson, à la taille des autres lignes (22,3 pt × l\'échelle), tracée' % T, bool(F) and F['ff'] == 'Atkinson' and F['autres'] and all(abs(F['fs'] - a) < 0.05 for a in F['autres']) and F['trace'] and F['vu'] == 'visible', F)
        # ── C-145 §4.3, sur le vrai premier lancement de CE thème (redteam_guide ne fait le premier lancement qu'en clair)
        juge('[%s] C-145 · le guide (étape du Studio) : sa phrase, centrée à 252 ± 4, ne recouvre aucune dalle colorée, aucune icône, ni la zone nette' % T, bool(GR) and abs(GR['centre'] - 252) <= 4 and GR['tot'] > 200 and GR['dalle'] == 0 and not GR['ico'] and not GR['trou'], GR)
        ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res))); sys.exit(0 if ok == len(res) else 1)
