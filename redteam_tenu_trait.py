#!/usr/bin/env python3
"""redteam_tenu_trait.py — ⚑ v163b (Tom, C-189 ; AUDIT-BOUTONS 15, point 1) : AUCUNE PAROLE NE DEVIENT TENUE SANS TRAIT TRACÉ.

« Retire l'acte TENIR du Fil (TRACER reste et ouvre la fiche). Retire « Belle série — partage ton Noyau » et « ✧ bravo » avec leur code. Liste par grep tous
les chemins qui écrivent l'état tenu. Juge : aucune parole ne devient tenue sans trait tracé. »
  A · LES CHEMINS (statique, sur le fichier) : chaque écriture de `status='tenu'` est listée ; seules restent celles du trait (le sélecteur d'état de la
      fiche, que seul le trait actionne ; la dernière part tracée, `lot-V145-PARTS`) — aucune autre ; `feedKeep`, la réaction et le message n'existent plus ;
  B · LE FIL AU DOIGT : une parole à tenir y porte TRACER et REPORTER, pas TENIR ; l'appui maintenu puis chaque acte touché : aucune parole ne passe tenue ;
      TRACER ouvre sa fiche ; aucun texte « bravo » ni « série » à l'écran ;
  C · LE PIÈGE : tant que le juge touche (Fil, cartes, accueil), toute écriture de « tenu » sur une parole est relevée avec sa pile — il n'y en a aucune ;
      puis un vrai trait sur la fiche la tient (le chemin légitime marche toujours).
Preuve : `--fichier=zz-v162.html` rougit (A, B).
"""
import sys, re, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-100s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
S = io.open(F, encoding='utf-8').read(); L = S.split('\n')
ecr = [(i + 1, l) for i, l in enumerate(L) if re.search(r"\.status\s*=\s*'tenu'|status\s*=\s*b\.dataset\.st", l)]
autorises = []
for n, l in ecr:
    if 'segStatus' in l: autorises.append((n, 'le sélecteur d\'état de la fiche (actionné par le trait)'))
    elif "else { p.status='tenu';" in l: autorises.append((n, 'la dernière part tracée (lot-V145-PARTS)'))
autres = [(n, l.strip()[:120]) for n, l in ecr if n not in [a[0] for a in autorises]]
print('  chemins qui écrivent « tenu » :'); [print('    l. %d · %s' % a) for a in autorises]; [print('    l. %d · AUTRE : %s' % a) for a in autres]
juge('A · seuls les chemins du trait écrivent « tenu »', not autres and len(autorises) >= 2, autres)
juge('A · feedKeep, la réaction ✧ et le message du 2e et du 5e tenu n\'existent plus', 'function feedKeep' not in S and "' bravo</div>'" not in S and 'Belle s\\u00e9rie' not in S and 'Belle série' not in S,
     [x for x in ('function feedKeep', "' bravo</div>'", 'Belle série', 'Belle s\\u00e9rie') if x in S])
PIEGE = """(()=>{ window.__tenu=[]; window.__garde=false; const pose=function(p){ if(!p || p.__piege) return; let v=p.status; p.__piege=1;
   Object.defineProperty(p,'status',{configurable:true, enumerable:true, get:()=>v, set:function(n){ if(n==='tenu' && v!=='tenu' && window.__garde) window.__tenu.push([p.title, (new Error()).stack.split('\\n').slice(1,5).join(' | ')]); v=n; }}); };
   setInterval(function(){ try{ (window.promises||[]).forEach(pose); }catch(_){ } try{ promises.forEach(pose); }catch(_){ } }, 200); })();"""
