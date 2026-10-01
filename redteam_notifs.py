#!/usr/bin/env python3
"""
redteam_notifs.py — LES NOTIFICATIONS (Tom, 30 sept. 2026, v109). WebKit, deux thèmes.

Décisions, écrites EN DUR ici (§7 : le juge porte la décision, l'app la respecte) :
  1 · JAMAIS AU LANCEMENT : aucune demande de permission au chargement ni en ouvrant les écrans
  2 · « Je te le rappelle ? » paraît à la plantation d'une parole DATÉE — et la permission n'est demandée qu'après « oui »
  3 · rien pour une parole EN L'AIR
  4 · deux « pas besoin » d'affilée, puis on n'insiste plus (et toujours aucune demande)
  5 · RIEN QUAND LA DATE EST PASSÉE — ni dans le plan, ni à l'envoi (« le point le plus important »)
  6 · les mots, au caractère près
  7 · une notification par jour au plus
  8 · la page : trois lignes + l'heure ; « en l'air » et « l'heure » sont un mur de Ma Parole ! (flou 4,8 px, la phrase monte) ;
      payé : la mémoire se règle et l'heure change ; « Ce qu'on me lance » attend Firebase
  9 · plus de « Rappels activés ✓ » : activer n'envoie rien
La permission est simulée (WebKit n'a pas d'API Notification hors écran d'accueil) : on compte les DEMANDES et les ENVOIS.
"""
import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8752/app.html'
MOTS = {
    'veille_soi':    ('Promi', 'Demain, c’est « lire au soleil ».'),
    'veille_autre':  ('« rendre le livre »', 'Tu as promis ça à Nico. Demain.'),
    'veille_chiche': ('Promi', 'Ton Chiche à Marion arrive demain.'),
    'jour':          ('« rendre le livre »', 'C’est aujourd’hui.'),
    'lair':          ('Promi', '« apprendre la guitare » flotte toujours. Un de ces jours ?'),
}
LIGNES = ['MES PAROLES DATÉES', 'MES PAROLES EN L’AIR', 'L’HEURE', 'CE QU’ON ME LANCE']
FLOU = 'blur(4.8px)'
FAUX = ("window.__notifs=[];window.__demandes=0;window.Notification=function(t,o){window.__notifs.push([t,o&&o.body])};"
        "Notification.permission='default';Notification.requestPermission=function(){window.__demandes++;Notification.permission='granted';return Promise.resolve('granted')};")
res = []
def t(nom, ok, detail=''):
    res.append(bool(ok)); print(('  ✅ ' if ok else '  ❌ ') + nom + ('  — ' + str(detail) if detail != '' else ''))

def plante(pg, titre, qui='moi', due=3, lair=False):
    pg.evaluate("()=>{closeAll();document.getElementById('createBtn').click()}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const x=[...document.querySelectorAll('#createSheet .tile')][0];x&&x.click()}"); pg.wait_for_timeout(1400)
    pg.evaluate("a=>{document.getElementById('fTitle').value=a[0];document.getElementById('fWho').value=a[1];due=a[2];window._csEnLair=a[3];window._csDueISO=null}", [titre, qui, due, lair])
    pg.evaluate("()=>document.getElementById('addPromi').click()"); pg.wait_for_timeout(2500)
    return pg.evaluate("()=>{const q=document.getElementById('rapQuestion');return !!(q&&q.classList.contains('vu')&&getComputedStyle(q).display!=='none')}")
def etat(pg): return pg.evaluate("()=>({d:window.__demandes,n:window.__notifs.length,e:window._notifEtat?_notifEtat():{}})")

