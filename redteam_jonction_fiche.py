# -*- coding: utf-8 -*-
"""⚑ v191 (Tom, C-259 suite) — PROMI ET CHICHE : LE TRAIT DU GESTE S'ACCROCHE À LA JONCTION ET S'APLATIT, COMME LA VAGUE DU CERCLE (C-247), PAR LE MÊME CODE.
Banc WebKit (banc_tom), horloge et hasard figés (banc_jonction.AMORCE) ; échelles 1, 0,79 (PYTHONPATH=scratchpad/v186/echelle079 PROMI_ECHELLE=0,79) et la fenêtre
de Tom (PYTHONPATH=scratchpad/v190/fenetretom PROMI_ECHELLE=tom). Promi et Chiche × quatre états : planté, à moitié tracé (à plusieurs, une part tracée), tenu,
date passée. La forme de la vraie ligne est lue sur ce que peint le peintre de la fiche (`#dpTrameCv.__ligne`, son empreinte), jamais sur la couche jugée.
  A · l'amplitude (1 − (s − s0)/40, bornée) en fonction du défilement, de 2 en 2 pt jusqu'à s0 + 60 : continue et monotone, aller et retour ; rien avant s0 ;
  B · accrochée, à chaque image (de s0 − 4 à s0 + 48, 2 en 2 pt, aller et retour) : le haut du trait, lu sur L'ÉCRAN autour du sommet de l'onde, à 0,5 pt près du haut de la
      ligne aplatie que trace le peintre de la fiche (`__ligne` sur l'onde (base', k·amp), coupée à 112) — à 112 pour un trait plein ;
  C · aucun pixel parasite dans la zone de la jonction, aux mêmes images : du bas de l'en-tête (104) jusqu'au haut de cette ligne aplatie (− 1,2 pt) ou de son axe (− 1 pt : entre deux points, le corps commence à l'axe), sous la matière du champ
      (l'empreinte de la vraie ligne) : rien que le champ (± 8) ;
  (⚑ v192 : la couche est là au repos — la boîte collante —, sans rien déclarer : « pas accrochée » = pas de `data-jonction` ; original : sauvegardes/redteam_jonction_fiche-avant-v192.py)
  D · au repos (défilement 0) : la fiche identique à v190 au pixel (zz-v190.html servie à côté, matière exceptée) ;
  E · le geste (planté, horloge réelle) : accroché, la zone du geste ne prend plus le doigt et un trait tracé sur la ligne accrochée ne tient rien ; après dix
      allers-retours de défilement, revenu en haut, tenir au doigt tient la parole. Aucune erreur de page."""
import sys, io, os, json, re; sys.path.insert(0, '.')
import banc_tom as B, banc_jonction as BJ
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
F = next((a for a in sys.argv[1:] if a.endswith('.html')), 'app.html')
REF = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--ref=')), 'zz-v190.html')
NATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--natures=')), ['promi', 'chiche'])
ETATS = next((a.split('=', 1)[1].split(',') for a in sys.argv[1:] if a.startswith('--etats=')), ['plante', 'moitie', 'tenu', 'passee'])
SANS_E = '--sans-geste' in sys.argv
ECH = os.environ.get('PROMI_ECHELLE', '1')
J = 112
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-112s %s' % ('✅' if ok else '❌', nom, str(d)[:240]), flush=True); return ok
TITRE = {'promi': 'faire les crêpes', 'chiche': 'réparer le vélo'}
ETAT = """a=>{ const [t, nat, etat, mots]=a; const p=promises.find(x=>x.title===t); if(!p) return null;
  if(nat==='chiche'){ p.chiche=true; p.chicheEtat='lance'; p.phraseSens='chiche'; }
  p.comments=mots.map((x,i)=>({t:x[1], by:x[0], d:'2026-11-0'+(i+1)+'T09:00:00Z', vu:true})); p.status='encours'; delete p.parts; delete p.req; if(nat==='chiche') p.who='Adrien';
  if(etat==='moitie'){ p.who='Rachel, Marion'; if(nat==='promi') p.req=true; p.parts={'Rachel':'2026-11-05T09:00:00Z'}; }
  if(etat==='tenu'){ p.status='tenu'; }
  if(etat==='passee'){ p.ech={iso:'2026-10-12', due:-28}; p.due=-28; }
  try{ saveState(true); }catch(e){}
  return p.id; }"""
