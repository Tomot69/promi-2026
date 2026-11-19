"""⚑ v210 (Tom, 18 nov. 2026, §6) — « de » et « d’ » : « de » devient « d’ » discrètement et en direct quand le mot tapé commence par une voyelle (accentuée ou non)
ou un h muet, et redevient « de » quand on efface ou qu'on change de mot, avec la transition tracée (détracé puis tracé : `_retour.liaison`). Les h aspirés gardent « de »
(haïr, hurler, hausser, honte…). Page + d'un Promi et d'un Chiche (un Cercle n'a pas de « de » : vérifié), et l'onboarding. Une série de mots tapés puis effacés, la
liaison attendue à chaque étape ; chaque changement passe par le tracé (`_douceur.texte`), jamais réécrit d'un coup. WebKit, au doigt, clavier simulé.
⚑ v212 (Tom, C-312) — CONTRAT REMIS AU NIVEAU DE LA DÉCISION (original : sauvegardes/redteam_liaison-avant-v212.py) : une place VIDE porte la liaison de son EXEMPLE (« d’ »
devant « apprendre… »), plus « de » d'office (« PASTILLE VIDE : de », v20, remplacé). Effacé → la liaison de l'exemple revenu ; un changement n'est attendu (et tracé) que si
la liaison du mot diffère de celle de l'exemple. La règle de l'exemple est écrite ici, en dur (celle de redteam_liaison_exemples)."""
import os, re, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
src = open('redteam_onb_exemple.py', encoding='utf-8').read(); ns = {}
for nom in ('CLAV', 'INIT'):
    m = re.search(r'^%s\s*=\s*(""".*?"""|\'\'\'.*?\'\'\'|"[^\n]*"|\'[^\n]*\')' % nom, src, re.S | re.M)
    if m: ns[nom] = eval(m.group(1))
CLAV = ns.get('CLAV', ''); 
SERIE = [('aller', 'd’'), ('écrire', 'd’'), ('Être', 'd’'), ('ôter', 'd’'), ('habiter', 'd’'), ('hiverner', 'd’'), ('haïr', 'de'), ('hurler', 'de'), ('hausser', 'de'),
         ('honte', 'de'), ('lire', 'de'), ('y aller', 'd’'), ('oui', 'de'), ('11 km', 'de')]
ok = tot = 0
def juge(m, c, d=''):
    global ok, tot
    tot += 1; ok += bool(c); print('  %s %s %s' % ('✅' if c else '❌', m, '' if c else str(d)[:260]), flush=True)
SUIT = """()=>{ window.__lt=[]; const D=window._douceur; if(D && D.texte && !D.__lt){ D.__lt=1; const f=D.texte; D.texte=function(el,a,b){ if(el && el.matches && el.matches('.ph-li, .onbv-de, em')) window.__lt.push([String(a).replace(/<[^>]*>/g,''), String(b).replace(/<[^>]*>/g,'')]); return f.apply(this, arguments); }; } }"""
# ⚑ v211 (Tom, C-310) — « aucune image où « de » ou « d’ » passe d'absent à entier, ou d'entier à absent » : à chaque image, l'état VU de la liaison — entier (le texte
# réel sans découpe), absent (découpé à vide et rien sur le canevas du tracé), ou en cours (le canevas du tracé porte de l'encre) ; deux images voisines entier ↔ absent = un changement sec.
REC = r"""(sel)=>{ window.__fr=[]; let on=true; window.__frStop=()=>{on=false;}; const V=c=>c.replace(/\s+/g,'')==='polygon(0px0px,0px0px,0px0px)';
  const f=()=>{ if(!on) return; const e=document.querySelector(sel); if(!e){ window.__fr.push(['?']); requestAnimationFrame(f); return; }
    const lr=e.getBoundingClientRect(), cp=getComputedStyle(e).clipPath; let ink=0;
    document.querySelectorAll('canvas[data-trace]').forEach(c=>{ const r=c.getBoundingClientRect(); if(!(r.width>0 && r.right>lr.left && r.left<lr.right && r.bottom>lr.top && r.top<lr.bottom)) return;
      try{ const g=c.getContext('2d'), sx=c.width/r.width, sy=c.height/r.height, x0=Math.max(0,Math.floor((lr.left-r.left)*sx)), y0=Math.max(0,Math.floor((lr.top-r.top)*sy)), w=Math.max(1,Math.min(c.width-x0,Math.ceil(lr.width*sx))), h=Math.max(1,Math.min(c.height-y0,Math.ceil(lr.height*sy)));
        const d=g.getImageData(x0,y0,w,h).data; for(let i=3;i<d.length;i+=4) if(d[i]>60) ink++; }catch(_){ } });
    const t=(e.textContent||'').trim(); const st=cp==='none'?(ink>0?'cours':'entier'):(V(cp)?(ink>0?'cours':'absent'):'cours');
    if(st==='absent'){ e.__abs=e.__abs||performance.now(); if(performance.now()-e.__abs>250 && !window.__diag310) window.__diag310={t:t, voulu:e.__voulu, tx:!!e.__v203tx, cache:!!e.__tlCache, trace:!!e.__trace, j:(window.__c310||[]).slice(-6), styleClip:e.style.getPropertyValue('clip-path').slice(0,30), dc:window.__dcA?window.__dcA.has(e):null}; } else e.__abs=0;
    window.__fr.push([t, cp==='none'?(ink>0?'cours':'entier'):(V(cp)?(ink>0?'cours':'absent'):'cours')]); requestAnimationFrame(f); }; requestAnimationFrame(f); }"""
