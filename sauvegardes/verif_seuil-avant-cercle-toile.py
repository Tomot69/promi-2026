# LE LOT DU SEUIL — VÉRIFIÉ À L'ÉCRAN (11 sept. 2026), deux thèmes, AVANT les batteries. Chaque contrat nomme ce qu'il a trouvé.
#   A · le rayon de CHAQUE champ de Peaufiner = la règle de hauteur (h ÷ 2 jusqu'à 94,5, 30 au-delà) — fiche, page +, Nuée,
#       notes ouvertes à 4 et 5 rangées ; et l'app déclare 94,5.
#   B · l'air de l'ENCRE au contour ≥ C − 0,5 (C = 15,19, l'air le plus serré d'un champ ouvert au rayon 30) — mesuré sur la
#       capture de chaque champ entièrement visible (confirmé au doigt : cinq points intérieurs tombent sur lui).
#   C · chantier 68 : la note à 4 et 5 rangées — le texte ne touche ni le libellé ni la visibilité, le champ montre toutes
#       ses lignes ; et sur la page +, AUCUN instant où la zone rebâtie garde sa hauteur de repos (sonde d'observateur).
#   D · l'écran qui vend : prix et boutons lisibles (rapport ≥ 4,5), la forme du prix, la marge de 24.
#   E · les portes y mènent : l'encart du gardé de côté (par-dessus), l'encart des Réglages.
#   F · côte à côte : une pilule à une ligne, un champ ouvert à quatre rangées (captures, deux thèmes).
import io, json, os, sys
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
# ⚠ une passe sur une AUTRE version (preuve sur une version fautive) écrit ailleurs : lancée en même temps que la passe
#   finale, elle avait écrasé ses captures (vu le 11 sept. : les contours crème sur crème « de la version finale » étaient
#   ceux de la version fautive — le chiffre, lui, disait 215).
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, 'seuil' if len(sys.argv) <= 1 else 'seuil_preuve'); os.makedirs(OUT, exist_ok=True)
SEUIL, C = 94.5, 15.19
def regle(h): return h / 2.0 if h <= SEUIL else 30.0
L2 = "prévenir Rachel la veille, apporter le gâteau et les bougies"
L3 = "prévenir Rachel la veille, apporter le gâteau et les bougies, et passer chercher Maman à la gare"
BASE = "()=>{ try{closeAll();}catch(e){} document.querySelectorAll('.screen.show,.poster.show').forEach(s=>s.classList.remove('show')); }"
OUTILS = open(os.path.join(D, 'verif_integration.py'), encoding='utf-8').read().split('OUTILS = r"""')[1].split('"""')[0]
CHAMPS = r"""(hote)=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, H=document.querySelector(hote); const out=[];
  H.querySelectorAll('*').forEach(c=>{ if(!c.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) return; const cs=getComputedStyle(c), r=c.getBoundingClientRect();
    const bw=parseFloat(cs.borderTopWidth), R=Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2);
    if(bw<=0 || r.height<40*s || R<20*s || r.width<300*s) return;
    if(!(c.matches('.s2-reg, .np-carte'))) return;
    const lab=(c.querySelector('.s2-lab,.np-lab')||c).textContent.replace(/\s+/g,' ').trim().slice(0,22);
    out.push({cle: lab+'|'+(c.id||String(c.className).split(' ').slice(0,3).join('.')), h:+(r.height/s).toFixed(2), R:+(R/s).toFixed(2)}); }); return out; }"""
