#!/usr/bin/env python3
"""redteam_parole_longue.py — ⚑ v160 (Tom, C-180) : LA PAROLE LONGUE DANS L'ONBOARDING, MISE EN PAGE.

« Pendant l'écriture, à la 3e ligne, la 2e ligne devient très courte et la 3e, pleine, sort de l'écran à droite ; en touchant ailleurs avant de valider,
la 1re ligne devient courte, la 2e sort à droite, et la suite disparaît. » Attendu : un cadre de largeur fixe (la colonne de texte de la page) ; coupe aux
espaces, chaque ligne remplie au maximum, seule la dernière peut être courte ; aucun caractère hors du cadre, jamais ; la même mise en page clavier ouvert
et clavier fermé ; au-delà de trois lignes, la taille descend par paliers (35 → 22 px), la coupe recalculée ; « Petite ou grande promesse, elle compte. »
reste ; rien sur le trait ; le → garde sa place libre ; un mot plus long que la largeur coupé à la largeur, jamais caché.

Banc comme Tom (WebKit, ×3, doigt, le clavier d'iOS simulé : visualViewport descend de 336 pt au focus), stockage vierge, le vrai parcours (prénom,
puis la phrase touchée), saisie CARACTÈRE PAR CARACTÈRE ; échelles 1 (430 × 932) et 0,79 (330 × 714) ; clair et sombre. Textes : 1 à 6 lignes À 35 px, un mot de 40
lettres, et (v160c, Q576 : le champ n'a plus de limite) deux paroles de 260 et 500 caractères — à 22 px, au-delà de la place, la COUPE PROPRE :
« Je me promets de … » puis la fin exacte de la parole ; le champ garde la parole entière. Après chaque espace et à la fin (clavier ouvert), puis après un toucher ailleurs (clavier fermé) :
  A · chaque glyphe et chaque pastille dans le cadre (24 → 366 pt) et dans l'écran ;
  B · aucune ligne plus large que le cadre ;
  C · aucune ligne, sauf la dernière, sous 70 % de la largeur quand le premier mot de la ligne suivante tenait ;
  D · la coupe identique clavier ouvert et clavier fermé (les mêmes mots sur les mêmes lignes, la même taille) ;
  E · aucun recouvrement (la phrase, « Petite ou grande promesse », la consigne, le trait, le →) ; « Petite ou grande promesse » est là ;
  F · le texte affiché est celui qui a été tapé, en entier ;
  G · au-delà de trois lignes à 35 px, la taille est descendue (jamais sous 22 px).
Preuve : `--fichier=zz-v159.html` rougit.
"""
import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
F = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fichier=')), 'app.html')
VITE = '--vite' in sys.argv
res = []
def juge(nom, ok, d=''):
    res.append(bool(ok)); print('  %s %-96s %s' % ('✅' if ok else '❌', nom, str(d)[:260]), flush=True)
CLAVIER = open('redteam_suite_libelle.py', encoding='utf-8').read().split('CLAVIER = """')[1].split('"""')[0]
TEXTES = [('une ligne', 'marcher une heure'),
          ('deux lignes', 'appeler ma grand-mère chaque dimanche'),
          ('trois lignes', 'appeler ma grand-mère chaque dimanche avant le déjeuner'),
          ('quatre lignes', 'appeler ma grand-mère chaque dimanche avant le déjeuner sans faute et lui dire'),
          ('cinq lignes', 'appeler ma grand-mère chaque dimanche et lui raconter ma semaine en entier'),
          ('six lignes', 'lire un vrai livre par mois et en parler à table avec les enfants le soir au lit'),
          ('mot de 40 lettres', 'relire anticonstitutionnellementdeboutpourtoujours ensemble'),
          ('260 caractères', 'appeler ma grand-mère chaque dimanche avant le déjeuner sans faute, lui raconter ma semaine en entier avec les enfants, le chien, le jardin, les voisins, et ne jamais raccrocher avant qu’elle ait fini de me parler de ses tomates et de ses roses'),
          ('500 caractères', ' '.join(['marcher une heure chaque matin au bord de la rivière, sans téléphone, en regardant les arbres changer avec les saisons et en notant une phrase par jour'] * 3))]
