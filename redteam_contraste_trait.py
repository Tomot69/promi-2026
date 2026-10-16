#!/usr/bin/env python3
"""
redteam_contraste_trait.py — v147 (Tom, 15 oct. 2026, C-140) : « Sur la fiche du Cercle, le trait et le violet du fond sont de la même couleur.
C'est une erreur dans le choix des violets ; c'est cheap et moche. » Règle : le trait (points et partie tracée) se détache de CHACUN des deux
fonds — le champ au-dessus de l'onde, le corps au-dessous — avec un contraste mesuré d'au moins 3:1 (WCAG). Même règle pour le Chiche et le Promi.

Lu SUR L'IMAGE (WebKit, 390 × 844 ×3) : le trait au centre de l'onde que le peintre déclare (`data-trait`), le champ 6 pt au-dessus de son bord,
le corps 6 pt au-dessous ; médiane sur plusieurs abscisses (la partie tracée, puis les points). Contextes : la fiche (à tenir, en cours ; et chaque
pinceau de Peaufiner), les cartes de l'Index et du Fil, la page + à la création — trois natures, clair et sombre.
Le seuil (3,0) est EN DUR. Verdicts : OK · KO (une couleur de trait tiendrait 3:1 face aux deux fonds) · IMPOSSIBLE (aucune couleur ne le peut avec
ces deux fonds : le meilleur atteignable est écrit — la décision revient aux fonds, Q de v147). `--vite` : un seul pinceau (Plein). `--page=` : une autre page servie (la version d'avant).
"""
import sys, io, json
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
SEUIL = 3.0
PAGE = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
VITE = '--vite' in sys.argv
PINCEAUX = ['Plein'] if VITE else ['Plein', 'Coulé', 'Peigné', 'Sec', 'Tressé', 'Frangé', 'Doublé', 'Fendu', 'Cranté', 'Vrillé', 'Semé', 'Perlé']
def lum(c):
    def f(v):
        v = v / 255.0; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
