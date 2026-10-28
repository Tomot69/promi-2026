#!/usr/bin/env python3
"""redteam_couleurs_exactes — v169 (Tom, C-204 §1).

« Dans la phrase du guide, les lettres de STUDIO reprennent EXACTEMENT les couleurs de la palette par défaut, en clair comme en sombre :
#82AEF8, #FFB8D2, #C9A8F5, #EFE3C7, dans l'ordre de la palette. » Le juge lit la couleur CALCULÉE de chaque lettre (la phrase posée par le guide,
`_guide.montre('studio')`), à l'hexadécimal près, deux thèmes, deux échelles (1 et 0,79).

L'OPTION (Q589) — `--exact` : sous `?exact=1`, « monde » et « partage-la » #C9A8F5, Promi · Chiche · Cercle de la phrase du + #82AEF8 · #FFB8D2 ·
#C9A8F5, et les mêmes trois mots dans l'onboarding, en clair comme en sombre. Sans `?exact=1`, ces mots gardent leurs couleurs d'avant (C-145, C-124) :
le juge vérifie aussi qu'elles n'ont PAS bougé (A5).

Les valeurs sont EN DUR. `--fichier=zz-v168c.html` : rouge (les dérivées de Q533).
"""
import sys
from playwright.sync_api import sync_playwright

F = 'app.html'
for a in sys.argv[1:]:
    if a.startswith('--fichier='): F = a.split('=', 1)[1]
OPTION = '--exact' in sys.argv
PAL = ['#82AEF8', '#FFB8D2', '#C9A8F5', '#EFE3C7']                 # la palette par défaut (Ingénu), dans son ordre — les valeurs de Tom
STUDIO = [PAL[i % 4] for i in range(6)]                            # S t u d i o
NAT = {'promi': '#82AEF8', 'chiche': '#FFB8D2', 'cercle': '#C9A8F5'}
AVANT_CLAIR = {'monde': '#8363AA', 'partage-la': '#8363AA'}          # C-145, v165 : sans ?exact=1, rien ne bouge
res = []

def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True)

def hexa(s):
    import re
    m = re.findall(r'[\d.]+', s or '')
    return '#%02X%02X%02X' % tuple(int(round(float(x))) for x in m[:3]) if len(m) >= 3 else s

