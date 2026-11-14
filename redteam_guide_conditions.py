"""⚑ v203 (Tom, C-277 ; fin de v203) — L'ÉTAPE OBLIGATOIRE (LE STUDIO) A SA CONDITION, ET JAMAIS UN TOUCHER AU HASARD NE LA VALIDE ; LE + ET PARTAGER RESTENT FACULTATIFS.
« Si la condition est déjà remplie quand l'étape devrait apparaître, l'étape ne s'affiche pas : le guide passe en douceur à l'étape suivante. » — pour le Studio seul.
« Partager reste facultatif » (Tom, fin de v203, qui rétablit v166) : à l'étape du + comme à celle de Partager, toucher ailleurs fait avancer (v165 : le + → Partager,
Partager → la phrase 2) ; ces étapes paraissent même si leur action a été faite avant.
WebKit, 390 × 844 ×3, au doigt (banc_tom), stockage d'un parcours fini (onboarding fait, guide jamais vu) ; le guide est demandé comme à la fin de l'onboarding
(`_guide.attend(false)`). Une sonde relève chaque image : l'étape (`data-guide`) et la phrase affichée.
  A · AVANT : le Studio ouvert (une palette changée) et refermé avant que le guide paraisse → la phrase du Studio ne paraît jamais ; le guide commence au +
      puis un toucher ailleurs au + → Partager ; un toucher ailleurs à Partager → la phrase 2 (v165, v166)
  B · AVANT, le + aussi (touché, le menu refermé) → le guide commence au + (facultatif : il paraît) ; tout fait → le guide commence au +
  C · PENDANT : le Studio touché pendant que le flou monte → le Studio s'ouvre ; refermé, le +, jamais la phrase du Studio après
  D · APRÈS : trois touchers au hasard à l'étape du Studio → elle reste, sa phrase redite (rappel) ; seule sa cible la fait passer
  E · le + touché avant le guide : l'étape du Studio, puis celle du + (facultative : elle paraît)
--seul=A,B,… · --sombre"""
import sys, os, time, json; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright

A = sys.argv[1:]
SEUL = next((a.split('=', 1)[1].split(',') for a in A if a.startswith('--seul=')), None)
F = next((a.split('=', 1)[1] for a in A if a.startswith('--fichier=')), 'app.html')
PH = {'studio': 'Choisis d’abord le monde qui te ressemble, au Studio.', 'plus': 'Promi, Chiche ou Cercle : tout commence par ce +.',
      'partage': 'Étoffe ta Toile, et partage-la !', 'reste': 'Le reste s’explore à ton rythme !'}
def norm(s): return ' '.join((s or '').replace(chr(0xa0), ' ').replace(chr(0x202f), ' ').replace('A' + chr(0x2019), 'à').replace('À', 'à').split())   # PromiLate n'a pas de « À » : composé (Q587)
QUEL = {norm(v): k for k, v in PH.items()}
SONDE = r"""(function(){ window.__o=[]; var der=''; (function f(){ try{ var g=document.getElementById('guide'), p=document.getElementById('guidePhrase'), s=(g?g.getAttribute('data-guide')||g.getAttribute('data-etape'):'-')+'|'+(p?p.textContent:'');
  if(s!==der){ der=s; window.__o.push([Math.round(performance.now()), g?(g.getAttribute('data-guide')||''):null, p?p.textContent:null]); } }catch(e){} requestAnimationFrame(f); })(); })();"""
ETAT = """()=>{ const g=document.getElementById('guide'), p=document.getElementById('guidePhrase'), st=document.getElementById('studioScreen'), sh=document.getElementById('shareScreen'), ch=document.getElementById('accChoix');
  const vis=e=>{ if(!e) return false; const r=e.getBoundingClientRect(), D=document.getElementById('device').getBoundingClientRect(); const c=getComputedStyle(e); return c.display!=='none' && c.visibility!=='hidden' && r.bottom>D.top+50 && r.top<D.bottom-50 && r.width>50; };
  return {guide:g?g.getAttribute('data-guide'):null, etape:g?g.getAttribute('data-etape'):null, saute:g?g.getAttribute('data-saute'):null, entier:!!(g&&g.getAttribute('data-entier')), phrase:p?p.textContent:null,
    rappels:g?+(g.getAttribute('data-rappels')||0):0, net:(window._guide?window._guide.etat().net:0), etat:(window._guide?window._guide.etat().etat:null),
    studio:!!(st&&st.classList.contains('show')&&vis(st)), partage:!!(sh&&sh.classList.contains('show')&&vis(sh)), choix:!!(ch&&ch.classList.contains('ouvert')), fait:(window._guideFait?_guideFait():{}), vu:localStorage.getItem('promi_guide') }; }"""