MESURE = """()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, X0=24, X1=366; const ph=document.getElementById('onbPh');
  const cs=getComputedStyle(ph), lh=parseFloat(cs.lineHeight)*1, fs=parseFloat(cs.fontSize);
  const R=[]; const tw=document.createTreeWalker(ph, NodeFilter.SHOW_TEXT); let n; while((n=tw.nextNode())){ const t=n.nodeValue; if(!t || !t.trim()) continue;
    const el=n.parentElement; if(el && getComputedStyle(el).visibility==='hidden') continue; const rg=document.createRange();
    for(let i=0;i<t.length;i++){ if(/\\s/.test(t[i])) continue; rg.setStart(n,i); rg.setEnd(n,i+1); const q=rg.getBoundingClientRect(); if(q.width<0.1) continue;
      R.push({c:t[i], x0:(q.left-D.left)/k, x1:(q.right-D.left)/k, y0:(q.top-D.top)/k, y1:(q.bottom-D.top)/k}); } }
  const P=[...ph.querySelectorAll('.onbv-pm,.onbv-pb')].flatMap(e=>[...e.getClientRects()].map(q=>({x0:(q.left-D.left)/k, x1:(q.right-D.left)/k, y0:(q.top-D.top)/k, y1:(q.bottom-D.top)/k})));
  /* les lignes : glyphes regroupés par leur centre vertical */
  R.sort((a,b)=>(a.y0+a.y1)-(b.y0+b.y1)); const L=[]; R.forEach(g=>{ const c=(g.y0+g.y1)/2, l=L.find(l=>Math.abs(l.c-c)<fs*0.6); if(l){ l.g.push(g); } else L.push({c:c, g:[g]}); });
  L.sort((a,b)=>a.c-b.c); L.forEach(l=>l.g.sort((a,b)=>a.x0-b.x0));
  const lignes=L.map(l=>{ let s='', av=null; l.g.forEach(g=>{ if(av && g.x0-av.x1 > fs*0.18) s+=' '; s+=g.c; av=g; });
    const pills=P.filter(p=>Math.abs((p.y0+p.y1)/2-l.c)<fs*0.8); const x0=Math.min(l.g[0].x0, ...pills.map(p=>p.x0)), x1=Math.max(l.g[l.g.length-1].x1, ...pills.map(p=>p.x1));
    return {texte:s, x0:x0, x1:x1, y0:Math.min(...l.g.map(g=>g.y0)), y1:Math.max(...l.g.map(g=>g.y1))}; });
  const hors=R.filter(g=>g.x0<X0-0.6||g.x1>X1+0.6||g.x1>390||g.x0<0).map(g=>g.c).join('')+'|'+P.filter(p=>p.x0<X0-0.6||p.x1>X1+0.6).length;
  /* le premier mot de la ligne suivante tenait-il ? */
  const esp=fs*0.24; const courtes=[]; lignes.forEach((l,i)=>{ if(i===lignes.length-1) return; const w=(lignes[i+1].texte.split(' ')[0]||''); const g=L[i+1].g, n0=w.length;
    const lw=n0?(g[n0-1].x1-g[0].x0):0; const fill=(l.x1-X0)/(X1-X0); if(fill<0.7 && l.x1+esp+lw+(i===0?24:0)<=X1) courtes.push(i+1+' ('+Math.round(fill*100)+' %, « '+w+' » tenait)'); });
  const rect=id=>{ const e=document.getElementById(id); if(!e||getComputedStyle(e).display==='none'||getComputedStyle(e).visibility==='hidden') return null; const q=e.getBoundingClientRect(); if(q.width<1) return null; return [(q.left-D.left)/k,(q.top-D.top)/k,(q.right-D.left)/k,(q.bottom-D.top)/k,id]; };
  const encre=id=>{ const e=document.getElementById(id); if(!e||getComputedStyle(e).display==='none') return null; const rg=document.createRange(); rg.selectNodeContents(e); const q=rg.getBoundingClientRect(); if(q.width<1) return null; return [(q.left-D.left)/k,(q.top-D.top)/k,(q.right-D.left)/k,(q.bottom-D.top)/k,id]; };
  const autres=[encre('onbSous'), encre('onbTrace'), rect('onbTrait'), rect('onbSuite')].filter(Boolean);
  const rec=[]; lignes.forEach(l=>autres.forEach(o=>{ if(o[4]==='onbTrait'){ if(l.y1>o[1]+8) rec.push('phrase/trait'); return; } if(l.x1>o[0] && l.x0<o[2] && l.y1>o[1] && l.y0<o[3]) rec.push('phrase/'+o[4]); }));
  const so=encre('onbSous'), tt=encre('onbTrace'); if(so && tt && so[3]>tt[1]) rec.push('Petite…/consigne');
  return {fs:fs, lignes:lignes.map(l=>l.texte), larg:lignes.map(l=>Math.round(l.x1-l.x0)), droite:lignes.map(l=>Math.round(l.x1)), hors:hors, courtes:courtes, rec:rec, sous:!!so,
    tape:(document.getElementById('onbIn')||{}).value||''}; }"""