def page(b, sombre, vw, vh, q=''):
    ctx = b.new_context(viewport={'width': vw, 'height': vh}, device_scale_factor=3, has_touch=True, is_mobile=True)
    ctx.add_init_script("try{ if(!sessionStorage.getItem('__ini')){ sessionStorage.setItem('__ini','1'); localStorage.setItem('promi_theme','%s'); localStorage.setItem('promi_onb','1'); localStorage.setItem('promi_rappel_n','9'); localStorage.setItem('promi_veille_off','1'); } }catch(e){}" % ('dark' if sombre else 'light'))
    pg = ctx.new_page(); er = []; pg.on('pageerror', lambda e: er.append(str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/' + F + q, timeout=180000); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(300)
    return ctx, pg, er

def phrase(pg, quoi):
    pg.evaluate("q=>{ try{ _guide.finir&&_guide.finir(); }catch(e){} _guide.montre(q, true); }", quoi)
    for _ in range(60):
        v = pg.evaluate("""()=>{ const p=document.getElementById('guidePhrase'); if(!p) return null;
          const c=e=>getComputedStyle(e).color, f=e=>getComputedStyle(e).webkitTextFillColor;
          return {lettres:[...p.querySelectorAll('.gd-studio .gd-l')].map(e=>[e.textContent,c(e),f(e)]),
                  cles:[...p.querySelectorAll('.gd-cle:not(.gd-studio)')].map(e=>[e.textContent,c(e),f(e)]),
                  nats:[...p.querySelectorAll('.gd-nat')].map(e=>[e.textContent,c(e),f(e)])}; }""")
        if v and (v['lettres'] or v['cles'] or v['nats']): return v
        pg.wait_for_timeout(150)
    return None

def onb_nats(pg):
    """les natures de l'onboarding : celles de la fin (Primo, Deuxio, Tertio), posées par le module de l'onboarding (sa fonction nat)"""
    return pg.evaluate("""()=>{ try{ window._onbNat && window._onbNat(); }catch(e){}
      return [...document.querySelectorAll('#onbV .onbv-nat')].map(e=>[e.getAttribute('data-n'), getComputedStyle(e).color, getComputedStyle(e).webkitTextFillColor]); }""")

with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, ech in ((390, 844, '1'), (330, 714, '0,79')):
        for sombre in (False, True):
            T = '%s · %s' % ('sombre' if sombre else 'clair', ech)
            ctx, pg, er = page(b, sombre, vw, vh)
            v = phrase(pg, 'studio') or {'lettres': []}
            L = v['lettres']
            got = [(l[0], hexa(l[1]), hexa(l[2])) for l in L]
            juge('[%s] « Studio » : chaque lettre à sa couleur de palette, à l\'hexadécimal près (color et fill)' % T,
                 ''.join(l[0] for l in L) == 'Studio' and all(got[i][1] == STUDIO[i] and got[i][2] == STUDIO[i] for i in range(6)), got)
            if not sombre:   # A5 : sans ?exact=1, « monde » et la phrase du + ne bougent pas
                mo = [hexa(c[1]) for c in v.get('cles', []) if c[0] == 'monde']
                juge('[%s] sans ?exact=1, « monde » garde #8363AA (C-145, rien d\'autre ne bouge)' % T, mo == ['#8363AA'], mo)
            juge('[%s] aucune erreur de page' % T, not er, er[:2])
            ctx.close()
    if OPTION:
        for sombre in (False, True):
            T = '%s · ?exact=1' % ('sombre' if sombre else 'clair')
            ctx, pg, er = page(b, sombre, 390, 844, '?exact=1')
            v = phrase(pg, 'studio') or {}
            mo = [(c[0], hexa(c[1]), hexa(c[2])) for c in v.get('cles', []) if c[0] == 'monde']
            juge('[%s] « monde » #C9A8F5' % T, mo and all(m[1] == m[2] == '#C9A8F5' for m in mo), mo)
            v = phrase(pg, 'plus') or {}
            na = [(n[0], hexa(n[1]), hexa(n[2])) for n in v.get('nats', [])]
            juge('[%s] Promi, Chiche, Cercle de la phrase du + aux couleurs exactes' % T,
                 [n[0] for n in na] == ['Promi', 'Chiche', 'Cercle'] and all(n[1] == n[2] == NAT[n[0].lower()] for n in na), na)
            v = phrase(pg, 'partage') or {}
            pl = [(c[0], hexa(c[1]), hexa(c[2])) for c in v.get('cles', []) if c[0] == 'partage-la']
            juge('[%s] « partage-la » #C9A8F5' % T, pl and all(x[1] == x[2] == '#C9A8F5' for x in pl), pl)
            juge('[%s] aucune erreur de page' % T, not er, er[:2])
            ctx.close()
        # l'onboarding : stockage vierge, l'onboarding s'affiche ; on lit les natures que son module pose (fonction natCol), dans les deux thèmes
        for sombre in (False, True):
            T = '%s · onboarding · ?exact=1' % ('sombre' if sombre else 'clair')
            ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
            ctx.add_init_script("try{ if(!sessionStorage.getItem('__ini')){ sessionStorage.setItem('__ini','1'); localStorage.setItem('promi_theme','%s'); } }catch(e){}" % ('dark' if sombre else 'light'))
            pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + F + '?exact=1', timeout=180000); pg.wait_for_timeout(6000)
            # les natures n'existent qu'aux pages de la fin : on pose un témoin par la fonction du module (le même chemin que la page)
            n = pg.evaluate("""()=>{ const h=document.getElementById('onbV'); if(!h) return null; const d=document.createElement('div'); d.id='__tem';
              d.innerHTML=['promi','chiche','cercle'].map(k=>'<i class="onbv-nat" data-n="'+k+'">x</i>').join(''); h.appendChild(d); try{ window._onbNat(); }catch(e){ return 'pas de _onbNat'; }
              const r=[...d.querySelectorAll('.onbv-nat')].map(e=>[e.getAttribute('data-n'), e.style.color, e.style.webkitTextFillColor]); d.remove(); return r; }""")
            ok = isinstance(n, list) and len(n) == 3 and all(hexa(x[1]) == NAT[x[0]] and hexa(x[2]) == NAT[x[0]] for x in n)
            juge('[%s] Promi, Chiche, Cercle aux couleurs exactes' % T, ok, [(x[0], hexa(x[1])) for x in n] if isinstance(n, list) else n)
            ctx.close()
    b.close()
print('\n%d/%d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