RES = []
def juge(nom, ok, d=''):
    RES.append(bool(ok)); print(('✅' if ok else '❌'), nom, ('— ' + str(d)) if d else '', flush=True)
def etat(pg): return pg.evaluate(ETAT)
def attend(pg, f, maxi=12000, pas=80):
    t0 = time.time()
    while (time.time() - t0) * 1000 < maxi:
        e = etat(pg)
        if f(e): return e
        pg.wait_for_timeout(pas)
    return etat(pg)
def pose(e, q): return e['guide'] == q and e['entier'] and e['net'] >= 0.99
def phrases(pg):
    o = pg.evaluate("()=>window.__o"); return [QUEL.get(norm(x[2]), '?' if x[2] else None) for x in o]
def ailleurs(pg, n=3):
    """trois touchers au hasard : la Toile (deux points) et le haut du plateau, loin de toute cible"""
    P = [(200, 380), (110, 560), (300, 250), (180, 470)]
    for i in range(n): B.tap(pg, *P[i % len(P)]); pg.wait_for_timeout(900)
def ferme_studio(pg):
    B.tap_sel(pg, '#studioScreen .closeb'); pg.wait_for_timeout(1400)
def ferme_partage(pg):
    B.tap_sel(pg, '#shareScreen .closeb'); pg.wait_for_timeout(1400)
def ouvre(b, sombre):
    ctx = B.contexte(b, sombre=sombre, guide=False); B.toile_pleine(ctx, 10); ctx.add_init_script(SONDE)
    pg = B.ouvre(ctx, F); pg.evaluate("()=>{ try{ closeAll(); }catch(e){} localStorage.removeItem('promi_guide'); }"); pg.wait_for_timeout(600)
    return ctx, pg
def lance(pg): pg.evaluate("()=>{ window.__o=[]; if(window._guide) _guide.attend(false); }")

