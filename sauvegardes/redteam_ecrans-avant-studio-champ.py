# -*- coding: utf-8 -*-
"""Batterie 4 — les huit écrans jamais testés.
   Chaque écran : ouverture réelle, éléments clés, géométrie, clair ET sombre."""
from playwright.sync_api import sync_playwright
import os as _os
_ICI = _os.path.dirname(_os.path.abspath(__file__))
def _url():
    for p in [_os.path.join(_ICI,'app.html'), '/home/claude/app.html']:
        if _os.path.exists(p): return 'file://' + p
    import re as _re
    for f in sorted(_os.listdir(_ICI), reverse=True):
        if _re.match(r'promi-v\d+\.html$', f): return 'file://' + _os.path.join(_ICI, f)
    return 'file:///home/claude/app.html'

import sys

R=[]
def t(n,ok,d=''): R.append((n,'OK' if ok else 'KO',d))

GEO = """(sel)=>{const d=document.getElementById('device').getBoundingClientRect();
  const e=document.querySelector(sel); if(!e) return null;
  const r=e.getBoundingClientRect();
  return {x:Math.round(r.left-d.left),y:Math.round(r.top-d.top),
          w:Math.round(r.width),h:Math.round(r.height),
          dw:Math.round(d.width),dh:Math.round(d.height),
          vis:getComputedStyle(e).display!=='none'&&r.width>0};}"""

DEBORDE = """(sel)=>{const d=document.getElementById('device').getBoundingClientRect();
  const root=document.querySelector(sel); if(!root)return -1;
  let n=0;
  root.querySelectorAll('*').forEach(e=>{
    const r=e.getBoundingClientRect();
    if(r.width<2||r.height<2)return;
    if(getComputedStyle(e).position==='fixed')return;
    if(r.right>d.right+2||r.left<d.left-2)n++;
  });
  return n;}"""

