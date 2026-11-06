#!/usr/bin/env python3
"""redteam_textes_longs.py — ⚑ v181b (Tom, 6 nov. 2026, C-244) — LES TEXTES LONGS.
« 5.1 Page + (Promi, Chiche, Cercle) : laisse la phrase prendre plus de lignes en réduisant encore sa taille par paliers, sans rien recouvrir. 5.2 Fiches :
la phrase ou le nom restent affichés comme aujourd'hui ; un toucher sur le texte le DÉPLIE en entier ; un nouveau toucher le REPLIE ; les éléments du dessous
descendent en douceur, sous le bandeau de Peaufiner ; si le texte est très long, la fiche défile. 5.3 Limite à la saisie : 280 caractères pour une parole,
40 pour le nom d'un Cercle ; dans la fiche d'un Cercle, son nom replié est plus court que la phrase d'un Promi. Juge : 3 natures, textes court, moyen et à la
limite ; aucun recouvrement, replié comme déplié ; mouvement doux ; la limite est tenue à la saisie, collage compris. »

Banc WebKit ×3 (banc_tom), 430 × 932 (échelle 1) ; la page + à la limite aussi à 330 × 714 (0,79).
  P · page + : la vraie saisie (la phrase touchée, le clavier, Retour), textes court, moyen et à la limite : aucun bloc ne se recouvre ni ne sort de l'écran,
      la parole est ENTIÈRE à l'écran (aucun « … »).
  L · la limite : 300 caractères tapés → 280 ; 300 collés → 280 ; le nom d'un Cercle : 50 tapés → 40, 50 collés → 40.
  F · fiche replié : ni recouvrement ni sortie sous le bandeau ; un Promi, un Chiche : trois lignes au plus ; un Cercle : deux lignes au plus.
  D · un titre coupé, touché au doigt : il se DÉPLIE en entier (le texte complet), ce qui suit DESCEND en glissant (au moins 6 positions intermédiaires,
      aucun pas de plus d'un tiers) ; rien ne se recouvre ; trop long pour l'écran, la fiche défile jusqu'à lui ; touché de nouveau, il se REPLIE tel qu'avant.
  E · aucune erreur de page.
Rouge sur v180b (`--fichier=zz-v180b.html`) : P à la limite (« … »), L, D.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
src = open('redteam_phrase_lignes.py', encoding='utf-8').read()
exec(src.split('with sync_playwright() as p:')[0].split('from playwright.sync_api import sync_playwright')[1].replace('F = next', 'F_ = next').replace('res = []', '').replace('def juge', 'def _juge'))
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
BASE = ('courir le marathon de Paris avec toute la bande des copains du quartier puis fêter cela longtemps au bord du canal sous les lampions jusqu’au matin '
        'et recommencer l’année suivante avec encore plus de monde, des voisins, des cousins, des collègues et même le chien de la boulangère qui court vite ') * 2
TXT = {'promi': {'court': 'appeler mamie', 'moyen': BASE[:110].strip(), 'limite': BASE[:280]},
       'chiche': {'court': 'nager le mardi', 'moyen': BASE[:110].strip(), 'limite': BASE[:280]},
       'nuee': {'court': 'Le potager', 'moyen': 'Les amis du jardin partagé', 'limite': 'Les amis du grand jardin partagé du coin'[:40]}}
FICHE = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, R=r=>[(r.left-D.left)/k,(r.top-D.top)/k,(r.right-D.left)/k,(r.bottom-D.top)/k];
  const vu=e=>{ if(!e) return false; const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; const r=e.getBoundingClientRect(); return r.width>1&&r.height>1; };
  const B={}; ['dptQui','dptTitre','dptQuand','cm5Ligne','cm5Dernier','nfAdd'].forEach(id=>{ const e=document.getElementById(id); if(!vu(e)) return; const rg=document.createRange(); rg.selectNodeContents(e); const r=rg.getBoundingClientRect(); if(r.width>1) B[id]=R(r); });
  const ti=document.getElementById('dptTitre'), lh=parseFloat(getComputedStyle(ti).lineHeight)||parseFloat(getComputedStyle(ti).fontSize)*1.02;
  const d=document.getElementById('detailPoster');
  return {B:B, texte:ti.textContent, lignes:Math.round(ti.getBoundingClientRect().height/k/lh), coupe:ti.getAttribute('data-coupe'), sh:d.scrollHeight, ch:d.clientHeight, st:d.scrollTop}; }"""