def secs(fr):
    out = []
    for a, z in zip(fr, fr[1:]):
        if len(a) < 2 or len(z) < 2: continue
        if {a[1], z[1]} == {'entier', 'absent'} or (a[1] == 'entier' and z[1] == 'entier' and a[0] != z[0]): out.append((a, z))
    return out
SECS = []
def norm(s): return (s or '').replace(' ', ' ').strip()
from liaison_regle import attendu as ATTENDU
EXEMPLE = """(s)=>{ if(s.indexOf('#onbPh')===0){ const pm=document.querySelector('#onbPh .onbv-pm[data-onb="parole"]'); return pm?pm.textContent:''; } return window._ppExempleCourant||''; }"""
def serie(pg, LI, T):
    for mot, att in SERIE:
        ex = pg.evaluate(EXEMPLE, LI); exli = ATTENDU(ex)
        pg.evaluate("()=>{ window.__lt=[]; }"); pg.evaluate(REC, LI)
        pg.keyboard.type(mot, delay=45); pg.wait_for_timeout(1500)
        li = norm(pg.evaluate("(s)=>{ const e=document.querySelector(s); return e?e.textContent:null; }", LI)); lt = pg.evaluate("()=>window.__lt")
        chg = att != exli
        juge('%s « %s » → « %s » (l’exemple : « %s… »)' % (T, mot, att, ex[:18]), li == att and (not chg or any(norm(b) == att for a, b in lt)), [li, lt])
        for _ in range(len(mot)): pg.keyboard.press('Backspace'); pg.wait_for_timeout(40)
        pg.wait_for_timeout(1500); li = norm(pg.evaluate("(s)=>{ const e=document.querySelector(s); return e?e.textContent:null; }", LI)); lt = pg.evaluate("()=>window.__lt")
        pg.evaluate("()=>__frStop()"); s_ = secs(pg.evaluate("()=>__fr")); SECS.extend(s_)
        if s_: print('     diag', pg.evaluate("()=>{ const d=window.__diag310; window.__diag310=null; return d; }"))
        juge('%s « %s » tapé puis effacé : aucun changement sec, image par image (C-310)' % (T, mot), not s_, s_[:2])
        juge('%s « %s » effacé → « %s » (la liaison de l’exemple)%s' % (T, mot, exli, ', tracé' if chg else ''), li == exli and (not chg or any(norm(b) == exli for a, b in lt)), [li, lt])
with sync_playwright() as p:
    b = p.webkit.launch(); print('redteam_liaison — %s · charge %.1f' % (F, B.charge()))
    for k in ('promi', 'chiche', 'nuee'):
        ctx = B.contexte(b, vw=430, vh=932)
        if CLAV: ctx.add_init_script(CLAV)
        pg = B.ouvre(ctx, F)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700); B.tap_sel(pg, '.acc-pil[data-k=%s]' % k); pg.wait_for_timeout(2600); pg.evaluate(SUIT)
        if k == 'nuee':
            t = pg.evaluate("()=>{ const p=document.getElementById('nueePhrase'); return p?p.textContent:''; }")
            juge('[Cercle] la phrase n\'a pas de « de »', not re.search(r"(^|\s)(de|d’)(\s|$)", t.replace(' ', ' ')), t); ctx.close(); continue
        B.tap_sel(pg, '#csPhrase [data-ph=titre]'); pg.wait_for_timeout(1500)
        serie(pg, '#csPhrase .ph-li', '[page + %s]' % k); ctx.close()
    # l'onboarding : la page de la parole
    ctx = B.contexte(b, onb=False, guide=False)
    if CLAV: ctx.add_init_script(CLAV)
    pg = B.ouvre(ctx, F, attente=7000); B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(700)
    pg.keyboard.type('Camille', delay=30); pg.wait_for_timeout(400); pg.keyboard.press('Enter'); pg.wait_for_timeout(4200); B.attend_parole(pg); pg.evaluate(SUIT)
    B.tap_sel(pg, '#onbPh [data-onb="parole"]'); pg.wait_for_timeout(1500)
    serie(pg, '#onbPh .onbv-de', '[onboarding]'); ctx.close()
    b.close()
print('\nredteam_liaison : %d/%d' % (ok, tot)); sys.exit(0 if ok == tot else 1)