TROUVE = r"""const trouve=(hote,cle)=>{ const H=document.querySelector(hote); return [...H.querySelectorAll('.s2-reg, .np-carte')].find(c=>{ const lab=(c.querySelector('.s2-lab,.np-lab')||c).textContent.replace(/\s+/g,' ').trim().slice(0,22); return lab+'|'+(c.id||String(c.className).split(' ').slice(0,3).join('.'))===cle; }); };"""
VISE = "([hote,cle])=>{ " + TROUVE + r""" const c=trouve(hote,cle); if(!c) return null; c.scrollIntoView({block:'center'}); return true; }"""
RECT = "([hote,cle])=>{ " + TROUVE + r""" const c=trouve(hote,cle); if(!c) return null; const r=c.getBoundingClientRect(), cs=getComputedStyle(c), dv=document.getElementById('device').getBoundingClientRect();
  const rate=[]; const pts=[[.5,.5],[.04,.12],[.96,.12],[.04,.88],[.96,.88]].map(([a,b])=>{ const h=document.elementFromPoint(r.left+r.width*a, r.top+r.height*b); const bon=!!(h && (h===c || c.contains(h) || h.contains(c)));   /* un ANCÊTRE sous le doigt : rien n'est posé par-dessus */ if(!bon) rate.push(h ? (h.id||String(h.className).split(' ')[0]||h.tagName) : 'rien'); return bon; });
  /* le rond photo de la page + (chantier 64) ne prend pas le doigt : elementFromPoint ne le voit pas — on le cherche par sa BOÎTE */
  const ov=[...document.querySelectorAll('.ph-photo-btn')].filter(o=>o.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})).map(o=>{ const q=o.getBoundingClientRect(); return {x:q.left-r.left, y:q.top-r.top, w:q.width, h:q.height}; })
    .filter(q=>q.x<r.width && q.x+q.w>0 && q.y<r.height && q.y+q.h>0);
  return {x:r.left, y:r.top, w:r.width, h:r.height, bw:parseFloat(cs.borderTopWidth), R:Math.min(parseFloat(cs.borderTopLeftRadius)||0, r.height/2), dedans: r.top>=dv.top && r.bottom<=dv.bottom, doigt:pts.every(Boolean), rate, ov}; }"""

VEND = r"""()=>{ const lum=(c)=>{ const m=c.match(/[\d.]+/g).map(Number); const f=v=>{v/=255; return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);}; return .2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]); };
  const L=(c)=>{ const m=c.match(/[\d.]+/g).map(Number); return .2126*m[0]+.7152*m[1]+.0722*m[2]; };
  const fond=(e)=>{ let x=e; while(x){ const b=getComputedStyle(x).backgroundColor; const a=(b.match(/[\d.]+/g)||[]).map(Number); if(a.length>=3 && (a.length<4 || a[3]>0.5)) return b; x=x.parentElement; } return 'rgb(255,255,255)'; };
  const rap=(e)=>{ const k=getComputedStyle(e); const c=k.webkitTextFillColor||k.color; const L1=lum(c), L2=lum(fond(e)); return {t:e.textContent.trim().slice(0,34), r:+((Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05)).toFixed(2), fill_egal:c===k.color, op:+k.opacity}; };
  const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390, ps=document.getElementById('plusScreen');
  /* ⚠ sur une version FAUTIVE (l'ancien écran) il n'y a ni cadre ni « 29 € » : le juge le DIT, il ne plante pas */
  if(!document.querySelector('#plusScreen #plCadre .plv-prix')) return {absent:true, dalles:window._vendDalles||null, textes:ps?ps.innerText.slice(0,160):null};
  const R=(e)=>{ const r=e.getBoundingClientRect(); return [+((r.left-dv.left)/s).toFixed(1), +((r.top-dv.top)/s).toFixed(1), +(r.width/s).toFixed(1), +(r.height/s).toFixed(1)]; };
  const Q=(q)=>document.querySelector('#plusScreen '+q);
  const px=(c)=>{ const W=c.width, d=c.getContext('2d').getImageData(0,0,W,c.height).data; let n=0,h=0,x0=W,y0=c.height,x1=-1,y1=-1; for(let i=3;i<d.length;i+=4){ if(d[i]>10){ n++; const p=(i-3)/4, x=p%W, y=(p/W)|0; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } h=(h*31+d[i-3]+d[i-2]*7+d[i-1]*13)>>>0; } return {peint:+(100*n/(d.length/4)).toFixed(1), h, bb: n ? [x1-x0+1, y1-y0+1] : null}; };
  const doigt=(e)=>{ const r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!(h&&(h===e||e.contains(h))); };
  const bbAlpha=(c)=>{ const W=c.width, d=c.getContext('2d').getImageData(0,0,W,c.height).data; let x0=W,y0=c.height,x1=-1,y1=-1;
    for(let i=3;i<d.length;i+=4){ if(d[i]>10){ const p=(i-3)/4, x=p%W, y=(p/W)|0; if(x<x0)x0=x; if(x>x1)x1=x; if(y<y0)y0=y; if(y>y1)y1=y; } }
    return x1<0?null:[x1-x0+1, y1-y0+1]; };
  /* la SOURCE, mesurée par le juge lui-même : il redemande la dalle au moteur, dans le même monde, et regarde son encre */
  const source=(d)=>{ try{ const t=document.createElement('canvas'); const mo=Object.assign({}, window.Toile.mondeCourant(), {m:d.monde});
      if(!window.Toile.dalleTrame(t, d.id, 1, mo) || !t.width) return null; return bbAlpha(t); }catch(e){ return null; } };
  const refs=(window._vendDalles||[]).map(d=>source(d));
  const y=Q('#buyYear'), m=Q('#buyMonth'), sb=fond(ps), kP=getComputedStyle(Q('.plv-prix'));
  const textes=[Q('.plv-prix'), Q('.plv-sous'), ...ps.querySelectorAll('#plCadre .plv-nom'), y, m, ...ps.querySelectorAll('#plCadre .pl-note')];
  return {dalles: window._vendDalles||null, canevas:[...ps.querySelectorAll('#plCadre .plv-dal')].map(c=>Object.assign({monde:c.dataset.monde, r:R(c)}, px(c))),
    prix:{t:Q('.plv-prix').textContent.replace(/\u00a0/g,' '), r:R(Q('.plv-prix')), ff:kP.fontFamily.split(',')[0].replace(/["']/g,''), fw:kP.fontWeight, fs:parseFloat(kP.fontSize)},
    sous:{t:Q('.plv-sous').textContent.replace(/\u00a0/g,' '), r:R(Q('.plv-sous'))}, noms:[...ps.querySelectorAll('#plCadre .plv-nom')].map(e=>[e.textContent, R(e)]),
    annee:{t:y.textContent.trim(), r:R(y), doigt:doigt(y)}, essai:{t:m.textContent.trim().replace(/\u00a0/g,' '), r:R(m), doigt:doigt(m)},
    notes:[...ps.querySelectorAll('#plCadre .pl-note')].map(e=>R(e)[1]), rapports:textes.map(rap),
    bord_essai:+Math.abs(L(getComputedStyle(m).borderTopColor)-L(sb)).toFixed(1), fond_annee:+Math.abs(L(getComputedStyle(y).backgroundColor)-L(sb)).toFixed(1),
    refs,     anciens:['#plHeroCv','.pl-h','.pl-sub','.pl-feat'].filter(q=>[...ps.querySelectorAll(q)].some(e=>e.checkVisibility())),
    ombre:getComputedStyle(ps,'::before').display, offert:/offert/i.test(ps.innerText), defile:ps.scrollHeight-ps.clientHeight}; }"""