def chevauche(Bx):
    pb = []; ks = list(Bx)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            if recouvre(Bx[ks[i]], Bx[ks[j]], 2): pb.append('%s × %s' % (ks[i], ks[j]))
    return pb
def suit(pg, sel, ms=3000):
    pg.evaluate("s=>{ window.__mv=[]; const e=document.querySelector(s); const t0=performance.now(); (function f(){ const r=e.getBoundingClientRect(); window.__mv.push(r.top); if(performance.now()-t0<%d) requestAnimationFrame(f); })(); }" % ms, sel)
with sync_playwright() as p:
    b = p.webkit.launch()
    # P et L · la page +
    for vw, vh, nom, cas in ((430, 932, '1', ('court', 'moyen', 'limite')), (330, 714, '0,79', ('limite',))):
        for k in ('promi', 'chiche', 'nuee'):
            ctx = B.contexte(b, vw=vw, vh=vh); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600)
            for c in cas:
                t = TXT[k][c]; T = '[page + · %s · ×%s · %s, %d car.]' % (k, nom, c, len(t))
                ok = pose(pg, k, t); g = stable(pg, k)
                blocs = [('ligne %d' % (i + 1), l) for i, l in enumerate(g['lignes'])] + list(g['B'].items()); pb = []
                for i in range(len(blocs)):
                    for j in range(i + 1, len(blocs)):
                        if blocs[i][0].startswith('ligne') and blocs[j][0].startswith('ligne'): continue
                        if recouvre(blocs[i][1], blocs[j][1]): pb.append('%s × %s' % (blocs[i][0], blocs[j][0]))
                    r = blocs[i][1]
                    if r[0] < -0.5 or r[2] > 390.5 or r[3] > 844.5 or r[1] < -0.5: pb.append('%s hors de l\'écran' % blocs[i][0])
                vu = pg.evaluate("k=>{ const e=document.querySelector(k==='nuee'?'#nueePhrase .ph-m[data-np=\"nom\"]':'#csPhrase .ph-m[data-ph=\"titre\"]'); return e?e.textContent:''; }", k)
                juge(T + ' P · rien ne se recouvre, la parole entière à l\'écran', ok and not pb and '…' not in vu and vu.replace(' ', ' ').strip() == t.strip(), (pb, len(g['lignes']), vu[-30:]))
            if nom == '1':
                lim = 40 if k == 'nuee' else 280; t300 = (BASE * 2)[:lim + 20]; sel = SEL[k]
                pose(pg, k, t300); stable(pg, k)
                v = pg.evaluate("k=>{ const f=document.getElementById(k==='nuee'?'nName':'fTitle'); return f.value.length; }", k)
                for _ in range(3):
                    c = pg.evaluate("s=>{ const e=document.querySelector(s); const r=e.getClientRects()[0]; return [r.left+Math.min(r.width/2,30), r.top+r.height/2]; }", sel); pg.touchscreen.tap(c[0], c[1]); pg.wait_for_timeout(450)
                    if pg.evaluate("()=>{ const a=document.activeElement; return !!(a && a.tagName==='INPUT'); }"): break
                col = pg.evaluate("t=>{ const a=document.activeElement; if(!a||a.tagName!=='INPUT') return -1; a.value=''; a.dispatchEvent(new Event('input',{bubbles:true})); a.focus(); document.execCommand('insertText', false, t); return a.value.length; }", t300)
                pg.keyboard.press('Enter'); pg.wait_for_timeout(600)
                juge('[page + · %s] L · %d tapés → %d, %d collés → %d (limite %d)' % (k, len(t300), v, len(t300), col, lim), v == lim and col == lim, (v, col))
            juge('[page + · %s · ×%s] aucune erreur de page' % (k, nom), not pg.erreurs, pg.erreurs[:2])
            ctx.close()
    # F et D · les fiches
    for k in ('promi', 'chiche', 'nuee'):
      for c in ('court', 'moyen', 'limite'):
        if True:
            ctx = B.contexte(b, vw=430, vh=932); B.toile_pleine(ctx, 'cercle'); pg = B.ouvre(ctx, F, 7000)   # une page neuve par fiche : rien ne se transmet d'une fiche à l'autre
            t = TXT[k][c]; T = '[fiche · %s · %s, %d car.]' % (k, c, len(t))
            pg.evaluate("()=>{ try{_peaufSortie()}catch(e){} closeAll(); }"); pg.wait_for_timeout(500)
            if k == 'nuee': pg.evaluate("t=>{ NUE['potager']=t; openNueeDetail('potager'); }", t)
            else: pg.evaluate("a=>{ const q=promises.find(x=>!x.draft&&!x.nuee&&(a[0]==='chiche'?x.chiche:!x.chiche)); q.title=a[1]; openDetail(q.id); }", [k, t])
            pg.wait_for_timeout(2600); f0 = pg.evaluate(FICHE)
            maxl = 2 if k == 'nuee' else 3
            pb = chevauche(f0['B']) + ['%s sous le bandeau' % x for x, r in f0['B'].items() if r[3] > 760.5 and f0['sh'] <= f0['ch']]
            juge(T + ' F · replié : aucun recouvrement, %d lignes au plus' % maxl, not pb and f0['lignes'] <= maxl, (pb, f0['lignes'], f0['texte'][-24:]))
            if not f0['coupe']:
                juge(T + ' E · aucune erreur de page', not pg.erreurs, pg.erreurs[:2]); ctx.close(); continue
            suit(pg, '#dptQuand'); B.tap_sel(pg, '#dptTitre'); pg.wait_for_timeout(3200); f1 = pg.evaluate(FICHE); mv = pg.evaluate("()=>window.__mv")   # 360 ms prévus ; sous charge les images s'allongent (34 ms d'avancée au plus par image) : on attend la fin
            pos = sorted(set(round(x, 1) for x in mv)); pas = max([abs(mv[i + 1] - mv[i]) for i in range(len(mv) - 1)] or [0]); course = abs(mv[-1] - mv[0]) if mv else 0
            pb = chevauche(f1['B'])
            juge(T + ' D · touché : déplié en entier, ce qui suit glisse, rien ne se recouvre', f1['texte'] == t and not pb and len(pos) >= 8 and pas <= course / 3 + 1 and course > 4,
                 {'texte entier': f1['texte'] == t, 'positions': len(pos), 'course': round(course, 1), 'plus grand pas': round(pas, 1), 'recouvre': pb})
            if f1['sh'] > f1['ch'] + 1:
                pg.evaluate("()=>{ const d=document.getElementById('detailPoster'); d.scrollTop=d.scrollHeight; }"); pg.wait_for_timeout(500); f2 = pg.evaluate(FICHE)
                bas = max(r[3] for r in f2['B'].values())
                juge(T + ' D · trop long pour l\'écran : la fiche défile, tout se lit au-dessus du bandeau', bas <= 760.5, round(bas, 1))
                pg.evaluate("()=>{ document.getElementById('detailPoster').scrollTop=0; }"); pg.wait_for_timeout(400)
            B.tap_sel(pg, '#dptTitre'); pg.wait_for_timeout(3200); f3 = pg.evaluate(FICHE)
            juge(T + ' D · touché de nouveau : replié tel qu\'avant', f3['texte'] == f0['texte'] and all(abs(a - b) < 0.6 for x in f0['B'] for a, b in zip(f0['B'][x], f3['B'].get(x, [0] * 4))), (f3['texte'][-20:], f0['texte'][-20:]))
            juge(T + ' E · aucune erreur de page', not pg.erreurs, pg.erreurs[:2]); ctx.close()
    b.close()
print('\n  %d / %d' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