def ouvre(b, f, nat, etat, fige=True):
    ctx = B.contexte(b); B.toile_pleine(ctx, 'cercle')
    if fige: ctx.add_init_script(BJ.AMORCE)
    pg = B.ouvre(ctx, f, 6000)
    pid = pg.evaluate(ETAT, [TITRE[nat], nat, etat, BJ.MOTS]); pg.evaluate("id=>{ try{ closeAll() }catch(e){} openDetail(id); }", pid)
    if fige:
        for _ in range(40): pg.evaluate("()=>{ window.__horloge(100); }"); pg.wait_for_timeout(60)
    else: pg.wait_for_timeout(3500)
    pg.wait_for_timeout(500); return ctx, pg, pid
def pas(pg, s):
    pg.evaluate("s=>{ document.getElementById('detailPoster').scrollTop=s; }", s)
    pg.evaluate("()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>requestAnimationFrame(r))))")
    return pg.evaluate("()=>{ const c=document.getElementById('v189Jonction'), d=document.getElementById('detailPoster'); if(!c || getComputedStyle(c).display==='none') return {s:d.scrollTop, t:null};"
                       " if(!c.hasAttribute('data-jonction')) return {s:d.scrollTop, t:null};"
                       " const a=c.getAttribute('data-jonction').split(','); return {s:d.scrollTop, t:+a[1], kind:a[0]}; }")
# la vraie ligne, lue sur ce que peint le peintre de la fiche (son empreinte : le haut de ce qu'il peint, colonne par colonne)
FORME = """()=>{ const c=document.getElementById('dpTrameCv'), t=(c.getAttribute('data-trait')||'').split(','), base=+t[0], amp=+t[1], y=_onde.onde(base, amp), P=[];
  for(let x=0;x<=390;x+=2) P.push(y(x)); const mn=Math.min(...P), lw=10*(window._TRAIT_K||1.3);
  const E=2, o=document.createElement('canvas'); o.width=390*E; o.height=Math.ceil(Math.max(...P)+60)*E; const g=o.getContext('2d'); g.setTransform(E,0,0,E,0,0); if(c.__ligne) c.__ligne(g, base, amp);
  const D=g.getImageData(0,0,o.width,o.height).data, EN=[];
  for(let i=0;i<P.length;i++){ let top=null; const xa=Math.max(0,(i*2-1)*E), xb=Math.min(o.width-1,(i*2+1)*E);
    for(let xx=xa;xx<=xb;xx++) for(let yy=0;yy<o.height;yy++){ if(D[(yy*o.width+xx)*4+3]>8){ if(top===null||yy<top) top=yy; break; } }
    EN.push(top===null?P[i]-lw/2:top/E); }
  const s0=mn-lw/2-112; return {P, EN, mn, lw, s0, base, amp, champ:c.getAttribute('data-champ'), smax:(()=>{ const d=document.getElementById('detailPoster'); return d.scrollHeight-d.clientHeight; })()}; }"""
# le haut EXACT de la ligne aplatie (le même peintre, sur l'onde (base', k·amp)), colonne par colonne, coupé à la jonction — calculé ici, hors de la couche jugée
HAUT = """a=>{ const [b2, a2]=a, c=document.getElementById('dpTrameCv'), E=3, o=document.createElement('canvas'); o.width=390*E; o.height=300*E; const g=o.getContext('2d'); g.setTransform(E,0,0,E,0,0);
  if(c.__ligne) c.__ligne(g, b2, a2); const D=g.getImageData(0,0,o.width,o.height).data, T=[];
  for(let i=0;i<=195;i++){ const x=Math.min(o.width-1, Math.round(i*2*E)); let t=null; for(let y=0;y<o.height;y++){ if(D[(y*o.width+x)*4+3]>8){ t=y/E; break; } } T.push(t===null?null:Math.max(112, t)); } return T; }"""
def hexrgb(h):
    h = (h or '').strip()
    if h.startswith('#'): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    m = re.findall(r'\d+', h); return tuple(int(x) for x in m[:3]) if len(m) >= 3 else None