def ratio(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
def med(L):
    if not L: return None
    return tuple(sorted(p[i] for p in L)[len(L) // 2] for i in range(3))
def hexa(c): return '#%02X%02X%02X' % c if c else '—'
def atteignable(a, b):
    """le meilleur des plus faibles contrastes qu'un trait d'UNE couleur peut obtenir face aux deux fonds (WCAG) : noir, blanc, ou la
    luminance moyenne géométrique entre les deux fonds"""
    la, lb = sorted((lum(a), lum(b)))
    c1 = (la + 0.05) / 0.05; c2 = 1.05 / (lb + 0.05); c3 = (((lb + 0.05) * (la + 0.05)) ** 0.5) / (la + 0.05)
    return max(min(c1, (lb + 0.05) / 0.05), min(c2, 1.05 / (la + 0.05)), c3)
# la géométrie déclarée par le peintre, en points ÉCRAN (client) : l'onde, le trait, les points
GEO = r"""(sel)=>{ const out=[];
  /* la nature, lue sur la carte (son libellé) ou sur la fiche ; et seuls comptent les points que le DOIGT atteint sur ce canevas (une carte
     cachée sous le plateau, sous une autre, ou hors de l'écran ne se mesure pas) */
  const nat=cv=>{ const c=cv.closest('.s4-carte')||cv.parentNode; const l=c&&c.querySelector&&c.querySelector('.s4-natlab'); if(l) return l.textContent.trim();
    const dp=cv.closest('#detailPoster'); if(dp) return dp.classList.contains('dp-chiche')?'Chiche':((dp.classList.contains('dp-nuee')||dp.classList.contains('dp-mode-nuee'))?'Cercle':'Promi'); return '?'; };
  const vus=(cv,S,v)=>S.filter(s=>{ const pts=v?[[s.h,s.y],[s.b,s.y],[s.x,s.y]]:[[s.x,s.h],[s.x,s.b],[s.x,s.y]];
      return pts.every(p=>{ if(p[0]<0||p[1]<0||p[0]>innerWidth||p[1]>innerHeight) return false; const h=document.elementFromPoint(p[0],p[1]); const c=cv.closest('.s4-carte')||cv.closest('#detailPoster')||cv.closest('#createSheet')||cv.parentNode;
        return !!h && (h===cv || c.contains(h) || h.contains(cv)); }); });
  document.querySelectorAll(sel).forEach(cv=>{ const t=(cv.getAttribute('data-trait')||'').split(','); if(t.length<4) return;
  const r=cv.getBoundingClientRect(); if(r.width<20||r.height<20||r.bottom<0||r.top>innerHeight) return;
  const carte=t[4]==='carte', W=carte?+t[5]:390, k=r.width/W, base=+t[0], amp=+t[1], per=carte?1:1.5, larg=W;
  const y=x=>{ const u=Math.max(0,Math.min(1,x/larg)); return base-amp*0.34*u-amp*0.62*Math.sin(2*Math.PI*per*u); };
  const ep=carte?+t[6]:10, rr=carte?+t[7]:6, esp=carte?+t[8]:18, mid=W/2, mode=t[3];
  const S=[];   /* {x, y, demi, quoi} en points de la page */
  const xs0=mode==='complet'?[0.12,0.3,0.5,0.7,0.88]:(mode==='points'?[]:[0.08,0.2,0.32,0.42]);
  xs0.forEach(f=>{ const x=f*W; S.push({x:r.left+x*k, y:r.top+y(x)*k, demi:ep/2*k, quoi:'tracé'}); });
  if(mode!=='complet'&&mode!=='duo'&&!cv.getAttribute('data-parts')){ const x0=(mode==='points')?W*0.11+esp*1.3:mid+esp; for(let x=x0, i=0; x<W-rr && i<6; x+=esp, i++) S.push({x:r.left+x*k, y:r.top+y(x)*k, demi:rr*k, quoi:'points'}); }
  /* le champ et le corps au même x, 6 pt au-delà du bord du trait — et dans la boîte du canevas */
  out.push({nat:nat(cv), col:t[2], mode:mode, carte:carte, k:k, box:[r.left,r.top,r.width,r.height], S:vus(cv, S.map(s=>Object.assign(s,{h:s.y-(s.demi+6*k), b:s.y+(s.demi+6*k)})), false)}); });
  /* le bandeau du Fil : l'onde est VERTICALE — le champ à gauche, le corps à droite */
  document.querySelectorAll(sel.replace(/canvas\[data-trait\]/g,'canvas[data-trait-v]')).forEach(cv=>{ const t=(cv.getAttribute('data-trait-v')||'').split(','); if(t.length<9) return;
    const r=cv.getBoundingClientRect(); if(r.width<20||r.height<20||r.bottom<0||r.top>innerHeight) return;
    const bx=+t[0], mont=+t[1], a=+t[2], H=+t[3], W=+t[8], k=r.width/W, ep=+t[6], rr=+t[7], mode=t[5];
    const x=yy=>{ const u=Math.max(0,Math.min(1,yy/H)); return bx-mont*u-a*Math.sin(2*Math.PI*u); };
    const S=[]; [0.12,0.25,0.38].forEach(f=>{ const yy=f*H; S.push({x:r.left+x(yy)*k, y:r.top+yy*k, demi:ep/2*k, quoi:'tracé'}); });
    if(mode!=='complet'&&mode!=='duo') for(let yy=77; yy<H; yy+=13) S.push({x:r.left+x(yy)*k, y:r.top+yy*k, demi:rr*k, quoi:'points'});
    out.push({nat:nat(cv), col:t[4], mode:mode, carte:true, vertical:true, k:k, box:[r.left,r.top,r.width,r.height], S:vus(cv, S.map(s=>Object.assign(s,{h:s.x-(s.demi+6*k), b:s.x+(s.demi+6*k)})), true)}); });
  return out.filter(o=>o.S.length); }"""
res = []; LIGNES = []
def juge(ou, img, dpr, g):
    """g : une géométrie déclarée → le rapport du trait au champ et au corps, lu sur l'image"""
    px = img.load(); W_, H_ = img.size
    def lit(x, y):
        X, Y = int(round(x * dpr)), int(round(y * dpr))
        if 0 <= X < W_ and 0 <= Y < H_: return px[X, Y][:3]
        return None
    T, C, B = {'tracé': [], 'points': []}, [], []
    for s in g['S']:
        if g.get('vertical'):
            t = [lit(s['x'] + d * s['demi'] * 0.5, s['y']) for d in (-1, -0.5, 0, 0.5, 1)]
            c = lit(s['h'], s['y']); b = lit(s['b'], s['y']); cin = s['h'] > g['box'][0]; bin_ = s['b'] < g['box'][0] + g['box'][2]
        else:
            t = [lit(s['x'], s['y'] + d * s['demi'] * 0.5) for d in (-1, -0.5, 0, 0.5, 1)]
            c = lit(s['x'], s['h']); b = lit(s['x'], s['b']); cin = s['h'] > g['box'][1]; bin_ = s['b'] < g['box'][1] + g['box'][3]
        t = [c_ for c_ in t if c_]
        if t: T[s['quoi']].append(med(t))
        if c and cin: C.append(c)
        if b and bin_: B.append(b)
    champ, corps = med(C), med(B)
    for quoi in ('tracé', 'points'):
        tr = med(T[quoi])
        if not tr: continue
        rc = ratio(tr, champ) if champ else None; rb = ratio(tr, corps) if corps else None
        bon = (rc is not None and rc >= SEUIL) and (rb is not None and rb >= SEUIL)
        mx = atteignable(champ, corps) if (champ and corps) else None
        verdict = 'OK' if bon else ('IMPOSSIBLE' if (mx is not None and mx < SEUIL) else 'KO')
        LIGNES.append((ou, quoi, hexa(tr), hexa(champ), rc, hexa(corps), rb, bon, verdict, mx))
        res.append(bon)
        print('%-10s %-44s %-7s trait %s · champ %s %s · corps %s %s%s' % (verdict, ou, quoi, hexa(tr), hexa(champ), ('%.2f' % rc) if rc else '—', hexa(corps), ('%.2f' % rb) if rb else '—',
              (' · au mieux %.2f avec ces deux fonds' % mx) if verdict == 'IMPOSSIBLE' else ''), flush=True)
def image(pg):
    import tempfile, os
    f = tempfile.mktemp(suffix='.png'); pg.screenshot(path=f); im = Image.open(f).convert('RGB'); os.remove(f); return im
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('clair', 'sombre'):
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True, is_mobile=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_guide','1');localStorage.setItem('promi_rappel_n','9');localStorage.setItem('promi_theme','%s');}catch(e){}" % ('light' if th == 'clair' else 'dark'))
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + PAGE); pg.wait_for_timeout(7000)
        dpr = 3
        def ferme():
            pg.evaluate("()=>{ try{ window._peaufSortie && window._peaufSortie(); closeAll(); }catch(e){} document.querySelectorAll('.screen.show').forEach(s=>s.classList.remove('show')); try{ setView('toile'); }catch(e){} }"); pg.wait_for_timeout(700)
        # ── la fiche : Promi (à tenir, en cours), Chiche, Cercle ; chaque pinceau
        cas = pg.evaluate("""()=>{ const P=promises.filter(p=>!p.draft&&p.status!=='tenu'); const pr=P.filter(p=>!p.chiche&&!p.nuee&&!p.from||p.from==='moi').filter(p=>!p.chiche);
          const ch=P.filter(p=>p.chiche); const n=Object.keys(NUE||{}); return {promi:(pr[0]||{}).id, promi2:(pr.find(p=>p.status==='rate')||pr[1]||{}).id, chiche:(ch[0]||{}).id, cercle:n[0]}; }""")
        for nat in ('promi', 'promi2', 'chiche', 'cercle'):
            for pin in PINCEAUX:
                ferme()
                if nat == 'cercle':
                    pg.evaluate("([k,pin])=>{ try{ window._pinceauNueeEcrit&&window._pinceauNueeEcrit(k,pin); }catch(e){} openNueeDetail(k); }", [cas['cercle'], pin])
                else:
                    pg.evaluate("([id,pin])=>{ const p=promises.find(q=>q.id===id); if(p) p.trait=pin; openDetail(id); }", [cas[nat], pin])
                pg.wait_for_timeout(1500)
                G = pg.evaluate(GEO, '#dpTrameCv')
                if not G: res.append(False); print('KO  fiche %s %s : aucun trait déclaré' % (nat, pin)); continue
                juge('%s · fiche %s · %s' % (th, {'promi': 'Promi', 'promi2': 'Promi (2)', 'chiche': 'Chiche', 'cercle': 'Cercle'}[nat], pin), image(pg), dpr, G[0])
        ferme()
        # ── les cartes de l'Index et du Fil
        for ou, js in (('Index', "()=>{ ouvrirIndex(); }"), ('Fil', "()=>{ document.getElementById('filBtn').click(); }")):
            ferme(); pg.evaluate(js); pg.wait_for_timeout(2600)
            for dy in (0, 600, 1200):
                if dy: pg.evaluate("(dy)=>{ const L=[document.getElementById('indexList'), document.getElementById('feedView')].filter(e=>e&&e.offsetParent); L.forEach(e=>e.scrollTop=dy); }", dy); pg.wait_for_timeout(1200)
                G = pg.evaluate(GEO, '#indexList canvas[data-trait], #feedView canvas[data-trait]')
                im = image(pg)
                for g_ in G:
                    juge('%s · carte %s · %s' % (th, ou, g_['nat']), im, dpr, g_)
        # ── la page + à la création : trois natures
        for nat in ('promi', 'chiche', 'nuee'):
            ferme()
            pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(900)
            pg.evaluate("(k)=>{ const b=document.querySelector('.acc-pil[data-k='+k+']'); if(b) b.click(); }", nat)
            for _ in range(40):
                pg.wait_for_timeout(150)
                if pg.evaluate("k=>{ const s=document.getElementById('createSheet'); return !!(s && s.classList.contains('show') && s.classList.contains('pp-'+k) && !s.classList.contains('pp-choix')); }", nat): break
            pg.wait_for_timeout(1600)
            G = pg.evaluate("""()=>{ const cv=document.getElementById('csTrameCv'); if(!cv||!window._ppEcran) return []; const e=window._ppEcran(); if(!e) return []; cv.setAttribute('data-trait-j', '1');
                const r=cv.getBoundingClientRect(), k=r.width/390, y=x=>{ const u=Math.max(0,Math.min(1,x/390)); return e.base-e.amp*0.34*u-e.amp*0.62*Math.sin(2*Math.PI*1.5*u); };
                const S=[]; for(let x=390*0.11+18*1.3, i=0; x<390-4.5 && i<6; x+=18, i++) S.push({x:r.left+x*k, y:r.top+y(x)*k, demi:6*k, quoi:'points'});
                [0.04].forEach(f=>{ const x=f*390; S.push({x:r.left+x*k, y:r.top+y(x)*k, demi:5*k, quoi:'tracé'}); });
                return [{col:'', mode:'points', carte:false, k:k, box:[r.left,r.top,r.width,r.height], S:S.map(s=>Object.assign(s,{h:s.y-(s.demi+6*k), b:s.y+(s.demi+6*k)}))}]; }""")
            if G: juge('%s · page + %s' % (th, {'promi': 'Promi', 'chiche': 'Chiche', 'nuee': 'Cercle'}[nat]), image(pg), dpr, G[0])
            else: res.append(False); print('KO  page + %s : pas de trait' % nat)
        ctx.close()
    b.close()
io.open('scratchpad/v147/contraste-trait.json', 'w', encoding='utf-8').write(json.dumps(LIGNES, ensure_ascii=False, indent=0))
n = sum(res); print('\n%d / %d' % (n, len(res))); sys.exit(0 if n == len(res) and res else 1)