with sync_playwright() as p:
    b = p.webkit.launch()
    ctx = B.contexte(b); B.toile_pleine(ctx, 10); ctx.add_init_script(PIEGE); pg = B.ouvre(ctx, F)
    # une parole à tenir, dans le Fil
    pid = pg.evaluate("()=>{ const p=promises.find(q=>!q.draft && !q.req && !q.chiche && q.status!=='tenu' && !q.nuee); p.due=-1; if(typeof feedAdd==='function') feedAdd('added','Ton Promi « '+p.title+' » est à tenir',{pid:p.id}); saveState&&saveState(); syncAll&&syncAll(); return p.id; }")
    pg.wait_for_timeout(600); pg.evaluate("()=>{ window.__garde=true; }")
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2600)
    carte = pg.evaluate("id=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const c=[...document.querySelectorAll('#feedView .s4-carte')].find(c=>+c.getAttribute('data-pid')===id) || document.querySelector('#feedView .s4-carte'); if(!c) return null; c.scrollIntoView({block:'center'}); const r=c.getBoundingClientRect(); return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", pid)
    pg.wait_for_timeout(400)
    carte = pg.evaluate("id=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const c=[...document.querySelectorAll('#feedView .s4-carte')].find(c=>+c.getAttribute('data-pid')===id) || document.querySelector('#feedView .s4-carte'); if(!c) return null; const r=c.getBoundingClientRect(); return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", pid)
    actes = []
    if carte:
        B.glisse(pg, [carte, carte], pas=20, tenue=700); pg.wait_for_timeout(700)
        actes = pg.evaluate("()=>[...document.querySelectorAll('#feedView .s4-acte')].filter(b=>b.getBoundingClientRect().height>0).map(b=>b.textContent.trim())")
    juge('B · une parole à tenir dans le Fil : TRACER et REPORTER, jamais TENIR', 'TRACER' in actes and 'TENIR' not in actes, actes)
    texte = pg.evaluate("()=>document.getElementById('feedView').innerText")
    juge('B · aucun « bravo » ni « série » à l\'écran du Fil', not re.search(r'bravo|série', texte, re.I), re.findall(r'.{0,20}(?:bravo|série).{0,20}', texte, re.I)[:3])
    if 'TRACER' in actes:
        t = pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const b=[...document.querySelectorAll('#feedView .s4-acte')].find(b=>b.textContent.trim()==='TRACER'); const r=b.getBoundingClientRect(); return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }")
        B.tap(pg, t[0], t[1]); pg.wait_for_timeout(2600)
        r = pg.evaluate("id=>({fiche:document.getElementById('detailPoster').classList.contains('show'), statut:promises.find(p=>p.id===id).status})", pid)
        juge('B · TRACER ouvre la fiche, la parole reste à tenir', r['fiche'] and r['statut'] != 'tenu', r)
    # C · tous les autres touchers du Fil : aucune écriture de « tenu »
    pg.evaluate("()=>{ try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(800)
    B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2400)
    for i in range(4):
        c = pg.evaluate("i=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const L=[...document.querySelectorAll('#feedView .s4-carte')]; const c=L[i]; if(!c) return null; c.scrollIntoView({block:'center'}); const r=c.getBoundingClientRect(); return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k]; }", i)
        if not c: break
        pg.wait_for_timeout(300); B.glisse(pg, [c, c], pas=20, tenue=700); pg.wait_for_timeout(600)
        for a in pg.evaluate("()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; return [...document.querySelectorAll('#feedView .s4-acte')].filter(b=>b.getBoundingClientRect().height>0 && b.textContent.trim()!=='TRACER').map(b=>{ const r=b.getBoundingClientRect(); return [(r.left+r.width/2-D.left)/k, (r.top+r.height/2-D.top)/k, b.textContent.trim()]; }); }"):
            if a[2] in ('REPORTER',): continue
            B.tap(pg, a[0], a[1]); pg.wait_for_timeout(500)
    tn = pg.evaluate("()=>window.__tenu")
    juge('C · aucune parole n\'est devenue tenue pendant les touchers du Fil', not tn, tn)
    # C · le vrai trait tient toujours
    pg.evaluate("()=>{ window.__garde=false; try{ window._peaufSortie&&_peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(800)
    pg.evaluate("id=>openDetail(id)", pid); pg.wait_for_timeout(2600)
    y = pg.evaluate("()=>{ const z=document.getElementById('tenirZone'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390; const r=z.getBoundingClientRect(); return (r.top+r.height/2-D.top)/k; }")
    pts = [[30 + 330 * i / 30, y] for i in range(31)]
    B.glisse(pg, pts, pas=16, tenue=380); pg.wait_for_timeout(3500)
    st = pg.evaluate("id=>promises.find(p=>p.id===id).status", pid)
    juge('C · un vrai trait sur la fiche tient la parole (le chemin légitime)', st == 'tenu', st)
    er = [x for x in pg.erreurs if 'version.json' not in x]
    if er: juge('aucune erreur de page', False, er[:2])
    ctx.close(); b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