def contrats_vend(v):
    """Les contrats de l'écran qui vend (Q205) — rendus comme (nom, tenu, détail). Les cotes de la planche sont EN DUR."""
    L = []; d = v['dalles'] or []; cv = v['canevas']
    L.append(('écran qui vend · trois VRAIES dalles du moteur, Sillons · Gravure · Terrazzo, dans cet ordre',
              len(d) == 3 and [x['monde'] for x in d] == ['sillons', 'gravure', 'terrazzo'] and all(x['ok'] and x['id'] is not None for x in d), d))
    XS = (24, 146, 268)
    cot = len(cv) == 3 and all(abs(c['r'][0] - XS[k]) <= 1 and abs(c['r'][1] - 132) <= 1 and abs(c['r'][2] - 98) <= 1 and abs(c['r'][3] - 98) <= 1 for k, c in enumerate(cv))
    # « jamais étirée » : la boîte PEINTE dans le canevas (mesurée par le juge, sur l'alpha) garde le rapport de la source que le
    # moteur a rendue — la déclaration de l'app ne suffit pas (CLAUDE §7 : un juge qui lit la valeur qu'il vérifie ne vérifie rien)
    # ⚑ DEUX ENCRES, MESURÉES PAR LE JUGE (§7) : celle peinte à l'écran, et celle d'un rendu FRAIS qu'il redemande au moteur.
    #    Première écriture : il comparait l'encre peinte à la TAILLE DU CANEVAS source déclarée — or une dalle peut laisser une
    #    marge transparente (Sillons : rapport canevas 1,247, encre peinte 1,315 → faux rouge du 12 sept.). Tolérance 6 % : la
    #    matière respire d'un rendu à l'autre (CLAUDE §7).
    etire = []
    refs = v.get('refs') or []
    for k, c in enumerate(cv):
        ref = refs[k] if k < len(refs) else None
        if not ref or not c.get('bb'): etire.append((c['monde'], 'rien de peint' if not c.get('bb') else 'le moteur ne rend pas cette dalle')); continue
        rs, rb = ref[0] / ref[1], c['bb'][0] / c['bb'][1]
        if abs(rb - rs) > 0.06 * rs: etire.append((c['monde'], 'encre du moteur %.3f, encre peinte %.3f' % (rs, rb)))
    L.append(('écran qui vend · chaque dalle peinte (≥ 5 % de pixels), à sa cote (24 | 146 | 268, 132, 98 × 98), jamais étirée, les trois différentes',
              cot and all(c['peint'] >= 5 for c in cv) and not etire and len(set(c['h'] for c in cv)) == 3,
              ([(c['monde'], c['r'], c['peint'], c.get('bb')) for c in cv], 'étirées', etire)))
    P_ = v['prix']
    L.append(('écran qui vend · « 29 € » en grand (Bricolage 700 / 56, à 24 / 276, 342 × 56)',
              P_['t'] == '29 €' and P_['ff'] == 'Bricolage' and P_['fw'] == '700' and abs(P_['fs'] - 56) < .6 and all(abs(a - b) <= 1 for a, b in zip(P_['r'], (24, 276, 342, 56))), P_))
    A_, E_ = v['annee'], v['essai']
    L.append(('écran qui vend · « Prendre l’année » en premier (386), l’essai de 14 jours VISIBLE dessous (464), sans défiler, au doigt',
              A_['t'] == "Prendre l'année" and E_['t'] == 'Essayer 14 jours, puis 3,99 €/mois' and abs(A_['r'][1] - 386) <= 1 and abs(E_['r'][1] - 464) <= 1
              and E_['r'][1] >= A_['r'][1] + A_['r'][3] and E_['r'][1] + E_['r'][3] <= 844 and A_['doigt'] and E_['doigt'] and v['defile'] <= 0, (A_, E_, 'défile', v['defile'])))
    faibles = [r for r in v['rapports'] if r['r'] < 4.5 or not r['fill_egal'] or r['op'] < .72]
    L.append(('écran qui vend · chaque texte se lit (rapport ≥ 4,5, remplissage = couleur, opacité ≥ 72 %)', not faibles, faibles or 'min %.2f' % min(r['r'] for r in v['rapports'])))
    L.append(('écran qui vend · les deux boutons se voient (fond de l’année, contour de l’essai : écart de luminosité ≥ 42)',
              v['fond_annee'] >= 42 and v['bord_essai'] >= 42, (v['fond_annee'], v['bord_essai'])))
    L.append(('écran qui vend · plus de visuel ni d’explication : visuel, titre, phrase, cinq lignes, ombre de dalle du fond',
              not v['anciens'] and v['ombre'] == 'none', (v['anciens'], v['ombre'])))
    L.append(('écran qui vend · les cotes de la planche (noms 238, sous-prix 342, notes 548 / 574) et la forme du prix, jamais « offert »',
              all(abs(n[1][1] - 238) <= 1 for n in v['noms']) and [n[0] for n in v['noms']] == ['Sillons', 'Gravure', 'Terrazzo'] and abs(v['sous']['r'][1] - 342) <= 1
              and [round(x) for x in v['notes']] == [548, 574] and v['sous']['t'] == 'soit 2,42 €/mois · −39 %' and not v['offert'], (v['noms'], v['sous'], v['notes'], v['offert'])))
    return L

