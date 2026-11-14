"""⚑ v203 (Tom, fin de v203, C-278 §4) — PAGE + : CHAQUE SÉQUENCE FINIT PAR UN SEUL MOUVEMENT CONTINU, SANS SAUT NI RECALAGE FINAL.
« En passant à “promets-moi”, les mots changent de place d'un coup : ils glissent. La fin de chaque séquence (taille, rail, phrase, dalle) arrive par un seul mouvement
continu. Juge : chaque séquence de la page + image par image, jusqu'à l'immobilité. Aucune image où un élément se déplace de plus de 2 pt d'un coup. »

WebKit, 390 × 844 ×3, au doigt (banc_tom), Toile de 10 paroles. Une sonde relève CHAQUE IMAGE dans la page, jusqu'à 600 ms d'immobilité : chaque mot de la phrase (son
créneau `data-ph`, ses mots de liaison), le haut de la phrase, sa taille, le rail du pinceau, la dalle et l'horizon (déclarés par le peintre, `_ppEcran`).
Ce qui est relevé est VISIBLE (ni caché, ni transparent : une copie figée peut porter la page pendant le mouvement du clavier, Q598) ; la taille est celle qu'on voit (police × `scale`).
Un SAUT : un déplacement de plus de 2 pt en une image (de 34 ms au plus : une image plus longue, la charge, ne se juge pas ici), quand les images voisines bougent trois fois moins (un glissement accélère et ralentit ; un saut est seul).
Séquences : la validation (Retour) ; le sens basculé trois fois (soi → à quelqu'un → « promets-moi » → soi) ; le titre effacé (l'exemple revient) ; une autre nature.
  A · aucun saut, pour aucun élément, jusqu'à l'immobilité
  B · l'immobilité est atteinte (≤ 4 s)
--seq=valide,sens,efface,nature · --fichier="""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
A = sys.argv[1:]
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
SEQ = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--seq=')), ['valide', 'sens', 'efface', 'nature'])
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
SONDE = r"""()=>{ const H=window.__P=[]; const t0=performance.now(); let calme=0, av=null;
  const D=()=>document.getElementById('device').getBoundingClientRect();
  (function f(){ try{ const d=D(), k=d.width/390, P={}, cs=document.getElementById('createSheet');
    const y=r=>Math.round(((r.top-d.top)/k)*10)/10, x=r=>Math.round(((r.left-d.left)/k)*10)/10;
    const vis=e=>{ for(let q=e;q&&q.nodeType===1;q=q.parentElement){ const c=getComputedStyle(q); if(c.display==='none'||c.visibility==='hidden'||+c.opacity<0.05) return false; if(q===cs) break; } return true; };
    if(cs && cs.classList.contains('show')){
      const t=document.querySelector('#csPhrase .ph-txt, #nueePhrase .ph-txt');
      if(t && vis(t)){ const T=t.getBoundingClientRect(); P.phrase=[x(T), y(T)]; const sc=parseFloat(getComputedStyle(t).scale)||1; P.taille=[Math.round((parseFloat(t.style.fontSize)||0)*sc*10)/10, 0]; const cnt={};
        t.querySelectorAll('[data-ph],[data-np],em').forEach(e=>{ if(e.tagName==='EM' && e.closest('[data-ph],[data-np]')) return; const s=(e.textContent||'').trim(), n=(cnt[s]=(cnt[s]||0)+1), r=e.getBoundingClientRect(); if(!(r.width>0) || !vis(e)) return;
          const kk=(e.getAttribute('data-ph')||e.getAttribute('data-np')) ? 'mot:'+(e.getAttribute('data-ph')||e.getAttribute('data-np')) : 'liaison:'+s+'#'+n; P[kk]=[x(r), y(r)]; }); }
      const rl=document.getElementById('csPinceau'); if(rl && getComputedStyle(rl).display!=='none' && getComputedStyle(rl).visibility!=='hidden'){ const r=rl.getBoundingClientRect(); if(r.height>0) P.rail=[x(r), y(r)]; }
      try{ const e=window._ppEcran && _ppEcran(); if(e && e.dalle) P.dalle=[Math.round(e.dalle.x*10)/10, Math.round((e.dalle.y+((window._ppHzDalle&&_ppHzDalle())||0))*10)/10]; }catch(_){ }
    }
    const now=performance.now(), s=JSON.stringify(P); H.push([Math.round(now-t0), P]);
    if(s===av) calme+=0; else { calme=now; av=s; }
    window.__Pcalme=now-calme;
  }catch(e){ window.__Perr=String(e); } if(performance.now()-t0<6000 && !(window.__Pcalme>600 && performance.now()-t0>800)) requestAnimationFrame(f); else window.__Pfin=performance.now()-t0; })(); }"""
