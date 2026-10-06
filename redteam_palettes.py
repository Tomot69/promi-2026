#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redteam_palettes.py — v133 (C-057) : LE MENU DES PALETTES DU STUDIO.
Tom (5 oct. 2026) : « Le menu des palettes du Studio bugue. Juge : il ouvre le menu des palettes, les fait toutes défiler et les choisit
une à une, dans les deux thèmes. » + « Primesautier passe en premier dans la liste des palettes. L'ordre des autres est inchangé. »
AU VRAI DOIGT (contexte tactile), deux thèmes, DEUX ouvertures du Studio (§8 : `#studioScreen` ne perd jamais `.show`).
Après CHAQUE toucher d'une pastille, lu à l'écran :
  · le menu est toujours ouvert, à sa place, et il porte UNE rangée de 24 pastilles, toutes dans le panneau, sans recouvrement ;
  · la palette du moteur est celle de la pastille touchée ; le nom affiché est le sien ; elle seule est marquée choisie ;
  · chaque pastille est sous le doigt à son centre ;
  · la Toile du Studio a changé de couleurs (sauf si la palette était déjà la bonne).
Valeurs EN DUR : 24 palettes, quatre rangées de six (23 sept.) ; la première est Primesautier, les 23 autres dans l'ordre d'avant (ORDRE).
Usage : python3 redteam_palettes.py [fichier.html]"""
import sys
from playwright.sync_api import sync_playwright
F=[a for a in sys.argv[1:] if not a.startswith('--')]; F=F[0] if F else 'app.html'
ORDRE=['primesautier', 'signal', 'candide', 'gouailleur', 'alangui', 'irascible', 'hurluberlu', 'beat', 'minaudier', 'chafouin', 'frivole', 'cajoleur', 'allegre', 'lunatique', 'flegmatique', 'narquois', 'truculent', 'petulant', 'fantasque', 'fielleux', 'sibyllin', 'veneneux', 'atrabilaire', 'taciturne']   # en dur : l'ordre d'avant v133, Primesautier remonté en tête
R=[]
def ok(nom, cond, detail=''):
    R.append((nom,bool(cond))); print(('  ✅ ' if cond else '  ❌ ')+nom+((' — '+str(detail)[:330]) if (detail!='' and not cond) else ''))
ETAT=r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(), k=dv.width/390, sc=document.getElementById('studioScreen'), P=document.getElementById('stpPals'); if(!P) return null;
  const r=P.getBoundingClientRect(), cs=getComputedStyle(P); const rangs=[...P.querySelectorAll('.st3-pals')].filter(e=>e.getBoundingClientRect().height>0);
  const O=[...P.querySelectorAll('.st3-pals > *')].filter(e=>e.getBoundingClientRect().width>0).map(e=>{ const q=e.getBoundingClientRect(), h=document.elementFromPoint(q.left+q.width/2,q.top+q.height/2);
    return {cle:e.getAttribute('data-pal')||e.getAttribute('data-k')||e.getAttribute('data-p')||'', x:(q.left-dv.left)/k, y:(q.top-dv.top)/k, w:q.width/k, h:q.height/k, sous:!!(h&&(h===e||e.contains(h))), on:/\bon\b|\bsel\b|\bactive\b/.test(e.className)||e.getAttribute('aria-pressed')==='true'||e.getAttribute('aria-checked')==='true', cls:e.className, titre:e.getAttribute('title')||e.getAttribute('aria-label')||''}; });
  const bt=(e)=>{ if(!e) return null; const q=e.getBoundingClientRect(); return [(q.top-dv.top)/k,(q.bottom-dv.top)/k]; };
  const noms=[...document.querySelectorAll('#st3pn')], nomVu=noms.filter(e=>e.getBoundingClientRect().height>0);
  return {nNoms:noms.length, yNom:bt(nomVu[0]), yGrille:bt(rangs[0]), yJauge:bt([...P.querySelectorAll('.st3-spec')].filter(e=>e.getBoundingClientRect().height>0)[0]), nJauges:P.querySelectorAll('.st3-spec').length,
    ouvert:sc.classList.contains('stp-pals')&&cs.display!=='none', panneau:[(r.left-dv.left)/k,(r.top-dv.top)/k,r.width/k,r.height/k], rangs:rangs.length, O:O, nom:(document.getElementById('st3pn')||{textContent:''}).textContent.trim(), pal:Toile.getPalette(), noms:(()=>{try{const p=Toile.palettes(); const o={}; Object.keys(p).forEach(k=>o[k]=p[k].name||p[k].nom||k); return o;}catch(e){return {}}})(), cles:Object.keys(Toile.palettes())}; }"""