def batterie(theme):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
        pg.goto(_url()); pg.wait_for_timeout(5200)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        if theme=='light':
            pg.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>{e.classList.add('light');e.classList.remove('dark');})")
            pg.wait_for_timeout(500)
        S=' ['+('clair' if theme=='light' else 'sombre')+']'

        # ---------- 1. TOILE ----------
        cv=pg.evaluate(GEO,'#toileCv')
        t('Toile : canvas présent'+S, bool(cv) and cv['vis'], str(cv))
        t('Toile : remplit l\'écran'+S, cv and cv['w']>=cv['dw']-4 and cv['h']>=cv['dh']-90, str(cv))
        t('Toile : des dalles colorées'+S, pg.evaluate("""()=>{const c=document.getElementById('toileCv');
          const g=c.getContext('2d');const im=g.getImageData(0,0,c.width,c.height).data;
          let n=0;for(let i=0;i<im.length;i+=400){const r=im[i],v=im[i+1],b=im[i+2];
            if(Math.abs(r-v)>18||Math.abs(v-b)>18)n++;}return n>30;}"""))
        v0=pg.evaluate("()=>JSON.stringify(Toile.vue())")
        t('Toile : API vue() lisible'+S, v0 and 's' in v0, v0)
        # ⚠ CONTRAT RÉÉCRIT AU NIVEAU DE LA DÉCISION (CLAUDE.md §7) — 20 août 2026.
        #   Règle encodée : « une cellule grise ne désigne aucun Promi ». Le contrôle la
        #   testait par `hit(...) === null`, la forme que l'API rendait quand la Toile était
        #   pleine (23 promesses de l'ancien jeu). Avec le jeu de la planche — 12 plantés
        #   pour ~69 cellules — `hit()` rend un descripteur de cellule VIDE :
        #   `{pid:null, kind:'promi', nuee:null}`. C'est le même renseignement.
        #   Mesuré : la forme rendue oscille selon le semis (null en sombre, descripteur en
        #   clair, sur le MÊME jeu) — le contrôle d'origine était donc aussi un flake.
        #   Le contrat protège la même chose : rien n'ouvre de fiche hors d'une dalle plantée.
        #   Version d'origine : sauvegardes/redteam_ecrans-avant-jeu-planche.py
        t('Toile : hit() ignore les cellules grises'+S,
          pg.evaluate("()=>{const h=Toile.hit(-9999,-9999);return h===null||h.pid==null;}"),
          pg.evaluate("()=>{const h=Toile.hit(-9999,-9999);return h===null?'null':JSON.stringify(h);}"))
        # et il garde ses dents : une dalle PLANTÉE, elle, se désigne bien.
        t('Toile : hit() désigne un Promi planté'+S,
          pg.evaluate("""()=>{const v=Toile.vue&&Toile.vue(); const ids=promises.filter(p=>!p.draft).map(p=>p.id);
            for(let x=8;x<390;x+=7) for(let y=8;y<760;y+=7){
              const h=Toile.hit(x,y); if(h&&h.pid!=null&&ids.indexOf(h.pid)>=0) return true;}
            return false;}"""))
        n0=pg.evaluate("()=>Toile.cells()")
        pg.evaluate("()=>Toile.plantOne()"); pg.wait_for_timeout(600)
        t('Toile : planter garde la densité'+S, pg.evaluate("()=>Toile.cells()")==n0,
          '%s -> %s'%(n0,pg.evaluate("()=>Toile.cells()")))
        pg.evaluate("()=>Toile.unplantOne()"); pg.wait_for_timeout(400)

        # ---------- 2. CRÉER ----------
        pg.evaluate("()=>document.getElementById('createBtn').click()"); pg.wait_for_timeout(1200)
        t('Créer : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('createSheet').classList.contains('show')"))
        t('Créer : trois tuiles (promi, chiche, nuée)'+S, pg.evaluate("()=>document.querySelectorAll('#createSheet .tile[data-kind]').length")==3)
        t('Créer : sélecteur de sens'+S, pg.evaluate("()=>document.querySelectorAll('#csSens button').length")==2)
        t('Créer : rien ne déborde'+S, pg.evaluate(DEBORDE,'#createSheet')==0,
          'éléments hors cadre : %s'%pg.evaluate(DEBORDE,'#createSheet'))
        # une forme à la fois
        # Trois natures à l'écran de choix : Promi · Chiche · Nuée (le Brouillon est un
        # ÉTAT via « garder de côté »). Le Chiche réutilise le formulaire du Promi.
        etats=[]
        for k in ['promi','chiche','nuee']:
            pg.evaluate("k=>document.querySelector('.tile[data-kind='+k+']').click()",k); pg.wait_for_timeout(450)
            etats.append(pg.evaluate("""()=>['promiForm','nueeForm']
              .filter(i=>{const e=document.getElementById(i);return e&&getComputedStyle(e).display!=='none';}).length"""))
        t('Créer : une seule forme visible'+S, etats==[1,1,1], str(etats))
        # le brouillon reste atteignable : le contrôle « garder de côté » existe
        t('Créer : « garder de côté » présent'+S,
          pg.evaluate("()=>!!document.querySelector('.garde-cote,[data-gc]')"))
        # champ obligatoire
        pg.evaluate("()=>document.querySelector('.tile[data-kind=promi]').click()"); pg.wait_for_timeout(400)
        n=pg.evaluate("()=>promises.length")
        pg.evaluate("()=>{document.getElementById('fTitle').value='';document.getElementById('addPromi').click();}")
        pg.wait_for_timeout(400)
        t('Créer : champ vide refusé'+S, pg.evaluate("()=>promises.length")==n)
        t('Créer : le refus se voit'+S, pg.evaluate("()=>document.getElementById('fTitle').classList.contains('req-vide')"))
        pg.evaluate("()=>closeAll()"); pg.wait_for_timeout(600)

        # ---------- 3. INDEX ----------
        pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();else document.getElementById('indexSheet').classList.add('show');}"); pg.wait_for_timeout(1400)
        t('Index : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('indexSheet').classList.contains('show')"))
        t('Index : des lignes'+S, pg.evaluate("()=>document.querySelectorAll('#indexSheet .row,#indexSheet .irow,#indexList > *').length")>0,
          str(pg.evaluate("()=>document.querySelectorAll('#indexList > *').length")))
        t('Index : miniatures de dalle'+S, pg.evaluate("()=>document.querySelectorAll('#indexSheet canvas').length")>0)
        t('Index : rien ne déborde'+S, pg.evaluate(DEBORDE,'#indexSheet')==0,
          str(pg.evaluate(DEBORDE,'#indexSheet')))
        t('Index : ✕ ferme'+S, (pg.evaluate("()=>{const c=document.querySelector('#indexSheet .closeb');if(c)c.click();return 1;}"),
           pg.wait_for_timeout(700), not pg.evaluate("()=>document.getElementById('indexSheet').classList.contains('show')"))[2])

        # ---------- 4. FIL ----------
        pg.evaluate("()=>{if(window.buildFeed)buildFeed();const e=document.getElementById('feedScreen');if(e)e.classList.add('show');}")
        pg.wait_for_timeout(1200)
        t('Fil : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('feedScreen').classList.contains('show')"))
        t('Fil : rien ne déborde'+S, pg.evaluate(DEBORDE,'#feedScreen')==0, str(pg.evaluate(DEBORDE,'#feedScreen')))
        pg.evaluate("()=>document.getElementById('feedScreen').classList.remove('show')"); pg.wait_for_timeout(400)

        # ---------- 5. AURA ----------
        pg.evaluate("()=>document.getElementById('souffleBtn').click()"); pg.wait_for_timeout(1800)
        t('Aura : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('auraScreen').classList.contains('show')"))
        t('Aura : anneau peint'+S, pg.evaluate("""()=>{const c=document.querySelector('#auraScreen .kr-c');
          if(!c)return false;const g=c.getContext('2d');const im=g.getImageData(0,0,c.width,c.height).data;
          let n=0;for(let i=3;i<im.length;i+=160)if(im[i]>40)n++;return n>20;}"""))
        t('Aura : « Partager mon Noyau » retiré'+S, not pg.evaluate("()=>!!document.getElementById('sealShare')"))
        t('Aura : rien ne déborde'+S, pg.evaluate(DEBORDE,'#auraScreen')==0, str(pg.evaluate(DEBORDE,'#auraScreen')))
        pg.evaluate("()=>{const c=document.querySelector('#auraScreen .closeb');if(c)c.click();}"); pg.wait_for_timeout(700)

        # ---------- 6. STUDIO ----------
        pg.evaluate("()=>document.getElementById('studioBtn').click()"); pg.wait_for_timeout(1800)
        t('Studio : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('studioScreen').classList.contains('show')"))
        t('Studio : les deux bascules groupées'+S, pg.evaluate("()=>!!document.querySelector('.studio-grp')"))
        g=pg.evaluate(GEO,'.studio-grp')
        t('Studio : groupe centré'+S, g and abs(g['x']-(g['dw']-g['x']-g['w']))<10, str(g))
        t('Studio : aperçus de monde'+S, pg.evaluate("()=>document.querySelectorAll('#studioScreen canvas').length")>0,
          str(pg.evaluate("()=>document.querySelectorAll('#studioScreen canvas').length")))
        pg.evaluate("()=>{const c=document.querySelector('#studioScreen .closeb');if(c)c.click();}"); pg.wait_for_timeout(700)

        # ---------- 7. RÉGLAGES ----------
        pg.evaluate("()=>{const e=document.getElementById('settingsScreen');if(e)e.classList.add('show');}")
        pg.wait_for_timeout(1000)
        t('Réglages : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('settingsScreen').classList.contains('show')"))
        t('Réglages : ligne Inviter'+S, pg.evaluate("()=>!!document.getElementById('setInvite')"))
        t('Réglages : encart Cercle'+S, pg.evaluate("()=>!!document.querySelector('.set-cercle')"))
        t('Réglages : rien ne déborde'+S, pg.evaluate(DEBORDE,'#settingsScreen')<=1,
          str(pg.evaluate(DEBORDE,'#settingsScreen')))
        pg.evaluate("()=>document.getElementById('settingsScreen').classList.remove('show')"); pg.wait_for_timeout(400)

        # ---------- 8. FICHE ----------
        pg.evaluate("""()=>{const p=promises.find(x=>!x.draft&&!x.req);
          if(p&&window.renderDetail){renderDetail(p.id);}
          const e=document.getElementById('detailPoster');if(e)e.classList.add('show');}""")
        pg.wait_for_timeout(1400)
        t('Fiche : s\'ouvre'+S, pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
        t('Fiche : vignette de dalle'+S, pg.evaluate("()=>{const e=document.getElementById('dForm');return !!e;}"))
        t('Fiche : le + commun'+S, pg.evaluate("()=>document.querySelectorAll('#detailPoster .dpf-plus').length")>0)
        t('Fiche : rien ne déborde'+S, pg.evaluate(DEBORDE,'#detailPoster')==0, str(pg.evaluate(DEBORDE,'#detailPoster')))




        # ---------- AURA : le Noyau ne porte que le mot ----------
        _tx = pg.evaluate("()=>[...document.querySelectorAll('#auraSeal svg text')].map(e=>e.textContent.trim())")
        # le Noyau ne porte que la serie, s'il y en a une. Le mot d'harmonie est
        # SOUS l'anneau, avec HARMONIE et le % : ils forment un ensemble.
        t('Aura : le Noyau ne porte que la serie'+S,
          all('série' in x for x in _tx), str(_tx))
        _mot = pg.evaluate("()=>{const e=document.querySelector('#kUnder .ku-mot');return e?e.textContent.trim():null;}")
        t('Aura : le mot d harmonie est sous le Noyau'+S, bool(_mot), str(_mot))
        _u = pg.evaluate("""()=>{const u=document.getElementById('kUnder');if(!u)return null;
          const p=u.querySelector('.ku-pct');const c=p?getComputedStyle(p):null;
          return {a:!!p, fam:c?c.fontFamily.split(',')[0]:'', sh:c?c.textShadow:''};}""")
        t('Aura : le % est sous le Noyau'+S, bool(_u and _u['a']), str(_u))
        t('Aura : le % est en signature'+S,
          bool(_u and _u['fam'] == 'Fraunces' and '240, 122, 46' in _u['sh'] and '58, 84, 255' in _u['sh']),
          str(_u['sh'][:50]) if _u else '')
        _g = pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
          const R=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();
            return [Math.round(r.top-d.top),Math.round(r.bottom-d.top)];};
          return {seal:R('#auraSeal svg'), under:R('#kUnder'), leg:R('#auraScreen .klegend')};}""")
        t('Aura : anneau puis % puis legende'+S,
          bool(_g['seal'] and _g['under'] and _g['leg']
               and _g['under'][0] > _g['seal'][0]          # le bloc commence dans la moitie basse
               and _g['under'][1] <= _g['leg'][0]+4), str(_g))   # et finit avant la legende


        _hc = pg.evaluate("()=>[...document.querySelectorAll('#kuLab i')].map(e=>getComputedStyle(e).color)")
        t('Aura : HARMONIE en trois teintes'+S, len(set(_hc)) == 3, str(len(set(_hc))))
        _p0 = _hc[0]
        pg.evaluate("()=>{try{Toile.setPalette('ocean');}catch(e){}if(window.buildAura)buildAura();}")
        pg.wait_for_timeout(1200)
        _hc2 = pg.evaluate("()=>[...document.querySelectorAll('#kuLab i')].map(e=>getComputedStyle(e).color)")
        t('Aura : les teintes suivent le Studio'+S, _hc2 and _hc2[0] != _p0, '%s -> %s' % (_p0, _hc2[0] if _hc2 else '?'))
        pg.evaluate("()=>{try{Toile.setPalette('signal');}catch(e){}if(window.buildAura)buildAura();}")
        pg.wait_for_timeout(1000)



        # ---------- Aura : la legende respire entre le % et les compteurs ----------
        _g2 = pg.evaluate("""()=>{const d=document.getElementById('device').getBoundingClientRect();
          const R=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();
            return [Math.round(r.top-d.top),Math.round(r.bottom-d.top)];};
          return {pct:R('#kUnder .ku-pct'), leg:R('#auraScreen .klegend'), cnt:R('#kCount')};}""")
        if _g2['pct'] and _g2['leg'] and _g2['cnt']:
            _a = _g2['leg'][0]-_g2['pct'][1]; _b = _g2['cnt'][0]-_g2['leg'][1]
            t('Aura : la legende est centree entre % et compteurs'+S,
              abs(_a-_b) <= 12, 'au-dessus %d · en-dessous %d' % (_a, _b))
        _sh = pg.evaluate("()=>getComputedStyle(document.querySelector('#kUnder .ku-pct')).textShadow")
        _fs = pg.evaluate("()=>parseFloat(getComputedStyle(document.querySelector('#kUnder .ku-pct')).fontSize)")
        _off = float(_sh.split('px')[0].split(' ')[-1].replace('-',''))
        t('Aura : le decalage suit le corps (0.116 em)'+S, abs(_off/_fs - 0.116) < 0.004,
          '%.4f' % (_off/_fs))


        # ---------- le selecteur du haut : Toile / Index ----------
        _v = pg.evaluate("()=>[...document.querySelectorAll('#viewSwitch button')].map(e=>e.textContent.trim())")
        t('le selecteur dit Toile / Index'+S, _v == ['Toile','Index'], str(_v))
        t('un seul Fil dans l app'+S, pg.evaluate("""()=>{let n=0;
          document.querySelectorAll('button,.dctrl').forEach(e=>{const q=e.querySelector('.l');
            const tx=(q?q.textContent:e.textContent||'').trim();
            if(/^Fil$/i.test(tx))n++;});return n;}""") == 1)
        pg.evaluate("()=>document.querySelector('#viewSwitch button[data-view=index]').click()")
        pg.wait_for_timeout(1500)
        t('le selecteur ouvre l Index'+S,
          pg.evaluate("()=>document.getElementById('indexSheet').classList.contains('show')"))
        pg.evaluate("()=>{if(window.closeAll)closeAll();}"); pg.wait_for_timeout(700)


        _sw = pg.evaluate("""()=>{const cv=document.createElement('canvas').getContext('2d');
          const s=document.getElementById('viewSwitch');
          const b=s.querySelector('button'); const c=getComputedStyle(b);
          cv.font=c.fontWeight+' '+c.fontSize+' Bricolage,system-ui,sans-serif';
          const demi=(parseFloat(getComputedStyle(s).width)||102)/2;
          const pad=parseFloat(c.paddingLeft);
          return [...s.querySelectorAll('button')].map(e=>{
            const w=cv.measureText(e.textContent.trim()).width;
            return {t:e.textContent.trim(), tient:w <= demi-2*pad};});}""")
        t('les libelles tiennent dans le selecteur'+S,
          all(x['tient'] for x in _sw), str(_sw))
        # REGLE : le selecteur fait exactement la largeur des deux boutons ronds
        _lw = pg.evaluate("()=>parseFloat(getComputedStyle(document.getElementById('viewSwitch')).width)")
        # la reference est MESUREE, pas codee en dur : deux .tc + le gap de .tcrow
        _ref = pg.evaluate("""()=>{const tc=document.querySelector('.tc');
          const row=document.querySelector('.tcrow');
          if(!tc||!row)return null;
          return 2*parseFloat(getComputedStyle(tc).width)+parseFloat(getComputedStyle(row).gap);}""")
        t('le selecteur fait la largeur des deux boutons'+S,
          _ref is not None and abs(_lw - _ref) < 1, '%s px pour une reference de %s' % (_lw, _ref))


        # ---------- L'INDEX EN BLOCS ----------
        pg.evaluate("()=>{if(window.ouvrirIndex)ouvrirIndex();}"); pg.wait_for_timeout(1800)
        # SECTION 4 · l'Index est porté au moodboard : le bloc plein cadre `.ix-bloc` est
        # devenu la CARTE `.s4-carte` (§3.9). L'intention des contrôles ne change pas —
        # seul le nom du nœud qu'ils désignent change.
        _nb = pg.evaluate("()=>document.querySelectorAll('#indexSheet .s4-carte').length")
        t('Index : les Promi sont des blocs'+S, _nb > 0, '%d blocs' % _nb)
        # « seuls les urgents ont un aplat » : dans la carte du moodboard l'état ne vit plus
        # dans le fond mais dans LA LIGNE (§2.1 bis). Le contrôle devient donc : aucune carte
        # n'est peinte d'une couleur d'état — le fond reste un des trois corps du §1.3.
        _etats = pg.evaluate("""()=>[...document.querySelectorAll('#indexSheet .s4-carte')]
          .map(e=>getComputedStyle(e).backgroundColor)
          .filter(c=>/240, 122, 46|43, 232, 140/.test(c)).length""")
        t('Index : seuls les urgents ont un aplat'+S, _etats == 0, 'fonds d\'état %s / %d' % (_etats, _nb))
        t('Index : le mot du temps est peint'+S,
          all(x for x in pg.evaluate("()=>[...document.querySelectorAll('#indexSheet .s4-carte .s4-et')].map(e=>e.textContent.trim())")))
        t('Index : la vraie dalle est peinte'+S,
          pg.evaluate("""()=>[...document.querySelectorAll('#indexSheet .s4-carte canvas')].filter(c=>{
            try{const g=c.getContext('2d');const d=g.getImageData(0,0,c.width,c.height).data;
            for(let i=3;i<d.length;i+=400)if(d[i]>10)return true;}catch(e){}return false;}).length""") > 0)
        t('Index : « a rattraper » a disparu'+S,
          not pg.evaluate("()=>document.body.innerText.toLowerCase().includes('rattraper')"))
        t('Index : la recherche est conservee'+S, pg.evaluate("()=>!!document.getElementById('ixSearch')"))
        t('Index : le ✕ Fermer est conserve'+S, pg.evaluate("()=>!!document.querySelector('#indexSheet .closeb')"))
        pg.evaluate("()=>{const b=document.querySelector('#indexSheet .s4-carte');if(b)b.click();}")
        pg.wait_for_timeout(1400)
        t('Index : toucher un bloc ouvre la fiche'+S,
          pg.evaluate("()=>document.getElementById('detailPoster').classList.contains('show')"))
        pg.evaluate("()=>{document.getElementById('detailPoster').classList.remove('show');document.getElementById('indexSheet').classList.remove('show');}")
        pg.wait_for_timeout(700)

        # ---------- CHANTIER 45 : le Fil dans le dock ----------
        _d = pg.evaluate("()=>[...document.querySelectorAll('.dock .dctrl,.dock .dhero')].map(e=>e.id)")
        t('le Fil a son bouton dans le dock'+S, 'filBtn' in _d, str(_d))
        t('le Fil a sa pastille'+S, pg.evaluate("()=>!!document.getElementById('filDot')"))
        pg.evaluate("()=>{FEED.push({id:99901,type:'x',text:'t',unread:true});if(window._majFilDot)_majFilDot();}")
        pg.wait_for_timeout(500)
        t('la pastille s allume sur du non-lu'+S,
          pg.evaluate("()=>document.getElementById('filDot').classList.contains('on')"))
        pg.evaluate("()=>document.getElementById('filBtn').click()"); pg.wait_for_timeout(1300)
        # le Fil vit dans #feedView (une vue), pas dans #feedScreen (un ecran)
        t('le bouton ouvre le Fil'+S,
          pg.evaluate("()=>{const v=document.getElementById('feedView');return !!v&&getComputedStyle(v).display!=='none';}"))

        _fv = pg.evaluate("""()=>{const v=document.getElementById('feedView');
          if(!v)return null; return {vis:getComputedStyle(v).display!=='none',
            n:v.querySelectorAll('.s4-carte,.fd-item').length};}""")
        t('le Fil affiche ses evenements'+S, bool(_fv and _fv['vis'] and _fv['n'] > 0), str(_fv))
        t('la pastille s eteint apres lecture'+S,
          not pg.evaluate("()=>document.getElementById('filDot').classList.contains('on')"))
        pg.evaluate("()=>{if(window.setView)setView('toile');}"); pg.wait_for_timeout(700)

        # ---------- CHANTIER 8 : l'anneau du bouton + suit la Toile ----------
        _v0 = pg.evaluate("()=>getComputedStyle(document.getElementById('createBtn')).getPropertyValue('--kr-a1').trim()")
        t('l anneau du + porte des proportions'+S, bool(_v0), _v0)
        _c = pg.evaluate("""()=>{let t=0,e=0,r=0;promises.forEach(p=>{if(p.draft||p.req)return;
          if(p.status==='tenu')t++;else if(p.status==='rate')r++;else e++;});return {t,tot:Math.max(1,t+e+r)};}""")
        _att = 360*_c['t']/_c['tot'] - 10.8
        t('elles correspondent aux Promi tenus'+S,
          _v0 and abs(float(_v0.replace('deg','')) - _att) < 1.5,
          '%s attendu %.1f' % (_v0, _att))


        _tr = pg.evaluate("""()=>[...document.querySelectorAll('.seal-crown line')].map(l=>({
          w:+l.getAttribute('stroke-width'), o:+l.getAttribute('opacity'), c:l.getAttribute('stroke')}))""")
        _pt = [x for x in _tr if x['w'] < 2.4]
        t('Aura : les petits traits sont lisibles'+S,
          bool(_pt) and min(x['o'] for x in _pt) >= 0.7,
          'opacite min %.2f' % min(x['o'] for x in _pt) if _pt else 'aucun')
        t('Aura : les traits suivent la palette'+S,
          any('rgb(' in (x['c'] or '') for x in _tr), str(_tr[0]['c'] if _tr else ''))
        t('bouton + : rotation lente'+S, pg.evaluate("""()=>{const e=document.getElementById('createBtn');
          return parseFloat(getComputedStyle(e,'::before').animationDuration) >= 40;}"""))

        # ---------- la signature est la MEME partout ----------
        _sig = pg.evaluate("""()=>{
          const r=(e)=>{if(!e)return null;const c=getComputedStyle(e);
            const f=parseFloat(c.fontSize);
            const m=c.textShadow.match(/(-?[\\d.]+)px\\s+(-?[\\d.]+)px/);
            return m? [(Math.abs(+m[1])/f).toFixed(3),(Math.abs(+m[2])/f).toFixed(3)] : null;};
          return {sig:r(document.querySelector('.sig')), kpct:r(document.getElementById('kPct'))};}""")
        t('la signature est identique Aura / app'+S,
          _sig['sig'] and _sig['kpct'] and _sig['sig']==_sig['kpct'], str(_sig))

        t('aucune erreur JS'+S, not er, str(er[:2]))
        b.close()

for th in ['dark','light']:
    batterie(th)

for n,s,d in R: print('%-46s %s  %s'%(n,s,d if s=='KO' else ''))
ok=sum(1 for _,s,_ in R if s=='OK')
print('\n%d/%d'%(ok,len(R)))
sys.exit(0 if ok==len(R) else 1)
