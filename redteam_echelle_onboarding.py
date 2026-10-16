#!/usr/bin/env python3
"""
redteam_echelle_onboarding.py — v147 (Tom, 15 oct. 2026, C-138) : UNE ÉCHELLE TYPOGRAPHIQUE POUR TOUT L'ONBOARDING ET LE GUIDE.
« Si tu grossis une page, tu grossis aussi celles d'avant et d'après, et inversement. Pas d'incohérence bête de ce genre. »
Le parcours entier au doigt (stockage vierge, clair puis sombre), puis le guide. Sur chaque page, chaque texte est rangé dans son RÔLE ; la règle : même
rôle = même police, même taille, sur toutes les pages — et ces tailles sont celles de l'échelle écrite dans CLAUDE.md (EN DUR ici) :
  titre      PromiLate 52   (« PROMI » de « Promi planté ! »)
  phrase     Gilbert 35     (« Toi, c'est … ? », « Je me promets de … »)
  texte      Atkinson 27    (« Prénom, donc. Enchanté. », « Quid… », « Petite ou grande promesse… », la phrase de ton, la phrase du guide)
  liste      Atkinson 24    (les lignes Primo, Deuxio, Tertio, « Le reste se découvre en traçant. »)
  mot-clé    PromiLate 27   (Primo, Deuxio, Tertio ; « monde », « Studio », « commence » dans le guide)
  mot de fin PromiLate 32   (« La suite t'appartient. »)
  consigne   PromiLate 19   (« trace pour planter »)
"""
import io, sys, re
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
URL = 'http://127.0.0.1:8752/' + next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--page=')), 'app.html')
ECHELLE = {'titre': ('PromiLate', 52), 'phrase': ('Gilbert', 35), 'texte': ('Atkinson', 27), 'liste': ('Atkinson', 24), 'mot-clé': ('PromiLate', 27), 'mot de fin': ('PromiLate', 32), 'consigne': ('PromiLate', 19)}
ROLES = [('#onbPh', 'phrase'), ('#onbDit', 'texte'), ('#onbQuid', 'texte'), ('#onbSous', 'texte'), ('#onbTrace', 'consigne'), ('#onbFin .onbv-pmot', 'titre'), ('#onbFin .onbv-ton', 'texte'),
         ('#onbFin .onbv-l:not(.onbv-l-der)', 'liste'), ('#onbFin .onbv-l:not(.onbv-l-der) .onbv-k', 'mot-clé'), ('#onbFin .onbv-l-der .onbv-k', 'mot de fin'), ('#guidePhrase', 'texte'), ('#guidePhrase .gd-cle', 'mot-clé')]
LIT = """(R)=>{ const out=[]; R.forEach(([sel, role])=>{ document.querySelectorAll(sel).forEach(e=>{ let v=e, vu=true; while(v&&v!==document.body){ const c=getComputedStyle(v); if(c.display==='none'){ vu=false; break; } v=v.parentElement; }
  if(!vu||!(e.textContent||'').trim()) return; const c=getComputedStyle(e); out.push({sel:sel, role:role, f:c.fontFamily.split(',')[0].replace(/["']/g,'').trim(), fs:Math.round(parseFloat(c.fontSize)*10)/10, t:(e.textContent||'').trim().slice(0,28)}); }); }); return out; }"""
res = []; vus = []
def juge(nom, c, d=''):
    res.append(bool(c)); print('%s  %s  %s' % ('OK' if c else 'KO', nom, str(d)[:260]), flush=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in ('light', 'dark'):
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, color_scheme='dark' if th == 'dark' else 'light')
        if th == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        def releve(page):
            for e in pg.evaluate(LIT, ROLES): e['page'] = page; e['th'] = th; vus.append(e)
        releve('prénom'); prenom(pg, cdp); pg.wait_for_timeout(2500); releve('parole'); parole(pg); saisie(pg); pg.wait_for_timeout(600); releve('trait')
        trace(pg, cdp); pg.wait_for_timeout(5200); d = pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width/390];}")
        toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(9000); releve('fin')
        toucher(cdp, pg, d[0] + 195 * d[2], d[1] + 260 * d[2]); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{ const t=document.querySelector('.onbv-compte .tard'); if(t) t.click(); }")
        for i in range(40):
            pg.wait_for_timeout(250)
            if pg.evaluate("()=>!!document.getElementById('guidePhrase')"): break
        pg.wait_for_timeout(2500); releve('guide')
        ctx.close()
    b.close()
for role, (f, fs) in ECHELLE.items():
    L = [e for e in vus if e['role'] == role]
    pages = sorted(set(e['page'] for e in L)); tailles = sorted(set((e['f'], e['fs']) for e in L))
    juge('« %s » : %s %s pt sur toutes ses pages (%s)' % (role, f, fs, ', '.join(pages) or 'aucune'), L and all(e['f'] == f and abs(e['fs'] - fs) <= 0.2 for e in L), tailles)
manque = [r for r in ('prénom', 'parole', 'trait', 'fin', 'guide') if not any(e['page'] == r for e in vus)]
juge('les cinq pages ont été lues (prénom, parole, trait, fin, guide)', not manque, manque)
n = sum(res); print('\n%d / %d' % (n, len(res))); sys.exit(0 if n == len(res) else 1)