SIG=r"""()=>{ const c=document.getElementById('stBg'); if(!c) return ''; try{ const g=c.getContext('2d'), d=g.getImageData(0,0,c.width,c.height).data; let s=[0,0,0], n=0; for(let i=0;i<d.length;i+=4*97){ s[0]+=d[i]; s[1]+=d[i+1]; s[2]+=d[i+2]; n++; } return s.map(v=>Math.round(v/n)).join(','); }catch(e){ return 'x'; } }"""
with sync_playwright() as p:
    b=p.webkit.launch()
    for th in ('dark','light'):
        ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
        pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto('http://127.0.0.1:8752/'+F); pg.wait_for_timeout(6500)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t); try{setPremium(true)}catch(e){} }", th); pg.wait_for_timeout(600)
        for tour in (1,2):
            tag='[%s · ouverture %d]'%(th,tour)
            pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(2600)
            c=pg.evaluate("()=>{const t=[...document.querySelectorAll('#studioScreen .stp-ton')].filter(e=>e.getBoundingClientRect().width>0)[0]; if(!t) return null; const r=t.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}")
            if c: pg.touchscreen.tap(*c); pg.wait_for_timeout(1200)
            e=pg.evaluate(ETAT)
            ok(tag+' toucher une teinte ouvre le menu des palettes', bool(e) and e['ouvert'], e and e['ouvert'])
            if not e or not e['O']: continue
            n=len(e['O']); ok(tag+' une seule rangée, 24 pastilles, quatre rangées de six', e['rangs']==1 and n==24 and len(set(round(o['y']) for o in e['O']))==4 and len(set(round(o['x']) for o in e['O']))==6, (e['rangs'], n))
            # ⚑ la forme du défaut vu par Tom (v133) : à la DEUXIÈME ouverture, le nom de la palette passait AU-DESSUS de la grille, qui descendait sur la jauge
            ok(tag+' un seul nom de palette dans le document, une seule jauge', e['nNoms']==1 and e['nJauges']==1, (e['nNoms'], e['nJauges']))
            ok(tag+' dans l\'ordre : la grille, puis le nom, puis la jauge — sans recouvrement', bool(e['yGrille'] and e['yNom'] and e['yJauge']) and e['yGrille'][1]<=e['yNom'][0]+0.5 and e['yNom'][1]<=e['yJauge'][0]+0.5 and max(o['y']+o['h'] for o in e['O'])<=e['yJauge'][0]+0.5, (e['yGrille'], e['yNom'], e['yJauge']))
            ok(tag+' l\'ordre des pastilles : Primesautier, puis les 23 autres dans l\'ordre d\'avant', [o['cle'] for o in e['O']]==ORDRE, [o['cle'] for o in e['O']])
            ko=[]; chang=0; pan0=e['panneau']
            for i in range(n):
                o=e['O'][i]; s0=pg.evaluate(SIG); p0=e['pal']
                pg.touchscreen.tap(dv:=0 or (20+o['x']+o['w']/2), 44+o['y']+o['h']/2) if False else pg.touchscreen.tap(*pg.evaluate("(i)=>{const e=[...document.querySelectorAll('#stpPals .st3-pals > *')].filter(e=>e.getBoundingClientRect().width>0)[i]; const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2]}", i))
                pg.wait_for_timeout(650)
                e=pg.evaluate(ETAT)
                if not e: ko.append((i,'plus de menu')); break
                pb=[]
                if not e['ouvert']: pb.append('menu fermé')
                if [round(v) for v in e['panneau']]!=[round(v) for v in pan0]: pb.append('panneau déplacé %s'%[round(v) for v in e['panneau']])
                if e['rangs']!=1 or len(e['O'])!=24: pb.append('%d rangée(s), %d pastilles'%(e['rangs'],len(e['O'])))
                else:
                    P=e['panneau']
                    if any(q['x']<P[0]-0.5 or q['y']<P[1]-0.5 or q['x']+q['w']>P[0]+P[2]+0.5 or q['y']+q['h']>P[1]+P[3]+0.5 for q in e['O']): pb.append('pastille hors du panneau')
                    if not all(q['sous'] for q in e['O']): pb.append('pastille recouverte : %s'%[j for j,q in enumerate(e['O']) if not q['sous']][:4])
                    ons=[j for j,q in enumerate(e['O']) if q['on']]
                    if ons!=[i]: pb.append('marquée choisie : %s (attendu %d)'%(ons,i))
                    cle=e['O'][i]['cle']
                    if cle and e['pal']!=cle: pb.append('moteur sur « %s », touchée « %s »'%(e['pal'],cle))
                    att=(e['noms'].get(e['pal'],'') or '').upper()
                    if att and e['nom'].upper()!=att: pb.append('nom affiché « %s », attendu « %s »'%(e['nom'],att))
                if e['pal']!=p0:
                    chang+=1
                    if pg.evaluate(SIG)==s0: pb.append('la Toile du Studio n\'a pas changé')
                if pb: ko.append((i, pb))
            ok(tag+' les 24 palettes choisies une à une : le menu reste juste à chaque toucher', not ko, ko[:4])
            ok(tag+' chaque toucher a changé la palette du moteur (%d changements)'%chang, chang>=22, chang)
            if tour==1:
                premiere=(e['O'][0]['cle'] if e else '')
                nom1=pg.evaluate("()=>{ const e=[...document.querySelectorAll('#stpPals .st3-pals > *')][0]; e.click(); return (document.getElementById('st3pn')||{textContent:''}).textContent.trim() }")
                ok(tag+' la première palette de la liste est Primesautier', nom1.upper()=='PRIMESAUTIER', nom1)
            pg.evaluate("()=>{ const x=document.querySelector('#studioScreen .closeb'); if(x) x.click(); }"); pg.wait_for_timeout(900)
        ok('[%s] aucune erreur de page'%th, not errs, errs[:2]); ctx.close()
    b.close()
n=sum(1 for _,c in R if c); print('\nredteam_palettes : %d/%d'%(n,len(R)))
for nom,c in R:
    if not c: print('   ROUGE :', nom)
sys.exit(0 if n==len(R) else 1)