VIDE = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), s=dv.width/390; const c=document.getElementById('plCadre');
  const y=(q)=>{ const e=document.querySelector('#plusScreen '+q); return e&&e.checkVisibility()? +((e.getBoundingClientRect().top-dv.top)/s).toFixed(1) : null; };
  const doigt=(q)=>{ const e=document.querySelector('#plusScreen '+q); if(!e) return false; const r=e.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return !!(h&&(h===e||e.contains(h))); };
  return {n:(typeof promises!=='undefined'?promises.length:null), sans:c?c.classList.contains('plv-sans'):null, declare:window._vendSans===true,
    dalles:[...document.querySelectorAll('#plCadre .plv-dal')].map(e=>e.checkVisibility()), noms:[...document.querySelectorAll('#plCadre .plv-nom')].map(e=>e.checkVisibility()),
    prix:y('.plv-prix'), sous:y('.plv-sous'), annee:y('#buyYear'), essai:y('#buyMonth'), essai_doigt:doigt('#buyMonth'), annee_doigt:doigt('#buyYear'),
    notes:[...document.querySelectorAll('#plCadre .pl-note')].map(e=>+((e.getBoundingClientRect().top-dv.top)/s).toFixed(1))}; }"""

def contrats_vide(v):
    """L'écran qui vend SANS aucun Promi (Tom, 11 sept., nuit) — la rangée cachée, le prix remonté de 144, l'essai visible."""
    pres = lambda a, b: a is not None and abs(a - b) <= 1
    return [
      ('écran qui vend SANS Promi · la rangée se cache (dalles et noms), l’app le déclare',
       v['n'] == 0 and v['sans'] and v['declare'] and v['dalles'] and not any(v['dalles']) and not any(v['noms']), v),
      ('écran qui vend SANS Promi · le prix remonte à 132, « Prendre l’année » 242, l’essai VISIBLE dessous à 320, notes 404 / 430',
       pres(v['prix'], 132) and pres(v['sous'], 198) and pres(v['annee'], 242) and pres(v['essai'], 320) and v['essai_doigt'] and v['annee_doigt']
       and [round(x) for x in v['notes']] == [404, 430], v)]

def sdf(x, y, w, h, R, bw):
    R = min(R, h / 2.0, w / 2.0); ri = max(R - bw, 0.0); a, b = w / 2.0 - bw, h / 2.0 - bw
    dx = np.abs(x - w / 2.0) - (a - ri); dy = np.abs(y - h / 2.0) - (b - ri)
    return ri - np.hypot(np.maximum(dx, 0), np.maximum(dy, 0)) - np.minimum(np.maximum(dx, dy), 0)
def air_encre(png, m):
    im = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.int16); H, W = im.shape[:2]; k = m['w'] / W
    ys, xs = np.mgrid[0:H, 0:W]; x = (xs + .5) * k; y = (ys + .5) * k; g = sdf(x, y, m['w'], m['h'], m['R'], m['bw'])
    dedans = g > 1.5
    for q in m.get('ov') or []:                       # un recouvrement DÉCLARÉ (chantier 64) n'est pas l'encre du champ
        dedans &= ~((x > q['x'] - 2) & (x < q['x'] + q['w'] + 2) & (y > q['y'] - 2) & (y < q['y'] + q['h'] + 2))
    fond = np.median(im[dedans], axis=0); ink = dedans & (np.abs(im - fond).max(axis=2) > 48)
    return float(g[ink].min()) if ink.any() else None

R = {}; KO = []; CONNUS = []
def ok(nom, cond, detail):
    R.setdefault(TH, []).append((nom, bool(cond), detail)); print('   %s %s  %s' % ('✓' if cond else '✗', nom, detail))
    if not cond: KO.append('%s · %s · %s' % (TH, nom, detail))
if __name__ != '__main__': raise SystemExit  # importé par preuve_vend.py : on ne prend que VEND et contrats_vend
with sync_playwright() as p:
    br = p.chromium.launch()
    for TH in ('dark', 'light'):
        print('\n════ %s' % TH)
        ctx = br.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=2); pg = ctx.new_page()
        pg.goto(URL); pg.wait_for_timeout(6800)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)", TH); pg.evaluate("()=>setPremium(true)"); pg.wait_for_timeout(400); pg.evaluate(OUTILS)
        ok('l’app déclare la bascule 94,5', pg.evaluate("()=>window._seuilPilule") == SEUIL, pg.evaluate("()=>window._seuilPilule"))
        def fiche():
            pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && q.status==='encours' && q.who && !q.chiche && !q.nuee) || promises.find(q=>!q.draft && !q.nuee); openDetail(p.id); return p.id; }"); pg.wait_for_timeout(1400)
            pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700); return '#detailPoster'
        def pageplus():
            pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(600)
            pg.evaluate("()=>{var t=[...document.querySelectorAll('#createSheet .tile')][0]; var b=t&&t.querySelector('button,.tg,.hname'); if(b)b.click(); else if(t)t.click();}"); pg.wait_for_timeout(900)
            for essai in range(3):
                pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1800)
                try:
                    pg.wait_for_function("()=>!!document.querySelector('#createSheet.pp-peauf .s2-zone textarea')", timeout=4000); break
                except Exception:
                    print('   … la page + n’a pas ouvert son Peaufiner (essai %d)' % (essai + 1))
            return '#createSheet'
        def nuee():
            pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>openEssaim('potager')"); pg.wait_for_timeout(1500)
            pg.evaluate("()=>document.querySelector('#dpDetails .dpd-tog').click()"); pg.wait_for_timeout(1700); return '#detailPoster'
        def ecrit(hote, t):
            r = pg.evaluate("([h,t])=>{ const x=document.querySelector(h+' .s2-zone textarea'); if(!x) return false; x.value=t; x.dispatchEvent(new Event('input',{bubbles:true})); return true; }", [hote, t]); pg.wait_for_timeout(700)
            return r
        def vide():
            pg.evaluate("()=>{ document.querySelectorAll('#dNote, #createSheet .s2-zone textarea').forEach(x=>{ x.value=''; x.dispatchEvent(new Event('input',{bubbles:true})); }); }"); pg.wait_for_timeout(300)
        def capture(hote, cle):
            for essai in range(3):
                if not pg.evaluate(VISE, [hote, cle]): return None, None
                pg.wait_for_timeout(350); m = pg.evaluate(RECT, [hote, cle])
                if not m: return None, None
                png = pg.screenshot(clip={'x': m['x'], 'y': m['y'], 'width': m['w'], 'height': m['h']})
                m2 = pg.evaluate(RECT, [hote, cle])
                if m2 and abs(m2['h'] - m['h']) < .5 and abs(m2['y'] - m['y']) < .5: return m, png
            return m, None
        # ── A + B · chaque champ, chaque état
        for ecran, ouvre, texte in (('fiche', fiche, None), ('fiche · note 4 rangées', fiche, L2), ('fiche · note 5 rangées', fiche, L3),
                                    ('page +', pageplus, None), ('page + · note 4 rangées', pageplus, L2), ('page + · note 5 rangées', pageplus, L3),
                                    ('Nuée', nuee, None)):
            hote = ouvre()
            if texte and not ecrit(hote, texte):
                ok('%s · la note s’ouvre (sinon rien n’est mesuré)' % ecran, False, 'le Peaufiner ne s’est pas ouvert : pas de zone de note'); continue
            champs = pg.evaluate(CHAMPS, hote)
            if texte: champs = [c for c in champs if c['cle'].startswith('NOTE|')]
            faux = [(c['cle'].split('|')[0], c['h'], c['R'], regle(c['h'])) for c in champs if abs(c['R'] - regle(c['h'])) > 0.6]
            ok('%s · rayon = règle de hauteur (%d champs)' % (ecran, len(champs)), champs and not faux, faux or sorted(set((c['h'], c['R']) for c in champs)))
            airs = []
            for c in champs:
                m, png = capture(hote, c['cle'])
                if not m:
                    airs.append((c['cle'].split('|')[0], 'non confirmé : nœud rebâti pendant la mesure')); continue
                if not png or not m['doigt'] or not m['dedans']:
                    pourquoi = 'hors cadre' if not m['dedans'] else 'recouvert par ' + ','.join(sorted(set(m['rate'])))
                    airs.append((c['cle'].split('|')[0], 'non confirmé : ' + pourquoi)); continue
                if m['ov']:
                    CONNUS.append('%s · %s · %s : le rond photo de la page + posé sur la rangée (chantier 64) — exclu de la mesure' % (TH, ecran, c['cle'].split('|')[0]))
                a = air_encre(png, m)
                if a is None: continue
                # (chantier 67 corrigé le 11 sept., nuit : LE TRAIT d'une Nuée n'est plus un défaut connu — il tient l'air comme les autres)
                airs.append((c['cle'].split('|')[0], round(a, 2)))
            bas = [x for x in airs if isinstance(x[1], float) and x[1] < C - 0.5]
            ok('%s · air de l’encre ≥ %.2f' % (ecran, C - 0.5), not bas, bas or ('min %.2f' % min([x[1] for x in airs if isinstance(x[1], float)] or [0]), [x for x in airs if not isinstance(x[1], float)]))
            if texte:
                z = pg.evaluate("(h)=>{ const z=document.querySelector(h+' .s2-zone'); z.scrollIntoView({block:'center'}); const t=z.querySelector('textarea'); return Object.assign(window.__V.lignes(z), {montre: t.scrollHeight <= t.clientHeight+1, hauteur: +z.getBoundingClientRect().height.toFixed(1)}); }", hote)
                n = 2 if texte == L2 else 3
                ok('%s · chantier 68 : libellé→texte et texte→visibilité ≥ 10, toutes les lignes montrées' % ecran,
                   z['air_haut'] >= 10 and z['air_bas'] >= 10 and z['montre'] and abs(z['hauteur'] - (118 + (n - 1) * 22.5)) <= .6,
                   ('rangées', z['lignes'], 'h', z['hauteur'], 'libellé→texte', z['air_haut'], 'texte→visibilité', z['air_bas'], 'tout montré', z['montre']))
                pg.wait_for_timeout(300); pg.locator('#device').screenshot(path=os.path.join(OUT, '%s_%s.png' % (TH, ecran.replace(' ', '_').replace('·', '').replace('+', 'plus'))))
                if ecran.startswith('page +') and texte == L3:
                    # la sonde : un observateur posé APRÈS celui du lot (les rappels suivent l'ordre de création) lit la zone
                    # à chaque rebâtissage, avant toute image ; on fait défiler et on attend les rebâtisseurs
                    pg.evaluate("""()=>{ window.__T=[]; const cs=document.getElementById('createSheet');
                        window.__Tmo=new MutationObserver(()=>{ const z=cs.querySelector('.s2-zone'); if(!z) return; const t=z.querySelector('textarea');
                          window.__T.push({n:+z.getAttribute('data-cercle-lignes')||0, h:+z.getBoundingClientRect().height.toFixed(1), montre: t ? t.scrollHeight <= t.clientHeight+1 : null}); });
                        window.__Tmo.observe(cs,{childList:true,subtree:true}); }""")
                    for k in range(5):
                        pg.evaluate("(k)=>{const c=document.querySelector('#createSheet .dpd-corps')||document.querySelector('#createSheet'); c.scrollTop=k*200;}", k); pg.wait_for_timeout(500)
                    pg.wait_for_timeout(1500); T = pg.evaluate("()=>{ window.__Tmo.disconnect(); return window.__T; }")
                    mauvais = [t for t in T if t['n'] != 3 or abs(t['h'] - 163) > .6 or t['montre'] is False]
                    # ⚑ CONTRAT MIS À JOUR AU NIVEAU DE LA DÉCISION (§7) — chantier 70 (11 sept., nuit) : la page + ne rebâtit plus
                    #   sa liste pour rien. Ma première écriture EXIGEAIT d'en voir au moins un (`T and not mauvais`) : « 0 rebâtissage »
                    #   est justement le bon résultat. Ce qu'on protège n'a pas changé — AUCUN rebâtissage ne doit laisser la zone à sa
                    #   hauteur de repos avec un texte plus long (118 au lieu de 163).
                    ok('page + · aucun rebâtissage ne laisse la zone mal calée (%d vus)' % len(T), not mauvais, mauvais[:4] or ('rien à reprendre' if not T else 'toutes à 163, trois lignes, tout montré'))
                vide()
        # ── F · côte à côte : la pilule d'une ligne et le champ ouvert à quatre rangées
        hote = fiche(); ecrit(hote, L2)
        m1, p1 = capture(hote, [c['cle'] for c in pg.evaluate(CHAMPS, hote) if c['cle'].startswith('À QUI|')][0])
        m2, p2 = capture(hote, [c['cle'] for c in pg.evaluate(CHAMPS, hote) if c['cle'].startswith('NOTE|')][0])
        if p1 and p2:
            a, b = Image.open(io.BytesIO(p1)), Image.open(io.BytesIO(p2)); fond = a.getpixel((a.width // 2, 6))
            cv = Image.new('RGB', (a.width + b.width + 120, max(a.height, b.height) + 80), fond); cv.paste(a, (40, 40 + (b.height - a.height) // 2)); cv.paste(b, (80 + a.width, 40))
            cv.save(os.path.join(OUT, '%s_cote_a_cote.png' % TH))
            ok('côte à côte · capturés (pilule %.0f / rayon %.0f · champ ouvert %.0f / rayon %.0f)' % (m1['h'], m1['R'], m2['h'], m2['R']), True, 'seuil/%s_cote_a_cote.png' % TH)
        vide()
        # ── D · L'ÉCRAN QUI VEND — LE BAS DE LA PLANCHE (Tom, 11 sept., Q205).
        #    ⚑ CONTRATS RÉÉCRITS AU NIVEAU DE LA DÉCISION (CLAUDE §7). Ils visaient l'ANCIEN écran corrigé (la phrase du prix,
        #    la marge du titre, de la phrase et de la liste) ; Tom a pris le bas de la planche : « trois mondes en vraies dalles,
        #    « 29 € » en grand, « Prendre l'année » en premier », « les vraies dalles, rendues par le moteur […] pas un visuel »,
        #    « l'essai de 14 jours reste visible, sous « Prendre l'année » ». Les cotes sont celles de la planche, EN DUR ici.
        #    Version d'origine : verif_seuil-avant-vend-planche.py
        pg.evaluate("()=>setPremium(false)"); pg.wait_for_timeout(300)
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>document.getElementById('cercleTopBtn').click()"); pg.wait_for_timeout(1500)
        v = pg.evaluate(VEND)
        if v.get('absent'):
            ok('écran qui vend · le bas de la planche est là (cadre, trois dalles, « 29 € »)', False, 'ABSENT — l’écran montre : %r' % v.get('textes')); v = None
        if v:
            for nom, cond, detail in contrats_vend(v): ok(nom, cond, detail)
        pg.screenshot(path=os.path.join(OUT, '%s_vend_haut.png' % TH), clip=pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}"))
        # ── E · les portes : le gardé de côté (par-dessus), les Réglages
        pg.evaluate(BASE); pg.wait_for_timeout(200); pg.evaluate("()=>{const d=promises.find(p=>p.draft); if(d) openDetail(d.id);}"); pg.wait_for_timeout(1800)
        pg.evaluate("()=>document.getElementById('csBotBar').click()"); pg.wait_for_timeout(1800)
        pt = pg.evaluate("()=>window.__V.point('#createSheet .s2-encart')"); pg.wait_for_timeout(250); pt = pg.evaluate("()=>window.__V.point('#createSheet .s2-encart')")
        if pt: pg.mouse.click(pt['x'], pt['y'])
        pg.wait_for_timeout(1000); e = pg.evaluate("()=>window.__V.etat()")
        ok('gardé de côté · l’encart mène à l’écran qui vend, par-dessus', e['ps_show'] and e['dessus'] and pg.evaluate("()=>window.__V.dessusVisible()"), (pt and pt['recoit'], e['couches']))
        pg.evaluate(BASE); pg.wait_for_timeout(300); pg.evaluate("()=>document.getElementById('settingsBtn').click()"); pg.wait_for_timeout(1700)
        pt = pg.evaluate("()=>window.__V.point('#openPlusTop')"); pg.wait_for_timeout(250); pt = pg.evaluate("()=>window.__V.point('#openPlusTop')")
        if pt: pg.mouse.click(pt['x'], pt['y'])
        pg.wait_for_timeout(1000); e = pg.evaluate("()=>window.__V.etat()")
        ok('Réglages · l’encart mène à l’écran qui vend', e['ps_show'] and pg.evaluate("()=>{const p=document.getElementById('plusScreen'); const r=p.getBoundingClientRect(); const h=document.elementFromPoint(r.left+r.width/2, r.top+420); return !!(h&&p.contains(h));}"), (pt and pt['recoit'], e['couches']))
        # ── G · SANS AUCUN PROMI : la vraie liste vidée dans la page (le démarrage neuf n'y arrive pas : le jeu se remplit
        #    derrière — chantier 71), puis la porte de l'accueil
        pg.evaluate("()=>{ promises.length=0; }"); pg.evaluate(BASE); pg.wait_for_timeout(400)
        pg.evaluate("()=>document.getElementById('cercleTopBtn').click()"); pg.wait_for_timeout(1400)
        for nom, cond, detail in contrats_vide(pg.evaluate(VIDE)): ok(nom, cond, detail)
        pg.screenshot(path=os.path.join(OUT, '%s_vend_vide.png' % TH), clip=pg.evaluate("()=>{const r=document.querySelector('.frame').getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};}"))
        ctx.close()
    br.close()
json.dump({'R': R, 'connus': CONNUS}, open(os.path.join(OUT, 'verif.json'), 'w'), ensure_ascii=False, indent=1)
print('\n══ défauts connus, déclarés (non comptés) :'); [print('   · ' + c) for c in CONNUS]
print('══ %d contrat(s) raté(s)' % len(KO)); [print('   ✗ ' + k) for k in KO]