with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('dark', 'light'):
        print('\n══ %s' % th)
        ctx = b.new_context(viewport={'width': 430, 'height': 932}, device_scale_factor=1, has_touch=True)
        ctx.add_init_script("try{localStorage.setItem('promi_onb','1')}catch(e){}"); ctx.add_init_script(FAUX)
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(7000)
        try:
            pg.evaluate("t=>{setTheme(t);setPremium(false)}", th)
            # ⚠ un closeAll() par script ne referme pas les Réglages (antérieur à v109) : on ferme chaque écran par son « ✕ FERMER »
            for sc, js in [('settingsScreen', "()=>document.getElementById('settingsBtn').click()"), ('auraScreen', "()=>document.getElementById('souffleBtn').click()"), ('indexSheet', "()=>document.getElementById('indexBtn').click()")]:
                pg.evaluate(js); pg.wait_for_timeout(900)
                pg.evaluate("i=>{const c=document.querySelector('#'+i+' [data-close], #'+i+' .closeb');if(c)c.click();closeAll()}", sc); pg.wait_for_timeout(700)
            e = etat(pg)
            t('1 · au lancement et en ouvrant les écrans : aucune demande de permission', e['d'] == 0 and e['n'] == 0, e)

            q = plante(pg, 'lire au soleil', 'moi', 0 + 4)
            e = etat(pg)
            t('2a · parole datée plantée : « Je te le rappelle ? » paraît, sans demande', q and e['d'] == 0,
              pg.evaluate("()=>{const q=document.getElementById('rapQuestion');return q&&q.textContent}"))
            t('2b · ses mots', pg.evaluate("()=>{const q=document.getElementById('rapQuestion');return q?[...q.children].map(x=>x.textContent):null}") == ['Je te le rappelle ?', 'oui', 'pas besoin'])

            # 4 · deux « pas besoin » (le premier ici, le second à la parole suivante)
            pg.evaluate("()=>document.querySelector('#rapQuestion [data-r=non]').click()"); pg.wait_for_timeout(300)
            q2 = plante(pg, 'ranger la cave', 'moi', 5)
            pg.evaluate("()=>{const x=document.querySelector('#rapQuestion.vu [data-r=non]');x&&x.click()}"); pg.wait_for_timeout(300)
            q3 = plante(pg, 'réparer le vélo', 'moi', 6)
            e = etat(pg)
            t('4 · deux « pas besoin », puis on n\'insiste plus — et aucune demande', q2 and not q3 and e['d'] == 0 and e['e']['refus'] == 2, 'q2 %s · q3 %s · %s' % (q2, q3, e))

            # repartir : un « oui »
            pg.evaluate("()=>{const o=_notifEtat();o.refus=0;localStorage.setItem('promi_notifs2',JSON.stringify(o))}")
            q3 = plante(pg, 'apprendre la guitare', 'moi', None, True)
            t('3 · parole en l\'air : pas de question', not q3)
            q4 = plante(pg, 'rendre le livre', 'Nico', 2)
            pg.evaluate("()=>document.querySelector('#rapQuestion [data-r=oui]').click()"); pg.wait_for_timeout(400)
            e = etat(pg)
            t('2c · « oui » : la permission est demandée alors, une fois, et les paroles datées sont activées', q4 and e['d'] == 1 and e['e']['datees'] is True, e)
            t('9 · activer n\'envoie rien (plus de « Rappels activés ✓ »)', e['n'] == 0, e)

            # 6 · les mots, sur des paroles posées à la main (moment calculé par l'app)
            mots = pg.evaluate("""()=>{const P2=(o)=>Object.assign({id:9e6+Math.random(),status:'encours',from:'moi',draft:false,req:false},o);
              const M=_notifMots;return {veille_soi:M.veille(P2({title:'lire au soleil',who:'moi'})),veille_autre:M.veille(P2({title:'rendre le livre',who:'Nico'})),
              veille_chiche:M.veille(P2({title:'courir',who:'Marion',chiche:true})),jour:M.jour(P2({title:'rendre le livre',who:'Nico'})),lair:M.lair(P2({title:'apprendre la guitare'}))}}""")
            faux = [k for k, v in MOTS.items() if (mots[k]['titre'], mots[k]['texte']) != v]
            t('6 · les mots, au caractère près', not faux, faux or '')

            # 10 · « C'est aujourd'hui » part à l'heure choisie, comme la veille (Tom, v110) — jamais à une autre heure
            hj = pg.evaluate("""()=>{const o=_notifEtat();const J=new Date();J.setHours(0,0,0,0);J.setDate(J.getDate()+1);
              const iso=J.getFullYear()+'-'+String(J.getMonth()+1).padStart(2,'0')+'-'+String(J.getDate()).padStart(2,'0');
              const p={id:8e6,title:'le jour même',who:'moi',status:'encours',from:'moi',dueISO:iso,rap:{vu:J.getTime()-3600e3}};promises.push(p);
              const e=_notifPlan().filter(x=>x.id===8e6)[0];promises.splice(promises.indexOf(p),1);
              return e?{type:e.type,h:new Date(e.quand).getHours(),heure:o.heure}:null}""")
            t('10 · « C\'est aujourd\'hui » part à l\'heure choisie', hj and hj['type'] == 'jour' and hj['h'] == hj['heure'], hj)
            # 5 · rien quand la date est passée ; 7 · une par jour
            r = pg.evaluate("""()=>{const p=promises.find(x=>x.title==='rendre le livre'&&x.who==='Nico');const L=_notifPlan(Date.now()).filter(e=>e.id===p.id);
              if(!L.length) return {err:'pas au plan'}; const e=L[0]; const J=e.jusque; // début du jour J pour une veille
              const apres=_notifPlan(J+2*864e5).filter(x=>x.id===p.id).length;           // J+1 : la date est passée
              localStorage.removeItem('promi_notifs_log'); window.__notifs=[];
              _notifTick(J+864e5+3600e3);                                               // pendant J+… : passé → rien
              const passe=window.__notifs.length;
              _notifTick(e.quand+60e3); const un=window.__notifs.slice();                 // la veille à l'heure : UNE
              _notifTick(e.quand+120e3); const deux=window.__notifs.length;               // le même jour : pas une de plus
              return {type:e.type,apres:apres,passe:passe,un:un,deux:deux}}""")
            t('5 · date passée : rien au plan, rien envoyé', r.get('apres') == 0 and r.get('passe') == 0, r)
            t('7 · la veille, une notification ; pas une de plus le même jour', len(r.get('un', [])) == 1 and r.get('deux') == 1 and r['un'][0][1] == MOTS['veille_autre'][1], r)

            # 8 · la page
            pg.evaluate("()=>{closeAll();document.getElementById('settingsBtn').click()}"); pg.wait_for_timeout(900)
            pg.evaluate("()=>document.getElementById('notifCard').click()"); pg.wait_for_timeout(1000)
            pgi = pg.evaluate("""()=>{const s=document.getElementById('notifScreen');if(!s||!s.classList.contains('show'))return null;
              const L=[...s.querySelectorAll('.nt-row')].map(r=>r.querySelector('.nt-k').textContent.toUpperCase());
              const f=[...s.querySelectorAll('.nt-mur .nt-row')].map(r=>getComputedStyle(r).filter);
              const libre=[...s.querySelectorAll('.nt-row:not(.nt-mur .nt-row)')].map(r=>getComputedStyle(r).filter);
              const dv=document.getElementById('device').getBoundingClientRect(),r0=s.querySelector('.nt-row').getBoundingClientRect();
              return {L:L,f:f,libre:libre,x:r0.left-dv.left,w:r0.width,settings:document.getElementById('settingsScreen').classList.contains('show')}}""")
            t('8a · « Notifications › » ouvre la page : trois lignes et l\'heure, dans l\'ordre, à x 24 sur 342', pgi and pgi['L'] == LIGNES and abs(pgi['x'] - 24) < 1.5 and abs(pgi['w'] - 342) < 1.5, pgi)
            t('8b · gratuit : « en l\'air » et « l\'heure » floutés à 4,8 px, le reste net', pgi and pgi['f'] == [FLOU, FLOU] and all(x == 'none' for x in pgi['libre']), pgi and (pgi['f'], pgi['libre']))
            pg.evaluate("()=>{localStorage.setItem('promi_murs',JSON.stringify({n:3,t:Date.now(),der:2,decouvert:1}))}")
            c = pg.evaluate("()=>{const r=document.querySelector('#notifScreen .nt-mur').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")
            pg.touchscreen.tap(*c); pg.wait_for_timeout(900)
            m = pg.evaluate("()=>({leve:!!document.querySelector('#murPhrase.leve'),t:(document.getElementById('murPhrase')||{}).textContent,lair:_notifEtat().lair})")
            t('8c · toucher le mur : la phrase monte, rien ne s\'active', m['leve'] and m['lair'] is False, m)
            pg.evaluate("()=>{window._murBaisse&&_murBaisse();setPremium(true);document.getElementById('notifScreen').classList.remove('show');window._notifPage()}"); pg.wait_for_timeout(800)
            pg.evaluate("()=>document.querySelector('#notifScreen [data-nt=lair]').click()"); pg.wait_for_timeout(200)
            pg.evaluate("()=>document.querySelector('#notifScreen [data-nt=heure]').click()"); pg.wait_for_timeout(200)
            py = pg.evaluate("()=>({e:_notifEtat(),f:[...document.querySelectorAll('#notifScreen .nt-mur .nt-row')].map(r=>getComputedStyle(r).filter),h:document.querySelector('#notifScreen [data-nt=heure] .nt-v').textContent,lairPlan:_notifPlan().filter(x=>x.type==='lair').map(x=>x.mots.texte)})")
            t('8d · Ma Parole ! : net, la mémoire s\'active, l\'heure passe au matin', py['f'] == ['none', 'none'] and py['e']['lair'] is True and py['e']['heure'] == 8 and py['h'] == 'le matin, vers 8 h', py)
            t('8e · la mémoire propose une parole en l\'air, avec ses mots', MOTS['lair'][1] in py['lairPlan'] or any('flotte toujours. Un de ces jours ?' in x for x in py['lairPlan']), py['lairPlan'])
            bt = pg.evaluate("()=>{const r=document.querySelector('#notifScreen .nt-bientot');r.click();return [r.querySelector('.nt-tog').classList.contains('on'),r.querySelector('.nt-s').textContent]}")
            t('8f · « Ce qu\'on me lance » attend Firebase : éteint, sans prise', bt[0] is False and 'bientôt' in bt[1], bt)
        except Exception as ex:
            t('le contrat s\'exécute jusqu\'au bout', False, str(ex).split('\n')[0][:160])
        t('0 · aucune erreur JS', not errs, errs[:2])
        ctx.close()
    b.close()
print('\n%d/%d' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