def verifie(T, m, texte, etiquette):
    ok = True; d = []
    if m['hors'] != '|0': ok = False; d.append('hors du cadre : %s' % m['hors'])
    if any(w > 342.6 for w in m['larg']): ok = False; d.append('ligne plus large que le cadre %s' % m['larg'])
    if m['courtes']: ok = False; d.append('lignes courtes %s' % m['courtes'])
    if m['rec'] or not m['sous']: ok = False; d.append('recouvrement %s · Petite… %s' % (m['rec'], m['sous']))
    vu = ''.join(m['lignes']).replace(' ', ''); ecrit = (m['tape'] or texte).replace(' ', '')
    if m['tape'].rstrip() != texte.rstrip(): ok = False; d.append('le champ n\'a pas gardé la parole entière (%d car. sur %d)' % (len(m['tape']), len(texte)))
    if '…' in vu:   # ⚑ v160c (C-180, Q576) : au-delà de la place, la coupe propre — « Je me promets de … » puis la FIN exacte de la parole
        fin = vu.split('…', 1)[1]
        if not fin or not ecrit.endswith(fin): ok = False; d.append('coupe : la fin affichée n\'est pas la fin de la parole : %s' % m['lignes'][-2:])
    elif ecrit not in vu: ok = False; d.append('texte incomplet : %s' % m['lignes'])
    return ok, d
with sync_playwright() as p:
    b = p.webkit.launch()
    for vw, vh in ((430, 932), (330, 714)):
        for sombre in ((False,) if VITE else (False, True)):
            for nom, texte in TEXTES:
                T = '%s · %s · %s' % ('échelle 1' if vw == 430 else 'échelle 0,79', 'sombre' if sombre else 'clair', nom)
                ctx = B.contexte(b, sombre=sombre, onb=False, guide=False, vw=vw, vh=vh); ctx.add_init_script(CLAVIER); pg = B.ouvre(ctx, F, attente=7000)
                B.tap_sel(pg, '#onbPh'); pg.wait_for_timeout(600); pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5600)
                B.attend_parole(pg); B.tap_sel(pg, '[data-onb="parole"]'); pg.wait_for_timeout(700)
                pires = []; tous = True
                for i, ch in enumerate(texte):
                    pg.keyboard.type(ch); pg.wait_for_timeout(25)
                    if ch == ' ' or i == len(texte) - 1 or (i % 9 == 4):
                        m = pg.evaluate(MESURE); ok, d = verifie(T, m, texte[:i + 1].rstrip(), 'ouvert')
                        if not ok: tous = False; pires.append('%d car. : %s' % (i + 1, '; '.join(d)))
                ouvert = pg.evaluate(MESURE)
                juge('[%s] A–C, E, F · pendant la saisie, clavier ouvert (à chaque espace) : dans le cadre, lignes pleines, rien recouvert' % T, tous, pires[:2])
                pg.evaluate("()=>{ const i=document.getElementById('onbIn'); if(i) i.blur(); }"); pg.wait_for_timeout(1300)
                ferme = pg.evaluate(MESURE); ok, d = verifie(T, ferme, texte, 'fermé')
                juge('[%s] A–C, E, F · après un toucher ailleurs, clavier fermé' % T, ok, '; '.join(d) + ' · %s' % ferme['lignes'])
                juge('[%s] D · la même coupe et la même taille clavier ouvert et fermé' % T, ouvert['lignes'] == ferme['lignes'] and ouvert['fs'] == ferme['fs'],
                     'ouvert %s @%s · fermé %s @%s' % (ouvert['lignes'], ouvert['fs'], ferme['lignes'], ferme['fs']))
                n = len(ferme['lignes'])
                juge('[%s] G · la taille : 35 px tant que trois lignes suffisent, plus petite au-delà, jamais sous 22' % T, ferme['fs'] >= 22 and (n <= 3 or ferme['fs'] < 35),
                     '%d lignes à %s px' % (n, ferme['fs']))
                er = [e for e in pg.erreurs if 'version.json' not in e]
                if er: juge('[%s] aucune erreur de page' % T, False, er[:2])
                ctx.close()
    b.close()
ok = sum(res); print('\n  %s  %d / %d' % ('✅' if ok == len(res) else '❌', ok, len(res)))
sys.exit(0 if ok == len(res) else 1)
