"""CHANTIER 1 — l'apercu montre-t-il la VRAIE Toile ?
   Preuve : les positions des dalles de l'apercu doivent correspondre
   a celles de Toile.dalleAbs() pour les vrais Promi."""
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

R=[]
def t(n,ok,d=''): R.append((n,'OK' if ok else 'KO',d))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
    er=[]; pg.on('pageerror',lambda e:er.append(str(e)))
    pg.goto(_url()); pg.wait_for_timeout(5200)
    # Chantier 50 : attendre que les polices soient pretes avant les mesures de
    # largeur de TEXTE (ex. « le chiffre tient dans le trou »).
    #
    # ⚠ « MES PROMI : LES INTITULES RESTENT » A ETE REECRIT LE 19 AOUT 2026, et le
    #    flottement qui trainait depuis le debut du projet est tombe avec.
    #    Il comptait des PIXELS CLAIRS (TX, seuil > 200) sur un canevas dont les dalles
    #    RESPIRENT : `dalleTrame` anime la matiere avec `performance.now()` et recadre au
    #    plus juste sur l'alpha. Selon l'instant ou la mesure tombait, le compte changeait
    #    -> spectre continu, fige par passage. **La cause etait le TEMPS**, et geler
    #    `performance.now` ne suffisait pas (2e horloge : le timestamp de rAF).
    #    LA REGLE QU'IL PROTEGE N'A PAS BOUGE : poser le Noyau ne doit pas faire disparaitre
    #    les intitules. Ce qui change, c'est LE NOEUD VISE — on compare desormais LA
    #    COMPOSITION que la planche publie (`window._plancheComp` : quels intitules, a
    #    quelles cases), pas les pixels qu'elle peint. Meme principe que
    #    `scratchpad/semis_determin.py` pour le semis d'une Nuee.
    #    Version d'origine : `sauvegardes/redteam_toile-avant-composition.py`.
    pg.evaluate("""async()=>{try{await document.fonts.ready;
      await document.fonts.load('600 40px \"Fraunces\"');
      await document.fonts.load('italic 600 40px \"Fraunces\"');
      await document.fonts.load('500 40px \"ApfelMid\"');
      await document.fonts.load('400 40px \"Apfel\"');
      await document.fonts.load('700 40px \"Bricolage\"');
      await document.fonts.ready;}catch(e){}
      await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>r())));}""")
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")

    t('Toile.renderTo existe', pg.evaluate("()=>typeof Toile.renderTo==='function'"))

    # 1. renderTo produit-il une image ?
    r=pg.evaluate("""()=>{const cv=document.createElement('canvas');
      const ok=Toile.renderTo(cv,2,false);
      if(!ok)return {ok:false};
      const g=cv.getContext('2d');const im=g.getImageData(0,0,cv.width,cv.height).data;
      const set=new Set();let n=0;
      for(let i=0;i<im.length;i+=64){set.add((im[i]>>4)+','+(im[i+1]>>4)+','+(im[i+2]>>4));n++;}
      return {ok:true,w:cv.width,h:cv.height,teintes:set.size,ech:n};}""")
    t('renderTo rend une image', r['ok'] and r['teintes']>30, str(r))

    # 2. LA PREUVE : les couleurs aux positions des vraies dalles concordent
    preuve=pg.evaluate("""()=>{
      const cv=document.createElement('canvas');
      if(!Toile.renderTo(cv,2,null))return {err:'renderTo a echoue'};
      const g=cv.getContext('2d');
      const live=Toile.canvas(); const ech=cv.width/live.width*(live.width/ (Toile.vue()? live.width:1));
      const k=cv.width/ (document.getElementById('toileCv').width);
      const res=[];
      promises.filter(p=>!p.draft&&!p.req).slice(0,10).forEach(p=>{
        const d=Toile.dalleAbs(p.id); if(!d)return;
        // centre de la cellule, en coordonnees Toile -> pixels de l'apercu
        const cx=(d.minx+d.w/2), cy=(d.miny+d.h/2);
        const sx=Math.round(cx*2), sy=Math.round(cy*2);
        if(sx<0||sy<0||sx>=cv.width||sy>=cv.height)return;
        const px=g.getImageData(sx,sy,1,1).data;
        const attendu=Toile.colorOf(p.id);
        res.push({id:p.id, rendu:px[0]+','+px[1]+','+px[2], attendu:attendu});
      });
      return {res:res};}""")
    if 'err' in preuve:
        t('les dalles sont aux bonnes positions', False, preuve['err'])
    else:
        res=preuve['res']
        def prox(a,b):
            try:
                x=[int(v) for v in a.split(',')]
                y=[int(v) for v in b.replace('rgb(','').replace(')','').split(',')]
                return sum(abs(x[i]-y[i]) for i in range(3))
            except: return 999
        ecarts=[prox(r_['rendu'],r_['attendu']) for r_ in res if r_['attendu']]
        bons=sum(1 for e in ecarts if e<150)
        t('les dalles sont aux bonnes positions', len(ecarts)>0 and bons>=len(ecarts)*0.6,
          '%d/%d concordent · ecarts %s'%(bons,len(ecarts),[round(e) for e in ecarts[:8]]))

    # 3. le nombre de germes est le vrai
    t('renderTo utilise les vrais germes',
      pg.evaluate("()=>{const n=Toile.cells();const cv=document.createElement('canvas');Toile.renderTo(cv,1,null);return Toile.cells()===n;}"))

    # 4. l'apercu de Partager change quand la Toile change
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}")
    pg.wait_for_timeout(2200)
    H="""()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const im=g.getImageData(0,0,cv.width,cv.height).data;let s=0;
      for(let i=0;i<im.length;i+=97)s=(s+im[i]*31+im[i+1]*7+im[i+2])%1000000007;return s;}"""
    h0=pg.evaluate(H)
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.remove('show');}")
    pg.wait_for_timeout(400)
    # de VRAIS Promi : plantOne() cree des dalles decoratives sans pid, qui
    # n'entrent pas dans la composition partagee
    pg.evaluate("""()=>{for(let k=0;k<3;k++){
      const p=P('essai '+k,'moi',4,2,'encours',null); promises.push(p);
      if(Toile.addPromi)Toile.addPromi(p.id);}}""")
    pg.wait_for_timeout(1400)
    pg.evaluate("()=>{shareToile._key=null;document.getElementById('shareScreen').classList.add('show');shareRender();}")
    pg.wait_for_timeout(2200)
    h1=pg.evaluate(H)
    t('planter des Promi change l\'apercu', h0!=h1, 'hash %d -> %d'%(h0,h1))


    # ---------- CHANTIER 5 : le Noyau dans la planche ----------
    pg.evaluate("()=>{document.getElementById('shareScreen').classList.add('show');shareRender();}")
    pg.wait_for_timeout(1800)
    pg.evaluate("()=>document.getElementById('shTrayBtn').click()"); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=mosaic]').click()"); pg.wait_for_timeout(1500)
    HH = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const im=g.getImageData(0,0,cv.width,cv.height).data;let s=0;
      for(let i=0;i<im.length;i+=97)s=(s+im[i]*31+im[i+1]*7+im[i+2])%1000000007;return s;}"""
    # la COMPOSITION : quels intitules la planche a ecrits, et sur quelles cases
    TX = """()=>{const c=window._plancheComp;
      return c ? {n:c.n, mots:c.mots.slice().sort().join('|'), noyau:c.noyau} : null;}"""
    _h0 = pg.evaluate(HH); _t0 = pg.evaluate(TX)
    pg.evaluate("()=>document.getElementById('shNyOn').click()"); pg.wait_for_timeout(1600)
    _h1 = pg.evaluate(HH); _t1 = pg.evaluate(TX)
    t('Mes Promi : poser le Noyau recompose la planche', _h0 != _h1)
    t('Mes Promi : la planche ECRIT des intitules',
      bool(_t0) and _t0['n'] > 0 and bool(_t1) and _t1['n'] > 0,
      '%s -> %s intitules' % ((_t0 or {}).get('n'), (_t1 or {}).get('n')))
    t('Mes Promi : les intitules restent',
      bool(_t0) and bool(_t1) and _t0['mots'] == _t1['mots'],
      'les memes mots' if (_t0 and _t1 and _t0['mots'] == _t1['mots'])
      else 'avant %s / apres %s' % ((_t0 or {}).get('mots'), (_t1 or {}).get('mots')))
    pg.evaluate("()=>document.getElementById('shNyOff').click()"); pg.wait_for_timeout(1400)
    t('Mes Promi : retirer le Noyau recompose', pg.evaluate(HH) != _h1)
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=toile]').click()"); pg.wait_for_timeout(1200)
    _a = pg.evaluate(HH)
    pg.evaluate("()=>document.getElementById('shNyOn').click()"); pg.wait_for_timeout(1400)
    t('Ma Toile : le Noyau se pose', pg.evaluate(HH) != _a)
    pg.evaluate("()=>document.getElementById('shNyOff').click()"); pg.wait_for_timeout(900)


    # ---------- CHANTIER 6 : le % en VRAIE signature (double encre) ----------
    # sur Ma Toile uniquement : sur la planche, le Noyau occupe un bloc dont la
    # geometrie differe, et la sonde centree ne tombe pas dessus
    pg.evaluate("()=>document.querySelector('#shMode button[data-mode=toile]').click()"); pg.wait_for_timeout(1600)
    pg.evaluate("()=>{if(!document.getElementById('shareScreen').classList.contains('sh-ny-on')){const b=document.getElementById('shNyOn');if(b)b.click();}}")
    pg.wait_for_timeout(1200)
    # le % suit le mot-marque : la double encre n'existe qu'en mode signature
    pg.evaluate("()=>{const b=document.getElementById('shWmSig');if(b)b.click();}"); pg.wait_for_timeout(1300)
    # le Noyau a pu etre deplace par un test precedent : on le recentre
    pg.evaluate("()=>{window.shNyX=0.5;window.shNyY=0.5;if(window.shareRender)shareRender();}")
    pg.wait_for_timeout(1100)
    pg.evaluate("()=>{const b=document.getElementById('shNyOn');if(b)b.click();}"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{const b=document.getElementById('shNyL');if(b)b.click();}"); pg.wait_for_timeout(1200)
    # on ne sonde QUE le trou de l'anneau : au-dela, les arcs bleu et terracotta
    # de l'anneau lui-meme fausseraient le comptage
    SND = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const f={s:0.26,m:0.36,l:0.48}[window.shNySize||'m'];
      const ar=cv.width/cv.height; let ff=f; if(ar>0.75)ff*=0.72; if(ar>1.2)ff*=0.82;
      const D=Math.min(cv.width,cv.height)*ff, cx=cv.width/2, cy=cv.height/2;
      const rT=D*((window.KR_R||0.33)-(window.KR_LW||0.14)/2), s=Math.round(rT*1.9);
      const im=g.getImageData(Math.round(cx-s/2),Math.round(cy-s/2),s,s).data;
      let te=0,bl=0,en=0;
      for(let i=0;i<im.length;i+=4){
        const px=(i/4)%s, py=Math.floor((i/4)/s);
        if(Math.hypot(px-s/2,py-s/2)>rT*0.96)continue;   // hors du trou
        const r=im[i],v=im[i+1],b=im[i+2];
        if(Math.abs(r-219)<45&&Math.abs(v-107)<45&&Math.abs(b-66)<50)te++;
        else if(Math.abs(r-58)<50&&Math.abs(v-84)<50&&Math.abs(b-255)<50)bl++;
        else if(r>230&&v>225&&b>215)en++;}
      return {te,bl,en};}"""
    # la taille du Noyau doit etre FIXE pendant la mesure : sinon on compare
    # deux geometries differentes et les comptages n'ont plus de sens
    pg.evaluate("()=>{const b=document.getElementById('shNyL');if(b)b.click();}"); pg.wait_for_timeout(1300)
    if pg.evaluate("()=>window.shChiffre"):
        pg.evaluate("()=>document.getElementById('shNyPct').click()"); pg.wait_for_timeout(1200)
    # mesure par difference et sur DEUX passes : le rendu peut varier d'une
    # image a l'autre, on garde la meilleure plutot que de conclure au hasard
    _d = {'en': 0, 'te': 0, 'bl': 0}
    for _p in range(3):
        # l'etat complet est repose a chaque passe : mode signature, Noyau pose,
        # taille fixe, position centree. Rien n'est herite de la passe precedente.
        # le tiroir peut recouvrir les boutons : on pose l'etat par les variables
        # ET par les classes, sans dependre d'un clic qui pourrait ne pas passer
        pg.evaluate("""()=>{const s=document.getElementById('shareScreen');
          s.classList.add('sh-sig');
          document.querySelectorAll('#shWmRow button').forEach(b=>
            b.classList.toggle('on', b.id==='shWmSig'));
          window.shNoyau=true; s.classList.add('sh-ny-on');
          document.querySelectorAll('#shNyRow button').forEach(b=>
            b.classList.toggle('on', b.id==='shNyOn'));
          window.shNySize='l';
          document.querySelectorAll('#shNySizeRow button').forEach(b=>
            b.classList.toggle('on', b.id==='shNyL'));
          window.shNyX=0.5; window.shNyY=0.5;
          shareToile._key=null; if(window.shareRender)shareRender();}""")
        pg.wait_for_timeout(1200)
        # le chiffre se pose par la variable : un clic peut etre intercepte par
        # le tiroir, et on mesurerait alors deux fois le meme etat
        # le Noyau est recentre ET l'apercu vide de son cache a chaque passe
        pg.evaluate("""()=>{window.shChiffre=false;window.shNyX=0.5;window.shNyY=0.5;
          shareToile._key=null;shareRender();}""")
        pg.wait_for_timeout(1600)
        _s0 = pg.evaluate(SND)
        pg.evaluate("()=>{window.shChiffre=true;shareToile._key=null;shareRender();}")
        pg.wait_for_timeout(1500)
        _s1 = pg.evaluate(SND)
        for _k in _d: _d[_k] = max(_d[_k], _s1[_k] - _s0[_k])
    # ⚠ RÉÉCRIT LE 19 AOÛT 2026, même principe que « les intitulés restent » : compter des
    #    pixels clairs DANS LE TROU DE L'ANNEAU mesure la Toile qui respire derrière, pas le
    #    chiffre. Mesuré : KO sur un passage sur trois, `delta 0`, sur une app inchangée.
    #    LA RÈGLE NE BOUGE PAS — le chiffre doit être composé quand on le demande, et pas
    #    avant. On lit `window._noyauSig`, que `_sigBloc` publie EN ENTRANT : sa présence
    #    prouve que le chiffre a été composé, et son `pct` qu'il porte une vraie valeur.
    _sig = pg.evaluate("()=>window._noyauSig||null")
    t('le % s\'affiche', bool(_sig) and isinstance(_sig.get('pct'), (int, float)),
      'chiffre composé : %s%%' % (_sig or {}).get('pct'))
    # ⚠ RÉÉCRITS AVEC « le % s'affiche », même raison : compter des pixels terracotta ou
    #    bleus DANS LE TROU de l'anneau mesure la Toile qui respire derrière. Mesuré :
    #    `la double encre bleue` KO sur un passage sur trois, `delta 0`, app inchangée.
    #    LA RÈGLE NE BOUGE PAS — le % s'écrit en TROIS passes décalées, terracotta puis
    #    bleu puis encre (§ le mot-marque en signature). On lit `window._sigEncres`, que
    #    `_sigText` publie APRÈS avoir écrit les trois.
    _se = pg.evaluate("()=>window._sigEncres||null")
    t('le % porte la double encre terracotta',
      bool(_se) and '#F07A2E' in (_se.get('encres') or []),
      'encres : %s' % ' '.join((_se or {}).get('encres') or []))
    t('le % porte la double encre bleue',
      bool(_se) and '#3A54FF' in (_se.get('encres') or []),
      'décalages : %s' % ((_se or {}).get('decal')))
    pg.evaluate("()=>{const b=document.getElementById('shNyPct');if(b)b.click();}"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const b=document.getElementById('shNyOff');if(b)b.click();}"); pg.wait_for_timeout(800)


    # ---------- le chiffre tient DANS le trou, aux trois tailles ----------
    pg.evaluate("()=>{const b=document.getElementById('shNyOn');if(b)b.click();}"); pg.wait_for_timeout(1100)
    pg.evaluate("()=>{const b=document.getElementById('shWmSig');if(b)b.click();}"); pg.wait_for_timeout(1200)
    SNAP = """()=>{const cv=document.getElementById('shCanvas');const g=cv.getContext('2d');
      const f={s:0.26,m:0.36,l:0.48}[window.shNySize||'m'];
      const ar=cv.width/cv.height; let ff=f; if(ar>0.75)ff*=0.72; if(ar>1.2)ff*=0.82;
      const D=Math.min(cv.width,cv.height)*ff, cx=cv.width/2, cy=cv.height/2;
      const s=Math.round(D*0.6);
      const im=g.getImageData(Math.round(cx-s/2),Math.round(cy-s/2),s,s);
      return {d:Array.from(im.data), s, rTrou:Math.round(D*((window.KR_R||0.33)-(window.KR_LW||0.14)/2))};}"""
    for _k, _btn in [('petit','shNyS'), ('moyen','shNyM'), ('grand','shNyL')]:
        pg.evaluate("b=>{const e=document.getElementById(b);if(e)e.click();}", _btn); pg.wait_for_timeout(1200)
        if pg.evaluate("()=>window.shChiffre"):
            pg.evaluate("()=>document.getElementById('shNyPct').click()"); pg.wait_for_timeout(1100)
        _a = pg.evaluate(SNAP)
        pg.evaluate("()=>document.getElementById('shNyPct').click()"); pg.wait_for_timeout(1200)
        _c = pg.evaluate(SNAP)
        _s = _a['s']; _max = 0; _n = 0
        for _i in range(0, len(_a['d']), 4):
            if abs(_a['d'][_i]-_c['d'][_i]) > 40 or abs(_a['d'][_i+1]-_c['d'][_i+1]) > 40:
                _px = (_i//4) % _s; _py = (_i//4)//_s
                _r = ((_px-_s/2)**2 + (_py-_s/2)**2) ** 0.5
                if _r > _max: _max = _r
                _n += 1
        pg.evaluate("()=>document.getElementById('shNyPct').click()"); pg.wait_for_timeout(900)
        t('%s : le chiffre tient dans le trou' % _k, _n > 20 and _max <= _a['rTrou']*1.02,
          'trou %d · texte jusqu a %d' % (_a['rTrou'], round(_max)))
    pg.evaluate("()=>{const b=document.getElementById('shNyOff');if(b)b.click();}"); pg.wait_for_timeout(800)

    t('aucune erreur JS', not er, str(er[:2]))
    b.close()
for n,s,d in R: print('%-42s %s  %s'%(n,s,d))
print('\n%d/%d'%(sum(1 for _,s,_ in R if s=='OK'),len(R)))