with sync_playwright() as p:
    b = p.webkit.launch()
    for nat in NATS:
        for etat in ETATS:
            T = '[%s · %s · %s]' % (ECH, nat, etat)
            ctx, pg, pid = ouvre(b, F, nat, etat)
            pas(pg, 1); G = pg.evaluate(FORME); P, EN, mn, lw, s0 = G['P'], G['EN'], G['mn'], G['lw'], G['s0']
            champ = hexrgb(G['champ']); n = len(P)
            top = min(int(s0 + 60), int(G['smax']))
            if top < s0 + 41: juge(T + ' la fiche défile assez pour aplatir le trait (s0 + 40 = %.0f, défilement possible %.0f)' % (s0 + 40, G['smax']), False); ctx.close(); continue
            # A
            aller = [pas(pg, s) for s in range(0, top + 1, 2)]; retour = [pas(pg, s) for s in range(top, -1, -2)]
            def att(s): return None if s < s0 else min(1.0, (s - s0) / 40)
            ec = [(r['s'], r['t'], att(r['s'])) for r in aller + retour if (r['t'] is None) != (att(r['s']) is None) or (r['t'] is not None and abs(r['t'] - att(r['s'])) > 0.012)]
            seq = [r['t'] for r in aller if r['t'] is not None]; mono = all(seq[i + 1] >= seq[i] - 1e-6 for i in range(len(seq) - 1))
            kinds = set(r.get('kind') for r in aller + retour if r['t'] is not None)
            juge(T + ' A · l\'amplitude suit le défilement (s0 = %.1f), continue et monotone, aller et retour (%d pas)' % (s0, len(aller) + len(retour)), not ec and mono and len(seq) > 10 and kinds == {'fiche'}, (ec[:3], kinds))
            # B, C — sur l'écran
            d = B.dev(pg); k = d[4]; DPR = pg.evaluate("()=>devicePixelRatio"); seqB = [s0 - 4 + i for i in range(0, 53, 2)]; seqB = seqB + seqB[::-1]
            ic = min(range(n), key=lambda i: P[i]); cols = [i for i in range(max(0, ic - 5), min(n, ic + 6))]
            hauts = []; mauvais = []
            for s in seqB:
                # l'écran ENTIER (une capture rognée à une cote fractionnaire est rééchantillonnée : CLAUDE.md §8), relu en pt de l'appareil
                r = pas(pg, s); im = Image.open(io.BytesIO(pg.screenshot())).convert('RGB'); px = im.load(); dpr = DPR; q = k * dpr
                Y = lambda yy: int(round((d[1] + yy * k) * dpr)); XX = lambda xx: int(round((d[0] + xx * k) * dpr)); PT = lambda Yp: (Yp / dpr - d[1]) / k
                if champ is None: champ = px[XX(4), Y(106)]
                if r['t'] is None: continue
                kk = 1 - r['t']; y0 = J + lw / 2; HT = pg.evaluate(HAUT, [y0 + kk * (G['base'] - mn), kk * G['amp']])
                h = None; hx = min([HT[i] for i in cols if HT[i] is not None] or [None])
                for i in cols:
                    X = XX(i * 2)
                    for yy in range(Y(104), Y(160)):
                        c = px[X, yy]
                        if sum(abs(c[j] - champ[j]) for j in range(3)) > 60:
                            v = PT(yy); h = v if h is None or v < h else h; break
                hauts.append((round(s, 1), h and round(h, 2), hx and round(hx, 2)))
                for i in range(2, n - 2, 2):
                    hs = [HT[j] for j in range(max(0, i - 1), min(n, i + 2)) if HT[j] is not None]
                    if not hs: continue
                    X = XX(i * 2); m = min(min(hs) - 1.2, y0 + (P[i] - mn) * kk - 1.0)   # entre deux points, le champ finit à l'axe de la vague accrochée (le corps dessous)
                    for yy in range(Y(max(104, EN[i] - s - 2.5)), Y(m)):
                        c = px[X, yy]
                        if sum(abs(c[j] - champ[j]) for j in range(3)) > 8: mauvais.append((round(s, 1), i * 2, round(PT(yy), 1), c)); break
            hors = [x for x in hauts if x[1] is None or x[2] is None or abs(x[1] - x[2]) > 0.5]
            juge(T + ' B · accroché : la place du trait à la jonction à 0,5 pt près à chaque image (le haut lu sur l\'écran contre la ligne aplatie de son peintre ; %d images)' % len(hauts), hauts and not hors, (hors[:4], hauts[:2]))
            juge(T + ' C · aucun pixel parasite au-dessus du trait accroché (rien que le champ, %d images)' % len(hauts), not mauvais, (len(mauvais), mauvais[:3]))
            # D — au repos, contre v190
            pas(pg, 0); dd = B.dev(pg)
            def fiche(pp):
                im = Image.open(io.BytesIO(pp.screenshot(clip={'x': dd[0], 'y': dd[1], 'width': 390 * dd[4], 'height': 844 * dd[4]}))).convert('RGB')
                z = pp.evaluate("()=>window._zonesMatiere ? _zonesMatiere().zones : []"); q = im.size[0] / 390.0
                m = Image.new('L', im.size, 0); from PIL import ImageDraw; dr = ImageDraw.Draw(m)
                for x, y, w, h in z: dr.rectangle([int(x * q) - 1, int(y * q) - 1, int((x + w) * q) + 1, int((y + h) * q) + 1], fill=255)
                return im, m
            A1 = fiche(pg); er = pg.erreurs[:]; ctx.close()
            c2, p2, _ = ouvre(b, REF, nat, etat); p2.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); p2.wait_for_timeout(300); A2 = fiche(p2); c2.close()
            dif = ImageChops.difference(A1[0], A2[0]).convert('L').point(lambda v: 255 if v > 24 else 0); dif = ImageChops.subtract(dif, ImageChops.lighter(A1[1], A2[1])); nd = sum(dif.histogram()[1:])
            if nd: dif.save('scratchpad/v191/D-%s-%s-%s.png' % (ECH.replace(',', ''), nat, etat))
            juge(T + ' D · au repos : la fiche identique à %s au pixel (matière exceptée)' % REF, nd == 0, nd)
            juge(T + ' aucune erreur de page', not er, er[:2])
        # E — le geste, horloge réelle (planté)
        if SANS_E: continue
        T = '[%s · %s · geste]' % (ECH, nat)
        ctx, pg, pid = ouvre(b, F, nat, 'plante', fige=False)
        pas(pg, 1); G = pg.evaluate(FORME); s0 = G['s0']
        pas(pg, s0 + 44); pg.wait_for_timeout(300)
        pe = pg.evaluate("()=>{ const z=document.getElementById('tenirZone'); return [getComputedStyle(z).pointerEvents, (window._v189Jonction()||{}).coupe]; }")
        y = 112 + G['lw'] / 2
        dessous = pg.evaluate("a=>{ const r=document.getElementById('device').getBoundingClientRect(), k=r.width/390; const e=document.elementFromPoint(r.left+a[0]*k, r.top+a[1]*k); return e ? (e.id||e.className||e.tagName)+'' : null; }", [200, y + 2])
        B.glisse(pg, [[30 + 33 * i, y] for i in range(11)], pas=60, tenue=380); pg.wait_for_timeout(2500)
        st = pg.evaluate("id=>{ const p=promises.find(x=>x.id===id); return [p.status, JSON.stringify(p.parts||null)]; }", pid)
        juge(T + ' E · accroché : la zone du geste ne prend pas le doigt ; un trait tracé sur la ligne accrochée ne tient rien', pe[0] == 'none' and pe[1] is True and dessous not in ('tenirZone', 'tenirCv') and st[0] != 'tenu', (pe, dessous, st))
        for _ in range(10): pas(pg, s0 + 60); pas(pg, 0)
        pg.wait_for_timeout(800)
        z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'), r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.left-d.left)/k,(r.top-d.top)/k,r.width/k,r.height/k, getComputedStyle(c).pointerEvents]; }")
        yy = z[1] + z[3] * 0.45; B.glisse(pg, [[30 + 33 * i, yy] for i in range(11)], pas=60, tenue=380); pg.wait_for_timeout(3500)
        st = pg.evaluate("id=>promises.find(x=>x.id===id).status", pid)
        juge(T + ' E · après dix allers-retours, revenu en haut : tenir au doigt tient la parole', st == 'tenu' and z[4] != 'none', (st, z))
        juge(T + ' aucune erreur de page', not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
