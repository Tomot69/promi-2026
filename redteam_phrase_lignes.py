#!/usr/bin/env python3
"""redteam_phrase_lignes.py — ⚑ v180b (Tom, C-240) : « page + d'un Chiche, phrase de cinq lignes : la dernière ligne et « Garder de côté » passent sous les
choix du trait (Plein, Coulé…). Rien ne doit se recouvrir, quelle que soit la longueur de la phrase. »

Banc WebKit ×3, Promi · Chiche · Cercle, phrases de 1 à 6 lignes (le titre allongé jusqu'à ce que la phrase compte n lignes), clavier fermé, échelles 1
(430 × 932) et 0,79 (330 × 714). Lu sur les boîtes du TEXTE (Range, l'encre de la police) et des blocs : les lignes de la phrase, le mot du trait, la rangée
du pinceau, « garder de côté », la barre Peaufiner, le bouton photo :
  R · aucun de ces blocs n'en recouvre un autre (≥ 2 pt d'air), aucun ne sort de l'écran ; la phrase entière est visible.
Une phrase d'un mot compte déjà 2 lignes (Promi), 3 (Cercle) ou 4 (Chiche) : « 1 à 6 lignes » se lit « chaque longueur que la phrase prend, de la plus
courte à la plus longue » ; mesuré, la phrase la plus longue tient en 5 lignes (le titre passe à la ligne puis se coupe en « … »).
Rouge sur v179b (`--fichier=zz-v179b.html`) : le Chiche de cinq lignes.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
PAS = [1, 3, 5, 8, 12, 18, 28]
ECH = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--echelle=')), '1,0.79').split(',')
NATS = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--natures=')), 'promi,chiche,nuee').split(',')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-80s %s' % ('✅' if ok else '❌', nom, str(d)[:300]), flush=True)
MOTS = 'courir le marathon de Paris avec toute la bande des copains du quartier puis fêter cela longtemps au bord du canal sous les lampions jusqu\'au matin et recommencer'.split()
SEL = {'promi': '#csPhrase .ph-m[data-ph="titre"]', 'chiche': '#csPhrase .ph-m[data-ph="titre"]', 'nuee': '#nueePhrase .ph-m[data-np="nom"]'}
def pose(pg, k, t):
    """la vraie saisie : toucher le mot de la phrase, tout remplacer au clavier, Retour (le clavier se ferme)"""
    ACT = "()=>{ const a=document.activeElement; return !!(a && (a.tagName==='INPUT'||a.tagName==='TEXTAREA')); }"
    for _ in range(3):
        c = pg.evaluate("s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getClientRects()[0]; return r?[r.left+Math.min(r.width/2,30), r.top+r.height/2]:null; }", SEL[k])   # une pastille sur deux lignes a un creux au milieu de sa boîte : on touche son premier rectangle
        if c: pg.touchscreen.tap(c[0], c[1])
        pg.wait_for_timeout(450)
        if pg.evaluate(ACT): break
    if not pg.evaluate(ACT): return False   # aucun champ n'a la main : on ne tape rien (Retour arrière ferait reculer la page)
    pg.evaluate("t=>{ const a=document.activeElement; a.value=''; a.dispatchEvent(new Event('input',{bubbles:true})); }", '')
    pg.keyboard.type(t, delay=4); pg.keyboard.press('Enter'); return True
GEO = """k=>{ const cs=document.getElementById('createSheet'), D=document.getElementById('device').getBoundingClientRect(), s=D.width/390;
  const R=r=>[(r.left-D.left)/s,(r.top-D.top)/s,(r.right-D.left)/s,(r.bottom-D.top)/s];
  const vu=e=>{ if(!e) return false; const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; const r=e.getBoundingClientRect(); return r.width>1&&r.height>1; };
  const ph=document.querySelector(k==='nuee'?'#nueePhrase .ph-txt':'#csPhrase .ph-txt'); const lignes=[];
  if(ph){ const rg=document.createRange(); rg.selectNodeContents(ph); const L=[...rg.getClientRects()].filter(r=>r.width>2&&r.height>2).map(R);
    L.sort((a,b)=>a[1]-b[1]); for(const r of L){ const d=lignes.find(l=>Math.abs((l[1]+l[3])/2-(r[1]+r[3])/2)<6); if(d){ d[0]=Math.min(d[0],r[0]); d[2]=Math.max(d[2],r[2]); d[1]=Math.min(d[1],r[1]); d[3]=Math.max(d[3],r[3]); } else lignes.push(r.slice()); } }
  const B={}; const txt=(sel,n)=>{ const e=cs.querySelector(sel); if(!vu(e)) return; const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); if(r.width>1) B[n]=R(r); };
  const box=(sel,n)=>{ const e=document.querySelector(sel); if(vu(e)) B[n]=R(e.getBoundingClientRect()); };
  txt('.pp-trace','trace'); box('#csPinceau','rail'); txt('.pp-garder','garder'); box('#csBotBar','barre'); box('#createSheet .dp-photo-nid button, #csPhotoBtn','photo');
  return {lignes:lignes, B:B, H:844}; }"""
def stable(pg, k, ms=9000):
    """la page + posée : clavier fermé (pas de `pp-ouvert`), aucun mouvement en cours (#ppMvt absent), deux relevés identiques à 350 ms"""
    av = None; t = 0; n_ok = 0
    while t < ms:
        pg.wait_for_timeout(350); t += 350
        if pg.evaluate("()=>{ const cs=document.getElementById('createSheet'); return !!(cs && !cs.classList.contains('pp-ouvert') && !document.getElementById('ppMvt') && !(document.activeElement && document.activeElement.tagName==='INPUT')); }"):
            g = pg.evaluate(GEO, k); sig = repr([[round(v) for v in l] for l in g['lignes']] + sorted((x, [round(v) for v in r]) for x, r in g['B'].items()))
            if sig == av and (('barre' not in g['B']) or g['B']['barre'][3] <= 845): n_ok += 1
            else: n_ok = 0
            if n_ok >= 2: return g
            av = sig
    return pg.evaluate(GEO, k)
def recouvre(a, b, air=2):
    return not (a[2] <= b[0] + 0.5 or b[2] <= a[0] + 0.5 or a[3] + air <= b[1] or b[3] + air <= a[1])
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh, nom in [x for x in ((430, 932, '1'), (330, 714, '0,79')) if (x[2] == '1' and '1' in ECH) or (x[2] != '1' and '0.79' in ECH)]:
        for k in NATS:
            ctx = B.contexte(b, vw=vw, vh=vh); pg = B.ouvre(ctx, F)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600)
            vus = {}
            for m in PAS:
                pose(pg, k, ' '.join(MOTS[:m])); g = stable(pg, k); n = len(g['lignes'])
                vus.setdefault(n, m)
                T = '[%s · ×%s · %d ligne%s · %d mots]' % (k, nom, n, 's' if n > 1 else '', m)
                blocs = [('ligne %d' % (i + 1), l) for i, l in enumerate(g['lignes'])] + list(g['B'].items())
                pb = []
                for i in range(len(blocs)):
                    for j in range(i + 1, len(blocs)):
                        a_, b_ = blocs[i], blocs[j]
                        if a_[0].startswith('ligne') and b_[0].startswith('ligne'): continue
                        if recouvre(a_[1], b_[1]): pb.append('%s × %s' % (a_[0], b_[0]))
                    r = blocs[i][1]
                    if r[0] < -0.5 or r[2] > 390.5 or r[3] > 844.5 or r[1] < -0.5: pb.append('%s hors de l\'écran' % blocs[i][0])
                juge(T + ' R · rien ne se recouvre, rien ne sort', n > 0 and not pb, pb or {x: [round(v) for v in r] for x, r in blocs})
            m = len(MOTS) + 1
            juge('[%s · ×%s] la phrase a été jugée de sa forme la plus courte (un mot) à la plus longue (%d mots)' % (k, nom, PAS[-1]), 1 in vus.values() and PAS[-1] >= len(MOTS) - 1, 'lignes : mots %s' % sorted(vus.items()))
            juge('[%s · ×%s] aucune erreur de page' % (k, nom), not pg.erreurs, pg.erreurs[:2])
            ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