def passe(b, sombre):
    T = 'sombre' if sombre else 'clair'
    if not SEUL or 'A' in SEUL:
        ctx, pg = ouvre(b, sombre); lance(pg); pg.wait_for_timeout(120)
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(1800)
        pg.evaluate("()=>{ try{ const P=Toile.palettes(), k=Object.keys(P); Toile.setPalette(k[3]); if(window.onPaletteChange) onPaletteChange(); }catch(e){} }"); pg.wait_for_timeout(600)
        ferme_studio(pg)
        e = attend(pg, lambda e: pose(e, 'plus') or pose(e, 'studio'), 15000)
        ph = phrases(pg)
        juge('[%s] A · le Studio ouvert AVANT le guide : le guide commence au +, la phrase du Studio ne paraît jamais' % T, e['guide'] == 'plus' and 'studio' not in ph and norm(e['phrase']) == norm(PH['plus']),
             'étape %s · phrases vues %s · saut %s' % (e['guide'], [x for x in ph if x], e['saute']))
        if e['guide'] == 'plus':
            B.tap(pg, 200, 380); e = attend(pg, lambda e: pose(e, 'partage'), 8000)
            juge('[%s] A · un toucher ailleurs à l\'étape du + (facultative) : Partager' % T, e['guide'] == 'partage' and norm(e['phrase']) == norm(PH['partage']), 'étape %s · « %s »' % (e['guide'], e['phrase']))
            if e['guide'] == 'partage':
                B.tap(pg, 200, 380); e = attend(pg, lambda e: e['guide'] == 'reste' and norm(e['phrase']) == norm(PH['reste']), 8000)
                juge('[%s] A · un toucher ailleurs à l\'étape de Partager (facultative) : la phrase 2' % T, e['guide'] == 'reste' and norm(e['phrase']) == norm(PH['reste']), 'étape %s · « %s »' % (e['guide'], e['phrase']))
        ctx.close()
    if not SEUL or 'B' in SEUL:
        ctx, pg = ouvre(b, sombre)   # les actions faites, PUIS le guide demandé (la fin de l'onboarding) : rien entre elles ne le lance
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(1500); ferme_studio(pg)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(900); B.tap(pg, 200, 330); pg.wait_for_timeout(900); lance(pg)
        e = attend(pg, lambda e: pose(e, 'partage') or pose(e, 'plus') or pose(e, 'studio'), 15000); ph = phrases(pg)
        juge('[%s] B · le Studio et le + faits AVANT : le guide commence au + (facultatif, il paraît), jamais au Studio' % T, e['guide'] == 'plus' and 'studio' not in ph, 'étape %s · phrases %s' % (e['guide'], [x for x in ph if x]))
        ctx.close()
        ctx, pg = ouvre(b, sombre)
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(1500); ferme_studio(pg)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(900); B.tap(pg, 200, 330); pg.wait_for_timeout(900)
        B.tap_sel(pg, '#shareBtn'); pg.wait_for_timeout(1600); ferme_partage(pg); lance(pg)
        e = attend(pg, lambda e: (e['guide'] == 'reste' and norm(e['phrase']) == norm(PH['reste'])) or pose(e, 'partage') or pose(e, 'plus') or pose(e, 'studio'), 15000); ph = phrases(pg)
        juge('[%s] B · tout fait AVANT : le guide commence au +, jamais au Studio' % T, e['guide'] == 'plus' and 'studio' not in ph, 'étape %s · phrases %s' % (e['guide'], [x for x in ph if x]))
        ctx.close()
    if not SEUL or 'C' in SEUL:
        ctx, pg = ouvre(b, sombre); lance(pg)
        e = attend(pg, lambda e: e['guide'] == 'couvre' or e['etat'] == 'couvre', 9000)
        pg.wait_for_timeout(250); B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(1600); e1 = etat(pg)
        ferme_studio(pg)
        e = attend(pg, lambda e: pose(e, 'plus'), 9000); ph = phrases(pg)
        juge('[%s] C · le Studio touché PENDANT que le flou monte : il s\'ouvre ; refermé, le + — la phrase du Studio jamais' % T, e1['studio'] and e['guide'] == 'plus' and 'studio' not in ph,
             'Studio ouvert %s (état %s) · étape %s · phrases %s' % (e1['studio'], e['etat'], e['guide'], [x for x in ph if x]))
        ctx.close()
    if not SEUL or 'D' in SEUL:
        ctx, pg = ouvre(b, sombre); lance(pg)
        e = attend(pg, lambda e: pose(e, 'studio'), 12000)
        ailleurs(pg); e = etat(pg)
        juge('[%s] D · trois touchers au hasard à l\'étape du Studio : elle reste, sa phrase redite' % T, e['guide'] == 'studio' and e['rappels'] >= 1 and norm(e['phrase']) == norm(PH['studio']) and not e['studio'],
             'étape %s · rappels %s · « %s »' % (e['guide'], e['rappels'], e['phrase']))
        ph0 = len(pg.evaluate("()=>window.__o"))
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(1600); e1 = etat(pg); ferme_studio(pg)
        e = attend(pg, lambda e: pose(e, 'plus'), 9000)
        juge('[%s] D · le Studio touché par sa zone : il s\'ouvre ; refermé, le +' % T, e1['studio'] and e['guide'] == 'plus', 'Studio %s · étape %s' % (e1['studio'], e['guide']))
        ctx.close()
    if not SEUL or 'E' in SEUL:
        ctx, pg = ouvre(b, sombre); lance(pg); pg.wait_for_timeout(100)
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(900); B.tap(pg, 200, 330); pg.wait_for_timeout(900)
        e = attend(pg, lambda e: pose(e, 'studio') or pose(e, 'plus'), 15000)
        ok0 = e['guide'] == 'studio'
        B.tap_sel(pg, '#studioBtn'); pg.wait_for_timeout(1600); ferme_studio(pg)
        e = attend(pg, lambda e: pose(e, 'partage') or pose(e, 'plus'), 9000); ph = phrases(pg)
        juge('[%s] E · le + touché avant le guide : l\'étape du Studio, puis celle du + (facultative, elle paraît)' % T, ok0 and e['guide'] == 'plus', 'étape %s · phrases %s' % (e['guide'], [x for x in ph if x]))
        ctx.close()

with sync_playwright() as p:
    b = p.webkit.launch()
    passe(b, '--sombre' in A)
    b.close()
print('%d/%d' % (sum(RES), len(RES)))