def sauts(H):
    out = []; cles = set(k for _, P in H for k in P)
    for c in cles:
        S = [(t, P[c]) for t, P in H if c in P]
        d = []
        for i in range(1, len(S)):
            (ta, a), (tb, b) = S[i - 1], S[i]; d.append((tb, max(abs(b[0] - a[0]), abs(b[1] - a[1])), tb - ta))
        for i, (t, v, dt) in enumerate(d):
            if v <= 2: continue
            if dt > 34: continue   # une image longue (la charge) : le mouvement a continué sans être peint — la cadence se juge sur le relevé, pas ici
            voisins = [d[j][1] for j in (i - 1, i + 1) if 0 <= j < len(d) and d[j][2] <= 34]
            if not voisins or v > 3 * max(max(voisins), 0.5): out.append((t, c, round(v, 1)))
    return sorted(out)
def releve(pg, geste, maxi=6500):
    pg.evaluate("()=>{ window.__Pfin=null; }"); pg.evaluate(SONDE); geste(); pg.wait_for_timeout(300)
    for _ in range(int(maxi / 200)):
        if pg.evaluate("()=>window.__Pfin"): break
        pg.wait_for_timeout(200)
    return pg.evaluate("()=>window.__P"), pg.evaluate("()=>window.__Pfin")
def ouvre_nat(pg, nat):
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % nat); pg.wait_for_timeout(2600)
def tape_titre(pg, txt):
    for _ in range(4):
        B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'); pg.wait_for_timeout(900)
        if pg.evaluate("()=>{const a=document.activeElement;return !!a&&a.id==='phIn';}"): break
    pg.keyboard.type(txt, delay=50); pg.wait_for_timeout(300)
def verdict(nom, H, fin):
    s = sauts(H)
    juge(nom + ' A · aucun saut jusqu\'à l\'immobilité', not s, s[:4])
    juge(nom + ' B · immobile en ≤ 4 s', fin is not None and fin <= 4600, fin)
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_page_plus_continu — %s · charge %.1f' % (F, B.charge()))
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx, F)
    ouvre_nat(pg, 'promi'); tape_titre(pg, 'lire')
    H, fin = releve(pg, lambda: pg.keyboard.press('Enter'))
    if 'valide' in SEQ: verdict('[valider]', H, fin)
    pg.wait_for_timeout(1500)
    if 'sens' in SEQ:
        for i, nom in enumerate(('soi → à quelqu\'un', 'à quelqu\'un → promets-moi', 'promets-moi → soi')):
            H, fin = releve(pg, lambda: B.tap_sel(pg, '#csPhrase [data-ph=sens]')); verdict('[sens %s]' % nom, H, fin); pg.wait_for_timeout(800)
    if 'efface' in SEQ:
        tape = lambda: (B.tap_sel(pg, '#csPhrase .ph-m[data-ph="titre"]'), pg.wait_for_timeout(700), [pg.keyboard.press('Backspace') for _ in range(4)], pg.keyboard.press('Enter'))
        H, fin = releve(pg, tape); verdict('[titre effacé]', H, fin)
    if 'nature' in SEQ:
        B.tap_sel(pg, '#createSheet .closeb'); pg.wait_for_timeout(900)
        H, fin = releve(pg, lambda: ouvre_nat(pg, 'chiche')); verdict('[autre nature]', H, fin)
    ctx.close(); b.close()
print('%d/%d' % (sum(RES), len(RES)))
