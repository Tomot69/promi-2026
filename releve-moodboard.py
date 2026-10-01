#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
releve-moodboard.py — la 9e batterie.
Relève TOUTES les propriétés calculées de chaque nœud mappé d'un .ph du moodboard
et les mêmes sur l'app dans l'état correspondant. Sort la liste BRUTE des écarts
triée par ampleur, + les nœuds « NON APPARIÉS ».

Règle de comparaison (le moodboard est une maquette 352 ; l'app un vrai téléphone 390) :
  · ABSOLU dans le fichier -> ABSOLU (px) : paddings, marges, rayons, tailles de
    police, interlettrage/interligne, bordures, et les hauteurs/largeurs déclarées
    en px (210, 62, 118…), + la distance au bord ANCRÉ (top/bottom, left/right).
  · RELATIF dans le fichier -> RELATIF (%) : largeurs/hauteurs en %, flex.
Ainsi « zéro » est atteignable et vrai.

Usage : python3 releve-moodboard.py [ecran]      (choix|phrase|prometsmoi|nuee|aqui|aquinuee|all)
"""
import sys, re, json
from playwright.sync_api import sync_playwright

MB  = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/MOODBOARD-parcours.html"
APP = "/Users/macbookpro/Documents/IA projetcs/Promi/Promi App/Promi 2026/app.html"

PROPS = ['fontFamily','fontSize','fontWeight','fontStyle','letterSpacing','lineHeight',
         'textTransform','textAlign','color','backgroundColor','opacity',
         'borderTopLeftRadius','boxShadow','borderTopWidth',
         'paddingTop','paddingRight','paddingBottom','paddingLeft',
         'marginTop','marginRight','marginBottom','marginLeft','display']
TYPO = {'fontFamily','fontSize','fontWeight','fontStyle','letterSpacing','lineHeight',
        'textTransform','textAlign','color'}

# --- états de l'app par écran (JS séquentiel après ouverture de la page +) ----
OPEN = "()=>document.getElementById('createBtn').click()"
CLK  = lambda k: "()=>{const t=document.querySelector('#createSheet .tile[data-kind=%s]');if(t)t.click();}" % k
SENS = "()=>{const s=document.querySelector('#csPhrase [data-ph=sens]');if(s)s.click();}"
QUI  = "()=>{const q=document.querySelector('#csPhrase [data-ph=qui]');if(q)q.click();}"
NUEE = "()=>{const nc=document.getElementById('nueeChips');if(nc){const c=[...nc.querySelectorAll('.chip')].find(x=>x.textContent.trim()&&x.textContent.trim()!=='Aucune');if(c)c.click();}}"
# Sélectionne la 2e pastille destinataire : le moodboard ph-4 illustre la 2e
# pastille sélectionnée (« Rachel »), l'app pré-sélectionne « Moi » (1re). On
# aligne l'ÉTAT pour comparer style-sélectionné à style-sélectionné (l'index
# retenu est une donnée, pas un choix de design).
SEL2 = "()=>{const os=document.querySelectorAll('#csChoix .ph-opts .ph-o');if(os.length>1){os.forEach(o=>o.classList.remove('on'));os[1].classList.add('on');}}"

# --- carte de correspondance moodboard -> app, par écran -----------------------
def cards_map():
    m=[('cartes-wrap','r.children[4]','.tiles'),
       ('cartes-flex','r.children[4].children[0]','.tiles-track')]
    kinds=['promi','nuee','draft']
    for i,k in enumerate(kinds):
        base=f'r.children[4].children[0].children[{i}]'
        m.append((f'carte{i+1}',base,f'.tile[data-kind={k}]'))
        m.append((f'carte{i+1}-nom',base+'.children[0]',f'.tile[data-kind={k}] .hname'))
        m.append((f'carte{i+1}-sous',base+'.children[1]',f'.tile[data-kind={k}] .hsub'))
    return m

def phrase_map():
    # .ph > [top(0), wordmark(1), fermer(2), phrase(3), panneau(4), barre(5)]
    P='r.children[3]'   # conteneur phrase (.big + aide)
    return [
      ('phone','r',''),
      ('zone-haut','r.children[0]','.cs-top'),
      ('wordmark','r.children[1]','.cs-mark'),
      ('fermer-mot','r.children[2].childNodes[r.children[2].childNodes.length-1]','.closeb .cb-mot') if False else ('fermer','r.children[2]','.closeb'),
      ('phrase',P+'.children[0]','#csPhrase .ph-txt'),
      ('aide',P+'.children[1]','#csPhrase .ph-hint'),
      ('panneau','r.children[4].children[0]','#planterZone'),
      ('panneau-lab','r.children[4].children[0].children[1]','#planterLab'),
      ('bouton','r.children[4].children[0].children[2]','#planterAlt'),
      ('barre-bas','r.children[5]','#csBotBar'),
      ('barre-lab','r.children[5].children[0]','#csBotBar .cbb-lab'),
    ]

def aqui_map(nchips, plus=False):
    # .ph > [top(0), wordmark(1), fermer(2), phrase(3), chooser(4), panneau(5), barre(6)]
    # chooser : children[4].children[0] > [«À QUI»(0), liste-pastilles(1)]
    # panneau : children[5].children[0] > [svg-geste(0), «glisse…»(1), «bouton»(2)]
    C='r.children[4].children[0]'; PL='r.children[5].children[0]'
    m=[('phone','r',''),('zone-haut','r.children[0]','.cs-top'),
       ('wordmark','r.children[1]','.cs-mark'),('fermer','r.children[2]','.closeb'),
       ('phrase','r.children[3].children[0]','#csPhrase .ph-txt'),
       ('aqui-lab',C+'.children[0]','#csChoix .ph-lab')]
    for i in range(nchips):
        m.append((f'pastille-{i+1}',C+f'.children[1].children[{i}]',
                  f'#csChoix .ph-opts .ph-o:nth-of-type({i+1})'))
    if plus:  # 6e pastille « + » (ajout de destinataire) — affordance absente de l'app,
              # hors périmètre de livraison → non appariée (justifiée, pas un écart).
        m.append(('pastille-plus',C+f'.children[1].children[{nchips}]',None))
    m+=[('panneau',PL,'#planterZone'),
        ('panneau-lab',PL+'.children[1]','#planterLab'),
        ('bouton',PL+'.children[2]','#planterAlt'),
        ('barre-bas','r.children[6]','#csBotBar')]
    return m

# --- FICHE (ph-6/7/8) : app-root = #detailPoster -----------------------------
# On ouvre une vraie fiche (openDetail) sur un Promi non-brouillon non-Nuée, en
# forçant son état (rate = À TENIR, tenu = TENUE) et son titre (court/long).
def FICHE(status, title, nuee=False):
    j = ("()=>{try{const ps=promises.filter(x=>!x.draft&&!x.nuee);if(!ps.length)return;"
         "const p=ps[0];p.status='"+status+"';p.who='Rachel';p.title="+repr(title)+";"
         "p.comments=[{t:'pas de presse \\u2665',d:new Date(Date.now()-9e7).toISOString(),by:'Rachel'}];")
    if nuee:
        j += "if(typeof NUE!=='undefined')NUE['famille']='Famille';p.nuee='famille';"
    else:
        j += "p.nuee=undefined;"
    j += "openDetail(p.id);}catch(e){}}"
    return j

# Mapping des nœuds moodboard de la fiche vers l'app (#detailPoster après _fichePose).
# state : 'court' | 'long' (À TENIR, geste) · 'tenue' (tracé, pas de geste).
def fiche_map(state):
    tenue = (state=='tenue')
    C='r.children[4].children[0]'   # corps > div couleur
    m=[('phone','r',''),
       ('dalle','r.children[0]','#dpTrameCv'),
       ('mot-marque','r.children[1]','#dpTete .dpt-nat'),
       ('fermer','r.children[2]','.closeb'),
       ('qui','r.children[3].children[0]','#dpTete .dpt-qui'),
       ('titre','r.children[3].children[1]','#dpTete .dpt-titre'),
       ('quand','r.children[3].children[2]','#dpTete .dpt-quand')]
    if tenue:
        m+=[('trace',C+'.children[0]','#dpTrace'),
            ('carte',C+'.children[1]','#dpMsg'),
            ('carte-head',C+'.children[1].children[0]','#dpMsg .dpm-head'),
            ('carte-msg',C+'.children[1].children[1]','#dpMsg .dpm-txt'),
            ('carte-rep',C+'.children[1].children[2]','#dpMsg .dpm-rep'),
            ('pastilles',C+'.children[2]','#dpPast'),
            ('pastille-1',C+'.children[2].children[0]','#dpPast .dp-pz:nth-of-type(1)'),
            ('pastille-2',C+'.children[2].children[1]','#dpPast .dp-pz:nth-of-type(2)'),
            ('barre','r.children[5]','#dpDetails .dpd-tog')]
    else:
        m+=[('carte',C+'.children[0]','#dpMsg'),
            ('carte-head',C+'.children[0].children[0]','#dpMsg .dpm-head'),
            ('carte-msg',C+'.children[0].children[1]','#dpMsg .dpm-txt'),
            ('carte-rep',C+'.children[0].children[2]','#dpMsg .dpm-rep'),
            ('pastilles',C+'.children[1]','#dpPast'),
            ('pastille-1',C+'.children[1].children[0]','#dpPast .dp-pz:nth-of-type(1)'),
            ('pastille-2',C+'.children[1].children[1]','#dpPast .dp-pz:nth-of-type(2)'),
            ('pastille-3',C+'.children[1].children[2]','#dpPast .dp-pz:nth-of-type(3)'),
            ('panneau','r.children[5].children[0]','#tenirZone'),
            ('panneau-lab','r.children[5].children[0].children[1]','#tenirLab'),
            ('bouton','r.children[5].children[0].children[2]','#tenirAlt'),
            ('barre','r.children[6]','#dpDetails .dpd-tog')]
    return m

ECRANS = {
 'choix': {'idx':0,'steps':[OPEN],'wait':2200,'map':[
    ('phone','r',''),
    ('zone-haut','r.children[0]','.cs-top'),
    ('dalle-1','r.children[0].children[0]','#csGrappe .cs-dalle:nth-of-type(1)'),
    ('dalle-2','r.children[0].children[1]','#csGrappe .cs-dalle:nth-of-type(2)'),
    ('dalle-3','r.children[0].children[2]','#csGrappe .cs-dalle:nth-of-type(3)'),
    ('wordmark','r.children[1]','.cs-mark'),
    ('fermer','r.children[2]','.closeb'),
    ('titre-conteneur','r.children[3]','#csQuest'),
    ('titre-texte','r.children[3].children[0]','#csQuest .cs-quest-big'),
  ]+cards_map()+[('barre-bas','r.children[5]','#csBotBar')]},
 'phrase':     {'idx':1,'steps':[OPEN,CLK('promi')],'wait':1600,'map':phrase_map()},
 'prometsmoi': {'idx':2,'steps':[OPEN,CLK('promi'),SENS],'wait':1600,'map':phrase_map()},
 'nuee':       {'idx':3,'steps':[OPEN,CLK('promi'),NUEE],'wait':1600,'map':phrase_map()},
 'aqui':       {'idx':4,'steps':[OPEN,CLK('promi'),QUI,SEL2],'wait':1400,'map':aqui_map(5,plus=True)},
 'aquinuee':   {'idx':5,'steps':[OPEN,CLK('promi'),NUEE,QUI],'wait':1400,'map':aqui_map(5)},
 'fiche-court':{'idx':6,'approot':'#detailPoster','steps':[FICHE('rate','rendre le livre',nuee=True)],'wait':2900,'map':fiche_map('court')},
 'fiche-long': {'idx':7,'approot':'#detailPoster','steps':[FICHE('rate','rapporter les photos du week-end',nuee=True)],'wait':2900,'map':fiche_map('long')},
 'fiche-tenue':{'idx':8,'approot':'#detailPoster','steps':[FICHE('tenu','rendre le livre',nuee=False)],'wait':2900,'map':fiche_map('tenue')},
}

MEAS = r"""(a)=>{const [isMb,idx,mp,props,approot]=a;
  const root = isMb ? document.querySelectorAll('.ph')[idx] : document.querySelector(approot||'#createSheet');
  const HT=function(n){var t='';for(var i=0;i<n.childNodes.length;i++){var c=n.childNodes[i];if(c.nodeType===3)t+=c.textContent;}return t.trim().length>0;};
  const rr=root.getBoundingClientRect();
  const rs=rr.width/(parseFloat(getComputedStyle(root).width)||rr.width);  // scale du châssis
  // Tout en px NON scalés (CSS px), origine = boîte de CONTENU de la racine :
  // on retire la bordure du châssis-mockup (clientLeft/Top) proprement.
  const CW=root.clientWidth, CH=root.clientHeight, CBL=root.clientLeft, CBT=root.clientTop;
  const CBR=root.offsetWidth-CW-CBL, CBB=root.offsetHeight-CH-CBT;
  const out={};
  for(const m of mp){
    let n=null;
    if(isMb){ try{n=(new Function('r','return ('+m[1]+')'))(root);}catch(e){} }
    else { n = (m[2]==='') ? root : (m[2]===null ? null : root.querySelector(m[2])); if(m[2]===null){out[m[0]]='UNMAPPED';continue;} }
    if(!n){ out[m[0]]=null; continue; }
    const c=getComputedStyle(n); const b=n.getBoundingClientRect();
    const pe=n.parentElement||root; const pb=pe.getBoundingClientRect();
    const uT=(b.top-rr.top)/rs-CBT, uL=(b.left-rr.left)/rs-CBL,
          uR=(rr.right-b.right)/rs-CBR, uB=(rr.bottom-b.bottom)/rs-CBB,
          uW=b.width/rs, uH=b.height/rs,
          pW=pe.clientWidth||1, pH=pe.clientHeight||1,
          plT=(b.top-pb.top)/rs-(pe.clientTop||0), plL=(b.left-pb.left)/rs-(pe.clientLeft||0);
    const o={ _top:uT, _bottom:uB, _left:uL, _right:uR, _w:uW, _h:uH,
              _wpct:100*uW/CW, _hpct:100*uH/CH,
              _lpp:100*plL/pW, _tpp:100*plT/pH,
              _rpp:100*(pW-plL-uW)/pW, _bpp:100*(pH-plT-uH)/pH,
              _wpp:100*uW/pW, _hpp:100*uH/pH,
              _txt:HT(n), _style: isMb ? (n.getAttribute('style')||'') : '' };
    props.forEach(p=>o[p]=c[p]);
    out[m[0]]=o;
  }
  return out;}"""

# COUVERTURE — parcourt TOUT l'arbre du .ph moodboard et liste les nœuds
# signifiants dont ni eux-mêmes ni un ancêtre ne figurent dans la map.
# « signifiant » = porte du texte direct, OU élément visible (aire>1) avec une
# classe / IMG / CANVAS / svg. On saute les entrailles svg (path, circle…) et BR.
# Règle de couverture : un nœud est couvert si lui ou un ancêtre est mappé —
# ainsi mapper le bloc-phrase couvre ses <span> internes (les deux DOM diffèrent).
COVERAGE = r"""(a)=>{const [idx,mp]=a;
  const root=document.querySelectorAll('.ph')[idx];
  (function st(n,p){n.__p=p;let i=0;for(const c of n.children){st(c,p?p+'/'+i:''+i);i++;}})(root,'');
  const HT=function(n){var t='';for(var i=0;i<n.childNodes.length;i++){var c=n.childNodes[i];if(c.nodeType===3)t+=c.textContent;}return t.trim();};
  const SKIP={PATH:1,CIRCLE:1,LINE:1,G:1,RECT:1,POLYGON:1,POLYLINE:1,ELLIPSE:1,DEFS:1,BR:1,STOP:1,LINEARGRADIENT:1,RADIALGRADIENT:1,CLIPPATH:1,MASK:1,USE:1,TITLE:1};
  const mapped=new Set();
  for(const m of mp){ if(!m[1])continue; let n=null; try{n=(new Function('r','return ('+m[1]+')'))(root);}catch(e){} if(n&&n.__p!==undefined)mapped.add(n.__p);}
  function covered(n){let x=n;while(x&&x!==root){if(mapped.has(x.__p))return true;x=x.parentElement;}return false;}
  const out=[];
  (function walk(n){
    const tag=(n.tagName||'').toUpperCase();
    if(!SKIP[tag]){
      const r=n.getBoundingClientRect(); const txt=HT(n).slice(0,30);
      const cls=(typeof n.className==='string'?n.className:'');
      const meaning=(txt.length>0)||(r.width>1&&r.height>1&&(cls||tag==='IMG'||tag==='CANVAS'||tag==='SVG'));
      if(meaning && n!==root && !covered(n)) out.push({p:n.__p,tag:tag,cls:cls,txt:txt});
    }
    for(const c of n.children) walk(c);
  })(root);
  return out;}"""

def rgb(s):
    m=re.findall(r'[\d.]+', s or '')
    if len(m)>=3:
        return (float(m[0]),float(m[1]),float(m[2]), float(m[3]) if len(m)>3 else 1.0)
    return None
def px(s):
    m=re.match(r'^(-?[\d.]+)px$', (s or '').strip())
    return float(m.group(1)) if m else None

def cmp_num(mv, av, tol, unit, label=''):
    if mv is None or av is None: return None
    d=abs(mv-av)
    if d<tol: return None
    return (d, f"{round(mv,1)}{unit}→{round(av,1)}{unit}  Δ{round(d,1)}{unit}")

def cmp_prop(prop, mv, av):
    if mv==av: return None
    if mv is None and av is None: return None
    if prop=='textAlign':   # start==left, end==right en LTR
        norm={'start':'left','end':'right'}
        if norm.get(mv,mv)==norm.get(av,av): return None
    if prop=='fontFamily':
        f=lambda s:(s or '').split(',')[0].strip().strip('"\'').lower()
        return (3, f"{mv} → {av}") if f(mv)!=f(av) else None
    if prop=='opacity':
        try:
            d=abs(float(mv)-float(av)); return (d*100, f"{mv}→{av} Δ{round(d,3)}") if d>=0.02 else None
        except: return None
    if 'olor' in prop or prop=='boxShadow':
        cm,ca=rgb(mv),rgb(av)
        if cm and ca:
            dch=max(abs(cm[0]-ca[0]),abs(cm[1]-ca[1]),abs(cm[2]-ca[2])); da=abs(cm[3]-ca[3])
            sc=dch/2.55+da*100
            return (sc, f"{mv} → {av}  Δ{round(dch)}/255 α{round(da,2)}") if sc>=2 else None
        return (5, f"{mv} → {av}") if mv!=av else None
    pm,pa=px(mv),px(av)
    if pm is not None and pa is not None:
        d=abs(pm-pa); return (d, f"{mv}→{av} Δ{round(d,2)}px") if d>=1 else None
    return (3, f"{mv} → {av}") if str(mv)!=str(av) else None

# ── HOMOTHÉTIE 352→390 ────────────────────────────────────────────────────────
# Le moodboard est dessiné pour .ph de 352 px de large (762 de haut) ; l'app fait
# 390×844. 390/352 = 844/762 = 1,108 : homothétie EXACTE. Copier les valeurs
# absolues telles quelles donne un écran 11 % trop petit. Donc on MULTIPLIE chaque
# valeur absolue du moodboard (px : tailles, paddings, marges, rayons, hauteurs,
# positions) par ce facteur, puis on compare à l'app. Les POURCENTAGES restent des
# pourcentages (déjà proportionnels). Comparer ainsi ⟺ valeur_app/390 = valeur_mb/352.
F = 390/352   # 1.10795…
def scale_mb(mb):
    for label,d in (mb or {}).items():
        if not isinstance(d,dict): continue
        for k in ('_top','_bottom','_left','_right','_w','_h'):
            if isinstance(d.get(k),(int,float)): d[k]=d[k]*F
        for k in list(d.keys()):
            v=d.get(k)
            if isinstance(v,str):
                m=re.match(r'^(-?[\d.]+)px$', v.strip())
                if m: d[k]=('%g'%(float(m.group(1))*F))+'px'
    return mb

# EXCLUSIONS justifiées (visibles, discutables) :
EX_BASE  = "base 352↔390 : %-dérivé d'un absolu (padding/flex) — l'absolu colle, le relatif reste relatif"
EX_DALLE = "dalle : hauteur = aspect moteur (une dalle ne se déforme jamais) ; positions & largeurs du fichier respectées"
EX_ROOT  = "auto-référence de la racine (le nœud .ph comparé à lui-même)"
# Écran « à qui » : les POSITIONS (x/y) du label et des pastilles dépendent du
# CONTENU, pas du CSS. (1) noms d'exemple + nombre différents (moodboard
# Moi/Rachel/Nico/Adrien/Maman/+ ; app Moi/Maman/Nico/Léa/Adrien) → le wrap se
# replie autrement. (2) la phrase du moodboard est une promesse REMPLIE (3 lignes) ;
# le flux synthétique laisse les créneaux objet vides (4 lignes) → la phrase est
# plus haute, donc le chooser descend d'autant. Le CONTENEUR flex (gap, wrap), le
# BOX des pastilles (padding, radius, hauteur), leur STYLE (couleurs, poids,
# line-height, sélection) et la position du PANNEAU sont, eux, vérifiés et alignés.
EX_AQUI  = ("position 'à qui' pilotée par le contenu (noms d'exemple + nombre "
            "différents → wrap ; phrase moodboard remplie 3 lignes vs créneaux vides "
            "4 lignes → hauteur) ; style, box et conteneur des pastilles vérifiés")

def geo_gaps(label, m, a):
    g=[]; st=(m.get('_style','') or '').replace(' ','')
    isdalle = label.startswith('dalle'); isroot = (label=='phone')
    isaqui = label.startswith('pastille') or label=='aqui-lab'  # positions = contenu
    expos = EX_AQUI if isaqui else (EX_ROOT if isroot else None)
    # VERTICAL — % explicite dans le fichier => RÉEL (% du parent) ; sinon bord ANCRÉ px
    if re.search(r'top:-?\d+%', st):
        r=cmp_num(m['_tpp'],a['_tpp'],0.6,'%');  g.append((r[0]*2,label,'top%',r[1],expos)) if r else None
    elif re.search(r'bottom:-?\d+%', st):
        r=cmp_num(m['_bpp'],a['_bpp'],0.6,'%');  g.append((r[0]*2,label,'bottom%',r[1],expos)) if r else None
    else:
        gt=cmp_num(m['_top'],a['_top'],1,'px'); gb=cmp_num(m['_bottom'],a['_bottom'],1,'px')
        if gt is not None and gb is not None:
            best=gt if gt[0]<=gb[0] else gb; side='top' if gt[0]<=gb[0] else 'bottom'
            g.append((best[0],label,'pos-'+side,best[1],expos))
    # HORIZONTAL
    if re.search(r'left:-?\d+%', st):
        r=cmp_num(m['_lpp'],a['_lpp'],0.6,'%');  g.append((r[0]*2,label,'left%',r[1],expos)) if r else None
    elif re.search(r'right:-?\d+%', st):
        r=cmp_num(m['_rpp'],a['_rpp'],0.6,'%');  g.append((r[0]*2,label,'right%',r[1],expos)) if r else None
    else:
        gl=cmp_num(m['_left'],a['_left'],1,'px'); gr=cmp_num(m['_right'],a['_right'],1,'px')
        if gl is not None and gr is not None:
            best=gl if gl[0]<=gr[0] else gr; side='left' if gl[0]<=gr[0] else 'right'
            g.append((best[0],label,'pos-'+side,best[1],expos))
    # LARGEUR — px|% explicite => RÉEL ; auto (fill/texte) => EXCLU base ; texte auto ignoré
    auto_txt = bool(m.get('_txt')) and not re.search(r'width:', st)
    if re.search(r'width:-?\d+px', st):
        r=cmp_num(m['_w'],a['_w'],1,'px');   g.append((r[0],label,'largeur',r[1],None)) if r else None
    elif re.search(r'width:-?\d+%', st):
        r=cmp_num(m['_wpp'],a['_wpp'],0.6,'%'); g.append((r[0]*2,label,'largeur%',r[1],None)) if r else None
    elif not auto_txt:
        # largeur auto/fill : on compare en % de la RACINE (homothétie app/390 = mb/352),
        # pas du parent — les hiérarchies de wrappers diffèrent (même largeur visuelle).
        r=cmp_num(m['_wpct'],a['_wpct'],0.8,'%'); g.append((r[0]*2,label,'largeur%',r[1],None)) if r else None
    # HAUTEUR — px explicite => RÉEL ; dalle => EXCLU dalle (aspect) ; sinon % racine
    if re.search(r'height:-?\d+px', st):
        r=cmp_num(m['_h'],a['_h'],1,'px');   g.append((r[0],label,'hauteur',r[1],None)) if r else None
    else:
        r=cmp_num(m['_hpct'],a['_hpct'],0.8,'%')
        if r: g.append((r[0]*2,label,'hauteur%',r[1], EX_DALLE if isdalle else None))
    return g

def run(name):
    E=ECRANS[name]; MP=E['map']
    with sync_playwright() as p:
        b=p.chromium.launch()
        pg=b.new_page(viewport={'width':1280,'height':2600}); pg.goto('file://'+MB); pg.wait_for_timeout(3500)
        mb=pg.evaluate(MEAS,[True,E['idx'],MP,PROPS]); mb=scale_mb(mb)
        cover=pg.evaluate(COVERAGE,[E['idx'],MP]); pg.close()
        pa=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); pa.goto('file://'+APP); pa.wait_for_timeout(7000)
        pa.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pa.evaluate("()=>document.querySelectorAll('.frame,.device').forEach(e=>e.classList.add('light'))")
        for i,step in enumerate(E['steps']):
            pa.evaluate(step); pa.wait_for_timeout(900 if i<len(E['steps'])-1 else E['wait'])
        app=pa.evaluate(MEAS,[False,E['idx'],MP,PROPS,E.get('approot','#createSheet')]); b.close()
    EX_FONT="repli de maquette : police non chargée dans le fichier (l'app garde Fraunces/Apfel, ses vraies polices)"
    FALLBACKS={'georgia','-apple-system','apple-system','system-ui','ui-sans-serif','times','serif','sans-serif'}
    reels=[]; exclus=[]; unmapped=[]; missing=[]
    # Écrans « à qui » (chooser ouvert) : le remplissage bug-a fixe la position par un
    # défilement ÉPINGLÉ dont le clamp cale le panneau pile au-dessus de la barre ; il
    # reste alors ~1,4 px d'arrondi sur la position de la phrase (phrase et panneau sont
    # rigidement liés dans le même formulaire). Sous 3 px, c'est ce résidu de scroll —
    # même mécanisme que la marge du panneau, déjà exclue. Le panneau, lui, est à zéro.
    EX_SCROLL=("résidu d'arrondi du défilement épinglé (remplissage bug-a) : phrase et "
               "panneau liés dans le formulaire ; le clamp cale le panneau à zéro, la "
               "phrase garde ~1,4 px — même mécanisme que la marge du panneau, déjà exclue")
    _choos = name in ('aqui','aquinuee')
    # BITONAL (CLAUDE.md §3) — la fiche a deux tons : haut couleur d'état pleine
    # (mot-marque, FERMER : blanc, comme le moodboard), corps CLAIR (contenu en
    # encre). Le moodboard pose le corps en blanc sur couleur pleine ; l'app le
    # pose en encre sur corps clair — patron de ph-8 étendu à tous les états.
    # Donc : (1) le fond racine (corps clair) diffère du moodboard (couleur pleine)
    # sur les 3 fiches ; (2) sur À TENIR (ph-6/7) les COULEURS du corps (texte, fond
    # carte, filets, contour pastilles, panneau) sont en encre vs blanc au moodboard.
    # Sur TENUE (ph-8) le moodboard est DÉJÀ en encre → aucune exclusion, ça doit
    # correspondre. C'est la SEULE exclusion « moodboard à la lettre » de la fiche.
    EX_BITON=("bitonal de fiche (CLAUDE.md §3) : corps CLAIR + contenu en encre "
              "(patron ph-8) ; le moodboard pose le corps en blanc sur couleur pleine. "
              "Seule exclusion — haut (mot-marque, FERMER) et toutes les tailles/structure à zéro")
    _fiche  = name.startswith('fiche')
    _atenir = name in ('fiche-court','fiche-long')
    CORPS = {'qui','titre','quand','carte','carte-head','carte-msg','carte-rep',
             'pastilles','pastille-1','pastille-2','pastille-3',
             'panneau','panneau-lab','bouton','barre','trace','barre-lab'}
    def biton(label,prop):
        if not _fiche: return False
        colorish = ('olor' in prop) or prop=='boxShadow'
        if not colorish: return False
        if prop=='backgroundColor' and label=='phone': return True   # fond racine = corps clair
        if _atenir and label in CORPS: return True                   # texte/fond corps encre vs blanc
        return False
    EX_BOUTON=("pastille « bouton » remontée : le moodboard (v592) la pose top:12 sur un "
               "panneau de 176px, mais le vrai panneau fait 118px (×1,108 = 131px) où elle "
               "CHEVAUCHERAIT le cercle de droite — repositionnée pour ne jamais le toucher")
    EX_PEAUF=("Peaufiner FIXE (demandé) : la fiche devient un CONTENEUR DE DÉFILEMENT "
              "(display:block, overflow auto) au lieu du flex statique du moodboard — la barre "
              "Peaufiner glisse avec le contenu et se colle en haut, les réglages vivent dessous. "
              "Le moodboard est une maquette figée, sans défilement ; structure/tailles à zéro")
    EX_FLECHES=("bascule « inverser le sens » remplacée par DEUX PETITES FLÈCHES (demandé, "
                "point 6) : le nœud 'bouton' n'est plus une pastille-texte arrondie mais une "
                "icône chevron (pas de texte, pas de padding, pas de pilule) — forme et texte "
                "diffèrent forcément ; position/pilotage vérifiés")
    # props de forme/texte du 'bouton' devenues sans objet avec les flèches
    FLECHE_PROPS={'borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius',
                  'borderBottomRightRadius','paddingLeft','paddingRight','paddingTop',
                  'paddingBottom','fontSize','boxShadow','lineHeight','textAlign','display'}
    EX_STICK=("barre Peaufiner FIXE (demandé) sur la page + : elle passe DANS le scroller et "
              "devient OPAQUE (fond = couleur de nature, identique au repos) pour que le contenu "
              "ne transparaisse pas quand elle se colle en haut ; sur l'écran « à qui » (plus haut) "
              "elle glisse naturellement sous le pli — d'où le décalage de position. Rien ne recouvre")
    def push(t):
        sc,label,prop,txt,excl=t
        # bouton : position corrigée d'après la v592 (erreur du moodboard à 131px).
        if excl is None and label=='bouton' and prop.startswith('pos-'):
            excl=EX_BOUTON; t=(sc,label,prop,txt,excl)
        # à-qui : la phrase du moodboard est une promesse REMPLIE (3 lignes) ; le flux
        # synthétique laisse les créneaux objet VIDES (4 lignes) → phrase plus haute.
        # Sa HAUTEUR relève du contenu, pas de l'homothétie (comme les pastilles).
        if excl is None and _choos and label=='phrase' and prop=='hauteur%':
            excl=EX_AQUI; t=(sc,label,prop,txt,excl)
        if excl is None and _choos and label=='phrase' and prop.startswith('pos-') and sc<3:
            excl=EX_SCROLL; t=(sc,label,prop,txt,excl)
        if excl is None and biton(label,prop):
            excl=EX_BITON; t=(sc,label,prop,txt,excl)
        # Peaufiner FIXE : la fiche est un conteneur de défilement (block), pas le flex du moodboard.
        if excl is None and _fiche and label=='phone' and prop=='display':
            excl=EX_PEAUF; t=(sc,label,prop,txt,excl)
        # bascule → deux flèches (point 6) : forme/texte du 'bouton' sans objet.
        if excl is None and label=='bouton' and prop in FLECHE_PROPS:
            excl=EX_FLECHES; t=(sc,label,prop,txt,excl)
        # barre Peaufiner FIXE opaque, dans le scroller (page +) : couleur/position.
        if excl is None and label in ('barre-bas','barre-lab') and prop in ('backgroundColor','color','pos-bottom','pos-top'):
            excl=EX_STICK; t=(sc,label,prop,txt,excl)
        # écran « à qui » : le geste (panneau) glisse avec la barre sous le pli.
        if excl is None and _choos and label in ('panneau','panneau-lab') and prop=='pos-bottom':
            excl=EX_STICK; t=(sc,label,prop,txt,excl)
        (exclus if t[4] else reels).append(t)
    for label,mbexpr,appsel in MP:
        m=mb.get(label); a=app.get(label)
        if appsel is None: unmapped.append(label); continue
        if m is None: missing.append((label,'nœud moodboard introuvable')); continue
        if a is None or a=='UNMAPPED': missing.append((label,f"app '{appsel}' introuvable")); continue
        for t in geo_gaps(label,m,a): push(t)
        hastxt=bool(m.get('_txt')) or bool(a.get('_txt'))
        skipmock = ['borderTopLeftRadius','borderTopWidth'] if label=='phone' else []  # châssis-mockup
        for prop in PROPS:
            if prop in skipmock: continue
            if prop in TYPO and not hastxt: continue
            r=cmp_prop(prop, m.get(prop), a.get(prop))
            if not r: continue
            excl=None
            if prop=='fontFamily':
                f=(m.get(prop) or '').split(',')[0].strip().strip('"\'').lower()
                if f in FALLBACKS: excl=EX_FONT
            # bug (a) : le panneau est ancré en bas par margin-top:auto (mécanisme
            # de remplissage), là où le moodboard utilise flex:1 sur la phrase.
            if label=='panneau' and prop in ('marginTop','marginBottom'):
                excl="mécanisme de remplissage (bug a) : margin-top:auto ancre le panneau en bas (le moodboard le fait via flex:1 sur la phrase)"
            push((r[0],label,prop,r[1],excl))
    reels.sort(key=lambda x:-x[0]); exclus.sort(key=lambda x:-x[0])
    print("="*76); print(f"  RELEVÉ MOODBOARD — « {name} » (ph-{E['idx']})"); print("="*76)
    print(f"  {len(MP)} nœuds mappés · {len(unmapped)} non appariés · {len(missing)} manquants")
    print(f"\n  ── ÉCARTS RÉELS ({len(reels)}) — objectif ZÉRO ──")
    if not reels: print("     ✅ ZÉRO ÉCART RÉEL")
    for sc,label,prop,txt,_ in reels:
        print(f"     [{sc:6.1f}] {label:<16} {prop:<14} {txt}")
    print(f"\n  ── EXCLUSIONS JUSTIFIÉES ({len(exclus)}) — à relire ──")
    seen=set()
    for sc,label,prop,txt,excl in exclus:
        tag=excl.split(':')[0].split('(')[0].strip()
        print(f"     [{tag:<7}] {label:<16} {prop:<14} {txt}")
        seen.add(excl)
    for e in sorted(seen): print(f"       → « {e} »")
    if unmapped: print("\n  NON APPARIÉS (map sans sélecteur app) :"); [print("   •",u) for u in unmapped]
    if missing: print("\n  MANQUANTS :"); [print("   •",l,'—',w) for l,w in missing]
    if cover:
        print(f"\n  ── NŒUDS MOODBOARD NON COUVERTS ({len(cover)}) — à mapper ──")
        for c in cover:
            print(f"     [{c['p']:<10}] {c['tag']:<6} .{c['cls']:<24} «{c['txt']}»")
    print()
    return len(reels)+len(cover)

if __name__=='__main__':
    which=sys.argv[1] if len(sys.argv)>1 else 'choix'
    order=['choix','phrase','prometsmoi','nuee','aqui','aquinuee','fiche-court','fiche-long','fiche-tenue']
    names=order if which=='all' else [which]
    total=sum(run(n) for n in names)
    sys.exit(0 if total==0 else 1)
